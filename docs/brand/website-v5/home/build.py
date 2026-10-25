#!/usr/bin/env python3
"""Aero homepage, round 5 (24 Oct 2026, evening), Team H. Builds home.html.

The app screens are the real v3 components, imported read-only from ../../v3/make/build.py and ../../v3/review/build.py,
with this page's example data (Pocket, a payments web app; Maya testing it). Every word people read is in COPY below and
is embedded in home.html as one JSON block (home.js applies it on load, so a word can be changed there too).
Run: python3 build.py"""
import html, importlib.util, json, pathlib, re

H = pathlib.Path(__file__).resolve().parent
R = H.parent.parent
SH = H.parent / 'shared'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


mk = load('v3make', R / 'v3/make/build.py')
rv = load('v3review', R / 'v3/review/build.py')
ic = mk.ic
rv.I.update({k: v for k, v in mk.I.items() if k not in rv.I})


def svg_logo(name, cls=''):
    s = (SH / name).read_text().strip().replace('fill="#1D1D1F"', 'fill="currentColor"')
    return s.replace('<svg ', f'<svg class="{cls}" aria-hidden="true" ', 1)


LOCKUP = svg_logo('lockup.svg')
GLASS_INK = 'data-glass-v3="primary" data-fill="rgba(29,29,31,.8)"'

