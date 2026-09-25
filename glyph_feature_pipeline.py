"""
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
█  💠 𝐆𝐋𝐘𝐏𝐇 𝐅𝐄𝐀𝐓𝐔𝐑𝐄 𝐏𝐈𝐏𝐄𝐋𝐈𝐍𝐄 ⟫⟫⟫
█     [Automated extraction, analysis & storage of glyphs with detailed data features]
█ ─────────────────────────────────────────────────────────────────────────────
█ M.01 > K-MEANS.COLOR.CLUSTERING
█        Dominant/secondary palette extraction
█ M.02 > QUANTITATIVE.VISUAL.METRICS
█        Edge density | Entropy | Texture | Contrast | Shape analysis
█ M.03 > MOOD.CLASSIFICATION
█        Color harmony evaluation & aesthetic profiling
█ M.04 > LIBRARY.EXPANDED
█        Incremental updates stored in JSON and CSV for continuous library expansion
█ M.05 > AUTO.STORAGE
█        Runtime > via GH Actions (images → glyphs/, data → data/)
█ ─────────────────────────────────────────────────────────────────────────────
█  >> SYS.AUTHOR: Duygu Dağdelen  [INIT 2026-09-23] 
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
"""
import os, sys, json, uuid, csv, traceback, colorsys, html
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime, timezone
from base64 import b64encode, b64decode
from concurrent.futures import ThreadPoolExecutor, as_completed
from io import BytesIO, StringIO

import numpy as np
import cv2
from PIL import Image
from sklearn.cluster import KMeans
from skimage.measure import shannon_entropy
from skimage.feature import local_binary_pattern
from skimage.color import rgb2gray
from github import Github as GH, Auth, GithubException as GhException, InputGitTreeElement

CATALOG_JSON = "data/glyphs.catalog.json"
CATALOG_CSV = "data/glyphs.catalog.csv"
BAR = "▓" * 79
BANNER = [
    BAR,
    "     ├─ ⌬ 𝐆𝐋𝐘𝐏𝐇 𝐅𝐄𝐀𝐓𝐔𝐑𝐄 𝐏𝐈𝐏𝐄𝐋𝐈𝐍𝐄    ⟩⟩⟩      SYS.ACTIVE",
    "     └──── [extract] → [analyze] → [classify] → [commit]",
    BAR,
]

# ---------------------- RUNTIME CONFIG ----------------------

@dataclass
class Source:
    owner: str
    repo: str
    branch: str | None = None  # None → the repo's default branch
    folder: str = ""

    @property
    def full(self):
        return f"{self.owner}/{self.repo}"

    def __str__(self):
        return f"{self.full}@{self.branch or '(default)'}/{self.folder or '(root)'}"


@dataclass
class Config:
    token: str
    owner: str
    storage_user: str
    storage_repo: str
    storage_branch: str = "main"
    sources: list = field(default_factory=list)
    clear_source: bool = False
    max_workers: int = 10
    k: int = 3
    min_cluster_fraction: float = 0.05

    @property
    def storage_full(self):
        return f"{self.storage_user}/{self.storage_repo}"


def fail(msg):
    print(f"\n  ⊗ [ERR] {msg}")
    print(f"::error::{msg}")  # annotation in the Actions UI
    sys.exit(1)


def env(name, default=""):
    val = (os.environ.get(name) or "").strip()
    return val if val else default


def env_bool(name, default=False):
    val = env(name).lower()
    return default if not val else val in ("1", "true", "yes", "y", "on")


def env_num(name, default, cast):
    raw = env(name, str(default))
    try:
        return cast(raw)
    except ValueError:
        fail(f"{name} must be a {cast.__name__}, got '{raw}'")


