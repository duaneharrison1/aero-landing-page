# D · Replay: UI directions stage notes

Files: `pages.html` (built from `pages.src.html` by `node build.cjs`, which inlines the Inter Tight "Aero." logo), `shoot-replay.cjs` (writes `shots/<id>.png` at 1440 wide), `shots/`.

The direction in one line: dark, player first, and one progress line along the bottom of every screen. On Home it is your loop (Publish, Test, Review); in a flow it is the steps; in a session it is the recording's own timeline.

## p1 Home
- Idea: opens on one moment worth watching (Session 2, cued to 03:08) with "What's new" beside it. Tests are reels: one bar per session, to scale, with friction ticks. Sites are real thumbnails.
- Works: you see a reason to press play before reading anything; the loop line tells you where Pocket is (4 read, 1 arriving, 1 with no audio).
- Unsure: the cued clip needs a server-side pick of "the" moment (top friction point by count). Reels may be too abstract for someone with one session.
- First run: the empty state is an empty player (dashed phone) with the three ways in as plain rows, prompt first. No tiles, no icons.

## p2 Sessions
- Idea: every session on one shared clock, like tracks in an editor. The 03:08 cluster lines up across 4 sessions with a guide.
- Works: states are honest and distinct: waveform (done), hatched (transcript arriving, never typing), flat dotted line (no audio). J and K step through; the top preview shows the first line in their words.
- Unsure: long sessions (30 min plus) squash short ones; needs a zoom or "fit to longest" toggle. The preview pane has spare room on the right.

## p3 Session review
- Idea: the recording is the page. Task chapters and friction markers sit on the timeline; the transcript follows the playhead word by word; summary, friction points and fix first sit under the player, every time a link back into it.
- Works: one screen holds everything; the amber mark means the same thing in the timeline, transcript and list. No cursor drawn. Light variant shown as a second frame.
- Unsure: three findings columns under the player get tight at 1280 wide; they may need to become tabs. The floating control pill needs a glass decision.

## p4 Publish from a prompt
- Idea: connect once, copy one line, wait, published. While waiting, a timecoded event log (copied 10:41:02, chat called Aero, receiving files) fills the empty player area.
- Works: the waiting step stops feeling like a hang; Claude's panel is outside Aero's window, beige, labelled "Outside Aero", no logo.
- Unsure: the log needs real events from the connector (prompt copied is client-side; "chat called Aero" and file receipt are server-side). ChatGPT connector steps are not drawn in detail.

## p5 Upload HTML or zip
- Idea: same structure as p4: the bottom line is the upload progress; the published state shows the site in the canvas as testers see it, address, version, rollback and "Now test it".
- Works: address set large in mono, one primary action. "Now test it" lands on Share with the link copied.
- Unsure: "up to 50 MB" is a placeholder: check the real upload limit in code before using it.

## p6 Review across sessions
- Idea: all sessions overlaid on one clock (where people got stuck), then what to fix first with counts ("4 of 5 testers") as cells and the quotes as playable clips. Themes, disagreements and "how this was made" on the right.
- Works: honest base ("Based on 5 of 6 sessions, session 5 had no audio"); every quote has its time and opens its moment.
- Unsure: "how long it held them" as a sort key needs a duration per friction point we don't store yet. Disagreement detection is proposed, not built.

## f1 The flow
- Idea: player-first. The journey is one timecoded progress line; each step is a chapter; the last chapter is the player itself. Example times 00:00, 00:05, 00:40, 00:50, later, +1 min after.
- Works: reads like the video brief (Aero, Claude cut in, live URL, test link, tester on their own computer, results); the blue end marks what happens after the tester finishes.
- Unsure: the tester frame is a stand-in; the real tester screen is a separate piece of work.

## m1 Marketing kit
- Idea: five app components (session track, friction point, site row, test link, transcript line) each beside a 2x marketing version with the metadata removed, then a 1200x630 card built only from them.
- Works: the quote and the address carry the brand at size; dark tiles on a light page keep D's striking window without a dark website.
- Unsure: the social card's window and quote overlap could feel busy at small preview size; a version with the quote alone may share better.

## How these become the shared design system
The window tokens (`--w-*`, dark and `.light`) already flip as one set; the pieces here (loop line, waveform with markers and playhead, track row, friction point, transcript line with word highlight, event log, link field) are each one class with a demo-data mode, so the marketing tiles in m1 are the same components with fewer rows. They would move into `aero-design-system.css` as tokens plus `ut-theme`-scoped components and be added to AeroShowcase, the loop line and the waveform first.

## Truth checks
- No moving cursor anywhere. No transcript typing; processing is hatching plus "usually about a minute". Word highlight only on a recorded session.
- Claude drawn simplified, labelled "Outside Aero", outside Aero's window.
- Plan used: Solo, "8 of 10 test sessions" (10 from PRICING-FACTS, no "a month"). First run shows "Free sites stay live 7 days".
- All names (Kestrel Studio, Mia Chen initials MC, Tester A to F) are examples, labelled in the page.
