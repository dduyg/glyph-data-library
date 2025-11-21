"""
🔱 GLYPH PROCESSOR
- Upload images → Process → Generate renamed images + metadata
- Extract dominant color using K-means clustering
- Unique timestamp + UUID filenames
- Incremental metadata updates (JSON + JS)
- Save options:
  1. Local ZIP
  2. Directly to GitHub via API (images → glyphs/, data → data/)
- Auto-creates GitHub repo/folders if it doesn't exist
"""

import os
import json
import colorsys
import uuid
from pathlib import Path
from datetime import datetime, timezone
import shutil
import zipfile
from getpass import getpass

from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

# ---------------------- COLOR DETECTION ----------------------

def get_dominant_color(image_path, k=3):
    """
    Detect the dominant color by grouping similar colors
    using K-Means clustering. Returns the RGB color
    of the largest cluster (largest surface area).
    """
    try:
        img = Image.open(image_path).convert("RGBA").resize((150,150))
        pixels = np.array(img)
        mask = (pixels[:,:,3] > 128) & ~(
            (pixels[:,:,0] > 240) & (pixels[:,:,1] > 240) & (pixels[:,:,2] > 240)
        )
        pixels = pixels[mask][:,:3]
        if len(pixels) == 0:
            return (200,200,200)
        kmeans = KMeans(n_clusters=k, n_init="auto").fit(pixels)
        centers = kmeans.cluster_centers_
        labels, counts = np.unique(kmeans.labels_, return_counts=True)
        dominant_cluster = labels[np.argmax(counts)]
        rgb = centers[dominant_cluster]
        return tuple(int(x) for x in rgb)
    except Exception as e:
        print(f"Error reading {image_path}: {e}")
        return (200,200,200)

def rgb_to_hex(rgb):
    return '{:02x}{:02x}{:02x}'.format(*rgb)

def rgb_to_lab(rgb):
    r, g, b = [x / 255.0 for x in rgb]
    r = ((r + 0.055) / 1.055)**2.4 if r > 0.04045 else r / 12.92
    g = ((g + 0.055) / 1.055)**2.4 if g > 0.04045 else g / 12.92
    b = ((b + 0.055) / 1.055)**2.4 if b > 0.04045 else b / 12.92
    x = r * 0.4124564 + g * 0.3575761 + b * 0.1804375
    y = r * 0.2126729 + g * 0.7151522 + b * 0.0721750
    z = r * 0.0193339 + g * 0.1191920 + b * 0.9503041
    x, y, z = x / 0.95047, y / 1.0, z / 1.08883
    def f(t): return t ** (1/3) if t > 0.008856 else (7.787 * t + 16/116)
    L = 116 * f(y) - 16
    a = 500 * (f(x) - f(y))
    b = 200 * (f(y) - f(z))
    return (L, a, b)

def get_color_name(rgb):
    r, g, b = rgb
    h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
    h = h * 360
    if s < 0.1:
        return "white" if v>0.8 else "black" if v<0.2 else "gray"
    if h < 15 or h > 345: return "red"
    if h < 45: return "orange"
    if h < 75: return "yellow"
    if h < 165: return "green"
    if h < 255: return "blue"
    if h < 290: return "purple"
    return "pink"

# ---------------------- PROCESSING GLYPHS ----------------------

def process_glyphs(input_folder, output_folder, github_user="your-username", github_repo="glyph-library"):
    os.makedirs(output_folder, exist_ok=True)
    png_files = list(Path(input_folder).glob('*.png'))
    glyphs = []

    for image_path in png_files:
        dominant_rgb = get_dominant_color(image_path)
        hex_color = rgb_to_hex(dominant_rgb)
        color_name = get_color_name(dominant_rgb)
        lab = rgb_to_lab(dominant_rgb)

        now = datetime.now(timezone.utc)
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")
        unique_id = uuid.uuid4().hex[:8]

        new_filename = f"{hex_color}_{now.strftime('%Y%m%d_%H%M%S')}_{unique_id}.png"
        out_path = Path(output_folder) / new_filename
        shutil.copy2(image_path, out_path)

        glyph_url = f"https://raw.githubusercontent.com/{github_user}/{github_repo}/main/glyphs/{new_filename}"

        glyph_data = {
            "id": unique_id,
            "filename": new_filename,
            "glyph_url": glyph_url,
            "color": {
                "hex": hex_color,
                "name": color_name,
                "rgb": list(dominant_rgb),
                "lab": [round(x,2) for x in lab]
            },
            "timestamp": {"date": date_str, "time": time_str}
        }
        glyphs.append(glyph_data)
        print(f"Processed {image_path.name} → {new_filename}")

    return glyphs

# ---------------------- METADATA ----------------------

