---
brand-sync: figmaApp docs/brand is the source. Copy this file unchanged to aero-landing-page/docs/brand/.
version: 2026-10-25.3
---

# Aero brand and product decisions

The running log of what Duane decided, newest first. Add a line whenever he decides something; never delete a line, strike it through and say what replaced it. The full evidence is in `research/conversation-audit.md`.

## 25 Oct 2026: glass final, and round 7 feedback
**Glass: one final version, no other presets**
- Colour from nearby: yes (as Subtle).
- Caustic: Subtle's (narrower, lower, near the bottom edge, tinted).
- Edge thickness: Subtle's crisper edge.
- Refraction: Subtle's.
- Shadow: off.
- Corners: the less rounded (10).
- Hover: keep the idea of the light changing on the button, but much subtler than Agreed's pointer light, which looked "too obvious and crazy" on the black button and still too much on white. Find a subtler way if the pointer light isn't it.
- Fix in the mockups: the black button looks bigger than the white one, and white buttons such as "Preview as tester" don't look caustic.

**Homepage**
- WhatsApp tab is missing its favicon, and WhatsApp Web could look more realistic.
- Maya's screen tilting the other way and panning left to right looks tacky; improve the handover.
- Pasting the prompt into Claude in the loop happens too fast.

**Features page**
- Keep the colour gradients in the boxes' UI backgrounds; only the section titles don't need one.

**Next**
- A final review of the homepage, the Features page and every UI illustration, by a team of roles (video, animation, illustration, copy, UX, UI, UI engineering, motion, brand).

