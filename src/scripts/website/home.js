/* Aero homepage, round 9 (Team H).
   - applies the COPY block, scales the real app windows, the made-with rotator, the #p1/#p2/#p3 headline switch
   - the hero loop: one clock (T seconds), every state computed from t, so ?t=8.2 freezes a frame and the recorder
     can step it frame by frame (window.__heroAt(t)). Pauses offscreen, in a hidden tab, and with Space on the focused stage (no visible button).
     Reduced motion: no loop; a still of Maya's test on her laptop, and the steps all filled.
   - section loops start when in view (CSS animations), off with reduced motion. */
(function () {
  'use strict';
  var D = document, W = window;
  var RM = W.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var Q = new URLSearchParams(location.search);
  if (Q.has('t')) D.documentElement.classList.add('rec');
  if (Q.has('review') || /^#p[123]$/.test(location.hash)) D.documentElement.classList.add('review'); // the headline switcher is a review tool
  var LAY = Q.get('l') || 'c'; if (/^[bc]$/.test(LAY)) D.documentElement.classList.add('lay-' + LAY); // hero layout: c (centred, decided 25 Oct), or ?l=a / ?l=b

  /* ---------- copy ---------- */
  try {
    var C = JSON.parse(D.getElementById('copy').textContent);
    var get = function (k) { return k.split('.').reduce(function (o, p) { return o == null ? o : (Array.isArray(o) && /^\d+$/.test(p) ? o[+p] : o[p]); }, C); };
    D.querySelectorAll('[data-c]').forEach(function (el) {
      var v = get(el.getAttribute('data-c'));
      if (typeof v === 'string' && !el.children.length) el.textContent = v;
    });
  } catch (e) { /* the built words stay */ }

  /* nav (phone): nav.js, shared with every page */

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
  function rotW() { if (!rot) return; var m = 0; words.forEach(function (w) { w.style.right = 'auto'; m = Math.max(m, w.offsetWidth); w.style.right = ''; }); rot.style.width = m + 'px'; }
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

  /* ---------- hero loop. Script time T = 49.6 s; the visitor's clock runs through warp() (the paste and send get
     2.7 s more), so a full loop is 52.3 s. The owner's browser at an angle; for the test, Maya's own computer (a
     narrower window, dark, her own WhatsApp) at the same angle; then back. The end flows into the start. ---------- */
  var T = 49.6;
  var $ = function (s, r) { return (r || D).querySelector(s); }, $$ = function (s, r) { return [].slice.call((r || D).querySelectorAll(s)); };
  var world = $('.st-world');
  function cl(x) { return x < 0 ? 0 : x > 1 ? 1 : x; }
  function r(t, a, b) { return cl((t - a) / (b - a)); }
  function sm(x) { return x * x * (3 - 2 * x); }
  function eo(x) { return 1 - Math.pow(1 - x, 3); }
  function io(t, a, b, c, d) { return sm(r(t, a, b)) * (1 - sm(r(t, c, d))); }
  function within(t, a, b) { return t >= a && t < b; }
  // write to the DOM only when a value changes (P2-5)
  function css(el, k, v) { if (!el) return; var c = el._c || (el._c = {}); if (c[k] !== v) { c[k] = v; el.style[k] = v; } }
  function cls(el, k, on) { if (!el) return; var c = el._k || (el._k = {}); on = !!on; if (c[k] !== on) { c[k] = on; el.classList.toggle(k, on); } }
  function txt(el, v) { if (el && el._t !== v) { el._t = v; el.textContent = v; } }
  function op(el, v) { css(el, 'opacity', (+v).toFixed(3)); }

  var OW = $('.hv-frame:not(.hv-mframe)'), MF = $('.hv-mframe');
  var S = world && {
    frame: OW, url: $('.hv-u', OW), urlBox: $('.hv-url', OW), prog: $('.hv-prog', OW),
    cur: $('.hv-cur'), ring: $('.hv-ring'), key: $('.hv-key'), tabs: {}, sc: {},
    sent: $('.cl-sent'), reply: $('.cl-reply'), work: $('.cl-work'), used: $('.cl-used'), done: $('.cl-done'),
    inp: $('[data-sc=claude] .cl-inp'), paste: $('[data-sc=claude] .cl-paste'), send: $('[data-sc=claude] .cl-send'),
    pdone: $('[data-sc=prompt] .hv-pdone'), pcopy: $('[data-sc=prompt2] .x-pba .btn'),
    banner: $('[data-sc=aero] .x-justpub'), live: $('[data-sc=aero] .x-addr .st.live'), visit: $('[data-sc=aero] .hv-visit'),
    more: $('[data-sc=aero] .x-morew .gbtn'), menu: $('[data-sc=aero] .x-menu-open'), mi: $('[data-sc=aero] .x-mi2'),
    blank: $('.hv-blank'), made: $('[data-sc=setup] .x-made'), copy: $('[data-sc=setup] .x-lk .btn'),
    oField: $('[data-wa=owner] .wa-field'), oSend: $('[data-wa=owner] .wa-send'), oInp: $('[data-wa=owner] .wa-inp'), oNew: $('[data-wa=owner] .wa-new'),
    mframe: MF, murl: $('.hv-u', MF), mprog: $('.hv-prog', MF), mtabs: {}, ms: {},
    mNew: $('[data-wa=maya] .wa-new'), mLink: $('[data-wa=maya] .wa-new .wa-link'), mLast: $('[data-wa=maya] .wa-hot .wa-last'), mTime: $('[data-wa=maya] .wa-hot .wa-rr small'),
    mcont: $('[data-ms=w] .x-tgo .btn'), mshare: $('[data-ms=p] .hv-share'), say: $$('.hv-say'), meter: $$('[data-ms=t] .st-meter i'),
    tpq: $('[data-ms=t] .pq-wrap'), tk1: $('[data-ms=t] .st-tk1'), tk2: $('[data-ms=t] .st-tk2'), done1: $('[data-ms=t] .st-tk1 .st-done'), rec: $('[data-ms=t] .x-recchip'),
    lines: $$('.st-trs .tl[data-s]'), ph: $('[data-sc=watch] .ph-line'), bars: $$('[data-sc=watch] .tline .wave i'), tc: $('.st-tc'), vpq: $('.st-vid .pq-wrap'),
    tpn: $('.st-tpn'), tpt: $('.st-tpt'), marks: $$('[data-sc=watch] .tline .marks .m'), iss: $$('[data-sc=ins] .sumcard2, [data-sc=ins] .iss'),
    sbSites: $$('[data-sc=ins] .sb-item')[1], newsite: $('[data-sc=sites] .mhead .r .btn'),
    steps: $$('.hm-step')
  };
  if (S) {
    $$('.hv-tab', OW).forEach(function (el) { S.tabs[el.getAttribute('data-tab')] = el; });
    $$('.hv-sc').forEach(function (el) { S.sc[el.getAttribute('data-sc')] = el; });
    $$('.hv-tab', MF).forEach(function (el) { S.mtabs[el.getAttribute('data-tab')] = el; });
    $$('.hv-ms').forEach(function (el) { S.ms[el.getAttribute('data-ms')] = el; });
    S.lines.forEach(function (l) { l._w = $$('.w', l); l._s = +l.getAttribute('data-s'); });
    S.tabX = S.tabs.site && S.tabs.site.querySelector('.hv-x');
    S.mLast0 = S.mLast && S.mLast.textContent;
  }

  // the owner's window: which page, when (crossfades 0.2 s)
  var SCENES = [['claude', 0, 7.3], ['prompt', 7.3, 8.5], ['aero', 8.5, 10.75], ['site', 10.75, 13.2], ['aero', 13.2, 16.1], ['setup', 16.1, 19.65],
                ['wa', 19.65, 34.6], ['watch', 34.6, 38.6], ['ins', 38.6, 46.6], ['sites', 46.6, 47.5], ['prompt2', 47.5, 49.25], ['claude', 49.25, 99]];
  var URL = { claude: 'claude.ai/chat/pocket', prompt: 'aeroapp.ai/new?from=prompt', prompt2: 'aeroapp.ai/new?from=prompt', aero: 'aeroapp.ai/sites/pocket', site: 'pocket.aeroapp.ai',
              setup: 'aeroapp.ai/tests/pocket/setup', wa: 'web.whatsapp.com', watch: 'aeroapp.ai/tests/pocket/sessions/6', ins: 'aeroapp.ai/tests/pocket/insights', sites: 'aeroapp.ai/sites' };
  var TABON = { claude: 'claude', site: 'site', wa: 'wa' };
  var LOADS = [8.5, 10.75, 16.1, 46.6, 47.5];
  var MS = [['wa', 0, 24.3], ['w', 24.3, 26.4], ['p', 26.4, 27.6], ['t', 27.6, 99]];
  function scene(t) { for (var i = 0; i < SCENES.length; i++) if (t < SCENES[i][2]) return SCENES[i][0]; return 'claude'; }

  // the owner's cursor (never on Maya's screen, never in the review): [time, target]
  var P = {};
  var CUR = [[0, 'tab:claude'], [1.2, 'inp'], [3.0, 'inp'], [3.45, 'send'], [6.6, 'send'], [7.2, 'tab:aero'], [9.4, 'tab:aero'], [10.6, 'visit'],
             [12.4, 'visit2'], [13.1, 'tab:aero'], [13.6, 'tab:aero'], [14.3, 'more'], [14.45, 'more'], [14.85, 'mi'], [16.0, 'mi'], [16.6, 'mi3'],
             [18.0, 'mi3'], [18.5, 'copy'], [19.0, 'copy'], [19.55, 'tab:wa'], [19.7, 'tab:wa'], [20.05, 'wa:field'], [20.6, 'wa:field'],
             [21.0, 'wa:send'], [21.7, 'wa:send'],
             [45.0, 'ins:park'], [45.6, 'tabx'], [45.8, 'tabx'], [46.4, 'sb:sites'], [46.8, 'sb:sites'], [47.3, 'newsite'], [47.6, 'newsite'], [48.1, 'pcopy'],
             [48.5, 'pcopy'], [49.1, 'tab:claude'], [T, 'tab:claude']];
  var CLICKS = [[1.3, 'inp'], [3.5, 'send'], [7.25, 'tab:aero'], [10.7, 'visit'], [13.15, 'tab:aero'], [14.4, 'more'], [16.0, 'mi'], [18.6, 'copy'],
                [19.6, 'tab:wa'], [20.1, 'wa:field'], [21.05, 'wa:send'],
                [45.7, 'tabx'], [46.5, 'sb:sites'], [47.4, 'newsite'], [48.2, 'pcopy'], [49.15, 'tab:claude']];
  var CURON = [[0, 21.8], [45.0, 99]];
  function curPos(t) {
    for (var i = 1; i < CUR.length; i++) if (t <= CUR[i][0]) {
      var a = P[CUR[i - 1][1]], b = P[CUR[i][1]], k = sm(r(t, CUR[i - 1][0], CUR[i][0]));
      if (!a || !b) return null;
      return [a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k];
    }
    return P[CUR[CUR.length - 1][1]];
  }

  var FR0 = [30, 40], FRW = [1440, 940], MF0 = [90, 56], MFW = [1240, 820];
  function measure() {
    if (!S) return;
    var wt = world.style.transform, ft = S.frame.style.transform, mt = S.mframe.style.transform;
    world.style.transform = 'none'; S.frame.style.transform = 'none'; S.mframe.style.transform = 'none';
    var fr = S.frame.getBoundingClientRect(), wr = world.getBoundingClientRect(), keep = [];
    function vis(el) {
      for (var s = el; s && s !== world; s = s.parentElement) if (s.classList && (s.classList.contains('hv-sc') || s.classList.contains('hv-ms') || s.classList.contains('hv-frame'))) {
        keep.push([s, s.style.opacity, s.style.display]); s.style.opacity = '1'; s.style.display = '';
      }
    }
    function pt(name, el, fx, fy) {
      if (!el) return; vis(el);
      var b = el.getBoundingClientRect();
      P[name] = [b.left - fr.left + b.width * (fx == null ? .5 : fx), b.top - fr.top + b.height * (fy == null ? .55 : fy)];
      P[name + '#'] = [b.left - wr.left + b.width * (fx == null ? .5 : fx), b.top - wr.top + b.height * (fy == null ? .5 : fy)];
    }
    var shown = $$('.hv-tab').map(function (x) { var o = x.classList.contains('show'); x.classList.add('show'); return [x, o]; });
    var typ = S.oInp && S.oInp.classList.contains('typing'); if (S.oInp) S.oInp.classList.add('typing');
    pt('inp', S.inp, .9, .5); pt('send', S.send); pt('tab:aero', S.tabs.aero, .4); pt('tab:claude', S.tabs.claude, .4); pt('tab:wa', S.tabs.wa, .4); pt('tabx', S.tabX); pt('visit', S.visit);
    var mo = S.menu && S.menu.style.opacity; if (S.menu) S.menu.style.opacity = '1';
    pt('more', S.more); pt('mi', S.mi, .3, .25); pt('cam:menu', S.menu, .5, .4); if (S.menu) S.menu.style.opacity = mo;
    pt('copy', S.copy); pt('pcopy', S.pcopy); pt('sb:sites', S.sbSites, .3); pt('newsite', S.newsite);
    pt('wa:field', S.oField, .8); pt('wa:send', S.oSend);
    pt('cam:claude', $('[data-sc=claude] .cl-msgs'), .5, .3); pt('cam:msgs', $('[data-sc=claude] .cl-msgs'), .5, .75); pt('cam:pdone', S.pdone, .4);
    pt('cam:banner', S.banner, .3); pt('cam:site', $('[data-sc=site] .pk-hero'), .3); pt('cam:setup', S.made, .3);
    pt('cam:wanew', S.oNew, .5); pt('cam:video', $('[data-sc=watch] .stage3')); pt('cam:trs', $('[data-sc=watch] .st-trs'), .5, .4);
    pt('cam:sum', $('[data-sc=ins] .sumcard2'), .4, .6); pt('cam:iss', $('[data-sc=ins] .iss'), .4, .4);
    pt('cam:sites', $('[data-sc=sites] .mhead'), .7, 3); pt('cam:prompt', $('[data-sc=prompt2] .x-pbox'), .4);
    pt('cam:mlabel', $('.hv-mlabel'), .3, 3.5); pt('cam:mnew', S.mNew, .5); pt('cam:wcard', $('[data-ms=w] .x-tcard')); pt('cam:pcard', $('[data-ms=p] .x-tcard'));
    pt('cam:tk', $('[data-ms=t] .st-tk1 .x-tk'), .9, .3); pt('cam:rec', S.rec, .5, 2.5); pt('cam:say', S.say[0], .2, .5);
    keep.forEach(function (k) { k[0].style.opacity = k[1]; k[0].style.display = k[2]; });
    if (S.oInp && !typ) S.oInp.classList.remove('typing');
    shown.forEach(function (x) { if (!x[1]) x[0].classList.remove('show'); });
    // invalidate the write caches for what measure touched
    $$('.hv-sc, .hv-ms, .hv-frame, .x-menu-open').forEach(function (el) { el._c = {}; });
    P.mi3 = P.mi && [P.mi[0] + 40, P.mi[1] + 6];
    P.visit2 = P.visit && [P.visit[0] - 140, P.visit[1] + 240];
    P['ins:park'] = P['sb:sites'] && [P['sb:sites'][0] + 420, P['sb:sites'][1] + 160];
    world.style.transform = wt; S.frame.style.transform = ft; S.mframe.style.transform = mt;
  }

  // phone width: windows flat; the camera follows the action. [time, target, zoom] (zoom: world px across the
  // screen; 520 to read, 720 for moves)
  var CAM = [[0, 'cam:claude', 600], [1.0, 'inp', 520], [4.2, 'cam:msgs', 560], [6.8, 'tab:aero', 640], [7.6, 'cam:pdone', 520], [8.8, 'cam:banner', 560],
             [10.0, 'visit', 600], [11.4, 'cam:site', 720], [12.6, 'tab:aero', 640], [14.0, 'cam:menu', 520], [16.6, 'cam:setup', 560], [18.2, 'copy', 560],
             [19.4, 'tab:wa', 640], [20.2, 'wa:field', 560], [21.3, 'cam:wanew', 560], [22.6, 'cam:mlabel#', 640], [23.4, 'cam:mnew#', 560],
             [24.6, 'cam:wcard#', 520], [26.6, 'cam:pcard#', 520], [27.8, 'cam:rec#', 640], [28.4, 'cam:tk#', 640], [30.0, 'cam:say#', 640],
             [32.0, 'cam:tk#', 640], [34.8, 'cam:video', 640], [36.0, 'cam:trs', 520], [38.8, 'cam:sum', 520], [41.3, 'cam:iss', 560],
             [45.2, 'tabx', 640], [46.2, 'sb:sites', 640], [46.8, 'cam:sites', 640], [47.7, 'cam:prompt', 560], [48.8, 'tab:claude', 640], [T + 1, 'cam:claude', 600]];
  function wpt(name) { var p = P[name]; if (!p) return null; return name.slice(-1) === '#' ? p : [p[0] + FR0[0], p[1] + FR0[1]]; }
  function cam(t) {
    var i = 0; while (i < CAM.length - 1 && t >= CAM[i + 1][0]) i++;
    var a = wpt(CAM[i][1]) || [740, 500], n = CAM[i + 1], b = n ? wpt(n[1]) || a : a, k = n ? sm(r(t, n[0] - .8, n[0])) : 0;
    var za = CAM[i][2], zb = n ? n[2] : za;
    return [a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k, za + (zb - za) * k];
  }

  function press(el, t, tc) {
    if (!el) return;
    var k = Math.sin(Math.PI * r(t, tc - .04, tc + .24));
    css(el, 'transform', k > 0 ? 'scale(' + (1 - .07 * k).toFixed(3) + ')' : '');
    css(el, 'filter', k > 0 ? 'brightness(' + (1 - .1 * k).toFixed(3) + ')' : '');
  }
  function presses(el, t, list) { var best = -9; list.forEach(function (tc) { if (Math.abs(t - tc) < Math.abs(t - best)) best = tc; }); press(el, t, best); }
  function glow(el, k, col) { css(el, 'boxShadow', k > .001 ? '0 0 0 ' + (2 + 4 * k).toFixed(1) + 'px rgba(' + (col || 'var(--accent-rgb)') + ',' + (.35 * k).toFixed(2) + ')' : ''); }
  function pq(el, map) {
    if (!el) return;
    if (el.hasAttribute('data-pq')) el.removeAttribute('data-pq');
    ['home', 'send', 'spend'].forEach(function (k) { var s = el.querySelector('.pq-' + k); if (s) op(s, map[k] || 0); });
  }
  function prog(el, t, list) {
    var k = -1; list.forEach(function (a) { if (t >= a && t < a + .75) k = (t - a) / .75; });
    op(el, k < 0 ? 0 : (k > .8 ? (1 - k) / .2 : 1));
    css(el, 'width', k < 0 ? '0' : (eo(Math.min(1, k * 1.25)) * 100).toFixed(1) + '%');
  }
  function tabGrow(el, t, a) {
    css(el, 'transform', t >= a ? 'scaleX(' + (.3 + .7 * eo(r(t, a, a + .25))).toFixed(3) + ')' : '');
    cls(el, 'load', within(t, a, a + .7)); if (within(t, a, a + .7)) el.style.setProperty('--spin', ((t * 720) % 360).toFixed(0) + 'deg');
  }
  function show(el, o) { css(el, 'display', o > 0 ? '' : 'none'); if (o > 0) op(el, Math.min(1, o)); } // far scenes leave the layout (P2-5)
  var LEN = 214, NARROW = false, LASTSC = '';
  var TILT = 'rotateY(-7deg) rotateX(3deg)';

  function at(t) {
    if (!S) return;
    var s, tx = 0, ty = 0, maya = t >= 22.45 && t < 34.4;
    if (NARROW) {
      var c = cam(t); s = VW / c[2];
      tx = VW / 2 - c[0] * s; ty = VH / 2 - c[1] * s;
      var F0 = maya ? MF0 : FR0, FW = maya ? MFW : FRW; // keep the camera on the window, never the stage behind it
      tx = Math.min(-F0[0] * s, Math.max(VW - (F0[0] + FW[0]) * s, tx)); ty = Math.min(-(F0[1] - 6) * s, Math.max(VH - (F0[1] + FW[1]) * s, ty));
    } else s = VW / 1540;
    css(world, 'transform', 'translate(' + tx.toFixed(1) + 'px,' + ty.toFixed(1) + 'px) scale(' + s.toFixed(5) + ')');

    // the handover, no movement: the owner's sent message holds, the window fades out, Maya's fades in where the same
    // message is arriving. Her window is narrower, dark, labelled inside its tab strip.
    var own = 1 - sm(r(t, 22.0, 22.4)) * (1 - sm(r(t, 34.35, 34.75)));
    var mon = sm(r(t, 22.45, 22.9)) * (1 - sm(r(t, 34.0, 34.35)));
    show(S.frame, own); css(S.frame, 'transform', NARROW ? '' : TILT);
    show(S.mframe, mon); css(S.mframe, 'transform', NARROW ? '' : TILT);

    var cur = scene(t), mcur = t < 24.3 ? 'wa' : t < 26.4 ? 'w' : t < 27.6 ? 'p' : 't';
    if (cur + mcur !== LASTSC) { LASTSC = cur + mcur; if (W.GlassV3 && W.GlassV3.refresh) try { W.GlassV3.refresh(); } catch (e) { /* glass is optional */ } }
    Object.keys(S.sc).forEach(function (k) {
      var o = 0;
      SCENES.forEach(function (sc) { if (sc[0] === k) o = Math.max(o, (sc[1] === 0 ? 1 : sm(r(t, sc[1] - .2, sc[1]))) * (1 - sm(r(t, sc[2] - .2, sc[2])))); });
      show(S.sc[k], own > 0 ? o : 0);
    });
    txt(S.url, URL[cur]);
    var dk = cur === 'watch' || cur === 'ins' ? 'dark' : 'light';
    if (S.frame._th !== dk) { S.frame._th = dk; S.frame.setAttribute('data-theme', dk); }
    ['claude', 'aero', 'wa'].forEach(function (k) { cls(S.tabs[k], 'show', 1); });
    var siteTab = t >= 10.75 && t < 45.75;
    cls(S.tabs.site, 'show', siteTab);
    if (siteTab) tabGrow(S.tabs.site, t, 10.75); else { css(S.tabs.site, 'transform', ''); cls(S.tabs.site, 'load', 0); }
    Object.keys(S.tabs).forEach(function (k) { cls(S.tabs[k], 'on', (TABON[cur] || 'aero') === k); });
    prog(S.prog, t, LOADS);
    glow(S.urlBox, io(t, 10.75, 10.95, 12.3, 12.7));

    // 1 Claude: paste, send, Claude works, it's live. The conversation clears before Claude comes back at the seam.
    var pasted = t >= 1.5 && t < 3.55;
    cls(S.inp, 'pasted', pasted); cls(S.paste, 'on', pasted); cls(S.paste, 'sel', within(t, 1.5, 2.0));
    press(S.inp, t, 1.3); press(S.send, t, 3.5);
    var conv = t < 48.8 ? 1 : 0;
    op(S.sent, sm(r(t, 3.55, 3.8)) * conv);
    op(S.reply, sm(r(t, 3.9, 4.1)) * conv);
    var pub = t >= 5.6;
    css(S.work, 'display', pub ? 'none' : 'inline-flex');
    css(S.used, 'display', pub ? 'inline-flex' : 'none'); css(S.done, 'display', pub ? 'block' : 'none');
    op(S.done, sm(r(t, 5.6, 5.9)));
    glow(S.used, io(t, 5.6, 5.75, 6.8, 7.2), '94,140,74');
    var keyAt = t < 10 ? 1.35 : 20.15, keyP = t < 10 ? P.inp : P['wa:field'];
    if (S.key && keyP) { op(S.key, io(t, keyAt, keyAt + .1, keyAt + .65, keyAt + .8)); css(S.key, 'transform', 'translate(' + (keyP[0] - 60).toFixed(0) + 'px,' + (keyP[1] - 54).toFixed(0) + 'px)'); }

    // 2 Aero: Published (the page updated by itself); the site's page, live; Visit opens a new tab, which loads
    glow(S.pdone, io(t, 7.4, 7.6, 8.1, 8.4), '31,143,95');
    if (S.pcopy) { cls(S.pcopy, 'copied', within(t, 48.25, 49.4)); press(S.pcopy, t, 48.2); }
    if (S.banner) { var bk = t > 13 ? 1 : eo(r(t, 8.6, 9.0)); op(S.banner, bk); css(S.banner, 'transform', 'translateY(' + ((1 - bk) * -10).toFixed(1) + 'px)'); }
    glow(S.live, io(t, 9.1, 9.3, 9.9, 10.2), '31,143,95'); css(S.live, 'borderRadius', '6px');
    press(S.visit, t, 10.7); presses(S.tabs.aero, t, [7.25, 13.15]); press(S.more, t, 14.4); press(S.mi, t, 16.0); press(S.copy, t, 18.6);
    presses(S.tabs.claude, t, [49.15]); press(S.tabs.wa, t, 19.6); press(S.tabX, t, 45.7); press(S.sbSites, t, 46.5); press(S.newsite, t, 47.4);
    op(S.blank, 1 - sm(r(t, 11.3, 11.55)));
    // 3 Test: ⋯, the menu opens, rest on "User test this site" for 1.2 s, click; "Test created"; copy the link
    if (S.menu) { var on = within(t, 14.42, 16.15), mk = eo(r(t, 14.42, 14.62));
      op(S.menu, on ? 1 : 0); css(S.menu, 'clipPath', on ? 'inset(0 0 ' + ((1 - mk) * 100).toFixed(1) + '% 0 round 12px)' : '');
      css(S.menu, 'transform', on ? 'translateY(' + ((1 - mk) * -6).toFixed(1) + 'px)' : ''); }
    cls(S.mi, 'hv-hover', within(t, 14.8, 16.15));
    if (S.made) { var crt = eo(r(t, 16.35, 16.75)); op(S.made, crt); css(S.made, 'transform', 'translateY(' + ((1 - crt) * -12).toFixed(1) + 'px)'); }
    glow(S.made, io(t, 16.5, 16.7, 17.6, 18.0), '31,143,95');
    cls(S.copy, 'copied', within(t, 18.65, 20));
    // 4 the owner's WhatsApp: the testers' group is open; paste the link, send. It holds before the cut.
    var typed = within(t, 20.25, 21.1);
    cls(S.oField, 'typed', typed); cls(S.oInp, 'typing', typed); press(S.oField, t, 20.1); press(S.oSend, t, 21.05);
    if (S.oNew) { var nb = eo(r(t, 21.1, 21.35)); css(S.oNew, 'display', t >= 21.1 ? '' : 'none'); op(S.oNew, nb); css(S.oNew, 'transform', 'translateY(' + ((1 - nb) * 10).toFixed(1) + 'px)'); }

    // the cursor
    var cp = curPos(t), cOn = 0;
    CURON.forEach(function (a) { cOn = Math.max(cOn, (a[0] === 0 ? 1 : sm(r(t, a[0], a[0] + .3))) * (1 - sm(r(t, a[1] - .3, a[1])))); });
    if (cp && cOn > 0) { op(S.cur, cOn); css(S.cur, 'transform', 'translate(' + (cp[0] - 5).toFixed(1) + 'px,' + (cp[1] - 3).toFixed(1) + 'px)'); }
    else op(S.cur, 0);
    var ring = 0, rp = null;
    CLICKS.forEach(function (c) { var k = r(t, c[0], c[0] + .45); if (k > 0 && k < 1) { ring = k; rp = P[c[1]]; } });
    if (rp) { op(S.ring, 1 - ring); css(S.ring, 'transform', 'translate(' + rp[0].toFixed(1) + 'px,' + rp[1].toFixed(1) + 'px) scale(' + (.5 + .7 * eo(ring)).toFixed(3) + ')'); }
    else op(S.ring, 0);

    // 5 Maya's computer: the message arrives in the group she's reading; she opens the link; the test runs.
    if (mon > 0) {
      var arrived = t >= 23.0;
      if (S.mNew) { var na = eo(r(t, 23.0, 23.3)); css(S.mNew, 'display', arrived ? '' : 'none'); op(S.mNew, na); css(S.mNew, 'transform', 'translateY(' + ((1 - na) * 12).toFixed(1) + 'px)'); }
      txt(S.mLast, arrived ? 'Mia Chen: Could you try this for me?' : S.mLast0); txt(S.mTime, arrived ? '21:04' : '20:58');
      glow(S.mLink, io(t, 23.6, 23.8, 24.0, 24.3)); press(S.mLink, t, 24.1);
      Object.keys(S.ms).forEach(function (k) {
        var o = 0; MS.forEach(function (m) { if (m[0] === k) o = Math.max(o, (m[1] === 0 ? 1 : sm(r(t, m[1] - .15, m[1] + .05))) * (1 - sm(r(t, m[2] - .15, m[2])))); });
        show(S.ms[k], o);
      });
      txt(S.murl, t < 24.3 ? 'web.whatsapp.com' : 'aeroapp.ai/t/pocket-7k2');
      cls(S.mtabs.wa, 'show', 1);
      cls(S.mtabs.ctl, 'show', t >= 24.3); if (t >= 24.3) tabGrow(S.mtabs.ctl, t, 24.3);
      cls(S.mtabs.pk, 'show', t >= 27.6); if (t >= 27.6) tabGrow(S.mtabs.pk, t, 27.6);
      cls(S.mtabs.wa, 'on', t < 24.3); cls(S.mtabs.ctl, 'on', within(t, 24.3, 27.6)); cls(S.mtabs.pk, 'on', t >= 27.6);
      prog(S.mprog, t, [24.3, 27.6]);
      press(S.mcont, t, 26.2); press(S.mshare, t, 27.4);
      op(S.rec, eo(r(t, 27.8, 28.1)));
      var sd = sm(r(t, 28.6, 28.85)) * (1 - sm(r(t, 30.3, 30.55))), sp = sm(r(t, 30.9, 31.15));
      pq(S.tpq, { home: 1 - Math.max(sd, sp), send: sd, spend: sp });
      var k2 = sm(r(t, 30.25, 30.5)); op(S.tk1, 1 - k2); op(S.tk2, k2);
      press(S.done1, t, 30.0);
      // her voice: the level meter in the Recording chip moves while she speaks; what she says sits beside the window
      var talking = within(t, 28.2, 30.0) || within(t, 31.3, 33.6);
      S.meter.forEach(function (b, i) {
        var v = talking ? .25 + .75 * Math.abs(Math.sin(t * 9.1 + i * 1.3) * Math.sin(t * 2.3 + i * .7)) : .2;
        css(b, 'height', (v * 100).toFixed(0) + '%');
      });
    }
    op(S.say[0], io(t, 28.2, 28.5, 30.6, 30.9) * mon); op(S.say[1], io(t, 31.3, 31.6, 33.7, 34.0) * mon);

    // 6 Review, in dark. No cursor here.
    if (cur === 'watch' || cur === 'ins') {
      var sess = 80 + (152 - 80) * r(t, 35.0, 38.4);
      S.lines.forEach(function (l, i) {
        var nx = S.lines[i + 1] ? S.lines[i + 1]._s : LEN, st = sess < l._s ? 'future' : sess >= nx ? 'past' : 'cur';
        if (l._st !== st) { l.className = 'tl ' + st; l._st = st; if (st !== 'cur') l._w.forEach(function (w) { w.className = 'w'; }); }
        if (st === 'cur') {
          var f = (sess - l._s) / Math.min(14, nx - l._s), n = l._w.length, k = Math.floor(f * n);
          l._w.forEach(function (w, j) { var c = 'w' + (j < k ? ' said' : j === k ? ' now' : ''); if (w._cl !== c) { w._cl = c; w.className = c; } });
        }
      });
      var pp = sess / LEN;
      css(S.ph, 'left', (pp * 100).toFixed(2) + '%');
      S.bars.forEach(function (b, i) { cls(b, 'p', i / S.bars.length < pp); });
      txt(S.tc, ('0' + Math.floor(sess / 60)).slice(-2) + ':' + ('0' + Math.floor(sess % 60)).slice(-2));
      pq(S.vpq, { home: sess < 92 ? 1 : 0, spend: sess >= 92 ? 1 : 0 });
      var t2 = sess >= 74;
      txt(S.tpn, t2 ? 'Task 2 of 2' : 'Task 1 of 2'); txt(S.tpt, t2 ? 'Find what you spent on eating out' : 'Send £20 to Sam');
      S.marks.forEach(function (m) { var x = parseFloat(m.style.left) / 100 * LEN; cls(m, 'hot', sess >= x && sess < x + 14); });
      // Insights: the summary alone for 2.5 s, then the issues one by one, then a hold
      S.iss.forEach(function (el, i) { var a0 = i === 0 ? 38.7 : 41.2 + .45 * (i - 1), k = eo(r(t, a0, a0 + .5)); op(el, k); css(el, 'transform', 'translateY(' + ((1 - k) * 18).toFixed(1) + 'px)'); });
    }

    // the steps: Publish from the owner's return to Aero (45.0 s); Test 13.2; Review 34.6
    var u = (t - JUMP[0] + T) % T, b1 = (JUMP[1] - JUMP[0] + T) % T, b2 = (JUMP[2] - JUMP[0] + T) % T;
    [[0, b1], [b1, b2], [b2, T]].forEach(function (ab, i) {
      var st = S.steps[i]; if (!st) return;
      css(st.querySelector('.hm-bar b'), 'width', (r(u, ab[0], ab[1]) * 100).toFixed(1) + '%');
      cls(st, 'on', u >= ab[0] && u < ab[1]);
    });
  }
  var JUMP = [45.0, 13.2, 34.6], JT = [46.4, 13.2, 34.6]; // JT: where a click lands (Publish: just as Sites is clicked)
  // Pace: the paste, the send and Claude "working" get more time. Times above are script time; the visitor's clock
  // runs through warp(), which stretches script 1.4 to 7.3 s over 1.4 to 10.1 s.
  var WA0 = 1.4, WA1 = 7.3, WSTR = 2.7, TR = T + WSTR;
  function warp(rt) { return rt < WA0 ? rt : rt < WA1 + WSTR ? WA0 + (rt - WA0) * (WA1 - WA0) / (WA1 - WA0 + WSTR) : rt - WSTR; }
  function unwarp(st) { return st < WA0 ? st : st < WA1 ? WA0 + (st - WA0) * (WA1 - WA0 + WSTR) / (WA1 - WA0) : st + WSTR; }
  W.__heroAt = function (rt) { clock = rt; fit(); at(warp(rt)); };
  W.__heroT = TR; W.__unwarp = unwarp;


  var last = null, playing = true, visible = false, started = false, raf = 0, clock = 0;
  function loop(now) {
    raf = 0;
    if (last != null) clock = (clock + Math.min(.1, (now - last) / 1000)) % TR;
    last = now; at(warp(clock));
    if (playing && visible && !D.hidden) raf = requestAnimationFrame(loop); else last = null;
  }
  function kick() { if (!raf && playing && visible && !D.hidden && !RM && !Q.has('t')) raf = requestAnimationFrame(loop); }
  // Pause (P2-9): no button on the stage (it clashed with the tester screen). Pressing the step that's playing pauses
  // and plays; Space or Enter on the focused stage does the same. A hidden live region says which.
  var live = $('#hm-live'), stepsEl = $('.hm-steps');
  function setPlaying(v) {
    playing = v; last = null; kick();
    if (stepsEl) stepsEl.classList.toggle('paused', !v);
    $$('.hm-stepb').forEach(function (b) { b.setAttribute('aria-pressed', b.parentNode.classList.contains('on') && !v ? 'true' : 'false'); });
    if (live) live.textContent = v ? 'Playing' : 'Paused';
  }
  var stage = $('.hm-stage');
  if (stage) stage.addEventListener('keydown', function (e) {
    if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); setPlaying(!playing); }
  });
  D.addEventListener('visibilitychange', kick);
  // Publish, Test, Review are buttons: jump to the start of that step; the one that's playing pauses and plays
  $$('.hm-stepb').forEach(function (b, i) {
    b.addEventListener('click', function () {
      if (b.parentNode.classList.contains('on') && !RM) { setPlaying(!playing); return; }
      clock = unwarp(JT[i]); started = true; fit(); at(JT[i]); setPlaying(!RM);
    });
  });

  /* ---------- section loops run while in view; the hero starts from 0 the first time it is 60% in view (P1-4) ---------- */
  var imgs = $$('.hm-img');
  if ('IntersectionObserver' in W) {
    var io2 = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        if (en.target.classList.contains('hm-stage')) {
          if (!started && en.intersectionRatio >= .6) { started = true; clock = 0; at(0); }
          visible = started && en.intersectionRatio >= .15; kick();
        } else if (!RM) en.target.classList.toggle('is-running', en.isIntersecting);
      });
    }, { threshold: [0, .15, .6] });
    imgs.forEach(function (i) { io2.observe(i); });
    var stg = $('.hm-stage'); if (stg) io2.observe(stg);
  } else { started = visible = true; }

  function start() {
    fit(); rotW();
    if (Q.has('t')) { clock = +Q.get('t') || 0; at(warp(clock)); return; }
    if (RM) { at(29.2); S && S.steps.forEach(function (s) { s.querySelector('.hm-bar b').style.width = '100%'; }); return; }
    at(0); kick();
  }
  W.addEventListener('resize', function () { fit(); rotW(); at(warp(clock)); });
  if (D.fonts && D.fonts.ready) D.fonts.ready.then(start); else W.addEventListener('load', start);
})();
