"""Buttons in situ (kit 2): four realistic button systems drawn inside the real app screens.
Reuses direction A Studio (explore/studio/build.py and its CSS) for everything except the buttons.
Builds pages.html. Contrast numbers come from contrast.json, written by measure.cjs (run it after a first build).
All names are example data (Kestrel Studio, Mia Chen, Pocket, Tester B)."""
import sys, json, pathlib, importlib.util

sys.dont_write_bytecode = True
H = pathlib.Path(__file__).resolve().parent
STUDIO = H.parent / 'studio'
spec = importlib.util.spec_from_file_location('studio_build', STUDIO / 'build.py')
st = importlib.util.module_from_spec(spec)
spec.loader.exec_module(st)
ic, thumb, sdots, sidebar, bar, pocket = st.ic, st.thumb, st.sdots, st.sidebar, st.bar, st.pocket
st.I.update({
    'dots': '<circle cx="3.5" cy="8" r=".9"/><circle cx="8" cy="8" r=".9"/><circle cx="12.5" cy="8" r=".9"/>',
    'x': '<path d="M4 4l8 8M12 4l-8 8"/>',
    'back5': '<path d="M3.5 8a4.5 4.5 0 1 0 1.4-3.3"/><path d="M3.5 2.8v2.4h2.4"/>',
    'fwd5': '<path d="M12.5 8a4.5 4.5 0 1 1-1.4-3.3"/><path d="M12.5 2.8v2.4h-2.4"/>',
    'full': '<path d="M3 6V3h3M10 3h3v3M13 10v3h-3M6 13H3v-3"/>',
    'min': '<path d="M4 8h8"/>',
    'trash': '<path d="M3 4.5h10M6.5 4.5V3h3v1.5M4.5 4.5l.6 8.5h5.8l.6-8.5"/>',
    'figma': '<path d="M6 2h4a2 2 0 0 1 0 4H6a2 2 0 0 1 0-4zM6 6h2v4H6a2 2 0 0 1 0-4zM8 6h2a2 2 0 1 1 0 4 2 2 0 0 1-2-2zM6 10h2v2a2 2 0 1 1-2-2z"/>',
    'zip': '<path d="M4 2h5l3 3v9H4z"/><path d="M7 4v1M7 6v1M7 8v1"/>',
    'chat': '<path d="M3 3.5h10v7H7l-3 2.5v-2.5H3z"/>',
    'ok': '<path d="m3.5 8.5 3 3 6-7"/>',
})
CSS = (STUDIO / 'src' / 'ui.css').read_text() + '\n' + (STUDIO / 'src' / 'pages.css').read_text() + '\n' + (H / 'kit2.css').read_text()
CONTRAST = json.loads((H / 'contrast.json').read_text()) if (H / 'contrast.json').exists() else {}

OPTS = {
    'o1': ('Ink', 'Near-black solid primary, white secondary with a hairline. The calmest choice: the blue dot in the logo stays the only bright thing, and it reads the same on every screen. Suits Aero if the app should feel like a precise tool.'),
    'o2': ('Deep Aero blue', 'A primary in the logo dot’s own hue, taken darker and a little greyer (#254A8D, same hue as #3478F6). The dot itself can’t carry white text (4.1:1), this can (8.6:1). Suits Aero if the app should feel branded and a touch warmer than black.'),
    'o3': ('Ink, glass where it floats', 'Option 1 everywhere you read, so the dashboard and every modal look exactly like option 1. The accessible V3 glass appears only on small controls that float over content Aero can’t predict: the player controls and the task chip over the recording, “I’m done” and the folded pill on the tester screen. Panels are the frosted plate (86% white, 22px blur).'),
    'o4': ('Soft graphite', 'A warm graphite pill for the primary and a warm stone fill for the secondary: no pure black, no hairlines, round ends. The calmest-looking app, closer to a notes app than a dev tool. Suits Aero if most people using it are designers who find black buttons heavy.'),
}
GLASS_CTRL = {'o3'}