# ================================================================ COPY: every word on the page
COPY = {
    'meta.title': 'Aero: one prompt and it’s live, one link and it’s tested',
    'meta.desc': 'Publish a Claude artifact, Figma prototype, Lovable app or HTML site to its own address, then send one test link. People try it on their own computer; you get the recording, transcript and summary back. Free to start.',
    'nav': ['Features', 'Pricing', 'Use cases', 'Guides', 'Blog'], 'nav.login': 'Log in', 'nav.start': 'Start free',

    # three propositions (research options 1, 2, 3); #p1 / #p2 / #p3 switch between them
    'p1.h1': ['One prompt and it’s live', 'One link and it’s tested'],
    'p1.lead': 'Then send one test link and get the recording, transcript and summary back.',
    'p2.h1': ['Test it the day you make it'],
    'p2.lead': 'Put it online at your own aeroapp.ai address and share one test link. Hear where people got stuck, in their own words. Testers need no software or account.',
    'p3.h1': ['From prompt to first session'],
    'p3.lead': 'Aero puts it online and gives you a link to test it. Testers need no download, and each session comes back transcribed and summarised.',
    'hero.made.a': 'Publish your', 'hero.made': ['Claude artifact', 'Figma prototype', 'Lovable app', 'HTML site'],
    'hero.cta1': 'Start free', 'hero.cta2': 'See pricing',
    'hero.fine': ['Free to start', 'From $3 a month', 'No call, no contract'],
    'steps': [['Publish', 'One prompt, and it’s live at its own address.'],
              ['Test', 'One link. They try it on their own computer, talking it through.'],
              ['Review', 'Transcript and summary, then every session together.']],
    'switch.k': 'Headline', 'switch': ['1', '2', '3'],

    # stage (the hero animation): words inside the screens
    'st.claude.ask': 'Make a simple web app for Pocket: balance, send money, cards and spending.',
    'st.claude.made': 'Here’s Pocket. A home screen with the balance and quick actions, a send flow and a spending page.',
    'st.claude.card': 'Pocket · web app',
    'st.prompt': 'Publish the app you just built to Aero as a site called “pocket”. Send every file through the Aero API at aeroapp.ai/api/v1/sites with my key aero_sk_••••7Q2c, then reply with the address.',
    'st.claude.work': 'Working · calling the Aero API',
    'st.claude.used': 'Used the Aero API · publish',
    'st.claude.done': 'Done. It’s live at pocket.aeroapp.ai, version 1.',
    'st.claude.input': 'Reply to Claude',
    'st.msg.to': 'To Maya',
    'st.msg': 'Could you try this for me? Takes a few minutes. aeroapp.ai/t/pocket-7k2',
    'st.copied': 'Copied',
    'st.who.maya': 'Maya’s laptop',
    'st.note.from': 'Mia Chen',
    'st.say': ['“Okay, send twenty pounds to Sam. Send is right there.”', '“I thought last month would be right here. Where do I change the month?”'],
    'cap': ['Paste Aero’s one prompt into Claude', 'Claude publishes it to Aero', 'In Aero it’s live, with its own page', 'Visit opens the live site in a new tab',
            'Make a test from the site and copy its link', 'Send the link to someone', 'Maya opens it on her own laptop',
            'She tries the tasks and thinks aloud. Her tab and voice are recorded', 'Her session, transcribed, with the friction points', 'Insights: every session together',
            'Next version: copy the prompt again'],
    'hero.aria': 'How Aero works, a 45-second loop. In Claude, Aero’s one prompt is pasted and Claude publishes Pocket to pocket.aeroapp.ai. In Aero the site is live; Visit opens it in a new tab. A test is made from the site and its link is sent to Maya. On her own laptop she opens it, allows the microphone and the tab, and tries two tasks while her tab and voice are recorded. Back in Aero her session is transcribed with friction points, and Insights sums up every session. Then the prompt is copied again for the next version. Press Space to pause.',

    'pub.k': 'Publish',
    'pub.h2': 'One prompt and it’s live',
    'pub.body': 'Built it in Claude or ChatGPT? Aero gives you one prompt. Paste it into the chat where you made the thing and it publishes there and then, at its own aeroapp.ai address. No hosting to set up, no domain settings to learn.',
    'pub.more': 'Or paste a Figma prototype link, or drop an HTML file, folder or zip. Publish again to the same address whenever it changes; every version is kept.',
    'pub.facts': [['prompt', 'One prompt', 'Nothing to install or connect'], ['folder', 'Figma link or HTML upload', 'A link, a file, a folder or a zip'],
                  ['globe', 'Custom domain', 'Your own domain, on Solo and up'], ['lock', 'Password protection', 'On Basic and up'],
                  ['undo', 'Versions', 'Every publish kept, roll back any time'], ['site', 'Your own address', 'name.aeroapp.ai, on Basic and up']],
    'test.k': 'Test',
    'test.h2': 'One link. They open it, and that’s it',
    'test.body': 'Every site can become a test with its own short link. Send it to a client, a friend or a classmate. They open it on their own computer, allow the microphone and this one tab, and think aloud while they try your tasks.',
    'test.more': 'No app to install, no account to make, no session to book. Your own “Preview as tester” runs are free and stay out of your results.',
    'test.facts': [['tab', 'Screen and voice', 'This tab only, never the camera'], ['user', 'No account', 'Or software, for testers'], ['check', 'Optional tasks', 'In a panel they can move'], ['ext', 'Preview as tester', 'Free, kept out of results']],
    'rev.k': 'Review',
    'rev.h2': 'What to fix, in their own words',
    'rev.body': 'About a minute after each session, it’s transcribed and summarised. Play any line and the words light up as they’re said. Insights puts every session together: what to fix first, how many testers hit it, and the quotes.',
    'rev.more': 'No hours scrubbing through recordings, and no notes to take. It still reads well: a session reads like a short article, and the whole test fits on one page.',
    'rev.facts': [['book', 'Transcript and summary', 'On every plan'], ['chart', '“4 of 6 testers”', 'Ranked by how serious'], ['play', 'Quotes you can play', 'From the moment it was said'], ['down', 'Download', 'The report, the transcript, the video']],

    'uc.k': 'Use cases',
    'uc.h2': 'For people who make things',
    'uc.body': 'A few of the ways people use it. Every name here is an example.',
    'uc.items': [
        ['folder', 'A portfolio from a folder of work', 'Lena asks Claude to turn her case-study folder into a site, publishes it with one prompt, then has two classmates try it. Neither found her contact link.', 'Student'],
        ['test', 'An idea at night, insights by the morning', 'Tom builds a pricing page after dinner, sends the test link to four customers at 9pm and reads where they hesitated over coffee.', 'Founder'],
        ['figma', 'A Figma flow before the review', 'Priya pastes her checkout prototype at 4pm, sends the link to five colleagues and reads three summaries before tomorrow’s design review.', 'Product designer'],
        ['lock', 'A client site behind a password', 'Marco sends his client a password-protected preview on their own domain, then asks three of their staff to test the booking flow.', 'Freelancer'],
        ['site', 'A weekend build with a real address', 'Sam turns a weekend Claude artifact into a live tool at sam.aeroapp.ai and shares it in a group chat, off claude.ai.', 'Maker'],
    ],

    'pr.k': 'Pricing',
    'pr.h2': 'Priced for one designer, not a corporate',
    'pr.body': 'Free to start, recordings included. Paid plans from $3 a month, billed monthly, with a 7-day free trial and no call. Below, the cheapest plan with recordings from each tool that tests a prototype with people you invite, every price per month.',
    'pr.cols': ['Aero Free', 'Aero Basic', 'Maze Free', 'Lookback Freelance', 'Userbrain Starter', 'Lyssna Growth'],
    'pr.us': 2,
    'pr.rows': [
        ['Price per month', ['$0', '$3', '$0', '$25 ²', '$49', '$199 ³']],
        ['Billing', ['No card needed', 'Monthly, cancel any time', 'Free plan', 'Yearly only, $299 a year', 'Monthly', 'Monthly, or $166 a month billed yearly']],
        ['Sessions with your own testers', ['3 ¹', '5 ¹', '1 study a month', '10 a year', '3 a month', '5 in-depth studies a month']],
        ['Screen and voice recording', ['yes', 'yes', 'no', 'yes', 'yes', 'yes']],
        ['Transcript and summary', ['yes', 'yes', 'no', 'AI analysis; transcript not checked', 'yes', 'yes']],
        ['Hosts your prototype', ['yes · live for 7 days', 'yes · your own aeroapp.ai address', 'no', 'no', 'no', 'no']],
        ['Testers install nothing', ['yes · in their browser ⁴', 'yes · in their browser ⁴', 'Not checked', 'iPhone needs an app; desktop not checked', 'Needs a Chrome extension or app', 'Desktop yes; phone recording uses an app']],
    ],
    'pr.notes': [
        '¹ Aero’s sessions are a total on your plan, not a monthly allowance. The others reset each month or year, so the counts aren’t a straight comparison.',
        '² Lookback sells yearly plans only: $299 a year, about $25 a month.',
        '³ $199 billed monthly; $166 a month when billed yearly. Lyssna Growth also includes unlimited unmoderated responses.',
        '⁴ Figma prototype tests also work on a phone, voice only; site and HTML tests need a computer.',
        'Maze Free: 1 study a month and 5 seats; recordings (Clips) and interview transcription are on Enterprise only, which has no public price. Dovetail is Free or Enterprise; UserTesting publishes no prices.',
        'Prices in USD from each company’s own pricing page and help centre, checked 24 Oct 2026. “Not checked” means we couldn’t confirm it, so we don’t claim it either way.',
    ],
    'pr.plans': [['Free', '$0', 'to start, 3 test sessions'], ['Basic', '$3', 'a month, 5 test sessions'], ['Solo', '$6', 'a month, adds custom domain'], ['Pro', '$19', 'a month, 20 test sessions']],
    'pr.link': 'See every plan',

    'faq.k': 'Questions',
    'faq.h2': 'Asked often',
    'faq.items': [
        ['Do my testers need an account or an app?', 'No. They open the link in their browser on their own computer, allow the microphone and the tab, and start. You choose who gets the link.'],
        ['What exactly is recorded?', 'The browser tab with your prototype, and the tester’s voice as they think aloud. Not their camera and not their other tabs.'],
        ['How does one prompt publish my site?', 'Aero gives you a prompt with a key in it. Paste it into the Claude or ChatGPT chat where you built the thing and it sends the files to Aero. Nothing to install or connect.'],
        ['What can I publish?', 'A Claude artifact or anything you built in a chat, a Figma prototype link, or an HTML file, folder or zip.'],
        ['How soon is the transcript ready?', 'About a minute after each session ends, with a short summary and the friction points in the tester’s own words.'],
        ['Is the test link the same as my site’s?', 'No. Testing a site makes a copy with its own short link, so you can change the test without touching the live site.'],
        ['Can I use my own domain?', 'Yes, on Solo and up. Password protection comes with Basic and up.'],
        ['Can people test on a phone?', 'Figma prototype tests work on a phone and record the tester’s voice only. Site and HTML tests need a computer, because Aero records the tab.'],
        ['What do I get for free?', '3 test sessions with recordings, transcripts and summaries, and sites that stay live for 7 days. Paid plans have a 7-day free trial.'],
    ],

    'close.h2': 'Put it online. Find out what people think',
    'close.p': 'Free to start. From $3 a month. No call, no contract.',
    'foot.tag': 'Made for people who make things',
    'foot.cols': [['Product', ['Features', 'Pricing', 'Use cases', 'Blog']],
                  ['Guides', ['Publish a Claude artifact', 'Test a Figma prototype', 'Host an HTML site']],
                  ['Aero', ['Log in', 'Start free', 'Coming from Figmafolio']],
                  ['Legal', ['Privacy', 'Terms']]],
    'foot.fine': 'Names, sessions and numbers shown on this page are examples.',
}
NAV_HREF = ['../site/features.html', '../site/pricing.html', '../site/use-cases.html', '../site/guides.html', '../site/blog.html']


def e(s):
    return html.escape(s, quote=False)


def c(key, tag='span', cls='', sub=None):
    v = COPY[key] if sub is None else COPY[key][sub]
    k = key if sub is None else f'{key}.{sub}'
    cl = f' class="{cls}"' if cls else ''
    return f'<{tag}{cl} data-c="{k}">{e(v)}</{tag}>'


