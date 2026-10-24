# Homepage rework, web2 (23 Oct 2026)

Round 5 A Studio's homepage structure and scale, drawn with the v3 app UI. Light only.

## Files
- `home.html`: the page (built, do not hand-edit except the COPY JSON at the top).
- `build.py`: builds `home.html`. Imports the real v3 components from `../v3/make/build.py` and `../v3/review/build.py` (read only). All words are in the `COPY` dict at the top, and the same block is embedded at the top of `home.html` as `<script id="copy" type="application/json">`; the page applies it on load, so a word can be changed in either place.
- `site.css`: page styles only (`h-` prefix, `.shot`), on the aero.css tokens and washes.
- `home.js`: copy block, window scaling, the made-with rotator, the hero replay loop, reveals.
- Copied in: `aero.css`, `extra.css` (make), `review.css`, `glass-v3.js`, `favicon.svg`, `lockup.svg`, `mark.svg`.
- `shoot.cjs`: Playwright. Fold and full page at 1440 and 390 (both 2x), three frozen replay frames and one live frame. Full pages are shot in slices and stitched because Chromium blanks past 16,384 device px. `home.html?t=189` freezes the replay at that second.
- `shots/`: `home-d-fold`, `home-d-full`, `home-m-fold`, `home-m-full`, `hero-replay-150/189/212`, `hero-live-6s`.

## Page, top to bottom
1. Hero: headline top left, sub and buttons right (round 5 A). "Publish your [Claude artifact | Figma prototype | Lovable app | HTML site]. Watch people use it." The rotator is its own line (the long items don't fit beside "Publish your" at this size). Under it, the full-width v3 Watch view in light, angled as round 5 A, on the hero wash: Maya's recorded tab, task regions on the timeline, the follow-along transcript with friction lines. Label: "Example session: Pocket, a payments app. Maya, thinking aloud."
2. Three proofs (as round 5 A).
3. 01 Publish, "One prompt and it's live.": v3 create flow, prompt step (copy one prompt, nothing to install), then the site's page in Aero after publishing, overlapped, on the Publish wash.
4. 02 Test, "One link. Their screen and their voice.": test setup with the test link, then the tester's own computer with the square task panel over the prototype and the "Recording" sign, on the Test wash.
5. 03 Review, "What to fix, in their own words.": Insights (summary, "4 of 6 testers", quote cards with play), then the Read view of one session, on the Review wash.
6. 04 From prompt to first session (timeline), 05 Price, 06 Who it's for, 07 FAQ, closing line, footer.

## The hero loop
- Plays session time 02:14 to 03:52 at 2x (about 49 s), then a short fade back. The control chip reads 2x to match.
- Moves only: the playhead, played waveform, time, the current task region and the task pill, the current transcript line with its word lit as it is said, the friction line and its timeline mark lit for 9 s after its moment, the More sheet opening at 03:25 (she finds cards under More at 03:31), and the "Add a note at" time.
- Truth rules: no cursor anywhere; the whole transcript is present from the start, only the highlight moves; the stage keeps "tab recordings have no pointer".
- Pauses offscreen and in a hidden tab. Reduced motion shows the 03:09 frame.

## Changes from round 5 A
- No photos: the "Who tests" photo strip is gone and "Who it's for" is text with small icons.
- Pricing from PRICING-FACTS only: Free $0 (3 sessions), Basic $3 (5), Solo $6 (10), Pro $19 (20), 7-day trial on paid plans, no "a month" after session counts. Round 5's Solo footnote is now a full card; Solo is the highlighted plan (my pick, easy to change).
- FAQ "Can Claude publish for me? Connect Aero once" replaced with "How does the prompt publish my site?" (a prompt, nothing to install or connect). Round 5's phone answer was dropped, since I couldn't confirm it against the v3 tester screens.
- Footer credit "Photo: Unsplash" removed. No founder. No em dashes (the build checks), British spelling.

## How the app screens are made
- Every screen is a real 1440-wide v3 window, scaled by `home.js` to its column (`.shot`, `data-w/h`). On a phone each one shows a chosen part (`data-mw/mx/my/mh`). The hero is re-laid as a narrow app instead (sidebar hidden, recording over transcript) so it stays readable at 390.
- The v3 create and setup screens were drawn for Checkout. On this page they say Pocket (name, address, link, tasks, welcome message, preview thumbnail), changed at build time without touching v3.

## Open points
- The rotator's four "made with" items include Lovable. Worth checking that a Lovable app publishes through the same prompt or an HTML export before launch.
- The Test section's tester sees the desktop "Pocket" prototype (coral, v3 m7), while the hero session uses the phone Pocket. Both come from v3. Using one would need a phone tester screen in v3.
- At 390 the section screens are crops of real windows, about 0.45 scale. They read as product, but the small text isn't meant to be read.
- The JSON block updates every string on the page except the footer column links.
