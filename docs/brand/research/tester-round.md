---
version: 2026-11-05.1
brand-sync: figmaApp docs/brand is the source. Copy this file unchanged to aero-landing-page/docs/brand/research/.
---

# Tester round: tasks, permission, stop sharing, pages

Board: `docs/brand/app-ui/tester-round.html` (built by `app-ui/src/tester-round-build.py` from the app-ui kit). Findings: `docs/research/user-tests/2026-10-30.md` (not synced). Nothing here is built.

## Summary

- **Pick: layout A, a task bar across the top.** It is part of the page above the site, not a card over it, so it can't read as a notification. It costs height (about 90px) and no width, so responsive sites test at their real width.
- The bar holds the step badge, the task, Done and Couldn't do it. After Done it offers an optional rating and a **Next task** button. The tester moves on when they choose. No hard stop per task, no modal.
- The Recording pill is its own glass pill, top centre, as on the website demo. Buttons are the V3 caustic glass buttons (`data-glass-v3`), as on the website. TaskPanel still uses the older `GlassButton`.
- **One permission card, one button: Start test.** It says what is recorded, who sees it, what Chrome will ask and how to finish. "Share tab" goes.
- **Stopping the share asks "Are you finished?"** with "Yes, I'm done" and "No, keep recording". It never ends as "abandoned".
- **Several pages:** HTML sites can show the page name and arrows now. Figma prototypes can't show "1 of 2" yet (see below).
- Your #302 question: the **⋯** is the panel menu (Move panel, Mute, Restart, End test). The **line** is Minimise, folding the panel to a pill. In A both go; the menu keeps Restart, Mute and End test.

## 1. Where the designs disagree

Sources: `tester.html`, `TESTER-NOTES.md`, `UI-BRIEF.md`, DECISIONS tester lines, `tester-panel.html`, the website hero demo, TaskPanel, the overlay. Full table on the board (section 01). The main splits:

- **Form:** floating plate (tester.html) or docked rail, or "a square panel" (23 Oct); now a bar.
- **Corner:** bottom right (boards, old TaskPanel) or bottom left (24 Oct, #302, demo).
- **Recording sign:** in the panel header with a timer (tester.html) or a separate pill with no timer (26 Oct, 4 Nov, demo).
- **Buttons:** older `GlassButton` (code), V3 glass (website, tester.html), flat outline (overlay), a text link for Couldn't do it (demo).
- **Done:** disabled until the prototype is used (Figma) or always on (site tests).
- **Permission:** two rows and two buttons (tester.html) or one Start press (site tests in code).
- **Stop sharing:** Figma drops video and goes on silently; HTML finishes at once; the notes propose "share again".
- **Rating, title, phone:** emoji modal or inline buttons; "Test" or "Pocket test"; dock below or compact bar.

## 2. Layouts

| | A. Top bar (pick) | B. Docked side panel | C. Floating, louder |
|---|---|---|---|
| Reads as a notification | No | No | Still can |
| Next step visible | On the rating step | Always | One line |
| Site layout | Height only | Width minus 320px, may flip to tablet | Unchanged |
| Covers the site | No | No | Yes |
| Phone | Compact bar | Needs another design | Needs the dock |
| Build | New component | Reuses the rail | Edits TaskPanel |

Scenarios drawn for A: task, rating then Next, Undo, long text with Show all, last task, no tasks, menu, end early, several pages, phone, thank-you. B and C are covered in a table.

## 3. Permission card

Copy (Example names):

- Heading: Press Start to begin.
- Intro: Mia would like to hear you try Pocket. This is what gets recorded.
- Your voice: So Mia hears what you think. Talk as you go.
- This tab, as a video: Only this tab. Not your face, your other tabs or the rest of your screen.
- Who sees it: Mia Chen at Kestrel Studio. It's transcribed and summarised for Mia, and nobody else gets it.
- What happens: Chrome asks to let this page see this tab, then to use your microphone. Choose Allow each time. Recording starts after the last one. To finish, press Finish at the top of the page. If you press Chrome's Stop sharing, we'll ask if you're done.
- Button: Start test. Under it: You can stop at any time.
- Two-tab fallback: "Record the Pocket tab" and "Choose the Pocket tab". Never "Share tab".
- Phone: voice only, same card.

Feasibility: the HTML flow already starts the tab share and the mic from one press. Ask for the tab first (it needs the click), then the mic. Not checked in Safari or Firefox. A browser that refuses falls back to two buttons.

## 4. Stopping the share

When the video track ends, show "You stopped sharing. The video has stopped. Your voice is still being recorded. Are you finished?" "Yes, I'm done" runs the Finish path. "No, keep recording" asks Chrome to share again; a second video file joins the session. Closing the card leaves voice-only with the pill saying "Voice only".

Today: HTML tests finish with no question (`UTHtmlController`); Figma tests drop the video and carry on silently (`UserTestingTester`). "Abandoned" comes from `cleanupStaleTestingSessions` for stale in-progress sessions, so a tester who stops sharing and closes the tab lands there. Change it so a session with saved recording is Incomplete (the session row already has that state).

## 5. Several pages

- **HTML site:** the overlay already reports page loads, so the page name is available. "2 of 3" needs the owner to list pages in setup (a site's pages have no order). Arrows message the overlay.
- **Figma:** embed URLs set `hide-ui=1`, which hides Figma's own controls, and the legacy embed sends no events. Now: stop hiding Figma's controls on test pages (to verify in a real embed) and let the task name the page. Later: the Embed API's screen-change events (OAuth setup, see `cursor-recording.md`) give the current screen name. A total needs the owner to type it.

## 6. What it does to recordings

The panel is in the tab recording, so its place is in every replay.

- **A:** the task is on screen in every frame (useful for review). No content hidden. Height is 90px less, so a full-height hero is shorter.
- **B:** the width is 320px less, so the recorded site can be a different layout from the real one. The main reason against it.
- **C:** hides whatever is under the card, and the card moves.
- **Pill (all):** top centre, about 120 by 32px, over the site's header area. It can sit on a site's own header.
- **Glass** is on buttons and the pill only. The bar is solid so text stays readable and the video isn't warped by refraction.
- Truth rules hold: no cursor, no live typing, names labelled Example.

## Decisions for Duane

1. **Layout:** A (recommended). B only if you want the full task list always visible.
2. **Recording pill:** hang it just under the bar at top centre (recommended), or inside the bar.
3. **Done always on:** drop the Figma rule that disables Done until the prototype is used.
4. **Rating:** inline and optional beside Next task, with Undo, instead of a modal.
5. **One permission button** for Figma and HTML tests, after a check in Chrome, Safari and Firefox.
6. **Stopping the share:** ask "Are you finished?", and change the clean-up job so a session with saved recording is Incomplete, not Abandoned.
7. **Pages:** HTML name and arrows now; Figma controls back now, a live count with the Embed API later.
8. **Buttons:** V3 caustic glass everywhere in the tester UI; move TaskPanel off the older `GlassButton`.
9. **Menu and minimise:** remove Move panel and Minimise in A; keep both, labelled, in C.
10. **Words:** "Share tab" removed; Start test; fallback "Record the Pocket tab".
11. **Two-tab overlay:** draw the same bar inside the site's tab so there is one design.
12. **After you pick:** I add the decisions to DECISIONS.md, the build to TODO (Phase 6), and the bar and pill to the AeroShowcase tester section.
