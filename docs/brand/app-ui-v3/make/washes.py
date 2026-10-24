"""Aero gradient system v3: generates the wash tokens block for shared/aero.css.

Run: python3 washes.py  -> rewrites the block between the GRADIENTS markers in ../shared/aero.css.

Why generated: every blob uses an eased falloff (smoothstep, 8 stops) instead of the default linear
two-stop fade, which is what makes CSS washes look banded and 'generated'. A fine grain sits on top.
"""
import pathlib, re, urllib.parse

H = pathlib.Path(__file__).resolve().parent
CSS = H.parent / 'shared' / 'aero.css'
T = [0, .14, .28, .42, .56, .70, .84, 1]


def ease(t):  # 1 at the centre, 0 at the edge, smooth both ends
    return 1 - (3 * t * t - 2 * t ** 3)


def blob(rgb, a, size, at, reach=100):
    r, g, b = rgb
    st = ','.join(f'rgba({r},{g},{b},{a * ease(t):.3f}) {t * reach:.0f}%' for t in T)
    return f'radial-gradient({size} at {at},{st})'


def blob_site(L, C, a, size, at, dh=0, reach=100):
    """A blob in the site's own hue (oklch relative colour from --site), lightness and chroma fixed so it stays in the family."""
    h = f'calc(h + {dh})' if dh else 'h'
    st = ','.join(f'oklch(from var(--site) {L} {C} {h} / {a * ease(t):.3f}) {t * reach:.0f}%' for t in T)
    return f'radial-gradient({size} at {at},{st})'


def hx(s):
    s = s.lstrip('#')
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


WHITE = (255, 255, 255)

# name: (light blobs, light base, dark blobs, dark base). Each blob: (colour, alpha, size, position)
WASHES = {
    'publish': (
        [('#FFC7AA', 1, '72% 92%', '10% 4%'), ('#FFCFD2', .75, '52% 70%', '64% -12%'), ('#FFE3B3', .9, '62% 88%', '98% 96%'),
         (WHITE, .7, '46% 58%', '46% 62%')], '#FFF8F3',
        [('#FF6F7D', .19, '72% 92%', '10% 4%'), ('#FF9466', .10, '46% 60%', '62% -14%'), ('#B07CFF', .09, '62% 88%', '98% 96%')], '#0F0E10'),
    'test': (
        [('#BFD8FF', 1, '72% 92%', '90% 4%'), ('#D8D0FF', .95, '64% 88%', '4% 98%'), ('#CFEFFF', .7, '50% 64%', '36% -12%'),
         (WHITE, .7, '46% 58%', '54% 60%')], '#F6F8FF',
        [('#4C8DFF', .26, '72% 92%', '90% 4%'), ('#8C73FF', .17, '64% 88%', '4% 98%'), ('#4CC8FF', .08, '50% 64%', '36% -12%')], '#0C0D12'),
    'review': (
        [('#BFEBD3', 1, '72% 92%', '8% 96%'), ('#CFE4FF', .95, '64% 88%', '94% 4%'), ('#EEF3C2', .7, '50% 64%', '16% -10%'),
         (WHITE, .7, '46% 58%', '48% 44%')], '#F5FBF8',
        [('#3CC77C', .20, '72% 92%', '8% 96%'), ('#4C8DFF', .15, '64% 88%', '94% 4%'), ('#C8DC5A', .06, '50% 64%', '74% 110%')], '#0B100E'),
    'hero': (
        [('#FFCDB2', 1, '60% 80%', '8% 12%'), ('#C8DDFF', 1, '56% 76%', '92% 6%'), ('#C8EEDA', .95, '64% 70%', '62% 108%'),
         ('#E2DAFF', .55, '40% 50%', '44% -10%'), (WHITE, .6, '40% 50%', '46% 50%')], '#FBF9F7',
        [('#FF6F7D', .15, '60% 80%', '8% 12%'), ('#4C8DFF', .2, '56% 76%', '92% 6%'), ('#3CC77C', .13, '64% 70%', '62% 108%'),
         ('#8C73FF', .08, '40% 50%', '44% -10%')], '#0D0D10'),
}


def build(blobs, base, k=1.0, card=False):
    out = []
    for col, a, size, at in blobs:
        rgb = hx(col) if isinstance(col, str) else col
        if card and rgb == WHITE:
            continue
        out.append(blob(rgb, min(1, a * k), size, at))
    return ','.join(out) + ',' + base


def grain(dark):
    rgb = '0 0 0 0 1  0 0 0 0 1  0 0 0 0 1' if dark else '0 0 0 0 0  0 0 0 0 0  0 0 0 0 0'
    a = '.07' if dark else '.08'
    svg = (f"<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3' stitchTiles='stitch'/>"
           f"<feColorMatrix values='{rgb}  0 0 0 {a} 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")
    return 'url("data:image/svg+xml,' + svg.replace('<', '%3C').replace('>', '%3E').replace('"', "'") + '") 0 0/160px 160px'


