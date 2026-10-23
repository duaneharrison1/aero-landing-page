---
brand-sync: figmaApp docs/brand is the source. Copy this file unchanged to aero-landing-page/docs/brand/.
version: 2026-10-23.4
---

# Aero playbook: re-evaluating the product, brand and website

The same process HeyBooking went through in October 2026 (see the HeyBooking repo, `docs/brand/PLAYBOOK.md`), run on Aero from 21 Oct 2026. The steps are the same; this file records what was done and **what was done differently**, so the next product starts from the better version.

## Steps and status
| Step | Status | Where |
|---|---|---|
| 0. Repair what is broken first | Done 21 Oct: recording, transcripts, AI notes on OpenRouter with fallbacks | DECISIONS.md |
| 1. Research | Done 22 Oct: code inventory, competitors, SEO, past decisions, live site | research/strategy-dossier.md |
| 2. Strategy | Done 22 Oct: lead, proofs, audiences, pricing check, SEO page tree, 10 decisions | research/strategy-dossier.md |
| 3. Art direction | Five rounds (see the log) | mockups/, research/reference-analysis.md |
| 4. Logo | Direction chosen ("Aero." in Geist, blue dot); refinement and motion to do | BRAND.md, logo/ |
| 5a. UI directions | 23 Oct: every main screen in A to D, beside the app UI round and today's app; buttons and logo options; waiting on Duane's marks | directions/ |
| 5b. App UI v2 on A | 23 Oct: two teams, one shared stylesheet, light and dark, built on research into pro review tools; waiting on Duane's marks and 13 questions | app-ui-v2/ |
| 5. Copy, UX, UI, motion passes | After 5b: tighten the app UI round into the agreed components and their marketing versions, then the website | DESIGN_SYSTEM_PLAN.md |
| 6. Illustration and card kit | To do, built from the marketing kit | DESIGN_SYSTEM_PLAN.md |
| 7. SEO | Plan done (task pages); pages to build later | research/strategy-dossier.md |
| 8. Make it automatic | Started: docs/brand, CLAUDE.md rules, two-repo sync rule | this folder, CLAUDE.md |

## What was done differently from HeyBooking
**Before brand work**
- The product was broken (no transcripts or insights), so the playbook started with a repair: model tests on real transcripts for price and quality, a fallback model list, and an end-to-end test run with a headless browser and a fake microphone.
- Aligned with Duane before starting, in batches of up to four multiple-choice questions, each with a recommended option. Faster than open questions.

**Research and strategy**
- Research ran as three parallel helpers (code inventory, competitors and SEO, past decisions) while the live site was captured. Helper claims were checked before use.
- Past decisions mattered more than for HeyBooking: Aero already had a locked headline and "never lead with AI" (July 2026), and the live site had drifted from both.
- Markets: no country pages. Aero's buyers search by task, so the SEO unit is the task page (/test/ai-prototype, /sites/html...), not /hk/.
- A per-job comparison (Aero against the best alternative for each job) was added at Duane's request.
- "Fix soon" truth problems (blank legal pages, placeholder FAQ, wrong limits) were split from brand work and shipped as separate PRs.

**Art direction took five rounds, not one**
1. Moodboards of five looks, same copy and example data. Rejected: weaker than HeyBooking's because it skipped the brand.
2. Brand first, as HeyBooking did: drawn wordmarks (fontTools and HarfBuzz outlines), a mark, icons checked at 16px, then colour, type, buttons and a homepage slice. A logo built from today's "Aero." was added at Duane's request ("Full stop") and won.
3. Each option led by one reference he respects (Claude, Cursor, Linear, OpenAI, Figma, Nothing), each with its own homepage layout. Showing the influence plainly mattered.
4. Combinations of what he liked, on Full stop, plus a 25-typeface study. Rejected as "mashed together".
5. Full mockups: one written creative brief, four parallel design teams each building a homepage, app screens, a content page and an MP4 animation, an independent reviewer, then a fix round. Far stronger. The UI turned out to be the most liked part, so the order changed: UI first.

**Lessons**
- A logo set in a system font (Georgia) must be checked on a machine that has the font. The container didn't, and an early comparison silently fell back to another serif.
- Give helpers a facts file (pricing, product limits) up front. Three of four teams invented plan features without one.
- Stock photos read as fake for this product. Use the real UI and illustration.
- Liquid glass only reads over detailed content; on flat white it looks like nothing. Show glass over real content, and keep it quiet by default.
- Never show a transcript typing live, or a cursor moving in a replay: neither is true.
- Helpers sharing a scratch folder overwrite each other's scripts. Give each helper its own folder and file names.
- Save decisions into the repo as you go (this folder), not only in published boards.
- Don't jump from liked mockups straight to a detailed app UI. Draw each main screen in every direction first and let the owner pick per screen; that was the missing step (23 Oct).
- Research how pro tools do a screen before redrawing it (session review: Lookback, UserTesting, Grain, Frame.io); the owner asked for it and it settled layout questions quickly.
- Name the patterns that read as AI-made (side-stripe cards, icons in pastel boxes) in the brief, so teams invent their own status marks.

## Log
- 21 Oct: repair, model tests, OpenRouter fallback, transcription dedupe.
- 22 Oct: research and strategy doc; fix PRs (#262, #263, landing #5); brand rounds 1 to 4; glass lab; app UX review; round 5 mockups.
- 23 Oct: feedback on the mockups; this folder, the decisions log, the design system plan and CLAUDE.md rules; cursor and Figma Embed API investigation; the app UI round (files in app-ui/); the UI directions stage (directions/).

## Boards and labs (private links, Duane's account)
| What | Link | Status |
|---|---|---|
| Research and strategy (doc) | https://claude.ai/artifact/LUswUMf2ZwPpMJUmThGrA5 | Current reference |
| Round 1 art directions | https://claude.ai/artifact/RG3skBxLXrb2byGAsGhjNp | Rejected |
| Round 2 brand | https://claude.ai/artifact/Epbx7nLfBcqRi9BQ4DUmSs | Superseded |
| Round 3 brand | https://claude.ai/artifact/MdD4Hhri8YRxox7PqrJS1t | Superseded |
| Round 4 brand and font study | https://claude.ai/artifact/UuZ6VJwV65nD8LQKjHPfVX | Font study still useful |
| Glass button lab | https://claude.ai/artifact/4dajXGEv5aYB5hsyS5mFVw | V3 chosen |
| Round 5 mockups (A Studio, B Colour, C Story, D Replay) | https://claude.ai/artifact/8BPToDfdd57Bpm1wpxWVtN | Feedback 23 Oct |
| App UI round (screens, tester flow, flows, components) | https://claude.ai/artifact/Y1vWdd2BsZdkn6HmvTW5Zk | To tighten after the directions stage |
| UI directions (every screen in A to D, buttons, logo) | https://claude.ai/artifact/6iCo36JkjhvNsaYxLUfbpb | A picked 23 Oct |
| App UI v2 (A refined, light and dark) | https://claude.ai/artifact/Mxv3bb9Pf1gkB5TYnY8mw3 | Current; waiting on Duane's marks |
