# Tester kit: every tester screen is composed from these functions, so the board
# (tester.html) and the clickable flow (tester-flow.html) share one source.
# Copy (words) lives in COPY-like constants near the top, not inside components.

# ---------------------------------------------------------------- example data
DESIGNER = "Mia Chen"
FIRST = "Mia"
STUDIO = "Kestrel Studio"
PROTO = "Pocket"
SITE = "pocket.aeroapp.ai"
LINK = "aeroapp.ai/pocket?test=1"
WELCOME_MSG = "Hi, thanks for doing this. I’m working on a new way to send money and I’d love to hear what you think. Go at your own pace."
THANKS_MSG = "Thank you, this really helps. I’ll listen to every word."
TASKS = [
    ("Send $20 to Sam", "Start from the home screen. Pay from your main balance."),
    ("Find what you spent on coffee last month", "Look anywhere in the app."),
    ("Freeze your card", "Imagine you’ve just lost it."),
    ("Split last night’s dinner with two friends", "The bill was $84."),
]

# ---------------------------------------------------------------- icons (1.6 stroke, 24 grid)
_P = {
    "mic": '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/>',
    "tab": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 9h18M7 5v4"/>',
    "screen": '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>',
    "check": '<path d="M5 12.5l4.2 4L19 7"/>',
    "x": '<path d="M6 6l12 12M18 6L6 18"/>',
    "alert": '<path d="M12 3.5l9.5 16.5h-19z"/><path d="M12 10v4.5M12 17.3v.2"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v5.5M12 7.7v.2"/>',
    "lock": '<rect x="5" y="10.5" width="14" height="10" rx="2"/><path d="M8 10.5V8a4 4 0 0 1 8 0v2.5"/>',
    "more": '<circle cx="5" cy="12" r="1.3"/><circle cx="12" cy="12" r="1.3"/><circle cx="19" cy="12" r="1.3"/>',
    "minus": '<path d="M5 12h14"/>',
    "move": '<path d="M12 3v18M3 12h18M12 3l-3 3M12 3l3 3M12 21l-3-3M12 21l3-3M3 12l3-3M3 12l3 3M21 12l-3-3M21 12l-3 3"/>',
    "restart": '<path d="M4 12a8 8 0 1 0 2.4-5.7M4 4v4.5h4.5"/>',
    "stop": '<rect x="6" y="6" width="12" height="12" rx="2"/>',
    "wifi": '<path d="M2 8.5a15 15 0 0 1 20 0M5.5 12a10 10 0 0 1 13 0M9 15.5a5 5 0 0 1 6 0M12 19v.2"/><path d="M3 3l18 18"/>',
    "copy": '<rect x="8" y="8" width="12" height="12" rx="2"/><path d="M16 8V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h2"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3.5 6.5l8.5 6.5 8.5-6.5"/>',
    "laptop": '<rect x="5" y="5" width="14" height="10" rx="1.5"/><path d="M2.5 18.5h19"/>',
    "phone": '<rect x="7" y="3" width="10" height="18" rx="2.5"/><path d="M11 18h2"/>',
    "eye": '<path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12z"/><circle cx="12" cy="12" r="3"/>',
    "cam": '<rect x="3" y="7" width="13" height="10" rx="2"/><path d="M16 11l5-3v8l-5-3"/>',
    "ext": '<path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "back": '<path d="M19 12H5M11 6l-6 6 6 6"/>',
    "share": '<rect x="3" y="5" width="18" height="12" rx="2"/><path d="M12 14V8M9 10.5L12 8l3 2.5"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7.5V12l3 2"/>',
    "user": '<circle cx="12" cy="8.5" r="3.5"/><path d="M5 20a7 7 0 0 1 14 0"/>',
    "cloud": '<path d="M7 18a4.5 4.5 0 0 1-.6-9A6 6 0 0 1 18 9.5 4 4 0 0 1 17.5 18z"/><path d="M12 11v5M9.5 13.5L12 11l2.5 2.5"/>',
    "pin": '<path d="M12 21s-6.5-5.6-6.5-11a6.5 6.5 0 0 1 13 0c0 5.4-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.3"/>',
}


