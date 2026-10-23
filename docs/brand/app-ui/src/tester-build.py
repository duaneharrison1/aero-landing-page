#!/usr/bin/env python3
# Builds tester.html (the board) and tester-flow.html (the clickable flow) from tester_kit.
# Run: python3 -I src/tester-build.py   (from /home/claude/research/app-ui)
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tester_kit import *  # noqa

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTRAST = {}
try:
    CONTRAST = json.load(open(os.path.join(ROOT, "src", "tester-contrast.json")))
except Exception:
    pass

HEAD = """<!doctype html><html lang="en-GB"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%231D1D1F'/%3E%3Ctext x='8' y='22' font-family='Arial' font-size='16' fill='white'%3EA%3C/text%3E%3Ccircle cx='23' cy='20' r='2.4' fill='%233478F6'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@300..600&family=Geist+Mono:wght@400;500&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="tokens.css"><link rel="stylesheet" href="components.css"><link rel="stylesheet" href="tester.css">
<script>window.GLASS_MODE='subtle';</script>
</head><body class="tb">"""
FOOT_JS = """<script src="tester.js"></script>
<script>(function(){var s=document.createElement('script');s.src='../glass/glass-v3.js';
s.onerror=function(){var t=document.createElement('script');t.src='glass-v3.js';document.body.appendChild(t);};
document.body.appendChild(s);})();</script></body></html>"""


def shot(inner, w=1280, h=800, cap="", extra_cls=""):
    c = f'<p class="tb-cap">{cap}</p>' if cap else ""
    return (f'<figure class="tb-opt" style="margin:0"><div class="tb-shot {extra_cls}" data-w="{w}" data-h="{h}">'
            f'<div class="tb-scale" style="width:{w}px;height:{h}px">{inner}</div></div>{c}</figure>')


def opt(title, tags, inner, notes="", key=""):
    k = f'<span class="tb-k">{key}</span>' if key else ""
    return (f'<div class="tb-opt"><div class="tb-opt-h">{k}<b>{title}</b>{tags}</div>{inner}'
            f'{f"<div class=tb-opt-n>{notes}</div>" if notes else ""}</div>')


def sec(num, sid, title, intro, body):
    return (f'<section class="tb-sec" id="{sid}"><div class="tb-wrap"><header><span class="tb-num">{num}</span>'
            f'<h2>{title}</h2><p>{intro}</p></header>{body}</div></section>')


def grid(n, *items):
    return f'<div class="tb-grid c{n}">{"".join(items)}</div>'


def ul(*items):
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


# ---------------------------------------------------------------- screen compositions
CH = 800  # chrome height
SHARE_THIS = "aeroapp.ai is sharing this tab."
FTABS = [("Testing Pocket", "ae", True, False)]
FTABS_REC = [("Testing Pocket", "ae", True, True)]


def scr_welcome_a(kind="figma", tasks=True, theme="light", clicks=False):
    base = proto_figma(theme) if kind == "figma" else '<div class="tx-stage is-page"></div>'
    return chrome(base + f'<div class="tx-stage is-dim">{welcome_card(kind, tasks, clicks=clicks)}</div>', FTABS)


def scr_welcome_b():
    left = (f'<div class="tx" style="display:flex;flex-direction:column;gap:22px;max-width:470px">{from_line()}'
            f'<h1 style="font-size:40px;font-weight:350;letter-spacing:-.03em;line-height:1.08">{DESIGNER} asked you to try {PROTO}<span style="color:var(--ae-blue)">.</span></h1>'
            f'{quote()}<ol class="tx-steps"><li>Allow your microphone and this tab.</li><li>Try 4 short tasks. Say what you think as you go.</li><li>Press Finish. That’s it.</li></ol>'
            f'<p class="tx-fine" style="color:var(--ae-ink-3);font-size:13px">Records your voice and this tab only, for {DESIGNER} at {STUDIO}. No camera, no account. Stop at any time.</p>'
            f'<div>{btn("Start", "is-primary is-lg", "primary")}</div></div>')
    right = (f'<div style="position:relative;width:440px;height:560px;border-radius:24px;background:#2C2C2C;overflow:hidden;box-shadow:var(--ae-sh-3)">'
             f'<div style="position:absolute;inset:0;filter:blur(1px);opacity:.9">{proto_figma("light")}</div>'
             f'<div class="tx-float br" style="right:16px;bottom:16px;zoom:.86">{panel(0, interacted=False)}</div>'
             f'<span class="tb-tag" style="position:absolute;left:14px;top:14px;background:#fff">What you’ll see</span></div>')
    body = f'<div class="tx-stage is-wash" style="grid-template-columns:auto auto;gap:72px">{left}{right}</div>'
    return chrome(body, FTABS)


def scr_allow(mic, tab, prompt="", ready=False, note="", kind="figma", theme="light", helper=None, title=None):
    base = proto_figma(theme) if kind == "figma" else '<div class="tx-stage is-page"></div>'
    tabs = FTABS_REC if (tab == "ok" and kind == "figma") else FTABS
    share = SHARE_THIS if (tab == "ok" and kind == "figma") else None
    return chrome(base + f'<div class="tx-stage is-dim">{allow_card(mic, tab, kind, note, ready, helper=helper, title=title)}</div>' + prompt, tabs, share=share)


def scr_testing(state="task", i=1, theme="light", style="plate", strip_html="", corner="br", menu=False, interacted=True, rec="live", time="04:12", proto=None, share=SHARE_THIS):
    base = proto if proto is not None else proto_figma(theme)
    p = panel(i, state, rec=rec, time=time, style=style, strip=strip_html, interacted=interacted, menu=menu)
    return chrome(base + f'<div class="tx-float {corner}">{p}</div>', FTABS_REC if share else FTABS, share=share)


def closeup(inner, theme="light", h=400, w=560, corner="br", web=True, cap=""):
    """1:1 crop of the prototype's bottom-right corner with a tester component on it."""
    page = proto_web(theme) if web else proto_figma(theme)
    body = (f'<div style="position:relative;width:{w}px;height:{h}px;overflow:hidden;border-radius:12px;box-shadow:0 0 0 1px var(--ae-line)">'
            f'<div style="position:absolute;right:0;bottom:0;width:1280px;height:720px">{page}</div>'
            f'<div class="tx-float {corner}">{inner}</div></div>')
    return shot(body, w, h, cap)


def cardshot(card, h=720, w=600, cap=""):
    return shot(f'<div class="tx-stage is-wash" style="border-radius:12px">{card}</div>', w, h, cap)


def scr_mini(theme="light", i=1):
    return chrome(proto_figma(theme) + f'<div class="tx-float br">{mini(i)}</div>', FTABS_REC, share=SHARE_THIS)


def scr_rail(i=1):
    body = (f'<div style="position:absolute;inset:0;display:flex">{rail(i)}'
            f'<div style="position:relative;flex:1">{proto_figma("light")}</div></div>')
    return chrome(body, FTABS_REC, share=SHARE_THIS)


def scr_thanks(save="saving", pct=72, note="", kind="figma"):
    body = f'<div class="tx-stage is-wash">{thanks_card(save, pct, kind, note)}</div>'
    tabs = FTABS
    return chrome(body, tabs)


def scr_msg(title, text, actions="", extra="", stage="is-wash", tabs=None, url=LINK, prompt=""):
    return chrome(f'<div class="tx-stage {stage}">{msg_card(title, text, actions, extra=extra)}</div>' + prompt, tabs or FTABS, url=url)


# HTML two-tab
HTABS_CTRL = [("Testing Pocket", "ae", True, False), ("Pocket", "pk", False, False)]
HTABS_CTRL_REC = [("Testing Pocket", "ae", True, False), ("Pocket", "pk", False, True)]
HTABS_POCKET = [("Testing Pocket", "ae", False, False), ("Pocket", "pk", True, False)]
HTABS_POCKET_REC = [("Testing Pocket", "ae", False, False), ("Pocket", "pk", True, True)]


def html_open_card(blocked=False):
    note = ""
    if blocked:
        note = (f'<div class="tx-note is-warn">{ic("alert")}<span><b>Chrome blocked the new tab.</b> Click the blocked-tab icon at the right of the address bar, '
                f'choose <b>Always allow</b>, then press Open {PROTO} again.</span></div>')
    rows = perm_row("mic", "ok") + (f'<div class="tx-perm is-active"><span class="ic">{ic("ext")}</span><div><b>Open {PROTO}</b>'
                                    f'<small>It opens in a new tab. Keep this tab open too: it holds the recording.</small></div>'
                                    f'{btn("Open " + PROTO, "is-primary is-sm", "primary")}</div>') + perm_row("ptab", "waiting")
    return (f'<section class="tx tx-card">{from_line()}<div style="display:grid;gap:6px"><h1>Two tabs for this test</h1>'
            f'<p class="tx-sub">{PROTO} opens in its own tab, so it works just as it would for real. This tab records and keeps your tasks.</p></div>'
            f'<div class="tx-perms">{rows}</div>{note}</section>')


def html_share_card(err=None, attempts=0):
    notes = {
        None: "",
        "wrong": f'<div class="tx-note is-warn">{ic("alert")}<span><b>That was a different tab.</b> Pick the one called <b>{PROTO}</b>, with the orange icon.</span></div>',
        "nottab": f'<div class="tx-note is-warn">{ic("alert")}<span><b>That was a window or your screen.</b> Choose <b>Chrome tab</b> at the top of the dialog, then <b>{PROTO}</b>.</span></div>',
        "denied": f'<div class="tx-note is-warn">{ic("alert")}<span><b>Sharing was cancelled.</b> The test needs to see the {PROTO} tab. Nothing outside it is recorded.</span></div>',
        "fallback": f'<div class="tx-note is-bad">{ic("alert")}<span><b>Your whole screen will be recorded,</b> including anything outside {PROTO}. Close anything private first.</span></div>',
    }[err]
    cta = "Share the " + PROTO + " tab" if not err else ("Share entire screen" if err == "fallback" else "Try again")
    alt = ""
    if attempts >= 2 and err != "fallback":
        alt = f'<button class="tx-link is-quiet" style="align-self:center">Can’t find it? Share your entire screen instead</button>'
    picker_hint = (f'<div class="tx-note">{ic("info")}<span>In the dialog: <b>Chrome tab</b>, then <b>{PROTO}</b>, then <b>Share</b>. '
                   f'Chrome then takes you to {PROTO}.</span></div>') if not err else ""
    return (f'<section class="tx tx-card">{from_line()}<div style="display:grid;gap:6px"><h1>Share the {PROTO} tab</h1>'
            f'<p class="tx-sub">So {FIRST} can see what you do. Only that tab is shared.</p></div>'
            f'<div class="tx-perms">{perm_row("mic", "ok")}<div class="tx-perm is-ok"><span class="ic">{ic("ext")}</span><div><b>{PROTO} is open</b><small>In the next tab along.</small></div><span class="tx-state">{ic("check")}Open</span></div></div>'
            f'{picker_hint}{notes}<div class="tx-actions">{btn(cta, "is-primary is-lg is-block", "primary")}{alt}</div></section>')