DOT = '<span class="hd-dot">.</span>'
CL_LOGO = '<svg class="cl-logo" viewBox="0 0 16 16" aria-hidden="true"><g stroke="#D97757" stroke-width="2.1" stroke-linecap="round"><path d="M8 8 L14.47 9.31"/><path d="M8 8 L11.65 13.50"/><path d="M8 8 L6.69 14.47"/><path d="M8 8 L2.50 11.65"/><path d="M8 8 L1.53 6.69"/><path d="M8 8 L4.35 2.50"/><path d="M8 8 L9.31 1.53"/><path d="M8 8 L13.50 4.35"/></g></svg>'


def gbtn_ink(label_key, size='md', href='#', cls=''):
    return f'<a class="btn g3 {size} {cls}" href="{href}" {GLASS_INK}>{c(label_key)}</a>'


def gbtn_clear(label_key, size='md', href='#', cls=''):
    return f'<a class="btn g3 {size} {cls}" href="{href}" data-glass-v3="secondary">{c(label_key)}</a>'


# ================================================================ example content: Pocket, the web app Claude builds
def pocket_desk(state='home', build=False):
    """Pocket desktop web app (the tester's content: fixed colours, never themed). Uses v3 .pk parts plus .pq-* for the
    send and spending screens. build=True tags the parts so the hero can build it up in Claude's preview."""
    b = (lambda n: f' data-b="{n}"') if build else (lambda n: '')
    top = f'<div class="pk-top"{b(0)}><b>● Pocket</b><span>Home</span><span>Cards</span><span>Spending</span><span class="pk-av">SR</span></div>'
    home = f'''<div class="pq pq-home">{top}
<div class="pk-hero"{b(1)}><small>Main balance</small><div class="pk-bal">£2,480<span>.12</span></div><div class="pk-acts"><span>Send</span><span>Request</span><span>Split</span><span>Freeze</span></div></div>
<div class="pk-row"{b(2)}><div class="pk-c" style="background:#FFD24A"><small>Groceries</small><b>£212</b></div><div class="pk-c" style="background:#1D1D1F;color:#fff"><small>Travel</small><b>£86</b></div><div class="pk-c" style="background:#fff"><small>Eating out</small><b>£64</b></div></div>
<div class="pk-list"{b(3)}><div><b>Corner Coffee</b><span>−£4.20</span></div><div><b>Sam Rivera</b><span>+£36.00</span></div><div><b>Market Hall</b><span>−£52.18</span></div></div></div>'''
    if build:
        return f'<div class="pk pq-wrap">{home}</div>'
    send = f'''<div class="pq pq-send">{top}<div class="pq-card"><small>Send money</small><div class="pq-to"><span class="pk-av">SR</span><div><b>Sam Rivera</b><span>In your contacts</span></div></div>
<div class="pq-amt">£20<span>.00</span></div><div class="pq-btn">Send £20</div></div></div>'''
    spend = f'''<div class="pq pq-spend">{top}<div class="pq-sh"><h6>Spending</h6><span class="pq-tabs"><span class="on">This week</span><span>Oct</span><span>Sep</span></span></div>
<div class="pq-bars"><div><span>Groceries</span><i style="width:78%"></i><b>£212</b></div><div><span>Travel</span><i style="width:34%"></i><b>£86</b></div><div class="hl"><span>Eating out</span><i style="width:26%"></i><b>£64</b></div><div><span>Bills</span><i style="width:52%"></i><b>£140</b></div></div></div>'''
    on = {'home': 'home', 'send': 'send', 'spend': 'spend'}[state]
    return f'<div class="pk pq-wrap" data-pq="{on}">{home}{send}{spend}</div>'


# ================================================================ app screens (real v3 components, Pocket data)
def scaled(inner, w, h, cls='', style=''):
    """A real app window at its native size (w x h), scaled by CSS to its box: --s is set by home.js."""
    return f'<div class="sc-box {cls}" data-w="{w}" data-h="{h}" style="{style}"><div class="sc-in" style="width:{w}px;height:{h}px">{inner}</div></div>'


def to_pocket(out):
    for a, b in [('checkout.zip · 17 files', 'From Claude · 9 files'), ('checkout.aeroapp.ai', 'pocket.aeroapp.ai'),
                 ('<b>Checkout</b>', '<b>Pocket</b>'), ('x-in">Checkout<', 'x-in">Pocket<'), ('--site:#1F8F5F', '--site:#FF5A36'),
                 ('aeroapp.ai/sites/checkout', 'aeroapp.ai/sites/pocket')]:
        out = out.replace(a, b)
    return out


def pq_thumb(w, h, cls=''):
    return f'<div class="th desk {cls}" style="width:{w}px;height:{h}px"><div class="pq-th" style="transform:scale({w / 1440:.4f})">{pocket_desk("home")}</div></div>'


def prompt_done():
    real = mk.thumb
    mk.thumb = lambda kind, w, h, scale=None, cls='', sheet=False, top=None: pq_thumb(w, h, cls)
    try:
        return mk.prompt_done().replace('the same page, a minute later', '')
    finally:
        mk.thumb = real


def site_published():
    real_thumb, real_window = mk.thumb, mk.window

    def thumb(kind, w, h, scale=None, cls='', sheet=False, top=None):
        if kind == 'checkout' and w == 700:
            return f'<div class="th desk {cls}" style="width:{w}px;height:{h}px"><div class="pq-th">{pocket_desk("home")}</div></div>'
        return real_thumb(kind, w, h, scale, cls, sheet, top)

    def window(url, side, main, h=900, cls='', rail=False):
        return real_window(url.replace('checkout', 'pocket'), side, to_pocket(main), h, cls, rail)

    mk.thumb, mk.window = thumb, window
    try:
        return mk.site_page(just=True, menu=True)
    finally:
        mk.thumb, mk.window = real_thumb, real_window


