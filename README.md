# glyph-data-library
Interactive 3D glyph library ready for use.

### 🔗 Integration
Works with: D3.js, Plotly, Chart.js, Three.js, React, Vue, Observable

# 📋 Guide

### Export Options
1. **📋 Copy Dataset**: Copies JSON to clipboard
2. **💾 Download JSON**: Downloads as file
3. **✕ Clear**: Deselects all

## 🎯 File Naming Convention

Your script generates filenames like:
```
{hexcolor}_{YYYYMMDD_HHMMSS}_{uuid}.png
```

**Examples**:
- `667eea_20241121_120000_a1b2c3d4.png`
- `ff6b6b_20241121_143000_e5f6g7h8.png`
- `2ecc71_20241121_150000_i9j0k1l2.png`


## 🐛 Troubleshooting

### Images not loading?
- ✅ Repository must be **PUBLIC**
- ✅ Check image URLs in GLYPH_DATA match GitHub structure
- ✅ Files must be in `glyphs/` folder
- ✅ Use `raw.githubusercontent.com` URLs (not `github.com`)

### Color search not working?
- ✅ Ensure LAB values are in data
- ✅ Check browser console (F12) for errors
- ✅ Verify hex codes start with `#`

### Script upload fails (Option 2)?
- ✅ Token needs **repo** permissions
- ✅ Generate token at: https://github.com/settings/tokens
- ✅ Use **Fine-grained tokens** or **Classic** with full repo access

### Gallery is empty?
- ✅ Check that `data/glyphs-metadata.json` exists
- ✅ Verify JSON file is valid (use JSONLint.com)
- ✅ Check browser console (F12) for fetch errors
- ✅ Ensure file path is correct relative to index.html

## 📦 What the Script Generates

### From `glyph_processor.py`:
- ✅ Renamed PNG files with unique IDs
- ✅ `glyphs-metadata.json` (complete metadata)
- ✅ `glyph-data.js` (ready-to-paste JavaScript)
- ✅ Color extraction using K-means clustering
- ✅ LAB color space values for accurate search

### Gallery Features:
- ✅ Perceptual color similarity search (LAB)
- ✅ Color-based similarity search
- ✅ Unique timestamped filenames
- ✅ LAB color space accuracy
- ✅ Auto-upload to GitHub option
- ✅ Beautiful interactive gallery
- ✅ Easy dataset export


# Automatic Data Loading

### 🔄 Adding New Glyphs

#### 📊 Data Flow
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

## 🐛 Common Issues

### Validate JSON
Before uploading, validate your JSON:
- Use https://jsonlint.com/
- Or run: `python -m json.tool data/glyphs-metadata.json`

### Version Control
Keep `glyphs.js` as backup:
- Python script generates both files
- `glyphs-data.json` = used by gallery
- `glyphs.js` = backup/reference
