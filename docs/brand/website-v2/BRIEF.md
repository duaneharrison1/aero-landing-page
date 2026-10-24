# Homepage rework: round 5 A's structure, v3 UI (23 Oct 2026)

Duane: "I really liked the hero before... it was a whole app at an angle and someone actually using it, the session. The timeline isn't a big feature; Publish, Test, Review is, and you aren't showing any of it." So the last round (`/home/claude/research/web/home.html`) shrank the product into small cards; that was wrong.

## Do this
Rebuild the homepage keeping **round 5 A Studio's homepage structure and scale** (`/home/claude/research/mockups/studio/home.html`, screenshot `/home/claude/research/mockups/review/studio-home-d.png` and fold `studio-home-fold.png`), but drawn with the **v3 app UI** (`/home/claude/research/v3/shared/aero.css`, `v3/make/pages.html`, `v3/review/pages.html`, shots in `v3/hi/`).

- **Hero:** headline and sub as round 5 A (top left headline, sub and buttons right), with the rotating made-with part: "Publish your [Claude artifact | Figma prototype | Lovable app | HTML site]. Watch people use it." Under it, the **big full-width app window, slightly angled as in round 5 A, showing a real session being reviewed** (v3 Watch view in light: the tester's recorded tab with the prototype, the follow-along transcript, friction points, the timeline with task regions). It plays as a calm loop of a recorded session playing back: the playhead moves, the current words light up as they're said, a friction point is highlighted when its moment comes. Truth rules: no mouse cursor drawn anywhere, no transcript typing in live (the whole transcript is there; only the highlight moves), label "Example session: Pocket, a payments app. Maya, thinking aloud."
- **Publish, Test, Review**: each as a full section with a **large real app screen** like round 5 A had (not small cards), on its step wash:
  - Publish: the v3 create flow / one prompt panel (copy one prompt into the chat where you built it; never "claude mcp", never a connector to install) and the published site page.
  - Test: the test link / share and the tester's screen with the task panel over the prototype (someone on their own computer).
  - Review: the session review and Insights ("4 of 6 testers", quotes you can play).
  Copy: "One prompt and it's live.", "One link. Their screen and their voice.", "In their own words." / "What to fix, in their own words."
- Keep round 5 A's other sections where they were (from prompt to first session, pricing, FAQ, closing line) but: no stock photos of people (round 5 had them; replace with illustration or drop the section), pricing exactly from `/home/claude/figmaapp/docs/brand/PRICING-FACTS.md` (Free, Basic $3, Solo $6, Pro $19; round 5's "Starter" plan is wrong), no founder, no em dashes, British spelling, AI never the headline.
- Light only. Desktop 1440 and phone 390, no sideways scroll. Copy in one data block at the top.

## Deliver
- `/home/claude/research/web2/home.html` (copy aero.css etc. into web2/), `NOTES.md`, your own Playwright script, full-page and fold screenshots at 1440 (2x) and 390 in `web2/shots/`. Look at every shot and fix what's broken. Work only in web2/. Report back briefly.