def split_repo(text, default_owner, label):
    """'repo-name' → (your account, repo-name) · 'owner/repo-name' → as given"""
    parts = [p.strip() for p in text.strip().strip("/").split("/")]
    if len(parts) == 1 and parts[0]:
        return default_owner, parts[0]
    if len(parts) == 2 and all(parts):
        return parts[0], parts[1]
    fail(f"{label} must be 'repo-name' or 'owner/repo-name' (got '{text}')")


def parse_sources(raw, owner):
    """
    Comma/newline-separated list of   repo-name:folder   (repos on your account)
      sketches:exports/png          → <you>/sketches, folder exports/png, default branch
      scratchpad                    → <you>/scratchpad, repo root
      old-glyphs:pending@develop    → optional @branch
    """
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
        return g.get_user().login          # works with a PAT
    except GhException:
        owner = env("GITHUB_REPOSITORY_OWNER")  # github.token can't call /user
        if not owner:
            fail("Could not determine your GitHub username")
        return owner


def resolve_config():
    token = env("GH_TOKEN") or env("GITHUB_TOKEN")
    if not token:
        fail("No token found. Add a GLYPH_PAT repository secret (see workflow file).")
    g = GH(auth=Auth.Token(token))
    owner = resolve_owner(g)

    # Storage is always the repo this workflow runs in → glyphs/ + data/
    storage = env("GITHUB_REPOSITORY")
    if not storage:
        fail("GITHUB_REPOSITORY is not set — run this script from GitHub Actions")
    storage_user, storage_repo = split_repo(storage, owner, "GITHUB_REPOSITORY")

    cfg = Config(
        token=token,
        owner=owner,
        storage_user=storage_user,
        storage_repo=storage_repo,
        storage_branch=env("GITHUB_REF_NAME", "main"),
        clear_source=env_bool("GLYPH_CLEAR_SOURCE"),
        max_workers=max(1, env_num("GLYPH_MAX_WORKERS", 10, int)),
        k=max(2, env_num("GLYPH_KMEANS_K", 3, int)),
        min_cluster_fraction=env_num("GLYPH_MIN_CLUSTER_FRACTION", 0.05, float),
    )

    cfg.sources = parse_sources(env("GLYPH_SOURCES"), owner)

    return cfg, g


def print_config(cfg):
    print("\n  ▓▓▓ RUN.CONFIG ⟫⟫⟫")
    print("━" * 79)
    print(f"   account         : {cfg.owner}")
    print("   input.mode      : FETCH.FROM.REPOSITORY")
    for i, s in enumerate(cfg.sources, 1):
        print(f"   source.{i:02d}       : {s}")
    print(f"   storage         : {cfg.storage_full}@{cfg.storage_branch}")
    print(f"   clear.source    : {cfg.clear_source}")
    print(f"   workers / k     : {cfg.max_workers} / {cfg.k} (min cluster {cfg.min_cluster_fraction})")
    print("━" * 79)

# ---------------------- COLOR DETECTION ----------------------

def rgb_to_hex(rgb):
    return "{:02x}{:02x}{:02x}".format(*rgb)

def rgb_to_lab(rgb):
    r, g, b = [x / 255 for x in rgb]
    r = ((r + 0.055)/1.055)**2.4 if r > 0.04045 else r/12.92
    g = ((g + 0.055)/1.055)**2.4 if g > 0.04045 else g/12.92
    b = ((b + 0.055)/1.055)**2.4 if b > 0.04045 else b/12.92
    x = r*0.4124 + g*0.3576 + b*0.1805
    y = r*0.2126 + g*0.7152 + b*0.0722
    z = r*0.0193 + g*0.1192 + b*0.9505
    x /= 0.95047
    z /= 1.08883
    f = lambda t: t**(1/3) if t > 0.008856 else 7.787*t + 16/116
    L = 116*f(y) - 16
    a = 500 * (f(x) - f(y))
    b = 200 * (f(y) - f(z))
    return (L, a, b)

def compute_hue(rgb):
    r, g, b = rgb
    return colorsys.rgb_to_hsv(r/255, g/255, b/255)[0] * 360

