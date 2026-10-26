"""Builds the glass compare page: python3 build.py
index.html (grid of 4 column iframes) + col-a.html (tester glass, no engine) + col-b/c/d.html (engine with
settings-b/c/d.js). Every column renders the same in-situ rows, rest and held hover."""
import json, pathlib, re, shutil, hashlib
H = pathlib.Path(__file__).resolve().parent
SH = H.parent / 'shared'
shutil.copy(SH / 'glass-v3.js', H / 'glass-v3.js'); shutil.copy(SH / 'aero.css', H / 'aero.css')

def settings_of(js):
    return json.loads(js[js.index('window.GLASS_P = ') + 17:js.rindex(';')])
cur_txt = (SH / 'glass-settings.js').read_text()
CUR = settings_of(cur_txt)
DUANE = json.loads((H.parent / 'glass-panel/saved/duane-2026-10-25.json').read_text())['s']
# Final as of 07:01: the current file before the afternoon changes (bottom light toned down, neutral floor, pickup reach)
C0701 = dict(CUR); C0701.update({'causW': .32, 'causH': .7, 'crestW': .35, 'volW': 1}); C0701.pop('causFloor', None)
for k in ('falloff', 'pickLo', 'pickHi'): C0701.pop(k, None)
COLS = [
    ('b', 'Duane, 25 Oct', 'his first panel settings, 25 Oct morning', DUANE),
    ('c', 'Final, 07:01', 'Final as of the 07:01 feedback', C0701),
    ('d', 'Final, now', 'shared/glass-settings.js as of this build', CUR),
]
for cid, name, sub, s in COLS:
    body = json.dumps(s, indent=1)
    h = hashlib.sha1(json.dumps(s, sort_keys=True).encode()).hexdigest()[:8]
    (H / f'settings-{cid}.js').write_text(f"/* glass compare, column {cid.upper()}: {name} ({sub}) */\nwindow.GLASS_MODE = 'subtle';\nwindow.GLASS_META = {json.dumps({'name': name, 'sub': sub, 'hash': h})};\nwindow.GLASS_P = {body};\n")

LOCK = (H.parent / 'shared/lockup.svg').read_text().replace('fill="#1D1D1F"', 'fill="currentColor"').replace('role="img" aria-label="Aero"', 'aria-hidden="true"')
def ink(size, hov, label='Start free', solid=False, A=False):
    f = ' data-force="hover" data-px=".7" data-py=".3"' if hov else ''
    if A: return f'<span class="btn {size} a-ink">{label}</span>'
    return f'<span class="btn g3 {size}" data-glass-v3="primary" data-fill="{"#1D1D1F" if solid else "rgba(29,29,31,.8)"}"{f}>{label}</span>'
def white(size, hov, label='See pricing', A=False):
    f = ' data-force="hover" data-px=".7" data-py=".3"' if hov else ''
    if A: return f'<span class="btn {size} x-gl a-white">{label}</span>'
    return f'<span class="btn g3 {size}" data-glass-v3="secondary"{f}>{label}</span>'
def gbtn(label, A=False):
    return f'<span class="gbtn{" x-gl a-white btn sm" if A else ""}">{label}</span>'

def rows(A):
    out = []
    def row(title, fn):
        out.append(f'<section class="gc-row"><h3>{title}</h3>' + ''.join(f'<div class="gc-st"><span class="gc-lb">{"Hovered" if hv else "Rest"}</span>{fn(hv)}</div>' for hv in (0, 1)) + '</section>')
    row('White hero', lambda hv: f'<div class="gc-hero"><b>One prompt and it’s live<span class="hd-dot">.</span></b><div class="ctas">{ink("lg", hv, A=A)}{white("lg", hv, A=A)}</div><div class="gc-pqstrip"></div></div>')
    row('Section wash', lambda hv: f'<div class="band w-publish"><span class="pill pill-publish">Publish</span><div class="ctas">{ink("md", hv, A=A)}{white("md", hv, "How it works", A=A)}</div></div>')
    def nav(hv):
        f = ' data-force="hover" data-px=".7" data-py=".3"' if hv else ''
        btns = (f'<span class="btn sm x-gl a-white">Log in</span><span class="btn sm a-ink">Start free</span>' if A else
                f'<span class="btn g3 sm" data-glass-v3="secondary"{f}>Log in</span><span class="btn g3 sm" data-glass-v3="primary" data-fill="rgba(29,29,31,.8)"{f}>Start free</span>')
        return f'<div class="gc-nav"><div class="gc-pqcard">£20.00</div><header class="site-nav"><div class="site-nav-in"><span class="site-logo">{LOCK}</span><div class="site-nav-r">{btns}</div></div></header></div>'
    row('Glass nav over the Pocket screen', nav)
    def tests(hv):
        f = ' data-force="hover" data-px=".7" data-py=".3"' if hv else ''
        pb = gbtn('Preview as tester', A) if not hv or A else '<span class="gbtn" data-hv="1">Preview as tester</span>'
        cp = '<span class="btn sm a-ink">Copy test link</span>' if A else f'<span class="btn g3 sm" data-glass-v3="primary" data-fill="#1D1D1F"{f}>Copy test link</span>'
        return (f'<div class="gc-app"><div class="mhead"><span class="crumb"><b>Pocket</b></span><div class="gc-r2">{pb}{cp}</div></div>'
                f'<div class="gc-appbody"><div class="gc-thumb"><div class="gc-pqmini"><i></i></div></div><div class="gc-meta"><b>Pocket</b><span class="pill pill-test"><span class="gc-dot"></span>Live</span><span class="gc-new">2 new</span></div></div></div>')
    row('App: Tests › Pocket', tests)
    def modal(hv):
        f = ' data-force="hover" data-px=".7" data-py=".3"' if hv else ''
        cn = gbtn('Cancel', A) if not hv or A else '<span class="gbtn" data-hv="1">Cancel</span>'
        st = '<span class="btn sm a-ink">Stop sessions</span>' if A else f'<span class="btn g3 sm" data-glass-v3="primary" data-fill="#1D1D1F"{f}>Stop sessions</span>'
        return f'<div class="modal"><div class="mh">Stop taking new sessions?</div><div class="mb">Sessions you already have are kept.</div><div class="mf">{cn}{st}</div></div>'
    row('App: modal footer', modal)
    def tester(hv):
        f = ' data-force="hover" data-px=".7" data-py=".3"' if hv else ''
        dn = '<span class="btn md a-ink">Done</span>' if A else f'<span class="btn g3 md" data-glass-v3="primary" data-fill="#1D1D1F"{f}>Done</span>'
        return (f'<div class="gc-proto"><div class="x-recchip x-gl"><span class="x-recd"></span>Recording</div><div class="x-tk2"><div class="x-tkn">Task 1 of 2</div>'
                f'<div class="x-tkb"><b>Send £20 to Sam.</b></div><div class="x-tka">{dn}<span class="x-cant">Couldn’t do it</span></div></div></div>')
    row('Tester screen over the prototype', tester)
    def dark(hv):
        f = ' data-force="hover" data-px=".7" data-py=".3"' if hv else ''
        ct = (f'<span class="gbtn x-gl a-white btn sm">Copy as table</span>' if A else (gbtn('Copy as table') if not hv else '<span class="gbtn" data-hv="1">Copy as table</span>'))
        dl = '<span class="btn sm a-ink">Download report</span>' if A else f'<span class="btn g3 sm" data-glass-v3="primary" data-fill="#1D1D1F"{f}>Download report</span>'
        return f'<div class="gc-dark{" tdark" if A else ""}" data-theme="dark"><span class="gc-t">Insights</span><div class="gc-r2">{ct}{dl}</div></div>'
    row('Dark review screen', dark)
    return ''.join(out)

