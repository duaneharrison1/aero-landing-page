"""Words, tables and page furniture for the pages round board. version: 2026-10-26.1
Copy follows TONE_OF_VOICE: no em dashes, British spelling, sentence case. All names and numbers are Example data."""
from build_common import *

def sec(n, sid, title, lede, why, inner):
    return (f'<section class="scr pr-sec" id="{sid}"><div class="scr__head"><span class="scr__n">{n:02d}</span><div><h2>{title}</h2><p>{lede}</p></div>'
            f'<div class="scr__why">{why}</div></div>{inner}</section>')

def notes(blocks):
    return '<div class="notes">' + "".join(f'<div class="note{" eng" if k == "Engineer check" else ""}"><h4>{k}</h4><ul>{"".join("<li>" + v + "</li>" for v in vs)}</ul></div>' for k, vs in blocks) + '</div>'

def table(head, rows):
    return ('<table class="pr-table"><thead><tr>' + "".join(f"<th>{h}</th>" for h in head) + '</tr></thead><tbody>'
            + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows) + '</tbody></table>')

def page_pr(fname, title, desc, body):
    toc = "".join(f'<a href="#s{n}">{t}</a>' for n, t in [(1, "Shared pattern"), (2, "Site page"), (3, "Test page"), (4, "Placement"), (5, "Figma convert"), (6, "Upsell"), (7, "Visits"), (8, "Motion"), (9, "Decisions")])
    ctl = ('<div class="b-ctl"><label>Layout</label><span class="ae-seg"><span class="ae-seg__opt" data-set-lay="side">Side by side</span><span class="ae-seg__opt" data-set-lay="large">Large</span></span></div>')
    return f'''<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}">
<!-- version: 2026-10-26.1 -->
{FONTS}<link rel="stylesheet" href="tokens.css"><link rel="stylesheet" href="components.css"><link rel="stylesheet" href="board.css"><link rel="stylesheet" href="pages-round.css">
</head><body class="ae-kit">{sprite()}
<header class="b-top"><span class="ae-logo">Aero</span><nav>{toc}</nav>{ctl}</header>
<div class="b-wrap">{body}</div>
<script>try{{if(!localStorage.getItem('aeui-layout'))localStorage.setItem('aeui-layout','large')}}catch(e){{}}</script>
<script src="board.js"></script>
<script>(function(){{function auto(){{document.querySelectorAll('.fit').forEach(function(el){{if(el.classList.contains('is-natural'))return;var n=el.firstElementChild,w=+el.getAttribute('data-w')||1180;n.style.transform='none';n.style.width=w+'px';n.style.height='auto';var h=n.scrollHeight;el.setAttribute('data-h',h);}});if(window.aeFitAll)window.aeFitAll();}}
document.addEventListener('DOMContentLoaded',function(){{setTimeout(auto,50);setTimeout(auto,600);}});if(document.fonts&&document.fonts.ready)document.fonts.ready.then(auto);window.addEventListener('resize',function(){{setTimeout(auto,0)}});}})();</script>
<script src="glass-v3.js"></script>
</body></html>'''

HERO = '''<div class="b-hero"><div class="b-kicker">Aero app UI · pages round · 26 Oct 2026</div>
<h1>One pattern for the site page and the test page<span class="d">.</span></h1>
<p>A site and its test now share most of their settings, so they should look and behave the same. This board proposes one page skeleton (work on the left, a Settings rail on the right), a preview on the test page, a clear home for every update action, an honest Figma convert path, plans shown in place instead of banners, and a Visits section built only from the data the app has.</p>
<p class="ae-small">All names, addresses and numbers are Example data. Nothing here is built; every mockup uses the v3 kit. <span class="proposed">Proposed</span> marks work that does not exist yet. The recommended approach carries a black <span class="pick">Recommended</span> label.</p></div>'''