# ---------------------------------------------------------------- the one thing that changes
def B(label='', kind='pri', size='', icon=None, o='o1', fl=False, state='', m=None, t=4.5, cls='', lbl=None):
    """kind: pri | sec | dan | qui. fl: floats over unknown content (glass in option 3).
    state: '', hover, focus, disabled, loading. m: name in the contrast table."""
    glass = fl and o in GLASS_CTRL
    a = ''
    c = ['bt', kind, size, cls]
    if glass:
        c.append('gx')
        a += f' data-glass-v3="{"primary" if kind == "pri" else "secondary"}"'
        if kind == 'pri':
            a += ' data-fill="#1D1D1F"'
    if state in ('hover', 'focus'):
        c.append(state)
    if state == 'disabled':
        a += ' disabled'
    if state == 'loading':
        a += ' aria-busy="true"'
    if m:
        a += f' data-m="{m}" data-t="{t}"'
    if not label:
        a += f' aria-label="{icon}"'
    lead = '<span class="spin" aria-hidden="true"></span>' if state == 'loading' else (ic(icon) if icon else '')
    return f'<button class="{" ".join(x for x in c if x)}"{a}><span class="bi">{lead}{f"<span class=lb>{label}</span>" if label else ""}</span></button>'


# ---------------------------------------------------------------- windows
def win(url, side, main, h=820, ov='', cls=''):
    o = f'<div class="ov">{ov}</div>' if ov else ''
    return f'<div class="win {cls}">{bar(url)}<div class="appwrap"><div class="app" style="--h:{h}px">{side}<div class="main">{main}</div></div>{o}</div></div>'


def frame(letter, title, note, body, wash='hero'):
    return f'<div class="frame {wash}"><div class="cap"><b>{letter}</b><b>{title}</b><span>{note}</span></div>{body}</div>'


# ---------------------------------------------------------------- a. dashboard
def dash_main(o, m=True):
    mm = (lambda s: s) if m else (lambda s: None)
    feed = f'''<div class="feed">
<div class="fi wash-r">{thumb('pocket', 76, 60)}<div><div class="w"><b>Pocket</b>12 min ago</div>
<div class="what">2 new sessions. Tester E had no audio, Tester F is being transcribed.</div></div>
<div class="acts">{sdots(['', '', '', '', 'no', 'pr'])}{B('Open sessions', 'sec', 'sm', o=o, m=mm('Small secondary, list row'))}</div></div>
<div class="fi">{thumb('pocket', 76, 60, sheet=True)}<div><div class="w"><b>Pocket</b>review · sessions 1 to 4</div>
<div class="what">Cards expected on the home screen, 3 of 4 testers. <q>Is it under More?</q></div></div>
<div class="acts">{B('Review', 'sec', 'sm', o=o)}</div></div>
<div class="fi">{thumb('checkout', 76, 60)}<div><div class="w"><b>Checkout</b>2 hours ago</div>
<div class="what">Version 8 is live at <span class="mono" style="font-size:12.5px">checkout.aeroapp.ai</span>. Nobody has opened the test link yet.</div></div>
<div class="acts">{B('Copy test link', 'sec', 'sm', 'copy', o=o)}</div></div>
<div class="fi">{thumb('onboarding', 76, 60)}<div><div class="w"><b>Onboarding v2</b>yesterday</div>
<div class="what">Review ready for 2 sessions. Both testers skipped the second screen.</div></div>
<div class="acts">{B('Review', 'sec', 'sm', o=o)}</div></div></div>'''
    rows = [('Pocket', 'pocket.aeroapp.ai', ['', '', '', '', 'no', 'pr'], '12 min ago', '<span class="st new">2 new</span>', '#1D1D1F', '2 tasks'),
            ('Onboarding v2', 'onboarding-v2.aeroapp.ai', ['', ''], 'Yesterday', '<span class="st ready">Reviewed</span>', '#8C88F5', 'Explore freely'),
            ('Checkout', 'checkout.aeroapp.ai', [], 'None yet', '<span class="st">Link ready</span>', '#1F8F5F', '3 tasks')]
    tr = ''.join(f'<div class="tr2"><div class="nm"><span class="swatch" style="background:{c}"></span><div>{n}<small>{s}</small></div></div><div>{sdots(d) if d else "<span class=mut>No sessions</span>"}</div><div class="mut">{k}</div><div class="mut">{w}</div><div>{stt}</div></div>' for n, s, d, w, stt, c, k in rows)
    tests = f'<div class="tbl tests"><div class="tr2 hd"><span>Test</span><span>Sessions</span><span>Tasks</span><span>Last</span><span>Status</span></div>{tr}</div>'
    sites = [('pocket', 'pocket.aeroapp.ai', 'v4', 'From a prompt, in Claude'), ('onboarding', 'onboarding-v2.aeroapp.ai', 'v2', 'Figma prototype link'), ('checkout', 'checkout.aeroapp.ai', 'v8', 'HTML upload')]
    sc = ''.join(f'<div class="sc2">{thumb(k, 300, 112, scale=(0.36 if k == "checkout" else 0.5), top=("14%" if k == "checkout" else "12%"))}<div class="meta"><span class="addr">{a}</span><span class="st live">Live</span><span class="hw">{v} · {hh}</span></div></div>' for k, a, v, hh in sites)
    return f'''<div class="mhead"><span class="crumb"><b>Home</b></span><div class="r">{B('', 'sec', '', 'search', o=o, cls='icon')}{B('New test', 'sec', '', 'plus', o=o, m=mm('Secondary, page header'))}{B('Publish', 'pri', '', 'plus', o=o, m=mm('Primary, page header'))}</div></div>
<div class="mbody"><div class="home"><div>
<div class="hh"><h3>What’s new</h3><span class="mono">since you looked, Wed 09:12</span></div>{feed}
<div class="hh"><h3>Tests</h3><span class="mono">3</span><span class="r lnk">All tests {ic('arrow')}</span></div>{tests}</div>
<div><div class="hh"><h3>Sites</h3><span class="mono">3 live</span><span class="r lnk">All sites {ic('arrow')}</span></div><div class="sitelist">{sc}</div></div>
</div></div>'''


