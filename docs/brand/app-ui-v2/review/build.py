"""Team 1 (review), Aero app UI round v2. Builds pages.html: Sessions, Watch, Read, no tasks / no audio,
Insights, Insights empty and early states, marketing versions. Links ../shared/aero.css (owned by this team)
and review.css (screen layouts). All names are example data (Kestrel Studio, Pocket, Maya, Tom...)."""
import pathlib, math, re

H = pathlib.Path(__file__).resolve().parent
SH = H.parent / 'shared'


def svgf(name, cls=''):
    s = (SH / name).read_text().strip().replace('fill="#1D1D1F"', 'fill="currentColor"')
    return s.replace('<svg ', f'<svg class="{cls}" aria-hidden="true" ', 1) if cls else s


LOCKUP = lambda cls='logo': svgf('lockup.svg', cls)
MARK = lambda cls='': svgf('mark.svg', cls)

I = {
    'home': '<path d="M2.5 7 8 2.5 13.5 7v6.5h-4v-4h-3v4h-4z"/>',
    'site': '<rect x="2" y="3" width="12" height="10" rx="2"/><path d="M2 6h12"/>',
    'test': '<circle cx="8" cy="8" r="5.5"/><circle cx="8" cy="8" r="2"/>',
    'link': '<path d="M7 9.5a2.5 2.5 0 0 0 3.5 0l2-2a2.5 2.5 0 0 0-3.5-3.5l-.6.6M9 6.5a2.5 2.5 0 0 0-3.5 0l-2 2A2.5 2.5 0 0 0 7 12l.6-.6"/>',
    'search': '<circle cx="7" cy="7" r="4"/><path d="m10 10 3 3"/>',
    'copy': '<rect x="5" y="5" width="8" height="8" rx="1.5"/><path d="M3 10V4a1 1 0 0 1 1-1h6"/>',
    'check': '<path d="m3.5 8.5 3 3 6-7"/>',
    'arrow': '<path d="M3 8h10M9 4l4 4-4 4"/>',
    'left': '<path d="M10 3 5 8l5 5"/>',
    'right': '<path d="m6 3 5 5-5 5"/>',
    'lock': '<rect x="3.5" y="7" width="9" height="6.5" rx="1.5"/><path d="M5.5 7V5a2.5 2.5 0 0 1 5 0v2"/>',
    'ext': '<path d="M9 3h4v4M13 3 7.5 8.5M12 9.5V13H3V4h3.5"/>',
    'down': '<path d="M8 2.5v8M4.5 7 8 10.5 11.5 7M3 13.5h10"/>',
    'book': '<path d="M3 3h4a1.5 1.5 0 0 1 1.5 1.5V13A1.5 1.5 0 0 0 7 11.5H3zM13 3H9.5A1.5 1.5 0 0 0 8 4.5"/><path d="M13 3v8.5H9.5"/>',
    'play': '<path d="m5.5 3.5 7 4.5-7 4.5z"/>',
    'chev': '<path d="m5 6.5 3 3 3-3"/>',
    'chevup': '<path d="m5 9.5 3-3 3 3"/>',
    'side': '<rect x="2" y="3" width="12" height="10" rx="2"/><path d="M6 3v10"/>',
    'watch': '<rect x="1.5" y="3" width="13" height="10" rx="1.6"/><path d="m6.5 6 3.5 2-3.5 2z"/>',
    'read': '<path d="M3 4h10M3 7h10M3 10h7M3 13h5"/>',
    'note': '<path d="M3 3h10v7l-3 3H3z"/><path d="M10 13v-3h3"/>',
    'kbd': '<rect x="1.5" y="4" width="13" height="8" rx="1.5"/><path d="M4 7h.01M6.5 7h.01M9 7h.01M11.5 7h.01M5 9.5h6"/>',
    'full': '<path d="M3 6V3h3M13 6V3h-3M3 10v3h3M13 10v3h-3"/>',
    'mic0': '<rect x="6" y="2" width="4" height="8" rx="2"/><path d="M3.5 8a4.5 4.5 0 0 0 9 0M8 12.5V14M2.5 2.5l11 11"/>',
    'desk': '<rect x="1.5" y="2.5" width="13" height="9" rx="1.4"/><path d="M5.5 14h5"/>',
    'phone': '<rect x="4.5" y="1.5" width="7" height="13" rx="1.6"/><path d="M7 12.5h2"/>',
    'table': '<rect x="2" y="3" width="12" height="10" rx="1.5"/><path d="M2 6.5h12M2 10h12M6 3v10"/>',
    'clock': '<circle cx="8" cy="8" r="5.5"/><path d="M8 5v3l2 1.5"/>',
    'plus': '<path d="M8 3v10M3 8h10"/>',
    'skip': '<path d="M3 4.5 8 8l-5 3.5zM8 4.5 13 8l-5 3.5z"/>',
    'ex': '<path d="M3 13 13 3M6 3h7v7"/>',
    'filter': '<path d="M2.5 4h11M4.5 8h7M6.5 12h3"/>',
}


def ic(name, cls='i'):
    return f'<svg class="{cls}" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{I[name]}</svg>'


PLAY = '<svg viewBox="0 0 10 10"><path d="M1.5 .8 9 5l-7.5 4.2z"/></svg>'
PAUSE = '<svg viewBox="0 0 10 10"><rect x="1.5" y="1" width="2.4" height="8" rx=".6"/><rect x="6.1" y="1" width="2.4" height="8" rx=".6"/></svg>'


def btn(label, kind='primary', size='sm', icon=None, cls=''):
    fill = ' data-fill="#1D1D1F"' if kind == 'primary' else ''
    return f'<span class="btn g3 {size} {cls}" data-glass-v3="{kind}"{fill}>{ic(icon) if icon else ""}{label}</span>'


def gbtn(label, icon=None, cls='', after=''):
    return f'<span class="gbtn {cls}">{ic(icon) if icon else ""}{label}{after}</span>'


def sev(n):
    return f'<span class="sev3 s{n}"><i></i><i></i><i></i></span>'


SEVN = {'minor': 1, 'major': 2, 'critical': 3}


def tag(kind, label='', sv=None):
    word = {'issue': 'Issue', 'conf': 'Confusion', 'good': 'Works well', 'note': 'Note'}[kind]
    s = f' <span class="sev">· {sv.capitalize()}</span> {sev(SEVN[sv])}' if sv else ''
    lab = f' <span style="color:var(--ink2)">{label}</span>' if label else ''
    return f'<span class="tg {kind}"><b>{word}</b>{s}{lab}</span>'


# ---------------------------------------------------------------- example data
STUDIO, OWNER = 'Kestrel Studio', 'Mia Chen'
LEN = 432  # Maya's session, 07:12
TASKS = [('1', 'Send £20 to Sam', 18, 156), ('2', 'Find your cards', 156, 350)]
# Maya's tagged moments: seconds, kind, severity, title
MOMENTS = [
    (72, 'good', None, 'Sending felt like my bank'),
    (140, 'conf', None, 'Not sure the money had gone'),
    (161, 'issue', 'minor', 'Send has no back label'),
    (182, 'conf', None, 'Balance looks tappable'),
    (188, 'issue', 'major', 'Cards are hidden under More'),
    (252, 'good', None, 'Freezing a card is clear'),
]
NOTES_M = [(196, 'Try cards as a row under the balance')]
NOW = 189  # 03:09

