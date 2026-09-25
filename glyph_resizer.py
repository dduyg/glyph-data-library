"""
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
  ██╗  ██╗ 🪜  【═══ ＧＬＹＰＨ　ＲＥＳＩＺＥＲ ═══】   🪜       ██╗  ██╗
  ╚██╗██╔╝       runtime > 𝒈𝒍𝒚𝒑𝒉-𝒓𝒆𝒔𝒊𝒛𝒆.𝒚𝒎𝒍 · ᵒᵛᵉʳʷʳⁱᵗᵉˢ ⁱⁿ ˢᵒᵘʳᶜᵉ ᶠᵒˡᵈᵉʳ   ╚██╗██╔╝ 
    ╚███╔╝                                                     ╚███╔╝ 
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
  Author: Duygu Dağdelen, 2026-09-23
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
"""
import os, sys, html
from base64 import b64encode, b64decode
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from io import BytesIO

from PIL import Image
from github import Github, Auth, GithubException, InputGitTreeElement

SUPPORTED_FORMATS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff", ".tif"}
BAR = "█" * 80
DONE_BAR = "▰" * 49


BANNER = [
    BAR,
    "██ GLYPH RESIZER 🪜 ⿻ グリフリサイザ   ⛶                                                     ██",
    "██ batch resize image pipeline ▸▸ width locked @ {width_px:<6}                                      ██",
    BAR,
    "██ [SYS.STATUS] ACTIVE                                                                      ██",
    BAR,
]

# ---------------------- CONFIG ----------------------

@dataclass
class Source:
    owner: str
    repo: str
    branch: str | None = None
    folder: str = ""

    @property
    def full(self):
        return f"{self.owner}/{self.repo}"

    def __str__(self):
        return f"{self.repo}:{self.folder or '(root)'}@{self.branch or '(default)'}"


def fail(msg):
    print(f"\n    ⊘ [ERR] {msg}")
    print(f"::error::{msg}")
    sys.exit(1)


def env(name, default=""):
    val = (os.environ.get(name) or "").strip()
    return val if val else default


def env_bool(name, default):
    val = env(name).lower()
    return default if not val else val in ("1", "true", "yes", "y", "on")


def gh_msg(e):
    return e.data.get("message", "Unknown error") if isinstance(e.data, dict) else str(e.data)


def parse_sources(raw, owner):
    """repo-name:folder[@branch], comma/newline-separated — repos on your account"""
    sources = []
    for spec in [x.strip() for x in raw.replace("\n", ",").split(",") if x.strip()]:
        body, branch = spec, None
        if "@" in body:
            body, branch = body.rsplit("@", 1)
            branch = branch.strip() or None
        repo, _, folder = body.partition(":")
        repo = repo.strip()
        if not repo or "/" in repo:
            fail(f"Source '{spec}' must be repo-name:folder (repos on your account, no owner prefix)")
        sources.append(Source(owner, repo, branch, folder.strip().strip("/")))
    if not sources:
        fail("GLYPH_SOURCES is empty — e.g. 'sketches:exports/png'")
    return sources


def resolve_owner(g):
    try:
        return g.get_user().login
    except GithubException:
        owner = env("GITHUB_REPOSITORY_OWNER")
        if not owner:
            fail("Could not determine your GitHub username")
        return owner

# ---------------------- RESIZE ----------------------

