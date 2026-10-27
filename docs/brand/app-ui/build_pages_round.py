"""
Aero pages round (site page, test page, Visits, upsell pattern). version: 2026-10-26.1
Builds pages-round.html from the v3 kit (kit.py, build_common.py, components.css, board.css).
Run: python3 build_pages_round.py     (all names, numbers and sites are Example data)
"""
from build_common import *
from build_pages_content import *   # copy, tables and decisions (words live there, not here)

S = SCENE
R = lambda n="right": i(n, "ae-i--sm")

# ------------------------------------------------------------------ small parts
def crumbs(*parts):
    out = []
    for k, p in enumerate(parts):
        out.append(f"<b>{p}</b>" if k == len(parts) - 1 else f"<span>{p}</span>{R()}")
    return '<div class="ae-crumbs">' + "".join(out) + '</div>'

def bar(cr, actions=""):
    return f'<div class="pr-bar">{cr}{actions}</div>'

def toggle(on=True, disabled=False):
    return f'<span class="ae-toggle{" is-on" if on else ""}{" is-disabled" if disabled else ""}"></span>'

def opt(title, sub="", control="", plan=None, locked=False, stack=False, extra=""):
    t = title + (f' <span class="pr-tagrow">{tag(plan, "line", "lock") if locked else tag(plan, "line")}</span>' if plan else "")
    cls = "ae-option" + (" is-locked" if locked else "") + (" is-stack" if stack else "")
    sb = f'<div class="ae-option__sub">{sub}</div>' if sub else ""
    if stack:
        return f'<div class="{cls}"><div class="ae-option__text"><div class="ae-option__title">{t}</div>{sb}</div>{control}{extra}</div>'
    return f'<div class="{cls}"><div class="ae-option__text"><div class="ae-option__title">{t}</div>{sb}</div>{control}</div>'

def field(v, end="", w=""):
    e = f'<span class="ae-affix__end">{end}</span>' if end else ""
    inner = f'<div class="ae-input">{v}</div>'
    return f'<div class="ae-affix">{inner}{e}</div>' if end else inner

def rail(title, rows, right=""):
    return f'<div class="pr-rail"><div class="pr-rail__head"><span class="ae-h3">{title}</span>{right}</div><div class="pr-set">{"".join(rows)}</div></div>'

def sect(title, inner, right="", plan=None, locked=False):
    t = title + (f' <span class="pr-tagrow">{tag(plan, "line", "lock")}</span>' if plan else "")
    return f'<div class="ae-section"><div class="ae-section__head"><span class="ae-h3" style="display:inline-flex;align-items:center;gap:8px">{t}</span><span class="ae-spacer"></span>{right}</div>{inner}</div>'

def prev(host, kind="site", cap="Screenshot · v4 · 2 hours ago", sm=False, action=True):
    cls = "pr-prev" + (" pr-prev--test" if kind == "test" else "") + (" pr-prev--sm" if sm else "")
    act = btn("Refresh preview", "ghost", size="sm", icon="refresh") if action else ""
    return (f'<div class="{cls}"><div class="pr-prev__win"><div class="pr-prev__bar"><span class="ae-window__dots"><i></i><i></i><i></i></span>{host}</div>'
            f'<div class="pr-prev__body"><div><span>Balance</span><b>£2,480.12</b><div class="pr-prev__cards"><i></i><i></i><i></i></div></div></div></div>'
            f'<div class="pr-prev__cap">{i("check","ae-i--sm")}{cap}<span class="ae-spacer"></span>{act}</div></div>')

def thumb52():
    return '<span class="pr-thumb" style="background:#FF6B4A"><span style="position:absolute;left:8px;top:10px;width:22px;height:5px;border-radius:3px;background:#fff;opacity:.9"></span><span style="position:absolute;left:8px;top:20px;width:34px;height:8px;border-radius:3px;background:#fff"></span><span style="position:absolute;left:8px;bottom:8px;width:10px;height:10px;border-radius:3px;background:#FFC93C"></span><span style="position:absolute;left:21px;bottom:8px;width:10px;height:10px;border-radius:3px;background:#1D1D1F"></span></span>'

def upcard(title, sub, btn_label="See plans", icon="clock", blue=False):
    return (f'<div class="pr-up{" pr-up--blue" if blue else ""}">{i(icon)}<div><div class="pr-up__t">{title}</div><div class="pr-up__s">{sub}</div>'
            f'<div class="pr-up__act">{btn(btn_label, "secondary", size="sm")}</div></div></div>')

def listcard(rows):
    return f'<div class="ae-list--card"><div class="ae-list">{"".join(rows)}</div></div>'

PLAN = {"free": ("Free", 2, 3), "basic": ("Basic", 3, 5), "pro": ("Pro", 9, 20)}

def shell(main, plan="free", active="sites", mtitle="Pocket", mback=True, mright=""):
    name, n, of = PLAN[plan]
    S["sessions_kept"], S["sessions_limit"] = n, of
    mright = mright or btn("", "ghost", size="sm", icon="more", extra="ae-btn--icon")
    h = app(main, "sidebar", active, mtitle, mback, mright=mright)
    h = h.replace("Free plan. Sites stay live 7 days.", "Free plan. Sites stay live 7 days." if plan == "free" else f"{name} plan.")
    h = h.replace("See plans from $3", "See plans" if plan != "pro" else "Manage plan")
    h = h.replace("Free plan", f"{name} plan") if plan != "free" else h
    S["sessions_kept"], S["sessions_limit"] = 2, 3
    return h

