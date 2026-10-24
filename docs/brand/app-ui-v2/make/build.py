"""Team 2 (make), Aero app UI round v2. Builds pages.html.
Links the shared stylesheet ../shared/aero.css (Team 1) and our own extra.css.
All names and numbers are example data: Kestrel Studio, Mia Chen, testers Maya, Tom, Priya, Jonas, Ana, Leo."""
import pathlib, re

H = pathlib.Path(__file__).resolve().parent
SH = H.parent / 'shared'


def logo_svg(name, cls):
    s = (SH / name).read_text().strip()
    s = s.replace('fill="#1D1D1F"', 'fill="currentColor"')
    return s.replace('<svg ', f'<svg class="{cls}" aria-hidden="true" ', 1)


LOCKUP = lambda cls='lockup': logo_svg('lockup.svg', cls)
MARK = lambda cls='mark': logo_svg('mark.svg', cls)

I = {
    'home': '<path d="M2.5 7 8 2.5 13.5 7v6.5h-4v-4h-3v4h-4z"/>',
    'site': '<rect x="2" y="3" width="12" height="10" rx="2"/><path d="M2 6h12"/>',
    'test': '<circle cx="8" cy="8" r="5.5"/><circle cx="8" cy="8" r="2"/>',
    'plus': '<path d="M8 3v10M3 8h10"/>',
    'link': '<path d="M7 9.5a2.5 2.5 0 0 0 3.5 0l2-2a2.5 2.5 0 0 0-3.5-3.5l-.6.6M9 6.5a2.5 2.5 0 0 0-3.5 0l-2 2A2.5 2.5 0 0 0 7 12l.6-.6"/>',
    'file': '<path d="M4 2h5l3 3v9H4z"/><path d="M9 2v3h3"/>',
    'folder': '<path d="M2 4.5h4l1.5 1.5H14v7H2z"/>',
    'search': '<circle cx="7" cy="7" r="4"/><path d="m10 10 3 3"/>',
    'copy': '<rect x="5" y="5" width="8" height="8" rx="1.5"/><path d="M3 10V4a1 1 0 0 1 1-1h6"/>',
    'mic': '<rect x="6" y="2" width="4" height="8" rx="2"/><path d="M3.5 8a4.5 4.5 0 0 0 9 0M8 12.5V14"/>',
    'check': '<path d="m3.5 8.5 3 3 6-7"/>',
    'arrow': '<path d="M3 8h10M9 4l4 4-4 4"/>',
    'right': '<path d="m6 3 5 5-5 5"/>',
    'left': '<path d="M10 3 5 8l5 5"/>',
    'lock': '<rect x="3.5" y="7" width="9" height="6.5" rx="1.5"/><path d="M5.5 7V5a2.5 2.5 0 0 1 5 0v2"/>',
    'ext': '<path d="M9 3h4v4M13 3 7.5 8.5M12 9.5V13H3V4h3.5"/>',
    'down': '<path d="M8 2.5v8M4.5 7 8 10.5 11.5 7M3 13.5h10"/>',
    'up': '<path d="M8 13.5v-8M4.5 9 8 5.5 11.5 9M3 2.5h10"/>',
    'book': '<path d="M3 3h4a1.5 1.5 0 0 1 1.5 1.5V13A1.5 1.5 0 0 0 7 11.5H3zM13 3H9.5A1.5 1.5 0 0 0 8 4.5"/><path d="M13 3v8.5H9.5"/>',
    'undo': '<path d="M5 6H10a3 3 0 0 1 0 6H6"/><path d="M7 3.5 4.5 6 7 8.5"/>',
    'tab': '<rect x="1.5" y="3" width="13" height="10" rx="1.6"/><path d="M1.5 6h13M5 3v3"/>',
    'play': '<path d="m5.5 3.5 7 4.5-7 4.5z"/>',
    'chev': '<path d="m5 6.5 3 3 3-3"/>',
    'side': '<rect x="2" y="2.5" width="12" height="11" rx="2"/><path d="M6 2.5v11"/>',
    'globe': '<circle cx="8" cy="8" r="5.8"/><path d="M2.2 8h11.6M8 2.2c1.8 1.7 2.6 3.6 2.6 5.8S9.8 12.1 8 13.8C6.2 12.1 5.4 10.2 5.4 8S6.2 3.9 8 2.2z"/>',
    'image': '<rect x="2" y="3" width="12" height="10" rx="2"/><circle cx="6" cy="6.5" r="1.2"/><path d="m2.5 12 3.5-3.5 2.5 2.5 2-2 3 3"/>',
    'figma': '<path d="M6 2h2v4H6a2 2 0 0 1 0-4zM8 2h2a2 2 0 0 1 0 4H8zM6 6h2v4H6a2 2 0 0 1 0-4zM10 6a2 2 0 1 1 0 4 2 2 0 0 1 0-4zM6 10h2v2a2 2 0 1 1-2-2z"/>',
    'prompt': '<rect x="1.5" y="3" width="13" height="10" rx="2"/><path d="m4.5 6.5 2 1.5-2 1.5M8 10h3.5"/>',
    'more': '<circle cx="4" cy="8" r=".9"/><circle cx="8" cy="8" r=".9"/><circle cx="12" cy="8" r=".9"/>',
    'user': '<circle cx="8" cy="5.5" r="2.6"/><path d="M3 13.5c.6-2.4 2.6-3.8 5-3.8s4.4 1.4 5 3.8"/>',
    'chart': '<path d="M2.5 13.5h11M4.5 11V8M8 11V4.5M11.5 11V6.5"/>',
    'pen': '<path d="M10.5 2.5 13.5 5.5 6 13H3v-3z"/>',
    'drag': '<circle cx="6" cy="4" r=".9"/><circle cx="10" cy="4" r=".9"/><circle cx="6" cy="8" r=".9"/><circle cx="10" cy="8" r=".9"/><circle cx="6" cy="12" r=".9"/><circle cx="10" cy="12" r=".9"/>',
    'x': '<path d="m4 4 8 8M12 4l-8 8"/>',
    'pause': '<path d="M6 4v8M10 4v8"/>',
    'up2': '<path d="m4.5 10 3.5-3.5 3.5 3.5"/>',
    'sun': '<circle cx="8" cy="8" r="3"/><path d="M8 1.5v1.5M8 13v1.5M1.5 8H3M13 8h1.5M3.4 3.4l1 1M11.6 11.6l1 1M3.4 12.6l1-1M11.6 4.4l1-1"/>',
}


def ic(name, cls='i'):
    return f'<svg class="{cls}" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{I[name]}</svg>'


def gbtn(label, icon=None, cls=''):
    return f'<span class="gbtn {cls}">{ic(icon) if icon else ""}{label}</span>'


THEME = ['light']


def btn(label, kind='primary', size='sm', icon=None, cls=''):
    dark = THEME[0] == 'dark'
    if kind == 'primary':
        attr = f'data-glass-v3="primary" data-fill="{"#F2F2F4" if dark else "#1D1D1F"}"'
    else:
        attr = f'data-glass-v3="{"dark" if dark else "secondary"}"'
    return f'<span class="btn g3 {size} {cls}" {attr}>{ic(icon) if icon else ""}{label}</span>'


def sdots(pattern, cls=''):
    return f'<span class="sdots {cls}">' + ''.join(f'<i class="{p}"></i>' for p in pattern) + '</span>'


def ex(t='Example'):
    return f'<span class="ex">{t}</span>'


# ---------------------------------------------------------------- example data
STUDIO, OWNER = 'Kestrel Studio', 'Mia Chen'
QUOTE = 'I thought my cards would be on the home screen. Is it under More?'