def match_folder(tree_elements, folder, exts):
    """
    Find image blobs directly inside `folder` (non-recursive).
    → (resolved_folder, items, hint)
    Falls back to a case-insensitive match (qwe4 ↔ QWE4); if still nothing,
    the hint lists which folders in the repo DO contain images.
    """
    def parent(p):
        return p.rsplit("/", 1)[0] if "/" in p else ""

    imgs = [el for el in tree_elements
            if el.type == "blob" and os.path.splitext(el.path)[1].lower() in exts]
    exact = [el for el in imgs if parent(el.path) == folder]
    if exact:
        return folder, exact, None

    ci = [el for el in imgs if parent(el.path).lower() == folder.lower()]
    if ci:
        real = parent(ci[0].path)
        ci = [el for el in ci if parent(el.path) == real]
        return real, ci, f"folder '{folder}' matched '{real}' (letter case differs)"

    counts = Counter(parent(el.path) or "(root)" for el in imgs)
    if counts:
        found = ", ".join(f"'{f}' ({n})" for f, n in counts.most_common(8))
        return folder, [], f"no {'/'.join(sorted(exts))} files directly in '{folder or '(root)'}' — folders that have them: {found}"
    return folder, [], f"no {'/'.join(sorted(exts))} files anywhere in this repo on this branch"


def resize_image(raw, width):
    """
    → (png_bytes, (w0, h0), (w1, h1))   or   None when already a PNG at target width.
    Aspect ratio preserved; RGBA keeps transparency for the glyph pipeline mask.
    """
    img = Image.open(BytesIO(raw))
    img.load()
    w0, h0 = img.size
    if w0 == width and img.format == "PNG":
        return None
    img = img.convert("RGBA")
    h1 = max(1, round(width * h0 / w0))
    img = img.resize((width, h1), Image.LANCZOS)
    buf = BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue(), (w0, h0), (width, h1)


def list_folder_images(repo, branch, folder):
    tree = repo.get_git_tree(repo.get_branch(branch).commit.sha, recursive=True)
    if tree.raw_data.get("truncated"):
        print(f"    ⚠ tree listing of {repo.full_name} truncated — some files may be missing")
    return match_folder(tree.tree, folder, SUPPORTED_FORMATS)


def process_source(g, src, width, remove_originals):
    """Resize every image in one folder and overwrite it there in a single commit"""
    stats = {"source": str(src), "resized": 0, "unchanged": 0, "skipped": [], "commit": None}

    try:
        repo = g.get_repo(src.full)
        src.branch = src.branch or repo.default_branch
        src.folder, items, hint = list_folder_images(repo, src.branch, src.folder)
    except GithubException as e:
        stats["skipped"].append(f"SOURCE_UNREACHABLE ({e.status} {gh_msg(e)})")
        print(f"    ⊘ {src}: unreachable — {e.status} {gh_msg(e)}")
        return stats

    print(f"\n    ◢◣ {src}  ⟨{len(items)} images⟩")
    if hint:
        print(f"      ⚠ {hint}")
        print(f"::warning::{src.repo}: {hint}")
    if not items:
        stats["skipped"].append(f"EMPTY_SOURCE — {hint}")
        return stats
    existing_paths = {el.path for el in items}

    def work(el):
        raw = b64decode(repo.get_git_blob(el.sha).content)
        return el, resize_image(raw, width)

    elements = []
    with ThreadPoolExecutor(max_workers=10) as ex:
        futures = {ex.submit(work, el): el for el in items}
        for fut in as_completed(futures):
            el = futures[fut]
            name = el.path.rsplit("/", 1)[-1]
            try:
                _, result = fut.result()
            except Exception as e:
                stats["skipped"].append(f"{name} ({e})")
                continue
            if result is None:
                stats["unchanged"] += 1
                continue

            png_bytes, (w0, h0), (w1, h1) = result
            out_path = os.path.splitext(el.path)[0] + ".png"
            is_png = el.path.lower().endswith(".png")

            # glyph.jpg next to an existing glyph.png → don't clobber the PNG
            if not is_png and out_path in existing_paths:
                stats["skipped"].append(f"{name} (NAME_COLLISION with {out_path.rsplit('/', 1)[-1]})")
                continue

            blob = repo.create_git_blob(b64encode(png_bytes).decode("utf-8"), "base64")
            elements.append(InputGitTreeElement(path=out_path, mode="100644", type="blob", sha=blob.sha))
            if not is_png and remove_originals:
                elements.append(InputGitTreeElement(path=el.path, mode="100644", type="blob", sha=None))
            stats["resized"] += 1
            print(f"      ◆ {name}  {w0}×{h0} → {w1}×{h1}")

    if not elements:
        print("      ─ nothing to change")
        return stats

    try:
        ref = repo.get_git_ref(f"heads/{src.branch}")
        head = repo.get_git_commit(ref.object.sha)
        tree = repo.create_git_tree(elements, head.tree)
        msg = f"⟨glyph-push⟩ {stats['resized']} images ◆ {width}px ◆ {datetime.now(timezone.utc).strftime('%Y.%m.%d-%H:%M')}"
        if env("GITHUB_RUN_ID"):
            msg += f"\n\nworkflow run: {env('GITHUB_SERVER_URL', 'https://github.com')}/{env('GITHUB_REPOSITORY')}/actions/runs/{env('GITHUB_RUN_ID')}"
        commit = repo.create_git_commit(msg, tree, [head])
        ref.edit(commit.sha)
        stats["commit"] = f"https://github.com/{src.full}/commit/{commit.sha}"
    except GithubException as e:
        stats["skipped"].append(f"COMMIT_FAILED ({e.status} {gh_msg(e)})")
        stats["resized"] = 0
    return stats

