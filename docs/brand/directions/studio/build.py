"""Studio (direction A), explore stage: the whole app drawn in one direction.
Builds pages.html from src/ (pages.css, ui.css for the Pocket prototype, glass-v3.js, logo SVGs).
All names and numbers are example data (Kestrel Studio, Mia Chen, Pocket)."""
import pathlib, math, re

H = pathlib.Path(__file__).resolve().parent
S = H / 'src'
CSS = (S / 'ui.css').read_text() + '\n' + (S / 'pages.css').read_text()
GLASS = (S / 'glass-v3.js').read_text()


def svg(name, cls=''):
    s = (S / name).read_text().strip()
    return s.replace('<svg ', f'<svg class="{cls}" aria-hidden="true" ', 1) if cls else s


LOCKUP = lambda cls='logo': svg('lockup.svg', cls)
MARK = lambda cls='': svg('mark.svg', cls)
FAVICON = 'data:image/svg+xml,' + re.sub(r'\s+', ' ', (S / 'favicon.svg').read_text()).replace('#', '%23').replace('"', "'")

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
    'desk': '<rect x="1.5" y="2.5" width="13" height="9" rx="1.4"/><path d="M5.5 14h5"/>',
    'mic': '<rect x="6" y="2" width="4" height="8" rx="2"/><path d="M3.5 8a4.5 4.5 0 0 0 9 0M8 12.5V14"/>',
    'check': '<path d="m3.5 8.5 3 3 6-7"/>',
    'arrow': '<path d="M3 8h10M9 4l4 4-4 4"/>',
    'left': '<path d="M10 3 5 8l5 5"/>',
    'right': '<path d="m6 3 5 5-5 5"/>',
    'lock': '<rect x="3.5" y="7" width="9" height="6.5" rx="1.5"/><path d="M5.5 7V5a2.5 2.5 0 0 1 5 0v2"/>',
    'ext': '<path d="M9 3h4v4M13 3 7.5 8.5M12 9.5V13H3V4h3.5"/>',
    'down': '<path d="M8 2.5v8M4.5 7 8 10.5 11.5 7M3 13.5h10"/>',
    'book': '<path d="M3 3h4a1.5 1.5 0 0 1 1.5 1.5V13A1.5 1.5 0 0 0 7 11.5H3zM13 3H9.5A1.5 1.5 0 0 0 8 4.5"/><path d="M13 3v8.5H9.5"/>',
    'undo': '<path d="M5 6H10a3 3 0 0 1 0 6H6"/><path d="M7 3.5 4.5 6 7 8.5"/>',
    'tab': '<rect x="1.5" y="3" width="13" height="10" rx="1.6"/><path d="M1.5 6h13M5 3v3"/>',
    'play': '<path d="m5.5 3.5 7 4.5-7 4.5z"/>',
    'chev': '<path d="m5 6.5 3 3 3-3"/>',
    'qr': '<rect x="2.5" y="2.5" width="4" height="4"/><rect x="9.5" y="2.5" width="4" height="4"/><rect x="2.5" y="9.5" width="4" height="4"/><path d="M9.5 9.5h1.5V11M13.5 9.5v4h-4"/>',
}


def ic(name, cls='i'):
    return f'<svg class="{cls}" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{I[name]}</svg>'


def gbtn(label, icon=None, cls=''):
    return f'<span class="gbtn {cls}">{ic(icon) if icon else ""}{label}</span>'


def btn(label, kind='primary', size='sm', icon=None):
    fill = ' data-fill="#1D1D1F"' if kind == 'primary' else ''
    return f'<span class="btn g3 {size}" data-glass-v3="{kind}"{fill}>{ic(icon) if icon else ""}{label}</span>'


# ---------------------------------------------------------------- example data
STUDIO, OWNER = 'Kestrel Studio', 'Mia Chen'
SESS = [  # n, letter, tester, device, length, status, friction count, first line in their words, day
    (1, 'a', 'Tester A', 'Laptop · Chrome', '05:40', 'ready', 1, 'Send was easy. I wasn’t sure the money had gone.', 'Mon 20 Oct'),
    (2, 'b', 'Tester B', 'Laptop · Chrome', '07:12', 'ready', 3, 'I thought my cards would be on the home screen. Is it under More?', 'Mon 20 Oct'),
    (3, 'c', 'Tester C', 'Laptop · Safari', '04:55', 'ready', 2, 'Where are my cards? I’ve tapped everything on this screen.', 'Tue 21 Oct'),
    (4, 'd', 'Tester D', 'Laptop · Edge', '06:21', 'ready', 2, 'The balance looks like a button. Nothing happens.', 'Tue 21 Oct'),
    (5, 'e', 'Tester E', 'Laptop · Chrome', '03:47', 'noaud', 0, '', 'Wed 22 Oct'),
    (6, 'f', 'Tester F', 'Laptop · Chrome', '08:02', 'proc', 0, '', 'Wed 22 Oct'),
]
DOTS6 = ['', '', '', '', 'no', 'pr']
QUOTE = 'I thought my cards would be on the home screen. Is it under More?'
FR_B = [('Send flow has no back label', '02:41', 'There’s an arrow but it doesn’t say where to.'),
        ('Balance looks tappable', '03:02', 'Is the balance a button? I keep wanting to tap it.'),
        ('Cards are hidden under More', '03:08', QUOTE)]
TRANSCRIPT_B = [
    ('task', 'Task 2 · Find your cards'),
    ('02:36', 'Okay, so now I want to find my cards.', ''),
    ('02:41', 'Right, sent. How do I get back? There’s an arrow but it doesn’t say where to.', 'fr'),
    ('03:02', 'Is the balance a button? I keep wanting to tap it.', 'fr'),
    ('03:08', QUOTE, 'cur'),
    ('03:31', 'Oh, there they are. Under More. I wouldn’t have looked there.', ''),
    ('04:12', 'Can I freeze a card from here? Yes, okay, that’s clear.', ''),
]


def sdots(pattern, cls=''):
    m = {'': '', 'no': 'no', 'pr': 'pr', 'off': 'off', 'nw': 'nw'}
    return f'<span class="sdots {cls}">' + ''.join(f'<i class="{m[p]}"></i>' for p in pattern) + '</span>'


# ---------------------------------------------------------------- prototypes
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