# ---------------------------------------------------------------- prototypes (real content, drawn small)
def pocket(sheet=False):
    acts = [('Send', '<path d="M5 11 11 5M6 5h5v5"/>'), ('Request', '<path d="M11 5 5 11M10 11H5V6"/>'),
            ('Top up', '<path d="M8 4v8M4 8h8"/>'), ('More', '<circle cx="4" cy="8" r=".8"/><circle cx="8" cy="8" r=".8"/><circle cx="12" cy="8" r=".8"/>')]
    a = ''.join(f'<div><i><svg viewBox="0 0 16 16">{p}</svg></i>{n}</div>' for n, p in acts)
    rows = [('#FFE1D2', 'Coffee Lab', 'Today', '−£4.20'), ('#D7F0E2', 'Salary', 'Mon', '+£2,100.00'), ('#DCE8FF', 'Rail ticket', 'Sun', '−£12.80'), ('#EFE6FF', 'Bookshop', 'Sat', '−£18.00')]
    r = ''.join(f'<div class="ph-row"><i style="background:{c}"></i><div><b>{n}</b><small>{d}</small></div><b>{v}</b></div>' for c, n, d, v in rows)
    return f'''<div class="ph{' s-sheet' if sheet else ''}"><div class="ph-scr"><div class="ph-home">
<div class="ph-status"><span>9:41</span><span>●●●</span></div>
<div class="ph-hi"><span class="pa">S</span><div><small>Good morning</small><b>Sam</b></div></div>
<div class="ph-bal"><small>Balance</small><b>£1,240.50</b><span>+£86.20 this week</span></div>
<div class="ph-acts">{a}</div><div class="ph-sec">Recent<span>See all</span></div>{r}
<div class="ph-tab"><span class="on">Home</span><span>Activity</span><span>Profile</span></div></div>
<div class="ph-scrim"></div><div class="ph-sheet"><div class="hd"></div><div class="ph-sec">More<span></span></div>
<div class="sr k"><i></i><b>Cards</b></div><div class="sr"><i></i>Statements</div><div class="sr"><i></i>Savings pots</div><div class="sr"><i></i>Help</div></div>
</div></div>'''


def onboarding():
    return '''<div class="ob"><div class="ph-status" style="padding:0 4px"><span>9:41</span><span>●●●</span></div>
<div class="art"><i style="width:120px;height:120px;left:46px;top:30px;background:#8C88F5"></i><i style="width:70px;height:70px;left:120px;top:96px;background:#C9C6FF"></i><i style="width:34px;height:34px;left:30px;top:120px;background:#FFC9B5"></i></div>
<h5>Money, sorted.</h5><p>Send, split and save with friends. Set up takes about two minutes.</p>
<div class="dots"><i></i><i></i><i></i></div><div class="go">Get started</div></div>'''


def checkout():
    its = [('#FFE1D2', 'Linen tote', 'Natural · 1', '£28.00'), ('#D7F0E2', 'Field notebook', 'A5 · 2', '£14.00'), ('#DCE8FF', 'Pencil set', '6 pack', '£6.00')]
    it = ''.join(f'<div class="it"><i style="background:{c}"></i><div><b>{n}</b><small>{d}</small></div><b>{p}</b></div>' for c, n, d, p in its)
    return f'''<div class="co"><div class="top">Paper &amp; Co<span>Basket (3)</span></div><div class="cob"><div><h6>Checkout</h6>{it}
<div style="margin-top:14px" class="fld">Email</div><div class="fld">Card number</div></div>
<div class="sum"><div><span>Subtotal</span><span>£48.00</span></div><div><span>Delivery</span><span>Free</span></div><div class="tot"><span>Total</span><span>£48.00</span></div><div class="pay">Pay £48.00</div></div></div></div>'''


def folio():
    """Kestrel Studio's own portfolio site (a site that is only a site, with visits)."""
    tiles = ['#E9E2D6', '#1F2A44', '#F2B8A0', '#C9D8C5']
    t = ''.join(f'<i style="background:{c}"></i>' for c in tiles)
    return f'''<div class="pf"><div class="pf-top"><b>Kestrel</b><span>Work</span><span>About</span><span>Contact</span></div>
<h6>Product design for money, travel and health apps.</h6><p>A small studio in Leeds. Example.</p><div class="pf-grid">{t}</div></div>'''


def pitch():
    return '''<div class="pt"><div class="pt-k">Pocket · investor preview</div><h6>Everyday money, without the noise.</h6>
<div class="pt-row"><div><b>38k</b><small>waitlist</small></div><div><b>4.7</b><small>beta rating</small></div><div><b>£0</b><small>monthly fee</small></div></div></div>'''


def thumb(kind, w, h, scale=None, cls='', sheet=False, top=None):
    desk = kind in ('checkout', 'folio', 'pitch')
    if desk:
        s = scale or (w * .9 / 640)
        inner = {'checkout': checkout, 'folio': folio, 'pitch': pitch}[kind]()
    else:
        s = scale or (w * .62 / 226)
        inner = pocket(sheet) if kind == 'pocket' else onboarding()
    t = f'top:{top};' if top else ''
    return f'<div class="th {"desk" if desk else ""} {cls}" style="width:{w}px;height:{h}px"><div class="sc" style="{t}transform:translateX(-50%) scale({s:.3f})">{inner}</div></div>'


# ---------------------------------------------------------------- shell
def bar(url, tester=False):
    return f'<div class="win-bar"><span class="lights"><i></i><i></i><i></i></span><span class="win-url"><span>{ic("lock")}{url}</span></span><span class="sp"></span></div>'


def sidebar(active='Home', plan=('Solo plan', '8 of 10 test sessions', 80), counts=('4', '4'), one_site=None, one_test=None, tests=True):
    sc, tc = counts
    nav = f'<div class="nav-i {"on" if active == "Home" else ""}">{ic("home")}Home</div>'
    nav += f'<div class="nav-i {"on" if active == "Sites" else ""}">{ic("site")}Sites<span class="ct">{sc}</span></div>'
    if one_site:
        nav += f'<div class="x-sub {"on" if active == "one-site" else ""}"><span class="x-tw">{thumb(one_site[0], 22, 16, scale=.03 if one_site[0] in ("checkout", "folio") else .07, top="6%")}</span><span class="nm">{one_site[1]}</span><span class="st live x-dotonly"></span></div>'
    nav += f'<div class="nav-i {"on" if active == "Tests" else ""}">{ic("test")}Tests<span class="ct">{tc}</span></div>'
    if one_test:
        nav += f'<div class="x-sub {"on" if active == "one-test" else ""}"><span class="x-tw">{thumb(one_test[0], 22, 16, scale=.07, top="6%")}</span><span class="nm">{one_test[1]}</span><span class="t">{one_test[2]}</span></div>'
    pl, pu, pw = plan
    return f'''<aside class="side"><div class="ws"><span class="ic">{MARK()}</span><span class="wsn">{STUDIO}</span><span class="chev">{ic("chev")}</span><span class="collapse" title="Hide sidebar">{ic("side")}</span></div>
<div class="x-nav">{nav}</div>
<div class="use"><span>{pl}</span><span class="mono">{pu}</span><i><b style="width:{pw}%"></b></i></div>
<div class="nav-i" style="margin-top:2px">{ic("book")}How it works</div>
<div class="acct"><span class="av m">M</span>{OWNER}<span class="ex">Example</span></div></aside>'''


def window(url, side, main, h=900, cls=''):
    s = side if side else ''
    grid = '' if side else ' x-noside'
    return f'<div class="fitw"><div class="win full x-w {cls}">{bar(url)}<div class="app{grid}" style="--h:{h - 36}px">{s}<div class="main">{main}</div></div></div></div>'


def section(id_, num, title, idea, body):
    return f'<section class="xp" id="{id_}"><h2><span class="n">{num}</span>{title}</h2><p class="idea">{idea}</p>{body}</section>'


def both(render, label=''):
    """Every frame in light, then the same in dark."""
    lab = f'<b>{label}</b>' if label else ''
    THEME[0] = 'light'; a = render()
    THEME[0] = 'dark'; b = render()
    THEME[0] = 'light'
    return (f'<div class="x-pair"><div class="x-tl">{lab}<span>Light</span></div><div class="x-theme" data-theme="light">{a}</div>'
            f'<div class="x-tl">{lab}<span>Dark</span></div><div class="x-theme" data-theme="dark">{b}</div></div>')


def note(t, kind='Option'):
    return f'<div class="x-note"><b>{kind}</b>{t}</div>'


# ---------------------------------------------------------------- shared pieces
SITES = [  # key, name, address, version, source, status, visits, test
    ('folio', 'Kestrel portfolio', 'kestrel.studio', 'v12', 'HTML upload', 'live', '214', None),
    ('pocket', 'Pocket', 'pocket.aeroapp.ai', 'v4', 'From a prompt', 'live', '38', 'Pocket'),
    ('checkout', 'Checkout', 'checkout.aeroapp.ai', 'v8', 'HTML upload', 'live', '12', 'Checkout'),
    ('pitch', 'Pocket pitch', 'pocket-pitch.aeroapp.ai', 'v2', 'From a prompt', 'private', '5', None),
]


