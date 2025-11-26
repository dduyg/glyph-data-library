## 📊 **Visual Metrics**
- **Edge Density**: Measures detail and complexity (0.0–1.0)
- **Entropy**: Quantifies visual variation (0.0–8.0)
- **Texture Complexity**: Analyzes surface patterns via Local Binary Patterns
- **Contrast**: Michelson contrast formula for luminance range (0.0–1.0)
- **Circularity**: Shape roundness (0.0–1.0, where 1.0 = perfect circle)
- **Aspect Ratio**: Width-to-height proportion
- **Edge Angle**: Dominant orientation of edges (0–180°)

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

## Use Cases

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
