---
brand-sync: figmaApp docs/brand is the source. Copy this file unchanged to aero-landing-page/docs/brand/.
version: 2026-10-23.1
---

# Aero brand

**Status, 23 Oct 2026: in progress.** The logo direction is chosen; the palette, the app UI and the website are being designed (UI first, see `DESIGN_SYSTEM_PLAN.md`). Until the token change ships, the app keeps `src/styles/aero-design-system.css` as it is; do not mix new and old by hand.

## Logo (direction chosen)
- **Wordmark:** "Aero." in Geist 500, converted to outlines, tracking -0.6%. The full stop is rebuilt as a true circle 1.2 times the o's stroke, in Aero blue #3478F6.
- **Mark and app icon:** "A." (today's collapsed-sidebar mark) in Geist with the blue dot, light on ink. The favicon uses a heavier weight and a bigger dot so it reads at 16px.
- **Files:** `logo/` (lockup, reversed lockup, wordmark, mark, reversed mark, app icon dark and light, favicon). The build script is in the research folder of the brand work; the font is Geist from Google Fonts.
- **The dot is the constant.** It is the one bright blue thing on a page. A headline's last full stop can carry it.
- **Still to do:** refine the logo (optical tweaks), motion for the dot (draw-in, hover, loading).

## Colour (working, not final)
| Token | Hex | Use |
|---|---|---|
| ink | #1D1D1F | Text, primary buttons |
| paper | #FFFFFF | Page |
| mist | #FAFAF9 | Panels |
| line | #E8E8EA | Borders |
| aero blue | #3478F6 | The dot, links, selection, playhead |
| washes | peach, sky, mint, soft gradients | Behind product shots; one soft gradient per section (Publish, Test, Review), to be chosen |

No dark website. The app may offer a dark theme.

## Type
- Geist 400 to 500 for headlines (light and large, never heavy), Geist for text, Geist Mono for small labels and timecodes.

## Buttons: V3 glass
- `glass/glass-v3.js`: Snell-law refraction at the edge, a Fresnel-weighted reflection of nearby colour, a key-light highlight. Duane's pick, 22 Oct.
- Quiet by default ("subtle"). "Liquid" only for a button floating over imagery.
- Pill or rounded rectangle by design; the engine reads each button's corner radius.
- Refraction renders in Chromium only; Safari and Firefox get a frosted blur.
- The source and the four other variants studied are in `glass/src/`. `glass/RESEARCH.md` lists the techniques and sources.

## Imagery
- The real app UI, from the demo mode (see `DESIGN_SYSTEM_PLAN.md`), on soft washes.
- Illustration and animation for people and context. No stock photos.
- Third-party UI (Claude, Figma) simplified and clearly separate from Aero's.

## Voice
See `TONE_OF_VOICE.md`.
