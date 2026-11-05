#!/usr/bin/env python3
# Builds tester-round.html from tester_kit. Run: python3 -I src/tester-round-build.py (from docs/brand/app-ui)
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tester_kit import *  # noqa

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHARE = "aeroapp.ai is sharing this tab."
TABS = [("Testing Pocket", "ae", True, True)]
T = TASKS[:3]
LONG_T = "Find the monthly fee for Pocket Plus, then work out whether the yearly plan is cheaper for two people sharing one account"
LONG_D = ("Start on the home page. Look at Cards and at Help if you need to. Say out loud what you were expecting to find, and what "
          "made you decide. If the numbers are not on the page, say what you would do next.")

HEAD = """<!--
version: 2026-11-05.1
brand-sync: figmaApp docs/brand/app-ui is the source. Copy unchanged to aero-landing-page/docs/brand/app-ui/.
-->
<!doctype html><html lang="en-GB"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Aero tester round</title><meta name="description" content="Where tester tasks live, the permission card, stopping the share and multi-page prototypes. Three layouts, one pick.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@300..600&family=Geist+Mono:wght@400;500&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="tokens.css"><link rel="stylesheet" href="components.css"><link rel="stylesheet" href="tester.css"><link rel="stylesheet" href="tester-round.css">
<script>window.GLASS_MODE='subtle';</script></head><body class="tb">"""
FOOT = """<script src="tester.js"></script>
<script>(function(){var s=document.createElement('script');s.src='../glass/glass-v3.js';
s.onerror=function(){var t=document.createElement('script');t.src='glass-v3.js';document.body.appendChild(t);};
document.body.appendChild(s);})();</script></body></html>"""


def shot(inner, w=1280, h=800, cap=""):
    c = f'<p class="tb-cap">{cap}</p>' if cap else ""
    return (f'<figure class="tb-opt" style="margin:0"><div class="tb-shot" data-w="{w}" data-h="{h}">'
            f'<div class="tb-scale" style="width:{w}px;height:{h}px">{inner}</div></div>{c}</figure>')


def sec(num, sid, title, intro, body):
    return (f'<section class="tb-sec" id="{sid}"><div class="tb-wrap"><header><span class="tb-num">{num}</span>'
            f'<h2>{title}</h2><p>{intro}</p></header>{body}</div></section>')


def grid(n, *items):
    return f'<div class="tb-grid c{n}">{"".join(items)}</div>'


def opt(title, tags, inner, notes=""):
    n = f'<div class="tb-opt-n">{notes}</div>' if notes else ""
    return f'<div class="tb-opt"><div class="tb-opt-h"><b>{title}</b>{tags}</div>{inner}{n}</div>'


def pill(state="live", label="Recording", glass=True):
    g = ' data-glass-v3="secondary" data-strength="1.6"' if glass else ""
    return f'<div class="tx tx-recpill"{g}>{rec_chip(state, label=label, meter=state=="live")}</div>'


def prog_bar(i, n, now_done=False):
    s = ""
    for k in range(n):
        s += '<i class="is-done"></i>' if (k < i or (k == i and now_done)) else ('<i class="is-now"></i>' if k == i else "<i></i>")
    return f'<div class="tx-tbar-prog" aria-hidden="true">{s}</div>'


def pager(cur=2, n=3, name="Pricing"):
    nm = f"<small>{name}</small>" if name else ""
    return (f'<div class="tx-pager" data-glass-v3="secondary" data-strength="1.4" aria-label="Pages"><i class="{"is-off" if cur == 1 else ""}">{ic("back")}</i>'
            f'<span>Page {cur} of {n}{nm}</span><i class="{"is-off" if cur == n else ""}">{ic("arrow")}</i></div>')


