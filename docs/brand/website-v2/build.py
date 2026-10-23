#!/usr/bin/env python3
"""Aero homepage, rework (23 Oct 2026): round 5 A Studio's structure and scale, drawn with the v3 app UI.
Builds home.html. The app screens are the real v3 components, imported from ../v3/make/build.py and
../v3/review/build.py (read only). All words people read on the page live in COPY below; the same block is
embedded at the top of home.html as JSON, so a word can be changed there without rebuilding."""
import html, importlib.util, json, pathlib, re

H = pathlib.Path(__file__).resolve().parent
V3 = H.parent / 'v3'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


mk = load('v3make', V3 / 'make/build.py')
rv = load('v3review', V3 / 'review/build.py')

# ================================================================ COPY: every word on the page
COPY = {
    'nav.product': 'Product', 'nav.how': 'How it works', 'nav.pricing': 'Pricing', 'nav.guides': 'Guides', 'nav.faq': 'FAQ',
    'nav.signin': 'Sign in', 'nav.start': 'Start free',

    'hero.eyebrow': 'Prototype hosting and user testing',
    'hero.h1.a': 'Publish your',
    'hero.h1.made': ['Claude artifact', 'Figma prototype', 'Lovable app', 'HTML site'],
    'hero.h1.b': 'Watch people use it',
    'hero.lead': 'Put what you made online, share one link, and watch real people use it. Their screen and their voice, transcribed for you.',
    'hero.cta1': 'Start free', 'hero.cta2': 'See a test',
    'hero.fine': ['Free to start', 'From $3 a month', 'No call, no contract'],
    'hero.cap': 'Example session: Pocket, a payments app. Maya, thinking aloud.',
    'hero.replay': 'Recorded replay',

    'proof.1.h': 'Live in a minute, however you made it.', 'proof.1.p': 'One prompt into the chat where you built it, a Figma link, or an HTML file or zip.',
    'proof.2.h': 'Their screen and their voice.', 'proof.2.p': 'Testers open one link on their own computer. No account, no webcam.',
    'proof.3.h': 'Priced for one designer.', 'proof.3.p': 'Free to start, recordings included. Paid plans from $3 a month.',

    'pub.num': '01', 'pub.k': 'Publish',
    'pub.h2': 'One prompt and it’s live.',
    'pub.body': 'Built it in Claude or ChatGPT? Aero gives you one prompt. Copy it into the chat where you built it and it publishes there and then. Or paste a Figma prototype link, or drop an HTML file or zip.',
    'pub.f1.b': 'A prompt, nothing to install.', 'pub.f1.t': 'Copy it into your chat; this page updates when the site is live.',
    'pub.f2.b': 'Figma link or HTML.', 'pub.f2.t': 'Paste the prototype link, or drop a file, folder or zip.',
    'pub.f3.b': 'Every version kept.', 'pub.f3.t': 'Publish again to the same address and roll back any time.',
    'pub.capA': 'In Aero: copy one prompt', 'pub.capB': 'A minute later: its page in Aero',

    'test.num': '02', 'test.k': 'Test',
    'test.h2': 'One link. Their screen and their voice.',
    'test.body': 'Every site comes with a test link. Send it to a client, a friend or a classmate. They open it on their own computer, say their first name if they like, and follow the tasks you set while they think aloud.',
    'test.f1.b': 'No account', 'test.f1.t': 'for testers. Only this tab and their voice are recorded.',
    'test.f2.b': 'Optional tasks,', 'test.f2.t': 'in a small panel they can move out of the way.',
    'test.f3.b': 'Try it yourself first.', 'test.f3.t': '“Preview as tester” is free and stays out of your results.',
    'test.capA': 'Your side: the test link', 'test.capB': 'Their side: their own computer',

    'rev.num': '03', 'rev.k': 'Review',
    'rev.h2': 'What to fix, in their own words.',
    'rev.body': 'About a minute after each session, the transcript and a summary are ready. Insights puts every session together: what to fix first, how many testers hit it, and the quotes, each one playing the moment it was said.',
    'rev.f1.b': '“4 of 6 testers”,', 'rev.f1.t': 'ranked by how serious it is, then by how many.',
    'rev.f2.b': 'Quotes you can play.', 'rev.f2.t': 'Each one opens the recording at that moment.',
    'rev.f3.b': 'No notes to take.', 'rev.f3.t': 'Read a session like an article, or copy it all as a table.',
    'rev.capA': 'Insights: every session together', 'rev.capB': 'One session, to read',

    'fast.num': '04', 'fast.k': 'Prompt to first session',
    'fast.h2': 'From prompt to first session.',
    'fast.body': 'One prompt to publish, one link to share. The rest is the tester’s time, not yours.',
    'fast.steps': [['00:00', 'You copy one prompt', 'Into the chat where you built it.'], ['00:50', 'It’s live', 'pocket.aeroapp.ai, with its page in Aero.'],
                   ['01:30', 'Link sent', 'To a friend, in a message.'], ['09:10', 'First session ends', 'Seven minutes of screen and voice.'],
                   ['10:10', 'Transcript ready', 'With the friction points, in their words.']],
    'fast.note': 'Example timings from one test. Yours depend on the build and the tester.',

    'price.num': '05', 'price.k': 'Price',
    'price.h2': 'Priced for one designer.',
    'price.body': 'Free to start, recordings included. Every paid plan has a 7-day free trial. Monthly, no call, no contract, cancel any time.',
    'price.plans': [
        ['Free', '$0', '', ['3 test sessions', 'Recordings included', 'Sites stay live for 7 days'], 'Start free', ''],
        ['Basic', '$3', '/month', ['5 test sessions', 'Your own aeroapp.ai address', 'Password protection', 'Custom favicon, no Aero badge'], 'Try Basic free', '7-day free trial'],
        ['Solo', '$6', '/month', ['10 test sessions', 'Everything in Basic', 'Custom domain', 'Site analytics'], 'Try Solo free', '7-day free trial'],
        ['Pro', '$19', '/month', ['20 test sessions', 'Everything in Solo', 'Priority support'], 'Try Pro free', '7-day free trial'],
    ],
    'price.foot': 'Prices in USD. Regional prices are shown at checkout.', 'price.compare': 'Compare plans',

    'who.num': '06', 'who.k': 'Who it’s for',
    'who.h2': 'For people who make things.',
    'who.body': 'Designers, researchers, PMs, founders and students. And anyone who made something and has nowhere to put it.',
    'who.items': [['UI and product designers', 'Test a Figma flow before the handoff, not after.'], ['UX researchers', 'Quick think-aloud sessions, with the transcripts kept for you.'],
                  ['PMs and founders', 'Put a build from Claude or Lovable in front of real people before you ship it.'], ['Students', 'Host your coursework and test it with classmates.']],

    'faq.num': '07', 'faq.k': 'Questions', 'faq.h2': 'Asked often.',
    'faq.items': [
        ['Do my testers need an account?', 'No. They open the link on their own computer and start. You choose who gets it: a client, a friend, a classmate.'],
        ['What exactly is recorded?', 'The browser tab with your prototype and the tester’s voice as they think aloud. Not their camera and not their other tabs, so you see what they did and hear what they said.'],
        ['How does the prompt publish my site?', 'Aero gives you one prompt with a key in it. You copy it into the Claude or ChatGPT chat where you built the thing, and it sends the files to Aero. There is nothing to install or connect.'],
        ['How soon is the transcript ready?', 'About a minute after each session ends. It follows the recording, with a short summary and the friction points quoted in the tester’s own words.'],
        ['Can I try a test myself first?', 'Yes. “Preview as tester” runs the test as a tester would. It is free, shows as You, and stays out of Insights.'],
        ['What do I get for free?', '3 test sessions with recordings included, and sites that stay live for 7 days. Paid plans start at $3 a month with a 7-day free trial, monthly, no call, no contract.'],
    ],

    'close.h2': 'Put it online. Hear what they think', 'close.p': 'Free to start. From $3 a month. No call, no contract.',
    'foot.tag': 'Publish your prototype. Watch people use it.',
    'foot.cols': [['Product', ['Publish', 'Test', 'Review', 'Pricing']], ['Guides', ['Test a Claude artifact', 'Test a Figma prototype', 'Host an HTML build']], ['Company', ['About', 'Privacy', 'Terms']]],
    'foot.fine': 'Every name, session and number shown on this page is an example.',
}