def site(dark):
    if dark:
        b = [blob_site(.66, 'clamp(.08, c * .8, .15)', .2, '90% 70%', '50% -18%'),
             blob_site(.6, 'clamp(.06, c * .6, .12)', .1, '60% 80%', '100% 110%', dh=-22)]
        base = 'oklch(from var(--site) .17 .012 h)'
    else:
        b = [blob_site(.90, 'clamp(.05, c * .5, .085)', 1, '72% 92%', '12% 4%'),
             blob_site(.93, 'clamp(.035, c * .4, .07)', .9, '60% 86%', '96% 96%', dh=-22),
             blob(hx('#FFE3D2'), .5, '50% 60%', '70% -10%'),  # a little Publish peach keeps it in the family
             blob(WHITE, .65, '46% 58%', '50% 56%')]
        base = 'oklch(from var(--site) .985 .01 h)'
    return ','.join(b) + ',' + base


def site_card(dark):
    if dark:
        return (blob_site(.64, 'clamp(.07, c * .7, .13)', .16, '90% 120%', '0% 0%') + ',oklch(from var(--site) .2 .01 h)')
    return (blob_site(.93, 'clamp(.04, c * .45, .075)', 1, '80% 120%', '0% 0%') + ','
            + blob_site(.95, 'clamp(.03, c * .35, .06)', .9, '70% 120%', '100% 100%', dh=-22) + ',oklch(from var(--site) .99 .008 h)')


def block():
    L, D = [], []
    for n, (lb, lbase, db, dbase) in WASHES.items():
        L.append(f'  --wash-{n}:{build(lb, lbase)};')
        D.append(f'  --wash-{n}:{build(db, dbase)};')
        if n != 'hero':
            # card version: same colours, smaller blobs anchored to the corners, no white core
            lcard = [(c, a * .8, '90% 130%', at) for c, a, s, at in lb[:2]]
            dcard = [(c, a * .6, '90% 130%', at) for c, a, s, at in db[:2]]
            L.append(f'  --in-{n}:{build(lcard, "#FFFFFF" if n != "publish" else "#FFFCFA", card=True)};')
            D.append(f'  --in-{n}:{build(dcard, "#161618", card=True)};')
    L.append(f'  --grain:{grain(False)};')
    D.append(f'  --grain:{grain(True)};')
    return f'''/* ===================== GRADIENTS v3 (generated by make/washes.py, do not edit by hand) =====================
   Three step washes match the marketing material: Publish = peach, coral and apricot; Test = sky and periwinkle;
   Review = mint and sky. Hero = all three. Each is a soft mesh of eased radial blobs (8 stops, smoothstep falloff,
   so no banding) with a white core in light to keep the middle luminous, never muddy. --grain is a fine noise layer:
   always put it first, e.g. background:var(--grain),var(--wash-test) (or the .w-* classes below).
   --wash-*  page and panel washes (empty states, first run, marketing panels, hero)
   --in-*    card washes: two corner blobs on white, for a card that sits on a plain page
   --wash-site / --in-site: set --site to the site's dominant colour on the element and add .w-site / .w-in-site.
   The hue comes from the site; lightness and chroma are fixed, so coral, green, navy or yellow all land in the
   same soft family. A touch of Publish peach ties it back. */
:root,[data-theme=light]{{
{chr(10).join(L)}
}}
[data-theme=dark]{{
{chr(10).join(D)}
}}
.w-site,.w-in-site{{--site:#FF8A5E}}
.w-site{{--wash-site:{site(False)};background:var(--grain),var(--wash-site)}}
[data-theme=dark] .w-site,[data-theme=dark].w-site{{--wash-site:{site(True)}}}
.w-in-site{{--in-site:{site_card(False)};background:var(--in-site)}}
[data-theme=dark] .w-in-site,[data-theme=dark].w-in-site{{--in-site:{site_card(True)}}}
.w-publish{{background:var(--grain),var(--wash-publish)}}.w-test{{background:var(--grain),var(--wash-test)}}
.w-review{{background:var(--grain),var(--wash-review)}}.w-hero{{background:var(--grain),var(--wash-hero)}}
.w-in-publish{{background:var(--in-publish)}}.w-in-test{{background:var(--in-test)}}.w-in-review{{background:var(--in-review)}}
.frame.hero{{background:var(--grain),var(--wash-hero)}}.frame.publish{{background:var(--grain),var(--wash-publish)}}
.frame.test{{background:var(--grain),var(--wash-test)}}.frame.review{{background:var(--grain),var(--wash-review)}}
.hero-block{{background:var(--grain),var(--wash-hero)}}
/* ===================== /GRADIENTS v3 ===================== */'''


if __name__ == '__main__':
    css = CSS.read_text()
    b = block()
    if '/* ===================== GRADIENTS v3' in css:
        css = re.sub(r'/\* =+ GRADIENTS v3.*?/\* =+ /GRADIENTS v3 =+ \*/', lambda m: b, css, flags=re.S)
    else:
        css = css.rstrip() + '\n\n' + b + '\n'
    CSS.write_text(css)
    print('ok', len(b))
