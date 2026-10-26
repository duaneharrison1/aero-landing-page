from build_common import *

S = SCENE

# ------------------------------------------------------------------ shared page parts
def head(title, crumbs=None, meta="", actions="", wash=None, sub=""):
    cr = ""
    if crumbs:
        cr = '<div class="ae-crumbs">' + ' <span>/</span> '.join(crumbs[:-1] + [f"<b>{crumbs[-1]}</b>"]) + '</div>'
    w = f" ae-head--wash ae-head--{wash}" if wash else ""
    m = f'<div class="ae-head__meta">{meta}</div>' if meta else ""
    sb = f'<p class="ae-p" style="max-width:640px">{sub}</p>' if sub else ""
    return f'<div class="ae-head{w}">{cr}<div class="ae-head__row"><h1 class="ae-h1 ae-head__title">{title}</h1><div class="ae-row-gap">{actions}</div></div>{sb}{m}</div>'

def tabs(items, active, inner=False):
    out = []
    for it in items:
        name, extra = (it if isinstance(it, tuple) else (it, ""))
        out.append(f'<span class="ae-tab{" is-active" if name == active else ""}">{name}{extra}</span>')
    return f'<div class="ae-tabs{" ae-tabs--inner" if inner else ""}">{"".join(out)}</div>'

TEST_TABS = lambda n=3, review_dot=True: [("Setup", ""), ("Share", ""), ("Sessions", f' <span class="ae-tab__n">{n}</span>'), ("Review", ' <span class="ae-tab__dot"></span>' if review_dot else "")]
SITE_TABS = ["Overview", "Versions", "Settings", "Domain", "Analytics"]

def body(inner, cls=""):
    return f'<div class="ae-body {cls}">{inner}</div>'

def section(title, inner, right=""):
    return f'<div class="ae-section"><div class="ae-section__head"><span class="ae-h3">{title}</span>{right}</div>{inner}</div>'

def feed(items):
    out = []
    for icon, kind, title, sub, right, unread in items:
        out.append(f'<div class="ae-feed-item{" is-unread" if unread else ""}"><span class="ae-feed-item__icon ae-feed-item__icon--{kind}">{i(icon)}</span><span style="min-width:0"><div class="ae-feed-item__title">{title}</div><div class="ae-feed-item__sub">{sub}</div></span>{right}</div>')
    return f'<div class="ae-list--card"><div class="ae-feed">{"".join(out)}</div></div>'

FEED_NEW = [
    ("sessions", "review", "2 new sessions on Pocket", "Tester B and Tester C · Session 3 transcript arriving", '<span class="ae-tc">10:51</span>', True),
    ("review", "review", "Review ready for Pocket", "What to fix first, based on 2 of 3 sessions", '<span class="ae-tc">10:52</span>', True),
    ("clock", "warn", "onboarding.aeroapp.ai goes offline in 2 days", "Free sites stay live 7 days", btn("Keep it live", "secondary", size="sm"), False),
]

def test_row(t):
    st = {"Review ready": tag("Review ready", "review"), "1 session": tag("Collecting", "test"), "Link shared": tag("Waiting for testers", "test")}[t["state"]]
    new = f'<span class="ae-test-row__new">{t["new"]} new</span>' if t["new"] else f'<span class="ae-tc">{t["sessions"]} session{"s" if t["sessions"] != 1 else ""}</span>'
    tk = f'{t["tasks"]} tasks' if t["tasks"] else "Explore freely"
    return f'<div class="ae-test-row"><span style="min-width:0"><div class="ae-test-row__name">{t["name"]}</div><div class="ae-test-row__sub">{t["site"]}</div></span><span class="ae-test-row__sub">{tk} · {t["kind"]}</span>{new}{st}{i("right","ae-i--sm")}</div>'

def tests_list(rows=None):
    rows = rows if rows is not None else S["tests"]
    return (f'<div class="ae-list--card"><div class="ae-listhead" style="grid-template-columns:minmax(0,2.2fr) minmax(0,1.3fr) 110px 120px 28px"><span>Test</span><span>Tasks</span><span>Sessions</span><span>Status</span><span></span></div>'
            f'<div class="ae-list">{"".join(test_row(t) for t in rows)}</div></div>')

def site_card(s, compact=False):
    st = {"live": status("Live", "live"), "soon": status(f'Offline in {s["days"]} days', "soon"), "offline": status("Offline, free plan ended", "offline"), "draft": status("Draft", "draft")}[s["status"]]
    off = " is-offline" if s["status"] == "offline" else ""
    if s["status"] == "offline":
        act = btn("Put back online", "secondary", size="sm")
    elif s.get("test"):
        act = f'<span class="ae-small">{i("tests","ae-i--sm")} Has a test</span>'
    else:
        act = btn("Run a test", "ghost", size="sm", icon="tests")
    return (f'<div class="ae-site-card{off}"><div class="ae-site-card__thumb">{thumb(s)}</div><div class="ae-site-card__body"><div class="ae-site-card__url">{s["slug"]}.aeroapp.ai</div>'
            f'<div class="ae-site-card__meta">{st}<span class="ae-sep"></span>v{s["ver"]} · {s["when"]}</div></div><div class="ae-site-card__foot">{tag(s["how"], "line")}<span class="ae-spacer"></span>{act}</div></div>')

def sites_grid(n=3):
    return f'<div class="ae-grid ae-grid--3">{"".join(site_card(s) for s in S["sites"][:n])}</div>'

def drafts_row(n=2):
    return f'<div class="ae-callout" style="align-items:center">{i("edit")}<span><b>{n} unfinished</b> · a site and a test you started but did not finish.</span><span class="ae-callout__act ae-row-gap">{btn("Resume", "ghost", size="sm")}{btn("Clear", "ghost", size="sm")}</span></div>'

def new_btn(label="New", glass=True):
    return btn(label, "primary", glass, icon="plus")

def srow(s, selected=False):
    st = {"ready": status("Ready", "ready"), "processing": status("Transcript arriving", "processing"), "recording": status("Recording now", "recording"), "noaudio": status("No audio", "noaudio"), "ended": status("Ended early", "offline")}[s["status"]]
    if s["quote"]:
        q = f'<span class="ae-session-row__quote">“{E(s["quote"])}”</span>'
    else:
        txt = {"processing": "Transcript arriving, usually about a minute", "recording": "The tester is still going", "noaudio": "Screen only. The tester turned off their mic.", "ended": "Closed the tab at 01:12"}.get(s["status"], "")
        q = f'<span class="ae-session-row__quote is-muted">{txt}</span>'
    return f'<div class="ae-session-row{" is-selected" if selected else ""}"><span class="ae-session-row__n">Session {s["n"]}</span><span class="ae-session-row__who">{avatar(s["who"][-1], s["av"])}<span style="min-width:0"><div class="ae-session-row__name">{s["who"]}</div><div class="ae-session-row__dev">{s["dev"]}</div></span></span>{q}<span class="ae-tc">{s["len"]}</span>{st}</div>'

MORE_S = [{"n": 4, "who": "Tester D", "av": "d", "dev": "Laptop · Safari", "len": "02:10", "status": "recording", "quote": ""},
          {"n": 5, "who": "Tester E", "av": "e", "dev": "Laptop · Chrome", "len": "03:31", "status": "noaudio", "quote": ""}]

def sessions_list(rows=None):
    rows = rows if rows is not None else list(reversed(S["sessions"]))
    return (f'<div class="ae-list--card"><div class="ae-listhead" style="grid-template-columns:76px minmax(150px,1.3fr) minmax(0,2.4fr) 52px 168px"><span>#</span><span>Tester</span><span>In their words</span><span>Length</span><span>Status</span></div>'
            f'<div class="ae-list">{"".join(srow(s) for s in rows)}</div></div>')

def test_head(active="Sessions", n=3, actions=None, wash="test", meta_extra="", name="Pocket", url="pocket.aeroapp.ai", tasks="2 tasks", st=None):
    acts = actions if actions is not None else btn("Copy link", "secondary", icon="copy") + btn("", "ghost", icon="more", extra="ae-btn--icon")
    st = st if st is not None else status("Collecting sessions", "live")
    meta = f'<span class="ae-area ae-area--test">Test</span>{st}<span class="ae-mono ae-small">{url}</span><span>{tasks}</span>{meta_extra}'
    return head(name, ["Tests", name], meta, acts, wash) + tabs(TEST_TABS(n, n >= 2), active)

def skel_rows(n=3, cols="1fr 2fr 80px"):
    r = "".join(f'<div style="display:grid;grid-template-columns:{cols};gap:16px;padding:14px 16px;align-items:center"><span class="ae-skel ae-skel--text" style="width:70%"></span><span class="ae-skel ae-skel--text" style="width:{60+k*10}%"></span><span class="ae-skel ae-skel--text"></span></div>' for k in range(n))
    return f'<div class="ae-list--card"><div class="ae-list">{r}</div></div>'

def phone(inner, title="Home", active="home", back=False, right=""):
    """Phone frame of the app (390 wide)."""
    return app(inner, active=active, mtitle=title, mback=back, mright=right)

out = []
out.append(f'''<div class="b-hero"><div class="b-kicker">Aero app UI · step 1 · screens 1 to 9, 11 to 13</div>
<h1>Every screen, side by side<span class="d">.</span></h1>
<p>For each screen: two or three approaches taken from the round 5 directions (A Studio, B Colour, C Story, D Replay), in the agreed brand, with the states below. Everything is built from <a href="components.html">the components</a>, with Kestrel Studio as example data.</p>
<p class="ae-small">Labels: <span class="today">Today</span> works in Aero now (redesigned). <span class="proposed">Proposed</span> needs new work. The tester flow (screen 10) is designed separately. Switch palette and layout at the top right; "Large" shows one approach per row.</p>
<div class="b-toc">{"".join(f'<a href="#s{n}">{n:02d} {t}</a>' for n,t in [(1,"Shell"),(2,"Home"),(3,"Create"),(4,"Site detail"),(5,"Test setup"),(6,"Share"),(7,"Sessions"),(8,"Session view"),(9,"Review across sessions"),(11,"Plans and usage"),(12,"Guidance"),(13,"States")])}</div></div>''')

# ================================================================== 01 SHELL
home_a_body = body(
    section("What's new", feed(FEED_NEW), '<a class="ae-link ae-small">Mark all as seen</a>')
    + section("Tests", tests_list(), btn("New test", "ghost", size="sm", icon="plus"))
    + section("Sites", sites_grid(), '<span class="ae-small">Versions and roll back on every site</span>')
    + drafts_row())
home_head = head("Good morning, Mia", None, "", new_btn("New"), None, "")

shell_a = app(home_head + home_a_body, "sidebar", "home")
shell_b = app(home_head + home_a_body, "top", "home")
ctx = ('<aside class="ae-context"><div class="ae-label" style="padding:6px 8px 8px">Pocket · sessions</div>'
       + "".join(f'<div class="ae-session-item{" is-active" if s["n"] == 2 else ""}">{avatar(s["who"][-1], s["av"], "sm")}<span style="min-width:0"><div class="ae-session-item__name">Session {s["n"]} · {s["who"]}</div><div class="ae-session-item__sub">{s["dev"]}</div></span><span class="ae-tc">{s["len"]}</span></div>' for s in S["sessions"])
       + f'<div style="margin-top:auto" class="ae-guide ae-guide--closed"><span class="ae-guide__head" style="font-size:12px">{i("book")}How the review is made</span></div></aside>')
sess_short = (head("Session 2 · Tester B", ["Tests", "Pocket", "Session 2"], f'{status("Ready","ready")}<span>Laptop · Chrome</span><span class="ae-tc">07:12</span><span>Sunday 11:40</span>', btn("", "ghost", icon="left", extra="ae-btn--icon") + btn("", "ghost", icon="right", extra="ae-btn--icon"))
              + body(f'<div class="ae-body--split" style="display:grid">{player(0.435)}<div class="ae-stack"><div class="ae-label">Summary</div><p class="ae-p" style="color:var(--ae-ink-2)">Sent money without help. Expected cards on the home screen and found them under More. Unsure how to leave Send.</p><div class="ae-label">Friction points</div>{friction(FRICTION[0], True)}</div></div>'))
shell_c = app(sess_short, "rail", "tests", extra_cols=ctx)

menu_overlay = f'<div style="position:absolute;top:58px;left:12px;z-index:50">{"".join([])}<div class="ae-menu"><div class="ae-menu__item is-active"><span class="ae-mark" style="width:20px;height:20px;font-size:10px;border-radius:6px"><span>A</span></span>Kestrel Studio<span class="ae-spacer"></span>{i("check","ae-i--sm")}</div><div class="ae-menu__item"><span class="ae-avatar ae-avatar--sm ae-avatar--e">P</span>Personal</div><div class="ae-menu__sep"></div><div class="ae-menu__item">{i("plus")}New studio</div><div class="ae-menu__item">{i("users")}Invite people</div><div class="ae-menu__sep"></div><div class="ae-menu__item">{i("settings")}Account and billing</div><div class="ae-menu__item">{i("book")}Help and guides</div><div class="ae-menu__item">{i("out")}Sign out</div></div></div>'
shell_states = (
    state("Phone", "390 · top bar + tab bar, nav at the thumb", phone(home_head + home_a_body), 390, 800, fixed=True)
    + state("Studio switcher open", "studios are proposed; today it is the account menu", app(home_head + home_a_body, "sidebar", "home", overlay=menu_overlay), prop="Studios")
    + state("Loading", "the shell paints at once; content shows its shapes", app(head("Good morning, Mia", None, "", new_btn("New")) + body(section("What's new", skel_rows(3)) + section("Tests", skel_rows(3))), "sidebar", "home"))
)
out.append(screen(1, "s1", "Shell", "Sidebar or top bar, studio switcher, nav (Home, Sites, Tests; Review lives inside a test), plan usage, account.",
    "<b>Pick A.</b> The sidebar has room for recent tests with a quiet \"2 new\", and usage that matches every other page. C's rail plus a sessions column is used <i>inside</i> a session, where you move between testers. No colour in the nav.",
    [approach("A", "Sidebar", "From A Studio. Studio, three places, recent tests, usage, account. Collapses to the A. mark.", shell_a, True, "A Studio"),
     approach("B", "Top bar", "From C Story. More width for content, but recent tests and usage have to hide in menus.", shell_b, False, "C Story"),
     approach("C", "Rail and context column", "From D Replay. Icons only, and a second column for whatever you are in. Best while reviewing sessions.", shell_c, False, "D Replay")],
    shell_states,
    [("Proposed", ["Studios and the switcher (today one account is one person). Without them, the top of the sidebar is the account menu.", "\"2 new\" counts on Tests: needs a seen-at time per test."]),
     ("Copy", ["Nav: Home, Sites, Tests. Review is a tab inside a test, so the three areas read Publish (Sites), Test, Review without three more nav items.", "Usage line is the same everywhere: \"2 of 3 sessions kept\"."]),
     ("Engineer check", ["Shell paints from the auth cache, then the three profile reads run together (B1).", "Phone: tab bar Home, Sites, Tests, Account. The studio switcher moves into Account."])]))