def c(key, tag='span', cls='', raw=None):
    """Render a piece of copy with its key, so the JSON block can replace it at load."""
    v = COPY[key] if raw is None else raw
    k = f' class="{cls}"' if cls else ''
    return f'<{tag}{k} data-c="{key}">{html.escape(v, quote=False)}</{tag}>'


ic = mk.ic


def hbtn(key, kind='primary', href='#'):
    if kind == 'primary':
        a = 'data-glass-v3="primary" data-fill="#1D1D1F"'
    else:
        a = 'data-glass-v3="secondary"'
    return f'<a class="btn g3 lg h-btn" href="{href}" {a}>{c(key)}</a>'


# ================================================================ app screens (real v3 components)
def shot(inner, w, h, cls='', m=None, label=''):
    """A real 1440-wide app window, scaled to fit its column. h = how much of it shows (native px).
    m = (width, x, y, height) of the part to show on a phone (native px); defaults to the whole thing."""
    mw, mx, my, mh = m or (w, 0, 0, h)
    al = f' role="img" aria-label="{html.escape(label)}"' if label else ''
    return (f'<div class="shot {cls}" data-w="{w}" data-h="{h}" data-mw="{mw}" data-mx="{mx}" data-my="{my}" data-mh="{mh}"'
            f' style="aspect-ratio:{w}/{h}"{al}><div class="shot-in" style="width:{w}px">{inner}</div></div>')