GLANCE = '<section class="scr" id="glance"><div class="scr__head"><span class="scr__n">00</span><div><h2>The answers in one table</h2><p>Duane’s seven questions, the short answer, and where it is on the board.</p></div><div class="scr__why">Details and the open choices are in the sections and in <b>Decisions for Duane</b>.</div></div>' + table(
    ["Question", "Recommendation", "Board"],
    [["1. Should tests and sites be consistent?", "Yes. Same skeleton and the same row pattern in a Settings rail, in the same order. Only the content of the rows differs (a site has an address and a domain, a test has tasks and recording).", '<a href="#s1">1</a>'],
     ["2. A preview on the test page?", "Yes. The site page’s preview component at its small size, at the top of Setup, plus a 52px thumbnail by the title on every tab. The snapshot pipeline already covers tests.", '<a href="#s3">3</a>'],
     ["3. Where do Test this site, Update with a prompt, Site source and Upload to this test go?", "Test this site: the Tests section and the ⋯ menu. The other three become one Update block (files, prompt, Figma link). Upload to this test is the same block on the test, writing to the test only.", '<a href="#s4">4</a>'],
     ["4. Figma “Convert with AI”", "It relies on the Figma connector, not on Dev Mode wording. The seat note is roughly right but incomplete. It is unfinished: label it as advanced and say what it gives (layout only), do not hide or promote it.", '<a href="#s5">5</a>'],
     ["5. Plan states and upsells", "Locked rows with the plan named, limits shown where they bite, and one card per page at most. The Free site page has six banners today.", '<a href="#s2">2</a> <a href="#s6">6</a>'],
     ["6. Visits", "Rebuild it from the six numbers, one chart and three lists the Plausible endpoint returns. Sentence case, flat, four headline numbers that switch the chart.", '<a href="#s7">7</a>'],
     ["7. Motion", "Opacity and transform only, three durations, nothing loops except skeletons, reduced motion removes movement and keeps the state change.", '<a href="#s8">8</a>']]) + '</section>'

# ---------------------------------------------------------------- 1
Q1_TITLE = "One settings pattern for sites and tests"
Q1_LEDE = "Both pages become the same skeleton: the work on the left, a Settings rail on the right. Rows are hairlines, not cards, as in the website demo that Duane likes."
Q1_WHY = "<b>Today</b> the site page has cards with all-caps labels and its own Save buttons; the test’s Setup is a stack of cards with a Save button and a debounced autosave. Two vocabularies for one idea."
Q1_ANATOMY = ('<div class="pr-answer"><h4>The row</h4><p>Title and one line of help on the left, one control on the right. Hairline between rows. No card per row.</p>'
              '<h4>How it saves</h4><ul><li>Switches save at once.</li><li>Text fields save when you leave them and show “Saved”.</li><li>Only an action with side effects has a button: a new password, connecting a domain, switching source.</li><li>The Setup tab loses its Save button.</li></ul>'
              '<h4 style="margin-top:12px">Order, top to bottom</h4><ul><li>Name</li><li>Link (a site’s address, a test’s link)</li><li>Access (password; taking new sessions)</li><li>Look (favicon, badge, domain) or Recording</li><li>Source</li></ul>'
              '<h4 style="margin-top:12px">Locked</h4><p>The same row, control at half strength, the plan named with a lock. Tapping opens the plans dialog in place.</p>'
              '<h4>Delete</h4><p>Only in the ⋯ menu, last, red, with a confirmation. The Danger zone card goes.</p></div>')
Q1_TABLE = table(["", "Same on both", "Genuinely different"], [
    ["Page", "Header bar with crumbs and actions, title, address or link, status, then work left and Settings right. Preview on top.", "Tests keep their tabs (Sessions, Insights, Setup) because reviewing is most of what you do there. A site is one page."],
    ["Settings", "Name. Link with Copy. An access switch. Source and how to update it. Same row, same order, same saving.", "Site: address, password, favicon, Aero badge, custom domain, versions, visits. Test: taking new sessions, record audio, record screen, difficulty rating, tasks, welcome and thank you."],
    ["Source", "“What it serves”: a version, who made it, how to replace it.", "A test is a copy pinned to a version. It updates with Upload to this test and never writes the site."],
    ["Left out of tests", "", "Custom domain and favicon (the demo shows them; the app has none). “Target responses” (Setup has it, the v3 mockups dropped it)."]])