def ic(name, cls=""):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_P[name]}</svg>')


# ---------------------------------------------------------------- small helpers
def btn(label, kind="", glass=None, attrs="", icon=None):
    """kind: '' | 'is-primary' plus size/width modifiers. glass: 'primary' | 'secondary' | None"""
    g = ""
    if glass == "primary":
        g = ' data-glass-v3="primary" data-fill="#1D1D1F"'
    elif glass == "secondary":
        g = ' data-glass-v3="secondary"'
    i = ic(icon) if icon else ""
    v = "ae-btn--primary" if "is-primary" in kind else "ae-btn--secondary"
    return f'<button class="ae-btn {v} tx-btn {kind}"{g} {attrs}>{i}{label}</button>'


def mark():
    return '<span class="tx-mark">A<i>.</i></span>'


def tag(kind, text=None):
    t = {"rec": "Recommended", "prop": "Proposed", "today": "Today", "fix": "Fix", "no": "Not recommended"}
    return f'<span class="tb-tag {kind}">{text or t[kind]}</span>'


def rec_chip(state="live", time="04:12", meter=True, label=None):
    labels = {"live": f"Rec {time}", "muted": "Muted", "voice": f"Voice only {time}", "screen": f"Screen only {time}",
              "off": "Offline, still recording", "saving": "Sending 72%", "saved": "Sent", "bad": "Not sent"}
    cls = {"live": "is-live", "voice": "is-live", "screen": "is-live", "muted": "is-muted", "off": "is-off",
           "saving": "is-saving", "saved": "is-saved", "bad": "is-bad"}[state]
    m = '<span class="tx-meter" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></span>' if meter and state in ("live", "voice") else ""
    return f'<span class="tx-rec {cls}" role="status"><span class="d"></span>{label or labels[state]}{m}</span>'


# ---------------------------------------------------------------- browser frames (third-party UI)
def chrome(body, tabs=None, url=LINK, share=None, prompt="", w=1280, h=800, url_extra=""):
    """tabs: list of (title, fav, active, recording)"""
    tabs = tabs or [("Testing Pocket", "ae", True, False)]
    t = "".join(
        f'<div class="cr-tab {"is-on" if a else ""}"><span class="fav is-{f}"></span>{tt}'
        f'{"<span class=rec></span>" if r else "<span class=x>×</span>"}</div>'
        for tt, f, a, r in tabs)
    lock = ic("lock", "lock")
    host, _, rest = url.partition("/")
    u = f'{lock}<span>{host}</span><span class="muted">{"/" + rest if rest else ""}</span>{url_extra}'
    sb = ""
    if share:
        sb = (f'<div class="cr-share">{ic("share", "ic")}<span>{share}</span>'
              f'<button>Stop sharing</button></div>')
    return (f'<div class="cr cr-win" style="width:{w}px;height:{h}px">'
            f'<div class="cr-tabs"><div class="cr-dots"><i></i><i></i><i></i></div>{t}</div>'
            f'<div class="cr-bar"><div class="cr-nav">‹ › ↻</div><div class="cr-url">{u}</div></div>'
            f'{sb}<div class="cr-body">{body}{prompt}</div></div>')


def phone(body, url=LINK, dark_status=False, w=390, h=844):
    col = "#fff" if dark_status else "#111"
    return (f'<div class="cr cr-phone"><div class="cr-phone-in">'
            f'<div class="cr-status" style="color:{col};position:absolute;left:0;right:0;top:0;z-index:30"><span>9:41</span><span class="isl"></span><span class="bat"></span></div>'
            f'<div class="cr-mbody" style="padding-top:0">{body}</div>'
            f'<div class="cr-mbar"><div class="u">{ic("lock")}{url.split("/")[0]}</div></div>'
            f'</div></div>')