def compute_palette_distance(rgb1, rgb2):
    """Perceptual distance between dominant and secondary colors in LAB space"""
    lab1, lab2 = rgb_to_lab(rgb1), rgb_to_lab(rgb2)
    delta = np.sqrt(sum((p - q)**2 for p, q in zip(lab1, lab2)))
    return round(float(delta / 100), 4)

def masked_pixels(rgb, mask):
    pts = rgb[mask]
    if len(pts) == 0:
        return np.zeros((1, 3), dtype=np.uint8)
    return pts

def compute_palette(rgb, mask, k=3, min_cluster_fraction=0.05):
    """
    ONE K-means pass → (dominant, secondary).
    Deterministic (random_state=0), so dominant & secondary always come from
    the same clustering and re-runs give the same colors/filenames.
    """
    pts = masked_pixels(rgb, mask)
    fallback = (200, 200, 200)
    if len(pts) < k:
        return fallback, fallback

    p = pts / 255.0
    max_c, min_c = p.max(axis=1), p.min(axis=1)
    weights = (max_c - min_c) / (max_c + 1e-6) + 0.5   # saturation-weighted

    kmeans = KMeans(n_clusters=k, n_init="auto", random_state=0).fit(pts, sample_weight=weights)
    centers = kmeans.cluster_centers_
    counts = np.bincount(kmeans.labels_, minlength=k)
    order = np.argsort(counts)[::-1]                      # largest cluster first
    large = [i for i in order if counts[i] / counts.sum() >= min_cluster_fraction]

    dom_idx = large[0] if large else order[0]
    if len(large) >= 2:
        sec_idx = large[1]
    elif counts[order[1]] > 0:
        sec_idx = order[1]
    else:
        sec_idx = dom_idx

    to_rgb = lambda c: tuple(int(x) for x in c)
    return to_rgb(centers[dom_idx]), to_rgb(centers[sec_idx])

# Backwards-compatible wrappers (README references these names)
def compute_dominant_color(rgb, mask, k=3, min_cluster_fraction=0.05):
    return compute_palette(rgb, mask, k, min_cluster_fraction)[0]

def compute_secondary_color(rgb, mask, k=3, min_cluster_fraction=0.05):
    return compute_palette(rgb, mask, k, min_cluster_fraction)[1]

def compute_color_harmony(c1, c2):
    d = abs(compute_hue(c1) - compute_hue(c2))
    d = min(d, 360 - d)
    if d < 30:
        return "analogous"
    elif 150 <= d <= 210:
        return "complementary"
    elif 90 <= d < 150:
        return "triadic"
    return "none"

# ---------------------- PROCESSING GLYPHS ----------------------

def compute_edge_density(rgb, mask):
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 80, 160)
    return round(float(np.mean(edges[mask] > 0)), 4)

def compute_entropy(rgb, mask):
    gray = rgb2gray(rgb)
    return round(float(shannon_entropy(gray[mask])), 4)

def compute_texture_complexity(rgb, mask):
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    lbp = local_binary_pattern(gray, 8, 1, "uniform")
    vals = lbp[mask].ravel()
    hist, _ = np.histogram(vals, bins=np.arange(0, 11), density=True)
    ent = -np.sum(hist * np.log2(hist + 1e-10))
    return round(float(ent), 4)

def compute_contrast(image_rgba):
    arr = np.array(image_rgba)
    mask = arr[..., 3] > 10
    if mask.sum() == 0:
        return 0.0
    rgb = arr[..., :3][mask].astype(np.float64)
    lum = 0.2126*rgb[:, 0] + 0.7152*rgb[:, 1] + 0.0722*rgb[:, 2]
    I_max, I_min = lum.max(), lum.min()
    if I_max + I_min == 0:
        return 0.0
    return float(round((I_max - I_min)/(I_max + I_min), 4))