def dash(o, ov='', h=820, m=True, cls=''):
    return win('aeroapp.ai/home', sidebar('Home', 'tests'), dash_main(o, m and not ov), h=h, ov=ov, cls=cls)


# ---------------------------------------------------------------- b. session review
def review_main(o, m=True):
    mm = (lambda s: s) if m else (lambda s: None)
    length = 432
    marks = [(st.tsec(t) / length, t == '03:08') for _, t, _ in st.FR_B]
    pos = 189 / length
    fps = ''.join(f'<div class="fq {"hot" if i == 2 else ""}"><b>{t}</b><span class="mono">{tc}</span><q>{q}</q></div>' for i, (t, tc, q) in enumerate(st.FR_B))
    pause = '<svg class="i" viewBox="0 0 16 16" aria-hidden="true"><path fill="currentColor" d="M4.5 3h2.4v10H4.5zM9.1 3h2.4v10H9.1z"/></svg>'
    glass = o in GLASS_CTRL
    if glass:
        ctl = f'''<div class="pctl gl">{B('', 'pri', 'lg', None, o=o, fl=True, cls='icon round pp', m=mm('Pause over the recording (icon, 3:1)'), t=3).replace('<span class="bi">', '<span class="bi">' + pause)}
{B('', 'sec', '', 'back5', o=o, fl=True, cls='icon round')}{B('', 'sec', '', 'fwd5', o=o, fl=True, cls='icon round')}{B('1x', 'sec', '', None, o=o, fl=True, cls='spd', m=mm('Speed over the recording'))}{B('', 'sec', '', 'full', o=o, fl=True, cls='icon round')}</div>'''
    else:
        ctl = f'''<div class="pctl plate">{B('', 'pri', 'lg', None, o=o, cls='icon round pp', m=mm('Pause over the recording (icon, 3:1)'), t=3).replace('<span class="bi">', '<span class="bi">' + pause)}
{B('', 'qui', '', 'back5', o=o, cls='icon round')}{B('', 'qui', '', 'fwd5', o=o, cls='icon round')}<span class="pdiv"></span>{B('1x', 'qui', 'sm', None, o=o, cls='spd', m=mm('Speed over the recording'))}{B('', 'qui', '', 'full', o=o, cls='icon round')}</div>'''
    task = B('Task 2 of 2 · Find your cards', 'sec', 'sm', None, o=o, fl=True, cls='taskchip', m=mm('Task chip over the recording'))
    return f'''<div class="mhead"><span class="crumb">Tests {ic('right')} Pocket {ic('right')} <b>Session 2 · Tester B</b></span>
<div class="r"><span class="navs">{B('', 'sec', 'sm', 'left', o=o, cls='icon')}<span class="mono nv">2 of 6</span>{B('', 'sec', 'sm', 'right', o=o, cls='icon')}</span>{B('Download summary', 'sec', '', 'down', o=o, m=mm('Secondary, session header'))}{B('', 'sec', '', 'dots', o=o, cls='icon')}</div></div>
<div class="sv2"><div class="svm"><div class="stage2"><div class="tag"><span>Screen and voice · Laptop · Chrome · Mon 20 Oct</span></div>
<div class="vid"><div class="vph">{pocket()}</div>{task}{ctl}</div></div>
<div class="scrub nop"><span class="tc">03:09 <span>/ 07:12</span></span>{st.wave(110, pos, marks)}</div>
<div class="below"><div><div class="lbl2">Summary · ready 1 min after the session</div><p class="para" style="margin-top:8px">Tester B sent £20 to Sam without help. Looking for cards, they checked the home screen and the balance for about 30 seconds before opening More.</p></div>
<div><div class="lbl2">Top priorities</div><ol><li><span class="mono">01</span>Show cards on the home screen</li><li><span class="mono">02</span>Label the back arrow in Send</li><li><span class="mono">03</span>Make the balance look less like a button</li></ol></div></div></div>
<div class="insp"><div class="itabs"><span class="on">Transcript</span><span>Notes</span><span class="r">follows the recording</span></div>
<div class="trs">{st.transcript_lines()}</div>
<div class="fps2"><div class="lbl2"><span class="bd" style="width:7px;height:7px;border-radius:50%;background:var(--blue);display:inline-block"></span>Friction points, in their own words<span class="r">click to play</span></div>{fps}</div>
<div class="how"><b>How this was made.</b> The recording was transcribed and summarised about a minute after the session ended. Quotes are the tester’s exact words.</div></div></div>'''


