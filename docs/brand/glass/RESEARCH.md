# Liquid glass on the web: research notes

## Techniques
- **SVG displacement refraction.** The main web technique is an SVG filter referenced from CSS: `backdrop-filter: url(#f)`.
  - The filter chain is `feImage` (a displacement map) into `feDisplacementMap` (`xChannelSelector="R"`, `yChannelSelector="G"`).
  - In the map, 128 is neutral. Values toward 0 or 255 shift the pixel by up to ±scale/2.
  - The map has to be built per size and radius, with the distortion kept to the edge. The rest of the button stays flat.
  - Sources: [LogRocket](https://blog.logrocket.com/how-create-liquid-glass-effects-css-and-svg/) (scale 55, `feColorMatrix` saturate, a rim image composited "in"); [ekino / Medium](https://medium.com/ekino-france/liquid-glass-in-css-and-svg-839985fcb88d) (feTurbulence or feImage maps, scale 20 to 30).
- **Physical lip (kube.io).**
  - The edge is a convex squircle, `z = (1-(1-t)^4)^(1/4)`.
  - A vertical ray refracts by Snell's law (n = 1.5). The displacement per depth is `height × tan(a - b)`, which is baked into the map.
  - A separate specular map comes from the surface normal against a light direction.
  - Source: [kube.io/blog/liquid-glass-css-svg](https://kube.io/blog/liquid-glass-css-svg/). The page was blocked from this session, so this summary comes from secondary coverage and prior knowledge.
  - The same lens model, with six lens profiles, appears in [Photorealistic liquid glass (dev.to)](https://dev.to/hlaaung/photorealistic-liquid-glass-4ikg).
- **liquid-glass-react.** Props: `displacementScale` 70, `blurAmount` 0.0625, `saturation` 140, `aberrationIntensity` 2, `elasticity` 0.15, `overLight`. Source: [README](https://cdn.jsdelivr.net/npm/liquid-glass-react@1.1.1/README.md), [repo](https://github.com/rdev/liquid-glass-react).
- **WebGL route.**
  - [liquidGL](https://github.com/naughtyduk/liquidGL) snapshots the page, then refracts it in a shader: `refraction`, `bevelDepth`, `bevelWidth`, `specular`, `frost`.
  - It works in every browser but uses a snapshot, not a live backdrop. Dynamic content has to be registered.
- **CSS-only.**
  - `blur(12–30px) saturate(140–200%)`, a 1px white inset top highlight and a brighter top border. Without these the glass reads as dirty grey.
  - Use it only for chrome (navigation, toolbars, floating controls), never for content.
  - Source: [buildmvpfast recipes](https://www.buildmvpfast.com/blog/liquid-glass-css-backdrop-filter-recipes-2026).

## Caveats
- `backdrop-filter: url()` renders only in Chromium.
  - Safari has an open WebKit bug ([313914](https://bugs.webkit.org/show_bug.cgi?id=313914)).
  - Firefox passes `@supports` and draws nothing, so detection needs a UA check. All four lab variants do this and fall back to blur and saturate.
- `backdrop-filter` only sees inside the element's own box. Refraction cannot pull in what is beside the button, so environment colour has to be sampled from the DOM. All four variants do this.
- The SVG displacement has no supersampling, so it can look pixelated. A 0.3 to 0.4px blur after it helps.
- Contrast varies with the backdrop. Check against the worst case. The variants raise glass opacity until the label passes 4.6:1.
- `prefers-reduced-transparency` is unreliable: Safari does not support it and Firefox has it off by default.

## What the lab takes from this
- **V3** is the kube.io model: Snell squircle map, plus a Schlick-style Fresnel term so reflected colour sits only on the steep lip.
- **V4** adds a mild chromatic split: three displacement scales (×1.07, ×1, ×0.93), one per channel, recombined with `feComposite` arithmetic.
- **All four** score sampled colour by OKLCH chroma × colour contrast to the button, weighted by distance and share of view. Ambient colour is removed from the rim, and a knee cap and a whole-rim budget clamp the total.

## Round 2 findings (fills, Liquid mode, V5)
- **V5 reference** is a direct port of liquid-glass-react 1.1.1, read from the npm package source (MIT, Max Rovensky; licence copied to `src/liquid-glass-react.LICENSE`).
  - It uses the library's own embedded "standard" displacement map and its filter chain verbatim: R/G/B displacement at -70 / -77 / -84 (yChannel B), screen blend, an edge mask from the map, and the clean centre composited back.
  - Also from the library: warp backdrop `blur(6px) saturate(140%)`, two masked gradient rims (screen 0.2 + overlay) and a `0 12px 40px rgba(0,0,0,.25)` shadow.
  - Not ported: the elastic cursor stretch.
  - One addition: a dark tint layer, raised only as far as white-label AA needs.
- **How the library applies the filter (the key detail).** It puts `filter: url(#f)` on a warp layer that has its own plain `backdrop-filter`. It does not put `url()` inside `backdrop-filter`. When `url()` sits inside `backdrop-filter`, Chromium renders an offset sub-rectangle of the box, seen as a hard-edged patch. V1 to V4 now use the library's structure: a warp layer for the backdrop plus an unfiltered body layer for the glass colour, since a filtered layer loses its own background.
- **Blend modes isolate the backdrop.** A child with `mix-blend-mode` isolates the button, and `backdrop-filter` inside it then sees nothing. Screen-blended reflections are therefore used only on solid fills.
- **Liquid mode (V1 to V4).** It applies the library's defaults scaled to button height:
  - Snell lip about 45% of the height deep
  - displacement about 1.1 × height (capped at 70)
  - lens magnification term
  - ±10% chromatic split
  - bright 1.5px rim
  - Clear glass picks ink or white label by whichever needs less opacity for AA, as vibrancy does.
  - Large text behind the label adds a 4px frost.
