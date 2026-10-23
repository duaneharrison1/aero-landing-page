"""Builds the UI directions board: board/index.html + board/img/*.jpg from shots and notes.json.
python3 build_board.py"""
import json, os, html
from PIL import Image

H = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(H, 'board')
os.makedirs(os.path.join(OUT, 'img'), exist_ok=True)
D = json.load(open(os.path.join(H, 'notes.json')))
e = html.escape


def img(src, name, w=1280):
    p = os.path.join(H, src)
    if not os.path.exists(p):
        return None
    im = Image.open(p).convert('RGB')
    if im.width > w:
        im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
    dst = f'img/{name}.jpg'
    im.save(os.path.join(OUT, dst), quality=74, optimize=True, progressive=True)
    return dst, im.width, im.height


def ul(items, cls):
    if not items:
        return ''
    return f'<ul class="{cls}">' + ''.join(f'<li>{e(i)}</li>' for i in items) + '</ul>'


def tile(sec, t):
    shots = []
    for i, s in enumerate(t.get('img', [])):
        cap = ''
        if isinstance(s, list):
            s, cap = s
        r = img(s, f"{sec['id']}-{t.get('vkey', t['key'])}-{i}")
        if r:
            shots.append(r + (cap,))
    if not shots:
        pics = '<div class="noimg">Not drawn in this direction</div>'
    else:
        pics = ''.join(f'<figure>{f"<figcaption>{e(c)}</figcaption>" if c else ""}<button class="shot" data-full="{s}" aria-label="Open full size"><img src="{s}" width="{w}" height="{h}" loading="lazy" alt="{e(t["label"])}, {e(sec["title"])}"></button></figure>' for s, w, h, c in shots)
    vid = f"{sec['id']}-{t.get('vkey', t['key'])}"
    return f'''<article class="tile" data-k="{t['key']}" id="t-{vid}">
  <header><span class="tk tk-{t['key']}">{e(t['key'])}</span><h3>{e(t['label'])}</h3></header>
  <div class="pics">{pics}</div>
  <div class="talk">
    {f'<p class="idea">{e(t["idea"])}</p>' if t.get('idea') else ''}
    <div class="cols">
      <div><h4>Works</h4>{ul(t.get('works'), 'w')}</div>
      <div><h4>Doesn't</h4>{ul(t.get('doesnt'), 'd')}</div>
    </div>
  </div>
  <div class="vote" data-v="{vid}">
    <span class="vq">Your call</span>
    <button data-c="keep">Keep</button><button data-c="part">Parts of it</button><button data-c="drop">Drop</button>
    <input type="text" placeholder="A note (what exactly)" aria-label="Note for {e(t['label'])}">
  </div>
</article>'''


secs = []
nav = []
for sec in D['sections']:
    nav.append(f'<a href="#{sec["id"]}">{e(sec["short"])}</a>')
    tiles = ''.join(tile(sec, t) for t in sec['tiles'])
    take = ''
    if sec.get('take'):
        take = '<aside class="take"><h4>How it ties together</h4>' + ''.join(f'<p>{e(p)}</p>' for p in sec['take']) + '</aside>'
    secs.append(f'''<section class="sec" id="{sec['id']}">
  <div class="sech"><p class="num">{e(sec['num'])}</p><h2>{e(sec['title'])}</h2><p class="q">{e(sec['question'])}</p></div>
  {take}
  <div class="tiles">{tiles}</div>
</section>''')

intro = ''.join(f'<p>{e(p)}</p>' for p in D['intro'])
roles = ''.join(f'<li><b>{e(r[0])}</b> {e(r[1])}</li>' for r in D['roles'])
patterns = ''.join(f'<li>{e(p)}</li>' for p in D['patterns'])
rec = ''.join(f'<li>{e(p)}</li>' for p in D['recommend'])

page = open(os.path.join(H, 'board_template.html')).read()
page = (page.replace('{{INTRO}}', intro).replace('{{ROLES}}', roles).replace('{{PATTERNS}}', patterns)
        .replace('{{NAV}}', ''.join(nav)).replace('{{SECTIONS}}', '\n'.join(secs)).replace('{{RECOMMEND}}', rec))
open(os.path.join(OUT, 'index.html'), 'w').write(page)
import shutil
os.makedirs(os.path.join(OUT,'live'),exist_ok=True)
for d in ['studio','colour','story','replay','kit']:
    shutil.copy(os.path.join(H,d,'pages.html'),os.path.join(OUT,'live',d+'.html'))
shutil.copy(os.path.join(H,'kit','glass-v3.js'),os.path.join(OUT,'live','glass-v3.js'))
print('ok', sum(len(s['tiles']) for s in D['sections']), 'tiles')