# ------------------------------------------------------------------ Visits (only data /api/plausible returns)
def vis_list(title, rows, tabs_=None):
    mx = max(v for _, v in rows)
    t = (f'<span class="ae-seg">' + "".join(f'<span class="ae-seg__opt{" is-active" if k == 0 else ""}">{x}</span>' for k, x in enumerate(tabs_)) + '</span>') if tabs_ else f'<span class="ae-small" style="color:var(--ae-ink)">{title}</span>'
    body_ = "".join(f'<div class="pr-list__row"><i style="width:{round(v / mx * 100)}%"></i><span>{n}</span><span>{v:,}</span></div>' for n, v in rows)
    lab = f'<span class="ae-label">{title}</span>' if tabs_ else '<span class="ae-label">Visitors</span>'
    return f'<div class="pr-list"><div class="pr-list__h">{t}</div>{body_}</div>'

def visits_block(state="data", period="7 days", plan="pro"):
    seg = ('<span class="ae-seg">' + "".join(f'<span class="ae-seg__opt{" is-active" if x == period else ""}">{x}</span>' for x in ["Today", "7 days", "30 days"])
           + f'<span class="ae-seg__opt" title="This month, 12 months">{i("down", "ae-i--sm")}</span></span>')
    head_ = f'<div class="pr-vis__head"><span class="ae-h3">Visits {example() if state == "data" else ""}</span>{seg if state != "locked" else ""}</div>'
    if state == "locked":
        return (f'<div class="pr-vis"><div class="pr-vis__head"><span class="ae-h3" style="display:inline-flex;gap:8px;align-items:center">Visits {tag("Solo", "line", "lock")}</span></div>'
                f'<div class="pr-lock"><div class="pr-bars pr-skelbars">{"".join(f"<i style=height:{h}%></i>" for h in (30, 52, 40, 70, 48, 85, 60))}</div>'
                f'<div><div class="ae-strong">See who opens your site</div><div class="ae-small" style="margin-top:3px">Visitors, where they came from, their country and device, for today, 7 days, 30 days and 12 months.</div></div>'
                f'<div>{btn("See plans", "secondary", size="sm")}</div></div></div>')
    if state == "empty":
        return (f'<div class="pr-vis">{head_.replace(example(), "")}<div class="pr-chart"><div class="pr-bars pr-skelbars">{"".join("<i style=height:6%></i>" for _ in range(7))}</div>'
                f'<div class="pr-axis"><span>20 Oct</span><span>26 Oct</span></div></div>'
                f'<div class="ae-callout ae-callout--info">{i("info")}<span><b>No visits yet.</b> They show here once someone opens the site. Your own visits count too.</span></div></div>')
    if state == "loading":
        sk = "".join('<div class="pr-stat"><span class="ae-skel ae-skel--text" style="width:50%"></span><span class="ae-skel ae-skel--title" style="width:70%"></span></div>' for _ in range(4))
        return (f'<div class="pr-vis">{head_.replace(example(), "")}<div class="pr-stats">{sk}</div><div class="pr-chart"><div class="pr-bars pr-skelbars" style="animation:none">{"".join("<i style=height:%d%%></i>" % h for h in (30, 52, 40, 70, 48, 85, 60))}</div></div></div>')
    stats = [("Visitors", "1,284", "+18%", True), ("Visits", "1,630", "+12%", False), ("Pageviews", "3,905", "+9%", False), ("Time on site", "2m 14s", "-4%", False)]
    st = "".join(f'<div class="pr-stat{" is-on" if on else ""}"><span class="pr-stat__l">{l}</span><span class="pr-stat__n">{n}</span><span class="pr-stat__c">{c} on the previous {period}</span></div>' for l, n, c, on in stats)
    hs = [38, 52, 44, 100, 68, 41, 57]
    bars = "".join(f'<i class="{"is-hi" if k == 3 else ""}" style="height:{h}%"></i>' for k, h in enumerate(hs))
    chart = (f'<div class="pr-chart"><div class="pr-bars">{bars}<span class="pr-tip" style="left:50%">Thu 23 Oct · 312 visitors</span></div>'
             f'<div class="pr-axis"><span>Mon 20</span><span>Tue</span><span>Wed</span><span>Thu</span><span>Fri</span><span>Sat</span><span>Sun 26</span></div></div>')
    lists = ('<div class="pr-lists">'
             + vis_list("Where from", [("Direct / None", 612), ("WhatsApp", 241), ("Google", 188), ("Slack", 96), ("LinkedIn", 63)])
             + vis_list("Where", [("United Kingdom", 502), ("United States", 311), ("Hong Kong", 148), ("Germany", 97), ("Japan", 64)], ["Countries", "Cities"])
             + vis_list("Devices", [("Desktop", 803), ("Mobile", 448), ("Tablet", 33)], ["Devices", "Browsers", "OS"]) + '</div>')
    more = '<div class="pr-more"><span>Views per visit <b>2.4</b></span><span>Bounce rate <b>41%</b></span><span class="ae-small">Visits to the live site, not test sessions.</span></div>'
    return f'<div class="pr-vis">{head_}<div class="pr-stats">{st}</div>{chart}{more}{lists}</div>'