## 25 Oct 2026: feedback on website round 6 (voice notes)
**Homepage hero**
- Prefers the centred layout: headline and subtext centred, so Start free and See pricing are centred too.
- Build the glass buttons so they can be swapped easily (one component, one settings file), since glass is still being refined. Use it on the website now. The buttons inside the hero animation must use the same component, so a glass change updates them too.
- Remove the caption pill ("Claude publishes it to Aero" etc.).
- The animation is "really cool" and about the right speed. Keep the angle, but it mustn't overlap the Publish, Test, Review timeline. Make those three clickable to jump the video to that step.
- The publish part (paste prompt, send, switch tab, it's there, Visit opens a new tab) is the best bit.
- Going back and choosing "User test this site" happens too quickly; show that click clearly. Copying the link is a bit much.
- Sharing idea: open WhatsApp Web and send the link to someone; they receive it in their own WhatsApp Web on another screen, angled the other way, with different people in it. That's how to show it's someone else.
- Maya: no laptop frame. Use a second screen tilted the other way.

**Other sections and pages**
- The other homepage sections are good for now.
- Features page: too many blue gradients. Section titles get no gradient background (almost no background). At most 6 boxes per section: group features (e.g. upload methods as one, tasks and welcome messages as one) while still mentioning each.

## 24 Oct 2026 (late): feedback on website round 5
**Glass**
- Round 5's caustic looks stronger than the one agreed before, and the slab shows a very thick line of glass. The caustic may be getting confused with the lighting.
- Wanted: a control panel with the buttons and nav in place, where Duane sets the strength of each effect himself (caustic, key light following the mouse, lift, edge thickness...), with a note on how each one works.
- The nav's refracting strip over scrolling content looks too thick.
- First setting from the control panel (25 Oct, "what I have so far"): Subtle with the bottom wall, rim reflection and drop shadow off, white fill a touch clearer. Saved in `website-v5/glass-panel/saved/`. Too many settings: the panel now has a simple mode with 8 sliders.

**Homepage**
- Remove the hero's pause button: it clashes with the test interface.
- The video is a bit too fast, but he likes it overall.
- The task panel should be on the left. Show the voice as the real tester UI does.
- Make it a proper loop: after the review, go back to the main UI, go to Publish, copy and paste the prompt again.
- No gradient behind the hero: white. Tighten the title, subtext and links; they take up a lot of space.
- It isn't clear that Maya is on a different computer. Make the whole video easier to follow for a newcomer, for example Visit opens a new tab and then the page loads.

## 24 Oct 2026 (evening): feedback on website round 4
**Glass and buttons**
- Buttons: go back to the slab of thick glass (rounded rectangle with depth), not the rounded pill.
- Bring back the caustic effect: the button picks up light and colour from what is near it, as in the decided V3 glass. Round 4's buttons lacked it.
- Hover: combine "key light follows" and "Lift". Tone the key light down to a slight effect. It suits the white glass button; it doesn't look good on the black button.
- The top nav must be glass. Round 4's wasn't.

**Homepage hero**
- Go back to the earlier liked hero: the screen at an angle with no background panel behind it. Show one screen, not floating windows.
- Layout still open: maybe buttons under the headline with the description to the side.
- The animation has the right steps but runs a little too fast. Add a cursor for the person's own actions, and highlight each effect at the moment it happens.
- After Claude publishes, show the site in Aero and the live site in a browser. Then back in Aero, go to Test.
- Test must read clearly as a user test. Maybe a phone alongside, maybe a webcam (Aero records screen and voice, never the camera, so a webcam can't be shown).

**Sections and content**
- Round 4's Publish, Test and Review animations were broken (they collapsed while playing), so they still need reviewing.
- No "Coming from Figmafolio?" strip. Put Figmafolio's features (custom domain, password, versions, testing) under their own sections.
- Price comparison must include Maze, and compare like with like in the same unit (always per month).

## 24 Oct 2026: feedback on the homepage rework (round 3 of the homepage)
Rounds named: 1 = round 5 A (liked), 2 = rework on round 5 A's structure, 3 = the previous round.
**Hero**
- The hero animation must tell the **three steps, quick and dynamic, showing all the features** (as round 1 did), not one slow screen: (1) Publish: someone in the Claude app with their site in the preview on the right, one prompt, then it's live on Aero; (2) Test: share the link, another browser window, someone opens it and does the test, their voice shown; (3) Review: the analysis (today's session screen), **in dark mode**; the rest of the page light. Keep the **progress bar along the bottom** showing which stage it's at. Pace: quicker than round 2 (too slow, prototype didn't move).
- No "Example session" or "Recorded replay" labels on the homepage: simple and confident.
- Rework the whole hero area; buttons maybe not under the headline.
- Under the hero: keep the small blue icon and text for the three steps, but as lines that fill in blue like a timeline (all black is too much).
**Proposition and copy**
- "Watch people use it" sounds weird. Review the whole proposition: speed, one prompt to publish, an easy place to manage your work, use it as a website, test it straight away ("get feedback on it instantly", "test it immediately"). Avoid cliché ("in seconds"). The ethos: less time on tedious things; "I can't think of a quicker way to publish something and then test it, with very little set-up, on one platform: fast, simple, cheap, even free."
- Writing: round 2's copy is closest.
- "From prompt to first session" section may no longer be needed (the hero tells it).
- "Priced for one designer" (not a corporate) is liked; move it elsewhere.
- Homepage pricing: compare competitors' self-serve prices like for like (not panels), rather than only our own plans.
- "For people who make things": think through archetypes; each step has its own advantage (publish: no tech knowledge, no hosting or domain jargon; test: user-testing pain points removed, no software for testers; review: no hours going through recordings, automatic, still a good reading experience).
- Use cases and scenarios, from real pain points (Reddit, forums): e.g. a portfolio from a folder of work via one prompt; a product idea the night before, a prototype sent to 3 people, insights by morning.
- Everything Figmafolio offers, Aero has; say so, even briefly: custom domain, password protection, testing.
- Study Maze and competitors' copy and language.
**Sections**
- Publish, Test, Review sections: round 1's layout (big hero then text and image per section) is the nicest, but not all on one UI element; round 2 too zoomed out with needless labels; round 3 lazy (two UI elements stacked). Each section's image is a **subtle, targeted animation** of its specific UI: pasting the prompt then published; sharing the link then someone opening it and recording; the session voice then all sessions (more abstract). Each has its own sell: one prompt to publish (also HTML upload and Figma, in text or UI); just share a link, no software for testers; transcribed automatically, insights ready, synthesis across sessions.
- **Step colours change: Publish blue, Test green, Review (analysis) orange.** Possibly a coloured pill label per section (Publish in the blue pill), since the washes are subtle and each step has many features.
- Gradients can change per section; maybe they slowly move or shift over time (even in the app), if not too much with the animations.
- The Questions section wastes white space; tighten it.
**Type and brand**
- Headline full stops: use the logo's round dot (Geist's own full stop is square). The logo's blue dot can be slightly bigger. No blue dot on small labels ("Example session", "Prototype hosting and user testing").
- Round 3 of the brand rounds used the blue dot in headers well.
**Buttons and glass**
- The caustic (V3) glass stays decided; it must be visible: use it where it reads (the top nav, Sign in as it scrolls over the page, buttons on gradients). Buttons don't need to get bigger. Explore hover options where the light refracts differently as if the button lifted, without moving or resizing (e.g. the cursor moving the light). Options, plus a simple one.
**Site structure and SEO**
- Every top menu item is its own page (Features, not Product). Features lists every feature of the app, grouped under Publish, Test, Review.
- A blog like HeyBooking's: dated posts for features shipped over time, so the site looks active. Now or later, don't forget it.
- Keep the hundreds of SEO task pages in the plan.
**Product ideas noted**
- AI follow-up questions for tasks during a test (not built).

