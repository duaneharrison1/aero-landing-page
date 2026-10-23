---
brand-sync: figmaApp docs/brand is the source. Copy this file unchanged to aero-landing-page/docs/brand/.
version: 2026-10-23.1
---

# Aero brand and product decisions

The running log of what Duane decided, newest first. Add a line whenever he decides something; never delete a line, strike it through and say what replaced it. The full evidence is in `research/conversation-audit.md`.

## 23 Oct 2026: after the round 5 mockups
- **UI first, then the website.** Design the whole app UI and the shared design system first; the homepage, content pages and videos are rebuilt on it afterwards.
- **One design system, two repos.** It lives in figmaApp (`docs/brand/` and `src/styles/aero-design-system.css`). The same files are copied into aero-landing-page as we go. Every synced file carries a `version:` header; whoever touches it takes the newest version in either repo, ports any newer change back, then copies it across. See `DESIGN_SYSTEM_PLAN.md`.
- **Marketing components are simplified real components.** The website, animations, videos and illustrations use the app's own components in a demo mode with example data, not hand-drawn copies, so UI changes flow through.
- **Direction to iterate:** A (Studio) as the base: one big hero showing the real app. Then three sections, **Publish, Test, Review** (not Watch/Read), each on a soft gradient of its own colour (B's clarity, A's softness, no colour in the nav). A little real context from C (one tester, one Sunday morning), not the full story.
- **Logo:** A's "Aero." in Geist with the blue full stop is the favourite. B's Funnel Display is out.
- **Keep these lines:** "One prompt and it's live." "Made for people who make things." "In their own words." "From prompt to first session."
- **Video:** follow A's in-app style, slower, as separate scenes: the Aero dashboard (a made-up studio name, never Duane's) → Claude building the page (Claude's own UI, accurate but simplified) → one prompt → back in Aero, published at a real-looking URL → create a test → someone else, on their own computer, takes the test → results. Keep D's progress line along the bottom and C's voice highlight with insights.
- **Truth rules for every mockup and video:**
  - The transcript arrives after the session; never show it typing live during recording. A replay may highlight words as the audio plays (word timings are stored).
  - Recordings of a browser tab do not show the tester's mouse. Don't show a cursor moving in a replay.
  - Keep Aero's interface and Claude's interface visibly separate.
  - Use real-looking URLs (name.aeroapp.ai, aeroapp.ai/...).
- **No stock photos.** They look fake; use illustration and animation instead.
- **Must design:** the tester screen (what testers see), with tasks over prototypes of any colour, and every variation: no tasks, which tab opens after creating a test, and so on.
- **More guidance everywhere:** explain how transcription and insights work, in the app and in content pages.
- **SEO:** hundreds of task pages later (publish a Claude artifact, publish a Lovable app, publish a Figma prototype, test a Figma prototype...). Only keep a "who it's for" section if it earns its place for SEO.
- **Glass:** the V3 glass ("Snell-law capsule refraction, Fresnel edge reflection, key-light specular") is the pick, pill or rounded rectangle depending on the design. It must work inside the app too.

## 22 Oct 2026: brand rounds 1 to 4
- Round 1 rejected. Timecode looked like audio software, Contrail like an airline, Redline like a wireframe; Cobalt was closest but old school.
- Round 2: Index looked like a train; the set felt too space-related; caustic buttons were "too much". Full stop (today's "Aero." refined) "looks expensive".
- Round 3: liked the Full stop logo and its blue dot, the pocket.aeroapp.ai window, Precision's dark angled app window (and a light version), Plain's colour-wash cards, a little of Canvas's colour. Disliked the Dot (dot matrix) direction and the search bar. Unsure about round versus square buttons.
- Round 4: Studio's sticky note forced and Caslon too elegant; the sans liked but the headline too bold; cursor name tags forced; options too similar. Asked for real mockups of homepage, app and content by a team of roles.
- Glass: buttons must take colour from what is near them, subtly, by distance and amount, like his original engine. V3 picked.

## 22 Oct 2026: strategy (from the research dossier)
- Homepage lead: the loop. "Publish your prototype. Watch people use it. Same link."
- Free sites: keep the 7-day window, say it clearly.
- Test sessions: move to a monthly allowance and keep history (proposed 3 / 10 / 30 / 100, to confirm when built). Not live yet.
- Upload your own video: later, hidden inside a test, paid plans only, about 60 minutes, consent box.
- Fix-soon list: separate small changes, each approved by Duane.
- Site counts per plan: enforce them; people already over keep their sites but can't add more.
- Scope: website plus the app dashboard and first run.
- Pro extras: keep priority support, drop the portfolio review.
- No founder or "one person" on the site. An About page, if useful for SEO: made by UX and UI designers with airline, banking and travel app backgrounds; no names or places.
- Change Aero files freely; flag anything shared with Figmafolio (Clark owns Figmafolio) before merging.
- AI stays in the background: named only on the way in ("built with your AI tool") and the way out ("transcribed and summarised").

## 21 Oct 2026: repair
- AI back on OpenRouter with a fallback list (GLM flash, then Qwen flash); synthesis runs Qwen first.
- Transcription runs once per session (transaction claim).
