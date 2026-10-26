/* Aero homepage, round 7 (Team H).
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

  /* ---------- hero loop (47.6 s). The owner's browser at an angle; for the test, Maya's own screen tilted the other
     way. The end flows into the start: after Insights the owner goes to Sites, New site, copies the prompt and
     switches to Claude, which is where the loop begins. Every state is computed from t. ---------- */
  var T = 47.6;
  var $ = function (s, r) { return (r || D).querySelector(s); }, $$ = function (s, r) { return [].slice.call((r || D).querySelectorAll(s)); };
  var world = $('.st-world');
  function cl(x) { return x < 0 ? 0 : x > 1 ? 1 : x; }
  function r(t, a, b) { return cl((t - a) / (b - a)); }
  function sm(x) { return x * x * (3 - 2 * x); }
  function eo(x) { return 1 - Math.pow(1 - x, 3); }
  function io(t, a, b, c, d) { return sm(r(t, a, b)) * (1 - sm(r(t, c, d))); }
  function within(t, a, b) { return t >= a && t < b; }

  var OW = $('.hv-frame:not(.hv-mframe)'), MF = $('.hv-mframe');
  var S = world && {
    frame: OW, url: $('.hv-u', OW), urlBox: $('.hv-url', OW), prog: $('.hv-prog', OW),
    cur: $('.hv-cur'), ring: $('.hv-ring'), key: $('.hv-key'), tabs: {}, sc: {},
    sent: $('.cl-sent'), reply: $('.cl-reply'), work: $('.cl-work'), used: $('.cl-used'), done: $('.cl-done'),
    inp: $('[data-sc=claude] .cl-inp'), paste: $('[data-sc=claude] .cl-paste'), send: $('[data-sc=claude] .cl-send'),
    pdone: $('.hv-pdone'), pwait: $('[data-sc=prompt] .x-waitb'), pcopy: $('[data-sc=prompt] .x-pba .btn'),
    banner: $('[data-sc=aero] .x-justpub'), live: $('[data-sc=aero] .x-addr .st.live'), visit: $('[data-sc=aero] .hv-visit'),
    more: $('[data-sc=aero] .x-morew .gbtn'), menu: $('[data-sc=aero] .x-menu-open'), mi: $('[data-sc=aero] .x-mi2'),
    blank: $('.hv-blank'), made: $('[data-sc=setup] .x-made'), copy: $('[data-sc=setup] .x-lk .btn'),
    owa: $('[data-wa=owner]'), oRow: $('[data-wa=owner] .wa-hot'), oEmpty: $('[data-wa=owner] .wa-empty'), oField: $('[data-wa=owner] .wa-field'),
    oSend: $('[data-wa=owner] .wa-send'), oNew: $('[data-wa=owner] .wa-new'), oTick: $('[data-wa=owner] .wa-new .wa-tick'),
    mframe: MF, murl: $('.hv-u', MF), mprog: $('.hv-prog', MF), mtabs: {}, ms: {},
    mRow: $('[data-wa=maya] .wa-hot'), mBadge: $('[data-wa=maya] .wa-hot .wa-badge'), mLast: $('[data-wa=maya] .wa-hot .wa-last'), mEmpty: $('[data-wa=maya] .wa-empty'),
    mNew: $('[data-wa=maya] .wa-new'), mLink: $('[data-wa=maya] .wa-new .wa-link'), mList: $('[data-wa=maya] .wa-list'),
    mcont: $('[data-ms=w] .x-tgo .btn'), mshare: $('[data-ms=p] .hv-share'), sayi: $('.hv-sayi'), q: $$('.hv-q'),
    tpq: $('[data-ms=t] .pq-wrap'), tk1: $('[data-ms=t] .st-tk1'), tk2: $('[data-ms=t] .st-tk2'), done1: $('[data-ms=t] .st-tk1 .st-done'), rec: $('[data-ms=t] .x-recchip'),
    lines: $$('.st-trs .tl[data-s]'), ph: $('[data-sc=watch] .ph-line'), bars: $$('[data-sc=watch] .tline .wave i'), tc: $('.st-tc'), vpq: $('.st-vid .pq-wrap'),
    tpn: $('.st-tpn'), tpt: $('.st-tpt'), marks: $$('[data-sc=watch] .tline .marks .m'), iss: $$('[data-sc=ins] .iss, [data-sc=ins] .sumcard2'),
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
    S.oWaRows = $$('[data-wa=owner] .wa-row'); S.mWaRows = $$('[data-wa=maya] .wa-row');
  }

  // the owner's window: which page, when (crossfades 0.2 s)
  var SCENES = [['claude', 0, 7.3], ['prompt', 7.3, 8.5], ['aero', 8.5, 10.75], ['site', 10.75, 13.2], ['aero', 13.2, 16.1], ['setup', 16.1, 19.65],
                ['wa', 19.65, 36.6], ['watch', 36.6, 40.6], ['ins', 40.6, 44.7], ['sites', 44.7, 45.6], ['prompt', 45.6, 47.25], ['claude', 47.25, 99]];
  var URL = { claude: 'claude.ai/chat/pocket', prompt: 'aeroapp.ai/new?from=prompt', aero: 'aeroapp.ai/sites/pocket', site: 'pocket.aeroapp.ai',
              setup: 'aeroapp.ai/tests/pocket/setup', wa: 'web.whatsapp.com', watch: 'aeroapp.ai/tests/pocket/sessions/2', ins: 'aeroapp.ai/tests/pocket/insights', sites: 'aeroapp.ai/sites' };
  var TABON = { claude: 'claude', site: 'site', wa: 'wa' };
  var LOADS = [8.5, 10.75, 16.1, 44.7, 45.6];
  var MS = [['wa', 0, 26.5], ['w', 26.5, 28.6], ['p', 28.6, 29.8], ['t', 29.8, 99]];
  var MURL = function (t) { return t < 26.5 ? 'web.whatsapp.com' : 'aeroapp.ai/t/pocket-7k2'; };
  function scene(t) { for (var i = 0; i < SCENES.length; i++) if (t < SCENES[i][2]) return SCENES[i][0]; return 'claude'; }

  // the owner's cursor (never on Maya's screen, never in the review): [time, target]
  var P = {};
  var CUR = [[0, 'tab:claude'], [1.2, 'inp'], [3.0, 'inp'], [3.45, 'send'], [6.6, 'send'], [7.2, 'tab:aero'], [9.4, 'tab:aero'], [10.6, 'visit'],
             [12.4, 'visit2'], [13.1, 'tab:aero'], [13.6, 'tab:aero'], [14.3, 'more'], [14.7, 'more'], [15.3, 'mi'], [15.9, 'mi'], [16.6, 'mi3'],
             [18.0, 'mi3'], [18.5, 'copy'], [19.0, 'copy'], [19.55, 'tab:wa'], [19.9, 'tab:wa'], [20.35, 'wa:row'], [20.7, 'wa:row'], [21.05, 'wa:field'],
             [21.6, 'wa:field'], [22.05, 'wa:send'], [23.3, 'wa:send'],
             [43.0, 'ins:park'], [43.7, 'tabx'], [43.9, 'tabx'], [44.5, 'sb:sites'], [44.9, 'sb:sites'], [45.4, 'newsite'], [45.8, 'newsite'], [46.2, 'pcopy'],
             [46.5, 'pcopy'], [47.15, 'tab:claude'], [T, 'tab:claude']];
  var CLICKS = [[1.3, 'inp'], [3.5, 'send'], [7.25, 'tab:aero'], [10.7, 'visit'], [13.15, 'tab:aero'], [14.4, 'more'], [16.0, 'mi'], [18.6, 'copy'],
                [19.6, 'tab:wa'], [20.4, 'wa:row'], [21.1, 'wa:field'], [22.1, 'wa:send'],
                [43.8, 'tabx'], [44.6, 'sb:sites'], [45.5, 'newsite'], [46.3, 'pcopy'], [47.2, 'tab:claude']];
  var CURON = [[0, 23.6], [43.0, 99]];
  function curPos(t) {
    for (var i = 1; i < CUR.length; i++) if (t <= CUR[i][0]) {
      var a = P[CUR[i - 1][1]], b = P[CUR[i][1]], k = sm(r(t, CUR[i - 1][0], CUR[i][0]));
      if (!a || !b) return null;
      return [a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k];
    }
    return P[CUR[CUR.length - 1][1]];
  }

  var FR0 = [30, 40], MF0 = [70, 40];
  function measure() {
    if (!S) return;
    var wt = world.style.transform, ft = S.frame.style.transform, mt = S.mframe.style.transform;
    world.style.transform = 'none'; S.frame.style.transform = 'none'; S.mframe.style.transform = 'none';
    var fr = S.frame.getBoundingClientRect(), wr = world.getBoundingClientRect(), keep = [];
    function vis(el) { var s = el; while (s && s !== world) { if (s.classList && (s.classList.contains('hv-sc') || s.classList.contains('hv-ms') || s.classList.contains('wa-empty'))) { keep.push([s, s.style.opacity, s.style.display]); s.style.opacity = '1'; } s = s.parentElement; } }
    function pt(name, el, fx, fy) {
      if (!el) return; vis(el);
      var b = el.getBoundingClientRect();
      P[name] = [b.left - fr.left + b.width * (fx == null ? .5 : fx), b.top - fr.top + b.height * (fy == null ? .55 : fy)];
      P[name + '#'] = [b.left - wr.left + b.width * (fx == null ? .5 : fx), b.top - wr.top + b.height * (fy == null ? .5 : fy)];
    }
    var shown = $$('.hv-tab').map(function (x) { var o = x.classList.contains('show'); x.classList.add('show'); return [x, o]; });
    var empties = $$('.wa-empty').map(function (x) { var d = x.style.display; x.style.display = 'none'; return [x, d]; });
    pt('inp', S.inp, .45, .5); pt('send', S.send); pt('tab:aero', S.tabs.aero, .4); pt('tab:claude', S.tabs.claude, .4); pt('tab:wa', S.tabs.wa, .4); pt('tabx', S.tabX); pt('visit', S.visit);
    var mo = S.menu && S.menu.style.opacity; if (S.menu) S.menu.style.opacity = '1';
    pt('more', S.more); pt('mi', S.mi, .3, .4); pt('cam:menu', S.menu, .5, .4); if (S.menu) S.menu.style.opacity = mo;
    pt('copy', S.copy); pt('pcopy', S.pcopy); pt('sb:sites', S.sbSites, .3); pt('newsite', S.newsite);
    pt('wa:row', S.oRow, .3); pt('wa:field', S.oField, .3); pt('wa:send', S.oSend);
    pt('cam:claude', $('[data-sc=claude] .cl-msgs'), .5, .3); pt('cam:msgs', $('[data-sc=claude] .cl-msgs'), .5, .75); pt('cam:pdone', S.pdone, .4);
    pt('cam:banner', S.banner, .3); pt('cam:site', $('[data-sc=site] .pk-hero'), .3); pt('cam:setup', S.made, .3);
    pt('cam:wamsgs', $('[data-wa=owner] .wa-msgs'), .6, .85);
    pt('cam:video', $('[data-sc=watch] .stage3')); pt('cam:trs', $('[data-sc=watch] .st-trs'), .5, .4); pt('cam:sum', $('[data-sc=ins] .sumcard2'), .4, .8);
    pt('cam:sites', $('[data-sc=sites] .mhead'), .7, 3); pt('cam:prompt', $('[data-sc=prompt] .x-pbox'), .4);
    pt('cam:mlist', S.mList, .5, .2); pt('cam:mnew', S.mNew, .4); pt('cam:wcard', $('[data-ms=w] .x-tcard')); pt('cam:pcard', $('[data-ms=p] .x-tcard'));
    pt('cam:tk', $('[data-ms=t] .st-tk1 .x-tk'), .9, .3); pt('cam:rec', S.rec, .5, 3);
    keep.forEach(function (k) { k[0].style.opacity = k[1]; });
    empties.forEach(function (x) { x[0].style.display = x[1]; });
    shown.forEach(function (x) { if (!x[1]) x[0].classList.remove('show'); });
    P.mi3 = P.mi && [P.mi[0] + 40, P.mi[1] + 6];
    P.visit2 = P.visit && [P.visit[0] - 140, P.visit[1] + 240];
    P['ins:park'] = P['sb:sites'] && [P['sb:sites'][0] + 420, P['sb:sites'][1] + 160];
    world.style.transform = wt; S.frame.style.transform = ft; S.mframe.style.transform = mt;
  }

  // phone width: windows flat, the camera follows the action. [time, target]
  var CAM = [[0, 'cam:claude'], [1.0, 'inp'], [4.2, 'cam:msgs'], [6.8, 'tab:aero'], [7.6, 'cam:pdone'], [8.8, 'cam:banner'], [10.0, 'visit'], [11.4, 'cam:site'],
             [12.6, 'tab:aero'], [14.0, 'cam:menu'], [16.6, 'cam:setup'], [18.2, 'copy'], [19.4, 'tab:wa'], [20.3, 'wa:row'], [21.4, 'cam:wamsgs'],
             [24.6, 'cam:mlist#'], [25.9, 'cam:mnew#'], [27.0, 'cam:wcard#'], [28.8, 'cam:pcard#'], [30.0, 'cam:rec#'], [31.2, 'cam:tk#'], [33.6, 'cam:tk#'],
             [37.0, 'cam:video'], [38.4, 'cam:trs'], [40.8, 'cam:sum'], [43.2, 'tabx'], [44.2, 'sb:sites'], [44.9, 'cam:sites'], [45.8, 'cam:prompt'], [46.8, 'tab:claude'], [T + 1, 'cam:claude']];
  function wpt(name) { var p = P[name]; if (!p) return null; return name.slice(-1) === '#' ? p : [p[0] + FR0[0], p[1] + FR0[1]]; }
  function cam(t) {
    var i = 0; while (i < CAM.length - 1 && t >= CAM[i + 1][0]) i++;
    var a = wpt(CAM[i][1]) || [740, 500], n = CAM[i + 1], b = n ? wpt(n[1]) || a : a, k = n ? sm(r(t, n[0] - .8, n[0])) : 0;
    return [a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k];
  }

  function press(el, t, tc) {
    if (!el) return;
    var k = Math.sin(Math.PI * r(t, tc - .04, tc + .24));
    el.style.transform = k > 0 ? 'scale(' + (1 - .07 * k).toFixed(3) + ')' : '';
    el.style.filter = k > 0 ? 'brightness(' + (1 - .1 * k).toFixed(3) + ')' : '';
  }
  function presses(el, t, list) { var best = -9; list.forEach(function (tc) { if (Math.abs(t - tc) < Math.abs(t - best)) best = tc; }); press(el, t, best); }
  function glow(el, k, col) { if (el) el.style.boxShadow = k > .001 ? '0 0 0 ' + (2 + 4 * k).toFixed(1) + 'px rgba(' + (col || 'var(--accent-rgb)') + ',' + (.35 * k).toFixed(3) + ')' : ''; }
  function pq(el, map) {
    if (!el) return;
    el.removeAttribute('data-pq');
    ['home', 'send', 'spend'].forEach(function (k) { var s = el.querySelector('.pq-' + k); if (s) s.style.opacity = (map[k] || 0).toFixed(3); });
  }
  function prog(el, t, list) {
    var k = -1; list.forEach(function (a) { if (t >= a && t < a + .75) k = (t - a) / .75; });
    if (!el) return;
    el.style.opacity = k < 0 ? '0' : (k > .8 ? ((1 - k) / .2).toFixed(2) : '1');
    el.style.width = k < 0 ? '0' : (eo(Math.min(1, k * 1.25)) * 100).toFixed(1) + '%';
  }
  function tabGrow(el, t, a) { el.style.transform = t >= a ? 'scaleX(' + (.3 + .7 * eo(r(t, a, a + .25))).toFixed(3) + ')' : ''; el.classList.toggle('load', within(t, a, a + .7)); el.style.setProperty('--spin', ((t * 720) % 360).toFixed(0) + 'deg'); }
  var LEN = 214, NARROW = false, LASTSC = '';
  var TILT = ' rotateY(-7deg) rotateX(3deg)', MTILT = ' rotateY(7deg) rotateX(3deg)';

  function at(t) {
    if (!S) return;
    var s, tx = 0, ty = 0;
    if (NARROW) {
      s = VW / 720; var c = cam(t);
      tx = VW / 2 - c[0] * s; ty = VH / 2 - c[1] * s;
      tx = Math.min(0, Math.max(VW - 1540 * s, tx)); ty = Math.min(0, Math.max(VH - 1090 * s, ty));
    } else s = VW / 1540;
    world.style.transform = 'translate(' + tx.toFixed(1) + 'px,' + ty.toFixed(1) + 'px) scale(' + s.toFixed(5) + ')';

    // the owner's window slides out to the left for Maya's part and back for the review; hers comes in from the right
    var oOut = sm(r(t, 23.4, 24.0)), oIn = sm(r(t, 36.6, 37.2)), off = t < 30 ? oOut : 1 - oIn;
    S.frame.style.opacity = (1 - off).toFixed(3);
    S.frame.style.transform = 'translateX(' + (-off * 1700).toFixed(0) + 'px)' + (NARROW ? '' : TILT);
    var mIn = eo(r(t, 23.8, 24.5)), mOut = sm(r(t, 36.3, 36.8)), mon = t < 30 ? mIn : 1 - mOut;
    S.mframe.style.opacity = mon.toFixed(3);
    S.mframe.style.transform = 'translateX(' + ((1 - mon) * 1700).toFixed(0) + 'px)' + (NARROW ? '' : MTILT);

    var cur = scene(t), mcur = t < 26.5 ? 'wa' : t < 28.6 ? 'w' : t < 29.8 ? 'p' : 't';
    if (cur + mcur !== LASTSC) { LASTSC = cur + mcur; if (W.GlassV3 && W.GlassV3.refresh) try { W.GlassV3.refresh(); } catch (e) { /* glass is optional */ } } // glass buttons that just appeared pick up their surroundings
    Object.keys(S.sc).forEach(function (k) {
      var o = 0;
      SCENES.forEach(function (sc) { if (sc[0] === k) o = Math.max(o, (sc[1] === 0 ? 1 : sm(r(t, sc[1] - .2, sc[1]))) * (1 - sm(r(t, sc[2] - .2, sc[2])))); });
      S.sc[k].style.opacity = Math.min(1, o).toFixed(3);
    });
    S.url.textContent = URL[cur];
    S.frame.setAttribute('data-theme', cur === 'watch' || cur === 'ins' ? 'dark' : 'light');
    ['claude', 'aero', 'wa'].forEach(function (k) { S.tabs[k].classList.add('show'); });
    var siteTab = t >= 10.75 && t < 43.85;
    S.tabs.site.classList.toggle('show', siteTab);
    if (siteTab) tabGrow(S.tabs.site, t, 10.75); else { S.tabs.site.style.transform = ''; S.tabs.site.classList.remove('load'); }
    Object.keys(S.tabs).forEach(function (k) { S.tabs[k].classList.toggle('on', (TABON[cur] || 'aero') === k); });
    prog(S.prog, t, LOADS);
    glow(S.urlBox, io(t, 10.75, 10.95, 12.3, 12.7));

    // 1 Claude
    var pasted = t >= 1.5 && t < 3.55;
    S.inp.classList.toggle('pasted', pasted); S.paste.classList.toggle('on', pasted); S.paste.classList.toggle('sel', within(t, 1.5, 2.0));
    press(S.inp, t, 1.3); press(S.send, t, 3.5);
    var conv = t < 47.25 ? 1 : 0;
    S.sent.style.opacity = (sm(r(t, 3.55, 3.8)) * conv).toFixed(3);
    S.reply.style.opacity = (sm(r(t, 3.9, 4.1)) * conv).toFixed(3);
    var pub = t >= 5.6;
    S.work.style.display = pub ? 'none' : 'inline-flex';
    S.used.style.display = pub ? 'inline-flex' : 'none'; S.done.style.display = pub ? 'block' : 'none';
    S.done.style.opacity = sm(r(t, 5.6, 5.9)).toFixed(3);
    glow(S.used, io(t, 5.6, 5.75, 6.8, 7.2), '94,140,74');
    var keyAt = t < 10 ? 1.35 : 21.15, keyP = t < 10 ? P.inp : P['wa:field'];
    if (S.key && keyP) { S.key.style.opacity = io(t, keyAt, keyAt + .1, keyAt + .65, keyAt + .8).toFixed(3); S.key.style.transform = 'translate(' + (keyP[0] + 24).toFixed(0) + 'px,' + (keyP[1] - 54).toFixed(0) + 'px)'; }

    // 2 Aero: the prompt page has updated by itself; the site's own page, live; Visit opens a new tab
    var fresh = t > 42;
    if (S.pdone) { S.pdone.style.display = fresh ? 'none' : ''; glow(S.pdone, io(t, 7.4, 7.6, 8.1, 8.4), '31,143,95'); }
    if (S.pwait) S.pwait.style.display = fresh ? '' : 'none';
    if (S.pcopy) { S.pcopy.classList.toggle('copied', within(t, 46.35, 47.4)); press(S.pcopy, t, 46.3); }
    if (S.banner) { var bk = eo(r(t, 8.6, 9.0)); S.banner.style.opacity = (t > 13 ? 1 : bk).toFixed(3); S.banner.style.transform = 'translateY(' + ((1 - (t > 13 ? 1 : bk)) * -10).toFixed(1) + 'px)'; }
    glow(S.live, io(t, 9.1, 9.3, 9.9, 10.2), '31,143,95'); if (S.live) S.live.style.borderRadius = '6px';
    press(S.visit, t, 10.7); presses(S.tabs.aero, t, [7.25, 13.15]); press(S.more, t, 14.4); press(S.mi, t, 16.0); press(S.copy, t, 18.6);
    presses(S.tabs.claude, t, [47.2]); press(S.tabs.wa, t, 19.6); press(S.tabX, t, 43.8); press(S.sbSites, t, 44.6); press(S.newsite, t, 45.5);
    if (S.blank) S.blank.style.opacity = (1 - sm(r(t, 11.3, 11.55))).toFixed(3);
    // 3 Test: the site's ⋯ menu, hover "User test this site", click; the test page arrives, created; copy its link
    if (S.menu) { var on = within(t, 14.42, 16.15), mk = eo(r(t, 14.42, 14.62));
      S.menu.style.opacity = on ? '1' : '0';
      S.menu.style.clipPath = on ? 'inset(0 0 ' + ((1 - mk) * 100).toFixed(1) + '% 0 round 12px)' : '';
      S.menu.style.transform = on ? 'translateY(' + ((1 - mk) * -6).toFixed(1) + 'px)' : ''; }
    if (S.mi) S.mi.classList.toggle('hv-hover', within(t, 15.25, 16.15));
    if (S.made) { var cr = eo(r(t, 16.35, 16.75)); S.made.style.opacity = cr.toFixed(3); S.made.style.transform = 'translateY(' + ((1 - cr) * -12).toFixed(1) + 'px)'; }
    glow(S.made, io(t, 16.5, 16.7, 17.6, 18.0), '31,143,95');
    if (S.copy) S.copy.classList.toggle('copied', within(t, 18.65, 20));
    // 4 WhatsApp: open Maya's chat, paste the link, send
    var chatOpen = t >= 20.45 || t < 19;
    if (S.oEmpty) S.oEmpty.style.display = chatOpen ? 'none' : '';
    S.oWaRows.forEach(function (rw) { rw.classList.toggle('on', rw === S.oRow && chatOpen); });
    press(S.oRow, t, 20.4);
    var typed = within(t, 21.25, 22.15);
    if (S.oField) { S.oField.classList.toggle('typed', typed); press(S.oField, t, 21.1); }
    press(S.oSend, t, 22.1);
    if (S.oNew) { var nb = eo(r(t, 22.15, 22.4)); S.oNew.style.display = t >= 22.15 ? '' : 'none'; S.oNew.style.opacity = nb.toFixed(3); S.oNew.style.transform = 'translateY(' + ((1 - nb) * 10).toFixed(1) + 'px)'; }
    if (S.oTick) S.oTick.style.setProperty('--wt', t >= 22.7 ? '#53BDEB' : '#8696A0');

    // the cursor
    var cp = curPos(t), cOn = 0;
    CURON.forEach(function (a) { cOn = Math.max(cOn, (a[0] === 0 ? 1 : sm(r(t, a[0], a[0] + .3))) * (1 - sm(r(t, a[1] - .3, a[1])))); });
    if (cp && cOn > 0) { S.cur.style.opacity = cOn.toFixed(3); S.cur.style.transform = 'translate(' + (cp[0] - 5).toFixed(1) + 'px,' + (cp[1] - 3).toFixed(1) + 'px)'; }
    else S.cur.style.opacity = '0';
    var ring = 0, rp = null;
    CLICKS.forEach(function (c) { var k = r(t, c[0], c[0] + .45); if (k > 0 && k < 1) { ring = k; rp = P[c[1]]; } });
    if (rp) { S.ring.style.opacity = (1 - ring).toFixed(3); S.ring.style.transform = 'translate(' + rp[0].toFixed(1) + 'px,' + rp[1].toFixed(1) + 'px) scale(' + (.5 + .7 * eo(ring)).toFixed(3) + ')'; }
    else S.ring.style.opacity = '0';

    // 5 Maya's own screen: her WhatsApp, the message arrives, she opens the link; the test runs in its own tab.
    var arrived = t >= 25.0;
    if (S.mRow && S.mList) { // her chat with Mia moves to the top when the message lands
      var mv = eo(r(t, 25.0, 25.35));
      S.mWaRows.forEach(function (rw) {
        var idx = S.mWaRows.indexOf(rw), hot = rw === S.mRow, before = idx < S.mWaRows.indexOf(S.mRow);
        rw.style.top = hot ? (-72 * S.mWaRows.indexOf(S.mRow) * mv).toFixed(1) + 'px' : (before ? (72 * mv).toFixed(1) + 'px' : '0');
        rw.style.position = 'relative'; rw.style.zIndex = hot ? 2 : 1;
      });
    }
    if (S.mNew) S.mNew.style.display = arrived ? '' : 'none';
    if (S.mBadge) S.mBadge.style.opacity = (arrived && t < 25.9 ? 1 : 0).toFixed(0);
    if (S.mLast) S.mLast.textContent = arrived ? 'Could you try this for me? Takes a few…' : 'Sure, send it over';
    var mOpen = t >= 25.7 && t < 30;
    if (S.mEmpty) S.mEmpty.style.display = mOpen ? 'none' : '';
    S.mWaRows.forEach(function (rw) { rw.classList.toggle('on', rw === S.mRow && mOpen); });
    press(S.mRow, t, 25.6);
    if (S.mLink) { glow(S.mLink, io(t, 26.0, 26.2, 26.4, 26.6)); press(S.mLink, t, 26.4); }
    Object.keys(S.ms).forEach(function (k) {
      var o = 0; MS.forEach(function (m) { if (m[0] === k) o = Math.max(o, (m[1] === 0 ? 1 : sm(r(t, m[1] - .15, m[1] + .05))) * (1 - sm(r(t, m[2] - .15, m[2])))); });
      S.ms[k].style.opacity = o.toFixed(3);
    });
    S.murl.textContent = MURL(t);
    S.mtabs.wa.classList.add('show');
    S.mtabs.ctl.classList.toggle('show', t >= 26.5); if (t >= 26.5) tabGrow(S.mtabs.ctl, t, 26.5);
    S.mtabs.pk.classList.toggle('show', t >= 29.8); if (t >= 29.8) tabGrow(S.mtabs.pk, t, 29.8);
    S.mtabs.wa.classList.toggle('on', t < 26.5); S.mtabs.ctl.classList.toggle('on', within(t, 26.5, 29.8)); S.mtabs.pk.classList.toggle('on', t >= 29.8);
    prog(S.mprog, t, [26.5, 29.8]);
    press(S.mcont, t, 28.4); press(S.mshare, t, 29.6);
    if (S.rec) S.rec.style.opacity = eo(r(t, 30.0, 30.3)).toFixed(3);
    var sd = sm(r(t, 30.8, 31.05)) * (1 - sm(r(t, 32.5, 32.75))), sp = sm(r(t, 33.1, 33.35));
    pq(S.tpq, { home: 1 - Math.max(sd, sp), send: sd, spend: sp });
    var k2 = sm(r(t, 32.45, 32.7));
    S.tk1.style.opacity = (1 - k2).toFixed(3); S.tk2.style.opacity = k2.toFixed(3);
    press(S.done1, t, 32.2);
    S.sayi.style.opacity = io(t, 30.3, 30.6, 35.8, 36.1).toFixed(3);
    S.q[0].style.opacity = io(t, 30.4, 30.7, 32.8, 33.1).toFixed(3);
    S.q[1].style.opacity = io(t, 33.5, 33.8, 35.8, 36.1).toFixed(3);

    // 6 Review, in dark. No cursor here.
    var sess = 80 + (152 - 80) * r(t, 37.0, 40.4);
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
    S.bars.forEach(function (b, i) { var on2 = i / S.bars.length < pp; if (b._p !== on2) { b.classList.toggle('p', on2); b._p = on2; } });
    if (S.tc) S.tc.textContent = ('0' + Math.floor(sess / 60)).slice(-2) + ':' + ('0' + Math.floor(sess % 60)).slice(-2);
    pq(S.vpq, { home: sess < 92 ? 1 : 0, spend: sess >= 92 ? 1 : 0 });
    var t2 = sess >= 74;
    if (S.tpn) { S.tpn.textContent = t2 ? 'Task 2 of 2' : 'Task 1 of 2'; S.tpt.textContent = t2 ? 'Find what you spent on eating out' : 'Send £20 to Sam'; }
    S.marks.forEach(function (m) { var x = parseFloat(m.style.left) / 100 * LEN; m.classList.toggle('hot', sess >= x && sess < x + 14); });
    S.iss.forEach(function (el, i) { var k = eo(r(t, 40.7 + .3 * i, 41.2 + .3 * i)); el.style.opacity = k.toFixed(3); el.style.transform = 'translateY(' + ((1 - k) * 18).toFixed(1) + 'px)'; });

    // the steps: Publish starts when the owner goes back to Aero (43.0 s); Test at 13.2; Review at 36.6
    var u = (t - JUMP[0] + T) % T, b1 = (JUMP[1] - JUMP[0] + T) % T, b2 = (JUMP[2] - JUMP[0] + T) % T;
    [[0, b1], [b1, b2], [b2, T]].forEach(function (ab, i) {
      var st = S.steps[i]; if (!st) return;
      st.querySelector('.hm-bar b').style.width = (r(u, ab[0], ab[1]) * 100).toFixed(1) + '%';
      st.classList.toggle('on', u >= ab[0] && u < ab[1]);
    });
  }
  var JUMP = [43.0, 13.2, 36.6], JT = [44.5, 13.2, 36.6]; // JT: where a click lands (Publish: just as Sites is clicked)
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
  // no visible pause button (it clashed with the tester screen): Space or Enter on the focused stage pauses
  var stage = $('.hm-stage');
  if (stage) stage.addEventListener('keydown', function (e) {
    if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); playing = !playing; kick(); }
  });
  D.addEventListener('visibilitychange', kick);
  // Publish, Test, Review are buttons: jump the animation to the start of that step
  $$('.hm-stepb').forEach(function (b, i) { b.addEventListener('click', function () { clock = JT[i]; fit(); at(clock); last = null; kick(); }); });

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
    if (RM) { at(31.4); S && S.steps.forEach(function (s) { s.querySelector('.hm-bar b').style.width = '100%'; }); return; }
    at(0); kick();
  }
  W.addEventListener('resize', function () { fit(); rotW(); at(clock); });
  if (D.fonts && D.fonts.ready) D.fonts.ready.then(start); else W.addEventListener('load', start);
})();
