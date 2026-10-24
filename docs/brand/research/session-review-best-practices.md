---
brand-sync: figmaApp docs/brand is the source. Copy this file unchanged to aero-landing-page/docs/brand/.
version: 2026-10-23.1
---

# Session review and cross-session analysis: what professional tools do

Research for Aero's session review and insights screens. October 2026. Checked against each tool's own help centre, docs or changelog where possible. Anything marked **(unverified)** comes from memory of the product or from secondary sources and was not confirmed in official docs during this pass.

Coverage note: EnjoyHQ is now part of UserTesting and has no independent product to study. Otter, Riverside and Descript are editing or meeting tools, useful only for transcript behaviour. Some help pages (Dovetail onboarding, Otter App Store, Contentsquare blog) could not be fetched.

---

## The 14 strongest patterns

| # | Pattern | Who does it |
|---|---|---|
| 1 | **Video left or centre, transcript in a right-hand panel with tabs** (Transcript, Notes, Clips, Info). Not below the video. | UserTesting, Lookback, Grain, Hotjar (Info/Actions), Frame.io (comments right) |
| 2 | **Click a transcript line or word to seek** the video there. | Grain, Condens (Ctrl+click a word), Lookback, Dovetail, HeyMarvin |
| 3 | **Follow-along transcript**: current word highlighted, panel auto-scrolls, a "Scroll to now" button after you scroll away. | Descript (current word), Circleback (all three); requested but not confirmed in Dovetail **(unverified)** |
| 4 | **Markers on the timeline** for tasks, notes, clips, sentiment and events, all clickable. | UserTesting (task starts, sentiment, smart tags), Lookback (task starts, findings), Hotjar and Clarity (rage clicks, errors, page visits) |
| 5 | **Highlight = clip**. Selecting transcript text creates a timestamped video clip that carries tags and a note. | Dovetail, Condens, HeyMarvin, Maze, Lookback (Findings), Great Question |
| 6 | **AI inline labels on the transcript**, not just one summary: short headlines per segment, positive/negative colouring. | Lookback (Eureka Headlines), Maze (green/red), UserTesting (sentiment and smart tags) |
| 7 | **Small, preset reaction sets** for marking moments, positive included, not only problems. | Hotjar (Bug, UI-UX issue, Confusion, Frustration, Success, Conversion), Userbrain (Usability issue, Confusion, Positive feedback, Behaviour, Suggestion), UserTesting (smart tags such as "easy", "confused") |
| 8 | **Theme with coverage count and clickable evidence**: each theme shows how many sessions it appears in, and each citation opens the exact moment. | Maze (session coverage %), Great Question (citation badges, hover for quote, click to open), Userbrain (ordered by how many testers) |
| 9 | **Confidence tied to sample size**. | Maze (low 1–4 sessions, medium 5–9, high 10+), Great Question (AI synthesis needs 3 interviews) |
| 10 | **Task-level quantitative block** before qualitative detail: success, misclicks, time, per-screen breakdown, path. | Maze, Lyssna, Useberry, UserTesting |
| 11 | **Summary that sorts the work**: "Screens to rework / to check / great". | Maze report |
| 12 | **Reels built automatically** from a tag or theme, exported as one MP4. | Dovetail (a reel per tag, MP4, up to 100 clips), Maze (theme reels), Great Question (highlight reel with quote count) |
| 13 | **Previous/next session shortcuts** so reviewers move through a study without returning to the list. | Clarity (play previous/next), Hotjar (Shift+P / Shift+N), Condens, Frame.io |
| 14 | **Speeds well above 2x and "skip inactivity"**. | Lookback 0.5–4x, UserTesting 9 speeds 0.5–4x, Hotjar up to 4x with skip inactivity, Clarity up to 12x with skip inactivity |

---

## 1. Single session review layout

**Video versus transcript.** The dominant layout is video in the centre or left, with a right sidebar of tabs.
- UserTesting: transcript, notes and clips are sidebar tabs on the right; the Study tab holds participant details; the timeline sits under the video with task-start markers and buttons for notes and clips.
- Lookback: canvas centre, timeline bottom, "Session Feed" on the right with Feed (notes, findings, AI insights) and Transcription tabs. A side-by-side option shows Feed and Transcription together, and the feed can be hidden to watch only the video.
- Grain: video top right, transcript as a tab, Summary tab is the default view. AI notes come first, video second.
- Hotjar: sidebar with Info and Actions tabs, toggled with **h**; clicking an action seeks.
- Frame.io V4: left navigation, centre player, right panel for comments; every panel can be collapsed for focus.
- Descript and Riverside put the editable script first, with the video as a preview. That suits editing, not review.