# ------------------------------------------------------------------ site page
def site_rows(plan):
    free, basic = plan == "free", plan == "basic"
    rows = [opt("Name", "Shown in your list and in the tab of password pages.", "", stack=True, extra=f'<div style="display:flex;gap:8px;align-items:center">{field("Pocket")}<span class="pr-saved">{i("check", "ae-i--sm")} Saved</span></div>')]
    if free:
        rows.append(opt("Address", "A generated address. Choose your own, like pocket.aeroapp.ai.", "", plan="Basic", locked=True, stack=True, extra=field("open-chestnut", ".aeroapp.ai")))
    else:
        rows.append(opt("Address", "Lowercase letters, numbers and hyphens. Changing it breaks the old link straight away.", "", stack=True, extra=field("pocket", ".aeroapp.ai")))
    if free:
        rows.append(opt("Password", "Only people with the password can open the site.", toggle(False, True), plan="Basic", locked=True))
        rows.append(opt("Favicon", "Your own icon in the browser tab.", btn("Upload", "secondary", size="sm"), plan="Basic", locked=True))
        rows.append(opt("Aero badge", "A small “Made with Aero” link shows in the corner on Free.", toggle(True, True), plan="Basic", locked=True))
        rows.append(opt("Custom domain", "Use a domain you already own.", btn("Connect", "secondary", size="sm"), plan="Solo", locked=True))
    elif basic:
        rows.append(opt("Password", "Visitors enter it once and stay signed in for a week.", toggle(False)))
        rows.append(opt("Favicon", "Your own icon in the browser tab.", btn("Upload", "secondary", size="sm")))
        rows.append(opt("Aero badge", "The “Made with Aero” link is hidden on your plan.", toggle(False)))
        rows.append(opt("Custom domain", "Use a domain you already own.", btn("Connect", "secondary", size="sm"), plan="Solo", locked=True))
    else:
        rows.append(opt("Password", "Visitors enter it once and stay signed in for a week.", toggle(False)))
        rows.append(opt("Favicon", "Using your upload.", f'<span style="display:inline-flex;gap:8px;align-items:center"><span class="ae-mark" style="width:24px;height:24px"><span>P</span></span>{btn("Replace", "secondary", size="sm")}</span>'))
        rows.append(opt("Aero badge", "The “Made with Aero” link is hidden on your plan.", toggle(False)))
        rows.append(opt("Custom domain", "Point a CNAME at the address above, then connect.", btn("Connect", "secondary", size="sm")))
    return rows

def tests_of_site(has=True, limit=False):
    row = ('<div style="display:flex;align-items:center;gap:12px;padding:12px 16px"><span style="flex:1;min-width:0"><div class="ae-strong">Pocket test</div>'
           f'<div class="ae-small"><span class="ae-mono">aeroapp.ai/t/pocket-7k2</span> · pinned to v3</div></span>{tag("Review ready", "review")}<span class="ae-tc">3 sessions · 2 new</span>{i("right", "ae-i--sm")}</div>')
    return listcard([row])

def update_block(plan="pro"):
    ways = ('<div class="pr-ways">'
            f'<div class="pr-way pr-way--drop"><div class="pr-way__t">{i("upload")}Drop files</div><div class="pr-way__s">A folder, zip or a few files. It becomes the next version at the same address.</div>{btn("Choose files", "secondary", size="sm")}</div>'
            f'<div class="pr-way"><div class="pr-way__t">{i("prompt")}Ask Claude or ChatGPT</div><div class="pr-way__s">Paste a prompt into your chat. It builds the next version and publishes it here.</div>{btn("Get prompt", "secondary", size="sm")}</div>'
            f'<div class="pr-way"><div class="pr-way__t">{i("figma")}Use a Figma link</div><div class="pr-way__s">Serve a Figma prototype instead. Your files are kept, switch back any time.</div>{btn("Switch source", "secondary", size="sm")}</div></div>')
    foot = (f'<div class="pr-set" style="margin-top:6px">{opt("Publish uploads straight away", "Turn off to save an upload as a draft and publish it from Versions.", toggle(True))}</div>')
    return ways + foot

def versions():
    def v(n, t, sub, live=False):
        return (f'<div class="ae-version{" is-live" if live else ""}"><span class="ae-version__n">v{n}</span><span><div class="ae-strong" style="font-size:13px">{t}</div><div class="ae-small">{sub}</div></span>'
                f'<span>{status("Live", "live") if live else ""}</span>{btn("", "ghost", size="sm", icon="more", extra="ae-btn--icon")}</div>')
    return listcard([v(4, "From Claude", "2 hours ago · 6 files · 412 KB", True), v(3, "Web upload", "Yesterday · 6 files · 409 KB"), v(2, "From Claude", "21 Oct · 5 files · 388 KB")])

def site_page(plan="free", phone=False, vis=None):
    free = plan == "free"
    host = "open-chestnut.aeroapp.ai" if free else "pocket.aeroapp.ai"
    acts = (btn("Copy address", "secondary", size="sm", icon="copy") + btn("Visit", "secondary", size="sm", icon="out") + btn("", "ghost", size="sm", icon="more", extra="ae-btn--icon"))
    meta = f'<span class="ae-mono">{host}</span>{status("Live", "live")}<span>v4 · updated 2 hours ago</span>' + (f'<span style="color:var(--ae-warn)">Offline in 5 days on Free</span>' if free else "")
    top = f'<div class="pr-top"><div class="pr-top__text"><h1 class="pr-title">Pocket</h1><div class="pr-meta">{meta}</div></div></div>'
    vstate = vis or ("data" if plan == "pro" else "locked")
    main = (f'<div class="pr-main">{prev(host)}'
            + sect("Tests", tests_of_site(), btn("Test this site", "secondary", size="sm", icon="tests"))
            + sect("Update", update_block(plan))
            + sect("Versions", versions())
            + visits_block(vstate)
            + '</div>')
    side = ""
    if free:
        side += upcard("This site goes offline on Mon 2 Nov.", "Free sites stay live 7 days. Your files are kept.", "See plans")
    side += rail("Settings", site_rows(plan))
    body_ = f'<div class="pr-cols"><div style="display:contents">{main}</div><div class="pr-rail" style="gap:var(--ae-s-5)">{side}</div></div>'
    # the rail wrapper above holds the card and the rail; rail() already has its own wrapper, so flatten
    body_ = f'<div class="pr-cols">{main}<div class="pr-rail">{(upcard("This site goes offline on Mon 2 Nov.", "Free sites stay live 7 days. Your files are kept.", "See plans") if free else "")}{rail("Settings", site_rows(plan))}</div></div>'
    return shell(bar(crumbs("Sites", "Pocket"), acts) + top + body_, plan, "sites")

