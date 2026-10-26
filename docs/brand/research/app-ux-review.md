# Aero web app: UX review

Reviewed 22 Oct 2026. Sources: the code in `/home/claude/figmaapp` (Aero routes only) and the 10 screenshots in `shots/`. Read-only: nothing was changed.

Paths below are relative to `/home/claude/figmaapp/`. "Verified" means I traced it in code. "Unverified" means it fits the code and the screenshots but I could not prove it without the live database or logs.

One note before starting: the live Share tab says "Share this URL, with testers. They can open it on any device", but the repo says "Share this link with testers. On a phone, only their voice is recorded." So production is running an older build than `src/`. Copy findings refer to the repo.

---

## Summary

- The product works end to end, but a new user loses trust in the first five minutes. Pages open blank. Tabs show "0 sessions" for a test that has sessions. Insights never arrive. The lists are buried under drafts the user never meant to make.
- Most of this comes from four causes:
  1. Pages render nothing until every read finishes.
  2. Tabs don't wait for the sessions listener.
  3. Cross-session insights only run when someone opens the Insights tab, and they fail silently.
  4. A draft is saved the moment someone clicks a source tile.
- Once synthesis does succeed, the Insights tab will crash. It reads field names the function never writes, and it renders an object as text. There is no error boundary, so the page goes blank. Fix this together with the trigger.
- The app leads with User Testing and "AI", but the order of value is publish, then share, then watch. The flows should follow that order.

---

## 1. Flow map (today)

### A. First visit to first published site
1. A visitor on aeroapp.ai signs up (`/signup`, `UTPluginAuth`).
2. `AeroLayout` checks auth, then makes 3 reads in a row (profile, subscription, user doc) and shows a skeleton while they run.
3. They land on `/`, which is **My Tests**, not Sites (`App.js:408`). The empty state says "Create your first test to start collecting feedback on your Figma prototypes."
4. To publish, they must find **Sites** in the sidebar (second item), then click **New site**.
5. CreateFlow step 1 offers Upload HTML, From Claude or ChatGPT, or From Figma. **Clicking a tile creates a draft doc at once**, with a random name like `cool-flamingo` (`CreateFlow.js:238-248`).
6. Step 2 depends on the source:
   - Drop: drop the files, then deploy.
   - Agent: copy a prompt with a token, paste it into Claude or ChatGPT, then wait for the deploy to land.
   - Figma: choose embed, convert with AI or export with a plugin.
7. They land on `/sites/:id`, with the link row and Visit.
8. There is no next step pointing to "Test this site". There is also no sign that on the free plan the site stops serving after 7 days (`api/site.js:276, 325-334`).

### B. First test to first session watched
1. My Tests, then **New test**. The same CreateFlow opens, and "A published site" appears only if they already have a live site.
2. The draft is created on tile click, as above.
3. Tasks are optional. Finish.
4. They land on **Setup** (`UserTesting/createFlowActions.js:87,112,133`), not Share, even though setup is done.
5. Next they click the Share tab and copy the link. The **Export** button in the header also only copies the link (`UserTestingProject.js:239-245`).
6. A tester takes the test (flow C).
7. Back on the dashboard, clicking the test card always lands on **Setup** (bug B6), even when there are sessions.
8. Sessions tab, then a row, then the session detail page. Its order is: AI Insights, Task results, a "Watch Recording" button, audio, transcript.
9. **The video is not on the page.** "Watch Recording" goes to a separate `/session-review/...` route outside the Aero shell.
10. The Insights tab only builds cross-session insights when it is opened and two or more sessions are analysed. That can take up to a minute, and it fails silently (bug B3).

### C. Tester journey (`UserTestingTester`, `WelcomeFlow.js`)
1. The tester opens the link.
2. **Welcome** screen: "X invited you to test their design", the welcome message, and "N tasks · About N minutes". A free-exploration test shows "0 tasks · About 1 minute".
3. **Enable Audio**: "Enable Microphone" or "Continue without audio". A denied permission continues silently.
4. **Screen Recording**: "Share Screen" or "Skip". This step only appears when video is on and they are not on mobile.
5. **Think Out Loud** tips, then **Start Testing**.
6. The tasks panel runs over the prototype. After each task there is a difficulty rating (emoji scale).
7. **All Done!** with "Saving your session... please keep this tab open", then "You can close this tab now."