def thumb(kind, w, h, scale=None, cls='', sheet=False, top=None):
    if kind == 'checkout':
        s = scale or (w * .9 / 640)
        inner = checkout()
        c = 'desk'
    else:
        s = scale or (w * .62 / 226)
        inner = pocket(sheet) if kind == 'pocket' else onboarding()
        c = ''
    t = f'top:{top};' if top else ''
    return f'<div class="th {c} {cls}" style="width:{w}px;height:{h}px"><div class="sc" style="{t}transform:translateX(-50%) scale({s:.3f})">{inner}</div></div>'


# ---------------------------------------------------------------- window and shell
def bar(url):
    return f'<div class="win-bar"><span class="lights"><i></i><i></i><i></i></span><span class="win-url"><span>{ic("lock")}{url}</span></span><span class="sp"></span></div>'


def sidebar(active='Home', recent='tests', on_test=None, on_session=None, plan=('Pro plan', '8 of 20 test sessions', 40), first=False):
    nav = [('home', 'Home', ''), ('site', 'Sites', '' if first else '3'), ('test', 'Tests', '' if first else '3')]
    n = ''.join(f'<div class="nav-i {"on" if l == active else ""}">{ic(k)}{l}<span class="ct">{c}</span></div>' for k, l, c in nav)
    s = ''
    if recent == 'tests':
        rows = [('#1D1D1F', 'Pocket', '<span class="t b">2 new</span>'), ('#8C88F5', 'Onboarding v2', '<span class="t">2</span>'), ('#1F8F5F', 'Checkout', '<span class="t">0</span>')]
        s = '<div class="side-lbl">Tests</div>' + ''.join(f'<div class="srow {"on" if nm == on_test else ""}"><span class="swatch" style="background:{c}"></span>{nm}{t}</div>' for c, nm, t in rows)
    elif recent == 'sessions':
        s = '<div class="side-lbl">Pocket · 6 sessions</div>'
        for n_, l, who, dev, ln, st, fc, q, day in SESS:
            mark = {'ready': '', 'noaud': 'no', 'proc': 'pr'}[st]
            t = {'ready': ln, 'noaud': 'No audio', 'proc': 'Arriving'}[st]
            s += f'<div class="srow {"on" if n_ == on_session else ""}"><span class="mono" style="font-size:10.5px;color:var(--w-mut2);width:12px">{n_}</span>{sdots([mark])}{who}<span class="t">{t}</span></div>'
        s += '<div class="legend" style="padding:10px 8px 0;margin:0;font-size:11px"><span class="kbd">J</span><span class="kbd">K</span> next, previous</div>'
    elif recent == 'none':
        s = '<div class="side-lbl">Tests</div><div style="padding:2px 8px;font-size:12px;color:var(--w-mut2)">Nothing yet</div>'
    pl, pu, pw = plan
    return f'''<aside class="side"><div class="ws"><span class="ic">{MARK()}</span>{STUDIO}<span class="chev">{ic("chev")}</span></div>{n}{s}
<div class="use"><span>{pl}</span><span class="mono">{pu}</span><i><b style="width:{pw}%"></b></i></div>
<div class="nav-i" style="margin-top:2px">{ic("book")}How it works</div>
<div class="acct"><span class="av m">M</span>{OWNER}<span class="ex">Example</span></div></aside>'''


def window(url, side, main, h=760, style=''):
    return f'<div class="win" style="{style}">{bar(url)}<div class="app" style="--h:{h}px">{side}<div class="main">{main}</div></div></div>'


def section(id_, num, title, idea, body):
    return f'<section class="xp" id="{id_}"><h2><span class="n">{num}</span>{title}</h2><p class="idea">{idea}</p>{body}</section>'


def wave(n=150, pos=.44, marks=(), seed=1.0, ticks=True, length=432):
    bars = []
    for k in range(n):
        x = k / n
        v = .25 + .55 * abs(math.sin(k * .37 * seed + 1.3)) * (.55 + .45 * math.sin(k * .09 + .4)) + .18 * abs(math.sin(k * 1.7))
        h = max(10, min(100, v * 100))
        bars.append(f'<i class="{"p" if x < pos else ""}" style="height:{h:.0f}%"></i>')
    mk = ''.join(f'<span class="mk {"hot" if hot else ""}" style="left:{p * 100:.1f}%"></span>' for p, hot in marks)
    tk = ''
    if ticks:
        for sec in range(0, length, 60):
            tk += f'<span class="tkl" style="left:{sec / length * 100:.1f}%"></span>'
    return f'<div class="wave">{"".join(bars)}{tk}{mk}<span class="phd" style="left:{pos * 100:.1f}%"><b></b></span></div>'


def tsec(t):
    m, s = t.split(':')
    return int(m) * 60 + int(s)


