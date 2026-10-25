---
brand-sync: figmaApp docs/brand is the source. Copy this file unchanged to aero-landing-page/docs/brand/.
version: 2026-10-25.1
---

# Review R8: homepage, Features page and every UI illustration

Independent review, 25 Oct 2026. Pages opened and run in Playwright (Chromium) at 1512x789 and 390x844. The hero was stepped every 1 s through its full loop (50.3 s of real time) at both sizes, plus extra frames at key beats; each section loop was shot every 0.75 s over its 9 s cycle. Evidence is in `review-r8/`.

**How times are given.** "Real" times are the visitor's clock, 0 to 50.3 s (what `window.__heroAt()` takes). `home.js` works in script time; real = script up to 1.4 s, script 1.4 to 7.3 s is stretched over real 1.4 to 10.1 s, and after that real = script + 2.7 s.

Hero beats in real time: Claude 0 to 10.0 (paste visible 1.6 to 4.5, published 7.5) · Aero prompt page 10.0 to 11.2 · site page 11.2 to 13.45 · Visit, new tab 13.45 to 15.9 · back, ⋯ menu 17.1 to 18.85 · test setup 18.8 to 22.35 · owner's WhatsApp 22.35 to 26.1 (send 24.8) · Maya 26.2 to 39.0 (WhatsApp 26.2 to 29.2, welcome 29.2 to 31.3, permissions 31.3 to 32.5, task 1 32.5 to 35.2, task 2 35.2 to 38.8) · session replay 39.3 to 43.3 · Insights 43.3 to 47.4 · Sites, New site, copy prompt 47.4 to 49.95 · back to Claude.

**Counts:** P1 6 · P2 18 · P3 13.

---

## P1: broken, wrong or untrue

### P1-1 Test section loop is broken (both sizes)
- **Where:** homepage, Test section ("One link. They open it, and that's it."), the whole 9 s loop.
- **What's wrong:** the WhatsApp-style message is unstyled body text lying across the test link card, and the tester window never appears, so 70% of the box is an empty green wash. Two causes in `home.css`:
  - `.st-bub` has no styles anywhere (the class was dropped when the hero moved to WhatsApp).
  - Line 216 is `.v-bub .v-tw{...}`, but `.v-tw` is a sibling of `.v-bub`, not inside it, so the tester window gets no position or width and collapses.
- **Fix:**
  - Change line 216 to `.v-tst .v-tw{left:7%;right:7%;bottom:7%;height:auto;aspect-ratio:1440/760;background:none}`.
  - Style the bubble as WhatsApp's outgoing bubble (another company's UI, fixed colours): `.v-bub .st-bub{background:#D9FDD3;color:#111B21;border-radius:8px;padding:7px 10px 8px;font-size:14px;line-height:1.35;box-shadow:0 1px .5px rgba(11,20,26,.13)}`, with the link on its own line in `#027EB5`. Better still, reuse the hero's `.wa-new` bubble markup so they stay in step.
  - Re-shoot with `shoot.cjs loops` and look at the frames, not only the height check (the height check passed while the loop was broken).
- **Screenshots:** `review-r8/_loops-d-1.png`, `review-r8/_loops-m-1.png`, `review-r8/loop-d-1-05.png`.

### P1-2 The homepage sells features that aren't built, and contradicts the Features page
- **Where:** homepage, Test and Review sections; hero scenes; compared with the Features page's own "Coming soon" tags and `figmaapp/docs/TODO.md` (all unticked).
- **What's wrong:**
  - Test body: "Your own 'Preview as tester' runs are free and stay out of your results." Test facts: "Preview as tester / Free, kept out of results". Features says Coming soon, and TODO lists it as decided, not built.
  - Review body: "Play any line and the words light up as they're said." Features says "Words light up as it plays. Click a line to jump to that moment. Coming soon". TODO lists word highlight and click-to-jump as not built.
  - The hero shows as current: the optional first name on the tester welcome (29.2 to 31.3), the Private toggle on the site page (11.2 to 18.85), "Taking new sessions" plus the test's own domain and favicon on Setup (18.8 to 22.35), word highlight and "click a line to jump" in the replay (39.3 to 43.3), and dark mode (TODO: not built). All of these are Coming soon on Features or unticked in TODO.