### D. Upgrade
- **Entry points:**
  - `AeroFeatureGate`, where a gated feature opens `AeroPricingModal` in place.
  - Settings, Billing & plans, "Choose a plan" or "Upgrade".
  - The demo's "Start Free Today".
- **Modal:** the title is "Upgrade your Aero account" and there are three plans, Basic, Solo and Pro, with a monthly/yearly toggle. Each plan lists "N test sessions with AI transcripts and notes". A footnote carries the two facts that matter most to a free user: "Free plan: 3 test sessions, and sites stay live for 7 days."
- **After that:** Stripe checkout, then back to Settings, which verifies the status. The session meter (`Account.js:295-320`) counts every session in every project with one read per project.
- **What's missing:** no in-context prompt tied to a real moment, such as "your site goes offline in 2 days" or "you have 1 of 3 sessions left".

---

## 2. Bugs found

| # | Symptom | Where | Cause | One-line fix | Status |
|---|---|---|---|---|---|
| B1 | `/user-testing/:id` is blank for about 3s | `UserTestingProject.js:113-115`; `hooks/useProjectData.js:94,107`; `layouts/AeroLayout.js:89-148` | The page returns `null` while loading. Before it, AeroLayout makes 3 reads in a row; after it, the project doc and then the synthesis doc are read in a row. `AeroSiteDetail.js:406-407` has the same `return null`. | Render the header and tab skeleton instead of `null`, and run the reads with `Promise.all`. | Verified |
| B2 | Landing directly on Share or Sessions shows "0 sessions" and "No sessions yet" | `hooks/useProjectData.js:151-179`; `tabs/UTSessionsTab.js:86`; `UserTestingProject.js:71` | The sessions listener is attached only after the project read, and `loading` flips to false (line 179) before the first snapshot arrives. In that gap `stats` is null, so the header and rail read 0, and the Sessions tab shows its empty state without checking `sessionsLoaded`. Setup only "shows 2" because by the time you look, the snapshot has landed. | Gate the counts and the empty state on `sessionsLoaded` (show a skeleton until then), and start the listener alongside the project read. | Cause verified. If the 0 never corrects itself, the listener is erroring (line 168 logs "Sessions listener error"): unverified. |
| B3 | Insights stuck on "Analyzing 2 sessions...", rail says "No sentiment yet" and "Themes appear after 2+ analysed sessions" | `tabs/UTInsightsTab.js:43-66`; `functions/index.js:1001-1141`; `UserTestingProject.js:142-143, 364-367` | **(a)** Synthesis is never triggered on the server. The per-session analysis (`index.js:567`) finishes and stops. The only trigger is a client-side `useEffect` that runs when someone opens Insights. So "analysed a day ago" still means no synthesis exists. **(b)** On failure the function *returns* `{success:false}` instead of throwing, and the client ignores the return value (line 43), so no error is ever shown. The text then flips to "ready to be generated". The "Analyzing" screenshot was taken during the call, which can run up to 60s. **(c)** It is not an off-by-one: client and server both use `>= 2` completed. The rail's themes text shows whenever no synthesis doc exists, whatever the count. **(d)** The sentiment card reads `synthesis.sentiment`, which the function never writes (`index.js:1112-1117`), so it can never fill. | Run synthesis on the server when the 2nd (and each later) analysis completes. Throw `HttpsError` and show the reason. Build the sentiment card from each session's `overall_sentiment`. | (a), (b) and (d) verified. Why this run failed (model or key) is unverified: check the function logs for "Synthesis failed". |
| B4 | The Insights tab will crash once synthesis succeeds | `tabs/UTInsightsTab.js:126-142, 200-202` vs `functions/index.js:974-986` | `contradictions` are objects `{topic, viewpoints}` but are rendered as `<li>{item}</li>`, which React refuses ("Objects are not valid as a React child"). There is no error boundary anywhere in `src/`, so the screen goes blank. Priority fixes also read `fix.priority` and `fix.description`, but the function writes `avg_severity` and no description, so every fix shows "L", a blank tag and no text. The legacy `CrossSessionInsights.js:184-230` reads the right fields. | Map the real fields (`avg_severity`, `topic`, `viewpoints`) and add a route-level error boundary. | Verified in code. Not seen live, because synthesis has never succeeded. |
| B5 | Insights never refresh after new sessions | `tabs/UTInsightsTab.js:55, 98-207` | The auto-run only fires when no synthesis exists, and the filled view has no "Update" action. | Re-run synthesis when the analysed count passes the stored `sessionCount`. Show "Based on N of M sessions". | Verified |
| B6 | Opening a test from the dashboard always lands on Setup | `UserTestingProject.js:74-82, 96-101` | The default tab is computed once, on first render, while `stats` is still null, so `sessionCount === 0` and the result is `'setup'`. `UTProjectIndexRedirect` is dead code, because the parent renders the tabs itself and never renders the index outlet. | Choose the default tab after `sessionsLoaded`, or link cards straight to `/sessions` when `sessionCount > 0`. | Verified |
| B7 | Lists full of "Draft / Setup not finished" with random names | `components/CreateFlow/CreateFlow.js:231-248`; `UserTesting/createFlowActions.js:42-47` | A draft doc is written as soon as a source tile is clicked, before any file, link or name. Closing the flow keeps it. Every look-around click leaves a card behind. | Only write a draft once there is real input (files dropped, link pasted or prompt copied). Auto-delete empty drafts after 7 days. | Verified |
| B8 | "Draft 0" pill while 5 draft cards show; drafts ignore filters | `UserTestingDashboard.js:155-160, 335-348` | The counts use `liveProjects` only, while drafts render above every filter, including Active and Completed. | Count drafts in the Draft pill, and show drafts only under All (collapsed) and Draft. | Verified (screenshot 01) |
| B9 | "Avg completion 0%" next to a card showing 20% | `UserTestingDashboard.js:139-141` vs `components/UTProjectRow.js:84-85` | These are two different metrics: task completion on the stat, sessions against target on the card. A test with no tasks always scores 0%. | Rename the stat to "Task success", and hide it when no test has tasks. | Verified |
| B10 | Header "Export" only copies the test link | `UserTestingProject.js:239-245` | The label doesn't match the action. | Make it a real export (CSV or PDF of findings) or remove it. | Verified |
| B11 | Session numbers run in reverse and change | `tabs/UTSessionDetailPage.js:844-846` | Sessions are ordered `startedAt desc`, so the newest is #1 and every new session renumbers the older ones. The list row calls the same session "Anonymous Tester" (`UTSessionRow.js:86`). | Number by start time ascending (stored once), and use the same label in the row and the detail page. | Verified |
| B12 | Session page rail says "No sentiment yet" while the session shows "Neutral" | `UserTestingProject.js:143, 301-325` | The rail is project-level and reads only synthesis (see B3d). | On a session page, show that session's data or hide the rail. | Verified (screenshot 07) |
| B13 | Free sites go offline after 7 days but the UI still says "Live" | `api/site.js:276, 325-334, 1128`; `AeroSites.js:545-547`; `AeroSiteDetail.js:581-583` | The serve path blocks expired free sites. The comment at `api/site.js:399` says the owner sees the expired status in the dashboard, but I found no expiry state in any Sites file. | Show "Offline: free plan ended" with an upgrade action on cards and on site detail, and a countdown from day 5. | Absence verified by search. Whether test links on an expired site also fail is unverified. |
| B14 | Session target "/ 10" on a free account that can keep 3 | `UserTestingProject.js:13, 158`; `components/Aero/AeroPricingModal.js:55` | The default target is 10, whatever the plan. | Default the target to the plan's limit, and show "2 of 3 on Free". | Verified |
| B15 | Tester sees "0 tasks · About 1 minute" on a free-exploration test | `components/UserTestingTester/WelcomeFlow.js:36, 141-149` | The meta row renders whatever the task count is. | Hide the meta row when there are no tasks, or say "Explore freely". | Verified |
| B16 | A tester who denies the mic gives a session with no transcript or insights, and the owner isn't told why | `WelcomeFlow.js:72-76, 183-185` | The permission error just moves to the next step. | Tell the tester what they lose, retry once, and tag the session "No audio" for the owner. | Verified for the tester side. The owner-side label is unverified. |
| B17 | Sites card: the slug and URL run together ("aero-large-upload-testaero-large-upload-test.ae...") | `AeroSites.js:565-579` | The CSS sets the slug to `display:block` (`AeroSites.css:476`), so something later probably overrides `.aero-test-card-meta`. The slug also repeats the URL. | Drop the slug line; the URL already contains it. | Seen in screenshot 09. CSS cause unverified. |

