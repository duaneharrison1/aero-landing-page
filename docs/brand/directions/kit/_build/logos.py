"""Logo options for the kit. Reuses the brand builder (research/brand/_build) to draw outlines.
Writes kit/logo/<id>-*.svg (standalone files) and kit/_build/defs.svg (inline <symbol>s for pages.html).
In the symbols, letters use currentColor, the dot uses var(--dot), favicon tiles use var(--tile)/var(--glyph)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/home/claude/research/brand/_build')
from lib import Font, fmt  # noqa: E402

KIT = os.path.dirname(HERE)
ACCENT, INK, PAPER, DARK = '#3478F6', '#1D1D1F', '#FFFFFF', '#F5F5F3'


def geom(f, text, track, k=1.2, dot=True):
    """Glyph outlines + a true-circle full stop (1.2 x the o stroke, gap tightened 15%)."""
    upm = f.tt['head'].unitsPerEm
    s = 1000 / upm
    t = text + ('.' if dot else '')
    glyphs, _ = f.shape(t, round(track / s))
    letters = glyphs[:-1] if dot else glyphs
    d = ' '.join(f.path(g['name'], g['x'], -g['y']) for g in letters)
    xs0, ys0, xs1, ys1 = [], [], [], []
    for g in letters:
        b = f.bounds(g['name'])
        if not b:
            continue
        xs0.append(g['x'] + b[0]); xs1.append(g['x'] + b[2]); ys0.append(-b[3]); ys1.append(-b[1])
    circ = ''
    if dot:
        o = 'o' if 'o' in text else 'a' if 'a' in text else None
        ob = f.bounds(f.gname('o'))
        xsn = f.scan_h(f.gname('o'), (ob[1] + ob[3]) / 2)
        D = round((xsn[1] - xsn[0]) * k)
        per, prev = glyphs[-1], glyphs[-2]
        pb, prb = f.bounds(per['name']), f.bounds(prev['name'])
        prev_right = prev['x'] + prb[2]
        gap = (per['x'] + pb[0]) - prev_right
        cx = prev_right + gap * 0.85 + D / 2
        cy = -D / 2 + 4 / s
        circ = (cx, cy, D)
        xs1.append(cx + D / 2); ys1.append(cy + D / 2)
    return dict(d=d, dot=circ, box=(min(xs0), min(ys0), max(xs1), max(ys1)), upm=upm)


def circle(c, style='fill:var(--dot,#3478F6)'):
    cx, cy, D = c
    return f'<circle cx="{fmt(cx)}" cy="{fmt(cy)}" r="{fmt(D / 2)}" style="{style}"/>'


def wm_body(g):
    b = f'<path fill="currentColor" d="{g["d"]}"/>'
    if g['dot']:
        b += circle(g['dot'])
    return b


def vb(box, pad=0):
    x0, y0, x1, y1 = box
    return f'{fmt(x0 - pad)} {fmt(y0 - pad)} {fmt(x1 - x0 + 2 * pad)} {fmt(y1 - y0 + 2 * pad)}'


def tile(f, ch, dot=True, size=32, cover=0.56, k=1.5, rx=7, dot_only=False):
    """Favicon tile: glyph (and dot) centred on a rounded square."""
    tl = f'<rect width="{size}" height="{size}" rx="{rx}" style="fill:var(--tile,#1D1D1F)"/>'
    if dot_only:
        r = size * 0.17
        return tl + f'<circle cx="{fmt(size * 0.66)}" cy="{fmt(size * 0.66)}" r="{fmt(r)}" style="fill:var(--dot,#3478F6)"/>'
    g = geom(f, ch, 0, k, dot)
    x0, y0, x1, y1 = g['box']
    cap = f.cap if ch.isupper() else f.xh
    s = size * cover / (cap if ch.isupper() else f.cap * 0.92)
    w = x1 - x0
    tx = (size - w * s) / 2 - x0 * s
    ty = size / 2 + cap * s / 2 + size * 0.01
    body = f'<path style="fill:var(--glyph,#F5F5F3)" d="{g["d"]}"/>' + (circle(g['dot']) if g['dot'] else '')
    return tl + f'<g transform="translate({fmt(tx)} {fmt(ty)}) scale({s:.5f})">{body}</g>'


G5, G7 = Font('geist500.ttf'), Font('geist700.ttf')
IS, SG = Font('instrumentsans500.ttf'), Font('schibsted500.ttf')

OPTS = []


def add(id, name, note, wm, fav, mark=None, lock_gap=0.34):
    OPTS.append(dict(id=id, name=name, note=note, wm=wm, fav=fav, mark=mark, gap=lock_gap))


# 1 favourite
add('aero-dot', '"Aero." Geist 500', 'Today\'s favourite. The blue full stop is the one bright thing on a page.',
    geom(G5, 'Aero', -6), tile(G7, 'A'))
# 2 no dot
add('aero-plain', '"Aero" Geist 500, no dot', 'Plainest. Loses the one memorable detail; colour moves to the product.',
    geom(G5, 'Aero', -6, dot=False), tile(G7, 'A', dot=False))
# 3 lowercase
add('aero-lower', '"aero." lowercase', 'Softer and more casual; closer to a tool than a company.',
    geom(G5, 'aero', -10), tile(G7, 'a'))
# 4 mark + wordmark
add('mark-lock', '"A." mark plus "Aero"', 'A tile you can recognise at 16px, then the plain word beside it.',
    geom(G5, 'Aero', -6, dot=False), tile(G7, 'A'), mark=tile(G7, 'A', size=32, cover=0.5, k=1.4, rx=8))
# 5 warmer sans
add('aero-instrument', '"Aero." Instrument Sans 500', 'A little warmer, rounder joins; same dot, same rules.',
    geom(IS, 'Aero', -8), tile(IS, 'A'))
# 6 editorial sans
add('aero-schibsted', '"Aero." Schibsted Grotesk 500', 'More character in the a and the r; reads editorial, less app.',
    geom(SG, 'Aero', -8), tile(SG, 'A'))
# 7 dot mark
add('dot-mark', 'Dot mark plus "Aero"', 'The dot alone is the mark: it becomes the playhead, the loader and the favicon.',
    geom(G5, 'Aero', -6, dot=False), tile(None, '', dot_only=True),
    mark='<circle cx="16" cy="16" r="16" style="fill:var(--dot,#3478F6)"/>', lock_gap=0.3)


def lockup(o):
    """Wordmark with optional mark on the left, in font units of the wordmark."""
    g = o['wm']
    x0, y0, x1, y1 = g['box']
    if not o['mark']:
        return wm_body(g), g['box']
    f_cap = (y1 - y0)
    if o['id'] == 'dot-mark':
        ms = f_cap * 0.42 / 32             # dot about 42% of the cap height
        my = y1 - 32 * ms                  # sits on the baseline, like a full stop before the word
    else:
        ms = f_cap * 1.18 / 32
        my = (y0 + y1) / 2 - 16 * ms
    mw = 32 * ms
    gap = f_cap * o['gap']
    mx = x0 - gap - mw
    body = f'<g transform="translate({fmt(mx)} {fmt(my)}) scale({ms:.4f})">{o["mark"]}</g>' + wm_body(g)
    return body, (mx, min(y0, my), x1, max(y1, my + mw))


def main():
    os.makedirs(f'{KIT}/logo', exist_ok=True)
    syms, meta = [], []
    for o in OPTS:
        body, box = lockup(o)
        v = vb(box)
        syms.append(f'<symbol id="lg-{o["id"]}" viewBox="{v}">{body}</symbol>')
        syms.append(f'<symbol id="fv-{o["id"]}" viewBox="0 0 32 32">{o["fav"]}</symbol>')
        if o['mark']:
            syms.append(f'<symbol id="mk-{o["id"]}" viewBox="0 0 32 32">{o["mark"]}</symbol>')
        w, h = box[2] - box[0], box[3] - box[1]
        meta.append(dict(id=o['id'], name=o['name'], note=o['note'], ratio=round(w / h, 4)))
        # standalone files: light and dark
        for mode, ink, tileC, glyph in (('light', INK, INK, DARK), ('dark', DARK, '#2A2A2E', DARK)):
            colored = body.replace('currentColor', ink).replace('var(--dot,#3478F6)', ACCENT)
            with open(f'{KIT}/logo/{o["id"]}-{mode}.svg', 'w') as fh:
                fh.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{v}" role="img" aria-label="Aero">{colored}</svg>\n')
            fv = o['fav'].replace('var(--tile,#1D1D1F)', tileC).replace('var(--glyph,#F5F5F3)', glyph).replace('var(--dot,#3478F6)', ACCENT)
            with open(f'{KIT}/logo/{o["id"]}-favicon-{mode}.svg', 'w') as fh:
                fh.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">{fv}</svg>\n')
    with open(f'{HERE}/defs.svg', 'w') as fh:
        fh.write('<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>' + ''.join(syms) + '</defs></svg>')
    import json
    with open(f'{HERE}/logos.json', 'w') as fh:
        json.dump(meta, fh, indent=1)
    print(json.dumps(meta, indent=1))


if __name__ == '__main__':
    main()
