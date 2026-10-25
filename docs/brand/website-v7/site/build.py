#!/usr/bin/env python3
"""Aero website round 4 (24 Oct 2026), Team S: the pages other than the homepage.

Builds features.html, pricing.html, use-cases.html, guides.html, publish-a-claude-artifact.html (the SEO task page
template), blog.html and one page per post (blog-<slug>.html, all from one template).

- Header, footer, type, pills, washes, the headline dot and the glass come from ../shared/aero.css (Team H's WEBSITE
  block); this folder only adds site.css (page layouts, prefix s-) and site.js.
- Every product picture is a crop of a real v3 app component, imported read-only from ../../v3/make/build.py and
  ../../v3/review/build.py. A crop names the screen and a CSS selector; site.js measures the element inside the real
  1440px window and scales that part to fit (see crop()).
- All words a visitor reads are in the COPY dict of each page below; the same dict is embedded at the top of each page
  as <script type="application/json" id="copy">. Strings there can be edited in place; lists need a rebuild.
Names, sessions and numbers in the pictures are examples (Kestrel Studio, Mia Chen, Pocket, Maya...)."""
import html, importlib.util, json, pathlib, re

H = pathlib.Path(__file__).resolve().parent
V3 = H.parent.parent / 'v3'
SH = H.parent / 'shared'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


mk = load('v3make', V3 / 'make/build.py')
rv = load('v3review', V3 / 'review/build.py')
ic = mk.ic
E = lambda s: html.escape(s, quote=False)


def lockup():
    s = (SH / 'lockup.svg').read_text().strip().replace('fill="#1D1D1F"', 'fill="currentColor"')
    return s.replace('<svg ', '<svg aria-hidden="true" ', 1)


def dot(text):
    """A headline ending in the logo's round dot (Team H's .hd-dot)."""
    t = text[:-1] if text.endswith('.') else text
    return f'{E(t)}<span class="hd-dot">.</span>'


# ================================================================ shared copy: nav and footer
NAVC = {
    'nav.features': 'Features', 'nav.pricing': 'Pricing', 'nav.uses': 'Use cases', 'nav.guides': 'Guides', 'nav.blog': 'Blog',
    'nav.login': 'Log in', 'nav.start': 'Start free',
    'foot.tag': 'Made for people who make things.',
    'foot.fine': 'Names, sessions and numbers shown on this page are examples.',
}
FOOT_COLS = [  # the same columns and words as the homepage footer (Team H)
    ('Product', [('Features', 'features.html'), ('Pricing', 'pricing.html'), ('Use cases', 'use-cases.html'), ('Blog', 'blog.html')]),
    ('Guides', [('Publish a Claude artifact', 'publish-a-claude-artifact.html'), ('Test a Figma prototype', 'guides.html'), ('Host an HTML site', 'guides.html')]),
    ('Aero', [('Log in', '#'), ('Start free', '#'), ('Coming from Figmafolio', '#')]),
    ('Legal', [('Privacy', '#'), ('Terms', '#')]),
]
HOME = '../home/home.html'
MENU = [('features', 'nav.features', 'features.html'), ('pricing', 'nav.pricing', 'pricing.html'), ('uses', 'nav.uses', 'use-cases.html'),
        ('guides', 'nav.guides', 'guides.html'), ('blog', 'nav.blog', 'blog.html')]


def c(copy, key, tag='span', cls='', inner=None):
    k = f' class="{cls}"' if cls else ''
    return f'<{tag}{k} data-c="{key}">{E(copy[key]) if inner is None else inner}</{tag}>'


def nav(cur):
    items = ''.join(f'<a href="{href}"{" class=\"on\" aria-current=\"page\"" if k == cur else ""}>{c(NAVC, key)}</a>' for k, key, href in MENU)
    return f'''<header class="site-nav"><div class="site-wrap site-nav-in">
<a class="site-logo" href="{HOME}" aria-label="Aero home">{lockup()}</a>
<nav class="site-menu" id="site-menu">{items}<a class="site-menu-login" href="#">{c(NAVC, 'nav.login')}</a></nav>
<div class="site-nav-r"><a class="btn g3 sm site-login" href="#" data-glass-v3="secondary">{c(NAVC, 'nav.login')}</a>
<a class="btn g3 sm" href="#" data-glass-v3="primary" data-fill="rgba(29,29,31,.8)">{c(NAVC, 'nav.start')}</a>
<button class="site-burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="site-menu"><i></i><i></i></button></div></div></header>'''


def footer():
    cols = ''.join(f'<div><h4>{h}</h4><ul>' + ''.join(f'<li><a href="{u}">{E(t)}</a></li>' for t, u in xs) + '</ul></div>' for h, xs in FOOT_COLS)
    tag = NAVC['foot.tag']
    return f'''<footer class="site-foot"><div class="site-wrap">
<div class="site-foot-top"><div class="site-foot-brand">{lockup()}<p data-c="foot.tag">{dot(tag)}</p></div><div class="site-foot-cols">{cols}</div></div>
<div class="site-foot-fine"><span>© 2026 Aero</span>{c(NAVC, 'foot.fine')}</div></div></footer>'''


def gbtn(label, href='#', kind='primary', size='md', key=None, copy=None):
    """A button on a gradient: V3 glass. kind primary = translucent ink, secondary = clear."""
    a = 'data-glass-v3="primary" data-fill="rgba(29,29,31,.8)"' if kind == 'primary' else 'data-glass-v3="secondary"'
    t = c(copy, key) if key else E(label)
    return f'<a class="btn g3 {size}" href="{href}" {a}>{t}</a>'


def ibtn(label, href='#', kind='ink', size='md', key=None, copy=None):
    """A button on plain white: ink or outline, no glass."""
    t = c(copy, key) if key else E(label)
    return f'<a class="btn {size} {kind}" href="{href}">{t}</a>'


STEP_ICON = {'publish': 'up', 'test': 'link', 'review': 'chart', 'account': 'user'}
STEP_NAME = {'publish': 'Publish', 'test': 'Test', 'review': 'Review', 'account': 'Plans and account'}


def pill(step, label=None):
    cls = {'publish': 'pill pill-publish', 'test': 'pill pill-test', 'review': 'pill pill-review'}.get(step, 'pill')
    return f'<span class="{cls}">{ic(STEP_ICON.get(step, "check"))}{E(label or STEP_NAME[step])}</span>'


# ================================================================ real app screens (v3), for crops
def sessions_win():
    rows = ''.join(rv.s_row(s, hot=(s[1] == 'Maya')) for s in rv.SESS)
    head = '''<div class="srow2 hd"><span>#</span><span>Tester</span><span>Summary, in their words where we can</span><span>When</span><span>Length</span><span>Tasks</span>
<span class="tg issue">Issue</span><span class="tg conf">Confusion</span><span class="tg good">Works well</span><span></span></div>'''
    main = rv.testhead() + f'<div class="sesbody">{rv.fbar()}<div class="tbl stbl2">{head}{rows}</div></div>'
    return rv.window('aeroapp.ai/tests/pocket/sessions', rv.sidebar(), main)


def pocket_site():
    """The site's page in Aero for Pocket, published from a prompt (as the homepage does)."""
    real_thumb, real_window = mk.thumb, mk.window

    def thumb(kind, w, h, scale=None, cls='', sheet=False, top=None):
        if kind == 'checkout' and w == 700:
            return real_thumb('pocket', w, h, scale=.95, cls=cls, top='3%')
        return real_thumb(kind, w, h, scale, cls, sheet, top)

    def window(url, side, main, h=900, cls='', rail=False):
        main = (main.replace('checkout.zip · 17 files', 'From Claude · 9 files').replace('checkout.aeroapp.ai', 'pocket.aeroapp.ai')
                .replace('<b>Checkout</b>', '<b>Pocket</b>').replace('x-in">Checkout<', 'x-in">Pocket<').replace('--site:#1F8F5F', '--site:#3478F6'))
        return real_window(url.replace('checkout', 'pocket'), side, main, h, cls, rail)

    mk.thumb, mk.window = thumb, window
    try:
        return mk.site_page(just=True)
    finally:
        mk.thumb, mk.window = real_thumb, real_window