def mic_prompt(host="aeroapp.ai", hl=True):
    return (f'<div class="cr-prompt"><h4>{host} wants to</h4>'
            f'<div class="row">{ic("mic")}Use your microphones</div>'
            f'<div class="btns"><button class="is-main {"hl" if hl else ""}">Allow while visiting the site</button>'
            f'<button>Allow this time</button><button>Never allow</button></div></div>'
            f'<span class="cr-tag" style="left:64px;top:262px">Chrome, not Aero</span>')


def tab_prompt(host="aeroapp.ai"):
    """getDisplayMedia with preferCurrentTab: Chrome asks to share THIS tab."""
    prev = proto_figma(theme="light", small=True)
    return (f'<div class="cr-scrim"></div><div class="cr-dialog" style="width:440px">'
            f'<h4>Allow {host} to see this tab?</h4><p>It will be able to see the contents of this tab.</p>'
            f'<div class="cr-prev" style="height:150px">{prev}</div>'
            f'<div class="btns"><button>Cancel</button><button class="is-main">Allow</button></div></div>'
            f'<span class="cr-tag" style="left:50%;top:calc(50% - 175px);transform:translateX(-50%)">Chrome, not Aero</span>')


def tab_picker(selected="Pocket"):
    """getDisplayMedia without preferCurrentTab (HTML tests): pick the Pocket tab."""
    rows = [("Pocket", "pk", SITE), ("Testing Pocket", "ae", "aeroapp.ai"), ("Inbox (3)", "", "mail.example.com")]
    li = "".join(f'<div class="{"is-on" if n == selected else ""}"><span class="fav is-{f or "x"}"></span><b style="font-weight:500">{n}</b>'
                 f'<span style="color:#80868B;margin-left:6px">{u}</span></div>' for n, f, u in rows)
    return (f'<div class="cr-scrim"></div><div class="cr-dialog">'
            f'<h4>Choose what to share with aeroapp.ai</h4><p>The site will be able to see the contents of your screen.</p>'
            f'<div class="cr-seg"><span class="is-on">Chrome tab</span><span>Window</span><span>Entire screen</span></div>'
            f'<div class="cr-list">{li}</div>'
            f'<div class="btns"><button>Cancel</button><button class="is-main">Share</button></div></div>'
            f'<span class="cr-tag" style="left:50%;top:calc(50% - 196px);transform:translateX(-50%)">Chrome, not Aero</span>')


def ios_sheet(title, text, a="Don’t Allow", b="Allow"):
    return (f'<div class="cr-scrim"></div><div class="cr-sheet"><h4>{title}</h4><p>{text}</p>'
            f'<div class="btns"><button>{a}</button><button class="is-main">{b}</button></div></div>')


# ---------------------------------------------------------------- the example prototype (Pocket)
def proto_web(theme="light"):
    return (f'<div class="pk {theme}"><div class="pk-web">'
            f'<div class="pk-nav"><div class="pk-logo"><i></i>Pocket</div><span>Personal</span><span>Business</span><span>Cards</span><span>Help</span>'
            f'<div class="r"><span>Log in</span><span class="pk-cta">Open an account</span></div></div>'
            f'<div class="pk-hero"><div><h1>Money that moves<br>when you do.</h1>'
            f'<p>Send, split and spend in one place. Freeze a card in a tap. Free to open, no monthly fee.</p>'
            f'<div class="row"><span class="pk-cta">Get Pocket</span><span class="pk-ghost">See how it works</span></div>'
            f'<div class="pk-stats"><div><b>2 sec</b><span>to send</span></div><div><b>0%</b><span>fees at home</span></div><div><b>4.8</b><span>app rating</span></div></div></div>'
            f'<div class="pk-cards"><div class="pk-cc c1"><span>Pocket</span><b>•••• 4021</b><span>SAM RIVERA</span></div>'
            f'<div class="pk-cc c2"><span>Pocket Plus</span><b>•••• 7730</b><span>SAM RIVERA</span></div></div></div>'
            f'<div class="pk-tiles"><div class="pk-tile"><b>Split anything</b>Dinner, rent, a taxi. Everyone pays their share.</div>'
            f'<div class="pk-tile"><b>See where it goes</b>Spending sorted by what it was for.</div>'
            f'<div class="pk-tile"><b>Freeze in a tap</b>Lost your card? Lock it from the app.</div></div>'
            f'</div></div>')