def html_ctrl_testing(i=1, ended=None):
    items = ""
    for k, (t, ins) in enumerate(TASKS):
        if k < i:
            items += f'<li class="is-done" data-n="{k + 1}"><span>{t}</span></li>'
        elif k == i:
            items += (f'<li class="is-now" data-n="{k + 1}"><span>{t}</span><span class="tx-ins">{ins}</span>'
                      f'<span class="tx-row">{btn("Done", "is-sm")}</span></li>')
        else:
            items += f'<li data-n="{k + 1}"><span>{t}</span></li>'
    top = (f'<div class="tx-note is-ok">{ic("check")}<span><b>Recording the {PROTO} tab.</b> Your tasks are shown there too. Come back here any time.</span></div>')
    if ended == "today":
        top = (f'<div class="tx-note is-warn">{ic("alert")}<span><b>Sharing stopped, so the test ended.</b> What you did up to then is being sent to {FIRST}.</span></div>')
    if ended == "prop":
        top = (f'<div class="tx-note is-warn">{ic("alert")}<span><b>Sharing stopped.</b> Your voice is still recording. Share {PROTO} again to carry on, or finish now.</span>'
               f'</div>')
    acts = btn("Finish early", "is-block")
    if ended == "prop":
        acts = f'<div class="tx-two" style="display:grid;grid-template-columns:1fr 1fr;gap:8px">{btn("Share again", "is-primary", "primary")}{btn("Finish now")}</div>'
    if ended == "today":
        acts = ""
    return (f'<section class="tx tx-card is-wide" style="gap:16px"><div style="display:flex;align-items:center;gap:10px">{mark()}'
            f'<b style="font-weight:520">Testing {PROTO}</b><span style="margin-left:auto">{rec_chip("voice" if ended else "live", "04:12")}</span></div>'
            f'{top}<ul class="tx-tasks" style="padding:0">{items}</ul>{acts}</section>')


def overlay_wait():
    body = (f'<span class="tx-label">Not recording yet</span><h2>One more step</h2>'
            f'<p class="tx-ins">Go back to the <b style="font-weight:520">Testing {PROTO}</b> tab and share this tab. Your first task appears here after that.</p>')
    return (f'<aside class="tx tx-panel" style="position:relative"><div class="tx-panel-h"><span class="tx-rec is-muted"><span class="d"></span>Not recording</span>'
            f'<button class="tx-icon">{ic("minus")}</button></div><div class="tx-panel-b">{body}</div></aside>')


def overlay_finished():
    body = (f'<span class="tx-label">Finished</span><h2>Go back to the Testing {PROTO} tab</h2>'
            f'<p class="tx-ins">Your recording is being sent from there. Keep it open until it says Sent.</p>')
    return (f'<aside class="tx tx-panel" style="position:relative"><div class="tx-panel-h">{rec_chip("saving")}'
            f'</div><div class="tx-panel-b">{body}</div></aside>')


# phone
def ph_stage(card, theme="light", dim=True):
    st = "is-dim" if dim else "is-wash"
    return f'{proto_app(theme)}<div class="tx-stage {st}" style="padding:12px;place-items:end center;padding-bottom:12px">{card}</div>'


def ph_testing(theme="light", i=1, explore=False, strip_html=""):
    return (f'<div style="position:absolute;inset:0;display:flex;flex-direction:column">'
            f'<div style="position:relative;flex:1">{proto_app(theme)}</div>{strip_html}{dock(i, explore=explore)}</div>')


def ph_allow(state="active", sheet=True):
    rows = perm_row("mic", state)
    note = f'<div class="tx-note">{ic("info")}<span>Phones can’t share a screen, so only your voice is recorded.</span></div>'
    card = (f'<section class="tx tx-card" style="padding:24px;gap:16px;border-radius:20px">{from_line()}'
            f'<div style="display:grid;gap:6px"><h1>Allow your microphone</h1><p class="tx-sub">Your phone will ask. Choose Allow.</p></div>'
            f'<div class="tx-perms">{rows}</div>{note}<div class="tx-actions">{btn("Start the test", "is-primary is-lg is-block is-disabled")}</div></section>')
    sh = ios_sheet("“aeroapp.ai” would like to access the microphone", "", "Don’t Allow", "Allow") if sheet else ""
    return ph_stage(card) + sh


def ph_html_unsupported():
    card = (f'<section class="tx tx-card" style="padding:24px;gap:16px;border-radius:20px">{from_line()}'
            f'<div style="display:grid;gap:8px"><h1>This test needs a computer</h1>'
            f'<p class="tx-sub">Thanks for being up for it. {PROTO} is tested in a desktop browser, because the test records a browser tab and phones can’t do that.</p></div>'
            f'<div class="tx-note">{ic("laptop")}<span>Open this link on a laptop or desktop, in Chrome or Edge:<br><b class="tx-mono" style="font-size:12px">{LINK}</b></span></div>'
            f'<div class="tx-actions">{btn("Copy link", "is-primary is-lg is-block", "primary", icon="copy")}{btn("Email it to myself", "is-lg is-block", icon="mail")}</div>'
            f'<p class="tx-fine">Nothing has been recorded.</p></section>')
    return f'<div class="tx-stage is-wash" style="padding:12px;place-items:center">{card}</div>'


# ---------------------------------------------------------------- the colour test
THEMES = [("dark", "Black", "#000 app, lime accent"), ("light", "White", "#FFF, ink text"), ("bright", "Bright", "Full-bleed coral"),
          ("busy", "Busy", "Card art, stripes, dots"), ("blue", "Aero-like blue", "#2F6BFF, clashes with the dot"), ("sun", "Light and bright", "Full-bleed yellow")]
APPROACHES = [("today", "Today’s glass panel", tag("no", "Fails")), ("plate", "A. Plate", tag("rec")),
              ("glass", "B. V3 glass panel", tag("prop", "Option")), ("mini", "Minimised pill, V3 glass", tag("rec"))]


APPNAME = {"today": "Today\u2019s glass", "plate": "A. Plate (recommended)", "glass": "B. V3 glass panel", "mini": "Minimised pill"}


def tile(theme, style):
    page = proto_web(theme)
    if style == "mini":
        p = mini(1)
    else:
        p = panel(1, "task", style=style)
    key = f"{theme}:{style}"
    sc = CONTRAST.get(key)
    score = ""
    if sc:
        v = sc["min"]
        cls = "ok" if v >= 4.5 else "bad"
        score = f'<span class="tb-score {cls}" data-score>{v:.1f}:1 {"AA" if v >= 4.5 else "fails"}</span>'
    # crop: the bottom-right corner of a 1280x720 page
    inner = (f'<div class="tb-tile" data-tile="{key}"><div style="position:absolute;right:0;bottom:0;width:1280px;height:720px">{page}</div>'
             f'<div class="tx-float br" data-measure>{p}</div></div>')
    return f'<div style="position:relative">{score}{shot(inner, 560, 300)}<span class="tb-tilecap">{APPNAME[style]}</span></div>'


def colour_test():
    head = '<div></div>' + "".join(f'<div class="ch {"" if k == 0 else ""}">{n} {t}</div>' for k, (s, n, t) in enumerate(APPROACHES))
    rows = ""
    for th, name, d in THEMES:
        rows += f'<div class="rh">{name}<small>{d}</small></div>' + "".join(tile(th, s) for s, _, _ in APPROACHES)
    return f'<div class="tb-ct">{head}{rows}</div>'