def mk_player_desk():
    """The replay of a Pocket session at desktop width: Pocket is a site, and site tests need a computer."""
    real = rv.pocket
    rv.pocket = lambda sheet=False, cls='': f'<div class="s-pkd"><div class="s-pkd-in">{mk.proto_bright()}</div></div>'
    try:
        return rv.mk_player()
    finally:
        rv.pocket = real


# Pocket is a site: every Pocket session is on a computer (Figma tests may be on a phone, voice only).
rv.SESS = [tuple(('Laptop' if i == 3 and v == 'Phone' else v) for i, v in enumerate(r)) for r in rv.SESS]
_WD = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')


def truth(h):
    """Small fixes to the v3 screens so they tell the truth: Aero records the tab, weekdays match 2026, no browser
    version numbers, and Pocket's sessions are on a computer."""
    import datetime
    h = re.sub(r'\b(Mon|Tue|Wed|Thu|Fri|Sat|Sun) (\d{1,2}) Oct\b', lambda m: f'{_WD[datetime.date(2026, 10, int(m[2])).weekday()]} {m[2]} Oct', h)
    h = re.sub(r'\b(Chrome|Firefox|Safari|Edge) \d{2,3}\b', r'\1', h)
    for a, b in (('Screen and voice', 'Tab and voice'), ('screen and voice', 'tab and voice'), ('Their screen', 'Their tab'),
                 ('Screen only, no audio', 'Tab only, no audio'), ('Laptop and phone', 'On a computer'),
                 ('I’ve tapped everything', 'I’ve clicked everything')):
        h = h.replace(a, b)
    return h


SCREENS = {
    'prompt': mk.prompt_page, 'claude': lambda: mk.claude_panel('done'), 'upload': mk.up_states, 'figma': mk.figma_ready, 'figstates': mk.figma_states,
    'site': mk.site_page, 'justpub': pocket_site, 'sites': mk.sites_list, 'tests': mk.tests_list, 'setup': mk.test_setup,
    'tstart': mk.tester_start, 'tperm': mk.tester_perm, 'ttask': lambda: mk.tester_task('home'),
    'mklink': mk.mk_link, 'mksite': mk.mk_site, 'mkev': mk.mk_ev,
    'sessions': sessions_win, 'watch': rv.s2_window, 'read': rv.s3_window, 'insights': rv.s5_window,
    'mkquote': rv.mk_quote, 'mkplayer': mk_player_desk, 'mkrow': rv.mk_row,
}
_cache = {}


def screen(k):
    if k not in _cache:
        _cache[k] = truth(SCREENS[k]())
    return _cache[k]


def crop(k, sel, pad=14, label='', cls='', maxs=1.3, w=1440, cw=0, ch=0, mcw=None):
    """A part of a real app screen. site.js finds `sel` (one or more selectors, their union) inside the 1440px window,
    adds `pad` native px around it and scales it to fit the frame (no larger than maxs). cw / ch keep only the first
    cw x ch native px of a wide or tall part (the cut edge fades out)."""
    al = f' role="img" aria-label="{html.escape(label)}"' if label else ' aria-hidden="true"'
    if mcw is None and k.startswith('mk'):
        mcw = 0  # marketing parts are big already; never cut them
    lim = (f' data-cw="{cw}"' if cw else '') + (f' data-ch="{ch}"' if ch else '') + (f' data-mcw="{mcw}"' if mcw is not None else '')
    return (f'<div class="s-crop {cls}" data-sel="{html.escape(sel)}" data-pad="{pad}" data-max="{maxs}"{lim}{al}>'
            f'<div class="s-crop-in" style="width:{w}px">{screen(k)}</div></div>')


# ================================================================ features
FEAT = {
    'title': 'Features: publish, test and review in one place · Aero',
    'desc': 'Every Aero feature, grouped by step: publish from one prompt, an HTML folder or a Figma link; test with one link and no software for testers; review transcripts, summaries and friction points across sessions.',
    'hero.eyebrow': 'Features',
    'hero.h1': 'Everything Aero does, in three steps.',
    'hero.lead': 'Publish what you made, send one link to test it, and review what people said. Here is every part of it, with the plan it comes on.',
    'hero.note': 'Every plan includes recordings of the tab and the tester’s voice.',
    'publish.h2': 'Publish.',
    'publish.sell': 'One prompt and it’s live. No hosting, no build step, no domain jargon. Bring it from Claude or ChatGPT, an HTML folder or a Figma link.',
    'test.h2': 'Test.',
    'test.sell': 'Send one link. Testers open it on their own computer: no software to install, no account, nothing for you to set up first.',
    'review.h2': 'Review.',
    'review.sell': 'No hours going through recordings. Each session comes back transcribed and summarised, and Insights puts every session together. It still reads well when you want the detail.',
    'account.h2': 'Plans and account.',
    'account.sell': 'Free to start, from $3 a month. No seats, no panels, no sales call.',
    'soon': 'Coming soon',
    'every': 'Every plan',
    'cta.h2': 'Try the whole loop on the free plan.',
    'cta.p': '3 test sessions with recordings included. Sites stay live for 7 days.',
    'cta.a': 'Start free', 'cta.b': 'See pricing',
    'fine': 'Pictures are the Aero app with example data. “Coming soon” marks work that is decided but not built yet.',
}