def proto_app(theme="light", toast=None):
    rows = [("CO", "Corner Coffee", "Today, 8:12", "−$4.20"), ("SA", "Sam Rivera", "Yesterday", "+$36.00"),
            ("MK", "Market Hall", "Mon", "−$52.18"), ("TR", "City Transit", "Mon", "−$2.90")]
    tx = "".join(f'<div class="pk-tx"><i>{a}</i><div>{n}<small>{d}</small></div><b>{v}</b></div>' for a, n, d, v in rows)
    t = f'<div class="pk-toast">{toast}</div>' if toast else ""
    return (f'<div class="pk {theme}"><div class="pk-app" style="padding-top:50px">'
            f'<div class="pk-top"><div class="pk-av">SR</div><div class="pk-logo" style="font-size:16px"><i></i>Pocket</div><div class="pk-av">⌕</div></div>'
            f'<div class="pk-bal">Main balance</div><div class="pk-big">$2,480<small>.12</small></div>'
            f'<div class="pk-acts"><div class="pk-act"><i>↗</i>Send</div><div class="pk-act"><i>↙</i>Request</div><div class="pk-act"><i>÷</i>Split</div><div class="pk-act"><i>❄</i>Freeze</div></div>'
            f'<div class="pk-sec">Recent<span>See all</span></div>{tx}'
            f'<div class="pk-tabbar"><span class="on">Home</span><span>Cards</span><span>Spending</span><span>Me</span></div>'
            f'</div>{t}</div>')


def proto_figma(theme="light", light_canvas=False, small=False):
    z = ' style="zoom:.42"' if small else ""
    return (f'<div class="fg {"is-light" if light_canvas else ""}"><div class="fg-frame"{z}>{proto_app(theme)}</div></div>')


# ================================================================ TESTER COMPONENTS (Aero UI)
def from_line(extra=""):
    return f'<div class="tx-from">{mark()}<span>Test by {STUDIO} · made with Aero</span>{extra}</div>'


def quote(text=WELCOME_MSG):
    return (f'<blockquote class="tx-quote" style="margin:0">“{text}”'
            f'<cite><span class="tx-avatar" style="width:20px;height:20px;font-size:9px">MC</span>{DESIGNER}</cite></blockquote>')


def facts(kind="figma", clicks=False):
    """What is recorded. kind: figma | html | phone | screen_off"""
    voice = f'<div><b>{ic("mic")}Your voice</b><span>So {FIRST} hears what you think.</span></div>'
    if kind == "phone":
        scr = f'<div class="is-off"><b>{ic("tab")}The screen</b><span>Phones can’t share a tab, so only your voice.</span></div>'
    elif kind == "html":
        scr = f'<div><b>{ic("tab")}The Pocket tab</b><span>Only that tab. Not other tabs or apps.</span></div>'
    else:
        scr = f'<div><b>{ic("tab")}This tab</b><span>Only this tab. Not other tabs or apps.</span></div>'
    clk = ""
    if clicks:
        what = "Where you move, click and scroll" if kind == "html" else "Where you click"
        why = f"Only inside {PROTO}, so {FIRST} can see where you went." if kind == "html" else f"Only on {PROTO}\u2019s screens. Not your mouse elsewhere."
        clk = f'<div style="grid-column:1/-1;background:var(--ae-test-tint)"><b>{ic("pin")}{what}</b><span>{why}</span></div>'
    return (f'<div class="tx-facts">{voice}{scr}{clk}'
            f'<div><b>{ic("user")}Who sees it</b><span>{DESIGNER} at {STUDIO}.</span></div>'
            f'<div class="is-off"><b>{ic("cam")}Your camera</b><span>Never used. No account needed.</span></div></div>')


