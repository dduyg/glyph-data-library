<div align="center">
    <h1>Glyph data library</h1>
    <a href="https://dduyg.github.io/glyph-data-library"><img src="https://cdn.jsdelivr.net/gh/dduyg/glyph-data-library@main/glyphs/cdd4d4_6f93b9_5bd11dc3.png" height="250"></a>
       <p align="center">
        <a href="https://dduyg.github.io/glyph-data-library">
            <img src="https://img.shields.io/badge/View%20Dynamic%20Gallery-D9D0D7?style=for-the-badge&logo=eight&logoColor=white"></a>
    </p>
    <samp align="center">
        An automated image processing pipeline that extracts quantitative metrics and semantic visual features from PNG glyph images, transforming raw visual data into rich, searchable data objects for analysis and retrieval.
    </samp>
</div><br><br>

#### 🔍Features:
- <sub>*Color Intelligence*: K-means color clustering extracts dominant/secondary palette with hex, RGB, and LAB color space representations for similarity search & semantic color grouping</sub>
- <sub>*Computing Quantitative Visual Metrics*: edge density, entropy, texture complexity, contrast, shape analysis, edge orientation</sub>
- <sub>*Aesthetic Profiling*: Evaluates color harmony and mood classification (serene, playful, energetic, mysterious, dramatic, etc.)</sub>
- <sub>Incremental updates stored in JSON and CSV for continuous library expansion</sub>

<br>

## 📜 Workflow Inputs

#### 💠 𝘎𝘭𝘺𝘱𝘩 𝘍𝘦𝘢𝘵𝘶𝘳𝘦 𝘗𝘪𝘱𝘦𝘭𝘪𝘯𝘦
| Input | Default | Description |
|---|---|---|
| `sources` | *required* | `repo-name:folder`, comma-separated |
| `clear_source` | `false` | Delete cache of source glyphs (after cataloging) |
| `max_workers` | `10` | Parallel worker threads |
| `kmeans_k` | `3` | K-means clusters for color extraction |

#### 🪜 ℝ𝕒𝕨 → Glyph Feature Pipeline
| Input | Default | Description |
|---|---|---|
| `sources` | *required* | `repo-name:folder`, comma-separated |
| `target_width` | `900` | Target width in px (aspect ratio preserved) |
| `remove_originals` | `true` | Delete `.jpg`/`.webp`/… originals after converting them to `.png` |
| `run_pipeline` | `true` | ⬢ RUN > 🪜💠 Glyph Feature Pipeline with resized glyphs |
| `clear_source` | `false` | Delete cache of resized glyphs (after cataloging) |

> [!IMPORTANT]
> → Use PNGs with transparency; opaque backgrounds skew color detection (alpha channel required for accurate masking)<br>
> → Only files directly inside the folder are read (not subfolders). Folder names are matched case-insensitively; if nothing is found, the run lists which folders do contain images.

#### 🪢 Wait for processing
   - Glyphs are fetched and processed in parallel
   - Processed glyphs are committed to `glyphs/`
   - `data/glyphs.catalog.json` and `data/glyphs.catalog.csv` are generated or updated
   - The run page shows a **▓▓▓ PROCESS.SUMMARY ⟫⟫⟫** with a clickable commit link

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
 │   ├── 550 + 52 = 602 glyphs in total
 │   └── 2 catalogs updated [CSV + JSON]
```

<br>

## 🔠 Data Dictionary
For detailed metric explanations and fields, see [data_dictionary.md](data_dictionary.md).

<br>

## 🧪 Integration
This makes it perfect for data/web projects, automated asset galleries, ML datasets, visual search & recommendation systems, building query interfaces, and data visualization assets. Experiment with texture coding (high-entropy glyphs for complex data, low-entropy for simple patterns), A/B test visual assets by tracking performance of different aesthetic profiles, or generate combinations based on category to discover unexpected visual relationships.

<br>

---
Built by Duygu Dağdelen, *architecting with creativity*
<br><samp>__Version: 1.2.0 (2026-09-23)</samp>