# sessions, newest first. (n, name, avatar, device, browser, day, time, length, tasks, state, issue(n, sev), conf, good, line)
SESS = [
    (9, 'Ines', 'a', 'Phone', 'Safari', 'Thu 23 Oct', '18:04', '06:10', '2 of 2', 'arriving', None, 0, 0, ''),
    (8, 'Tester 8', 'f', 'Laptop', 'Firefox', 'Wed 22 Oct', '11:20', '04:02', '2 of 2', 'noaudio', None, 0, 0, ''),
    (7, 'Leo', 'f', 'Laptop', 'Chrome', 'Wed 22 Oct', '09:41', '05:18', '2 of 2', 'ready', (1, 'minor'), 1, 2, 'Found everything, but More is a funny place for cards.'),
    (6, 'Ana', 'e', 'Laptop', 'Edge', 'Tue 21 Oct', '16:02', '06:21', '1 of 2', 'ready', (2, 'major'), 1, 0, 'Gave up on cards after four minutes. “The balance looks like a button. Nothing happens.”'),
    (5, 'Jonas', 'd', 'Phone', 'Chrome', 'Tue 21 Oct', '10:15', '04:55', '2 of 2', 'ready', (1, 'major'), 2, 1, '“Where are my cards? I’ve tapped everything on this screen.”'),
    (4, 'Priya', 'c', 'Laptop', 'Safari', 'Mon 20 Oct', '19:30', '05:40', '2 of 2', 'ready', None, 1, 3, '“Send was easy. I wasn’t sure the money had gone.”'),
    (3, 'Tom', 'b', 'Laptop', 'Chrome', 'Mon 20 Oct', '18:52', '03:58', '2 of 2', 'ready', (1, 'minor'), 1, 1, 'Quick on both tasks. Wanted to type the amount rather than use the keypad.'),
    (2, 'Maya', 'a', 'Laptop', 'Chrome', 'Mon 20 Oct', '18:04', '07:12', '2 of 2', 'ready', (2, 'major'), 2, 2, '“I thought my cards would be on the home screen. Is it under More?”'),
    (1, 'You', 'm', 'Laptop', 'Chrome', 'Mon 20 Oct', '17:30', '01:52', '2 of 2', 'owner', None, 0, 0, 'Your own run, from “Open as a tester”. Not counted in Insights.'),
]
TRANSCRIPT = [  # seconds, text, tags
    ('task', 'Task 1 · Send £20 to Sam'),
    (24, 'Okay, this is Pocket. First thing, send twenty pounds to Sam.', ''),
    (72, 'Send, Sam, twenty. Easy enough, it’s a bit like my bank.', 'good'),
    (140, 'Done? I think it went. There’s no tick or anything.', 'conf'),
    ('task', 'Task 2 · Find your cards'),
    (161, 'Right, how do I get back? There’s an arrow but it doesn’t say where to.', 'issue:minor'),
    (182, 'Is the balance a button? I keep wanting to tap it.', 'conf'),
    (188, 'I thought my cards would be on the home screen. Is it under More?', 'issue:major:cur'),
    (211, 'Oh, there they are. Under More. I wouldn’t have looked there.', ''),
    (252, 'Can I freeze a card from here? Yes, okay, that’s clear.', 'good'),
    (301, 'So cards are fine once you find them. It’s just where they live.', ''),
]


def mmss(s):
    return f'{s // 60:02d}:{s % 60:02d}'


# ---------------------------------------------------------------- prototypes (the tester's content, never themed)
def pocket(sheet=False, cls=''):
    acts = [('Send', '<path d="M5 11 11 5M6 5h5v5"/>'), ('Request', '<path d="M11 5 5 11M10 11H5V6"/>'),
            ('Top up', '<path d="M8 4v8M4 8h8"/>'), ('More', '<circle cx="4" cy="8" r=".8"/><circle cx="8" cy="8" r=".8"/><circle cx="12" cy="8" r=".8"/>')]
    a = ''.join(f'<div><i><svg viewBox="0 0 16 16">{p}</svg></i>{n}</div>' for n, p in acts)
    rows = [('#FFE1D2', 'Coffee Lab', 'Today', '−£4.20'), ('#D7F0E2', 'Salary', 'Mon', '+£2,100.00'), ('#DCE8FF', 'Rail ticket', 'Sun', '−£12.80'), ('#EFE6FF', 'Bookshop', 'Sat', '−£18.00')]
    r = ''.join(f'<div class="ph-row"><i style="background:{c}"></i><div><b>{n}</b><small>{d}</small></div><b>{v}</b></div>' for c, n, d, v in rows)
    return f'''<div class="ph {cls}{' s-sheet' if sheet else ''}"><div class="ph-scr"><div class="ph-home">
<div class="ph-status"><span>9:41</span><span>●●●</span></div>
<div class="ph-hi"><span class="pa">S</span><div><small>Good morning</small><b>Sam</b></div></div>
<div class="ph-bal"><small>Balance</small><b>£1,240.50</b><span>+£86.20 this week</span></div>
<div class="ph-acts">{a}</div><div class="ph-sec">Recent<span>See all</span></div>{r}
<div class="ph-tab"><span class="on">Home</span><span>Activity</span><span>Profile</span></div></div>
<div class="ph-scrim"></div><div class="ph-sheet"><div class="hd"></div><div class="ph-sec">More<span></span></div>
<div class="sr k"><i></i><b>Cards</b></div><div class="sr"><i></i>Statements</div><div class="sr"><i></i>Savings pots</div><div class="sr"><i></i>Help</div></div>
</div></div>'''


def checkout():
    its = [('#FFE1D2', 'Linen tote', 'Natural · 1', '£28.00'), ('#D7F0E2', 'Field notebook', 'A5 · 2', '£14.00'), ('#DCE8FF', 'Pencil set', '6 pack', '£6.00')]
    it = ''.join(f'<div class="it"><i style="background:{c}"></i><div><b>{n}</b><small>{d}</small></div><b>{p}</b></div>' for c, n, d, p in its)
    return f'''<div class="co"><div class="top">Paper &amp; Co<span>Basket (3)</span></div><div class="cob"><div><h6>Checkout</h6>{it}
<div style="margin-top:14px" class="fld">Email</div><div class="fld">Card number</div></div>
<div class="sum"><div><span>Subtotal</span><span>£48.00</span></div><div><span>Delivery</span><span>Free</span></div><div class="tot"><span>Total</span><span>£48.00</span></div><div class="pay">Pay £48.00</div></div></div></div>'''


def thumb(w, h, scale=None, kind='pocket'):
    if kind == 'checkout':
        s = scale or (w * .9 / 640)
        return f'<div class="th desk" style="width:{w}px;height:{h}px"><div class="sc" style="transform:translateX(-50%) scale({s:.3f})">{checkout()}</div></div>'
    s = scale or (w * .62 / 226)
    return f'<div class="th" style="width:{w}px;height:{h}px"><div class="sc" style="transform:translateX(-50%) scale({s:.3f})">{pocket()}</div></div>'


# ---------------------------------------------------------------- waveform and timeline
def bars(n, seed=1.0, pos=None, silent=()):
    out = []
    for k in range(n):
        x = k / n
        v = .25 + .55 * abs(math.sin(k * .37 * seed + 1.3)) * (.55 + .45 * math.sin(k * .09 + .4)) + .18 * abs(math.sin(k * 1.7 * seed))
        if any(a <= x < b for a, b in silent):
            v = .06
        h = max(8, min(100, v * 100))
        out.append(f'<i class="{"p" if pos is not None and x < pos else ""}" style="height:{h:.0f}%"></i>')
    return ''.join(out)


def timeline(length=LEN, now=NOW, tasks=TASKS, moments=MOMENTS, notes=NOTES_M, n=180, only=None, audio=True, hover=None, ticks_every=60):
    p = lambda s: s / length * 100
    tk = ''
    if tasks:
        for num, name, a, b in tasks:
            on = ' on' if a <= now < b else ''
            tk = tk + f'<span class="task{on}" style="left:{p(a):.2f}%;width:calc({p(b) - p(a):.2f}% - 3px)"><span class="mono">{num}</span>{name}</span>'
        tasks_html = f'<div class="tasks">{tk}</div>'
    else:
        tasks_html = ''
    ticks = ''.join(f'<span style="left:{p(s):.2f}%">{mmss(s)}</span>' for s in range(0, length + 1, ticks_every) if 0 < s < length)
    if audio:
        wv = f'<div class="wave">{bars(n, pos=now / length, silent=((.0, .03), (.93, 1)))}</div>'
    else:
        wv = '<div class="nowave"><span>No sound in this recording</span></div>'
    mk = ''
    for s, kind, sv, title in moments:
        dim = ' dim' if only and kind != only else ''
        hot = ' hot' if s == 188 and not only else ''
        mk += f'<span class="m {kind}{dim}{hot}" style="left:{p(s):.2f}%" title="{title}"></span>'
    for s, t in notes:
        dim = ' dim' if only and only != 'note' else ''
        mk += f'<span class="m note{dim}" style="left:{p(s):.2f}%" title="{t}"></span>'
    hv = f'<span class="hover" style="left:{p(hover[0]):.2f}%">{hover[1]}</span>' if hover else ''
    return f'''<div class="tline"><div class="lanes"><div class="ticks">{ticks}</div>{tasks_html}{wv}<div class="marks">{mk}{hv}</div>
<span class="ph-line" style="left:{p(now):.2f}%"><b></b></span></div></div>'''