**Follow-along and seek.** Descript highlights the current word as it plays. Circleback added word highlighting, auto-scroll and a "Scroll to now" button (a good example of a small detail). Click-to-seek is universal (Grain lines, Condens Ctrl+click on a word, Hotjar actions list). Grain, HeyMarvin and Lookback have transcript search; HeyMarvin also lets you edit words and play one speaker only.

**Speed and shortcuts.** Frame.io sets the standard: Space and K play/pause, J/L shuttle back and forward at 1x, 2x, 4x, 8x, arrows step, C focuses the comment box and pauses, I/O mark a range, M mute, F fullscreen. Typing a comment pauses playback; submitting returns focus to the player. Condens: play/pause, 5 s back and forward, play from the text cursor. Most tools list shortcuts behind a "?" or settings icon rather than in the help text.

**Clips, notes and timestamps.** Notes are anchored to a timestamp and appear in the feed at that time (Lookback, UserTesting). A clip is a selection plus a tag plus an optional description (Condens, Dovetail). Dovetail adds a "Highlights only" tab above the player that plays just the highlighted parts, and can split long silences into "No audio" lines that can be tagged, which matters for screen tests where people go quiet.

**Task and event markers.** UserTesting and Lookback mark task starts on the timeline. Session replay tools add behavioural events: Clarity marks rage clicks, dead clicks, excessive scrolling, quick backs and JavaScript errors; Hotjar marks clicks, rage clicks, U-turns and survey answers; FullStory defines rage, dead and error clicks and "thrashed cursor". UserTesting puts sentiment markers (green and red) along the bottom of the player.

**Watching versus reading.** No tool reviewed has a named "reading mode", but three patterns cover it: Grain opens on the summary and puts the video in a corner; Lookback lets you hide the feed or show feed and transcript side by side; Frame.io collapses panels for focus. Picture-in-picture (Grain) keeps video visible while reading.

**Theme.** Frame.io V4 offers light and dark, built in LCH so media looks accurate on toned surfaces. Video-first editors (Frame.io, Descript, Riverside) are commonly dark by default; research repositories (Dovetail, Condens, Maze, Great Question) are light **(defaults unverified; not stated in docs)**.

## 2. Tags beyond "friction"

- Preset sets include positive outcomes: Hotjar has Success and Conversion beside Bug and Frustration. Userbrain groups AI insights into Usability issues, Confusion, Positive feedback, Behaviour and Suggestions. UserTesting's smart tags include "easy" as well as "confused".
- Sentiment is the most common second axis: Maze colours transcript lines green or red and tags themes positive or negative; UserTesting shows sentiment on the timeline and on path flows, sized by how many people felt it.
- Severity scales (for example 1 to 4, cosmetic to critical) were **not found in any official doc reviewed**. Teams appear to make them with custom tags (Dovetail custom tags need the Enterprise plan). Maze's three report bands (rework, check, great) are the closest built-in severity.
- Filtering by tag: UserTesting's smart tags can be switched on and off on the player and transcript; UserTesting's path filter filters by sentiment; Dovetail creates a reel per tag; Great Question regroups highlights by tag or participant.

## 3. Session lists

- Maze: each response row shows a tester ID, time on screen, clicks and misclicks. Testers are anonymous IDs.
- UserTesting: filter by participant, audience, completion date, test and technology; the player's Study tab shows date, duration, an ID, demographics, device and screener answers. Moderated sessions can carry an alias.
- Lookback: the participant types a name (a first name or alias is fine) and it becomes part of the session name, for example "SelfTest with ...". Project-level anonymisation renames everyone "Redacted Participant". No numbered default was found **(unverified)**.
- Userbrain: a tester overview summarises device, country, age and screener across testers.
- Clarity: device, location, clicks, page views, entry and exit URL, plus favourites and a rating.
- A quote or one-line AI summary per row, and severity counts per row, were **not confirmed in any list** reviewed. This is a gap Aero could fill.

## 4. Cross-session synthesis

**By task (quantitative).** Maze per mission: usability score (0 to 100 from success, time and misclicks; High 80+, Medium 50 to 80, Low under 50), direct success, unfinished, misclick rate, average duration, expected-path analysis, per-screen breakdown. Lyssna: success % plus count, average misclicks, average duration, common and individual paths, heatmaps, and success metrics only for those who reached the goal. Useberry: user flows with steps, clicks and time per screen. UserTesting: interactive path flows, sentiment path, intent path, click maps.