---

## 3. Page by page: top 3 each

### Dashboard (My Tests)
1. **Show real tests first.** Fold drafts into one quiet row ("3 unfinished, resume or clear") under All, and stop making empty ones (B7, B8).
2. **Make each card answer "is there anything new?"** Show "2 new sessions" or "Insights ready", and link straight to Sessions or Insights, not Setup (B6).
3. **Fix the header and stats.**
   - Header: "Record people using your prototype, watch the sessions and see what to fix." No "Figma", no "AI".
   - Drop or rename "Avg completion" (B9).
   - Remove the Refresh button; the data should be live.

### Test page tabs (Setup, Share, Sessions, Insights)
1. **No false zeros.** Skeleton until `sessionsLoaded` (B1, B2). Rename "Export", or make it export something (B10).
2. **Order by job, not by setup.** Once a test is live, Share and Sessions matter far more than Setup. After creation, land on Share with the link already copied and a "Send to 5 people" hint.
3. **Share tab:**
   - Show one link only. The header shows `duanesite.aeroapp.ai` while Share shows `aeroapp.ai/duanesite?test=1`, which reads like two different things.
   - Add a QR code and an "Open as a tester" preview.
   - State plainly what the tester will be asked for (mic, screen) and that sessions have no fixed length.

### Session detail
1. **Put the recording at the top, inline.** Today it is a button to another route outside the Aero shell. Watching is the core value.
2. **Link the transcript to the video.** Click a line to jump to that moment. Friction quotes should seek too.
3. **Name sessions consistently** (B11), show "Transcript arriving, usually about a minute" during processing, and hide the project-level rail here (B12).