def mini_wave(n=34, seed=1.3, pos=None):
    return f'<div class="wave">{bars(n, seed, pos)}</div>'


def qcard(who, av, t, quote, on=False, seed=1.0, pos=None):
    return f'''<div class="qc{' on' if on else ''}"><span class="play{' pause' if on else ''}">{PAUSE if on else PLAY}</span>
<div class="who"><span class="av {av}">{who[0]}</span><b>{who}</b><span class="mono">{t}</span></div>
<q>{quote}</q>{mini_wave(40, seed, pos)}</div>'''


# ---------------------------------------------------------------- window and shell
def wbar(url):
    return f'<div class="win-bar"><span class="lights"><i></i><i></i><i></i></span><span class="win-url"><span>{ic("lock")}{url}</span></span><span class="sp"></span></div>'


TESTS = [('#1D1D1F', 'Pocket', '<span class="t b">1 new</span>'), ('#8C88F5', 'Onboarding v2', '<span class="t">2</span>'), ('#1F8F5F', 'Checkout', '<span class="t">4</span>'), ('#E58A5A', 'Pricing page', '<span class="t">0</span>')]


def sidebar(on_test='Pocket', rail=False, plan=('Pro plan', '15 of 20 test sessions', 75)):
    nav = [('home', 'Home', '', ''), ('site', 'Sites', '3', ''), ('test', 'Tests', '4', 'on')]
    n = ''.join(f'<div class="nav-i {o}">{ic(k)}<span>{l}</span><span class="ct">{c}</span></div>' for k, l, c, o in nav)
    if rail:
        return f'''<aside class="side"><div class="ws"><span class="ic">{MARK()}</span></div>{n}
<div style="margin-top:auto" class="nav-i" title="Show sidebar">{ic('side')}</div><div class="acct"><span class="av m">M</span></div></aside>'''
    rows = ''.join(f'<div class="srow {"on" if nm == on_test else ""}"><span class="swatch" style="background:{c}"></span>{nm}{t}</div>' for c, nm, t in TESTS)
    pl, pu, pw = plan
    return f'''<aside class="side"><div class="ws"><span class="ic">{MARK()}</span>{STUDIO}<span class="chev">{ic("chev")}</span><span class="collapse" title="Hide sidebar">{ic("side")}</span></div>{n}
<div class="side-lbl">Tests</div>{rows}
<div class="use"><span>{pl}</span><span class="mono">{pu}</span><i><b style="width:{pw}%"></b></i></div>
<div class="nav-i" style="margin-top:2px">{ic("book")}<span>How it works</span></div>
<div class="acct"><span class="av m">M</span><span>{OWNER}</span><span class="ex">Example</span></div></aside>'''


def window(url, side, main, h=864, rail=False):
    return f'<div class="win full">{wbar(url)}<div class="app{" rail" if rail else ""}" style="--h:{h}px">{side}<div class="main">{main}</div></div></div>'


def testhead(name='Pocket', meta=None, tab='Sessions', count='9', kind='pocket'):
    meta = meta or f'<span class="mono">aeroapp.ai/t/pocket</span><span class="st live">Live</span><span>2 tasks</span><span>Laptop and phone</span>'
    tabs = [('Sessions', count), ('Insights', ''), ('Share', ''), ('Setup', '')]
    t = ''.join(f'<span class="{"on" if l == tab else ""}">{l}{f" <span class=mono>{c}</span>" if c else ""}</span>' for l, c in tabs)
    return f'''<div class="mhead"><span class="crumb">Tests {ic('right')} <b>{name}</b></span>
<span class="r">{gbtn('Open as a tester', 'ext')}{btn('Copy test link', icon='copy')}</span></div>
<div class="testhead">{thumb(52, 52, kind=kind) if kind else ''}<div><h3>{name}</h3><div class="sub">{meta}</div></div></div>
<div class="mtabs">{t}<span class="r">Example</span></div>'''


def frames(html_light, cap, wash='review', note='', dark_first=False, h_note=''):
    dark = html_light.replace('data-fill="#1D1D1F"', 'data-fill="#F2F2F4"')
    L = f'<div class="frame {wash}" data-theme="light"><div class="cap"><b>{cap}</b><span class="th-lbl">Light</span></div>{html_light}{note}</div>'
    D = f'<div class="frame {wash}" data-theme="dark"><div class="cap"><b>{cap}</b><span class="th-lbl">Dark</span></div>{dark}{note}</div>'
    return D + L if dark_first else L + D


def section(id_, num, title, idea, body):
    return f'<section class="xp" id="{id_}"><h2><span class="n">{num}</span>{title}</h2><p class="idea">{idea}</p>{body}</section>'


def opt(text):
    return f'<div class="opt">{text}</div>'


# ================================================================ s1 Sessions tab
def s_row(s, hot=False):
    n, name, av, dev, br, day, time, ln, tasks, state, iss, conf, good, line = s
    devi = ic('phone' if dev == 'Phone' else 'desk')
    who = 'You' if state == 'owner' else name
    avh = f'<span class="av lg {av}">{"" if state == "owner" else name[0]}</span>' if state != 'owner' else f'<span class="av lg m">Y</span>'
    extra = ''
    if state == 'owner':
        extra = '<span class="lab">Owner run</span>'
    elif name.startswith('Tester'):
        extra = '<span class="lab">no name</span>'
    elif state == 'arriving':
        extra = '<span class="lab new">New</span>'
    td, tt = tasks.split(' of ')
    tdots = ''.join(f'<i class="{"" if k < int(td) else "off"}"></i>' for k in range(int(tt)))
    if state == 'arriving':
        summary = f'<div class="q arr"><span class="dotload"></span><span><b>Transcript arriving, about a minute.</b> The recording is ready to watch now.</span></div>'
        counts = '<span class="cnt shimc"><i></i></span>' * 3
    elif state == 'noaudio':
        summary = f'<div class="q dim"><span class="st noaud"></span><span><b>No audio.</b> The microphone was off, so there is no transcript or summary. You can still watch it.</span></div>'
        counts = '<span class="cnt na">–</span>' * 3
    elif state == 'owner':
        summary = f'<div class="q dim">{line}</div>'
        counts = '<span class="cnt na">–</span>' * 3
    else:
        summary = f'<div class="q">{line}</div>'
        ih = f'<span class="cnt"><span class="tg issue"><b>{iss[0]}</b></span><small>{iss[1]}</small></span>' if iss else '<span class="cnt z"><span class="tg issue z">0</span></span>'
        ch = f'<span class="cnt"><span class="tg conf"><b>{conf}</b></span></span>' if conf else '<span class="cnt z"><span class="tg conf z">0</span></span>'
        gh = f'<span class="cnt"><span class="tg good"><b>{good}</b></span></span>' if good else '<span class="cnt z"><span class="tg good z">0</span></span>'
        counts = ih + ch + gh
    act = btn('Watch', icon='play') if hot else gbtn('Watch', 'play')
    return f'''<div class="srow2{' hot' if hot else ''}{' owner' if state == 'owner' else ''}"><span class="num">{n}</span>
<div class="who">{avh}<div><b>{who}</b>{extra}<small>{devi}{dev} · {br}</small></div></div>
{summary}<div class="when"><span>{day}</span><small>{time}</small></div><span class="mono len">{ln}</span>
<span class="tasks"><span class="sdots">{tdots}</span><span class="mono">{tasks}</span></span>{counts}<span class="go">{act}</span></div>'''