# ================================================================== 02 HOME
def area_col(area, title, rows, cta):
    r = "".join(f'<div style="display:flex;align-items:center;gap:10px;padding:10px 0;border-top:1px solid rgba(0,0,0,.06)"><span style="flex:1;min-width:0"><div class="ae-strong" style="font-size:13.5px">{a}</div><div class="ae-small">{b}</div></span>{c}</div>' for a, b, c in rows)
    return f'<div class="ae-card ae-card--{area}" style="padding:16px 16px 10px;display:flex;flex-direction:column;gap:6px"><div class="ae-row-gap"><span class="ae-area ae-area--{area}">{title}</span><span class="ae-spacer"></span>{cta}</div>{r}</div>'
home_b = app(head("Good morning, Mia", None, "", new_btn("New")) + body(
    f'<div class="ae-grid ae-grid--3" style="align-items:start">'
    + area_col("publish", "Publish", [("pocket.aeroapp.ai", "v4 · live · 2 hours ago", status("Live", "live")), ("onboarding.aeroapp.ai", "Figma · 5 days ago", status("2 days", "soon")), ("kestrel.aeroapp.ai", "HTML · free plan ended", status("Offline", "offline"))], btn("", "ghost", size="sm", icon="plus", extra="ae-btn--icon"))
    + area_col("test", "Test", [("Checkout", "Link shared yesterday", tag("0 sessions", "line")), ("Onboarding v2", "Explore freely", tag("1 session", "line")), ("Pocket", "2 tasks", tag("3 sessions", "line"))], btn("", "ghost", size="sm", icon="plus", extra="ae-btn--icon"))
    + area_col("review", "Review", [("Pocket", "Based on 2 of 3 sessions", tag("Ready", "review")), ("Session 2 · Tester B", "3 friction points", tag("New", "blue")), ("Session 3 · Tester C", "Transcript arriving", status("", "processing"))], "")
    + '</div>' + drafts_row()), "sidebar", "home")

def project_card(name, url, now, line1, line2, act, kind):
    return (f'<div class="ae-card" style="padding:16px;display:grid;grid-template-columns:120px minmax(0,1fr) auto;gap:16px;align-items:center"><div class="ae-site-card__thumb" style="height:84px;border-radius:10px">{thumb(kind)}</div>'
            f'<div class="ae-stack ae-stack--tight"><div class="ae-row-gap"><span class="ae-h3">{name}</span><span class="ae-mono ae-small">{url}</span></div>{progress(now)}<div class="ae-small" style="margin-top:4px">{line1}</div><div class="ae-small">{line2}</div></div>{act}</div>')
home_c = app(head("Good morning, Mia", None, "", new_btn("New")) + body(
    '<div class="ae-stack">'
    + project_card("Pocket", "pocket.aeroapp.ai", 3, "<b class='ae-strong'>2 new sessions</b> since yesterday. Review ready, based on 2 of 3.", "Session 3 transcript arriving, usually about a minute.", btn("Open review", "primary", True), S["sites"][0])
    + project_card("Onboarding v2", "onboarding.aeroapp.ai", 2, "1 session. Patterns across sessions appear after the second one.", "<span style='color:var(--ae-warn)'>Offline in 2 days on Free.</span>", btn("Copy test link", "secondary", icon="copy"), S["sites"][1])
    + project_card("Checkout", "checkout.aeroapp.ai", 1, "Link shared yesterday. No sessions yet.", "Send it to 3 to 5 people.", btn("Copy test link", "secondary", icon="copy"), {"thumb": "#47B58A", "phone": False})
    + '</div>' + drafts_row()), "sidebar", "home")
home_a = app(home_head + home_a_body, "sidebar", "home")

first_run = app(head("Welcome, Mia", None, "", "", None, "Put a prototype online, share a test link, and review what people said. Free to start.") + body(
    f'<div class="ae-grid ae-grid--3">'
    f'<div class="ae-source-tile"><span class="ae-source-tile__icon">{i("prompt")}</span><span class="ae-source-tile__title">One prompt</span><span class="ae-source-tile__sub">Built it in Claude or ChatGPT? Ask it to publish to Aero.</span></div>'
    f'<div class="ae-source-tile"><span class="ae-source-tile__icon">{i("figma")}</span><span class="ae-source-tile__title">Figma link</span><span class="ae-source-tile__sub">Paste a prototype link. Live straight away.</span></div>'
    f'<div class="ae-source-tile"><span class="ae-source-tile__icon">{i("upload")}</span><span class="ae-source-tile__title">HTML or zip</span><span class="ae-source-tile__sub">Drop a file or folder with an index.html.</span></div></div>'
    f'<div class="ae-source-tile ae-source-tile--row"><span class="ae-source-tile__icon" style="background:var(--ae-test-tint);color:var(--ae-test-ink)">{i("tests")}</span><span style="flex:1"><span class="ae-source-tile__title">Already online somewhere else?</span><div class="ae-source-tile__sub">Test any site or Figma prototype by its link.</div></span>{i("right")}</div>'
    f'<div class="ae-guide"><div class="ae-guide__head">{i("book")}How Aero works</div><ol><li><b>Publish.</b> Your prototype gets its own address, like pocket.aeroapp.ai, in seconds to a minute.</li><li><b>Test.</b> Share one link. Testers talk through it while their screen and voice are recorded. Nothing to install.</li><li><b>Review.</b> About a minute after each session: the transcript, a summary and the friction points, in their own words.</li></ol></div>'), "sidebar", "home")
home_loading = app(home_head + body(section("What's new", skel_rows(2)) + section("Tests", skel_rows(3)) + section("Sites", '<div class="ae-grid ae-grid--3">' + "".join('<div class="ae-card"><span class="ae-skel" style="height:120px;border-radius:12px 12px 0 0"></span><div style="padding:12px" class="ae-stack ae-stack--tight"><span class="ae-skel ae-skel--text" style="width:70%"></span><span class="ae-skel ae-skel--text" style="width:40%"></span></div></div>' for _ in range(3)) + '</div>')), "sidebar", "home")
home_quiet = app(home_head + body(section("What's new", f'<div class="ae-empty ae-empty--line" style="padding:22px"><div class="ae-small">{i("check","ae-i--sm")} Nothing new since you last looked. New sessions and reviews show up here.</div></div>') + section("Tests", tests_list([dict(t, new=0, state="1 session") if t["name"] == "Pocket" else t for t in S["tests"]][:2]))), "sidebar", "home")
drafts_open = app(home_head + body(section("Unfinished", f'<div class="ae-list--card"><div class="ae-list">' + "".join(f'<div class="ae-test-row" style="grid-template-columns:minmax(0,1fr) auto auto"><span><div class="ae-test-row__name">{a}</div><div class="ae-test-row__sub">{b}</div></span>{btn("Resume","secondary",size="sm")}{btn("","ghost",size="sm",icon="trash",extra="ae-btn--icon")}</div>' for a, b in [("Untitled site", "HTML upload · 3 files dropped · yesterday"), ("Checkout test", "Figma link pasted, no tasks yet · 3 days ago")]) + '</div></div><p class="ae-small" style="margin:0">Unfinished items with no input are never saved. These clear themselves after 7 days.</p>', btn("Clear all", "ghost", size="sm")) + section("Tests", tests_list())), "sidebar", "home")

out.append(screen(2, "s2", "Home", "What's new across everything, real tests and sites first, drafts folded. No friction points from random projects on Home.",
    "<b>Pick A, with C's progress line as a later option.</b> A answers \"is anything new\" in one list, then shows tests and sites like today but honest. B is the clearest about the three areas, but it splits one prototype across three columns. C groups by prototype, which suits people with a few projects.",
    [approach("A", "What's new, then tests and sites", "From A Studio. One feed of new things (sessions, reviews, expiring sites), each opening where the action is.", home_a, True, "A Studio", "\"What's new\" feed"),
     approach("B", "Three areas", "From B Colour, softened. Publish, Test, Review side by side, each on its wash. No colour in the nav.", home_b, False, "B Colour"),
     approach("C", "By prototype", "From D Replay. Each prototype is one card with the Publish, Test, Review line and its next step.", home_c, False, "D Replay")],
    state("First run", "empty Home teaches the three steps", first_run)
    + state("Loading", "shapes of the real sections, never blank", home_loading)
    + state("Nothing new", "the feed says so, and lists stay", home_quiet)
    + state("Drafts opened", "only drafts with real input exist", drafts_open, prop="Draft rule")
    + state("Phone", "390", phone(home_head + home_a_body), 390, 800, fixed=True),
    [("Proposed", ["The feed needs events (session finished, review ready, site expiring) and a seen-at time.", "Draft rule (B7): save a draft only after real input; clear empty ones after 7 days.", "Clicking a test opens Sessions or Review when they have content, not Setup (B6)."]),
     ("Copy", ["Greeting uses the first name only. No exclamation marks.", "\"Review ready for Pocket\" not \"Insights ready\": Review is the area name.", "Expiry: \"goes offline in 2 days\", with \"Keep it live\" (opens plans)."]),
     ("Engineer check", ["No friction quotes on Home: they belong to a test. The feed only says something happened.", "Drafts count in the Unfinished row, never in Live (B8).", "Counts load with their lists; no \"0\" before the read lands (B2)."])], n_states=3))

# ================================================================== 03 CREATE
prompt_box = (f'<div class="ae-card ae-card--mist" style="padding:16px;display:flex;flex-direction:column;gap:12px">'
              f'<div class="ae-row-gap"><span class="ae-stepper__n" style="width:20px;height:20px">1</span><span class="ae-strong">Copy this prompt</span><span class="ae-spacer"></span>{tag("Has a one-time key", "line", "lock")}</div>'
              f'<div class="ae-copy" style="align-items:flex-start;padding:12px 8px 12px 14px"><span style="flex:1;font-size:13px;color:var(--ae-ink);line-height:1.5">Put this prototype online with Aero and reply with the live link. Name: Pocket. <span class="ae-muted ae-mono" style="font-size:11.5px">key: ae_1f…c9</span></span>{btn("Copy","primary",True,size="sm",icon="copy")}</div>'
              f'<div class="ae-row-gap"><span class="ae-stepper__n" style="width:20px;height:20px">2</span><span class="ae-strong">Paste it in the chat where you built it</span></div>'
              f'<div class="ae-small" style="padding-left:28px">Claude or ChatGPT publishes the files to Aero and replies with the live link. This page updates on its own.</div></div>')
create_a = app(head("New", ["Home", "New"], "", btn("Cancel", "ghost"), None) + body(
    f'<div class="ae-body--split" style="display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:24px">'
    f'<div class="ae-stack ae-stack--loose"><div><div class="ae-h2">How did you make it?</div><p class="ae-p">Three ways in. Each one ends at a live address.</p></div>'
    f'<div class="ae-grid ae-grid--3"><div class="ae-source-tile is-active"><span class="ae-source-tile__icon">{i("prompt")}</span><span class="ae-source-tile__title">One prompt</span><span class="ae-source-tile__sub">Claude or ChatGPT publishes it for you.</span></div><div class="ae-source-tile"><span class="ae-source-tile__icon">{i("figma")}</span><span class="ae-source-tile__title">Figma link</span><span class="ae-source-tile__sub">Paste a prototype link.</span></div><div class="ae-source-tile"><span class="ae-source-tile__icon">{i("upload")}</span><span class="ae-source-tile__title">HTML or zip</span><span class="ae-source-tile__sub">Drop a file or folder.</span></div></div>'
    f'{prompt_box}<div class="ae-source-tile ae-source-tile--row"><span class="ae-source-tile__icon" style="background:var(--ae-test-tint);color:var(--ae-test-ink)">{i("tests")}</span><span style="flex:1"><span class="ae-source-tile__title">Test an existing site instead</span><div class="ae-source-tile__sub">One of your 3 sites, or any link.</div></span>{i("right")}</div></div>'
    f'<div class="ae-stack"><div class="ae-field"><span class="ae-field__label">Name</span><div class="ae-input">Pocket</div></div><div class="ae-field"><span class="ae-field__label">Address</span><div class="ae-affix"><div class="ae-input">pocket</div><span class="ae-affix__end">.aeroapp.ai</span></div></div>'
    f'<div class="ae-guide"><div class="ae-guide__head">{i("clock")}What happens next</div><ol><li>It goes live at pocket.aeroapp.ai, in seconds to a minute.</li><li>You can add a test straight away, or later.</li><li>Every update is a new version you can roll back.</li></ol></div>'
    f'<div class="ae-small">Nothing is saved until you copy the prompt, paste a link or drop files.</div></div></div>'), "sidebar", "home")

