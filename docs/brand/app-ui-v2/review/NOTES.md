# Team 1 (review), app UI round v2: notes

Files: `pages.html` (built by `build.py`), `review.css` (screen layouts), `shoot-review.cjs` (shots in `../hi/review-s1.png` to `review-s7.png`). Shared: `../shared/aero.css`, `glass-v3.js`, logo SVGs.

## The shared stylesheet (`../shared/aero.css`)
- A Studio's `ui.css` and `pages.css` rebuilt on tokens: surfaces, text, lines, accent, buttons, tags, waveform, avatars, washes. Every colour in light and dark.
- Theme: `data-theme="dark"` on `<html>` (the toggle) or on any wrapper, so one page shows the same frame in both. Legacy `--w-*` aliases are redeclared on every theme root so A's markup works inside dark frames.
- Primary buttons stay ink with the quiet V3 glass. In dark, the fill flips to light ink (`data-fill="#F2F2F4"`).
- New shared parts: tags (Issue diamond, Confusion circle, Works well square, Note ring; a shape and a word, so colour is never the only signal), the three-bar severity mark, filter chips, segmented switch, session timeline (task regions, waveform, marks, playhead), floating task pill, follow-along transcript lines, "Back to now", quote card (one play control, waveform), popover, modal, blue dot loader.
- Fixes: the Checkout "Pay" label (specificity), and the app grid no longer grows past the window when content is long.
- The prototypes (Pocket, Checkout) keep fixed colours in both themes, because they are the tester's content.

## What changed from A, and why
- **Sessions:** full-width rows instead of the table plus peek panel. Each row has the tester's name and device, a summary or quote, when, length, tasks "2 of 2", counts per tag with severity under issues, and a Watch button. Ines is "Transcript arriving, about a minute" (and can already be watched), Tester 8 is "No audio", and the owner's run shows "You" and is left out of Insights. Newest first.
- **Watch:** dark is the hero. The sidebar collapses to icons. A recorded browser tab (a Figma prototype on Figma's grey, with no pointer), the floating task pill, one timeline with the two tasks as regions, and tag marks under the waveform. Filter chips dim the other marks. The transcript follows along: the current word is highlighted and it auto-scrolls, with "Back to now" once you scroll away. Click a line to jump. Speeds, Skip silence, the "?" keyboard sheet, Shift N / Shift P for the next and previous tester, and Download (video, transcript, transcript and summary).
- **Read:** C Story's article. Her words are the headline, the summary is the standfirst with the task results, and the transcript is the body with tags and notes in the margin. The video shrinks to a corner and keeps playing.
- **No tasks / no audio:** no task lane, a flat line saying "No sound in this recording", a crossed-out Transcript tab, Read turned off, and a plain explanation. Task ticks still count. Nothing is invented.
- **Insights:** its own tab. The summary comes first, then a per-task table (completed, median, longest, where people got stuck). Task 2 is opened into D Replay's timeline, but per task, with each tester measured from their own start and a median line. That replaces the shared clock Duane found unclear. Issues are ranked "4 of 6 testers" with dots per tester and playable quote cards. Beside them: what worked, where testers disagreed, a confidence note, and links to the sessions. There are switches for By priority, By task and By theme, plus Download report and Copy as table.
- **Empty and early:** with 0 sessions, three steps say what happens and when, a faded Example preview of the finished page sits beside them, and there are two buttons: Copy test link and Open the example. With 2 sessions, the page shows "Patterns appear from 3 sessions" as dots, low confidence, and "Seen so far", unranked.
- **Marketing:** three components shown bigger (session row, quote card, player with task timeline) and a 1200x630 card built only from them, dark first.

## Open questions for Duane
1. Sessions order: newest first (my pick) or numbered from the first as in A?
2. Should the owner's own runs ("You") stay out of Insights by default? I'd say yes, with a switch in Setup.
3. Insights as a tab of each test (my pick), with Home only linking to it. Or should there also be one place for all tests?
4. Ranking: severity first, then how many testers hit it? Severity is three levels (Minor, Major, Critical), set by the summary and editable by you.
5. Should the Read view open by default once someone has seen the session? I'd keep Watch first and remember each person's last choice.
6. Primary button in dark: light ink (shown), or soft graphite?
7. "Open the example": a read-only Example study inside the account, listed under Tests until dismissed. OK?
8. Truth checks before build: does the recorder log task ticks with times, so time on task is real? Can a session have no audio while tasks still count? Is "Skip silence" possible from the audio track?

## Notes
- The Insights frame is drawn as the full scrolling page (1440 x 1640). Every other frame is 1440 x 900, shown at 88%.
- Example names added to the brief's list: Ines, plus "Tester 8" to show a tester who gave no name.
