# Round v3: refine v2 (23 Oct 2026)

Duane on v2: "overall looks amazing". This round polishes it, it does not redesign it. Read `BRIEF.md` (the v2 brief, still valid) and the newest section of `/home/claude/figmaapp/docs/brand/DECISIONS.md` ("after the app UI v2 board"). Answers to open questions may arrive later; until then keep what v2 shows.

Act as the principal art director, product designer and UI engineer of a top product company (OpenAI-level craft). Every gradient, spacing step and type size should feel inevitable.

## Changes everyone applies
1. **Sidebar = today's sidebar, slightly improved.** Top: the "Aero." logo (Geist 500, blue dot) with the collapse arrow beside it (collapses to an icon rail). No workspace name at the top. Nav: Home, Sites, Tests (recent tests listed under Tests, up to 5). Bottom left: the account (avatar, name "Mia Chen", email, labelled Example) with the plan meter above it. Team A writes the CSS (`.sb-*` in shared/aero.css) first; both teams update their own markup to it.
2. **"Open as tester" is "Preview as tester"** everywhere.
3. **Sample site and sample test exist in every account** (labelled Example, deletable): show them in lists and Home where natural.

## Team A ("system and make"): owns `shared/aero.css` and `make/`
- **The gradient system (the main job).** Three step washes, Publish, Test, Review, that match the marketing material: study `/home/claude/research/mockups/studio/home.html` (A's marketing page), the round 3 references board `/home/claude/research/brand/board3/aero-brand-round3.html` (the OpenAI- and Linear-like directions he liked) and `/home/claude/research/explore/hi/studio-m1.png`. Define them as tokens (light and dark), each a soft multi-stop mesh, never muddy, never banding, with a subtle grain if it helps; the same tokens drive app cards, empty states and the marketing kit. Plus a **site-tinted wash**: after an upload, derive a wash from the site's own dominant colour (show 4 examples: coral, green, navy, yellow sites) that still sits in the same family. Show a token sheet section (`g0`) with every wash in light and dark, and what each is used for.
- **Site page:** remove the "Test it if you like" push; testing lives in the site's menu as "User test this site" (explain it copies). After publishing, land on the site's page in Aero, not the live site.
- **Tester task panel:** a square panel the tester can drag out of the way (show it moved to two positions and minimised), a separate timer, buttons "Done" and "Couldn't do it", task title with an optional description line. Keep words on the frosted plate; glass only on small chrome.
- Recheck every make section (m1 to m8) for spacing, alignment, type scale, and how gradients sit; fix anything that looks generated.

## Team B ("review"): owns `review/` (only `review/review.css` for styles; ask nothing new of shared CSS beyond the sidebar)
- **Sessions:** add filters (status, tag, device, has audio, tasks completed, date) and search; the same filter bar on an "All sessions" view across tests.
- **Session review:** tidy the transcript: even line rhythm, consistent time column, tags as one quiet line under the line they belong to, no crowding; current line clearly lit, others calm. Keep follow-along, click to jump, Back to now.
- **Insights timeline:** redraw it to align with the session timeline's design language (same task regions, same marks, same playhead colour), one row per tester with their name, a clear scale, a median, hover state; click a row to open that session at that moment.
- Recheck s1 to s7 for spacing and alignment.

## Both
- Light and dark for every frame. 1440 x 900 frames.
- Screenshots at deviceScaleFactor 2 to `/home/claude/research/v3/hi/<team>-<id>.png`; look at them and fix before finishing.
- Report: what changed, anything that needs Duane.