def compute_shape_metrics(alpha):
    mask = (alpha > 10).astype("uint8")*255
    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not cnts:
        return 0.5, 1.0
    c = max(cnts, key=cv2.contourArea)
    area = cv2.contourArea(c)
    peri = cv2.arcLength(c, True)
    circularity = 4*np.pi*area/(peri*peri + 1e-6)
    x, y, w, h = cv2.boundingRect(c)
    aspect = w/(h + 1e-6)
    return round(float(circularity), 4), round(float(aspect), 4)

def compute_edge_angle(rgb, mask):
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    sx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, 3)
    sy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, 3)
    mag = np.sqrt(sx*sx + sy*sy)
    ang = np.degrees(np.arctan2(sy, sx))
    if mask.sum() == 0:
        return 0.0
    strong = mag[mask] > np.percentile(mag[mask], 75)
    if strong.sum() == 0:
        return 0.0
    return round(float(abs(np.median(ang[mask][strong])) % 180), 4)

def compute_mood(dom_rgb, entropy, edge, tex, contrast, circ, aspect, angle, harmony):
    r, g, b = dom_rgb
    brightness = 0.2126*r + 0.7152*g + 0.0722*b
    h = compute_hue(dom_rgb)
    sat = (max(dom_rgb) - min(dom_rgb)) / (max(dom_rgb) + 1e-6)

    is_warm = (h <= 60) or (h >= 330)
    is_cool = (165 <= h <= 295)

    scores = {
        "serene": 0, "calm": 0, "playful": 0, "energetic": 0,
        "futuristic": 0, "mysterious": 0, "dramatic": 0, "chaotic": 0
    }

    if entropy < 2.2: scores["serene"] += (2.2 - entropy)/2.2
    elif entropy <= 2.8: scores["calm"] += (entropy - 2.2)/(2.8 - 2.2)
    elif entropy <= 3.8: scores["playful"] += (entropy - 2.8)/(3.8 - 2.8)
    else: scores["chaotic"] += min((entropy - 3.8)/2.5, 1)*0.4

    if edge < 0.01: scores["serene"] += 0.3
    elif edge < 0.03: scores["calm"] += 0.15
    elif edge < 0.06: scores["playful"] += 0.3
    elif edge < 0.10: scores["energetic"] += 0.3
    else: scores["chaotic"] += 0.1

    if brightness > 180: scores["playful"] += 0.5
    if brightness < 80: scores["mysterious"] += 0.6
    if contrast > 0.5: scores["dramatic"] += (contrast - 0.5)/0.5 * 0.8
    if sat > 0.6: scores["energetic"] += 0.6
    if sat < 0.2: scores["calm"] += 0.2

    if harmony == "analogous": scores["calm"] += 0.3; scores["serene"] += 0.2
    elif harmony == "complementary": scores["energetic"] += 0.4; scores["playful"] += 0.2
    elif harmony == "triadic": scores["energetic"] += 0.3; scores["futuristic"] += 0.2

    if circ > 0.8: scores["serene"] += 0.4
    if circ < 0.55: scores["playful"] += 0.4
    if 0.4 < aspect < 0.7 or 1.3 < aspect < 1.6: scores["futuristic"] += 0.6

    if is_warm and sat > 0.45: scores["energetic"] += 0.3; scores["playful"] += 0.2
    if is_cool and brightness < 120: scores["mysterious"] += 0.3; scores["calm"] += 0.1
    if 2.8 < entropy <= 3.8: scores["playful"] += 0.3
    if sat > 0.5 and brightness > 120: scores["energetic"] += 0.3

    return max(scores, key=scores.get)

