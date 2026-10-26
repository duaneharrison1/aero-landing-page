# Buttons in situ (kit 2): notes

Exploration only, nothing decided. Follows Duane's notes on kit 1: the options were mostly shown on the tester screen, he wanted the dashboard and modals, the stock blue was ugly, and the accessible glass wasn't shown.

## Files
- `pages.html`: the page, built by `build.py` (`python3 -I build.py`). It reuses Studio's builder and CSS (`../studio/build.py`, `../studio/src/*.css`) read-only. Everything except the buttons is Studio. `kit2.css` holds the button tokens and the new pieces (modals, floating player, tester panel, Pocket's website, the states strip, the tables).
- `glass-v3.js`: copied unchanged from figmaApp `docs/brand/glass/`, referenced relatively. Subtle mode.
- `measure.cjs`: measures every button marked `data-m`. It hides the label, captures the area under the text at 2x and takes the ratio against the worst pixel there. Writes `contrast.json`, which `build.py` turns into each option's table. Order: build, measure, build.
- `shoot-kit2.cjs` + `stitch.py`: screenshots each section one viewport at a time and stitches them into `../hi/kit2-<id>.png`. Chromium blanks single captures over about 16k px, and the option sections are about 17.5k px at 2x.

## The four options (one CSS block each in `kit2.css`, `.o1` to `.o4`)
1. **Ink**: #1D1D1F primary, white secondary with a #D2D2D7 hairline, red #C4321F destructive, 10px corners (8px small). The focus ring is the logo blue #3478F6.
2. **Deep Aero blue**: #254A8D, which is the dot's own OKLCH hue (259°) at L 0.42 and C 0.12. White on it is 8.6:1. The dot itself only reaches 4.07:1 with white, so it can't be a button fill, and that is the reason for going deeper. Quiet white secondary with a cool hairline.
3. **Ink, glass where it floats**: option 1 everywhere you read. V3 glass only on the player controls over the recording, the task chip, the tester's "I'm done" and the folded pill. Panels use the frosted plate (86% white, 22px blur). The dashboard and modals are the same as option 1 on purpose.
4. **Soft graphite**: warm graphite #45413C pill primary with an off-white label, warm stone #EFECE7 secondary with no hairline, and round ends throughout.

## What each moment shows (frames a to g, in every option)
- a: the dashboard header (search, New test, Publish) and the small action on each row.
- b: the session header (prev/next, Download summary, ⋯). The recording is now drawn as a tab capture: a Figma prototype on its grey canvas, no cursor. The player controls float over it.
- c: Share the test (link field, Copy link primary, Done secondary, "Open as a tester").
- d: Delete this session? over the session view.
- e: New test with three choices (Figma prototype link, HTML or zip, From Claude or ChatGPT), Continue and Cancel.
- f: the tester task panel over a bright Pocket website, plus the folded pill over coral, busy colour, and black with text.
- g: Continue disabled with a hint saying why, and Publishing loading. Then a strip of every state: rest, hover, focus, disabled, loading and small. For option 3 it adds glass over four backgrounds.

## Contrast (measured)
- Every button passes AA in every option. Solid fills: ink 16.83:1, deep blue 8.60:1, graphite 9.62:1, stone secondary 12.31:1, red 5.49:1 (6.57:1 in option 4). Hover and loading fills stay at 7.35:1 or better.
- Option 3 glass, against the worst pixel: task chip 4.76:1, speed 4.68:1, folded pill 7.56 (coral), 4.90 (busy colour) and 4.76 (black with text). All pass, but with little to spare. The engine reaches AA by raising opacity, so over the dark Figma canvas the secondary glass turns smoky grey.
- Disabled buttons measure about 2.1:1. WCAG exempts them, and each one sits next to a hint.
- Non-text parts: the focus ring is 4.07:1 (passes 3:1). The hairlines and the stone fill are below 3:1 against white; the label carries the button, so that is acceptable but worth knowing.

## Unsure
- Over dark recordings the accessible glass looks grey and flat, which is less "glass" than people expect. A "dark" engine variant (smoked, white label) may suit recordings better, but it would need its own colour test over white prototypes.
- Option 2's ring and fill are both blue, so the focus state is less distinct there.
- The half-width windows in g squeeze the sidebar. They are only a backdrop for the modals.

## Recommendation
Option 3. It reads as option 1 on the dashboard and in modals, and glass appears only where controls float over content Aero can't predict. Keep #254A8D for marketing calls to action. Drop option 4: every button becomes a soft pill, so the hierarchy flattens. Next tests: a five-second test of the dashboard, and the tester panel over five real customer prototypes.