def s1():
    rows = ''.join(s_row(s, hot=(s[1] == 'Maya')) for s in SESS)
    head = '''<div class="srow2 hd"><span>#</span><span>Tester</span><span>Summary, in their words where we can</span><span>When</span><span>Length</span><span>Tasks</span>
<span class="tg issue">Issue</span><span class="tg conf">Confusion</span><span class="tg good">Works well</span><span></span></div>'''
    tools = f'''<div class="stools"><div class="fchips"><span class="fchip on">All <span class="mono">9</span></span><span class="fchip">With issues <span class="mono">5</span></span><span class="fchip">No audio <span class="mono">1</span></span><span class="fchip">Phone <span class="mono">2</span></span></div>
<span class="r"><span class="input sm">{ic('search')}Search what testers said</span><span class="mono hint"><span class="kbd">J</span><span class="kbd">K</span> move · <span class="kbd">↵</span> watch</span></span></div>'''
    foot = '<div class="sfoot"><span class="st ready">Ready</span><span class="st proc">Transcript arriving</span><span class="st noaud">No audio</span><span class="r">Sessions kept: 15 of 20 on Pro, across all tests</span></div>'
    main = testhead() + f'<div class="sesbody">{tools}<div class="tbl stbl2">{head}{rows}</div>{foot}</div>'
    win = window('aeroapp.ai/tests/pocket/sessions', sidebar(), main)
    note = opt('<b>Decision for Duane.</b> Option A (shown): newest first, so a new session lands at the top. Option B: oldest first, numbered from 1, as A Studio had. I’d pick A: people open this page to see what just happened. Your own runs stay in the list as “You” and are left out of Insights (switch in Setup).')
    return section('s1', '01', 'Sessions', 'One row per tester: who, on what, how long, tasks done, and what they ran into, counted by tag. A line in their own words. The way in is a Watch button on every row, and the whole row opens the session too.', frames(win, 'Pocket · 9 sessions · Ines just finished, Tester 8 had no audio', 'test', note))


# ================================================================ s2 Watch view
def sesshead(mode='watch', name='Maya', test='Pocket', pos='2 of 9', prev='You', nxt='Tom', read_ok=True):
    rcls = ("on" if mode == "read" else "") if read_ok else 'off" title="Nothing to read: no audio'
    seg = f'<span class="seg"><span class="{"on" if mode == "watch" else ""}">{ic("watch")}Watch</span><span class="{rcls}">{ic("read")}Read</span></span>'
    return f'''<div class="mhead shead"><span class="crumb">Tests {ic('right')} {test} {ic('right')} Sessions {ic('right')} <b>{name}</b></span>
<span class="mid">{seg}</span>
<span class="r"><span class="pn">{gbtn('', 'left', 'ic')}<span class="mono">{prev} · <b>{pos}</b>{' · ' + nxt if nxt else ''}</span>{gbtn('', 'right', 'ic')}</span>{gbtn('Download', 'down', after=ic('chev'))}</span></div>'''


def meta_strip(name='Maya', av='a', dev='Laptop · Chrome 129 · macOS', when='Mon 20 Oct, 18:04', ln='07:12', rec='Screen and voice', tasks='Tasks 2 of 2'):
    t = f'<span>{tasks}</span>' if tasks else ''
    return f'''<div class="mstrip"><span class="av lg {av}">{name[0]}</span><b>{name}</b><span>{ic('desk')}{dev}</span><span>{ic('clock')}{when}</span><span class="mono">{ln}</span><span>{rec}</span>{t}<span class="r ex">Example</span></div>'''


def stage(content, pill=True, label='Recorded browser tab · Figma prototype · tab recordings have no pointer'):
    tp = '<span class="taskpill"><span class="dot"></span><span class="mono">Task 2 of 2</span>Find your cards</span>' if pill else ''
    return f'''<div class="stage3"><div class="slbl">{label}</div><div class="video">{content}<div class="vpill">{tp}</div></div></div>'''


def player_controls(only=None, playing=True, length=LEN, now=NOW, tasks=TASKS, moments=MOMENTS, notes=NOTES_M, audio=True, chips=True, hover=None):
    cnt = {k: sum(1 for m in moments if m[1] == k) for k in ('issue', 'conf', 'good')}
    ch = ''
    if chips:
        ch = f'''<div class="fchips"><span class="fchip {'' if only else 'on'}">All</span>
<span class="fchip tg issue {'on' if only == 'issue' else ''}">Issue <span class="mono">{cnt['issue']}</span></span>
<span class="fchip tg conf {'on' if only == 'conf' else ''}">Confusion <span class="mono">{cnt['conf']}</span></span>
<span class="fchip tg good {'on' if only == 'good' else ''}">Works well <span class="mono">{cnt['good']}</span></span>
<span class="fchip tg note {'on' if only == 'note' else ''}">Notes <span class="mono">{len(notes)}</span></span></div>'''
    return f'''<div class="pctl"><div class="prow"><span class="play pause">{PAUSE if playing else PLAY}</span>
<span class="tc">{mmss(now)} <span>/ {mmss(length)}</span></span>{ch}
<span class="r">{gbtn('1x', after=ic('chev'))}{'<span class="sw"><i class="on"></i>Skip silence</span>' if audio else ''}{gbtn('?', cls='ic', )}{gbtn('', 'full', 'ic')}</span></div>
{timeline(length, now, tasks, moments, notes, only=only, audio=audio, hover=hover)}</div>'''


def tline_html(row, cur_word=True):
    if row[0] == 'task':
        return f'<div class="tl task">{row[1]}</div>'
    s, text, tg = row
    tags = ''
    cls = 'past' if s < NOW else 'future'
    if 'cur' in tg:
        cls = 'cur'
    if tg:
        parts = tg.split(':')
        k = parts[0]
        sv = parts[1] if len(parts) > 1 and parts[1] in SEVN else None
        title = {72: 'Sending felt like my bank', 140: 'Not sure the money had gone', 161: 'Send has no back label', 182: 'Balance looks tappable', 188: 'Cards are hidden under More', 252: 'Freezing a card is clear'}[s]
        tags = f'<div class="tags">{tag(k, title, sv)}</div>'
    if cls == 'cur' and cur_word:
        body = '<span class="said">I thought my cards would be on the home screen.</span> <span class="now">Is</span> it under More?'
    else:
        body = text
    return f'<div class="tl {cls}"><span class="mono">{mmss(s)}</span><div><span>{body}</span>{tags}</div></div>'


def panel_transcript(back=False):
    lines = ''.join(tline_html(r) for r in TRANSCRIPT)
    bn = f'<div class="bnow">{"<span class=backnow>" + ic("down") + "Back to now · 03:09</span>" if back else ""}</div>'
    return f'''<div class="insp2"><div class="itabs"><span>Summary</span><span class="on">Transcript</span><span>Notes <span class="mono">1</span></span><span class="r">{ic('search')}</span></div>
<div class="tfollow"><span class="sw"><i class="on"></i>Follow the recording</span><span class="mono">click a line to jump</span></div>
<div class="trs scroll{' up' if back else ''}">{lines}</div>{bn}
<div class="addnote"><span class="input">{ic('note')}Add a note at 03:09<span class="kbd" style="margin-left:auto">C</span></span></div></div>'''


def panel_summary(tasks=True, audio=True, inner_only=False):
    if not audio:
        body = f'''<div class="noaud-box"><span class="mic">{ic('mic0')}</span><h4>No audio in this session</h4>
<p>The microphone was off or blocked, so there is no transcript and no summary. The screen recording is complete: you can watch all of it.</p></div>'''
        if tasks:
            body += '''<div class="sumblk"><div class="lbl2">Tasks · from the tester’s own ticks</div>
<div class="tsum"><span class="mono">1</span><div><b>Send £20 to Sam</b><span class="mut">Done · 01:36</span></div></div>
<div class="tsum"><span class="mono">2</span><div><b>Find your cards</b><span class="mut">Done · 02:50</span></div></div></div>'''
        body += f'''<div class="sumblk"><div class="lbl2">What you can still do</div>
<div class="can">{ic('watch')}<span>Watch it, at up to 3x</span></div><div class="can">{ic('note')}<span>Add notes as you watch: <span class="kbd">C</span> pauses and opens a note</span></div>
<div class="can">{ic('test')}<span>{'Its task results still count in Insights; it adds no quotes' if tasks else 'It is left out of Insights: there is nothing to quote'}</span></div></div>'''
    elif tasks:
        body = f'''<div class="sumblk"><div class="lbl2">Summary <span class="r">ready a minute after the session</span></div>
<p class="sump">Maya sent £20 to Sam without help, though she wasn’t sure it had gone. Finding her cards took over three minutes: she looked on the home screen, tried the balance, then found them under More.</p></div>
<div class="sumblk"><div class="tsum big"><span class="mono">1</span><div><b>Send £20 to Sam</b><span class="ok">{ic('check')}Done · 02:18</span>
<p>Quick and confident. No confirmation after sending, so she checked twice.</p><div class="tgs">{tag('good')}{tag('conf')}</div></div></div>
<div class="tsum big"><span class="mono">2</span><div><b>Find your cards</b><span class="ok">{ic('check')}Done · 03:14 · the longest task</span>
<p>Expected cards on the home screen. Tapped the balance, then opened More.</p><div class="tgs">{tag('issue', '', 'major')}{tag('issue', '', 'minor')}{tag('conf')}{tag('good')}</div></div></div></div>'''
    else:
        body = f'''<div class="sumblk"><div class="lbl2">Session summary <span class="r">no tasks were set</span></div>
<p class="sump">Jonas browsed the shop, filled the basket and reached payment. He liked the clean basket but hesitated at delivery: he couldn’t tell whether “Free” meant tomorrow or next week.</p></div>
<div class="sumblk"><div class="lbl2">Moments</div>
<div class="mom"><span class="mono">01:12</span>{tag('good', 'Basket is clear')}</div><div class="mom"><span class="mono">02:40</span>{tag('conf', 'Delivery date not shown')}</div><div class="mom"><span class="mono">03:05</span>{tag('issue', 'Card field rejects spaces', 'major')}</div></div>'''
    if inner_only:
        return body
    t_tab = '<span>Transcript</span>' if audio else '<span class="off" title="No audio">Transcript</span>'
    return f'''<div class="insp2"><div class="itabs"><span class="on">Summary</span>{t_tab}<span>Notes <span class="mono">1</span></span></div>
<div class="sumscroll">{body}</div>
<div class="addnote"><span class="input">{ic('note')}Add a note at {'03:09' if audio else '01:40'}<span class="kbd" style="margin-left:auto">C</span></span></div></div>'''