def hero_window():
    """v3 Watch view, light: Maya's recorded tab, the timeline with task regions, the follow-along transcript."""
    w = rv.s2_window()
    w = w.replace('<span class="m issue hot"', '<span class="m issue"')  # the loop lights friction points itself
    w = w.replace('1x<svg', '2x<svg', 1)  # the loop plays at 2x
    return w


def publish_a():
    return mk.prompt_page()


def publish_b():
    """The site's page in Aero, straight after publishing, for Pocket (the prompt's site)."""
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
        out = mk.site_page(just=True)
    finally:
        mk.thumb, mk.window = real_thumb, real_window
    return out


def test_a():
    """Test setup with the link, for the Pocket test the tester is about to open."""
    real_thumb = mk.thumb

    def thumb(kind, w, h, scale=None, cls='', sheet=False, top=None):
        if kind == 'checkout':
            return real_thumb('pocket', w, h, .2, cls, sheet, '4%')
        return real_thumb(kind, w, h, scale, cls, sheet, top)

    mk.thumb = thumb
    try:
        out = mk.test_setup()
    finally:
        mk.thumb = real_thumb
    for a, b in [('Add the linen tote to your basket and check out.', 'Send £20 to Sam.'), ('Use any card details; nothing is charged.', 'Sam is already in your contacts.'),
                 ('Change delivery to next day.', 'Find out how much you spent on eating out last month.'), ('Find out how to return an item.', 'Freeze your debit card.'),
                 ('This is an early checkout for Paper &amp; Co.', 'This is an early version of Pocket, a payments app.'),
                 ('aeroapp.ai/t/checkout-4mq', 'aeroapp.ai/t/pocket-7k2'), ('checkout.aeroapp.ai', 'pocket.aeroapp.ai'),
                 ('aeroapp.ai/tests/checkout/setup', 'aeroapp.ai/tests/pocket/setup'), ('<b>Checkout</b></span>', '<b>Pocket</b></span>'),
                 ('x-in">Checkout<', 'x-in">Pocket<'), ('test.kestrel.studio', 'test.pocket.money')]:
        out = out.replace(a, b)
    out = out.replace('sidebar-placeholder', '')
    # the recent tests list: Pocket is the open one
    out = out.replace('<div class="sb-si on"><span class="sb-st "></span><span class="sb-nm">Checkout</span>', '<div class="sb-si"><span class="sb-st "></span><span class="sb-nm">Checkout</span>')
    out = out.replace('<div class="sb-si "><span class="sb-st new"></span><span class="sb-nm">Pocket</span>', '<div class="sb-si on"><span class="sb-st new"></span><span class="sb-nm">Pocket</span>')
    return out