# ---------------------------------------------------------------- p1 home
def p1():
    feed = f'''<div class="feed">
<div class="fi wash-r">{thumb('pocket', 76, 60)}<div><div class="w"><b>Pocket</b>12 min ago</div>
<div class="what">2 new sessions. Tester E had no audio, Tester F is being transcribed.</div></div>
<div class="acts">{sdots(['', '', '', '', 'no', 'pr'])}{gbtn('Open sessions')}</div></div>
<div class="fi">{thumb('pocket', 76, 60, sheet=True)}<div><div class="w"><b>Pocket</b>review · sessions 1 to 4</div>
<div class="what">Cards expected on the home screen, 3 of 4 testers. <q>Is it under More?</q></div></div>
<div class="acts">{gbtn('Review')}</div></div>
<div class="fi">{thumb('checkout', 76, 60)}<div><div class="w"><b>Checkout</b>2 hours ago</div>
<div class="what">Version 8 is live at <span class="mono" style="font-size:12.5px">checkout.aeroapp.ai</span>. Nobody has opened the test link yet.</div></div>
<div class="acts">{gbtn('Copy test link', 'copy')}</div></div>
<div class="fi">{thumb('onboarding', 76, 60)}<div><div class="w"><b>Onboarding v2</b>yesterday</div>
<div class="what">Review ready for 2 sessions. Both testers skipped the second screen.</div></div>
<div class="acts">{gbtn('Review')}</div></div></div>'''
    rows = [('Pocket', 'pocket.aeroapp.ai', ['', '', '', '', 'no', 'pr'], '12 min ago', '<span class="st new">2 new</span>', '#1D1D1F'),
            ('Onboarding v2', 'onboarding-v2.aeroapp.ai', ['', ''], 'Yesterday', '<span class="st ready">Reviewed</span>', '#8C88F5'),
            ('Checkout', 'checkout.aeroapp.ai', [], 'None yet', '<span class="st">Link ready</span>', '#1F8F5F')]
    tr = ''.join(f'<div class="tr2"><div class="nm"><span class="swatch" style="background:{c}"></span><div>{n}<small>{s}</small></div></div><div>{sdots(d) if d else "<span class=mut>No sessions</span>"}</div><div class="mut">{k}</div><div class="mut">{w}</div><div>{st}</div></div>' for (n, s, d, w, st, c), k in zip(rows, ['2 tasks', 'Explore freely', '3 tasks']))
    tests = f'<div class="tbl tests"><div class="tr2 hd"><span>Test</span><span>Sessions</span><span>Tasks</span><span>Last</span><span>Status</span></div>{tr}</div>'
    sites = [('pocket', 'pocket.aeroapp.ai', 'v4', 'From a prompt, in Claude'), ('onboarding', 'onboarding-v2.aeroapp.ai', 'v2', 'Figma prototype link'), ('checkout', 'checkout.aeroapp.ai', 'v8', 'HTML upload')]
    sc = ''.join(f'<div class="sc2">{thumb(k, 300, 112, scale=(0.36 if k == "checkout" else 0.5), top=("14%" if k == "checkout" else "12%"))}<div class="meta"><span class="addr">{a}</span><span class="st live">Live</span><span class="hw">{v} · {h}</span></div></div>' for k, a, v, h in sites)
    main = f'''<div class="mhead"><span class="crumb"><b>Home</b></span><div class="r">{gbtn('', 'search', 'ic')}{gbtn('New test', 'plus')}{btn('Publish', icon='plus')}</div></div>
<div class="mbody"><div class="home"><div>
<div class="hh"><h3>What’s new</h3><span class="mono">since you looked, Wed 09:12</span></div>{feed}
<div class="hh"><h3>Tests</h3><span class="mono">3</span><span class="r lnk">All tests {ic('arrow')}</span></div>{tests}</div>
<div><div class="hh"><h3>Sites</h3><span class="mono">3 live</span><span class="r lnk">All sites {ic('arrow')}</span></div><div class="sitelist">{sc}</div></div>
</div></div>'''
    big = window('aeroapp.ai/home', sidebar('Home', 'tests'), main, h=820)
    # first run
    ways = f'''<div class="way"><span class="k">Figma prototype</span><div class="field">{ic('link')}<span style="overflow:hidden;white-space:nowrap;text-overflow:ellipsis;min-width:0">figma.com/proto/…</span>{btn('Publish')}</div></div>
<div class="way"><span class="k">HTML file or zip</span><div class="drop">{ic('folder')}Drop a file, folder or zip</div></div>
<div class="way"><span class="k">From Claude or ChatGPT</span><div class="drop" style="border-style:solid;border-color:#E2E2E6;background:#fff;color:var(--w-ink2)">{ic('copy')}Connect once, then ask it<span class="lnk" style="margin-left:auto">Set up {ic('arrow')}</span></div></div>'''
    fr_main = f'''<div class="mhead"><span class="crumb"><b>Home</b></span></div><div class="mbody"><div class="firstrun">
<div class="fr-wash"><h3>Put something online first<span style="color:var(--blue)">.</span></h3><p>Then share one link and watch people use it. Pick the way you made it.</p>{ways}</div>
<div><div class="steps3"><div class="s3"><span class="mono">01</span><div><b>Publish</b>Your prototype gets an address like name.aeroapp.ai.</div></div>
<div class="s3"><span class="mono">02</span><div><b>Test</b>Send the test link. Testers share their screen and voice, no account needed.</div></div>
<div class="s3"><span class="mono">03</span><div><b>Review</b>About a minute after each session: the transcript, a summary and the friction points.</div></div></div>
<div class="plannote">Free plan: 3 test sessions, and sites stay live for 7 days. Paid plans from $3.</div></div></div></div>'''
    small = window('aeroapp.ai/home', sidebar('Home', 'none', first=True, plan=('Free plan', '0 of 3 test sessions', 0)), fr_main, h=470)
    body = f'''<div class="frame hero"><div class="cap"><b>Home</b><span>Example: Kestrel Studio, Wednesday morning</span></div>{big}
<div class="sub-frame"><div class="cap"><b>First run</b><span>A new account on Free: nothing to show yet, so the page is the way in</span></div><div style="width:1120px">{small}</div></div></div>'''
    return section('p1', '01', 'Home', 'What’s new comes first, each line with a real thumbnail of the prototype and the session dots (one per session). The first run is the way in, not an empty table.', body)


# ---------------------------------------------------------------- shared test header
def testhead(tab):
    tabs = [('Sessions', '6'), ('Review', ''), ('Share', ''), ('Setup', '')]
    t = ''.join(f'<span class="{"on" if n == tab else ""}">{n}{f" <span class=mono>{c}</span>" if c else ""}</span>' for n, c in tabs)
    return f'''<div class="mhead"><span class="crumb">Tests {ic('right')} <b>Pocket</b></span><div class="r">{gbtn('Open as a tester', 'ext')}{btn('Copy test link', icon='copy')}</div></div>
<div class="testhead">{thumb('pocket', 52, 52)}<div><h3>Pocket</h3><div class="sub"><span class="mono">pocket.aeroapp.ai</span><span class="st live">Live</span><span>v4</span><span>2 tasks</span><span>Desktop testers</span></div></div></div>
<div class="mtabs">{t}<span class="r">Example</span></div>'''


