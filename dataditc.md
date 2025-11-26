### `mood`
- **Type**: String (categorical)
- **Possible Values**: `"minimalistic"`, `"futuristic"`, `"mysterious"`, `"energetic"`, `"organic"`, `"serene"`
- **Example**: `"energetic"`
- **Description**: Aesthetic mood computed from color, entropy, edge density, and texture
- **Classification Rules**:
  - **minimalistic**: Low entropy (<4), low edges (<0.05), low saturation (<0.25)
  - **futuristic**: Blue hue (>200°), bright (>170), low saturation (<0.25)
  - **mysterious**: Dark (<80), cool hues (>180°)
  - **energetic**: High saturation (>0.5), moderate entropy (<6)
  - **organic**: High texture (>1.6), high entropy (>6)
  - **serene**: Default fallback
- **Use Cases**: Mood-based browsing, thematic collections, emotional design matching

## Timestamps

### `created_at.date`
- **Type**: String (ISO 8601 date)
- **Format**: `YYYY-MM-DD`
- **Example**: `"2024-11-25"`
- **Description**: UTC date when glyph was processed

### `created_at.time`
- **Type**: String (ISO 8601 time)
- **Format**: `HH:MM:SS`
- **Example**: `"14:30:22"`
- **Description**: UTC time when glyph was processed

### 6. **Machine Learning Features**
All numeric metrics can serve as feature vectors for:
- Similarity search
- Clustering
- Style classification
- Recommendation system
