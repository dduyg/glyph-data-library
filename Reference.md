# Automatic Data Loading

### 🔄 Adding New Glyphs

#### 📊 Data Flow
```
Python Script (Colab)
    ↓
Generates: glyphs-metadata.json
    ↓
Upload to: GitHub repo/data/
    ↓
index.html fetches from: data/glyphs-metadata.json
    ↓
Gallery displays glyphs ✨
```

## 🐛 Common Issues

### Gallery shows "Loading..." forever?

**Check:**
1. Open browser console (F12)
2. Look for fetch errors
3. Verify `data/glyphs-metadata.json` exists
4. Check file path is correct

**Fix:**
- Ensure file is in `data/` folder
- File must be named exactly `glyphs-metadata.json`
- Check repo is public (for GitHub Pages)

### "Failed to load glyph data" error?

**Possible causes:**
- File doesn't exist at `data/glyphs-metadata.json`
- JSON syntax error (use JSONLint to validate)
- Wrong folder structure
- Repo is private (must be public for GitHub Pages)

**Fix:**
- Check file path in repo
- Validate JSON syntax
- Make repo public
- Clear browser cache

### New glyphs not appearing?

**Solution:**
1. **Hard refresh** the page:
   - Windows/Linux: `Ctrl + Shift + R`
   - Mac: `Cmd + Shift + R`
2. Or clear browser cache
3. Verify new glyphs are in `data/glyphs-metadata.json`

---

## 💡 Pro Tips

### Tip 1: Validate JSON
Before uploading, validate your JSON:
- Use https://jsonlint.com/
- Or run: `python -m json.tool data/glyphs-metadata.json`

### Tip 2: Version Control
Keep `glyph-data.js` as backup:
- Python script generates both files
- `glyphs-metadata.json` = used by gallery
- `glyph-data.js` = backup/reference

### Tip 3: CDN Loading
You can also load from CDN for better performance:

```javascript
// In index.html, change fetch URL to:
const response = await fetch(
  'https://cdn.jsdelivr.net/gh/username/repo@main/data/glyphs-metadata.json'
);
```