def review(o, ov='', m=True):
    return win('aeroapp.ai/tests/pocket/sessions/2', sidebar('Tests', 'sessions', on_session=2), review_main(o, m and not ov), h=820, ov=ov)


# ---------------------------------------------------------------- modals
def modal(title, sub, body, foot, o, w=480, foot_left=''):
    return f'''<div class="mdl" style="width:{w}px" role="dialog" aria-label="{title}"><div class="mdl-h"><div><h4>{title}</h4>{f"<p>{sub}</p>" if sub else ""}</div>{B('', 'qui', 'sm', 'x', o=o, cls='icon mx')}</div>
<div class="mdl-b">{body}</div><div class="mdl-f">{foot_left}<span class="sp"></span>{foot}</div></div>'''


def share_modal(o, m=True):
    mm = (lambda s: s) if m else (lambda s: None)
    body = f'''<div class="fl-l">Test link</div><div class="linkrow"><div class="lf mono">aeroapp.ai/t/pocket-7k2m</div>{B('Copy link', 'pri', '', 'copy', o=o, m=mm('Primary, modal'))}</div>
<div class="mrows"><div><span class="k">Testers see</span><span>Pocket, 2 tasks, then a thank you</span></div><div><span class="k">Recorded</span><span>One browser tab and their voice, after they say yes</span></div><div><span class="k">Account</span><span>Not needed. Anyone with the link can take it</span></div></div>'''
    return modal('Share the test', 'Pocket · pocket.aeroapp.ai · v4', body, B('Done', 'sec', '', None, o=o, m=mm('Secondary, modal')), o,
                 foot_left=f'<span class="lnk q">{ic("ext")}Open as a tester</span>')