def s2_window():
    video = f'<div class="vfig">{pocket(sheet=False, cls="bare")}</div>'
    main = sesshead() + meta_strip() + f'''<div class="watch"><div class="wleft">{stage(video)}{player_controls()}</div>{panel_transcript()}</div>'''
    return window('aeroapp.ai/tests/pocket/sessions/2', sidebar(rail=True), main, rail=True)


def s2_states():
    keys = [('Space', 'Play, pause'), ('J  L', 'Back, forward 10 s'), ('← →', 'Back, forward 5 s'), ('C', 'Add a note (pauses)'), ('Shift N', 'Next tester'), ('Shift P', 'Previous tester'), ('1 2 3', 'Show Issue, Confusion, Works well'), ('W  R', 'Watch, Read'), ('?', 'This list')]
    kl = ''.join(f'<div class="krow2"><span class="kbd">{k}</span><span>{v}</span></div>' for k, v in keys)
    speeds = ''.join(f'<div class="it{" on" if s == "1.5x" else ""}">{s}<span class="r">{"✓" if s == "1.5x" else ""}</span></div>' for s in ['0.5x', '1x', '1.5x', '2x', '3x'])
    filt = player_controls(only='issue', chips=True)
    return f'''<div class="states2">
<div class="stcard w2"><div class="sth">Filter: Issue only. Other marks fade, the transcript keeps only issue lines, and <span class="kbd">N</span> jumps to the next one.</div><div class="pad">{filt}</div></div>
<div class="stcard"><div class="sth">Scrolled away: “Back to now” appears; following pauses until you press it.</div><div class="crop">{panel_transcript(back=True)}</div></div>
<div class="stcard"><div class="sth">Summary tab, per task</div><div class="crop">{panel_summary()}</div></div>
<div class="stcard narrow"><div class="sth"><span class="kbd">?</span> Keyboard</div><div class="pop keys">{kl}</div>
<div class="sth" style="margin-top:16px">Speed and Download</div><div style="display:flex;gap:10px"><div class="pop" style="width:110px">{speeds}</div>
<div class="pop" style="flex:1"><div class="it">{ic('down')}Download video<span class="r">.mp4</span></div><div class="it">{ic('down')}Download transcript<span class="r">.txt</span></div><div class="it">{ic('down')}Transcript and summary<span class="r">.docx</span></div><div class="sep"></div><div class="it">{ic('copy')}Copy link to 03:09</div></div></div></div>
</div>'''


def s2():
    body = frames(s2_window(), 'Maya · 03:09 · the word lights up as she says it (a recorded replay)', 'review', dark_first=True)
    body += frames(s2_states(), 'States and menus around the player', 'review', dark_first=True)
    note = opt('<b>Decisions for Duane.</b> (1) The sidebar collapses to icons on this page by default to give the recording room; the arrow brings it back. (2) Speeds 0.5x to 3x plus “Skip silence”. (3) Filters dim the other marks rather than hide them, so you still see where you are.')
    return section('s2', '02', 'Session review, Watch', 'Dark is the hero here. The recording on the left, one timeline under it with the two tasks as regions and every tag as a mark, the follow-along transcript on the right. Click a line or a mark to jump. Shift N for the next tester.', body + note)


# ================================================================ s3 Read view
def s3_window():
    tlines = ''
    margins = {
        161: f'<div class="mg">{tag("issue", "", "minor")}<b>Send has no back label</b><span class="mut">· 3 of 6</span></div>',
        182: f'<div class="mg">{tag("conf")}<b>Balance looks tappable</b><span class="mut">· 3 of 6</span></div>',
        188: f'<div class="mg">{tag("issue", "", "major")}<b>Cards are hidden under More</b><span class="mut">· 4 of 6</span></div><div class="mg note"><span class="tg note"><b>Note</b></span><span>Try cards as a row under the balance.</span><span class="mut">Mia · 03:16 · Example</span></div><div class="mg add"><span class="input">{ic("note")}Add a note at 03:09</span></div>',
        252: f'<div class="mg">{tag("good")}<b>Freezing a card is clear</b><span class="mut">· 4 of 6</span></div>',
        72: f'<div class="mg">{tag("good")}<b>Sending felt like my bank</b><span class="mut">· 6 of 6</span></div>',
        140: f'<div class="mg">{tag("conf")}<b>Not sure the money had gone</b><span class="mut">· 2 of 6</span></div>',
    }
    for r in TRANSCRIPT:
        if r[0] == 'task':
            tlines += f'<div class="rl task"><span></span><div>{r[1]}</div><span></span></div>'
            continue
        s, text, tg = r
        cur = 'cur' in tg
        body = '<span class="said">I thought my cards would be on the home screen.</span> <span class="now">Is</span> it under More?' if cur else text
        cls = 'cur' if cur else ('past' if s < NOW else 'future')
        tlines += f'<div class="rl {cls}"><span class="mono">{mmss(s)}</span><div class="t">{body}</div><div class="m">{margins.get(s, "")}</div></div>'
    pip = f'''<div class="pip"><div class="pv">{pocket(cls="bare")}<span class="taskpill sm"><span class="dot"></span>Task 2</span></div>
<div class="pc"><span class="play pause">{PAUSE}</span><span class="tc">03:09 <span>/ 07:12</span></span><span class="r">{gbtn('', 'full', 'ic quiet')}</span></div>
<div class="pt">{timeline(n=90, ticks_every=600)}</div></div>'''
    read = f'''<div class="read"><div class="col">
<div class="kick mono">Session 2 of 9 · Pocket</div>
<h1 class="hq">“Is it under More?”</h1>
<div class="by"><span class="av lg a">M</span><b>Maya</b><span>Mon 20 Oct, 18:04 · 07:12 · Laptop, Chrome · screen and voice</span><span class="ex">Example</span></div>
<div class="stand"><p>Maya sent £20 to Sam without help, though she wasn’t sure it had gone. Finding her cards took over three minutes: she looked on the home screen, tried the balance, then found them under More.</p>
<div class="tk2"><span><span class="mono">1</span> Send £20 to Sam <span class="ok">{ic('check')}02:18</span></span><span><span class="mono">2</span> Find your cards <span class="ok">{ic('check')}03:14</span></span></div></div>
<div class="rhead"><span class="lbl2">Transcript</span><span class="lbl2 r">follows the recording · click a line to play from it</span></div>
<div class="rlines">{tlines}</div></div>{pip}</div>'''
    main = sesshead('read') + read
    return window('aeroapp.ai/tests/pocket/sessions/2?view=read', sidebar(rail=True), main, rail=True)


def s3():
    body = frames(s3_window(), 'Maya, Read: her words are the headline, the summary is the standfirst, tags and notes sit in the margin', 'review')
    note = opt('<b>Decision for Duane.</b> Read opens by default when the transcript is ready and the reviewer has seen this session before? I’d keep Watch as the default for a first look and remember the last choice per person. The corner player can be dragged to any corner and closed (audio keeps playing).')
    return section('s3', '03', 'Session review, Read', 'The same session as calm reading, from C Story: the quote as the headline, the summary as a standfirst, the transcript as the body, friction and your notes in the margin. The recording shrinks to a corner and keeps playing; the word highlight still follows it.', body + note)