# ---------------------------------------------------------------- p2 sessions
def p2():
    rows = ''
    for n, l, who, dev, ln, st, fc, q, day in SESS:
        if st == 'ready':
            qq = f'<span class="q">“{q}”</span>'
            stw = '<span class="st ready">Ready</span>'
            fcs = f'<span class="fcount">{fc}</span>'
        elif st == 'noaud':
            qq = '<span class="q dim">No audio: the microphone was off. You can still watch it.</span>'
            stw = '<span class="st noaud">No audio</span>'
            fcs = '<span class="fcount z">–</span>'
        else:
            qq = '<span class="q dim" style="display:flex;gap:10px;align-items:center"><span class="shim" style="width:90px"><i style="width:100%"></i><i style="width:70%"></i></span>Transcript arriving, usually about a minute</span>'
            stw = '<span class="st proc">Processing</span>'
            fcs = '<span class="fcount z">–</span>'
        rows += f'<div class="tr2 {"on" if n == 2 else ""}"><span class="num">{n}</span><div class="who"><span class="av {l}">{l.upper()}</span><div>{who}<small>{day}</small></div></div><span class="mono" style="font-size:12px">{ln}</span>{fcs}{qq}{stw}</div>'
    # strip: one block per session, width by length
    total = sum(tsec(s[4]) for s in SESS)
    strip = ''
    for n, l, who, dev, ln, st, fc, q, day in SESS:
        w = tsec(ln) / total * 100
        bg = {'ready': '#1D1D1F', 'noaud': 'repeating-linear-gradient(135deg,#E4E4E8 0 4px,#F4F4F6 4px 8px)', 'proc': '#fff'}[st]
        bd = 'box-shadow:inset 0 0 0 1.4px #C9C9CE' if st != 'ready' else ''
        sel = 'outline:2px solid var(--blue);outline-offset:2px;' if n == 2 else ''
        strip += f'<div style="width:{w:.2f}%;padding-right:4px"><div style="height:8px;border-radius:3px;background:{bg};{bd};{sel}"></div><div class="mono" style="font-size:10px;color:var(--w-mut2);margin-top:6px">{n} · {ln}</div></div>'
    head = f'<div class="tr2 hd"><span>#</span><span>Tester</span><span>Length</span><span>Friction</span><span>First friction, in their words</span><span>Status</span></div>'
    fps = ''.join(f'<div class="fq {"hot" if i == 2 else ""}"><b>{t}</b><span class="mono">{tc}</span><q>{q}</q></div>' for i, (t, tc, q) in enumerate(FR_B))
    peek = f'''<div class="peek"><div class="lbl2">Session 2<span class="r">{gbtn('', 'left', 'ic')} {gbtn('', 'right', 'ic')}</span></div>
<div class="ph-mini">{thumb('pocket', 92, 120, scale=.4, sheet=True)}<div><h4>Tester B</h4><div class="pm">07:12 · Laptop · Chrome</div><div class="pm">Mon 20 Oct, 18:04</div><div style="margin-top:10px">{btn('Watch session', icon='play')}</div></div></div>
<div class="lbl2">Summary</div><p class="para">Sent money to Sam quickly. Looked for cards on the home screen for about 30 seconds, then found them under More.</p>
<div class="lbl2">Friction points<span class="r">3</span></div>{fps}</div>'''
    main = f'''{testhead('Sessions')}<div class="ses-split"><div class="ses-list">
<div class="lbl2" style="margin-bottom:10px">6 sessions, by length · numbered from the first<span class="r"><span class="kbd">J</span> <span class="kbd">K</span> to move</span></div>
<div style="display:flex;margin-bottom:18px">{strip}</div>
<div class="tbl stbl">{head}{rows}</div>
<div class="legend">{sdots([''])} Ready {sdots(['pr'])} Processing {sdots(['no'])} No audio <span style="margin-left:auto">Sessions kept: 8 of 20 on Pro</span></div></div>{peek}</div>'''
    body = f'<div class="frame test"><div class="cap"><b>Sessions</b><span>Pocket, 6 sessions. Session 5 had no audio, session 6 has just ended</span></div>{window("aeroapp.ai/tests/pocket/sessions", sidebar("Tests", "tests", on_test="Pocket"), main, h=800)}</div>'
    return section('p2', '02', 'Sessions', 'One test, every session in a calm table numbered from the first. A length strip on top, a peek on the right, J and K to move. Status is a word with its own mark, never a coloured pill.', body)


# ---------------------------------------------------------------- p3 session review
def transcript_lines(compact=False):
    out = ''
    for ln in TRANSCRIPT_B:
        if ln[0] == 'task':
            out += f'<div class="tl task">{ln[1]}</div>'
            continue
        tc, txt, kind = ln
        if kind == 'cur':
            ws = txt.split(' ')
            said, now, rest = ' '.join(ws[:10]), ws[10], ' '.join(ws[11:])
            out += f'<div class="tl cur fr"><span class="mono">{tc}</span><span><span class="said">{said}</span> <span class="now">{now}</span> {rest}<span class="mark"></span></span></div>'
        else:
            out += f'<div class="tl {"fr" if kind == "fr" else ""}"><span class="mono">{tc}</span><span>{txt}{"<span class=mark></span>" if kind == "fr" else ""}</span></div>'
    return out


def p3():
    length = 432
    marks = [(tsec(t) / length, t == '03:08') for _, t, _ in FR_B]
    pos = 189 / length
    fps = ''.join(f'<div class="fq {"hot" if i == 2 else ""}"><b>{t}</b><span class="mono">{tc}</span><q>{q}</q></div>' for i, (t, tc, q) in enumerate(FR_B))
    main = f'''<div class="mhead"><span class="crumb">Tests {ic('right')} Pocket {ic('right')} <b>Session 2 · Tester B</b></span>
<div class="r"><span class="navs">{gbtn('', 'left', 'ic')}2 of 6{gbtn('', 'right', 'ic')}</span>{gbtn('Download summary', 'down')}</div></div>
<div class="sv2"><div class="svm"><div class="stage2"><div class="tag"><span>Screen and voice · Laptop · Chrome · Mon 20 Oct</span></div>
<div class="task">{gbtn('Task 2 of 2 · Find your cards')}</div><div style="transform:scale(.98)">{pocket()}</div></div>
<div class="scrub"><span class="play"><svg viewBox="0 0 10 10"><path d="M2 1h2v8H2zM6 1h2v8H6z"/></svg></span><span class="tc">03:09 <span>/ 07:12</span></span>{wave(110, pos, marks)}<span class="mono" style="font-size:11px;color:var(--w-mut)">1x</span></div>
<div class="below"><div><div class="lbl2">Summary · ready 1 min after the session</div><p class="para" style="margin-top:8px">Tester B sent £20 to Sam without help. Looking for cards, they checked the home screen and the balance for about 30 seconds before opening More.</p></div>
<div><div class="lbl2">Top priorities</div><ol><li><span class="mono">01</span>Show cards on the home screen</li><li><span class="mono">02</span>Label the back arrow in Send</li><li><span class="mono">03</span>Make the balance look less like a button</li></ol></div></div></div>
<div class="insp"><div class="itabs"><span class="on">Transcript</span><span>Notes</span><span class="r">follows the recording</span></div>
<div class="trs">{transcript_lines()}</div>
<div class="fps2"><div class="lbl2"><span class="bd" style="width:7px;height:7px;border-radius:50%;background:var(--blue);display:inline-block"></span>Friction points, in their own words<span class="r">click to play</span></div>{fps}</div>
<div class="how"><b>How this was made.</b> The recording was transcribed and summarised about a minute after the session ended. Quotes are the tester’s exact words.</div></div></div>'''
    body = f'<div class="frame review"><div class="cap"><b>Session review</b><span>Playing at 03:09: the words light up as Tester B says them</span></div>{window("aeroapp.ai/tests/pocket/sessions/2", sidebar("Tests", "sessions", on_session=2), main, h=820)}</div>'
    return section('p3', '03', 'Session review', 'Recording first, on the Review wash. The transcript follows the playback word by word (it was written after the session, this is replay). Friction points jump to their moment. No cursor: tab recordings have none.', body)


