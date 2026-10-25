# Aero website round 4 (24 Oct 2026)

Act as a studio: brand expert, art director, copywriter, UX and UI designer, animator and motion designer, graphic designer, video maker, IA and SEO adviser.

## Read first (all of it)
- `/home/claude/figmaapp/docs/brand/DECISIONS.md`: the newest section, "24 Oct 2026: feedback on the homepage rework", is this brief. Every line applies. Also the truth rules.
- `/home/claude/research/web3/research/proposition-research.md`: competitor copy, pricing (like for like), pain points, archetypes, proposition options.
- `/home/claude/figmaapp/docs/brand/TONE_OF_VOICE.md`, `PRICING-FACTS.md` (only source for our plans; transcription and summaries are on every plan), `BRAND.md`.
- Homepage rounds: round 1 = `/home/claude/research/mockups/studio/home.html` (the liked one: one big hero, then text + image per section); round 2 = `/home/claude/research/web2/home.html` (closest copy); round 3 = `/home/claude/research/web/home.html`. Screens in `/home/claude/research/compare/img/`.
- v3 app UI (the real screens to use): `/home/claude/research/v3/make/pages.html`, `/home/claude/research/v3/review/pages.html`, shots `/home/claude/research/v3/hi/`. Shared stylesheet copied to `/home/claude/research/web3/shared/aero.css` (+ `washes.py`, `glass-v3.js`, logo SVGs).
- Glass hover lab (may still be in progress): `/home/claude/research/web3/glass-lab/` (use its recommended hover once it exists).

## Shared changes (Team H does these first, in `web3/shared/`, then tells nothing: Team S waits for the file to change)
- **Step colours: Publish blue, Test green, Review orange.** Regenerate the washes with `washes.py` (keep the smooth 8-stop curve and grain; keep hues soft; blue must not clash with the logo dot blue, use a sky-cornflower). Add step pill styles (`.pill-publish` etc.).
- **Headline full stop**: the logo's round blue dot, not Geist's square stop; the logo dot slightly bigger.
- **Glass where it reads**: top nav as glass, Sign in and primary buttons on gradients as V3 glass; ink buttons elsewhere.

## Team H: the homepage `web3/home/home.html`
- **Hero**: rework the whole area. Proposition: lead with "One prompt and it's live. One link and it's tested." (research option 1), with the rotating made-with idea available (Claude artifact | Figma prototype | Lovable app | HTML site) in the sub line or first line; include a quick switcher (`#p1/#p2/#p3`) showing research options 2 and 3 too. Buttons placed where they work best (not necessarily under the headline).
- **Hero animation** (the main job; quick, dynamic, shows the real flow and features; about 15 to 20 s loop; respects reduced motion):
  1. Publish: a browser window with Claude (simplified, clearly Claude's UI, kept separate) building a page with the preview on the right; one prompt pasted; then Aero's app shows it live at pocket.aeroapp.ai.
  2. Test: the test link is copied and shared; a second browser window (someone else's computer) opens it; the tester screen with the task panel over the prototype, the prototype moving through screens, and their voice shown (waveform, "Recording"). No cursor drawn.
  3. Review: Aero's session analysis in **dark mode** (v3 Watch view): playback with word highlight, friction points, then Insights across sessions.
  A **progress bar along the bottom** shows the stage (Publish, Test, Review), with small blue icons and text lines that fill in blue like a timeline. No "Example session" or "Recorded replay" labels.
- **Three sections, Publish (blue), Test (green), Review (orange)**: round 1's layout (text + image per section), each with a coloured pill label and a **subtle, targeted animation** of its own UI: Publish: pasting the prompt, then published (mention HTML upload and Figma in text); Test: copy the link, someone opens it, recording starts, no software; Review: a voice clip with the transcript highlight, then all sessions summarised (more abstract). Each states its sell and removes a pain (publish: no hosting or domain jargon; test: no software for testers, no set-up; review: no hours going through recordings, still a good read).
- **What Figmafolio users get**: a compact strip: custom domain, password protection, versions, user testing.
- **Use cases / archetypes**: 3 to 5 short scenario cards from the research (portfolio from a folder in one prompt; idea at night, 3 testers, insights by morning; client site behind a password...). "For people who make things" can head it.
- **Pricing on the homepage**: a like-for-like competitor comparison (self-serve plans only, footnotes for session counting and unverified figures; never claim what the research marked unverified), with "Priced for one designer, not a corporate" as its line, linking to the Pricing page. Our plans: Free to start, from $3.
- **FAQ**: tight, no wasted white space (two columns or a dense accordion).
- Gradients per section; optionally a very slow drift (check it doesn't fight the animations; respect reduced motion).
- Drop "From prompt to first session" as a section.
- Copy: round 2's as the base, British spelling, sentence case, no em dashes, AI never the headline, no "Watch people use it", no "Same link", no `claude mcp`.

## Team S: the site's other pages `web3/site/`
- **Nav**: every menu item is its own page: Features, Pricing, Use cases, Guides, Blog (and Log in, Start free). Glass nav.
- **features.html**: every feature of the app grouped under Publish, Test, Review (and Account / plans), each group with its pill and wash, each feature a short line and a small real UI crop; read the app code if needed to be complete (`/home/claude/figmaapp/src`), and the decisions for what is planned vs live (mark planned ones "Coming soon" only if decided).
- **pricing.html**: our four plans exactly from PRICING-FACTS, "Priced for one designer", the competitor comparison table with sources and footnotes, FAQ about billing.
- **blog.html** (index) + one post template: HeyBooking-style dated posts for features shipped (use real dates from the git log of `/home/claude/figmaapp` for real Aero features, e.g. OpenRouter switch, transcription fix, HTML hosting, agent publishing; read `git log --since=2026-03-01 --format='%ad %s' --date=short` and pick 8 to 10 user-visible ones; plain-language titles).
- **use-cases.html**: the archetypes and scenarios as pages-in-a-list (each could become an SEO page later), plus one full SEO task page template example: "Publish a Claude artifact" (H1, steps, FAQ, related).
- Same header, footer and shared CSS as the homepage; light only.

## Both
- Light only; desktop 1440 and phone 390, no sideways scroll; copy in one data block per page.
- Your own Playwright script in your folder; screenshots at 1440 (2x) and 390 into your folder's `shots/`, plus an MP4 of the hero loop (Team H). Look at every shot and fix what's broken.
- Work only in your folder (Team H also `web3/shared/`). Report back briefly with what needs Duane.