def bar(state="task", i=1, n=3, title=None, desc=None, clamp=False, menu=False, page=None, drop=False, phone=False, explore=False):
    """state: task | rate | undo | last | explore | confirm | stopped"""
    cls = "tx tx-tbar" + (" is-clamp" if clamp else "")
    menu_h = ""
    if menu:
        menu_h = (f'<div class="tx-menu" role="menu"><button role="menuitem">{ic("restart")}Restart {PROTO}</button>'
                  f'<button role="menuitem">{ic("mic")}Mute microphone</button><hr><button role="menuitem" class="is-end">{ic("stop")}End test</button></div>')
    more = f'<button class="tx-icon" aria-label="Test menu">{ic("more")}</button>'
    tt, dd = (title or T[i][0]), (desc if desc is not None else T[i][1])
    pg = pager(*page) if page else ""
    lab = f"Task {i + 1} of {n}"
    if state == "task":
        badge = f'<div class="tx-tbar-n"><b>{i + 1}</b><small>of {n}</small></div>'
        more_l = f' <button class="tx-more">Show all</button>' if clamp else ""
        body = f'<span class="tx-label">{lab}</span><h2>{tt}</h2><p>{dd}{more_l}</p>'
        acts = pg + btn("Couldn’t do it", "", "secondary") + btn("Done", "is-primary", "primary") + more
        if phone:
            acts = btn("Done", "is-primary is-sm", "primary")
        prg = prog_bar(i, n)
    elif state == "rate":
        badge = f'<div class="tx-tbar-n is-ok">{ic("check")}</div>'
        opts = [("1", "Very hard"), ("2", "Hard"), ("3", "OK"), ("4", "Easy"), ("5", "Very easy")]
        chips = "".join(f'<button><b>{a}</b>{b}</button>' for a, b in opts)
        body = (f'<span class="tx-label">{lab} · done</span><h2>How easy was that?</h2><div class="tx-rate-row">{chips}'
                f'<button class="tx-more" style="border:0;height:auto">Skip</button></div>')
        acts = btn("Next task", "is-primary", "primary", icon="arrow") + more
        prg = prog_bar(i, n, True)
    elif state == "undo":
        badge = f'<div class="tx-tbar-n"><b>{i + 1}</b><small>of {n}</small></div>'
        body = (f'<span class="tx-label">{lab}</span><h2>{tt}</h2><p>{dd}</p>'
                f'<div class="tx-undo">{ic("check")}Task {i} saved. <button class="tx-more">Undo</button></div>')
        acts = btn("Couldn’t do it", "", "secondary") + btn("Done", "is-primary", "primary") + more
        prg = prog_bar(i, n)
    elif state == "last":
        badge = f'<div class="tx-tbar-n is-ok">{ic("check")}</div>'
        body = (f'<span class="tx-label">All {n} tasks done</span><h2>Anything else to say?</h2>'
                f'<p>Say it now, while it’s still recording. Then press Finish.</p>')
        acts = btn("Finish", "is-primary", "primary") + more
        prg = prog_bar(n, n)
    elif state == "explore":
        badge = f'<div class="tx-tbar-n is-ok">{ic("eye")}</div>'
        body = f'<span class="tx-label">Explore freely</span><h2>Look around {PROTO} and say what you think.</h2><p>There are no tasks. Stop whenever you’ve seen enough.</p>'
        acts = btn("Finish", "is-primary", "primary") + more
        prg = ""
    elif state == "confirm":
        badge = f'<div class="tx-tbar-n"><b>{i + 1}</b><small>of {n}</small></div>'
        body = f'<span class="tx-label">{lab}</span><h2>End the test now?</h2><p>What you’ve done so far is sent to {FIRST}.</p>'
        acts = btn("Keep going", "", "secondary") + btn("End test", "is-primary", "primary")
        prg = prog_bar(i, n)
    nxt = ""
    if state == "rate" and i + 1 < n:
        nxt = f'<div class="tx-next">{ic("arrow")}Next: <b>{T[i + 1][0]}</b></div>'
    dr = ""
    if drop:
        dr = f'<div class="tx-drop"><b>{tt}</b>{dd}</div>'
    return f'<div class="{cls}" role="region" aria-label="Test tasks">{badge}<div class="tx-tbar-t">{body}{nxt}</div><div class="tx-tbar-a">{acts}</div>{prg}{menu_h}{dr}</div>'


def pg_a(barhtml, proto=None, pill_html=None, extra="", share=SHARE, w=1280, h=800, tabs=TABS):
    pr = proto if proto is not None else proto_web("light")
    p = pill_html if pill_html is not None else pill()
    body = f'<div class="tr-page"><div class="tx-tbar-slot" style="position:relative;z-index:6">{barhtml}</div><div class="tr-frame">{pr}{p}{extra}</div></div>'
    return chrome(body, tabs, share=share, w=w, h=h)


def barcrop(barhtml, h=176, w=1280, pill_html=None, cap="", proto=None):
    pr = proto if proto is not None else proto_web("light")
    p = pill_html if pill_html is not None else pill()
    inner = (f'<div class="tr-crop" style="width:{w}px;height:{h}px"><div class="tr-page" style="position:absolute;inset:0"><div style="position:relative;z-index:6">{barhtml}</div>'
             f'<div class="tr-frame">{pr}{p}</div></div></div>')
    return shot(inner, w, h, cap)


def dim(card):
    return f'<div class="tx-stage is-dim">{card}</div>'