### Insights
1. **Generate on the server, automatically** (B3). Show "Updated after session 3 · Based on 3 of 3 sessions" (B5), and email when ready if notifications are on.
2. **Fix the renderer before it ships** (B4). Lead with "What to fix first": priority fixes with severity and the quotes behind them, each linking to the session moment.
3. **With fewer than 2 sessions, don't show a dead end.** List each session's top issues now, and say "Patterns across sessions appear after the second one."

### Sites list
1. **Same draft clean-up as Tests** (B7). With 11 live and 8 drafts, the live sites are below the fold.
2. **Each card shows URL, last published, expiry on free (B13), and "Test this site".**
3. **Fix the header and the slug.**
   - Header: "Publish a prototype from a Figma link, an HTML upload or your AI agent." Today it says static HTML only, and it uses an em dash.
   - Remove the duplicate slug line (B17).

### Site detail
1. **Add a "Run a test on this site" action.** It's the bridge between the two products, and today it only exists in the other direction ("Manage in Sites").
2. **Replace the blank load with a skeleton** (`AeroSiteDetail.js:406-407`), and put a status line under the URL: "Live · published 2 days ago · offline in 5 days on Free".
3. **Rename the "Prototype" tab for Figma sites** to "Source", to match the test page's "Prototype source". Keep Versions for HTML, and add one-click roll back there if it isn't already obvious.

### Account and billing
1. **Put plan limits in plain view, not in a footnote.** "Free: 3 sessions kept at once, sites live for 7 days. Paid from $3 a month."
2. **Usage that matches what pages say.** "2 of 3 sessions kept" here, on the test rail (B14) and in the sidebar. The count now reads every project's sessions one by one (`Account.js:303-311`); store a counter instead.
3. **Show Account in the sidebar nav,** not only behind the avatar, and add a "What you get on Basic" line next to "Choose a plan".

