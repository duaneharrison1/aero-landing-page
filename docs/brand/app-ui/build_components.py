from build_common import *

def cell(name, body, sub="", cls="", prop=""):
    pr = proposed(prop) if prop else ""
    return f'<div class="c-cell {cls}"><div class="c-name"><b>{name}</b>{sub}{pr}</div>{body}</div>'

def sec(sid, title, lede, body):
    return f'<section class="c-sec" id="{sid}"><h2>{title}</h2><p>{lede}</p>{body}</section>'

def sw(name, var, hexv):
    return f'<div class="sw"><i style="background:var({var})"></i><b>{name}</b><span>{var}<br>{hexv}</span></div>'

out = []
out.append(f'''<div class="b-hero"><div class="b-kicker">Aero app UI · step 1 · components</div>
<h1>Tokens and components<span class="d">.</span></h1>
<p>The small set of named pieces every Aero screen is built from. Each one uses only the tokens in <code>tokens.css</code>, and responds to its container, so the website and videos can reuse the same markup in a demo mode with example data.</p>
<p class="ae-small">Class names are stable: <code>ae-component</code>, <code>ae-component--variant</code>, <code>is-state</code>. Files: <code>tokens.css</code>, <code>components.css</code>, <code>kit.py</code> (helpers and the example scene). Switch palette at the top right.</p>
<div class="b-toc">{"".join(f'<a href="#{a}">{b}</a>' for a,b in [("c-colour","Colour"),("c-type","Type and space"),("c-glass","Glass"),("c-buttons","Buttons"),("c-tags","Tags and status"),("c-shell","Shell"),("c-forms","Forms"),("c-lists","Lists and cards"),("c-review","Review"),("c-feedback","Feedback"),("c-plans","Plans"),("c-tester","Tester pieces"),("c-outside","Outside Aero")])}</div></div>''')

# ---------------- colour
core = "".join(sw(n, v, h) for n, v, h in [("Ink", "--ae-ink", "#1D1D1F"), ("Ink 2", "--ae-ink-2", "#3A3A3D"), ("Ink 3", "--ae-ink-3", "#6E6E73"), ("Paper", "--ae-paper", "#FFFFFF"), ("Mist", "--ae-mist", "#FAFAF9"), ("Mist 2", "--ae-mist-2", "#F3F3F1"), ("Line", "--ae-line", "#E8E8EA"), ("Line 2", "--ae-line-2", "#D7D7DC"), ("Aero blue", "--ae-blue", "#3478F6"), ("Link", "--ae-link", "#1F63DD"), ("Marker", "--ae-mark", "#FFEAA0"), ("Recording", "--ae-rec", "#E5484D"), ("OK", "--ae-ok", "#1C8752"), ("Warn", "--ae-warn", "#9A5B00"), ("Bad", "--ae-bad", "#C4372C")])

def palcol(name, attr, desc):
    areas = ""
    for a, label, line in [("publish", "Publish", "Sites, versions, address"), ("test", "Test", "Setup, share, sessions"), ("review", "Review", "Summary, friction, themes")]:
        areas += (f'<div class="pal__area" style="background:var(--ae-{a}-wash)"><span class="ae-area ae-area--{a}">{label}</span><b>{label}<span style="color:var(--ae-blue)">.</span></b>'
                  f'<span class="ae-small" style="color:var(--ae-ink-2)">{line}</span><span class="ae-row-gap">{tag(label, a)}<span class="ae-feed-item__icon ae-feed-item__icon--{a}" style="width:22px;height:22px;border-radius:6px">{i("dot","ae-i--sm")}</span></span></div>')
    return f'<div class="pal__col" {attr}><div class="c-name"><b>{name}</b></div><p class="ae-small" style="margin:0">{desc}</p><div class="pal__areas">{areas}</div></div>'

out.append(sec("c-colour", "Colour", "Ink, white, mist and line do almost all the work. Aero blue is the one bright thing: the dot, links, selection and the playhead. Each area has one soft gradient, used for page headers, empty states and the website sections, never in the nav. Two palettes to choose from.",
    f'<div class="sw-grid">{core}</div><div style="height:18px"></div><div class="pal">'
    + palcol("Palette 1 · Morning", "", "A Studio's softness: peach, lilac, mint. Calm, close to today's brand washes.")
    + palcol("Palette 2 · Clear", 'data-palette="clear"', "B Colour's clarity, softened: butter, rose, sea. Easier to tell apart at a glance.")
    + '</div>'))