# ------------------------------------------------------------------ test page
def tabsrow(active, n=3, new=2):
    items = [("Sessions", f' <span class="ae-tab__n">{n}</span>' + (f' <span class="ae-test-row__new">{new} new</span>' if new else "")), ("Insights", ""), ("Setup", "")]
    return '<div class="ae-tabs">' + "".join(f'<span class="ae-tab{" is-active" if a == active else ""}">{a}{x}</span>' for a, x in items) + '</div>'

def srow(s):
    st = {"ready": status("Ready", "ready"), "processing": status("Transcript arriving", "processing")}[s["status"]]
    q = (f'<span class="ae-session-row__quote">“{E(s["quote"])}”</span>' if s["quote"] else '<span class="ae-session-row__quote is-muted">Transcript arriving, usually about a minute</span>')
    return (f'<div class="ae-session-row"><span class="ae-session-row__n">Session {s["n"]}</span><span class="ae-session-row__who">{avatar(s["who"][-1], s["av"])}<span style="min-width:0"><div class="ae-session-row__name">{s["who"]}</div><div class="ae-session-row__dev">{s["dev"]}</div></span></span>{q}<span class="ae-tc">{s["len"]}</span>{st}</div>')

def sessions_table():
    rows = list(reversed(S["sessions"]))
    return (f'<div class="ae-list--card"><div class="ae-listhead" style="grid-template-columns:76px minmax(150px,1.3fr) minmax(0,2.4fr) 52px 168px"><span>#</span><span>Tester</span><span>In their words</span><span>Length</span><span>Status</span></div>'
            f'<div class="ae-list">{"".join(srow(s) for s in rows)}</div></div>')

def test_top(thumb=True, limit=False, plan="free"):
    name, n, of = PLAN[plan]
    acts = (btn("Preview as tester", "secondary", size="sm", icon="out") + btn("Copy test link", "primary", True, size="sm", icon="copy") + btn("", "ghost", size="sm", icon="more", extra="ae-btn--icon"))
    kept = (f'<span style="color:var(--ae-warn)">3 of 3 sessions kept</span>' if limit else "")
    meta = f'<span class="ae-mono">aeroapp.ai/t/pocket-7k2</span>{status("Taking sessions", "live")}<span>2 tasks</span><span>3 sessions</span><span>Updated 22:30</span><span>From: <span class="ae-link">Pocket</span></span>{kept}'
    th = thumb52() if thumb else ""
    return bar(crumbs("Tests", "Pocket"), acts) + f'<div class="pr-top">{th}<div class="pr-top__text"><h1 class="pr-title">Pocket</h1><div class="pr-meta">{meta}</div></div></div>'

def test_sessions(plan="free", limit=False, thumb=True):
    card = ""
    if limit:
        card = upcard("You have 3 of 3 sessions kept.", "New sessions can't start until you delete one or move to a bigger plan. The ones you have stay.", "See plans", "alert")
    body_ = f'<div class="ae-body">{card}{sessions_table()}</div>'
    return shell(test_top(thumb, limit, plan) + tabsrow("Sessions") + body_, plan, "tests", "Pocket")

def test_rail(plan="free", demo_thumb=False):
    link = (f'<div class="pr-set"><div class="ae-option is-stack"><div class="ae-option__text"><div class="ae-option__title">Test link</div></div>'
            f'<div class="ae-copy" style="width:100%"><span class="ae-copy__url">aeroapp.ai/t/pocket-7k2</span>{btn("Copy", "secondary", size="sm", icon="copy")}</div>'
            f'<div class="ae-small">{i("monitor", "ae-i--sm")} Their tab · {i("mic", "ae-i--sm")} Their voice · no account</div></div></div>')
    rows = [opt("Name", "Testers see this at the start.", "", stack=True, extra=f'<div style="display:flex;gap:8px;align-items:center">{field("Pocket")}<span class="pr-saved">{i("check", "ae-i--sm")} Saved</span></div>'),
            opt("Taking new sessions", "Turn off to stop new sessions. The ones you have stay.", toggle(True)),
            opt("Record audio", "Their voice as they think aloud.", toggle(True)),
            opt("Record screen", "The tab they test in.", toggle(True)),
            opt("Difficulty rating", "Ask how hard each task was.", toggle(True))]
    if demo_thumb:
        rows.append(opt("What testers open", "A copy of pocket.aeroapp.ai v3. Updating the site doesn't change it.", "", stack=True,
                        extra=f'<div style="display:flex;gap:10px;align-items:center"><span class="pr-thumb" style="width:96px;height:62px">{thumb52().replace("pr-thumb","")}</span>{btn("Upload to this test", "secondary", size="sm", icon="upload")}</div>'))
    return f'<div class="pr-rail">{link}{rail("Settings", rows)}</div>'

