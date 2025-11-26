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

---

## Data Dictionary

For detailed metric explanations and fields, see [DATA_DICTIONARY.md](DATA_DICTIONARY.md).
