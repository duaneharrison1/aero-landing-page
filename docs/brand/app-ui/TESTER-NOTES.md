---
version: 2026-10-23.1
brand-sync: figmaApp docs/brand/app-ui is the source. Copy unchanged to aero-landing-page/docs/brand/app-ui/.
---

# Tester flow (screen 10): notes

What a tester sees after opening a test link. The person reading has never heard of Aero and is doing someone a favour. Example data: Mia Chen at Kestrel Studio testing Pocket, a payments prototype at pocket.aeroapp.ai. All names are made up.

## Files
| File | What it is |
|---|---|
| `tester.html` | The board: journey map, every step with approaches side by side, the colour test, variations, preview, glass, what-ifs, copy deck |
| `tester-flow.html` | Clickable flows, 9 scenarios, 53 steps (Figma on a computer, HTML on a computer, Figma on a phone, no tasks, mic denied, sharing stopped, network and saving, HTML on a phone, designer preview) |
| `tester.css` | Tester-only components on `tokens.css`, loaded after `components.css`. Prefixes: `.tx-` tester UI, `.cr-` browser UI (not Aero), `.pk-` the example prototype, `.tb-` board layout only |
| `tester.js` | Scales screens to their column, re-runs glass, runs the flow player |
| `src/tester_kit.py` | Every screen is built from these functions; example data and copy sit at the top |
| `src/tester-build.py` | Builds both pages: `python3 -I src/tester-build.py` |
| `tester-measure.mjs` | The colour test: measures task-title contrast against the worst pixel behind it, writes `src/tester-contrast.json` |
| `tester-clickthrough.mjs` | Clicks the pulsing control through every flow step; fails if a step doesn't render or advance |
| `tester-shoot.mjs` | Screenshots: `node tester-shoot.mjs <page> <width> <out> [full] [height] [hash]` |
| `shots/tester-*` | 1440 and 390 board and flow, plus close-ups of welcome, panel and colour test |

## The approach in five rules
1. **Say it before asking.** Who asked, what happens, what is recorded, who sees it, stop any time. All of it shows before any browser prompt.
2. **One permission step.** The mic and the tab are two rows on one card, in order. Each row has its own button, because each opens its own browser prompt and that needs a click. Today's four modals become two screens.
3. **Solid where you read.** The task panel is a frosted plate (the shared `--ae-glass-plate`, 86% white with a 22px blur). Glass goes only on small floating chrome.
4. **Never in the way.** The panel moves to any corner and folds to a pill. On a phone it docks below the prototype, so it never covers the prototype's own tab bar.
5. **Say what's lost.** No mic means no transcript. No tab means voice only. Every failure says which.

## The panel over prototypes of any colour
Aero can't read what is behind the panel: a Figma embed is a cross-origin frame. So the panel can't adapt to the prototype and has to work everywhere as it is. The colour test checks four treatments over six Pocket pages: black, white, bright coral, busy, an Aero-like blue and bright yellow. It measures the task title against the worst pixel behind it.

| Treatment | Worst | Passes AA |
|---|---|---|
| Today's smoky glass, white text | 2.4:1 on white | 2 of 6 |
| **A. Plate (pick)** | **14.1:1 on black** | **6 of 6** |
| B. V3 glass as the panel | 1.9:1 on busy | 2 of 6 |
| Minimised pill, V3 glass | 4.6:1 on black | 6 of 6 |

The same plate at 94% white measures 14.8:1 or better. It looks cleaner on dark prototypes, but 86% matches the shared token and passes, so the board uses 86%.

## Where glass is used
- **V3 primary, subtle:** Start, Start the test and Copy link on the tester cards, plus Done in the panel. Done is the one place the prototype's colour reaches the panel.
- **V3 secondary:** the minimised pill (small chrome floating over unknown colour, which is what glass is for).
- **No glass:** the panel body, the welcome card and the thank-you card. Each of these:
  - holds text that people have to read;
  - appears in every recording, where refraction would warp the prototype in the replay;
  - would get only a frosted blur in Safari and Firefox.
- **Engine note:** `glass-v3.js` styles its host as a button (pill radius, nowrap, inline-flex). Option B overrides that in `tester.css`. A panel variant would need engine work if it is ever wanted.

