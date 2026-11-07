---
brand-sync: figmaApp docs/brand is the source. Copy this file unchanged to aero-landing-page/docs/brand/.
version: 2026-11-07.1
---

# How we redesigned Aero, start to end

Written 7 Nov 2026 from the repos (figmaApp, aero-landing-page, heybooking), the PR history, the session transcript and helper briefs, Duane's feedback files, the research folder and past chats. It records the Aero rebrand and redesign (21 Oct to 6 Nov 2026) so the process can be run again on another product, and compares it with HeyBooking's run.

Rules used here: only what is recorded is written down. Where something was not recorded, it says "not recorded". Times are UTC unless marked; Duane was in Seattle (UTC-7, then UTC-8 from 1 Nov). `DECISIONS.md` dates follow Duane's day in Seattle, so the 24 and 25 Oct rows below use those dates and can sit a day earlier than the UTC times of the same work.

**A note on sources.** The working session was compacted several times. Duane's messages before 26 Oct 02:21 survive only in places: verbatim for 22 Oct (10:06 to 15:57) and his attached feedback files, and as summaries in `research/conversation-audit.md` and the compaction summaries. So some prompts below are whole and some are fragments; each says which.

**Who did what.** "Duane" is the founder. "Claude" is the lead Claude Code session (one long cloud session). "Helpers" are Claude sub-agents briefed as named roles (brand designer, copywriter, animator, UI engineer and so on). "Reviewer" is a helper told to critique without seeing the lead's opinions. Boards were published as private claude.ai artifacts; from 5 Nov a Claude Design canvas was used. Claude in Chrome was used for console steps in Duane's browser. From 26 Oct helpers ran on Sonnet by default (Duane's ask, to save tokens); which model ran the helpers before that is not recorded.

---

## Step 0. What changed from the HeyBooking playbook and from the earlier Aero prompt, and why

### What existed before this document
- **HeyBooking playbook** (`heybooking/docs/brand/PLAYBOOK.md`, last changed 25 Oct UTC): research, strategy, art direction, logo, copy/UX/UI/motion passes, illustration (the Animator's card kit), SEO, "make it automatic". Its "Repeating this on another product" prompt asks the next product to "Keep a PLAYBOOK of what you did differently".
- **The earlier Aero prompt.** Duane's kickoff on 22 Oct asked to run the HeyBooking process on Aero and "lets align on the plan but do exactly the same things", noting what differed in Aero's own playbook. The full text was lost in compaction (only these fragments survive, in `research/conversation-audit.md`). No other Aero process prompt was found. The companion file `prompts/heybooking-process-playbook-prompt.md` named in this task's prompt was not found in any repo here.
- **Aero's own playbook** (`docs/brand/PLAYBOOK.md`, version 2026-10-23.5) and the running notes behind it (`/home/claude/research/playbook-notes.md`). They stop at 23 Oct.
- `DECISIONS.md` (version 2026-11-06.1), `BRAND.md` and `TONE_OF_VOICE.md` (2026-10-23.1), `DESIGN_SYSTEM_PLAN.md` (2026-10-23.1), `PRICING-FACTS.md` (2026-10-25.1), `docs/TODO.md`, the `/aero` style guide (AeroShowcase) and `src/components/Aero/DESIGN_SYSTEM.md`.

### Added (not in the HeyBooking playbook)
- **Repair before rebrand.** The product was broken (no transcripts or insights), so 21 Oct went on fixing it (#259, #260, #261). Why: no point selling a loop that didn't work.
- **Align first, with multiple-choice questions** in batches of up to four, each with a recommended option. Why: faster than open questions.
- **Parallel research helpers** (code inventory, competitors and SEO, past decisions), with their claims checked before use.
- **A facts file for plans** (`PRICING-FACTS.md`). Why: three of four round 5 teams invented plan features without one.
- **Truth rules** written into both CLAUDE.md files: no live-typing transcripts, no cursor in replays, example names labelled, other tools' UI kept separate, no stock photos of people.
- **A decisions log** (`DECISIONS.md`), newest first, never deleted, struck through when replaced. HeyBooking kept `REDESIGN_TRACKER.md` and `APP_REDESIGN_DECISIONS.md` instead.
- **Two repos, one design system**, with a `version:` header on every synced file and twin PRs.
- **A glass lab and then a glass control panel** where Duane set each effect himself; then one settings file for the glass.
- **An independent reviewer** before decisions and before go-live (round 5 critique, review R8).
- **A questions page** with a picture per question and one-tap answers saved for Claude (16 answered "in a few minutes").
- **A UI directions stage**: every main screen drawn in every direction before detailed components (the missing step, found 23 Oct).
- **A feature parity rule**: everything the website and hero video show must exist in the app, so missing features were built (25 Oct).
- **A real user test** (Emily, 30 Oct, moderated by Duane) fed into the final design round.
- **Design on a canvas built from live code** (5 to 6 Nov) after a canvas drawn from the mockup kit drifted from the real app.

### Dropped
- **Country pages.** HeyBooking had /hk and /ph. Aero's buyers are international and search by task, so the SEO unit is the task page.
- **The card kit** (HeyBooking's Animator feature cards). Still "to do" for Aero; the hero video took its place on the homepage. Not built as of 6 Nov.
- **PRODUCT.md and CHANGELOG.md.** HeyBooking generates its site from these. Aero has neither; `DECISIONS.md` and `PRICING-FACTS.md` play part of that role. The conversation audit (23 Oct) lists them as not done; nothing since says otherwise.
- **The emails pass.** HeyBooking did "now vs suggested" for every email. For Aero: not recorded.

### Reordered
- **Five art direction rounds instead of one**, and brand before page looks (round 1 skipped the brand and was rejected).
- **UI first, then the website** (decided 23 Oct). HeyBooking did the website first and aligned the app afterwards in seven rounds.
- **In practice the UI boards and the homepage were designed on the same day** (23 Oct), the website went live (26 Oct 00:34) before the real app was rebuilt (26 Oct onwards), and the app was then built to match the website's video. See part 7.

### What was learned (added to what the Aero playbook already lists)
- Check system-font logos on a machine that has the font.
- Stock photos read as fake for this product.
- Liquid glass only reads over detailed content.
- Helpers sharing a scratch folder overwrite each other's files.
- Draw every main screen in every direction before components.
- Boards drawn from a mockup kit drift from the shipped app; snapshot the real code instead (5 Nov).
- A marketing video that is a copy of the UI must be updated by hand when the UI changes (6 Nov, LP #32).
- The video's Insights design ended up cleaner than the app's, and the app was changed to match it (6 Nov).

### Things in the existing docs that are now wrong or stale
These were found while writing this. They are listed here, not edited; this piece of work changes no other file.
- `PLAYBOOK.md` status table stops at 23 Oct ("hero A or B to pick", "SEO pages to build later"). Since then: the site went live (LP #7), the app was rebuilt (#267 onwards) and 20 SEO task pages shipped (LP #29).
- `PLAYBOOK.md` says round 4 had "a 25-typeface study"; the conversation audit and running notes say 14 typefaces. Which is right is not recorded.
- `BRAND.md` (23 Oct) still calls the palette "working, not final"; the v3 tokens shipped on 26 Oct (#267, #270). Logo refinement and dot motion are still listed as to do; whether they were done is not recorded.
- `DESIGN_SYSTEM_PLAN.md` describes a demo mode (`/kit` routes in the app) that the marketing pieces would be built from. No `/kit` route exists in figmaApp. The hero video is a separate HTML copy (see part 11).
- `docs/TODO.md` still lists as waiting: merging #262, #263 and LP #5 (merged 26 Oct), the brand folder PRs #264 and LP #6 (merged 26 Oct), and the Node 22 PR #265 (merged 26 Oct).

---

## 1. Timeline

| When (UTC) | What | Who or what |
|---|---|---|
| Feb 2026 | Figma refused a plugin listing because "Figmafolio" contains "Figma" (trademark rules: no "Figma" or "Fig" in product names). A new parent brand was explored; Aero emerged as the brand that month. | Duane, claude.ai chats (12 and 19 Feb) |
| Jun 2026 | aero-landing-page made from a copy of figmafolio-landing-page and re-skinned to the app's look then ("Aero." in Georgia, steel blue #3D78B0, Inter) (LP #1 to #4). | Duane, Cowork, Claude Code |
| Jul 2026 | Earlier decisions: the headline "Publish prototypes and run real user tests" and "AI as a quiet helper". They had drifted on the live site by October. | Recorded in the strategy dossier |
| 21 Oct | Repair: Figma test fixes (#259), AI back on OpenRouter with fallbacks (#260), one transcription per session (#261, merged 22 Oct 02:04). | Claude, Duane approving each merge |
| 22 Oct, before 08:38 | Kickoff: run the HeyBooking process on Aero; alignment answers (full re-think, research decides, international, stop at each pick). | Duane |
| 22 Oct 08:38 | Three research helpers: feature inventory from code, competitors and SEO, past decisions. Live site captured. | Helpers, Claude |
| 22 Oct 08:40 to 09:19 | Research and strategy doc (Claude Doc); 10 strategy decisions answered. | Claude, Duane |
| 22 Oct 09:19 | "Fix soon" truth fixes as separate PRs (#262, #263, LP #5; merged 26 Oct). | Helper |
| 22 Oct, before 09:39 | Round 1, five moodboard directions: rejected. | Claude, Duane |
| 22 Oct 09:39 to 10:22 | Round 2, brand first: reference analysis of 28 sites, five logo systems drawn as outlines, copy per direction, caustic glass button. "Full stop" added at Duane's ask (10:06). | Brand researcher, brand designer, copywriter, animator helpers |
| 22 Oct 10:22 to 14:20 | Round 3: six directions, each led by one reference (Claude, Cursor, Linear, OpenAI, Figma, Nothing), each its own layout; glass v2. | Helpers |
| 22 Oct 14:20 to 15:30 | Round 4 (Full stop combinations and a font study); glass button lab V1 to V5; app UX review. V3 glass picked at 15:30. | Helpers, Duane |
| 22 Oct 15:07 to 15:57 | Round 5: one creative brief, four design teams (A Studio, B Colour, C Story, D Replay), each a homepage, app screens, a content page and an MP4 animation; independent critique; fix round; back and close navigation added. | Four team helpers, reviewer |
| 23 Oct 01:47 | Duane's round 5 feedback file: UI first, one shared design system, marketing components from real components, save everything, audit the conversation. | Duane |
| 23 Oct 01:48 to 02:01 | Conversation audit; `docs/brand/` folder, decisions log, design system plan and CLAUDE.md rules (#264, LP #6). | Claude, helper |
| 23 Oct 02:02 to 08:33 | App UI round (designer app, tester flow); UI directions stage (every screen in A to D); buttons in situ; research on pro session review tools; app UI v2 (two teams); questions page; app UI v3 (two teams). Cursor recording investigation. | Helpers, Duane answering |
| 23 Oct 08:33 and 10:00 | Homepage round on the v3 UI, then a rework on round 5 A's structure. | Helpers |
| 24 Oct | Duane's feedback on the homepage rework (file). Proposition research (competitor copy, like-for-like pricing, pain points). Website round 4 (Team H homepage and hero video, Team S other pages). Glass hover lab. Feedback on round 4 (evening). | Duane, helpers |
| 25 Oct | Website round 5, glass control panel, rounds 6 and 7, Features page rework, final review by a team of roles (review R8), rounds 8 and 9. Glass final. Go-live decided. | Helpers, reviewer, Duane |
| 26 Oct 00:34 | New website live: LP #7 merged with figmaApp #266 (routes for /use-cases and /guides). Favicon and centred buttons (#8 to #10, #268, #269). | UI engineer helper, Claude merging after Duane's yes |
| 26 Oct 01:22 to 27 Oct 05:18 | App rebuilt on v3 in phases: tokens and glass (#267), shell and Home (#270), Sites (#271), snapshots (#272, #274, #276), New site (#273), Tests (#275), Insights (#277, #278), tester (#279, #281), review (#280), demo parity (#282), visitor pages (#284), settings (#285), test copy (#286), states (#287), test page (#288), onboarding popup (#289), one-tab tests (#290), Figma connect (#291) and follow-ups to #298. Parity audit 26 Oct 03:52. | Helpers per phase, Claude, Duane merging |
| 27 to 29 Oct | Pages round board (#299, not merged); tester panel (#302); admin session review (#301). | Helpers |
| 30 Oct | User test with Emily (47 minutes, Central Market, Hong Kong). | Duane moderating |
| 3 to 5 Nov | Free plan rules (#306); Figma link check and breakpoints (#307 to #313); handoff screens and recording pill (#319, #320). Tester round, upsell round and pages build PRs (#321 to #325, not merged). Emily's feedback processed (5 Nov). | Helpers, Duane |
| 5 Nov | Claude Design canvas: round 1 (drawn from the mockup kit) rejected; round 2 redone by snapshotting live code; round 3. | Helpers on the canvas, Duane |
| 6 Nov | Canvas rounds 4 and 5 (voice note review); "implement all of this now": tester (#330), Sites (#331), Tests and Insights (#332), review (#333), Convert with AI (#335), follow-ups (#337), recording in pieces behind a flag (#338), tabs and delete modal (#340). Website: homepage copy and new hero sequence (LP #28), 20 SEO task pages (LP #29), "How findings are made" (LP #30). Hero video refreshed to the shipped UI (LP #32, 17:13 to 17:29). Decisions and TODO (#336, LP #31). | Helpers, Claude, Duane merging |
| 7 Nov | This document. | Claude |

---

## 2. The prompts that started each stage

Verbatim where recorded. Long ones are in the appendix. Spelling is Duane's own.

| Stage | Date | Prompt | Status |
|---|---|---|---|
| Repair | 21 Oct | "lets align first ask me any questions, then i want you to work on this" | Fragment (voice-note prompt; the rest not recorded) |
| Rebrand kickoff | 22 Oct | "it worked i see ... next" ... "lets align on the plan but do exactly the same things" | Fragments; full text not recorded |
| Research doc reply | 22 Oct | "ask me them now but give me options and tell me which you recommend"; "keep doing these"; "mcp is not a moat but i do think ours is so simple" | Fragments |
| Round 1 rejected, round 2 started | 22 Oct, before 09:39 | "present brand, logo a bit of the home page first" | Fragment |
| Logo from the existing mark | 22 Oct 10:06 | "cotninue, but i think we sohuld have a logo option base don our existing .A or whatever it is too.... but jsut flesh that our more how does htat look liek as a brand etc... keep doing..." | Verbatim |
| Round 3 | 22 Oct 10:22 | Appendix A1 | Verbatim |
| Round 4 and glass lab | 22 Oct 14:20 | Appendix A2 | Verbatim |
| Glass colours | 22 Oct 14:42 | "the glass button lab is itneresting... cna you try differnt colour buttons as well lie not just black , maybe basedo n the desing optinos as thats laso the most extrmee as black cant reflecct so maybe true a trnaslusent black etc ok?" | Verbatim |
| Glass done properly | 22 Oct 14:47 | "but i didnt think liquid class look very liquid glass a re you sure you impelemnted it the best way liek you foudn a futitorial online on how its done, otherwise continue" | Verbatim |
| Round 5 mockups | 22 Oct 14:58 | Appendix A3 | Verbatim |
| Glass pick | 22 Oct 15:30 | "wait i like V3 From researchSnell-law capsule refraction, Fresnel edge reflection, key-light specular. so mabye intergreat that, whther its roudned pill or roudned rectangle depends o n the diesngs... otherwise continue" | Verbatim |
| UI first and the design system | 23 Oct 01:47 | Appendix A4 (attached file "Aero feedback") | Verbatim |
| App UI rounds, directions, v2, v3 | 23 Oct | Not recorded verbatim; the answers are in DECISIONS.md, 23 Oct sections | Not recorded |
| Homepage rework round | 24 Oct | Appendix A5 (attached file "Aero Feedback") | Verbatim |
| Go live | 25 Oct | "implement this right away, make the necessary changes and go live, but make it in such a way decisions are recorded and we can change it later." | Verbatim, as quoted in the builder's brief |
| Feature parity | 26 Oct 03:51 | "...did you do all the UI for thesessions / analysis, thougth there isa lot to do there comapred withour mcoks and product demo (the hero video) i want to make sure there is feature parity between what we dhow and the actual app" | Verbatim (extract) |
| Canvas round 2 | 5 Nov | Appendix A6 (attached file "Aero feedback 2") | Verbatim |
| Canvas round 4 | 6 Nov | A 25-minute voice note; a summary and the raw transcript are in Duane's attachment `ui-ux-review-voice-note-6-11-2026.md` | Summary in this repo's briefs only |
| Implementation | 6 Nov | "the reason i was giving feedback on all the ui is i want you do implement that ui, got it?" | As quoted in the compaction summary |
| Hero video refresh | 6 Nov | "yes upadate the video to show the updated ui please"; the helper brief is Appendix A7 | Duane's line as quoted in the compaction summary; brief verbatim |
| This document | 7 Nov | Appendix A8 | Verbatim |

HeyBooking's kickoff prompt is in its own playbook, Step 0.

---

## 3. Research

### What was searched and read
- **The code** (feature inventory helper, 22 Oct). It found that Privacy and Terms were blank; confirmed headlessly.
- **Past decisions** in project docs and past chats (helper used past-chat search, because helpers could not open project docs).
- **The live site**, captured as text (`research/live/`): aeroapp.ai, pricing, how it works, the blog, the app and the demo.
- **Competitors and SEO**: Maze, Lyssna, Userbrain, UserTesting, Ballpark, Outset, tiiny.host, Static.app, Vercel, Figma Sites, Lovable, v0. Output: `research/strategy-dossier.md`.
- **An empirical check**: which AI builders allow their output to be framed (lovable.dev, claude.ai, bolt and v0 block it). It became SEO page ideas.
- **28 reference sites** designers respect (Linear, OpenAI, Claude, Figma, xAI, SpaceX, Cursor, Vercel, Raycast, Arc, Nothing, Stripe, Notion, Framer and others), with a current versus dated list (`research/reference-analysis.md`).
- **Liquid glass techniques** online, including the liquid-glass-react library (V5 benchmark; licence kept in `glass/src/`). Notes in `glass/RESEARCH.md`.
- **The live logo font**, rendered in Duane's own browser: today's logo was Georgia 400.
- **How pro tools lay out session review** (Lookback, UserTesting, Grain, Frame.io and others; `research/session-review-best-practices.md`).
- **Whether tab recordings can show the cursor** (`research/cursor-recording.md`): they can't; options listed.
- **Proposition research** (24 Oct): competitor copy, like-for-like self-serve pricing, pain points from forums, archetypes (`research/proposition-research.md`).
- **A parity audit** of what the website and video show versus the app (26 Oct, `research/app-v3/PARITY.md`).
- **A user test** with Emily, a UX designer who runs tests on UserZoom (30 Oct).

### Research that changed a decision
| Research | Decision it changed |
|---|---|
| Past decisions (July headline, never lead with AI) | Kept, not re-asked; the drift was named as a problem to fix |
| Dossier: cheap self-serve testing is gone, nobody joins hosting and testing | Homepage leads with the loop (publish, then test on the same link) |
| Code inventory: blank legal pages, placeholder FAQ, wrong limits | Split out as "fix soon" PRs, shipped before the rebrand |
| Reference analysis | Round 3 rebuilt each option on one named reference |
| Font check in Duane's browser | An earlier comparison had silently used another serif; led to the font study and to Geist |
| Liquid glass research | V3 picked; Subtle by default, Liquid only over imagery |
| Pro session review tools | Settled the review layout questions quickly |
| Cursor investigation | Rule: no moving cursor in any replay until cursor tracking ships |
| Proposition research | Round 4 copy; price comparison per month with Maze |
| Parity audit | Build the missing features rather than hide them (25 Oct) |
| Emily's test | Fed into: the new hero line (LP #28), "Allow recording" permission card, skip silence that shortens the timeline, editable labels, Visit site as the main button (6 Nov) |

---

## 4. Decisions

The full log is `DECISIONS.md`. The main forks:

| Topic | Options shown | Chosen | Why |
|---|---|---|---|
| Lead message | Several proposition lines | The loop: publish, then test on the same link (22 Oct); hero later "From an idea you had today / to findings for your team." with the rotating "Publish your [Claude artifact / Figma prototype / Lovable app / HTML site]" (6 Nov) | Research gap; Emily said the old homepage didn't say what Aero does |
| Logo | Round 1 to 4 systems (Timecode, Contrail, Redline, Cobalt, Index, Daylight, Afterglow, Studio, Full stop, Dot and others) | "Aero." in Geist 500 with the blue dot (#3478F6) | Full stop "looks expensive"; "defintiely liek the dot"; "I like the logo for A studio really" |
| Direction | A Studio, B Colour, C Story, D Replay | A Studio as base, a little of B's clarity and C's context | "feels like Figma, which isn't bad"; B "a bit too much" |
| Steps | Publish, Watch, Read; others | Publish, Test, Review | "Read" is wrong because you can watch; the session is already summarised |
| Step colours | One blue; three colours | Publish blue, Test green, Review orange (24 Oct) | Clearer per section |
| Buttons | Caustic v1, glass v2, lab V1 to V5 | V3 glass, then one final glass from the control panel (25 Oct) | Picks up nearby colour subtly, like his original engine |
| Website theme | Light, dark (Afterglow) | Light only; the app may have dark mode (session review dark) | "unsur eof dark mode websites" |
| Imagery | Stock photos, illustration, real UI | Real UI and illustration; no stock photos of people | Stock "look a bit fake" |
| Order | Website first, UI first, both | UI first (23 Oct) | "the UI is shared with the marketing website" |
| Design system home | figmaApp, separate repo, copies | figmaApp is the source, copies in aero-landing-page with versions | One system, two repos |
| Hero video | One calm screen; a session replay; three steps | Three steps with a progress bar; later no WhatsApp and no cursor (6 Nov) | See part 11 |
| Homepage pricing | Own plans; competitor table | Competitor table (24 Oct), then four short plan cards with the table on the pricing page (6 Nov) | Simpler homepage |
| SEO unit | Country pages; task pages | Task pages, built from one template (LP #29) | Buyers search by task |
| App structure | Sites and Tests merged or separate | Separate; "Test this site" makes a real copy | Combining was more confusing |
| Counts and labels (6 Nov) | Dots, pills, "new" words, squares | A muted square with a mono number; bare label icons | Too much colour and too many tags (voice note, 6 Nov) |

### Likes, dislikes and corrections (Duane)
- **Liked:** the Full stop logo and its dot; the pocket.aeroapp.ai window; Precision's dark angled window; Plain's colour-wash cards; A Studio's app view; D Replay's animated app and the progress line; C Story's voice highlight; "One prompt and it's live." ("a great sentence"), "Made for people who make things.", "In their own words.", "From prompt to first session."; the publish part of the hero video ("the best bit"); the video overall ("really cool", "the video is better now").
- **Disliked:** Timecode ("too audio software"), Contrail ("looks like airline"), Redline ("looks like a wireframe"), Index ("looks like atrain"), Dot ("didnt like at all"); everything "too space related"; options "mashed together"; caustic buttons "too much"; glass that didn't look liquid; Studio's sticky note ("forced") and too-elegant serif; headlines too bold; cursor name tags; stock photos; dark websites; "Live in minutes, however you made it" ("vey ai cliche") and its graphic mixing Aero's and Claude's UI; "Watch people use it" ("sounds weoird"); too many gradients (Features, How findings); the AI-sounding "it's not X, it's Y"; thumbnails by titles; the dropdown's left bar ("very ai").
- **Corrections:** the transcript isn't live; testers' mouse isn't recorded; don't use his name in mockups; sessions have no fixed length (no "10 minute session"); the website and app must match ("feature parity"); the canvas must match the live code and style guide ("its not effecting what’s in the app unless you are purposely changing it .. , if you are then you should discuss with me first"); the hero was too slow in one round and too fast in another; previews shouldn't be a customer setting.

---

## 5. What worked and what did not

### Worked
- Repairing first, then aligning with recommended options.
- Brand before page looks (round 2 onwards).
- One reference per option, each with its own layout (round 3).
- Full mockups by parallel teams from one brief, then an independent reviewer and a fix round (round 5). "Far stronger" than mashing liked parts together.
- A facts file and truth rules given to every helper.
- The glass control panel: Duane set the look himself, saved as one settings file.
- The questions page with one-tap answers.
- Building the website on one copy block per page and one glass settings file, so words and glass change without a rebuild.
- Phased app PRs, one per area, each with the `/aero` style guide updated.
- Snapshotting live code into the canvas (5 Nov round 2 onwards).
- Recording decisions in the repo as they were made.

### Did not work, and the back and forth
- **Round 1** moodboards skipped the brand: rejected.
- **Round 4** combinations were "mashed together", not rethought.
- **Glass:** caustic too strong, then not liquid enough, then too strong again on washes, then hover too obvious ("too obvious and crazy"), then too subtle. Settled on 25 Oct after the control panel.
- **Typography check:** the container lacked Georgia, so an early comparison silently used another serif.
- **Stock photos** read as fake; three of four teams invented plans.
- **Jumping from liked mockups straight to detailed app UI** missed a step (UI directions), found on 23 Oct.
- **Hero video pace:** round 2 "very slow and doesn't show much"; later rounds a bit too fast; specific beats too quick ("User test this site", pasting into Claude). See part 11.
- **Website showed unbuilt features** (tester first name, word highlight, Private, "Taking new sessions", free Preview runs). Hidden with `data-soon` before go-live, then built (25 Oct onwards).
- **Canvas round 1 (5 Nov)** was drawn from the mockup kit and drifted from the app and the live homepage: Duane was unhappy; redone by copying live code.
- **Broken boards:** blank canvas boards from malformed markup; a broken Test section loop and collapsing section loops in website rounds; all fixed.
- **Process friction:** helpers overwrote each other's scripts; GitHub GraphQL was blocked (REST only); draft PRs could not be marked ready (closed and reopened); merges always waited for Duane's explicit yes.

---

## 6. How the design system was built, and how website, app and illustrations were kept in step

1. **Boards first (22 to 23 Oct).** Static HTML boards generated by Python build scripts, all sharing one stylesheet per round (`app-ui-v2/shared/aero.css`, then `app-ui-v3/shared/aero.css`), with the V3 glass script and the logo SVGs. Light and dark.
2. **Website mockups built from the board stylesheets (23 to 25 Oct).** Each homepage round copied the v3 stylesheet and drew "real components" (the board's components, at their own size, scaled to fit). All words lived in one JSON block per page.
3. **Glass as one component and one settings file** (`glass-v3.js` reads only `glass-settings.js`; `website-v7/shared/GLASS.md`).
4. **Website live (26 Oct)** in Astro: copy in `src/data/copy/*.json`, glass in `src/glass/glass-settings.js`, tokens in `src/styles/website/aero.css`.
5. **App tokens and components (26 Oct, #267, #270).** A v3 token block was added to `src/styles/aero-design-system.css`, then the old `--aero-*` tokens were turned into aliases of it (accent to #3478F6, font to Geist), so every screen changed at once. The website's glass engine was ported into the app (`glassV3/`, `GlassButtonV3`) with one `glassSettings.js` mirroring the site's file. New components went into `/aero`.
6. **Parity both ways (25 Oct onwards).** Anything the website or video showed had to exist in the app, and was built (#277 to #289). The onboarding popup's video (#289) was recorded frame by frame from the website's own hero loop.
7. **Canvas from live code (5 to 6 Nov).** Boards were made by snapshotting the real rendered DOM of the app and site with Playwright, linking the live CSS as canvas assets, and marking each change with a numbered note. Shared rules for counts and labels lived in one file (SYSTEM-R4).
8. **Implementation from the boards (6 Nov),** with the app's own components and tokens only, every new component added to `/aero`.
9. **Sync.** `docs/brand/**` files carry a `version:` header and go to aero-landing-page in a twin PR (for example LP #11 to #23, #31).

**How "built from the real components" held up.** The plan (`DESIGN_SYSTEM_PLAN.md`) was a demo mode in the app (`/kit` routes) that the website, videos and illustrations would render. That was not built. In practice the website and hero video are hand-written HTML and CSS that copy the app's design (first the v3 board stylesheet, from 6 Nov the shipped app's shapes and token values in `hero-new.css`). They follow the real product UI, because the app was built to match them and then they were updated to match the app, but they are copies. Keeping them in step is a manual step (LP #32). The website mirrors only about 14 `--aero-*` tokens (TODO audit). Illustrations: no card kit or separate illustration set was built; the guides use real UI pieces.

---

## 7. Order of work: the new UI and the home page at the same time

**What happened.** On 23 Oct Duane decided "UI first, then the website". The same day the app UI was designed in boards (app UI round, directions, v2, v3), and a homepage round was built on the v3 boards that evening. The website went through rounds 4 to 9 on 24 to 25 Oct and went live on 26 Oct 00:34. The real app was rebuilt from 26 Oct 01:22, after the website was live. So the UI design came first by hours, the homepage followed on the same design, and the real app came last.

**Why.** Duane: "the UI is shared with the marketing website", and "great UI but it’s not real which makes me think we need tow work on the UI last the same time as the website."

**Did it help?**
- Helped: one visual language from the start; the homepage's real-looking screens sold the product clearly; the video became the spec the app was built to (25 Oct parity rule) and in places beat the app (6 Nov: "the isnights pade from the video is sitll cleaner so pelase just use that").
- Hurt: the website showed features the app didn't have, so they had to be hidden before go-live and then built in a rush; the boards and the shipped app drifted (5 Nov canvas round 1 was rejected for this); the hero video had to be redone when the app changed (6 Nov, LP #32).
- Net: helped for speed and consistency, at the cost of truth risk and rework. A demo mode built once would remove most of the rework.

---

## 8. Checks for quality and truth

- **Truth rules** in both CLAUDE.md files and `DESIGN_SYSTEM_PLAN.md`: transcripts arrive after a session (never typing live); no moving cursor in replays; Claude's, Figma's and other tools' UI kept visibly separate; example names made up and labelled "Example", never Duane's; real-looking URLs (pocket.aeroapp.ai); no stock photos of people; no webcam (Aero records screen and voice).
- **Plans and limits** only from `PRICING-FACTS.md` (no "a month" after session counts; transcripts on every plan, confirmed 25 Oct).
- **Copy** by `TONE_OF_VOICE.md`: no em dashes, British spelling, sentence case, AI never the headline, no "AI-powered".
- **Feature parity** (25 Oct): the website shows only what the app does; unbuilt items tagged `data-soon` and hidden by `not-yet-live.css` until they ship.
- **SEO guides**: every claim checked against the app (LP #29). "How findings are made" makes no claims about unbuilt features (LP #30).
- **Independent reviewers**: round 5 critique (invented plans, shared stock photos, no video showing the full loop) and review R8 (P1 broken or untrue, P2, P3; 6, 18 and 13 items) before go-live.
- **Screenshots of everything**: Playwright at 1440 or 1512 and at 390, no sideways scroll, no console errors, reduced motion shows a still; the hero stepped every second through its loop.
- **Builds**: `CI=true npm run build` in figmaApp, `npm run build` in aero-landing-page, before every commit.
- **Merges**: every merge after Duane's explicit yes.
- **Real people**: Emily's test checked the words and the tester flow.

---

## 9. Reusable checklist for another project

`[Duane]` marks a step that needs Duane. Everything else Claude and its helpers can do.

**Before brand work**
1. Read the product's playbooks (this file, HeyBooking's), DECISIONS, CLAUDE.md and the TODO.
2. Check the product works end to end; repair it first if not. `[Duane]` approves each fix PR.
3. Align: up to four multiple-choice questions per batch, each with a recommended option. `[Duane]` answers.

**Research and strategy**
4. Run parallel helpers: code inventory, competitors and SEO, past decisions. Capture the live site. Check every helper claim.
5. Write one research and strategy doc with decisions as options plus a recommendation. `[Duane]` decides.
6. Ship "fix soon" truth problems as separate small PRs. `[Duane]` merges.
7. Write the facts file (plans, limits) and the truth rules before any helper writes copy. `[Duane]` confirms the facts.

**Brand**
8. Reference research: sites the owner respects, current versus dated.
9. Brand first: wordmark outlines, mark, icons checked at 16px, colour, type, buttons, a homepage slice. Always include one "evolve what you have" option. Check system fonts on a machine that has them.
10. Options led by one named reference each, each with its own layout. `[Duane]` reacts per round.
11. Full mockups by parallel teams from one brief (homepage, app screens, content page, video). Independent reviewer, then a fix round. `[Duane]` picks.

**UI and design system**
12. Every main screen drawn in every direction, beside today's app. `[Duane]` picks per screen.
13. Research how pro tools do the key screen before redrawing it.
14. Detailed UI rounds on one shared stylesheet; open questions on a questions page with one-tap answers. `[Duane]` answers.
15. Decide where the design system lives and the sync rule. `[Duane]` decides.
16. Build the demo mode (real components, example data) before marketing pieces. (Not done on Aero.)

**Website**
17. Homepage rounds built from the UI; copy in one block per page; glass or other effects in one settings file. `[Duane]` reviews each round.
18. Parity check: anything shown must exist, or be hidden until it does.
19. Independent final review, then go live. `[Duane]` says go live and merges.

**App**
20. Tokens first (alias old tokens to new ones), then one PR per area, each updating the style guide. `[Duane]` merges each.
21. Real user test of the new flow. `[Duane]` runs it.
22. Design rounds on a canvas snapshotted from live code, changes numbered. `[Duane]` reviews.
23. Implement, then update every marketing piece that copies the UI (video, guides).

**Keep it automatic**
24. Log every decision in DECISIONS the same day; keep TODO current; sync twin files. `[Duane]` merges twin PRs.
25. Never touch billing, keys, Firestore rules or regional pricing without `[Duane]`.

---

## 10. What to do differently next time

- Build the demo mode first (`/kit` routes with example data), and render the website, video and guides from it, so a UI change flows through without hand edits.
- Do the UI directions stage before detailed UI, and before the homepage.
- Give every helper the facts file and truth rules from the first brief.
- Start the canvas or boards by snapshotting live code, not by drawing from a kit.
- Keep PLAYBOOK, BRAND and TODO current at each stage, not only DECISIONS (all three went stale here).
- Hold a real user test before the website goes live, not after.
- Keep the full text of every kickoff prompt in the repo (it was lost to compaction here).
- Write PRODUCT.md and CHANGELOG.md, as HeyBooking did, so pages can be generated from them.
- Agree the hero's pace and scene list on a storyboard before building it.
- Record how long each stage took; it wasn't recorded here.

---

## 11. Aero extras

### The hero video

**Tools.** Claude Code (the lead and role helpers, for example "Team H" on 24 Oct and a Sonnet helper on 6 Nov). Static HTML, CSS and JavaScript mockups generated by Python build scripts, then ported to Astro. The glass engine `glass-v3.js` with its settings file, for every button inside the video. Playwright (Chromium) to screenshot and record. ffmpeg to encode H.264 MP4s. claude.ai artifacts as review pages. Vercel previews for each PR.

**How it is built.** One scripted animation, not a screen recording. In `src/scripts/website/home.js` every frame is computed from one clock `t`, so `?t=8.2` freezes a frame and `window.__heroAt(t)` lets a script step it frame by frame; the shoot scripts call it at 30 fps and ffmpeg joins the frames. It pauses off screen and in a hidden tab, Space pauses it, and reduced motion shows a still. The Publish, Test and Review steps are clickable and jump the video. The markup is in `src/markup/home.html`.

**Built from what.** Made-up markup that copies the real product UI, not the app's React components. Until 6 Nov the Aero screens used the v3 board stylesheet's classes. On 6 Nov (LP #32) they were restyled to the app as shipped that day (site page tabs, count chips, "Allow recording" card, one-track review, Insights chips), in `src/styles/website/hero-new.css`, scoped to `.hm-stage.hn`, with shapes and values copied from figmaApp's `LabelIcon.js`, `SiteDetailHead`, `SitePreviewHero`, `insights-v6.css` and `TesterParts`. Claude's window, the live Pocket site and Maya's screens are simplified drawings, kept visibly separate from Aero. Example names (Pocket, Maya) are made up.

**Follows the real UI?** Yes, as a copy. The app was built to match the video (parity rule, 25 Oct), and the video was then updated to match the app (6 Nov). Truth rules hold: no cursor (from 6 Nov; earlier rounds drew a cursor for the owner's own clicks only), no live-typing transcripts, no webcam.

**The two versions.** `HERO_DEFAULT = 'new'` in `home.js`. `?hero=classic` plays the round 9 sequence (with WhatsApp). The new loop is written as a time remap over the classic scenes: it skips the WhatsApp scenes, Publish about 14 s, Test about 17 s, Review about 21 s, total about 52.3 s. Shared markup uses `<s-nx>` (new only) and `<s-cx>` (classic only); the script keeps one side.

**The prompts.** Duane's direction for the video is in his 23 Oct feedback (appendix A4: "show the studio app ... then show claude building html ... then one prompt ... then show going back and its published then show making a test ... then another person or screen testing it and getting the results... boom"), his 24 Oct feedback (appendix A5: three steps, timer bar at the bottom, analysis in dark mode) and the voice notes logged in DECISIONS (24 and 25 Oct). The Team H brief is `docs/brand/website-v3/BRIEF.md` ("Hero animation (the main job ...)"). The 6 Nov refresh brief is appendix A7.

**How it evolved, and what failed.**
| Round | Date | Video | What went wrong or changed |
|---|---|---|---|
| Round 5 mockups | 22 Oct | Each team made an MP4 (D Replay's animated app liked) | Critique: no video showed the full loop; D "a bit too quick" |
| Website v1 | 23 Oct | 14.5 s loop inside the Home screen; MP4 via Playwright `recordVideo` and ffmpeg | Replaced the same day: keep round 5 A's angled app hero instead |
| Website v2 | 23 Oct | About 49 s replay of a session at 2x | "very slow and doesn't show much, the prototype doesn't even move" |
| Round 4 | 24 Oct | Three steps (Claude, test on Maya's computer, review in dark), progress bar | Section loops collapsed (CSS class clash); a bit too fast |
| Round 5 | 24 Oct | One angled browser window; cursor for the owner's clicks | Pause button clashed with the test UI; unclear Maya is on another computer |
| Round 6 | 25 Oct | 45 s, captions, Maya on her own laptop | Caption pill removed; "User test this site" too quick |
| Round 7 | 25 Oct | 48 s, centred, WhatsApp handover, clickable steps | Maya's tilt and pan "looks tacky"; pasting into Claude too fast; WhatsApp tab missing its favicon |
| Rounds 8 and 9 | 25 Oct | 52 s; review R8 stepped it every second | P1 fixes (for example the Test section loop) before go-live; unbuilt features hidden |
| Live | 26 Oct | LP #7 | |
| Round 4b | 6 Nov | No WhatsApp, no cursor, shorter Publish, longer Review (LP #28) | Classic kept behind `?hero=classic` |
| UI refresh | 6 Nov | Aero screens match the shipped UI (LP #32), recorded at 1280 x 800 | Scene order and timings unchanged |

**How long it took.** From the round 5 team briefs (22 Oct 15:07) to the live site (26 Oct 00:34): about three and a half days of calendar time across about nine rounds. The 6 Nov sequence change ran across LP #28's commits (06:12 to 16:24). The 6 Nov UI refresh helper ran from 17:13 to 17:28 (about 15 minutes) and the PR merged at 17:29. Hours of actual work are not recorded.

### What Aero did differently from HeyBooking, and whether it was better
| | HeyBooking | Aero | Better? |
|---|---|---|---|
| Start | One review prompt | Repair, then alignment questions | Better: the loop worked before it was sold |
| Art direction | One round, six looks stacked | Five rounds, then four full mockups and a reviewer | Slower, but the round 5 method was "far stronger" |
| Logo | Wave and dot, new | Evolved the existing "Aero." | Kept equity; adds the rule to always offer "evolve what you have" |
| Order | Website, then app in seven rounds | UI first on paper, website live, then app built to the website | Faster to a live site; more rework (part 7) |
| Illustration | Card kit from real screens | Hero video; no card kit | Video loved; card kit still missing |
| Knowledge files | PRODUCT, CHANGELOG, BRAND, TONE, PLAYBOOK | DECISIONS, PRICING-FACTS, BRAND, TONE, PLAYBOOK, DESIGN_SYSTEM_PLAN | DECISIONS was kept current; PLAYBOOK, BRAND and TODO went stale |
| Repos | One repo | Two repos with a sync rule | Necessary; extra twin PRs |
| SEO | Country folders | Task pages from one template | Right for international buyers |
| Glass | Liquid Glass dropped ("too much") | Glass central, tuned in a lab and a control panel | Distinctive; took many rounds |
| Testing | Not recorded | Real user test fed the last round | Better |
| Design tool | Review pages | Boards, then a Claude Design canvas from live code | Better once it copied live code |

### How Aero and Figmafolio relate, and the Figma logo and font risk Clark raised
- **One codebase, two brands.** figmaApp serves both, branching by hostname. Aero is the growth product; Figmafolio is stable and changed as little as possible (Bootstrap pages, no Aero tokens).
- **Why Aero exists.** In Feb 2026 Figma refused a plugin listing because "Figmafolio" contains "Figma"; its trademark rules ban "Figma" or "Fig" in product names, domains and handles, and allow "for Figma". (Past chat, 12 Feb.)
- **Same plans and prices** from one Stripe account; each checkout is labelled `brand: aero | figmafolio` (4 Nov, #319).
- **Moving people across.** "Figmafolio is now Aero" screens, a "Try it on Aero" gate and /redeem sign-in handoff (#319, #320), and an onboarding popup (#289). The migration test is control versus Aero only (4 Nov). Duane's memory notes say the forced migration test has run since 16 Jul 2026 (from memory, not the repo).
- **One logic, two looks** for shared features (for example Figma links, 4 Nov). The free plan, offline rules and "unavailable" words are the same in both brands (3 Nov).
- **Ownership.** Clark (Clark Wong, Hong Kong, per Duane's memory notes) owns or is taking over Figmafolio. The rule since 22 Oct: change Aero files freely, flag anything shared with Figmafolio before merging. #270 flagged five Figmafolio styles moving to the new blue.
- **Figma in Aero's own brand.** Aero's logo is "Aero." in Geist (from Google Fonts) with a blue dot; no Figma mark or Figma font is used in the logo. Duane said A Studio "feels like Figma, which isn't bad" (23 Oct). The truth rules keep Figma's UI visibly separate, and the share guide draws a simplified share dialog in HTML (`ShareDialogMock`) rather than using Figma screenshots.
- **The risk Clark raised:** not recorded. No repo file, transcript, brief, attachment or past chat found here records what Clark said about the Figma logo or font, when, or what was decided. Open questions for Duane: what exactly Clark flagged (Figmafolio's own logo or font, Aero's, or Figma's mark in guides and plugins), and what action he wants. Until then nothing here should be read as a decision on it.

---

## Appendix: prompts, verbatim

Duane's messages are as he typed or dictated them.

### A1. Round 2 feedback, starts round 3 (22 Oct 10:22)

````
i didnt liek index, looks like atrain , where are the options that take linear or openai as refernce, what other design tools did you reference liek wheres the figma isnpired version?

daylight looks kinda cool not sure i like the roudned buttons

all the cuatic buttons seem too much.... the idea was it takes whats around it and reflects it, kind of like a hyper liquid glass, i dont see it in the buttons, it should take distance into acocutn etc..

afteflow also looked ncie but unsur eof dark mode websites

studio whle it looks genric, it kind of is more approachable as a design tool, as it probably has the brightest colirs

full stop is nice, looks expensive, is it really using hte same font and A s e do now, maybe check that and the weights.... 

not sure where all the influences are lie nothingl iek claude etc.... all of these seem too space related

then all of them have the same layout, but would be nice to see differneces dependingonthe brand too
````

### A2. Round 3 feedback, starts round 4 and the glass lab (22 Oct 14:20)

````
i liek the full stop logo, although crurus how it looks in different font, 

defintiely liek the dot

the caustic button needs to be more lie my original and subtly take nearby colours like glass.. liek sometimes like white next to black button its a bit too obvious looks weird , it shoudl be subtle and effected by distance and how much is near it or itnensity etc,,, maybe do some vriations based on the caustic code and your own interpreatinos and also searcn. ald learn fro minternaet how to implement liquid glass buttons and htne also do a hybrid

i like the 'pocket.aeroapp.ai' that whole window ection fro mthat it looks good...

precision only like that black winow (maybe do a light bersion too) i think that UI for that looks really good, and jsut how its at an angle etc

plain ,dont like the searhc bar, rounded vs square buttons i am not usre but i do like the colour cards...

canvasnot sure i like it overall but i do think we need to bring soem of the colours in and some of that desinery stuff in jsut a little, 

dot didnt like at all

i think given that , do a new set of optinos, combinations an dsoem variations on what i like etc,

and maybe start to look at hte existing app pages andseew hat youd imrpove page wise and ux / flow wise...
````

### A3. Round 4 feedback, starts the round 5 mockups (22 Oct 14:58)

````
for round 4, 

i think for studio  the postcit seems forced and that font it uses too elgant

i do like the sans fotn , its jsut hte headline page title seems way too bold or bog and the you , tester a and be seem forced, i would liek to see more san sefir logo used in the otpinos and the nwe can paly with aero and different ones as oyu think make sense

all the otpinos you did seem so simialr now, dispite me aying wha ti liek you jsut maashed them tgoether without rrethinking the optinos form there

maybe start to mock up, you need the art director , copywriter ,ui diesgner ,ux designer ,information archtect, brand expert, animatior  , animations, video export, graphic deisgner ..as differnt tools and tools to work on 4 diffent deisgns of the imape page, app and content... we cna start to explroe deeper the app and ohw it looks so the mockups , animcations how it al lworks together etcccc...

we want a bit of colour, we want it to be liek a design 

tihnk of it its user testing real people bring in soem stock iamges, but then also bring in like it saves time... its smart.... its simple.... transcopption automatic, its fast, striaght form prompt, think abotu the propsotion etc from our conversation and the dossier you did etc..

Design tool, profesional, but accessible, a bit of colour , a bit on ai insight from real sessions ... theres a lot to sell and the first page neess to do it all

think of the design options, like the oens i like and ther eferenfces behind them make one or two optinos a bit unorthadox or differnet, jsut follwo your process and what makes sense... show the ui as htat hleps show ihow it works etc...
````

### A4. Feedback on the round 5 mockups, starts UI first and the design system (23 Oct 01:47, attached file)

````
Aero feedback

OK for all designs the UI looks incredible, it seems we might have to work on that first, as the UI is shared with the marketing website.

but not sure how much you are saving along the way you can save a lot of thie artifacts na decisinos locally, not sure you picked up on using a shared design system and having marketing components that are simplier versions of the real components to be used in animations and illsutrations and then updeated automatically as we go ahead..... in claude.md etc i still want to do all of this, analyse our whole conversation not sure that was in your head.

I liek option A studio, its nice to just see the APP its probably the quickest way…  although its a bit lmisslaading as the transcript isn’t live its processed after….

Also maybe the video should cover likegonig from clue, the prompt to published etc….

And use real urls etc… 

Like the graphic - Live in minutes, however you made it.
Is just wrong you are mixing our interface with claude, they are separate you should show that…

Hmmm the unsplashed images do look a bit fake maybe 

Their screen and their voice, in step - it looks great but again, (maybe you can enhance it) but we are unable to see their mouse movements nth video…. 

And again great UI but it’s not real which makes me think we need tow work on the UI last the same time as the website.

I liek 

From prompt to first session.

I think it could show the different scenes , like need to publish a website, how quick it is….

Then need to test it… soy just ( think thats ossicle in the app too) then send link then test)….

Better with some simple illsutaiton animation,… as you did before, act as a team of experts …

For people who make things.
 Looks a bit fake, hmm does that section exist for SEO, actually might be useful , but I don know, lead with SEO first if that section makes sense and then they need their pages then do it if not do something else

It looks fake as th stock images, might transition to illustration, animation etc…. 

Overall I relax like the app here…maybe having friction points on home from any project is a bit focfnusing though,, also what happened to the caustic engine within the app…. Hmm try and make it work, we picked a 

Also for the new site mock up why is their record screen and voice thoughts that’s another flow

Also you never show what the testing screen looks like, which at the moment uses a glass effect but then we don’t use that eslewehrere… and then ptorotopes can be any colour so how do we make the task, prototype recording flow work well

And make sure each variation and step makes sense e.g. no tasks, which tab do they pick etc, need to act as a good software engineer…. Copywriter..ui designer etc again…

The content is useful too…. I thin the more guidance and explanation the better ,think of SEO and ever part of the app .g. how does the insights work, trnascritpino etc… think forom all the feats of the app then set etc…

I like the logo for A studio really…

Ok B - colour

So not sure about the typeface and logo on this one

The colours DO make it clearer and having separate sections I think is good…. Just makes it clearer

Jsut wonder what those are , publish makes sense, publish code, prototype etc

Test makes sense, maybe user test? Is clearer, but one word is also clean and that’s like share…. Test.... Guide ,all the features over there

Then I am not sure read is right, as you can watch the video, tis more like ‘review’ or analyse right … so maybe 3 sections….. 

I think having the colour in the menu might be too much ,although it is clear… maybe not have it…

So I’m split I think this option is a bit too much, to start with the voclorus hand have block colour etc…. But it definitely makes it clearer

So maybe we iterate like I think what worked is that big one hero image showing the app (and with my design system idea ) itwoudl be based on real UI…. Which we need to figure out) and then…followed by the 3 sections, tmaybe using the colour gradient style fro meh first one A (but still keeping a more softer gradient colour palette for each of the sections…  and although the sections are clear not sure I like just having a picture for testing, its more accurate someone elsewhere on their computer screen tests it and this doesn’t show the app as much

Well I guess for B vcolour the 03 01 02 04 aren’t so clear but the n the sections after that e.g. live in minute however you made it (although the copy is vey ai cliche, ) those are clear..

Oh yes there’s versioning too,,

I mean think holistically today I can’t think of something quicker … it’s quick to publish , it’s quick to test (eg. Just upload or ) its quick to alanyise (transcription and insights)

And cheaper than competitors…

For B - colour , I don’t think the UI looks as good, but it is clearer… and yeah consistency with branding and the product is great…. 

Although the session vie is similar, so perhaps separately we just need a session on the UI for the whole app the different approaches ,side by side or section by sedation given the options you already did etc..

Animation is a bit quick, could be useful for a video (that’s a operate outcome I guess… I think I prefer A for this,  I suppose A, could show different faces e.g. screens like show the studio app, duane’s studio don’t use my name use another name…  then show claude building html or already built (use accurate ui, then one prompt (make it realistic perhaps simplified) then show going back and its published) then show making a test (therein app again) then another person or screen testing it and getting the results… boom… so proefe animation A, just needs to separate to context, steps e.g. screens…

C story hmm the ui is okay, , I like how it shows teaser and the voice quite … (maybe we can have that animation of the text as it plays ) in the app, just makes that voice part interesting and we can say we ranscripbe and analyse at the same time

I like ‘Made for people who make things.

‘

The story concept is a bit verbose .. I think you nailed add just a little of that into the previous concept , just a little bit of real context that’s it 

I do like the UI under ’11:40
Seven minutes on a Sunday morning.
‘ Section though, it feels good for analysis…. So its an option

Hmm we will have to see C - story, the UI feels calmer, more sub stack like, it feels clearer , colour calve is nice, so its also an option wonder what’s in-between this and option A for example and how either work with the caustic buttons we landed upon

Content looks clean again ts those 3 sections we seek talking about but its not watch and read, its more like, ok the session is already synthesises, transcript done, main insights , andtohle ting summariesed and. You can look for detail the main points or synthesis across tests.. (the ai does that too)

The animation, I like a few things in it , the ne prompt shows it well

The voice animation and how it highlights and shows insights… so we should take those and combine it with what I’m saying. About A , like doing it in the app etc…

Oen prompt and its live is a great sentence too..

Ok last option D…

I kinda like this …. The animation is interesting a bit too quick… and only showing nippers of the UI, we can show the whole app ui ,but the animated parts tell people what to focus on I guess..

The copy is also good for this one ‘in their own words and showing the feature  m just not sure about the scrolling parallax

As for D the app, again looks quite good… , similar but different so just need to do combinations of some of these options and experiment a little and see how it works in an action flow… 

The content you made, hmm its interesting ‘test your claude artefact with real people ‘ can be an action content page, remember set friendly publish claude artefact publish lovable, we want 100s of pages for every scenario… publish sigma prototype, test sigma prototype, but act as a set , even use set tools now in my browser and then act as an set adscisor ,the work wit, act as the content creator ,animator and make peoples ( I guess this can be done later when we are eonhte style though)

The animation here is pretty cool a bit too quick, but I like the sections as it shows how quick it is to go from one stake to another…. Like that line at the bottom… pretty cool, again showing the animated app really good stuff, so think generally we are aligning, you need to build ti in a good way that the structure is there but we can change the ui, the story , the copy without rebuilding the whole thing etc…
````

### A5. Feedback on the homepage rework, starts website round 4 (24 Oct, attached file)

````
Aero Feedback

Looks good, for headers I know they have a full stop at th end, but the full stop is square I wonder if we should use the same (is it the same font as the logo)? Where we have the bleu ot, I think the blue dot in the logo can be slightly bigger ..  Not sure I like the blue dot fro example session or prototype histing and user testing , it seems a bit too much… 
Caustic buttons, is this in the mockup as the buttons don’t seem so cuaustic to me, but we already rdecided to use it, so what’s going on there?  ‘Watch people use it’ sounds weoird and I don’t know, review the whole aero proposition, its hard as its like on one hand, publish your claude artefact in seconds (sounds cliche) it is aobut speed, one prompt to publish….easy place to manage your work…. Use it as a website …. Do user testing on it. I just down gge th the ‘watch people use it’ maybe ‘get feedback on it instantly’ or ‘test it immigdately’ I odnt know oyu can do a better job then me ,

Not sure I feel the buttons should be under the header maybe rework the whole hero area  ok for the hero image / animation, I asked for it slower now its very slow and doesn’t show much, the prototype doesn’t even move, this is very different otwhat you showed, the version I liked before!!

The version I liked before was dynamic, quick, showed all features which I liked… this jsut shows just one screen…..

My thinking was to show the 3 steps, so the first is quick publishing ,you can show someone using claude app, with their site on the right like the preview function, then they put in one prompt then its published on aero, then second  , so you show the publish, then test…. So that’s liek maybe you share then another browser window, someone open then does ht etest… and you show a voice or something…, then show the analysis….. (the screen you ahve now)  
So should still have that thing form before, like the timer bar at the bottom sohing what stage they are at…. And ptu the analysis part in dark mode… but the rest light..

And the gradient can change per section. Guess....

Not sure you need to say example session or recorded play keep it simple and. Confident

For the three text bits under the big hero animation, I do think the small blue icon and test work though, but just have the liens maybe theat fill timeline the line in blue, all black looks too much

Ok so for the first section publish…. I think should be a mix between the round 5, rework and previous round , lets call this 1 , 2 and 3 respectively…

I think design 1 looks the nicest like aver having 1 big hero then you have the text and image, the image text for each section etc…. Its just that was a bit too much on one UI element, 2 feels like too zoomed our, with labels not needed, and 3 feels a bit lazy like just two ui elements on top of each other…

I think the image/animation for these sections can be subtle animated targetied…. While th big one just literally shows all the real flow etc… and all the features, these can just show the specific ui elements e.g. maybe pasting in the prompt then it being published….

Then next is sharing the link ,then soemotn opening it… it records

Then ext is analysis ,which is maybe session voice, then even all sessions, so that’s showing something a bit more apbstact maybe… 

Each has their own sell, one prompt to publish (perhaps also show you can just upload html or sigma or maybe thats vovered by text and suggested in the ui),
Then ext sell is, yeah just share a link , then someone can user test no software… then the next is transcribed automatically, insights already there, and syntheses across session…

I guess in terms of the writing version 2, the rework version seems closest

I am not sure th prompt to first session makes sense anymore  as we do tell the story its quick.. perhaps overall a slight emphasis should be . Like I don know in my words I can’t think of a quicker way to publish something an then test it with very little set up… on one platform…. Its fast, simple quick, and not expensive , even free (I forgotten what’s free)

Since we are changing the bit below the big hero to the timeline, like which stage, the ‘priced for one designer’ should be somewhere elsewhere….I like it, I thin priced for a designer not a corporate or something like this….

Maybe for pricing we should compare competitors and their pricing (make sure we are comparing apples to apples though not for panels etc) rather than showing our own pricing

I kidn of like for people who make things….maybe have a think of the archetypes… again each section has its own advantage… like publishing, there no tech knowledge needed…I forget the tech terms for hosting or domains but you don’t need to know that really (maybe when you connect a custom domain you do), then for testing, just think of the pinpoints of user testing software ,then analysis, like the time spent going through whereas this is automatic… but still allows for reading experience…

Everything figmafolio has we have… so that should be added even in a small waay ,like connect a custom domain, password protect it, test it…

I don’t like how the questions part seems a lot of wasted white space here in my option

Remember our tricks before, act as many roles and tools, the best brand expert, art director, copyrighter , ui designer ,ux designer ,animator, graphic designer , motions expert, video maker etc…..

Maybe the colours should be , the more blue for publish, green for test and orange for analysis, might make more sense to em.. 

The previous round 3, did get somethings right like I notie it did use the sbleu dot for the header , I think the publish , test review… perhaps a coloured pull for each section might help pi don’t know …. Like publish uses the blue pill try it but I am not sure about it, just to make it clear as the gradients are kind of subtle ways , still might need a label, because under each one there are a lot onefeatures so might be useful for the features page to have sections and list our every single feature..

I mean the ethos is really about it being quick, like less time on the tedious things, like perhaps different use cases would be good, you can brainstorm sum, maybe look on reddit how people are doing things, and pain points, ,maybe dircous scenarios like

Online portfolio needed, someone puts al their work in the folder …. Ask ai to make a html portfolio ,the none prompt published

Then on the testing side… maybe someone has a product idea the night before….usualyl take a week but now, they have a prototype, they can send out to 3 people, they accept do in own time, next morning they have the insights (already transcribed and pain points, fdlgihts recorded)


I can’t remember if we distinguish the promtps like different prompt of testing or publishing…. And for testing ,can it ask follow up questions for tasks, that would be nice etc..
 for tue buttons I like the cuastic but I don’t think they need to get bigger , maybe there should be a visual hover e.g. maybe imagine it raises, I don’t want it to physically move but lets say in real life if you are looking soemtihng above and it goes up, it wouldn’t change size but the light would refract differently, sometihng lie that, maybe some options for this, other skeep it simple, def want the caustic one re decided before but for hover maybe its the cursor that changes the light reflection etc…. 

I am thinking the gradients, it might be too much as each part is animated but I do wonder if that slowly moves or changes over time might be interesting, even in the app…

Also in the UI you have this nice glass cusastic glass, just make sure that is used e.g. our top nav or in the ui, as maybe if button on gradient that’s the time to use cglass button, maybe even the sign in button as as you scroll it goes over parts of the webstie etc…

Lastly make sure the site makes sense from see perspective ,remember we were going to have so many seo pages, my feedback is each menu item at the top should be asseverate page…. So maybe features not product, and then features has al features of the app, in the publish ,test sections etc…

And we need a blog what has, similar to heybooknig…. Blog that has all the features www did per time with the date so it looks active etc.. don’t forget all of that whether we do it now or later… 
 I guess one last thing is that - you could look up MAze and competitors to see what they advertise and how they copywriter and what laugne they use , I think it will be good to lear for the,
````

### A6. "Aero feedback 2", starts canvas round 2 onwards (5 Nov, attached file)

````
Aero feedback 2

Feedback on canvas  Styleguidel looks good but does it align with what we have live e.g. /aero?  anything missing from it, I felt the life one has more but unsure , also we need to keep it updated so it really reflects real app…  Ok sites list, my problem here is the side nav looks different the dashboard is missing the top bar… its not effecting what’s in the app unless you are purposely changing it .. , if you are then you should discuss with me first …  like when we create site, not sure I like this name and what happens next in the side bar??? And the cancel in top bar at all , or just consider it,

Then I am also uncle , you need to make the screensizes realistic… I thought we were only going to show screenshzies later unless you think it works on. That screen, the button seems wrong too is it using chelatest glass buttons and for ‘other ways’ isn’t that a bit hidden? If we will build the feature

Just feels the ux / ui can be improved on this page or you can give options, feels a bit bland compared to other pages…

Is the guidance for from claude or chatgpt clear? Like it assumes the alreadyy have an artefact or html,,, so might need to explain it a bit more there , but make the design nice 

For site I don’t get why there is a thumbnail near the title and tests not, please keep it consistent…

 I like the oven live and refresh button, but not sure they should b. Outside the box, maybe a bottom bar over the thumbnail or I mean at bottom or the bo  is tests too prominent there? should that really be over updating the file?   hmm and why is sites all on one page but lets have tabs … lets make that part consistent tooo…. What needs to be on the first page by default vs not, is sidebar always there or its within the tabs etc…. Give some options  again as I said previously act as the best ux research, information architect, brand designer ,copyrighted ui designer graphic designer , animator, motion ui expert etc and think thus through

For the updated account account just improve that a bit hmm not sure the ‘everything in basic; is a good approach as makes it look like you get less …   also yes the popover but didn’t you have a better design previously for that and the design you have for that uses an old blue button, so you really have done a bad job of that part   for visits i mean I like it , it was a bit different in another design you did so find that give Orem options, I mean again act as the best ux research, information architect, brand designer ,copyrighted ui designer graphic designer , animator, motion ui expert etc and think thus through  given what we have what data we have now and can do please…

Ok for tests the ‘2 new since you last looked under sessions’ seems added on looks wrong the ui and what happens how do we display draft tests if there are any…

Teh input of tasks looks bette but unclear best practise to save, did tou have a different design to this before etc?   source - hmm is that different to upload is it insiddtn etccc how do you save the messages o than you, is it clear why those appear can you give a preview of that what’s the best ux ui for those   insights look good , any difference between this and rte review ui or the video ui just access  hmm the testers welcome is quite nice …. What was the feedback from the user test about the copy ‘share this tab’ did you ge that our lets align that first what was her comment and act as the best copy righter give me options, shunt it just say aglow, microsohw allow makes sense  learn from permissions dialog iOS which is clear etcccc short copy etc 

Recording your voice ‘is that too much just put recording… hmm I don’t think the days should appear in the mingle, keep it in a corner please and make sure it aligns with what we have in style guide ,should use a bit glassy and the most rescent buttons etc  hmm I think you over explain ‘the recording made so far is still sent’ no nee to mention, just say it will stop the test as is oor something… not sure why you need to say recording your voice there   for three states of last screen - I thought we were going to try to send as we go along which is. Technical enahcneemnt 

For review it tested well so it was just about making the skip silent actually work andd effect the timeline ,  hmm maybe making the timeline have some options (not making it complcated… I like the lands by kind actually, I wonder if we should actually show the voice, I like that we show the tasks and should have a toggle to show quotes on the timelineee or the summary like C too, that would be nice , so b and C but also be able to collapse it so its just a time ice as well, and hide task etc… jut make ti more flexible but the default is a balance with al to of into clearly laid out 

Change label is good although I don’t like the drop-down has this left bar on it ,that’s very ai doesnt, so remove that.. otherwise looks fine   I can’t remember if the user test said wit needs an explatinoatino of how things were processed maybe somewhere like a footnote and a nice page explaining how it works (tou can make it almost like am rating page) and sohulnt that be used as feature page for the website too)

For the website lets align firs what version do you think works wel and what if any are yo changing to the vide was we liked the video… 

I kind of like version 2… but it might focus on testing 

If we go that route it’s almost like we need a separate page for publishing and hosting….

If that makes sense ….

I definitely like the copy on version 2, so maybe lets align on a balance or maybe not lets discuss ….
````

### A7. Brief for the 6 Nov hero video refresh (helper, 17:13)

````
Update the Aero homepage hero video so its app screens match the app UI that shipped today. Deliver it as a PR on aero-landing-page; don't merge.

**Repo:** /home/claude/aero-landing-page (GitHub duaneharrison1/aero-landing-page, base main).
- Read CLAUDE.md first, then docs/brand/DECISIONS.md (it now has a 6 Nov section listing the shipped UI) and TONE_OF_VOICE.md.
- Create a worktree from origin/main on branch claude/hero-video-new-ui.

**What exists**
- The hero is a scripted animation in src/scripts/website/home.js plus its markup and CSS. It has a 'new' sequence, the default, and a 'classic' sequence (?hero=classic) that must stay untouched.
- The timing and sequence were agreed and Duane is happy with them, so keep the scene order and timings exactly. Only change how the Aero screens inside the scenes look.

**What to match.** Use the real app screens from figmaApp origin/master (/home/claude/figmaapp; use `git show origin/master:<path>`):
- **Site page** (src/pages/AeroSites/):
  - tabs Site / Versions (with the count chip) / Analytics, and the Settings rail beside them with no box
  - the shaded preview bar with Open live and Refresh
  - Visit site as the primary button
- **Test link / test page** (src/pages/UserTesting/): count chips; the quiet source line.
- **Tester** (src/components/UserTestingTester/):
  - permission card: "Allow recording", Microphone and Screen recording rows with Allow buttons
  - recording pill that says just "Recording"
  - task panel with the grip
- **Session review** (src/pages/UserTesting/review/): the one-track timeline with a very faint waveform, bare label icons on it (warning triangle, question mark, lightbulb, tick), and the one-row toolbar.
- **Insights** (src/pages/UserTesting/insights/, tabs/UTInsightsTab.js):
  - gradient summary card
  - numbered findings with "N of M testers" and a severity chip in one red family
  - quote cards with a play button, tester, time and a sound-wave strip
- **Shared look:** the label icon SVG paths are in src/components/Aero/LabelIcon.js. The count chip is .aero-ct in LabelIcon.css. Copy the shapes and token values into the site's CSS using the site's own tokens, where the synced tokens allow.

The /aero showcase on app.aeroapp.ai renders these. You can build figmaApp locally and screenshot the showcase for reference.

**Truth rules**
- no cursor
- transcripts never typing live
- example names only, labelled Example
- Claude, Figma and Chrome UI visibly separate from Aero
- copy follows TONE_OF_VOICE

**Build, record, PR**
1. Run `npm run build`; it must pass.
2. Record the new loop with Playwright `recordVideo` at 1280x800 to /home/claude/research/app-v3/shots/homepage-r5/hero-new-ui.webm. Take stills of each scene at 1440 at 2x.
3. Commit with a "[wip]" subject and this trailer:
   ```
   Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
   Claude-Session: https://claude.ai/code/session_014Md1dz56eBq9Rm2Z2nPcoZ
   ```
4. Push and open the PR via gh api REST (GraphQL is blocked). End the PR body with:
   ```
   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   https://claude.ai/code/session_014Md1dz56eBq9Rm2Z2nPcoZ
   ```
5. Get the Vercel preview URL from the PR comment, then remove the worktree.

**Report back:** the PR link, the preview URL, which scenes changed, and the video path. Be token-conservative.
````

### A8. The prompt for this document (7 Nov)

````
# Prompt for the Aero project: document the rebrand and redesign process
Task: Aero process prompt (Aero day, Thursday). Paste into the Aero project. Paste the answer back to the Daily CEO. Companion: prompts/heybooking-process-playbook-prompt.md.

---

We rebranded and redesigned Aero after we did it for HeyBooking. I want the whole process written down so I can repeat it on other projects, and I want to learn what Aero did differently.

Step 0, compare with what exists. Find the earlier versions: any process or playbook prompt I gave you before, `docs/brand/DECISIONS.md`, `BRAND.md`, `TONE_OF_VOICE.md`, `DESIGN_SYSTEM_PLAN.md`, `docs/TODO.md`, the AeroShowcase page, the design system docs, the commit and PR history, and our chat history. Then list **what changed from the HeyBooking playbook and from any earlier Aero prompt, and why**: what we added, dropped or reordered, and what we learned. Build on what exists and fix anything wrong.

Write one document, "How we redesigned Aero, start to end", with these parts:

1. Timeline, with dates and who or what did each step.
2. The prompts that started each stage, word for word (long ones in an appendix).
3. Research: what we searched and read, and which research changed a decision.
4. Decisions, the options, what we chose and why, including my likes, dislikes and corrections.
5. What worked and what did not, including the back and forth.
6. How the design system was built, and how the website, app and illustrations were kept in step (the marketing pieces are built from the real components).
7. Order of work. We did the new UI and the home page at the same time. Say why, and whether it helped or hurt.
8. The checks for quality and truth (for example, no invented claims about the product).
9. A reusable checklist for another project, marking which steps need me.
10. What to do differently next time.
11. Aero extras:
    - The hero video. I loved it. Document exactly how it was made: the tools, the prompts, what it was built from, and whether it follows the real product UI or a made-up one. Say how long it took and what failed.
    - What we did differently from HeyBooking, and whether it was better.
    - How the Aero and FigmaFolio brands relate, and the Figma logo and font risk Clark raised.

Rules: only write what you can find in the repo or in our history. Where something was not recorded, write "not recorded". Plain language, no em dashes, British spelling. Save it in the repo under `docs/brand/` and give me the same text here.
````