def delete_modal(o):
    body = '<p class="mp">Session 2 with Tester B (07:12) will be deleted with its recording, transcript and summary. Quotes from it will disappear from the Pocket review.</p><p class="mp dim">This can’t be undone.</p>'
    foot = B('Cancel', 'sec', '', None, o=o, m='Secondary, confirm') + B('Delete session', 'dan', '', None, o=o, m='Destructive, confirm')
    return modal('Delete this session?', '', body, foot, o, w=440)


def choice(icon, title, desc, sel=False, extra=''):
    return f'<div class="ch {"on" if sel else ""}"><span class="rd"></span><span class="chi">{ic(icon)}</span><div><b>{title}</b><small>{desc}</small>{extra}</div></div>'


def newtest_modal(o, chosen=True, m=True):
    ex = '<div class="lf mono sm">figma.com/proto/8fK2pQ/Pocket?node-id=12-4</div>' if chosen else ''
    body = (choice('figma', 'Figma prototype link', 'Paste the prototype link. Testers use it in their browser.', chosen, ex)
            + choice('zip', 'HTML or zip', 'Upload a file, a folder or a zip. It goes live at name.aeroapp.ai first.')
            + choice('chat', 'From Claude or ChatGPT', 'One prompt publishes it through the Aero connector, then the test is ready.')
            + '<div class="orsite">Or test a site you’ve published: <span class="mono">pocket.aeroapp.ai</span> <span class="mono">checkout.aeroapp.ai</span></div>')
    hint = '' if chosen else '<span class="hint">Choose where it comes from</span>'
    foot = hint + B('Cancel', 'sec', '', None, o=o) + B('Continue', 'pri', '', None, o=o, state='' if chosen else 'disabled',
                                                        m=('Primary, modal (Continue)' if chosen else 'Disabled primary (exempt)') if m else None, t=4.5 if chosen else 0)
    return modal('New test', 'What will testers use?', body, foot, o, w=520)


def publish_modal(o):
    body = '''<div class="file"><span class="chi">''' + ic('zip') + '''</span><div><b>checkout-v8.zip</b><small>17 files · 2.4 MB · index.html found</small></div><span class="ok">''' + ic('ok') + '''Uploaded</span></div>
<div class="pbar"><i style="width:100%"></i></div>
<div class="mrows"><div><span class="k">Address</span><span class="mono">checkout.aeroapp.ai</span></div><div><span class="k">Version</span><span>8, replaces version 7 (kept, you can roll back)</span></div></div>'''
    foot = B('Cancel', 'sec', '', None, o=o, state='disabled') + B('Publishing', 'pri', '', None, o=o, state='loading', m='Loading primary (Publishing)', cls='w-pub')
    return modal('Publish HTML or zip', 'Checkout', body, foot, o, w=480)


# ---------------------------------------------------------------- f. tester
def pocket_web():
    return f'''<div class="pw"><div class="pw-nav"><b>Pocket</b><span>Cards</span><span>Pots</span><span>Splits</span><span class="cta">Get the app</span></div>
<i class="bl b1"></i><i class="bl b2"></i><i class="bl b3"></i>
<div class="pw-hero"><h1>Split it before the bill arrives.</h1><p>Send, split and save with friends. Your cards, pots and splits in one place.</p></div>
<div class="pw-ph">{pocket()}</div>
<div class="pw-band"><div><b>Cards</b><span>Freeze, unfreeze, order a new one</span></div><div><b>Pots</b><span>Put money aside for the holiday</span></div><div><b>Splits</b><span>Share the bill as you pay</span></div></div></div>'''


def task_panel(o, m=True):
    mm = (lambda s: s) if m else (lambda s: None)
    return f'''<div class="tp"><div class="tp-h"><span class="rec"><i></i>Recording <span class="mono">04:12</span></span><span class="mono tn">Task 2 of 3</span>{B('', 'qui', 'sm', 'min', o=o, cls='icon')}</div>
<div class="tp-b"><div class="prog"><i class="d"></i><i class="c"></i><i></i></div><h4>Find your cards</h4><p>You’ve lost a card and want to freeze it. Find where Pocket keeps your cards.</p>
<div class="tp-a">{B('I’m done', 'pri', '', None, o=o, fl=True, cls='grow', m=mm('Primary, tester panel'))}{B('Skip', 'sec', '', None, o=o, m=mm('Secondary, tester panel'))}</div></div>
<div class="tp-f">Say what you’re thinking as you go.<span class="lnk q">End test</span></div></div>'''