def tasks_msgs():
    tk = "".join(f'<div class="ae-task"><span class="ae-task__n">{k + 1}</span><span class="ae-task__text">{t}</span>{i("grip", "ae-task__grip")}</div>' for k, t in enumerate(S["tasks"]))
    return (sect("Tasks", f'<div class="ae-stack ae-stack--tight">{tk}<div class="ae-task ae-task--add"><span>+</span><span>Add a task</span></div></div><div class="ae-small">Optional. With none, testers explore freely.</div>')
            + sect("Messages", '<div class="ae-field"><span class="ae-field__label">Welcome</span><div class="ae-textarea" style="min-height:56px">Thanks for helping with Pocket. Try the two tasks and say what you think as you go.</div></div>'
                   '<div class="ae-field"><span class="ae-field__label">Thank you</span><div class="ae-textarea" style="min-height:44px">That is everything. Thank you.</div></div>'))

def source_block():
    return (f'<div class="pr-set">{opt("What testers open", "A copy of <b>pocket.aeroapp.ai</b> v3, pinned. Updating the site doesn’t change it. Sessions keep the version they saw.", "", stack=True, extra=f"""<div style="display:flex;gap:8px;flex-wrap:wrap">{btn("Upload to this test", "secondary", size="sm", icon="upload")}{btn("Use the site’s latest (v4)", "ghost", size="sm", icon="refresh")}</div>""")}</div>')

def test_setup(variant="B", plan="free"):
    if variant == "A":
        main = f'<div class="pr-main">{tasks_msgs()}</div>'
        rail_ = test_rail(plan, demo_thumb=True)
        thumb = False
    else:
        main = f'<div class="pr-main">{sect("What testers open", prev("aeroapp.ai/t/pocket-7k2", "test", "Screenshot · v3 · pinned", sm=True) + source_block().replace("What testers open", "Source"))}{tasks_msgs()}</div>'
        rail_ = test_rail(plan)
        thumb = True
    return shell(test_top(thumb, False, plan) + tabsrow("Setup") + f'<div class="pr-cols">{main}{rail_}</div>', plan, "tests", "Pocket")

# ------------------------------------------------------------------ menus
def menu(items):
    out = []
    for it in items:
        if it == "-":
            out.append('<div class="ae-menu__sep"></div>')
            continue
        ic, label, kind = it[0], it[1], (it[2] if len(it) > 2 else "")
        cls = "ae-menu__item" + (" ae-menu__item--bad" if kind == "bad" else "")
        pr = f' <span style="margin-left:auto">{proposed()}</span>' if kind == "prop" else ""
        out.append(f'<div class="{cls}">{i(ic, "ae-i--sm")}{label}{pr}</div>')
    return f'<div class="ae-menu" style="width:260px">{"".join(out)}</div>'

SITE_MENU = menu([("tests", "Test this site"), ("copy", "Duplicate"), ("download", "Download files", "prop"), "-", ("trash", "Delete site", "bad")])
SITE_MENU_HAS = menu([("tests", "Open its test"), ("copy", "Duplicate"), ("download", "Download files", "prop"), "-", ("trash", "Delete site", "bad")])
TEST_MENU = menu([("out", "Preview as tester"), ("copy", "Copy test link"), ("sites", "Open Pocket (the site)"), ("copy", "Duplicate test", "prop"), "-", ("trash", "Delete test", "bad")])
LIST_MENU = menu([("edit", "Rename"), ("copy", "Duplicate"), ("tests", "Test this site"), "-", ("trash", "Delete", "bad")])

def plain(inner, title="", sub=""):
    cap = f'<figcaption>{title} <span class="n">{sub}</span></figcaption>' if title else ""
    return f'<figure class="pr-fig">{cap}<div class="pr-card">{inner}</div></figure>'

# ------------------------------------------------------------------ section frames for the upsell comparison (rail only, unscaled)
def rail_free_A():
    return (upcard("This site goes offline on Mon 2 Nov.", "Free sites stay live 7 days. Your files are kept.", "See plans")
            + '<div style="height:14px"></div>' + rail("Settings", site_rows("free")[:6]))

def rail_free_today():
    def ban(t, m, ic="sparkle"):
        return f'<div class="pr-up pr-up--blue" style="margin:10px 0">{i(ic)}<div style="flex:1"><div class="pr-up__t">{t}</div><div class="pr-up__s">{m}</div></div>{btn("Upgrade now", "primary", size="sm")}</div>'
    dim = lambda x: f'<div style="opacity:.45">{x}</div>'
    return ("".join([
        dim(opt("Site address", "", "", stack=True, extra=field("open-chestnut", ".aeroapp.ai"))) + ban("Choose your aeroapp.ai address", "Swap the generated address for a short one people can remember.", "sites"),
        dim(opt("Password protection", "Require a password to view this site", toggle(False))) + ban("Password protection", "Only people with the password can open the site.", "lock"),
        dim(opt("Favicon", "", btn("Upload image", "secondary", size="sm"))) + ban("Your own favicon", "Show your own icon in the browser tab."),
        dim(opt("Custom domain", "", btn("Connect", "secondary", size="sm"))) + ban("Use your own domain", "Connect a domain you already own.", "sites"),
        ban("Remove the Aero badge", "Your site shows without “Made with Aero” in the corner.", "tests"),
    ]))