# ---------------------------------------------------------------- 2
Q2_TITLE = "The site page on Free, Basic and Pro"
Q2_LEDE = "One page, one rail. What changes with the plan is the state of the rows, not the layout. Plans and limits are from PRICING-FACTS: Free has 3 test sessions and sites live 7 days; Basic adds your own aeroapp.ai address, password, favicon and no badge; Solo adds custom domain and analytics; Pro includes everything."
Q2_WHY = "<b>The problem today:</b> on Free the page shows a banner with Upgrade now under the address, domain, password, favicon and analytics blocks, plus a badge banner. Six prompts, none of them tied to something the person is trying to do."
Q2_NOTES = notes([
    ("Proposed", ["The Update block (three ways in) replaces Drop a new version, Publish automatically, Update with a prompt and the Site source row.", "Delete moves from a Danger zone card into ⋯.", "“Refresh preview” as a quiet link under the preview (the function exists).", "Download files in ⋯."]),
    ("Copy", ["“Offline in 5 days on Free”, never “expires”.", "Locked rows name the plan: Basic, Solo. No prices on these pages; the plans dialog keeps the regional price logic.", "Free card: “Free sites stay live 7 days. Your files are kept.”"]),
    ("Engineer check", ["The 7-day clock needs one source of truth for the days left (same number in the header, the card and the list).", "Confirm that paid sites have no expiry before the card says a plan keeps a site live. The card above does not say it.", "Locked rows reuse AeroFeatureGate’s tier check; only the presentation changes.", "Visits at Solo and above stays as the code has it."])])

# ---------------------------------------------------------------- 3
Q3_TITLE = "The test page, with a preview"
Q3_LEDE = "Tests are copies of a site. Their documents already carry previewUrl and previewColors from the snapshot pipeline (functions/preview/plan.js treats an HTML test, and a Figma test with a prototype link, as eligible), so the preview needs no new backend."
Q3_WHY = "<b>Duane:</b> “The site page has a preview, tests don’t.” The Tests list already shows one. The page is the only place that doesn’t."
Q3_NOTES = notes([
    ("Proposed", ["Preview on Setup: <code>AeroSitePreview</code> at size sm, on the Test wash, captioned “Screenshot · v3 · pinned”.", "A 52px thumbnail beside the title on every tab (B).", "“Use the site’s latest (v4)” next to Upload to this test, with the existing confirm once sessions exist.", "A ⋯ menu on the test page (it has none).", "Setup autosaves; the Save button goes."]),
    ("Copy", ["“What testers open”, not “Prototype source”.", "“Screenshot”, never “live”: it is a picture, Preview as tester is the real thing.", "Over the limit: “New sessions can't start until you delete one or move to a bigger plan.” Wording waits on Decision 8."]),
    ("Engineer check", ["A test copy captures from its own address, so Upload to this test re-captures by itself. Check the capture follows the pinned version.", "A password-gated site clears its preview; show the initial on the default wash, as decided on 25 Oct.", "Figma tests use Figma’s public link preview, no per-user token.", "Truth rules held: no cursor anywhere, nothing typing, the transcript is shown as arriving."])])

# ---------------------------------------------------------------- 4
Q4_TITLE = "Where each action lives"
Q4_LEDE = "Four actions overlap today. Each gets one home, and the ⋯ menu holds actions on the whole thing, never settings."
Q4_WHY = "<b>Rule of thumb:</b> the header holds what you do every day (copy, visit, preview). Sections hold the work. The rail holds settings. ⋯ holds rare and destructive actions."
Q4_TABLE = table(["Action", "Home", "Also", "Not here"], [
    ["Test this site", "Tests section on the site page, as a button in the section head (the loop: publish, then test)", "⋯ menu, first item (“Open its test” once one exists), as in the demo. Sites list card ⋯ as today.", "Header primary (that stays Copy address and Visit); Settings"],
    ["Update with a prompt", "Update block, middle tile", "Phone: same block, tiles stack", "⋯ menu; a separate settings row"],
    ["Site source (switch to Figma)", "Update block, third tile “Use a Figma link”, with the lossless-switch confirm", "A Figma site shows “Switch to uploaded files” in the same tile", "Settings rail (it is an act of publishing, not a setting)"],
    ["Upload to this test", "“What testers open” on the test’s Setup: the same drop zone as the site, writing to the test only", "“Use the site’s latest” next to it; the From link in the header goes back to the site", "The site page (it must never write the test’s version)"],
    ["Publish uploads straight away", "Under the Update tiles (it describes what an upload does)", "", "Settings rail"],
    ["Delete", "⋯ menu, last, red, confirm dialog", "Sites and Tests list card ⋯ as today", "A Danger zone card"]])