# ------------------------------------------------------------ permission card
def start_card(kind="site", phone=False):
    items = [("mic", "Your voice", f"So {FIRST} hears what you think. Talk as you go."),
             ("tab", "This tab, as a video" if not phone else "Nothing on screen", "Only this tab. Not your face, your other tabs or the rest of your screen." if not phone else "On a phone only your voice is recorded.")]
    if phone:
        items = items[:1] + [("eye", "No video", "The screen isn’t recorded on a phone.")]
    items.append(("user", f"Who sees it", f"{DESIGNER} at {STUDIO}. It’s transcribed and summarised for {FIRST}, and nobody else gets it."))
    rows = "".join(f'<div><span class="ic">{ic(a)}</span><span><b>{b}</b><small>{c}</small></span></div>' for a, b, c in items)
    steps = (f'<div class="tx-steps2"><span><b>What happens when you press Start.</b> '
             f'{"Chrome asks to let this page see this tab, then to use your microphone." if not phone else "Your phone asks to use the microphone."} '
             f'Choose Allow each time. Recording starts after the last one.</span>'
             f'<span><b>To finish,</b> press Finish at the top of the page. '
             f'{"If you press Chrome’s Stop sharing, we’ll ask if you’re done." if not phone else ""}</span></div>')
    pad = ' style="padding:24px;gap:14px;border-radius:20px"' if phone else ""
    return (f'<section class="tx tx-card is-start"{pad} role="dialog" aria-labelledby="s-t">{from_line()}'
            f'<div style="display:grid;gap:6px"><h1 id="s-t">Press Start to begin<span class="dot">.</span></h1>'
            f'<p class="tx-sub">{FIRST} would like to hear you try {PROTO}. This is what gets recorded.</p></div>'
            f'<div class="tx-rec-list">{rows}</div>{steps}'
            f'<div class="tx-actions">{btn("Start test", "is-primary is-lg is-block", "primary")}'
            f'<p class="tx-fine" style="text-align:center">You can stop at any time.</p></div></section>')


def stop_card():
    return (f'<section class="tx tx-card is-ask" role="alertdialog" aria-labelledby="st-t">'
            f'<div style="display:grid;gap:6px"><h1 id="st-t" style="font-size:24px">You stopped sharing<span class="dot">.</span></h1>'
            f'<p class="tx-sub">The video has stopped. Your voice is still being recorded. Are you finished?</p></div>'
            f'<div class="tx-actions">{btn("Yes, I’m done", "is-primary is-lg is-block", "primary")}{btn("No, keep recording", "is-lg is-block", "secondary")}</div>'
            f'<p class="tx-fine">“No” asks Chrome to share this tab again. Closing this page now keeps what you’ve recorded.</p></section>')


# ------------------------------------------------------------ layouts B and C
def rail2(i=1, n=3):
    items = ""
    for k, (t, ins) in enumerate(T):
        if k < i:
            items += f'<li class="is-done" data-n="{k + 1}"><span>{t}</span></li>'
        elif k == i:
            items += (f'<li class="is-now" data-n="{k + 1}"><span>{t}</span><span class="tx-ins">{ins}</span>'
                      f'<span class="tx-row">{btn("Done", "is-primary is-sm", "primary")}{btn("Couldn’t do it", "is-sm", "secondary")}</span></li>')
        else:
            items += f'<li data-n="{k + 1}"><span>{t}</span></li>'
    return (f'<aside class="tx tx-rail is-loud" aria-label="Test tasks"><div class="tx-rail-h">{mark()}<b style="font-weight:520;font-size:14px">{PROTO}</b>'
            f'<button class="tx-icon" style="margin-left:auto" aria-label="Test menu">{ic("more")}</button></div>'
            f'<div style="padding:14px 16px 4px"><span class="tx-label">Task {i + 1} of {n}</span></div>'
            f'<ul class="tx-tasks">{items}</ul><div class="tx-next"><b>After this:</b> {T[i + 1][0] if i + 1 < n else "Finish"}</div></aside>')


def loud(i=1, n=3, new=True, title=None, desc=None):
    tt, dd = title or T[i][0], desc if desc is not None else T[i][1]
    return (f'<aside class="tx tx-loud{" is-new" if new else ""}" aria-label="Test tasks"><div class="tx-loud-h"><span class="nb">Task {i + 1} of {n}</span><span class="sp"></span>'
            f'<button class="tx-icon" aria-label="Hide">{ic("minus")}</button><button class="tx-icon" aria-label="Test menu">{ic("more")}</button></div>'
            f'<h2>{tt}</h2><p>{dd}</p><div class="tx-two">{btn("Couldn’t do it", "", "secondary")}{btn("Done", "is-primary", "primary")}</div>'
            f'<div class="tx-next" style="margin:0">{ic("arrow")}Next: <b>{T[i + 1][0] if i + 1 < n else "Finish"}</b></div></aside>')