def rail_free_C():
    rows = [("Address", "Own aeroapp.ai address", "Basic"), ("Password", "Password protection", "Basic"), ("Favicon", "Custom favicon", "Basic"), ("Aero badge", "No Aero badge", "Basic"), ("Custom domain", "Your own domain", "Solo"), ("Visits", "Site analytics", "Solo")]
    lock = "".join(f'<div style="display:flex;align-items:center;gap:8px;padding:8px 0;border-top:1px solid var(--ae-line)"><span class="ae-small" style="flex:1;color:var(--ae-ink)">{b}</span>{tag(c, "line", "lock")}</div>' for a, b, c in rows)
    return ('<div class="pr-set">' + opt("Name", "", "", stack=True, extra=field("Pocket")) + opt("Password", "", toggle(False)) + '</div>'
            f'<div class="ae-card ae-card--pad" style="margin-top:14px"><div class="ae-label">Your plan: Free</div><div class="ae-small" style="margin:6px 0 4px">3 test sessions, recordings, transcripts and summaries. Sites stay live 7 days.</div>'
            f'<div class="ae-small" style="margin:10px 0 2px"><b style="color:var(--ae-ink)">Not on Free</b></div>{lock}<div style="margin-top:10px">{btn("See plans", "secondary", size="sm")}</div></div>')

# ================================================================== assemble
out = []
out.append(HERO)
out.append(GLANCE)

# ---- 1 shared pattern
site_rail_demo = f'<div class="pr-card" style="width:340px">{rail("Settings", site_rows("basic")[:5])}</div>'
test_rail_demo = f'<div class="pr-card" style="width:340px">{rail("Settings", [opt("Name", "Testers see this at the start.", "", stack=True, extra=field("Pocket")), opt("Taking new sessions", "Turn off to stop new sessions. The ones you have stay.", toggle(True)), opt("Record audio", "Their voice as they think aloud.", toggle(True)), opt("Record screen", "The tab they test in.", toggle(True)), opt("Difficulty rating", "Ask how hard each task was.", toggle(True))])}</div>'
out.append(sec(1, "s1", Q1_TITLE, Q1_LEDE, Q1_WHY,
    f'<div class="pr-grid pr-grid--3"><figure class="pr-fig"><figcaption>Site: Settings rail <span class="n">Basic plan</span></figcaption>{site_rail_demo}</figure>'
    f'<figure class="pr-fig"><figcaption>Test: Settings rail <span class="n">Setup tab</span></figcaption>{test_rail_demo}</figure>'
    f'<div>{Q1_ANATOMY}</div></div>' + Q1_TABLE))

# ---- 2 site page
out.append(sec(2, "s2", Q2_TITLE, Q2_LEDE, Q2_WHY,
    '<div class="appr" style="--n:1">'
    + approach("Free", "Site page", "One upsell card (the 7-day clock). Every paid row is locked in place with its plan named. Visits is locked and names Solo.", site_page("free"), False, "", "", 1180, 1560)
    + approach("Basic", "Site page", "Own address, password, favicon and badge are live. Custom domain and Visits wait for Solo. No card.", site_page("basic"), False, "", "", 1180, 1560)
    + approach("Pro", "Site page", "Nothing locked, no upsell. Visits has data (Example numbers).", site_page("pro"), False, "", "", 1180, 1900)
    + '</div><h3 class="states-h">Phone, 390 wide</h3><div class="states" style="--n:3">'
    + state("Free", "card first, then the page", shell(bar(crumbs("Sites", "Pocket"), btn("", "ghost", size="sm", icon="more", extra="ae-btn--icon")) + f'<div class="pr-top"><div class="pr-top__text"><h1 class="pr-title">Pocket</h1><div class="pr-meta"><span class="ae-mono">open-chestnut.aeroapp.ai</span>{status("Live", "live")}</div></div></div><div class="pr-cols"><div class="pr-main">{prev("open-chestnut.aeroapp.ai")}{sect("Tests", tests_of_site(), btn("Test this site", "secondary", size="sm"))}{sect("Update", update_block())}</div><div class="pr-rail">{upcard("Offline on Mon 2 Nov.", "Free sites stay live 7 days.", "See plans")}{rail("Settings", site_rows("free")[:4])}</div></div>', "free", "sites"), 390, 1500, 1500)
    + state("Pro", "settings, then Visits", shell(bar(crumbs("Sites", "Pocket"), btn("", "ghost", size="sm", icon="more", extra="ae-btn--icon")) + f'<div class="pr-top"><div class="pr-top__text"><h1 class="pr-title">Pocket</h1><div class="pr-meta"><span class="ae-mono">pocket.aeroapp.ai</span>{status("Live", "live")}</div></div></div><div class="pr-cols"><div class="pr-main">{prev("pocket.aeroapp.ai")}{visits_block("data")}</div><div class="pr-rail">{rail("Settings", site_rows("pro")[:4])}</div></div>', "pro", "sites"), 390, 1700, 1700)
    + state("Menu", "bottom sheet on a phone", f'<div class="pr-card" style="margin:40px 14px">{SITE_MENU}</div>', 390, 360, 360)
    + '</div>' + Q2_NOTES))