create_b = app(head("Put a prototype online", ["Home", "New"], f'<div class="ae-stepper"><span class="ae-stepper__step is-now"><span class="ae-stepper__n">1</span>How you made it</span><span class="ae-stepper__step"><span class="ae-stepper__n">2</span>Name and address</span><span class="ae-stepper__step"><span class="ae-stepper__n">3</span>Add a test</span></div>', btn("Cancel", "ghost")) + body(
    f'<div style="max-width:620px;width:100%;margin:0 auto" class="ae-stack ae-stack--loose"><div class="ae-h2" style="font-size:24px;font-weight:350">How did you make it?</div>'
    + "".join(f'<div class="ae-source-tile ae-source-tile--row{" is-active" if k == 0 else ""}"><span class="ae-radio{" is-on" if k == 0 else ""}"></span><span class="ae-source-tile__icon">{i(ic)}</span><span style="flex:1"><span class="ae-source-tile__title">{t}</span><div class="ae-source-tile__sub">{d}</div></span>{tg}</div>' for k, (ic, t, d, tg) in enumerate([("prompt", "One prompt to Claude or ChatGPT", "It publishes the files and replies with the link.", tag("Fastest", "blue")), ("figma", "A Figma prototype link", "Embed it as it is, or convert it to HTML.", ""), ("upload", "An HTML file, folder or zip", "Needs an index.html at the top.", "")]))
    + f'<div class="ae-row-gap" style="justify-content:space-between"><a class="ae-link ae-small">Or test something already online</a>{btn("Continue","primary",True,icon_after="arrow")}</div></div>'), "sidebar", "home")

create_c = app(head("New", ["Home", "New"], "", btn("Cancel", "ghost")) + body(
    f'<div style="max-width:760px;width:100%;margin:0 auto" class="ae-stack ae-stack--loose"><div><div class="ae-display ae-dot-end">One prompt and it\'s live</div><p class="ae-p" style="margin-top:8px;font-size:15px">Paste this where you built your prototype. Claude or ChatGPT publishes it to Aero.</p></div>'
    f'<div class="ae-copy ae-copy--lg" style="align-items:flex-start;padding:16px 10px 16px 18px;background:var(--ae-publish-wash);box-shadow:none"><span style="flex:1;font-size:15px;color:var(--ae-ink);line-height:1.5">Put this prototype online with Aero and reply with the live link. Name: Pocket.</span>{btn("Copy prompt","primary",True,icon="copy")}</div>'
    f'<div class="ae-row-gap ae-small">{status("Waiting for your chat to publish", "processing")}<span class="ae-sep"></span><span>The key in the prompt works once, for 30 minutes.</span></div>'
    f'<hr class="ae-hr"><div class="ae-label">Or</div><div class="ae-grid ae-grid--2"><div class="ae-stack"><div class="ae-field"><span class="ae-field__label">{i("figma","ae-i--sm")} Figma prototype link</span><div class="ae-input is-placeholder">https://www.figma.com/proto/…</div></div></div><div class="ae-drop" style="padding:18px">{i("upload")}<b>Drop HTML, a folder or a zip</b></div></div>'
    f'<a class="ae-link ae-small">Test a site that is already online</a></div>'), "sidebar", "home")

wait = app(head("New", ["Home", "New"], "", btn("Cancel", "ghost")) + body(
    f'<div style="max-width:620px;margin:0 auto;width:100%" class="ae-stack ae-stack--loose"><div class="ae-card ae-card--publish" style="padding:28px;text-align:center;display:flex;flex-direction:column;gap:10px;align-items:center"><span class="ae-spin" style="width:22px;height:22px;color:var(--ae-ink-2)"></span><div class="ae-h2">Waiting for Claude to publish</div><p class="ae-p">Paste the prompt in the chat where you built Pocket. This page updates on its own when the files arrive.</p><div class="ae-row-gap">{btn("Copy prompt again","secondary",icon="copy")}</div></div>'
    f'<div class="ae-callout ae-callout--info">{i("info")}<span>First time? Claude asks you to connect Aero once. After that it publishes straight away.</span></div></div>'), "sidebar", "home")
upl = app(head("New", ["Home", "New"], "", btn("Cancel", "ghost")) + body(
    f'<div style="max-width:620px;margin:0 auto;width:100%" class="ae-stack"><div class="ae-drop" style="padding:30px">{i("file","ae-i--lg")}<b>pocket.zip · 14 files</b><span>Uploading 9 of 14 files (64%)</span><div class="ae-meter__bar" style="width:240px;height:4px"><i style="width:64%"></i></div></div><div class="ae-field"><span class="ae-field__label">Address</span><div class="ae-affix"><div class="ae-input">pocket</div><span class="ae-affix__end">.aeroapp.ai</span></div></div></div>'), "sidebar", "home")
err = app(head("New", ["Home", "New"], "", btn("Cancel", "ghost")) + body(
    f'<div style="max-width:620px;margin:0 auto;width:100%" class="ae-stack"><div class="ae-callout ae-callout--bad">{i("alert")}<span><b>No index.html at the top of pocket.zip.</b> Aero opens index.html first. Your zip has it inside a folder called pocket-main.</span></div><div class="ae-drop">{i("upload","ae-i--lg")}<b>Drop it again</b><span>Or zip the files inside the folder, not the folder itself.</span></div></div>'), "sidebar", "home")
done = app(head("Pocket is live", ["Home", "New"], "", "", "publish") + body(
    f'<div style="max-width:620px;margin:0 auto;width:100%" class="ae-stack ae-stack--loose"><div class="ae-copy ae-copy--lg"><span class="ae-copy__url">pocket.aeroapp.ai</span>{btn("","ghost",icon="copy",extra="ae-btn--icon")}{btn("Open","secondary",icon="out")}</div>{progress(1)}'
    f'<div class="ae-card" style="padding:18px;display:flex;gap:14px;align-items:center"><span class="ae-source-tile__icon" style="background:var(--ae-test-tint);color:var(--ae-test-ink)">{i("tests")}</span><span style="flex:1"><div class="ae-strong">Now test it</div><div class="ae-small">Add up to a few tasks, or let people explore. You get one link to share.</div></span>{btn("Create a test","primary",True)}</div>'
    f'<div class="ae-small">Free sites stay live 7 days. {"<a class=\"ae-link\">Keep it live from $3</a>"}</div></div>'), "sidebar", "home")
figma = app(head("New", ["Home", "New"], "", btn("Cancel", "ghost")) + body(
    f'<div style="max-width:620px;margin:0 auto;width:100%" class="ae-stack"><div class="ae-field"><span class="ae-field__label">Figma prototype link</span><div class="ae-input">figma.com/proto/Kx82/Pocket?node-id=12</div></div><div class="ae-label" style="margin-top:6px">How to bring it in</div>'
    + "".join(f'<div class="ae-source-tile ae-source-tile--row{" is-active" if k == 0 else ""}"><span class="ae-radio{" is-on" if k == 0 else ""}"></span><span style="flex:1"><span class="ae-source-tile__title">{t}</span><div class="ae-source-tile__sub">{d}</div></span>{g}</div>' for k, (t, d, g) in enumerate([("Embed it", "Live straight away. Flows and transitions work as in Figma.", tag("Instant", "blue")), ("Convert to HTML", "Makes real pages from your frames. Takes a few minutes.", ""), ("Export with a plugin", "Use a Figma plugin, then drop the zip here.", "")]))
    + f'<div class="ae-row-gap" style="justify-content:flex-end">{btn("Publish","primary",True)}</div></div>'), "sidebar", "home")
existing = app(head("Test a site", ["Home", "New"], "", btn("Cancel", "ghost")) + body(
    f'<div style="max-width:620px;margin:0 auto;width:100%" class="ae-stack"><div class="ae-label">Your sites</div>'
    + "".join(f'<div class="ae-source-tile ae-source-tile--row{" is-active" if k == 0 else ""}"><span class="ae-radio{" is-on" if k == 0 else ""}"></span><span style="flex:1;min-width:0"><span class="ae-source-tile__title ae-mono" style="font-size:13px">{s["slug"]}.aeroapp.ai</span><div class="ae-source-tile__sub">v{s["ver"]} · {s["how"]}{" · has a test" if s.get("test") else ""}</div></span>{status("Live","live") if s["status"]=="live" else status(f"{s["days"]} days","soon")}</div>' for k, s in enumerate(S["sites"][:2]))
    + f'<div class="ae-label" style="margin-top:6px">Or any link</div><div class="ae-input is-placeholder">https://… or a Figma prototype link</div><div class="ae-small">The test records the version live today. Later updates don\'t change it until you choose to.</div><div class="ae-row-gap" style="justify-content:flex-end">{btn("Continue","primary",True)}</div></div>'), "sidebar", "home")
out.append(screen(3, "s3", "Create", "Three ways in (Figma link, HTML or zip, one prompt to Claude or ChatGPT), plus \"Test an existing site\". Only save a draft once there is real input.",
    "<b>Pick A.</b> All three ways are visible and equal, the prompt is ready to copy, and the right column answers \"what happens next\". C is the strongest for first-time users arriving from the website (\"One prompt and it's live\"), so it can be the first-run version of the same page.",
    [approach("A", "Three tiles, one page", "From A Studio. Tiles on top, the chosen way opens below, name and address on the right.", create_a, True, "A Studio"),
     approach("B", "One question at a time", "From B Colour's stepper. Calm, but one more click for everyone.", create_b, False, "B Colour"),
     approach("C", "Prompt first", "From D Replay. Leads with the fastest way; Figma and HTML sit below.", create_c, False, "D Replay")],
    state("Waiting for the chat", "updates on its own", wait)
    + state("Figma link pasted", "embed is instant; convert and export also offered", figma)
    + state("Uploading", "real progress from the upload", upl)
    + state("Error", "says what is wrong and how to fix it", err)
    + state("Published", "next step points to Test", done, prop="Now test it")
    + state("Test an existing site", "pick a site or paste any link", existing),
    [("Proposed", ["Draft saved only after the prompt is copied, a link pasted or files dropped (B7).", "\"Now test it\" step after publishing; today the flow ends on the site page.", "Testing any outside link (not only Aero sites) needs checking: today a test points at an Aero site or a Figma link."]),
     ("Copy", ["\"One prompt\" not \"Build with AI\". AI named only on the way in: \"Claude or ChatGPT publishes it for you\".", "Errors name the file and the fix."]),
     ("Engineer check", ["The prompt carries a one-time key tied to this draft; copying it is the moment the draft is saved.", "The waiting page listens for the deploy; closing it is fine, the site still appears under Sites.", "Address is checked as you type; taken names suggest pocket-2."])], n_states=3))

# ================================================================== 04 SITE DETAIL
site_meta = f'<span class="ae-area ae-area--publish">Publish</span>{status("Live","live")}<span>v4 · published 2 hours ago from Claude</span><span style="color:var(--ae-warn)">Offline in 5 days on Free</span>'
site_actions = btn("Open", "secondary", icon="out") + btn("Run a test on this site", "primary", True, icon="tests")
def site_overview():
    return body(f'<div class="ae-body--split" style="display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:24px"><div class="ae-stack ae-stack--loose">'
        f'<div class="ae-copy ae-copy--lg"><span class="ae-copy__url">pocket.aeroapp.ai</span>{btn("Copy","secondary",size="sm",icon="copy")}</div>'
        f'<div class="ae-card" style="overflow:hidden"><div class="ae-site-card__thumb" style="height:230px">{thumb(S["sites"][0]).replace("ae-thumb-phone","ae-thumb-phone\" style=\"transform:scale(1.7);transform-origin:bottom")}</div></div>'
        f'{section("Update it", f"<div class=\"ae-grid ae-grid--2\"><div class=\"ae-drop\" style=\"padding:18px\">{i("upload")}<b>Drop new files</b><span>Publishes as v5</span></div><div class=\"ae-card ae-card--pad ae-stack ae-stack--tight\"><span class=\"ae-strong\">{i("prompt","ae-i--sm")} Update from your chat</span><span class=\"ae-small\">Ask Claude: \"Update Pocket on Aero\". It publishes a new version.</span></div></div>")}</div>'
        f'<div class="ae-stack"><div class="ae-card ae-card--pad ae-stack ae-stack--tight"><div class="ae-label">Free plan</div>{meter(5,7,"days left on Free")}<div class="ae-small">Goes offline on Mon 28 Oct. Your files and versions are kept.</div><a class="ae-link ae-small">Keep it live from $3</a></div>'
        f'<div class="ae-card ae-card--pad ae-stack ae-stack--tight"><div class="ae-label">Test on this site</div><div class="ae-strong">Pocket</div><div class="ae-small">3 sessions · review ready · pinned to v3</div><a class="ae-link ae-small">Open test</a></div>'
        f'<dl class="ae-dl" style="grid-template-columns:90px 1fr"><dt>Made with</dt><dd>One prompt (Claude)</dd><dt>Files</dt><dd>6 · 412 KB</dd><dt>Password</dt><dd>Off</dd></dl></div></div>')
