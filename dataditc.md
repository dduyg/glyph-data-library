### `metrics.texture`
- **Type**: Float
- **Range**: 0.0–3.5 (typical 0.5–2.5)
- **Example**: `1.4523`
- **Interpretation**:
  - **0.0–0.8**: Smooth surface (flat colors, clean vectors)
  - **0.8–1.5**: Slight texture (subtle gradients, soft shading)
  - **1.5–2.0**: Moderate texture (visible patterns, clear surface detail)
  - **2.0–2.5**: High texture (rough surfaces, intricate patterns)
  - **2.5+**: Very high texture (organic materials, complex surfaces)
- **Algorithm**: Local Binary Pattern (LBP) entropy with 8 neighbors, radius 1
- **Use Cases**: Distinguishing smooth vs. textured glyphs, material classification

### `metrics.contrast`
- **Type**: Float
- **Range**: 0.0–1.0
- **Example**: `0.6234`
- **Interpretation**:
  - **0.0–0.15**: Very low (solid colors, no shading)
  - **0.15–0.35**: Low (subtle gradients, soft lighting)
  - **0.35–0.65**: Moderate (visible detail, some shadows)
  - **0.65–0.90**: High (strong edges, clear shadows)
  - **0.90–1.0**: Extreme (black + white, stark silhouettes)
- **Formula**: Michelson contrast `(I_max - I_min) / (I_max + I_min)`
- **Use Cases**: Finding high-contrast icons, accessibility checks, visual impact sorting

### `metrics.circularity`
- **Type**: Float
- **Range**: 0.0–1.0
- **Example**: `0.7845`
- **Interpretation**:
  - **0.0–0.3**: Very irregular (complex shapes, jagged edges)
  - **0.3–0.5**: Somewhat irregular (stars, polygons)
  - **0.5–0.7**: Moderately round (rounded squares, ovals)
  - **0.7–0.9**: Highly circular (near-perfect circles)
  - **0.9–1.0**: Perfect circle
- **Formula**: `4π × area / perimeter²`
- **Use Cases**: Shape-based filtering, finding circular vs. angular designs

### `metrics.aspect_ratio`
- **Type**: Float
- **Range**: 0.0+ (typical 0.5–2.0)
- **Example**: `1.3456`
- **Interpretation**:
  - **< 0.5**: Very tall/narrow (vertical bars, portraits)
  - **0.5–0.8**: Moderately tall (portrait orientation)
  - **0.8–1.2**: Square-ish (balanced proportions)
  - **1.2–2.0**: Moderately wide (landscape orientation)
  - **> 2.0**: Very wide (horizontal bars, banners)
- **Formula**: `width / height` of bounding box
- **Use Cases**: Finding portrait vs. landscape glyphs, layout optimization

### `metrics.edge_angle`
- **Type**: Float
- **Range**: 0.0–180.0 (degrees)
- **Example**: `45.2300`
- **Interpretation**:
  - **0–22.5**: Horizontal emphasis
  - **22.5–67.5**: Diagonal emphasis (often dynamic, motion)
  - **67.5–112.5**: Vertical emphasis
  - **112.5–157.5**: Opposite diagonal
  - **157.5–180**: Horizontal (opposite direction)
- **Algorithm**: Median angle of strongest edges (top 25% by gradient magnitude)
- **Use Cases**: Finding glyphs with specific orientations, directional matching

---

## Aesthetic Properties

### `color_harmony`
- **Type**: String (categorical)
- **Possible Values**: `"analogous"`, `"complementary"`, `"none"`
- **Example**: `"analogous"`
- **Description**:
  - **analogous**: Dominant and secondary colors are within 30° on color wheel (harmonious)
  - **complementary**: Colors are ~180° apart on color wheel (high contrast)
  - **none**: No clear harmonic relationship
- **Use Cases**: Color palette generation, aesthetic filtering

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

---

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

---

## Data Formats

### JSON Structure
```json
{
  "total": 150,
  "glyphs": [
    {
      "id": "a3f7c21b",
      "filename": "ff5733_20241125_143022_a3f7c21b.png",
      "glyph_url": "https://cdn.jsdelivr.net/gh/user/repo@main/glyphs/...",
      "color": {
        "hex": "ff5733",
        "group": "orange",
        "rgb": [255, 87, 51],
        "lab": [58.23, 52.14, 48.76]
      },
      "metrics": {
        "edge_density": 0.1823,
        "entropy": 5.2341,
        "texture": 1.4523,
        "contrast": 0.6234,
        "circularity": 0.7845,
        "aspect_ratio": 1.3456,
        "edge_angle": 45.23
      },
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

## Common Use Cases

### 1. **Color-Based Search**
- Filter by `color.group` for semantic matching
- Use `color.lab` for perceptual distance calculations
- Sort by `color.hex` for hue-based organization

### 2. **Complexity Filtering**
- Combine `edge_density`, `entropy`, and `texture` to find simple vs. complex glyphs
- Low values = minimalist, high values = intricate

### 3. **Visual Style Matching**
- Use `mood` for quick aesthetic categorization
- Combine `contrast` + `circularity` for style archetypes (e.g., bold circles vs. soft shapes)

### 4. **Layout Optimization**
- Use `aspect_ratio` to select portrait/landscape/square glyphs
- Filter by `circularity` to find glyphs that fit circular frames

### 5. **Accessibility**
- Filter by `contrast` to ensure sufficient visual distinction
- Avoid low-contrast glyphs for small sizes or backgrounds

### 6. **Machine Learning Features**
All numeric metrics can serve as feature vectors for:
- Similarity search
- Clustering
- Style classification
- Recommendation systems

---

## Algorithm References

- **Color Clustering**: K-means (k=3, scikit-learn)
- **Edge Detection**: Canny edge detector (OpenCV, thresholds: 80, 160)
- **Entropy**: Shannon entropy (scikit-image)
- **Texture**: Local Binary Pattern with uniform patterns (scikit-image)
- **Color Space**: sRGB → CIE LAB (D65 illuminant, 2° observer)
- **Shape Analysis**: Contour analysis (OpenCV)