# ---------------------------------------------------------------- p4 publish from a prompt
def claude_panel(state='done'):
    end = ('<div class="tool">● Aero · publish_site</div><p>It’s live at <b>pocket.aeroapp.ai</b>. I’ve set up a test too; the link is in your Aero dashboard.</p>'
           if state == 'done' else '<div class="tool">● Aero · publish_site · working</div>')
    return f'''<div class="outside">Outside Aero · Claude, simplified</div><div class="claude"><div class="top"><i></i>Claude</div>
<div class="you">Put this prototype online with Aero and set up a test.</div>{end}<div class="inp">Reply to Claude…</div></div>'''


def p4():
    check = ic('check')
    steps = f'''<div class="pub-steps">
<div class="ps done"><span class="k">{check}</span><div><b>Connect Aero to your AI tool</b><div class="s">Claude connected · 10:38. You only do this once.</div></div>{gbtn('Connect ChatGPT')}</div>
<div class="ps done"><span class="k">{check}</span><div><b>Copy the prompt into the chat where you built it</b>
<div class="prompt"><span class="mono">Put this prototype online with Aero and set up a test.</span>{gbtn('Copied', 'check')}</div></div><span></span></div>
<div class="ps done"><span class="k">{check}</span><div><b>Waiting for your chat</b><div class="s">Claude sent the files at 10:41 · 14 files, 2.1 MB</div></div><span></span></div>
<div class="ps done"><span class="k">{check}</span><div style="grid-column:2/4"><b>Published</b>
<div class="result">{thumb('pocket', 150, 118, scale=.48)}<div><div class="addr">pocket.aeroapp.ai <span class="st live" style="font-size:13px">Live</span></div>
<div class="meta"><span>Version 1</span><span>From Claude</span><span>10:41</span></div>
<div class="acts">{btn('Now test it', size='md', icon='arrow')}{gbtn('Open site', 'ext')}{gbtn('Copy address', 'copy')}</div>
<div class="note">A test was set up from the chat too. Next you’ll see its link, ready to send.</div></div></div></div></div></div>'''
    aside = '''<div><h5>What the prompt does</h5><p>Your AI tool sends the files it built to Aero through the connector. Nothing is copied by hand.</p>
<h5>How long</h5><p>Usually seconds to a minute, then this page updates by itself.</p>
<h5>Free plan</h5><p>Sites stay live 7 days. Paid plans keep them live and add your own address.</p></div>'''
    main = f'''<div class="mhead"><span class="crumb">Sites {ic('right')} <b>New site</b> · from a prompt</span><div class="r">{gbtn('Cancel')}</div></div>
<div class="mbody" style="padding:0"><div class="pubpage">{steps}</div></div>'''
    # earlier states, small
    s1 = f'''<div class="stc"><div class="hd"><span class="n">1</span><b>Connect once</b></div><div class="stb" style="font-size:13px">
<div style="display:flex;gap:10px;align-items:center;margin-bottom:10px"><span class="st live">Claude connected</span></div>
<div style="display:flex;gap:8px">{gbtn('Connect ChatGPT')}<span style="font-size:12px;color:var(--mut);align-self:center">Opens ChatGPT to approve</span></div></div></div>'''
    s2 = f'''<div class="stc"><div class="hd"><span class="n">2</span><b>Copy the prompt</b></div><div class="stb"><div class="prompt" style="margin:0"><span class="mono">Put this prototype online with Aero and set up a test.</span>{btn('Copy', icon='copy')}</div></div></div>'''
    s3 = f'''<div class="stc"><div class="hd"><span class="n">3</span><b>Waiting for your chat</b></div><div class="stb" style="display:flex;gap:12px;align-items:center;font-size:13px;color:var(--ink2)"><span class="spin"></span>Paste it into Claude. This page updates when it publishes.</div></div>'''
    body = f'''<div class="frame publish"><div class="cap"><b>Publish from a prompt</b><span>Example: the first time Pocket went live, Tue 14 Oct</span></div>
<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr)) 300px;gap:20px;margin-bottom:24px;align-items:start">{s1}{s2}{s3}<div>{claude_panel('working')}</div></div>
<div style="display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:20px;align-items:start">{window("aeroapp.ai/sites/new?from=prompt", sidebar("Sites", "tests"), main, h=650)}<div>{claude_panel('done')}<div class="aside-note" style="margin-top:22px">{aside}</div></div></div></div>'''
    return section('p4', '04', 'Publish from a prompt', 'One page that keeps its own history: each step ticks off in place, and the page ends on the address with “Now test it”. Claude sits beside it as a separate, simplified panel in its own colours.', body)