# ================================================================ s4 no tasks, no audio
def s4_window():
    video = f'<div class="vdesk">{checkout()}</div>'
    main = sesshead(name='Tester 4', test='Checkout', pos='4 of 4', prev='Jonas', nxt='', read_ok=False) + meta_strip('Tester 4', 'f', 'Laptop · Firefox 131 · Windows', 'Wed 22 Oct, 14:12', '03:46', 'Screen only, no audio', None) + \
        f'''<div class="watch"><div class="wleft">{stage(video, pill=False, label='Recorded browser tab · checkout.aeroapp.ai · no tasks were set, the tester explored')}{player_controls(playing=False, length=226, now=100, tasks=None, moments=[], notes=[(100, 'Paused on the card field for 20 seconds')], audio=False, chips=False)}</div>{panel_summary(tasks=False, audio=False)}</div>'''
    return window('aeroapp.ai/tests/checkout/sessions/4', sidebar('Checkout', rail=True), main, rail=True)


def s4():
    body = frames(s4_window(), 'Checkout · Tester 4 · no tasks, no audio', 'review')
    pair = f'''<div class="states2 two"><div class="stcard"><div class="sth">No tasks, with audio: one session summary and a list of moments, instead of a summary per task. The timeline has no task lane.</div><div class="crop">{panel_summary(tasks=False, audio=True)}</div></div>
<div class="stcard"><div class="sth">Tasks, no audio: the tasks still show done and time (the tester ticks them), nothing is made up.</div><div class="crop">{panel_summary(tasks=True, audio=False)}</div></div></div>'''
    body += frames(pair, 'The two half-cases', 'review')
    return section('s4', '04', 'No tasks and no audio', 'What changes, honestly. No tasks: no task lane and a single session summary. No audio: no transcript, no summary, a flat line where the waveform was, and a plain note saying so. The recording, notes and task ticks still work.', body)


# ================================================================ s5 Insights
TESTER6 = [('Maya', 'a'), ('Tom', 'b'), ('Priya', 'c'), ('Jonas', 'd'), ('Ana', 'e'), ('Leo', 'f')]


def who_dots(hit):
    return '<span class="sdots wd">' + ''.join(f'<i class="{"" if n in hit else "off"}" title="{n}"></i>' for n, _ in TESTER6) + '</span>'


def task_bars():
    # task 2, time from each tester's own task start, in seconds; marks at seconds into the task
    rows = [('Maya', 'a', 194, [(26, 'issue'), (32, 'conf'), (36, 'issue')], 'done'), ('Tom', 'b', 80, [(40, 'good')], 'done'),
            ('Priya', 'c', 65, [], 'done'), ('Jonas', 'd', 220, [(70, 'issue'), (120, 'conf'), (150, 'conf')], 'done'),
            ('Ana', 'e', 270, [(60, 'conf'), (150, 'issue'), (230, 'issue')], 'gave'), ('Leo', 'f', 130, [(90, 'issue')], 'done'),
            ('Tester 8', 'f', 170, [], 'noaud')]
    mx = 300
    out = ''
    for n, av, t, mk, st in rows:
        w = t / mx * 100
        m = ''.join(f'<span class="m {k}" style="left:{s / t * 100:.1f}%"></span>' for s, k in mk)
        end = {'done': f'<span class="end ok">{ic("check")}</span>', 'gave': '<span class="end gave">Gave up</span>', 'noaud': '<span class="end na">No audio</span>'}[st]
        out += f'<div class="tbrow"><span class="nm"><span class="av {av}">{n[0] if n != "Tester 8" else "8"}</span>{n}</span><div class="trk"><div class="b {st}" style="width:{w:.1f}%">{m}</div>{end if st != "done" else ""}<span class="tt mono" style="left:calc({w:.1f}% + 8px)">{mmss(t)}</span></div></div>'
    axis = ''.join(f'<span style="left:{s / mx * 100:.1f}%">{mmss(s)}</span>' for s in range(0, mx + 1, 60))
    med = 170 / mx * 100
    return f'''<div class="tbars"><div class="tbh"><span class="lbl2">Time on task 2, per tester, each from their own start</span><span class="lbl2 r">dashed line: median 02:50 · marks: where they hit something</span></div>
<div class="tbgrid">{out}<div class="tbrow axis"><span></span><div class="trk ax">{axis}<span class="med" style="left:{med:.1f}%"><b>median 02:50</b></span></div></div></div></div>'''


def issue_item(n, title, kind, sv, hit, desc, quotes, more=''):
    q = ''.join(qcard(*x) for x in quotes)
    return f'''<div class="iss"><span class="big">{n}</span><div class="ib"><div class="it1"><h4>{title}</h4>{tag(kind, '', sv)}</div>
<p>{desc}</p><div class="qgrid">{q}</div>{more}</div>
<div class="cnt2"><b>{len(hit)} of 6</b><small>testers</small>{who_dots(hit)}</div></div>'''


def s5_window():
    summ = '''<div class="sumcard2"><div class="lbl2">Summary <span>· 6 sessions with audio · updated Thu 18:06</span><span class="r"><span class="dotload"></span> Ines’s session joins in about a minute</span></div>
<p>Everyone sent money to Sam without help. Finding cards was the problem: <b>4 of 6 testers</b> looked on the home screen first, and Ana gave up. Three tried tapping the balance. Fix first: put cards on the home screen.</p></div>'''
    tasks = f'''<div class="blk"><div class="bh"><h3>Tasks</h3><span class="lbl2">7 sessions · Tester 8 counts here, without quotes</span></div>
<div class="tbl ttbl"><div class="tr2 hd"><span>Task</span><span>Completed</span><span>Median time</span><span>Longest</span><span>Where people got stuck</span><span></span></div>
<div class="tr2"><span class="nm"><span class="mono">1</span>Send £20 to Sam</span><span class="comp"><span class="cb"><b style="width:100%"></b></span>7 of 7</span><span class="mono">01:41</span><span class="mono">02:18 · Maya</span><span class="mut">Getting back from Send · 3 testers</span><span class="lnk">{ic('chev')}</span></div>
<div class="tr2 open"><span class="nm"><span class="mono">2</span>Find your cards</span><span class="comp"><span class="cb"><b style="width:86%"></b></span>6 of 7</span><span class="mono">02:50</span><span class="mono">04:30 · Ana, gave up</span><span class="mut">Looked on the home screen first · 5 testers</span><span class="lnk">{ic('chevup')}</span></div>
{task_bars()}</div></div>'''
    issues = issue_item(1, 'Cards are hidden under More', 'issue', 'major', ['Maya', 'Jonas', 'Ana', 'Leo'],
                        'Testers expected cards on the home screen, near the balance. They found them under More after one to four minutes.',
                        [('Maya', 'a', '03:08', 'I thought my cards would be on the home screen. Is it under More?', True, 1.0, .45), ('Jonas', 'd', '01:52', 'Where are my cards? I’ve tapped everything on this screen.', False, 1.4), ('Leo', 'f', '02:30', 'More is a funny place for cards.', False, .8)],
                        '<span class="lnk blue more">Ana’s moment, and 2 more clips</span>')
    issues += issue_item(2, 'Send has no back label', 'issue', 'minor', ['Maya', 'Tom', 'Leo'], 'An arrow alone; three testers stopped to work out how to leave Send.',
                         [('Maya', 'a', '02:41', 'There’s an arrow but it doesn’t say where to.', False, 1.2), ('Tom', 'b', '01:10', 'Is that back, or close?', False, .9)])
    issues += issue_item(3, 'Balance looks tappable', 'conf', None, ['Maya', 'Jonas', 'Ana'], 'Testers tapped the balance expecting details or cards.',
                         [('Ana', 'e', '00:48', 'The balance looks like a button. Nothing happens.', False, 1.1)])
    lst = f'''<div class="blk"><div class="bh"><h3>What to fix first</h3><span class="seg"><span class="on">By priority</span><span>By task</span><span>By theme</span></span>
<span class="r">{gbtn('Copy as table', 'table')}{btn('Download report', icon='down')}</span></div>
<div class="lbl2" style="margin:-4px 0 6px">Issues first, by severity, then by how many testers hit them. Every quote plays the moment; click a name to open the session there.</div>{issues}</div>'''
    aside = f'''<aside class="ins-side">
<div class="blk2"><div class="lbl2">Confidence</div><p class="conf"><b>Medium.</b> 6 sessions with audio. Patterns hold from 3; from 10 they are steady. Ines’s session will be added.</p></div>
<div class="blk2"><div class="lbl2">What worked</div>
<div class="wk">{tag('good')}<span>Sending money felt familiar</span><span class="mono">6 of 6</span></div>
<div class="wk">{tag('good')}<span>Freezing a card is clear</span><span class="mono">4 of 6</span></div>
<div class="wk">{tag('good')}<span>Big keypad for the amount</span><span class="mono">3 of 6</span></div></div>
<div class="blk2"><div class="lbl2">Where testers disagreed</div><div class="dis"><b>The amount keypad.</b> <span>Tom wanted to type the amount; Priya and Leo liked the big keys.</span>
<div class="dq"><span class="av b">T</span><span>“Can I just type it?”</span><span class="mono">01:02</span></div><div class="dq"><span class="av c">P</span><span>“Nice big buttons.”</span><span class="mono">00:55</span></div></div></div>
<div class="blk2"><div class="lbl2">In this summary <span class="r">open a session</span></div>
{''.join(f'<div class="sl"><span class="av {a}">{n[0]}</span>{n}<span class="mono r">{l}</span></div>' for n, a, l in [('Maya', 'a', '07:12'), ('Tom', 'b', '03:58'), ('Priya', 'c', '05:40'), ('Jonas', 'd', '04:55'), ('Ana', 'e', '06:21'), ('Leo', 'f', '05:18')])}
<div class="sl dim"><span class="av f">8</span>Tester 8<span class="mono r">tasks only</span></div><div class="sl dim"><span class="av m">Y</span>You<span class="mono r">left out</span></div></div>
<div class="how"><b>How this was made.</b> Each session is transcribed and summarised about a minute after it ends. This page groups what came up in more than one session and links every quote to its moment.</div></aside>'''
    main = testhead(tab='Insights') + f'<div class="insights"><div class="ins-main">{summ}{tasks}{lst}</div>{aside}</div>'
    return window('aeroapp.ai/tests/pocket/insights', sidebar(), main, h=1640)