# ---- 3 test page
out.append(sec(3, "s3", Q3_TITLE, Q3_LEDE, Q3_WHY,
    '<div class="appr" style="--n:1">'
    + approach("Free", "Sessions, at the limit", "The meter turns amber in the header and one card says what to do. The list stays first: sessions are the point of the page.", test_sessions("free", True), False, "", "", 1180, 760)
    + approach("Pro", "Sessions", "Nothing about plans. The header thumbnail says which prototype this is on every tab.", test_sessions("pro", False), False, "", "", 1180, 700)
    + approach("A", "Setup, preview as in the website demo", "Smallest change: a thumbnail in the “What testers open” row of the rail. Keeps the page as short as today.", test_setup("A", "free"), False, "", "", 1180, 1000)
    + approach("B", "Setup, same preview as the site page", "The site page’s preview component at its small size, then the source. Matches the site page, which is the point of question 1.", test_setup("B", "free"), True, "", "", 1180, 1250)
    + '</div><h3 class="states-h">Phone, 390 wide</h3><div class="states" style="--n:3">'
    + state("Sessions, Free", "limit reached", test_sessions("free", True), 390, 980, 980)
    + state("Setup, Free", "preview, source, tasks, then settings", test_setup("B", "free"), 390, 1900, 1900)
    + state("Menu", "", f'<div class="pr-card" style="margin:40px 14px">{TEST_MENU}</div>', 390, 360, 360)
    + '</div>' + Q3_NOTES))

# ---- 4 placement, menus
rel = ('<div class="pr-flow"><div class="pr-box pr-box--pub"><b>Site</b>pocket.aeroapp.ai · v4 · public<span class="pr-mono">Update: drop files, prompt, Figma link</span></div>'
       f'<div class="pr-arrow">{i("arrow")}<span class="pr-mono">Test this site</span></div>'
       '<div class="pr-box pr-box--test"><b>Test copy</b>aeroapp.ai/t/pocket-7k2 · pinned to v3<span class="pr-mono">Update: Upload to this test (the site is never written)</span></div>'
       f'<div class="pr-arrow">{i("arrow")}<span class="pr-mono">testers</span></div>'
       '<div class="pr-box"><b>Sessions</b>each keeps the version it saw<span class="pr-mono">Insights read across them</span></div></div>')
out.append(sec(4, "s4", Q4_TITLE, Q4_LEDE, Q4_WHY,
    f'<div style="margin-bottom:22px">{rel}</div>' + Q4_TABLE
    + '<div class="pr-grid pr-grid--4">'
    + plain(SITE_MENU, "Site ⋯", "no test yet") + plain(SITE_MENU_HAS, "Site ⋯", "has a test") + plain(TEST_MENU, "Test ⋯", "new") + plain(LIST_MENU, "Sites list card ⋯", "today, unchanged") + '</div>'
    + '<h3 class="states-h">The Update block, close up</h3><div class="pr-grid pr-grid--2">'
    + plain(update_block(), "Site: Update", "replaces Drop a new version, Publish automatically, Update with a prompt and Site source")
    + plain(source_block(), "Test: What testers open", "Upload to this test, and the way back to the site") + '</div>' + Q4_NOTES))

# ---- 5 Figma convert
flow = ('<div class="pr-flow">'
        '<div class="pr-box pr-box--pub"><b>1. In Aero</b>New site, From Figma, Other ways, Convert. Paste a Figma link, pick Claude or ChatGPT, copy the prompt.<span class="pr-mono">Copy saves a draft and mints a publish key</span></div>'
        f'<div class="pr-arrow">{i("arrow")}</div>'
        '<div class="pr-box pr-box--out"><b>2. Outside Aero: your chat</b>You add the Figma connector yourself (claude.ai/customize/connectors, or ChatGPT Settings, Apps). The agent reads the frame through it.<span class="pr-mono">Figma’s side: its MCP server</span></div>'
        f'<div class="pr-arrow">{i("arrow")}</div>'
        '<div class="pr-box pr-box--out"><b>3. Outside Aero: the agent writes one index.html</b>CSS inline, colour blocks in place of images, zips it and POSTs it with curl.<span class="pr-mono">Needs a shell and network in the chat</span></div>'
        f'<div class="pr-arrow">{i("arrow")}</div>'
        '<div class="pr-box pr-box--pub"><b>4. In Aero</b>The page is watching the draft. When the deploy lands it says “It is live”.</div></div>')
modal_today = (f'<div class="ae-modal" style="width:100%;max-width:460px;position:static"><div class="ae-modal__head"><span class="ae-h3">Add a Figma prototype</span></div><div class="ae-modal__body ae-stack">'
               f'<div class="ae-field"><span class="ae-field__label">Figma prototype link</span><div class="ae-input" style="color:var(--ae-ink-4)">https://www.figma.com/proto/…</div></div>'
               f'<div class="ae-source-tile"><div class="ae-source-tile__title">Convert with AI</div><div class="ae-source-tile__sub">Your AI agent rebuilds the design as real code and publishes it here. Needs a paid Figma seat.</div></div></div></div>')
def modal_opt(t, s, tagx=""):
    return (f'<div class="ae-modal" style="width:100%;max-width:460px;position:static"><div class="ae-modal__head"><span class="ae-h3">Add a Figma prototype</span></div><div class="ae-modal__body ae-stack">'
            f'<div class="ae-field"><span class="ae-field__label">Figma prototype link</span><div class="ae-input" style="color:var(--ae-ink-4)">https://www.figma.com/proto/…</div></div>'
            f'<div class="ae-small" style="margin-top:-4px">Other ways</div>{t}{s}</div></div>')
lab = ('<div class="ae-source-tile"><div class="ae-source-tile__title">Build real code from your design ' + tag("Advanced", "line") + '</div>'
       '<div class="ae-source-tile__sub">Claude or ChatGPT reads one frame through Figma’s connector and writes a plain web page. Layout only: no prototype interactions, images become colour blocks. Needs a Dev or Full seat on a paid Figma plan.</div></div>')