- **Fix:**
  - Copy, now. Test body: cut the "Preview as tester" sentence and end on "No app to install, no account to make, no session to book." Test facts: replace "Preview as tester" with "Works on any prototype / Claude, HTML or a Figma link". Review body: "About a minute after each session, it's transcribed and summarised. Insights puts every session together: what to fix first, how many testers hit it, and the quotes."
  - Hero: the hero shows the v3 UI by decision, so add a launch gate. Either these items ship before the site goes live, or the hero drops them: the name field becomes plain text "Anonymous tester", no Private row, no "Taking new sessions" row, no word highlight. Put the list in `docs/TODO.md` under "Before the website launches".
  - Keep the Features page as the single list of what's built. Any homepage line about a feature must match its tag there.
- **Screenshots:** `review-r8/hero-d-30.png` (name field), `review-r8/hero-d-18.png` (Private), `review-r8/heroS-d-41.0.png` (word highlight), `review-r8/_home-d-full-1.png` (Test and Review copy), `review-r8/_features-d-full-1.png` and `review-r8/_features-d-full-2.png` (Coming soon tags).

### P1-3 Phone sessions on a site test (Features page)
- **Where:** Features, Review: the "Every session in a list" box (Ines, "Phone · Safari") and the "Recording and transcript" box (the replay of Pocket is a phone layout, while the session header reads "Laptop, Chrome").
- **What's wrong:** Pocket is a site (a copy of pocket.aeroapp.ai). Site and HTML tests need a computer; only Figma tests work on phones, voice only. Footnote 4 and the FAQ on the homepage say so, and TODO records that phones are blocked today. The text extraction also lists "Phone · Chrome" sessions for the same test.
- **Fix:** make every Pocket session a laptop (Laptop · Safari, Laptop · Edge and so on), and draw the replay at desktop width to match its "Laptop, Chrome" header. To show phones, use the Figma test (Onboarding v2) with a "Voice only" tag on those rows.
- **Screenshots:** `review-r8/_features-d-full-2.png` (top-left and middle-left boxes).

### P1-4 At 1512x789 the hero's key actions happen off screen
- **Where:** homepage hero, desktop.
- **What's wrong:**
  - The stage is 1200x849 and starts at y=356, so only 433 px (51%) is above the fold. The Claude input, where the paste happens (the bit Duane calls "the best bit"), sits at about y=1060. WhatsApp's message field (paste and send, 23.9 to 24.8) is also near the bottom of the window.
  - The loop starts at 15% visibility, so a visitor reading the headline misses the paste and send (1.6 to 4.5) before scrolling.
  - No scroll position shows the whole window and the Publish, Test, Review steps together: stage plus steps is 932 px against 725 px of visible area. Scrolling far enough to see the window's bottom puts its tabs, the "Maya's computer" label and the voice quotes under the sticky nav.