def test_setup():
    real_thumb = mk.thumb

    def thumb(kind, w, h, scale=None, cls='', sheet=False, top=None):
        if kind == 'checkout':
            return f'<div class="th desk {cls}" style="width:{w}px;height:{h}px"><div class="pq-th sm">{pocket_desk("home")}</div></div>'
        return real_thumb(kind, w, h, scale, cls, sheet, top)

    mk.thumb = thumb
    try:
        out = mk.test_setup()
    finally:
        mk.thumb = real_thumb
    for a, b in [('Add the linen tote to your basket and check out.', 'Send £20 to Sam.'), ('Use any card details; nothing is charged.', 'Sam is already in your contacts.'),
                 ('Change delivery to next day.', 'Find out what you spent on eating out last month.'), ('<div class="x-task">', '<div class="x-task">', ),
                 ('This is an early checkout for Paper &amp; Co.', 'This is an early version of Pocket, a payments app.'),
                 ('aeroapp.ai/t/checkout-4mq', 'aeroapp.ai/t/pocket-7k2'), ('checkout.aeroapp.ai', 'pocket.aeroapp.ai'),
                 ('aeroapp.ai/tests/checkout/setup', 'aeroapp.ai/tests/pocket/setup'), ('<b>Checkout</b></span>', '<b>Pocket</b></span>'),
                 ('x-in">Checkout<', 'x-in">Pocket<'), ('test.kestrel.studio', 'test.pocket.money')]:
        out = out.replace(a, b)
    # only two tasks: drop the third
    out = re.sub(r'<div class="x-task">(?:(?!<div class="x-task">).)*?Find out how to return an item\..*?</div>', '', out, count=1, flags=re.S)
    out = out.replace('<div class="sb-si on"><span class="sb-st "></span><span class="sb-nm">Checkout</span>', '<div class="sb-si"><span class="sb-st "></span><span class="sb-nm">Checkout</span>')
    out = out.replace('<div class="sb-si "><span class="sb-st new"></span><span class="sb-nm">Pocket</span>', '<div class="sb-si on"><span class="sb-st new"></span><span class="sb-nm">Pocket</span>')
    # just made: no sessions yet, and it's a copy of version 1
    out = out.replace('<span class="sb-st new"></span><span class="sb-nm">Pocket</span><span class="sb-t new">2 new</span>', '<span class="sb-st "></span><span class="sb-nm">Pocket</span><span class="sb-t">0</span>')
    out = out.replace('<span class="mono">pocket.aeroapp.ai</span> v8', '<span class="mono">pocket.aeroapp.ai</span> v1')
    # the copy button gets a "Copied" state the stage can switch to
    out = out.replace('<span class="mono">aeroapp.ai/t/pocket-7k2</span>', '<span class="mono st-link">aeroapp.ai/t/pocket-7k2</span>', 1)
    return out


TASKS2 = [('Send £20 to Sam', 'Sam is already in your contacts.'), ('Find out what you spent on eating out last month', 'Use the app as you normally would.')]


def task_panel(n):
    """The v3 task plate, on the left (decided). Like the real overlay, a red recording dot sits by "Task n of 2"."""
    t, d = TASKS2[n - 1]
    segs = ''.join(f'<i class="{"done" if k < n - 1 else ("cur" if k == n - 1 else "")}"></i>' for k in range(2))
    return f'''<div class="x-tk st-tk" data-theme="light" style="left:28px;bottom:28px"><div class="x-tkh"><span class="x-gl x-grip">{ic('drag')}</span><span class="st-recdot"></span><span class="x-tkn">Task {n} of 2</span><span class="x-gl x-tkmin">{ic('chev')}</span></div>
<div class="x-tkb"><b>{t}.</b><p>{d}</p></div><div class="x-tkp">{segs}</div>
<div class="x-tka"><span class="btn g3 md ink st-done">Done</span><span class="x-cant">Couldn’t do it</span></div></div>'''


def tester_screen(bar=True, h=724):
    """Maya's computer: the site in its own tab, the task plate over it (left) and the quiet "Recording" sign.
    No waveform and no timer: the real tester UI shows a recording dot, not her voice."""
    layer = (f'<div class="st-tks"><div class="st-tk1">{task_panel(1)}</div><div class="st-tk2">{task_panel(2)}</div></div>'
             + mk.recchip(mk.REC_AT))
    inner = f'{pocket_desk("home")}<div class="x-tklayer">{layer}</div>'
    top = mk.bar("aeroapp.ai/t/pocket-7k2") if bar else ''
    return f'<div class="win full x-w x-tb st-tester">{top}<div class="x-tbody" style="height:{h}px">{inner}</div></div>'


TR = [  # seconds, words, tag kind, severity, title
    ('task', '1', 'Send £20 to Sam'),
    (14, 'Okay, send twenty pounds to Sam. Send is right there.', 'good', None, 'Send is easy to find'),
    (51, 'Done? I think it went. There’s no tick or anything.', 'conf', None, 'Not sure the money went'),
    ('task', '2', 'Find what you spent on eating out'),
    (80, 'Spending, maybe? No, that’s only this week.', '', None, ''),
    (102, 'I thought last month would be right here. Where do I change the month?', 'issue', 'major', 'Last month is hard to find'),
    (125, 'Oh, the months are those tiny tabs at the top. Quite small.', 'issue', 'minor', 'Month tabs are small'),
    (151, 'Sixty-four pounds. Fine, that’s clear once you’re there.', 'good', None, 'Totals read clearly'),
]
LEN = 214
TK = [('1', 'Send £20 to Sam', 8, 74), ('2', 'Find what you spent on eating out', 74, 178)]
MOM = [(14, 'good', None, ''), (51, 'conf', None, ''), (102, 'issue', 'major', ''), (125, 'issue', 'minor', ''), (151, 'good', None, '')]


def watch_window():
    """v3 Watch view (dark in the hero) for Maya's session on Pocket, desktop."""
    rows = ''
    for r in TR:
        if r[0] == 'task':
            rows += f'<div class="tl task"><span class="mono">Task {r[1]}</span><span class="tn">{r[2]}</span></div>'
            continue
        s, words, k, sv, title = r
        w = ' '.join(f'<span class="w">{e(x)}</span>' for x in words.split(' '))
        tg = rv.tagline(k, title, sv) if k else ''
        rows += f'<div class="tl future" data-s="{s}"><span class="mono">{rv.mmss(s)}</span><div class="tx"><p>{w}</p>{tg}</div></div>'
    trans = f'''<div class="insp2"><div class="itabs"><span>Summary</span><span class="on">Transcript</span><span>Notes</span><span class="r">{ic('search')}</span></div>
<div class="tfollow"><span class="sw"><i class="on"></i>Follow the recording</span><span class="mono">click a line to jump</span></div>
<div class="trs scroll st-trs">{rows}</div>
<div class="addnote"><span class="input">{rv.ic('note')}Add a note<span class="kbd" style="margin-left:auto">C</span></span></div></div>'''
    video = f'<div class="st-vid">{pocket_desk("home")}</div>'
    stg = f'<div class="stage3"><div class="video">{video}<div class="vpill"><span class="taskpill"><span class="dot"></span><span class="mono st-tpn">Task 1 of 2</span><span class="st-tpt">Send £20 to Sam</span></span></div></div></div>'
    ctl = rv.player_controls(length=LEN, now=80, tasks=TK, moments=MOM, notes=[])
    ctl = ctl.replace('<span class="tc">01:20', '<span class="tc"><span class="st-tc">01:20</span>', 1)
    head = rv.sesshead(name='Maya', pos='2 of 6', prev='Tom', nxt='Priya')
    strip = rv.meta_strip(name='Maya', dev='Laptop · Chrome 129 · macOS', ln='03:34', tasks='Tasks 2 of 2')
    main = head + strip + f'<div class="watch"><div class="wleft">{stg}{ctl}</div>{trans}</div>'
    return rv.window('aeroapp.ai/tests/pocket/sessions/2', rv.sidebar(rail=True), main, h=900, rail=True)