# ---------------------------------------------------------------- p5 upload
def p5():
    files = [('index.html', '4 KB', 100), ('styles.css', '18 KB', 100), ('app.js', '96 KB', 100), ('images/ (14 files)', '1.6 MB', 58)]
    fl = ''.join(f'<div class="uprow">{ic("file")}<div><div style="display:flex;justify-content:space-between"><span>{n}</span><span class="mono">{s}</span></div><div class="bar" style="margin-top:5px"><b style="width:{p}%"></b></div></div><span class="mono">{"Done" if p == 100 else f"{p}%"}</span></div>' for n, s, p in files)
    s1 = f'''<div class="stc"><div class="hd"><span class="n">1</span><b>Drop</b><span style="margin-left:auto">Any time on the Versions tab, or New site</span></div><div class="stb"><div class="dropbig">{ic('folder')}<b>Drop an HTML file, a folder or a zip</b><span>index.html at the top level · up to 100 MB</span></div></div></div>'''
    s2 = f'''<div class="stc"><div class="hd"><span class="n">2</span><b>Uploading checkout-v8.zip</b><span style="margin-left:auto">72% · about 10 seconds</span></div><div class="stb" style="padding:8px 16px 12px">{fl}</div></div>'''
    vers = [('v8', 'checkout-v8.zip · 17 files', 'Today, 08:20', '<span class="st live">Live</span>', ''),
            ('v7', 'checkout-v7.zip · 16 files', 'Mon 20 Oct', '<span class="st">Saved</span>', gbtn('Roll back', 'undo')),
            ('v6', 'index.html', 'Fri 17 Oct', '<span class="st">Saved</span>', gbtn('Roll back', 'undo'))]
    vr = ''.join(f'<div class="tr2"><span class="mono" style="font-weight:500">{v}</span><span class="mut">{f}</span><span class="mut">{d}</span>{s}<span>{b}</span></div>' for v, f, d, s, b in vers)
    main = f'''<div class="mhead"><span class="crumb">Sites {ic('right')} <b>Checkout</b></span><div class="r">{gbtn('Open site', 'ext')}{gbtn('Upload new version', 'down')}</div></div>
<div class="mtabs"><span>Overview</span><span class="on">Versions <span class="mono">8</span></span><span>Settings</span><span>Domain</span><span>Analytics</span><span class="r">Example</span></div>
<div class="mbody"><div class="result" style="grid-template-columns:200px minmax(0,1fr);margin:0 0 24px">{thumb('checkout', 200, 130, scale=.28)}<div>
<div class="lbl2" style="margin-bottom:8px">Published · just now</div><div class="addr">checkout.aeroapp.ai <span class="st live" style="font-size:13px">Live</span></div>
<div class="meta"><span>Version 8 of 8</span><span>HTML upload</span><span>17 files, 1.7 MB</span><span>Took 14 seconds</span></div>
<div class="acts">{btn('Now test it', size='md', icon='arrow')}{gbtn('Copy address', 'copy')}<span style="font-size:12px;color:var(--w-mut)">The test link always opens the live version.</span></div></div></div>
<div class="hh"><h3>Versions</h3><span class="mono">roll back to any of them, the address stays the same</span></div>
<div class="tbl vers"><div class="tr2 hd"><span>Version</span><span>Files</span><span>Published</span><span>Status</span><span></span></div>{vr}</div></div>'''
    body = f'''<div class="frame publish"><div class="cap"><b>Upload HTML or zip</b><span>Example: Checkout, version 8</span></div>
<div class="states" style="grid-template-columns:1fr 1fr">{s1}{s2}</div>{window("aeroapp.ai/sites/checkout/versions", sidebar("Sites", "tests"), main, h=560)}</div>'''
    return section('p5', '05', 'Upload HTML or zip', 'Drop, a calm file list while it uploads, then the live address and version on the Publish wash with one next step: “Now test it”. Every version stays, so rolling back is one click.', body)


# ---------------------------------------------------------------- p6 review across sessions
def p6():
    #            A    B    C    D    E(no audio) F
    themes = [('Cards expected on the home screen', ['off', '', '', '', 'no', ''], '4 of 5', 'I’d expect my cards right here, under the balance.', 'Tester F'),
              ('Balance looks tappable', ['off', '', 'off', '', 'no', ''], '3 of 5', 'The balance looks like a button. Nothing happens.', 'Tester D'),
              ('Not sure the payment went through', ['', 'off', 'off', 'off', 'no', ''], '2 of 5', 'Send was easy. I wasn’t sure the money had gone.', 'Tester A'),
              ('Back arrow in Send has no label', ['off', '', 'off', 'off', 'no', 'off'], '1 of 5', 'There’s an arrow but it doesn’t say where to.', 'Tester B')]
    th = ''.join(f'<div class="theme"><span>{t}</span><span class="mono">{c}</span><span style="grid-column:1/-1;margin:3px 0">{sdots(d, 'lg')}</span><q>{q}</q></div>' for t, d, c, q, w in themes)
    fixes = [('Put cards on the home screen', '4 of 5 testers', [('Tester B · 03:08', 'I thought my cards would be on the home screen. Is it under More?'), ('Tester C · 01:52', 'Where are my cards? I’ve tapped everything on this screen.'), ('Tester F · 02:30', 'I’d expect my cards right here, under the balance.')]),
             ('Make the balance look less like a button', '3 of 5 testers', [('Tester D · 00:48', 'The balance looks like a button. Nothing happens.'), ('Tester B · 03:02', 'Is the balance a button? I keep wanting to tap it.')]),
             ('Confirm the payment after Send', '2 of 5 testers', [('Tester A · 02:12', 'Send was easy. I wasn’t sure the money had gone.')])]
    fx = ''.join(f'<div class="fix"><span class="big">{k + 1}</span><div><h4>{t}</h4><div class="qs">' + ''.join(f'<div><span class="mono">{ic("play")} {w}</span>“{q}”</div>' for w, q in qs) + f'</div></div><div class="cnt"><b>{n.split(" testers")[0]}</b><small>testers</small></div></div>' for k, (t, n, qs) in enumerate(fixes))
    main = f'''{testhead('Review')}<div class="mbody"><div class="rv"><div>
<div class="sumcard"><div class="lbl2" style="margin-bottom:8px">Summary · updated after session 6 · based on 5 of 6 sessions</div>
<p>Everyone sent money without help. Four of five testers looked for their cards on the home screen before finding them under More, and three tried tapping the balance.</p></div>
<div class="hh"><h3>What to fix first</h3><span class="mono">ordered by how many testers ran into it</span><span class="r">{gbtn('Download summary', 'down')}</span></div>{fx}</div>
<div><div class="hh"><h3>Themes</h3><span class="mono">one dot per session</span></div>{th}
<div class="disagree"><div class="lbl2">Where testers disagreed</div><div class="row"><span class="av a">A</span><span>Found Send quick and clear.</span></div><div class="row"><span class="av b">B</span><span>Lost the way back after sending.</span></div></div>
<div class="legend" style="flex-wrap:wrap;gap:8px 14px">{sdots([''])} said it {sdots(['off'])} didn’t {sdots(['no'])} no audio, not counted</div></div></div></div>'''
    body = f'<div class="frame review"><div class="cap"><b>Review across sessions</b><span>Pocket, after 6 sessions</span></div>{window("aeroapp.ai/tests/pocket/review", sidebar("Tests", "tests", on_test="Pocket"), main, h=830)}</div>'
    return section('p6', '06', 'Review across sessions', 'What to fix first, as a short numbered list with the quotes behind each item and a play link to the moment. Themes show who said it as a row of session dots, so “4 of 5” is something you can see.', body)


# ---------------------------------------------------------------- f1 flow
def mini(url, inner, cls=''):
    return f'<div class="mini {cls}"><div class="mb"><i></i><i></i><i></i><span>{url}</span></div>{inner}</div>'