# At most 6 boxes per step (Duane, 25 Oct 2026). Each box groups several features; every feature is still named
# in its box's list. (title, line, [(item, plan tag ('' = every plan), soon)], crop(screen, selector, pad, opts))
GROUPS = {
    'publish': [
        ('Bring it however you made it', 'Three ways in, and each one goes live at its own address.', [
            ('One prompt from your chat: built it in Claude or ChatGPT? Copy one prompt into the same chat. It sends the files to Aero and the page updates when it’s live. Nothing to install.', '', False),
            ('Upload HTML: drop a single file, a folder or a zip.', '', False),
            ('Figma prototype link: Aero checks it, then publishes it with desktop and phone sizes. Changes in Figma show up on their own.', '', False),
        ], ('prompt', '.x-pbox, .x-key', 12, {'cw': 430})),
        ('Its page, and every version', 'After publishing you land on the site’s page: the address, a preview and every version.', [
            ('Publish again to the same address, from the same chat if you like', '', False),
            ('Every version kept. Roll back to any earlier one in one click.', '', False),
        ], ('site', '.x-vers', 10, {'cw': 440})),
        ('Your address', 'Free sites get an address made for them.', [
            ('Pick the name in yourname.aeroapp.ai', 'Basic and up', False),
            ('Custom domain, like work.yourname.com. Change or remove it yourself.', 'Solo and up', False),
        ], ('site', '.x-sps > .x-set:nth-child(4)', 12)),
        ('Who can see it', 'Sites are public by default: anyone with the address.', [
            ('Password protection, for client work and anything under NDA', 'Basic and up', False),
            ('Private sites: only people signed in to your account can open the address. Separate from a password.', '', True),
        ], ('site', '.x-sps > .x-set:nth-child(3)', 12)),
        ('Favicon, badge and visits', 'Small touches that make a site yours.', [
            ('Use your own favicon and drop the small “Made with Aero” link', 'Basic and up', False),
            ('Site analytics: how many people visited this week, per site', 'Solo and up', False),
        ], ('site', '.x-sps > .x-set:nth-child(5), .x-sps > .x-set:nth-child(6), .x-sps > .x-set:nth-child(7)', 12)),
        ('All your sites in one place', 'Each site as a preview with its address, version and visits.', [
            ('Search and filter by status', '', False),
            ('Duplicate or rename a site', '', False),
            ('Free sites stay live for 7 days', '', False),
        ], ('sites', '.x-filt, .x-site@0, .x-site@1', 10, {'cw': 600})),
    ],
    'test': [
        ('One link, nothing to install', 'Every test has a short link. Copy it into a message, an email or a group chat.', [
            ('Testers open it in their browser on their own computer', '', False),
            ('No app, no account, no webcam', '', False),
        ], ('setup', '.x-linkc', 14)),
        ('Test what you have', 'Whatever you published, you can test.', [
            ('A Figma prototype, an uploaded HTML site or one of your published sites', '', False),
            ('Set up a test from the same prompt you published with', '', False),
        ], ('tests', '.x-tline@0, .x-tline@1, .x-tline@2', 10, {'cw': 480})),
        ('Tab and voice', 'Aero records the tab with your prototype and the tester’s voice as they think aloud.', [
            ('Two quick permissions: the microphone and the tab. Nothing records until the tester presses Start.', '', False),
            ('A small sign shows it’s recording', '', False),
            ('Device, browser and time saved with each session', '', False),
        ], ('ttask', '.x-recchip', 16)),
        ('Tasks and messages', 'Add tasks, or leave them out and let people explore.', [
            ('A task panel over the prototype: one task at a time, and testers say when they’re done', '', False),
            ('Ask testers to rate how hard each task was', '', False),
            ('A task can tick itself off when the tester reaches the right page', '', True),
            ('Welcome and thank-you messages, in your own words', '', False),
            ('Testers can give an optional first name, shown next to their session', '', True),
        ], ('ttask', '.x-tk', 22)),
        ('Test settings', 'Run your own test first, and close it when you have enough.', [
            ('Preview as tester: free, shows as You and stays out of Insights', '', True),
            ('Stop taking sessions. The ones you have stay.', '', True),
            ('Its own domain and favicon, separate from the site’s', 'Solo and up', True),
        ], ('setup', '.x-tss > .x-set:nth-child(2), .x-tss > .x-set:nth-child(3)', 4, {'cw': 460})),
    ],
    'review': [
        ('Recording and transcript', 'Watch the tab and hear the voice, with the tasks and tagged moments on the timeline.', [
            ('Transcript about a minute after the session ends, with the time of every line', '', False),
            ('Download the transcript and video', '', False),
            ('Words light up as it plays. Click a line to jump to that moment.', '', True),
        ], ('mkplayer', '.mk-player', 6)),
        ('A summary of each session', 'What happened, in a few lines.', [
            ('Each task marked done or not, and how long it took', '', False),
        ], ('read', '.col .hq, .col .by, .col .stand', 14, {'cw': 600})),
        ('Friction points, in their words', 'Moments where people struggled, quoted as they said them.', [
            ('Tagged Issue or Confusion, with how serious it is', '', False),
            ('Positive moments tagged Works well', '', False),
        ], ('mkquote', '.mk-quote', 6)),
        ('Every session in a list', 'Who, on what device, how long, tasks done and what they ran into, counted.', [
            ('Delete a session you don’t need', '', False),
            ('Filters by status, tag, device, audio, tasks or date, and search what testers said', '', True),
        ], ('sessions', '.srow2:nth-child(-n+4)', 10, {'cw': 640})),
        ('Insights across sessions', 'One summary for the whole test: what most people hit and what worked.', [
            ('A short overall summary for each test', '', False),
            ('Recurring themes across sessions', '', False),
            ('Where testers disagreed: both sides, and who said what', '', False),
        ], ('insights', '.sumcard2', 12, {'cw': 520})),
        ('What to fix first', 'The issues to fix first, in order.', [
            ('How serious each one is', '', False),
            ('The quotes that back each one up', '', False),
        ], ('insights', '.iss@0', 12, {'cw': 600})),
    ],
    'account': [
        ('Free to start', '3 test sessions with recordings included. Sites stay live for 7 days.', [], None),
        ('Plans from $3 a month', 'Basic, Solo and Pro, each with a 7-day free trial. Monthly, cancel any time.', [], None),
        ('Sessions used, at a glance', 'The sidebar shows how many test sessions your plan has used.', [], None),
        ('Sign in with Google or email', 'Use either, and link both from your account settings.', [], None),
        ('Manage billing yourself', 'Change plan, update a card or cancel from your account. No call, no contract.', [], None),
        ('Everything Figmafolio did', 'Custom domains, password protection, versions and user testing, all in Aero.', [], None),
    ],
}


def ftags(plan, soon):
    t = f'<span class="s-tag soon">{E(FEAT["soon"])}</span>' if soon else ''
    return t + (f'<span class="s-tag">{E(plan)}</span>' if plan else '')


def feat_card(step, f, wide=False):
    t, line, items, cr = f
    pic = f'<div class="s-fpic">{crop(cr[0], cr[1], cr[2], label=t, **(cr[3] if len(cr) > 3 else {}))}</div>' if cr else ''
    lis = ''.join(f'<li class="{"is-soon" if soon else ""}">{ic("check")}<span>{E(x)}{" " + ftags(plan, soon) if plan or soon else ""}</span></li>'
                  for x, plan, soon in items)
    ul = f'<ul class="s-fl">{lis}</ul>' if lis else ''
    cls = 's-feat' + (' nopic' if not cr else '') + (' wide' if wide else '')
    return f'''<article class="{cls}">{pic}<div class="s-ftx"><h3>{E(t)}</h3><p>{E(line)}</p>{ul}</div></article>'''


def features_page():
    jump = ''.join(f'<a href="#{s}">{pill(s)}</a>' for s in ('publish', 'test', 'review', 'account'))
    groups = ''
    for s in ('publish', 'test', 'review', 'account'):
        n = len(GROUPS[s])
        cards = ''.join(feat_card(s, f, wide=(n % 3 == 2 and i == 0)) for i, f in enumerate(GROUPS[s]))
        groups += f'''<section class="s-group" id="{s}"><div class="site-wrap">
<div class="s-ghead"><div>{pill(s)}<h2 class="site-h2" data-c="{s}.h2">{dot(FEAT[s + ".h2"])}</h2></div>{c(FEAT, s + ".sell", "p", "site-lead")}</div>
<div class="s-fgrid">{cards}</div></div></section>'''
    body = f'''<section class="s-hero"><div class="site-wrap">
<p class="site-eyebrow" data-c="hero.eyebrow">{E(FEAT['hero.eyebrow'])}</p>
<h1 class="site-h1" data-c="hero.h1">{dot(FEAT['hero.h1'])}</h1>
<div class="s-hero-row">{c(FEAT, 'hero.lead', 'p', 'site-lead')}<div class="s-jump">{jump}</div></div>
<p class="s-note">{ic('mic')}{c(FEAT, 'hero.note')}</p></div></section>
{groups}
{closing(FEAT)}'''
    return page('features', FEAT, body)


def closing(C, href_b='pricing.html'):
    return f'''<section class="s-close-w"><div class="site-wrap"><div class="site-band w-hero s-close">
<div><h2 class="site-h2" data-c="cta.h2">{dot(C['cta.h2'])}</h2>{c(C, 'cta.p', 'p', 'site-lead')}</div>
<div class="s-ctas">{gbtn('', '#', 'primary', 'md', 'cta.a', C)}{gbtn('', href_b, 'secondary', 'md', 'cta.b', C)}</div></div>
{c(C, 'fine', 'p', 's-fine') if 'fine' in C else ''}</div></section>'''