def insights_window():
    summ = '''<div class="sumcard2"><div class="lbl2">Summary <span>· 6 sessions with audio</span></div>
<p>Everyone sent money to Sam without help, though three weren’t sure it had gone. Last month’s spending was the problem: <b>4 of 6 testers</b> looked for it on the home screen first, and the month tabs were easy to miss. Fix first: make the month easy to change.</p></div>'''
    iss = rv.issue_item(1, 'Last month is hard to find', 'issue', 'major', ['Maya', 'Jonas', 'Ana', 'Leo'],
                        'Testers expected a month switch near the totals. Most found the small tabs after a minute or more.',
                        [('Maya', 'a', '01:42', 'I thought last month would be right here. Where do I change the month?', True, 1.0, .45),
                         ('Jonas', 'd', '01:15', 'Is this only this week? I need October.', False, 1.4), ('Leo', 'f', '02:02', 'The tabs are tiny.', False, .8)])
    iss += rv.issue_item(2, 'No confirmation after sending', 'conf', None, ['Maya', 'Tom', 'Priya'], 'No tick or message after Send, so three testers checked twice.',
                         [('Maya', 'a', '00:51', 'Done? I think it went. There’s no tick or anything.', False, 1.2), ('Tom', 'b', '00:40', 'Did that work?', False, .9)])
    iss += rv.issue_item(3, 'Month tabs are small', 'issue', 'minor', ['Maya', 'Ana', 'Leo'], 'Once found, the tabs were hard to hit.',
                         [('Ana', 'e', '02:20', 'I keep missing the tab.', False, 1.1)])
    lst = f'''<div class="blk"><div class="bh"><h3>What to fix first</h3><span class="seg"><span class="on">By priority</span><span>By task</span><span>By theme</span></span>
<span class="r">{rv.gbtn('Copy as table', 'table')}{rv.btn('Download report', icon='down')}</span></div>{iss}</div>'''
    tg = rv.tag
    aside = f'''<aside class="ins-side"><div class="blk2"><div class="lbl2">What worked</div>
<div class="wk">{tg('good')}<span>Send is easy to find</span><span class="mono">6 of 6</span></div>
<div class="wk">{tg('good')}<span>Totals read clearly</span><span class="mono">5 of 6</span></div></div>
<div class="blk2"><div class="lbl2">In this summary</div>
{''.join(f'<div class="sl"><span class="av {a}">{n[0]}</span>{n}<span class="mono r">{l}</span></div>' for n, a, l in [('Maya', 'a', '03:34'), ('Tom', 'b', '02:58'), ('Priya', 'c', '04:40'), ('Jonas', 'd', '03:55'), ('Ana', 'e', '05:21'), ('Leo', 'f', '03:18')])}</div></aside>'''
    main = rv.testhead(tab='Insights', count='6', kind='', meta='<span class="mono">aeroapp.ai/t/pocket-7k2</span><span class="st live">Live</span><span>2 tasks</span><span>6 sessions</span>') + f'<div class="insights"><div class="ins-main">{summ}{lst}</div>{aside}</div>'
    return rv.window('aeroapp.ai/tests/pocket/insights', rv.sidebar(), main, h=900)


# ================================================================ hero stage: ONE browser window at an angle, then Maya's own laptop
def claude_window():
    """Claude, simplified and clearly not Aero: its own colours and type. Pocket is already built in its preview."""
    ar = (f'<div class="cl-art"><span class="cl-arti"></span><span><b data-c="st.claude.card">{e(COPY["st.claude.card"])}</b><small>Click to open</small></span></div>')
    return f'''<div class="cl-win"><div class="cl-body"><div class="cl-chat">
  <div class="cl-head">{CL_LOGO}Claude</div>
  <div class="cl-msgs">
    <div class="cl-you">{c('st.claude.ask')}</div>
    <div class="cl-ai"><p>{c('st.claude.made')}</p>{ar}</div>
    <div class="cl-you cl-sent">{c('st.prompt')}</div>
    <div class="cl-ai cl-reply"><div class="cl-tool cl-work"><span class="dotload"></span>{c('st.claude.work')}</div>
      <div class="cl-tool cl-used">{ic('check')}{c('st.claude.used')}</div><p class="cl-done">{c('st.claude.done')}</p></div>
  </div>
  <div class="cl-inp"><span class="cl-ph">{c('st.claude.input')}</span><span class="cl-paste">{c('st.prompt')}</span><span class="cl-send">{ic('up')}</span></div>
</div>
<div class="cl-prev"><div class="cl-ptop"><b>Pocket</b><span>Preview</span><span class="cl-code">Code</span></div><div class="cl-pv"><div class="cl-pvin">{pocket_desk('home')}</div></div></div>
</div></div>'''


MARK_SM = svg_logo('mark.svg', 'hv-fav').replace('fill="#3478F6"', 'fill="var(--blue)"')
TABS = [('claude', CL_LOGO.replace('cl-logo', 'hv-fav'), 'Pocket · Claude'), ('aero', MARK_SM, 'Pocket · Aero'), ('site', '<span class="hv-pq"></span>', 'Pocket')]
MTABS = [('ctl', MARK_SM, 'Testing Pocket'), ('pk', '<span class="hv-pq"></span>', 'Pocket')]
CURSOR = '<svg class="hv-cur" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 2.5v17.2l4.3-4.2 2.9 6.6 3-1.3-2.9-6.5h6.1z" fill="#1D1D1F" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"/></svg>'


def chrome(tabs, url, cls=''):
    t = ''.join(f'<span class="hv-tab" data-tab="{k}">{fav}<span>{e(n)}</span><i class="hv-x"></i></span>' for k, fav, n in tabs)
    return f'''<div class="hv-chrome {cls}"><div class="hv-tabs"><span class="lights"><i></i><i></i><i></i></span>{t}</div>
<div class="hv-addr"><span class="hv-nav">{ic('left')}{ic('right')}</span><span class="hv-url">{ic('lock')}<span class="hv-u">{url}</span></span><span class="hv-prof"></span><i class="hv-prog"></i></div></div>'''


def prompt_scene():
    """New site, from a prompt: copy the prompt; after Claude publishes, the same page says so (it updates by itself)."""
    out = mk.prompt_page().replace('--h:624px', '--h:864px').replace('aeroapp.ai/sites/', 'aeroapp.ai/sites/')
    done = f'<div class="hv-pdone">{scaled(prompt_done(), 560, 230, "hv-dn")}</div>'
    out = out.replace('<div class="x-waitb">', done + '<div class="x-waitb">', 1)
    return out.replace('Copy prompt</span>', '<span class="hv-cp">Copy prompt</span><span class="hv-cpd">Copied</span></span>', 1)