site_a = app(head("Pocket", ["Sites", "Pocket"], site_meta, site_actions, "publish") + tabs(SITE_TABS, "Overview") + site_overview(), "sidebar", "sites")
site_b = app(head("Pocket", ["Sites", "Pocket"], site_meta, site_actions, "publish") + body(
    f'<div class="ae-body--split" style="display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:28px"><div class="ae-stack ae-stack--loose">'
    + section("Address", f'<div class="ae-affix"><div class="ae-input">pocket</div><span class="ae-affix__end">.aeroapp.ai</span></div><div class="ae-row-gap ae-small">{tag("Solo","line")} Use your own domain, like pocket.kestrel.studio</div>')
    + section("Versions", f'<div class="ae-list--card"><div class="ae-list"><div class="ae-version is-live"><span class="ae-version__n">v4</span><span><div class="ae-strong" style="font-size:13px">From Claude</div><div class="ae-small">Today 10:03</div></span>{status("Live","live")}{btn("","ghost",size="sm",icon="more",extra="ae-btn--icon")}</div><div class="ae-version"><span class="ae-version__n">v3</span><span><div class="ae-strong" style="font-size:13px">From Claude</div><div class="ae-small">Yesterday 17:40</div></span><span class="ae-tc">Test pinned here</span>{btn("Roll back","secondary",size="sm",icon="undo")}</div></div></div>')
    + section("Settings", f'<div class="ae-card" style="padding:0 16px"><div class="ae-option"><div class="ae-option__text"><div class="ae-option__title">Password {tag("Basic","line")}</div><div class="ae-option__sub">Viewers enter it once and stay signed in for a week.</div></div><span class="ae-toggle is-disabled"></span></div><div class="ae-option"><div class="ae-option__text"><div class="ae-option__title">Favicon {tag("Basic","line")}</div><div class="ae-option__sub">Shown in the browser tab.</div></div>{btn("Upload","secondary",size="sm",extra="is-disabled")}</div><div class="ae-option"><div class="ae-option__text"><div class="ae-option__title">Aero badge</div><div class="ae-option__sub">A small "Made with Aero" link. Removed on Basic and up.</div></div><span class="ae-toggle is-on is-disabled"></span></div></div>')
    + f'</div><div class="ae-stack"><div class="ae-copy"><span class="ae-copy__url">pocket.aeroapp.ai</span>{btn("Copy","secondary",size="sm",icon="copy")}</div><div class="ae-card" style="overflow:hidden"><div class="ae-site-card__thumb" style="height:160px">{thumb(S["sites"][0])}</div></div><div class="ae-callout ae-callout--warn">{i("clock")}<span><b>Offline in 5 days.</b> Free sites stay live 7 days.</span></div></div></div>'), "sidebar", "sites")

def site_tab(tab, inner, meta=site_meta, banner=""):
    return app(banner + head("Pocket", ["Sites", "Pocket"], meta, site_actions, "publish") + tabs(SITE_TABS, tab) + body(inner), "sidebar", "sites")
vers_tab = site_tab("Versions", f'<div class="ae-list--card"><div class="ae-list">' + "".join(f'<div class="ae-version{" is-live" if n == 4 else ""}"><span class="ae-version__n">v{n}</span><span><div class="ae-strong" style="font-size:13px">{w}</div><div class="ae-small">{d}</div></span>{x}{y}</div>' for n, w, d, x, y in [(4, "Published from Claude", "Today 10:03 · 6 files", status("Live","live"), btn("","ghost",size="sm",icon="more",extra="ae-btn--icon")), (3, "Published from Claude", "Yesterday 17:40 · 6 files", '<span class="ae-tc">Test pinned here</span>', btn("Roll back","secondary",size="sm",icon="undo")), (2, "Uploaded pocket.zip", "Mon 21 Oct · 5 files", '<span></span>', btn("Roll back","secondary",size="sm",icon="undo")), (1, "Uploaded pocket.zip", "Mon 21 Oct · 5 files", '<span></span>', btn("Roll back","secondary",size="sm",icon="undo"))]) + '</div></div><p class="ae-small" style="margin:0">Rolling back makes an old version live again. Nothing is deleted.</p>' + f'<div class="ae-scrim" style="position:absolute"><div class="ae-modal"><div class="ae-modal__head"><span class="ae-h3" style="flex:1">Roll back to v3?</span></div><div class="ae-modal__body"><p class="ae-p">pocket.aeroapp.ai will show v3 straight away. v4 stays in your history, so you can switch back.</p></div><div class="ae-modal__foot">{btn("Cancel","ghost")}{btn("Roll back","primary",True)}</div></div></div>')
settings_tab = site_tab("Settings", f'<div style="max-width:640px" class="ae-stack ae-stack--loose"><div class="ae-field"><span class="ae-field__label">Name</span><div class="ae-input">Pocket</div><span class="ae-field__hint">Only you see this.</span></div><div class="ae-card" style="padding:0 16px"><div class="ae-option"><div class="ae-option__text"><div class="ae-option__title">Password</div><div class="ae-option__sub">Viewers enter it once and stay signed in for a week.</div></div>{tag("Basic","line")}<span class="ae-toggle is-disabled"></span></div><div class="ae-option"><div class="ae-option__text"><div class="ae-option__title">Favicon</div><div class="ae-option__sub">Shown in the browser tab.</div></div>{tag("Basic","line")}</div><div class="ae-option"><div class="ae-option__text"><div class="ae-option__title">Aero badge</div><div class="ae-option__sub">Removed on Basic and up.</div></div>{tag("Basic","line")}</div></div><div class="ae-callout">{i("info")}<span>These come with <b>Basic, $3 a month</b>, with a 7-day free trial.</span><span class="ae-callout__act">{btn("See plans","secondary",size="sm")}</span></div><div class="ae-card ae-card--pad ae-row-gap" style="box-shadow:inset 0 0 0 1px var(--ae-bad-bg)"><span style="flex:1"><div class="ae-strong">Delete this site</div><div class="ae-small">Its versions and history go too. This can\'t be undone.</div></span>{btn("Delete site","secondary")}</div></div>')
offline_meta = f'<span class="ae-area ae-area--publish">Publish</span>{status("Offline, free plan ended","offline")}<span>v12 · last published 9 days ago</span>'
offline = app(head("Studio site", ["Sites", "Studio site"], offline_meta, btn("Put back online","primary",True), "publish") + tabs(SITE_TABS, "Overview") + body(f'<div class="ae-callout ae-callout--warn">{i("clock")}<span><b>kestrel.aeroapp.ai is offline.</b> Free sites stay live 7 days. Visitors see a short "This site is offline" page. Your files and all 12 versions are kept.</span><span class="ae-callout__act">{btn("See plans","secondary",size="sm")}</span></div><div class="ae-card" style="overflow:hidden"><div class="ae-site-card__thumb" style="height:220px;filter:grayscale(1);opacity:.6">{thumb(S["sites"][2])}</div></div>'), "sidebar", "sites")
domain_tab = site_tab("Domain", f'<div style="max-width:640px" class="ae-stack ae-stack--loose"><div class="ae-field"><span class="ae-field__label">Aero address</span><div class="ae-affix"><div class="ae-input">pocket</div><span class="ae-affix__end">.aeroapp.ai</span></div><span class="ae-field__hint">Changing it breaks the old link straight away.</span></div><div class="ae-field"><span class="ae-field__label">Your own domain {tag("Solo","line")}</span><div class="ae-input is-placeholder">pocket.kestrel.studio</div><span class="ae-field__hint">Add one CNAME record at your domain provider. We check it for you.</span></div><div class="ae-list--card"><div class="ae-listhead" style="grid-template-columns:80px 1fr 1fr"><span>Type</span><span>Name</span><span>Value</span></div><div class="ae-test-row" style="grid-template-columns:80px 1fr 1fr;cursor:default"><span class="ae-mono ae-small">CNAME</span><span class="ae-mono ae-small">pocket</span><span class="ae-mono ae-small">cname.vercel-dns.com</span></div></div></div>')
publishing = site_tab("Overview", f'<div class="ae-callout ae-callout--info">{i("refresh")}<span><b>Publishing v5 from Claude.</b> 4 of 6 files. The live site keeps showing v4 until this finishes.</span></div>' + site_overview().replace('<div class="ae-body ">', '<div>'))
out.append(screen(4, "s4", "Site detail", "URL and status (Live, or offline on Free after 7 days with a countdown), versions and roll back, settings (address, password, favicon, badge, domain), and \"Run a test on this site\".",
    "<b>Pick A.</b> Tabs match today's code (Overview, Versions, Settings, Domain, Analytics), so it is a redesign, not a rebuild. The header always shows status and the days left on Free. \"Run a test on this site\" is the one glass button. B is a good single page for phones.",
    [approach("A", "Header and tabs", "From A Studio. Status line under the name, Overview with the address, preview and how to update.", site_a, True, "A Studio", "Countdown"),
     approach("B", "One page", "From C Story. Address, versions and settings in one scroll, preview on the right.", site_b, False, "C Story")],
    state("Versions, rolling back", "confirm in a modal, nothing deleted", vers_tab)
    + state("Settings on Free", "paid features shown with the plan they need", settings_tab)
    + state("Offline", "free plan ended, files kept", offline, prop="Offline state")
    + state("Domain", "Solo and up", domain_tab)
    + state("Publishing a new version", "the live site stays on v4", publishing),
    [("Proposed", ["Expiry state and countdown on Free (B13): status line, Overview card, site cards, Home feed.", "\"Run a test on this site\" (today only the other way round).", "Rename the Figma \"Prototype\" tab to \"Source\"."]),
     ("Copy", ["\"Offline in 5 days on Free\", never \"expires\". \"Keep it live from $3\".", "Gated settings name the plan: \"Basic\", \"Solo\"."]),
     ("Engineer check", ["Days left come from the site's publish date and plan; same number on every surface.", "Roll back reuses the version pointer; tests stay pinned to their own version.", "Skeleton header while the site loads, not null (AeroSiteDetail B1)."])], n_states=3))

# ================================================================== 05 TEST SETUP
setup_left = (section("What testers try", f'<div class="ae-stack ae-stack--tight">' + "".join(f'<div class="ae-task"><span class="ae-task__n">{k+1}</span><span class="ae-task__text">{t}</span>{i("grip","ae-task__grip")}</div>' for k, t in enumerate(S["tasks"])) + f'<button class="ae-task ae-task--add">{i("plus","ae-i--sm")}<span style="text-align:left">Add a task</span></button></div><span class="ae-small">Optional. With no tasks, testers explore freely.</span>', '<span class="ae-seg"><span class="ae-seg__opt is-active">Tasks</span><span class="ae-seg__opt">Explore freely</span></span>')
              + section("Messages", f'<div class="ae-field"><span class="ae-field__label">Welcome</span><div class="ae-textarea" style="min-height:60px">Thanks for helping with Pocket. Try the two tasks and say what you think as you go.</div></div><div class="ae-field"><span class="ae-field__label">Thank you</span><div class="ae-textarea" style="min-height:44px">Thanks, that really helps.</div></div>')
              + section("What is recorded", f'<div class="ae-card" style="padding:0 16px"><div class="ae-option"><div class="ae-option__text"><div class="ae-option__title">Screen</div><div class="ae-option__sub">Testers pick the tab to share. Laptop and desktop only.</div></div><span class="ae-toggle is-on"></span></div><div class="ae-option"><div class="ae-option__text"><div class="ae-option__title">Voice</div><div class="ae-option__sub">Needed for the transcript, summary and friction points.</div></div><span class="ae-toggle is-on"></span></div><div class="ae-option"><div class="ae-option__text"><div class="ae-option__title">Ask how hard each task was</div><div class="ae-option__sub">A quick rating after each task.</div></div><span class="ae-toggle"></span></div></div>'))
preview = (f'<div class="ae-stack"><div class="ae-row-gap"><span class="ae-label">What testers see</span><span class="ae-spacer"></span>{proposed()}</div><div class="ae-card" style="overflow:hidden"><div style="padding:18px;background:var(--ae-mist);display:flex;flex-direction:column;gap:10px">'
           f'<div class="ae-small">Mia from Kestrel Studio asked you to try</div><div class="ae-h3" style="font-size:17px;font-weight:450">Pocket</div><p class="ae-small" style="margin:0;color:var(--ae-ink-2)">Thanks for helping with Pocket. Try the two tasks and say what you think as you go.</p>'
           f'<div class="ae-stack ae-stack--tight ae-small"><span>{i("monitor","ae-i--sm")} Your screen, the tab you choose</span><span>{i("mic","ae-i--sm")} Your voice</span><span>{i("x","ae-i--sm")} You can stop at any time</span></div>{btn("Start","primary",size="sm")}</div></div>'
           f'<div class="ae-small">Pinned to v3 of pocket.aeroapp.ai. {"<a class=\"ae-link\">Use v4</a>"}</div></div>')
setup_a = app(test_head("Setup", 3, btn("Open as a tester", "secondary", icon="out") + btn("Save", "primary", True)) + body(f'<div style="display:grid;grid-template-columns:minmax(0,1fr) 280px;gap:28px"><div class="ae-stack ae-stack--loose">{setup_left}</div>{preview}</div>'), "sidebar", "tests")
def story_card(n, title, inner, active=False):
    return f'<div class="ae-card{" ae-card--raised" if active else ""}" style="padding:14px;display:flex;flex-direction:column;gap:10px;min-height:250px;{"box-shadow:inset 0 0 0 1.5px var(--ae-ink),var(--ae-sh-2)" if active else ""}"><div class="ae-row-gap"><span class="ae-stepper__n" style="width:20px;height:20px">{n}</span><span class="ae-strong" style="font-size:13px">{title}</span></div>{inner}</div>'
setup_b = app(test_head("Setup", 3, btn("Open as a tester", "secondary", icon="out") + btn("Save", "primary", True)) + body(
    f'<p class="ae-p">What testers see, in order. Edit any step.</p><div class="ae-grid ae-grid--4" style="align-items:stretch">'
    + story_card(1, "Welcome", f'<div class="ae-textarea" style="min-height:96px;font-size:13px">Thanks for helping with Pocket. Try the two tasks and say what you think as you go.</div><span class="ae-small">Shows your name and studio.</span>')
    + story_card(2, "Recording", f'<div class="ae-stack ae-stack--tight"><div class="ae-row-gap ae-small"><span class="ae-toggle is-on"></span>Screen</div><div class="ae-row-gap ae-small"><span class="ae-toggle is-on"></span>Voice</div></div><span class="ae-small">Testers allow both in one step and pick the tab to share.</span>')
    + story_card(3, "Tasks", f'<div class="ae-stack ae-stack--tight">' + "".join(f'<div class="ae-task" style="padding:6px 8px"><span class="ae-task__n">{k+1}</span><span class="ae-task__text" style="font-size:13px">{t}</span></div>' for k, t in enumerate(S["tasks"])) + f'<button class="ae-task ae-task--add" style="padding:6px 8px">{i("plus","ae-i--sm")}<span style="text-align:left;font-size:13px">Add</span></button></div>', True)
    + story_card(4, "Thank you", '<div class="ae-textarea" style="min-height:70px;font-size:13px">Thanks, that really helps.</div><span class="ae-small">Then they can close the tab.</span>')
    + '</div>'), "sidebar", "tests")