# ---------------------- ENTRYPOINT ----------------------

def main():
    token = env("GH_TOKEN")
    if not token:
        fail("No token found. Add a GLYPH_PAT repository secret.")
    try:
        width = int(env("GLYPH_TARGET_WIDTH", "900"))
    except ValueError:
        fail("GLYPH_TARGET_WIDTH must be an integer")
    if width < 1:
        fail("GLYPH_TARGET_WIDTH must be > 0")
    remove_originals = env_bool("GLYPH_REMOVE_ORIGINALS", True)

    banner = [line.format(width_px=f"{width}px") for line in BANNER]
    print("\n".join(banner) + "\n")

    g = Github(auth=Auth.Token(token))
    owner = resolve_owner(g)
    sources = parse_sources(env("GLYPH_SOURCES"), owner)

    print(f"\n    ⟨◆⟩ account: {owner}")
    print(f"    ├─ width: {width}px  (ratio preserved)")
    print(f"    ├─ remove.originals: {remove_originals}")
    print(f"    └─ sources: {', '.join(str(s) for s in sources)}")

    results = [process_source(g, s, width, remove_originals) for s in sources]

    # ---------- console summary ----------
    lines = [DONE_BAR, "  ⟨⟨ TRANSMISSION.COMPLETE ⟩⟩", DONE_BAR]
    hard_fail = False
    for r in results:
        lines += [
            "",
            f"    ◆ resized: {r['resized']}",
            f"    ⊘ unchanged: {r['unchanged']}",
            f"    ⊘ skipped: {len(r['skipped'])}",
        ]
        for msg in r["skipped"]:
            lines.append(f"    │   ⊘ {msg}")
            if msg.startswith(("SOURCE_UNREACHABLE", "EMPTY_SOURCE", "COMMIT_FAILED")):
                hard_fail = True
        lines += [
            f"    ├─ source: {r['source']}",
            f"    └─ commit: {r['commit'] or '— (nothing to change)'}",
        ]
    lines += ["", "▓" * 80]

    print("\n" + "\n".join(lines))

    def to_html(line):
        out = html.escape(line, quote=False)
        for r in results:
            if r["commit"] and r["commit"] in line:
                out = out.replace(r["commit"], f'<a href="{r["commit"]}">{r["commit"]}</a>')
        return out

    pre = [html.escape(l, quote=False) for l in banner] + [""] + [to_html(l) for l in lines]
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if path:
        with open(path, "a", encoding="utf-8") as fh:
            fh.write("\n".join(["### ▓▓▓ PROCESS.SUMMARY ⟫⟫⟫", "", "<pre>" + "\n".join(pre) + "</pre>"]) + "\n")

    # Stop the chained glyph pipeline if a source couldn't be read or written
    if hard_fail:
        fail("One or more sources failed — glyph pipeline will not run")

if __name__ == "__main__":
    main()
