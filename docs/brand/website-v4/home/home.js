/* Aero homepage, round 5 (Team H).
   - applies the COPY block, scales the real app windows, the made-with rotator, the #p1/#p2/#p3 headline switch
   - the hero loop: one clock (T seconds), every state computed from t, so ?t=8.2 freezes a frame and the recorder
     can step it frame by frame (window.__heroAt(t)). Pauses offscreen, in a hidden tab and on the pause button.
     Reduced motion: no loop; a still of the Test step (Maya's screen), and the steps all filled.
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
    if (view) { VW = view.offsetWidth; VH = view.offsetHeight; NARROW = VW / VH < 1.2; }
    if (typeof measure === 'function') measure();
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

  /* ---------- hero loop: ONE browser window at an angle; the page inside it changes ---------- */
  var T = 28.8;
  var $ = function (s, r) { return (r || D).querySelector(s); }, $$ = function (s, r) { return [].slice.call((r || D).querySelectorAll(s)); };
  var world = $('.st-world');
  function cl(x) { return x < 0 ? 0 : x > 1 ? 1 : x; }
  function r(t, a, b) { return cl((t - a) / (b - a)); }
  function sm(x) { return x * x * (3 - 2 * x); }
  function eo(x) { return 1 - Math.pow(1 - x, 3); }
  function io(t, a, b, c, d) { return sm(r(t, a, b)) * (1 - sm(r(t, c, d))); }

  var S = world && {
    frame: $('.hv-frame'), vp: $('.hv-vp'), url: $('.hv-u'), urlBox: $('.hv-url'), cur: $('.hv-cur'), ring: $('.hv-ring'), key: $('.hv-key'),
    tabs: {}, sc: {},
    parts: $$('.cl-pvin [data-b]'), sent: $('.cl-sent'), reply: $('.cl-reply'), work: $('.cl-work'),
    used: $('.cl-used'), done: $('.cl-done'), inp: $('[data-sc=claude] .cl-inp'), paste: $('[data-sc=claude] .cl-paste'), send: $('[data-sc=claude] .cl-send'),
    banner: $('[data-sc=aero] .x-justpub'), live: $('[data-sc=aero] .x-addr .st.live'), visit: $('[data-sc=aero] .hv-visit'),
    more: $('[data-sc=aero] .x-morew .gbtn'), menu: $('[data-sc=aero] .x-menu-open'), mi: $('[data-sc=aero] .x-mi2'),
    made: $('[data-sc=setup] .x-made'), copy: $('[data-sc=setup] .x-lk .btn'), link: $('[data-sc=setup] .x-lk'), copied: $('.st-copied'),
    msg: $('.st-msg'), sentl: $('.st-msg .st-sent'), who1: $('.hv-who1'),
    tpq: $('[data-sc=tester] .pq-wrap'), tk1: $('.st-tk1'), tk2: $('.st-tk2'), done1: $('.st-tk1 .st-done'), lv: $$('.st-lv i'), rec: $('[data-sc=tester] .x-recchip'),
    lines: $$('.st-trs .tl[data-s]'), ph: $('[data-sc=watch] .ph-line'), bars: $$('[data-sc=watch] .tline .wave i'), tc: $('.st-tc'), vpq: $('.st-vid .pq-wrap'),
    tpn: $('.st-tpn'), tpt: $('.st-tpt'), marks: $$('[data-sc=watch] .tline .marks .m'), iss: $$('[data-sc=ins] .iss, [data-sc=ins] .sumcard2'),
    steps: $$('.hm-step')
  };
  if (S) {
    $$('.hv-tab').forEach(function (el) { S.tabs[el.getAttribute('data-tab')] = el; });
    $$('.hv-sc').forEach(function (el) { S.sc[el.getAttribute('data-sc')] = el; });
    S.lines.forEach(function (l) { l._w = $$('.w', l); l._s = +l.getAttribute('data-s'); });
  }

  // which page the one window shows, and when (crossfades are 0.18 s)
  var SCENES = [['claude', 0, 7.35], ['aero', 7.35, 9.5], ['site', 9.5, 11.75], ['aero', 11.75, 13.6], ['setup', 13.6, 17.4],
                ['tester', 17.4, 23.0], ['watch', 23.0, 26.0], ['ins', 26.0, 28.55], ['claude', 28.55, 99]];
  var URL = { claude: 'claude.ai/chat/pocket', aero: 'aeroapp.ai/sites/pocket', site: 'pocket.aeroapp.ai', setup: 'aeroapp.ai/tests/pocket/setup',
              tester: 'aeroapp.ai/t/pocket-7k2', watch: 'aeroapp.ai/tests/pocket/sessions/2', ins: 'aeroapp.ai/tests/pocket/insights' };
  var TABON = { claude: 'claude', aero: 'aero', site: 'site', setup: 'aero', tester: 'test', watch: 'aero', ins: 'aero' };
  function scene(t) { for (var i = 0; i < SCENES.length; i++) if (t < SCENES[i][2]) return i; return SCENES.length - 1; }

  // the owner's own cursor: [time, target] (a target is measured from the real layout; 'off' parks it). Never on the
  // tester's screen and never in the review.
  var P = {}; // measured points, frame coordinates
  var CUR = [[2.0, 'enter'], [2.9, 'inp'], [3.7, 'inp'], [4.35, 'send'], [6.6, 'send'], [7.2, 'tab:aero'], [8.6, 'tab:aero'], [9.3, 'visit'],
             [11.0, 'visit2'], [11.6, 'tab:aero'], [11.9, 'tab:aero'], [12.5, 'more'], [12.8, 'more'], [13.4, 'mi'], [13.9, 'mi2'], [14.6, 'copy'], [16.6, 'copy']];
  var CLICKS = [[3.0, 'inp'], [4.4, 'send'], [7.3, 'tab:aero'], [9.4, 'visit'], [11.7, 'tab:aero'], [12.6, 'more'], [13.5, 'mi'], [14.7, 'copy']];
  function curPos(t) {
    for (var i = 1; i < CUR.length; i++) if (t <= CUR[i][0]) {
      var a = P[CUR[i - 1][1]], b = P[CUR[i][1]], k = sm(r(t, CUR[i - 1][0], CUR[i][0]));
      if (!a || !b) return null;
      return [a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k];
    }
    return P[CUR[CUR.length - 1][1]];
  }
  function measure() {
    if (!S) return;
    var wt = world.style.transform, ft = S.frame.style.transform;
    world.style.transform = 'none'; S.frame.style.transform = 'none';
    var fr = S.frame.getBoundingClientRect(), wr = world.getBoundingClientRect();
    var keep = [];
    function vis(el) { var s = el; while (s && s !== S.frame) { if (s.classList && s.classList.contains('hv-sc')) { keep.push([s, s.style.opacity]); s.style.opacity = '1'; } s = s.parentElement; } }
    function pt(name, el, fx, fy) {
      if (!el) return; vis(el);
      var b = el.getBoundingClientRect(); P[name] = [b.left - fr.left + b.width * (fx == null ? .5 : fx), b.top - fr.top + b.height * (fy == null ? .55 : fy)];
      P[name + '#'] = [b.left - wr.left + b.width / 2, b.top - wr.top + b.height / 2]; // world centre, for the phone camera
    }
    var tabsShown = $$('.hv-tab').map(function (x) { var o = x.classList.contains('show'); x.classList.add('show'); return [x, o]; });
    pt('inp', S.inp, .45, .5); pt('send', S.send); pt('tab:aero', S.tabs.aero, .4); pt('visit', S.visit);
    var mo = S.menu && S.menu.style.opacity; if (S.menu) S.menu.style.opacity = '1';
    pt('more', S.more); pt('mi', S.mi, .3, .4); if (S.menu) S.menu.style.opacity = mo;
    pt('copy', S.copy); pt('link', S.link);
    pt('cam:claude', $('[data-sc=claude] .cl-pv'), .2, .4); pt('cam:msgs', $('[data-sc=claude] .cl-msgs'), .5, .7); pt('cam:addr', $('[data-sc=aero] .x-addr'), .3);
    pt('cam:banner', S.banner, .35); pt('cam:site', $('[data-sc=site] .pk-hero'), .3); pt('cam:tk', $('[data-sc=tester] .st-tk1 .x-tk'));
    pt('cam:voice', $('[data-sc=tester] .st-voice'), .9); pt('cam:pq', $('[data-sc=tester] .pk-hero'), .33, .15); pt('cam:video', $('[data-sc=watch] .stage3'));
    pt('cam:trs', $('[data-sc=watch] .st-trs'), .5, .4); pt('cam:sum', $('[data-sc=ins] .sumcard2'), .4, .8); pt('cam:menu', S.menu, .5, .4);
    keep.forEach(function (k) { k[0].style.opacity = k[1]; });
    tabsShown.forEach(function (x) { if (!x[1]) x[0].classList.remove('show'); });
    P.enter = [P.send ? P.send[0] + 380 : 900, 760];
    P.mi2 = P.mi; P.visit2 = P.visit && [P.visit[0] - 120, P.visit[1] + 220];
    var mr = S.msg.getBoundingClientRect();
    P['cam:msg#'] = [mr.left - wr.left + mr.width / 2 - 60, mr.top - wr.top + mr.height / 2];
    if (P.copy && S.copied) { S.copied.style.left = (P.copy[0] - 160) + 'px'; S.copied.style.top = (P.copy[1] - 76 - 66) + 'px'; }
    world.style.transform = wt; S.frame.style.transform = ft;
  }

  // the phone-width camera: [time, target]; the window is shown flat and the camera follows the action
  var CAM = [[0, 'cam:claude'], [2.3, 'inp'], [4.6, 'cam:msgs'], [6.7, 'tab:aero'], [7.6, 'cam:banner'], [8.7, 'visit'], [9.6, 'cam:site'],
             [11.2, 'tab:aero'], [12.3, 'cam:menu'], [14.0, 'copy'], [15.4, 'cam:msg#'], [17.4, 'cam:tk'], [18.4, 'cam:pq'], [19.6, 'cam:voice'],
             [20.6, 'cam:tk'], [23.0, 'cam:video'], [24.0, 'cam:trs'], [26.0, 'cam:sum'], [28.4, 'cam:claude']];
  var FR0 = [30, 52]; // the frame's place in the world (matches .hv-frame)
  function wpt(name) { var p = P[name]; if (!p) return null; return name.slice(-1) === '#' ? p : [p[0] + FR0[0], p[1] + FR0[1]]; }
  function cam(t) {
    var i = 0; while (i < CAM.length - 1 && t >= CAM[i + 1][0]) i++;
    var a = wpt(CAM[i][1]) || [740, 500], n = CAM[i + 1], b = n ? wpt(n[1]) || a : a, k = n ? sm(r(t, n[0] - .7, n[0])) : 0;
    return [a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k];
  }

  function press(el, t, tc) { // a button pressed at tc: in and out in 0.25 s
    if (!el) return;
    var k = Math.sin(Math.PI * r(t, tc - .04, tc + .22));
    el.style.transform = k > 0 ? 'scale(' + (1 - .07 * k).toFixed(3) + ')' : '';
    el.style.filter = k > 0 ? 'brightness(' + (1 - .1 * k).toFixed(3) + ')' : '';
  }
  function glow(el, k, col) { if (el) el.style.boxShadow = k > .001 ? '0 0 0 ' + (2 + 4 * k).toFixed(1) + 'px rgba(' + (col || 'var(--accent-rgb)') + ',' + (.35 * k).toFixed(3) + ')' : ''; }
  function pq(el, map) {
    if (!el) return;
    el.removeAttribute('data-pq');
    ['home', 'send', 'spend'].forEach(function (k) { var s = el.querySelector('.pq-' + k); if (s) s.style.opacity = (map[k] || 0).toFixed(3); });
  }
  var LEN = 214, NARROW = false;

  function at(t) {
    if (!S) return;
    // the camera: a wide screen sees the whole world (window at an angle); a phone sees the window flat, following the action
    var s, tx = 0, ty = 0;
    if (NARROW) {
      s = VW / 720; var c = cam(t);
      tx = VW / 2 - c[0] * s; ty = VH / 2 - c[1] * s;
      tx = Math.min(0, Math.max(VW - 1540 * s, tx)); ty = Math.min(0, Math.max(VH - 1030 * s, ty));
    } else s = VW / 1540;
    world.style.transform = 'translate(' + tx.toFixed(1) + 'px,' + ty.toFixed(1) + 'px) scale(' + s.toFixed(5) + ')';

    // the page in the window
    var si = scene(t), cur = SCENES[si][0];
    Object.keys(S.sc).forEach(function (k) {
      var o = 0;
      SCENES.forEach(function (sc) { if (sc[0] === k) o = Math.max(o, sm(r(t, sc[1] - .18, sc[1])) * (1 - sm(r(t, sc[2] - .18, sc[2]))) + (sc[1] === 0 && t < .18 ? 1 : 0)); });
      S.sc[k].style.opacity = Math.min(1, o).toFixed(3);
    });
    S.url.textContent = URL[cur];
    var maya = cur === 'tester', dark = cur === 'watch' || cur === 'ins';
    S.frame.setAttribute('data-theme', dark ? 'dark' : 'light');
    S.tabs.claude.classList.toggle('show', !maya); S.tabs.aero.classList.toggle('show', !maya);
    S.tabs.site.classList.toggle('show', !maya && t >= 9.45 && t < 28.55); S.tabs.test.classList.toggle('show', maya);
    Object.keys(S.tabs).forEach(function (k) { S.tabs[k].classList.toggle('on', TABON[cur] === k); });
    glow(S.urlBox, io(t, 9.5, 9.7, 10.6, 11.0) + io(t, 17.4, 17.6, 18.3, 18.7));

    // 1 Publish: Claude builds Pocket in its preview; the owner pastes the one prompt and sends it; Claude publishes
    var tt = t > 27 ? t - T : t;
    S.parts.forEach(function (p, i) { var k = eo(r(tt, .2 + .45 * i, .75 + .45 * i)); p.style.opacity = k.toFixed(3); p.style.transform = 'translateY(' + ((1 - k) * 22).toFixed(1) + 'px)'; });
    var pasted = t >= 3.2 && t < 4.45;
    S.inp.classList.toggle('pasted', pasted); S.paste.classList.toggle('on', pasted); S.paste.classList.toggle('sel', t >= 3.2 && t < 3.6);
    press(S.inp, t, 3.0); press(S.send, t, 4.4);
    S.sent.style.opacity = sm(r(t, 4.45, 4.7)).toFixed(3);
    S.reply.style.opacity = sm(r(t, 4.8, 5.0)).toFixed(3);
    var pub = t >= 6.0;
    S.work.style.display = pub ? 'none' : 'inline-flex';
    S.used.style.display = pub ? 'inline-flex' : 'none'; S.done.style.display = pub ? 'block' : 'none';
    S.done.style.opacity = sm(r(t, 6.0, 6.3)).toFixed(3);
    glow(S.used, io(t, 6.0, 6.15, 6.9, 7.3), '94,140,74');

    // 2 In Aero: the site's page, live; then the live site in its own tab; back to Aero
    if (S.banner) { var bk = eo(r(t, 7.45, 7.9)); S.banner.style.opacity = (t < 7.35 ? 1 : bk).toFixed(3); S.banner.style.transform = 'translateY(' + ((1 - (t < 7.35 ? 1 : bk)) * -10).toFixed(1) + 'px)'; }
    glow(S.live, io(t, 7.9, 8.1, 8.7, 9.1) + io(t, 11.85, 12.0, 12.3, 12.5), '31,143,95');
    if (S.live) S.live.style.borderRadius = '6px';
    press(S.visit, t, 9.4); press(S.tabs.aero, t, t < 10 ? 7.3 : 11.7); press(S.more, t, 12.6); press(S.mi, t, 13.5); press(S.copy, t, 14.7);
    // 3 Test: the site's menu, "User test this site", the test link copied and sent
    if (S.menu) { // opaque from its first frame: it unrolls downwards instead of fading over the settings
      var on = t >= 12.62 && t < 13.6, mk = eo(r(t, 12.62, 12.8));
      S.menu.style.opacity = on ? '1' : '0';
      S.menu.style.clipPath = on ? 'inset(0 0 ' + ((1 - mk) * 100).toFixed(1) + '% 0 round 12px)' : '';
      S.menu.style.transform = on ? 'translateY(' + ((1 - mk) * -6).toFixed(1) + 'px)' : '';
    }
    glow(S.made, io(t, 13.7, 13.9, 14.4, 14.8), '31,143,95');
    S.copied.style.opacity = io(t, 14.75, 14.9, 16.0, 16.3).toFixed(3);
    S.copied.style.transform = 'translateY(' + ((1 - eo(r(t, 14.75, 15.0))) * 8).toFixed(1) + 'px)';
    glow(S.link, io(t, 14.7, 14.85, 15.8, 16.2));
    var mI = eo(r(t, 15.4, 15.8)), mO = sm(r(t, 17.0, 17.35));
    S.msg.style.opacity = (mI * (1 - mO)).toFixed(3);
    S.msg.style.transform = 'translate(' + ((1 - mI) * -30 + mO * 60).toFixed(1) + 'px,' + ((1 - mI) * 14).toFixed(1) + 'px)';
    S.sentl.style.opacity = sm(r(t, 16.2, 16.35)).toFixed(3);

    // the cursor (the owner's actions only), its click rings and the paste keys
    var cp = curPos(t), cOn = io(t, 1.95, 2.15, 16.4, 16.7);
    if (cp && cOn > 0) { S.cur.style.opacity = cOn.toFixed(3); S.cur.style.transform = 'translate(' + (cp[0] - 5).toFixed(1) + 'px,' + (cp[1] - 3).toFixed(1) + 'px)'; }
    else S.cur.style.opacity = '0';
    var ring = 0, rp = null;
    CLICKS.forEach(function (c) { var k = r(t, c[0], c[0] + .45); if (k > 0 && k < 1) { ring = k; rp = P[c[1]]; } });
    if (rp) { S.ring.style.opacity = (1 - ring).toFixed(3); S.ring.style.transform = 'translate(' + rp[0].toFixed(1) + 'px,' + rp[1].toFixed(1) + 'px) scale(' + (.5 + .7 * eo(ring)).toFixed(3) + ')'; }
    else S.ring.style.opacity = '0';
    if (P.inp) { S.key.style.opacity = io(t, 3.05, 3.15, 3.7, 3.85).toFixed(3); S.key.style.transform = 'translate(' + (P.inp[0] + 24).toFixed(0) + 'px,' + (P.inp[1] - 54).toFixed(0) + 'px)'; }

    // 4 Maya tries it on her laptop: this tab and her voice are recorded. No cursor drawn on her screen.
    S.who1.style.opacity = io(t, 17.5, 17.8, 22.6, 22.9).toFixed(3);
    if (S.rec) { var rk = eo(r(t, 17.6, 17.9)); S.rec.style.opacity = rk.toFixed(3); }
    var sd = sm(r(t, 19.0, 19.25)) * (1 - sm(r(t, 20.0, 20.25))), sp = sm(r(t, 20.6, 20.85));
    pq(S.tpq, { home: 1 - Math.max(sd, sp), send: sd, spend: sp });
    var k2 = sm(r(t, 19.95, 20.2));
    S.tk1.style.opacity = (1 - k2).toFixed(3); S.tk2.style.opacity = k2.toFixed(3);
    press(S.done1, t, 19.75);
    function talk(bars, a, b, f) {
      var on = t > a && t < b;
      bars.forEach(function (el, i) {
        var v = on ? .2 + .8 * Math.abs(Math.sin(t * f + i * .9) * Math.sin(t * 2.1 + i * .37)) : .15;
        if (on && (t % 2.4) > 1.9) v *= .25;
        el.style.height = (v * 100).toFixed(0) + '%';
      });
    }
    talk(S.lv, 18.0, 22.7, 7.3);

    // 5 Review, in dark: the session plays, her words lit as they're said; then every session in Insights. No cursor.
    var sess = 80 + (152 - 80) * r(t, 23.3, 25.9);
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
    S.iss.forEach(function (el, i) { var k = eo(r(t, 26.1 + .3 * i, 26.6 + .3 * i)); el.style.opacity = k.toFixed(3); el.style.transform = 'translateY(' + ((1 - k) * 18).toFixed(1) + 'px)'; });

    // the steps along the bottom fill blue like a timeline
    [[0, 11.75], [11.75, 23.0], [23.0, 28.55]].forEach(function (ab, i) {
      var st = S.steps[i]; if (!st) return;
      st.querySelector('.hm-bar b').style.width = (r(t, ab[0], ab[1]) * 100).toFixed(1) + '%';
      st.classList.toggle('on', t >= ab[0] && t < ab[1]);
    });
  }
  W.__heroAt = function (t) { clock = t; fit(); at(t); };
  W.__heroT = T;

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
        else if (!RM) en.target.classList.toggle('is-running', en.isIntersecting);
      });
    }, { threshold: .15 });
    imgs.forEach(function (i) { io2.observe(i); });
    var stg = $('.hm-stage'); if (stg) io2.observe(stg);
  }

  function start() {
    fit(); rotW();
    if (Q.has('t')) { clock = +Q.get('t') || 0; at(clock); return; }
    if (RM) { at(19.4); S && S.steps.forEach(function (s) { s.querySelector('.hm-bar b').style.width = '100%'; }); if (pause) pause.hidden = true; return; }
    at(0); kick();
  }
  W.addEventListener('resize', function () { fit(); rotW(); at(clock); });
  if (D.fonts && D.fonts.ready) D.fonts.ready.then(start); else W.addEventListener('load', start);
})();