no_tasks = app(test_head("Setup", 1, btn("Open as a tester", "secondary", icon="out") + btn("Save", "primary", True), name="Onboarding v2", url="onboarding.aeroapp.ai", tasks="Explore freely") + body(f'<div style="display:grid;grid-template-columns:minmax(0,1fr) 280px;gap:28px"><div class="ae-stack ae-stack--loose">'
    + section("What testers try", f'<div class="ae-empty ae-empty--line" style="padding:22px;align-items:flex-start;text-align:left"><div class="ae-strong">Explore freely</div><div class="ae-small">Testers get one prompt: "Look around and say what you think, as if you found this yourself." They decide when they are done.</div></div>', '<span class="ae-seg"><span class="ae-seg__opt">Tasks</span><span class="ae-seg__opt is-active">Explore freely</span></span>')
    + section("Messages", f'<div class="ae-field"><span class="ae-field__label">Welcome</span><div class="ae-textarea" style="min-height:60px">Have a look around Onboarding v2 and talk through what you notice.</div></div>')
    + f'</div>{preview.replace("Thanks for helping with Pocket. Try the two tasks and say what you think as you go.", "Have a look around Onboarding v2 and talk through what you notice.").replace(">Pocket<", ">Onboarding v2<").replace("Pinned to v3 of pocket.aeroapp.ai.", "Pinned to v2 of onboarding.aeroapp.ai.").replace("Use v4", "")}</div>'), "sidebar", "tests")
edit_live = app(test_head("Setup", 3, btn("Save", "primary", True)) + body(f'<div class="ae-callout ae-callout--warn">{i("alert")}<span><b>3 people have already taken this test.</b> Changing tasks now means later sessions won\'t match earlier ones. For a big change, make a new test.</span><span class="ae-callout__act">{btn("Duplicate test","secondary",size="sm")}</span></div><div style="max-width:640px" class="ae-stack ae-stack--loose">{setup_left}</div>'), "sidebar", "tests")
pinned = app(test_head("Setup", 3, btn("Save", "primary", True)) + body(f'<div class="ae-callout ae-callout--info">{i("layers")}<span><b>pocket.aeroapp.ai has a newer version (v4).</b> This test records v3, so sessions stay comparable. New sessions can record v4 instead.</span><span class="ae-callout__act ae-row-gap">{btn("Keep v3","ghost",size="sm")}{btn("Use v4","secondary",size="sm")}</span></div><div style="max-width:640px" class="ae-stack ae-stack--loose">{setup_left}</div>'), "sidebar", "tests")
out.append(screen(5, "s5", "Test setup", "Tasks (optional), welcome and thank-you messages, what testers will be asked for. Variation: no tasks (\"Explore freely\").",
    "<b>Pick A.</b> Same fields as today (tasks, welcome, thank you, screen, voice, difficulty rating, pinned version) in plain words, with a preview of the tester's first screen beside it. B's storyboard is clearer about order but cramped for longer tasks.",
    [approach("A", "Form with a tester preview", "From A Studio's create panel. Tasks first, messages, then what is recorded. Preview on the right.", setup_a, True, "A Studio", "Preview"),
     approach("B", "Storyboard", "From D's sequence. The four steps a tester sees, left to right, each editable.", setup_b, False, "D Replay")],
    state("No tasks: explore freely", "the tester gets one open prompt", no_tasks)
    + state("Editing after sessions", "warns, offers a copy", edit_live, prop="Duplicate test")
    + state("Newer version available", "today's pinned version update, in plain words", pinned),
    [("Proposed", ["Tester preview panel.", "\"Duplicate test\".", "Session target is removed from Setup: the plan limit already sets it (B14)."]),
     ("Copy", ["\"What testers try\", not \"Goals\". \"Ask how hard each task was\", not \"Difficulty rating\".", "Explore freely prompt is fixed and shown, so the owner knows what testers read."]),
     ("Engineer check", ["Explore freely = zero tasks; the tester sees no \"0 tasks\" line (B15).", "Voice off disables transcript, summary and review; say so next to the toggle.", "Changing tasks after sessions keeps old sessions' task list on each session."])], n_states=3))

# ================================================================== 06 SHARE
recorded = f'<div class="ae-stack ae-stack--tight ae-small"><span>{i("monitor","ae-i--sm")} Their screen, only the tab they choose</span><span>{i("mic","ae-i--sm")} Their voice, for the transcript</span><span>{i("x","ae-i--sm")} No camera, no mouse movements. They can stop at any time.</span></div>'
share_a = app(test_head("Share", 3, btn("", "ghost", icon="more", extra="ae-btn--icon"), meta_extra="") + body(
    f'<div class="ae-card ae-card--test" style="padding:26px;display:grid;grid-template-columns:minmax(0,1fr) auto;gap:28px;align-items:center"><div class="ae-stack"><div class="ae-h2" style="font-weight:350;font-size:24px">Your test link is ready<span style="color:var(--ae-blue)">.</span></div>'
    f'<div class="ae-copy ae-copy--lg" style="background:rgba(255,255,255,.75)"><span class="ae-copy__url">pocket.aeroapp.ai/t/8kq2</span>{btn("Copy link","primary",True,icon="copy")}</div>'
    f'<div class="ae-row-gap">{btn("Open as a tester","secondary",True,icon="out")}<span class="ae-small">Send it to 3 to 5 people. They open it in their browser, nothing to install.</span></div></div><div class="ae-stack ae-stack--tight" style="align-items:center">{qr()}<span class="ae-small">For phones</span></div></div>'
    f'<div class="ae-grid ae-grid--3"><div class="ae-card ae-card--pad ae-stack ae-stack--tight"><div class="ae-label">What is recorded</div>{recorded}</div>'
    f'<div class="ae-card ae-card--pad ae-stack ae-stack--tight"><div class="ae-label">On a phone</div><div class="ae-small">Figma prototypes record voice only. HTML sites ask testers to switch to a laptop.</div></div>'
    f'<div class="ae-card ae-card--pad ae-stack ae-stack--tight"><div class="ae-label">After each session</div><div class="ae-small">It appears under Sessions. The transcript follows about a minute later.</div></div></div>'
    f'<div class="ae-row-gap"><span class="ae-strong" style="font-size:13px">Link status</span><span class="ae-toggle is-on"></span><span class="ae-small">Open. Turn off to stop new sessions.</span></div>'), "sidebar", "tests")
msg = "Hi, could you try a prototype for me? It takes a few minutes. Open the link on a laptop, allow screen and mic, and talk through what you think: pocket.aeroapp.ai/t/8kq2"
share_b = app(test_head("Share", 3, btn("", "ghost", icon="more", extra="ae-btn--icon")) + body(
    f'<div style="max-width:680px" class="ae-stack ae-stack--loose"><div class="ae-copy ae-copy--lg"><span class="ae-copy__url">pocket.aeroapp.ai/t/8kq2</span>{btn("","ghost",icon="qr",extra="ae-btn--icon")}{btn("Copy link","primary",True,icon="copy")}</div>'
    f'<div class="ae-stack"><div class="ae-label">A message you can send</div><div class="ae-card ae-card--mist" style="padding:14px 16px;font-size:14px;color:var(--ae-ink-2);line-height:1.55">{msg}</div><div class="ae-row-gap">{btn("Copy message","secondary",icon="copy")}{btn("Open as a tester","ghost",icon="out")}</div></div>'
    f'<div class="ae-guide"><div class="ae-guide__head">{i("book")}What happens next</div><ol><li>They open the link, allow their mic and pick the tab to share.</li><li>They try your 2 tasks and talk as they go. There is no time limit.</li><li>The session appears under Sessions. The transcript, summary and friction points follow about a minute later.</li></ol></div></div>'), "sidebar", "tests")
toast = '<div style="position:absolute;left:50%;bottom:24px;transform:translateX(-50%);z-index:90"><span class="ae-toast">' + i("check") + 'Test created. Link copied.</span></div>'
just = app(test_head("Share", 0, btn("", "ghost", icon="more", extra="ae-btn--icon"), name="Checkout", url="checkout.aeroapp.ai", tasks="3 tasks", st=status("Waiting for testers", "draft")) + body(share_a.split('<div class="ae-body ">', 1)[1].rsplit('</div></main>', 1)[0] if False else f'<div class="ae-card ae-card--test" style="padding:26px" ><div class="ae-stack"><div class="ae-h2" style="font-weight:350;font-size:24px">Your test link is ready<span style="color:var(--ae-blue)">.</span></div><div class="ae-copy ae-copy--lg" style="background:rgba(255,255,255,.75)"><span class="ae-copy__url">checkout.aeroapp.ai/t/3fz7</span>{btn("Copied","primary",extra="is-done",icon="check")}</div><span class="ae-small">You landed here after creating the test, with the link already copied.</span></div></div>'), "sidebar", "tests", overlay=toast)
full = app(test_head("Share", 3, btn("", "ghost", icon="more", extra="ae-btn--icon")) + body(f'<div class="ae-callout ae-callout--warn">{i("alert")}<span><b>3 of 3 sessions kept on Free.</b> New testers can still take the test, but their sessions won\'t be kept until you delete one or upgrade.</span><span class="ae-callout__act">{btn("See plans","secondary",size="sm")}</span></div><div class="ae-copy ae-copy--lg"><span class="ae-copy__url">pocket.aeroapp.ai/t/8kq2</span>{btn("Copy link","primary",True,icon="copy")}</div>'), "sidebar", "tests")
closed = app(test_head("Share", 3, btn("", "ghost", icon="more", extra="ae-btn--icon")) + body(f'<div class="ae-copy ae-copy--lg" style="opacity:.6"><span class="ae-copy__url">pocket.aeroapp.ai/t/8kq2</span>{btn("Copy link","secondary",icon="copy")}</div><div class="ae-row-gap"><span class="ae-strong" style="font-size:13px">Link status</span><span class="ae-toggle"></span><span class="ae-small">Closed. People who open it see "This test has closed. Thanks for your interest."</span></div>'), "sidebar", "tests")
out.append(screen(6, "s6", "Share", "One link, copy, QR code, \"Open as a tester\" preview, a plain line on what is recorded. After creating a test, land here with the link ready.",
    "<b>Pick A</b>, with B's \"message you can send\" below it. One link only (today the header and the Share tab show two different-looking URLs). The test wash makes the glass buttons pick up a little colour.",
    [approach("A", "The link, large", "From A Studio and B Colour. Link and QR on the Test wash, then three plain facts.", share_a, True, "A + B", "QR"),
     approach("B", "Link and a message", "From C Story. A ready message to paste into email or chat, and what happens next.", share_b, False, "C Story")],
    state("Just created", "lands here, link already copied", just, prop="Land on Share")
    + state("Sessions limit reached", "be plain about what happens", full, prop="Limit copy")
    + state("Link closed", "today's Status, in words", closed)
    + state("Phone", "390", phone(test_head("Share", 3, "") + body(f'<div class="ae-copy ae-copy--lg"><span class="ae-copy__url">pocket.aeroapp.ai/t/8kq2</span></div>{btn("Copy link","primary",True,icon="copy",extra="ae-btn--block")}{btn("Share","secondary",icon="out",extra="ae-btn--block")}<div class="ae-card ae-card--pad">{recorded}</div>'), "Pocket", "tests", True), 390, 760, fixed=True),
    [("Proposed", ["Land on Share after creating a test, link copied (today: Setup).", "QR code and \"Open as a tester\" (preview without saving a session).", "What happens to sessions over the Free limit needs a decision: block, or record and hide."]),
     ("Copy", ["\"Send it to 3 to 5 people\" is advice, not a limit.", "\"No camera, no mouse movements\" is true and reassuring.", "No \"About N minutes\": sessions have no set length."]),
     ("Engineer check", ["One canonical link format everywhere (B: header vs Share mismatch).", "\"Open as a tester\" must not count as a session or use the allowance.", "Header \"Export\" removed; it only copied the link (B10)."])], n_states=4))

# ================================================================== 07 SESSIONS LIST
sess_a = app(test_head("Sessions", 5, btn("Copy link", "secondary", icon="copy")) + body(
    f'<div class="ae-row-gap"><span class="ae-seg"><span class="ae-seg__opt is-active">All 5</span><span class="ae-seg__opt">Ready 2</span><span class="ae-seg__opt">With friction 2</span></span><span class="ae-spacer"></span>{meter(3,3,"sessions kept",full=True).replace("ae-meter ","ae-meter ae-hide-m ")}</div>'
    + sessions_list(list(reversed(S["sessions"] + MORE_S))) + f'<p class="ae-small" style="margin:0">Numbered in the order they happened. Session 1 is the first.</p>'), "sidebar", "tests")
def scard(s):
    q = f'<p class="ae-quote" style="font-size:16px">“{E(s["quote"])}”</p>' if s["quote"] else f'<p class="ae-small" style="margin:0">{ {"processing":"Transcript arriving, usually about a minute.","recording":"Recording now. The tester is still going.","noaudio":"Screen only. The tester turned off their mic."}[s["status"]] }</p>'
    st = {"ready": status("Ready","ready"), "processing": status("Transcript arriving","processing"), "recording": status("Recording now","recording"), "noaudio": status("No audio","noaudio")}[s["status"]]
    return f'<div class="ae-card" style="padding:16px;display:flex;flex-direction:column;gap:10px"><div class="ae-row-gap">{avatar(s["who"][-1], s["av"])}<span class="ae-strong" style="font-size:13px">Session {s["n"]} · {s["who"]}</span><span class="ae-spacer"></span><span class="ae-tc">{s["len"]}</span></div>{q}<div class="ae-row-gap ae-small">{st}<span class="ae-sep"></span>{s["dev"]}{(" · " + str(s.get("fr", 0)) + " friction points") if s.get("fr") else ""}</div></div>'