Q4_NOTES = notes([
    ("Proposed", ["⋯ on the test page: Preview as tester, Copy test link, Open the site, Duplicate test, Delete test.", "Update block on the site; the test gets the same tiles it can honour (files today; the prompt tile needs the agent to target a test copy).", "Download files (site ⋯)."]),
    ("Copy", ["Plain verbs, no “…”: “Test this site”, “Get prompt”, “Choose files”, “Switch source”.", "“Delete test” confirm: “Its sessions and recordings are deleted too.”"]),
    ("Engineer check", ["testMenuItem already returns “Test this site” or “Open its test”; the header ⋯ is wired.", "The prompt tile on a test copy has no backend: AgentPublishModal targets a site id. Ship files first.", "The site must never be written by a test upload (testCopy.js already keeps it that way)."])])

# ---------------------------------------------------------------- 5
Q5_TITLE = "Figma “Convert with AI”: what it does today"
Q5_LEDE = "In plain words: Aero writes a prompt, you paste it into Claude or ChatGPT, that chat reads your Figma frame through the Figma connector, writes one HTML file and uploads it to Aero with a web request. Aero does nothing smart itself."
Q5_WHY = "<b>Verdict:</b> half finished. Aero’s side works as written. The result is a plain page, not your prototype, and nobody on the team has recorded it running end to end. Label it, do not promote it."
Q5_TABLE = table(["Question", "What the code says", "What Figma says (sources below)"], [
    ["Does it use Figma’s Dev Mode MCP server?", "No such wording anywhere. <code>buildAgentPrompt</code> in CreateFlow.js opens with “Read my Figma design at (link) using the Figma connector.” The screen tells you to add “the Figma connector” (Claude: claude.ai/customize/connectors) or “the Figma integration” (ChatGPT: Settings, Apps).", "Figma’s MCP server has a remote version at mcp.figma.com/mcp that needs no desktop app, and a desktop version. The connector is almost certainly the remote one; I could not open Claude’s connector listing to confirm."],
    ["Where does “needs a paid Figma seat” come from?", "Only from Aero’s own copy, written twice (CreateFlow.js, FigmaLinkModal.js). Nothing checks it.", "Rate limits: View and Collab seats get 20 tool calls a month on every plan. Full and Dev seats get 200 a day on Professional (more on Organization and Enterprise). On Starter, Full and Dev are not available. So it is roughly right, but the wording should say Dev or Full seat on a paid plan."],
    ["Does it work end to end?", "Aero’s half reads correctly: the copy saves a draft and makes a publish key, the prompt carries a curl upload, the page watches the draft and flips to live. No test covers it and convert is not counted in creation stats.", "Not run by me: it needs a paid Dev or Full seat and a chat with a shell. Treat it as unverified."],
    ["What comes out?", "The prompt asks for one self-contained, responsive index.html, CSS inline, solid colours where images were.", "Design context only: layout, variables, components. No prototype flows, so a tester cannot click through your Figma prototype."],
    ["Who can run it?", "Copy says claude.ai, Claude Code and Cowork “all use the same prompt”. The prompt needs a shell and network to curl.", "A plain chat without code execution may not be able to upload. Unverified."]])
Q5_NOTES = notes([
    ("Recommended: B, label it", ["Rename to “Build real code from your design” with an Advanced tag, said plainly: one frame, layout only, images become colour blocks, Dev or Full seat on a paid plan.", "Keep it under Other ways, beside the plugin export. Embedding the prototype stays the first path.", "Name Claude and ChatGPT once, on the way in; AI is not the label."]),
    ("To finish it (not recommended now)", ["Run it on five real files with a paid seat and record the result.", "Ask the agent to run Figma’s whoami first and say if the seat is a View seat.", "Handle images, and give the page a check that the upload really arrived.", "Count it in creation stats."]),
    ("Engineer check", ["Copy lives in two places: CreateFlow.js and FigmaLinkModal.js. Change both.", "BuildWithAI only checks that the link is not empty; it accepts a design link, which is right here (embed needs a proto link)."])])