# ---------------- type
typ = "".join(f'<div class="typo-row"><code>{c}</code><div class="{cls}">{t}</div></div>' for c, cls, t in [
    ("display 34 / 350", "ae-display ae-dot-end", "From prompt to first session"),
    ("h1 26 / 450", "ae-h1", "Pocket"),
    ("h2 21 / 450", "ae-h2", "What to fix first"),
    ("h3 15 / 520", "ae-h3", "Friction points"),
    ("quote 21 / 350", "ae-quote", "“I thought my cards would be on the home screen. Is it <mark>under More?</mark>”"),
    ("transcript 15 / 1.7", "ae-tline__text", "Right, sent. How do I get back? There's an arrow but it doesn't say where to."),
    ("body 14 / 400", "", "Share this link with testers. They open it in their browser, nothing to install."),
    ("small 12.5", "ae-small", "Free plan. Sites stay live 7 days."),
    ("label mono 10.5", "ae-label", "Themes across sessions"),
    ("timecode mono 11.5", "ae-tc", "03:08 / 07:12"),
])
space = "".join(f'<div style="display:flex;flex-direction:column;align-items:center;gap:6px"><i style="display:block;width:var(--ae-s-{k});height:var(--ae-s-{k});background:var(--ae-ink);border-radius:2px"></i><span class="ae-tc">{k}</span></div>' for k in [1,2,3,4,5,6,8,10,12,16])
radii = "".join(f'<div style="display:flex;flex-direction:column;align-items:center;gap:6px"><i style="display:block;width:56px;height:40px;border-radius:var(--ae-r-{k});box-shadow:inset 0 0 0 1.5px var(--ae-ink-3)"></i><span class="ae-tc">{k}</span></div>' for k in ["xs","sm","md","btn","lg","xl","pill"])
shad = "".join(f'<div style="display:flex;flex-direction:column;align-items:center;gap:8px"><i style="display:block;width:84px;height:56px;border-radius:12px;background:#fff;box-shadow:var(--ae-sh-{k})"></i><span class="ae-tc">sh-{k}</span></div>' for k in ["1","2","3","float"])
out.append(sec("c-type", "Type, space, radius, elevation", "Geist, light and large for headings, never heavy. Geist Mono only for timecodes, counts and small labels. A 4px grid.",
    f'<div class="c-grid" style="--n:2">{cell("Type scale", typ)}{cell("Space · radius · elevation", f"<div class=\"c-row\" style=\"align-items:flex-end;gap:14px\">{space}</div><hr class=\"ae-hr\"><div class=\"c-row\" style=\"gap:14px\">{radii}</div><hr class=\"ae-hr\"><div class=\"c-row\" style=\"gap:18px;padding:6px 0 4px\">{shad}</div>")}</div>'))

# ---------------- glass
dark_proto = '<div class="over" style="background:#111;"><div style="position:absolute;inset:0;background:radial-gradient(circle at 30% 30%,#2b2b35,#0b0b0d)"></div>'
glass_cells = (
    cell("Primary action", f'<div class="c-row">{btn("Create test","primary",True,icon="plus")}{btn("Publish","primary",True)}</div><p class="ae-small" style="margin:0">One per view, in the page header or a modal footer. Ink glass, quiet: the rim takes a little colour from what is near it.</p>', '<span class="today">V3 glass</span>')
    + cell("Over an area wash", f'<div class="over" style="background:var(--ae-test-wash);min-height:120px"><div class="c-row">{btn("Copy link","primary",True,icon="copy")}{btn("Open as a tester","secondary",True,icon="out")}</div></div><p class="ae-small" style="margin:0">On the share page the wash tints the rim. This is where the engine earns its place.</p>', "", "c-cell--mist")
    + cell("Floating player controls", f'<div class="over" style="background:linear-gradient(135deg,#FF6F4F,#FFB199);min-height:120px;justify-content:center"><div class="c-row">{btn("","secondary",True,icon="back10",extra="ae-btn--icon ae-btn--pill")}{btn("","primary",True,icon="pause",extra="ae-btn--icon ae-btn--pill")}{btn("1×","secondary",True,extra="ae-btn--pill")}</div></div><p class="ae-small" style="margin:0">Pills float over the recording, so they pick up the prototype’s colour. Shown on hover and when paused.</p>', "", "", "Proposed")
    + cell("Flat, not glass", f'<div class="c-row">{btn("Cancel","secondary")}{btn("Settings","ghost",icon="settings")}{btn("Delete site","danger")}</div><p class="ae-small" style="margin:0">Secondary and tertiary buttons stay flat. Glass on everything is noise; on one thing per view it reads as "this is the next step".</p>')
    + cell("Tester task panel (shared)", f'{dark_proto}<div class="ae-taskpanel" style="position:relative;width:100%"><div class="ae-taskpanel__top"><span class="ae-label">Task 1 of 2</span><span class="ae-spacer"></span><span class="ae-rec">00:42</span></div><div class="ae-taskpanel__task">Send £20 to Sam</div><div class="c-row">{btn("Next task","primary",True,size="sm")}{btn("Skip","ghost",size="sm")}</div></div></div>', "", "", "Proposed")
    + cell("Fallback", '<p class="ae-small" style="margin:0">Refraction renders in Chromium. Safari and Firefox get a frosted blur with the same shape and label contrast. Reduced motion: no hover scale. <code>?glass=0</code> on any of these pages shows the flat version for comparison.</p>')
)
out.append(sec("c-glass", "Glass: where it belongs", "V3 glass (Snell refraction, Fresnel edge, key light), quiet by default, rounded rectangle in the app, pill when it floats. The engine reads each button's radius. Proposed rule: glass for the one primary action per view, floating player controls, and the tester task panel. Everything else is flat.", f'<div class="c-grid">{glass_cells}</div>'))