def welcome_card(kind="figma", tasks=True, glass=True, clicks=False):
    n = len(TASKS)
    if kind == "html":
        steps = ["Allow your microphone.",
                 f"{PROTO} opens in a second tab. Share that tab.",
                 f"Try {n} short tasks and say what you think as you go." if tasks else f"Look around {PROTO} and say what you think as you go.",
                 "Press Finish. That’s it."]
    elif kind == "phone":
        steps = ["Allow your microphone.",
                 f"Try {n} short tasks and say what you think as you go." if tasks else f"Look around {PROTO} and say what you think as you go.",
                 "Press Finish. That’s it."]
    else:
        steps = ["Allow your microphone and this tab.",
                 f"Try {n} short tasks in {PROTO}. Say what you think as you go." if tasks else f"Look around {PROTO} for as long as you like. Say what you think as you go.",
                 "Press Finish. That’s it."]
    st = "".join(f"<li>{s}</li>" for s in steps)
    fk = "phone" if kind == "phone" else kind
    pad = ' style="padding:24px;gap:16px;max-width:none;border-radius:20px"' if kind == "phone" else ""
    return (f'<section class="tx tx-card"{pad} role="dialog" aria-labelledby="w-t">'
            f'{from_line()}'
            f'<h1 id="w-t">{DESIGNER} asked you to try {PROTO}<span class="dot">.</span></h1>'
            f'{quote()}'
            f'<div style="display:grid;gap:10px"><span class="tx-label">What happens</span><ol class="tx-steps">{st}</ol></div>'
            f'<div style="display:grid;gap:10px"><span class="tx-label">What’s recorded</span>{facts(fk, clicks)}</div>'
            f'<p class="tx-fine">There are no right or wrong answers. You’re testing {PROTO}, not yourself. Take as long as you need, and stop at any time.</p>'
            f'<div class="tx-actions">{btn("Start", "is-primary is-lg is-block", "primary" if glass else None)}</div>'
            f'</section>')


def perm_row(kind, state="idle", extra=""):
    """kind: mic | tab | ptab (Pocket tab, HTML). state: idle | active | waiting | ok | bad | na"""
    data = {
        "mic": ("mic", "Microphone", f"So {FIRST} hears what you think.", "Allow"),
        "tab": ("tab", "This tab", "Only this tab. Nothing else on your screen.", "Share tab"),
        "ptab": ("tab", f"The {PROTO} tab", "Only that tab. Nothing else on your screen.", f"Share the {PROTO} tab"),
    }[kind]
    icn, title, sub, cta = data
    right = ""
    if state in ("idle", "active"):
        right = btn(cta, "is-primary is-sm" if state == "active" else "is-sm", "primary" if state == "active" else None)
    elif state == "waiting":
        right = '<span class="tx-state is-off">Next</span>'
    elif state == "ok":
        right = f'<span class="tx-state">{ic("check")}{"Allowed" if kind == "mic" else "Sharing"}</span>'
        sub = {"mic": "We can hear you.", "tab": "Only this tab is shared.", "ptab": f"Only the {PROTO} tab is shared."}[kind]
    elif state == "bad":
        right = f'<span class="tx-state is-bad">{ic("x")}{"Blocked" if kind == "mic" else "Not shared"}</span>'
    elif state == "na":
        right = '<span class="tx-state is-off">Skipped</span>'
    cls = {"idle": "", "active": "is-active", "waiting": "is-waiting", "ok": "is-ok", "bad": "is-bad", "na": "is-na"}[state]
    return (f'<div class="tx-perm {cls}"><span class="ic">{ic(icn)}</span><div><b>{title}</b><small>{sub}</small></div>{right}{extra}</div>')


def think_aloud(short=False):
    if short:
        return f'<div class="tx-note">{ic("info")}<span><b>Talk as you go.</b> What you’re looking for, what you expect, anything that surprises you.</span></div>'
    return (f'<div class="tx-note">{ic("info")}<span><b>Talk as you go.</b> Say what you’re looking for, what you expect to happen, '
            f'and anything that surprises you. Half-finished thoughts are fine.</span></div>')


