# Mood Classification – Full (Old) Dictionary + Corrected Criteria Table

This document restores the **full original mood list** from the older data dictionary while also including a **corrected, up‑to‑date classification table** based on the latest script.

---

# 🔮 Full Mood List (Old Dictionary)

The older version of the pipeline described the following moods:

- **serene**
- **calm**
- **energetic**
- **chaotic**
- **mysterious**
- **futuristic**
- **minimalistic**
- **dramatic**
- **playful**

⚠️ *Note:*  
The current script does **not** use *minimalistic* anymore, but it is included here because you asked for the **old full list**.

---

# 📊 Corrected Mood Classification Criteria Table

Below is the corrected and consolidated table that merges the **old dictionary style** with the **actual rules** from the latest script.

| Mood | Core Characteristics | Influencing Metrics | Notes |
|------|----------------------|---------------------|-------|
| **Serene** | Soft, low-detail, smooth, bright or balanced | Very low entropy, very low edge density, high circularity | Calm simplicity; minimal noise improves score |
| **Calm** | Gentle, low-contrast, soft transitions | Low–medium entropy, low edges, low saturation, analogous harmony | Soft, cool colors boost score |
| **Playful** | Fun, organic, quirky | Medium entropy (2.8–3.8), medium edge density, low circularity | Irregular shapes increase score |
| **Energetic** | High saturation, dynamic, vivid | High saturation, warm hues, medium-high entropy & edges, complementary harmony | Warm (red/orange/yellow) increases score |
| **Futuristic** | Tech-like, sleek, structured | Aspect ratio near elongated (0.4–0.7 or 1.3–1.6), bright cool colors | Blue/purple tones with low saturation help |
| **Mysterious** | Dark, moody, cool-toned | Low brightness, cool hues, mid entropy | Darkness is the strongest factor |
| **Dramatic** | High-impact, bold contrast | High contrast (>0.5), medium–high entropy | Warm hues can amplify drama |
| **Chaotic** | Very noisy, irregular, high-complexity | Very high entropy (>5.3), high edge density | Extreme detail dominates score |
| **Minimalistic*** | Extremely simple, ultra-clean | Very low entropy (<3.5), extremely low edges (<0.03) | *Old dictionary only — not in current script* |

---

# ✔ Compatibility Notes

- The **old list** included *minimalistic*, which is **not present** in the new classifier.
- The table above merges both worlds:  
  the *concepts* of the old moods + the *actual measured signals* from the current algorithm.

---

# 📁 File Information

Generated automatically by ChatGPT.  
Format: **Markdown (.md)**  
Encoding: UTF‑8

