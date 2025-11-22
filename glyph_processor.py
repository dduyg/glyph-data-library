"""
🔱 GLYPH PROCESSOR
- Upload images → Process → Generate renamed images + metadata
- Extract dominant color using K-means clustering
- Compute Edge Density + Entropy + Texture + Contrast + Shape + Color Harmony + Mood
- Unique timestamp + UUID filenames
- Incremental metadata updates (JSON + JS)
- Save options:
  1. Local ZIP
  2. Directly to GitHub via API (images → glyphs/, data → data/)
- Auto-creates GitHub repo/folders if it doesn't exist
"""

!pip install -q opencv-python-headless scikit-learn scikit-image PyGithub

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
import cv2
from sklearn.cluster import KMeans
from skimage.measure import shannon_entropy, label, regionprops
from skimage.color import rgb2gray
from skimage.feature import local_binary_pattern
from github import Github, Auth, GithubException
from google.colab import files

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
        mask = (pixels[:,:,3] > 128) & ~((pixels[:,:,0] > 240) & (pixels[:,:,1] > 240) & (pixels[:,:,2] > 240))
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

def get_secondary_color(image_path, k=3):
    """Return the second most dominant color for color harmony"""
    try:
        img = Image.open(image_path).convert("RGBA").resize((150,150))
        pixels = np.array(img)
        mask = (pixels[:,:,3] > 128) & ~((pixels[:,:,0] > 240) & (pixels[:,:,1] > 240) & (pixels[:,:,2] > 240))
        pixels = pixels[mask][:,:3]
        if len(pixels) < 2:
            return (200,200,200)
        kmeans = KMeans(n_clusters=k, n_init="auto").fit(pixels)
        centers = kmeans.cluster_centers_
        labels, counts = np.unique(kmeans.labels_, return_counts=True)
        sorted_idx = np.argsort(counts)[::-1]
        secondary_cluster = sorted_idx[1] if len(sorted_idx)>1 else sorted_idx[0]
        rgb = centers[secondary_cluster]
        return tuple(int(x) for x in rgb)
    except:
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

def get_edge_density(image_path):
    img = cv2.imread(str(image_path))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3,3), 0)
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)
    sobel_mag = np.sqrt(sobelx**2 + sobely**2)
    sobel_norm = (sobel_mag / sobel_mag.max() * 255).astype(np.uint8)
    canny = cv2.Canny(gray, 80, 160)
    combined = cv2.bitwise_or(canny, sobel_norm)
    edge_pixels = np.sum(combined > 50)
    total_pixels = combined.size
    return round(edge_pixels / total_pixels, 4)

def get_entropy(image_path):
    img = Image.open(image_path).convert("RGB")
    arr = np.array(img)
    gray = rgb2gray(arr)
    return round(float(shannon_entropy(gray)), 4)

def get_texture_complexity(image_path):
    img = cv2.imread(str(image_path))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    lbp = local_binary_pattern(gray, P=8, R=1, method="uniform")
    hist, _ = np.histogram(lbp.ravel(), bins=np.arange(0,11), density=True)
    return round(float(np.std(hist)), 4)

def get_contrast(image_path):
    img = cv2.imread(str(image_path))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return round(float((gray.max()-gray.min())/(gray.max()+gray.min()+1e-5)),4)

def get_edge_orientation(image_path):
    img = cv2.imread(str(image_path))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1,0,3)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0,1,3)
    magnitude = np.sqrt(sobelx**2 + sobely**2) + 1e-5
    angle = np.arctan2(sobely, sobelx) * 180 / np.pi
    dominant_angle = np.median(angle[magnitude>np.percentile(magnitude,70)])
    return abs(dominant_angle)%180

def get_shape_metrics(image_path):
    img = cv2.imread(str(image_path))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray,10,255,cv2.THRESH_BINARY)
    labels = label(thresh)
    regions = regionprops(labels)
    if not regions:
        return 0.5,1.0
    region = max(regions, key=lambda r: r.area)
    circularity = (4*np.pi*region.area)/(region.perimeter**2+1e-5)
    minr, minc, maxr, maxc = region.bbox
    aspect_ratio = (maxc-minc)/(maxr-minr+1e-5)
    return round(circularity,2), round(aspect_ratio,2)

def get_color_harmony(dominant_rgb, secondary_rgb):
    r1,g1,b1=dominant_rgb
    r2,g2,b2=secondary_rgb
    h1 = colorsys.rgb_to_hsv(r1/255,g1/255,b1/255)[0]*360
    h2 = colorsys.rgb_to_hsv(r2/255,g2/255,b2/255)[0]*360
    delta_h = abs(h1-h2)%360
    if delta_h<30:
        return "analogous"
    elif abs(delta_h-180)<30:
        return "complementary"
    return "none"