def tester_pill(o, where, m=True):
    mm = (lambda s: s) if m else (lambda s: None)
    if o in GLASS_CTRL:
        return f'<button class="bt sec gx tpill-g" data-glass-v3="secondary"{f" data-m=\"Folded pill over {where}\" data-t=\"4.5\"" if m else ""}><span class="bi"><i class="rdot"></i><span class="lb">04:12 · Task 2 of 3</span><span class="psep"></span><span class="lb">Open</span></span></button>'
    return f'<div class="tpill"{f" data-m=\"Folded pill over {where}\" data-t=\"4.5\"" if m else ""}><i class="rdot"></i><span class="lb" data-lbl>04:12 · Task 2 of 3</span>{B("Open", "pri", "sm", None, o=o)}</div>'


def tester(o):
    w = win('pocket.aeroapp.ai', '', f'<div class="tview">{pocket_web()}<div class="tp-at">{task_panel(o)}</div></div>', h=680, cls='tw')
    crops = ''
    for where, x, y in [('coral', 40, 330), ('busy colour', 851, 300), ('black with text', 520, 494)]:
        crops += f'<div class="pcrop"><div class="pcin" style="left:-{x}px;top:-{y}px">{pocket_web()}</div><div class="pcp">{tester_pill(o, where)}</div><span class="pcl mono">Folded, over {where}</span></div>'
    return w + f'<div class="pcrops">{crops}</div>'


# ---------------------------------------------------------------- g. states
def states(o):
    def cell(btn, lab):
        return f'<div class="sc"><div class="sb">{btn}</div><span class="mono">{lab}</span></div>'
    rows = ''
    sets = [('Primary', 'pri', 'Publish', 'plus'), ('Secondary', 'sec', 'New test', 'plus'), ('Destructive', 'dan', 'Delete session', None)]
    for name, k, lab, icn in sets:
        cells = cell(B(lab, k, '', icn, o=o), 'Rest') + cell(B(lab, k, '', icn, o=o, state='hover', m=f'{name}, hover' if k != 'dan' else None), 'Hover') + cell(B(lab, k, '', icn, o=o, state='focus'), 'Keyboard focus')
        if k != 'dan':
            cells += cell(B(lab, k, '', icn, o=o, state='disabled'), 'Disabled') + cell(B('Publishing' if k == 'pri' else 'Saving', k, '', None, o=o, state='loading'), 'Loading')
            cells += cell(B(lab, k, 'sm', icn, o=o), 'Small')
        rows += f'<div class="srow2"><span class="sn">{name}</span>{cells}</div>'
    if o in GLASS_CTRL:
        cells = ''
        for bg, nm in [('#2B2B2E', 'Figma grey'), ('#FF5A3C', 'coral'), ('#FFD23F', 'yellow'), ('#FFFFFF', 'white')]:
            cells += f'<div class="sc"><div class="sb gbg" style="background:{bg}">{B("", "pri", "lg", "play", o=o, fl=True, cls="icon round")}{B("1x", "sec", "", None, o=o, fl=True)}</div><span class="mono">Over {nm}</span></div>'
        rows += f'<div class="srow2"><span class="sn">Glass, floating</span>{cells}</div>'
    return f'<div class="states">{rows}</div>'


def g_frame(o):
    left = win('aeroapp.ai/home', sidebar('Home', 'tests'), dash_main(o, False), h=600, ov=newtest_modal(o, chosen=False), cls='half')
    right = win('aeroapp.ai/home', sidebar('Home', 'tests'), dash_main(o, False), h=600, ov=publish_modal(o), cls='half')
    return f'''<div class="halves"><div><div class="sublab">Continue stays disabled until a way is chosen, and says why</div>{left}</div>
<div><div class="sublab">Publishing: the button keeps its width and fill; Cancel waits</div>{right}</div></div>
<div class="sublab" style="margin-top:28px">Every state at real size</div>{states(o)}'''