# ---------------- buttons
b = (cell(".ae-btn", f'<div class="c-row">{btn("Primary","primary")}{btn("Secondary","secondary")}{btn("Ghost","ghost")}{btn("Delete","danger")}</div><div class="c-row">{btn("Small","secondary",size="sm")}{btn("Large","primary",size="lg")}{btn("","secondary",icon="more",extra="ae-btn--icon")}{btn("Pill","secondary",extra="ae-btn--pill")}</div>', " variants and sizes")
     + cell("States", f'<div class="c-row">{btn("Publishing","primary",extra="is-loading",icon=None)}{btn("Copied","primary",extra="is-done",icon="check")}{btn("Disabled","primary",extra="is-disabled")}<button class="ae-btn ae-btn--secondary" style="box-shadow:var(--ae-ring)">Focus</button></div><p class="ae-small" style="margin:0">Loading keeps the label and adds a spinner. Labels are plain verbs, no "…".</p>'.replace('Publishing</button>', '<span class="ae-spin"></span>Publishing</button>'))
     + cell("Wording", '<div class="ae-stack ae-stack--tight ae-small"><span>Publish · Copy link · Create test · Open as a tester · Run a test on this site · Roll back · See plans</span><span class="ae-muted">Not: Deploy · Get insights · Unlock · Launch</span></div>'))
out.append(sec("c-buttons", "Buttons", "Rounded rectangles, 10px radius, 34px tall in the app. Sentence case.", f'<div class="c-grid">{b}</div>'))

# ---------------- tags and status
t = (cell(".ae-tag", f'<div class="c-row">{tag("Figma")}{tag("HTML","line")}{tag("Publish","publish")}{tag("Test","test")}{tag("Review","review")}{tag("Insights ready","ok")}{tag("Offline in 2 days","warn")}{tag("Failed","bad")}{tag("2 new","blue")}{tag("v4","line")}</div>')
     + cell(".ae-status", f'<div class="ae-stack ae-stack--tight">{status("Live","live")}{status("Offline in 2 days","soon")}{status("Offline · free plan ended","offline")}{status("Draft","draft")}</div>', " sites")
     + cell(".ae-status", f'<div class="ae-stack ae-stack--tight">{status("Recording now","recording")}{status("Transcript arriving, usually about a minute","processing")}{status("Ready","ready")}{status("No audio","noaudio")}{status("Ended early","offline")}</div>', " sessions"))
out.append(sec("c-tags", "Tags and status", "One status per object, as a dot and words. Tags for kind and counts. Area tags use the area tint.", f'<div class="c-grid">{t}</div>'))