# ---------------------------------------------------------------- page
def build_board():
    o = [HEAD.format(title="Aero tester flow", desc="Screen 10: what a tester sees, every step and variation, and the colour test for the task panel.")]
    o.append(f"""<div class="tb-top"><div class="tb-wrap"><span class="tb-logo">Aero<i>.</i></span><span class="tb-crumb">App UI round · screen 10 · tester</span>
<nav class="tb-toc"><a href="#map">Journey</a><a href="#welcome">Welcome</a><a href="#allow">Allow</a><a href="#html">Two tabs</a><a href="#panel">Task panel</a><a href="#colour">Colour test</a><a href="#rec">Recording</a><a href="#rate">Ratings</a><a href="#done">Done</a><a href="#vars">Variations</a><a href="#preview">Preview</a><a href="#glass">Glass</a><a href="#whatif">What if</a><a href="#copy">Copy</a><a href="tester-flow.html">Clickable flow →</a></nav></div></div>
<header class="tb-hero"><div class="tb-wrap"><h1>What a tester sees<i>.</i></h1>
<p>The person opening a test link has never heard of Aero and is doing {DESIGNER} a favour. Every screen tells them who asked, what happens, what is recorded and that they can stop. Example: {DESIGNER} at {STUDIO} testing {PROTO}, a payments prototype at {SITE}.</p>
<div class="tb-legend"><span>{tag("rec")} the pick</span><span>{tag("today")} works like this in the code now</span><span>{tag("prop")} needs new work</span><span>{tag("fix")} fixes a known bug</span><span>{tag("no")} shown for comparison</span><span><span class="tb-tag" style="border:1px dashed #BDC1C6;background:#fff">Chrome, not Aero</span> the browser’s own UI, simplified</span></div></div></header>""")

    # principles
    pr = [("01", "Say it before asking", "Who asked, what happens, what is recorded, who sees it, stop any time. Before any browser prompt."),
          ("02", "One permission step", "Mic and tab on one card, in order. Four modals today become two screens."),
          ("03", "Solid where you read", "The task panel is a frosted plate (86% white), so it reads on any prototype. Glass only on small floating chrome."),
          ("04", "Never in the way", "The panel moves to any corner and folds to a pill. On a phone it docks below the prototype instead of over it."),
          ("05", "Say what’s lost", "Every failure says what still works and what doesn’t: no mic means no transcript; no tab means voice only.")]
    o.append(sec("00", "principles", "Five rules for every tester screen",
                 "Drawn from the bugs (B15, B16), the review’s tester section and Duane’s note that the panel has to work over prototypes of any colour.",
                 '<div class="tb-pr">' + "".join(f'<div><span class="tb-num">{a}</span><b>{b}</b><p>{c}</p></div>' for a, b, c in pr) + "</div>"))

    # journey map
    cols = ["Opens the link", "Welcome", "Allow", "Opens / shares", "Tasks", "Finish, rate", "Thanks"]
    rows = [
        ("Figma, computer", "One tab", ["Tab 1 · " + LINK, "Card over the dimmed prototype", "Mic, then this tab (Chrome: Allow)", "Not needed: the prototype is in this tab", "Panel floats over the prototype", "Rating inside the panel", "Same tab: sending, then Sent"], []),
        ("Figma, phone", "Voice only", ["Tab 1", "Card says: only your voice", "Mic only (iOS or Android sheet)", "Not needed", "Bar docked under the prototype", "Rating in the bar’s sheet", "Same tab"], []),
        ("HTML, computer", "Two tabs", ["Tab 1 · controller", "Card mentions the second tab", "Mic", f"Opens tab 2 · {SITE}, then pick it in Chrome", "Panel in tab 2; list in tab 1", "Finish in either; rating in tab 1", "Tab 1: sending, then Sent"], [3, 4]),
        ("HTML, phone", "Not supported", ["Tab 1", "“This test needs a computer”", "", "", "", "", "Copy link, nothing recorded"], ["off"]),
    ]
    m = '<div class="h">Context</div>' + "".join(f'<div class="h">{c}</div>' for c in cols)
    for name, sub, steps, flags in rows:
        m += f'<div class="r">{name}<small>{sub}</small></div>'
        for k, s in enumerate(steps):
            cls = "s"
            if "off" in flags and not s:
                cls += " off"
            if k in flags:
                cls += " tab2"
            em = ""
            if name.startswith("HTML, computer"):
                em = "<em>" + ("tab 2" if k in (3, 4) else "tab 1") + "</em>"
            m += f'<div class="{cls}" data-h="{cols[k]}">{em}{s or "Not used"}</div>'
    o.append(sec("01", "map", "The journey, by context",
                 f"Which tab is in front at each step. Figma tests stay in one tab ({'preferCurrentTab'}). HTML tests need two: the site runs in its own tab so it behaves as it would for real, and the first tab records it. HTML tests are computer only. A phone with Figma records the voice only.",
                 f'<div class="tb-map">{m}</div>'))

    # 02 welcome
    a = opt("Card over the prototype", tag("rec"), shot(scr_welcome_a()),
            ul("The prototype is visible but dimmed: the tester sees what they are about to try.",
               f"{DESIGNER}’s own message is a quote with her name, so her voice and Aero’s stay apart.",
               "“What’s recorded” is four plain facts, including what is never used (camera).",
               "No time estimate: sessions have no fixed length. “Take as long as you need” instead."), "A")
    b = opt("A page first", tag("prop", "Option"), shot(scr_welcome_b()),
            ul("Calmer and more branded, with a preview of the panel.",
               "But the preview is a picture of something they’re about to see anyway, and the prototype loads later, so Start feels slower.",
               "Worth it only if testers often bounce from the card. Keep A."), "B")
    o.append(sec("02", "welcome", "Invite and welcome",
                 "Today: “Welcome!” with a wave emoji, “0 tasks · About 1 minute” on free exploration (B15), and an em dash. The fix: say who asked, what happens, what’s recorded, then one Start button.",
                 grid(2, a, b) + '<h3 class="tb-h3">Same card, other contexts</h3>' +
                 grid(3, opt("HTML test", tag("today", "Today’s flow"), shot(scr_welcome_a("html")), "Step 2 says the site opens in a second tab, before it happens."),
                      opt("No tasks", tag("fix", "Fixes B15"), shot(scr_welcome_a("figma", tasks=False)), "No count, no minutes. “Look around Pocket for as long as you like.”"),
                      opt("Phone, Figma", tag("today", "Voice only"), shot(phone(ph_stage(welcome_card("phone"))), 390, 844), "The screen fact is struck through: “Phones can’t share a tab, so only your voice.”")) +
                 '<h3 class="tb-h3">If cursor and click tracking ships</h3>' +
                 grid(3, opt("Today", tag("today"), shot(scr_welcome_a("html")), "Voice and the Pocket tab. A tab recording shows no mouse, so the card says nothing about the pointer."),
                      opt("HTML, with tracking", tag("prop"), shot(scr_welcome_a("html", clicks=True)), "The overlay script would send pointer moves, clicks and scroll inside Pocket. Consent must say so before Start: “Where you move, click and scroll”."),
                      opt("Figma, with tracking", tag("prop"), shot(scr_welcome_a("figma", clicks=True)), "Figma’s Embed API gives clicks and screen changes, not movement, so it says “Where you click” and nothing more. See research/cursor-recording.md."))))

    # 03 allow
    s1 = shot(scr_allow("active", "waiting", mic_prompt()), cap="<b>1.</b> Allow is pressed, Chrome asks for the mic. The row being asked about is outlined.")
    s2 = shot(scr_allow("ok", "active", tab_prompt()), cap="<b>2.</b> Share tab: with <span class=tx-mono>preferCurrentTab</span> Chrome only asks about this tab. No list to pick from.")
    s3 = shot(scr_allow("ok", "ok", ready=True), cap="<b>3.</b> Both done. Chrome’s blue “sharing this tab” bar appears. The think-aloud tip lands here, next to Start.")
    two = (f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">'
           f'<div class="tb-shot" data-w="560" data-h="420"><div class="tb-scale" style="width:560px;height:420px;position:relative;background:var(--tx-dim);display:grid;place-items:center">'
           f'{msg_card("Enable audio", "We’d like to record your voice as you share your thoughts.", btn("Enable microphone", "is-primary is-block") + btn("Continue without audio", "is-block"))}</div></div>'
           f'<div class="tb-shot" data-w="560" data-h="420"><div class="tb-scale" style="width:560px;height:420px;position:relative;background:var(--tx-dim);display:grid;place-items:center">'
           f'{msg_card("Screen recording", "We’d like to record your screen to see how you navigate.", btn("Share screen", "is-primary is-block") + btn("Skip", "is-block"))}</div></div></div>')
    o.append(sec("03", "allow", "Microphone and screen share, in one step",
                 "Today these are two modals, then a third for think-aloud tips, then the prototype. The review asked for one “Allow recording” step. Each row has its own button because each opens its own browser prompt, and browsers only allow that from a click.",
                 grid(3, opt("Step 1 of 2", tag("rec"), s1), opt("Step 2 of 2", tag("rec"), s2), opt("Ready", tag("rec"), s3)) +
                 '<h3 class="tb-h3">B. Today’s structure, restyled</h3>' + grid(2, opt("Two separate steps", tag("no", "Not recommended"), two,
                    "Same facts across two screens plus a tips screen. More clicks before the prototype and no overview of what’s left. Keep A."),
                    '<div class="tb-box"><h4>Why the order is mic first, then tab</h4><p>The voice carries the value: without it there is no transcript, summary or friction points. Asking for it first, while the tester is most willing, gets more audio. The tab share is the bigger ask and comes second, with the facts already on screen.</p><h4 style="margin-top:14px">Browser notes</h4>' +
                    ul("Chrome and Edge: the tab prompt is a single Allow (<span class=tx-mono>preferCurrentTab</span>).",
                       "Firefox and Safari can’t share a single tab: they show a window or screen list. The helper line changes to “Choose the window with Pocket in it.”",
                       "Start enables as soon as the mic is decided (allowed, blocked and accepted, or skipped).") + "</div>")))

    # 04 HTML two tabs
    h1 = shot(chrome(f'<div class="tx-stage is-wash">{html_open_card()}</div>', [("Testing Pocket", "ae", True, False)]), cap="<b>1.</b> Mic done. Open Pocket opens tab 2.")
    h2 = shot(chrome(proto_web("light") + f'<div class="tx-float br">{overlay_wait()}</div>', HTABS_POCKET, url=SITE),
              cap=f"<b>2.</b> Tab 2 opens in front. Today its panel already shows Task 1, though nothing records yet. Proposed: a “not recording yet” state that sends them back.")
    h3 = shot(chrome(f'<div class="tx-stage is-wash">{html_share_card()}</div>' + tab_picker(), HTABS_CTRL), cap="<b>3.</b> Back in tab 1: Share opens Chrome’s picker. They choose Chrome tab, then Pocket.")
    h4 = shot(chrome(proto_web("light") + f'<div class="tx-float br">{panel(0, "task")}</div>', HTABS_POCKET_REC, url=SITE, share="This tab is being shared with aeroapp.ai."),
              cap="<b>4.</b> Chrome jumps to Pocket. The panel shows the task; the blue bar shows it’s shared.")
    h5 = shot(chrome(f'<div class="tx-stage is-wash is-top">{html_ctrl_testing(1)}</div>', HTABS_CTRL_REC), cap="<b>5.</b> Tab 1 meanwhile: the full list, a backup Done, Finish early.")
    h6 = shot(chrome(proto_web("light") + f'<div class="tx-float br">{overlay_finished()}</div>', HTABS_POCKET, url=SITE),
              cap="<b>6.</b> After Finish in tab 2: today the panel just disappears. Proposed: tell them where to go.")
    errs = grid(4,
                opt("Wrong tab", tag("today"), shot(chrome(f'<div class="tx-stage is-wash">{html_share_card("wrong")}</div>', HTABS_CTRL), 1280, 800)),
                opt("A window, not a tab", tag("today"), shot(chrome(f'<div class="tx-stage is-wash">{html_share_card("nottab")}</div>', HTABS_CTRL), 1280, 800)),
                opt("Cancelled twice", tag("today"), shot(chrome(f'<div class="tx-stage is-wash">{html_share_card("denied", 2)}</div>', HTABS_CTRL), 1280, 800), "After two misses the whole-screen option appears."),
                opt("Whole screen chosen", tag("today"), shot(chrome(f'<div class="tx-stage is-wash">{html_share_card("fallback")}</div>', HTABS_CTRL), 1280, 800), "Red, not amber: privacy changes."))
    pop = opt("New tab blocked", tag("today"), shot(chrome(f'<div class="tx-stage is-wash">{html_open_card(True)}</div>', [("Testing Pocket", "ae", True, False)],
                                                         url_extra='<span class="blocked">⧉ Pop-up blocked</span>')))
    o.append(sec("04", "html", "HTML sites: the two-tab flow",
                 f"An HTML test can’t embed the site, so tab 1 ({LINK}) records and tab 2 ({SITE}) is the site, with a small panel injected into every page. The tester must pick tab 2 in Chrome’s list, and the code checks the pick (Capture Handle). This is the most confusing part of testing, so each step names the tab and says why.",
                 grid(3, h1, h2, h3) + '<div style="height:24px"></div>' + grid(3, h4, h5, h6) + '<h3 class="tb-h3">When the pick goes wrong</h3>' + errs + '<div style="height:24px"></div>' + grid(3, pop, "", "")))

    # 05 panel
    pa = opt("A. Plate", tag("rec"), shot(scr_testing("task", 1, proto=proto_web("busy"), share=SHARE_THIS)),
             ul("The shared plate token (86% white, 22px blur), a dark hairline outside a white one, and a soft shadow. Measured 14:1 or better on all six test prototypes.",
                "Glass only on the Done button: it picks up the prototype’s colour at its edge, so the panel feels part of the moment without risking the text.",
                "Same component for Figma (in the page) and HTML (injected into the site, in a closed shadow root)."), "A")
    pb = opt("B. V3 glass panel", tag("prop", "Option"), shot(scr_testing("task", 1, proto=proto_web("busy"), style="glass")),
             ul("The whole panel is V3 dark glass; the engine raises the tint until the text passes.",
                "Prettier on calm prototypes, but over busy ones the tint ends up nearly opaque anyway, and the refracted edge shows in every recording.",
                "Safari and Firefox get frost only. Keep for floating chrome, not for reading."), "B")
    pc = opt("C. Docked rail (Figma only)", tag("prop", "Option"), shot(scr_rail(1)),
             ul("Never covers the prototype; the whole list is visible.",
                "The Figma frame shrinks to fit: fine for phone frames, 22% smaller for desktop frames.",
                "Impossible for HTML tests (the site is its own tab), so it would be a second design to keep. Use the docked idea on phones only."), "C")
    states = grid(4,
                  opt("Before they\u2019ve tried", tag("today"), closeup(panel(0, interacted=False), "light", 430, cap="Done waits until they interact. The hint says why.")),
                  opt("Menu", tag("rec"), closeup(panel(1, menu=True), "light", 430, cap="Restart Pocket, Move panel (four corners), Mute, End test.")),
                  opt("Moved", tag("prop"), closeup(panel(1), "sun", 430, corner="bl", cap="Moved to bottom left, over a yellow page. Kept for the session.")),
                  opt("Minimised", tag("rec"), closeup(mini(1), "busy", 430, cap="A V3 glass pill: still recording, still shows the task number.")))
    o.append(sec("05", "panel", "The task panel over the prototype",
                 "Prototypes can be any colour, and Aero can’t read their pixels (a Figma embed is a cross-origin frame), so the panel can’t adapt to what’s behind it. It has to work everywhere as it is. Today’s panel is smoky glass with white text: fine on dark prototypes, unreadable on white ones. The panel is also inside every recording, so it shows which task was on screen in the replay.",
                 grid(3, pa, pb, pc) + '<h3 class="tb-h3">Panel states (A)</h3>' + states))

    # 06 colour test
    phones = grid(3, *[opt(n, "", shot(phone(ph_testing(t, 1), dark_status=(t in ("dark", "busy", "bright", "blue"))), 390, 844)) for t, n in (("dark", "Black"), ("bright", "Bright"), ("sun", "Light and bright"))])
    o.append(sec("06", "colour", "Colour test: six prototypes, four treatments",
                 "Each tile is the bottom-right corner of a 1280px Pocket page, with the panel at real size. The badge is the measured contrast of the task title against the worst pixel behind it, taken from a screenshot with the text hidden (script: <span class=tx-mono>tester-measure.mjs</span>). AA for this text is 4.5:1.",
                 colour_test() + '<h3 class="tb-h3">On a phone, the bar docks below the prototype</h3><p class="tb-cap" style="margin-bottom:14px">Nothing overlaps, so colour can’t break it. It never covers the prototype’s own tab bar.</p>' + phones))

    # 07 recording indicator
    chips = "".join(f'<div class="tb-box" style="display:flex;flex-direction:column;gap:8px;padding:16px">{rec_chip(s)}<span class="tb-cap">{d}</span></div>' for s, d in [
        ("live", "Voice and tab. The bars move with their voice, so they know the mic hears them."),
        ("voice", "Mic only: phone, or tab sharing stopped."),
        ("screen", "Tab only: mic blocked or skipped. Amber copy in the panel says what’s lost."),
        ("muted", "Muted from the menu. Grey dot, no bars."),
        ("off", "Network lost. Still recording in the tab."),
        ("saving", "After Finish: sending, with a percentage."),
        ("saved", "Sent. Green."),
        ("bad", "Not sent. The thank-you screen offers Try again.")])
    ra = opt("A. In the panel’s header", tag("rec"), shot(scr_testing("task", 1)),
             "One thing to keep track of. Minimised, the pill keeps it. Chrome adds its own red dot on the tab and the blue sharing bar, so a second Aero badge would be the third signal.", "A")
    rb = opt("B. Separate pill, top centre", tag("today", "Like today"), shot(chrome(proto_figma("light") + f'<div class="tx-float tc"><div class="tx tx-mini">{rec_chip("live")}{btn("Mute", "is-sm is-pill")}</div></div><div class="tx-float br">{panel(1, "task", rec="none")}</div>', FTABS_REC, share=SHARE_THIS)),
             "Two floating objects over the prototype instead of one, and the top centre is where prototypes put their own headers.", "B")
    o.append(sec("07", "rec", "Recording indicator",
                 "Today a separate pill says “Recording”, “Saving...” or “Save failed”. Proposed: it lives in the panel header with an elapsed time and a small level meter (Web Audio analyser on the mic stream, no extra permission).",
                 grid(2, ra, rb) + '<h3 class="tb-h3">States</h3><div class="tb-grid c4">' + chips + "</div>"))

    # 08 next task and ratings
    seq = grid(4,
               opt("1. Task", "", closeup(panel(1, "task"), "light", 430, cap="Done or Couldn\u2019t do it.")),
               opt("2. Rating", tag("rec"), closeup(panel(1, "rate"), "light", 430, cap="In the panel, not a modal. Words, not emoji. Keys 1 to 5.")),
               opt("3. Next task", "", closeup(panel(2, "task", time="03:51"), "light", 430, cap="The next task replaces it. Focus moves to its title.")),
               opt("4. All done", tag("prop"), closeup(panel(3, "last", time="07:15"), "light", 430, cap="A beat for closing thoughts, still recording.")))
    seq2 = grid(4,
                opt("Couldn\u2019t do it", tag("rec"), closeup(panel(1, "stuck-rate"), "dark", 430, cap="Same scale, kinder words. It\u2019s data, not a failure.")),
                opt("End early", tag("rec"), closeup(panel(1, "confirm-end"), "dark", 430, cap="From the menu. What\u2019s done is kept.")),
                opt("Ratings off", tag("today"), closeup(panel(2, "task", time="05:40"), "dark", 430, cap="If the designer turned ratings off, Done goes straight to the next task.")),
                opt("Today", tag("no", "Replace"), shot(chrome(proto_figma("light") + '<div class="tx-stage is-dim"><div class="tx tx-card" style="max-width:420px;text-align:center;gap:14px"><h1 style="font-size:20px">How easy was this?</h1><div style="display:flex;gap:8px;justify-content:center;font-size:26px"><span>\U0001F62B</span><span>\U0001F615</span><span>\U0001F610</span><span>\U0001F642</span><span>\U0001F604</span></div><button class="tx-link is-quiet">Skip</button></div></div>', FTABS_REC, share=SHARE_THIS),
                                                                  cap="A modal of emoji over the prototype. Faces read differently across cultures and screen readers.")))
    o.append(sec("08", "rate", "Next task and ratings",
                 "Ratings are optional per test (askDifficulty). On Figma tests they come after each task; on HTML tests the code asks once, for the whole session, in tab 1.",
                 seq + '<div style="height:24px"></div>' + seq2))

    # 09 done and saving
    da = grid(3,
              opt("Sending", tag("rec"), cardshot(thanks_card("saving", 72)), "Thanks first, saving second: they’ve finished their part. The bar is real: most of the recording is already uploaded in 5 MB pieces during the test."),
              opt("Sent", tag("rec"), cardshot(thanks_card("done")), "Green, then “You can close this tab now.” What happens next, in one honest line, including transcription."),
              opt("B. Two screens", tag("no", "Not recommended"), cardshot(msg_card("Saving your session", "Please keep this tab open.", extra='<div class="tx-bar"><i style="width:72%"></i></div>')), "A saving screen, then a thank-you. Makes them wait to be thanked."))
    o.append(sec("09", "done", "Done, sending and thank you",
                 "Today: “All Done!” with a party emoji, “Saving your session... please keep this tab open”, then “You can close this tab now.” Leaving early triggers the browser’s own “Leave site?” warning.",
                 da + '<div style="height:24px"></div>' + grid(3,
                     opt("Slow connection", tag("prop"), cardshot(thanks_card("slow", 41))),
                     opt("Didn’t send", tag("prop"), cardshot(thanks_card("bad", 88), 760), "Try again re-runs the upload from the blob still in memory. Download a copy is a last resort they can email to Mia."),
                     opt("Closing too early", tag("today"), shot(chrome(f'<div class="tx-stage is-wash">{thanks_card("saving", 72)}</div><div class="cr-alert"><h4>Leave site?</h4><p>Changes you made may not be saved.</p><div class="btns"><button>Leave</button><button class="is-main">Cancel</button></div></div><span class="cr-tag" style="left:50%;top:150px;transform:translateX(-50%)">Chrome, not Aero</span>', FTABS)),
                         "Chrome’s wording can’t be changed. The bar behind it explains."))))

    # 10 variations
    v_mic = grid(3,
                 opt("Mic blocked", tag("fix", "Fixes B16"), shot(scr_allow("bad", "waiting")),
                     "Today a blocked mic silently moves on and the designer gets a session with no transcript."),
                 opt("Mic blocked: how to fix", tag("prop"), shot(chrome(proto_figma("light") + f'<div class="tx-stage is-dim"><section class="tx tx-card">{from_line()}<div style="display:grid;gap:6px"><h1>Allow recording</h1><p class="tx-sub">Your browser will ask twice. Choose Allow each time.</p></div><div class="tx-perms">' +
                     perm_row("mic", "bad", f'<div class="tx-perm-help"><span>Without your voice, {FIRST} sees what you do but not why. To turn it on: click the icon left of the address bar, set <b>Microphone</b> to <b>Allow</b>.</span><div class="tx-row">{btn("I’ve allowed it", "is-sm is-primary", "primary")}<button class="tx-link is-quiet">Continue without voice</button></div></div>') +
                     perm_row("tab", "waiting") + '</div></section></div>', FTABS, url_extra='<span class="blocked">' + ic("mic") + '</span>')),
                     "A blocked prompt can’t be asked again from the page, so the copy says where the switch is. Proposed: listen for the permission change and continue by itself."),
                 opt("Then: tab only", tag("prop"), shot(scr_testing("task", 1, rec="screen", strip_html=strip("warn", f"<b>Your voice isn’t recorded.</b> {FIRST} will see the screen only.", '<button class="tx-link">Turn on mic</button>'))),
                     "The strip stays until they dismiss it. The designer sees a “No audio” tag on the session (proposed, owner side)."))
    v_tab = grid(3,
                 opt("Figma: tab not shared", tag("today", "Voice only"), shot(scr_allow("ok", "bad", note=f'<div class="tx-note is-warn">{ic("alert")}<span><b>{FIRST} will hear you but won’t see the screen.</b> <button class="tx-link" style="color:inherit">Try again</button> or start with your voice only.</span></div>', ready=True, title="Allow recording")),
                     "Figma tests can go ahead with voice only. Start stays enabled."),
                 opt("Figma: sharing stopped mid-way", tag("today", "Voice goes on"), shot(scr_testing("task", 2, rec="voice", strip_html=strip("warn", f"<b>Screen sharing stopped.</b> Your voice is still recording.", '<button class="tx-link">Share again</button><button class="tx-link">Carry on</button>'), share=None)),
                     "Today video stops and audio continues, silently. Share again is proposed (a new picker and a second video file)."),
                 opt("HTML: sharing stopped mid-way", tag("today", "Ends the test"), shot(chrome(f'<div class="tx-stage is-wash is-top">{html_ctrl_testing(2, "today")}</div>', HTABS_CTRL)),
                     "Today Chrome’s Stop sharing ends the session. Proposed below: pause and offer to share again."))
    v_tab2 = grid(3,
                  opt("HTML: stopped, proposed", tag("prop"), shot(chrome(f'<div class="tx-stage is-wash is-top">{html_ctrl_testing(2, "prop")}</div>', HTABS_CTRL))),
                  opt("No tasks: panel", tag("fix", "Fixes B15"), shot(scr_testing("explore", 0, proto=proto_figma("dark"))), "One sentence and Finish. Nothing to count."),
                  opt("No tasks: HTML tab 1", tag("today"), shot(chrome('<div class="tx-stage is-wash is-top">' + f'<section class="tx tx-card is-wide" style="gap:16px"><div style="display:flex;align-items:center;gap:10px">{mark()}<b style="font-weight:520">Testing {PROTO}</b><span style="margin-left:auto">{rec_chip("live", "02:31")}</span></div><div class="tx-note is-ok">{ic("check")}<span><b>Recording the {PROTO} tab.</b> Look around and say what you think. Come back here when you’re done.</span></div>{btn("Finish", "is-primary is-block is-lg", "primary")}</section></div>', HTABS_CTRL_REC))))
    v_phone = grid(5,
                   opt("Welcome", tag("today"), shot(phone(ph_stage(welcome_card("phone"))), 390, 844)),
                   opt("Mic", tag("rec"), shot(phone(ph_allow()), 390, 844)),
                   opt("Testing", tag("rec"), shot(phone(ph_testing("light", 1)), 390, 844), "Docked under the prototype; the Figma frame fits the space above."),
                   opt("Rating", tag("rec"), shot(phone(f'<div style="position:absolute;inset:0;display:flex;flex-direction:column"><div style="position:relative;flex:1">{proto_app("light")}<div class="tx-stage is-dim" style="padding:0"></div></div><div style="padding:10px;background:#fff">{panel(1, "rate").replace("tx-panel", "tx-panel", 1)}</div></div>'), 390, 844), "The bar opens into a sheet for the rating."),
                   opt("Thanks", tag("rec"), shot(phone(f'<div class="tx-stage is-wash" style="padding:12px;place-items:center">{thanks_card("voice", kind="phone")}</div>'), 390, 844)))
    v_html_phone = grid(3,
                        opt("HTML on a phone", tag("rec"), shot(phone(ph_html_unsupported()), 390, 844),
                            "Today: “Desktop browser required”. Now: thanks first, why in one line, the link to copy. Email it to myself is proposed (needs a small mail function)."),
                        opt("Phone: mic blocked", tag("prop"), shot(phone(ph_stage(f'<section class="tx tx-card" style="padding:24px;gap:16px;border-radius:20px">{from_line()}<div style="display:grid;gap:6px"><h1>No microphone</h1><p class="tx-sub">On a phone the voice is the whole recording. Without it, {FIRST} only sees which tasks you finished.</p></div>{perm_row("mic", "bad")}<div class="tx-note">{ic("info")}<span>Settings, Safari, Microphone, then Allow. Then come back here.</span></div><div class="tx-actions">{btn("Try again", "is-primary is-lg is-block", "primary")}<button class="tx-link is-quiet" style="align-self:center">Continue anyway</button></div></section>')), 390, 844)),
                        opt("Test closed or full", tag("fix"), shot(phone(f'<div class="tx-stage is-wash" style="padding:12px;place-items:center">{msg_card("This test isn’t open right now", f"{DESIGNER} isn’t taking new sessions at the moment. Let {FIRST} know, and thanks for trying.", kind="phone", extra="<p class=tx-fine>Nothing has been recorded.</p>")}</div>'), 390, 844),
                            "Today the limit screen says the owner “reached their session limit”. That exposes the designer’s plan to their tester. One neutral message for both closed and full."))
    v_net = grid(3,
                 opt("Network lost during the test", tag("prop"), shot(scr_testing("task", 2, rec="off", strip_html=strip("warn", "<b>You’re offline.</b> Still recording in this tab. Keep going: it sends when you’re back."))),
                     "MediaRecorder keeps going without a network; only the 5 MB piece uploads fail. Figma screens already loaded still work."),
                 opt("Finished while offline", tag("prop"), shot(scr_thanks("offline", 64))),
                 opt("Back online", tag("prop"), shot(scr_testing("task", 2, strip_html=strip("info", "Back online. Everything so far is saved."))), "Shown for 4 seconds, then the strip folds away."))
    o.append(sec("10", "vars", "Variations",
                 "Every branch a tester can hit, with what the code does today and what is proposed.",
                 '<h3 class="tb-h3" style="margin-top:0">Microphone denied</h3>' + v_mic +
                 '<h3 class="tb-h3">Screen share denied or stopped</h3>' + v_tab + '<div style="height:24px"></div>' + v_tab2 +
                 '<h3 class="tb-h3">Phone with a Figma prototype: voice only</h3>' + v_phone +
                 '<h3 class="tb-h3">HTML on a phone, and other dead ends</h3>' + v_html_phone +
                 '<h3 class="tb-h3">Network lost, slow saving</h3>' + v_net))

    # 11 preview
    pv_bar = (f'<div class="tx tx-preview"><span class="tag">Preview</span><span class="msg">This is what testers see. Nothing is saved and it doesn’t use a session.</span>'
              f'<div class="jump"><button>Welcome</button><button class="is-on">Allow</button><button>Tasks</button><button>Thanks</button></div>'
              f'{btn("Exit preview", "is-sm")}</div>')
    pv = chrome(f'<div style="position:absolute;inset:0;display:flex;flex-direction:column">{pv_bar}<div style="position:relative;flex:1">{proto_figma("light")}'
                f'<div class="tx-stage is-dim">{allow_card("active", "waiting")}</div></div></div>', [("Preview: Pocket", "ae", True, False)], url="aeroapp.ai/pocket?test=1&preview=1")
    share_card = (f'<div class="tx" style="position:absolute;inset:0;background:var(--ae-mist);padding:40px"><div style="max-width:620px;background:#fff;border:1px solid var(--ae-line);border-radius:16px;padding:24px;display:grid;gap:16px">'
                  f'<span class="tx-label">Share</span><div style="display:flex;gap:8px"><div style="flex:1;height:40px;border-radius:10px;box-shadow:inset 0 0 0 1px var(--ae-line-2);display:flex;align-items:center;padding:0 12px;font-family:var(--ae-mono);font-size:13px">{LINK}</div>{btn("Copy link", "is-primary", "primary", icon="copy")}</div>'
                  f'<div style="display:flex;gap:8px">{btn("Open as a tester", "", icon="eye")}{btn("QR code", "")}</div>'
                  f'<p class="tx-fine" style="color:var(--ae-ink-3)">Testers are asked for their microphone and this tab. On a phone, only their voice. Sessions have no fixed length.</p></div></div>')
    o.append(sec("11", "preview", "Open as a tester (designer preview)",
                 "Proposed on the Share tab. Opens the real tester link with <span class=tx-mono>&amp;preview=1</span> in a new tab. The designer sees their own name, message and tasks exactly as testers will. Today the closest thing is the plugin preview, which hides the designer’s name and does record a session.",
                 grid(2, opt("Entry on Share", tag("prop"), shot(share_card, 1280, 420)),
                      opt("Preview, with a jump bar", tag("prop"), shot(pv), ul("A dark bar outside the prototype, so it’s never mistaken for the tester UI and isn’t in any recording.",
                                                                             "Jump straight to any step without allowing the mic again.",
                                                                             "Decision for Duane: record nothing (shown), or record a practice session marked Preview that doesn’t count.")))))

    # 12 glass
    gt = """<table class="tb-table"><tr><th>Where</th><th>Glass?</th><th>Why</th></tr>
<tr><td>Primary buttons on tester cards (Start, Start the test, Copy link)</td><td>V3 primary, subtle</td><td>The same quiet glass as the app’s primary actions. On a white card it barely shows, which is right.</td></tr>
<tr><td>Done in the task panel</td><td>V3 primary, subtle</td><td>The one place the prototype’s colour reaches the panel: a thin reflection on the button’s edge. The label stays ink-on-white AA because the engine nudges the fill.</td></tr>
<tr><td>Minimised pill</td><td>V3 secondary, strength 1.6</td><td>Small floating chrome over unknown colour: exactly what the research says glass is for. The engine raises opacity until the label passes: lowest measured 4.6:1, over black.</td></tr>
<tr><td>Task panel body</td><td>No. Near-opaque plate with a light blur</td><td>Content needs guaranteed contrast. Glass over a busy prototype either fails or becomes opaque. The panel is in every recording, so refraction would also warp the prototype in the replay. Safari and Firefox would get only frost.</td></tr>
<tr><td>Welcome and thank-you cards</td><td>No</td><td>Solid paper on a dim or a soft Test wash. Reading, not floating.</td></tr>
<tr><td>Today’s smoky glass (white text)</td><td>Remove</td><td>Fails on four of six prototypes (measured 2.4:1 on white). It’s also the only glass panel in Aero, which is what Duane spotted.</td></tr></table>"""
    o.append(sec("12", "glass", "Where glass is used, and why",
                 "Duane: “the testing screen uses a glass effect but we don’t use that elsewhere.” With V3 now the app’s button glass, the tester screens use it the same way: on buttons and floating chrome, never on text you have to read.",
                 gt))

    # 13 what if
    wi = [
        ("They open the link in Safari or Firefox", "Figma: works, but the picker lists windows or the screen, not this tab. Helper text says “Choose the window with Pocket in it.” HTML: works with the surface check only (no Capture Handle).", "Today, copy proposed"),
        ("They block the mic", "Row turns red, says what’s lost, shows where the switch is. Continue without voice is allowed on a computer; on a phone it leaves only task results.", "Fix B16"),
        ("They skip the tab share (Figma)", "Voice only. The panel chip says Voice only.", "Today"),
        ("They pick the wrong tab (HTML)", "Rejected by the Capture Handle check, with a message naming the right tab. After two misses: whole screen, with a privacy warning.", "Today"),
        ("Chrome blocks the second tab", "Amber note with the fix; the button stays.", "Today"),
        ("They close the Pocket tab mid-test (HTML)", "Tab 1 says the recording is still running and offers Reopen Pocket.", "Today"),
        ("They close tab 1 mid-test (HTML)", "The recording lives there, so it’s lost after the last 5 MB piece. The browser warns first. The overlay hides itself when its opener is gone.", "Today"),
        ("They press Done without touching the prototype", "Done is disabled until the prototype has had a click or focus, with a hint.", "Today"),
        ("The prototype’s own nav sits under the panel", "Move panel (menu) to any corner, or minimise to a pill. On phones the bar docks below instead.", "Proposed"),
        ("They talk for 40 minutes", "No limit. Uploads go in 5 MB pieces during the test, so Finish is quick.", "Today"),
        ("They refresh mid-test", "A new session starts; the old one keeps what was uploaded. Proposed: resume prompt for 10 minutes.", "Today, resume proposed"),
        ("The network drops", "Recording continues in the tab; pieces upload when back. Offline strip in the panel.", "Proposed UI"),
        ("Two people open the same link", "Two separate sessions. Nothing is shared between testers.", "Today"),
        ("The designer is over their plan’s limit", "Neutral “This test isn’t open right now”. Don’t mention plans to testers.", "Copy fix"),
        ("A screen reader user takes the test", "The panel is a labelled region; new tasks are announced (aria-live polite); the rating is a radio group. Figma prototypes themselves are not accessible, which is outside Aero’s control.", "Proposed"),
    ]
    t = '<table class="tb-table"><tr><th style="width:28%">What happens if</th><th>Then</th><th style="width:16%">Status</th></tr>' + "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in wi) + "</table>"
    acc = ul("Contrast: the panel title and body pass 4.5:1 on all six prototypes (measured). Secondary text on the plate uses ink-2, not ink-3.",
             "Focus: Start and each new task title receive focus; Escape folds the panel to the pill; the pill’s Show restores it.",
             "Announcements: “Task 3 of 4: Freeze your card”, “Recording”, “Sent” are aria-live polite. Errors are role=alert.",
             "Ratings: a radio group with text labels, keys 1 to 5. No emoji.",
             "Colour is never the only signal: every state has words (Rec, Muted, Offline, Sent).",
             "Motion: the pulse and level meter stop under prefers-reduced-motion.",
             "Targets: 40px buttons on desktop, 46px on phones; the rating buttons are 48px tall.")
    o.append(sec("13", "whatif", "What happens if…",
                 "The software engineer’s pass. Each answer matches the code today or says what’s proposed.",
                 '<div class="tb-scroll">' + t + '</div><h3 class="tb-h3">Accessibility review</h3><div class="tb-box">' + acc + "</div>"))

    # 14 copy deck
    cd = [("welcome.title", "Welcome!", f"{DESIGNER} asked you to try {PROTO}."),
          ("welcome.meta", "0 tasks · About 1 minute", "(hidden) Take as long as you need, and stop at any time."),
          ("welcome.note", "There are no right or wrong answers—we’re testing the design, not you!", f"There are no right or wrong answers. You’re testing {PROTO}, not yourself."),
          ("welcome.cta", "Get Started", "Start"),
          ("welcome.recorded (if tracking ships)", "Only this tab is recorded.", f"Proposed: your voice, the {PROTO} tab, and where you move, click and scroll inside {PROTO} (HTML). Figma: where you click."),
          ("allow.title", "Enable Audio / Screen Recording", "Allow recording"),
          ("allow.mic.sub", "We’d like to record your voice as you share your thoughts.", f"So {FIRST} hears what you think."),
          ("allow.tab.sub", "Only this tab is recorded. You can stop anytime.", "Only this tab. Nothing else on your screen."),
          ("allow.micBlocked", "(nothing, moves on)", f"Without your voice, {FIRST} sees what you do but not why."),
          ("tips", "Don’t worry about being polished—just speak naturally!", "Talk as you go. Half-finished thoughts are fine."),
          ("panel.hint", "Interact with the prototype first", f"Try it in {PROTO} first, then press Done."),
          ("panel.done", "✓ Done", "Done"),
          ("panel.explore", "Share your thoughts as you explore", f"Look around {PROTO} and say what you think."),
          ("panel.end", "End session early / End Session", "End test"),
          ("rate.q", "How easy was this?", "How easy was that?"),
          ("html.open", "Open the Prototype", "Two tabs for this test"),
          ("html.share", "Share the Prototype Tab", f"Share the {PROTO} tab"),
          ("done.title", "All Done!", "Thanks, you’re done."),
          ("done.saving", "Saving your session... please keep this tab open", f"Sending your recording to {FIRST}. Keep this tab open until it’s sent."),
          ("done.saved", "You can close this tab now.", "Sent. You can close this tab now."),
          ("limit", "The owner of this project has reached their session limit.", f"{DESIGNER} isn’t taking new sessions at the moment."),
          ("mobile.html", "Desktop browser required", "This test needs a computer.")]
    c = '<div class="tb-copy"><div class="hd">Key</div><div class="hd hide-m">Today</div><div class="hd hide-m">Proposed</div>' + "".join(f'<div class="k">{a}</div><div class="old">{b}</div><div>{d}</div>' for a, b, d in cd) + "</div>"
    o.append(sec("14", "copy", "Copy deck",
                 "Every tester string, today and proposed. Sentence case, British spelling, no emoji, no em dashes, no exclamation marks. Copy lives in the test’s strings, not inside the components.",
                 c))

    o.append(f'<footer class="tb-foot"><div class="tb-wrap">Screen 10 of the app UI round. Example data: {DESIGNER} and {STUDIO} are made up. Built from <span class="tx-mono">tokens.css</span> + <span class="tx-mono">tester.css</span>; generated by <span class="tx-mono">src/tester-build.py</span>. <a href="tester-flow.html">Clickable flow →</a></div></footer>')
    o.append(FOOT_JS)
    return "".join(o)