# ================================================================ pricing
PRICE = {
    'title': 'Pricing: free to start, from $3 a month · Aero',
    'desc': 'Aero plans: Free, Basic $3, Solo $6 and Pro $19 a month. Recordings on every plan. 7-day free trial, no call, no contract. Compared with Maze, Lookback, Userbrain and Lyssna, per month.',
    'hero.eyebrow': 'Pricing',
    'hero.h1': 'Priced for one designer.',
    'hero.lead': 'Not for a research department. Free to start, then from $3 a month. Every plan includes recordings of the tab and the tester’s voice.',
    'hero.fine': ['7-day free trial on paid plans', 'Monthly, cancel any time', 'No call, no contract'],
    'plans': [
        ['Free', '$0', '', 'To try the whole loop.', ['3 test sessions', 'Recordings included', 'Sites stay live for 7 days'], 'Start free', ''],
        ['Basic', '$3', '/month', 'For a portfolio or a few tests.', ['5 test sessions', 'Your own aeroapp.ai address', 'Password protection', 'Custom favicon, no Aero badge'], 'Try Basic free', '7-day free trial'],
        ['Solo', '$6', '/month', 'For your own domain.', ['10 test sessions', 'Everything in Basic', 'Custom domain', 'Site analytics'], 'Try Solo free', '7-day free trial'],
        ['Pro', '$19', '/month', 'For regular testing.', ['20 test sessions', 'Everything in Solo', 'Priority support'], 'Try Pro free', '7-day free trial'],
    ],
    'plans.foot': 'Prices in USD. Regional prices are shown at checkout. Test sessions are a total on your plan, not a monthly allowance.',
    'tbl.h2': 'Every plan, side by side.',
    'tbl.rows': [
        ['Test sessions', '3', '5', '10', '20'],
        ['Tab and voice recording', 'y', 'y', 'y', 'y'],
        ['Testers need no account or software', 'y', 'y', 'y', 'y'],
        ['Publish from a prompt, HTML or Figma', 'y', 'y', 'y', 'y'],
        ['Sites stay live', '7 days', 'y', 'y', 'y'],
        ['Your own aeroapp.ai address', '', 'y', 'y', 'y'],
        ['Password protection', '', 'y', 'y', 'y'],
        ['Custom favicon, no Aero badge', '', 'y', 'y', 'y'],
        ['Custom domain', '', '', 'y', 'y'],
        ['Site analytics', '', '', 'y', 'y'],
        ['Priority support', '', '', '', 'y'],
        ['7-day free trial', '', 'y', 'y', 'y'],
    ],
    'cmp.eyebrow': 'Compared',
    'cmp.h2': 'What testing with your own people costs elsewhere, per month.',
    'cmp.lead': 'Each tool’s cheapest plan with recordings that tests a prototype with people you invite. Every price is per month; yearly-only plans are shown as their monthly equivalent.',
    'cmp.cols': ['Aero Free', 'Aero Basic', 'Maze Free', 'Lookback Freelance', 'Userbrain Starter', 'Lyssna Growth'],
    'cmp.rows': [
        ['Price per month', '$0', '$3', '$0', '$25²', '$49', '$199³'],
        ['Billing', 'Free plan', 'Monthly, cancel any time', 'Free plan', 'Yearly only, $299 a year', 'Monthly', 'Monthly, or $166 a month billed yearly'],
        ['Sessions with your own testers', '3¹', '5¹', '1 study a month', '10 a year', '3 a month', '5 in-depth studies a month'],
        ['Tab and voice recording', 'Yes', 'Yes', 'No', 'Yes', 'Yes', 'Yes'],
        ['Hosts your prototype', 'Yes, live for 7 days', 'Yes, at your own aeroapp.ai address', 'No', 'No', 'No', 'No'],
        ['Testers install nothing', 'Yes, in their browser⁵', 'Yes, in their browser⁵', 'Not checked', 'iPhone needs an app; desktop not checked', 'Needs a Chrome extension or app', 'Desktop yes; phone recording uses an app'],
    ],
    'cmp.notes': [
        '¹ Aero’s sessions are a total on your plan, not a monthly allowance. The others reset each month or year, so the counts aren’t a straight comparison.',
        '² Lookback sells yearly plans only: $299 a year, about $25 a month.',
        '³ $199 billed monthly; $166 a month when billed yearly. Lyssna Growth also includes unlimited unmoderated responses.',
        '⁵ Figma prototype tests also work on a phone, voice only; site and HTML tests need a computer.',
        'Maze Free: 1 study a month and 5 seats; recordings (Clips) and interview transcription are on Enterprise only, which has no public price. Dovetail is Free or Enterprise; UserTesting publishes no prices.',
        'Prices in USD from each company’s own pricing page and help centre, checked 24 Oct 2026. “Not checked” means we couldn’t confirm it, so we don’t claim it either way.',
    ],
    'cmp.sources': [['Maze pricing', 'https://maze.co/pricing/'], ['Lookback pricing', 'https://www.lookback.com/pricing'], ['Userbrain pricing', 'https://www.userbrain.com/en/pricing'],
                    ['Lyssna pricing', 'https://www.lyssna.com/pricing/'], ['Lyssna pricing help', 'https://help.lyssna.com/en/articles/4953377-lyssna-pricing'],
                    ['Lookback iOS help', 'https://help.lookback.io/en/articles/3087247-how-do-i-join-an-ios-live-test'], ['Userbrain own testers help', 'https://help.userbrain.com/help/how-can-i-test-with-my-own-users'],
                    ['Lyssna recordings help', 'https://help.lyssna.com/en/articles/9398996-recordings'], ['UserTesting plans', 'https://www.usertesting.com/plans']],
    'host.h2': 'And to put it online.',
    'host.lead': 'Hosting tools stop at the link. Here is where custom domains and passwords start on each.',
    'host.cols': ['', 'Free plan', 'Custom domain from', 'Password from', 'Testing with people'],
    'host.rows': [
        ['Aero', 'Yes, sites live 7 days', 'Solo, $6 a month', 'Basic, $3 a month', 'Included'],
        ['Netlify', 'Yes', 'Free', 'Pro, $20 a month', 'No'],
        ['Vercel', 'Hobby, non-commercial use only', 'Free', 'Pro, $20 a month plus $20 a project', 'No'],
        ['Framer', 'Yes, on a Framer domain', 'Basic, $10 a month billed yearly', 'Not confirmed', 'No'],
        ['Figma Sites', 'Starter, figma.site address', 'Professional full seat, $16⁴', 'Not confirmed', 'No'],
        ['Claude artifacts', 'Share a link on any plan', 'Not possible, always on claude.ai', 'No; Pro and Max can invite by email', 'No'],
    ],
    'host.notes': ['⁴ Figma’s page did not confirm whether $16 is the monthly or yearly-billed price.', '“Not confirmed”: the feature is listed, but the pricing page doesn’t make clear which plan includes it.'],
    'host.sources': [['Netlify pricing', 'https://www.netlify.com/pricing/'], ['Netlify password protection', 'https://www.netlify.com/knowledge-base/how-to-password-protect-a-netlify-site-or-deploy-previews/'], ['Vercel pricing', 'https://vercel.com/pricing'],
                     ['Framer pricing', 'https://www.framer.com/pricing'], ['Figma pricing', 'https://www.figma.com/pricing/'], ['Figma custom domains', 'https://help.figma.com/hc/en-us/articles/31414274019863'], ['Claude artifact sharing', 'https://support.claude.com/en/articles/9547008-publish-and-share-artifacts']],
    'src': 'Sources',
    'faq.eyebrow': 'Billing',
    'faq.h2': 'Questions about paying.',
    'faq': [
        ['Is there a free plan?', 'Yes. Free has 3 test sessions with recordings included, and your sites stay live for 7 days.'],
        ['How does the free trial work?', 'Basic, Solo and Pro each start with a 7-day free trial. You can cancel before it ends.'],
        ['Can I cancel any time?', 'Yes. Plans are monthly, with no contract. Cancel from your account in a couple of clicks; there is no call.'],
        ['What counts as a test session?', 'One person taking one of your tests. Today the number on your plan is a total of sessions stored, not a monthly allowance.'],
        ['Why do I see a different price at checkout?', 'Aero has regional prices. The site shows USD; checkout shows the price for where you are.'],
        ['What happens to a free site after 7 days?', 'It goes offline. It keeps its address and versions, and a paid plan keeps sites live.'],
        ['Do my testers pay or sign up?', 'No. They open your link and start. They never need an account.'],
        ['Is there a team or yearly plan?', 'Not today. Aero is priced for one person, paid monthly. There are no seats, panels or sales calls.'],
        ['What does priority support mean?', 'On Pro, your questions go to the front of the queue.'],
    ],
    'cta.h2': 'Start free. Upgrade when you need your own address.',
    'cta.p': 'Free to start, from $3 a month. No call, no contract.',
    'cta.a': 'Start free', 'cta.b': 'See every feature',
}