# ---------------- shell
studio_menu = f'''<div class="ae-menu"><div class="ae-menu__item is-active"><span class="ae-mark" style="width:20px;height:20px;font-size:10px;border-radius:6px"><span>A</span></span>Kestrel Studio<span class="ae-spacer"></span>{i("check","ae-i--sm")}</div><div class="ae-menu__item"><span class="ae-avatar ae-avatar--sm ae-avatar--e">P</span>Personal</div><div class="ae-menu__sep"></div><div class="ae-menu__item">{i("plus")}New studio</div><div class="ae-menu__item">{i("settings")}Studio settings</div></div>'''
sh = (cell(".ae-sidebar", f'<div style="height:560px;display:flex;background:var(--ae-mist);border-radius:12px;box-shadow:inset 0 0 0 1px var(--ae-line)" class="ae-app">{sidebar("home")}</div>', "", "", "")
      + cell("Studio switcher", studio_menu + '<p class="ae-small" style="margin:0">Studios are a proposal (today an account is one person). Without studios the switcher shows the account name and opens the account menu.</p>', "", "", "Proposed")
      + cell(".ae-usage", f'<div class="ae-usage">{meter(1,3)}</div><div class="ae-usage">{meter(2,3)}<span class="ae-small">Free plan. Sites stay live 7 days.</span></div><div class="ae-usage">{meter(3,3,full=True)}<span class="ae-small" style="color:var(--ae-warn)">All 3 kept. Delete one or upgrade to keep new sessions.</span><a class="ae-link ae-small">See plans from $3</a></div><p class="ae-small" style="margin:0">Same words everywhere: "2 of 3 sessions kept". Never "a month" (not live yet).</p>')
      + cell(".ae-progress", f'{progress(0)}{progress(1)}{progress(2)}{progress(3)}<p class="ae-small" style="margin:0">From D: where a prototype is in Publish, Test, Review. Used on Home and in the flows.</p>')
      + cell(".ae-tabs", f'<div class="ae-tabs ae-tabs--inner"><span class="ae-tab">Setup</span><span class="ae-tab">Share</span><span class="ae-tab is-active">Sessions <span class="ae-tab__n">3</span></span><span class="ae-tab">Review <span class="ae-tab__dot"></span></span></div><span class="ae-seg"><span class="ae-seg__opt is-active">All</span><span class="ae-seg__opt">Live</span><span class="ae-seg__opt">Drafts 2</span></span>')
      + cell(".ae-head--wash", f'<div style="border-radius:12px;overflow:hidden;box-shadow:inset 0 0 0 1px var(--ae-line)" class="ae-app"><div class="ae-head ae-head--wash ae-head--test"><div class="ae-crumbs">Tests <span>/</span> <b>Pocket</b></div><div class="ae-head__row"><h1 class="ae-h1 ae-head__title">Pocket</h1></div><div class="ae-head__meta"><span class="ae-area ae-area--test">Test</span>{status("Collecting","live")}<span>3 sessions</span></div></div></div><p class="ae-small" style="margin:0">The page header carries the area wash. Content below stays white.</p>'))
out.append(sec("c-shell", "Shell", "Sidebar, studio switcher, usage, progress line, tabs and page header.", f'<div class="c-grid">{sh}</div>'))

