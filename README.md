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
- Mo..

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

## Library Expansion
The pipeline intelligently handles incremental updates:
1. **First Run**: Creates new catalog from uploaded images
2. **Subsequent Runs**: 
   - Fetches existing `glyphs.catalog.json` from GitHub
   - Processes new images
   - Merges with existing catalog
   - Uploads combined dataset

**Example Output**:
```
🎊 ALL DONE! Library successfully expanded to 227 glyphs in total.
```

## Data Dictionary
For detailed metric explanations and fields, see [DATA_DICTIONARY.md](DATA_DICTIONARY.md).

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
