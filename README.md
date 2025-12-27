<div align="center">
    <h1>Glyph data library</h1>
    <a href="https://dduyg.github.io/glyph-data-library"><img src="https://cdn.jsdelivr.net/gh/dduyg/LiminalLoop@shelf/06/BLOBs/blob-36.png" height="250"></a>
       <p align="center">
        <a href="https://dduyg.github.io/glyph-data-library">
            <img src="https://img.shields.io/badge/View%20Dynamic%20Gallery-D9D0D7?style=for-the-badge&logo=eight&logoColor=white"></a>
    </p>
    <samp align="center">
        A fully automated image processing pipeline that extracts quantitative metrics and semantic visual features from simple PNG glyph images and transforms them into rich, searchable data objects for storage and retrieval.
    </samp>
</div><br><br>

#### 🔍Features:
- <sub>*Color Intelligence*: K-means color clustering extracts dominant/secondary palette with hex, RGB, and LAB color space representations for similarity search & semantic color grouping</sub>
- <sub>*Computing Quantitative Visual Metrics*: edge density, entropy, texture complexity, contrast, shape analysis, edge orientation</sub>
- <sub>*Aesthetic Profiling*: Evaluates color harmony and mood classification (serene, playful, energetic, mysterious, dramatic, etc.)</sub>
- <sub>Incremental updates stored in JSON and CSV for continuous library expansion</sub>
- <sub>*Automated Storage*: Commits processed glyphs + structured data (JSON/CSV) directly to GitHub via API</sub>

<br>

## 🏛 Output Structure
```
repo-name/
├── glyphs/
│   ├── ff5733_a8f3e1b9.png
│   ├── 3498db_c2d4e5f6.png
│   └── ... (all processed glyphs with auto-renamed color-coded filenames)
│
└── data/
    ├── glyphs.catalog.json  # Structured data registry
    └── glyphs.catalog.csv   # Flat table for analysis
```

<br>

## 📜 Getting Started

1️⃣ Run the script `glyph_feature_pipeline.py`, which will prompt you to configure settings and select images for processing:

```
  ▓▓▓ INPUT.SOURCE.CONFIG   ⟫⟫⟫
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
▓▓▓▓▓▓▓▓▓ [1] →  SELECT.FROM.LOCAL.COMPUTER
▓▓▓▓▓▓▓▓▓ [2] →  FETCH.FROM.REPOSITORY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  [>] Select mode [1 or 2] >> .....
```
> <sub><em>→ Ensure PNGs with transparency; opaque backgrounds skew color detection (alpha channel required for accurate masking)</em></sub>

```
  ▓▓▓ STORAGE.CONFIG ⟫⟫⟫
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
━━━STORAGE_REPO  (username/repo-name)━━━
　　　＞ .....
━━━STORAGE_BRANCH  [default=main]━━━
　　　＞ .....

━━━ACCESS_TOKEN  [✦]
　　　＞ .....
```

> <sub><em>If repository doesn't exist, the pipeline will create it automatically with proper folder structure</em></sub>

<br>

2️⃣ Wait for processing
   - The pipeline processes all images in parallel
   - Commits processed glyphs to `glyphs/` folder
   - Generates or updates `data/glyphs.catalog.json` and `data/glyphs.catalog.csv`

<br>

> __🔐 How to Create a GitHub Personal Access Token:__
> 1.  Go to: https://github.com/settings/tokens
> 2.  Click **“Generate new token (classic)”**
> 3.  Give it a name, e.g., *"Glyph Pipeline Token"*
> 4.  Enable these permissions:
    -   `repo` (full control of private/public repos)
> 5.  Generate & copy the token (you won't see it again)
> 6.  Enter it when the script requests:
> ```
> ━━━ACCESS_TOKEN  [✦]
>    ＞ .....
> ```

<br>

## 🌱 Library Expansion
The pipeline intelligently handles incremental updates to expand the library:
1. **First Run**: Creates new catalog from processed images
2. **Subsequent Runs**: 
   - Fetches existing `glyphs.catalog.json` and `glyphs.catalog.csv`
   - Processes the new images
   - Merges with existing catalog
   - Uploads combined dataset

**Example Output**:
```
 ├── commit.type: LIBRARY.EXPANDED
 │   ├── 212 + 52 = 264 glyphs in total
 │   └── 2 catalogs updated [CSV + JSON]
```

<br>

## 🪢 Example workflows

```
STORAGE_REPO: myusername/myrepo
STORAGE_BRANCH: main
ACCESS_TOKEN: ghp_xxxxxxxxxxxx
Input: Selecting 150 PNG glyphs from local computer

→ Pipeline processes all images in parallel
→ Commits to myusername/myrepo:
   - glyphs/ff5733_a8f3e1b9.png
   - glyphs/3498db_c2d4e5f6.png
   - data/glyphs.catalog.json
   - data/glyphs.catalog.csv
```

#### ⚡︎ Fetch from another repository
```
# Fetch 1000+ glyphs from another repo
SOURCE_REPO: sourceuser/source-repo
SOURCE_BRANCH: develop
SOURCE_FOLDER: pending_glyphs

→ Pipeline streams directly to storage_repo
→ No local storage needed
```

<br>

> __🔧 Advanced Features__
> 
> <sub><samp>Adjust worker threads for faster parallel processing (default: max_workers=10):</samp></sub>
> ```python
> execute_glyph_pipeline(streamed, gh_user, gh_repo, token, branch, max_workers=20, fetch_skipped=fetch_skipped, input_mode=input_method, original_input_count=original_input_count)  # Default: 10
> ```
> 
> <sub><samp>Custom K-means Clustering, modify color extraction precision (default: k=5):</samp></sub>
> ```python
> compute_dominant_color(rgb, mask, k=8)  # Default: 5
> ```

<br>

## 🔠 Data Dictionary
For detailed metric explanations and fields, see [data_dictionary.md](data_dictionary.md).

<br>

## 🧪 Integration
This makes it perfect for data/web projects, automated asset galleries, ML datasets, visual search & recommendation systems, building query interfaces, and data visualization assets. Experiment with texture coding (high-entropy glyphs for complex data, low-entropy for simple patterns), A/B test visual assets by tracking performance of different aesthetic profiles, or generate combinations based on category to discover unexpected visual relationships.

<br>

---
Built by Duygu Dağdelen, *architecting with data-driven creativity*
<br><samp>__Version: 1.2.0 (2025-12-20)</samp>