def sites_scene():
    real = mk.SITES[:]
    mk.SITES[1] = ('pocket', 'Pocket', 'pocket.aeroapp.ai', 'v1', 'From a prompt', 'live', '6', 'Pocket')
    real_thumb = mk.thumb
    mk.thumb = lambda kind, w, h, scale=None, cls='', sheet=False, top=None: pq_thumb(w, h, cls) if kind == 'pocket' else real_thumb(kind, w, h, scale, cls, sheet, top)
    try:
        out = mk.sites_list()
    finally:
        mk.SITES[:] = real
        mk.thumb = real_thumb
    return out.replace('--h:744px', '--h:864px')


def maya_device():
    """Maya's own laptop: a different machine (bezel, her wallpaper, menu bar, dock, her profile in Chrome).
    The notification arrives, she opens the link, says yes to the microphone and the tab, and the test runs in a
    second tab with the task plate. Nothing on her screen is a cursor."""
    welcome = mk.tester_start().replace('Mia at Kestrel Studio asked you to try', 'Mia at Kestrel Studio asked you to try').replace('Ana<span class="x-car"></span>', 'Maya')
    perm = mk.tester_perm().replace('Step 2 of 2 · Ana', 'Step 2 of 2 · Maya').replace('So Mia can hear what you think.', 'So Mia can hear what you think.')
    perm = perm.replace('Share this tab</span>', '<span class="hv-share">Share this tab</span></span>', 1)
    dock = ''.join(f'<i style="background:{c}"></i>' for c in ('#2F7CF6', '#34C759', '#FF9F0A', '#FF453A', '#BF5AF2', '#8E8E93'))
    return f'''<div class="hv-maya"><div class="hv-lap"><div class="hv-scr">
<div class="hv-wall"></div>
<div class="hv-menu"><b></b><span>Chrome</span><span>File</span><span>Edit</span><span>View</span><span class="r">Sun 21:04</span></div>
<div class="hv-note"><span class="hv-nicon">{ic('prompt')}</span><div><b>{c('st.note.from')}</b><span>{c('st.msg')}</span></div><small>now</small></div>
<div class="hv-mwin">{chrome(MTABS, 'aeroapp.ai/t/pocket-7k2', 'hv-mch')}
<div class="hv-mvp"><div class="hv-mvi">
  <div class="hv-ms" data-ms="w">{welcome}</div>
  <div class="hv-ms" data-ms="p">{perm}</div>
  <div class="hv-ms" data-ms="t">{tester_screen(bar=False, h=788)}</div>
</div></div></div>
<div class="hv-dock">{dock}</div>
</div></div><div class="hv-base"></div>
<div class="hv-under"><span class="hv-who">{ic('user')}{c('st.who.maya')}</span><span class="hv-say"><span class="hv-sayi">{ic('mic')}</span><q class="hv-q" data-q="0">{e(COPY['st.say'][0])}</q><q class="hv-q" data-q="1">{e(COPY['st.say'][1])}</q></span></div>
</div>'''


def stage():
    site = site_published()
    site = re.sub(r'<span class="gbtn ">(<svg[^>]*>(?:(?!</svg>).)*</svg>)Visit</span>', r'<span class="gbtn hv-visit">\1Visit</span>', site, count=1, flags=re.S)
    site = site.replace('<div class="sb-si "><span class="sb-st new"></span><span class="sb-nm">Pocket</span><span class="sb-t new">2 new</span></div>', '')  # no test yet
    msg = f'''<div class="st-msg"><div class="st-msg-to">{c('st.msg.to')}</div><div class="st-bub">{c('st.msg')}</div><div class="st-sent">{ic('check')}Delivered</div></div>'''
    return f'''<div class="st-world" aria-hidden="true">
<div class="hv-frame">{chrome(TABS, 'claude.ai/chat/pocket')}
<div class="hv-vp">
  <div class="hv-sc" data-sc="claude" data-theme="light">{claude_window()}</div>
  <div class="hv-sc" data-sc="prompt" data-theme="light">{prompt_scene()}</div>
  <div class="hv-sc" data-sc="aero" data-theme="light">{site}</div>
  <div class="hv-sc" data-sc="site" data-theme="light"><div class="hv-live">{pocket_desk('home')}</div><div class="hv-blank"></div></div>
  <div class="hv-sc" data-sc="setup" data-theme="light">{test_setup()}<div class="st-copied">{ic("check")}{c("st.copied")}</div></div>
  <div class="hv-sc" data-sc="watch" data-theme="dark">{watch_window()}</div>
  <div class="hv-sc" data-sc="ins" data-theme="dark">{insights_window()}</div>
  <div class="hv-sc" data-sc="sites" data-theme="light">{sites_scene()}</div>
</div>
<span class="hv-ring"></span><span class="hv-key">⌘V</span>{CURSOR}</div>
{maya_device()}
{msg}
</div>'''


STEP_IC = ['prompt', 'link', 'chart']


def hero():
    made = COPY['hero.made']
    rot = ''.join(f'<span class="hm-w{" on" if i == 0 else ""}">{e(m)}</span>' for i, m in enumerate(made))
    fine = ''.join(f'<li>{ic("check")}<span data-c="hero.fine.{i}">{e(t)}</span></li>' for i, t in enumerate(COPY['hero.fine']))
    h1s = ''
    for p in ('p1', 'p2', 'p3'):
        lines = ''.join(f'<span class="hm-l">{e(x)}{DOT}</span>' for x in COPY[f'{p}.h1'])
        h1s += f'<h1 class="site-h1 hm-h1" data-p="{p}" data-c="{p}.h1"{" hidden" if p != "p1" else ""}>{lines}</h1>'
    leads = ''.join(f'<span class="hm-lead2" data-p="{p}" data-c="{p}.lead"{" hidden" if p != "p1" else ""}>{e(COPY[p + ".lead"])}</span>' for p in ('p1', 'p2', 'p3'))
    steps = ''.join(f'''<li class="hm-step" data-i="{i}"><span class="hm-bar"><b></b></span><span class="hm-sk">{ic(STEP_IC[i])}<b data-c="steps.{i}.0">{e(a)}</b></span><span class="hm-sd" data-c="steps.{i}.1">{e(d)}</span></li>'''
                    for i, (a, d) in enumerate(COPY['steps']))
    caps = ''.join(f'<span class="hm-cap" data-k="{i}" data-c="cap.{i}">{e(x)}</span>' for i, x in enumerate(COPY['cap']))
    return f'''<section class="hm-hero"><div class="site-wrap">
<div class="hm-top">
  <div class="hm-tl">{h1s}</div>
  <div class="hm-tr"><p class="site-lead hm-lead"><span class="hm-made"><span data-c="hero.made.a">{e(COPY['hero.made.a'])}</span> <span class="hm-rot" data-c="hero.made">{rot}</span>.</span> {leads}</p>
    <div class="hm-act"><div class="hm-ctas">{gbtn_ink('hero.cta1', 'md')}{gbtn_clear('hero.cta2', 'md', '../site/pricing.html')}</div>
    <ul class="hm-fine">{fine}</ul></div></div>
</div>
<div class="hm-stage" tabindex="0" role="img" aria-roledescription="animation" aria-label="{e(COPY['hero.aria'])}">
  <div class="hm-caps" aria-hidden="true">{caps}</div>
  <div class="hm-view">{stage()}</div>
</div>
<ol class="hm-steps" aria-label="Publish, Test, Review">{steps}</ol>
</div></section>'''


