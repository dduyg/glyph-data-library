# Glyph Processor

**Automated visual analysis and cataloging system for PNG glyphs with color extraction, metrics computation, and GitHub deployment.**

---

## Overview

The Glyph Processor analyzes PNG images to extract comprehensive visual metadata including color profiles, shape characteristics, texture metrics, and aesthetic properties. It generates a searchable catalog with CDN-hosted images, perfect for building design systems, icon libraries, or visual asset management tools.

---

## Features

### 🎨 **Color Analysis**
- Dominant and secondary color extraction via K-means clustering
- Semantic color grouping (red, blue, gold, silver, etc.)
- RGB and perceptually-uniform LAB color space values
- Color harmony detection (analogous/complementary)

### 📊 **Visual Metrics**
- **Edge Density**: Measures detail and complexity (0.0–1.0)
- **Entropy**: Quantifies visual variation (0.0–8.0)
- **Texture Complexity**: Analyzes surface patterns via Local Binary Patterns
- **Contrast**: Michelson contrast formula for luminance range (0.0–1.0)
- **Circularity**: Shape roundness (0.0–1.0, where 1.0 = perfect circle)
- **Aspect Ratio**: Width-to-height proportion
- **Edge Angle**: Dominant orientation of edges (0–180°)

### 🎭 **Aesthetic Classification**
- **Mood Detection**: Automatically categorizes glyphs as minimalistic, futuristic, mysterious, energetic, organic, or serene
- **Color Harmony Analysis**: Identifies harmonious color relationships

### 📦 **Export & Deployment**
- **JSON Catalog**: Structured metadata with nested fields
- **CSV Export**: Flattened format for spreadsheet analysis
- **GitHub Integration**: Automated batch uploads to repository
- **CDN Hosting**: jsDelivr URLs for instant web access

---

## Installation

### Requirements
- Python 3.7+
- Google Colab (or local Jupyter environment)
- GitHub account (for deployment)

### Dependencies
The script auto-installs required packages:
```bash
opencv-python-headless
scikit-learn
scikit-image
PyGithub
```

---

## Usage

### 1. **Prepare Your Images**
- Format: PNG with transparency (RGBA)
- Recommended: Clean, well-cropped glyphs with alpha channels
- Any resolution (processor handles all sizes)

### 2. **Run the Script**
In Google Colab or Jupyter:

```python
# The script will prompt you to upload images
# Upload one or more PNG files when prompted
```

### 3. **Configure GitHub Deployment**
When prompted, provide:
- **GitHub username**: Your GitHub username (e.g., `johndoe`)
- **Repository name**: Target repo (e.g., `my-glyph-library`)
- **Branch**: Branch name (default: `main`)

### 4. **Choose Export Method**

**Option 1: Download ZIP**
- Downloads a local archive with:
  - Processed PNG files (renamed with metadata)
  - `glyphs.catalog.json`
  - `glyphs.catalog.csv`

**Option 2: Upload to GitHub**
- Requires GitHub Personal Access Token (see below)
- Creates repository structure:
  ```
  repo/
  ├── glyphs/           # PNG files
  │   └── ff5733_20241125_143022_a3f7c21b.png
  └── data/             # Metadata files
      ├── glyphs.catalog.json
      └── glyphs.catalog.csv
  ```

---

## Getting a GitHub Personal Access Token