def allow_card(mic="active", tab="waiting", kind="figma", note="", ready=False, title=None, helper=None):
    rows = perm_row("mic", mic)
    if kind == "figma":
        rows += perm_row("tab", tab)
    sub = helper or ("Your browser will ask twice. Choose Allow each time." if kind == "figma" else "Your browser will ask. Choose Allow.")
    cta_ok = ready
    start = btn("Start the test", "is-primary is-lg is-block" + ("" if cta_ok else " is-disabled"), "primary" if cta_ok else None,
                "" if cta_ok else 'aria-disabled="true"')
    t = title or ("You’re ready" if ready else "Allow recording")
    return (f'<section class="tx tx-card" role="dialog" aria-labelledby="a-t">'
            f'{from_line()}'
            f'<div style="display:grid;gap:6px"><h1 id="a-t">{t}</h1><p class="tx-sub">{sub}</p></div>'
            f'<div class="tx-perms">{rows}</div>{note}'
            f'{think_aloud() if ready else ""}'
            f'<div class="tx-actions">{start}</div></section>')


# ---------------------------------------------------------------- task panel
def panel_head(rec="live", time="04:12", glassy=False, menu=False):
    chip = '<span class="tx-label" style="margin-right:auto">Pocket test</span>' if rec == "none" else rec_chip(rec, time)
    return (f'<div class="tx-panel-h">{chip}'
            f'<button class="tx-icon" aria-label="More">{ic("more")}</button>'
            f'<button class="tx-icon" aria-label="Minimise">{ic("minus")}</button></div>')


def prog(i, n=len(TASKS), done_now=False):
    out = []
    for k in range(n):
        if k < i or (k == i and done_now):
            out.append('<i class="is-done"></i>')
        elif k == i:
            out.append('<i class="is-now"></i>')
        else:
            out.append("<i></i>")
    return f'<div class="tx-prog" aria-hidden="true">{"".join(out)}</div>'


def panel(i=1, state="task", rec="live", time="04:12", style="plate", strip="", interacted=True, menu=False, body=None, glass=True):
    """state: task | rate | stuck-rate | last | confirm-end | explore | ended
    style: plate (A) | glass (B) | today"""
    n = len(TASKS)
    cls = {"plate": "", "glass": " is-glass", "today": " is-today"}[style]
    g = ' data-glass-v3="dark"' if style == "glass" and glass else ""
    title, ins = TASKS[min(i, n - 1)]
    pg = glass and style == "plate"
    if body is not None:
        b = body
    elif state == "task":
        done = btn("Done", "is-primary" + ("" if interacted else " is-disabled"), "primary" if (pg and interacted) else None)
        hint = "" if interacted else f'<p class="tx-hint">Try it in {PROTO} first, then press Done.</p>'
        b = (f'<span class="tx-label">Task {i + 1} of {n}</span>{prog(i)}<h2>{title}</h2><p class="tx-ins">{ins}</p>'
             f'<div class="tx-two">{done}{btn("Couldn’t do it")}</div>{hint}')
    elif state in ("rate", "stuck-rate"):
        lab = "Done" if state == "rate" else "Couldn’t do it"
        q = "How easy was that?" if state == "rate" else "That’s useful too. How hard was it?"
        opts = [("1", "Very hard"), ("2", "Hard"), ("3", "OK"), ("4", "Easy"), ("5", "Very easy")]
        rb = "".join(f'<button role="radio" aria-checked="false"><b>{a}</b>{t}</button>' for a, t in opts)
        b = (f'<span class="tx-label">Task {i + 1} of {n} · {lab}</span>{prog(i, done_now=True)}<h2>{q}</h2>'
             f'<div class="tx-rate" role="radiogroup" aria-label="{q}">{rb}</div>'
             f'<div class="tx-row" style="display:flex;justify-content:space-between;align-items:center"><button class="tx-link is-quiet">Skip</button>'
             f'<span class="tx-hint" style="font-size:12px;color:var(--ae-ink-3)">Keys 1 to 5</span></div>')
    elif state == "last":
        b = (f'<span class="tx-label">All {n} tasks done</span>{prog(n)}<h2>Anything else to say?</h2>'
             f'<p class="tx-ins">Say it now, while it’s still recording. Then press Finish.</p>'
             f'{btn("Finish", "is-primary is-block", "primary" if pg else None)}')
    elif state == "confirm-end":
        b = (f'<span class="tx-label">Task {i + 1} of {n}</span><h2>End the test now?</h2>'
             f'<p class="tx-ins">What you’ve done so far is sent to {FIRST}.</p>'
             f'<div class="tx-two">{btn("End test", "is-primary", "primary" if pg else None)}{btn("Keep going")}</div>')
    elif state == "explore":
        b = (f'<span class="tx-label">Explore freely</span><h2>Look around {PROTO} and say what you think.</h2>'
             f'<p class="tx-ins">There are no tasks. Stop whenever you’ve seen enough.</p>'
             f'{btn("Finish", "is-primary is-block", "primary" if pg else None)}')
    m = ""
    if menu:
        m = (f'<div class="tx-menu" role="menu"><button role="menuitem">{ic("restart")}Restart {PROTO}</button>'
             f'<button role="menuitem" class="is-hover">{ic("move")}Move panel<span class="tx-corners"><i></i><i></i><i></i><i class="is-on"></i></span></button>'
             f'<button role="menuitem">{ic("mic")}Mute microphone</button><hr>'
             f'<button role="menuitem" class="is-end">{ic("stop")}End test</button></div>')
    return (f'<aside class="tx tx-panel{cls}"{g} aria-label="Test tasks" style="position:relative">'
            f'{panel_head(rec, time)}{strip}<div class="tx-panel-b">{b}</div>{m}</aside>')