def site_block(k, name, addr, v, src, status, visits, test, big=False, free=None):
    if free:
        stw = f'<span class="st {"soon" if free.startswith("Offline") else "live"}">{free}</span>'
    elif status == 'private':
        stw = f'<span class="st priv">{ic("lock")}Private</span>'
    else:
        stw = '<span class="st live">Live</span>'
    sc = {'pocket': .5, 'checkout': .4, 'folio': .4, 'pitch': .4}[k]
    h = 150 if big else 128
    vis = f'<span class="x-vis">{ic("chart")}{visits} visits this week</span>' if visits and not free else ''
    tst = f'<span class="x-hast">{ic("test")}Test: {test}</span>' if test else ''
    return f'''<div class="sc2 x-site">{thumb(k, 400, h, scale=sc, top=("14%" if k != "pocket" else "10%"))}<div class="meta">
<span class="x-nm">{name}</span>{stw}<span class="addr">{addr}</span><span class="hw">{v} · {src}</span><span class="x-foot">{vis}{tst}</span></div></div>'''


TESTS = [  # key, name, source line, link, dots, count, last, status
    ('pocket', 'Pocket', 'Copy of pocket.aeroapp.ai, v4', 'aeroapp.ai/t/pocket-7k2', ['', '', '', '', 'no', 'pr'], '6 sessions', '09:41 today', 'new'),
    ('onboarding', 'Onboarding v2', 'Figma prototype, hosted in this test', 'aeroapp.ai/t/onboard-v2', ['', ''], '2 sessions', 'Yesterday', 'live'),
    ('checkout', 'Checkout', 'Copy of checkout.aeroapp.ai, v8', 'aeroapp.ai/t/checkout-4mq', [], 'No sessions yet', 'None yet', 'live'),
    ('onboarding', 'Sign-up flow', 'Figma prototype, hosted in this test', 'aeroapp.ai/t/signup-3', ['', '', '', ''], '4 sessions', 'Fri 17 Oct', 'closed'),
]


def test_line(k, name, src, link, dots, cnt, last, status, compact=False):
    st = {'new': '<span class="st new">2 new</span>', 'live': '<span class="st live">Open</span>', 'closed': '<span class="st">Closed</span>'}[status]
    d = sdots(dots) if dots else ''
    sc = .09 if k != 'checkout' else .05
    if compact:
        return f'''<div class="x-tline c">{thumb(k, 40, 32, scale=sc, top="8%")}<div class="x-tn"><b>{name}</b><small>{cnt} · {last}</small></div>{d}{st}</div>'''
    return f'''<div class="x-tline">{thumb(k, 64, 46, scale=sc * 1.5, top="8%")}<div class="x-tn"><b>{name}</b><small>{src}</small></div>
<span class="mono x-link">{link}</span><div class="x-ses">{d}<small>{cnt}</small></div><span class="x-mut">{last}</span>{st}</div>'''


# event rows for what's new: kind decides the mark on the timeline
def ev(time, kind, subject, text, act='', who=''):
    w = f'<span class="x-who">{who}</span>' if who else ''
    return f'''<div class="x-ev k-{kind}"><span class="x-t mono">{time}</span><span class="x-mk"></span>
<div class="x-evb"><div class="x-evh"><b>{subject}</b>{w}</div><div class="x-evt">{text}</div></div><div class="x-eva">{act}</div></div>'''


def av(l, name):
    return f'<span class="av {l}">{name[0]}</span>'


def timeline(compact=False):
    today = [
        ev('09:41', 'proc', 'Pocket', 'Leo finished a session. The transcript arrives in about a minute.', gbtn('Open'), av('f', 'Leo') + 'Leo'),
        ev('09:12', 'noaud', 'Pocket', 'Ana finished a session with no audio, so there is no transcript. You can still watch it.', gbtn('Watch'), av('e', 'Ana') + 'Ana'),
        ev('08:30', 'review', 'Pocket', 'Review ready across 4 sessions. Cards expected on the home screen, 4 of 4 testers.', gbtn('Review')),
        ev('08:20', 'pub', 'Checkout', 'Version 8 published at <span class="mono">checkout.aeroapp.ai</span>.', gbtn('Copy address', 'copy')),
    ]
    yest = [
        ev('18:00', 'visits', 'Kestrel portfolio', '31 visits yesterday, 214 this week. Most opened the Pocket case study.', gbtn('Visits')),
        ev('16:05', 'review', 'Onboarding v2', 'Review ready for 2 sessions. Both testers skipped the second screen.', gbtn('Review')),
        ev('11:22', 'ses', 'Onboarding v2', 'Jonas finished a session. 6 minutes, 2 friction points.', gbtn('Open'), av('d', 'Jonas') + 'Jonas'),
    ]
    mon = [ev('15:30', 'made', 'Pocket', 'Test made from <span class="mono">pocket.aeroapp.ai</span> v4, with its own link.', gbtn('Copy test link', 'copy')),
           ev('10:02', 'pub', 'Pocket', 'Version 4 published from Claude.', '')]
    if compact:
        yest = yest[:1]; mon = []
    m = f'<div class="x-day">Monday<span class="mono">20 Oct</span></div>{"".join(mon)}' if mon else ''
    return f'''<div class="x-tlw"><div class="x-day">Today<span class="mono">Wed 22 Oct</span></div>{"".join(today)}
<div class="x-day">Yesterday<span class="mono">Tue 21 Oct</span></div>{"".join(yest)}{m}</div>'''


# ---------------------------------------------------------------- m1 home
def home_main(layout='A'):
    head = f'''<div class="mhead"><span class="crumb"><b>Home</b></span><div class="r">{gbtn('', 'search', 'ic')}{gbtn('New test', 'plus')}{btn('New site', icon='plus')}</div></div>'''
    sites = ''.join(site_block(*s) for s in SITES[:3])
    if layout == 'A':
        sb = ''.join(f'''<div class="x-mini">{thumb(k, 150, 78, scale=(.21 if k != "pocket" else .3), top=("10%" if k != "pocket" else "8%"))}<div class="x-mm"><b>{n}</b><span class="addr">{a}</span>{"<span class='st live'>Live</span>" if s == "live" else "<span class='st priv'>" + ic("lock") + "Private</span>"}</div></div>''' for k, n, a, v, src, s, vis, t in SITES[:3])
        tl = ''.join(test_line(*t, compact=True) for t in TESTS[:3])
        body = f'''<div class="mbody"><div class="x-homeA"><div><div class="hh"><h3>What’s new</h3><span class="mono">since you looked, Wed 08:05</span><span class="r lnk">Mark all as seen</span></div>{timeline()}</div>
<div class="x-rc"><div class="hh"><h3>Sites</h3><span class="mono">4</span><span class="r lnk">All sites {ic("arrow")}</span></div><div class="x-mgrid">{sb}</div>
<div class="hh" style="margin-top:22px"><h3>Tests</h3><span class="mono">4</span><span class="r lnk">All tests {ic("arrow")}</span></div><div class="x-tlist c">{tl}</div></div></div></div>'''
    else:
        tl = ''.join(test_line(*t, compact=True) for t in TESTS[:4])
        body = f'''<div class="mbody"><div class="hh"><h3>Sites</h3><span class="mono">4</span><span class="r lnk">All sites {ic("arrow")}</span></div><div class="x-srow3">{sites}</div>
<div class="x-homeB"><div><div class="hh"><h3>What’s new</h3><span class="mono">since you looked, Wed 08:05</span></div>{timeline(compact=True)}</div>
<div><div class="hh"><h3>Tests</h3><span class="mono">4</span><span class="r lnk">All tests {ic("arrow")}</span></div><div class="x-tlist c">{tl}</div></div></div></div>'''
    return head + body