if __name__ == "__main__":
    html = build_board()
    open(os.path.join(ROOT, "tester.html"), "w").write(html)
    print("tester.html", len(html))


# ================================================================ clickable flow
FLOW_CSS = """<style>
.fl-top{position:sticky;top:0;z-index:50;background:rgba(250,250,249,.9);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);border-bottom:1px solid var(--ae-line)}
.fl-top .tb-wrap{display:flex;align-items:center;gap:20px;height:56px}
.fl-pick{display:flex;gap:6px;flex-wrap:wrap;padding:18px 0 6px}
.fl-pick button{height:32px;padding:0 12px;border-radius:999px;border:0;background:var(--ae-paper);box-shadow:inset 0 0 0 1px var(--ae-line-2);font:inherit;font-size:13px;color:var(--ae-ink-2);cursor:pointer}
.fl-pick button.is-on{background:var(--ae-ink);color:#fff;box-shadow:none}
.fl-head{display:flex;align-items:baseline;gap:14px;margin:18px 0 12px;flex-wrap:wrap}
.fl-head h1{margin:0;font-size:26px;font-weight:400;letter-spacing:-.025em}
.fl-head .c{font-family:var(--ae-mono);font-size:12px;color:var(--ae-ink-3)}
.fl-nav{margin-left:auto;display:flex;gap:8px}
.fl-stage{display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:28px;align-items:start}
.fl-screen{min-width:0}
.fl-screen [data-screen] .tb-shot{margin:0 auto}
.fl-screen [data-screen].is-phone .tb-shot{max-width:min(390px,calc((100vh - 230px) * .462))}
.fl-side{position:sticky;top:76px;display:grid;gap:14px}
.fl-note{font-size:14px;color:var(--ae-ink-2);background:var(--ae-paper);border:1px solid var(--ae-line);border-radius:14px;padding:16px 18px;min-height:80px}
.fl-note b{color:var(--ae-ink);font-weight:500}
.fl-dots{display:grid;gap:2px;counter-reset:d}
.fl-dots button{display:flex;align-items:center;gap:10px;text-align:left;border:0;background:none;padding:7px 10px;border-radius:8px;font:inherit;font-size:13px;color:var(--ae-ink-3);cursor:pointer;counter-increment:d}
.fl-dots button::before{content:counter(d);width:20px;height:20px;border-radius:50%;box-shadow:inset 0 0 0 1px var(--ae-line-2);font:500 10.5px/20px var(--ae-mono);text-align:center;flex:none}
.fl-dots button.is-on{background:var(--ae-paper);color:var(--ae-ink);box-shadow:0 0 0 1px var(--ae-line)}
.fl-dots button.is-on::before{background:var(--ae-blue);color:#fff;box-shadow:none}
.is-hot{cursor:pointer;animation:fl-hot 1.6s ease-in-out infinite}
@keyframes fl-hot{0%,100%{box-shadow:0 0 0 0 rgba(52,120,246,.0),0 0 0 0 rgba(52,120,246,.0)}50%{box-shadow:0 0 0 4px rgba(52,120,246,.55),0 0 0 10px rgba(52,120,246,.12)}}
@media (prefers-reduced-motion:reduce){.is-hot{animation:none;box-shadow:0 0 0 3px rgba(52,120,246,.55)}}
.fl-hint{font-size:12.5px;color:var(--ae-ink-3)}
@media (max-width:600px){.fl-top .tb-crumb{display:none}}
@media (max-width:900px){.fl-stage{grid-template-columns:1fr}.fl-side{position:static}.fl-dots{grid-template-columns:1fr 1fr}}
</style>"""