def strip(kind, text, actions=""):
    icn = {"warn": "alert", "bad": "alert", "info": "info"}[kind]
    a = f'<div class="tx-row">{actions}</div>' if actions else ""
    return f'<div class="tx-panel-strip is-{kind}" role="status">{ic(icn)}<div>{text}{a}</div></div>'


def mini(i=1, time="04:12", glass=True, rec="live"):
    g = ' data-glass-v3="secondary" data-strength="1.6"' if glass else ""
    return (f'<div class="tx tx-mini"{g} role="status">{rec_chip(rec, time, meter=False)}<span class="sep"></span>'
            f'<span class="tx-mini-t">Task {i + 1} of {len(TASKS)}</span>{btn("Show", "is-sm is-pill")}</div>')


def dock(i=1, time="04:12", explore=False):
    if explore:
        t = f'<b>Look around {PROTO}</b><small>{rec_chip("voice", time, meter=False, label="Rec " + time)}</small>'
        a = btn("Finish", "is-primary", "primary")
    else:
        t = f'<b>{TASKS[i][0]}</b><small>Task {i + 1} of {len(TASKS)} · {rec_chip("voice", time, meter=False, label="Rec " + time)}</small>'
        a = btn("Done", "is-primary", "primary")
    return (f'<div class="tx tx-dock" role="region" aria-label="Test tasks"><div class="t">{t}</div>'
            f'<button class="tx-icon" aria-label="More">{ic("more")}</button>{a}</div>')


def rail(i=1, time="04:12"):
    items = ""
    for k, (t, ins) in enumerate(TASKS):
        if k < i:
            items += f'<li class="is-done" data-n="{k + 1}"><span>{t}</span></li>'
        elif k == i:
            items += (f'<li class="is-now" data-n="{k + 1}"><span>{t}</span><span class="tx-ins">{ins}</span>'
                      f'<span class="tx-row">{btn("Done", "is-primary is-sm", "primary")}{btn("Couldn’t do it", "is-sm")}</span></li>')
        else:
            items += f'<li data-n="{k + 1}"><span>{t}</span></li>'
    return (f'<aside class="tx tx-rail" aria-label="Test tasks"><div class="tx-rail-h">{mark()}<b style="font-weight:520;font-size:14px">{PROTO}</b>{rec_chip("live", time)}</div>'
            f'<ul class="tx-tasks">{items}</ul>'
            f'<div style="margin-top:auto;padding:16px;border-top:1px solid var(--ae-line);display:flex;justify-content:space-between">'
            f'<button class="tx-link is-quiet">Restart {PROTO}</button><button class="tx-link is-quiet">End test</button></div></aside>')


