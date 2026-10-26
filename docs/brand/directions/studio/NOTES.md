# A. Studio: every screen (explore stage)

Files: `pages.html` (built by `build.py` from `src/`), `shots/<id>.png` (by `shoot-studio.cjs`). Example data throughout: Kestrel Studio, Mia Chen (Example), Pocket at pocket.aeroapp.ai with 6 sessions, Onboarding v2, Checkout. The old hero's moving cursor and typing transcript are gone.

The system in one line: one real light window on a soft wash, with colour only in the washes. Each step has its own: **Publish is peach, Test is sky, Review is mint**. The same washes appear quieter inside the app, on the one card that matters on each screen.

## p1 Home
- Idea: "What's new" first. Each line has a real thumbnail of the prototype (not an icon tile) and the session dots, one per session: filled for ready, dashed for processing, struck through for no audio.
- Works: calm, and it answers "anything new?" in one glance. The session dots are a status mark Aero can own.
- Unsure: there are now three ways to see tests (feed, table, sidebar). The table may be redundant once the feed is good.
- First run: a single Publish-wash panel with the three ways in as rows, and 01 Publish, 02 Test, 03 Review beside it. Free limits are stated plainly.

## p2 Sessions
- Idea: a Linear-style table numbered from the first session, a length strip above it, a peek panel on the right, and J/K to move between sessions.
- Works: no audio and processing read as plain words with their own marks. Nothing is a pill. The first friction line is quoted in their words.
- Unsure: whether the length strip earns its row with only 6 sessions. It could matter more at 20.

## p3 Session review
- Idea: the recording comes first, on the Review wash. The transcript follows the playback word by word, friction dots sit on the waveform and in the text, and the summary and priorities sit under the player.
- Works: the highlight is true (it is a replay of words already transcribed), and there is no cursor. The "How this was made" note covers the guidance Duane asked for.
- Unsure: the inspector is dense at 380px, and the transcript and friction list compete for height.

## p4 Publish from a prompt
- Idea: a single page keeps its own history. Connect once, copy, waiting and published each tick off in place, and the page ends on the address and "Now test it". The earlier states are shown small above it. Claude is a separate, simplified panel in its own colours, labelled "Outside Aero".
- Works: the result card on the Publish wash is the one coloured thing, so the eye lands on the address.
- Unsure: showing two Claude panels (working, then done) may be one too many.

## p5 Upload HTML or zip
- Idea: drop, then a quiet file list with progress, then the site's Versions tab with the live result on the Publish wash and roll back on every older version.
- Works: version and rollback are visible at the moment you publish, and "the address stays the same" is said once.
- Unsure: the upload limit ("up to 100 MB") is a placeholder. Confirm it against the code.

## p6 Review across sessions
- Idea: a summary on the Review wash, then "What to fix first" as a numbered list with the quotes and play links behind each item. Themes show who said it as a row of session dots.
- Works: "4 of 5" is something you can see. The no-audio session is shown and clearly not counted. "Where testers disagreed" is short.
- Unsure: "based on 5 of 6 sessions" might confuse people who expect 6. It may need the no-audio reason inline.

## f1 The flow
- Idea: **one page that fills in.** After the prompt you stay on the prototype's own page, and each step lands as a new row: Publish, then Test, then each session and its review. There is nothing to navigate to. The progress line runs peach to sky to mint.
- Works: very calm, and it matches Studio's single-window character.
- Unsure: today the app splits Sites and Tests, so this needs the site and test merged on one page (a real IA change).

## m1 Marketing kit
- Idea: the same five components (session card, friction quote, site card, test link, playing transcript line), each drawn about 2x with less detail on its step's wash. The composed hero reads Publish, Test, Review from top to bottom, and the social card is "In their own words."
- Works: the components are recognisably the app, just quieter, and the washes carry the brand without decoration.
- Unsure: the site card's thumbnail area is mostly grey at large sizes. It needs a better crop of the prototype.

## Becoming the shared design system
Studio's pieces map straight to tokens and components. The tokens are the three step washes (in two strengths: stage and in-app) plus ink, greys and the blue dot. The components are the status word with its mark, the session dots, the real-thumbnail slot, the friction quote, the transcript line and the window shell. The marketing versions are the same components with a `size="display"` variant that hides metadata, so a UI change flows through to the site.