def build_flow():
    S = {}  # id -> (html, w, h)

    def d(i, html):
        S[i] = (html, 1280, 800)

    def m(i, html):
        S[i] = (phone(html), 390, 844)

    # Figma, computer
    d("f-welcome", scr_welcome_a())
    d("f-mic", scr_allow("active", "waiting", mic_prompt()))
    d("f-tab", scr_allow("ok", "active", tab_prompt()))
    d("f-ready", scr_allow("ok", "ok", ready=True))
    d("f-t1-new", scr_testing("task", 0, interacted=False))
    d("f-t1", scr_testing("task", 0, time="00:48"))
    d("f-r1", scr_testing("rate", 0, time="01:30"))
    d("f-t2", scr_testing("task", 1, time="01:34"))
    d("f-menu", scr_testing("task", 1, menu=True, time="02:10"))
    d("f-mini", scr_mini())
    d("f-t4", scr_testing("task", 3, time="06:02"))
    d("f-last", scr_testing("last", 3, time="07:15"))
    d("f-sending", scr_thanks("saving", 72))
    d("f-sent", scr_thanks("done"))
    # HTML, computer
    d("h-welcome", scr_welcome_a("html"))
    d("h-mic", scr_allow("active", "waiting", mic_prompt(), kind="html"))
    d("h-open", chrome(f'<div class="tx-stage is-wash">{html_open_card()}</div>', [("Testing Pocket", "ae", True, False)]))
    d("h-wait", chrome(proto_web("light") + f'<div class="tx-float br">{overlay_wait()}</div>', HTABS_POCKET, url=SITE))
    d("h-share", chrome(f'<div class="tx-stage is-wash">{html_share_card()}</div>', HTABS_CTRL))
    d("h-picker", chrome(f'<div class="tx-stage is-wash">{html_share_card()}</div>' + tab_picker(), HTABS_CTRL))
    d("h-wrong", chrome(f'<div class="tx-stage is-wash">{html_share_card("wrong")}</div>', HTABS_CTRL))
    d("h-t1", chrome(proto_web("light") + f'<div class="tx-float br">{panel(0, "task")}</div>', HTABS_POCKET_REC, url=SITE, share="This tab is being shared with aeroapp.ai."))
    d("h-ctrl", chrome(f'<div class="tx-stage is-wash is-top">{html_ctrl_testing(1)}</div>', HTABS_CTRL_REC))
    d("h-t4", chrome(proto_web("light") + f'<div class="tx-float br">{panel(3, "last")}</div>', HTABS_POCKET_REC, url=SITE, share="This tab is being shared with aeroapp.ai."))
    d("h-fin", chrome(proto_web("light") + f'<div class="tx-float br">{overlay_finished()}</div>', HTABS_POCKET, url=SITE))
    rate_all = (f'<section class="tx tx-card" style="gap:16px">{from_line()}<h1>How easy was Pocket to use, overall?</h1>'
                f'<div class="tx-rate" role="radiogroup">' + "".join(f'<button><b>{a}</b>{t}</button>' for a, t in [("1", "Very hard"), ("2", "Hard"), ("3", "OK"), ("4", "Easy"), ("5", "Very easy")]) +
                f'</div><button class="tx-link is-quiet" style="align-self:start">Skip</button></section>')
    d("h-rate", chrome(f'<div class="tx-stage is-wash">{rate_all}</div>', HTABS_CTRL))
    d("h-sent", scr_thanks("done"))
    # phone
    m("p-welcome", ph_stage(welcome_card("phone")))
    m("p-mic", ph_allow())
    m("p-ready", ph_stage(f'<section class="tx tx-card" style="padding:24px;gap:16px;border-radius:20px">{from_line()}<h1>You’re ready</h1>{perm_row("mic", "ok")}{think_aloud()}<div class="tx-actions">{btn("Start the test", "is-primary is-lg is-block", "primary")}</div></section>'))
    m("p-t1", ph_testing("light", 0))
    m("p-rate", f'<div style="position:absolute;inset:0;display:flex;flex-direction:column"><div style="position:relative;flex:1">{proto_app("light")}<div class="tx-stage is-dim" style="padding:0"></div></div><div style="padding:10px;background:#fff">{panel(0, "rate")}</div></div>')
    m("p-t2", ph_testing("light", 1))
    m("p-sent", f'<div class="tx-stage is-wash" style="padding:12px;place-items:center">{thanks_card("voice", kind="phone")}</div>')
    m("p-html", ph_html_unsupported())
    # no tasks
    d("n-welcome", scr_welcome_a("figma", tasks=False, theme="dark"))
    d("n-ready", scr_allow("ok", "ok", ready=True, theme="dark"))
    d("n-explore", scr_testing("explore", 0, proto=proto_figma("dark"), time="03:20"))
    d("n-sent", scr_thanks("done"))
    # mic denied
    d("x-ask", scr_allow("active", "waiting", mic_prompt()))
    d("x-blocked", chrome(proto_figma("light") + f'<div class="tx-stage is-dim"><section class="tx tx-card">{from_line()}<div style="display:grid;gap:6px"><h1>Allow recording</h1><p class="tx-sub">Your browser will ask twice. Choose Allow each time.</p></div><div class="tx-perms">' +
                         perm_row("mic", "bad", f'<div class="tx-perm-help"><span>Without your voice, {FIRST} sees what you do but not why. To turn it on: click the icon left of the address bar, set <b>Microphone</b> to <b>Allow</b>.</span><div class="tx-row">{btn("I’ve allowed it", "is-sm is-primary", "primary")}<button class="tx-link is-quiet">Continue without voice</button></div></div>') +
                         perm_row("tab", "waiting") + '</div></section></div>', FTABS, url_extra='<span class="blocked">' + ic("mic") + '</span>'))
    d("x-tab", scr_allow("na", "active", tab_prompt()))
    d("x-test", scr_testing("task", 0, rec="screen", strip_html=strip("warn", f"<b>Your voice isn’t recorded.</b> {FIRST} will see the screen only.", '<button class="tx-link">Turn on mic</button>')))
    # sharing stopped
    d("s-t2", scr_testing("task", 1))
    d("s-fig", scr_testing("task", 1, rec="voice", strip_html=strip("warn", "<b>Screen sharing stopped.</b> Your voice is still recording.", '<button class="tx-link">Share again</button><button class="tx-link">Carry on</button>'), share=None))
    d("s-html-today", chrome(f'<div class="tx-stage is-wash is-top">{html_ctrl_testing(2, "today")}</div>', HTABS_CTRL))
    d("s-html-prop", chrome(f'<div class="tx-stage is-wash is-top">{html_ctrl_testing(2, "prop")}</div>', HTABS_CTRL))
    # network and saving
    d("w-off", scr_testing("task", 2, rec="off", strip_html=strip("warn", "<b>You’re offline.</b> Still recording in this tab. Keep going: it sends when you’re back.")))
    d("w-back", scr_testing("task", 2, strip_html=strip("info", "Back online. Everything so far is saved.")))
    d("w-slow", scr_thanks("slow", 41))
    d("w-bad", scr_thanks("bad", 88))
    d("w-sent", scr_thanks("done"))
    # preview
    pv_bar = (f'<div class="tx tx-preview"><span class="tag">Preview</span><span class="msg">This is what testers see. Nothing is saved and it doesn’t use a session.</span>'
              f'<div class="jump"><button class="is-on">Welcome</button><button>Allow</button><button>Tasks</button><button>Thanks</button></div>{btn("Exit preview", "is-sm")}</div>')
    pv_bar2 = pv_bar.replace('<button class="is-on">Welcome</button><button>Allow</button><button>Tasks</button>', '<button>Welcome</button><button>Allow</button><button class="is-on">Tasks</button>')
    d("v-1", chrome(f'<div style="position:absolute;inset:0;display:flex;flex-direction:column">{pv_bar}<div style="position:relative;flex:1">{proto_figma("light")}<div class="tx-stage is-dim">{welcome_card()}</div></div></div>', [("Preview: Pocket", "ae", True, False)], url="aeroapp.ai/pocket?test=1&preview=1"))
    d("v-2", chrome(f'<div style="position:absolute;inset:0;display:flex;flex-direction:column">{pv_bar2}<div style="position:relative;flex:1">{proto_figma("light")}<div class="tx-float br">{panel(0, "task")}</div></div></div>', [("Preview: Pocket", "ae", True, False)], url="aeroapp.ai/pocket?test=1&preview=1"))

    P = ".ae-btn--primary:not(.is-disabled)"
    flows = {
        "figma": {"name": "Figma on a computer", "steps": [
            ("Welcome", "f-welcome", P, f"<b>{DESIGNER} sent a link.</b> The prototype loads behind a dimmed card that says who asked, what happens and what is recorded."),
            ("Microphone", "f-mic", ".cr-prompt .is-main", "Allow on the row opens <b>Chrome’s own prompt</b>. Aero can’t style it, so the card says which button to press."),
            ("This tab", "f-tab", ".cr-dialog .is-main", "Share tab asks for <b>this tab only</b> (preferCurrentTab). No list to pick from in Chrome or Edge."),
            ("Ready", "f-ready", P, "Both allowed. Chrome adds its blue sharing bar and a red dot on the tab. The think-aloud tip sits next to Start."),
            ("Task 1, not tried yet", "f-t1-new", None, "Done stays disabled until they’ve interacted with the prototype. The hint says why. <span class=fl-hint>(Next to continue.)</span>"),
            ("Task 1", "f-t1", P, "Now Done is live. The panel header shows the time and a level meter, so they know they’re heard."),
            ("Rating", "f-r1", ".tx-rate button:nth-child(4)", "If the designer asked for ratings: five labelled buttons, inside the panel. Keys 1 to 5."),
            ("Task 2", "f-t2", ".tx-panel-h .tx-icon", "The next task replaces it. Focus moves to the title and it is announced to screen readers."),
            ("Menu", "f-menu", ".tx-menu button:nth-child(2)", "The menu: restart the prototype, move the panel to another corner, mute, or end the test."),
            ("Minimised", "f-mini", ".tx-mini .tx-btn", "Folded to a V3 glass pill: still recording, still showing the task number."),
            ("Task 4", "f-t4", P, "Last task."),
            ("Anything else?", "f-last", P, "A beat for closing thoughts while it’s still recording."),
            ("Sending", "f-sending", None, "Thanks first. The bar is real: most of the recording uploaded in 5 MB pieces during the test."),
            ("Sent", "f-sent", None, "They can close the tab. One honest line on what happens next, including transcription."),
        ]},
        "html": {"name": "HTML site on a computer", "steps": [
            ("Welcome", "h-welcome", P, "Step 2 tells them now that Pocket will open in a second tab."),
            ("Microphone", "h-mic", ".cr-prompt .is-main", "Only the mic here. The tab is shared later, once it exists."),
            ("Open Pocket", "h-open", ".tx-perm.is-active .ae-btn--primary", "Opens tab 2. If Chrome blocks it, an amber note says how to allow it."),
            ("Tab 2, not recording yet", "h-wait", None, "<b>Proposed.</b> Chrome jumps to the new tab. Today its panel already shows Task 1 though nothing records. Instead it says to go back. <span class=fl-hint>(Next to continue.)</span>"),
            ("Share the Pocket tab", "h-share", P, "Back in tab 1. The hint says exactly what to press in Chrome’s dialog."),
            ("Chrome’s picker", "h-picker", ".cr-dialog .is-main", "Chrome tab, then Pocket, then Share. The code checks the pick (Capture Handle)."),
            ("Task 1, in Pocket", "h-t1", P, "Chrome switches to the shared tab. Tasks show over the site; a backup list is in tab 1."),
            ("Tab 1 meanwhile", "h-ctrl", None, "The full list, a second Done (in case a page of the site drops the panel) and Finish early."),
            ("All tasks done", "h-t4", P, "Finish in the Pocket tab."),
            ("Back to tab 1", "h-fin", None, "<b>Proposed.</b> Today the panel just disappears. It should say where the recording is being sent from."),
            ("Overall rating", "h-rate", ".tx-rate button:nth-child(4)", "HTML tests rate the whole session once, in tab 1, when ratings are on."),
            ("Sent", "h-sent", None, "Same thank-you as Figma."),
        ]},
        "phone": {"name": "Figma on a phone", "steps": [
            ("Welcome", "p-welcome", P, "Same card. The screen fact is struck through: phones can’t share a tab, so only the voice is recorded."),
            ("Microphone", "p-mic", ".cr-sheet .is-main", "The phone’s own sheet."),
            ("Ready", "p-ready", P, ""),
            ("Task 1", "p-t1", P, "The bar docks below the prototype, so it never covers the prototype’s own tab bar."),
            ("Rating", "p-rate", ".tx-rate button:nth-child(3)", "The bar opens into a sheet for the rating."),
            ("Task 2", "p-t2", None, ""),
            ("Sent", "p-sent", None, ""),
        ]},
        "notasks": {"name": "No tasks", "steps": [
            ("Welcome", "n-welcome", P, "<b>Fixes B15.</b> No “0 tasks · About 1 minute”. “Look around Pocket for as long as you like.”"),
            ("Ready", "n-ready", P, ""),
            ("Explore freely", "n-explore", P, "One sentence and Finish. Over a black prototype here: the plate still reads."),
            ("Sent", "n-sent", None, ""),
        ]},
        "mic": {"name": "Mic denied", "steps": [
            ("Asked", "x-ask", ".cr-prompt .btns button:nth-child(3)", "Say they press <b>Never allow</b>."),
            ("Blocked", "x-blocked", ".tx-perm-help .tx-link", "<b>Fixes B16.</b> Says what’s lost and where the switch is. A blocked prompt can’t be shown again from the page."),
            ("Tab still asked", "x-tab", ".cr-dialog .is-main", "They can still share the tab."),
            ("Testing, tab only", "x-test", None, "An amber strip stays until dismissed. The designer’s session gets a “No audio” tag (proposed)."),
        ]},
        "stopped": {"name": "Sharing stopped", "steps": [
            ("Figma, testing", "s-t2", None, "They press Chrome’s <b>Stop sharing</b>."),
            ("Figma, after", "s-fig", None, "Today: video stops, voice goes on, nothing is said. Proposed: this strip, with Share again."),
            ("HTML, today", "s-html-today", None, "Today: Stop sharing ends an HTML test."),
            ("HTML, proposed", "s-html-prop", None, "Proposed: pause, keep the voice, offer to share again."),
        ]},
        "network": {"name": "Network and saving", "steps": [
            ("Offline", "w-off", None, "<b>Proposed.</b> Recording goes on in the tab; only the uploads wait."),
            ("Back online", "w-back", None, "Shown for a few seconds, then folds away."),
            ("Slow send", "w-slow", None, ""),
            ("Didn’t send", "w-bad", P, "Try again re-runs the upload from memory. Download a copy is a last resort."),
            ("Sent", "w-sent", None, ""),
        ]},
        "htmlphone": {"name": "HTML on a phone", "steps": [
            ("Not supported", "p-html", None, "Thanks first, the reason in one line, the link to copy. Nothing recorded."),
        ]},
        "preview": {"name": "Designer preview", "steps": [
            ("Welcome", "v-1", ".tx-preview .jump button:nth-child(3)", "<b>Proposed.</b> From Share, Open as a tester. The dark bar sits outside the tester UI. Jump to any step."),
            ("Tasks", "v-2", None, "Jumped to Tasks without allowing the mic."),
        ]},
    }
    js = {k: {"name": v["name"], "steps": [{"label": a, "screen": b, "hot": c, "note": n} for a, b, c, n in v["steps"]]} for k, v in flows.items()}
    used = {s[1] for v in flows.values() for s in v["steps"]}
    screens = "".join(
        f'<div data-screen="{i}" class="{"is-phone" if w == 390 else ""}" hidden>'
        f'<div class="tb-shot" data-w="{w}" data-h="{h}"><div class="tb-scale" style="width:{w}px;height:{h}px">{html}</div></div></div>'
        for i, (html, w, h) in S.items() if i in used)
    o = [HEAD.format(title="Aero tester flow, clickable", desc="Click through what a tester sees, in each context: Figma, HTML, phone and every failure.").replace("</head>", FLOW_CSS + "</head>")]
    o.append(f"""<div class="fl-top"><div class="tb-wrap"><span class="tb-logo">Aero<i>.</i></span><span class="tb-crumb">Tester flow · clickable</span>
<a href="tester.html" style="margin-left:auto;font-size:13px;color:var(--ae-ink-2)">All screens and notes →</a></div></div>
<main class="tb-wrap"><nav class="fl-pick" data-flow-picker aria-label="Scenario"></nav>
<div class="fl-head"><h1 data-flow-title></h1><span class="c" data-flow-count></span><div class="fl-nav">{btn("Back", "is-sm", icon="back", attrs="data-flow-prev")}{btn("Next", "is-sm is-primary", icon="arrow", attrs="data-flow-next")}</div></div>
<div class="fl-stage"><div class="fl-screen" data-flow-root>{screens}</div>
<aside class="fl-side"><div class="fl-note" data-flow-note></div><p class="fl-hint">Click the pulsing control, or use the arrow keys.</p><div class="fl-dots" data-flow-dots></div></aside></div>
<div style="height:64px"></div></main>
<script>window.TESTER_FLOWS={json.dumps(js)};</script>""")
    o.append(FOOT_JS)
    return "".join(o)


if __name__ == "__main__":
    f = build_flow()
    open(os.path.join(ROOT, "tester-flow.html"), "w").write(f)
    print("tester-flow.html", len(f))