# ================================================================ section visuals (subtle, targeted loops)
def crop(inner, w, h, x, y, cw, ch, cls=''):
    """Show the (x, y, cw, ch) part of a native w x h render, scaled to its box."""
    return f'<div class="cr {cls}" data-cw="{cw}" data-ch="{ch}" style="aspect-ratio:{cw}/{ch}"><div class="cr-in" data-x="{x}" data-y="{y}" style="width:{w}px;height:{h}px;left:0;top:0">{inner}</div></div>'


def vis_publish():
    pp = mk.prompt_page().replace('Waiting for your chat', '<span class="v-wait">Waiting for your chat</span>')
    return f'''<div class="vis v-pub">
  <div class="v-card v-app">{crop(pp, 1440, 660, 520, 92, 860, 470)}</div>
  <div class="v-card v-cl"><div class="cl-mini"><div class="cl-head">{CL_LOGO}Claude</div>
    <div class="cl-inp"><span class="cl-ph">Reply to Claude</span><span class="cl-paste">{e(COPY['st.prompt'])}</span><span class="cl-send">{ic('up')}</span></div>
    <div class="cl-tool cl-used">{ic('check')}Used the Aero API · publish</div></div></div>
  <div class="v-card v-done">{scaled(prompt_done(), 560, 230, 'v-dn')}</div>
</div>'''


def vis_test():
    ts = test_setup()
    start = mk.tester_start()
    return f'''<div class="vis v-tst">
  <div class="v-card v-link">{crop(ts, 1440, 900, 1032, 120, 392, 150)}</div>
  <div class="v-bub"><div class="st-bub">{e(COPY['st.msg'])}</div></div>
  <div class="v-card v-tw">{scaled(start, 1440, 760, 'v-t1')}{scaled(tester_screen(), 1440, 760, 'v-t2')}</div>
</div>'''


def vis_review():
    words = 'I thought last month would be right here. Where do I change the month?'.split(' ')
    w = ' '.join(f'<span class="w">{e(x)}</span>' for x in words)
    q = rv.qcard('Maya', 'a', '01:42', '', True, 1.0, 0)
    q = q.replace('<q></q>', f'<q class="v-q">{w}</q>')
    dots = ''.join(f'<span class="v-s"><span class="av {a}">{n[0]}</span><b>{n}</b><span class="mono">{l}</span></span>' for n, a, l in
                   [('Maya', 'a', '03:34'), ('Tom', 'b', '02:58'), ('Priya', 'c', '04:40'), ('Jonas', 'd', '03:55'), ('Ana', 'e', '05:21'), ('Leo', 'f', '03:18')])
    summ = f'''<div class="v-sum"><div class="lbl2">Insights · 6 sessions</div>
<div class="v-iss"><span class="big">1</span><div><b>Last month is hard to find</b>{rv.tag('issue', '', 'major')}</div><span class="v-n"><b>4 of 6</b> testers</span></div>
<div class="v-iss"><span class="big">2</span><div><b>No confirmation after sending</b>{rv.tag('conf')}</div><span class="v-n"><b>3 of 6</b> testers</span></div>
<div class="v-iss"><span class="big">3</span><div><b>Month tabs are small</b>{rv.tag('issue', '', 'minor')}</div><span class="v-n"><b>3 of 6</b> testers</span></div></div>'''
    return f'''<div class="vis v-rev"><div class="v-card v-clip">{q}</div><div class="v-sess">{dots}</div>{summ}</div>'''


def section(p, wash, vis, flip=False):
    facts = ''.join(f'<li>{ic(i)}<span><b data-c="{p}.facts.{k}.1">{e(a)}</b><span data-c="{p}.facts.{k}.2">{e(b)}</span></span></li>' for k, (i, a, b) in enumerate(COPY[p + '.facts']))
    pill = {'pub': 'publish', 'test': 'test', 'rev': 'review'}[p]
    sid = {'pub': 'publish', 'test': 'test', 'rev': 'review'}[p]
    return f'''<section class="hm-sec" id="{sid}"><div class="site-wrap hm-two{" flip" if flip else ""}">
<div class="hm-txt"><span class="pill pill-{pill}">{ic(STEP_IC[['pub', 'test', 'rev'].index(p)])}<span data-c="{p}.k">{e(COPY[p + '.k'])}</span></span>
<h2 class="site-h2"><span data-c="{p}.h2">{e(COPY[p + '.h2'])}</span>{DOT}</h2>{c(p + '.body', 'p', 'site-body hm-b1')}{c(p + '.more', 'p', 'site-body hm-b2')}
<ul class="hm-facts">{facts}</ul></div>
<div class="hm-img site-band {wash}">{vis}</div></div></section>'''


def figmafolio():
    it = ''.join(f'<li>{ic(i)}<b data-c="ff.items.{k}.1">{e(a)}</b><span data-c="ff.items.{k}.2">{e(b)}</span></li>' for k, (i, a, b) in enumerate(COPY['ff.items']))
    return f'''<section class="hm-ff"><div class="site-wrap"><div class="hm-ffin"><div class="hm-ffh"><span class="site-eyebrow" data-c="ff.k">{e(COPY['ff.k'])}</span><p data-c="ff.h">{e(COPY['ff.h'])}</p></div><ul>{it}</ul></div></div></section>'''


def usecases():
    cards = ''.join(f'''<article class="hm-uc"><div class="hm-uct">{ic(i)}<span class="site-ex" data-c="uc.items.{k}.3">{e(r)}</span></div><h3 class="site-h3" data-c="uc.items.{k}.1">{e(t)}</h3><p data-c="uc.items.{k}.2">{e(d)}</p></article>'''
                    for k, (i, t, d, r) in enumerate(COPY['uc.items']))
    return f'''<section class="hm-sec hm-ucs" id="use-cases"><div class="site-wrap">
<div class="hm-head"><span class="site-eyebrow" data-c="uc.k">{e(COPY['uc.k'])}</span><h2 class="site-h2"><span data-c="uc.h2">{e(COPY['uc.h2'])}</span>{DOT}</h2>{c('uc.body', 'p', 'site-body')}</div>
<div class="hm-ucg">{cards}</div></div></section>'''