def get_mood(dominant_rgb, entropy, edge_density, texture, contrast, circularity, aspect_ratio, edge_angle, color_harmony):
    r,g,b = dominant_rgb
    brightness = (r+g+b)/3
    maxc=max(r,g,b)
    minc=min(r,g,b)
    saturation=(maxc-minc)/maxc if maxc else 0
    hue = colorsys.rgb_to_hsv(r/255,g/255,b/255)[0]*360

    # 9 moods rules
    if entropy<4 and edge_density<0.05 and saturation<0.3: return "minimalistic"
    if entropy<4 and edge_density<0.05 and saturation>=0.3: return "serene"
    if entropy<6 and edge_density<0.1 and saturation>=0.4 and brightness>130: return "calm"
    if entropy>6 and edge_density>0.15 and texture>0.05: return "chaotic"
    if brightness<90 and hue>180 and contrast>0.4: return "mysterious"
    if brightness>150 and hue>200 and saturation<0.35: return "futuristic"
    if saturation>0.45 and entropy<6 and edge_density<0.1: return "energetic"
    if contrast>0.5 and entropy<6 and edge_density<0.1 and circularity<0.6: return "dramatic"
    if saturation>0.5 and brightness>120 and edge_density<0.1 and color_harmony=="analogous": return "playful"
    return "serene"

def process_glyphs(input_folder, output_folder, github_user="your-username", github_repo="glyph-library"):
    os.makedirs(output_folder, exist_ok=True)
    png_files = list(Path(input_folder).glob("*.png"))
    glyphs=[]
    for image_path in png_files:
        dominant_rgb=get_dominant_color(image_path)
        secondary_rgb=get_secondary_color(image_path)
        hex_color=rgb_to_hex(dominant_rgb)
        color_name=get_color_name(dominant_rgb)
        lab=rgb_to_lab(dominant_rgb)

        # Metrics
        edge_density=get_edge_density(image_path)
        entropy=get_entropy(image_path)
        texture=get_texture_complexity(image_path)
        contrast=get_contrast(image_path)
        circularity, aspect_ratio=get_shape_metrics(image_path)
        edge_angle=get_edge_orientation(image_path)
        color_harmony=get_color_harmony(dominant_rgb, secondary_rgb)
        mood=get_mood(dominant_rgb, entropy, edge_density, texture, contrast, circularity, aspect_ratio, edge_angle, color_harmony)

        now=datetime.now(timezone.utc)
        date_str=now.strftime("%Y-%m-%d")
        time_str=now.strftime("%H:%M:%S")
        unique_id=uuid.uuid4().hex[:8]

        new_filename=f"{hex_color}_{now.strftime('%Y%m%d_%H%M%S')}_{unique_id}.png"
        out_path=Path(output_folder)/new_filename
        shutil.copy2(image_path,out_path)

        glyph_url=f"https://raw.githubusercontent.com/{github_user}/{github_repo}/main/glyphs/{new_filename}"

        glyph_data={
            "id": unique_id,
            "filename": new_filename,
            "glyph_url": glyph_url,
            "color":{
                "hex":hex_color,
                "name":color_name,
                "rgb":list(dominant_rgb),
                "lab":[round(x,2) for x in lab]
            },
            "metrics":{
                "edge_density":edge_density,
                "entropy":entropy,
                "texture":texture,
                "contrast":contrast,
                "circularity":circularity,
                "aspect_ratio":aspect_ratio,
                "edge_angle":edge_angle
            },
            "color_harmony":color_harmony,
            "mood":mood,
            "timestamp":{"date":date_str,"time":time_str}
        }
        glyphs.append(glyph_data)
        print(f"Processed {image_path.name} → {new_filename}")
    return glyphs

# ---------------------- DATA HANDLING ----------------------

def load_existing_metadata(json_path=None, repo=None, branch="main", json_repo_path="data/glyphs-data.json"):
    metadata={"total":0,"glyphs":[]}
    if json_path and json_path.exists():
        with open(json_path,'r',encoding='utf-8') as f:
            metadata=json.load(f)
    elif repo:
        try:
            file_content=repo.get_contents(json_repo_path, ref=branch)
            metadata=json.loads(file_content.decoded_content.decode())
        except:
            pass
    return metadata

def upload_or_update(repo, file_path, repo_path, branch):
    with open(file_path,"rb") as f:
        content=f.read()
    try:
        existing_file=repo.get_contents(repo_path, ref=branch)
        repo.update_file(existing_file.path,f"Update {file_path.name}",content,existing_file.sha,branch=branch)
        print(f"🌀 Updated {repo_path}")
    except GithubException:
        repo.create_file(repo_path,f"Add {file_path.name}",content,branch=branch)
        print(f"✔ Uploaded {repo_path}")

