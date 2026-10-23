---
brand-sync: figmaApp docs/brand is the source. Copy this file unchanged to aero-landing-page/docs/brand/.
version: 2026-10-23.1
---

# Aero app UI round: brief (step 1 of the design system plan)

Duane, 23 Oct: "the UI looks incredible ... we might have to work on that first, as the UI is shared with the marketing website." This round designs the **whole app**, screen by screen. Each screen shows the best approaches from the round 5 mockups side by side, in the agreed brand. It also starts the real design system: tokens plus components, built so the UI, story and copy can change without rebuilding.

Read first: `../DECISIONS.md`, `../BRAND.md`, `../TONE_OF_VOICE.md`, `../DESIGN_SYSTEM_PLAN.md`, `../PRICING-FACTS.md`, and `../research/app-ux-review.md` (flow map, bugs B1 to B17, page-by-page fixes).

## Brand to use
- Logo: "Aero." in Geist with the blue full stop (`../logo/`). Mark "A." in the sidebar.
- Type: Geist (light headings, never heavy), Geist Mono for timecodes and labels.
- Colour: ink, white, mist, line, Aero blue for the dot, links, selection and playhead. One soft gradient per area: Publish, Test, Review (propose two palettes).
- Buttons: V3 glass (`../glass/glass-v3.js`), quiet. Propose where glass belongs in the app: primary actions, the tester task panel, floating player controls.
- Example studio: **Kestrel Studio**, example owner Mia Chen. Never Duane's name. Example site pocket.aeroapp.ai, a payments prototype.

## Screens (each with 2 to 3 approaches side by side, plus states)
1. **Shell:** sidebar or top bar, studio switcher, nav (Home, Sites, Tests; Review inside tests), plan usage, account.
2. **Home / dashboard:** what's new across everything ("2 new sessions on Pocket", "Insights ready"), real tests and sites first, drafts folded. No friction points from random projects on Home (Duane found that confusing).
3. **Create:** three ways in (Figma link, HTML or zip, one prompt to Claude or ChatGPT), plus "Test an existing site". Only save a draft once there is real input.
4. **Site detail:** URL and status (Live, offline on Free after 7 days with a countdown), versions and roll back, settings (address, password, favicon, badge, domain), "Run a test on this site".
5. **Test setup:** tasks (optional), welcome and thank-you messages, what testers will be asked for. Variation: **no tasks** ("Explore freely").
6. **Share:** one link, copy, QR code, "Open as a tester" preview, a plain line on what is recorded. After creating a test, land here with the link ready.
7. **Sessions list:** consistent numbering (oldest is 1), status (recording, processing: "Transcript arriving, usually about a minute", ready, no audio).
8. **Session view (Review):** the recording at the top, inline; the transcript below or beside it, with **word-by-word highlight as the audio plays** (word timings are stored); click a line to jump; summary, priorities and friction points quoted in their own words, each jumping to its moment. **No moving cursor** (tab recordings don't show the mouse). Show where the transcript and summary come from in one plain line.
9. **Review across sessions:** themes, what to fix first, contradictions; "Based on 3 of 3 sessions"; fewer than 2 sessions shows each session's top issues instead of a dead end.
10. **Tester flow (never designed before):** welcome (who invited you, what happens, what is recorded, stop any time), microphone, screen share (pick the tab), the task panel floating over a prototype **of any colour** (it must stay legible over black, white, bright and busy prototypes: propose how), recording indicator, next task, done and thank you. Variations: no tasks, mic denied, screen share denied, phone (Figma: voice only), HTML on a phone (not supported: say so kindly).
11. **Plans and usage:** usage that matches everywhere ("2 of 3 sessions kept"), expiry warnings, the upgrade modal from real moments.
12. **Guidance:** short, honest explainers inside the app: how transcription works, how summaries and friction points are made, what testers see. Empty states that teach.
13. **States for every screen:** loading (skeletons, never blank), empty, error, processing.

## Rules
- Every screen must be true to what Aero does today, or be labelled **Proposed** where it needs new work (for example the inline recording player, QR code, server-side insights).
- Every flow must make sense end to end. Think like a software engineer and a UX designer: which tab opens, what happens with no tasks, what a tester sees when something is denied.
- Components first: build each screen from a small set of named components (Button, Tag, SessionRow, Player, TranscriptLine, FrictionCard, TaskPanel...) on CSS tokens, so the marketing kit can reuse them.

## Deliverables
- `tokens.css`: the proposed tokens (both palettes as themes).
- `components.html`: the component sheet, with every component and state.
- `screens.html`: screens 1 to 13, approaches side by side, states below each, notes on what is proposed.
- `flows.html`: four end-to-end flows as clickable sequences (publish from a prompt; create and share a test; tester takes a test; review results).
- Screenshots at 1440 and 390, and `NOTES.md`.
