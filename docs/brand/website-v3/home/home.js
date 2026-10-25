/* Aero homepage, round 4 (Team H).
   - applies the COPY block, scales the real app windows, the made-with rotator, the #p1/#p2/#p3 headline switch
   - the hero loop: one clock (T seconds), every state computed from t, so ?t=8.2 freezes a frame and the recorder
     can step it frame by frame (window.__heroAt(t)). Pauses offscreen, in a hidden tab and on the pause button.
     Reduced motion: no loop; a still of the Test step, and the steps all filled.
   - section loops start when in view (CSS animations), off with reduced motion. */
(function () {
  'use strict';
  var D = document, W = window;
  var RM = W.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var Q = new URLSearchParams(location.search);
  if (Q.has('t')) D.documentElement.classList.add('rec');

  /* ---------- copy ---------- */
  try {
    var C = JSON.parse(D.getElementById('copy').textContent);
    var get = function (k) { return k.split('.').reduce(function (o, p) { return o == null ? o : (Array.isArray(o) && /^\d+$/.test(p) ? o[+p] : o[p]); }, C); };
    D.querySelectorAll('[data-c]').forEach(function (el) {
      var v = get(el.getAttribute('data-c'));
      if (typeof v === 'string' && !el.children.length) el.textContent = v;
    });
  } catch (e) { /* the built words stay */ }

  /* ---------- nav (phone) ---------- */
  var nav = D.querySelector('.site-nav'), burger = D.querySelector('.site-burger');
  if (burger) burger.addEventListener('click', function () {
    var o = nav.classList.toggle('open'); burger.setAttribute('aria-expanded', o ? 'true' : 'false');
  });

  /* ---------- scale the real windows to their boxes ---------- */
  function fit() {
    D.querySelectorAll('.sc-box').forEach(function (b) {
      var w = +b.getAttribute('data-w'), h = +b.getAttribute('data-h'), s = b.offsetWidth / w;
      if (!s) return;
      b.style.setProperty('--s', s.toFixed(5)); b.style.height = (h * s) + 'px';
    });
    D.querySelectorAll('.cr').forEach(function (b) {
      var cw = +b.getAttribute('data-cw'), s = b.offsetWidth / cw, inn = b.firstElementChild;
      inn.style.transform = 'scale(' + s.toFixed(5) + ') translate(' + (-b.firstElementChild.getAttribute('data-x')) + 'px,' + (-b.firstElementChild.getAttribute('data-y')) + 'px)';
    });
    var view = D.querySelector('.hm-view');
    if (view) { VW = view.offsetWidth; VH = view.offsetHeight; }
  }
  var VW = 0, VH = 0;

  /* ---------- the made-with rotator ---------- */
  var rot = D.querySelector('.hm-rot'), words = rot ? [].slice.call(rot.querySelectorAll('.hm-w')) : [], wi = 0;
  function rotW() { if (rot) rot.style.width = words[wi].offsetWidth + 'px'; }
  if (rot && !RM && !Q.has('t')) setInterval(function () {
    if (D.hidden) return;
    var a = words[wi]; wi = (wi + 1) % words.length; var b = words[wi];
    a.classList.remove('on'); a.classList.add('out'); setTimeout(function () { a.classList.remove('out'); }, 500);
    b.classList.add('on'); rotW();
  }, 2600);

  /* ---------- headline switch: #p1 / #p2 / #p3 ---------- */
  function prop() {
    var p = (/^#p[123]$/.test(location.hash) ? location.hash.slice(1) : 'p1');
    D.querySelectorAll('[data-p]').forEach(function (el) {
      if (el.tagName === 'A') el.classList.toggle('on', el.getAttribute('data-p') === p);
      else el.hidden = el.getAttribute('data-p') !== p;
    });
  }
  W.addEventListener('hashchange', prop); prop();

  /* ---------- hero loop ---------- */
  var T = 19.2;
  var $ = function (s, r) { return (r || D).querySelector(s); }, $$ = function (s, r) { return [].slice.call((r || D).querySelectorAll(s)); };
  var world = $('.st-world');
  function cl(x) { return x < 0 ? 0 : x > 1 ? 1 : x; }
  function r(t, a, b) { return cl((t - a) / (b - a)); }
  function sm(x) { return x * x * (3 - 2 * x); }
  function eo(x) { return 1 - Math.pow(1 - x, 3); }
  function io(t, a, b, c, d) { return sm(r(t, a, b)) * (1 - sm(r(t, c, d))); }

  var S = world && {
    claude: $('.st-claude'), parts: $$('.cl-pvin [data-b]'), sent: $('.cl-sent'), reply: $('.cl-reply'), work: $('.cl-work'),
    used: $('.cl-used'), done: $('.cl-done'), inp: $('.st-claude .cl-inp'), paste: $('.st-claude .cl-paste'),
    aero: $('.st-aero'), a1: $('.st-a1'), a2: $('.st-a2'), copied: $('.st-copied'), link: $('.st-a2 .st-link'),
    msg: $('.st-msg'), sentl: $('.st-msg .st-sent'), desk: $('.st-desk'), tw: $('.st-tw'),
    tpq: $('.st-tw .pq-wrap'), tk1: $('.st-tk1'), tk2: $('.st-tk2'), done1: $('.st-tk1 .st-done'), lv: $$('.st-lv i'),
    dark: $('.st-dark'), watch: $('.st-watch'), ins: $('.st-ins'), lines: $$('.st-trs .tl[data-s]'),
    ph: $('.st-watch .ph-line'), bars: $$('.st-watch .tline .wave i'), tc: $('.st-tc'), vpq: $('.st-vid .pq-wrap'),
    tpn: $('.st-tpn'), tpt: $('.st-tpt'), marks: $$('.st-watch .tline .marks .m'), iss: $$('.st-ins .iss, .st-ins .sumcard2'),
    steps: $$('.hm-step')
  };
  if (S) S.lines.forEach(function (l) { l._w = $$('.w', l); l._s = +l.getAttribute('data-s'); });

  function pq(el, map) { // crossfade the Pocket screens: map = {home: o, send: o, spend: o}
    if (!el) return;
    el.removeAttribute('data-pq');
    ['home', 'send', 'spend'].forEach(function (k) { var s = el.querySelector('.pq-' + k); if (s) s.style.opacity = (map[k] || 0).toFixed(3); });
  }
  var LEN = 214, CAM_P = [[0, 640], [2.1, 640], [2.6, 330], [4.5, 330], [5.0, 720], [6.8, 720], [7.2, 930], [8.8, 930], [9.4, 820], [12.7, 820], [13.2, 900], [16.1, 900], [16.5, 600], [19.2, 600]];
  function cam(t) {
    for (var i = 1; i < CAM_P.length; i++) if (t <= CAM_P[i][0]) {
      var a = CAM_P[i - 1], b = CAM_P[i]; return a[1] + (b[1] - a[1]) * sm(r(t, a[0], b[0]));
    }
    return CAM_P[CAM_P.length - 1][1];
  }

  function at(t) {
    if (!S) return;
    // camera: the whole world on a wide screen; on a phone, pan to where the action is
    var s = VW / 1200, tx = 0, ty = 0;
    if (VW / VH < 1.2) { s = VH / 700; tx = VW / 2 - cam(t) * s; tx = Math.min(0, Math.max(VW - 1200 * s, tx)); }
    else { ty = (VH - 700 * s) / 2; }
    world.style.transform = 'translate(' + tx.toFixed(1) + 'px,' + ty.toFixed(1) + 'px) scale(' + s.toFixed(5) + ')';

    // 1 Publish: Claude builds Pocket; one prompt pasted; Claude publishes; Aero shows it live
    var cO = io(t, 0, .35, 6.7, 7.2), push = sm(r(t, 4.5, 5.2));
    S.claude.style.opacity = cO.toFixed(3);
    S.claude.style.transform = 'scale(' + (1 - .035 * push).toFixed(4) + ')';
    S.claude.style.filter = push ? 'saturate(' + (1 - .3 * push).toFixed(2) + ') brightness(' + (1 - .04 * push).toFixed(3) + ')' : '';
    S.parts.forEach(function (p, i) { var k = eo(r(t, .25 + .38 * i, .7 + .38 * i)); p.style.opacity = k.toFixed(3); p.style.transform = 'translateY(' + ((1 - k) * 22).toFixed(1) + 'px)'; });
    var pasted = t >= 2.25 && t < 2.95;
    S.inp.classList.toggle('pasted', pasted); S.paste.classList.toggle('on', pasted); S.paste.classList.toggle('sel', t >= 2.25 && t < 2.55);
    S.sent.style.opacity = sm(r(t, 2.95, 3.2)).toFixed(3);
    S.reply.style.opacity = sm(r(t, 3.25, 3.45)).toFixed(3);
    S.work.style.display = t < 4.05 ? 'inline-flex' : 'none';
    S.used.style.display = S.done.style.display = t >= 4.05 ? '' : 'none';
    if (t >= 4.05) { S.used.style.display = 'inline-flex'; S.done.style.display = 'block'; }
    S.done.style.opacity = sm(r(t, 4.05, 4.35)).toFixed(3);

    var aI = eo(r(t, 4.55, 5.2)), aO = sm(r(t, 9.4, 9.6));
    S.aero.style.opacity = (sm(r(t, 4.55, 4.68)) * (1 - aO)).toFixed(3);
    S.aero.style.transform = 'translateY(' + ((1 - aI) * 46).toFixed(1) + 'px)';
    // 2 Test: the test link, copied and sent; Maya opens it on her own computer
    var a2 = sm(r(t, 6.75, 6.9));
    S.a2.style.opacity = a2.toFixed(3); S.a1.style.opacity = (1 - a2 * .999).toFixed(3);
    S.copied.style.opacity = io(t, 7.55, 7.7, 8.7, 9.0).toFixed(3);
    if (S.link) S.link.style.background = t > 7.45 && t < 8.6 ? 'var(--accent-soft)' : '';
    var mI = eo(r(t, 7.9, 8.3)), mO = sm(r(t, 9.0, 9.3));
    S.msg.style.opacity = (mI * (1 - mO)).toFixed(3);
    S.msg.style.transform = 'translate(' + ((1 - mI) * -30 + mO * 60).toFixed(1) + 'px,' + ((1 - mI) * 14).toFixed(1) + 'px)';
    S.sentl.style.opacity = sm(r(t, 8.45, 8.6)).toFixed(3);
    var dI = eo(r(t, 8.95, 9.6)), dO = sm(r(t, 13.0, 13.15));
    S.desk.style.transform = 'translateX(' + ((1 - dI) * 1220).toFixed(1) + 'px)';
    S.desk.style.opacity = (t < 8.9 ? 0 : 1 - dO).toFixed(3);
    var sd = sm(r(t, 10.1, 10.35)) * (1 - sm(r(t, 11.0, 11.25))), sp = sm(r(t, 11.65, 11.9));
    pq(S.tpq, { home: 1 - Math.max(sd, sp), send: sd, spend: sp });
    var k2 = sm(r(t, 10.95, 11.2));
    S.tk1.style.opacity = (1 - k2).toFixed(3); S.tk2.style.opacity = k2.toFixed(3);
    S.done1.style.transform = t > 10.7 && t < 10.9 ? 'scale(.96)' : '';
    var talk = t > 9.7 && t < 12.8;
    S.lv.forEach(function (b, i) {
      var v = talk ? .2 + .8 * Math.abs(Math.sin(t * 7.3 + i * .9) * Math.sin(t * 2.1 + i * .37)) : .15;
      if (talk && (t % 2.4) > 1.9) v *= .25; // pauses between phrases
      b.style.height = (v * 100).toFixed(0) + '%';
    });

    // 3 Review, in dark: Maya's session plays with her words lit; then every session together in Insights
    S.dark.style.opacity = io(t, 12.75, 12.9, 18.75, 19.2).toFixed(3);
    S.dark.style.transform = 'translateY(' + ((1 - eo(r(t, 12.75, 13.4))) * 30).toFixed(1) + 'px)';
    var sess = 80 + (152 - 80) * r(t, 13.4, 16.0);
    S.lines.forEach(function (l, i) {
      var nx = S.lines[i + 1] ? S.lines[i + 1]._s : LEN, st = sess < l._s ? 'future' : sess >= nx ? 'past' : 'cur';
      if (l._st !== st) { l.className = 'tl ' + st; l._st = st; if (st !== 'cur') l._w.forEach(function (w) { w.className = 'w'; }); }
      if (st === 'cur') {
        var f = (sess - l._s) / Math.min(14, nx - l._s), n = l._w.length, k = Math.floor(f * n);
        l._w.forEach(function (w, j) { w.className = 'w' + (j < k ? ' said' : j === k ? ' now' : ''); });
      }
    });
    var pp = sess / LEN;
    if (S.ph) S.ph.style.left = (pp * 100).toFixed(2) + '%';
    S.bars.forEach(function (b, i) { var on = i / S.bars.length < pp; if (b._p !== on) { b.classList.toggle('p', on); b._p = on; } });
    if (S.tc) S.tc.textContent = ('0' + Math.floor(sess / 60)).slice(-2) + ':' + ('0' + Math.floor(sess % 60)).slice(-2);
    pq(S.vpq, { home: sess < 92 ? 1 : 0, spend: sess >= 92 ? 1 : 0 });
    var t2 = sess >= 74;
    if (S.tpn) { S.tpn.textContent = t2 ? 'Task 2 of 2' : 'Task 1 of 2'; S.tpt.textContent = t2 ? 'Find what you spent on eating out' : 'Send £20 to Sam'; }
    S.marks.forEach(function (m) { var x = parseFloat(m.style.left) / 100 * LEN; m.classList.toggle('hot', sess >= x && sess < x + 14); });
    var ins = sm(r(t, 16.15, 16.3));
    S.ins.style.opacity = ins.toFixed(3); S.watch.style.opacity = (1 - ins * .999).toFixed(3);
    S.iss.forEach(function (el, i) { var k = eo(r(t, 16.35 + .28 * i, 16.85 + .28 * i)); el.style.opacity = k.toFixed(3); el.style.transform = 'translateY(' + ((1 - k) * 18).toFixed(1) + 'px)'; });

    // the steps along the bottom fill blue like a timeline
    [[0, 6.6], [6.6, 12.75], [12.75, 18.9]].forEach(function (ab, i) {
      var st = S.steps[i]; if (!st) return;
      st.querySelector('.hm-bar b').style.width = (r(t, ab[0], ab[1]) * 100).toFixed(1) + '%';
      st.classList.toggle('on', t >= ab[0] && t < ab[1] + .3);
    });
  }
  W.__heroAt = function (t) { fit(); at(t); };

  var t0 = 0, last = null, playing = true, visible = true, raf = 0, clock = 0;
  function loop(now) {
    raf = 0;
    if (last != null) clock = (clock + Math.min(.1, (now - last) / 1000)) % T;
    last = now; at(clock);
    if (playing && visible && !D.hidden) raf = requestAnimationFrame(loop); else last = null;
  }
  function kick() { if (!raf && playing && visible && !D.hidden && !RM && !Q.has('t')) raf = requestAnimationFrame(loop); }
  var pause = $('.hm-pause');
  if (pause) pause.addEventListener('click', function () {
    playing = !playing; pause.setAttribute('aria-label', playing ? 'Pause the animation' : 'Play the animation');
    pause.innerHTML = playing ? '<svg class="i" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M6 4v8M10 4v8"/></svg>' : '<svg class="i" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"><path d="m5.5 3.5 7 4.5-7 4.5z"/></svg>';
    kick();
  });
  D.addEventListener('visibilitychange', kick);

  /* ---------- section loops: run while in view ---------- */
  var imgs = $$('.hm-img');
  if ('IntersectionObserver' in W) {
    var io2 = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        if (en.target.classList.contains('hm-stage')) { visible = en.isIntersecting; kick(); }
        else if (!RM) en.target.classList.toggle('play', en.isIntersecting);
      });
    }, { threshold: .15 });
    imgs.forEach(function (i) { io2.observe(i); });
    var stg = $('.hm-stage'); if (stg) io2.observe(stg);
  }

  function start() {
    fit(); rotW();
    if (Q.has('t')) { clock = +Q.get('t') || 0; at(clock); return; }
    if (RM) { at(10.4); S && S.steps.forEach(function (s) { s.querySelector('.hm-bar b').style.width = '100%'; }); if (pause) pause.hidden = true; return; }
    at(0); kick();
  }
  W.addEventListener('resize', function () { fit(); rotW(); at(clock); });
  if (D.fonts && D.fonts.ready) D.fonts.ready.then(start); else W.addEventListener('load', start);
})();