def page_b():
    body = (f'<div class="tr-page is-row">{rail2()}<div class="tr-frame">{proto_web("light")}{pill()}</div></div>')
    return chrome(body, TABS, share=SHARE)


def page_c(long=False):
    p = loud(1, 3, True, LONG_T if long else None, LONG_D if long else None)
    body = f'<div class="tr-page"><div class="tr-frame">{proto_web("light")}{pill()}<div class="tx-float bl">{p}</div></div></div>'
    return chrome(body, TABS, share=SHARE)


# ------------------------------------------------------------ phone
def phone_a(state="task", open_=False):
    b = bar(state, 1, 3, phone=True, clamp=True)
    extra = ""
    if open_:
        extra = (f'<div style="position:absolute;z-index:8;left:10px;right:10px;top:8px;background:#fff;border-radius:18px;box-shadow:var(--ae-sh-3);padding:16px;display:grid;gap:10px">'
                 f'<span class="tx-label">Task 2 of 3</span><h2 style="font-size:17px;font-weight:520;margin:0">{T[1][0]}</h2><p style="margin:0;color:var(--ae-ink-2);font-size:14px">{T[1][1]}</p>'
                 f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">{btn("Couldn’t do it", "", "secondary")}{btn("Done", "is-primary", "primary")}</div></div>')
    body = (f'<div class="tr-page is-phone"><div style="position:relative;z-index:6">{b}</div><div class="tr-frame">{proto_app("light")}'
            f'<div class="tx-recpill is-lo" data-glass-v3="secondary" data-strength="1.6">{rec_chip("live", label="Recording", meter=False)}</div>{extra}</div></div>')
    return phone(body)


def phone_start():
    return phone(f'<div class="tx-stage is-wash" style="padding:12px">{start_card(phone=True)}</div>')


# ------------------------------------------------------------ build
def build():
    o = [HEAD]
    toc = [("sum", "Summary"), ("conf", "Conflicts"), ("lay", "Layouts"), ("scn", "Scenarios"), ("pick", "Pick"), ("perm", "Permission"), ("stop", "Stop sharing"), ("pages", "Pages"), ("rec", "Recordings"), ("dec", "Decisions")]
    o.append('<div class="tb-top"><div class="tb-wrap"><span class="tb-logo">Aero<i>.</i></span><span class="tb-crumb">Tester round · 30 Oct user test</span><nav class="tb-toc">'
             + "".join(f'<a href="#{a}">{b}</a>' for a, b in toc) + "</nav></div></div>")
    o.append(f"""<header class="tb-hero"><div class="tb-wrap"><h1>Tasks the tester can’t miss<i>.</i></h1>
<p>The user test said the task bubble looks like a notification, the permission step doesn’t say what starts the test, and stopping the share ends as “abandoned”. This board lines up every tester design we have, shows three places for the tasks, and designs the permission card, stop-sharing and page count. All names and tasks are made up (Example). Nothing here is built.</p></div></header>""")

    o.append(sec("00", "sum", "Summary", "The short version.", f"""<div class="tb-grid c2">
<div class="tb-opt"><div class="tb-opt-h"><b>Pick: A, a task bar across the top</b>{tag("rec")}</div><div class="tb-opt-n"><ul class="tr-list">
<li>It sits in the page, above the site, so it can’t read as a notification. It keeps the full width, so a responsive site shows its real layout.</li>
<li>One row: step badge, the task, Done and Couldn’t do it. After Done: an optional rating and a <b>Next task</b> button the tester presses. No hard stop.</li>
<li>The Recording pill is its own glass pill at the top centre, as on the website demo. Buttons are the V3 caustic glass buttons.</li></ul></div></div>
<div class="tb-opt"><div class="tb-opt-h"><b>Also decided here</b>{tag("prop")}</div><div class="tb-opt-n"><ul class="tr-list">
<li>One card, one button: <b>Start test</b>. It says what is recorded and who sees it. “Share tab” goes.</li>
<li>Stopping the share asks “Are you finished?” and never ends as abandoned.</li>
<li>Page count: HTML sites can show the page name and arrows now. Figma prototypes can’t show “1 of 2” until the Embed API work; until then Figma’s own controls come back.</li>
<li>Your question on #302: the <b>⋯</b> is the panel menu (Move panel, Mute, Restart, End test). The <b>line</b> is Minimise, which folds the panel to a small pill. Under A both go: the bar doesn’t move or hide, and the menu keeps three items.</li></ul></div></div></div>"""))

    conf = [
        ("Where tasks live", "A floating plate, 320px (tester.html pick, TESTER-NOTES)", "A docked rail (tester.html decision 3); “a square panel” (DECISIONS 23 Oct)", "A bar across the top (this round)"),
        ("Corner", "Bottom right (tester.html boards, TaskPanel before #302)", "Bottom left (DECISIONS 24 Oct, #302, overlay, website demo)", "Not a corner in A. Bottom left in C."),
        ("Recording sign", "Inside the panel header, with a timer (tester.html, TESTER-NOTES 6)", "A separate glass pill at the top (DECISIONS 26 Oct and 4 Nov, website demo, overlay); no timer (23 Oct)", "Separate pill, no timer. Not built yet in the one-tab panel."),
        ("Buttons", "Older GlassButton, fill ink and glass (TaskPanel in code)", "V3 caustic glass, `data-glass-v3` (website, tester.html); flat outline (overlay); “Couldn’t do it” as a text link (website demo)", "V3 glass for both, primary and secondary"),
        ("Done gating", "Off until the tester has used the prototype (TaskPanel, Figma tests)", "Always on (overlay, site tests)", "Always on. A site in a frame can’t tell us if they tried."),
        ("Minimise", "Fold to a pill with Show (tester.html, TaskPanel)", "A chevron on the demo panel; nothing in the overlay", "Gone in A. Kept in C, labelled."),
        ("Permission step", "Two rows, two buttons: mic, then tab (tester.html, TESTER-NOTES rule 2)", "One Start press shares the tab and asks for the mic (DECISIONS 26 Oct, site tests in code)", "One card, one button, both kinds of test"),
        ("Stop sharing", "Figma: video stops, voice goes on silently. HTML: ends the session (code)", "“Share again” or pause instead of ending (TESTER-NOTES proposal 5)", "Ask “Are you finished?”. Offer to share again."),
        ("Rating", "Emoji modal after each task (today)", "Five labelled buttons in the panel, keys 1 to 5 (tester.html)", "Inline, optional, with the Next button"),
        ("Panel title", "“Pocket test” or the recording chip (tester_kit)", "“Test” only (DECISIONS 4 Nov)", "No title. The step badge is the label."),
        ("Phones", "Dock below the prototype (tester.html, TaskPanel under 600px)", "Voice only on Figma, HTML blocked (code)", "Compact bar at the top, details in a sheet"),
    ]
    rows = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in conf)
    o.append(sec("01", "conf", "Where our tester designs disagree", "Sources: app-ui/tester.html, TESTER-NOTES.md, UI-BRIEF.md, DECISIONS.md tester lines, tester-panel.html, the website hero demo, TaskPanel and the overlay.",
                 f'<table class="tr-tbl"><thead><tr><th>Question</th><th>One design says</th><th>Another says</th><th>This round</th></tr></thead><tbody>{rows}</tbody></table>'))

    lay = grid(1,
        opt("A. Task bar across the top", tag("rec"), shot(pg_a(bar("task", 1, 3)), cap="Task 2 of 3. The bar has the step, the task, both buttons and the menu. The pill hangs just under it at the top centre."),
            "Full width, inside the page above the site. Louder because of its place, size and the blue step badge, not because it floats. Costs about 90px of height."),
        opt("B. Docked side panel", tag("prop", "Option"), shot(page_b(), cap="All tasks listed, the current one open with its buttons."),
            "Very clear, and shows what comes next. But it takes 320px of width, so a 1280px site is tested at 960px and may flip to its tablet layout."),
        opt("C. Today’s floating panel, louder", tag("no", "Weakest"), shot(page_c(), cap="Bigger type, blue top edge, a ring for a moment when the task changes."),
            "Cheapest to build. Still a card over the prototype, which is what the participant ignored, and it hides part of the page in every recording."))
    o.append(sec("02", "lay", "Three places for the tasks", "Each has the separate Recording pill and the V3 glass buttons. The pill’s glass shows over the site’s own colours.", lay))

    sc = [
        ("Task, one of three", shot(pg_a(bar("task", 1, 3)), w=1280, h=800)),
    ]
    crops = [
        ("Done pressed: optional rating, then Next task", "The tester decides when to move on. Pressing a rating also moves on. If the owner turned ratings off, Done moves on at once and shows “Task 2 saved. Undo” for a few seconds.", barcrop(bar("rate", 1, 3))),
        ("After moving on: Undo", "A chatty tester who pressed Done too early can take it back.", barcrop(bar("undo", 2, 3))),
        ("Long title and description", "The title keeps two lines, the description one, and Show all opens the rest in a drop-down over the page. The bar never grows, so the site doesn’t jump.", barcrop(bar("task", 1, 3, LONG_T, LONG_D, clamp=True, drop=True), h=300)),
        ("Last task done", "The bar becomes the finish step. It stays recording while they say what they think.", barcrop(bar("last", 2, 3))),
        ("No tasks", "Explore freely. One button, Finish.", barcrop(bar("explore"))),
        ("Menu open", "Three items: Restart, Mute, End test (red, last).", barcrop(bar("task", 1, 3, menu=True), h=290)),
        ("End early", "End test asks first. What’s done so far is kept.", barcrop(bar("confirm", 1, 3))),
        ("A multi-page site", "Page name and arrows from the site, next to the buttons.", barcrop(bar("task", 1, 3, page=(2, 3, "Pricing"))))]
    body = shot(pg_a(bar("task", 1, 3)), cap="Layout A in full. Everything below is the same bar in another state.")
    body += "".join(f'<div style="margin-top:28px"><h3 style="margin:0 0 4px;font-size:17px;font-weight:520">{t}</h3><p style="margin:0 0 10px;color:var(--ae-ink-2);font-size:14px">{d}</p>{c}</div>' for t, d, c in crops)
    ph = (f'<div class="tr-phones"><div class="tr-phone-box">{shot(phone_a(), 390, 844, "Phone: a compact bar. Done is always in reach.")}</div>'
          f'<div class="tr-phone-box">{shot(phone_a(open_=True), 390, 844, "Tap the bar for the full task and Couldn’t do it.")}</div>'
          f'<div class="tr-phone-box">{shot(phone_start(), 390, 844, "Phone start card: voice only.")}</div></div>')
    body += f'<div style="margin-top:36px"><h3 style="margin:0 0 10px;font-size:17px;font-weight:520">Phone</h3>{ph}</div>'
    thanks = shot(chrome(f'<div class="tx-stage is-wash">{thanks_card("saving", 72, "site")}</div>', [("Testing Pocket", "ae", True, False)]), cap="Thank-you: unchanged from the tester board. The bar is gone and the pill is replaced by the sending state.")
    body += f'<div style="margin-top:36px"><h3 style="margin:0 0 10px;font-size:17px;font-weight:520">Thank-you</h3>{thanks}</div>'
    mx = [("Task, one of three", "Bar", "Rail, current task open", "Panel, bigger"), ("Done then next", "Rating and Next in the bar", "Rating in the rail, next task opens", "Rating in the panel; panel pulses on the new task"),
          ("No tasks", "One line, Finish", "Rail with one Finish", "Panel with Finish"), ("Long text", "Clamp and Show all", "Rail scrolls", "Panel grows, scrolls when tall"),
          ("End early", "In the bar", "Link in the rail footer", "In the panel menu"), ("Phone", "Compact bar", "Doesn’t fit, would become the bar", "Doesn’t fit, would become the dock"),
          ("Several pages", "Pager beside the buttons", "Pager under the task", "Pager under the title")]
    rows = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in mx)
    body += (f'<div style="margin-top:36px"><h3 style="margin:0 0 10px;font-size:17px;font-weight:520">The same scenarios in B and C</h3>'
             f'<table class="tr-tbl"><thead><tr><th>Scenario</th><th>A. Bar</th><th>B. Rail</th><th>C. Floating</th></tr></thead><tbody>{rows}</tbody></table></div>')
    o.append(sec("03", "scn", "Every scenario in the pick (A)", "Task, rating, no tasks, long text, end early, thank-you, phone and several pages. B and C are in the table at the end of this section.", body))

    o.append(sec("04", "pick", "How they compare", "What the tester sees, and what the recording shows.", """<table class="tr-tbl"><thead><tr><th></th><th>A. Top bar</th><th>B. Side panel</th><th>C. Floating, louder</th></tr></thead><tbody>
<tr><td>Reads as a notification</td><td class="y">No: part of the page</td><td class="y">No</td><td class="n">Still can</td></tr>
<tr><td>Next step visible</td><td class="m">Only on the rating step</td><td class="y">Always, a list</td><td class="m">One line</td></tr>
<tr><td>Site layout changes</td><td class="y">Height only</td><td class="n">Width: may flip to a tablet layout</td><td class="y">None</td></tr>
<tr><td>Covers the site</td><td class="y">No</td><td class="y">No</td><td class="n">Yes, a 380px card</td></tr>
<tr><td>Task visible in every recorded frame</td><td class="y">Yes</td><td class="y">Yes</td><td class="m">Yes, but it moves</td></tr>
<tr><td>Phone</td><td class="y">Compact bar</td><td class="n">Needs a second design</td><td class="m">Needs the dock</td></tr>
<tr><td>Build</td><td class="m">New component</td><td class="m">Reuses the rail</td><td class="y">Edits TaskPanel</td></tr></tbody></table>"""))

    cards = grid(2,
        opt("Today: two rows, two buttons", tag("today"), shot(chrome(proto_figma("light") + dim(allow_card("active", "waiting", "figma")), [("Testing Pocket", "ae", True, False)], h=900), 1280, 900, "“Allow”, then “Share tab”. Nothing says which button starts the test.")),
        opt("New: one card, one button", tag("rec"), shot(chrome(proto_web("light") + dim(start_card()), [("Testing Pocket", "ae", True, False)], h=900), 1280, 900, "Says what is recorded, who sees it, what Chrome will ask, and which button starts it.")))
    copy = f"""<div class="tr-copy" style="margin-top:24px"><b>Copy</b>
<p><code>Heading</code> Press Start to begin.</p><p><code>Intro</code> {FIRST} would like to hear you try {PROTO}. This is what gets recorded.</p>
<p><code>Rows</code> Your voice: So {FIRST} hears what you think. Talk as you go. / This tab, as a video: Only this tab. Not your face, your other tabs or the rest of your screen. / Who sees it: {DESIGNER} at {STUDIO}. It’s transcribed and summarised for {FIRST}, and nobody else gets it.</p>
<p><code>What happens</code> Chrome asks to let this page see this tab, then to use your microphone. Choose Allow each time. Recording starts after the last one. To finish, press Finish at the top of the page. If you press Chrome’s Stop sharing, we’ll ask if you’re done.</p>
<p><code>Button</code> Start test. <code>Under it</code> You can stop at any time.</p>
<p><code>Two-tab fallback</code> The row says “Record the {PROTO} tab” and the button “Choose the {PROTO} tab”, never “Share tab”. Chrome’s own words stay Chrome’s.</p></div>
<ul class="tr-list" style="margin-top:16px"><li><b>Why “Share tab” went:</b> the participant read it as sharing a link. Chrome’s own dialog uses “share”, so the card explains it before Chrome asks.</li>
<li><b>One button for both kinds of test:</b> the HTML flow already starts the tab share and the mic from one press. The same should work for Figma tests. Ask for the tab first (it needs the click), then the mic. To check in Chrome, Safari and Firefox before building. If a browser refuses, that browser falls back to two buttons.</li></ul>"""
    chrome_seq = grid(2,
        shot(chrome(proto_web("light") + '<div class="tx-stage is-dim"></div>' + tab_prompt(), [("Testing Pocket", "ae", True, False)]), 1280, 800, "After Start: Chrome asks about the tab. This is Chrome’s dialog, not Aero’s."),
        shot(chrome(proto_web("light") + '<div class="tx-stage is-dim"></div>' + mic_prompt(), [("Testing Pocket", "ae", True, False)], share=SHARE), 1280, 800, "Then the microphone. After Allow, the bar and pill appear."))
    o.append(sec("05", "perm", "The permission card", "Today’s screen and the new one, the copy, and what Chrome shows next.", cards + copy + '<div style="margin-top:24px">' + chrome_seq + "</div>" +
                 f'<div style="margin-top:24px">{shot(phone_start(), 390, 844, "Phone: voice only, one button.")}</div>'.replace('class="tb-opt"', 'class="tb-opt" style="max-width:300px"')))

    stop = grid(2,
        shot(chrome(proto_web("light") + dim(stop_card()) , [("Testing Pocket", "ae", True, False)], share=None), 1280, 800, "Stop sharing in Chrome: the video stops, the voice goes on, and we ask."),
        shot(pg_a(bar("task", 1, 3), pill_html=pill("voice", "Voice only", True), share=None), 1280, 800, "If they answer No and don’t share again: the pill says Voice only, the task bar stays."))
    o.append(sec("06", "stop", "Stopping the share", "The participant stopped the share the way people do in Zoom, missed Finish, and the session read “abandoned”. “Abandoned” is written by a clean-up job for sessions whose tab died, not by this.", stop + """<ul class="tr-list" style="margin-top:16px">
<li><b>Behaviour:</b> when the video track ends, show the card. “Yes, I’m done” runs the same finish as the Finish button (thank-you, upload). “No, keep recording” asks Chrome to share again and a second video file joins the session; if they close the card, voice-only continues with the pill saying so.</li>
<li><b>Today in code:</b> HTML tests finish at once with no question (UTHtmlController). Figma tests drop the video and carry on silently (UserTestingTester).</li>
<li><b>Closing the page with the card open:</b> a session that has saved recording should show as Incomplete, not Abandoned. That is a change to the clean-up function, flagged as decision 6.</li>
<li>The start card now tells them about this before it happens.</li></ul>"""))

    pg = grid(2,
        barcrop(bar("task", 1, 3, page=(2, 3, "Pricing")), cap="HTML site: page name and arrows."),
        barcrop(bar("task", 1, 3, page=(1, 2, None)), cap="Figma prototype with a known count: “Page 1 of 2”."))
    o.append(sec("07", "pages", "Several pages", "The participant’s prototype had two pages and the arrows were found late. What is possible in code.", pg + """<table class="tr-tbl" style="margin-top:20px"><thead><tr><th></th><th>What we know</th><th>What we can show</th></tr></thead><tbody>
<tr><td>HTML site</td><td>The site’s overlay already reports each page load to the test page. Aero hosts the files, so it knows the page names.</td><td class="y">Current page name now. “2 of 3” only if the owner lists the pages in setup (a site’s pages have no order). Back and forward arrows send a message to the overlay.</td></tr>
<tr><td>Figma prototype</td><td>Aero’s embed URLs set <code>hide-ui=1</code>, which hides Figma’s own controls. The legacy embed sends no events.</td><td class="m">Now: stop hiding Figma’s controls on test pages (to verify in a real embed) and let the task text name the page. Later: the Embed API’s screen-change events give the current screen name, with the OAuth setup in cursor-recording.md. A total count needs the owner to type it.</td></tr>
<tr><td>Phone</td><td>Figma only, voice only.</td><td class="m">Same as Figma on a computer.</td></tr></tbody></table>"""))

    o.append(sec("08", "rec", "What this does to recordings", "The panel is in the tab recording, so its place becomes part of every replay.", """<table class="tr-tbl"><thead><tr><th></th><th>A. Top bar</th><th>B. Side panel</th><th>C. Floating</th></tr></thead><tbody>
<tr><td>What the video shows</td><td>The site with a bar above it. The task is on screen in every frame, which helps whoever reviews it.</td><td>Same, with the list on the left.</td><td>The site with a card over part of it.</td></tr>
<tr><td>Hidden content</td><td class="y">None</td><td class="y">None</td><td class="n">Whatever is under the card, which changes as it is moved</td></tr>
<tr><td>Site behaves as real?</td><td class="y">Width is real. Height is 90px less, so a 100vh hero is shorter.</td><td class="n">Width is 320px less, so breakpoints can change</td><td class="y">Yes</td></tr>
<tr><td>Rating and Next in the video</td><td>Visible. Lets Aero line up tasks with the timeline.</td><td>Visible</td><td>Visible</td></tr>
<tr><td>Recording pill</td><td colspan="3">Same for all three: top centre, over the site’s header area, about 120 by 32px. It is in the video as a small glass pill. It can sit on a site’s own header, so we need your yes (decision 2).</td></tr>
<tr><td>Glass</td><td colspan="3">V3 glass is on the buttons and the pill only. The bar body is solid so the text is readable and the recording isn’t warped by refraction.</td></tr></tbody></table>
<ul class="tr-list" style="margin-top:16px"><li>Truth rules hold: no cursor, no live typing; the transcript arrives afterwards. Names are Example.</li></ul>"""))

    dec = [
        ("Layout", "A, the top bar. B only if you want the full task list always visible. C is not recommended."),
        ("Recording pill", "Hang it just under the bar at the top centre (as on the demo), or put it inside the bar and lose the separate-pill look? I recommend under the bar."),
        ("Done always on", "Drop the Figma rule that disables Done until the tester has used the prototype. The tester decides."),
        ("Rating", "Inline and optional next to Next task, with Undo, instead of a modal after every task."),
        ("One permission button", "One card and one Start test button for Figma and HTML tests, after we check it in Chrome, Safari and Firefox."),
        ("Stopping the share", "Ask “Are you finished?”. And change the clean-up job so a session with saved recording is Incomplete, not Abandoned."),
        ("Pages", "HTML: page name and arrows now, count if the owner lists pages. Figma: stop hiding Figma’s controls on test pages now; a live count later with the Embed API."),
        ("Buttons", "V3 caustic glass buttons everywhere in the tester UI. TaskPanel still uses the older GlassButton."),
        ("Menu and minimise", "In A, remove Move panel and Minimise and keep Restart, Mute and End test behind the ⋯. Keep both in C, with text labels."),
        ("Words", "“Share tab” is removed. Start test is the button. The fallback says “Record the Pocket tab”."),
        ("The two-tab overlay", "Draw the same bar inside the site’s tab, so there is one design in both flows."),
        ("Next after you pick", "I’ll add the decisions to DECISIONS.md, put the build in TODO as Phase 6, and add the bar and pill to the AeroShowcase tester section.")]
    o.append(sec("09", "dec", "Decisions for you", "Numbered, with a recommendation.", '<ol class="tr-dec">' + "".join(f"<li><div><b>{a}</b><span>{b}</span></div></li>" for a, b in dec) + "</ol>"))
    o.append(FOOT)
    return "\n".join(o)


if __name__ == "__main__":
    open(os.path.join(ROOT, "tester-round.html"), "w").write(build())
    print("ok")