def yes():
    return f'<span class="s-yes" title="Included">{ic("check")}<span class="sr-only">Included</span></span>'


def no():
    return '<span class="s-no" aria-label="Not included">–</span>'


def cell(v):
    return yes() if v == 'y' else (no() if v == '' else E(v))


def pricing_page():
    C = PRICE
    plans = ''
    for n, p, u, who, f, cta, tr in C['plans']:
        li = ''.join(f'<li>{ic("check")}{E(x)}</li>' for x in f)
        mid = n == 'Solo'
        b = gbtn(cta, '#', 'primary', 'md') if mid else ibtn(cta, '#', 'line', 'md')
        plans += f'''<div class="s-plan{" mid w-publish" if mid else ""}"><div class="pn"><b>{n}</b><span class="site-eyebrow">{E(tr)}</span></div>
<div class="pr">{p}<small>{u}</small></div><p class="who">{E(who)}</p><ul>{li}</ul>{b}</div>'''
    fine = ''.join(f'<span>{ic("check")}{E(t)}</span>' for t in C['hero.fine'])
    head = '<tr><th></th>' + ''.join(f'<th>{n}<small>{p}{u}</small></th>' for n, p, u, *_ in C['plans']) + '</tr>'
    rows = ''.join('<tr><th scope="row">' + E(r[0]) + '</th>' + ''.join(f'<td>{cell(v)}</td>' for v in r[1:]) + '</tr>' for r in C['tbl.rows'])
    ch = '<tr><th></th>' + ''.join(f'<th{" class=us" if i < 2 else ""}>{E(n)}</th>' for i, n in enumerate(C['cmp.cols'])) + '</tr>'
    cr = ''.join('<tr><th scope="row">' + E(r[0]) + '</th>' + ''.join(f'<td{" class=us" if i < 2 else ""}>{E(v)}</td>' for i, v in enumerate(r[1:])) + '</tr>' for r in C['cmp.rows'])
    hh = '<tr>' + ''.join(f'<th>{E(n)}</th>' for n in C['host.cols']) + '</tr>'
    hr = ''.join(f'<tr{" class=us" if r[0] == "Aero" else ""}><th scope="row">{E(r[0])}</th>' + ''.join(f'<td>{E(v)}</td>' for v in r[1:]) + '</tr>' for r in C['host.rows'])
    srcs = lambda k: '<p class="s-src"><b>' + E(C['src']) + '</b> ' + ' · '.join(f'<a href="{u}" rel="nofollow noopener">{E(t)}</a>' for t, u in C[k]) + '</p>'
    notes = lambda k: '<ul class="s-notes">' + ''.join(f'<li>{E(n)}</li>' for n in C[k]) + '</ul>'
    faq = faq_block(C['faq'])
    body = f'''<section class="s-hero s-hero-c"><div class="site-wrap">
<p class="site-eyebrow">{E(C['hero.eyebrow'])}</p><h1 class="site-h1" data-c="hero.h1">{dot(C['hero.h1'])}</h1>
{c(C, 'hero.lead', 'p', 'site-lead s-lead-c')}<p class="s-fine-row">{fine}</p></div></section>
<section><div class="site-wrap"><div class="s-plans">{plans}</div>{c(C, 'plans.foot', 'p', 's-fine')}</div></section>
<section class="s-sec"><div class="site-wrap"><h2 class="site-h2 s-h2" data-c="tbl.h2">{dot(C['tbl.h2'])}</h2>
<div class="s-tscroll"><table class="s-tbl s-matrix">{head}{rows}</table></div></div></section>
<section class="s-sec" id="compare"><div class="site-wrap"><div class="site-band w-test s-cmp">
<p class="site-eyebrow">{E(C['cmp.eyebrow'])}</p><h2 class="site-h2" data-c="cmp.h2">{dot(C['cmp.h2'])}</h2>{c(C, 'cmp.lead', 'p', 'site-lead')}
<div class="s-tscroll"><table class="s-tbl s-ctbl">{ch}{cr}</table></div>{notes('cmp.notes')}{srcs('cmp.sources')}</div>
<div class="s-host"><h3 class="site-h3" data-c="host.h2">{E(C['host.h2'])}</h3>{c(C, 'host.lead', 'p', 'site-body')}
<div class="s-tscroll"><table class="s-tbl s-htbl">{hh}{hr}</table></div>{notes('host.notes')}{srcs('host.sources')}</div></div></section>
<section class="s-sec" id="faq"><div class="site-wrap s-faq"><div><p class="site-eyebrow">{E(C['faq.eyebrow'])}</p><h2 class="site-h2" data-c="faq.h2">{dot(C['faq.h2'])}</h2></div>{faq}</div></section>
{closing(C, 'features.html')}'''
    ld = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in C['faq']]}
    return page('pricing', C, body, ld=[ld])


def faq_block(items, cols=True):
    det = ''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in items)
    return f'<div class="s-faq-list{" two" if cols else ""}">{det}</div>'


# ================================================================ use cases
USES = {
    'title': 'Use cases: who uses Aero and for what · Aero',
    'desc': 'How designers, founders, students, freelancers and researchers use Aero to put a prototype or site online and test it with their own people.',
    'hero.eyebrow': 'Use cases',
    'hero.h1': 'For people who make things.',
    'hero.lead': 'Six people, six jobs. Each one starts with something made and ends with a link someone else can open. Names are examples.',
    'more': 'Read the use case',
    'steps': 'Uses',
    'pain': 'The problem',
    'fix': 'With Aero',
    'guide.eyebrow': 'Step by step',
    'guide.h2': 'Guides for one job each.',
    'guide.p': 'Short pages that do one thing, start to finish. The first is live; more are on the way.',
    'cta.h2': 'Bring what you made.',
    'cta.p': 'Free to start, from $3 a month. No call, no contract.',
    'cta.a': 'Start free', 'cta.b': 'See pricing',
}
USE_CASES = [
    # slug, who, title, pain, fix, scenario, steps, picture
    ('figma-prototype-test', 'UX designer with a Figma prototype', 'Test a Figma prototype before the review',
     'Testing tools cost $49 to $199 a month or start with a sales call. Figma’s share link shows the prototype but not what people did with it.',
     'Paste the Figma link, send the test link, and read each session’s summary and friction points.',
     'Priya pastes her checkout prototype at 4pm, sends the link to five colleagues, and reads three summaries before tomorrow’s review.',
     ['publish', 'test', 'review'], ('insights', '.sumcard2', 12, {'cw': 560}), 'w-review'),
    ('idea-overnight', 'PM or founder with an idea', 'An idea at night, answers by morning',
     'A Claude-built page and a hunch. No researcher, no budget and no time to set up a study.',
     'One prompt publishes it, one link tests it, and the summaries are waiting in the morning.',
     'Tom publishes his pricing page from Claude, sends the link to three customers at 9pm, and hears where they hesitated over coffee.',
     ['publish', 'test', 'review'], ('prompt', '.x-pbox, .x-key', 12, {'cw': 560}), 'w-publish'),
    ('claude-artifact-live', 'Someone with a Claude artifact or Lovable build', 'Give an AI-built app a real address',
     'The artifact lives on claude.ai, and moving it somewhere with a proper address is fiddly.',
     'It gets a real address and a place to keep every version, with your own domain on Solo.',
     'Sam turns a weekend Claude artifact into a live tool at sam.aeroapp.ai and shares it in a group chat.',
     ['publish'], ('mksite', '.mk-site', 6), 'w-publish'),
    ('portfolio-folder', 'Student or job seeker', 'A portfolio from a folder of work',
     'Case studies in a folder, no hosting know-how and little money. Domain options on student plans are confusing.',
     'Upload the folder, or ask Claude to build it from the folder in one prompt. It’s live at your own address from $3. Then test it with a friend.',
     'Lena uploads her case-study folder, asks two classmates to try it, and learns nobody found her contact link.',
     ['publish', 'test'], ('sites', '.x-dropt', 12), 'w-publish'),
    ('client-site-password', 'Freelancer sending a client a site', 'A client preview behind a password',
     'A private preview link and a tidy address, without setting up Netlify or Vercel for one client.',
     'Password protection from $3, a custom domain from $6, and no Aero badge.',
     'Marco sends his client a password-protected preview, then asks three of the client’s staff to try the booking flow.',
     ['publish', 'test'], ('site', '.x-sps > .x-set:nth-child(3)', 12), 'w-test'),
    ('think-aloud-sessions', 'UX researcher', 'Five think-aloud sessions, no panel',
     'Panels and per-seat pricing are too much for five sessions with people you already know.',
     'Bring your own testers. The tab and the voice are recorded, and each session is transcribed with themes across all of them.',
     'Aisha runs five think-aloud sessions with existing customers on Basic instead of paying for a $199 plan for one month.',
     ['test', 'review'], ('mkquote', '.mk-quote', 6), 'w-review'),
]