def process_glyph_from_bytes(image_bytes, filename, cfg):
    """Process a single glyph directly from bytes"""
    try:
        pil = Image.open(BytesIO(image_bytes)).convert("RGBA")
    except Exception:
        return None, f"SKIP.INVALID_IMAGE :: {filename}"

    arr = np.array(pil)
    rgb, alpha = arr[:, :, :3], arr[:, :, 3]
    mask = alpha > 10

    coords = np.column_stack(np.where(mask))
    if len(coords) > 0:
        y0, x0 = coords.min(axis=0)
        y1, x1 = coords.max(axis=0) + 1
        rgb_crop, alpha_crop, mask_crop = rgb[y0:y1, x0:x1], alpha[y0:y1, x0:x1], mask[y0:y1, x0:x1]
    else:
        return None, f"SKIP.FULLY_TRANSPARENT :: {filename}"

    dom, sec = compute_palette(rgb_crop, mask_crop, cfg.k, cfg.min_cluster_fraction)
    dom_hex, sec_hex = rgb_to_hex(dom), rgb_to_hex(sec)
    dom_lab, sec_lab = rgb_to_lab(dom), rgb_to_lab(sec)
    palette_distance = compute_palette_distance(dom, sec)
    edge = compute_edge_density(rgb_crop, mask_crop)
    ent = compute_entropy(rgb_crop, mask_crop)
    tex = compute_texture_complexity(rgb_crop, mask_crop)
    con = compute_contrast(pil)
    circ, ar = compute_shape_metrics(alpha_crop)
    ang = compute_edge_angle(rgb_crop, mask_crop)
    harmony = compute_color_harmony(dom, sec)
    mood = compute_mood(dom, ent, edge, tex, con, circ, ar, ang, harmony)

    uid = uuid.uuid4().hex[:8]
    now = datetime.now(timezone.utc)
    newname = f"{dom_hex}_{sec_hex}_{uid}.png"

    buf = BytesIO()
    pil.save(buf, format="PNG")

    url = f"https://cdn.jsdelivr.net/gh/{cfg.storage_user}/{cfg.storage_repo}@{cfg.storage_branch}/glyphs/{newname}"

    glyph_data = {
        "id": uid,
        "filename": newname,
        "glyph_url": url,
        "color": {
            "dominant": {"hex": dom_hex, "rgb": list(dom), "lab": [round(x, 2) for x in dom_lab]},
            "secondary": {"hex": sec_hex, "rgb": list(sec), "lab": [round(x, 2) for x in sec_lab]},
            "palette_distance": palette_distance
        },
        "metrics": {
            "edge_density": edge,
            "entropy": ent,
            "texture": tex,
            "contrast": con,
            "circularity": circ,
            "aspect_ratio": ar,
            "edge_angle": ang
        },
        "color_harmony": harmony,
        "mood": mood,
        "created_at": {"date": now.strftime("%Y-%m-%d"), "time": now.strftime("%H:%M:%S")}
    }
    return (newname, buf.getvalue(), glyph_data), None

# ---------------------- INPUT SOURCES ----------------------

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


def fetch_from_sources(g, cfg):
    """
    Pull PNGs from each source folder (non-recursive) at the live branch head.
    Git tree + blob API: no 1,000-file directory cap, no 1 MB file cap.
    Stream keys are 'owner/repo:path' so equal filenames from different repos never collide.
    """
    stream, skipped, total = {}, [], 0

    for src in cfg.sources:
        try:
            repo = g.get_repo(src.full)
            src.branch = src.branch or repo.default_branch
            tree = repo.get_git_tree(repo.get_branch(src.branch).commit.sha, recursive=True)
        except GhException as e:
            msg = f"SKIP.SOURCE_UNREACHABLE :: {src} ({e.status} {_gh_msg(e)})"
            print(f"  ⟨⚠⟩  {msg}")
            skipped.append(msg)
            continue

        if tree.raw_data.get("truncated"):
            print(f"  ⟨⚠⟩  Tree listing of {src.full} was truncated by GitHub — some files may be missing")

        src.folder, items, hint = match_folder(tree.tree, src.folder, {".png"})
        total += len(items)
        print(f"\n◢◤ [FETCHING.DATA] {len(items)} files FROM {src}...")
        if hint:
            print(f"  ⟨⚠⟩  {hint}")
            print(f"::warning::{src.repo}: {hint}")
        if not items:
            skipped.append(f"SKIP.EMPTY_SOURCE :: {src} — {hint}")
            continue

        def pull(el, repo=repo):
            return b64decode(repo.get_git_blob(el.sha).content)

        with ThreadPoolExecutor(max_workers=cfg.max_workers) as ex:
            futures = {ex.submit(pull, el): el for el in items}
            for fut in as_completed(futures):
                el = futures[fut]
                key = f"{src.full}:{el.path}"
                try:
                    data = fut.result()
                except Exception:
                    skipped.append(f"SKIP.FETCH_ERROR :: {key}")
                    continue
                stream[key] = {"repo": src.full, "branch": src.branch, "path": el.path, "data": data}

    print()
    return stream, skipped, total