sess_b = app(test_head("Sessions", 5, btn("Copy link", "secondary", icon="copy")) + body(f'<div class="ae-grid ae-grid--3">{"".join(scard(s) for s in reversed(S["sessions"] + MORE_S))}</div>'), "sidebar", "tests")
empty_s = app(test_head("Sessions", 0, btn("Copy link", "secondary", icon="copy"), name="Checkout", url="checkout.aeroapp.ai", tasks="3 tasks", st=status("Waiting for testers", "draft")) + body(f'<div class="ae-empty" style="background:var(--ae-test-wash)"><div class="ae-empty__title">No sessions yet</div><div class="ae-empty__text">Share your link. Sessions appear here as testers finish, and the transcript follows about a minute later.</div><div class="ae-empty__actions">{btn("Copy link","primary",True,icon="copy")}{btn("Open as a tester","secondary",icon="out")}</div></div>'), "sidebar", "tests")
load_s = app(head("Pocket", ["Tests", "Pocket"], f'<span class="ae-area ae-area--test">Test</span><span class="ae-skel ae-skel--text" style="width:120px"></span>', btn("Copy link", "secondary", icon="copy"), "test") + tabs([("Setup", ""), ("Share", ""), ("Sessions", ' <span class="ae-skel" style="width:12px;height:10px;display:inline-block"></span>'), ("Review", "")], "Sessions") + body(skel_rows(4, "76px 1.3fr 2.4fr 160px")), "sidebar", "tests")
out.append(screen(7, "s7", "Sessions list", "Consistent numbering (oldest is 1), and status: recording, processing (\"Transcript arriving, usually about a minute\"), ready, no audio.",
    "<b>Pick A.</b> A table scans fastest once there are more than a few sessions, and the first line in their words helps you choose which to open. B's cards suit the first two or three sessions and the marketing kit.",
    [approach("A", "Table", "From A Studio. Number, tester, first line in their words, length, one status.", sess_a, True, "A Studio"),
     approach("B", "Cards with a quote", "From C Story. Each session led by its strongest line.", sess_b, False, "C Story")],
    state("Empty", "teaches what happens next", empty_s)
    + state("Loading", "no false zero in the tab or the list (B2)", load_s)
    + state("Phone", "390, rows stack", phone(test_head("Sessions", 5, "") + body(sessions_list(list(reversed(S["sessions"] + MORE_S)))), "Pocket", "tests", True), 390, 800, fixed=True),
    [("Proposed", ["Stable session numbers stored at start, oldest is 1 (B11).", "\"No audio\" status when the mic was denied or off (B16).", "Filters: Ready, With friction."]),
     ("Copy", ["\"Tester B\" when no name was given, the same in the row and the session page.", "\"Ended early\" for an abandoned tab, with when it closed."]),
     ("Engineer check", ["Status order: Recording now, Transcript arriving, Ready, No audio, Ended early. One per row.", "Recording now comes from the live session doc; it flips without a refresh."])], n_states=3))

# ================================================================== 08 SESSION VIEW
sess_meta = f'{status("Ready","ready")}<span>Tester B · Laptop · Chrome</span><span class="ae-tc">07:12</span><span>Sunday 11:40</span><span>2 tasks</span>'
sess_actions = btn("", "ghost", icon="left", extra="ae-btn--icon") + btn("", "ghost", icon="right", extra="ae-btn--icon") + btn("", "ghost", icon="more", extra="ae-btn--icon")
def fr_jump(f, k, active=False):
    t = {"03:08": 188000, "02:41": 161000, "03:02": 182000}[f["t"]]
    return friction(f, active).replace('class="ae-friction', f'data-jump="{t}" class="ae-friction', 1)
right_col = (f'<div class="ae-stack ae-stack--loose"><div class="ae-stack ae-stack--tight"><div class="ae-label">Summary</div><p style="margin:0;font-size:14.5px;line-height:1.6;color:var(--ae-ink)">Sent money without help. Expected cards on the home screen and found them under More after about 20 seconds. Unsure how to leave the Send flow.</p></div>'
             f'<div class="ae-stack ae-stack--tight"><div class="ae-label">What to fix first</div>{prio_list(PRIOS)}</div>'
             f'<div class="ae-stack ae-stack--tight"><div class="ae-label">Friction points · in their own words</div>{"".join(fr_jump(f, k, k == 0) for k, f in enumerate(FRICTION))}</div>{source_line()}</div>')

CURSOR_SVG = '<svg class="ae-cursor" viewBox="0 0 24 24" style="left:{x}%;top:{y}%"><path d="M4 2l15 11-6.5 1.2L16 21l-3 1.3-3.4-6.8L4 20z" fill="#1D1D1F" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"/></svg>'
def player_cursor():
    stage_extra = (CURSOR_SVG.format(x=56.5, y=50) + '<span class="ae-ripple" style="left:55.5%;top:48.5%"></span>'
                   + '<span class="ae-ripple ae-ripple--miss" style="left:45%;top:37%"></span>')
    p = player(0.435, stage_extra=stage_extra)
    clicks = "".join(f'<span class="ae-scrub__click" style="left:{t/432*100:.1f}%"></span>' for t in (20, 41, 66, 75, 150, 160, 205, 214, 250))
    misses = "".join(f'<span class="ae-scrub__miss" style="left:{t/432*100:.1f}%" title="Click on nothing"></span>' for t in (176, 183, 186))
    p = p.replace('<span class="ae-scrub__head"', clicks + misses + '<span class="ae-scrub__head"', 1)
    return p
clickpath = (f'<div class="ae-card ae-card--pad ae-stack ae-stack--tight" style="padding:12px 14px"><div class="ae-row-gap"><span class="ae-label">Click path · Task 2</span><span class="ae-spacer"></span><span class="ae-small">HTML: Aero’s overlay · Figma: Embed API</span></div>'
             f'<div class="ae-clickpath"><span class="ae-clickpath__screen">Home</span><span class="ae-clickpath__miss">3 misclicks on Balance</span>{i("right","ae-i--sm")}<span class="ae-clickpath__screen">More</span>{i("right","ae-i--sm")}<span class="ae-clickpath__screen is-now">Cards</span><span class="ae-tc" style="margin-left:auto">03:02 to 03:31</span></div></div>')
cursor_right = (f'<div class="ae-stack ae-stack--loose"><div class="ae-stack ae-stack--tight"><div class="ae-label">What the clicks add</div>'
                f'<div class="ae-friction is-active"><div class="ae-friction__top"><span class="ae-friction__title">Balance looks tappable</span><span class="ae-tc">03:02</span></div><p class="ae-friction__quote">Is the balance a button? I keep wanting to tap it.</p>'
                f'<div class="ae-friction__foot"><span class="ae-clickpath__miss">3 clicks on nothing</span><span class="ae-sep"></span><span>Tester B</span><span class="ae-spacer"></span><span class="ae-link">{i("play","ae-i--sm")} Play moment</span></div></div>'
                f'{friction(FRICTION[0])}</div><div class="ae-small">Blue rings are clicks, red rings are clicks that hit nothing. On the timeline, dots are clicks and red rings are misclicks.</div>'
                f'<div class="ae-source">{i("info")}<span>HTML sites on Aero: the cursor and clicks come from Aero\'s overlay in the tested page, lined up with the recording. Figma: clicks and screen changes from Figma\'s Embed API, no movement. Today neither is recorded.</span></div></div>')
sess_a = app(head("Session 2 · Tester B", ["Tests", "Pocket", "Sessions", "Session 2"], sess_meta, sess_actions) + body(
    f'<div style="display:grid;grid-template-columns:minmax(0,1fr) 330px;gap:28px;align-items:start"><div class="ae-stack ae-stack--loose">{player(0.435)}<div class="ae-stack ae-stack--tight"><div class="ae-row-gap"><span class="ae-label">Transcript</span><span class="ae-spacer"></span><span class="ae-small">Click a line to jump · press play to follow along</span></div>{transcript(5, start=3)}</div></div>{right_col}</div>'), "sidebar", "tests")
article = (f'<div class="ae-stack ae-stack--loose" style="max-width:640px"><div><span class="ae-tag ae-tag--blue">Pocket · Session 2</span></div><p class="ae-quote" style="font-size:30px;line-height:1.25">“I thought my cards would be on the home screen. <mark>Is it under More?</mark>”</p>'
           f'<div class="ae-small">Tester B · Sunday, 11:40 · 07:12 · Send £20 to Sam, Find your cards</div><div class="ae-stack ae-stack--tight" style="border-left:2px solid var(--ae-mark);padding-left:14px"><div class="ae-label">Summary</div><p style="margin:0;font-size:15px;line-height:1.6;color:var(--ae-ink)">Sent money without help. Expected cards on the home screen and found them under More. Unsure how to leave the Send flow.</p></div>{transcript(5, read=True, start=2)}</div>')
dock = (f'<div class="ae-stack" style="position:sticky;top:0">{player(0.435, chips=False, tall=True)}<div class="ae-label">Friction points</div>{"".join(fr_jump(f, k, k == 0) for k, f in enumerate(FRICTION))}{source_line()}</div>')
sess_d = app(head("Session 2 · Tester B", ["Tests", "Pocket", "Sessions", "Session 2"], sess_meta, sess_actions) + body(
    f'<div style="display:grid;grid-template-columns:minmax(0,1fr) 330px;gap:28px;align-items:start"><div class="ae-stack">{player_cursor()}{clickpath}<div class="ae-stack ae-stack--tight"><div class="ae-label">Transcript</div>{transcript(5, start=4)}</div></div>{cursor_right}</div>'), "sidebar", "tests")
sess_b = app(head("Session 2", ["Tests", "Pocket", "Sessions", "Session 2"], "", sess_actions) + body(f'<div style="display:grid;grid-template-columns:minmax(0,1fr) 340px;gap:40px;align-items:start">{article}{dock}</div>'), "sidebar", "tests")
theatre_right = (f'<div style="border-left:1px solid var(--ae-line);display:flex;flex-direction:column;min-height:0;background:var(--ae-paper)">{tabs([("Summary",""),("Transcript",""),("Friction"," <span class=\"ae-tab__n\">3</span>")], "Transcript", inner=True).replace("ae-tabs ae-tabs--inner", "ae-tabs ae-tabs--inner\" style=\"padding:0 16px")}<div style="padding:12px;overflow:hidden">{transcript(5, start=3)}</div></div>')
sess_c = app(head("Session 2 · Tester B", ["Tests", "Pocket", "Sessions", "Session 2"], sess_meta, sess_actions)
             + f'<div style="display:grid;grid-template-columns:minmax(0,1fr) 380px;flex:1;min-height:0;border-top:1px solid var(--ae-line)"><div style="padding:20px;background:var(--ae-mist);display:flex;flex-direction:column;gap:12px">{player(0.435, floating=True)}<div class="ae-card ae-card--pad" style="padding:14px 16px">{progress(3).replace("Publish","Task 1").replace("Test","Task 2").replace("Review","Done")}</div></div>{theatre_right}</div>', "rail", "tests", extra_cols=ctx)
proc = app(head("Session 3 · Tester C", ["Tests", "Pocket", "Sessions", "Session 3"], f'{status("Transcript arriving","processing")}<span>Tester C · Phone · voice only</span><span class="ae-tc">04:55</span>', sess_actions) + body(
    f'<div style="display:grid;grid-template-columns:minmax(0,1fr) 330px;gap:28px;align-items:start"><div class="ae-stack ae-stack--loose"><div class="ae-player ae-player--voice"><div class="ae-player__stage"><div class="ae-wave">{"".join(f"<i style=\"height:{8+abs(((k*37)%29)-14)*2.4:.0f}px\"></i>" for k in range(64))}</div><div class="ae-player__chips"><span class="ae-player__chip">{i("phone","ae-i--sm")}Phone · voice only</span></div></div><div class="ae-player__bar"><button class="ae-play">{i("play")}</button><span class="ae-player__time"><b>00:00</b> / 04:55</span>{scrub(0,(),295,())}</div></div>'
    f'<div class="ae-stack"><div class="ae-row-gap"><span class="ae-label">Transcript</span></div><div class="ae-callout ae-callout--info">{i("clock")}<span><b>Transcript arriving, usually about a minute.</b> You can listen now. This page fills in on its own.</span></div>{"".join("<span class=\"ae-skel ae-skel--text\" style=\"width:" + str(w) + "%\"></span>" for w in (92, 80, 86, 60))}</div></div>'
    f'<div class="ae-stack"><div class="ae-label">Summary</div><span class="ae-skel ae-skel--text"></span><span class="ae-skel ae-skel--text" style="width:80%"></span><div class="ae-label" style="margin-top:8px">Friction points</div><span class="ae-skel" style="height:70px;border-radius:9px"></span><span class="ae-skel" style="height:70px;border-radius:9px"></span></div></div>'), "sidebar", "tests")
noaudio = app(head("Session 5 · Tester E", ["Tests", "Pocket", "Sessions", "Session 5"], f'{status("No audio","noaudio")}<span>Laptop · Chrome</span><span class="ae-tc">03:31</span>', sess_actions) + body(
    f'<div style="display:grid;grid-template-columns:minmax(0,1fr) 330px;gap:28px;align-items:start">{player(0.2, cur="00:42").replace("Screen and voice","Screen only")}<div class="ae-stack"><div class="ae-callout ae-callout--warn">{i("micoff")}<span><b>No audio in this session.</b> Tester E turned off their mic, so there is no transcript, summary or friction points. You can still watch the screen.</span></div><div class="ae-guide"><div class="ae-guide__head">{i("book")}Why it matters</div><span>The review is written from what testers say. Ask people to keep their mic on; the test asks them once, kindly.</span></div></div></div>'), "sidebar", "tests")