def test_b():
    return mk.tester_task('home')


def review_a():
    """Insights for Pocket: the summary, what to fix first ranked with '4 of 6 testers' and quotes you can play."""
    summ = '''<div class="sumcard2"><div class="lbl2">Summary <span>· 6 sessions with audio · updated Thu 18:06</span><span class="r"><span class="dotload"></span> Ines’s session joins in about a minute</span></div>
<p>Everyone sent money to Sam without help. Finding cards was the problem: <b>4 of 6 testers</b> looked on the home screen first, and Ana gave up. Three tried tapping the balance. Fix first: put cards on the home screen.</p></div>'''
    issues = rv.issue_item(1, 'Cards are hidden under More', 'issue', 'major', ['Maya', 'Jonas', 'Ana', 'Leo'],
                           'Testers expected cards on the home screen, near the balance. They found them under More after one to four minutes.',
                           [('Maya', 'a', '03:08', 'I thought my cards would be on the home screen. Is it under More?', True, 1.0, .45), ('Jonas', 'd', '01:52', 'Where are my cards? I’ve tapped everything on this screen.', False, 1.4), ('Leo', 'f', '02:30', 'More is a funny place for cards.', False, .8)],
                           '<span class="lnk blue more">Ana’s moment, and 2 more clips</span>')
    issues += rv.issue_item(2, 'Send has no back label', 'issue', 'minor', ['Maya', 'Tom', 'Leo'], 'An arrow alone; three testers stopped to work out how to leave Send.',
                            [('Maya', 'a', '02:41', 'There’s an arrow but it doesn’t say where to.', False, 1.2), ('Tom', 'b', '01:10', 'Is that back, or close?', False, .9)])
    issues += rv.issue_item(3, 'Balance looks tappable', 'conf', None, ['Maya', 'Jonas', 'Ana'], 'Testers tapped the balance expecting details or cards.',
                            [('Ana', 'e', '00:48', 'The balance looks like a button. Nothing happens.', False, 1.1)])
    lst = f'''<div class="blk"><div class="bh"><h3>What to fix first</h3><span class="seg"><span class="on">By priority</span><span>By task</span><span>By theme</span></span>
<span class="r">{rv.gbtn('Copy as table', 'table')}{rv.btn('Download report', icon='down')}</span></div>
<div class="lbl2" style="margin:-4px 0 6px">Issues by severity first (Critical, Major, Minor), then by how many testers hit them. Every quote plays the moment.</div>{issues}</div>'''
    tg = rv.tag
    aside = f'''<aside class="ins-side">
<div class="blk2"><div class="lbl2">Confidence</div><p class="conf"><b>Medium.</b> 6 sessions with audio. Patterns hold from 3; from 10 they are steady.</p></div>
<div class="blk2"><div class="lbl2">What worked</div>
<div class="wk">{tg('good')}<span>Sending money felt familiar</span><span class="mono">6 of 6</span></div>
<div class="wk">{tg('good')}<span>Freezing a card is clear</span><span class="mono">4 of 6</span></div>
<div class="wk">{tg('good')}<span>Big keypad for the amount</span><span class="mono">3 of 6</span></div></div>
<div class="blk2"><div class="lbl2">In this summary <span class="r">open a session</span></div>
{''.join(f'<div class="sl"><span class="av {a}">{n[0]}</span>{n}<span class="mono r">{l}</span></div>' for n, a, l in [('Maya', 'a', '07:12'), ('Tom', 'b', '03:58'), ('Priya', 'c', '05:40'), ('Jonas', 'd', '04:55'), ('Ana', 'e', '06:21'), ('Leo', 'f', '05:18')])}
<div class="sl dim"><span class="av m">Y</span>You<span class="mono r">left out</span></div></div>
<div class="how"><b>How this was made.</b> Each session is transcribed and summarised about a minute after it ends. This page groups what came up in more than one session and links every quote to its moment.</div></aside>'''
    main = rv.testhead(tab='Insights') + f'<div class="insights"><div class="ins-main">{summ}{lst}</div>{aside}</div>'
    return rv.window('aeroapp.ai/tests/pocket/insights', rv.sidebar(), main, h=1240)