def s5_alt():
    theme = f'''<div class="pad" style="padding:20px 22px"><div class="bh" style="margin-bottom:10px"><h3>Themes</h3><span class="seg"><span>By priority</span><span>By task</span><span class="on">By theme</span></span></div>
<div class="thm"><div><b>Where cards live</b><span class="mut">Cards hidden under More · Balance looks tappable</span></div>{tag('issue', '', 'major')}<span class="mono">5 of 6</span>{who_dots(['Maya', 'Jonas', 'Ana', 'Leo', 'Tom'])}</div>
<div class="thm"><div><b>Knowing the money went</b><span class="mut">No tick after Send · checked Activity</span></div>{tag('conf')}<span class="mono">2 of 6</span>{who_dots(['Priya', 'Tom'])}</div>
<div class="thm"><div><b>Moving around Send</b><span class="mut">Back arrow has no label</span></div>{tag('issue', '', 'minor')}<span class="mono">3 of 6</span>{who_dots(['Maya', 'Tom', 'Leo'])}</div>
<div class="thm"><div><b>Sending feels familiar</b><span class="mut">“A bit like my bank” · big keypad</span></div>{tag('good')}<span class="mono">6 of 6</span>{who_dots(['Maya', 'Tom', 'Priya', 'Jonas', 'Ana', 'Leo'])}</div></div>'''
    bytask = f'''<div class="pad" style="padding:20px 22px"><div class="bh" style="margin-bottom:10px"><h3>By task</h3><span class="seg"><span>By priority</span><span class="on">By task</span><span>By theme</span></span></div>
<div class="tgrp"><div class="lbl2">Task 1 · Send £20 to Sam</div><div class="thm"><div><b>Send has no back label</b></div>{tag('issue', '', 'minor')}<span class="mono">3 of 6</span></div><div class="thm"><div><b>Not sure the money had gone</b></div>{tag('conf')}<span class="mono">2 of 6</span></div></div>
<div class="tgrp"><div class="lbl2">Task 2 · Find your cards</div><div class="thm"><div><b>Cards are hidden under More</b></div>{tag('issue', '', 'major')}<span class="mono">4 of 6</span></div><div class="thm"><div><b>Balance looks tappable</b></div>{tag('conf')}<span class="mono">3 of 6</span></div><div class="thm"><div><b>Freezing a card is clear</b></div>{tag('good')}<span class="mono">4 of 6</span></div></div></div>'''
    table = '''<div class="pad" style="padding:20px 22px"><div class="bh" style="margin-bottom:10px"><h3>Copy as table</h3><span class="lbl2">pastes into FigJam, Sheets, Notion</span></div>
<div class="ctable mono"><div><b>#</b><b>Finding</b><b>Tag</b><b>Severity</b><b>Testers</b><b>Example quote</b><b>Link</b></div>
<div><span>1</span><span>Cards are hidden under More</span><span>Issue</span><span>Major</span><span>4 of 6</span><span>“Is it under More?”</span><span>…/2?t=188</span></div>
<div><span>2</span><span>Send has no back label</span><span>Issue</span><span>Minor</span><span>3 of 6</span><span>“Is that back, or close?”</span><span>…/3?t=70</span></div>
<div><span>3</span><span>Balance looks tappable</span><span>Confusion</span><span></span><span>3 of 6</span><span>“Nothing happens.”</span><span>…/6?t=48</span></div></div></div>'''
    return f'<div class="states2 three"><div class="stcard">{bytask}</div><div class="stcard">{theme}</div><div class="stcard">{table}</div></div>'


def s5():
    body = frames(s5_window(), 'Pocket · Insights · the whole page, as it scrolls', 'review')
    body += frames(s5_alt(), 'The other two views, and what “Copy as table” gives you', 'review')
    note = opt('<b>Decisions for Duane.</b> (1) Insights is a tab of the test, beside Sessions, so each test has its own; Home only links to it (“Pocket: 1 new pattern”). (2) Ranking: issues by severity, then by how many testers. (3) The D Replay timeline is used per task, each tester measured from their own start, never one shared clock. (4) Severity is three levels, set by the summary and changeable by you.')
    return section('s5', '05', 'Insights', 'Its own tab, across every session. Summary first, then a score per task, then issues ranked “4 of 6 testers” with their words as playable clips. Task 2 is opened to show where each tester spent their time on it.', body + note)


# ================================================================ s6 empty and early
def s6_empty():
    ghost = f'''<div class="ghost"><div class="gl">What this page will look like <span class="ex">Example</span></div>
<div class="gsum"><div class="lbl2">Summary</div><p>Everyone sent money without help. <b>4 of 6 testers</b> looked for cards on the home screen first.</p></div>
<div class="gtask"><span class="mono">1</span><span>Send £20 to Sam</span><span class="cb"><b style="width:100%"></b></span><span class="mono">7 of 7</span></div>
<div class="gtask"><span class="mono">2</span><span>Find your cards</span><span class="cb"><b style="width:86%"></b></span><span class="mono">6 of 7</span></div>
<div class="giss"><span class="big">1</span><div><b>Cards are hidden under More</b><div style="margin:6px 0">{tag('issue', '', 'major')}</div>{qcard('Maya', 'a', '03:08', 'Is it under More?', False, 1.0)}</div><div class="cnt2"><b>4 of 6</b>{who_dots(['Maya', 'Jonas', 'Ana', 'Leo'])}</div></div></div>'''
    left = f'''<div class="empty"><div class="lbl2">Insights</div><h2>Patterns across your testers will appear here</h2>
<p class="lead">You need a few sessions first. Here is what happens, and when.</p>
<div class="steps4"><div><span class="mono">1</span><b>Share the test link</b><span>Testers open it, allow screen and voice, and do your tasks. No account needed.</span></div>
<div><span class="mono">2</span><b>About a minute after each session</b><span>The recording is transcribed and summarised. It appears in Sessions.</span></div>
<div><span class="mono">3</span><b>From 3 sessions</b><span>This page fills in: a summary, scores per task, and issues ranked by how many testers hit them.</span></div></div>
<div class="acts">{btn('Copy test link', size='md', icon='copy')}{gbtn('Open the example', 'arrow')}</div>
<p class="small">The example is a finished study with six testers, so you can see a full review before inviting anyone.</p></div>'''
    meta = '<span class="mono">aeroapp.ai/t/pricing-page</span><span class="st live">Live</span><span>No tasks yet</span><span>Laptop testers</span>'
    main = testhead('Pricing page', meta, tab='Insights', count='0', kind='checkout') + f'<div class="emptywrap">{left}{ghost}</div>'
    return window('aeroapp.ai/tests/pricing-page/insights', sidebar('Pricing page'), main)


