# Aero mockups, round 5: independent critique

Reviewed in Chromium (Playwright) at 1440 full page, 1440x900 first screen, and 390 full page, plus replay scroll positions and frames from every motion.mp4. My captures are in this folder (`*-fold.png`, `*-d.png`, `*-m.png`, `replay-scroll-*.png`, `mo-*.jpg`, `slices/`). No page has sideways scroll at 390 and none throws a JS error.

## Problems shared by all four

- **Pricing doesn't match PRICING-FACTS.md.** The real plans are Free / Basic $3 / Solo $6 / Pro $19, with 3 / 5 / 10 / 20 sessions. A and B invent a plan called "Starter". A, B and D put "Themes across sessions" behind Pro, which is a made-up gate. None of the four shows session counts. Use: Free (3 test sessions, recordings included, live 7 days), Basic from $3 (5 sessions, your own aeroapp.ai address, password, no badge), Pro $19 (20 sessions, custom domain, analytics, priority support). Add a "7-day free trial" line. Don't put "a month" after session counts.
- **The same four "who it's for" photos appear in every direction:** the designer at a monitor, the man in the coat, the phone over code, the curly-haired woman on the floor. A, B, C and D also share the p09 tester. Each team should pick a different set from PHOTOS.md, or the owner will see "every option looking the same".
- **No motion shows the full loop.** A only shows Watch. B never gets to Read. C only shows a quote. D stops at Friction before Insights. The insight payoff, the thing he most wants sold, is missing from all four videos.
- **The test link format is inconsistent.** B and D use `pocket.aeroapp.ai/t/8kq2` (or `/t/4kx`) while their own copy says "the same link". Confirm the real format, then use one link everywhere.

---

## A. Studio

**Strengths**
1. The clearest first screen of the four. Headline, sub, both actions and the three checks ("Free to start / From $3 / No call, no contract") sit above a real session window, and the three proofs row below it answers how, what you get and price.
2. The product UI is the best built. The session window, the insights card ("Top three to fix" with "3 of 4 · 03:08") and the create flow with the prompt and "Aero is connected to Claude" read as a shippable app, and clearly beat today's app.
3. The best copy discipline. Every number is labelled, "Screen and voice. Never a webcam." is stated, and the 05 timeline is honest and labelled.

**Must fix**
1. **Price (06):** "Starter" and its bullets ("Sites that stay live", "Versions and rollback") and Pro's "Themes across sessions" are invented. Replace them with the real Free / Basic / Pro facts above.
2. **App dashboard and site cards:** "v3 · Starter" also uses the invented plan name. Change it to Basic.
3. **Hero window:** the brief asks for "a slight angle" and it is flat. Give it a 4 to 6 degree perspective tilt, as the art direction asked, or it reads as a generic Linear clone.
4. **Hero first frame:** on load the Friction points panel is empty and the transcript has only two lines. A first visitor sees a blank right column. Start the loop with one friction card already present, as at about 6s in the loop.
5. **Mobile hero (390):** the window is about 1,000px tall and is mostly an empty phone frame plus an empty friction panel, and the URL is clipped ("…/sessions/teste"). Use a shorter crop: phone plus two transcript lines plus one friction card, about 560px tall.
6. **Rhythm:** 01, 02 and 04 all use the same pattern of copy beside a washed card. Make 04 Read different, for example a full-width insights panel with its three stat tiles across the top, as Watch is.
7. **Distinctiveness:** it is the safest of the four, close to Vercel and Linear. Add one owned detail: the blue dot as the playhead or friction marker colour across all UI, or colour-wash avatars that match the testers.
8. **Motion:** the 12s loop shows only Watch. Open with 2s of the prompt going live (the 01 card) and close with 2s of the insights card, so the video shows publish, watch and read.

**Scores:** clarity 8, desire 6, craft 8, truth 7, distinctiveness 4. **Total 33/50**

---

## B. Colour

