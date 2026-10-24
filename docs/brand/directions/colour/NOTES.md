# B · Colour: explore stage notes

The idea in one line: each step owns a colour (Publish sunflower, Test pink, Review mint), and the colour lives in the canvas, never in the nav. Blue is not a step: it means "where you are" (the selected row, the playhead, the word being spoken), the same blue as the brand dot.

Changes from round 5: three steps, not four (Watch and Read merged into Review, which took mint; cobalt is gone as a step). The nav is neutral. Washes are soft gradients within one hue, not flat blocks. Funnel Display is gone: everything is Figtree, with a plain "Aero" logo in Figtree 650, plus Geist Mono for times. No pastel icon boxes: the ways in are drawn as the inputs themselves. The cursor that was drawn on the old replay is removed.

Files: `pages.html` (built from `src/build.cjs` + `src/pages.css` + `src/glass-v3.js`: `node src/build.cjs`), `shoot-colour.cjs` (`node shoot-colour.cjs [ids]`), `shots/<id>.png`.

## p1 Home
- Idea: "What's new" in three columns, one per step, so the colour tells you what kind of news it is. Tests list with a real thumbnail on its step wash and a loop meter (three segments filled to where the test has got to). Sites table with "Test this site".
- Works: the neutral sidebar lets the three washes carry the meaning; the loop meter is a status mark you can read in a blink, and it isn't a pill or a stripe.
- Unsure: the three columns are nearly equal and could read as "three cards in a row". If one step is empty its column needs a quiet state. Thumbnails are tiny at 112px.
- First run: only Publish is in colour; Test and Review wait in grey and say what they'll hold. I think this is the clearest first-run of the direction.

## p2 Sessions
- Idea: the test header takes the colour of the active tab's step (Sessions and Review are mint, Share is pink, Setup is sunflower). A numbered list, oldest first, with length drawn to scale and a tick per friction point. Selection blue for the current row. A preview pane beside it, and arrow keys to move.
- Works: you can see the long sessions and the bumpy ones before reading anything. Processing uses grey shapes, never typing. No audio has its own dashed strip.
- Unsure: a header that changes colour per tab might feel jumpy. The alternative is to keep the header mint once a test has any sessions.

## p3 Session review
- Idea: recording first, in the tester's shared tab, with no cursor. Mint friction ticks on the timeline and mint times in the list. The transcript follows playback word by word in selection blue. Summary, friction points, priorities and tasks on the right.
- Works: the colour logic holds. Mint means "found in review" and blue means "now". The word highlight is true to what the app can do (word timings are already stored).
- Unsure: the three columns (list, player, findings) are tight below 1300px. The player stage is grey, which is honest, but it's the dullest part of the screen.

## p4 Publish from a prompt
- Idea: one sunflower page that fills in from top to bottom: connect once, copy the prompt, wait for the chat, published. The waiting state is shown beside it. Claude sits outside the window in its own cream colour and serif, labelled "Outside Aero".
- Works: four numbered rows read as progress without needing a stepper widget. The result card has a real thumbnail, the address, the version and Live.
- Unsure: the prompt set up the test too, so the button says "Share the test", not "Now test it". Check the real connector wording and whether "Connect once" is accurate for both Claude and ChatGPT.

## p5 Upload HTML or zip
- Idea: three states on the same sunflower canvas: drop (the file being dragged in), uploading (per-file progress), published (address, version, Live) with "Next: Test" in pink inside the card and "Now test it". Versions with roll back below.
- Works: the pink "Next: Test" corner is the hand-off moment: you see the next colour before you get there.
- Unsure: the "new link or keep the old test" choice when a site version changes needs a real rule.

## p6 Review across sessions
- Idea: "What to fix first" as big mint numbers, each with a count drawn as filled squares (4 of 5) and the quotes behind it, all playable. Themes, what worked and where testers disagreed on the right. A line says what it is based on (5 of 6, one had no audio).
- Works: the count squares are a mark of this direction and replace a percentage or a pill. It reads like a short report.
- Unsure: the counts are out of 5, not 6, which is honest but may confuse people. The first-run version (fewer than 2 sessions) isn't drawn.

## f1 Flow
- Idea: a colour stepper. Each step is the normal screen for that job, and the canvas colour says which of the three steps you're in. A seven-part bar under each frame fills in sunflower, pink, mint. The tester's screen and Claude are neutral because they aren't Aero.
- Works: you could follow the loop with the frames' words blurred, by colour alone.
- Unsure: seven frames at 184px are small; for the website it should become three groups (one per colour).

## m1 Marketing kit
- Idea: the same components, bigger, with one row instead of six, each on the wash of its step. Session card, friction quote, site card, test link and transcript line with player. Composed into a homepage hero (site card, test link, quote stacked in step order) and a 1200x630 card (three washes, one component each).
- Works: the social card explains the product in three colours and about twelve words. The hero needs no illustration.
- Unsure: the hero stack is the same order every time; for video the three should arrive one by one (sunflower, pink, mint), slowly.

## Into the shared design system
Tokens: three step hues with a wash, a gradient, a mid and a deep text colour each (`--sun-*`, `--pink-*`, `--mint-*`, `--g-pub/test/rev`), plus `--sel` for selection. One rule for components: a component never picks its own colour; it inherits the step of the canvas it sits on (a `data-step="publish|test|review"` on the container). That's what makes the same session card, site card or quote work in the app, on the website and in a video without changes. The marks (loop meter, count squares, session strip) become small shared components.
