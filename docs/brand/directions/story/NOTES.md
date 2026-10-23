# C. Story: UI directions stage

The app read like a calm article. Every main screen leads with what the tester said, set large in Schibsted Grotesk. Around it: warm paper, hairline rules, a single yellow highlighter and the blue full stop. There are no cards with stripes and no icon tiles. Type and status come from the prototype's own thumbnail, words, numbers and rules. The shell is a top masthead (Home, Tests, Sites) instead of a sidebar, so the reading column can be wide. Example data is the same throughout: Kestrel Studio, Solo plan, Pocket (6 sessions, 5 with audio), Tester B at 03:08.

Files: `pages.html` (built by `node src/build.cjs` from `src/build.cjs` + `src/pages.css`), `shoot-story.cjs`, `shots/<id>.png`.

## p1 Home
- Idea: a front page. The lead is the top friction point, quoted, with "4 of 5 testers" and "Play 03:08". "Also new" lists briefs with times. Tests and sites form an index column.
- Works: you see what people said before anything else. Statuses need no badges: Live is the blue dot, waiting is grey text, new is a highlighter mark.
- First run: no lead story, so the page becomes a contents page (i, ii, iii ways in) with "What happens next: Publish, Test, Review".
- Unsure: whether the lead should always be the top friction point or simply the newest session (AppUI round chose a feed without quotes).

## p2 Sessions
- Idea: a contents page for one test. The number is set large (kept from the oldest), with the tester, their first line in their words, the length and the count. Processing shows grey shapes and "Transcript arriving", never typing. No audio says so plainly and offers Watch.
- Moving between sessions: every session ends with "Next session" like the next article, plus No. 1 / No. 3 in the header and J/K.
- Unsure: the first line of the transcript is not always the best line. It may need to be "the line we'd quote" (the top friction quote).

## p3 Session review
- Idea: her words are the headline, the summary is the standfirst, the transcript is the body, and friction points are margin notes. The recording sits in a dock (browser tab, phone prototype, no pointer). The playing line is highlighted word by word.
- Works: this is the calm view Duane liked, now with player, priorities and tasks beside it.
- Unsure: the yellow is doing two jobs (playback highlight and friction rule). The margin rule is the darker yellow so they read apart, but it is close.

## p4 Publish from a prompt
- Idea: a numbered log (i Connect, ii Copy the prompt, iii Waiting, iv Published). Done steps stay visible and grey. The result is a title block with the address, Live, version and "Now test it".
- Claude's side is drawn apart, labelled "Outside Aero", in its own serif and colours, plus the "waiting" state as a small frame.
- Unsure: whether the done steps should collapse to one line once it is published.

## p5 Upload HTML or zip
- Idea: drop area, then one thin ink rule filling (no percentage pill), then a title page: the address set at 42px, Live, version, "Now test it", and the versions with "Roll back to this".
- Works: the address is the hero, which is what people copy.
- Unsure: the drop step could merge with the address field into one line.

## p6 Review across sessions
- Idea: a short report. A headline sentence ("People found sending easy. Almost nobody found their cards."), what to fix first with quotes and play moments, and a margin with themes (tally marks), disagreements and which sessions were included. "Based on 5 sessions with audio, out of 6" is honest about Tester E.
- Unsure: the headline sentence is a summary written for you. It needs a careful prompt so it never overstates.

## f1 Flow: one page that keeps a log
- Idea: no stepper and no new screens. The Pocket page writes an entry with a time for each step (connected, live, test added, link copied, Tester B opened it, transcribed), newest at the bottom, ending on her quote.
- Works: it is clearly different from a stepper or a player-first flow, and it doubles as the test's history.
- Unsure: a long log needs folding once sessions arrive (proposed: one "History" line).

## m1 Marketing kit
- Five components (session card, friction quote, site card, test link, playing transcript line). Each has its app version beside a marketing version at about 1.6x to 2x with less metadata. Then a homepage hero block and a 1200x630 social card built only from them.
- Buttons in the hero are the direction's pill CTAs, drawn flat. The glass script is not inlined here; buttons are being explored elsewhere.

## Toward the shared design system
The components are built from a few typographic parts rather than containers: quote (head face plus highlight), byline, kicker, margin note, rule-led list, status word, tally, and the real prototype thumbnail. Each part maps to an `--aero-*` token set (paper, rule, highlight, ink and type steps). The marketing versions are the same parts at a larger type step, so the same components work in the app and on the site.