**By theme (qualitative).** Maze Analyze: highlights clustered by theme with session coverage %, key findings and sentiment; uncategorised highlights are left out of the report. Great Question: overview, then themes with citation badges counting quotes (hover shows the quote, click opens the transcript moment), then numbered key insights with a quote and date, then a reel with duration and quote count. Lookback separates the layers explicitly: sessions, then findings (clips as evidence, "not conclusions"), then themes, then reels. Condens and Great Question offer manual boards where highlights are dragged into groups, with AI "find similar".

**By question.** Maze summarises open questions with sentiment and selectable quotes. A view "by research question" across sessions was not found as a named feature **(unverified)**.

**Visualising many sessions.** Path or Sankey diagrams (Maze, UserTesting), heatmaps and click maps per screen (Maze, Lyssna, Useberry, UserTesting), affinity-style boards (Condens, Great Question). No tool reviewed shows a stacked timeline of all sessions side by side.

**Layering.** The common order is: one-paragraph summary, then metrics, then themes or issues ranked by how many people hit them, then quotes and clips, then the raw session. Maze's report has Summary and Full analysis; UserTesting's "Instant insights" cards open the related task.

## 5. Empty and first-run states

Weakest area of evidence. Confirmed: Maze builds a report automatically after the first tester and recommends 20+; Great Question's AI synthesis waits for 3 interviews; Maze's confidence label rises with session count; Dovetail recommends a pinned "Start here" doc and project templates that arrive with tags already set. A pre-filled sample project in Dovetail, Maze or Clarity was **not verified** in this pass (Dovetail's onboarding page could not be fetched).

## 6. Exports people expect

- Recording and transcript download: Maze, HeyMarvin (transcript as .docx), Grain (copy, download, or open in Claude or ChatGPT), Clarity share links.
- Reels as one rendered MP4: Dovetail (up to 100 clips, no subtitles burned in), Maze, Great Question.
- Reports: Maze link, embed and PDF (paid), single-slide share, presentation mode; Maze and Dovetail share links to a single highlight.
- Copy highlights as a table into FigJam or Sheets: Great Question.
- Heatmap images: Maze, Lyssna.

---

## What this means for Aero

Truth rules apply throughout: transcripts arrive after a session, no cursor in replays, example names labelled "Example".

### Session review layout
1. **Video left, transcript right**, as UserTesting, Lookback and Grain do. Right panel tabs: Summary, Transcript, Notes. Open on the summary when the transcript is ready, as Grain does, with a "Watch" view that widens the video and a "Read" view that shrinks it to a corner (picture-in-picture).
2. **Follow-along transcript**: highlight the current word or line, auto-scroll, and show "Back to now" once the reviewer scrolls away. Click any line to seek.
3. **One timeline under the video** with task starts, AI-flagged moments and the reviewer's clips as clickable markers. Click and rage-click markers only if Aero actually captures those events; otherwise leave them out rather than imply them **(check what the recorder captures)**.
4. **Keyboard**: Space and K, J and L for 10 s back and forward or shuttle, C to add a note (pauses playback), Shift+N and Shift+P for next and previous session, "?" for the list. Speeds 0.5x to 2x minimum, ideally to 4x, plus "Skip silence", borrowing Dovetail's long-silence idea for quiet testers.
5. **Light and dark**: keep the app light by default but give the player area its own darker surface token in both themes so the video reads clearly; in dark theme use the same surfaces as the rest of the app. Frame.io treats colour accuracy around media as the main concern.

### Tags and filters
6. **A small fixed set, positive included**: Issue, Confusion, Works well, Suggestion, plus an optional severity (Minor, Major, Critical) on issues only. No reviewed tool ships severity, so this is a differentiator; keep it to three levels. Colour the transcript lightly by tag, as Maze does with sentiment. Filter chips above the transcript and timeline hide everything except the chosen tag.

### Session list
7. Each row: participant name, device, duration, tasks completed (for example 3 of 4), issue counts by severity, and one line of AI summary or a quote. Ask the tester for a first name or nickname on the start screen, optional, as Lookback does; fall back to "Participant 3" in order of arrival, and allow renaming. Offer an "anonymise" switch like Lookback's.

### Cross-session analysis
8. **Layer it**: a short summary, then a per-task table (completion, time, where people got stuck), then issues ranked by how many sessions hit them shown as "4 of 6 sessions", each with playable quote clips. Every claim links to the exact moment, as Great Question's citation badges do. Show a confidence note under 5 sessions, as Maze does. Toggle between "By task" and "By theme"; skip heatmaps and path diagrams until Aero has click data.
9. Build a reel automatically for each issue and theme, exported as MP4.

### Empty states
10. Ship an **Example study** (made-up names labelled "Example") so a new user can open a finished session review and insights page before inviting anyone. On a real study, show what will appear and when: "Transcript and summary arrive about a minute after each session", "Patterns appear from 3 sessions". This copies Great Question's threshold and Maze's confidence label, and covers the gap left by every tool reviewed.

### Exports
11. Transcript (.txt or .docx), the session video, clips and reels as MP4, a shareable report link, and "Copy as table" for issues so they paste into FigJam or Sheets.

---

## Sources

- Lookback player: https://help.lookback.io/en/articles/4911701-the-new-lookback-player
- Lookback participant names: https://help.lookback.io/en/articles/5967019-does-my-participant-have-to-enter-their-name-and-email-address
- Lookback anonymise: https://blog.lookback.com/whats-new/anonymize-project-participants-and-sessions
- Lookback Headlines: https://help.lookback.io/en/articles/13455370-headlines
- Lookback sessions to findings: https://help.lookback.io/en/articles/13429122-from-sessions-to-findings
- Dovetail highlights: https://docs.dovetail.com/help/highlights
- Dovetail reels: https://docs.dovetail.com/help/highlight-reels
- Dovetail rollout guide: https://docs.dovetail.com/help/self-serve-onboarding
- Dovetail autoscroll request (not fetched): https://feedback.dovetail.com/feedback/p/autoscroll-transcript
- Maze AI-moderated analysis: https://help.maze.co/hc/en-us/articles/42231180695827
- Maze interview results: https://help.maze.co/hc/en-us/articles/20575413264019-Results-and-reporting-in-Maze-Interview-Studies
- Maze reports: https://help.maze.co/hc/en-us/articles/360052722693
- Maze heatmaps and paths: https://help.maze.co/hc/en-us/articles/360052722953
- UserTesting video player: https://help.usertesting.com/hc/articles/360000669697-Video-Player-Session-Replay
- UserTesting analytics: https://help.usertesting.com/hc/articles/11880400532509
- UserTesting videos page: https://help.usertesting.com/hc/en-us/articles/28679653304733
- UserTesting EnjoyHQ: https://help.usertesting.com/hc/en-us/sections/12573494676509-EnjoyHQ-Account-and-Resources
- Lyssna prototype tasks: https://help.lyssna.com/en/articles/5442240-prototype-task-sections
- Lyssna recordings: https://www.lyssna.com/blog/recordings-from-lyssna/
- Useberry features: https://intercom.help/useberry/en/articles/7959951-new-features
- Hotjar player: https://help.hotjar.com/hc/en-us/articles/36820025895697-Recordings-Player-Guide
- Clarity player: https://learn.microsoft.com/en-us/clarity/inline-player
- Clarity Copilot: https://clarity.microsoft.com/blog/microsoft-claritys-copilot-ai-driven-session-replays/
- FullStory frustration signals: https://help.fullstory.com/hc/en-us/articles/360020624154
- Grain recording page: https://support.grain.com/en/articles/9232495-recording-page
- HeyMarvin annotate: https://help.heymarvin.com/en/articles/10130418-annotate-and-analyze-files
- Condens shortcuts: https://condens.io/help/tips-and-shortcuts/general/list-of-shortcuts
- Condens clips and reels: https://condens.io/help/using-condens/structuring-and-analyzing/creating-video-clips-and-highlight-reels
- Great Question synthesis: https://greatquestion.co/support/repository/synthesis.md
- Userbrain AI insights: https://www.userbrain.com/blog/ai-insights-instantly-uncover-key-insights-and-patterns-across-your-user-tests/
- Listen Labs: https://listenlabs.ai/use-case/usability-testing
- Outset usability: https://help.outset.ai/en/articles/11147152-intro-to-usability-studies-video
- Descript playback: https://help.descript.com/hc/en-us/articles/10164534109837
- Descript editor: https://help.descript.com/hc/en-us/articles/37585546799757
- Riverside editor: https://riverside.com/blog/new-ai-editor
- Frame.io shortcuts: https://help.frame.io/en/articles/7785-keyboard-shortcuts
- Frame.io V4 design: https://blog.frame.io/2024/05/21/frame-io-v4-web-app-beta-feature-focus-new-design-smooth-navigation/
- Frame.io V4 player: https://blog.frame.io/2024/05/28/frame-io-v4-features-player-and-commenting/
- Circleback transcript update: https://circleback.ai/releases/transcript-tab-updates
