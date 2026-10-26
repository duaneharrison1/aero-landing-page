# Aero homepage round on the v3 UI (23 Oct 2026): notes

Files in this folder:
- `home.html`: the page. `?hero=a` (window centred under the headline, default) or `?hero=b` (headline left, window right, bleeding off the edge). Extra review switches: `?state=0..4` freezes the hero loop at one beat, `?still=1` stops the rotating word and the transcript playback, `?shoot=1` hides the A/B switcher.
- `aero.css`, `aero-make.css`, `aero-review.css`: copies of `v3/shared/aero.css`, `v3/make/extra.css`, `v3/review/review.css`, unchanged. The page adds only an `hp-*` layer on top, using the v3 tokens (no new colours).
- `glass-v3.js`, `favicon.svg`, `lockup.svg`: copied from `v3/shared/`.
- `shoot.cjs`: Playwright script. `node shoot.cjs` (all), `shots`, or `video`.
- `shots/`: `home-{a,b}-d1440-{fold,full}.png` (1440 wide at 2x), `home-{a,b}-m390-{fold,full}.png` (390 wide at 3x), `loop-state-0..4.png` (each beat of the hero loop), `hero-loop.mp4` (15 s, 1440 x 900, one full loop).

## How it is built
- **All words, examples and timings sit in one `window.PAGE` block at the top of `home.html`.** Change copy, the example story (names, times, quote), the app data in the hero window, plans or FAQ there. The rest of the file renders from it.
- **Real components, not drawings.** The hero is the v3 Home screen (layout A: what's new timeline, Sites as preview blocks, Tests as status lines, the `.sb-*` sidebar), built from the same classes. Step sections use the marketing versions from make m8 (site preview block, test link card, event row) and review s7 (session row, quote card, player with task timeline). Components are drawn at their own size and scaled to the column (`.fit`), so a change in the app CSS flows straight through.
- When this moves to Astro: the `PAGE` block becomes a content file and the render functions become components, rendered on the server (for SEO, the text should be in the HTML, not built in the browser as it is in this mockup). The JSON-LD (SoftwareApplication with the four offers, FAQPage) is already generated from the same data.

## Choices
- **Nav:** "Aero." lockup, three plain links, Log in, ink "Start free". No colour. On phones: logo, Start free and a menu button that opens a plain list.
- **Rotating headline:** "Publish your / [Claude artifact | Figma prototype | Lovable app | HTML site]. / Watch people use it." The changing part has its own line so nothing else moves; a calm fade and lift every 2.8 s. Screen readers get one sentence: "Publish your Claude artifact, Figma prototype, Lovable app or HTML site. Watch people use it." Reduced motion: no rotation (first item stays). The last full stop is the blue dot, drawn as a true circle.
- **Hero loop (14.5 s, in the real Home screen):** 1) a "Publishing version 4" row appears with the breathing blue dot; 2) it turns green, "Version 4 published at pocket.aeroapp.ai", and Pocket's preview block joins Sites; 3) "Maya finished a session. The transcript arrives in about a minute." with the dashed "processing" mark, Pocket gets "1 new" in the sidebar and the session meter ticks up; 4) the transcript is in: "7 minutes, 3 friction points", and her first quote opens under it as the app's quote card. Then it resets. No cursor, no typing, no Claude UI.
- **D's progress line** under the hero window: Publish (10:02), Test (11:47), Review (11:48), filling with the loop. In hero B it sits under the copy on desktop and under the window on phones.
- **Hero A vs B:** A is calmer and reads like A Studio; the window starts just below the fold at 1440 x 900. B puts the product in the first screen and lets it run off the right edge, at the cost of hiding the Sites and Tests column. My pick: **B on desktop** (the product is visible without scrolling), with A's phone layout, which both share.
- **Publish, Test, Review:** three rounded panels on the v3 step washes (`--wash-publish`, `--wash-test`, `--wash-review`, with grain). Each has the step word, one heading, one line, and the real component(s) large. Publish: the prompt card from m5 (with "It's a prompt, nothing to install"), whose "Waiting for your chat" turns into "Live at pocket.aeroapp.ai" in step with the hero, then the site preview block. Test: the test link card and the session row. Review: the quote card and the player with tasks on the timeline. On phones the session row (too small to read at that size) is hidden.
- **C's moment:** "Seven minutes on a Sunday morning." Maya (Example), her recorded session playing back with each word highlighting as it plays, the time following along, the waveform filling, and the Issue tag on the 03:08 line already there (it was made after the session). Labelled "Playing back her recording" so it never reads as live. It only plays while on screen.
- **"From prompt to first session"** as D's line: six example times from the prompt to the transcript, drawn in as you reach it (vertical on phones).
- **Good to know:** "Every publish is a version" (the versions list from the site page, with Roll back), "Free sites stay live for 7 days" (the app's own "Offline soon" event), "Bring your own testers".
- **No price comparison.** I didn't have competitor prices I could stand behind today, so I left it out rather than guess. See open questions.
- **Pricing:** exactly PRICING-FACTS, USD, no "a month" after session counts, regional prices left to checkout.
- **Light only, no photos, no founder, AI only as "built with your AI tool" on the way in (Claude, ChatGPT named as places you built it) and "transcribed and summarised" on the way out.**

## Copy deck (every line on the page)

**Meta**
- Title: Aero: publish your prototype, watch people use it
- Description: Put a Claude artifact, Figma prototype, Lovable app or HTML site online at its own address, share one test link, and get each session back transcribed and summarised. Free to start.
- Social: One prompt and it's live. One link to test it. Each session comes back in their own words.

**Nav:** How it works · Pricing · Questions · Log in · Start free

**Hero**
- Prototype hosting and user testing
- Publish your [Claude artifact. | Figma prototype. | Lovable app. | HTML site.] Watch people use it.
- Paste a Figma link, drop an HTML folder, or copy one prompt into the chat where you built it. Share one test link. Each session comes back transcribed and summarised.
- Start free · See an example
- Free to start, recordings included. Paid plans from $3 a month. No call, no contract.
- Progress line: Publish, Live at pocket.aeroapp.ai, 10:02 · Test, Maya finished a session, 11:47 · Review, In her own words, 11:48
- Window (Example data): Publishing version 4. → Version 4 published at pocket.aeroapp.ai. → Maya finished a session. The transcript arrives in about a minute. → Maya finished a session. 7 minutes, 3 friction points. → "I thought my cards would be on the home screen. Is it under More?" 03:08

**How it works:** Publish, Test, Review.
- Publish. **One prompt and it's live.** Paste a Figma link, drop an HTML folder, or copy one prompt into Claude or ChatGPT. It goes live at its own address in seconds to a minute.
  - In the card: Figma link · HTML folder · One prompt / Copy this into the chat where you built it / It's a prompt, nothing to install. / Publish the app you just built to Aero as a site called "pocket". Send every file through the Aero API at aeroapp.ai/api/v1/sites with my key aero_sk_••••7Q2c, then reply with the address. / Copy prompt / Waiting for your chat → Live at pocket.aeroapp.ai
- Test. **One link. Their screen and their voice.** Send the test link to a client, a friend or a classmate. They open it on their own device. No account, nothing to install.
  - In the card: Send this to your testers / aeroapp.ai/t/pocket-7k2 / Copy link / Their screen · Their voice · No account
- Review. **In their own words.** About a minute after each session, it's transcribed and summarised: the friction points, the moment each one happened, and what keeps coming up across sessions.

**Moment**
- One session, start to finish
- **Seven minutes on a Sunday morning.**
- Maya opens the link on her laptop and talks as she goes. You aren't there, and you don't need to be. About a minute after she finishes, her words are written down and the moment she got stuck is marked.
- Maya · Sunday 11:40 · Laptop · Example
- Playing back her recording
- 02:41 Right, sent. How do I get back? There's an arrow but it doesn't say where to.
- 03:02 Is the balance a button? I keep wanting to tap it.
- 03:08 I thought my cards would be on the home screen. Is it under More? (Issue · Major · Cards are hidden under More)
- 03:31 Oh, there they are. Under More. I wouldn't have looked there.
- **From prompt to first session.** 10:02 You copy one prompt, into the chat where you built it · 10:03 Pocket is live, pocket.aeroapp.ai · 10:04 Test link sent, to a client, a friend and a classmate · 11:40 Maya opens it, on her own laptop · 11:47 She finishes, 7 minutes, 2 tasks · 11:48 Transcribed and summarised, 3 friction points, in her words
- Example times. Publishing takes seconds to a minute; the transcript about a minute after a session. The only real wait is for your tester.

**Good to know.**
- Every publish is a version. Roll back to any of them. The address stays the same.
- Free sites stay live for 7 days. On the Free plan a site goes offline after 7 days. Paid plans keep it online. (UI: Offline soon, pocket.aeroapp.ai goes offline in 2 days.)
- Bring your own testers. No panel to buy, no seats, no sales call. Anyone you send the link to can take part.

**Pricing**
- **Free to start. From $3 a month.** Every paid plan starts with a 7-day free trial. Monthly, no call, no contract, cancel any time.
- Free, $0: 3 test sessions · Recordings included · Sites stay live 7 days · Start free
- Basic, $3 a month: 5 test sessions · Your own aeroapp.ai address · Password protection · Custom favicon · No Aero badge · Start 7-day trial
- Solo, $6 a month: 10 test sessions · Everything in Basic · Custom domain · Site analytics · Start 7-day trial
- Pro, $19 a month: 20 test sessions · Everything in Solo · Priority support · Start 7-day trial
- Prices in US dollars. Your local price is shown at checkout.

**Questions.**
- What can I put online? A Figma prototype (paste its link), an HTML folder or zip, or anything you built in Claude or ChatGPT, which can send it to Aero with one prompt. Each one gets its own address on aeroapp.ai.
- How does publishing from Claude or ChatGPT work? Aero gives you a prompt with your key in it. Paste it into the chat where you built the page. The chat sends the files to Aero and replies with the address. There's nothing to install.
- Do my testers need an account? No. They open the test link on their own device and start. Aero asks their permission to record their screen and voice, and they can stop at any time.
- What is recorded? Their screen and their voice as they think aloud. Never their face: there is no webcam recording. The recording doesn't show the mouse pointer.
- How soon can I read a session? You can watch it as soon as it ends. The transcript and summary follow about a minute later, with friction points in their own words and the time each one happened.
- How long is a session? As long as your tester needs. There is no set length and no timer on their screen.
- What happens to my site on the Free plan? It stays live for 7 days, then goes offline. Any paid plan keeps it online, and every plan keeps your versions.
- Can I use my own domain or a password? Password protection and a custom favicon come with Basic and up. A custom domain comes with Solo and up.

**Closing:** From prompt to first session. / Free to start, recordings included. No call, no contract. / Start free · See an example

**Footer:** Made for people who make things. / Product: How it works, Pricing, Questions, Log in / Guides: Publish a Claude artifact, Publish a Figma prototype, Test a Figma prototype, Host an HTML site / Aero: About, Privacy, Terms, Contact / © 2026 Aero. Names and data in the examples on this page are made up.

## Open questions for Duane
1. **Hero A or B?** I'd pick B on desktop. Both share the phone layout.
2. **Prompt or connector?** DECISIONS says the prompt flow is a prompt, not a connector, and the page says so ("nothing to install"). Today's live site still leads with `claude mcp add ...` and an MCP FAQ. Confirm the prompt is the story, or tell me to mention the MCP route as well.
3. **Lovable app in the headline.** How does a Lovable app reach Aero today: its exported build as an HTML folder or zip, or a prompt in Lovable's chat? The page only promises "anything you built", so the answer decides one FAQ line.
4. **Free sites after 7 days.** I wrote "goes offline" and "paid plans keep it online". Is that exact (offline vs deleted, and does upgrading bring it back)?
5. **Phone testing.** Earlier mockups said Figma prototypes can be tested on a phone (voice only) and HTML sites on a desktop for now. I left it off the page because I couldn't confirm it's still true. Add it as an FAQ?
6. **Price comparison.** Brief allows it only if honest. Want me to research current Maze, Lookback and UserTesting prices with sources, or leave it out?
7. **Live site differs from PRICING-FACTS**: its fallback plan table puts password protection on Solo and lists project counts. The page follows PRICING-FACTS (password on Basic). Worth fixing on the live site when this ships.
8. **Hero B crops the Sites column.** Fine as a bleed, or do you want the window shifted so the quote and Sites both show?
9. **Example names.** Maya (tester), Mia Chen / Kestrel Studio (account), Pocket. The v3 sidebar showed "Pro plan 15 of 20"; the homepage uses "Solo plan 6 of 10" so the session count can tick up during the loop.
