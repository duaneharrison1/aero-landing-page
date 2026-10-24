from build_screens import *  # reuses every screen piece (builds screens.html too)

def claude_window(state="sent"):
    """Simplified Claude, clearly outside Aero: its own colours, serif reply text, labelled."""
    msgs = (f'<div class="ae-outside__me">Make a payments prototype called Pocket: balance, send money, cards.</div>'
            f'<div class="ae-outside__bot">Here is Pocket. It has a home screen with the balance, a Send flow and Cards under More.</div>')
    if state in ("sent", "done"):
        msgs += f'<div class="ae-outside__me">Put this prototype online with Aero and reply with the live link. Name: Pocket. <span style="opacity:.6;font-family:var(--ae-mono);font-size:11px">key: ae_1f…c9</span></div>'
    if state == "sent":
        msgs += '<div class="ae-outside__tool">Using Aero: publish_site…</div>'
    if state == "done":
        msgs += '<div class="ae-outside__tool">Used Aero: publish_site</div><div class="ae-outside__bot">Pocket is live at <u>pocket.aeroapp.ai</u>. Version 1, published just now.</div>'
    inner = (f'<div style="flex:1;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);background:#F5F4EE;font-family:ui-serif,Georgia,serif;color:#2B2A26">'
             f'<div style="padding:22px 26px;display:flex;flex-direction:column;gap:14px;border-right:1px solid #E6E3D8"><div class="ae-outside__bar" style="font-size:13px"><span class="ae-outside__logo"></span>Claude<span style="margin-left:auto;font-family:var(--ae-mono);font-size:10.5px;letter-spacing:.08em;text-transform:uppercase">Simplified · not Aero</span></div>{msgs}'
             f'<div style="margin-top:auto;border-radius:16px;background:#fff;box-shadow:0 0 0 1px #E0DCCF;padding:14px 16px;font-family:var(--ae-font);font-size:13px;color:#8A8676">Reply to Claude…</div></div>'
             f'<div style="display:grid;place-items:center;background:#EFEDE5"><div style="display:flex;flex-direction:column;align-items:center;gap:10px"><span style="font-family:var(--ae-font);font-size:12px;color:#6B675C">Pocket · artifact</span>{proto()}</div></div></div>')
    return f'<div class="ae-window" style="flex:1"><div class="ae-window__bar" style="background:#EAE7DC;border-color:#E0DCCF"><span class="ae-window__dots"><i></i><i></i><i></i></span><span class="ae-window__url">{i("lock","ae-i--sm")}claude.ai/chat</span><span style="width:46px"></span></div><div class="ae-window__fill">{inner}</div></div>'

def frame(inner, url, outside=False, w=1180, h=760):
    win = inner if outside else window(url, inner)
    tag_ = '<span class="outside-tag">Outside Aero · Claude</span>' if outside else ""
    cls = "outside-frame" if outside else ""
    return f'<div class="flow__frame"><div style="position:relative" class="{cls}">{tag_}{fitbox(win, w, h)}</div></div>'

def flow(fid, title, lede, steps, rng=(0, 100)):
    frames = "".join(frame(s["inner"], s.get("url", "aeroapp.ai"), s.get("outside", False)) for s in steps)
    lis = "".join(f'<li><span class="k">{k+1:02d}</span><span>{E(s["name"])}<span class="w{" out" if s.get("outside") else ""}">{"Outside Aero" if s.get("outside") else s.get("where","Aero")}</span></span></li>' for k, s in enumerate(steps))
    caps = "".join(f'<div class="flow__cap flow__capt"><h4>{E(s["name"])}</h4>{s["cap"]}</div>' for s in steps)
    return (f'<section class="flow" id="{fid}" tabindex="0" data-from="{rng[0]}" data-to="{rng[1]}"><div class="flow__head"><h2>{E(title)}</h2><div class="flow__nav">{btn("","secondary",icon="left",extra="ae-btn--icon",attrs="data-prev aria-label=\"Previous\"")}<span class="flow__count"></span>{btn("Next","primary",True,icon_after="right",attrs="data-next")}</div></div>'
            f'<p class="ae-p" style="margin:-6px 0 16px;max-width:760px">{lede}</p>'
            f'<div class="flow__stage"><div><div class="flow__frames">{frames}</div><div class="flow__line"><div class="ae-flowline"><span class="ae-flowline__fill" style="width:0"></span></div><div class="labels"><span>Publish</span><span>Test</span><span>Review</span><span>From prompt to first session</span></div></div></div>'
            f'<aside class="flow__side"><ol class="flow__steps">{lis}</ol>{caps}</aside></div></section>')

