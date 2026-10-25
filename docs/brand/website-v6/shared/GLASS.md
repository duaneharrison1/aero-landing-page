# Aero glass: one component, one settings file

## Files
- `glass-settings.js`: the ONE place the look is set. It defines `window.GLASS_P`, a flat object with the same keys as the glass panel's JSON. Current settings: "Duane, 25 Oct".
- `glass-v3.js`: the engine. It reads only `window.GLASS_P`, and uses the panel's own defaults for any key that is missing. Do not tune numbers in it.
- `aero.css`: button sizes (`.btn.sm/.md/.lg`) and the glass nav. The nav reads its frost and strip values from CSS variables, which the engine sets from the settings.

## Loading (every page)
Load the settings first, then the engine, at the end of `<body>`:

```html
<script src="../shared/glass-settings.js"></script><script src="../shared/glass-v3.js"></script>
```

## Using the component
Buttons keep the existing markup. Nothing else is needed.

```html
<!-- ink glass (primary) -->
<a class="btn g3 md" href="#" data-glass-v3="primary" data-fill="rgba(29,29,31,.8)">Start free</a>
<!-- white glass (secondary) -->
<a class="btn g3 md" href="#" data-glass-v3="secondary">See pricing</a>
<!-- app-style solid ink (no refraction; still lit) -->
<span class="btn g3 sm" data-glass-v3="primary" data-fill="#1D1D1F">Copy test link</span>
```

- **Sizes:** `.sm` is 32px, `.md` 38px and `.lg` 44px. The corner radius comes from the settings: `radius` sets `.lg`, `.md` is 0.9 of it and `.sm` is 0.8.
- **Ink opacity:** a translucent ink fill takes the settings' `inkA`, whatever alpha the markup gives. Solid fills stay solid.
- **Hover:** `:focus-visible` gets the same effect as hover. Under reduced motion the states snap. Nothing moves or resizes.
- **Holding a state:** `data-force="hover"` keeps a button in its hover state, for screenshots or a scripted cursor. `data-px` and `data-py` (0 to 1) say where the light rests.
- **The nav:** `<header class="site-nav">` is glass automatically, with the frost and the refracting lower strip.
- **Buttons added later:** call `GlassV3(el)` for one button, or `GlassV3.init(root)` for everything under `root`.
- **Animated scenes** (the hero):
  - Buttons in scaled or tilted scenes work, because the engine uses each button's layout size.
  - Buttons that move without a scroll or resize are re-read when the browser is idle, at most 3 per check, about once a second.
  - After a scene change, `GlassV3.refresh()` updates every button at once.

## Changing the glass (swap the settings)
1. Open the glass panel (`web3/glass-panel/index.html`) and set it up. Simple mode has 8 sliders; "All settings" has every key.
2. Press **Export for site**. It copies the exact text of `glass-settings.js`.
3. Paste it over the whole of `shared/glass-settings.js`. Every page, including the hero animation, picks it up on the next load.

At runtime (the panel does this): change `window.GLASS_P`, then add 1 to `window.GLASS_P_V` and call `GlassV3.refresh()`.

## Cost
- One full refresh of the homepage hero's buttons takes about 20 to 50ms. Before the 25 Oct changes it took about 300ms.
- Hit tests are cached per refresh and shared between buttons, and there are fewer samples per button.
- Scrolling only re-reads buttons whose position on the page changed: the sticky nav, or anything moved by an animation.
- No long tasks were measured during 8 seconds of hero playback.

## Planned port to the app (figmaApp)
The app has its own `src/components/Aero/GlassButton.js`, which uses `glassEngine.js`, the original engine: canvas tint from `[data-color]` sources. The plan, not done yet:
- Port `glass-v3.js` into the app as a module, keeping `P(name)` and the defaults.
- Pass the settings in as a `settings` prop or context. One `glassSettings.js` module would be the app's version of `glass-settings.js`, kept in step with this file and covered by the two-repo sync rule.
- `GlassButton` would keep its props (`fill`, `size`) and map them to `data-glass-v3` and `data-fill`. Colour would come from DOM sampling, with `[data-color]` still honoured, as `glass-v3.js` already does.
- The glass's look stays the same in both places because both read the same settings keys.
- Before porting: the canvas tint and refraction need the Chromium check (SVG backdrop refraction is Chrome only; other browsers get the frost), and the AeroShowcase entry needs updating.