# ---------------- forms
tasks = f'<div class="ae-stack ae-stack--tight"><div class="ae-task"><span class="ae-task__n">1</span><span class="ae-task__text">Send £20 to Sam</span>{i("grip","ae-task__grip")}</div><div class="ae-task"><span class="ae-task__n">2</span><span class="ae-task__text">Find your cards</span>{i("grip","ae-task__grip")}</div><button class="ae-task ae-task--add">{i("plus","ae-i--sm")}<span style="text-align:left">Add a task</span></button></div>'
fm = (cell(".ae-field / .ae-input", f'<div class="ae-field"><span class="ae-field__label">Name</span><div class="ae-input">Pocket</div><span class="ae-field__hint">Only you see this.</span></div><div class="ae-field"><span class="ae-field__label">Welcome message</span><div class="ae-textarea">Thanks for helping. Try the two tasks and say what you think as you go.</div></div><div class="ae-field is-error"><span class="ae-field__label">Figma link</span><div class="ae-input">figma.com/file/Abc</div><span class="ae-field__error">This is a file link. Use Share, then Copy prototype link.</span></div>')
      + cell(".ae-affix / .ae-copy", f'<div class="ae-field"><span class="ae-field__label">Address</span><div class="ae-affix"><div class="ae-input">pocket</div><span class="ae-affix__end">.aeroapp.ai</span></div><span class="ae-field__hint">Changing it breaks the old link straight away.</span></div><div class="ae-copy"><span class="ae-copy__url">pocket.aeroapp.ai/t/8kq2</span>{btn("Copy","secondary",size="sm",icon="copy")}</div><div class="ae-copy ae-copy--lg"><span class="ae-copy__url">pocket.aeroapp.ai/t/8kq2</span>{btn("Copied","primary",extra="is-done",icon="check")}</div>')
      + cell("Toggles and options", f'<div><div class="ae-option"><div class="ae-option__text"><div class="ae-option__title">Record screen</div><div class="ae-option__sub">Testers pick the tab to share. Laptop and desktop only.</div></div><span class="ae-toggle is-on"></span></div><div class="ae-option"><div class="ae-option__text"><div class="ae-option__title">Record voice</div><div class="ae-option__sub">Needed for the transcript and summary.</div></div><span class="ae-toggle is-on"></span></div><div class="ae-option"><div class="ae-option__text"><div class="ae-option__title">Ask how hard each task was</div><div class="ae-option__sub">A quick rating after each task.</div></div><span class="ae-toggle"></span></div></div>')
      + cell(".ae-task", tasks)
      + cell(".ae-source-tile", f'<div class="ae-grid ae-grid--2" style="gap:10px"><div class="ae-source-tile is-active"><span class="ae-source-tile__icon">{i("prompt")}</span><span class="ae-source-tile__title">One prompt</span><span class="ae-source-tile__sub">Claude or ChatGPT publishes it for you.</span></div><div class="ae-source-tile"><span class="ae-source-tile__icon">{i("figma")}</span><span class="ae-source-tile__title">Figma link</span><span class="ae-source-tile__sub">Paste a prototype link.</span></div></div><div class="ae-source-tile ae-source-tile--row"><span class="ae-source-tile__icon" style="background:var(--ae-test-tint);color:var(--ae-test-ink)">{i("tests")}</span><span><span class="ae-source-tile__title">Test a site you published</span><div class="ae-source-tile__sub">Pick one of your sites.</div></span></div>')
      + cell(".ae-drop", f'<div class="ae-drop">{i("upload","ae-i--lg")}<b>Drop an HTML file, folder or zip</b><span>It needs an index.html at the top.</span></div><div class="ae-drop is-over">{i("upload","ae-i--lg")}<b style="color:inherit">Drop to publish</b></div>')
      + cell(".ae-stepper / .ae-seg", f'<div class="ae-stepper"><span class="ae-stepper__step is-done"><span class="ae-stepper__n">{i("check","ae-i--sm")}</span>Publish</span><span class="ae-stepper__step is-now"><span class="ae-stepper__n">2</span>Test</span><span class="ae-stepper__step"><span class="ae-stepper__n">3</span>Share</span></div><span class="ae-seg"><span class="ae-seg__opt is-active">{i("monitor","ae-i--sm")}Laptop</span><span class="ae-seg__opt">{i("phone","ae-i--sm")}Phone</span></span>'))
out.append(sec("c-forms", "Forms", "Inputs, the address field, copy field, options, tasks, ways in, drop zone.", f'<div class="c-grid">{fm}</div>'))

# ---------------- lists
S = SCENE
feed = f'''<div class="ae-list--card"><div class="ae-feed">
<div class="ae-feed-item is-unread"><span class="ae-feed-item__icon ae-feed-item__icon--review">{i("sessions")}</span><span><div class="ae-feed-item__title">2 new sessions on Pocket</div><div class="ae-feed-item__sub">Tester B and Tester C · today</div></span><span class="ae-tc">10:51</span></div>
<div class="ae-feed-item is-unread"><span class="ae-feed-item__icon ae-feed-item__icon--review">{i("review")}</span><span><div class="ae-feed-item__title">Review ready for Pocket</div><div class="ae-feed-item__sub">Based on 2 of 3 sessions</div></span><span class="ae-tc">10:52</span></div>
<div class="ae-feed-item"><span class="ae-feed-item__icon ae-feed-item__icon--warn">{i("clock")}</span><span><div class="ae-feed-item__title">onboarding.aeroapp.ai goes offline in 2 days</div><div class="ae-feed-item__sub">Free sites stay live 7 days</div></span>{btn("Keep it live","secondary",size="sm")}</div></div></div>'''
def test_row(t):
    st = {"Review ready": tag("Review ready","review"), "1 session": tag("1 session","line"), "Link shared": tag("Link shared","test")}[t["state"]]
    new = f'<span class="ae-test-row__new">{t["new"]} new</span>' if t["new"] else f'<span class="ae-tc">{t["sessions"]} sessions</span>'
    return f'<div class="ae-test-row"><span><div class="ae-test-row__name">{t["name"]}</div><div class="ae-test-row__sub">{t["site"]}</div></span><span class="ae-test-row__sub">{t["tasks"] or "No"} tasks · {t["kind"]}</span>{new}{st}{i("right","ae-i--sm")}</div>'