# ---------------------------------------------------------------- 6
Q6_TITLE = "Plans in place, not banners everywhere"
Q6_LEDE = "Figmafolio’s upsells are good because each one sits on the exact feature: the real control greyed out, a benefit headline such as “Need to keep things confidential?”, one button that opens the plans dialog in place. Aero copied that block, but its one-page site has six gated blocks, so the pattern became a wall."
Q6_WHY = "<b>Recommendation (A):</b> a locked row with the plan named, limits shown where they bite, and at most one card per page, only when something real is running out."
Q6_TABLE = table(["Who", "What they do (as documented)", "What to take from it"], [
    ["Figmafolio (this codebase)", "<code>FeatureGate</code>: greyed live control, then a CTA row (headline, benefit line, Upgrade now). Used on password, favicon, custom domain, address rename, analytics (blurred sample), and “Session limit reached” with the next plan’s allowance. The Figmafolio user-testing tab also carries an Aero card (replay mini, three features, Try on Aero).", "Contextual, outcome-led, one or two per page. Keep the greyed real control; drop the per-block banner."],
    ["Vercel", "Hobby and Pro compared in one table with included usage per resource; upgrade from Settings, Billing; Pro trial. Password protection is a paid add-on.", "Plan facts in one place; the upgrade path is a single door."],
    ["Maze", "A trial ends after 30 days or 3 studies. After it, premium blocks stay in existing drafts but cannot be added.", "A limit stated as a count, and the person’s work is kept."],
    ["Loom", "Starter is stated as 25 videos per person and 5 minutes per recording; Business offers Try for free.", "Limits are concrete numbers, not “limited”."],
    ["Netlify", "Free has a hard cap of 300 credits a month; features are marked N/A on lower plans; plans change under Usage and billing.", "A declared hard limit beats a surprise."],
    ["Lyssna", "Free: 15 self-recruited responses; higher plans read “Everything in Free, plus”.", "Say what is in, then what is added."],
    ["Framer", "Plans attach to each site; a custom domain needs a paid site plan; “Running low? Upgrade a site”.", "Upgrade is scoped to the thing you are looking at, like Aero’s per-site view."],
    ["SaaS UX writing", "saasui.design: an inline lock with a one-line reason, a usage meter before the limit, “gate the action, not the session”; a banner on every page regardless of intent trains people to ignore paywalls.", "The principle behind A."]])
Q6_NOTES = notes([
    ("Caveat", ["I read documentation and pricing pages, not logged-in screens. Where a product’s in-app lock or banner is not described in its docs, I do not claim it. Webflow’s help page could not be opened and is not used."]),
    ("Rules for A", ["A locked row looks like a normal row, half strength, with the plan and a lock. Tapping it opens the plans dialog in place.", "One card per page at most, only for a real clock or limit (7 days left; sessions at the limit). It disappears when the condition clears.", "Never in the header, never on a session or review screen (reading), never twice, never a banner under every block.", "Prices stay out of these pages. The dialog keeps the regional logic."]),
    ("Engineer check", ["<code>AeroFeatureGate</code> keeps its tier check; the banner it renders is replaced by the row treatment.", "Session limit comes from the same count as the sidebar meter. Do not write “a month” after counts (PRICING-FACTS)."])])

# ---------------------------------------------------------------- 7
Q7_TITLE = "Visits"
Q7_LEDE = "The Visits block looks out of place because it is the old Figmafolio analytics component dropped in: a second “Analytics” title inside “Visits”, all-caps labels, a six-tile grid and its own period menu. The data behind it is good; the shape is wrong."
Q7_WHY = "<b>Rule:</b> use only what the app has. That is a Plausible query per site, not Firestore, and not test sessions."
Q7_TODAY = ('<div class="pr-answer"><h4>What the app has today (read from the code)</h4><ul>'
            '<li><b>Source:</b> Plausible, one shared account, filtered to the site’s own hostnames (its aeroapp.ai address and its custom domain). The tracking script is added to served pages by api/site.js. Nothing about visits is stored in Firestore.</li>'
            '<li><b>Endpoint:</b> /api/plausible, one call per metric, owner checked from the signed-in token.</li>'
            '<li><b>Periods:</b> today, 7 days, 30 days, this month, 12 months.</li>'
            '<li><b>Numbers:</b> visitors, visits, pageviews, views per visit, bounce rate, visit duration, each with its change against the previous period.</li>'
            '<li><b>Over time:</b> visitors, visits, pageviews, bounce rate and duration, by hour for Today, by day, by month for 12 months.</li>'
            '<li><b>Lists:</b> sources, countries, cities, devices, browsers, operating systems (visitor counts only). A pages list exists in the API; the screen dropped it.</li>'
            '<li><b>Gate:</b> Solo and Pro.</li>'
            '<li><b>Not there:</b> which tester saw what, events or goals, per-page paths in the UI, anything about test sessions. The new design shows none of these.</li></ul></div>')