## 23 Oct 2026: next phase, the website
- **Next: a homepage round on the v3 UI**, then the video storyboard, one feature page and the SEO template, then the build in aero-landing-page.
- **Rotating headline**, as HeyBooking did: the made-with part changes ("Publish your Claude artifact", "...your Figma prototype", "...your Lovable app", "...your HTML site"), so people see what they can bring. The rest of the line stays ("Watch people use it.").
- ~~Hero: one big real app window with a short calm loop (published, then a session arriving).~~ Replaced 23 Oct: **keep round 5 A's hero**, the whole app at an angle with someone's session being reviewed (true to the app: no cursor, no live typing). **Publish, Test, Review each show a large real app screen**; the timeline is not a headline feature. Never mention `claude mcp`: "one prompt to publish".
- **Node 20 upgrade** opened as its own PR now (deadline 30 Oct).

## 23 Oct 2026: answers on the questions page
- **Home:** layout A, what's new first with sites and tests beside it.
- **Sample project: personalised.** A silly one-page site made from the person's name and what we know, plus a finished test on it. Labelled Example, deletable.
- **Private is not password.** Password protection is its own feature. Private means people from outside (not signed in to the account) can't open the address.
- **Test link: short**, as today (today's form is the app address, the test name and `?test=1`).
- **Custom domain and favicon on tests:** paid plans only.
- **Keep a switch to stop taking new sessions** on a test.
- **After "Now test it",** the test opens on Setup.
- **Your own "Preview as tester" runs are free** and kept out of Insights; they show as "You".
- **Figma prototype link** offered under New site and under Tests.
- **Sessions newest first** (numbers never change).
- **Insights ranks by severity first** (Critical, Major, Minor), then how many testers.
- **Sessions open in Watch**, then remember each person's last choice.
- **Tasks can have an optional description.**
- **Tester screen light or dark is automatic**, from the prototype's background colour.
- **No timer for testers.** Keep a recording indicator ("just helpful to know it's being recorded"), in the new style; time is still recorded.
- **Recent tests (up to 5) listed under Tests** in the sidebar.

## 23 Oct 2026: after the app UI v2 board ("overall looks amazing")
- **Sidebar: improve today's**, don't replace it. "Aero." at the top with the collapse arrow; the account stays bottom left; no separate workspace name at the top.
- **A sample site and a sample test in every account by default** (open: personalised or fixed, see the questions page). It affects the first run; the first-run page still looks good.
- **Gradients must be nailed**: the three step washes match the marketing material (Publish, Test, Review), drawn to the standard of the OpenAI-style references from round 3; an uploaded site's own colour can tint its wash.
- **Site page:** no "Test it if you like" push (testing lives in the site's menu, e.g. "User test this site"). After publishing, go to the site's page in Aero, not the live site.
- **"Open as tester" becomes "Preview as tester".**
- **Tester task panel:** a square panel the tester can move out of the way, with a separate timer, and both "Done" and "Couldn't do it".
- **Sessions list needs filters**, also in the all-sessions view.
- **Session review:** looks good; tidy the transcript (cleaner, more even).
- **Insights timeline:** better UI, aligned with the session timeline.
- **Marketing:** the component versions suit feature pages; general marketing keeps the earlier real-UI pages he liked.
- **Questions page** for the open product questions, with pictures and inline answers.

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
