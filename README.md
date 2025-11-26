<div align="center">
    <h1>Glyph data library</h1>
    <a href="#🔍"><img src="https://cdn.jsdelivr.net/gh/dduyg/LiminalLoop@shelf/06/BLOBs/blob-36.png" height="250"></a>
       <p align="center">
        <a href="#🔍">
            <img src="https://img.shields.io/badge/View%20Dynamic%20Gallery-D9D0D7?style=for-the-badge&logo=eight&logoColor=white"></a>
    </p>
    <samp align="center">
        A fully automated pipeline that extracts quantitative and semantic visual features from glyph images and transforms them into tagged, searchable metadata objects for storage and retrieval.
    </samp>
</div><br><br>

### 🔍Features:
- Dominant color extraction using K-means
- Perceptual color similarity search (LAB) color conversion & semantic color grouping
- Edge density, entropy, texture complexity (LBP) 
- Shape circularity, aspect ratio  
- Edge orientation & contrast  

#### 🌀 Mood classification
The script assigns one of nine moods (serene, calm, energetic, chaotic, mysterious, futuristic, minimalistic, dramatic, playful) based on a few decision rules:

| Mood | Rule |
|---|---|
| Serene | Low entropy (<4), low edge density (<0.05), soft colors, low saturation |
| Calm | Low entropy (<5), moderate edge density (<0.08), pastel or cool hues |
| Energetic | High saturation (>0.45), warm colors, moderate complexity (entropy 4–6) |
| Chaotic | High entropy (>6), high edge density (>0.15), irregular shapes |
| Mysterious | Dark brightness (<90), cool colors (blue/purple), medium entropy (4–6) |
| Futuristic | Bright (>150), cool hue (blue/purple), low to moderate saturation (<0.35) |
| Minimalistic | Low entropy (<3.5), very low edge density (<0.03), simple shapes |
| Dramatic | High contrast, moderate to high entropy (5–7), bold warm colors |
| Playful | Medium entropy (4–6), bright colors, irregular or whimsical shapes |

## 🏛 Output Structure
- `glyphs.catalog.json`:

  Full metadata registry

- `glyphs.catalog.csv`:

  Human-readable dataset.

- <samp>glyphs/</samp>

  Auto-renamed glyph files.

- <samp>data/</samp>

  Metadata files stored for versioning.

## 📋 Getting Started

1️⃣ Run the script, and it will prompt you to select images for processing

<br>

2️⃣ Enter GitHub Settings:
```
👾 GitHub username:  ....
🗃️ GitHub repo name: ....
🌿 Branch name: main (default)
```
*If the repository doesn’t exist, the script will create it.*

<br>

3️⃣ Choose Output Mode:
```
1 - Save locally as ZIP archive
2 - Commit directly to GitHub
```

## 🌀 Committing to GitHub
```
glyphs/ → images  
data/   → metadata (JSON + JS)
```
- All metadata is incremental — repeated runs expand the library
- jsDelivr CDN URLs generated automatically

### 🔐 How to Create a GitHub Personal Access Token:
1.  Go to: https://github.com/settings/tokens
2.  Click **“Generate new token (classic)”**
4.  Give it a name, e.g., *"Glyph Pipeline Token"*
5.  Enable these permissions:
    -   `repo` (full control of private/public repos)
6.  Generate & copy the token (you won't see it again)
8.  Enter it when the script requests:
```
🔑 GitHub Personal Access Token:
```

## 🧪 Integration
This makes it perfect for web projects, galleries, or ML datasets.
 
- Machine learning feature datasets
- Visual search systems    
- Generative AI training datasets
- building large glyph/icon libraries  
- color–based classification  
- texture/shape analysis  
- automated repository-based asset libraries  
- generating structured datasets for ML/AI research

## 🐛 Troubleshooting
- Gallery is empty?: `data/glyphs-data.json` exists
- Check browser console (F12) for fetch errors
- Before uploading, validate your JSON. Use https://jsonlint.com/ or run: `python -m json.tool data/glyphs-data.json`