Q7_MAP = table(["On the screen", "Data", "Endpoint metric"], [
    ["Four headline numbers (they also switch the chart)", "Visitors, visits, pageviews, visit duration, with “+18% on the previous 7 days”", "overview, timeseries"],
    ["One line under the chart", "Views per visit, bounce rate", "overview"],
    ["Chart", "The chosen metric by hour, day or month", "timeseries"],
    ["Where from", "Top sources by visitors (Direct / None kept as it comes)", "sources"],
    ["Where", "Countries and cities, one tab each", "countries, cities"],
    ["Devices", "Devices, browsers and operating systems, one tab each", "devices, browsers, os"],
    ["Period control", "Today, 7 days, 30 days; “This month” and “12 months” in the small menu", "period"]])
Q7_NOTES = notes([
    ("Proposed", ["Sentence case and Geist throughout; no “Analytics” title inside “Visits”.", "Locked on Free and Basic as a plain skeleton with no sample numbers, naming Solo.", "A line saying these are visits to the live site, not tester sessions."]),
    ("Copy", ["“Time on site”, “Where from”, “Where”. No jargon: bounce rate stays because the data has it, in the quiet line.", "“No visits yet. They show here once someone opens the site. Your own visits count too.”", "Change text uses a neutral grey, no red or green: a falling bounce rate is good news."]),
    ("Engineer check", ["No new endpoint. The six calls become the same eight the component already makes.", "Rebuild as an Aero component under .ut-theme and add it to AeroShowcase; retire the Figmafolio Analytics.css use on Aero pages only (Figmafolio keeps its own).", "Keep the owner token check. Cache the last answer and refresh behind it."])])

# ---------------------------------------------------------------- 8
Q8_TITLE = "Motion"
Q8_LEDE = "Small and quiet, from the three tokens in tokens.css: 120ms, 220ms and 420ms with the standard ease. Only opacity and transform move."
Q8_WHY = "<b>Truth rules hold:</b> no moving cursor, nothing typing while a session runs, transcripts arrive and fade in."
Q8_TABLE = table(["Element", "What moves", "Duration", "Reduced motion"], [
    ["Switch", "The thumb slides, the track changes colour. The row never moves.", "220ms (dur-2)", "Instant"],
    ["“Saved” after a field", "Fades in, stays 2 seconds, fades out", "220ms in, 120ms out", "Appears and disappears with no fade"],
    ["Preview snapshot", "Fades in over its wash when loaded; the wash never changes colour in front of you", "220ms", "Appears at once"],
    ["New preview after an upload", "Cross-fades once the new snapshot exists; until then the old one stays with “Preview updating”", "420ms (dur-3)", "Swaps at once"],
    ["Loading shapes", "Grey shapes from the real layout, a slow shimmer", "1.4s loop (dur-skel)", "Static grey, no shimmer"],
    ["Visits bars", "Rise from the baseline once, staggered by 30ms, when data first arrives. A period change morphs the heights; opening the page animates nothing else.", "420ms, 220ms on change", "Bars appear at final height"],
    ["Stat tile selected", "The underline and the chart change together", "120ms", "Instant"],
    ["New session in the list", "Fades in and the “N new” count changes. No slide, no highlight flash", "220ms", "Appears at once"],
    ["The one upsell card", "Present when the page loads, no entrance. Fades out when its condition clears.", "120ms out", "Disappears at once"],
    ["Locked row tapped", "The plans dialog opens in place: fade and 8px rise (a bottom sheet on a phone)", "220ms", "Fade only"],
    ["⋯ menu", "Fade and 4px", "120ms", "Fade only"],
    ["Processing and recording dots", "The existing pulse and spinner", "1.6s loop", "Dot stays, no pulse"]])