# ---------------------------------------------------------------- flow 1: publish from a prompt
home_empty = app(head("Good morning, Mia", None, "", new_btn("New")) + body(section("Tests", tests_list()[:0] + f'<div class="ae-empty ae-empty--line" style="padding:20px"><div class="ae-small">No tests yet.</div></div>') + section("Sites", '<div class="ae-small">No sites yet.</div>')), "sidebar", "home")
create_copied = create_a.replace(btn("Copy","primary",True,size="sm",icon="copy"), btn("Copied","primary",size="sm",icon="check",extra="is-done"))
waiting_f = wait.replace("Waiting for Claude to publish", "Waiting for Claude to publish")
live_toast = '<div style="position:absolute;left:50%;bottom:24px;transform:translateX(-50%);z-index:90"><span class="ae-toast">' + i("check") + 'pocket.aeroapp.ai is live</span></div>'
done_f = done.replace('</div></div>', '</div></div>', 1)
site_new = app(head("Pocket", ["Sites", "Pocket"], f'<span class="ae-area ae-area--publish">Publish</span>{status("Live","live")}<span>v1 · published just now from Claude</span><span style="color:var(--ae-warn)">Offline in 7 days on Free</span>', site_actions, "publish") + tabs(SITE_TABS, "Overview") + site_overview().replace("5 of 7", "7 of 7").replace("Mon 28 Oct", "Wed 30 Oct").replace("3 sessions · review ready · pinned to v3", "Watch people use it, with one link").replace('<div class="ae-strong">Pocket</div>', '<div class="ae-strong">No test yet</div>').replace("Open test", "Run a test on this site").replace("6 · 412 KB", "6 · 398 KB"), "sidebar", "sites")
F1 = [
    {"name": "Start from Home", "url": "aeroapp.ai/home", "inner": home_empty, "cap": "<p>Mia has built Pocket in Claude. In Aero she clicks <b>New</b>. Nothing is saved yet.</p>"},
    {"name": "Choose one prompt and copy it", "url": "aeroapp.ai/new", "inner": create_copied, "cap": "<p>One prompt is picked. She names it Pocket (address pocket.aeroapp.ai) and copies the prompt. <b>Copying is the moment a draft is saved</b> (proposed rule B7).</p><p class='ae-small'>The prompt carries a one-time key, so the chat can publish to her account.</p>"},
    {"name": "Paste it into Claude", "outside": True, "inner": claude_window("sent"), "cap": "<p>She pastes it into the chat where Pocket was built. Claude calls Aero's publish tool with the files.</p><p class='ae-small'>Claude's interface is drawn simplified and labelled. It is never inside Aero's frame. First time only: Claude asks her to connect Aero.</p>"},
    {"name": "Aero is waiting", "url": "aeroapp.ai/new", "inner": waiting_f, "cap": "<p>Back in Aero, the page waits and updates on its own. If she closes it, the site still appears under Sites.</p>"},
    {"name": "Claude replies with the link", "outside": True, "inner": claude_window("done"), "cap": "<p>Claude confirms: live at pocket.aeroapp.ai, version 1. Seconds to a minute.</p>"},
    {"name": "It's live, now test it", "url": "aeroapp.ai/new", "inner": app(head("Pocket is live", ["Home", "New"], "", "", "publish") + body(f'<div style="max-width:620px;margin:0 auto;width:100%" class="ae-stack ae-stack--loose"><div class="ae-copy ae-copy--lg"><span class="ae-copy__url">pocket.aeroapp.ai</span>{btn("","ghost",icon="copy",extra="ae-btn--icon")}{btn("Open","secondary",icon="out")}</div>{progress(1)}<div class="ae-card" style="padding:18px;display:flex;gap:14px;align-items:center"><span class="ae-source-tile__icon" style="background:var(--ae-test-tint);color:var(--ae-test-ink)">{i("tests")}</span><span style="flex:1"><div class="ae-strong">Now test it</div><div class="ae-small">Add a few tasks, or let people explore. You get one link to share.</div></span>{btn("Create a test","primary",True)}</div><div class="ae-small">Free sites stay live 7 days. <a class="ae-link">Keep it live from $3</a></div></div>'), "sidebar", "home", overlay=live_toast), "cap": "<p>The page turns into the result: the address, the Publish, Test, Review line, and one next step. <span class='proposed'>Proposed</span></p>"},
    {"name": "The site page", "url": "aeroapp.ai/sites/pocket", "inner": site_new, "cap": "<p>Under Sites: live, version 1, offline in 7 days on Free, and <b>Run a test on this site</b>. Updating is a drop or another prompt; every update is a version.</p>"},
]

