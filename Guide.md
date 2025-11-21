# 📋 Setup Guide

### 🎨 Color Search
- **Color Picker**: Click to choose color visually
- **Hex Input**: Type exact hex code (e.g., `#B27D74`)
- **Tolerance Slider**: 
  - `5-15`: Nearly identical colors
  - `20-35`: Similar shades (recommended)
  - `40-60`: Same color family
  - `70+`: Broad matches

### 🔍 Search Results
- Automatically sorted by color similarity
- Shows **Similarity Δ** value (lower = more similar)
- Color badge and hex code displayed
- Color family name tag

### 📦 Selection & Export

**Single Click** (no modifier key):
- Instantly copies glyph URL to clipboard
- Toast notification confirms copy

**Multi-Select** (Shift/Ctrl/Cmd + Click):
- Green border indicates selection
- Selection bar appears at bottom
- Can select multiple glyphs

**Export Options**:
1. **📋 Copy Dataset**: Copies JSON to clipboard
2. **💾 Download JSON**: Downloads as file
3. **✕ Clear**: Deselects all

---

## 🎯 Usage Examples

### In Data Visualization (D3.js)
```javascript
// Search for red glyphs
const redGlyphs = GLYPH_DATA.filter(g => g.colorName === 'red');

// Use in D3
d3.select('svg')
  .selectAll('image')
  .data(redGlyphs)
  .enter()
  .append('image')
  .attr('href', d => d.glyph_url)
  .attr('x', (d, i) => i * 50)
  .attr('width', 40);
```

### In React
```jsx
function GlyphMarker({ color }) {
  const glyph = GLYPH_DATA.find(g => g.hex === color);
  return <img src={glyph.glyph_url} alt={glyph.colorName} />;
}
```

### In Plotly
```javascript
const trace = {
  x: [1, 2, 3],
  y: [10, 15, 13],
  mode: 'markers',
  marker: {
    size: 50,
    symbol: GLYPH_DATA.map(g => g.glyph_url)
  }
};
```

---

## 🔧 File Naming Convention

Your script generates filenames like:
```
{hexcolor}_{YYYYMMDD_HHMMSS}_{uuid}.png
```

**Examples**:
- `667eea_20241121_120000_a1b2c3d4.png`
- `ff6b6b_20241121_143000_e5f6g7h8.png`
- `2ecc71_20241121_150000_i9j0k1l2.png`

**Benefits**:
- ✅ Unique filename (UUID prevents collisions)
- ✅ Timestamp for tracking when added
- ✅ Hex color visible in filename
- ✅ No overwrites (re-running creates new files)

---

## 🚀 Quick Commands

### Initial Setup
```bash
# Clone your repo
git clone https://github.com/your-username/glyph-library.git
cd glyph-library

# Create folders (if not using auto-upload)
mkdir -p glyphs data

# Add files and push
git add .
git commit -m "Initial glyph library"
git push origin main
```

### Adding New Glyphs
```bash
# If using script Option 2 - it handles everything automatically!
# Just re-run the Colab script with new images

# If manual:
# Add new processed images
cp ~/Downloads/output_glyphs/*.png glyphs/

# Replace metadata file
cp ~/Downloads/output_glyphs/glyphs-metadata.json data/

# Commit
git add glyphs/ data/
git commit -m "Add 20 new glyphs"
git push origin main

# Refresh your gallery page - new glyphs appear!
```

---

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

---

## 📦 What the Script Generates

### From `glyph_processor.py`:
- ✅ Renamed PNG files with unique IDs
- ✅ `glyphs-metadata.json` (complete metadata)
- ✅ `glyph-data.js` (ready-to-paste JavaScript)
- ✅ Color extraction using K-means clustering
- ✅ LAB color space values for accurate search

### Gallery Features:
- ✅ Perceptual color similarity search (LAB)
- ✅ Adjustable tolerance slider
- ✅ Single-click URL copy
- ✅ Multi-select with Shift/Ctrl
- ✅ Export as JSON dataset
- ✅ Responsive grid layout
- ✅ Beautiful animations
- ✅ Empty state handling

---

## 🌐 Live URLs

After setup, your URLs will be:

**Gallery Page**:
```
https://your-username.github.io/glyph-library/
```

**Direct Image Access** (for code):
```
https://raw.githubusercontent.com/your-username/glyph-library/main/glyphs/667eea_20241121_120000_a1b2c3d4.png
```

**Metadata**:
```
https://raw.githubusercontent.com/your-username/glyph-library/main/data/glyphs-metadata.json
```

---

## 💡 Pro Tips

### Color Tolerance Guide
- Use **20-30** for finding similar colors to your search
- Use **40-60** for broader color family searches
- Use **5-15** for nearly exact color matches

### Selecting Multiple Glyphs
- **Shift + Click**: Add to selection
- **Ctrl/Cmd + Click**: Toggle individual items
- Select, then export to get subset of glyphs

### K-means Color Detection
- Script uses **3 clusters** by default
- Finds dominant color by largest surface area
- Ignores transparent and near-white pixels
- More accurate than simple average

### Organizing by Date
- Filenames include timestamp
- Easy to track when glyphs were added
- Can filter by date in custom code

---

## 🎉 You're Ready!

Your glyph library now has:
- ✅ Color-based similarity search
- ✅ Unique timestamped filenames
- ✅ LAB color space accuracy
- ✅ Auto-upload to GitHub option
- ✅ Beautiful interactive gallery
- ✅ Easy dataset export
- ✅ One-click URL copying