failed = app(head("Session 2 · Tester B", ["Tests", "Pocket", "Sessions", "Session 2"], sess_meta, sess_actions) + body(
    f'<div style="display:grid;grid-template-columns:minmax(0,1fr) 330px;gap:28px;align-items:start"><div class="ae-stack">{player(0.1, cur="00:42")}<div class="ae-callout ae-callout--bad">{i("alert")}<span><b>The transcript didn\'t finish.</b> The transcription service timed out. The recording is safe.</span><span class="ae-callout__act">{btn("Try again","secondary",size="sm")}</span></div></div><div class="ae-stack"><div class="ae-label">Summary</div><p class="ae-small" style="margin:0">Waits for the transcript.</p></div></div>'), "sidebar", "tests")
sess_phone = phone(head("Session 2", None, f'{status("Ready","ready")}<span class="ae-tc">07:12</span>', "") + body(player(0.435, chips=False) + f'<div class="ae-stack ae-stack--tight"><div class="ae-label">Summary</div><p style="margin:0;font-size:14.5px;line-height:1.55;color:var(--ae-ink)">Sent money without help. Expected cards on the home screen and found them under More.</p></div>{friction(FRICTION[0], True)}<div class="ae-label">Transcript</div>{transcript(5, upto=7)}'), "Tester B", "tests", True)
out.append(screen(8, "s8", "Session view (Review)", "The recording at the top, inline. The transcript with word-by-word highlight as the audio plays; click a line to jump. Summary, priorities and friction points quoted in their words, each jumping to its moment. No moving cursor today.",
    "<b>Pick A, with B's calm reading type.</b> A keeps the recording first (watching is the core value) with everything that came out of it beside it. B is the calmest for reading (Duane liked C's \"11:40\" view): offer it as a \"Read\" view toggle. C works best for long sessions and moving between testers. Press play on any of them: words follow the audio. <b>D</b> is A once clicks are recorded (see the cursor research): proposed, shown beside today's true version.",
    [approach("A", "Recording first, findings beside", "From A Studio. True to the app: the recording has no cursor. Transcript under it follows the audio word by word; summary and friction points on the right.", sess_a, True, "A Studio", "Inline player", demo=True),
     approach("D", "A, plus the cursor and clicks", "The same page once Aero records clicks: a cursor and click ripples over HTML replays, misclick markers and a click path (Figma: Home → More → Cards) on the timeline.", sess_d, False, "Cursor research", "Proposed: cursor and clicks", demo=True),
     approach("B", "Read like an article", "From C Story. Their words as the headline, transcript as the page, recording docked.", sess_b, False, "C Story", "Inline player", demo=True),
     approach("C", "Theatre", "From D Replay. Large recording, tabs on the right, sessions in a column on the left.", sess_c, False, "D Replay", "Inline player", demo=True)],
    state("Processing", "listen now, transcript about a minute later", proc)
    + state("No audio", "honest about what is missing", noaudio, prop="No audio")
    + state("Transcript failed", "what happened, what is safe, try again", failed)
    + state("Phone", "390", sess_phone, 390, 860, fixed=True),
    [("Proposed", ["Inline player on the session page (today a separate route outside the shell).", "Word-by-word highlight using the stored word timings (AssemblyAI returns them; they are saved on the session).", "Friction points and priorities jump to their moment: needs a time per item, matched from the quote.", "D: cursor and click ripples for HTML sites (overlay track saved as one JSON file per session); misclicks and a click path for Figma (Embed API, needs a Figma OAuth client id)."]),
     ("Copy", ["One source line: transcript from their voice after the session; summary and friction points written from it; quotes are exact.", "\"Friction points\" not \"AI insights\". Severity as Low, Medium, High."]),
     ("Engineer check", ["No cursor in A, B or C: tab recordings have none. D draws one only from a saved click track.", "During processing nothing animates as typing; lines appear together when ready.", "The project-level rail (\"No sentiment yet\") is removed from this page (B12)."])], n_states=4))

# ================================================================== 09 REVIEW ACROSS SESSIONS
rev_head = lambda: test_head("Review", 3, btn("Copy link", "secondary", icon="copy"))
fix_card = lambda n, title, quotes, who: (f'<div class="ae-card" style="padding:16px;display:grid;grid-template-columns:28px minmax(0,1fr) auto;gap:12px"><span class="ae-mono" style="font-size:13px;color:var(--ae-ink-3)">0{n}</span><div class="ae-stack ae-stack--tight"><span class="ae-strong" style="font-size:15px">{title}</span>'
                                          + "".join(f'<span class="ae-small" style="color:var(--ae-ink-2)">“{q}” <span class="ae-tc">{w}</span></span>' for q, w in quotes)
                                          + f'</div><span class="ae-stack ae-stack--tight" style="align-items:flex-end">{tag(who, "review")}<a class="ae-link ae-small">{i("play","ae-i--sm")} Play moments</a></span></div>')
rev_a = app(rev_head() + body(
    f'<div class="ae-row-gap"><span class="ae-small">{i("check","ae-i--sm")} Based on 2 of 3 sessions. Session 3 is being transcribed; this updates after it.</span><span class="ae-spacer"></span>{btn("Download summary","secondary",icon="download")}</div>'
    f'<div style="display:grid;grid-template-columns:minmax(0,1fr) 320px;gap:28px;align-items:start"><div class="ae-stack"><div class="ae-h2">What to fix first</div>'
    + fix_card(1, "Put cards on the home screen", [("Is it under More?", "B 03:08"), ("Where are my cards?", "A 01:52")], "2 of 2")
    + fix_card(2, "Label the back arrow in Send", [("It doesn't say where to.", "B 02:41")], "1 of 2")
    + fix_card(3, "Confirm when money has gone", [("I wasn't sure the money had gone.", "A 02:20")], "1 of 2")
    + f'</div><div class="ae-stack ae-stack--loose"><div class="ae-stack ae-stack--tight"><div class="ae-label">Themes across sessions</div>{themes([("Cards hard to find",2,2),("Send flow unclear after paying",2,2),("Balance looks tappable",1,2)])}</div>'
    f'<div class="ae-stack ae-stack--tight"><div class="ae-label">Where they disagreed</div><div class="ae-card ae-card--pad ae-small" style="color:var(--ae-ink-2)"><b class="ae-strong">Send flow.</b> Tester A found it "easy, like my bank". Tester B lost her way after paying.</div></div>'
    f'<div class="ae-stack ae-stack--tight"><div class="ae-label">What worked</div><div class="ae-small" style="color:var(--ae-ink-2)">Both sent money first time. “Easy enough, it\'s a bit like my bank.”</div></div>{source_line("Themes need at least 2 sessions.")}</div></div>'), "sidebar", "tests")
rev_b = app(rev_head() + body(
    f'<div style="max-width:760px" class="ae-stack ae-stack--loose"><div class="ae-small">Review · 2 sessions · Sunday</div><div class="ae-display" style="font-size:30px">Both testers looked for their cards on the home screen<span style="color:var(--ae-blue)">.</span></div>'
    f'<p style="margin:0;font-size:16px;line-height:1.65;color:var(--ae-ink-2)">Sending money worked for both of them. After paying, one lost her way back, and the balance looked like something to tap. The clearest change: put cards next to the balance.</p>'
    f'<div class="ae-grid ae-grid--2" style="gap:28px"><div class="ae-stack ae-stack--tight"><div class="ae-label">Themes</div>{themes([("Cards hard to find",2,2),("Back from Send unclear",1,2),("Balance looks tappable",1,2)])}</div>'
    f'<div class="ae-stack ae-stack--tight"><div class="ae-label">In their own words</div><p class="ae-quote" style="font-size:17px">“Is it <mark>under More?</mark>”</p><div class="ae-quote__by">Tester B · <span class="ae-tc">03:08</span></div><p class="ae-quote" style="font-size:17px">“Where are my cards?”</p><div class="ae-quote__by">Tester A · <span class="ae-tc">01:52</span></div></div></div>{source_line()}</div>'), "sidebar", "tests")
one = app(test_head("Review", 1, btn("Copy link", "secondary", icon="copy"), name="Onboarding v2", url="onboarding.aeroapp.ai", tasks="Explore freely") + body(
    f'<div class="ae-callout">{i("info")}<span><b>Patterns across sessions appear after the second one.</b> Until then, here is what came up in Session 1.</span><span class="ae-callout__act">{btn("Copy link","secondary",size="sm",icon="copy")}</span></div><div class="ae-stack"><div class="ae-label">Session 1 · Tester F · top issues</div>{friction({"title":"Skip looks like the main button","q":"I pressed skip by accident, it was the big one.","t":"00:48","sev":2,"n":""}, who="Tester F")}{friction({"title":"Unclear why the app needs contacts","q":"Why does it want my contacts already?","t":"01:30","sev":1,"n":""}, who="Tester F")}</div>'), "sidebar", "tests")
updating = app(rev_head() + body(f'<div class="ae-callout ae-callout--info"><span class="ae-spin" style="color:var(--ae-link)"></span><span><b>Updating after Session 3.</b> Usually under a minute. The review below is from 2 sessions until then.</span></div><div style="opacity:.55" class="ae-stack"><div class="ae-h2">What to fix first</div>' + fix_card(1, "Put cards on the home screen", [("Is it under More?", "B 03:08")], "2 of 2") + '</div>'), "sidebar", "tests")
rev_fail = app(rev_head() + body(f'<div class="ae-callout ae-callout--bad">{i("alert")}<span><b>The review didn\'t finish.</b> The summary service didn\'t answer in time. Your sessions and transcripts are safe.</span><span class="ae-callout__act">{btn("Try again","secondary",size="sm")}</span></div><div class="ae-small">Each session\'s own summary is still on its page.</div>'), "sidebar", "tests")
stale = app(rev_head() + body(f'<div class="ae-callout">{i("refresh")}<span><b>Based on 2 of 3 sessions.</b> Session 3 finished after this review was made.</span><span class="ae-callout__act">{btn("Update review","secondary",size="sm")}</span></div><div class="ae-h2">What to fix first</div>' + fix_card(1, "Put cards on the home screen", [("Is it under More?", "B 03:08")], "2 of 2")), "sidebar", "tests")
out.append(screen(9, "s9", "Review across sessions", "Themes, what to fix first, where testers disagreed. \"Based on 3 of 3 sessions\". With fewer than 2 sessions, show each session's top issues instead of a dead end.",
    "<b>Pick A.</b> It leads with the decision (what to fix first, in their words, with the moments to play), then themes and disagreements. B, the calm written version from C, is the \"Download summary\" output and the email when a review is ready.",
    [approach("A", "What to fix first", "Ranked fixes with quotes and a play link, then themes, disagreements and what worked.", rev_a, True, "A + C", "Server-side review"),
     approach("B", "Written summary", "From C Story. One headline in plain words, a short paragraph, themes and their words.", rev_b, False, "C Story")],
    state("One session", "no dead end: that session's issues", one)
    + state("Updating", "after a new session", updating, prop="Auto update")
    + state("Failed", "says why, keeps the old one", rev_fail)
    + state("Out of date", "Based on 2 of 3 sessions", stale),
    [("Proposed", ["Run the review on the server after each analysed session, not when the tab opens (B3, B5).", "Fix the renderer's field names (avg_severity, topic, viewpoints) and add an error boundary (B4).", "\"Download summary\" replaces the header's Export (B10)."]),
     ("Copy", ["\"Review\" is the tab; \"What to fix first\" is the lead. Never \"AI insights\".", "Contradictions read as \"Where they disagreed\"."]),
     ("Engineer check", ["Themes need 2 or more analysed sessions; the count is shown, not hidden.", "Sentiment card removed: it read a field never written (B3d).", "Every quote links to session + time."])], n_states=4))

# ================================================================== 11 PLANS AND USAGE
def plan(name, price, items, pick=False, cta="Start 7-day trial", current=False):
    li = "".join(f'<li>{i("check")}{E(x)}</li>' for x in items)
    p = '<small>a month</small>' if price != "$0" else ""
    b = btn("Current plan", "secondary", extra="ae-btn--block is-disabled") if current else btn(cta, "primary" if pick else "secondary", pick, extra="ae-btn--block")
    return f'<div class="ae-plan{" is-pick" if pick else ""}"><div class="ae-plan__name">{name}{tag("Suggested","blue") if pick else ""}</div><div class="ae-plan__price">{price}{p}</div><ul>{li}</ul>{b}</div>'
PLANS = (plan("Free", "$0", ["3 test sessions, recordings included", "Sites stay live 7 days"], current=True)
         + plan("Basic", "$3", ["5 test sessions", "Your own aeroapp.ai address", "Password protection", "Custom favicon, no Aero badge"], True)
         + plan("Solo", "$6", ["10 test sessions", "Everything in Basic", "Custom domain", "Site analytics"])
         + plan("Pro", "$19", ["20 test sessions", "Everything in Solo", "Priority support"]))
plans_a = app(head("Plan and usage", ["Account", "Plan and usage"], "", "") + tabs(["Account", "Plan and usage", "API keys"], "Plan and usage") + body(
    f'<div class="ae-grid ae-grid--3"><div class="ae-card ae-card--pad ae-stack ae-stack--tight"><div class="ae-label">Plan</div><div class="ae-h2">Free</div><div class="ae-small">Paid plans from $3 a month, with a 7-day free trial.</div></div>'
    f'<div class="ae-card ae-card--pad ae-stack">{meter(2,3)}<div class="ae-small">Delete a session to make room, or upgrade.</div></div>'
    f'<div class="ae-card ae-card--pad ae-stack ae-stack--tight"><div class="ae-label">Sites</div><div class="ae-small">3 sites. Free sites stay live 7 days: <span style="color:var(--ae-warn)">1 offline in 2 days</span>, 1 offline.</div></div></div>'
    f'<div class="ae-grid ae-grid--4">{PLANS}</div><div class="ae-small">Monthly, no call, no contract, cancel any time. Prices shown in USD; you pay in your local currency at checkout.</div>'), "sidebar", "home")