# ---------------------------------------------------------------- flow 2: create and share a test
test_create = app(head("New test", ["Sites", "Pocket", "New test"], f'<div class="ae-stepper"><span class="ae-stepper__step is-done"><span class="ae-stepper__n">{i("check","ae-i--sm")}</span>pocket.aeroapp.ai</span><span class="ae-stepper__step is-now"><span class="ae-stepper__n">2</span>What testers try</span><span class="ae-stepper__step"><span class="ae-stepper__n">3</span>Share</span></div>', btn("Cancel", "ghost")) + body(
    f'<div style="display:grid;grid-template-columns:minmax(0,1fr) 280px;gap:28px"><div class="ae-stack ae-stack--loose">{setup_left}<div class="ae-row-gap" style="justify-content:flex-end">{btn("Create test","primary",True)}</div></div>{preview}</div>'), "sidebar", "tests")
explore_choice = test_create.replace('<span class="ae-seg__opt is-active">Tasks</span><span class="ae-seg__opt">Explore freely</span>', '<span class="ae-seg__opt">Tasks</span><span class="ae-seg__opt is-active">Explore freely</span>')
share_landed = app(test_head("Share", 0, btn("", "ghost", icon="more", extra="ae-btn--icon"), st=status("Waiting for testers", "draft")) + body(
    f'<div class="ae-card ae-card--test" style="padding:26px;display:grid;grid-template-columns:minmax(0,1fr) auto;gap:28px;align-items:center"><div class="ae-stack"><div class="ae-h2" style="font-weight:350;font-size:24px">Your test link is ready<span style="color:var(--ae-blue)">.</span></div>'
    f'<div class="ae-copy ae-copy--lg" style="background:rgba(255,255,255,.75)"><span class="ae-copy__url">pocket.aeroapp.ai/t/8kq2</span>{btn("Copied","primary",extra="is-done",icon="check")}</div>'
    f'<div class="ae-row-gap">{btn("Open as a tester","secondary",True,icon="out")}<span class="ae-small">Send it to 3 to 5 people. They open it in their browser, nothing to install.</span></div></div><div class="ae-stack ae-stack--tight" style="align-items:center">{qr()}<span class="ae-small">For phones</span></div></div>'
    f'<div class="ae-grid ae-grid--3"><div class="ae-card ae-card--pad ae-stack ae-stack--tight"><div class="ae-label">What is recorded</div>{recorded}</div><div class="ae-card ae-card--pad ae-stack ae-stack--tight"><div class="ae-label">On a phone</div><div class="ae-small">Figma prototypes record voice only. HTML sites ask testers to switch to a laptop.</div></div><div class="ae-card ae-card--pad ae-stack ae-stack--tight"><div class="ae-label">After each session</div><div class="ae-small">It appears under Sessions. The transcript follows about a minute later.</div></div></div>'), "sidebar", "tests", overlay=toast.replace("Test created. Link copied.", "Test created. Link copied."))
tester_hand = (f'<div class="ae-app" style="background:#0E0E10;display:grid;place-items:center"><div style="display:flex;flex-direction:column;gap:14px;align-items:center;color:#fff;text-align:center;max-width:520px">'
               f'<span class="ae-outside-label" style="color:#A1A1A8">Tester view · designed in the tester flow</span><div style="font-size:26px;font-weight:350;letter-spacing:-.02em">Tester B opens pocket.aeroapp.ai/t/8kq2 on her own laptop</div>'
               f'<div style="font-size:14px;color:#C7C7CC;line-height:1.6">Welcome from Mia, one permission step (mic and the tab to share), the two tasks in a small panel over Pocket, then the thank-you. Sunday, 11:40. She takes 7 minutes 12.</div>'
               f'<div style="position:relative;margin-top:8px;padding:20px 30px;border-radius:16px;background:#1C1C1F;display:flex;gap:24px;align-items:center">{proto("sm")}<div class="ae-taskpanel" style="width:240px;text-align:left"><div class="ae-taskpanel__top"><span class="ae-label">Task 2 of 2</span><span class="ae-spacer"></span><span class="ae-rec">03:08</span></div><div class="ae-taskpanel__task">Find your cards</div></div></div></div></div>')
