# Team 2 (make): app UI round v2, notes

Files: `pages.html` (built by `build.py`; links `../shared/aero.css` unchanged, plus `extra.css`), `shoot-make.cjs` (saves `/home/claude/research/v2/hi/make-<id>.png`), `peek.cjs` (one PNG per frame, for checking). Every frame is shown in light, then the same frame in dark (`data-theme` on a wrapper). All windows are true 1440 x 900 `.win.full`. Example data: Kestrel Studio, Mia Chen, testers Maya, Tom, Priya, Jonas, Ana, Leo, all labelled Example.

## What changed from A, and why

- **Home "what's new" is a timeline of events, not a feed of cards.** Time, a mark on one vertical line, subject, one sentence, one action. Each kind has its own mark by shape: filled dot (session arrived), dashed ring (transcribing), struck ring (no audio), ring with a dot (review ready), green dot (published), ring (test made), three bars (visits), half-filled amber (offline soon, Free). There are no icon tiles and no stripes.
- **Sites and Tests are separate lists.** Sites are preview blocks (cached screenshot, name, address, Live / Private / time left on Free, visits, "Test: Pocket" when a test was copied from it). Tests are status lines (small preview, where it came from, link, session dots, last session, Open or Closed). A's tests table and the feed thumbnails are gone.
- **Sidebar:** the workspace name sits at the top with the collapse arrow. With only one site or one test, that item sits under Sites or Tests in the sidebar.
- **First run teaches by saying what appears and when** ("Seconds after you add it", "As soon as someone finishes", "About a minute after each session"), with a faint shape of each. It has two actions: the three ways in and "Open the example". A's "Connect once" row is gone, because the prompt flow has no connector.
- **The site page is one page.** There are no Overview, Versions, Domain or Settings tabs. The main column holds the preview, the address with Copy and Visit, a drop zone for a new version, and versions with roll back. The side column holds name, public switch, custom domain, favicon, badge, visits and "Test this site". Paid settings show their plan in small type instead of hiding.
- **"Test this site" says it makes a copy** (popover: own link, own versions, neither changes the other).
- **Create has one flow per source.** C's done-steps run down the left and round 5's radio choice comes first. A segmented switch (Upload / Prompt / Figma link) jumps to the other flow. No screen asks to publish before there is a file, a prompt or a link. Upload publishes on drop. Figma shows Publish only after the link is checked.
- **The prompt flow is a prompt.** You copy it with a scoped key into Claude or ChatGPT, then wait (the blue dot is the loader). Claude is shown separately, labelled "Outside Aero".
- **After upload the page wash takes a little of the site's own colours** (Checkout's green and peach, about 10 to 30% in light). It is quieter in dark.
- **Test setup and share are one tab.** The link card comes first on the right, because it already works when you arrive from "Now test it". It also has "Open as tester" (recorded as You), a taking-sessions switch, the test's own custom domain and favicon, and "What testers open" (the copy, with Upload to this test).
- **The tester start screen asks for a first name (optional) before any browser prompt.** It says what is recorded and who sees it. Then a separate permissions card: microphone, then this tab.
- **Task pill:** a full pill floating at the bottom. The words sit on a frosted plate (86% white, or 86% near-black in dark) so they read over any colour. V3 glass is used only on Done. It is shown over coral, black, yellow, busy stripes and white, and opened as a task card.
- **Marketing versions:** the site preview block, the test link card and the event rows (three events tell the loop). There is one homepage hero built only from them, in light and dark.
- **Fixed in our CSS:** the Checkout prototype's "Pay" button text was unreadable in the shared stylesheet (`.co .sum div` overrides `.co .pay`). The override lives in `extra.css`, so Team 1 may want it in `aero.css`.

## Open questions for Duane

1. **Home layout: A or B?** A puts the timeline first, with sites and tests beside it. B puts the sites row on top. I'd pick A.
2. **What does "Private" mean?** Password protection (Basic, per `PRICING-FACTS.md`), or signed-in only? This decides whether the public switch is on Free.
3. **Site visits on Home** need analytics (Solo). Is a daily "31 visits yesterday" event buildable from what we store?
4. **The test's own custom domain** (`test.kestrel.studio`, separate from the site's): is a second domain allowed on Solo?
5. **Test link form:** `aeroapp.ai/t/pocket-7k2` (as drawn) or `name.aeroapp.ai`?
6. **"Taking sessions" switch (Open / Closed):** new. Is it wanted?
7. **After "Now test it", which tab opens:** Setup (as drawn, link first) or Sessions?
8. **Does an "Open as tester" session (You) count against the session allowance?**
9. **Prompt key:** is a per-workspace key that can only publish, with "Make a new key", right?
10. **Example study:** should every account get a read-only Pocket example with 6 sessions?
11. **Figma link as a site:** keep it in New site, or offer Figma only under Tests (hosted in the test)?
12. **Site wash from the site's colours:** keep it, or use the colour only around the screenshot?
