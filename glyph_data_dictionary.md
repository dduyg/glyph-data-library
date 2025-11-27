# Updated Data Dictionary (Aligned to Final Script)

## Top-Level JSON Structure
Each glyph entry:
```json
{
  "id": "",
  "filename": "",
  "glyph_url": "",
  "color": { ... },
  "metrics": { ... },
  "color_harmony": "",
  "mood": "",
  "created_at": { ... }
}
```

## Field Definitions

### id
- **Type:** string  
- **Description:** Unique 8-character identifier.

### filename
- **Format:** `{hex_color}_{YYYYMMDD_HHMMSS}_{id}.png`

### glyph_url
CDN URL to the glyph in GitHub.

## Color Fields
### color.hex
Dominant color in hex.

### color.rgb
Dominant RGB triplet.

### color.lab
L\*a\*b\* representation, 2 decimal precision.

### color.group
Categorical semantic color group:
`black`, `white`, `gray`, `gold`, `silver`, `brown`,  
`red`, `orange`, `yellow`, `green`, `blue`, `purple`, `pink`

### color_harmony
Values: `analogous`, `complementary`, `none`

## Metrics
### edge_density
Canny-based edge density.

### entropy
Shannon entropy of grayscale masked pixels.

### texture
LBP texture entropy.

### contrast
Michelson contrast.

### circularity
4πA / P² of largest contour.

### aspect_ratio
Width/height of bounding box around largest contour.

### edge_angle
Median Sobel edge orientation (0–180°).

## Mood
Possible values:
`serene`, `calm`, `playful`, `energetic`,  
`futuristic`, `mysterious`, `dramatic`, `chaotic`

## created_at
- `date`: YYYY-MM-DD  
- `time`: HH:MM:SS