def review_b():
    return rv.s3_window()


# ================================================================ page parts
def facts(items):
    return '<ul class="h-facts">' + ''.join(f'<li>{ic(i)}<span>{c(b, "b")} {c(t)}</span></li>' for i, b, t in items) + '</ul>'


def sec_head(p, facts_items):
    return f'''<div class="h-sh"><span class="h-num"><b data-c="{p}.num">{COPY[p + '.num']}</b> <span data-c="{p}.k">{html.escape(COPY[p + '.k'])}</span></span></div>
<div class="h-head"><h2 data-c="{p}.h2">{html.escape(COPY[p + '.h2'])}</h2><div>{c(p + '.body', 'p', 'h-body')}{facts(facts_items)}</div></div>'''


def comp(wash, a, b, capA, capB, labelA, labelB, ov=12):
    return f'''<div class="h-panel {wash}" style="--ov:{ov}%"><div class="h-comp">
<div class="h-a"><div class="h-cap"><span class="h-n">1</span>{c(capA)}</div>{a}</div>
<div class="h-b"><div class="h-cap"><span class="h-n">2</span>{c(capB)}</div>{b}</div></div>
<p class="h-ex">Example screens from the Aero app. Names and numbers are examples.</p></div>'''


NAV = f'''<header class="h-nav"><div class="wrap"><a href="#" class="h-logo" aria-label="Aero home">{mk.LOCKUP('lockup')}</a>
<nav class="h-nav-l"><a href="#publish">{c('nav.product')}</a><a href="#test">{c('nav.how')}</a><a href="#price">{c('nav.pricing')}</a><a href="#">{c('nav.guides')}</a><a href="#faq">{c('nav.faq')}</a></nav>
<div class="h-nav-r"><a class="h-si" href="#">{c('nav.signin')}</a><a class="btn g3 sm" href="#" data-glass-v3="primary" data-fill="#1D1D1F">{c('nav.start')}</a></div></div></header>'''


def hero():
    made = COPY['hero.h1.made']
    rot = ''.join(f'<span class="h-w{" on" if i == 0 else ""}">{html.escape(m)}</span>' for i, m in enumerate(made))
    fine = ''.join(f'<span>{ic("check")}<span data-c="hero.fine.{i}">{html.escape(t)}</span></span>' for i, t in enumerate(COPY['hero.fine']))
    proofs = ''.join(f'<div>{ic(k)}{c(f"proof.{n}.h", "b")}{c(f"proof.{n}.p", "p")}</div>' for n, k in zip((1, 2, 3), ('prompt', 'tab', 'check')))
    win = hero_window()
    return f'''<section class="h-hero"><div class="wrap">
<div class="h-top">
  <div><p class="h-eyebrow"><span class="d"></span>{c('hero.eyebrow')}</p>
  <h1 aria-label="Publish your {made[0]}, {made[1]}, {made[2]} or {made[3]}. Watch people use it."><span aria-hidden="true">{c('hero.h1.a')}<br><span class="h-rot" data-c="hero.h1.made">{rot}</span><span class="h-dot0">.</span><br>{c('hero.h1.b')}<span class="dot">.</span></span></h1></div>
  <div class="h-side">{c('hero.lead', 'p', 'h-lead')}
    <div class="h-ctas">{hbtn('hero.cta1')}{hbtn('hero.cta2', 'secondary', '#review')}</div>
    <p class="h-fine">{fine}</p></div>
</div>
<div class="h-stage w-hero"><div class="h-scap"><span class="d"></span>{c('hero.cap')}<span class="h-rep">{c('hero.replay')}</span></div>
  <div class="h-tilt">{shot(win, 1440, 900, 'hero-shot', (520, 0, 0, 902), 'An Aero session being reviewed: the recorded tab, the timeline and the transcript following along')}</div></div>
<div class="h-proofs">{proofs}</div>
</div></section>'''


