---
brand-sync: figmaApp docs/brand is the source. Copy this file unchanged to aero-landing-page/docs/brand/.
version: 2026-10-23.4
---

# Aero brand and product decisions

The running log of what Duane decided, newest first. Add a line whenever he decides something; never delete a line, strike it through and say what replaced it. The full evidence is in `research/conversation-audit.md`.

## 23 Oct 2026: after the UI directions board
**Look**
- **A (Studio) is the base.** "Looks great, feels like Figma, which isn't bad." Round 5 versions were too busy.
- **Dark mode too**, especially for session review (video, prototype, sound); demos and videos of session review in dark.
- **Buttons: ink.** Fully rounded pill only where it's needed (a floating task pill), rounded rectangle elsewhere. Still a little glassy: the V3 glass agreed earlier, kept subtle. Soft graphite "isn't bad" as a fallback.
- **Logo: "Aero." in Geist 500 with the blue dot.** Blue is the secondary or tertiary colour: the dot can become the loader, the playhead, the video player accent.
- **B's colour is too much**: end-to-end colour, gradients and coloured tiles feel basic and assume every project is linear (someone may only have a site). A subtle wash is fine: Publish wash before upload, and after upload the wash could pick up the site's own colours very slightly.

**Structure**
- **Sites and Tests stay separate.** Combining them is more confusing. Sites come first naturally; a site can become a test (its own test link). People can also go straight to a test. Both should get custom domain, favicon and so on.
- **Site to test copies** (Duane, 23 Oct): "Test this site" makes the test its own copy with its own link; the test is then updated from the test, never affecting the live site. The reverse works the same way ("Publish as a site" copies). Simpler than keeping versions in sync. Both keep their own versions.
- **Going straight to Test** hosts the prototype under the test (versions, domain, favicon), shown only under Tests.
- **New sites are public by default** (anyone with the address), with a switch to make them private.
- **Lists:** sites as blocks with a real preview (screenshot, cached iframe); tests as a status line (sessions, live or not). Tests can show a preview too.
- **Sidebar:** keep it collapsible (today's arrow). Maybe the workspace name at the top instead of the logo. Maybe show a single site or test in the sidebar when there is only one.
- **Empty states must teach the features without overwhelming.** None of the empty states so far convinced; D's empty player didn't make sense.
- **Home "what's new"** as a timeline of events is interesting (could include site visits); check it can be built.

**Sessions and review**
- **Each session is a tester with a name.** Ask testers their name at the start (today it says "Anonymous Tester"); when the owner tests with "Open as tester", record "You".
- **Each session gets a summary**: per task when tasks were set, a plain session summary when not, and a clear "no audio" state. A big button to go deep into the session with video. Show all the details (browser, time, device).
- **Cross-session analysis is its own overall place**, not under the Sessions tab (maybe its own tab, maybe Home; needs an empty state). Views by task, by theme, by priority; longest task, most friction; summary and scores first, detail after. Keep links to each session.
- **Session review:** A's layout "looks really cool", dense. Tasks on the player timeline; tags beyond friction (good, delight, critical) with filters; word highlight in the transcript; click a line to jump; flexible layout (video small or big, a reading mode with notes vs a video mode). Keep "Download transcript" and "Download video". Research how pro tools lay out transcript, video and insights before deciding.
- **Liked:** C's lead quote; D's sound bite with waveform, playable inline (one play control, not two); D's task timeline and quote cards with play; "4 of 5 testers". D's shared-clock bars and B's session side panel were not clear.
- **The prompt flow is a prompt**, not a connector (true in the code: the prompt calls Aero's API with a key). Don't ask to publish before there is a link, file or prompt.
- **Create:** one guided flow per source (pick Figma, HTML or prompt, then that flow; switching goes to the other flow). C's "Done" steps plus round 5's radio choice. B's create is too much.
- **Upload:** A liked. B's guidance and "Now test it" setting the test up straight away liked. Settings (name, badge, domain) can sit on the site's one page. E's update and free 7-day notes liked; its "Run test" button too big.

## 23 Oct 2026: after the app UI round
- **A step was missing: UI directions before components.** Before tightening components, show each main screen (home, sessions, session review, publish from a prompt, upload HTML, review across sessions) drawn in each direction (A, B, C, D) next to the app UI round and today's app; decide what works and what doesn't; then do the detailed components. The app UI round is good work to reuse and tighten after that decision.
- **Marketing versions of components are still to do:** the real component, simplified and bigger, for the website, videos and cards.
- **Primary button colour not decided.** Black "looks nice", but explore button options in the directions stage first.
- **Logo not decided.** "Aero." with the blue dot is still the favourite, but earlier mockups used "Aero" in full and other forms; explore in use.
- **Avoid patterns that look AI-made:** white cards with a coloured stripe down one side; icons sitting in pastel rounded boxes.
- **Work as a team of roles** (marketer, brand, copywriter, UX, UI, information architect, animator, graphic designer), as in round 5.

## 23 Oct 2026: after the round 5 mockups
- **UI first, then the website.** Design the whole app UI and the shared design system first; the homepage, content pages and videos are rebuilt on it afterwards.
- **One design system, two repos.** It lives in figmaApp (`docs/brand/` and `src/styles/aero-design-system.css`). The same files are copied into aero-landing-page as we go. Every synced file carries a `version:` header; whoever touches it takes the newest version in either repo, ports any newer change back, then copies it across. See `DESIGN_SYSTEM_PLAN.md`.
- **Marketing components are simplified real components.** The website, animations, videos and illustrations use the app's own components in a demo mode with example data, not hand-drawn copies, so UI changes flow through.
- **Direction to iterate:** A (Studio) as the base: one big hero showing the real app. Then three sections, **Publish, Test, Review** (not Watch/Read), each on a soft gradient of its own colour (B's clarity, A's softness, no colour in the nav). A little real context from C (one tester, one Sunday morning), not the full story.
- **Logo:** A's "Aero." in Geist with the blue full stop is the favourite. B's Funnel Display is out.
- **Keep these lines:** "One prompt and it's live." "Made for people who make things." "In their own words." "From prompt to first session."
- **Video:** follow A's in-app style, slower, as separate scenes: the Aero dashboard (a made-up studio name, never Duane's) → Claude building the page (Claude's own UI, accurate but simplified) → one prompt → back in Aero, published at a real-looking URL → create a test → someone else, on their own computer, takes the test → results. Keep D's progress line along the bottom and C's voice highlight with insights.
- **Be true to the app** in every mockup and video (Duane's point, 23 Oct). For example:
  - The transcript is made after the session. Highlighting words while a recorded session plays is true, and liked: keep it.
  - Tab recordings show no mouse today. Can it be recorded? Yes, with work: see `research/cursor-recording.md` (full cursor for HTML sites through our overlay script, clicks and misclicks for Figma through Figma's Embed API). Until that ships, don't show a moving cursor in a replay.
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