def m1():
    a = lambda: window('aeroapp.ai/home', sidebar('Home'), home_main('A'))
    b = lambda: window('aeroapp.ai/home', sidebar('Home'), home_main('B'))
    kinds = [('ses', 'Session arrived', 'Jonas finished a session.'), ('proc', 'Transcribing', 'Transcript in about a minute.'),
             ('noaud', 'No audio', 'You can still watch it.'), ('review', 'Review ready', '4 of 4 testers.'),
             ('pub', 'Published', 'Version 8 is live.'), ('made', 'Test made', 'A copy with its own link.'), ('visits', 'Site visits', '31 visits yesterday.'),
             ('soon', 'Offline soon (Free)', 'checkout.aeroapp.ai goes offline in 2 days.')]
    cat = ''.join(f'<div class="x-kind k-{k}"><span class="x-mk"></span><div><b>{t}</b><small>{d}</small></div></div>' for k, t, d in kinds)
    catalogue = f'''<div class="x-cat"><div class="x-cath"><b>Every kind of event, one mark each</b><span>The mark sits on the timeline line. No icon tiles, no coloured stripes.</span></div><div class="x-catg">{cat}</div></div>'''
    body = (f'<h3 class="x-sub-h">A · Timeline first, sites and tests beside it <span class="x-pick">I’d pick A</span></h3>' + both(a, 'Home A')
            + note('A puts what changed first, which is the reason to open Home. B leads with the sites row, which reads better for someone who mostly publishes and rarely tests. Both use the same timeline, blocks and lines, so it is a layout choice only.', 'Option')
            + '<h3 class="x-sub-h">B · Sites row on top, timeline and tests below</h3>' + both(b, 'Home B')
            + '<h3 class="x-sub-h">The event kinds</h3>' + both(lambda: catalogue, 'Events'))
    return section('m1', '01', 'Home', 'What’s new is a plain timeline of events, newest first: sessions arriving, reviews ready, sites published, visits, and a Free site about to go offline. Sites sit beside it as preview blocks, tests as status lines.', body)


# ---------------------------------------------------------------- m2 first run
def first_run():
    ways = [('up', 'Upload HTML or a zip', 'A folder or zip with index.html at the top. Live in seconds.'),
            ('prompt', 'A prompt for Claude or ChatGPT', 'Built it in a chat? Copy one prompt into that chat and it publishes here.'),
            ('figma', 'A Figma prototype link', 'Paste the share link. Flows and transitions work as in Figma.')]
    w = ''.join(f'<div class="x-way">{ic(i)}<div><b>{t}</b><small>{d}</small></div>{ic("right", "i x-go")}</div>' for i, t, d in ways)
    steps = [('01', 'Publish', 'Your site appears here as a preview, with its address.', 'Seconds after you add it'),
             ('02', 'Test', 'Send one link. Each person who takes the test shows up by name.', 'As soon as someone finishes'),
             ('03', 'Review', 'A summary and the friction points, in their own words.', 'About a minute after each session')]
    s = ''.join(f'<div class="x-step"><span class="mono">{n}</span><b>{t}</b><p>{d}</p><span class="x-when">{ic("chev")}{w_}</span><div class="x-ghost g{n}"></div></div>' for n, t, d, w_ in steps)
    main = f'''<div class="mhead"><span class="crumb"><b>Home</b></span></div><div class="mbody"><div class="x-fr">
<div class="x-frl"><h3>Put something online<span class="d">.</span></h3><p class="x-lead">Then share one link and watch people use it. Start from what you have.</p>
<div class="x-ways">{w}</div>
<div class="x-steps">{s}</div></div>
<div class="x-frr"><div class="x-exc">{thumb('pocket', 300, 168, scale=.5, top='8%')}<div class="x-exb"><span class="ex">Example study</span><h4>Pocket, after 6 sessions</h4>
<p>See a finished review before you invite anyone: the sessions, what each tester said, and what to fix first.</p>{btn('Open the example', 'secondary', 'md', 'arrow')}</div></div>
<div class="plannote">Free plan: 3 test sessions, and sites stay live for 7 days. Paid plans from $3.</div></div></div></div>'''
    return window('aeroapp.ai/home', sidebar('Home', plan=('Free plan', '0 of 3 test sessions', 0), counts=('', '')), main)


def one_site():
    main = f'''<div class="mhead"><span class="crumb"><b>Home</b></span><div class="r">{gbtn('New test', 'plus')}{btn('New site', 'secondary', icon='plus')}</div></div><div class="mbody"><div class="x-one">
<div>{site_block('checkout', 'Checkout', 'checkout.aeroapp.ai', 'v1', 'HTML upload', 'live', '', None, big=True, free='Live · 7 days left')}
<div class="x-tlw sm" style="margin-top:22px"><div class="x-day">Today</div>{ev('10:02', 'pub', 'Checkout', 'Version 1 published at <span class="mono">checkout.aeroapp.ai</span>.')}</div></div>
<div class="x-next"><span class="ex">Next</span><h4>Watch someone use it</h4><p>“Test this site” makes a copy with its own test link. Send that link; people share their screen and voice while they try it. Your live site doesn’t change.</p>
{btn('Test this site', size='md', icon='arrow')}<div class="x-nextg"><div class="x-ghost g02"></div><small>Sessions appear here, with each tester’s name.</small></div>
<div class="x-or">Not ready to test? {gbtn('Open the example')}</div></div></div></div>'''
    return window('aeroapp.ai/home', sidebar('Home', plan=('Free plan', '0 of 3 test sessions', 0), counts=('', ''), one_site=('checkout', 'Checkout')), main, h=700)


def one_test():
    main = f'''<div class="mhead"><span class="crumb"><b>Home</b></span><div class="r">{gbtn('New test', 'plus')}{btn('New site', 'secondary', icon='plus')}</div></div><div class="mbody"><div class="x-one">
<div class="x-otest">{thumb('onboarding', 150, 150, scale=.5, top='6%')}<div><span class="ex">Test</span><h4>Onboarding v2</h4><div class="x-mut" style="margin-bottom:12px">Figma prototype, hosted in this test · 2 tasks</div>
<div class="prompt x-linkrow"><span class="mono">aeroapp.ai/t/onboard-v2</span>{btn('Copy link', icon='copy')}</div>
<div style="display:flex;gap:8px;margin-top:10px">{gbtn('Open as tester', 'ext')}{gbtn('Edit tasks', 'pen')}</div></div></div>
<div class="x-next"><span class="ex">Waiting for the first session</span><h4>What happens next</h4>
<div class="x-wait"><div><span class="x-mk k-ses"></span><b>Someone opens the link</b><small>They type a first name if they like, then share the tab and microphone.</small></div>
<div><span class="x-mk k-proc"></span><b>They finish</b><small>The session lands here straight away, with their name.</small></div>
<div><span class="x-mk k-review"></span><b>About a minute later</b><small>The transcript, a summary and the friction points.</small></div></div>
<div class="x-or"><span>Try it yourself first: “Open as tester” records you as <b>You</b>.</span></div></div></div></div>'''
    return window('aeroapp.ai/home', sidebar('Home', plan=('Free plan', '0 of 3 test sessions', 0), counts=('', ''), one_test=('onboarding', 'Onboarding v2', '0')), main, h=700)


def m2():
    body = (both(first_run, 'Nothing yet')
            + note('The three steps are not cards to click: each says what will appear and when, with a faint shape of it. The only actions are the three ways in and the example. “Open the example” is secondary on purpose: the main job is to put something online.', 'Why')
            + '<h3 class="x-sub-h">Only one site: it sits in the sidebar under Sites</h3>' + both(one_site, 'One site')
            + '<h3 class="x-sub-h">Only one test: it sits in the sidebar under Tests</h3>' + both(one_test, 'One test'))
    return section('m2', '02', 'First run', 'Nothing yet: teach Publish, Test, Review by saying what appears and when, offer the three ways in, and “Open the example” for a finished review. With one site or one test, the item sits in the sidebar and Home points to the next step.', body)


# ---------------------------------------------------------------- m3 lists
def sites_list():
    blocks = ''.join(site_block(*s) for s in SITES)
    blocks += f'<div class="x-dropt">{ic("up")}<b>Drop a folder or zip</b><span>to publish a new site</span><span class="x-or2">or {gbtn("New site", "plus")}</span></div>'
    main = f'''<div class="mhead"><span class="crumb"><b>Sites</b></span><div class="r">{gbtn('', 'search', 'ic')}{btn('New site', icon='plus')}</div></div>
<div class="x-filt"><span class="on">All <i>4</i></span><span>Live <i>3</i></span><span>Private <i>1</i></span><span class="r">Newest first {ic("chev")}</span></div>
<div class="mbody"><div class="x-sgrid">{blocks}</div>
<p class="x-foot2">Previews are a screenshot of each site’s home page, taken when it was published.</p></div>'''
    return window('aeroapp.ai/sites', sidebar('Sites'), main, h=780)