# ---------------------------------------------------------------- thank you
def thanks_card(save="saving", pct=72, kind="figma", note=""):
    if save == "saving":
        s = (f'<div class="tx-save" role="status"><div class="top"><b>Sending your recording to {FIRST}</b><span>{pct}%</span></div>'
             f'<div class="tx-bar"><i style="width:{pct}%"></i></div><small>Keep this tab open until it’s sent.</small></div>')
    elif save == "slow":
        s = (f'<div class="tx-save is-warn" role="status"><div class="top"><b>Still sending. Your connection is slow.</b><span>{pct}%</span></div>'
             f'<div class="tx-bar"><i style="width:{pct}%"></i></div><small>Keep this tab open. About 2 minutes left.</small></div>')
    elif save == "offline":
        s = (f'<div class="tx-save is-warn" role="status"><div class="top"><b>Waiting for a connection</b><span>{pct}%</span></div>'
             f'<div class="tx-bar"><i style="width:{pct}%"></i></div><small>Your recording is safe in this tab. It sends as soon as you’re back online. Keep this tab open.</small></div>')
    elif save == "bad":
        s = (f'<div class="tx-save is-bad" role="alert"><div class="top"><b>The recording didn’t send</b><span>{pct}%</span></div>'
             f'<div class="tx-bar"><i style="width:{pct}%"></i></div><small>It’s still in this tab, so don’t close it yet.</small>'
             f'<div style="display:flex;gap:10px;margin-top:6px">{btn("Try again", "is-primary is-sm", "primary")}{btn("Download a copy", "is-sm")}</div></div>')
    elif save == "voice":
        s = (f'<div class="tx-save is-ok" role="status"><div class="top"><b>Sent to {FIRST}</b><span>100%</span></div>'
             f'<div class="tx-bar"><i style="width:100%"></i></div><small>You can close this tab.</small></div>')
    else:
        s = (f'<div class="tx-save is-ok" role="status"><div class="top"><b>Sent to {FIRST}</b><span>100%</span></div>'
             f'<div class="tx-bar"><i style="width:100%"></i></div><small>You can close this tab now.</small></div>')
    pad = ' style="padding:24px;gap:16px;border-radius:20px"' if kind == "phone" else ""
    return (f'<section class="tx tx-card"{pad} aria-labelledby="t-t">{from_line()}'
            f'<h1 id="t-t">Thanks, you’re done<span class="dot">.</span></h1>{quote(THANKS_MSG)}{s}{note}'
            f'<div style="display:grid;gap:6px"><span class="tx-label">What happens next</span>'
            f'<p class="tx-fine" style="color:var(--ae-ink-2)">{FIRST} gets your recording in a minute or two. What you said is transcribed and summarised for {FIRST}, '
            f'who may watch parts of it. To have it deleted, ask {FIRST}.</p></div>'
            f'<p class="tx-fine" style="border-top:1px solid var(--ae-line);padding-top:14px">Test made with <b style="font-weight:520;color:var(--ae-ink)">Aero<span style="color:var(--ae-blue)">.</span></b> Publish and test your own prototypes at aeroapp.ai</p>'
            f'</section>')


def msg_card(title, text, actions="", icon="info", kind="figma", extra=""):
    pad = ' style="padding:24px;gap:16px;border-radius:20px"' if kind == "phone" else ""
    return (f'<section class="tx tx-card"{pad}>{from_line()}'
            f'<div style="display:grid;gap:8px"><h1>{title}</h1><p class="tx-sub">{text}</p></div>{extra}'
            f'{f"<div class=tx-actions>{actions}</div>" if actions else ""}</section>')