sess_recording = app(test_head("Sessions", 1, btn("Copy link", "secondary", icon="copy")) + body(sessions_list([{"n": 1, "who": "Tester B", "av": "b", "dev": "Laptop · Chrome", "len": "03:08", "status": "recording", "quote": ""}]) + '<p class="ae-small" style="margin:0">Recording now. It flips to "Transcript arriving" when she finishes.</p>'), "sidebar", "tests")
sess_proc = app(test_head("Sessions", 1, btn("Copy link", "secondary", icon="copy")) + body(sessions_list([{"n": 1, "who": "Tester B", "av": "b", "dev": "Laptop · Chrome", "len": "07:12", "status": "processing", "quote": ""}])), "sidebar", "tests")
F2 = [
    {"name": "Run a test on this site", "url": "aeroapp.ai/sites/pocket", "inner": site_new, "cap": "<p>From the site page, the one glass button. (Also from Home's \"Now test it\", or New, then Test an existing site.)</p>"},
    {"name": "What testers try", "url": "aeroapp.ai/tests/new", "inner": test_create, "cap": "<p>Two tasks, a welcome and a thank-you. Screen and voice on. The preview shows the tester's first screen. Pinned to the version live now.</p>"},
    {"name": "Or: explore freely", "url": "aeroapp.ai/tests/new", "inner": explore_choice, "cap": "<p>With no tasks, testers get one open prompt and decide when they are done. The tester never sees \"0 tasks\" (B15).</p>"},
    {"name": "Land on Share, link copied", "url": "aeroapp.ai/tests/pocket/share", "inner": share_landed, "cap": "<p><b>The Share tab opens</b>, not Setup, with the link already copied. One link, a QR code, and what is recorded. <span class='proposed'>Proposed</span></p>"},
    {"name": "Someone else takes it", "where": "Tester", "inner": tester_hand, "url": "pocket.aeroapp.ai/t/8kq2", "cap": "<p>On her own computer. The tester screens are designed in the tester flow (screen 10). Only the tab she picks and her voice are recorded.</p>"},
    {"name": "Recording now", "url": "aeroapp.ai/tests/pocket/sessions", "inner": sess_recording, "cap": "<p>Mia sees Session 1 appear live. Numbered from the first one, so it stays Session 1.</p>"},
    {"name": "Transcript arriving", "url": "aeroapp.ai/tests/pocket/sessions", "inner": sess_proc, "cap": "<p>She finished at 07:12. The transcript follows, usually about a minute. Nothing types live.</p>"},
]

# ---------------------------------------------------------------- flow 3: review results
sess_play = sess_a
jumped = sess_a.replace('data-jump="188000" class="ae-friction is-active"', 'data-jump="188000" class="ae-friction"').replace('data-jump="161000" class="ae-friction"', 'data-jump="161000" class="ae-friction is-active"')
one_more = rev_a
F3 = [
    {"name": "Home says what's new", "url": "aeroapp.ai/home", "inner": home_a, "cap": "<p>\"2 new sessions on Pocket\" and \"Review ready for Pocket\". Clicking opens where the action is: Sessions, or Review.</p>"},
    {"name": "The sessions", "url": "aeroapp.ai/tests/pocket/sessions", "inner": app(test_head("Sessions", 3, btn("Copy link", "secondary", icon="copy")) + body(sessions_list()), "sidebar", "tests"), "cap": "<p>Session 3 is still being transcribed; 1 and 2 are ready, each with its first line in their words.</p>"},
    {"name": "Watch and read Session 2", "url": "aeroapp.ai/tests/pocket/sessions/2", "inner": sess_play, "cap": "<p>The recording is on the page. Press play: the transcript follows word by word from the stored timings. No cursor on the recording, because a tab recording has none. <span class='proposed'>Inline player</span></p>"},
    {"name": "Jump to a friction point", "url": "aeroapp.ai/tests/pocket/sessions/2", "inner": jumped, "cap": "<p>\"Send flow has no back label\" jumps to 02:41 and plays her words.</p>"},
    {"name": "Read it calmly", "url": "aeroapp.ai/tests/pocket/sessions/2?read", "inner": sess_b, "cap": "<p>The same session as an article (C's calm view): her words as the headline, the summary, the transcript.</p>"},
    {"name": "What to fix first", "url": "aeroapp.ai/tests/pocket/review", "inner": one_more, "cap": "<p>Across sessions: ranked fixes with their quotes and moments, themes, where they disagreed. \"Based on 2 of 3\", updating after Session 3. <span class='proposed'>Server-side review</span></p>"},
]

body_html = (f'''<div class="b-hero"><div class="b-kicker">Aero app UI · step 1 · flows</div><h1>Three flows, end to end<span class="d">.</span></h1>
<p>Click through each one (or use the arrow keys). Each step is a real screen from <a href="screens.html">the screens</a>, with which page opens and why. The tester flow is the fourth, designed separately.</p>
<div class="b-toc"><a href="#f1">1 · Publish from a prompt</a><a href="#f2">2 · Create and share a test</a><a href="#f3">3 · Review results</a></div></div>'''
    + flow("f1", "Publish from a prompt", "From Claude to a live address, and the next step. Aero and Claude stay visibly separate.", F1, (0, 33))
    + flow("f2", "Create and share a test", "From a live site to a test link, someone else taking it, and the first session arriving.", F2, (33, 67))
    + flow("f3", "Review results", "From \"2 new sessions\" to what to fix first, each finding linked to its moment.", F3, (67, 100)))
html_out = page("flows.html", "Aero flows", "Three end-to-end Aero flows as clickable sequences: publish from a prompt, create and share a test, review results.", body_html)
open("flows.html", "w").write(html_out)
print("flows.html", len(html_out))
