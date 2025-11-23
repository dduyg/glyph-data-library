# 📋 Guide

### 1. Open a new Colab Notebook  
Paste the entire script into a cell and run it.

### 2. Upload PNG images  
The script will prompt:

```
📤 Select images to process:
```

Upload any amount of `.png` files.

### 3. Enter GitHub info  
```
👾 GitHub username:
🗃️ GitHub repo name:
```

If it doesn’t exist, it's automatically created.

### 4. Choose export method  
After processing:

#### Option 1 — Local ZIP  
Saves `glyphs_processed.zip` to any folder you specify.

#### Option 2 — Upload to GitHub  
The script asks for a **GitHub Personal Access Token** (PAT).

---

# 🔐 How to Generate a GitHub Token (Required for Autoload)

### 1. Visit token page:  
👉 https://github.com/settings/tokens?type=beta

### 2. Choose:  
**“Generate new token (classic)”**

### 3. Set a name  
Example:
```
glyph-uploader
```

### 4. Enable required permissions  
Under **Scopes**, check:

```
[x] repo
    [x] repo:status
    [x] repo_deployment
    [x] public_repo
    [x] repo:invite
```

If working with private repos:
```
[x] repo
```

### 5. Generate → copy token  
Paste into the Colab prompt:

```
🔑 GitHub Personal Access Token:
```

## 📁 Output Structure (GitHub)
```
📂 glyph-library/
 ├── 📂 glyphs/
 │    ├── ff7711_20250101_153344_a1b2c3.png
 │    ├── 22cc99_20250101_153345_9fa221.png
 │    └── ...
 ├── 📂 data/
 │    ├── glyphs-data.json
 │    └── glyphs.js
 └── README.md
```

## 🧠 Example Metadata (`glyphs-data.json`)

```json
{
  "id": "c1a2f3b4",
  "filename": "ffcc11_20250101_123456_c1a2f3b4.png",
  "glyph_url": "https://raw.githubusercontent.com/<user>/<repo>/main/glyphs/ffcc11_20250101_123456_c1a2f3b4.png",
  "color": {
    "hex": "ffcc11",
    "name": "yellow",
    "rgb": [255, 204, 17],
    "lab": [82.1, 12.4, 78.6]
  },
  "metrics": {
    "edge_density": 0.054,
    "entropy": 5.91,
    "texture": 0.024,
    "contrast": 0.31,
    "circularity": 0.67,
    "aspect_ratio": 1.25,
    "edge_angle": 72.4
  },
  "color_harmony": "analogous",
  "mood": "playful",
  "timestamp": { "date": "2025-01-01", "time": "12:34:56" }
}
```

## 🐛 Troubleshooting

- Gallery is empty?: `data/glyphs-data.json` exists
- Check browser console (F12) for fetch errors

#### Validate JSON
Before uploading, validate your JSON:
- Use https://jsonlint.com/
- Or run: `python -m json.tool data/glyphs-metadata.json`

#### Version Control
Keep `glyphs.js` as backup:
- Python script generates both files
- `glyphs-data.json` = used by gallery
- `glyphs.js` = backup/reference
