# UI directions stage: brief for every team (23 Oct 2026)

## Why this stage exists
Duane liked the round 5 mockups (A Studio, B Colour, C Story, D Replay) and the later "app UI round", but said a step was skipped: before tightening components, he wants to see **each main screen of the app drawn in each direction**, side by side, decide what works and what doesn't, and only then do detailed components. He also asked for the **marketing versions of components**: the real component, simplified and bigger, as it would appear on the website, in a video or on a feature card.

Your job: take ONE direction and draw the whole app in it, plus its marketing kit and its flow. You are a small studio acting as all the roles together: information architect, UX designer, UI designer, copywriter, brand designer, graphic designer, animator (motion notes only), and marketer (the marketing kit). Stay faithful to your direction's character; push it further where it was thin. The four teams must look clearly different from each other.

## Read first (do not skip)
- `/home/claude/figmaapp/docs/brand/DECISIONS.md` (what Duane decided and disliked)
- `/home/claude/figmaapp/docs/brand/TONE_OF_VOICE.md` (copy rules)
- `/home/claude/research/mockups/PRICING-FACTS.md` (the ONLY source for plans and limits)
- `/home/claude/research/mockups/CREATIVE-BRIEF.md` (round 5 brief; product facts and example data)
- Your direction's existing files: `/home/claude/research/mockups/<dir>/app.html`, `home.html`, `NOTES.md`, `src/`. Reuse its CSS, type, colours, logo and components. Screenshots of the existing app sections are in `/home/claude/research/explore/shots/<dir>-N.png`.
- The app UI round (latest whole-app proposal, useful for content, states and IA, not for look): `/home/claude/research/app-ui/screens.html`, `NOTES.md`, `/home/claude/research/app-review/REVIEW.md` (problems in today's live app).

## What the product really does (be true to it)
- Three steps: **Publish, Test, Review.**
- Publish three ways: paste a Figma prototype link; upload an HTML file or a zip (hosted at name.aeroapp.ai, with versions and rollback); or one prompt in Claude or ChatGPT, which publishes through the Aero connector. Free sites stay live 7 days.
- Test: a test gets a share link. Testers open it, allow screen and voice (they share a browser tab), and do optional tasks. No account for testers.
- Review: after a session ends, the recording is transcribed (about a minute later), then summarised: a summary, friction points quoted in the tester's words with a time, and top priorities. Across sessions, themes ("4 of 6 testers").
- Truth rules: never animate a transcript typing during a recording; word-by-word highlight while a *recorded* session plays back is fine. Tab recordings have **no mouse cursor**: never draw a moving cursor in a replay. Keep Claude's and Figma's interfaces visibly separate from Aero's. All names are made up and labelled "Example"; never "Duane". Studio name: Kestrel Studio. Example project: Pocket (a payments prototype), Tester B, 03:08 "I thought my cards would be on the home screen. Is it under More?" Other tests: Onboarding v2, Checkout.
- Copy: British spelling, sentence case, no em dashes, AI never the headline (name it only as "built with your AI tool" on the way in and "transcribed and summarised" on the way out).

## Do NOT use these (Duane: "looks like AI")
- White cards with a **coloured stripe down one side**.
- **Icons sitting in pastel rounded squares** (the generic feature-tile icon).
- Also avoid: sparkle/magic icons, purple-blue gradients, emoji, rows of three identical icon cards, glowing pills on everything, stock photos of people.
Find your direction's own way to signal type and status (type, a mark, a real thumbnail of the prototype, colour fields, numbers, rules).
- Buttons and the logo are NOT decided. Use your direction's existing button and logo, and keep them as they were; another team explores those separately.

## Deliverable: `/home/claude/research/explore/<dir>/pages.html`
A single self-contained HTML page (inline CSS; Google Fonts allowed; inline SVG; no external images except files you copy into `/home/claude/research/explore/<dir>/` and reference relatively). Each item is a `<section class="xp" id="...">` holding an `<h2>` title, one short line saying what idea it shows, and a frame 1360px wide drawn at desktop size (laptop window). No review nav bar. Sections, with these exact ids:

1. `p1` **Home / dashboard**: what's new, tests, sites. Include the first-run (empty) variant as a smaller second frame inside the same section.
2. `p2` **Sessions**: the list of sessions for one test (Pocket, 6 sessions: done, processing, one with no audio), how you move between them.
3. `p3` **Session review**: one session: recording (prototype in a phone or laptop frame, no cursor), transcript, summary, friction points with times, priorities. Show the playback highlight moment if your direction suits it.
4. `p4` **Publish from a prompt**: the connector flow (connect once, copy the prompt, waiting for the chat, published). Show Claude's side as a clearly separate small panel if you show it at all.
5. `p5` **Upload HTML or zip**: drop, uploading with progress, published with address and version, then "Now test it".
6. `p6` **Review across sessions**: themes for a test across 6 sessions, with quotes and counts, what to fix first.
7. `f1` **The flow**: your direction's flow "from prompt to first session" as a strip of 5 to 7 small step frames with one-line captions. Make it genuinely different from the other teams (e.g. one page vs stepper vs prompt-first vs player-first): state which in the subtitle.
8. `m1` **Marketing kit**: the marketing versions of 5 real components from your screens: session card, friction-point quote, published site card (address + version + Live), test link / share card, the transcript line with highlight (or the player). Each drawn at about 1.5x to 2x, with less detail (fewer rows, no tiny metadata), ready for a homepage, a video frame and a social card. Show for each: the app version small beside its marketing version, and one composed example (a homepage hero block or a 1200x630 card) built only from these.

Use consistent example data across all sections. Fill realistic content; no lorem ipsum.

## Also deliver
- `/home/claude/research/explore/<dir>/NOTES.md`: for each section, 2 to 4 bullets: the idea, what you think works, what you are unsure of. Plus a line on how the direction's components would become the shared design system.
- Screenshots: write your own script `/home/claude/research/explore/<dir>/shoot-<dir>.cjs` (Playwright: `require('/home/claude/e2e/node_modules/playwright')`, `chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' })`) that saves each section as `/home/claude/research/explore/<dir>/shots/<id>.png` at 1440 wide. Look at every screenshot yourself and fix what's broken (overflow, clipped text, overlapping, empty areas) before you finish.
- Use ONLY your own folder `/home/claude/research/explore/<dir>/` for files; never write into another team's folder or the mockups folders.

## Finish with
A short report: file paths, and the one thing in your direction you'd fight for and the one thing you'd drop.