# ---------------------- INTERACTION LAYER ----------------------

print("\n🔱 𝙶𝙻𝚈𝙿𝙷 𝙿𝚁𝙾𝙲𝙴𝚂𝚂𝙾𝚁\n")

print("📤 Select images to process:\n")
uploaded = files.upload()
if not uploaded:
    print("✖️ No files uploaded.")
    raise SystemExit

input_dir=Path("/content/input_glyphs")
output_dir=Path("/content/output_glyphs")
input_dir.mkdir(exist_ok=True)
output_dir.mkdir(exist_ok=True)

for fname, content in uploaded.items():
    with open(input_dir/fname,"wb") as f:
        f.write(content)
print(f"☑️ Uploaded {len(uploaded)} images")

github_user=input("👾 GitHub username: ").strip() or "your-username"
github_repo=input("🗃️ GitHub repo name: ").strip() or "glyph-library"

print("⏳️ Processing images …")
new_glyphs=process_glyphs(input_dir, output_dir, github_user, github_repo)

# ---------------------- SAVE OPTIONS ----------------------

print("\n🗄️ Where to save results?")
print("1️⃣ Local ZIP")
print("2️⃣ Autoload directly to GitHub")
choice=input("Choose 1 or 2: ").strip()
zip_name="glyphs_processed.zip"

if choice=="1":
    zip_path=Path(f"/content/{zip_name}")
    with zipfile.ZipFile(zip_path,'w') as zipf:
        for root, dirs, files_list in os.walk(output_dir):
            for f in files_list:
                full=os.path.join(root,f)
                arc=os.path.relpath(full, output_dir)
                zipf.write(full,arc)
    save_path=input("Enter local folder path to save ZIP: ").strip()
    save_folder=Path(save_path)
    save_folder.mkdir(parents=True,exist_ok=True)
    shutil.copy2(zip_path, save_folder/zip_name)
    print(f"📦 ZIP saved locally to: {save_folder/zip_name}")

elif choice=="2":
    gh_token=getpass("🔑 GitHub Personal Access Token (with repo permissions): ").strip()
    branch=input("🌿 Branch name (default: main): ").strip() or "main"

    g=Github(auth=Auth.Token(gh_token))
    user=g.get_user()
    try:
        repo=user.get_repo(github_repo)
        print(f"✔ Repo found: {github_repo}")
    except GithubException:
        print(f"⚠ Repo '{github_repo}' not found — creating it now...")
        repo=user.create_repo(github_repo, private=False)
        repo.create_file("glyphs/.gitkeep","Init glyphs folder","",branch=branch)
        repo.create_file("data/.gitkeep","Init data folder","",branch=branch)
        print("🗂️ Base folders created ('glyphs/' and 'data/')")

    existing_metadata=load_existing_metadata(repo=repo, branch=branch)
    incremental_update=bool(existing_metadata.get("glyphs"))

    all_glyphs=existing_metadata.get("glyphs",[])+new_glyphs
    metadata={"total":len(all_glyphs),"glyphs":all_glyphs}

    json_path=Path(output_dir)/"glyphs-data.json"
    with open(json_path,'w',encoding='utf-8') as f:
        json.dump(metadata,f,indent=2)

    js_path=Path(output_dir)/"glyphs.js"
    js_code="// Glyph Data\nconst GLYPH_DATA=[\n"
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
            f"edgeDensity:{g['metrics']['edge_density']},"
            f"entropy:{g['metrics']['entropy']},"
            f"texture:{g['metrics']['texture']},"
            f"contrast:{g['metrics']['contrast']},"
            f"circularity:{g['metrics']['circularity']},"
            f"aspectRatio:{g['metrics']['aspect_ratio']},"
            f"edgeAngle:{g['metrics']['edge_angle']},"
            f"colorHarmony:'{g['color_harmony']}',"
            f"mood:'{g['mood']}',"
            f"date:'{g['timestamp']['date']}',"
            f"time:'{g['timestamp']['time']}'"
            "},\n"
        )
    js_code += "];\n"

    with open(js_path,'w',encoding='utf-8') as f:
        f.write(js_code)

    for f in Path(output_dir).glob("*.png"):
        upload_or_update(repo, f, f"glyphs/{f.name}", branch)

    upload_or_update(repo, json_path, "data/glyphs-data.json", branch)
    upload_or_update(repo, js_path, "data/glyphs.js", branch)

    if incremental_update:
        print(f"🎊 All done! Library successfully expanded to {len(all_glyphs)} glyphs in total.")
    else:
        print("🎊 All done!")

else:
    print("Invalid option. Files remain in /content/output_glyphs.")