## True to the app (checked in code)
- **Figma tests:**
  - One tab, `preferCurrentTab`. Chrome only asks about this tab.
  - Screen share is optional. If sharing stops part-way, the video stops and the voice goes on, silently.
- **HTML tests:**
  - Two tabs: `UTHtmlController` in tab 1, the site in tab 2 with `src/ut-overlay`.
  - The tab pick is checked (Capture Handle). After two misses, a whole-screen fallback appears.
  - A denied share can't be skipped, and stopping the share ends the session.
- **Ratings:** `askDifficulty`. After each task on Figma tests; once per session, in tab 1, on HTML tests.
- **Uploads:** recordings upload in about 5 MB pieces during the test, with a `beforeunload` warning.
- **Phones:** voice only on Figma tests. HTML tests are blocked on phones (`unsupported`).
- **Transcripts** arrive about a minute after the session. Tab recordings show no mouse.

## Proposed (needs new work)
1. **"Not recording yet" in tab 2 (HTML).**
   - Today the overlay shows Task 1 as soon as tab 2 opens, before the share and before any recording.
   - It needs a controller-to-overlay message (today only the overlay talks).
2. **Finished state in tab 2.** Today the overlay disappears after Finish. It should say "Go back to the Testing Pocket tab".
3. **Mic denied handling (B16).** Say what's lost, say where the switch is, and continue on its own when the permission changes (`navigator.permissions` change event).
4. **"No audio" tag on the session for the designer** (owner side, B16).
5. **Share again after sharing stops.** Figma: start a new picker and a second video file. HTML: pause instead of ending.
6. **In-panel recording chip.**
   - It shows the elapsed time and a level meter (Web Audio analyser on the existing mic stream).
   - It also covers offline, sending, sent and not sent.
7. **Inline rating.** Five labelled buttons with keys 1 to 5, replacing the emoji modal. A "Couldn't do it" path that uses the same scale.
8. **"Anything else to say?" beat** after the last task, while it's still recording.
9. **Panel menu.** Move to a corner (kept for the session), Mute, Restart, End test with a confirm.
10. **Offline and back online strips.** "Try again" and "Download a copy" when a send fails.
11. **HTML on a phone: "Email it to myself"** (needs a small mail function).
12. **Neutral "This test isn't open right now".** It replaces "the owner has reached their session limit", which exposes the designer's plan to their tester.
13. **Designer preview** (`&preview=1`): a dark bar outside the tester UI and a jump bar to any step.
14. **If cursor or click tracking ships** (see `../research/cursor-recording.md`), the consent copy says so before Start:
    - HTML: "Where you move, click and scroll", inside Pocket only.
    - Figma: "Where you click", because the Embed API gives clicks and screen changes, not movement.
    - The board shows these beside today's card.

## Decisions for Duane
1. **Panel treatment:** A, the plate (recommended), or keep some glass on the panel (B fails on four of six prototypes).
2. **Plate opacity:** 86%, the shared token (passes everywhere, a little grey on dark prototypes), or 94% (cleaner).
3. **Figma on desktop:** the floating plate everywhere (one component for Figma and HTML), or the docked rail for Figma (never covers anything, but the frame shrinks and it's a second design).
4. **Preview:** record nothing, or record a practice session marked "Preview" that doesn't count.
5. **Thank-you footer:** "Test made with Aero. Publish and test your own prototypes at aeroapp.ai". Keep it (growth) or drop it (pure courtesy)?
6. **Welcome copy:** keep "There are no right or wrong answers. You're testing Pocket, not yourself."

## Weakest parts
- **HTML two-tab flow.** It is still the hardest part for testers. Chrome's picker and the jump between tabs can only be explained, not removed. The "not recording yet" fix depends on a new message channel.
- **Phones.**
  - The docked bar and the rating sheet are drawn at one size. Long task titles and small phones aren't tested.
  - The iOS steps for a blocked mic vary by browser.
- **Browser coverage.** Firefox and Safari (no tab capture) get a helper line only, with no screens drawn.
- **The colour test** uses CSS-drawn pages, not real customer prototypes. Real pages with photos would be a fairer check.
- **Desktop frames on the board** are small at 3 to 5 per row. The flow page shows each one full size.