def load_existing_metadata(json_path=None, repo=None, branch="main", json_repo_path="data/glyphs-metadata.json"):
    metadata = {"total": 0, "glyphs": []}
    if json_path and json_path.exists():
        with open(json_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
    elif repo:
        try:
            file_content = repo.get_contents(json_repo_path, ref=branch)
            metadata = json.loads(file_content.decoded_content.decode())
        except:
            pass
    return metadata

# ---------------------- UPLOAD/UPDATE FILES ----------------------

def upload_or_update(repo, file_path, repo_path, branch):
    with open(file_path, "rb") as f:
        content = f.read()
    try:
        existing_file = repo.get_contents(repo_path, ref=branch)
        repo.update_file(existing_file.path, f"Update {file_path.name}", content, existing_file.sha, branch=branch)
        print(f"🌀 Updated {repo_path}")
    except:
        repo.create_file(repo_path, f"Add {file_path.name}", content, branch=branch)
        print(f"✔ Uploaded {repo_path}")

# ---------------------- INTERACTION LAYER ----------------------

print("🔱 𝙶𝙻𝚈𝙿𝙷 𝙿𝚁𝙾𝙲𝙴𝚂𝚂𝙾𝚁")

!pip install -q opencv-python-headless PyGithub scikit-learn

from google.colab import files
from github import Github, Auth, GithubException

print("🔘 Select the images you want to process:")
uploaded = files.upload()
if not uploaded:
    print("✖️ No files uploaded.")
    raise SystemExit

input_dir = Path("/content/input_glyphs")
output_dir = Path("/content/output_glyphs")
input_dir.mkdir(exist_ok=True)
output_dir.mkdir(exist_ok=True)

for fname, content in uploaded.items():
    with open(input_dir / fname, 'wb') as f:
        f.write(content)

print(f"☑️ Uploaded {len(uploaded)} images")

github_user = input("👤 GitHub username: ").strip() or "your-username"
github_repo = input("🗃️ GitHub repo name: ").strip() or "glyph-library"

print("⏳️ Processing images …")
new_glyphs = process_glyphs(input_dir, output_dir, github_user, github_repo)

# ---------------------- SAVE OPTION ----------------------

print("\n🗂️ Where to save results?")
print("1️⃣ Local ZIP")
print("2️⃣ Autoload directly to GitHub")
choice = input("Choose 1 or 2: ").strip()

zip_name = "glyphs_processed.zip"

if choice == "1":
    zip_path = Path(f"/content/{zip_name}")
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, dirs, files_list in os.walk(output_dir):
            for f in files_list:
                full = os.path.join(root, f)
                arc = os.path.relpath(full, output_dir)
                zipf.write(full, arc)
    save_path = input("Enter local folder path to save ZIP: ").strip()
    save_folder = Path(save_path)
    save_folder.mkdir(parents=True, exist_ok=True)
    shutil.copy2(zip_path, save_folder / zip_name)
    print(f"📦 ZIP saved locally to: {save_folder / zip_name}")

elif choice == "2":
    gh_token = getpass("🔑 GitHub Personal Access Token (with repo permissions): ").strip()
    branch = input("🌿 Branch name (default: main): ").strip() or "main"

    g = Github(auth=Auth.Token(gh_token))
    user = g.get_user()

    try:
        repo = user.get_repo(github_repo)
        print(f"✔ Repo found: {github_repo}")
    except GithubException:
        print(f"⚠ Repo '{github_repo}' not found — creating it now...")
        repo = user.create_repo(github_repo, private=False)
        repo.create_file("glyphs/.gitkeep", "Init glyphs folder", "", branch=branch)
        repo.create_file("data/.gitkeep", "Init data folder", "", branch=branch)
        print("📂 Base folders created ('glyphs/' and 'data/')")

    existing_metadata = load_existing_metadata(repo=repo, branch=branch)
    incremental_update = bool(existing_metadata.get("glyphs"))

    all_glyphs = existing_metadata.get("glyphs", []) + new_glyphs
    metadata = {"total": len(all_glyphs), "glyphs": all_glyphs}

    json_path = Path(output_dir) / "glyphs-metadata.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)

    js_path = Path(output_dir) / "glyph-data.js"
    js_code = "// Glyph Data\nconst GLYPH_DATA = [\n"
    for g in all_glyphs:
        js_code += (
            "  {"
            f"id:'{g['id']}',"
            f"glyph_url:'{g['glyph_url']}',"
            f"filename:'{g['filename']}',"
            f"hex:'#{g['color']['hex']}',"
            f"rgb:{g['color']['rgb']},"
            f"lab:{g['color']['lab']},"
            f"colorName:'{g['color']['name']}',"
            f"date:'{g['timestamp']['date']}',"
            f"time:'{g['timestamp']['time']}'"
            "},\n"
        )
    js_code += "];\n"
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(js_code)

    for f in Path(output_dir).glob("*.png"):
        upload_or_update(repo, f, f"glyphs/{f.name}", branch)

    upload_or_update(repo, json_path, "data/glyphs-metadata.json", branch)
    upload_or_update(repo, js_path, "data/glyph-data.js", branch)

    if incremental_update:
        print(f"🎊 All done! The library has been successfully expanded to {len(all_glyphs)} glyphs in total.")
    else:
        print("🎊 All done!")

else:
    print("Invalid option. Files remain in /content/output_glyphs.")