def use_cases_page():
    C = USES
    items = ''
    for i, (slug, who, title, pain, fix, scen, steps, cr, wash) in enumerate(USE_CASES):
        pills = ''.join(pill(s) for s in steps)
        items += f'''<article class="s-use" id="{slug}"><div class="s-use-tx">
<p class="site-eyebrow">{E(who)}</p><h2 class="site-h3 s-use-h">{E(title)}</h2>
<dl><dt>{E(C['pain'])}</dt><dd>{E(pain)}</dd><dt>{E(C['fix'])}</dt><dd>{E(fix)}</dd></dl>
<p class="s-scen"><span class="site-ex">Example</span>{E(scen)}</p>
<div class="s-use-f"><div class="s-pills">{pills}</div></div></div>
<div class="s-use-pic {wash}">{crop(cr[0], cr[1], cr[2], label=title, **(cr[3] if len(cr) > 3 else {}))}</div></article>'''
    guides = guide_cards(4)
    body = f'''<section class="s-hero"><div class="site-wrap"><p class="site-eyebrow">{E(C['hero.eyebrow'])}</p>
<h1 class="site-h1" data-c="hero.h1">{dot(C['hero.h1'])}</h1>{c(C, 'hero.lead', 'p', 'site-lead s-lead-w')}</div></section>
<section><div class="site-wrap s-uses">{items}</div></section>
<section class="s-sec"><div class="site-wrap"><p class="site-eyebrow">{E(C['guide.eyebrow'])}</p><h2 class="site-h2 s-h2" data-c="guide.h2">{dot(C['guide.h2'])}</h2>
{c(C, 'guide.p', 'p', 'site-lead s-lead-w')}{guides}</div></section>
{closing(C)}'''
    return page('uses', C, body)


# ================================================================ guides
GUIDES = [  # step, title, slug or '' (planned)
    ('publish', 'Publish a Claude artifact', 'publish-a-claude-artifact.html'),
    ('publish', 'Publish a Lovable app', ''), ('publish', 'Publish a Figma prototype', ''), ('publish', 'Host an HTML folder', ''),
    ('publish', 'Put a site on your own domain', ''), ('publish', 'Password-protect a site', ''),
    ('test', 'Test a Figma prototype', ''), ('test', 'Test a Claude artifact', ''), ('test', 'Run a think-aloud test with friends', ''),
    ('test', 'Write tasks testers understand', ''),
    ('review', 'Read a session in five minutes', ''), ('review', 'Turn five sessions into a fix list', ''),
]
GUIDE = {
    'title': 'Guides: publish and test, one job at a time · Aero',
    'desc': 'Step-by-step guides for Aero: publish a Claude artifact, a Lovable app, a Figma prototype or an HTML folder, then test it with your own people.',
    'hero.eyebrow': 'Guides',
    'hero.h1': 'One job, start to finish.',
    'hero.lead': 'Short guides for publishing, testing and reviewing. Each one does one thing and takes a few minutes to read.',
    'soon': 'Coming soon',
    'cta.h2': 'Try it on the free plan.',
    'cta.p': '3 test sessions with recordings included.',
    'cta.a': 'Start free', 'cta.b': 'See pricing',
}


def guide_cards(n=None, step=None, pills=True):
    gs = [g for g in GUIDES if step is None or g[0] == step]
    if n:
        gs = gs[:n]
    out = ''
    for s, t, u in gs:
        if u:
            out += f'<a class="s-gcard{"" if pills else " np"}" href="{u}">{pill(s) if pills else ""}<b>{E(t)}</b><span class="s-garr">{ic("arrow")}</span></a>'
        else:
            out += f'<div class="s-gcard off{"" if pills else " np"}">{pill(s) if pills else ""}<b>{E(t)}</b><span class="s-tag soon">{E(GUIDE["soon"])}</span></div>'
    return f'<div class="s-gcards">{out}</div>'


def guides_page():
    C = GUIDE
    secs = ''.join(f'<div class="s-gsec"><h2 class="site-h3">{pill(s)}</h2>{guide_cards(step=s, pills=False)}</div>' for s in ('publish', 'test', 'review'))
    body = f'''<section class="s-hero"><div class="site-wrap"><p class="site-eyebrow">{E(C['hero.eyebrow'])}</p>
<h1 class="site-h1" data-c="hero.h1">{dot(C['hero.h1'])}</h1>{c(C, 'hero.lead', 'p', 'site-lead s-lead-w')}</div></section>
<section><div class="site-wrap">{secs}</div></section>{closing(C)}'''
    return page('guides', C, body)


# ================================================================ SEO task page template: Publish a Claude artifact
TASK = {
    'title': 'Publish a Claude artifact to its own address · Aero',
    'desc': 'How to publish a Claude artifact as a real website at your own address, in one prompt or by uploading its HTML. Then test it with people you choose.',
    'crumb.a': 'Guides', 'crumb.b': 'Publish a Claude artifact',
    'h1': 'Publish a Claude artifact.',
    'answer': 'Copy one prompt from Aero into the Claude chat where you made the artifact. Claude sends the files to Aero and it goes live at an address like yourname.aeroapp.ai. Or download the artifact as HTML and drop it into Aero.',
    'meta': ['About 2 minutes', 'Free plan works', 'Nothing to install'],
    'need.h': 'What you need',
    'need': ['The Claude chat where you built the artifact', 'An Aero account (free)', 'A name for the site, like pocket'],
    'steps.h': 'Steps',
    'steps': [
        ['Start a new site from a prompt', 'In Aero, go to Sites, New site, and pick Prompt. Give the site a name.', ('prompt', '.x-seg, .mhead .crumb', 12)],
        ['Copy the prompt', 'Aero shows one prompt with your key in it. Press Copy prompt. The key only lets this prompt publish sites in your account.', ('prompt', '.x-pbox, .x-key', 12)],
        ['Paste it into your Claude chat', 'Go back to the chat where you made the artifact and paste it. Claude sends the files to Aero and replies with the address.', ('claude', '.x-outside', 8, {'cw': 600})],
        ['Open its page in Aero', 'Aero updates by itself when the site is live and opens its page: the address, a preview and its versions.', ('justpub', '.x-justpub, .x-stage, .x-addr', 12, {'cw': 560})],
    ],
    'alt.h': 'Prefer not to use a prompt?',
    'alt.p': 'Download the artifact from Claude as an HTML file, then drop it on New site, Upload. It goes live at its own address the same way.',
    'next.h': 'Then test it.',
    'next.p': 'Start a new test and pick this site. You get a test link to send to anyone: they open it on their own computer, and you get the recording, transcript and summary back.',
    'next.a': 'How testing works',
    'faq.h': 'Questions.',
    'faq': [
        ['Does my artifact stay on claude.ai?', 'Yes. Aero publishes a copy at its own address. Your chat and the artifact in Claude don’t change.'],
        ['Can I use my own domain?', 'Yes, on Solo and up. Every site also has an aeroapp.ai address, and on Basic and up you choose its name.'],
        ['How do I update it?', 'Ask Claude for the change in the same chat, then use the prompt again. Aero keeps every version, so you can roll back.'],
        ['Can I keep it private?', 'Add a password on Basic and up, so only people you give it to can open it.'],
        ['Does it work with ChatGPT too?', 'Yes. The same prompt works in the ChatGPT chat where you built it.'],
        ['How long does a free site stay live?', '7 days. Paid plans keep it live; they start at $3 a month with a 7-day free trial.'],
    ],
    'rel.h': 'Related guides',
    'cta.h2': 'Publish your artifact.',
    'cta.p': 'Free to start. Live at its own address, ready to test.',
    'cta.a': 'Start free', 'cta.b': 'See pricing',
}