- **Fix:**
  - Cap the stage by height: `.hm-stage{width:min(1200px,calc((100svh - 184px) * 1.413))}` and centre it (the 1.413 is the stage's 1200/849 ratio). At 789 px tall that gives about 855x605, and one scroll shows window and steps together.
  - Start the loop (or restart at 0 on first entry) only when the stage is 60% in view: IntersectionObserver `threshold:[.15,.6]`, and kick at `.6`.
  - Optionally raise Claude's input by making the Claude scene a shorter conversation pane (the window has about 400 px of empty chat above the input).
- **Screenshots:** `review-r8/home-d-fold.png`, `review-r8/_home-d-full-0.png`, `review-r8/heroS-d-23.5.png` (WhatsApp field cut off).

### P1-5 The handover still doesn't read as "someone else, on another computer"
- **Where:** hero, 26.0 to 27.0 (owner's WhatsApp to Maya's WhatsApp), both sizes.
- **What's wrong:**
  - Maya's window dissolves in at the same place and the same angle (`MTILT` is defined but unused), showing the same app with the same layout. A newcomer sees "the WhatsApp screen changed".
  - The only cues are darker browser chrome and the "Maya's computer" pill. The pill sits on the stage's top edge (y=356), where at the natural scroll it is under the glass nav. On phones the camera never frames it.
  - Script times make the pill fade in at 26.2, while the owner's window is still half visible (it only fades out by 26.45), so for about 0.3 s the pill labels the owner's screen.
  - This is the third round with this problem (24 Oct: "It isn't clear that Maya is on a different computer"; 25 Oct: tilt and pan "looks tacky").
- **Fix (director's cut, no tilt or pan):**
  - Match cut on the message: hold the owner's sent bubble ("Could you try this for me?") for 0.4 s, dissolve, and land on Maya's chat list with the same text as the incoming preview in the same screen position. The eye follows the message across the cut.
  - Make her machine look different at a glance: WhatsApp's own dark theme (it has one) on top of the dark Chrome, and a different window proportion (for example 1280 wide, inset 4% on each side) so the frame edge visibly changes.
  - Move the pill inside the window: over the tab strip, top-left, at z above the frame. Fade it in from 26.55 (when Maya's window starts) to 38.8. Add `cam:mlabel` to the phone camera path at 26.4 so it's framed on phones.
- **Screenshots:** `review-r8/heroS-d-26.3.png` (label over the owner's screen), `review-r8/hero-d-26.png` then `review-r8/hero-d-27.png` (the two WhatsApps), `review-r8/m-hero-strip-2.png` (phone, no cue).

### P1-6 The hero's story contradicts itself (state, numbers, dates)
- **Where:** hero, several scenes; Features Review box.
- **What's wrong:**
  - **A test that doesn't exist yet:** at 10.0 to 11.2 (prompt page, just published) the sidebar already lists "Pocket · 2 new" under Tests. The test is only created at 18.8. The prompt page is shared with the end of the loop, so it carries the end state. `review-r8/heroS-d-10.5.png`
  - **Plan counter over the limit:** "Pro plan 15 of 20" never moves, but Pocket gains 6 sessions. That would be 21 of 20, more than Pro has (PRICING-FACTS: 20). `review-r8/heroS-d-47.5.png`
  - **Six sessions from one message:** the link goes to Maya alone, then Insights shows 6 testers with no passage of time.
  - **Clock and calendar:**
    - Published "10:41".
    - WhatsApp "20:56" to "21:04" ("tonight").
    - Maya's session "Mon 20 Oct, 18:04", three hours before the link was sent.
    - 20 Oct 2026 is a Tuesday. The Features list also has "Wed 22 Oct" and "Thu 23 Oct", which in 2026 are a Thursday and a Friday.
    - `review-r8/heroS-d-41.0.png`
  - **Maya is session "2 of 6"** (URL `/sessions/2`, pager "Tom · 2 of 6 · Priya") although she is the newest and sessions are newest first with numbers that never change. She should be session 6, shown first.
  - **Sidebar drift:** Sites shows 5 in light scenes and 4 in Insights. The test list is "Onboarding v2, Checkout, Very serious port… (Example), Sign-up flow" in setup but "Onboarding v2, Checkout, Pricing page, Juniper (Sample)" in Insights. Pocket shows "1 new" in Insights and "2 new" in Sites. "Example" and "Sample" are both used.
- **Fix:** put one state table in `build.py`, keyed by scene, and render every sidebar from it:
  - Before the test: Sites 5, Tests 4, no Pocket test, plan 9 of 20.
  - After the test: Tests 5 with "Pocket · 1 new", plan 15 of 20.
  - Owner sends the link to a WhatsApp group "Pocket testers" (6 people), or the WhatsApp chat shows "Forwarded to 5 chats" under the bubble, so 6 sessions make sense.
  - Times: Published 20:41, WhatsApp 20:56 to 21:04, Maya's session "Tue 20 Oct, 21:09", Insights "updated 22:30". Maya is session 6.
  - Use "Example" only.
  - Fix the Features weekdays the same way.

---

## P2: clarity and craft

### P2-1 Maya's voice is shown as a caption far from the action, and reads like live transcription
- **Where:** hero, task 1 (33.1 to 35.8) and task 2 (36.2 to 38.8), both sizes.
- **What's wrong:**
  - The quotes ("Okay, send twenty pounds to Sam…") are 19 px text with a mic icon, pinned to the top-right edge of the stage outside the window. That's about 700 px from the task panel and the Send card where the eye is.
  - At the natural scroll they sit under the nav, and on phones the camera never frames them.
  - A mic icon next to words, during a recording, reads as a live transcript. The truth rule says transcripts come after.
- **Fix:**
  - Show voice the way the real tester UI does: a small live level meter (5 bars) inside the Recording chip, moving only while she speaks.
  - Optional: put the line she says in a speech bubble from a "Maya" avatar just outside the window's right edge, level with the task panel, in quotation marks. Use a voice style (no mic icon, not mono, no transcript chrome), so it reads as what you'd hear, not what Aero writes.
  - Frame it on phones (`cam:say`).
- **Screenshots:** `review-r8/heroS-d-35.0.png`, `review-r8/hero-d-34.png`.

### P2-2 Review gets the least time, yet it's the payoff
- **Where:** hero, replay 39.3 to 43.3 (4.0 s) and Insights 43.3 to 47.4 (4.1 s).
- **What's wrong:** Review is 16% of the loop. The Insights summary is 48 words and gets about 4 s, with the issue cards still rising in at 43.4 to 44.4. The owner's WhatsApp (3.75 s) and Maya's chat list (3 s before she opens the link) get as long.
- **Fix:**
  - Cut 1.2 s from the owner's WhatsApp (open the chat already focused) and 1.0 s from Maya's list (badge, then open).
  - Give Insights at least 6.5 s: summary alone for 2.5 s, then issue 1 rises and its first quote card plays (word highlight runs), then hold.
  - Move JT and JUMP to match.

### P2-3 Loop seam: the conversation pops back, and "next version" isn't one
- **Where:** hero, 49.95 to 50.3 into 0.0.
- **What's wrong:**
  - Claude fades in showing the finished publish conversation, then one frame later it's the original two-message chat (`conv` flips 1 to 0 at script 47.25).
  - The ending says "copy the prompt again for the next version", but the loop republishes "Version 1".
- **Fix:** either fade `.cl-sent`, `.cl-reply` and `.cl-done` out over 0.3 s before Claude's crossfade completes, or keep the history and make the opening beat a second publish ("Done. Version 2 is live at pocket.aeroapp.ai"). With the second option, the prompt page's Published card says "Version 2".
- **Screenshot:** `review-r8/_seam.png` (top-left 49.9, top-right 50.1).

### P2-4 Phone hero is too small to read and crops the action
- **Where:** hero at 390x844, whole loop.
- **What's wrong:**
  - World scale is VW/720, so app body text is about 5 to 6 px.
  - The camera crops the Send £20 button and the right of the menu.
  - The Maya pill and the voice never appear (see P1-5 and P2-1).
  - A grey band shows under the window on some beats.
- **Fix:**
  - Use VW/520 on beats with reading (prompt, Published, menu, welcome, transcript, Insights summary) and VW/720 only for scene-wide moves.
  - Retarget `CAM` so each key control sits in the middle third.
  - Clamp `ty` so the window's bottom edge never shows the stage background.
- **Screenshots:** `review-r8/m-hero-strip-1.png`, `review-r8/m-hero-strip-2.png`.

### P2-5 Performance: hitches at scene cuts, jank on phones
- **Where:** hero playback.
- **What's wrong:** measured over 12 s:
  - Desktop: long tasks of 448 ms and 342 ms (visible hitches), frame p95 33 ms.
  - 390 px: 15 long tasks (50 to 176 ms) and frame p95 100 ms.
  - The stage holds 3,263 of the page's 4,869 elements, all laid out and painted at opacity 0.
  - Likely causes, worth profiling to confirm: `GlassV3.refresh()` on every scene change, the engine's idle re-read of "buttons that moved" (on phones the camera moves every button every frame), and per-frame DOM writes (`S.url.textContent`, classes on transcript words, tab classes) even when nothing changed.
- **Fix:**
  - Mark the stage's glass as static (render once per scene, never re-read on camera moves).
  - Write to the DOM only on change.
  - Set `display:none` on scenes more than one step away from the current one.
  - Add `will-change:transform` on `.st-world`.
  - Re-measure with the same script: `review-r8` method, PerformanceObserver longtask.

### P2-6 Review loop: the words don't light up "as they're said"
- **Where:** homepage, Review section loop.
- **What's wrong:** all 14 words share one animation with no delay, so they flash together. The waveform and playhead don't move. The copy beside it promises the opposite.
- **Fix:**
  - In `build.py`, give each `.w` `style="--i:N"` and `animation-delay:calc(var(--i) * .16s)`, with the highlight window 1.5% wide.
  - Fill the waveform bars left to right in step with the words.
  - Once P1-2 lands, the copy should match whatever is built.
- **Screenshot:** `review-r8/_loops-d-2.png`.

### P2-7 Publish loop doesn't match how Claude and Aero behave
- **Where:** homepage, Publish section loop (both sizes).
- **What's wrong:**
  - The prompt stays in Claude's input box while "Used the Aero API · publish" appears below the input. In Claude, the message is sent (it moves into the conversation, the input clears) and tool use shows above the input.
  - From 52% of the loop the Published card covers half the tool chip ("…API · publish").
  - Aero's page still says "Waiting for your chat" when the site is live.
  - On phones the Aero prompt page is hidden, so the prompt has no visible source.
- **Fix:**
  - Sequence it: Copy prompt press, then a sent bubble in Claude, then the tool step, then "Done. It's live…".
  - Move `.v-done` to `left:5%;bottom:4%;width:52%` and `.v-cl` to `top:30%`, so they don't touch.
  - Swap "Waiting for your chat" for the Published row at 52% (same as the hero).
  - On phones, show a 2-line crop of the prompt page with "Copy prompt" above the Claude card.
- **Screenshots:** `review-r8/_loops-d-0.png`, `review-r8/_loops-m-0.png`.

### P2-8 Claude's tool chip looks like a connector
- **Where:** hero 7.5 to 10.0 and the Publish loop: "✓ Used the Aero API · publish".
- **What's wrong:** "Aero API · publish" is how Claude labels a connector tool. DECISIONS (23 Oct) is explicit that the prompt flow is a prompt, not a connector. Claude's UI should look like Claude's and stay visibly separate from Aero's.
- **Fix:** run the real prompt once in Claude, capture what Claude shows while it sends the files (for example a code or command step), and copy that label and styling exactly, simplified. Keep the green highlight on it.

### P2-9 No visible pause for a 50 s autoplay
- **Where:** hero.
- **What's wrong:** the only pause is Space or Enter on the focused stage (a `role="img"`). Mouse and touch users can't pause, which fails WCAG 2.2.2. The pause button was removed for good reason (it clashed with the tester screen). The stage's aria-label also says "a 48-second loop"; it is 50.3 s.
- **Fix, without a button on the stage:**
  - Clicking the step that's already playing toggles pause. Show a 10 px pause or play glyph at the right end of that step's progress bar on hover or focus, and set `aria-pressed`.
  - Add one visually hidden live region that says "Paused" or "Playing".
  - Correct the aria-label to 50 seconds.

### P2-10 The rotator makes the subhead jump, and screen readers hear all four
- **Where:** hero subhead, every 2.6 s.
- **What's wrong:**
  - The centred paragraph re-wraps as the word width changes ("Claude artifact" to "Lovable app"), so both lines shift sideways and the line break moves on phones.
  - Screen readers read "Publish your Claude artifact Figma prototype Lovable app HTML site".
  - The publish blue makes it look like a link, and it isn't one.
- **Fix:**
  - Give `.hm-rot` a fixed width equal to the widest phrase ("Figma prototype") and centre the word inside it, or put the rotating phrase on its own line.
  - `aria-hidden="true"` on the rotator, plus a visually hidden "Publish your Claude artifact, Figma prototype, Lovable app or HTML site."
  - Use ink with a 2 px blue underline, or ink alone.

### P2-11 Glass: muddy white glass in dark mode, no caustic on white
- **Where:**
  - Hero Insights 43.3 to 47.4: "Preview as tester" and "Copy as table" (white glass on dark).
  - Hero CTAs, "Log in", Setup's "Preview as tester" (white glass on white).
- **What's wrong:**
  - On dark, the white glass becomes a mid-grey slab with dark text (about 2:1), so it looks disabled next to the bright "Copy test link".
  - On white, there is no colour within reach, so the caustic is invisible and the buttons read as plain bordered white. The 25 Oct note ("white buttons such as Preview as tester don't look caustic") is still open.
- **Fix:**
  - In dark themes, `data-glass-v3="secondary"` gets fill `rgba(255,255,255,.08)`, text `#E8EAED` and a 1 px `rgba(255,255,255,.14)` hairline.
  - For the caustic, add a settings key (for example `causFloor:.25`) that tints the caustic with `--aero-accent` when the nearby colour is below `paleLo`, so white buttons on white still catch a faint blue.
  - Decide it in the glass panel, not by hand.
- **Screenshot:** `review-r8/_glass-sheet.png` (rows: rest, ink hover, white hover, setup pair, dark pair, nav).

### P2-12 "Screen" when Aero records the tab
- **Where:**
  - Homepage Test facts: "Screen and voice".
  - Test link chips: "Their screen" (hero setup, Test loop, Features).
  - Session header: "Screen and voice".
  - Features intro: "Every plan records screen and voice".
- **What's wrong:** Aero records one browser tab. "Screen" suggests the whole screen, which is less private than the truth and conflicts with the tester welcome ("This tab and your voice are recorded").
- **Fix:** "Tab and voice" (facts and session header), "Their tab" (chip), "Every plan records the tab and the voice, and transcribes and summarises each session."

### P2-13 "One link and it's tested." overclaims
- **Where:** hero H1 line 2; Features Test intro.
- **What's wrong:** a link doesn't test anything. People do, and they may never open it. It's also the one line on the page that isn't concrete.
- **Fix:** "One prompt and it's live. One link and they're trying it." For Features: "Send one link. Testers open it on their own computer: no software to install, no account, nothing for you to set up first."

### P2-14 Plan claims that aren't in PRICING-FACTS
- **Where:** homepage price table ("Billing: No card needed"; "Transcript and summary ✓" for Free); Review facts ("Transcript and summary / On every plan"); FAQ and Features ("3 test sessions with recordings, transcripts and summaries").
- **What's wrong:** PRICING-FACTS says only "Free, $0: recordings included, 3 test sessions, sites stay live 7 days". "No card needed" and transcripts on Free aren't there.
- **Fix:** confirm both with Duane and add them to PRICING-FACTS (bump its version and sync it to aero-landing-page), or remove them: Billing for Free becomes "Free plan", and "On every plan" becomes "About a minute after".

### P2-15 Two different Pocket stories
- **Where:** homepage (month tabs: "Last month is hard to find", Pocket v1, 0 to 6 visits) and Features Review boxes ("Is it under More?", "Cards are hidden under More", Maya took over 3 minutes, Pocket v4, 38 visits).
- **What's wrong:** the same people (Maya, Tom, Jonas, Ana, Leo, Priya) and the same app give different findings on the two pages. It reads as made-up data.
- **Fix:** one Pocket dataset in a shared JSON used by both `build.py` files: one set of findings, one version history, one visit count.

### P2-16 WhatsApp details
- **Where:** hero, owner's and Maya's WhatsApp.
- **What's wrong:**
  - The tab favicon is a plain green dot (25 Oct: "WhatsApp tab is missing its favicon").
  - The owner's message turns to blue read ticks at 25.4, three seconds before Maya opens the chat at 28.4.
- **Fix:**
  - A simplified 14 px WhatsApp glyph (green speech bubble with white handset) as the tab icon. It is another company's mark, so keep it plain.
  - Keep the ticks grey until 28.4. Blue ticks can show when the camera is back on the owner, which it isn't, so simply never turn them blue.

### P2-17 Features that need checking before they're listed
- **Where:** Features: "Ask testers to rate how hard each task was", "A task can tick itself off when the tester reaches the right page", "Set up a test from the same prompt you published with", "Download the transcript and video, or share them with your team", "Search and filter by status", "Duplicate or rename a site".
- **What's wrong:** none of these is in TODO either way, and I couldn't confirm them as built. If any isn't built, it's the same problem as P1-2.
- **Fix:** check each against the app. Tag anything not live "Coming soon", and say which in `docs/brand/DECISIONS.md`.

### P2-18 Low-contrast labels
- **Where:** homepage use-case cards' role labels ("Student", "Founder"…), 11 px mono `#8E8E94` on `#FAFAFB`, 3.1:1. The Features "Coming soon" tags use the same grey.
- **Fix:** use `--mut` (`#6E6E73`, 5.07:1 on white), as the rest of the page does.

---

## P3: polish

1. **Review tool overlay:** the "Headline 1 2 3" switch sits over the hero window at both sizes. Fine for review; remove it, or hide it unless `?review`, before shipping. (`review-r8/home-d-fold.png`)
2. **Pocket's list rows:** amounts sit about half a row below their names in the Claude preview, the live site and the tester view ("Corner Coffee" vs "−£4.20"). Fix `.pk-list > div` to `align-items:baseline`. (`review-r8/hero-d-15.png`)
3. **Claude's artifact preview:** the bottom 45% of the orange panel is empty. Add the "Recent" header and two more rows, or crop the preview panel height. (`review-r8/hero-d-03.png`)
4. **The cursor parks on what it's showing:** over the pasted prompt (1.6 to 4.5) and over the "User test this site" description (17.9 to 18.85). Offset `inp` to `fx .9` and `mi` to `fy .25`.
5. **"User test this site" hover** lasts 0.75 s before the click. 24 Oct asked to "show that click clearly": hold it 1.2 s.
6. **Upgrade chips for a Pro owner:** a Pro owner still sees "Solo and up" and "Basic and up" chips. Hide them when the plan already includes the feature.
7. **"Laptop · Chrome 129 · macOS":** drop the version number (it will look dated).
8. **Prompt page stepper:** step 3 ("Live at an address") isn't ticked when the Published card shows (10.0 to 11.2).
9. **Tester task panel:** about 90 px of empty space between the task text and the progress bar. Size it to content. (`review-r8/heroS-d-35.0.png`)
10. **"Allow the microphone and this one tab"** (Test body): say "the microphone and the tab with your prototype".
11. **Names reused in different roles:** Priya (owner's friend, tester, product designer), Tom (Kestrel colleague, tester, founder), Sam (Pocket contact, maker), Leo (friend, tester). Give each context its own names.
12. **Homepage step sections:** these don't link to the Features page. Add "Every Publish feature" (and Test, Review) under each facts list, pointing to `features.html#publish` and the others. It's good for scanning and for SEO.
13. **Price table on phones:** it scrolls sideways with no cue. Add a right-edge fade and "Swipe for the others" under it.

---

## What's working (keep)
- The Publish arc (paste, send, switch tab, it's there, Visit opens a new tab and the page loads) is clear and paced well at desktop size.
- No cursor ever appears on Maya's screen or in the replay, and transcript words only light up during the recorded replay, never live. The welcome card states tab and voice, not camera.
- The tester welcome and permissions copy is the best writing on the page: plain, true, calm.
- Step buttons are real buttons with a visible focus ring, and they work as a manual stepper under reduced motion.
- No em dashes, British spelling and sentence case throughout. AI is never the headline.
- The Features page meets the 25 Oct brief: no gradient behind section titles, gradients kept in the boxes, at most 6 boxes per section, and clear Coming soon and plan tags.
- No horizontal scroll at 390 on either page. Ink and white glass are the same size and baseline.