CSS = (H / 'rows.css').read_text()
def page(cid, title, sub):
    A = cid == 'a'
    scripts = '' if A else f'<script src="settings-{cid}.js"></script><script src="glass-v3.js"></script>'
    head = f'<div class="colh"><b>{title}</b><span>{sub}</span><code id="meta">{"no glass engine: CSS from the hero tester screen" if A else ""}</code></div>'
    meta = '' if A else '''<script>(function(){var m=window.GLASS_META||{},s=JSON.stringify(window.GLASS_P||{}),h=2166136261;for(var i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,16777619)>>>0}
document.getElementById('meta').textContent='file '+m.hash+' · live '+('0000000'+h.toString(16)).slice(-8)+' · loaded '+new Date().toLocaleTimeString('en-GB')+' · '+Object.keys(window.GLASS_P||{}).length+' keys';
// hover rows: upgrade the held app secondaries too (they are plain .gbtn in the markup)
document.querySelectorAll('[data-hv]').forEach(function(g){g.setAttribute('data-force','hover');g.setAttribute('data-px','.7');g.setAttribute('data-py','.3');});if(window.GlassV3)GlassV3.init();})();</script>'''
    return f'''<!doctype html>
<html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Glass compare, {title}</title>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@300..600&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="aero.css"><style>{CSS}</style></head>
<body class="site{" colA" if A else ""}">{head}{rows(A)}{scripts}{meta}</body></html>
'''
(H / 'col-a.html').write_text(page('a', 'Tester glass', 'task panel, Recording sign, Done, as in the hero'))
for cid, name, sub, s in COLS: (H / f'col-{cid}.html').write_text(page(cid, name, sub))

IDX = '''<!doctype html>
<html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Aero Glass Compare</title>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@300..600&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{--ink:#1D1D1F;--mut:#6E6E73;--line:#E5E5EA}
html,body{background:#fff}
body{margin:0;font:14px/1.5 Geist,system-ui,sans-serif;color:var(--ink)}
.top{padding:16px 20px 8px}
.top h1{margin:0;font-size:20px;font-weight:500;letter-spacing:-.02em}
.top p{margin:4px 0 0;color:var(--mut);max-width:70em}
.g{display:grid;grid-template-columns:repeat(4,minmax(330px,1fr));gap:10px;padding:10px 20px 40px;overflow-x:auto}
iframe{width:100%;height:2140px;border:1px solid var(--line);border-radius:12px;display:block;background:#fff}
@media (max-width:900px){.top{padding:14px 16px 6px}.g{padding:10px 16px 30px}}
</style></head><body>
<div class="top"><h1>Glass compare</h1><p>The same real markup in every column, at rest and with hover held. A: the tester screen's frosted glass (no engine). B to D: the glass engine with each settings file; the code under each title is that file's hash and the time this page loaded it. Scroll sideways on a phone.</p></div>
<div class="g">
<iframe src="col-a.html" title="A: Tester glass"></iframe>
<iframe src="col-b.html" title="B: Duane, 25 Oct"></iframe>
<iframe src="col-c.html" title="C: Final, 07:01"></iframe>
<iframe src="col-d.html" title="D: Final, now"></iframe>
</div></body></html>
'''
(H / 'index.html').write_text(IDX)
print('built', [c[0] for c in COLS])