def free_strip():
    b = [site_block('checkout', 'Checkout', 'checkout.aeroapp.ai', 'v2', 'HTML upload', 'live', '', None, free='Live · 5 days left'),
         site_block('pocket', 'Pocket', 'pocket.aeroapp.ai', 'v1', 'From a prompt', 'live', '', None, free='Offline in 2 days'),
         site_block('pitch', 'Pocket pitch', 'pocket-pitch.aeroapp.ai', 'v1', 'From a prompt', 'live', '', None, free='Offline')]
    b[2] = b[2].replace('class="sc2 x-site"', 'class="sc2 x-site x-off"')
    return f'''<div class="x-freew"><div class="x-freeh"><b>On the Free plan</b><span>Sites stay live 7 days. The status says when a site goes offline; an offline site keeps its address and versions.</span>{gbtn("See plans")}</div><div class="x-sgrid three">{"".join(b)}</div></div>'''


def tests_list():
    rows = ''.join(test_line(*t) for t in TESTS)
    main = f'''<div class="mhead"><span class="crumb"><b>Tests</b></span><div class="r">{gbtn('', 'search', 'ic')}{btn('New test', icon='plus')}</div></div>
<div class="x-filt"><span class="on">All <i>4</i></span><span>Open <i>3</i></span><span>Closed <i>1</i></span><span class="r">Last session first {ic("chev")}</span></div>
<div class="mbody"><div class="x-thd"><span></span><span>Test</span><span>Test link</span><span>Sessions</span><span>Last session</span><span>Status</span></div><div class="x-tlist">{rows}</div>
<div class="legend">{sdots([''])} ready {sdots(['pr'])} transcribing {sdots(['no'])} no audio</div></div>'''
    return window('aeroapp.ai/tests', sidebar('Tests'), main, h=640)


def m3():
    body = (both(sites_list, 'Sites') + both(free_strip, 'Sites on Free')
            + note('A test’s preview is small on purpose: the line is about sessions and status, the picture only helps you find it. “Open” means the link accepts sessions; “Closed” stops new ones and keeps the history.', 'Why')
            + both(tests_list, 'Tests'))
    return section('m3', '03', 'Sites and tests lists', 'Sites are blocks with a real preview (a cached screenshot of the page) and say Live, Private or, on Free, how long until offline. Tests are status lines: sessions as dots, the last one, open or closed, with a small preview.', body)


# ---------------------------------------------------------------- m4 site page
def switch(on=True):
    return f'<span class="x-sw {"on" if on else ""}"><i></i></span>'


def site_page():
    vers = [('v8', 'checkout-v8.zip · 17 files', 'Today, 08:20', True), ('v7', 'checkout-v7.zip · 16 files', 'Mon 20 Oct', False),
            ('v6', 'index.html', 'Fri 17 Oct', False), ('v5', 'checkout-v5.zip · 15 files', 'Thu 16 Oct', False)]
    vr = ''.join(f'<div class="x-ver"><span class="mono vv">{v}</span><span class="x-mut">{f}</span><span class="x-mut">{d}</span>{"<span class=\"st live\">Live</span><span></span>" if live else "<span></span>" + gbtn("Roll back", "undo")}</div>' for v, f, d, live in vers)
    main = f'''<div class="mhead"><span class="crumb">Sites {ic('right')} <b>Checkout</b></span><div class="r">{btn('Test this site', icon='test')}</div></div>
<div class="x-sp"><div class="x-spm">
<div class="x-prev"><div class="x-pbar"><span class="lights"><i></i><i></i><i></i></span><span class="mono">checkout.aeroapp.ai</span><span class="x-mut" style="margin-left:auto">Screenshot · v8 · today 08:20</span></div>{thumb('checkout', 760, 300, scale=1.1, top='4%')}</div>
<div class="x-addr"><span class="mono">checkout.aeroapp.ai</span><span class="st live">Live</span><span class="x-mut">Public: anyone with the address</span><span class="r">{gbtn('Copy', 'copy')}{gbtn('Visit', 'ext')}</span></div>
<div class="x-dropn">{ic('up')}<div><b>Drop a new version</b><small>A file, folder or zip. It goes live at the same address; the old one is kept.</small></div>{gbtn('Choose files')}</div>
<div class="hh" style="margin-top:20px"><h3>Versions</h3><span class="mono">8 · roll back to any of them, the address stays the same</span></div><div class="x-vers">{vr}</div></div>
<div class="x-sps">
<div class="x-set"><label>Name</label><div class="x-in">Checkout</div></div>
<div class="x-set"><div class="x-row"><div><b>Public</b><small>Anyone with the address can open it. Turn off to make it private.</small></div>{switch(True)}</div></div>
<div class="x-set"><label>Custom domain <span class="x-plan">Solo</span></label><div class="x-in x-pl">shop.kestrel.studio</div><small>Point a CNAME at <span class="mono">sites.aeroapp.ai</span>. {('<span class="lnk">How to</span>')}</small></div>
<div class="x-set"><label>Favicon <span class="x-plan">Basic</span></label><div class="x-row"><span class="x-fav">{MARK()}</span><small style="flex:1">Using the one in your upload. {('<span class="lnk">Replace</span>')}</small></div></div>
<div class="x-set"><div class="x-row"><div><b>Aero badge <span class="x-plan">Basic</span></b><small>A small “Made with Aero” link in the corner.</small></div>{switch(False)}</div></div>
<div class="x-set"><label>Visits <span class="x-plan">Solo</span></label><div class="x-visn"><b>12</b><small>this week</small><span class="x-spark">{"".join(f'<i style="height:{h}%"></i>' for h in (20, 35, 10, 55, 40, 80, 60))}</span></div></div>
<div class="x-set x-testit"><b>Test this site</b><p>Makes a copy of v8 with its own test link. Change the test without touching this site, and the other way round.</p>{gbtn('Test this site', 'arrow')}</div>
<div class="x-danger">Delete site</div>
</div></div>'''
    return window('aeroapp.ai/sites/checkout', sidebar('Sites'), main)


def m4():
    pop = f'''<div class="x-pop"><b>Test this site</b><p>Aero makes a copy of <span class="mono">checkout.aeroapp.ai</span> v8 as a new test, with its own link and its own versions.</p>
<ul><li>Update the site later and the test stays as it is.</li><li>Upload to the test and the live site stays as it is.</li></ul>
<div class="x-popa">{btn('Make the test', size='sm')}{gbtn('Cancel')}</div></div>'''
    body = (both(site_page, 'Site page')
            + note('Everything is on one page: no Overview, Versions, Domain and Settings tabs. The settings column is short enough to scan. Paid settings say their plan in small type and open the upgrade sheet when touched, rather than being hidden.', 'Why')
            + '<h3 class="x-sub-h">“Test this site”: what it says before it makes the copy</h3>' + both(lambda: f'<div class="x-popw">{pop}</div>', 'Popover'))
    return section('m4', '04', 'Site page', 'One page: the preview, the address with Copy and Visit, drop to publish a new version, versions with roll back, and the settings in a side column. “Test this site” says plainly that it makes a copy with its own link.', body)


# ---------------------------------------------------------------- m5 create
def rail(cur, src):
    """C Story’s done-steps, down the left of every create flow."""
    names = {'up': 'HTML or zip', 'prompt': 'A prompt', 'figma': 'Figma link'}
    add = {'up': 'Add the files', 'prompt': 'Copy the prompt into your chat', 'figma': 'Paste the link'}[src] if src else 'Add it'
    st = [('Where it’s from', names.get(src, '')), (add, ''), ('Live at an address', ''), ('Test it, if you like', '')]
    out = ''
    for k, (t, s) in enumerate(st):
        cls = 'done' if k < cur else ('cur' if k == cur else '')
        mark = ic('check') if k < cur else str(k + 1)
        ch = f'<span class="lnk">Change</span>' if k == 0 and src else ''
        out += f'<div class="x-rs {cls}"><span class="k">{mark}</span><div><b>{t}</b>{f"<small>{s}</small>" if s else ""}</div>{ch}</div>'
    return f'<div class="x-rail">{out}</div>'


def srcseg(src):
    o = [('up', 'Upload'), ('prompt', 'Prompt'), ('figma', 'Figma link')]
    return '<div class="seg x-seg">' + ''.join(f'<span class="{"on" if k == src else ""}">{ic(k)}{t}</span>' for k, t in o) + '</div>'


def create_head(src=None, title='New site'):
    seg = srcseg(src) if src else ''
    return f'<div class="mhead"><span class="crumb">Sites {ic("right")} <b>{title}</b></span>{seg}<div class="r">{gbtn("Cancel")}</div></div>'


