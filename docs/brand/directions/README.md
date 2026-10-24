---
brand-sync: figmaApp docs/brand is the source. Copy this folder unchanged to aero-landing-page/docs/brand/.
version: 2026-10-23.2
---

# UI directions stage (23 Oct 2026)

The step Duane asked for before tightening components: every main screen drawn in each round 5 direction, side by side with the app UI round and today's app, plus each direction's flow, its marketing kit, and button and logo options.

- `BRIEF.md`: the brief every team worked from (product truth, banned patterns, deliverables).
- `studio/`, `colour/`, `story/`, `replay/`: one team per direction. `pages.html` holds sections p1 Home, p2 Sessions, p3 Session review, p4 Publish from a prompt, p5 Upload HTML, p6 Review across sessions, f1 the flow, m1 marketing kit. `NOTES.md` says what each team would keep and drop.
- `kit/`: buttons (b1 families, b2 in context) and logo (l1 options, l2 in use, r1 pairings).
- `kit2/`: four realistic button options drawn on seven real app moments (dashboard, session player, share, delete confirm, new test, tester panel, disabled and loading), with measured contrast (`contrast.json`).
- Board v2 (23 Oct, after Duane's notes): one long page, no inner scrolling, every picture full width at 2x; each screen starts with today's live app (captured from app.aeroapp.ai at 2x and stitched with `stitch.py`; not committed because they show real account data); E shown one layout per picture (`shoot-e.cjs`).
- `notes.json` (built by `notes.py`): the per-tile works / doesn't and the "how it ties together" read; `build_board.py` + `board_template.html` build the board.
- Screenshots are not committed (about 20 MB); rebuild them with each team's `shoot-*.cjs`.
- Board: https://claude.ai/artifact/6iCo36JkjhvNsaYxLUfbpb (Duane marks tiles Keep, Parts of it or Drop).