rows = f'<div class="ae-list--card"><div class="ae-listhead" style="grid-template-columns:minmax(0,2.2fr) minmax(0,1.3fr) 110px 120px 28px"><span>Test</span><span>Tasks</span><span>Sessions</span><span>Status</span><span></span></div><div class="ae-list">{"".join(test_row(t) for t in S["tests"])}</div></div>'
def srow(s):
    st = {"ready": status("Ready","ready"), "processing": status("Transcript arriving","processing"), "recording": status("Recording now","recording"), "noaudio": status("No audio","noaudio")}[s["status"]]
    q = f'<span class="ae-session-row__quote">“{E(s["quote"])}”</span>' if s["quote"] else '<span class="ae-session-row__quote is-muted">Transcript arriving, usually about a minute</span>'
    return f'<div class="ae-session-row"><span class="ae-session-row__n">Session {s["n"]}</span><span class="ae-session-row__who">{avatar(s["who"][-1], s["av"])}<span style="min-width:0"><div class="ae-session-row__name">{s["who"]}</div><div class="ae-session-row__dev">{s["dev"]}</div></span></span>{q}<span class="ae-tc">{s["len"]}</span>{st}</div>'
extra_s = [{"n": 4, "who": "Tester D", "av": "d", "dev": "Laptop · Safari", "len": "02:10", "status": "recording", "quote": "", "fr": 0}, {"n": 5, "who": "Tester E", "av": "e", "dev": "Laptop · Chrome", "len": "03:31", "status": "noaudio", "quote": "", "fr": 0}]
srows = f'<div class="ae-list--card"><div class="ae-list">{"".join(srow(s) for s in S["sessions"])}{srow(extra_s[0]).replace("Transcript arriving, usually about a minute","Recording now · the tester is still going")}{srow(extra_s[1]).replace("Transcript arriving, usually about a minute","Screen only, the tester turned off their mic")}</div></div>'
def site_card(s):
    st = {"live": status("Live","live"), "soon": status(f'Offline in {s["days"]} days',"soon"), "offline": status("Offline","offline")}[s["status"]]
    off = " is-offline" if s["status"] == "offline" else ""
    act = btn("Run a test","ghost",size="sm",icon="tests") if s["status"] != "offline" else btn("Put back online","ghost",size="sm")
    return f'<div class="ae-site-card{off}"><div class="ae-site-card__thumb">{thumb(s)}</div><div class="ae-site-card__body"><div class="ae-site-card__url">{s["slug"]}.aeroapp.ai</div><div class="ae-site-card__meta">{st}<span class="ae-sep"></span>v{s["ver"]} · {s["when"]}</div></div><div class="ae-site-card__foot">{tag(s["how"],"line")}<span class="ae-spacer"></span>{act}</div></div>'
cards = f'<div class="ae-grid ae-grid--3">{"".join(site_card(s) for s in S["sites"])}</div>'
vers = f'''<div class="ae-list--card"><div class="ae-list"><div class="ae-version is-live"><span class="ae-version__n">v4</span><span><div class="ae-strong" style="font-size:13px">Published from Claude</div><div class="ae-small">Today 10:03 · 6 files</div></span>{status("Live","live")}{btn("","ghost",size="sm",icon="more",extra="ae-btn--icon")}</div><div class="ae-version"><span class="ae-version__n">v3</span><span><div class="ae-strong" style="font-size:13px">Published from Claude</div><div class="ae-small">Yesterday 17:40 · 6 files</div></span><span class="ae-tc">Pinned to test</span>{btn("Roll back","secondary",size="sm",icon="undo")}</div></div></div>'''
ls = (cell(".ae-feed-item", feed, " what's new") + cell(".ae-test-row", rows) + cell(".ae-site-card", cards, " live · soon · offline")
      + cell(".ae-session-row", srows, " every status, numbered oldest first") + cell(".ae-version", vers))
out.append(sec("c-lists", "Lists and cards", "Each row answers one question: is there anything new, and where do I go next.", f'<div class="c-grid" style="--n:2">{ls}</div>'))

