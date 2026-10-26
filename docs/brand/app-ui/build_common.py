"""Page frame shared by components.html, screens.html and flows.html."""
from kit import *

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Geist:wght@300..600&family=Geist+Mono:wght@400;500&display=swap" rel="stylesheet">')

PAGES = [("components.html", "Components"), ("screens.html", "Screens"), ("flows.html", "Flows")]

def page(fname, title, desc, body):
    nav = "".join(f'<a href="{f}" class="{"is-active" if f == fname else ""}">{t}</a>' for f, t in PAGES)
    ctl = ('<div class="b-ctl"><label>Palette</label><span class="ae-seg"><span class="ae-seg__opt" data-set-pal="morning">Morning</span><span class="ae-seg__opt" data-set-pal="clear">Clear</span></span>'
           '<label>Layout</label><span class="ae-seg"><span class="ae-seg__opt" data-set-lay="side">Side by side</span><span class="ae-seg__opt" data-set-lay="large">Large</span></span></div>')
    return f'''<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}">
<!-- version: 2026-10-23.1 -->
{FONTS}<link rel="stylesheet" href="tokens.css"><link rel="stylesheet" href="components.css"><link rel="stylesheet" href="board.css">
</head><body class="ae-kit">{sprite()}
<header class="b-top"><span class="ae-logo">Aero</span><nav>{nav}</nav>{ctl}</header>
<div class="b-wrap">{body}</div>
<script>if(new URLSearchParams(location.search).get('glass')==='0')document.addEventListener('DOMContentLoaded',function(){{document.querySelectorAll('[data-glass-v3]').forEach(function(b){{b.removeAttribute('data-glass-v3')}})}});</script>
<script src="board.js"></script>
<script src="glass-v3.js"></script>
</body></html>'''

def fitbox(inner, w=1180, h=760, mh=None, fixed=False, extra=""):
    a = f' data-w="{w}" data-h="{h}"' + (f' data-mh="{mh}"' if mh else "") + (" data-fixed" if fixed else "")
    return f'<div class="fit"{a}{extra}><div class="fit__in">{inner}</div></div>'

def approach(letter, name, why, inner, pick=False, frm="", prop="", w=1180, h=760, mh=None, demo=False):
    p = '<span class="pick">Recommended</span>' if pick else ""
    f = f'<span class="from">{E(frm)}</span>' if frm else ""
    pr = proposed(prop) if prop else ""
    d = ' data-demo="session"' if demo else ""
    return (f'<figure class="ap"{d}><figcaption><span class="t">{letter}. {E(name)} {p}{pr}{f}</span><p>{why}</p></figcaption>'
            f'{fitbox(inner, w, h, mh)}</figure>')

def state(name, sub, inner, w=1180, h=640, mh=None, prop="", fixed=False):
    pr = proposed(prop) if prop else ""
    ph = " st--phone" if w <= 420 else ""
    return (f'<figure class="st{ph}"><figcaption>{E(name)} <span class="n">{E(sub)}</span>{pr}</figcaption>{fitbox(inner, w, h, mh, fixed)}</figure>')

def screen(n, sid, title, lede, why, approaches, states_html="", notes=None, n_states=3):
    na = len(approaches)
    na = 2 if na == 4 else na
    nt = ""
    if notes:
        nt = '<div class="notes">' + "".join(f'<div class="note{" eng" if k == "Engineer check" else ""}"><h4>{E(k)}</h4><ul>{"".join("<li>"+v+"</li>" for v in vs)}</ul></div>' for k, vs in notes) + '</div>'
    st = f'<h3 class="states-h">States</h3><div class="states" style="--n:{n_states}">{states_html}</div>' if states_html else ""
    return (f'<section class="scr" id="{sid}"><div class="scr__head"><span class="scr__n">{n:02d}</span><div><h2>{E(title)}</h2><p>{lede}</p></div>'
            f'<div class="scr__why">{why}</div></div><div class="appr" style="--n:{na}">{"".join(approaches)}</div>{st}{nt}</section>')
