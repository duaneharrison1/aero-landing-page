---
brand-sync: figmaApp docs/brand is the source. Copy this file unchanged to aero-landing-page/docs/brand/app-ui/.
version: 2026-10-23.1
---

# Aero app UI round: notes (screens 1 to 9, 11 to 13, tokens, components, flows)

Step 1 of the design system plan. The tester flow (screen 10) is a separate piece of work in the same folder (`tester*.html`).

## Files
- `tokens.css`: every token. Two area palettes as themes: **Morning** (default: peach, lilac, mint) and **Clear** (`data-palette="clear"`: butter, rose, sea). A proposed app-only dark theme (`data-theme="dark"`).
- `components.css` + `components.html`: the component sheet. Class names are stable (`ae-component`, `--variant`, `is-state`). Components respond to their container, not the viewport. That lets the same markup work in the app, on a scaled board and in the marketing kit.
- `kit.py`: the component helpers, the icon sprite and the example scene (Kestrel Studio, Mia Chen, Pocket at pocket.aeroapp.ai, Tester B's transcript with word timings). Copy lives in the scene and the pages, not in the helpers.
- `screens.html`: each screen with 2 to 4 approaches side by side, then its states, then Proposed / Copy / Engineer check notes. The Layout switch has a "Large" mode that shows one approach per row.
- `flows.html`: three clickable flows (publish from a prompt; create and share a test; review results). One progress line runs across all three ("From prompt to first session").
- `board.css`, `board.js`: presentation only (frame scaling, palette and layout switches, the playable transcript, the flow steppers).
- `glass-v3.js`: a copy of `../glass/glass-v3.js`.
- `shots/`: screenshots at 1440 and 390, plus the Large layout, the Clear palette, the session view and the proposed cursor approach. The docs copy has the full-page ones as JPG; the phone one is at half size.
- Rebuild: `python3 build_components.py`, then `python3 build_flows.py` (which also builds screens.html). Screenshots: `node shoot.cjs <page> <width> <name> [query]`. Query options: `palette=clear`, `layout=large`, `glass=0`, `f1=2` (opens a flow at a given step).

## What each screen recommends
| # | Screen | Pick | From |
|---|---|---|---|
| 1 | Shell | Sidebar: studio, Home / Sites / Tests, recent tests, usage, account. Rail + sessions column only inside a session. | A |
| 2 | Home | "What's new" feed (sessions, review ready, expiring sites), then tests, then sites. Drafts are folded into one row. No friction quotes. | A (C's progress line as an option) |
| 3 | Create | Three tiles on one page; the chosen way opens below; "what happens next" on the right. Prompt-first (D) for first-run. | A, D |
| 4 | Site detail | Status line with the days left on Free, today's tabs, "Run a test on this site" as the glass button. | A |
| 5 | Test setup | Today's fields in plain words, plus a tester preview. Tasks or Explore freely. | A |
| 6 | Share | One large link on the Test wash, a QR code, "Open as a tester", what is recorded, a ready message. | A + B, C |
| 7 | Sessions | A table numbered from the oldest, one status per row, the first line in their words. | A |
| 8 | Session view | Recording first, the transcript following the audio word by word, findings beside it. C's article view as a "Read" toggle. D (proposed) adds the cursor and clicks. | A + C |
| 9 | Review | What to fix first (quotes, play moments), themes, where testers disagreed. The written version is the download and the email. | A + C |
| 11 | Plans | One page for plans; modals that open from real moments; the limit shown in place. | B + A |
| 12 | Guidance | Short guides in place, plus a "How it works" panel whose text feeds aeroapp.ai guides. | C |
| 13 | States | A table of the loading, empty, error and processing state for every screen, plus frames under each screen. | |

## Glass: where it belongs (proposal)
- One primary action per view (page header or modal footer): ink V3 glass, quiet.
- Floating player controls over the recording (pill), so the rim picks up the prototype's colour.
- The tester task panel (shared piece). An opaque-enough plate (92%) with two hairlines keeps it legible over black, white, bright and busy prototypes.
- Everything else is flat. The area washes (Share, Site header) are where the rim colour shows best.

## Truth checks
- Transcripts arrive after the session. Processing shows "Transcript arriving, usually about a minute" and grey shapes, never typing.
- The word-by-word highlight while the recording plays is true: AssemblyAI word timings are already saved on each session (`functions/index.js`). Press play in screens.html to see it.
- A, B and C have no cursor in the replay. D shows the cursor and clicks as **Proposed**, following `../research/cursor-recording.md`: a cursor and click ripples for HTML sites (Aero's overlay), and misclicks plus a click path for Figma (Embed API). D sits beside today's true version.
- Claude is drawn simplified, in its own colours, labelled "Outside Aero". Never inside Aero's frame.
- Plans and limits come only from PRICING-FACTS. No "a month" after a session count.
- Every field is from today's code: tasks, welcome, thank you, record screen, record audio, difficulty rating, pinned version, link status; site tabs Overview, Versions, Settings, Domain, Analytics. The one exception: session target is dropped from Setup (proposed, B14).

## Proposed (needs new work), in one list
Inline player, the word highlight in the app, friction points that jump to their moment, the "What's new" feed and the seen-at time, the draft-on-real-input rule, "Now test it" after publishing, landing on Share with the link copied, QR code, "Open as a tester" preview, the expiry countdown and offline state, "Run a test on this site", stable session numbers, the "No audio" status, server-side review with "Based on N of M", "Download summary", Duplicate test, the tester preview in Setup, moment upgrade modals, studios and the switcher, the How it works panel, the cursor and clicks (D), and the dark theme.

## Decisions needed from Duane
1. Palette: Morning or Clear.
2. Home: A (what's new), or C (by prototype) for people with only a few projects.
3. Session view: A with a "Read" toggle for C's article view. Should the cursor and clicks (D) be scheduled?
4. Over the Free limit: stop new sessions, or record them and keep them hidden until upgrade?
5. Studios: build them, or keep the account-only switcher?
6. Glass placement as proposed: one primary per view, the player pill, the task panel.

## Weakest screens (iterate next)
- Plans and usage (11): the moment modal is fine, but the plan page is a plain grid and has no history or invoices.
- Guidance (12): approach B's panel is a list. The articles themselves aren't designed yet.
- Shell C and Session C (theatre): cramped at 1180 wide, with a lot of empty space below.
- On phones every approach falls back to the same mobile layout. Only one phone layout per screen is designed, not one per approach.
- Frames shown side by side at three across are small (about 0.37 scale); use Large to judge detail.
