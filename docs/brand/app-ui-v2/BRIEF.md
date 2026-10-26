# Aero app UI, round v2 (23 Oct 2026): A Studio, refined, light and dark

Duane picked **A · Studio** as the base after the UI directions board. This round redraws the app on that base with his notes. Two teams work in parallel on different screens; both must look like one product.

## Read first (do not skip)
- `/home/claude/figmaapp/docs/brand/DECISIONS.md`: the section "23 Oct 2026: after the UI directions board" is the brief. Follow every line.
- `/home/claude/figmaapp/docs/brand/research/session-review-best-practices.md`: what pro tools do (Dovetail, Lookback, UserTesting, Maze, Frame.io...). Use it.
- `/home/claude/research/explore/BRIEF.md`: product truths, banned "looks AI-made" patterns, copy rules (British spelling, sentence case, no em dashes, AI never the headline).
- `/home/claude/figmaapp/docs/brand/PRICING-FACTS.md`: the only source for plans and limits.
- The A Studio pages to start from: `/home/claude/research/explore/studio/pages.html` and its source `/home/claude/research/explore/studio/src/` (pages.css, ui.css, glass-v3.js, logo SVGs) and `build.py`. Look at the screenshots in `/home/claude/research/explore/hi/studio-*.png`.
- Today's live app, as the base to improve on: `/home/claude/research/explore/today/t-*.png`.

## Shared rules for both teams
- **One shared stylesheet.** Team 1 owns `/home/claude/research/v2/shared/aero.css` (tokens for light and dark, type, shell, sidebar, buttons, badges, cards, modal, player). Copy A's `ui.css` into it as the starting point in your first 15 minutes, then refine. Team 2 links that same file and asks nothing of it beyond what A already has; if Team 2 needs a new component, it puts it in its own `extra.css` with the same tokens. Both pages must work in light and dark with a toggle (`[data-theme=dark]` on the root), and every frame is shown in both.
- **Logo:** "Aero." in Geist 500 with the blue dot (`/home/claude/figmaapp/docs/brand/logo/`). Blue is the accent for secondary actions, the playhead, focus, loading (the dot as a loader).
- **Buttons:** ink. Rounded rectangle normally; a full pill only for floating controls (task pill, player). Primary has a subtle V3 glass finish (`glass-v3.js`, quiet setting), solid ink fallback; must pass AA.
- **Sidebar:** collapsible (an arrow hides it, as today). Workspace name at the top ("Kestrel Studio", Example). Items: Home, Sites, Tests. When a person has one test, it can sit in the sidebar directly.
- **Sites and Tests are separate.** Sites list = blocks with real previews (cached screenshot of the page). Tests list = status lines (sessions, live, last session) with a small preview. "Test this site" copies the site into a new test with its own link. Going straight to Test hosts the prototype under the test. Sites are public by default with a private switch.
- **Testers have names** (asked on the start screen, optional; "You" when the owner tested). Example names: Maya, Tom, Priya, Jonas, Ana, Leo (labelled Example).
- **Empty states teach without overwhelming**: show what will appear and when, and offer the Example study ("Open the example") so people can see a finished review before inviting anyone.
- **Truth rules:** transcripts arrive about a minute after a session; no moving cursor in any replay; word highlight only while a recorded session plays back; Claude's UI kept visibly separate and labelled "Outside Aero". The prompt flow is a prompt the person copies into Claude or ChatGPT (it calls Aero's API with a key); there is no connector to install.
- Frames are 1440 x 900 app windows, real content, Example data labelled. No lorem ipsum.

## Deliverables (each team)
- `/home/claude/research/v2/<team>/pages.html` with `<section class="xp" id="...">` sections, each: h2, one line on the idea, the frame(s) in light, then the same in dark. Add short notes beside each frame only where a decision is needed ("Option: ..."). Where you are unsure between two layouts, show both, labelled A and B, and say which you'd pick.
- `NOTES.md`: what changed from A and why, open questions for Duane.
- Your own screenshot script in your folder (Playwright: `require('/home/claude/e2e/node_modules/playwright')`, `chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' })`, viewport 1440 wide, deviceScaleFactor 2), saving `/home/claude/research/v2/hi/<team>-<id>.png`. Look at every shot and fix what's broken before finishing.
- Work only in your folder (and Team 1 in `shared/`).