# ---------------- review
rv = (cell(".ae-player", f'<div data-demo="session">{player(0.435, glass_float=False)}</div><p class="ae-small" style="margin:0">Inline at the top of a session. Diamonds mark friction points, ticks mark task changes, the blue head is the playhead. No cursor on the stage: tab recordings don\'t show one.</p>', "", "", "Proposed: inline")
      + cell(".ae-player--voice", f'<div class="ae-player ae-player--voice"><div class="ae-player__stage"><div class="ae-wave">{"".join(f"<i class=\"{"on" if k<30 else ""}\" style=\"height:{8+abs(((k*37)%29)-14)*2.4:.0f}px\"></i>" for k in range(64))}</div><div class="ae-player__chips"><span class="ae-player__chip">{i("phone","ae-i--sm")}Phone · voice only</span></div></div><div class="ae-player__bar"><button class="ae-play">{i("play")}</button><span class="ae-player__time"><b>02:10</b> / 04:55</span>{scrub(.44,(120,200),295,())}</div></div><p class="ae-small" style="margin:0">Figma on a phone records voice only. Show it honestly as audio.</p>')
      + cell(".ae-transcript / .ae-tline", f'<div data-demo="session">{transcript(5, True, upto=7)}<div style="display:none"><button class="ae-play"></button></div></div><p class="ae-small" style="margin:0">Click a line to jump. While the audio plays, heard words turn ink and the current word is held in blue. Friction lines carry the marker.</p>')
      + cell(".ae-friction", f'{friction(FRICTION[0], True, True)}{friction(FRICTION[1])}')
      + cell(".ae-quote", f'<p class="ae-quote">“I thought my cards would be on the home screen. <mark>Is it under More?</mark>”</p><div class="ae-quote__by">{avatar("B","b","sm")}Tester B · Session 2 · <span class="ae-tc">03:08</span></div><p class="ae-small" style="margin:0">From C: their words, set large, with the marker on the part that matters.</p>')
      + cell(".ae-prio / .ae-theme", f'<div class="ae-label">What to fix first</div>{prio_list(PRIOS)}<div class="ae-label" style="margin-top:6px">Themes across sessions</div><div>{themes([("Cards hard to find",3,3),("Back from Send unclear",2,3),("Balance looks tappable",1,3)])}</div>')
      + cell(".ae-source", source_line(), " where it comes from"))
out.append(sec("c-review", "Review", "The recording, the transcript, and what came out of it, each jumping to its moment.", f'<div class="c-grid">{rv}</div>'))

# ---------------- feedback
skel = '<div class="ae-stack"><span class="ae-skel ae-skel--title"></span><span class="ae-skel ae-skel--text" style="width:90%"></span><span class="ae-skel ae-skel--text" style="width:70%"></span><div class="c-row"><span class="ae-skel ae-skel--circle" style="width:26px;height:26px"></span><span class="ae-skel ae-skel--text" style="flex:1"></span></div></div>'
fb = (cell(".ae-skel", skel + '<p class="ae-small" style="margin:0">Every page opens on its real header and the shapes of its rows. Never blank, never "0 sessions" before the count has loaded.</p>')
      + cell(".ae-empty", f'<div class="ae-empty"><div class="ae-h3" style="font-weight:450;font-size:17px">No sessions yet</div><div class="ae-empty__text">Share your link. Sessions appear here as testers finish, and the transcript follows about a minute later.</div><div class="ae-empty__actions">{btn("Copy link","primary",True,icon="copy")}{btn("Open as a tester","secondary",icon="out")}</div></div>')
      + cell(".ae-guide", f'<div class="ae-guide"><div class="ae-guide__head">{i("book")}How the transcript is made</div><ol><li>The tester\'s voice is recorded with their screen.</li><li>When they finish, the audio is transcribed, with a time for every word.</li><li>The summary and friction points are written from that transcript. Quotes are their exact words.</li></ol><a class="ae-link ae-small">More on how it works</a></div><div class="ae-guide ae-guide--closed"><span class="ae-guide__head">{i("book")}How the review is made</span><span class="ae-spacer"></span>{i("down","ae-i--sm")}</div>')
      + cell(".ae-callout", f'<div class="ae-callout ae-callout--info">{i("info")}<span>Testers pick the tab to share. Ask them to choose the Pocket tab.</span></div><div class="ae-callout ae-callout--warn">{i("clock")}<span><b>Offline in 2 days.</b> Free sites stay live 7 days.</span><span class="ae-callout__act">{btn("Keep it live","secondary",size="sm")}</span></div><div class="ae-callout ae-callout--bad">{i("alert")}<span><b>The review didn\'t finish.</b> The summary service timed out. Your sessions are safe.</span><span class="ae-callout__act">{btn("Try again","secondary",size="sm")}</span></div>')
      + cell(".ae-toast / .ae-menu", f'<span class="ae-toast">{i("check")}Link copied</span><div class="ae-menu"><div class="ae-menu__item">{i("out")}Open site</div><div class="ae-menu__item">{i("tests")}Run a test on this site</div><div class="ae-menu__item">{i("copy")}Copy address</div><div class="ae-menu__sep"></div><div class="ae-menu__item ae-menu__item--bad">{i("trash")}Delete site</div></div>')
      + cell(".ae-modal", f'<div class="ae-modal"><div class="ae-modal__head"><span class="ae-h3" style="flex:1">Roll back to v3?</span>{btn("","ghost",size="sm",icon="x",extra="ae-btn--icon")}</div><div class="ae-modal__body"><p class="ae-p">pocket.aeroapp.ai will show v3 straight away. v4 stays in your history, so you can switch back.</p></div><div class="ae-modal__foot">{btn("Cancel","ghost")}{btn("Roll back","primary",True)}</div></div>'))