def f1():
    g = lambda l, b: f'<div class="mrow ghost"><div class="l">{l}</div><b>{b}</b></div>'
    pub = '<div class="mrow p"><div class="l">Publish</div><b>pocket.aeroapp.ai · v1 · Live</b><span class="mbtn">Now test it</span></div>'
    pub2 = '<div class="mrow p"><div class="l">Publish</div><b>pocket.aeroapp.ai · v1 · Live</b></div>'
    tst = '<div class="mrow t {n}"><div class="l">Test</div><b>aeroapp.ai/t/pocket-7k2</b><span class="mbtn">Copied</span></div>'
    tst2 = '<div class="mrow t"><div class="l">Test</div><b>aeroapp.ai/t/pocket-7k2</b></div>'
    head = '<h6>Pocket</h6><div class="s">Kestrel Studio · Example</div>'
    claude = '''<div style="background:#F5F4EE;height:100%;padding:10px;font-family:ui-serif,Georgia,serif;color:#3D3929;font-size:9.5px;line-height:1.45">
<div style="font-family:var(--sans);font-size:8px;color:#7a7462;display:flex;gap:4px;align-items:center;margin-bottom:10px"><i style="width:8px;height:8px;border-radius:2px;background:#D97757;display:block"></i>Claude · outside Aero</div>
<div style="background:#EAE7DC;border-radius:7px;padding:6px 7px;margin:0 0 8px 18px;font-family:var(--sans)">Put this prototype online with Aero and set up a test.</div>
<div style="font-family:var(--sans);font-size:8px;color:#7a7462;border:1px solid #E3E0D3;border-radius:5px;padding:4px 6px;margin-bottom:6px;background:#FBFAF6">● Aero · publish_site</div>
It’s live at <b>pocket.aeroapp.ai</b>, and your test link is ready in Aero.</div>'''
    tester = '''<div class="tw"><div style="font-family:var(--mono);font-size:7.5px;color:var(--mut);margin-bottom:12px">aeroapp.ai/t/pocket-7k2 · tester’s laptop</div>
<h6>Mia invited you to try Pocket</h6><p>You’ll use a prototype and think out loud. Your screen and voice are recorded. Take as long as you like, and stop any time.</p>
<div class="chk"><i></i>Share this tab</div><div class="chk"><i></i>Allow microphone</div><div class="chk" style="border-bottom:1px solid #F0F0F2"><i style="background:none;box-shadow:inset 0 0 0 1px #9A9AA0"></i>2 tasks, then you’re done</div>
<span class="mrow" style="display:inline-block;margin-top:10px;background:var(--ink);color:#fff;padding:5px 10px;border-radius:5px;box-shadow:none;font-size:8.5px">Start</span>
<div style="font-size:7.5px;color:var(--mut);margin-top:10px">No account needed.</div></div>'''
    arriving = '<div class="mrow new"><div class="l">Session 1 · Tester A · 05:40</div><div class="shim" style="margin-top:4px"><i style="width:90%"></i><i style="width:60%"></i></div><div class="l" style="margin-top:5px">Transcript arriving, about a minute</div></div>'
    review = '<div class="mrow r"><div class="l">Review · session 1</div><b>“Send was easy. I wasn’t sure the money had gone.”</b><div class="l" style="margin-top:4px">● 02:12 · Not sure the payment went through</div></div>'
    steps = [
        ('Example 0:00', 'Ask Claude, in the chat where you built it.', mini('claude.ai', claude)),
        ('0:40', 'It’s live. The Pocket page opens on the address.', mini('aeroapp.ai/pocket', f'<div class="pg">{head}{pub}{g("Test", "Not set up")}{g("Sessions", "None yet")}{g("Review", "After the first session")}</div>')),
        ('1:10', '“Now test it” adds the test link to the same page, copied.', mini('aeroapp.ai/pocket', f'<div class="pg">{head}{pub2}{tst.format(n="new")}{g("Sessions", "None yet")}{g("Review", "After the first session")}</div>')),
        ('Later that day', 'A friend opens it on their own laptop. No account.', mini('aeroapp.ai/t/pocket-7k2', tester, 'tester')),
        ('+ 5:40', 'The session lands on the page. Transcribing.', mini('aeroapp.ai/pocket', f'<div class="pg">{head}{pub2}{tst2}{arriving}{g("Review", "After the first session")}</div>')),
        ('+ about 1 min', 'Summary and friction points, in their own words.', mini('aeroapp.ai/pocket', f'<div class="pg">{head}{pub2}{tst2}<div class="mrow"><div class="l">Session 1 · Tester A · 05:40 · Ready</div><b>1 friction point</b></div>{review}</div>')),
    ]
    fs = ''.join(f'<div class="fstep">{m}<div class="cap2"><span class="mono">{t}</span>{c}</div></div>' for t, c, m in steps)
    dots = ''.join(f'<span style="left:{(k + .5) / 6 * 100:.2f}%" class="{"end" if k == 5 else ""}"></span>' for k in range(6))
    body = f'''<div class="frame hero"><div class="cap"><b>From prompt to first session</b><span>Times are an example</span></div>
<div class="flow">{fs}</div><div class="flowline"><b></b>{dots}</div>
<div style="display:flex;justify-content:space-between;margin-top:12px;font-family:var(--mono);font-size:11px;color:var(--mut)"><span>Publish</span><span>Test</span><span>Review</span></div></div>'''
    return section('f1', '07', 'The flow', 'Studio’s flow is <b>one page that fills in</b>: after the prompt, you stay on the prototype’s own page and each step lands as a new row on it (Publish, then Test, then each session and its review). Nothing to navigate.', body)


# ---------------------------------------------------------------- m1 marketing kit
def mk_session(l='b', who='Tester B', meta='07:12 · 3 friction points', q=QUOTE, sheet=True):
    return f'''<div class="mk mk-session">{thumb('pocket', 150, 170, scale=.6, sheet=sheet)}<div><div class="who"><span class="av {l} lg">{l.upper()}</span>{who}</div>
<div class="meta">{meta}</div><q>{q}</q></div></div>'''


def mk_fq():
    return f'''<div class="mk mk-fq"><div class="top"><span class="bd"></span>Cards are hidden under More<span class="mono">03:08</span></div>
<q>I thought my cards would be on the home screen. Is it under More?</q><div class="by"><span class="av b">B</span>Tester B, in their own words</div></div>'''


def mk_site():
    return f'''<div class="mk mk-site">{thumb('pocket', 560, 230, scale=.62, top='9%')}<div class="meta"><span class="addr">pocket.aeroapp.ai</span><span class="v">v4</span><span class="st live">Live</span></div></div>'''