# ---------------------- STORAGE ----------------------

def _gh_msg(e):
    return e.data.get("message", "Unknown error") if isinstance(e.data, dict) else str(e.data)


def get_or_create_storage_repo(g, cfg):
    created = False
    try:
        repo = g.get_repo(cfg.storage_full)
        print(f"\n  ⬢ REPO.FOUND: {cfg.storage_full}\n")
    except GhException as e:
        if e.status != 404:
            raise
        print(f"\n   ⟨⚠⟩  REPO.NOT_FOUND → creating '{cfg.storage_full}'...")
        me = g.get_user()
        owner = me if me.login.lower() == cfg.storage_user.lower() else g.get_organization(cfg.storage_user)
        repo = owner.create_repo(cfg.storage_repo, auto_init=True)
        created = True
        print("  ▲  REPO.INIT (folders 'glyphs/' and 'data/' are created by the first commit)\n")

    try:
        repo.get_branch(cfg.storage_branch)
    except GhException as e:
        if e.status != 404:
            raise
        base = repo.get_branch(repo.default_branch)
        repo.create_git_ref(f"refs/heads/{cfg.storage_branch}", base.commit.sha)
        print(f"  ▲  BRANCH.CREATED: {cfg.storage_branch} (from {repo.default_branch})\n")

    return repo, created


def load_existing_catalog(repo, branch):
    """
    Reads the catalog via the blob API so it keeps working past 1 MB.
    Only a missing file counts as 'no catalog' — any other error aborts,
    so an unreadable catalog can never be silently overwritten.
    """
    try:
        meta = repo.get_contents(CATALOG_JSON, ref=branch)
    except GhException as e:
        if e.status == 404:
            return []
        raise
    raw = b64decode(repo.get_git_blob(meta.sha).content)
    return json.loads(raw.decode("utf-8")).get("glyphs", [])


def commit_elements(repo, branch, elements, message):
    ref = repo.get_git_ref(f"heads/{branch}")
    head = repo.get_git_commit(ref.object.sha)
    tree = repo.create_git_tree(elements, head.tree)
    commit = repo.create_git_commit(message, tree, [head])
    ref.edit(commit.sha)  # non-force: fails instead of clobbering if branch moved
    return commit


def deletion_elements(paths):
    # sha=None in a tree element deletes that path
    return [InputGitTreeElement(path=p, mode="100644", type="blob", sha=None) for p in paths]