# ---------------------------------------------------------------- 9
DEC_LEDE = "Eleven choices. My pick is first in each, so a plain yes to all of them is a clean brief."
DEC_WHY = "Everything above is a proposal; nothing is built. Decisions are not written into DECISIONS.md until you make them."
DECISIONS = '<ol class="pr-decisions">' + "".join(f"<li><b>{a}</b><span>{b}</span></li>" for a, b in [
    ("Use one skeleton and one Settings rail on both pages, with delete moved into ⋯?", "Yes (recommended) or keep the two pages separate."),
    ("Test preview: B, the site page’s preview at the top of Setup plus a thumbnail by the title?", "Or A, the small thumbnail in the rail that the website demo shows today."),
    ("Tests get no custom domain or favicon rows, and the hero demo drops them?", "Yes (recommended: a tester never sees either) or build them for tests."),
    ("Merge Drop a new version, Publish automatically, Update with a prompt and Site source into one Update block?", "Yes (recommended). The test gets files first; the prompt tile needs new backend work."),
    ("Add Download files and Duplicate test to the ⋯ menus?", "Both are new. Download files is in the demo; build it or take it out of the demo."),
    ("Convert with AI: label it (recommended), hide it, or finish it?", "Label means new copy in two files and a rename. Finishing needs a paid Figma seat to test."),
    ("Upsells: locked rows plus at most one card per page?", "Yes (recommended) or the plan summary card (C). The Free site page drops from six banners to one card."),
    ("What happens at the session limit: stop new sessions, or record and hide them until an upgrade?", "Open since the first UI round. The card copy depends on it."),
    ("Visits: keep it at Solo and above, and show Free and Basic a plain locked skeleton with no sample numbers?", "Yes (recommended)."),
    ("Remove “Target responses” from Setup and drop the Save button in favour of autosave?", "Yes (recommended). It is in the code; the v3 mockups dropped it."),
    ("Before the card says paid plans keep a site live, confirm that paid sites never go offline?", "The mockup avoids the claim. PRICING-FACTS only says Free sites stay live 7 days.")]) + '</ol>'

SOURCES = ('<h3 class="states-h">Sources</h3><div class="pr-src"><ul>'
           '<li>Figma, <a href="https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server">Guide to the Figma MCP server</a> (remote server at mcp.figma.com/mcp; plans and seats).</li>'
           '<li>Figma, <a href="https://developers.figma.com/docs/figma-mcp-server/rate-limits-access/">Rate limits and access</a> (20 calls a month for View and Collab seats; Full and Dev 200 a day on Professional; not available on Starter).</li>'
           '<li>saasui.design, <a href="https://www.saasui.design/blog/saas-upgrade-paywall-ux-patterns">SaaS upgrade and paywall UX patterns</a>.</li>'
           '<li>Vercel, <a href="https://vercel.com/docs/plans/hobby">Hobby plan</a>. Maze, <a href="https://help.maze.co/hc/en-us/articles/28513024118547-Maze-free-trials">Free trials</a>. Loom, <a href="https://www.loom.com/pricing">Pricing</a>. Lyssna, <a href="https://www.lyssna.com/pricing/">Pricing</a>. Framer, <a href="https://www.framer.com/pricing/">Pricing</a>. Netlify, <a href="https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-credit-based-plans/credit-based-pricing-plans/">Credit-based plans</a>.</li>'
           '<li>In this repo: src/pages/AeroSites/SiteOnePage.js, tabs/SiteSettingsTab.js, tabs/SiteDomainTab.js, tabs/SiteAnalyticsTab.js, FigmaLinkModal.js; src/pages/UserTesting/tabs/UTSetupTab.js, components/TestDetailHead.js; src/components/CreateFlow/CreateFlow.js, BuildWithAI.js; src/components/Aero/AeroFeatureGate.js; src/components/FeatureGate; src/components/Analytics/Analytics.js; api/plausible.js; functions/preview/plan.js.</li>'
           '</ul></div>')
