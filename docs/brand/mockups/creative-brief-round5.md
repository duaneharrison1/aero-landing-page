# Aero mockups: creative brief (round 5)

Owner: Duane (UX designer, runs Aero). Art direction, information architecture and core copy: me. You are one of four design teams. Work through the roles below in order; each is a pass, not a document.

## 1. The product, as it really is (do not invent features)
Aero puts a prototype online and shows you real people using it, from the same link.
- **Publish, however you made it:** paste a Figma prototype link; drop an HTML file or zip; or ask Claude or ChatGPT in one prompt and it publishes to Aero for you (MCP). Live at name.aeroapp.ai in seconds to a minute. Versions and rollback.
- **Share one link:** testers open it on their own device, no account needed. Optional tasks ("Find your cards").
- **Real people, recorded:** screen and voice (think-aloud). NOT webcam: never show a tester's face as if recorded. Photos of people are fine as "who tests" and atmosphere.
- **Automatic transcripts:** about a minute after each session. The transcript is time-coded and follows the recording.
- **Insights from real sessions:** per session, a short summary, top priorities and friction points quoted in the tester's own words; across sessions, recurring themes. AI does this, but AI is never the headline. Say "transcribed and summarised", "friction points", "in their own words".
- **Price:** free to start (recordings included), paid from $3 a month, monthly, no call, no contract. Free sites stay live 7 days.
- **Who:** UI and product designers, UX researchers, PMs and founders testing AI builds, students, people who made something and can't host it. "Bring your own testers": a client, a friend, a classmate.
- **Limits to respect:** tests of HTML sites are desktop only today; Figma tests on a phone record voice only. Don't claim panels, recruiting, seats, SOC 2.

## 2. What the homepage must sell (information architecture)
One page, in roughly this order. Each direction can merge, reorder or stage these differently, but all must be covered:
1. **Hero:** the loop in one line. Publish your prototype. Watch people use it. (Same link.) Plus a sub line and two actions (Start free / See a test). Show the product, not an illustration.
2. **Way in:** three ways to publish (Figma link, HTML or zip, one prompt to Claude/ChatGPT). "Straight from a prompt" must be visible.
3. **Share and test:** one link, any device, tasks, real people (photos).
4. **Watch:** a session: prototype + recording + transcript writing itself.
5. **Read:** insights from real sessions: friction points quoted in their own words, priorities, themes across sessions. Make "it saves you time" concrete: no note-taking, transcript in a minute, the three things to fix.
6. **Fast and simple:** a short "from prompt to first session" timeline. Use honest, labelled example times.
7. **Price:** free to start, from $3. A three-plan teaser (Free, from $3, Pro $19) and "no call, no contract".
8. **Who it's for:** designers, researchers, PMs and founders, students (with photos).
9. **FAQ** (4 to 6 real questions) and **footer**.

## 3. Core copy (copywriter): adapt the voice per direction, keep the facts
- Headline options: "Publish your prototype. Watch people use it." / "Your prototype, live. Real people, recorded." / "From prompt to real people in minutes."
- Sub: "Put a Figma prototype or HTML build online, share one link, and watch real people use it. Screen and voice, transcribed for you."
- Proofs: "Live in minutes, however you made it." / "Watch, then read." / "Priced for one designer."
- Time saver: "No notes to take. The transcript is ready about a minute after they finish, with the friction points in their own words."
- Prompt moment: You type "Put this prototype online with Aero and set up a test." Aero: "It's live. Your test link is ready to share."
- Example session data (label as example): Pocket, a payments app. Tester B, 07:12. Quote: "I thought my cards would be on the home screen. Is it under More?" Friction point: "Cards are hidden under More" at 03:08. Others: "Send flow has no back label" 02:41, "Balance looks tappable" 03:02.
- Rules: plain words, British spelling, sentence case, no em or en dashes, no exclamation marks, no "AI-powered", "seamless", "leverage", "revolutionary". No fake testimonials, logos or user counts. Any number not true today is labelled "Example".