def pick_page():
    ch = [('up', 'Upload HTML or a zip', 'A file, a folder or a zip with index.html at the top.', 'Live in seconds'),
          ('prompt', 'A prompt for Claude or ChatGPT', 'For something you built in a chat. You copy one prompt into that chat; it publishes here.', 'About a minute'),
          ('figma', 'A Figma prototype link', 'Paste the prototype’s share link. Flows and transitions work as in Figma.', 'Instant')]
    r = ''.join(f'<div class="x-radio {"on" if k == 0 else ""}"><span class="x-rd"></span>{ic(i)}<div><b>{t}</b><small>{d}</small></div><span class="x-mut x-sm">{w}</span></div>' for k, (i, t, d, w) in enumerate(ch))
    main = f'''{create_head()}<div class="x-create"><div class="x-cl">{rail(0, None)}</div><div class="x-cm">
<h3>Where is it coming from?</h3><p class="x-lead">Pick one. Each has its own short steps, and you can switch later.</p><div class="x-radios">{r}</div>
<div class="x-cta">{btn('Continue', size='md', icon='arrow')}<span class="x-mut">Making a test instead? Start from Tests, New test: same steps, and it’s hosted inside the test.</span></div></div></div>'''
    return window('aeroapp.ai/new', sidebar('Sites'), main, h=760)


def up_states():
    drop = f'''<div class="stc"><div class="hd"><span class="n">1</span><b>Drop</b><span style="margin-left:auto">nothing to publish yet, so no Publish button</span></div><div class="stb"><div class="dropbig">{ic('folder')}<b>Drop an HTML file, a folder or a zip</b><span>index.html at the top level · or {('<span class="lnk">choose files</span>')}</span></div></div></div>'''
    files = [('index.html', '4 KB', 100), ('styles.css', '18 KB', 100), ('app.js', '96 KB', 100), ('images/ (14 files)', '1.6 MB', 58)]
    fl = ''.join(f'<div class="uprow">{ic("file")}<div><div style="display:flex;justify-content:space-between"><span>{n}</span><span class="mono">{s}</span></div><div class="bar" style="margin-top:5px"><b style="width:{p}%"></b></div></div><span class="mono">{"Done" if p == 100 else f"{p}%"}</span></div>' for n, s, p in files)
    upl = f'''<div class="stc"><div class="hd"><span class="n">2</span><b>Uploading checkout.zip</b><span style="margin-left:auto">72% · about 10 seconds</span></div><div class="stb" style="padding:8px 16px 12px">{fl}</div></div>'''
    return f'<div class="states x-st2">{drop}{upl}</div>'


def up_done():
    main = f'''{create_head('up')}<div class="x-create x-sitewash" style="--site-c:#1F8F5F;--site-c2:#FFE1D2"><div class="x-cl">{rail(3, 'up')}</div><div class="x-cm">
<span class="ex">Published · just now</span><h3 class="x-addrbig mono">checkout.aeroapp.ai <span class="st live">Live</span></h3>
<div class="x-meta"><span>Version 1</span><span>17 files, 1.7 MB</span><span>Took 14 seconds</span><span>Public</span></div>
<div class="x-pubrow">{thumb('checkout', 420, 260, scale=.62, top='6%', cls='x-shot')}<div class="x-nowtest"><b>Now test it</b><p>Sets up a test straight away: a copy of this site with its own link, ready to send. Tasks are optional; add them on the next page.</p>
{btn('Now test it', size='md', icon='arrow')}<div class="x-acts2">{gbtn('Copy address', 'copy')}{gbtn('Visit', 'ext')}{gbtn('Site settings')}</div></div></div></div></div>'''
    return window('aeroapp.ai/new?from=upload', sidebar('Sites', one_site=None), main, h=760)


def claude_panel(state):
    if state == 'wait':
        end = '<div class="tool">● Working · calling the Aero API</div>'
    else:
        end = '<div class="tool">● Used the Aero API · publish</div><p>Done. It’s live at <b>pocket.aeroapp.ai</b>, version 1. Open Aero to set up a test.</p>'
    return f'''<div class="x-outside"><div class="outside">Outside Aero · Claude, simplified</div><div class="claude"><div class="top"><i></i>Claude</div>
<div class="you">Publish this to Aero as a site called pocket. Use my Aero key: aero_sk_••••7Q2c …</div>{end}<div class="inp">Reply to Claude</div></div></div>'''


def prompt_page():
    p = 'Publish the app you just built to Aero as a site called “pocket”. Send every file through the Aero API at aeroapp.ai/api/v1/sites with my key aero_sk_••••7Q2c, then reply with the address.'
    main = f'''{create_head('prompt')}<div class="x-create"><div class="x-cl">{rail(1, 'prompt')}</div><div class="x-cm">
<h3>Copy this into the chat where you built it</h3><p class="x-lead">It’s a prompt, nothing to install. It tells Claude or ChatGPT to send the files to Aero with your key.</p>
<div class="x-pbox"><p>{p}</p><div class="x-pba">{btn('Copy prompt', size='md', icon='copy')}<span class="x-mut">Site name {('<span class="x-in x-inl">pocket</span>')}</span></div></div>
<div class="x-key">{ic('lock')}<span>The key only lets this prompt publish sites in Kestrel Studio. Treat it like a password. {('<span class="lnk">Make a new key</span>')}</span></div>
<div class="x-waitb"><span class="dotload"></span><div><b>Waiting for your chat</b><small>Paste the prompt, then come back. This page updates by itself when the site is live.</small></div></div>
</div></div>'''
    return window('aeroapp.ai/new?from=prompt', sidebar('Sites'), main, h=660)


def prompt_done():
    return f'''<div class="stc"><div class="hd"><span class="n">{ic('check')}</span><b>Published</b><span style="margin-left:auto">the same page, a minute later</span></div><div class="stb">
<div class="result">{thumb('pocket', 150, 118, scale=.48)}<div><div class="addr">pocket.aeroapp.ai <span class="st live" style="font-size:13px">Live</span></div>
<div class="meta"><span>Version 1</span><span>From Claude</span><span>10:41</span></div>
<div class="acts">{btn('Now test it', size='md', icon='arrow')}{gbtn('Visit', 'ext')}{gbtn('Copy address', 'copy')}</div></div></div></div></div>'''


def figma_states():
    paste = f'''<div class="stc"><div class="hd"><span class="n">1</span><b>Paste</b></div><div class="stb"><div class="field x-f">{ic('link')}<span>figma.com/proto/8Gk2…/Onboarding-v2</span>{btn('Check')}</div><small class="x-mut x-sm2">In Figma: Share, Copy link, from the prototype view.</small></div></div>'''
    chk = f'''<div class="stc"><div class="hd"><span class="n">2</span><b>Checking the link</b></div><div class="stb"><div class="x-waitb sm"><span class="dotload"></span><div><b>Opening the prototype</b><small>A few seconds.</small></div></div>
<div class="x-err">{ic('lock')}<span>If it’s private, Figma says no. Set Share to “Anyone with the link” and paste it again.</span></div></div></div>'''
    return f'<div class="states x-st2">{paste}{chk}</div>'


def figma_ready():
    main = f'''{create_head('figma')}<div class="x-create"><div class="x-cl">{rail(2, 'figma')}</div><div class="x-cm">
<span class="ex">Link checked</span><h3>Onboarding v2 is ready</h3>
<div class="x-fready">{thumb('onboarding', 220, 270, scale=.56, top='5%')}<div>
<div class="x-facts"><div><span>File</span><b>Kestrel · Pocket onboarding</b></div><div><span>Starts at</span><b>Welcome</b></div><div><span>Screens</span><b>6</b></div><div><span>Sharing</span><b>Anyone with the link</b></div></div>
<div class="x-set" style="margin-top:16px"><label>Address</label><div class="x-in" style="gap:0"><span class="mono">onboarding-v2</span><span class="x-mut mono">.aeroapp.ai</span></div></div>
<div class="x-cta">{btn('Publish', size='md', icon='arrow')}<span class="x-mut">Changes you make in Figma show up here on their own.</span></div></div></div></div></div>'''
    return window('aeroapp.ai/new?from=figma', sidebar('Sites'), main, h=760)