def task_page():
    C = TASK
    meta = ''.join(f'<span>{ic("check")}{E(m)}</span>' for m in C['meta'])
    need = ''.join(f'<li>{ic("check")}{E(n)}</li>' for n in C['need'])
    steps = ''
    for i, (t, p, cr) in enumerate(C['steps']):
        steps += f'''<li class="s-step"><div class="s-step-tx"><span class="s-step-n">{i + 1}</span><div><h3 class="site-h3">{E(t)}</h3><p class="site-body">{E(p)}</p></div></div>
<div class="s-step-pic w-publish">{crop(cr[0], cr[1], cr[2], label=t, **(cr[3] if len(cr) > 3 else {}))}</div></li>'''
    rel_items = [g for g in GUIDES if g[1] != 'Publish a Claude artifact'][:4]
    relh = ''.join(f'<div class="s-gcard off">{pill(s)}<b>{E(t)}</b><span class="s-tag soon">Coming soon</span></div>' for s, t, u in rel_items)
    body = f'''<section class="s-hero s-task-hero"><div class="site-wrap s-narrow">
<nav class="s-crumb" aria-label="Breadcrumb"><a href="guides.html">{E(C['crumb.a'])}</a>{ic('right')}<span aria-current="page">{E(C['crumb.b'])}</span></nav>
{pill('publish')}<h1 class="site-h1 s-h1-task" data-c="h1">{dot(C['h1'])}</h1>
<p class="site-lead s-answer" data-c="answer">{E(C['answer'])}</p><p class="s-fine-row">{meta}</p></div></section>
<section><div class="site-wrap s-narrow"><div class="s-need"><h2 class="site-h3">{E(C['need.h'])}</h2><ul>{need}</ul></div>
<h2 class="site-h2 s-h2">{E(C['steps.h'])}</h2><ol class="s-steps">{steps}</ol>
<div class="s-alt"><h3 class="site-h3">{E(C['alt.h'])}</h3>{c(C, 'alt.p', 'p', 'site-body')}</div>
<div class="site-band w-test s-next"><div>{pill('test')}<h2 class="site-h2" data-c="next.h">{dot(C['next.h'])}</h2>{c(C, 'next.p', 'p', 'site-body')}</div>
<div>{gbtn(C['next.a'], 'features.html#test', 'secondary', 'md')}</div></div>
<div class="s-tfaq"><h2 class="site-h2 s-h2">{dot(C['faq.h'])}</h2>{faq_block(C['faq'], cols=False)}</div>
<div class="s-rel"><h2 class="site-h3">{E(C['rel.h'])}</h2><div class="s-gcards">{relh}</div></div></div></section>
{closing(C)}'''
    howto = {'@context': 'https://schema.org', '@type': 'HowTo', 'name': 'Publish a Claude artifact', 'description': C['answer'], 'totalTime': 'PT2M',
             'step': [{'@type': 'HowToStep', 'position': i + 1, 'name': t, 'text': p} for i, (t, p, _) in enumerate(C['steps'])]}
    fq = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in C['faq']]}
    bc = {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'Guides', 'item': 'https://aeroapp.ai/guides'},
                                                                                         {'@type': 'ListItem', 'position': 2, 'name': 'Publish a Claude artifact'}]}
    return page('guides', C, body, ld=[howto, fq, bc], canonical='https://aeroapp.ai/guides/publish-a-claude-artifact')


# ================================================================ blog
BLOG = {
    'title': 'Blog: what’s new in Aero',
    'desc': 'Dated notes on what changed in Aero: publishing, testing and reviewing.',
    'hero.eyebrow': 'Blog',
    'hero.h1': 'What’s new.',
    'hero.lead': 'What changed in Aero, when it changed, in plain words.',
    'all': 'All', 'read': 'Read',
    'back': 'All posts', 'prev': 'Older', 'next': 'Newer',
    'cta.h2': 'Try what’s new.',
    'cta.p': 'Free to start, from $3 a month.',
    'cta.a': 'Start free', 'cta.b': 'See pricing',
}
# date (from the figmaApp git log), step, slug, title, lead, body paragraphs, what changed, picture, feature link
POSTS = [
    ('2026-10-21', 'test', 'steadier-figma-tests', 'Steadier Figma tests and summaries',
     'Figma prototype tests are more reliable for testers, and each session is summarised once, with a backup if the first try fails.',
     ['Some testers saw a blank prototype, or the prototype reloaded partway through a session. Both are fixed, and a session can no longer be saved twice.',
      'Summaries now run on a new provider with a backup lined up. If the first one is busy, the second takes over, so a session doesn’t sit there without a summary.'],
     ['Figma prototypes load reliably for testers', 'No more reloads partway through a session', 'One transcript and one summary per session', 'A backup for summaries'],
     ('mkplayer', '.mk-player', 6), 'features.html#test'),
    ('2026-09-21', 'publish', 'change-custom-domain', 'Change or remove your custom domain yourself',
     'You can now switch a site to a different custom domain, or remove it, without contacting support.',
     ['Before, moving a domain could get stuck halfway. Now Aero tells you what went wrong in plain words, and you can remove the domain and start again from the site’s settings.'],
     ['Switch a site to a new domain', 'Remove a domain in one step', 'Clear messages when a domain can’t be connected'],
     ('site', '.x-sps > .x-set:nth-child(4)', 12), 'features.html#publish'),
    ('2026-07-16', 'publish', 'figma-sites-custom-domains', 'Custom domains for Figma sites',
     'Sites made from a Figma prototype now get the same settings as HTML sites, including your own domain.',
     ['A Figma site now has the same tabs as any other site: overview, versions, domain, analytics and settings. On Solo and up, you can put it on your own domain.'],
     ['Custom domains on Figma sites', 'The same settings for every kind of site'],
     ('figma', '.x-fready', 16), 'features.html#publish'),
    ('2026-07-02', 'account', 'sign-in-with-google', 'Sign in with Google',
     'You can sign in to Aero with your Google account, and link it to an existing email and password.',
     ['Use whichever you prefer. In your account settings you can link Google and a password to the same account, or unlink one, so you never end up with two accounts by mistake.'],
     ['Sign in or sign up with Google', 'Link or unlink Google and a password', 'A clearer page for resetting your password'],
     None, 'features.html#account'),
    ('2026-06-23', 'test', 'test-from-a-prompt', 'Set up a test from the same prompt',
     'The prompt that publishes your site can now set up a test on it too.',
     ['Ask for a test in the same chat where you published. Aero makes the test with its own link, ready to send. You can add tasks and messages afterwards in Aero.'],
     ['Create a test from your chat', 'The test link comes back in the reply'],
     ('setup', '.x-linkc', 14), 'features.html#test'),
    ('2026-06-16', 'test', 'tasks-are-optional', 'Tasks are optional',
     'A test no longer needs tasks. Leave them out and testers explore freely.',
     ['With no tasks, the review sums up the whole session instead of each task.'],
     ['Tests without tasks', 'The review sums up the whole session'],
     ('setup', '.x-tsm > .x-set:nth-child(3)', 12), 'features.html#test'),
    ('2026-06-12', 'publish', 'publish-from-claude', 'Publish from Claude or ChatGPT with one prompt',
     'Built something in Claude or ChatGPT? Aero now gives you one prompt to publish it from the same chat.',
     ['Pick Prompt under New site, copy the prompt, and paste it into the chat where you built it. It sends the files to Aero with your key, and the page in Aero updates when the site is live. Nothing to install or connect.',
      'New site now offers three ways in: a prompt, an HTML upload or a Figma link. And what used to say Deploy now says Publish.'],
     ['One prompt to publish from your chat', 'Three ways to start a site', 'Each version shows where it came from'],
     ('prompt', '.x-pbox, .x-key', 12), 'features.html#publish'),
    ('2026-06-11', 'test', 'test-html-sites', 'Test an HTML site, with tasks',
     'You can now run a test on any HTML site you’ve published, not only on Figma prototypes.',
     ['Testers open the test link and see your site with a small task panel on top. Aero records the tab and their voice, and the device and browser are saved with the session.'],
     ['Tests on HTML sites', 'A task panel over the site', 'Device and browser saved with each session'],
     ('ttask', '.x-tk', 22), 'features.html#test'),
    ('2026-06-11', 'publish', 'site-settings', 'Passwords, favicons and visits for your sites',
     'Every site now has a settings page: its name, password protection, favicon and visits.',
     ['Password protection and your own favicon come with Basic. Visits per site, and your own domain, come with Solo. Passwords are checked by Aero, never in the browser, and never stored as plain text.'],
     ['Password protection (Basic and up)', 'Custom favicon (Basic and up)', 'Site analytics (Solo and up)', 'Rename the site’s address'],
     ('site', '.x-sps > .x-set:nth-child(3)', 12), 'features.html#publish'),
    ('2026-06-07', 'publish', 'html-hosting', 'Drop an HTML folder and it’s live',
     'Aero now hosts HTML sites: a single file, a folder or a zip, live at its own aeroapp.ai address.',
     ['Drop the files on New site. Aero gives the site a two-word address and keeps every upload as a version, so you can roll back.'],
     ['Upload a file, folder or zip', 'An address made for you', 'Every version kept'],
     ('sites', '.x-dropt', 12), 'features.html#publish'),
]
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']


