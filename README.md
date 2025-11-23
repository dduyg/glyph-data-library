<div align="center">
    <h1>glyph-data-library</h1>
    <img src="https://cdn.jsdelivr.net/gh/dduyg/LiminalLoop@shelf/06/BLOBs/blob-36.png" width="882" />
    <p align="center">
        Interactive 3D glyph library ready for use..
    </p>
    <p align="center">
       View Dynamic Gallery
    </p>
</div>

#### Integration
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