def sections():
    pub = sec_head('pub', [('prompt', 'pub.f1.b', 'pub.f1.t'), ('link', 'pub.f2.b', 'pub.f2.t'), ('undo', 'pub.f3.b', 'pub.f3.t')])
    pub += comp('w-publish', shot(publish_a(), 1440, 660, '', (800, 535, 36, 560), 'Aero create flow: copy one prompt into your chat'),
                shot(publish_b(), 1440, 900, '', (760, 236, 36, 560), 'The published site’s page in Aero'), 'pub.capA', 'pub.capB', '', '', 6)
    tst = sec_head('test', [('lock', 'test.f1.b', 'test.f1.t'), ('check', 'test.f2.b', 'test.f2.t'), ('ext', 'test.f3.b', 'test.f3.t')])
    tst += comp('w-test', shot(test_a(), 1440, 900, '', (380, 1056, 80, 360), 'Aero test setup with the test link'),
                shot(test_b(), 1440, 760, '', (900, 540, 280, 480), 'The tester’s screen: the task panel over the prototype'), 'test.capA', 'test.capB', '', '', 16)
    rvw = sec_head('rev', [('chart', 'rev.f1.b', 'rev.f1.t'), ('play', 'rev.f2.b', 'rev.f2.t'), ('book', 'rev.f3.b', 'rev.f3.t')])
    rvw += comp('w-review', shot(review_a(), 1440, 1240, '', (830, 256, 140, 900), 'Aero Insights: what to fix first, 4 of 6 testers, quotes you can play'),
                shot(review_b(), 1440, 900, '', (900, 56, 36, 520), 'One session in the Read view'), 'rev.capA', 'rev.capB', '', '', 30)

    steps = ''.join(f'<div class="h-st"><div class="tm">{t}</div><div class="h-pt"></div><b>{html.escape(a)}</b><p>{html.escape(b)}</p></div>' for t, a, b in COPY['fast.steps'])
    plans = ''
    for n, p, u, f, cta, tr in COPY['price.plans']:
        li = ''.join(f'<li>{ic("check")}{html.escape(x)}</li>' for x in f)
        mid = ' mid' if n == 'Solo' else ''
        kind = 'primary' if n == 'Solo' else 'secondary'
        fill = ' data-fill="#1D1D1F"' if kind == 'primary' else ''
        plans += f'''<div class="h-plan{mid}"><div class="pn"><b>{n}</b><span class="lbl">{tr}</span></div><div class="pr">{p}<small>{u}</small></div><ul>{li}</ul>
<a class="btn g3 md" href="#" data-glass-v3="{kind}"{fill}>{html.escape(cta)}</a></div>'''
    whoi = ['site', 'test', 'arrow', 'book']
    who = ''.join(f'<div class="h-who-i">{ic(k)}<b>{html.escape(a)}</b><p>{html.escape(b)}</p></div>' for k, (a, b) in zip(whoi, COPY['who.items']))
    faq = ''.join(f'<details{" open" if i == 0 else ""}><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>' for i, (q, a) in enumerate(COPY['faq.items']))
    return f'''
<section class="h-sec" id="publish"><div class="wrap">{pub}</div></section>
<section class="h-sec" id="test"><div class="wrap">{tst}</div></section>
<section class="h-sec" id="review"><div class="wrap">{rvw}</div></section>

<section class="h-sec" id="fast"><div class="wrap">
  <div class="h-sh"><span class="h-num"><b>{COPY['fast.num']}</b> {c('fast.k')}</span></div>
  <div class="h-head h-end"><h2 data-c="fast.h2">{COPY['fast.h2']}</h2>{c('fast.body', 'p', 'h-body')}</div>
  <div class="h-tlx" data-c="fast.steps"><span class="prog"></span>{steps}</div>
  {c('fast.note', 'p', 'lbl h-tlnote')}
</div></section>

<section class="h-sec" id="price"><div class="wrap">
  <div class="h-sh"><span class="h-num"><b>{COPY['price.num']}</b> {c('price.k')}</span></div>
  <div class="h-head h-end"><h2 data-c="price.h2">{COPY['price.h2']}</h2>{c('price.body', 'p', 'h-body')}</div>
  <div class="h-plans" data-c="price.plans">{plans}</div>
  <div class="h-pfoot">{c('price.foot', 'span', 'lbl')}<a class="lbl" href="#">{c('price.compare')} {ic('arrow')}</a></div>
</div></section>

<section class="h-sec" id="who"><div class="wrap">
  <div class="h-sh"><span class="h-num"><b>{COPY['who.num']}</b> {c('who.k')}</span></div>
  <div class="h-head h-end"><h2 data-c="who.h2">{COPY['who.h2']}</h2>{c('who.body', 'p', 'h-body')}</div>
  <div class="h-who" data-c="who.items">{who}</div>
</div></section>

<section class="h-sec" id="faq"><div class="wrap h-faq">
  <div><div class="h-sh"><span class="h-num"><b>{COPY['faq.num']}</b> {c('faq.k')}</span></div><h2 data-c="faq.h2">{COPY['faq.h2']}</h2></div>
  <div data-c="faq.items">{faq}</div>
</div></section>

<div class="wrap"><div class="h-close w-hero"><div><h2><span data-c="close.h2">{COPY['close.h2']}</span><span class="dot">.</span></h2>{c('close.p', 'p')}</div>
<div class="h-ctas">{hbtn('hero.cta1')}{hbtn('hero.cta2', 'secondary', '#review')}</div></div></div>'''