# ---------------------------------------------------------------- contrast table
def ctable(o):
    rows = CONTRAST.get(o)
    if not rows:
        return '<div class="ct-empty">Contrast not measured yet: run measure.cjs.</div>'
    tr = ''
    for r in rows:
        t = r['t']
        if t == 0:
            verdict = '<span class="ex">Exempt (disabled)</span>'
        else:
            verdict = f'<span class="{"ok" if r["ratio"] >= t else "no"}">{"Pass" if r["ratio"] >= t else "Fail"} {t:g}:1</span>'
        tr += f'''<div class="ctr"><span>{r["name"]}</span><span class="sw"><i style="background:{r["fg"]}"></i>{r["fg"]}</span><span class="sw"><i style="background:{r["bg"]}"></i>{r["bg"]}{" worst pixel" if r.get("varied") else ""}</span><span class="mono rt">{r["ratio"]:.2f}:1</span>{verdict}</div>'''
    extra = ''.join(f'<div class="ctr nt"><span>{n}</span><span class="sw"><i style="background:{a}"></i>{a}</span><span class="sw"><i style="background:{b}"></i>{b}</span><span class="mono rt">{st_cr(a, b):.2f}:1</span><span class="{"ok" if st_cr(a, b) >= th else "inf"}">{("Pass " + str(th) + ":1") if st_cr(a, b) >= th else "Below 3:1, label carries it"}</span></div>' for n, a, b, th in NONTEXT[o])
    return f'''<div class="ctab"><div class="ctr hd"><span>Button, where</span><span>Label</span><span>Behind the label</span><span>Ratio</span><span>WCAG AA</span></div>{tr}{extra}</div>
<p class="cnote">Measured in Chromium at 2x: the label is hidden, the area under its text is captured, and the ratio is taken against the worst pixel there (for solid fills that is the fill). Icon-only controls need 3:1. The last rows are non-text parts, computed from the tokens.</p>'''


def st_cr(a, b):
    def lin(v):
        v /= 255
        return v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4

    def lum(h):
        h = h.lstrip('#')
        c = [int(h[i:i + 2], 16) for i in (0, 2, 4)]
        return .2126 * lin(c[0]) + .7152 * lin(c[1]) + .0722 * lin(c[2])
    x, y = lum(a) + .05, lum(b) + .05
    return max(x, y) / min(x, y)


NONTEXT = {
    'o1': [('Focus ring vs white page', '#3478F6', '#FFFFFF', 3), ('Secondary hairline vs white', '#D2D2D7', '#FFFFFF', 3)],
    'o2': [('Focus ring vs white page', '#3478F6', '#FFFFFF', 3), ('Primary fill vs white (shape)', '#254A8D', '#FFFFFF', 3), ('Secondary hairline vs white', '#D3D8E2', '#FFFFFF', 3)],
    'o3': [('Focus ring vs white page', '#3478F6', '#FFFFFF', 3), ('Secondary hairline vs white', '#D2D2D7', '#FFFFFF', 3)],
    'o4': [('Focus ring vs white page', '#3478F6', '#FFFFFF', 3), ('Secondary stone fill vs white', '#EFECE7', '#FFFFFF', 3)],
}


# ---------------------------------------------------------------- sections
def option(o):
    name, idea = OPTS[o]
    n = o[1]
    fr = [
        frame('a', 'Home dashboard', 'Page header: New test and Publish. Each row has one small action.', dash(o)),
        frame('b', 'Session review', 'Header actions, and the player controls floating over the recording (a Figma prototype on its grey canvas, no cursor)', review(o), 'review'),
        frame('c', 'Share modal', 'Opened from Copy test link, over the dimmed dashboard', dash(o, ov=share_modal(o)), 'test'),
        frame('d', 'Confirm delete', 'Opened from the ⋯ menu in the session header', review(o, ov=delete_modal(o)), 'review'),
        frame('e', 'New test modal', 'Figma prototype chosen, so Continue is ready', dash(o, ov=newtest_modal(o)), 'hero'),
        frame('f', 'Tester task panel', 'What Tester B sees over a bright prototype at pocket.aeroapp.ai. The panel is the frosted plate in every option.', tester(o), 'test'),
        frame('g', 'Disabled and loading, in place', 'Two moments, then every state at real size', g_frame(o), 'publish'),
    ]
    return f'''<section class="xp opt {o}" id="{o}"><h2><span class="n">0{n}</span>{name}</h2><p class="idea">{idea}</p>{''.join(fr)}
<div class="frame plain"><div class="cap"><b>Contrast</b><span>Each label against its fill, measured</span></div>{ctable(o)}</div></section>'''


