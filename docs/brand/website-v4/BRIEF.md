# Aero website round 5 (24 Oct 2026, evening)

Duane's feedback on round 4 is logged in `/home/claude/figmaapp/docs/brand/DECISIONS.md`, section "24 Oct 2026 (evening): feedback on website round 4". Read it first, then the round 4 brief `BRIEF.md` (still applies unless overridden), `TONE_OF_VOICE.md`, `PRICING-FACTS.md` and the truth rules in `/home/claude/figmaapp/CLAUDE.md`.

## Bug found (fix first)
The section loops collapse while playing: `home.js` adds the class `play` to `.hm-img`, and a global `.play` rule from the v3 stylesheets (the little play button) sets `display:grid` and 28px size. Rename the section class (e.g. `is-running`) everywhere in home.css/home.js. Check no other generic class collides. Then verify in Playwright that the boxes keep their height while running (round 4's screenshots missed it because they were taken before the loops started).

## Team G: glass (works in `web3/shared/` and a lab in `web3/glass-r5/`)
- Buttons back to a **slab of thick glass**: rounded rectangle with visible depth/thickness, like the glass Duane picked (V3). Find it: `/home/claude/research/glass/`, `/home/claude/research/caustic/`, `/home/claude/research/glass-lab/`, `web3/glass-lab/`, `/home/claude/figmaapp/docs/brand/app-ui/` (tester.css, flows.html), the app's `src/components/Aero/glassEngine.js` + `GlassButton.js` (his original engine: buttons take colour from nearby `[data-color]` items by distance and amount).
- **Caustic must be visible again**: the button picks up light and colour from what is near it. Round 4's lost it. Work out why (pale washes? fill too solid? sampling?), fix it.
- **Hover = key light follows + Lift, combined.** Key light toned down to slight. On the black (ink) button, no key light (or almost none); Lift only. Same on `:focus-visible`; snap under reduced motion; nothing moves or resizes.
- **Top nav is glass** (it wasn't). It must look like glass as content scrolls under it, and stay readable.
- Lab page `web3/glass-r5/index.html`: the buttons (white glass, ink) at rest/hover/focus over the washes, a nav over scrolling content, next to round 4's for comparison. Shots in `glass-r5/shots/`. Then put the result into `shared/glass-v3.js` / `shared/aero.css` (keep class names; tell Team H if markup must change).
- Test in real Chromium at 1512x789 too (Duane's viewport). His browser is Chrome 155 on macOS.

## Team H: homepage (`web3/home/`)
- Fix the bug above.
- **Hero:** back to the liked earlier hero: round 1 `/home/claude/research/mockups/studio/home.html` (one big screen at an angle, no background panel behind it, not floating windows). Compare `/home/claude/research/compare/` for what he liked. Headline then buttons under it; description to the side is one option, do what reads best.
- **Hero animation:** same steps, a little slower (aim ~26 to 30 s), on ONE screen at an angle (a browser window whose contents change; switching tabs or the address bar is fine):
  1. Claude builds Pocket with the preview (Claude's UI clearly Claude's). Paste the one prompt, Claude publishes.
  2. Show it in Aero (the Sites page: live, pocket.aeroapp.ai), then the live site open in the browser at pocket.aeroapp.ai.
  3. Back in Aero, go to Test: create the test from the site, copy the link, send it.
  4. Make it obvious this is a **user test**: the tester's screen with "Recording", task panel, voice waveform; a phone alongside doing a test is allowed (on phones Aero records voice only, no screen, so show the phone test with voice only). **No webcam**: Aero never records the camera.
  5. Review in dark: playback with word highlight, friction points, then Insights.
  - Add a **cursor for the owner's own actions** (clicking Copy, pasting, clicking Test). Highlight each effect at the moment it happens (button press, toast, "Live" badge). Truth rule: NO cursor drawn inside the session replay (step 5) and none on the tester's recorded screen.
  - Keep the timeline along the bottom (blue fill), pause button, offscreen pause, reduced-motion still.
- **Sections:** remove the "Coming from Figmafolio?" strip; put custom domain, password protection and versions under Publish (facts list and/or loop), user testing is Test. Keep the round-1 text+image layout, pills and washes. Make sure each loop is legible at 1512 wide and 390.
- **Price table:** add **Maze**, everything in the **same unit, per month** (annual-only plans as the monthly equivalent, "billed yearly" noted). Maze now shows Free and Enterprise plans publicly: compare Maze Free on the same rows (sessions with your own testers, recording, transcript, hosting, testers install nothing). Check every competitor figure again on their pricing pages with WebFetch/WebSearch today; anything unconfirmed says "Not checked". Footnote: Aero's sessions are a total. Source date.
- Use the shared glass markup; when Team G changes `shared/`, pick it up (rebuild). Nav markup stays the same unless G says otherwise.
- Shots at 1512x789 and 390 (fold + full) into `home/shots/`, AFTER the loops have run a few seconds; hero frames and MP4. Look at every shot.

## Both
- Light only; no em dashes; British spelling; sentence case; example names only.
- Report briefly: what changed, what needs Duane.