def mk_link():
    return f'''<div class="mk mk-link"><div class="l">Send this to your testers</div><div class="url">aeroapp.ai/t/pocket-7k2{btn('Copy link', size='md', icon='copy')}</div>
<div class="rec"><span>{ic('tab')}Their screen</span><span>{ic('mic')}Their voice</span><span>No account</span></div></div>'''


def mk_tr():
    ws = QUOTE.split(' ')
    return f'''<div class="mk mk-tr"><div class="row"><span class="mono">03:08</span><span><span class="said">{' '.join(ws[:10])}</span> <span class="now">{ws[10]}</span> {' '.join(ws[11:])}</span></div>{wave(90, .55, [(.3, False), (.55, True)], ticks=False)}</div>'''


def m1():
    app_session = f'<div class="tbl stbl" style="font-size:12px"><div class="tr2 on" style="grid-template-columns:18px 1fr 70px;height:52px"><span class="num">2</span><div class="who"><span class="av b">B</span><div>Tester B<small>07:12</small></div></div><span class="st ready">Ready</span></div></div><p class="para" style="font-size:12px">“{QUOTE}”</p>'
    app_fq = f'<div class="fq hot"><b>{FR_B[2][0]}</b><span class="mono">03:08</span><q>Is it under More?</q></div>'
    app_site = f'<div class="sc2" style="width:220px">{thumb("pocket", 220, 90, scale=.4)}<div class="meta"><span class="addr" style="font-size:11px">pocket.aeroapp.ai</span><span class="st live">Live</span><span class="hw">v4 · From a prompt, in Claude</span></div></div>'
    app_link = f'<div class="prompt" style="margin:0;background:var(--in-test)"><span class="mono" style="font-size:11.5px">aeroapp.ai/t/pocket-7k2</span>{gbtn("Copy", "copy")}</div><div style="font-size:11.5px;color:var(--mut)">Screen and voice · no account · tasks optional</div>'
    app_tr = f'<div class="trs" style="padding:0"><div class="tl fr"><span class="mono">03:02</span><span>Is the balance a button?<span class="mark"></span></span></div><div class="tl cur fr"><span class="mono">03:08</span><span><span class="said">I thought my cards would be on the home screen.</span> <span class="now">Is</span> it under More?<span class="mark"></span></span></div></div>'
    rows = [
        ('Session card', 'Sessions list, peek', app_session, mk_session(), 'wash-r', 'Thumbnail at the moment, one quote, two numbers. No device, date or status.', '1.8x'),
        ('Friction-point quote', 'Session review', app_fq, mk_fq(), 'wash-r', 'The quote grows to headline size; the title and time stay small. The blue dot carries over.', '2x'),
        ('Published site card', 'Home, Sites', app_site, mk_site(), 'wash-p', 'A big real thumbnail, the address, the version and Live. How it was made is dropped.', '2.5x'),
        ('Test link', 'Share tab', app_link, mk_link(), 'wash-t', 'One link and one button, plus the three facts a tester needs. The glass button picks up the wash.', '1.8x'),
        ('Transcript line, playing', 'Session review', app_tr, mk_tr(), 'wash-r', 'One line, set large, with the word highlight and the waveform. Only ever on a recorded replay.', '2x'),
    ]
    kr = ''.join(f'''<div class="krow"><div class="app-v"><div class="klbl"><b>{n}</b></div><div class="klbl">In the app · {w}</div>{a}<div class="knote">{note}</div></div>
<div class="mk-v {wash}"><div><div class="sizes">On the website · {sz}</div>{m}</div></div></div>''' for n, w, a, m, wash, note, sz in rows)
    hero = f'''<div class="sizes">Composed: homepage hero block, 1360 x 660, built only from the kit</div><div class="hero-block">
<h3>Publish your prototype. Watch people use it<span class="d">.</span></h3>
<p class="lead">Put a Figma prototype or HTML build online, share one link, and see real people use it. Screen and voice, transcribed for you.</p>
<div class="ctas">{btn('Start free', size='', )}{btn('See a test', 'secondary', size='')}</div>
<div class="lnk" style="margin-top:22px;font-weight:400;color:var(--ink2);font-family:var(--mono);font-size:12px">Free to start · from $3 a month · no call, no contract</div>
<div class="pos" style="left:640px;top:56px;transform:scale(.86);transform-origin:0 0">{mk_site()}</div>
<div class="pos" style="left:760px;top:330px;transform:scale(.78);transform-origin:0 0">{mk_link()}</div>
<div class="pos" style="left:560px;top:488px;transform:scale(.72);transform-origin:0 0">{mk_fq()}</div>
<div class="pos" style="right:22px;bottom:16px;font-family:var(--mono);font-size:11px;color:var(--mut)">Example</div></div>'''
    social = f'''<div class="sizes" style="margin-top:28px">Composed: social card, 1200 x 630</div><div class="social">{LOCKUP('lockup')}
<h3>In their own words<span class="d">.</span></h3>
<div class="pos" style="position:absolute;left:520px;top:70px">{mk_fq()}</div>
<div class="pos" style="position:absolute;left:600px;top:356px;transform:scale(.92);transform-origin:0 0">{mk_session('c', 'Tester C', '04:55 · 2 friction points', 'Where are my cards? I’ve tapped everything on this screen.', False)}</div>
<div class="foot">aeroapp.ai · Publish, Test, Review · Example session</div></div>'''
    body = f'<div class="kit">{kr}</div><div class="compose">{hero}{social}</div>'
    return section('m1', '08', 'Marketing kit', 'The same five components, drawn bigger with less detail and set on the step washes: Publish is peach, Test is sky, Review is mint. The composed hero reads Publish, Test, Review from top to bottom.', body)


# ---------------------------------------------------------------- page
def page():
    secs = [p1(), p2(), p3(), p4(), p5(), p6(), f1(), m1()]
    return f'''<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=1440">
<title>Aero app, Studio</title><link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@300..600&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
<header class="pagehead">{LOCKUP('logo')}<div><h1>Studio, every screen</h1></div><p>Direction A drawn across the whole app: one real window on a soft wash, colour only in the washes. Publish is peach, Test is sky, Review is mint. All names and numbers are examples.</p></header>
{''.join(secs)}<div class="end"></div>
<script>window.GLASS_MODE=window.GLASS_MODE||'subtle';</script><script>{GLASS}</script></body></html>'''


if __name__ == '__main__':
    (H / 'pages.html').write_text(page())
    print('ok', len(page()))