def cmp():
    cells1 = ''.join(f'<div class="cc {o}"><div class="ccl"><b>0{o[1]}</b> {OPTS[o][0]}</div><div class="crop c1"><div class="cin" style="right:0;top:-37px">{dash(o, m=False)}</div></div></div>' for o in OPTS)
    cells2 = ''
    for o in OPTS:
        cells2 += f'<div class="cc {o}"><div class="ccl"><b>0{o[1]}</b> {OPTS[o][0]}</div><div class="crop c2"><div class="cin" style="left:-330px;top:-140px">{dash(o, m=False)}</div><div class="cov">{share_modal(o, m=False)}</div></div></div>'
    body = f'''<div class="frame hero"><div class="cap"><b>1</b><b>Dashboard header and the first row</b><span>Real size, right-hand side of the window</span></div><div class="cgrid">{cells1}</div></div>
<div class="frame test"><div class="cap"><b>2</b><b>Share modal</b><span>Real size, over the dimmed dashboard</span></div><div class="cgrid">{cells2}</div></div>'''
    return f'<section class="xp" id="cmp"><h2><span class="n">05</span>Side by side</h2><p class="idea">The same two moments in all four options. Options 1 and 3 are the same here on purpose: glass only appears where controls float over the recording or a prototype.</p>{body}</section>'


def rec():
    return '''<section class="xp" id="rec"><h2><span class="n">06</span>Recommendation</h2><div class="recbox">
<p><b>Pick option 3: ink solid where you read, accessible glass only where controls float.</b> On the dashboard and in every modal it is option 1, the calmest and most legible set (16.8:1), and the blue dot stays the one bright thing.</p>
<p>Glass earns its place in the three spots where Aero can’t know what is behind a control (the player over the recording, the task chip, the tester’s “I’m done” and folded pill), and the measured worst-pixel ratios above show it now holds AA there.</p>
<p>Keep option 2’s deep blue (#254A8D) in reserve for marketing calls to action, where a coloured primary helps. In the app it makes every screen a little louder and puts a second blue next to the dot. Drop option 4: calm, but every button becomes a soft pill, so Publish and the row actions look alike and the dashboard drifts towards the “pills on everything” look.</p>
<p>Test next: a five-second test of the dashboard (does Publish read as the main action?) and the tester panel over five real customer prototypes.</p></div></section>'''


def page():
    secs = [option(o) for o in OPTS] + [cmp(), rec()]
    return f'''<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=1440">
<title>Aero buttons in situ</title><link rel="icon" href="{st.FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@300..600&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
<header class="pagehead">{st.LOCKUP('logo')}<div><h1>Buttons, in the app</h1></div><p>Four realistic button systems, each drawn full size on the same seven moments: the dashboard, a session, three modals, the tester screen and the disabled and loading states. Only the buttons change. Example data throughout.</p></header>
<nav class="toc">{''.join(f'<a href="#{o}"><b>0{o[1]}</b>{OPTS[o][0]}</a>' for o in OPTS)}<a href="#cmp"><b>05</b>Side by side</a><a href="#rec"><b>06</b>Recommendation</a></nav>
{''.join(secs)}<div class="end"></div>
<script>window.GLASS_MODE=window.GLASS_MODE||'subtle';</script><script src="glass-v3.js"></script></body></html>'''


if __name__ == '__main__':
    out = page()
    (H / 'pages.html').write_text(out)
    print('ok', len(out))