def m5():
    body = ('<h3 class="x-sub-h">First: pick where it’s from</h3>' + both(pick_page, 'Pick')
            + note('Steps down the left come from C Story: each ticks off and stays, so you can see how you got here. The choice is round 5’s radio list, one line each with how long it takes. The source switch at the top of each flow goes straight to the other flow and keeps nothing half-filled.', 'Why')
            + '<h3 class="x-sub-h">a · Upload HTML or a zip</h3>' + both(up_states, 'Drop, uploading') + both(up_done, 'Published')
            + note('After upload the page wash takes about 6% of the site’s own colours (here Checkout’s green and peach), read from the screenshot. Before upload it is the neutral Publish wash. Option: keep the wash neutral and use the site colour only around the screenshot.', 'Option')
            + '<h3 class="x-sub-h">b · From a prompt</h3>' + both(lambda: f'<div class="x-pw">{prompt_page()}{claude_panel("wait")}</div>', 'Copy, waiting')
            + both(lambda: f'<div class="x-pw sm">{prompt_done()}{claude_panel("done")}</div>', 'Published')
            + '<h3 class="x-sub-h">c · Figma prototype link</h3>' + both(figma_states, 'Paste, check') + both(figma_ready, 'Ready'))
    return section('m5', '05', 'Create: one guided flow per source', 'First pick where it comes from, then that source’s own short flow. Nothing asks you to publish before there is a file, a prompt or a link. Switching source goes to the other flow.', body)


# ---------------------------------------------------------------- m6 test setup and share
def test_setup():
    tasks = [('Add the linen tote to your basket and check out.', ''), ('Change delivery to next day.', ''), ('Find out how to return an item.', '')]
    tk = ''.join(f'<div class="x-task">{ic("drag", "i x-dr")}<span class="mono">{k + 1}</span><span class="x-tt">{t}</span>{ic("x", "i x-dr")}</div>' for k, (t, _) in enumerate(tasks))
    main = f'''<div class="mhead"><span class="crumb">Tests {ic('right')} <b>Checkout</b></span><div class="r">{gbtn('Open as tester', 'ext')}{btn('Copy test link', icon='copy')}</div></div>
<div class="mtabs"><span>Sessions <span class="mono">0</span></span><span>Review</span><span class="on">Setup</span><span class="r">Example</span></div>
<div class="x-ts"><div class="x-tsm">
<div class="x-made">{ic('check')}<span>Set up from <span class="mono">checkout.aeroapp.ai</span> just now. The link works already; everything below is optional.</span></div>
<div class="x-set"><label>Name</label><div class="x-in">Checkout</div><small>Testers see this at the start.</small></div>
<div class="x-set"><label>Tasks <span class="x-opt">optional</span></label>{tk}<div class="x-add">{ic('plus')}Add a task</div><small>With no tasks, testers explore freely and the review sums up the whole session.</small></div>
<div class="x-set"><label>Welcome message</label><div class="x-in x-ta">Thanks for helping. This is an early checkout for Paper &amp; Co. Say what you think as you go, there are no wrong answers.</div></div>
<div class="x-set"><label>Thank-you message</label><div class="x-in x-ta">That’s everything. Thank you, it really helps.</div></div>
</div><div class="x-tss">
<div class="x-linkc"><label>Test link</label><div class="x-lk"><span class="mono">aeroapp.ai/t/checkout-4mq</span>{btn('Copy', icon='copy')}</div><div class="x-recs"><span>{ic('tab')}Their screen</span><span>{ic('mic')}Their voice</span><span>No account</span></div></div>
<div class="x-set"><div class="x-row"><div><b>Open as tester</b><small>Try it yourself. Your session shows as <b>You</b> in Sessions.</small></div>{gbtn('Open', 'ext')}</div></div>
<div class="x-set"><div class="x-row"><div><b>Taking sessions</b><small>Turn off to close the test. The sessions stay.</small></div>{switch(True)}</div></div>
<div class="x-set"><label>Custom domain <span class="x-plan">Solo</span></label><div class="x-row"><div class="x-in x-pl" style="flex:1">test.kestrel.studio</div>{gbtn('Connect')}</div><small>Its own domain, separate from the site’s.</small></div>
<div class="x-set"><label>Favicon <span class="x-plan">Basic</span></label><div class="x-row"><span class="x-fav">{MARK()}</span><small style="flex:1">Same as the site. {('<span class="lnk">Replace</span>')}</small></div></div>
<div class="x-set x-src"><label>What testers open</label><div class="x-row">{thumb('checkout', 72, 50, scale=.1, top='8%')}<small style="flex:1">A copy of <span class="mono">checkout.aeroapp.ai</span> v8. Updating the site doesn’t change it. {('<span class="lnk">Upload to this test</span>')}</small></div></div>
</div></div>'''
    return window('aeroapp.ai/tests/checkout/setup', sidebar('Tests'), main)


def m6():
    body = (both(test_setup, 'Test setup')
            + note('Setup and Share are one tab: the link is the first thing on the right because it already works when you land here from “Now test it”. Option: open on Sessions instead, with the link card on top, and keep Setup for later edits.', 'Option'))
    return section('m6', '06', 'Test setup and share', 'Name, optional tasks, welcome and thank-you messages on the left; the test link with Copy, “Open as tester” (recorded as You), domain and favicon on the right. Landing here from “Now test it”, the link already works.', body)


# ---------------------------------------------------------------- m7 tester
def proto_bright(veil=False):
    cards = [('#FFD24A', 'Groceries', '£212'), ('#1D1D1F', 'Travel', '£86'), ('#FFFFFF', 'Eating out', '£64')]
    c = ''.join(f'<div class="pk-c" style="background:{b};{"color:#fff" if b == "#1D1D1F" else ""}"><small>{n}</small><b>{v}</b></div>' for b, n, v in cards)
    return f'''<div class="pk {"veil" if veil else ""}"><div class="pk-top"><b>● Pocket</b><span>Home</span><span>Cards</span><span>Spending</span><span class="pk-av">SR</span></div>
<div class="pk-hero"><small>Main balance</small><div class="pk-bal">£2,480<span>.12</span></div><div class="pk-acts"><span>Send</span><span>Request</span><span>Split</span><span>Freeze</span></div></div>
<div class="pk-row">{c}</div><div class="pk-list"><div><b>Corner Coffee</b><span>−£4.20</span></div><div><b>Sam Rivera</b><span>+£36.00</span></div><div><b>Market Hall</b><span>−£52.18</span></div></div></div>'''


def tbrowser(url, inner, h=760):
    return f'<div class="fitw"><div class="win full x-w x-tb">{bar(url)}<div class="x-tbody" style="height:{h - 36}px">{inner}</div></div></div>'


def tester_start():
    card = f'''<div class="x-tcard"><div class="x-tfrom"><span class="av m">M</span><span>Mia at Kestrel Studio asked you to try</span></div><h3>Pocket</h3>
<p>Thanks for helping. Use the prototype as if it were real and say what you think as you go. There are no wrong answers.</p>
<div class="x-tfacts"><div>{ic('tab')}<span><b>This tab and your voice are recorded.</b> Not your camera, not other tabs.</span></div><div>{ic('user')}<span>Only Mia’s studio sees the recording.</span></div><div>{ic('x')}<span>Stop any time. It takes as long as you like.</span></div></div>
<label class="x-tl2">Your first name <span>optional</span></label><div class="x-in x-tin">Ana<span class="x-car"></span></div><small class="x-mut">Shown next to your session. Leave it empty to stay anonymous.</small>
<div class="x-tgo">{btn('Continue', size='md', icon='arrow')}<span class="x-mut">Next: allow the microphone and this tab</span></div>
<div class="x-tfoot">{LOCKUP('lk')}<span>No account needed</span></div></div>'''
    return tbrowser('aeroapp.ai/t/pocket-7k2', f'{proto_bright(veil=True)}<div class="x-tover">{card}</div>')


def tester_perm():
    card = f'''<div class="x-tcard sm"><span class="ex">Step 2 of 2 · Ana</span><h3>Two quick permissions</h3><p>Your browser asks for each. Nothing records until you press Start.</p>
<div class="x-perm done"><span class="k">{ic('check')}</span>{ic('mic')}<div><b>Microphone</b><small>So Mia can hear what you think.</small></div><span class="st live">Allowed</span></div>
<div class="x-perm"><span class="k">2</span>{ic('tab')}<div><b>This tab</b><small>Pick “This tab” when the browser asks.</small></div>{gbtn('Share this tab')}</div>
<small class="x-mut">Without the microphone there’s no transcript, only the video.</small></div>'''
    return tbrowser('aeroapp.ai/t/pocket-7k2', f'{proto_bright(veil=True)}<div class="x-tover">{card}</div>', h=620)