def build_csv(all_glyphs):
    out = StringIO()
    w = csv.writer(out)
    w.writerow([
        "id", "filename", "glyph_url",
        "dominant_hex", "dominant_rgb", "dominant_lab",
        "secondary_hex", "secondary_rgb", "secondary_lab",
        "palette_distance",
        "edge_density", "entropy", "texture", "contrast", "circularity", "aspect_ratio",
        "edge_angle", "color_harmony", "mood", "created_date", "created_time"
    ])
    for gl in all_glyphs:
        c, m = gl["color"], gl["metrics"]
        w.writerow([
            gl["id"], gl["filename"], gl["glyph_url"],
            c["dominant"]["hex"], str(c["dominant"]["rgb"]), str(c["dominant"]["lab"]),
            c["secondary"]["hex"], str(c["secondary"]["rgb"]), str(c["secondary"]["lab"]),
            c["palette_distance"],
            m["edge_density"], m["entropy"], m["texture"],
            m["contrast"], m["circularity"], m["aspect_ratio"],
            m["edge_angle"], gl["color_harmony"], gl["mood"],
            gl["created_at"]["date"], gl["created_at"]["time"]
        ])
    return out.getvalue()


def write_step_summary(lines):
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if path:
        with open(path, "a", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")

# ---------------------- DATA PIPELINE ----------------------

def execute_glyph_pipeline(g, cfg, glyph_stream, fetch_skipped, original_input_count):
    repo, created = get_or_create_storage_repo(g, cfg)
    existing_glyphs = [] if created else load_existing_catalog(repo, cfg.storage_branch)

    print(f"\n⟨██⟩ Processing {len(glyph_stream)} glyphs...\n")

    all_data, elements, processed = [], [], []
    skipped = list(fetch_skipped or [])

    with ThreadPoolExecutor(max_workers=cfg.max_workers) as ex:
        futures = {
            ex.submit(process_glyph_from_bytes, item["data"], key, cfg): (key, item)
            for key, item in glyph_stream.items()
        }
        for fut in as_completed(futures):
            key, item = futures[fut]
            try:
                result, skip_msg = fut.result()
            except Exception as e:
                skipped.append(f"SKIP.PROCESSING_ERROR :: {key} ({e})")
                continue
            if skip_msg:
                skipped.append(skip_msg)
                continue

            newname, image_bytes, glyph_data = result
            blob = repo.create_git_blob(b64encode(image_bytes).decode("utf-8"), "base64")
            elements.append(InputGitTreeElement(path=f"glyphs/{newname}", mode="100644", type="blob", sha=blob.sha))
            all_data.append(glyph_data)
            processed.append(item)
            print(f"   ◇ {key}  →  {newname}  [{glyph_data['mood']}]")

    if not all_data:
        fail("No valid glyphs to process")

    all_glyphs = existing_glyphs + all_data
    catalog = {"total": len(all_glyphs), "glyphs": all_glyphs}
    elements.append(InputGitTreeElement(path=CATALOG_JSON, mode="100644", type="blob",
                                        content=json.dumps(catalog, indent=2)))
    elements.append(InputGitTreeElement(path=CATALOG_CSV, mode="100644", type="blob",
                                        content=build_csv(all_glyphs)))

    # Group processed inputs per (repo, branch) for optional clearing
    groups = defaultdict(list)
    for item in processed:
        groups[(item["repo"].lower(), item["branch"])].append(item["path"])

    cleared = []
    if cfg.clear_source:
        own = groups.pop((cfg.storage_full.lower(), cfg.storage_branch), [])
        if own:  # inputs live in the storage repo+branch → delete in the same commit
            elements += deletion_elements(own)
            cleared.append(f"{len(own)} from {cfg.storage_full} (same commit)")

    if existing_glyphs:
        commit_type = "LIBRARY.EXPANDED"
        commit_msg = f"⟨LIBRARY.EXPANDED⟩   +{len(all_data)} glyphs, 2 catalogs updated"
        catalog_status = "2 catalogs updated [CSV + JSON]"
        library_info = f"{len(existing_glyphs)} + {len(all_data)} = {len(all_glyphs)} glyphs in total"
    else:
        commit_type = "LIBRARY.INIT"
        commit_msg = f"⟨LIBRARY.INIT⟩   {len(all_data)} glyphs + 2 catalogs generated"
        catalog_status = "2 catalogs generated [CSV + JSON]"
        library_info = f"{len(all_data)} glyphs"

    footer = ""
    if env("GITHUB_RUN_ID"):
        footer = f"\n\nworkflow run: {env('GITHUB_SERVER_URL', 'https://github.com')}/{env('GITHUB_REPOSITORY')}/actions/runs/{env('GITHUB_RUN_ID')}"

    commit = commit_elements(repo, cfg.storage_branch, elements, commit_msg + footer)

    # Inputs in other repos → one clearing commit per source repo/branch
    if cfg.clear_source:
        for (src_full, src_branch), paths in groups.items():
            try:
                commit_elements(g.get_repo(src_full), src_branch, deletion_elements(paths),
                                f"⟨SOURCE.CLEARED⟩   -{len(paths)} processed glyphs → {cfg.storage_full}" + footer)
                cleared.append(f"{len(paths)} from {src_full}@{src_branch}")
            except GhException as e:
                cleared.append(f"FAILED on {src_full} ({e.status}) — library commit is safe")
                print(f"::warning::Clearing {src_full} failed: {e.status} {_gh_msg(e)}")
    cleared_status = "; ".join(cleared) if cleared else "off"

    # ---------- console summary ----------
    lines = [
        BAR,
        "██  ",
        "██  ⟫⟫⟫ [COMPLETE] STREAM.SUCCESSFUL",
        "██  ",
        f"██      ├── total.input: {original_input_count}",
        f"██      ├── status.success: {len(all_data)}",
        f"██      ├── status.skipped: {len(skipped)}",
        f"██      ├── commit.type: {commit_type}",
        f"██      │   ├── {library_info}",
        f"██      │   └── {catalog_status}",
        f"██      ├── input.mode: FETCH.FROM.REPOSITORY ({len(cfg.sources)} source(s))",
        f"██      ├── source.cleared: {cleared_status}",
        f"██      └── storage.location: {cfg.storage_full}@{cfg.storage_branch}",
        f"██        └── [⫘] https://github.com/{cfg.storage_full}/commit/{commit.sha}",
        "██  ",
    ]
    if skipped:
        lines += [BAR, "██  ", f"██      [◢◣]⎯⎯⎯⎯ SKIPPED {len(skipped)} FILE(S):", "██  "]
        lines += [f"██                >>   {msg}" for msg in skipped]
        lines += ["██  "]
    lines.append(BAR)

    print("\n" + "\n".join(lines))

    commit_url = f"https://github.com/{cfg.storage_full}/commit/{commit.sha}"

    def to_html(line):
        out = html.escape(line, quote=False)
        if commit_url in line:
            out = out.replace(commit_url, f'<a href="{commit_url}">{commit_url}</a>')
        return out

    pre = [html.escape(l, quote=False) for l in BANNER] + [""] + [to_html(l) for l in lines]
    write_step_summary([
        "### ▓▓▓ PROCESS.SUMMARY ⟫⟫⟫",
        "",
        "<pre>" + "\n".join(pre) + "</pre>",
    ])

# ---------------------- ENTRYPOINT ----------------------

def main():
    print("\n" + "\n".join(BANNER) + "\n")

    cfg, g = resolve_config()
    print_config(cfg)

    stream, fetch_skipped, original_count = fetch_from_sources(g, cfg)

    if not stream:
        reasons = "".join(f"\n      >> {m}" for m in fetch_skipped)
        fail(f"No valid glyphs detected to process{reasons}")

    try:
        execute_glyph_pipeline(g, cfg, stream, fetch_skipped, original_count)
    except GhException as e:
        fail(f"ERROR.GITHUB_API: {e.status} - {_gh_msg(e)}")
    except SystemExit:
        raise
    except Exception as e:
        traceback.print_exc()
        fail(f"UNEXPECTED_ERROR: {e}")


if __name__ == "__main__":
    main()