out.append(sec("c-feedback", "Feedback", "Loading, empty, guidance, warnings, errors. Errors say what happened, what is safe, and what to do.", f'<div class="c-grid">{fb}</div>'))

# ---------------- plans
def plan(name, price, items, pick=False, cta="Start 7-day trial"):
    li = "".join(f'<li>{i("check")}{E(x)}</li>' for x in items)
    p = f'<small>a month</small>' if price != "$0" else ""
    return f'<div class="ae-plan{" is-pick" if pick else ""}"><div class="ae-plan__name">{name}{tag("Suggested","blue") if pick else ""}</div><div class="ae-plan__price">{price}{p}</div><ul>{li}</ul>{btn(cta, "primary" if pick else "secondary", pick, extra="ae-btn--block")}</div>'
pl = (plan("Free", "$0", ["3 test sessions, recordings included", "Sites stay live 7 days"], cta="Current plan").replace('ae-btn ae-btn--secondary', 'ae-btn ae-btn--secondary is-disabled')
      + plan("Basic", "$3", ["5 test sessions", "Your own aeroapp.ai address", "Password protection", "Custom favicon, no Aero badge"], True)
      + plan("Solo", "$6", ["10 test sessions", "Everything in Basic", "Custom domain", "Site analytics"])
      + plan("Pro", "$19", ["20 test sessions", "Everything in Solo", "Priority support"]))
out.append(sec("c-plans", ".ae-plan", "Only facts from PRICING-FACTS.md. Every paid plan: 7-day free trial, monthly, cancel any time. Session counts never say \"a month\".", f'<div class="c-grid" style="--n:4">{pl}</div>'))

# ---------------- tester
bgs = [("Black", "#0B0B0D"), ("White", "#FFFFFF"), ("Bright", "linear-gradient(135deg,#FF3D7F,#FFD500)"), ("Busy", "repeating-linear-gradient(45deg,#1D1D1F 0 14px,#FFE14D 14px 28px),#fff")]
tp = "".join(cell(f".ae-taskpanel over {n.lower()}", f'<div class="over" style="background:{bg};min-height:200px;padding:16px"><div class="ae-taskpanel" style="width:100%"><div class="ae-taskpanel__top"><span class="ae-label">Task 2 of 2</span><span class="ae-spacer"></span><span class="ae-rec">03:08</span></div><div class="ae-taskpanel__task">Find your cards</div><div class="c-row">{btn("Done","primary",True,size="sm")}{btn("Skip","ghost",size="sm")}</div></div></div>') for n, bg in bgs)
out.append(sec("c-tester", "Tester pieces (shared with the tester flow)", "Base task panel and recording indicator. The tester designer owns the flow; this is the starting piece. Over any colour it stays legible because the plate is 92% opaque with a blur, and the edge is two hairlines (dark outside, light inside), so it reads on black, white, bright and busy screens.", f'<div class="c-grid" style="--n:4">{tp}</div>'))

# ---------------- outside
oc = cell(".ae-outside", f'<div class="ae-outside-label">Outside Aero · Claude</div><div class="ae-outside"><div class="ae-outside__bar"><span class="ae-outside__logo"></span>Claude</div><div class="ae-outside__me">Put this prototype online with Aero and set up a test. Tasks: send £20 to Sam, find your cards.</div><div class="ae-outside__tool">Used Aero: publish_site, create_test</div><div class="ae-outside__bot">It\'s live at pocket.aeroapp.ai. Your test link is pocket.aeroapp.ai/t/8kq2.</div></div>', "", "", "")
out.append(sec("c-outside", "Outside Aero", "When a flow crosses into Claude or ChatGPT, it is drawn simplified, in its own colours and type, and labelled. Never in Aero’s components.", f'<div class="c-grid" style="--n:2">{oc}{cell("Rule", "<p class=\"ae-small\" style=\"margin:0\">Aero never imitates another app’s UI inside its own frame. The flows show Claude as a separate step, with an \"Outside Aero\" label, before coming back to Aero.</p>")}</div>'))

html_out = page("components.html", "Aero components", "Tokens and component sheet for the Aero app UI round.", "".join(out))
open("components.html", "w").write(html_out)
print("components.html", len(html_out))