def s6_early():
    meta = '<span class="mono">aeroapp.ai/t/onboarding-v2</span><span class="st live">Live</span><span>1 task</span><span>Phone testers</span>'
    early = f'''<div class="early"><div class="ins-main">
<div class="wait"><span class="sdots xl"><i></i><i></i><i class="off"></i></span><div><b>Patterns appear from 3 sessions.</b> You have 2. Until then, here is what each tester said, side by side.</div>{gbtn('Open the example', 'arrow')}</div>
<div class="sumcard2"><div class="lbl2">So far <span>· 2 sessions · low confidence, treat these as leads</span></div><p>Both testers finished sign-up. Tom skipped the intro slides; Priya read every one and asked what “pots” were.</p></div>
<div class="blk"><div class="bh"><h3>Task</h3></div><div class="tbl ttbl"><div class="tr2 hd"><span>Task</span><span>Completed</span><span>Median time</span><span>Longest</span><span>Where people got stuck</span><span></span></div>
<div class="tr2"><span class="nm"><span class="mono">1</span>Create an account</span><span class="comp"><span class="cb"><b style="width:100%"></b></span>2 of 2</span><span class="mono">01:20</span><span class="mono">01:46 · Priya</span><span class="mut">Too few sessions to say</span><span></span></div></div></div>
<div class="blk"><div class="bh"><h3>Seen so far</h3><span class="lbl2">each in one session, not ranked yet</span></div>
<div class="seen">{tag('conf')}<b>What are “pots”?</b><span class="mono">1 of 2</span>{qcard('Priya', 'c', '00:58', 'Pots? Is that savings or something else?', False, 1.2)}</div>
<div class="seen">{tag('good')}<b>Skipping the intro is easy</b><span class="mono">1 of 2</span>{qcard('Tom', 'b', '00:12', 'Skip, great. I never read these.', False, .9)}</div></div></div>
<aside class="ins-side"><div class="blk2"><div class="lbl2">Confidence</div><p class="conf"><b>Low.</b> 2 sessions. One more and patterns start; from 5 they are worth acting on.</p></div>
<div class="how"><b>Why wait for 3?</b> One tester can be unusual. When two or more say the same thing, it is more likely a pattern than a person.</div></aside></div>'''
    main = testhead('Onboarding v2', meta, tab='Insights', count='2', kind=None) + early
    return window('aeroapp.ai/tests/onboarding-v2/insights', sidebar('Onboarding v2'), main)


def s6():
    body = frames(s6_empty(), 'No sessions yet', 'review')
    body += frames(s6_early(), '2 sessions', 'review')
    note = opt('<b>Decision for Duane.</b> “Open the example” opens a read-only Example study (Pocket, six testers) inside the account, not a video. It stays in the sidebar under Tests as “Example study” until dismissed.')
    return section('s6', '06', 'Insights, empty and early', 'Teach without overwhelming: say what will appear and when, show a quiet preview of a finished page, and offer the example. With 1 or 2 sessions, show what each tester said and wait to rank: “Patterns appear from 3 sessions”.', body + note)


# ================================================================ s7 marketing
def mk_row():
    return f'''<div class="mk mk-row"><span class="av xl a">M</span><div class="w"><b>Maya</b><span>07:12 · 2 of 2 tasks</span></div>
<q>I thought my cards would be on the home screen. Is it under More?</q>
<div class="c">{tag('issue')}<b>2</b></div><div class="c">{tag('conf')}<b>2</b></div><div class="c">{tag('good')}<b>2</b></div>{btn('Watch', size='lg', icon='play')}</div>'''


def mk_quote():
    return f'''<div class="mk mk-quote"><div class="top"><span class="play lg pause">{PAUSE}</span><div class="wave">{bars(70, 1.0, .42)}</div><span class="tc">03:08</span></div>
<q>I thought my cards would be on the home screen. Is it under More?</q>
<div class="by"><span class="av lg a">M</span><b>Maya</b><span>Finding your cards</span><span class="r">{tag('issue', '', 'major')}</span></div></div>'''


def mk_player():
    t = timeline(n=110, moments=[m for m in MOMENTS if m[0] in (72, 161, 188, 252)], notes=[], ticks_every=600)
    return f'''<div class="mk mk-player"><div class="v">{pocket(cls="bare")}<span class="taskpill"><span class="dot"></span><span class="mono">Task 2</span>Find your cards</span></div>
<div class="ctl"><span class="play lg pause">{PAUSE}</span><span class="tc">03:09 <span>/ 07:12</span></span><div class="tw">{t}</div></div></div>'''


def mk_card():
    return f'''<div class="social2"><div class="sc-l">{LOCKUP('lockup')}<h3>In their own words<span class="d">.</span></h3>
<div class="foot mono">aeroapp.ai · Publish, Test, Review · Example session</div></div>
<div class="sc-p">{mk_player()}</div><div class="sc-q">{mk_quote()}</div></div>'''


def s7():
    rows = [('Session row', 'Sessions tab', s_row(SESS[7], hot=False), mk_row(), 'One tester, one line in their words, three counts and one button. Date, browser and numbering are dropped.', '1.6x'),
            ('Quote card', 'Insights, Read view', qcard('Maya', 'a', '03:08', 'I thought my cards would be on the home screen. Is it under More?', True, 1.0, .42), mk_quote(), 'The quote becomes the headline. One play control, the waveform across the top, the tag kept small.', '2x'),
            ('Player with task timeline', 'Watch view', f'<div style="width:300px">{timeline(n=60, ticks_every=600)}</div>', mk_player(), 'The recording, the floating task pill and the timeline with task regions and marks. Only ever a recorded replay; no pointer.', '1.5x')]
    kr = ''.join(f'''<div class="krow2"><div class="app-v"><div class="klbl"><b>{n}</b></div><div class="klbl">In the app · {w}</div><div class="appbox">{a}</div><div class="knote">{note}</div></div>
<div class="mk-v"><div><div class="sizes">On the website · {sz}</div>{m}</div></div></div>''' for n, w, a, m, note, sz in rows)
    body = frames(f'<div class="kit2">{kr}</div>', 'Three components, app size beside website size', 'review', dark_first=True)
    body += frames(f'<div class="sizes">Social card, 1200 x 630, built only from the three</div>{mk_card()}', 'Composed card', 'review', dark_first=True)
    return section('s7', '07', 'Marketing versions', 'The real components in a demo mode: bigger, simpler, the same tokens. Dark first, as Duane asked for review demos. The card is built from these three and nothing else.', body)


# ---------------------------------------------------------------- page
def page():
    secs = [s1(), s2(), s3(), s4(), s5(), s6(), s7()]
    toggle = '''<div class="theme-toggle" role="group" aria-label="Board theme"><button aria-pressed="true" data-t="light">Light</button><button aria-pressed="false" data-t="dark">Dark</button></div>
<script>document.querySelectorAll('.theme-toggle button').forEach(function(b){b.onclick=function(){document.documentElement.setAttribute('data-theme',b.dataset.t);document.querySelectorAll('.theme-toggle button').forEach(function(x){x.setAttribute('aria-pressed',x===b)})}})</script>'''
    return f'''<!doctype html><html lang="en-GB" data-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=1440">
<title>Aero review screens</title><link rel="icon" href="../shared/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@300..600&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../shared/aero.css"><link rel="stylesheet" href="review.css"></head><body>
{toggle}
<header class="pagehead">{LOCKUP('logo')}<div><h1>Review, round v2</h1></div><p>A Studio, refined, light and dark. Sessions, the session player in two views, the hard cases, Insights and its empty states, and the marketing versions. Every frame is a 1440 x 900 window shown at 88%. All names and numbers are examples.</p></header>
{''.join(secs)}<div class="end"></div>
<script>window.GLASS_MODE=window.GLASS_MODE||'subtle';</script><script src="../shared/glass-v3.js"></script></body></html>'''


if __name__ == '__main__':
    (H / 'pages.html').write_text(page())
    print('ok')