## 4. Brand constants (all directions)
- Logo: "Aero." with a blue full stop (#3478F6). Each direction has its own sans version; outlined SVGs in `/home/claude/research/brand/fullstop-<font>/`: lockup.svg, lockup-reversed.svg, mark.svg ("A."), mark-reversed.svg, app-icon.svg, app-icon-light.svg, favicon.svg. Inline the SVG.
- The blue dot is the one constant. The headline's final full stop can be blue.
- Buttons: liquid glass is Aero's signature, but quiet. Inline `/home/claude/research/glass-lab/glass-v4.js` (attribute `data-glass-v4="primary|secondary|dark"`, `data-fill="#hex"`) on the main buttons only.
- Photos: `/home/claude/research/mockups/images/` (see PHOTOS.md). Reference them as `images/pNN.jpg` (a copy sits in your folder).

## 5. Duane's likes and dislikes (hard rules)
Likes: the Full stop logo and blue dot; the sans font (Geist); the "pocket.aeroapp.ai" browser window with prototype and session notes; the dark app window at an angle (and a light version); the soft colour-wash cards; a little Figma-like colour and designer feel; real people; liquid glass.
Dislikes: headlines that are too bold or too big; forced decoration (fake sticky notes, cursor name tags for the sake of it); overly elegant fonts; dark websites; space, flight or train imagery; Nothing-style dot matrix; every option looking the same; wireframe looks; heavy glass panels.
He wants: "a design tool, professional but accessible, a bit of colour, a bit of AI insight from real sessions". The first page has to sell it all.

## 6. The four directions (art director)

### A. Studio (`studio/`), safe and polished. Refs: Linear, Cursor, Vercel, Claude's calm
- Logo: `fullstop-geist500`. Type: Geist 400 to 500 for headlines (light, large but not shouting, tracking -0.03em), Geist Mono for small labels.
- Colour: white, ink #1D1D1F, greys; colour only in soft washes (peach, sky, mint) behind product shots and in the blue dot.
- Layout: left-aligned hero; the product is the hero: the Aero app window at a slight angle (light), with a session playing (prototype, transcript writing itself, friction point appearing). Sections are calm two-column rows of copy and real UI. People appear as a quiet "who tests" photo strip.
- App: light, Linear-like sidebar, dense but airy.
- Motion: the hero window: the cursor moves, the transcript types, the friction point fades in; smooth and restrained.

### B. Colour (`colour/`), the design-tool one. Refs: Figma, Framer, Pitch, Arc
- Logo: `fullstop-funneldisplay500`. Type: Funnel Display for headlines (500, not heavier), Figtree or Geist for text.
- Colour: big flat colour blocks per step: Publish = sunflower #FFC21A, Test = pink #FF8FCF, Watch = cobalt #3355FF (white text), Read = mint #9BE3C3, on white. Ink #16151A.
- Layout: modular, playful grid. Photos of people cropped into rounded colour frames. The pocket window sits on colour. Designer details where they explain something (a selection outline around the friction point, layer names on frames), never as stickers.
- App: white UI with colour-coded test cards and tags; feels like a design tool.
- Motion: tiles slide in by colour; the three ways in morph into one live link.

### C. Story (`story/`), unorthodox: editorial. Refs: Stripe Press, Claude, The Browser Company stories, magazines
- Logo: `fullstop-schibsted500`. Type: Schibsted Grotesk for headlines (400 to 500), a readable text face (Schibsted or Geist), generous measure.
- Colour: warm white #FBFAF7, ink, one highlighter colour (soft yellow #FFE58A) for quotes, and the blue dot.
- Layout: the page reads like a feature story of one test. Big photography (a tester at home, p09 or p17), her quotes set large and highlighted word by word as if the audio is playing; the friction points and insights as margin notes beside the transcript; the product shown as calm figures with captions ("Fig. 2: the session view"). Still covers every IA section, as chapters.
- App: a session view that reads like an article (transcript first, video docked), plus dashboard.
- Motion: the highlighter sweeping through a quote in sync with a waveform.

### D. Replay (`replay/`), unorthodox: the page is a session. Refs: Apple product scroll pages, Linear's app shots, Arc
- Logo: `fullstop-intertight600`. Type: Inter Tight 500 headlines, Inter text, Geist Mono timecodes.
- Colour: light page; the stage is the angled dark app window (#101114), with a light-mode toggle showing the same window light. Accent blue; red only for REC.
- Layout: a sticky stage. As you scroll, the session scrubs forward: publish (prompt goes live), share (link copied), tester starts (photo of tester), cursor moves, transcript scrolls, friction points pop in, insights summary arrives. Copy blocks on the side change per step. Ends with price and FAQ as a normal page.
- App: player-first session view (dark and light), with a timeline of friction markers.
- Motion: the scroll story itself, plus a 12s hero loop.

## 7. Deliverables (each team, in its folder)
1. `home.html`: the full homepage, desktop and mobile (it must work at 390px with no sideways scroll).
2. `app.html`: three app screens stacked with labels: dashboard (tests and sites), session view (recording, transcript, friction points, insights), create flow (three ways in, prompt option).
3. `content.html`: the SEO page "Test your Claude artifact with real people" (/test/ai-prototype): what to do, the three steps, the honest note that claude.ai can't be framed so you publish to Aero first, FAQ.
4. `motion.html`: the hero animation alone at 1280x720, a 10 to 14 second loop. Also export `motion.mp4` (H.264): record with Playwright (`recordVideo`, Chromium at `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`, playwright at `/home/claude/e2e/node_modules/playwright`), convert with `ffmpeg -c:v libx264 -pix_fmt yuv420p -crf 20`.
5. `shots/`: desktop (1440) and mobile (390) full-page screenshots of home, app, content.
6. `NOTES.md`: the idea in 3 lines, what each role pass changed, and known weaknesses.

Technical: each HTML file self-contained (inline CSS and JS; Google Fonts link allowed; images via `images/pNN.jpg`). Light theme only is fine, but set explicit colours. No external JS except what you inline. Keep each page under 3MB plus images.

## 8. Roles, in order (one pass each, then loop back)
1. Information architect: lay out the sections for your direction; make sure every IA item in section 2 is covered.
2. Copywriter: write every word from section 3, in your direction's voice.
3. UI designer: build the real product UI pieces (app window, session view, transcript, friction cards) properly; they are the heroes.
4. Graphic designer: type scale, colour, photo crops and composition; make it distinctive.
5. Animator: hero motion and scroll or reveal motion (respect reduced motion), then motion.html and the MP4.
6. UX designer: check the page answers "what is it, how does it work, why trust it, what does it cost, what do I do now" in the first two screens; check mobile.
7. Brand expert: check against sections 4 and 5. Then look at your screenshots like a critical art director and fix the three weakest things. Do at least two full screenshot-and-fix loops.