def footer():
    cols = ''.join(f'<div><h4>{h}</h4><ul>' + ''.join(f'<li><a href="#">{html.escape(x)}</a></li>' for x in xs) + '</ul></div>' for h, xs in COPY['foot.cols'])
    return f'''<footer class="h-foot"><div class="wrap"><div>{mk.LOCKUP('lockup')}{c('foot.tag', 'p')}</div>{cols}
<div class="h-fine2"><span>© 2026 Aero</span>{c('foot.fine')}</div></div></footer>'''


def page():
    js = (H / 'home.js').read_text()
    data = json.dumps(COPY, ensure_ascii=False, indent=1).replace('</', '<\\/')
    return f'''<!doctype html><html lang="en-GB" data-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Aero: publish your prototype, watch people use it</title>
<meta name="description" content="Publish a Claude artifact, Figma prototype, Lovable app or HTML site, share one link, and watch real people use it. Their screen and their voice, transcribed for you.">
<!-- COPY: every word on this page, in one block. Edit it here; the page reads it on load. Built from build.py. -->
<script type="application/json" id="copy">
{data}
</script>
<link rel="icon" href="favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@300..600&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="aero.css"><link rel="stylesheet" href="extra.css"><link rel="stylesheet" href="review.css"><link rel="stylesheet" href="site.css"></head>
<body class="h-page">
{NAV}
<main>{hero()}{sections()}</main>
{footer()}
<script>window.GLASS_MODE=window.GLASS_MODE||'subtle';</script><script src="glass-v3.js"></script>
<script>{js}</script></body></html>'''


if __name__ == '__main__':
    out = page()
    bad = [w for w in ('—', 'claude mcp', 'connector', 'Starter', 'color', 'Connect Aero') if w in re.sub(r'<style.*?</style>|style="[^"]*"', '', out)]
    (H / 'home.html').write_text(out)
    print('ok', len(out), 'check:', bad or 'clean')