### Tester screens
1. **Fewer steps.** Merge the mic and screen steps into one "Allow recording" step, which shows the tips at the same time. Four modal steps before the prototype is a lot.
2. **Be honest about privacy:** who sees the recording, how long it is kept, and how to stop. "Only this tab is recorded" is good; extend it. Handle a mic denial properly (B16).
3. **Copy and tone:**
   - Drop the emojis and "All Done!". Use "Thanks, you're done", British spelling and no "—".
   - Hide "0 tasks" (B15).
   - Remove the "About N minutes" estimate, since sessions have no fixed length.

### Empty states
1. **First-run Tests:** "Publish something first, or test a Figma link" with two buttons. Today it is a Figma-only message.
2. **First-run Sites:** three source tiles inline (Upload, Figma link, AI agent) instead of a lone button.
3. **Sessions and Insights:** say what happens next and when. "Share your link. Sessions appear here as testers finish; transcripts follow about a minute later." Never show an empty state while data is still loading (B2).

### Also: demo at `/demo/user-testing`
- It uses an "A" square logo where the app uses the "Aero." wordmark.
- It says "portfolio", "Get AI Insights" and "Our AI analyzes".
- It only demos testing, not publishing.
- Align the logo and wording with the app, and add a "publish in a minute" panel.

---

## 4. The 10 changes that matter most

Ranked by effect on a new user getting value (publish, share, watch) and on trust.

| Rank | Change | Effort |
|---|---|---|
| 1 | Run cross-session synthesis on the server after each analysis, surface failures, and fix the Insights renderer's field names and add an error boundary (B3, B4, B5) | M |
| 2 | Never show false zeros or blank pages: skeletons on first load, gate counts on `sessionsLoaded`, parallel reads (B1, B2) | S |
| 3 | Put the session recording inline at the top of session detail, with a transcript that seeks the video | M |
| 4 | Stop creating drafts on tile click; collapse and auto-expire empty drafts in both lists (B7, B8) | S |
| 5 | Show free-plan expiry and limits where they bite: "offline in N days" on sites, "2 of 3 sessions", correct targets (B13, B14) | M |
| 6 | Open tests where the action is: after creation land on Share with the link copied; from the dashboard land on Sessions or Insights when they have content (B6) | S |
| 7 | Join the two products: "Run a test on this site" on site detail and site cards, "Publish first" on the empty Tests page | S |
| 8 | Simplify the tester start to one permission step, with clear privacy text and proper handling of a denied mic (B15, B16) | M |
| 9 | Rewrite page headers and empty states to cover Figma, HTML and AI agents, without leading with "AI", in British spelling and without em dashes (dashboard, Sites, demo, pricing features) | S |
| 10 | Make labels and numbers honest: rename or remove "Export" and "Avg completion", give sessions stable numbers and one name, one share URL (B9, B10, B11) | S |

---

## 5. Copy notes

These follow the brand rule against leading with AI.

- **Dashboard header:** "Collect feedback on your Figma prototypes. Share a test link, review sessions, and surface AI-generated insights." becomes "Record people using your prototype. Watch the sessions and see what to fix first."
- **Sites header:** "Host static HTML sites on Aero. Drop a folder or .zip and it goes live on its own aeroapp.ai address — publish instantly or save a draft to publish later." becomes "Publish a prototype from a Figma link, an HTML upload or your AI agent. Each one gets its own aeroapp.ai address."
- **Section labels:** change "AI Insights" to "Findings", and "No AI insights yet" to "No findings yet".
- **Pricing features:** change "N test sessions with AI transcripts and notes" to "N recorded sessions with transcripts and notes".
- **Spelling:** "Analyzing" becomes "Analysing", and "Customize" becomes "Customise".
- **Tester screens:** remove the em dashes ("There are no right or wrong answers—we're testing the design, not you!", "Don't worry about being polished—just speak naturally!").