**Strengths**
1. The four-tile hero bento shows the whole loop in the first screen: prompt to live link, a real tester, the session, and the three things to fix. That is the strongest "sell it all on page one" answer.
2. The colour-as-map system pays off in the app. Dashboard status cards ("Live / Testing / To watch / To read") and the colour tags turn the step colours into a real navigation idea. It is the most "design tool" app of the four.
3. Designer details that explain something: the Figma frame labels, the noodles joining three ways into one live link, and the selection outline on the top friction point. Not stickers.

**Must fix**
1. **Hero Read tile, desktop:** "Three things to fix", item 1 is broken. The "1" chip sits alone, the text is pushed right and "03:08" drops to its own line. The selection outline is breaking the row grid. The same component renders correctly at 390.
2. **App session view, mobile (390):** completely broken. The phone frame overlaps the transcript, labels collide ("Skip silences", "Screen · Voice · Friction points") and text runs over text. Rebuild the stacking for narrow widths.
3. **Price:** "Starter" is invented, the bullets are invented, and Pro's "Themes across sessions" is a made-up gate. Use the real plans.
4. **Invented app features:** "Skip silences" and per-task timings ("Task 1 · Find your cards · 2:10") aren't in the product. Remove them, or label them as concepts and confirm with the owner.
5. **Watch section:** the full cobalt slab (about 560px of #3355FF with white text) sits close to the owner's "no dark websites" line, and four saturated slabs in a row is loud. Make Watch a cobalt frame or band around a white panel, not a solid fill behind everything.
6. **Headline weight:** Funnel Display 500 at 58px with -0.03em tracking reads heavy next to the others. Drop to 52px and loosen the tracking to -0.02em.
7. **Who it's for:** linking each persona to a step chip (Designers to Publish, Researchers to Watch, PMs to Read, Students to Test) is forced and not true. Remove the chips. The thick coloured photo borders also look chunky; use 4px.
8. **Mobile hero:** the hero tiles and then the full sections repeat the same content (the prompt card and the session appear twice in the first 3 screens). On mobile, collapse the bento to one tile, or skip it and go straight to the step legend.
9. **Motion:** never gets to Read. The Read chip stays grey to the end. Cut Publish to 2s and add a 3s mint Read scene with the three things to fix.

**Scores:** clarity 8, desire 8, craft 6, truth 6, distinctiveness 9. **Total 37/50**

---

## C. Story

**Strengths**
1. The most distinctive and most desirable direction. Warm paper, roman-numeral chapters, captioned "Fig." product shots and a highlighter used only on her words make it feel like a design publication, not a SaaS template, without being too elegant.
2. It handles the truth best. "The product is real. The session in this story is an example." sits in the top bar, the photo caption says "Aero records her screen and her voice, never her face", the FAQ asks "Does Aero record my testers' faces?", and the clock is labelled "Example times". The content page uses its own habit-tracker example rather than reusing Pocket.
3. The app's transcript-as-article session view puts friction notes in the margin beside the line that caused them, uses her quote as the page title, and shows top priorities and themes in the dock. It is the most original screen of the review and the clearest "insights from real sessions" story.

**Must fix**
1. **Price (VI):** the tiers carry no facts. "Paid, from $3" and "Pro, For designers and teams who test every week" ("teams" hints at seats, which aren't offered). Add the real session counts and key features, plus "7-day free trial". Drop "teams".
2. **Closing line:** "The first test is free" is ambiguous. The free plan is 3 sessions. Use "Free to start, recordings included."
3. **Hero headline:** three lines at 52px plus a 22px sub takes the whole left column. Cut it to two lines ("Publish your prototype. / Watch people use it.") by widening the column to 640px or dropping to 46px.
4. **Quote band under the hero:** the friction margin note starts at about 25% opacity and waits for the animation, so on first view it looks broken or disabled. Start it at full opacity and animate only the highlight.
5. **Length:** about 9,000px desktop and 14,000px mobile, with text-led chapter openings. Cut chapter I's drop-cap paragraph to half, merge "The clock" into Read, and give II or VII one larger photograph so the middle has a visual break.
6. **App sidebar:** the nav icons are empty square placeholders (Home, Tests, Sites, Insights) and look like checkboxes. Use real icons.
7. **Motion:** beautiful but the least explanatory. It is only the quote highlighting over a waveform, with no publish, link or product window. Add a 3s opening of the prompt going live and a 3s end on the Fig. 5 session with margin notes, or the video won't explain Aero to a stranger.
8. **Photos:** p09 appears three times (hero, quote avatar, tester strip), and the "who" set is the same as A, B and D. Swap the quote avatar for initials and pick a different "who" set.

**Scores:** clarity 7, desire 8, craft 8, truth 8, distinctiveness 9. **Total 40/50**

---

## D. Replay

**Strengths**
1. The scroll-scrubbed sticky stage works. Publish, Share, Record, Watch, Friction and Insights each drive the same window, and the chapter bar along the bottom shows progress with the friction marker. It explains "how it works" better than any other page.
2. The motion.mp4 is the most explanatory video: prompt to live, link copied, recording, transcript, friction, all in one window.
3. The angled dark window on a light page meets the owner's "dark app window at an angle" like without making the site dark. The floating "Your AI chat" card makes "straight from a prompt" unmissable.

**Must fix**
1. **Everything after the stage has no gutter.** "Fast, because there is nothing to set up", Price, Who and Questions (`.blk.wrap`) sit at x=0 on desktop and mobile, so text and cards touch the screen edge. The 05 heading on mobile is also at x=0. This is a class collision on `.wrap`. Restore the 63px desktop and 16px mobile gutter.
2. **Hero headline:** 56px Inter Tight in a narrow column wraps to four tight lines and is the heaviest-looking hero of the four, which breaks "too bold, too big". Widen the copy column so it sets in two lines, or drop to 48px.
3. **Price:** "Most people" on the $3 card is an invented usage claim, Pro's "Themes across all your sessions" is an invented gate, and there are no session counts. Use the real plans.
4. **Motion:** ends on Friction with a visible crossfade ghost (the Send screen over Home), and the side caption "Is it under More?" sits against a card that says "Send flow has no back label". Reach Insights by 11s, fix the crossfade and keep the caption and card in step.
5. **Mobile stage:** the window is scaled to about 0.78 and its text is about 6px, so the product, the hero of this direction, is unreadable on a phone. On mobile, show one pane at a time (phone or panel) at 1:1.
6. **App screens:** the dashboard site thumbnails are empty phone outlines (a wireframe look the owner dislikes), and the light transcript and create screens leave half the window empty. Fill the thumbnails with the prototype screens and give the transcript its full length.
7. **Dark default:** the stage and the app default to dark. Given the owner's "no dark websites" rule, try the light window as the default on the homepage and keep dark as the toggle.
8. **Photos:** the "who" strip repeats the same set as the others. "On the sofa / On the go / By the window" is good; make the persona row new too.

**Scores:** clarity 7, desire 8, craft 6, truth 6, distinctiveness 8. **Total 35/50**

---

## Summary table

| | Clarity | Desire | Craft | Truth | Distinct. | Total |
|---|---|---|---|---|---|---|
| A Studio | 8 | 6 | 8 | 7 | 4 | 33 |
| B Colour | 8 | 8 | 6 | 6 | 9 | 37 |
| C Story | 7 | 8 | 8 | 8 | 9 | 40 |
| D Replay | 7 | 8 | 6 | 6 | 8 | 35 |

## Which to show first

**C. Story.** It is the only direction that feels made for Duane rather than for a generic SaaS. It's warm, light, editorial, a designer's tool. It already sells "insights from real sessions" in the tester's own words, which is his stated must-have, and it is the most honest about what is example data and what is recorded. Its weaknesses (vague pricing, a three-line headline, a quote-only video) are quick fixes. B is the strong second if he wants more colour. Fix B's broken mobile session view first.

## One idea each should steal

- **From A (Studio):** the three-proof row right under the hero (Live in minutes / Watch, then read / Priced for one designer). It answers how, what and price on the first screen.
- **From B (Colour):** the step colours as app statuses ("Live / Testing / To watch / To read"). The dashboard tells you what each test needs from you next.
- **From C (Story):** friction points as margin notes beside the transcript line that caused them, plus the "never her face" photo caption.
- **From D (Replay):** the chapter progress bar with the friction marker on it. A small timeline that turns any section sequence into "one test, start to finish".