def task_pill(expanded=False):
    if expanded:
        return f'''<div class="x-tpanel"><div class="x-tph"><span class="x-rec">● 02:14</span><span>Task 2 of 3</span>{ic('chev', 'i x-dr')}</div>
<b>Find out how much you spent on eating out last month.</b><div class="x-tpa">{btn('Done', size='sm')}{gbtn("Couldn’t do it")}</div></div>'''
    return f'''<div class="x-pill"><span class="x-rec">● 02:14</span><span class="x-sep"></span><span class="x-pt"><small>Task 2 of 3</small>Find out how much you spent on eating out last month</span>{btn('Done', size='sm', cls='pill')}<span class="x-pup">{ic('up2')}</span></div>'''


def tester_task():
    return tbrowser('aeroapp.ai/t/pocket-7k2', f'{proto_bright()}<div class="x-pillw">{task_pill()}</div>', h=620)


def pill_on(bg, label):
    return f'<div class="x-pon" style="background:{bg}"><span class="x-ponl">{label}</span>{task_pill()}</div>'


def m7():
    pills = lambda: f'''<div class="x-pills">{pill_on('#FF5A36', 'Bright coral')}{pill_on('#000', 'Black')}{pill_on('#FFE14D', 'Yellow')}{pill_on('repeating-linear-gradient(45deg,#2F6BFF 0 14px,#16C2A3 14px 28px,#FFB800 28px 42px)', 'Busy')}{pill_on('#fff', 'White')}
<div class="x-pon x-pexp" style="background:#FF5A36"><span class="x-ponl">Opened</span>{task_pill(True)}</div></div>'''
    body = (both(tester_start, 'Start')
            + note('The name comes first and is optional, before any browser prompt, so the person knows what is recorded before being asked. “Anonymous tester” becomes their name, or “Tester 3” when left empty.', 'Why')
            + both(tester_perm, 'Permissions') + both(tester_task, 'During the test')
            + note('The pill is V3 glass (full pill, floating). The text sits on its own frosted plate inside the glass, so it stays readable over any colour: Aero can’t see a Figma embed’s pixels, so it can’t adapt. Tap the arrow to open the task card.', 'Why')
            + both(pills, 'Task pill over five prototypes'))
    return section('m7', '07', 'Tester start screen', 'The tester is asked their first name (optional) before screen and voice permission. Shown over a bright, colourful prototype, then the task pill floating over it.', body)


# ---------------------------------------------------------------- m8 marketing
def mk_site():
    return f'''<div class="mk mk-site">{thumb('pocket', 560, 250, scale=.66, top='8%')}<div class="meta"><span class="addr">pocket.aeroapp.ai</span><span class="st live">Live</span></div></div>'''


def mk_link():
    return f'''<div class="mk mk-link"><div class="l">Send this to your testers</div><div class="url">aeroapp.ai/t/pocket-7k2{btn('Copy link', size='md', icon='copy')}</div>
<div class="rec"><span>{ic('tab')}Their screen</span><span>{ic('mic')}Their voice</span><span>No account</span></div></div>'''


def mk_ev(n=3):
    e = [('review', '14:12', 'Review ready', 'Cards expected on the home screen, 4 of 4 testers.'),
         ('ses', '14:10', 'Tom finished a session', '7 minutes, 3 friction points.'),
         ('pub', '10:02', 'Published', 'pocket.aeroapp.ai, version 4.')][:n]
    return '<div class="mk x-mke">' + ''.join(f'<div class="x-ev k-{k}"><span class="x-t mono">{t}</span><span class="x-mk"></span><div class="x-evb"><div class="x-evh"><b>{h}</b></div><div class="x-evt">{d}</div></div></div>' for k, t, h, d in e) + '</div>'


def m8_render():
    app_site = f'<div style="width:260px">{site_block("pocket", "Pocket", "pocket.aeroapp.ai", "v4", "From a prompt", "live", "38", "Pocket")}</div>'
    app_link = f'<div class="x-linkc" style="width:280px"><label>Test link</label><div class="x-lk"><span class="mono">aeroapp.ai/t/pocket-7k2</span>{btn("Copy", icon="copy")}</div></div>'
    app_ev = f'<div class="x-tlw sm" style="width:300px">{ev("08:30", "review", "Pocket", "Review ready across 4 sessions. Cards expected on the home screen, 4 of 4.")}</div>'
    rows = [('Site preview block', 'Home, Sites', app_site, mk_site(), 'wash-p', 'A bigger real screenshot, the address and Live. Name, version, visits and source are dropped.'),
            ('Test link card', 'Test setup', app_link, mk_link(), 'wash-t', 'One link, one button and the three facts a tester needs.'),
            ('What’s new event row', 'Home', app_ev, mk_ev(), 'wash-r', 'Three events in a row tell the loop: published, a session, a review. The mark and the line carry over.')]
    kr = ''.join(f'''<div class="krow"><div class="app-v"><div class="klbl"><b>{n}</b></div><div class="klbl">In the app · {w}</div>{a}<div class="knote">{nt}</div></div>
<div class="mk-v {wash}">{m}</div></div>''' for n, w, a, m, wash, nt in rows)
    hero = f'''<div class="sizes">Homepage hero block, built only from the three components</div><div class="hero-block x-hero">
<h3>Publish your prototype. Watch people use it<span class="d">.</span></h3>
<p class="lead">Upload an HTML folder, paste a Figma link or ask Claude. Share one test link. Each session comes back transcribed and summarised, in their own words.</p>
<div class="ctas">{btn('Start free', size='md')}{btn('Open the example', 'secondary', size='md')}</div>
<div class="x-hnote">Free to start · paid plans from $3 · no call, no contract</div>
<div class="pos" style="left:660px;top:48px;transform:scale(.82);transform-origin:0 0">{mk_site()}</div>
<div class="pos" style="left:770px;top:306px;transform:scale(.72);transform-origin:0 0">{mk_link()}</div>
<div class="pos" style="left:600px;top:470px;transform:scale(.7);transform-origin:0 0">{mk_ev(3)}</div>
<div class="pos" style="right:22px;bottom:16px" class="ex"><span class="ex">Example</span></div></div>'''
    return f'<div class="kit">{kr}</div><div class="compose">{hero}</div>'


def m8():
    return section('m8', '08', 'Marketing versions', 'Three of these components drawn bigger and simpler for the website and videos: the site preview block, the test link card and the what’s-new event row. Then one homepage hero built only from them.', both(m8_render, 'Kit'))


# ---------------------------------------------------------------- page
def page():
    secs = [m1(), m2(), m3(), m4(), m5(), m6(), m7(), m8()]
    toc = ''.join(f'<a href="#{i}">{t}</a>' for i, t in [('m1', 'Home'), ('m2', 'First run'), ('m3', 'Lists'), ('m4', 'Site page'), ('m5', 'Create'), ('m6', 'Test setup'), ('m7', 'Tester'), ('m8', 'Marketing')])
    return f'''<!doctype html><html lang="en-GB" data-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=1440">
<title>Aero app v2, Team 2</title><link rel="icon" href="../shared/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@300..600&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../shared/aero.css"><link rel="stylesheet" href="extra.css"></head><body>
<header class="pagehead x-ph">{LOCKUP('logo')}<div><h1>App v2: make</h1></div><p>Home, first run, lists, the site page, create, test setup, the tester start and the marketing versions. A Studio refined, every frame in light and then dark. All names and numbers are examples.</p>
<nav class="x-toc">{toc}</nav></header>
<div class="theme-toggle"><button aria-pressed="true" onclick="setT('light',this)">Light</button><button aria-pressed="false" onclick="setT('dark',this)">Dark</button></div>
<script>function setT(t,b){{document.documentElement.dataset.theme=t;document.querySelectorAll('.theme-toggle button').forEach(function(x){{x.setAttribute('aria-pressed',x===b)}})}}</script>
{''.join(secs)}<div class="end"></div>
<script>window.GLASS_MODE=window.GLASS_MODE||'subtle';</script><script src="../shared/glass-v3.js"></script></body></html>'''


if __name__ == '__main__':
    html = page()
    (H / 'pages.html').write_text(html)
    print('ok', len(html))