### Step 1: Navigate to Token Settings
1. Go to [github.com](https://github.com) and sign in
2. Click your profile picture (top-right) → **Settings**
3. Scroll down to **Developer settings** (bottom-left sidebar)
4. Click **Personal access tokens** → **Tokens (classic)**

### Step 2: Generate New Token
1. Click **Generate new token** → **Generate new token (classic)**
2. Add a note: `Glyph Processor Upload`
3. Set expiration: Choose duration (recommend 30-90 days)
4. Select scopes:
   - ✅ **repo** (all sub-options)
   - ✅ **workflow** (if using GitHub Actions)

### Step 3: Generate and Copy
1. Click **Generate token** at the bottom
2. **⚠️ COPY THE TOKEN IMMEDIATELY** (you won't see it again)
3. Store securely (password manager recommended)

### Step 4: Use in Script
When the script prompts for "GitHub token", paste your token (input will be hidden).

---

## Output Files

### `glyphs.catalog.json`
Structured JSON with nested metadata:
```json
{
  "total": 3,
  "glyphs": [
    {
      "id": "a3f7c21b",
      "filename": "ff5733_20241125_143022_a3f7c21b.png",
      "glyph_url": "https://cdn.jsdelivr.net/gh/user/repo@main/glyphs/ff5733_20241125_143022_a3f7c21b.png",
      "color": {
        "hex": "ff5733",
        "group": "orange",
        "rgb": [255, 87, 51],
        "lab": [58.23, 52.14, 48.76]
      },
      "metrics": { ... },
      "color_harmony": "analogous",
      "mood": "energetic",
      "created_at": {
        "date": "2024-11-25",
        "time": "14:30:22"
      }
    }
  ]
}
```

### `glyphs.catalog.csv`
Flattened spreadsheet format with all fields as columns:
```csv
id,filename,glyph_url,color_hex,color_group,color_rgb,edge_density,entropy,...
a3f7c21b,ff5733_2024...,https://...,ff5733,orange,"[255, 87, 51]",0.1823,5.2341,...
```

### Processed PNG Files
- **Naming**: `{hex_color}_{YYYYMMDD_HHMMSS}_{id}.png`
- **Example**: `ff5733_20241125_143022_a3f7c21b.png`
- **Sorting**: Alphabetical by hex color for quick browsing

---

## Use Cases

### 🎨 **Design Systems**
- Build searchable icon libraries with color-coded organization
- Filter by mood, style, or visual complexity
- Ensure consistent visual language across products

### 🖼️ **Asset Management**
- Catalog large collections of visual assets
- Search by color, shape, or aesthetic properties
- Track asset creation timestamps

### 🔍 **Visual Search Engines**
- Power similarity search using LAB color space
- Find glyphs by mood, harmony, or metrics
- Build recommendation systems based on visual features

### 🤖 **Machine Learning Datasets**
- Use extracted metrics as feature vectors
- Train style classifiers or clustering models
- Analyze visual trends in design

### 🌐 **Web Development**
- Instant CDN access via jsDelivr URLs
- Dynamic icon selection based on metadata
- API endpoints for design tools

### 📱 **App Development**
- Programmatic asset selection by visual properties
- Adaptive UI based on color groups
- Accessibility checks using contrast values

---

## Library Expansion

The processor intelligently handles incremental updates:

1. **First Run**: Creates new catalog from uploaded images
2. **Subsequent Runs**: 
   - Fetches existing `glyphs.catalog.json` from GitHub
   - Processes new images
   - Merges with existing catalog
   - Uploads combined dataset

**Example Output**:
```
🎊 ALL DONE! Library successfully expanded to 247 glyphs in total.
```

---

## Data Dictionary

For detailed explanations of all metrics and fields, see [DATA_DICTIONARY.md](DATA_DICTIONARY.md).

Quick reference:
- **Contrast 0.0–0.15**: Flat/solid colors
- **Contrast 0.35–0.65**: Moderate detail
- **Contrast 0.90–1.0**: Extreme (black + white)
- **Circularity 0.0–0.3**: Irregular shapes
- **Circularity 0.7–1.0**: Circular shapes
- **Edge Density 0.0–0.1**: Minimal detail
- **Edge Density 0.5–1.0**: High detail

---

## Technical Details

### Color Extraction
- **Algorithm**: K-means clustering (k=3)
- **Space**: RGB for extraction, LAB for perceptual analysis
- **Masking**: Only analyzes opaque pixels (alpha > 10)

### Metrics Computation
- **Edge Detection**: Canny (thresholds: 80, 160)
- **Entropy**: Shannon entropy on grayscale
- **Texture**: Local Binary Pattern (8 neighbors, radius 1)
- **Contrast**: Michelson formula `(I_max - I_min) / (I_max + I_min)`
- **Shape**: OpenCV contour analysis

### GitHub Upload
- **Batch Processing**: Single commit for all files
- **Tree Creation**: Git tree API for efficiency
- **CDN**: jsDelivr automatically caches from GitHub

---

## Troubleshooting

### "GitHub Error: 404 Not Found"
- Verify repository exists and is public (or token has access to private repos)
- Check token permissions include `repo` scope

### "No dominant color found"
- Ensure PNGs have visible pixels (not fully transparent)
- Check alpha channel integrity

### "Rate limit exceeded"
- GitHub API has rate limits; wait an hour or use authenticated requests

### "Module not found"
- Ensure you run the `!pip install` line at the top of the script
- Restart runtime if needed

---

## Examples

### Build a Color-Coded Icon Library
```python
# Filter orange glyphs from catalog
import json

with open('glyphs.catalog.json') as f:
    data = json.load(f)

orange_glyphs = [g for g in data['glyphs'] if g['color']['group'] == 'orange']
print(f"Found {len(orange_glyphs)} orange glyphs")
```

### Find High-Contrast Icons
```python
high_contrast = [g for g in data['glyphs'] if g['metrics']['contrast'] > 0.7]
```

### Build a Mood-Based Gallery
```python
energetic = [g for g in data['glyphs'] if g['mood'] == 'energetic']
```

---

## Roadmap

- [ ] Semantic tagging via CLIP embeddings
- [ ] Duplicate detection based on perceptual hashing
- [ ] Batch processing of SVG files
- [ ] REST API for metadata queries
- [ ] Interactive web viewer with filtering

---

## Contributing

Contributions welcome! Areas for improvement:
- Additional mood classification rules
- More sophisticated color harmony detection
- Performance optimization for large batches
- Alternative storage backends (S3, Firebase, etc.)

---

## License

MIT License - feel free to use in personal or commercial projects.

---

## Credits

Built with:
- [OpenCV](https://opencv.org/) - Computer vision
- [scikit-learn](https://scikit-learn.org/) - K-means clustering
- [scikit-image](https://scikit-image.org/) - Image processing
- [PyGithub](https://pygithub.readthedocs.io/) - GitHub API
- [jsDelivr](https://www.jsdelivr.com/) - CDN hosting

---

## Support

For detailed metric explanations, see [DATA_DICTIONARY.md](DATA_DICTIONARY.md).

For issues or questions, open an issue on GitHub or contact the maintainer.