def fdate(d):
    y, m, dd = d.split('-')
    return f'{int(dd)} {MONTHS[int(m) - 1]} {y}'


def blog_page():
    C = BLOG
    rows, month = '', ''
    for d, s, slug, t, lead, *_ in POSTS:
        mo = fdate(d).split(' ', 1)[1]
        if mo != month:
            rows += f'<h2 class="s-month">{mo}</h2>'
            month = mo
        rows += f'''<a class="s-post" href="blog-{slug}.html"><time datetime="{d}">{fdate(d)}</time><div><div class="s-post-h">{pill(s)}<h3>{E(t)}</h3></div><p>{E(lead)}</p></div><span class="s-garr">{ic('arrow')}</span></a>'''
    body = f'''<section class="s-hero"><div class="site-wrap s-narrow"><p class="site-eyebrow">{E(C['hero.eyebrow'])}</p>
<h1 class="site-h1" data-c="hero.h1">{dot(C['hero.h1'])}</h1>{c(C, 'hero.lead', 'p', 'site-lead')}</div></section>
<section><div class="site-wrap s-narrow"><div class="s-posts">{rows}</div></div></section>{closing(C)}'''
    return page('blog', C, body)


def post_page(i):
    d, s, slug, t, lead, paras, changed, pic, link = POSTS[i]
    C = dict(BLOG, title=f'{t} · Aero blog', desc=lead, h1=t, lead=lead)
    newer = POSTS[i - 1] if i > 0 else None
    older = POSTS[i + 1] if i + 1 < len(POSTS) else None
    ps = ''.join(f'<p>{E(p)}</p>' for p in paras)
    ch = ''.join(f'<li>{ic("check")}{E(x)}</li>' for x in changed)
    wash = {'publish': 'w-publish', 'test': 'w-test', 'review': 'w-review'}.get(s, 'w-hero')
    fig = f'<figure class="s-post-pic {wash}">{crop(pic[0], pic[1], pic[2], label=t)}</figure>' if pic else ''
    nav_ = '<nav class="s-pn">'
    nav_ += f'<a href="blog-{older[2]}.html"><span class="site-eyebrow">{E(C["prev"])}</span><b>{E(older[3])}</b></a>' if older else '<span></span>'
    nav_ += f'<a class="r" href="blog-{newer[2]}.html"><span class="site-eyebrow">{E(C["next"])}</span><b>{E(newer[3])}</b></a>' if newer else '<span></span>'
    nav_ += '</nav>'
    body = f'''<article class="s-article"><div class="site-wrap s-narrow">
<nav class="s-crumb" aria-label="Breadcrumb"><a href="blog.html">{E(C['back'])}</a></nav>
<div class="s-post-meta"><time datetime="{d}">{fdate(d)}</time>{pill(s)}</div>
<h1 class="site-h1 s-h1-post" data-c="h1">{dot(t)}</h1><p class="site-lead" data-c="lead">{E(lead)}</p>
{fig}<div class="s-prose">{ps}<h2 class="site-h3">What changed</h2><ul class="s-changed">{ch}</ul>
<p><a class="s-more" href="{link}">See it on the features page{ic('arrow')}</a></p></div>{nav_}</div></article>{closing(C)}'''
    ld = {'@context': 'https://schema.org', '@type': 'BlogPosting', 'headline': t, 'datePublished': d, 'description': lead, 'publisher': {'@type': 'Organization', 'name': 'Aero'}}
    return page('blog', C, body, ld=[ld])


# ================================================================ page shell
def page(cur, C, body, ld=None, canonical=None):
    data = dict(NAVC)
    data.update({k: v for k, v in C.items()})
    js = (H / 'site.js').read_text()
    blob = json.dumps(data, ensure_ascii=False, indent=1).replace('</', '<\\/')
    lds = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (ld or []))
    can = f'<link rel="canonical" href="{canonical}">' if canonical else ''
    return f'''<!doctype html><html lang="en-GB" data-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(C['title'])}</title>
<meta name="description" content="{html.escape(C['desc'])}">{can}
<!-- COPY: every word on this page, in one block. Strings can be edited here; lists need build.py. -->
<script type="application/json" id="copy">
{blob}
</script>{lds}
<link rel="icon" href="../shared/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@300..600&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../shared/aero.css"><link rel="stylesheet" href="extra.css"><link rel="stylesheet" href="review.css"><link rel="stylesheet" href="site.css"></head>
<body class="site s-page">
{nav(cur)}
<main>{body}</main>
{footer()}
<script src="../shared/glass-settings.js"></script><script src="../shared/glass-v3.js"></script>
<script>{js}</script></body></html>'''


BAD = ('—', '–', 'claude mcp', 'connector', 'Starter plan', 'color', 'Connect Aero', 'Watch people use it', 'Same link', 'in seconds', 'AI-powered', 'a month after')


def check(name, out):
    vis = re.sub(r'<style.*?</style>|<script(?! type="application/json").*?</script>|style="[^"]*"|<div class="s-crop-in".*?</div></div>', '', out, flags=re.S)
    # the crops carry v3 app markup (checked in v3); scan only the page's own words
    words = re.sub(r'<div class="s-crop.*?data-max="[^"]*"[^>]*>', '', vis)
    bad = [w for w in BAD if w in words and not (w == '–' and 's-no' in words and words.count('–') == words.count('aria-label="Not included">–'))]
    return bad


if __name__ == '__main__':
    pages = {'features.html': features_page(), 'pricing.html': pricing_page(), 'use-cases.html': use_cases_page(), 'guides.html': guides_page(),
             'publish-a-claude-artifact.html': task_page(), 'blog.html': blog_page()}
    for i, p in enumerate(POSTS):
        pages[f'blog-{p[2]}.html'] = post_page(i)
    allc = json.dumps([FEAT, GROUPS, PRICE, USES, USE_CASES, GUIDE, GUIDES, TASK, BLOG, POSTS, NAVC], ensure_ascii=False)
    bad = [w for w in BAD if w in allc and w != '–']
    for n, out in pages.items():
        (H / n).write_text(out)
    print('built', len(pages), 'pages', 'copy check:', bad or 'clean')
