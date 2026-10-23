# Buttons and logo in use: notes

Exploration only. Nothing here is decided. Page: `pages.html` (built by `_build/make.py` from `_build/template.html`; logos by `_build/logos.py`, which reuses the brand builder in `research/brand/_build`). Screenshots: `shots/` via `shoot-kit.cjs`. Glass: `glass-v3.js`, copied unchanged from figmaApp `docs/brand/glass/`.

## b1 Button families
- Eight families: ink solid, Aero blue solid, ink outline, quiet text, neutral soft tint, V3 glass clear, V3 glass ink tint, V3 glass blue tint. Each as primary, secondary, small, disabled, loading, in pill and rounded rect (10px, 8px small).
- Glass families are shown over the Pocket example prototype, never on white. The neutral tint is 7% ink, so it avoids the pastel box.
- Works: ink solid is the calmest and keeps the blue dot unique. Blue glass is the most "Aero", and the most legible of the glass sets over busy colour.
- Unsure: clear glass primary versus secondary differ only by weight; over yellow and orange the clear label gets thin. Disabled glass (engine opacity .45) is hard to read as disabled rather than broken.

## b2 Buttons in context
- Five moments (create footer, session header, tester screen before and during, marketing hero, dark surface), each drawn in all eight families with their natural shape.
- The session header is drawn player-first (controls float over the recording) so glass has something to refract. The progress line has a blue playhead and no cursor.
- Works: solid ink and blue read everywhere. Glass is best where the content behind is consistent (tester panel, dark bar over thumbnails).
- Unsure: glass is weakest when a button straddles two backgrounds (hero CTA half over the wash, half over the app shot; create footer over the chart bars). A white bar with a solid button is still the clearer create footer.

## l1 Logo options
- Seven options drawn as outlines: "Aero." Geist 500 (favourite), "Aero" no dot, "aero." lowercase, "A." tile plus "Aero", "Aero." Instrument Sans 500, "Aero." Schibsted Grotesk 500, dot mark plus "Aero". Each at large, 24px, favicon 32 and 16, light and dark.
- Favicons use Geist 700 (or the option's own font) with a bigger dot (1.5x the o stroke) so the dot survives at 16px.
- Works: "Aero." Geist still looks the most expensive; the "A." tile is the strongest favicon at 16px.
- Unsure: the dot mark's lockup dot is tiny at 24px; it may need its own small-size drawing. Lowercase favicon "a." is busier than "A.".

## l2 Logo in use
- Sidebar, tester footer ("Made with", Free plan only since paid plans have no Aero badge), share email, browser tabs (light and dark Chrome) and website nav.
- Works: in the tab bar the wordmark options all collapse to the same "A." tile, so the favicon choice matters more than the wordmark choice.
- Unsure: "Made with Aero." puts a full stop mid-sentence; the dot reads oddly in running text. The no-dot or dot-mark options handle "Made with" better.

## r1 Recommendation
1. Ink solid + "Aero." Geist: safest, the dot stays the one bright thing. Test: five-second recall on dashboard and hero.
2. Ink-tinted glass only where controls float over prototypes, ink solid elsewhere, with "Aero.": one family, two states. Test: task panel over five prototype colours (AA contrast, do testers find "I'm done").
3. Blue glass + dot mark: boldest; the dot as mark, playhead and loader. Test: preference test against pair 1, favicon among ten open tabs.

## Into the shared design system
- Each family is one `.bt` component with `pri`/`sec`, `md`/`sm`, `pill`/`rect`, `disabled`, `aria-busy` loading; glass is the same component with a `data-glass-v3` attribute, so tokens (ink, blue, radius 10/8/999, heights 40/30) map straight onto `--aero-*` tokens in `aero-design-system.css` and the logo symbols become the `logo/` files.