def cell(v):
    if v == 'yes':
        return f'<span class="yes">{ic("check")}<span class="sr">Yes</span></span>'
    if v.startswith('yes · '):
        return f'<span class="yes">{ic("check")}<span class="sr">Yes</span></span><span>{e(v[6:])}</span>'
    if v == 'no':
        return '<span class="no">No</span>'
    if v.startswith('no · '):
        return f'<span class="no">No</span> <span class="mutd">{e(v[5:])}</span>'
    return e(v)


def pricing():
    cols = COPY['pr.cols']
    n = COPY['pr.us']
    us = lambda i: (' class="us us-l"' if i == n - 1 else ' class="us"') if i < n else ''
    head = '<tr><th scope="col"><span class="sr">Plan</span></th>' + ''.join(f'<th scope="col"{us(i)}>{e(x)}</th>' for i, x in enumerate(cols)) + '</tr>'
    rows = ''.join('<tr><th scope="row">' + e(l) + '</th>' + ''.join(f'<td{us(i)}>{cell(v)}</td>' for i, v in enumerate(vs)) + '</tr>' for l, vs in COPY['pr.rows'])
    notes = ''.join(f'<li>{e(n)}</li>' for n in COPY['pr.notes'])
    plans = ''.join(f'<div class="hm-pl"><b>{e(n)}</b><span class="hm-pp">{e(p)}</span><small>{e(d)}</small></div>' for n, p, d in COPY['pr.plans'])
    return f'''<section class="hm-sec hm-price" id="pricing"><div class="site-wrap">
<div class="hm-head hm-head2"><div><span class="site-eyebrow" data-c="pr.k">{e(COPY['pr.k'])}</span><h2 class="site-h2"><span data-c="pr.h2">{e(COPY['pr.h2'])}</span>{DOT}</h2></div>{c('pr.body', 'p', 'site-body')}</div>
<div class="hm-tblw"><table class="hm-tbl"><thead>{head}</thead><tbody>{rows}</tbody></table></div>
<div class="hm-pfoot"><div class="hm-plans">{plans}</div><a class="btn md ink" href="../site/pricing.html">{c('pr.link')}{ic('arrow')}</a></div>
<ol class="hm-notes">{notes}</ol></div></section>'''


def faq():
    items = ''.join(f'<details><summary data-c="faq.items.{i}.0">{e(q)}</summary><p data-c="faq.items.{i}.1">{e(a)}</p></details>' for i, (q, a) in enumerate(COPY['faq.items']))
    return f'''<section class="hm-sec hm-faq" id="faq"><div class="site-wrap hm-faqg">
<div class="hm-faqh"><span class="site-eyebrow" data-c="faq.k">{e(COPY['faq.k'])}</span><h2 class="site-h2"><span data-c="faq.h2">{e(COPY['faq.h2'])}</span>{DOT}</h2></div>
<div class="hm-faql">{items}</div></div></section>'''


def close():
    return f'''<section class="hm-close-s"><div class="site-wrap"><div class="hm-close w-hero"><div><h2 class="site-h2"><span data-c="close.h2">{e(COPY['close.h2'])}</span>{DOT}</h2>{c('close.p', 'p', 'site-lead')}</div>
<div class="hm-ctas">{gbtn_ink('hero.cta1', 'lg')}{gbtn_clear('hero.cta2', 'lg', '../site/pricing.html')}</div></div></div></section>'''


def nav():
    links = ''.join(f'<a href="{h}" data-c="nav.{i}">{e(t)}</a>' for i, (t, h) in enumerate(zip(COPY['nav'], NAV_HREF)))
    return f'''<header class="site-nav"><div class="site-wrap site-nav-in">
<a class="site-logo" href="home.html" aria-label="Aero home">{LOCKUP}</a>
<nav class="site-menu" id="site-menu" aria-label="Main">{links}<a class="site-menu-login" href="#" data-c="nav.login">{e(COPY['nav.login'])}</a></nav>
<div class="site-nav-r"><a class="btn g3 sm site-login" href="#" data-glass-v3="secondary">{c('nav.login')}</a><a class="btn g3 sm" href="#" {GLASS_INK}>{c('nav.start')}</a>
<button class="site-burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="site-menu"><i></i><i></i></button></div></div></header>'''


def footer():
    cols = ''.join(f'<div><h4>{e(h)}</h4><ul>' + ''.join(f'<li><a href="#">{e(x)}</a></li>' for x in xs) + '</ul></div>' for h, xs in COPY['foot.cols'])
    return f'''<footer class="site-foot"><div class="site-wrap"><div class="site-foot-top"><div class="site-foot-brand">{LOCKUP}<p><span data-c="foot.tag">{e(COPY['foot.tag'])}</span>{DOT}</p></div>
<div class="site-foot-cols">{cols}</div></div>
<div class="site-foot-fine"><span>© 2026 Aero</span>{c('foot.fine')}</div></div></footer>'''


def switcher():
    b = ''.join(f'<a href="#p{i + 1}" data-p="p{i + 1}">{i + 1}</a>' for i in range(3))
    return f'<div class="hm-switch" aria-label="Review tool: switch headline">{c("switch.k")}{b}</div>'


def page():
    data = json.dumps(COPY, ensure_ascii=False, indent=1).replace('</', '<\\/')
    body = (hero() + section('pub', 'w-publish', vis_publish()) + section('test', 'w-test', vis_test(), True)
            + section('rev', 'w-review', vis_review()) + usecases() + pricing() + faq() + close())
    return f'''<!doctype html><html lang="en-GB" data-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(COPY['meta.title'])}</title>
<meta name="description" content="{html.escape(COPY['meta.desc'])}">
<!-- COPY: every word on this page, in one block. Edit it here; the page applies it on load. Built by build.py. -->
<script type="application/json" id="copy">
{data}
</script>
<link rel="icon" href="../shared/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@300..600&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../shared/aero.css"><link rel="stylesheet" href="extra.css"><link rel="stylesheet" href="review.css"><link rel="stylesheet" href="home.css"></head>
<body class="site hm">
{nav()}
<main>{body}</main>
{footer()}
{switcher()}
<script>window.GLASS_MODE=window.GLASS_MODE||'subtle';</script><script src="../shared/glass-v3.js"></script>
<script src="home.js"></script></body></html>'''


if __name__ == '__main__':
    out = page()
    text = re.sub(r'<style.*?</style>|style="[^"]*"|<script.*?</script>', '', out, flags=re.S)
    bad = [w for w in ('—', '–', 'claude mcp', 'Watch people use it', 'Same link', 'in seconds', 'color', 'Recorded replay', 'Example session') if w in text]
    (H / 'home.html').write_text(out)
    print('ok', len(out), 'check:', bad or 'clean')
