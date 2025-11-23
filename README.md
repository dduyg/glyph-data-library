<div align="center">
    <h1>glyph-data-library</h1>
    <img src="https://cdn.jsdelivr.net/gh/dduyg/LiminalLoop@shelf/06/BLOBs/blob-36.png" height="250" />
    <p align="center">
        Interactive 3D glyph library ready for use..
    </p>
    <p align="center">
       View Dynamic Gallery
    </p>
</div>

#### Integration
Works with: D3.js, Plotly, Chart.js, Three.js, React, Vue, Observable

<p align="center">
  Automated Glyph Image Analysis → Renaming → Color Extraction → Metadata Generation → GitHub Publishing
</p>

**Glyph Processor** is a complete automation pipeline for transforming glyph-like PNG images into fully tagged and searchable metadata objects.  
It extracts color information, visual metrics, shapes, and aesthetic "moods," then renames images with a unique hash and exports everything to:

- A **local ZIP**, or  
- A **GitHub repository**, organized as:
  ```
  glyphs/ → images  
  data/   → metadata (JSON + JS)
  ```

This makes it perfect for:
- Procedural graphics datasets  
- Generative art archives  
- Glyph/icon catalogs  
- Machine learning image labeling  
- Automated asset libraries  

---

## ✨ Features

### 🎨 Color Analysis
- Dominant color detection (K-Means)
- Secondary color extraction
- HEX, RGB, LAB → computed for each glyph
- Color naming (categorical)
- Color harmony classification (analogous / complementary / none)

### 🧠 Image Metrics
- Edge density
- Shannon entropy
- Texture complexity (LBP)
- Contrast normalization
- Shape metrics (circularity + aspect ratio)
- Edge orientation

### 🌀 Mood Classification (rule-based)
Examples:
- **minimalistic**
- **serene**
- **chaotic**
- **mysterious**
- **playful**
- **dramatic**
…and more.

### 🔧 File Handling
- Automatically generates unique names:
  ```
  <hex>_<timestamp>_<uuid>.png
  ```
- Creates:
  - `glyphs-data.json`
  - `glyphs.js` (JavaScript-ready dataset)

### 🛠 GitHub Automation
- Uploads images → `glyphs/`  
- Uploads metadata → `data/`  
- Creates repo automatically if missing  
- Updates existing files incrementally  

# Automatic Data Loading

### 🔄 Data Flow
```
Python Script
    ↓
Generates: glyphs-data.json
    ↓
Auto-load to repo/data/
    ↓
index.html fetches from: data/glyphs-data.json
    ↓
Gallery displays glyphs ✨
```