moment_modal = (f'<div class="ae-scrim"><div class="ae-modal"><div class="ae-modal__head"><span style="flex:1" class="ae-stack ae-stack--tight"><span class="ae-area ae-area--publish">Publish</span><span class="ae-h2">Keep onboarding.aeroapp.ai live</span></span>{btn("","ghost",size="sm",icon="x",extra="ae-btn--icon")}</div>'
                f'<div class="ae-modal__body"><p class="ae-p">It goes offline in 2 days. On any paid plan your sites stay live, and you keep more sessions.</p>{plan("Basic","$3",["Sites stay live","5 test sessions","Your own aeroapp.ai address, password protection"],True)}<a class="ae-link ae-small">Compare all plans</a></div>'
                f'<div class="ae-modal__foot"><span class="ae-small" style="margin-right:auto">7-day free trial. Cancel any time.</span>{btn("Not now","ghost")}</div></div></div>')
plans_b = app(home_head + home_a_body, "sidebar", "home", overlay=moment_modal)
limit_inline = app(test_head("Sessions", 3, btn("Copy link", "secondary", icon="copy")) + body(
    f'<div class="ae-card ae-card--test" style="padding:18px;display:grid;grid-template-columns:minmax(0,1fr) auto;gap:16px;align-items:center"><div class="ae-stack ae-stack--tight">{meter(3,3,"sessions kept",full=True)}<span class="ae-small" style="color:var(--ae-ink-2)">That\'s all 3 on Free. To keep the next one, delete a session or move to Basic (5 sessions, $3 a month).</span></div><div class="ae-row-gap">{btn("Manage sessions","ghost")}{btn("Try Basic free","primary",True)}</div></div>'
    + sessions_list(list(reversed(S["sessions"][:2])) + [dict(S["sessions"][2], status="ready", quote="It's quick. I'd want a receipt after sending.")])), "sidebar", "tests")
trial = app(head("Plan and usage", ["Account", "Plan and usage"], "", "") + tabs(["Account", "Plan and usage", "API keys"], "Plan and usage") + body(f'<div class="ae-callout ae-callout--info">{i("clock")}<span><b>Basic trial: 5 days left.</b> Then $3 a month. Cancel any time before Mon 28 Oct and you won\'t be charged.</span><span class="ae-callout__act">{btn("Manage billing","secondary",size="sm")}</span></div><div class="ae-grid ae-grid--3"><div class="ae-card ae-card--pad">{meter(3,5)}</div></div>'), "sidebar", "home")
expiry_card = app(head("Sites", None, "", new_btn("New site")) + body(f'<div class="ae-callout ae-callout--warn">{i("clock")}<span><b>onboarding.aeroapp.ai goes offline in 2 days.</b> Free sites stay live 7 days.</span><span class="ae-callout__act">{btn("Keep it live","secondary",size="sm")}</span></div>{sites_grid()}'), "sidebar", "sites")
out.append(screen(11, "s11", "Plans and usage", "Usage that matches everywhere (\"2 of 3 sessions kept\"), expiry warnings, and the upgrade modal from real moments.",
    "<b>All three, at different moments.</b> A is the one place for plans. B opens from a real moment (a site about to go offline) and suggests one plan. C sits where the limit bites. Same meter, same words, same numbers on every surface.",
    [approach("A", "Plan and usage page", "Usage in plain view, then the four plans from PRICING-FACTS.", plans_a, True, "B Colour + A"),
     approach("B", "Upgrade from a moment", "Opened by \"Keep it live\". One suggested plan, the rest one click away.", plans_b, False, "", "Moment modals"),
     approach("C", "At the limit, in place", "On Sessions when all 3 are kept.", limit_inline, False, "", "Limit behaviour")],
    state("Trial", "days left, when billing starts", trial)
    + state("Expiry on Sites", "warning where it bites", expiry_card, prop="Countdown"),
    [("Proposed", ["Moment modals: site expiring, last session slot, gated setting.", "Stored usage counter instead of reading every project (Account B14).", "Monthly allowance is planned, not live: never write \"a month\" after a session count."]),
     ("Copy", ["Plan lines only from PRICING-FACTS. Trial: \"7-day free trial, cancel any time\".", "\"See plans from $3\" as the soft link everywhere."]),
     ("Engineer check", ["Usage meter reads one counter used by sidebar, Sessions, Share and this page.", "Regional prices at checkout; the app shows USD with a line saying so."])], n_states=2))

# ================================================================== 12 GUIDANCE
guide_a = app(test_head("Sessions", 3, btn("Copy link", "secondary", icon="copy")) + body(
    f'<div style="display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:28px;align-items:start">{sessions_list()}'
    f'<div class="ae-stack"><div class="ae-guide"><div class="ae-guide__head">{i("book")}How a session becomes a review</div><ol><li>The tester\'s screen and voice are recorded in their browser.</li><li>When they finish, the voice is transcribed, with a time for every word. Usually about a minute.</li><li>A summary and friction points are written from the transcript. Every quote is their exact words.</li><li>From the second session, themes across sessions are added under Review.</li></ol><a class="ae-link ae-small">Read more</a></div>'
    f'<div class="ae-guide ae-guide--closed"><span class="ae-guide__head">{i("eye")}What testers see</span><span class="ae-spacer"></span>{i("down","ae-i--sm")}</div><div class="ae-guide ae-guide--closed"><span class="ae-guide__head">{i("lock")}Who can see recordings</span><span class="ae-spacer"></span>{i("down","ae-i--sm")}</div></div></div>'), "sidebar", "tests")
drawer = (f'<div style="position:absolute;top:0;right:0;bottom:0;width:380px;background:var(--ae-paper);box-shadow:var(--ae-sh-3),-1px 0 0 var(--ae-line);z-index:80;display:flex;flex-direction:column">'
          f'<div class="ae-row-gap" style="padding:16px 18px;border-bottom:1px solid var(--ae-line)"><span class="ae-h3" style="flex:1">How it works</span>{btn("","ghost",size="sm",icon="x",extra="ae-btn--icon")}</div>'
          f'<div style="padding:16px 18px;display:flex;flex-direction:column;gap:14px;overflow:hidden"><div class="ae-input is-placeholder">{i("search","ae-i--sm")}&nbsp; Search guides</div>'
          + "".join(f'<div class="ae-stack ae-stack--tight" style="padding-bottom:12px;border-bottom:1px solid var(--ae-line)"><span class="ae-area ae-area--{a}">{x}</span><span class="ae-strong">{t}</span><span class="ae-small">{d}</span></div>' for a, x, t, d in [
              ("review", "Review", "How the transcript is made", "Their voice is transcribed after the session ends, with a time for every word. About a minute."),
              ("review", "Review", "How summaries and friction points are made", "Written from the transcript by a language model. Quotes are exact; if it can't find evidence, it leaves it out."),
              ("test", "Test", "What testers see", "A welcome from you, one permission step, your tasks in a small panel, then your thank-you."),
              ("publish", "Publish", "What happens on Free", "Sites stay live 7 days, then go offline. Files and versions are kept."),
              ("test", "Test", "Testing on a phone", "Figma prototypes record voice only. HTML sites need a laptop.")])
          + '</div></div>')
guide_b = app(home_head + home_a_body, "sidebar", "home", overlay=drawer)
teach_sites = app(head("Sites", None, "", new_btn("New site")) + body(f'<div class="ae-empty" style="background:var(--ae-publish-wash);padding:36px"><div class="ae-empty__title">Put your first prototype online</div><div class="ae-empty__text">Each site gets its own address, like pocket.aeroapp.ai. Update it any time; every update is a version you can roll back.</div></div><div class="ae-grid ae-grid--3"><div class="ae-source-tile"><span class="ae-source-tile__icon">{i("prompt")}</span><span class="ae-source-tile__title">One prompt</span><span class="ae-source-tile__sub">Claude or ChatGPT publishes it.</span></div><div class="ae-source-tile"><span class="ae-source-tile__icon">{i("figma")}</span><span class="ae-source-tile__title">Figma link</span><span class="ae-source-tile__sub">Live straight away.</span></div><div class="ae-source-tile"><span class="ae-source-tile__icon">{i("upload")}</span><span class="ae-source-tile__title">HTML or zip</span><span class="ae-source-tile__sub">With an index.html.</span></div></div>'), "sidebar", "sites")
teach_tests = app(head("Tests", None, "", new_btn("New test")) + body(f'<div class="ae-empty" style="background:var(--ae-test-wash);padding:36px"><div class="ae-empty__title">Watch people use your prototype</div><div class="ae-empty__text">A test is one link. People open it, talk through your tasks, and you get the recording, the transcript and what to fix first. Bring your own testers: friends, clients, classmates.</div><div class="ae-empty__actions">{btn("Test pocket.aeroapp.ai","primary",True)}{btn("Test a Figma link","secondary")}</div></div>'), "sidebar", "tests")
out.append(screen(12, "s12", "Guidance", "Short, honest explainers inside the app: how transcription works, how summaries and friction points are made, what testers see. Empty states that teach.",
    "<b>Both.</b> A puts a short guide where the question comes up (beside Sessions, under the share link, in the session source line). B is the \"How it works\" panel behind the book icon, which is also the seed of the SEO content pages.",
    [approach("A", "In place", "A short numbered guide beside the thing it explains, closed after the first visit.", guide_a, True, "C Story"),
     approach("B", "How it works panel", "Five short guides, each tagged with its area. The same text feeds the website guides.", guide_b, False, "", "Help panel")],
    state("Sites, first run", "teaches versions and addresses", teach_sites)
    + state("Tests, first run", "uses the site they already have", teach_tests),
    [("Proposed", ["Guide content lives as data (one file), shown in the app and on aeroapp.ai/guides.", "Each guide remembers it was closed, per person."]),
     ("Copy", ["Name AI only on the way out: \"written from the transcript by a language model\". Never \"AI-powered\".", "Say what isn't recorded too: no camera, no mouse."]),
     ("Engineer check", ["Empty states never show while data is loading.", "First-run Tests suggests the newest live site by name."])], n_states=2))

# ================================================================== 13 STATES
rules = [("Home", "Shapes of feed, tests, sites", "First run: three ways in + how it works", "\"Couldn't load your tests. Try again.\" Lists kept if cached", "Feed shows \"Transcript arriving\" per session"),
         ("Create", "n/a (static)", "Nothing saved until real input", "Names the file and the fix", "Waiting for the chat · upload progress · publishing"),
         ("Site detail", "Header and tabs paint, preview shape", "n/a", "Publish failed: v4 stays live, files kept", "Publishing v5, live stays on v4"),
         ("Test setup", "Fields with shapes", "Explore freely (no tasks)", "Save failed: keep edits, retry", "n/a"),
         ("Share", "Link shape, never a wrong URL", "n/a", "Copy failed: select-all fallback", "n/a"),
         ("Sessions", "Rows; tab count waits (B2)", "\"No sessions yet\" + copy link", "Listener error: \"Live updates paused. Refresh.\"", "Recording now · Transcript arriving"),
         ("Session view", "Player and text shapes", "n/a", "Transcript failed: recording safe, try again", "Listen now, transcript about a minute"),
         ("Review", "Fix cards shapes", "1 session: its top issues", "Didn't finish: why, keep old, try again", "Updating after session N"),
         ("Plans", "Meter shape", "n/a", "Checkout error from Stripe, in plain words", "Verifying payment after checkout")]
tbl = ('<div class="ae-list--card ae-kit" style="overflow:auto"><div class="ae-listhead" style="grid-template-columns:130px repeat(4,minmax(0,1fr))"><span>Screen</span><span>Loading</span><span>Empty</span><span>Error</span><span>Processing</span></div><div class="ae-list">'
       + "".join(f'<div style="display:grid;grid-template-columns:130px repeat(4,minmax(0,1fr));gap:12px;padding:11px 16px;font-size:13px;color:#3A3A3D"><b style="font-weight:520;color:#1D1D1F">{a}</b><span>{b}</span><span>{c}</span><span>{d}</span><span>{e}</span></div>' for a, b, c, d, e in rules) + '</div></div>')
net = app(home_head + body(f'<div class="ae-callout ae-callout--bad">{i("alert")}<span><b>Couldn\'t load your tests.</b> Check your connection. What you saw last is shown below.</span><span class="ae-callout__act">{btn("Try again","secondary",size="sm")}</span></div>' + section("Tests", f'<div style="opacity:.6">{tests_list()}</div>')), "sidebar", "home")
pubfail = app(head("Pocket", ["Sites", "Pocket"], site_meta, site_actions, "publish") + tabs(SITE_TABS, "Overview") + body(f'<div class="ae-callout ae-callout--bad">{i("alert")}<span><b>v5 didn\'t publish.</b> The upload stopped at 9 of 14 files when the connection dropped. v4 is still live.</span><span class="ae-callout__act">{btn("Try again","secondary",size="sm")}</span></div>'), "sidebar", "sites")
out.append(f'''<section class="scr" id="s13"><div class="scr__head"><span class="scr__n">13</span><div><h2>States for every screen</h2><p>Loading (shapes, never blank), empty, error, processing. Each screen above shows its own; this is the checklist the build follows.</p></div><div class="scr__why"><b>Rules.</b> Paint the real header first. No count until its data has loaded. Errors say what happened, what is safe, and what to do. Processing never animates typing.</div></div>
{tbl}<h3 class="states-h">Two more errors</h3><div class="states" style="--n:2">{state("Can't load", "keep what was on screen", net)}{state("Publish failed", "the live version is untouched", pubfail)}</div></section>''')

html_out = page("screens.html", "Aero screens", "Aero app UI round: screens 1 to 9 and 11 to 13 with approaches side by side and their states.", "".join(out))
open("screens.html", "w").write(html_out)
print("screens.html", len(html_out))