exp = '<div class="ae-source-tile"><div class="ae-source-tile__title">Export with a plugin</div><div class="ae-source-tile__sub">Anima, Figma to Code or pxCode inside Figma, then drop the HTML here.</div></div>'
out.append(sec(5, "s5", Q5_TITLE, Q5_LEDE, Q5_WHY,
    f'<div style="margin-bottom:22px">{flow}</div>' + Q5_TABLE
    + '<div class="pr-grid pr-grid--3">'
    + plain(modal_today, "Today", "the row, collapsed under Other ways")
    + plain(modal_opt(lab, exp), "B. Label it  (recommended)", "same place, honest words, plugin export beside it")
    + plain(f'<div class="ae-modal" style="width:100%;max-width:460px;position:static"><div class="ae-modal__head"><span class="ae-h3">Add a Figma prototype</span></div><div class="ae-modal__body ae-stack"><div class="ae-field"><span class="ae-field__label">Figma prototype link</span><div class="ae-input" style="color:var(--ae-ink-4)">https://www.figma.com/proto/…</div></div><div class="ae-small" style="margin-top:-4px">Other ways</div>{exp}</div></div>', "A. Hide it", "link and plugin export only; the code path stays, unlinked") + '</div>' + Q5_NOTES))

# ---- 6 upsell
out.append(sec(6, "s6", Q6_TITLE, Q6_LEDE, Q6_WHY,
    '<div class="pr-grid pr-grid--3">'
    + plain(rail_free_today(), "Today: a banner under every locked block", "5 here, 6 on the page, each with Upgrade now. Redrawn from the code, not a screenshot.")
    + plain(rail_free_A(), "A. Locked rows and one card  (recommended)", "Plan named in the row. One card, only for a real limit.")
    + plain(rail_free_C(), "C. One plan summary", "Everything locked in one card at the foot of the rail. Fewer words, but it moves value away from the feature.")
    + '</div>' + Q6_TABLE
    + '<h3 class="states-h">Where the one card shows up</h3><div class="pr-grid pr-grid--3">'
    + plain(upcard("This site goes offline on Mon 2 Nov.", "Free sites stay live 7 days. Your files are kept.", "See plans"), "Site, Free", "the 7-day clock. Gone on any paid plan")
    + plain(upcard("You have 3 of 3 sessions kept.", "New sessions can't start until you delete one or move to a bigger plan. The ones you have stay.", "See plans", "alert"), "Test, any plan at its limit", "the session meter at its limit")
    + plain('<div class="pr-set">' + opt("Custom domain", "Use a domain you already own.", btn("Connect", "secondary", size="sm"), plan="Solo", locked=True) + '</div><div class="ae-small" style="margin-top:10px">Tap a locked row: the plans dialog opens in place, scrolled to the plan that has it. Close it and you are back on the row.</div>', "Any locked row", "no card, the row is the prompt") + '</div>' + Q6_NOTES))

# ---- 7 visits
loading = shell(bar(crumbs("Sites", "Pocket")) + '<div class="pr-cols pr-cols--one" style="padding-top:24px">' + visits_block("loading") + '</div>', "pro", "sites")
out.append(sec(7, "s7", Q7_TITLE, Q7_LEDE, Q7_WHY,
    Q7_TODAY + Q7_MAP
    + '<div class="appr" style="--n:1">'
    + approach("A", "Visits section, Pro", "Four headline numbers that also switch the chart, one chart, three short lists. Sentence case, Geist, flat. Example numbers.", shell(bar(crumbs("Sites", "Pocket")) + '<div class="pr-cols pr-cols--one" style="padding-top:24px"><div class="pr-main">' + visits_block("data") + '</div></div>', "pro", "sites"), True, "", "", 1180, 880)
    + '</div><h3 class="states-h">States, and phone</h3><div class="states" style="--n:2">'
    + state("Loading", "shapes from the real layout", shell(bar(crumbs("Sites", "Pocket")) + '<div class="pr-cols pr-cols--one" style="padding-top:24px">' + visits_block("loading") + '</div>', "pro", "sites"), 1180, 520, None)
    + state("No visits yet", "", shell(bar(crumbs("Sites", "Pocket")) + '<div class="pr-cols pr-cols--one" style="padding-top:24px">' + visits_block("empty") + '</div>', "pro", "sites"), 1180, 520, None)
    + state("Locked on Free and Basic", "no sample numbers", shell(bar(crumbs("Sites", "Pocket")) + '<div class="pr-cols pr-cols--one" style="padding-top:24px">' + visits_block("locked") + '</div>', "basic", "sites"), 1180, 520, None)
    + state("Phone", "stats 2 by 2, lists stacked", shell(bar(crumbs("Sites", "Pocket")) + '<div class="pr-cols pr-cols--one"><div class="pr-main">' + visits_block("data") + '</div></div>', "pro", "sites"), 390, 1500, 1500)
    + '</div>' + Q7_NOTES))

# ---- 8 motion
out.append(sec(8, "s8", Q8_TITLE, Q8_LEDE, Q8_WHY, Q8_TABLE))

# ---- 9 decisions, sources
out.append(sec(9, "s9", "Decisions for Duane", DEC_LEDE, DEC_WHY, DECISIONS + SOURCES))

html_out = page_pr("pages-round.html", "Aero pages round", "Site page, test page, Visits, the Figma convert path and the upsell pattern, designed in the v3 kit.", "".join(out))
open("pages-round.html", "w").write(html_out)
print("pages-round.html", len(html_out))
