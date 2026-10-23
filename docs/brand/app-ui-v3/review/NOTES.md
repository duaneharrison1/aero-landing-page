# Team B (review), app UI round v3: notes

Files: `pages.html` (built by `build.py`), `review.css` (all of Team B's styles), `shoot-review.cjs` (shots in `../hi/review-s1.png` to `review-s7.png`, 1440 wide, 2x). Shared: `../shared/aero.css` (Team A), `glass-v3.js`, logo SVGs. Nothing new was asked of the shared CSS beyond the sidebar.

## What changed from v2

**Everywhere**
- **Sidebar:** switched to Team A's `.sb-*` sidebar. "Aero." with the blue dot and the collapse arrow at the top, Home, Sites, Tests, then up to 5 recent tests under Tests (Pocket, Onboarding v2, Checkout, Pricing page, Juniper labelled "Sample"). Plan meter and account (Mia Chen, mia@kestrel.studio, Example) bottom left. Watch, Read and the no-audio session use the collapsed icon rail.
- **"Open as a tester" is "Preview as tester"** on every test header and in the owner's session row.
- **Sample test:** Juniper (a plant shop prototype, four finished sessions) is in the sidebar, in All sessions with a "Sample" label, and is what the empty Insights page offers ("Open Juniper, the sample test"). Sample sessions don't count towards the plan.

**s1 Sessions**
- **Filter bar** replaces the four chips: search across everything testers said, then Status, Tag, Device, Audio, Tasks, Date, a count ("2 of 9 sessions") and the sort. An applied filter reads "Tag  Issue, Major and up ×"; Clear removes them all.
- New **All sessions** frame (Tests › All sessions tab): the same rows plus a Test column, the same bar with a Test filter first.
- New states card: every filter menu with counts (Tag also has a severity switch), two filters applied, search with matched words highlighted in the quote, and the "nothing matches" state.
- Owner runs: "You", with a small "Not in Insights" label; the line says the run is free.

**s2 Watch**
- **Transcript tidied:** one time column (44px, tabular figures), one rhythm (13.5/21, 9px padding per line), task headers as a quiet divider with the task name, and tags as one quiet line under their line (shape, word, severity as a word, the moment's title) instead of coloured chips. Past lines ink-2, future lines muted, the current line lit with the soft blue and its time in blue; the bottom fades out. Follow along, click to jump and Back to now are unchanged.
- New state: hovering a task region shows its name, the optional task description and its time.
- Per-task summary shows the optional description under each task name.

**s3 Read**
- Margin notes are two calm lines: the moment's title, then shape, word, severity and "4 of 6 testers". No more wrapping counts.

**s5 Insights**
- **Timeline redrawn** as "Session by session": one row per tester with their name and length, each from their own start, using the session player's parts (the same task regions, the same tag marks, the same blue line for hover). A minute scale with faint gridlines, a median row (task 1 01:41, task 2 02:50) and a dashed median finish line (04:46). Ana's task 2 is hatched "Gave up", Tester 8 shows "No audio · tasks only". Jonas's row is shown hovered: the blue line, a card with the moment ("Where are my cards?" 01:52) and "Open session". Clicking any point opens that session there. Whole session / Task 1 / Task 2 rescale it.
- The task numbers were checked so the table and the timeline agree (medians 01:41 and 02:50, longest 02:18 Maya and 04:30 Ana).
- "By task", "By theme" and "Copy as table" now sit two up with the table full width, so nothing wraps.

**s6, s7** sample test copy; ranking text now says severity first. Marketing note: these components suit feature pages; general marketing keeps the real-UI pages.

**Fixes:** the Checkout "Pay £48.00" label is centred again; a class name clash with a new shared `.fcount` was avoided.

## Duane's answers, applied
- Newest first; numbers never change.
- Own "Preview as tester" runs are free, shown as "You" with "Not in Insights", and kept out of Insights.
- Issues rank by severity (Critical, Major, Minor), then by how many testers.
- Sessions open in Watch, then remember each person's last choice.
- Tasks have an optional description (task tooltip and per-task summary).
- Recent tests (up to 5) under Tests in the sidebar.

## Still open for Duane
1. Sample test: the same Juniper for everyone (shown), or one made from the person's first site?
2. Where All sessions lives: a tab on the Tests page (shown), or its own line in the sidebar under Tests?
3. Truth checks before build (unchanged): does the recorder log task ticks with times? Can a session have no audio while tasks still count? Is "Skip silence" possible from the audio track?

## Notes for Team A
- The sidebar plan line in the shared CSS example says "Test sessions this month". PRICING-FACTS says not to write "a month" after session counts yet, so Team B writes "Test sessions used".
- Team B shows Pro plan, 15 of 20 (9 + 2 + 4 sessions across the tests); Team A's frames show Solo, 8 of 10. Worth picking one for the board.
