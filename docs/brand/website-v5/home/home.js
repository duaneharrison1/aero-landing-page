/* Aero homepage, round 6 (Team H).
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
  if (/^[bc]$/.test(Q.get('l') || '')) D.documentElement.classList.add('lay-' + Q.get('l')); // review: hero layouts a (default), b, c

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

  /* ---------- hero loop (45 s): the owner's one browser window at an angle, then Maya's own laptop, then back.
     The end flows into the start: after Insights the owner goes to Sites, New site, copies the prompt and switches
     to Claude, which is where the loop begins (pasting it). Every state is computed from t. ---------- */
  var T = 45.2;
  var $ = function (s, r) { return (r || D).querySelector(s); }, $$ = function (s, r) { return [].slice.call((r || D).querySelectorAll(s)); };
  var world = $('.st-world');
  function cl(x) { return x < 0 ? 0 : x > 1 ? 1 : x; }
  function r(t, a, b) { return cl((t - a) / (b - a)); }
  function sm(x) { return x * x * (3 - 2 * x); }
  function eo(x) { return 1 - Math.pow(1 - x, 3); }
  function io(t, a, b, c, d) { return sm(r(t, a, b)) * (1 - sm(r(t, c, d))); }
  function within(t, a, b) { return t >= a && t < b; }

  var S = world && {
    frame: $('.hv-frame'), url: $('.hv-frame .hv-u'), urlBox: $('.hv-frame .hv-url'), prog: $('.hv-frame .hv-prog'),
    cur: $('.hv-cur'), ring: $('.hv-ring'), key: $('.hv-key'), tabs: {}, sc: {},
    sent: $('.cl-sent'), reply: $('.cl-reply'), work: $('.cl-work'), used: $('.cl-used'), done: $('.cl-done'),
    inp: $('[data-sc=claude] .cl-inp'), paste: $('[data-sc=claude] .cl-paste'), send: $('[data-sc=claude] .cl-send'),
    pdone: $('.hv-pdone'), pwait: $('[data-sc=prompt] .x-waitb'), pcopy: $('[data-sc=prompt] .x-pba .btn'),
    banner: $('[data-sc=aero] .x-justpub'), live: $('[data-sc=aero] .x-addr .st.live'), visit: $('[data-sc=aero] .hv-visit'),
    more: $('[data-sc=aero] .x-morew .gbtn'), menu: $('[data-sc=aero] .x-menu-open'), mi: $('[data-sc=aero] .x-mi2'),
    blank: $('.hv-blank'), made: $('[data-sc=setup] .x-made'), copy: $('[data-sc=setup] .x-lk .btn'), link: $('[data-sc=setup] .x-lk'), copied: $('.st-copied'),
    msg: $('.st-msg'), sentl: $('.st-msg .st-sent'),
    maya: $('.hv-maya'), note: $('.hv-note'), mwin: $('.hv-mwin'), murl: $('.hv-mch .hv-u'), mtabs: {}, ms: {}, mprog: $('.hv-mch .hv-prog'),
    mcont: $('[data-ms=w] .x-tgo .btn'), mshare: $('[data-ms=p] .hv-share'), sayi: $('.hv-sayi'), q: $$('.hv-q'),
    tpq: $('[data-ms=t] .pq-wrap'), tk1: $('[data-ms=t] .st-tk1'), tk2: $('[data-ms=t] .st-tk2'), done1: $('[data-ms=t] .st-tk1 .st-done'), rec: $('[data-ms=t] .x-recchip'),
    lines: $$('.st-trs .tl[data-s]'), ph: $('[data-sc=watch] .ph-line'), bars: $$('[data-sc=watch] .tline .wave i'), tc: $('.st-tc'), vpq: $('.st-vid .pq-wrap'),
    tpn: $('.st-tpn'), tpt: $('.st-tpt'), marks: $$('[data-sc=watch] .tline .marks .m'), iss: $$('[data-sc=ins] .iss, [data-sc=ins] .sumcard2'),
    sbSites: $$('[data-sc=ins] .sb-item')[1], newsite: $('[data-sc=sites] .mhead .r .btn'),
    caps: $$('.hm-cap'), steps: $$('.hm-step')
  };
  if (S) {
    $$('.hv-frame .hv-tab').forEach(function (el) { S.tabs[el.getAttribute('data-tab')] = el; });
    $$('.hv-sc').forEach(function (el) { S.sc[el.getAttribute('data-sc')] = el; });
    $$('.hv-mch .hv-tab').forEach(function (el) { S.mtabs[el.getAttribute('data-tab')] = el; });
    $$('.hv-ms').forEach(function (el) { S.ms[el.getAttribute('data-ms')] = el; });
    S.lines.forEach(function (l) { l._w = $$('.w', l); l._s = +l.getAttribute('data-s'); });
    S.tabX = S.tabs.site && S.tabs.site.querySelector('.hv-x');
  }

  // the owner's window: which page, when (crossfades 0.2 s)
  var SCENES = [['claude', 0, 7.3], ['prompt', 7.3, 8.8], ['aero', 8.8, 11.05], ['site', 11.05, 14.5], ['aero', 14.5, 16.5], ['setup', 16.5, 33.0],
                ['watch', 33.0, 37.8], ['ins', 37.8, 42.1], ['sites', 42.1, 43.1], ['prompt', 43.1, 44.85], ['claude', 44.85, 99]];
  var URL = { claude: 'claude.ai/chat/pocket', prompt: 'aeroapp.ai/new?from=prompt', aero: 'aeroapp.ai/sites/pocket', site: 'pocket.aeroapp.ai',
              setup: 'aeroapp.ai/tests/pocket/setup', watch: 'aeroapp.ai/tests/pocket/sessions/2', ins: 'aeroapp.ai/tests/pocket/insights', sites: 'aeroapp.ai/sites' };
  var TABON = { claude: 'claude', site: 'site' };
  var LOADS = [8.8, 11.05, 16.5, 42.1, 43.1]; // a page loads: the blue line under the address bar runs
  // captions, in step with the timeline
  var CAPS = [[0, 3.6], [3.6, 7.3], [7.3, 11.0], [11.0, 14.5], [14.5, 18.6], [18.6, 20.4], [20.4, 26.5], [26.5, 33.0], [33.0, 37.8], [37.8, 40.4], [40.4, 45.2]];
  // Maya's browser: which page, when
  var MS = [['w', 23.0, 25.15], ['p', 25.15, 26.5], ['t', 26.5, 99]];
  function scene(t) { for (var i = 0; i < SCENES.length; i++) if (t < SCENES[i][2]) return SCENES[i][0]; return 'claude'; }

  // the owner's cursor (never on Maya's screen, never in the review): [time, target]
  var P = {};
  var CUR = [[0, 'tab:claude'], [1.2, 'inp'], [3.0, 'inp'], [3.45, 'send'], [6.6, 'send'], [7.2, 'tab:aero'], [9.6, 'tab:aero'], [10.9, 'visit'],
             [13.2, 'visit2'], [14.4, 'tab:aero'], [14.6, 'tab:aero'], [15.3, 'more'], [15.6, 'more'], [16.3, 'mi'], [16.9, 'mi2'], [17.8, 'copy'], [19.9, 'copy'],
             [40.4, 'ins:park'], [41.1, 'tabx'], [41.4, 'tabx'], [41.9, 'sb:sites'], [42.3, 'sb:sites'], [42.9, 'newsite'], [43.3, 'newsite'], [43.8, 'pcopy'],
             [44.1, 'pcopy'], [44.75, 'tab:claude'], [T, 'tab:claude']];
  var CLICKS = [[1.3, 'inp'], [3.5, 'send'], [7.25, 'tab:aero'], [11.0, 'visit'], [14.45, 'tab:aero'], [15.4, 'more'], [16.4, 'mi'], [17.9, 'copy'],
                [41.2, 'tabx'], [42.0, 'sb:sites'], [43.0, 'newsite'], [43.9, 'pcopy'], [44.8, 'tab:claude']];
  var CURON = [[0, 20.0], [40.4, 99]];
  function curPos(t) {
    for (var i = 1; i < CUR.length; i++) if (t <= CUR[i][0]) {
      var a = P[CUR[i - 1][1]], b = P[CUR[i][1]], k = sm(r(t, CUR[i - 1][0], CUR[i][0]));
      if (!a || !b) return null;
      return [a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k];
    }
    return P[CUR[CUR.length - 1][1]];
  }

  var FR0 = [30, 62]; // the owner's window in the world (matches .hv-frame)
  function measure() {
    if (!S) return;
    var wt = world.style.transform, ft = S.frame.style.transform, mt = S.maya.style.transform, mwt = S.mwin.style.transform;
    world.style.transform = 'none'; S.frame.style.transform = 'none'; S.maya.style.transform = 'none'; S.mwin.style.transform = 'none';
    var fr = S.frame.getBoundingClientRect(), wr = world.getBoundingClientRect(), keep = [];
    function vis(el) { var s = el; while (s && s !== world) { if (s.classList && (s.classList.contains('hv-sc') || s.classList.contains('hv-ms'))) { keep.push([s, s.style.opacity]); s.style.opacity = '1'; } s = s.parentElement; } }
    function pt(name, el, fx, fy) {
      if (!el) return; vis(el);
      var b = el.getBoundingClientRect();
      P[name] = [b.left - fr.left + b.width * (fx == null ? .5 : fx), b.top - fr.top + b.height * (fy == null ? .55 : fy)];
      P[name + '#'] = [b.left - wr.left + b.width * (fx == null ? .5 : fx), b.top - wr.top + b.height * (fy == null ? .5 : fy)];
    }
    var shown = $$('.hv-tab').map(function (x) { var o = x.classList.contains('show'); x.classList.add('show'); return [x, o]; });
    pt('inp', S.inp, .45, .5); pt('send', S.send); pt('tab:aero', S.tabs.aero, .4); pt('tab:claude', S.tabs.claude, .4); pt('tabx', S.tabX); pt('visit', S.visit);
    var mo = S.menu && S.menu.style.opacity; if (S.menu) S.menu.style.opacity = '1';
    pt('more', S.more); pt('mi', S.mi, .3, .4); pt('cam:menu', S.menu, .5, .4); if (S.menu) S.menu.style.opacity = mo;
    pt('copy', S.copy); pt('pcopy', S.pcopy); pt('sb:sites', S.sbSites, .3); pt('newsite', S.newsite);
    pt('cam:claude', $('[data-sc=claude] .cl-msgs'), .5, .3); pt('cam:msgs', $('[data-sc=claude] .cl-msgs'), .5, .75); pt('cam:pdone', S.pdone, .4);
    pt('cam:banner', S.banner, .3); pt('cam:site', $('[data-sc=site] .pk-hero'), .3); pt('cam:setup', S.made, .3);
    pt('cam:video', $('[data-sc=watch] .stage3')); pt('cam:trs', $('[data-sc=watch] .st-trs'), .5, .4); pt('cam:sum', $('[data-sc=ins] .sumcard2'), .4, .8);
    pt('cam:sites', $('[data-sc=sites] .mhead'), .7, 3); pt('cam:prompt', $('[data-sc=prompt] .x-pbox'), .4);
    pt('cam:note', S.note); pt('cam:wcard', $('[data-ms=w] .x-tcard')); pt('cam:pcard', $('[data-ms=p] .x-tcard'));
    pt('cam:tk', $('[data-ms=t] .st-tk1 .x-tk'), .9, .3); pt('cam:say', $('.hv-say'), .3); pt('cam:rec', S.rec, .5, 3);
    keep.forEach(function (k) { k[0].style.opacity = k[1]; });
    shown.forEach(function (x) { if (!x[1]) x[0].classList.remove('show'); });
    P.mi2 = P.mi; P.visit2 = P.visit && [P.visit[0] - 140, P.visit[1] + 240];
    P['ins:park'] = P['sb:sites'] && [P['sb:sites'][0] + 420, P['sb:sites'][1] + 160];
    var mr = S.msg.getBoundingClientRect();
    P['cam:msg#'] = [mr.left - wr.left + mr.width / 2 - 80, mr.top - wr.top + mr.height / 2];
    if (P.copy && S.copied) { S.copied.style.left = (P.copy[0] - 160) + 'px'; S.copied.style.top = (P.copy[1] - 76 - 66) + 'px'; }
    world.style.transform = wt; S.frame.style.transform = ft; S.maya.style.transform = mt; S.mwin.style.transform = mwt;
  }

  // phone width: the window is flat and the camera follows the action. [time, target]
  var CAM = [[0, 'cam:claude'], [1.0, 'inp'], [4.2, 'cam:msgs'], [6.8, 'tab:aero'], [7.6, 'cam:pdone'], [9.0, 'cam:banner'], [10.2, 'visit'], [11.6, 'cam:site'],
             [13.9, 'tab:aero'], [15.0, 'cam:menu'], [16.8, 'cam:setup'], [17.4, 'copy'], [18.7, 'cam:msg#'], [20.9, 'cam:note#'], [23.2, 'cam:wcard#'],
             [25.3, 'cam:pcard#'], [26.7, 'cam:rec#'], [27.8, 'cam:say#'], [29.0, 'cam:tk#'], [30.4, 'cam:say#'], [33.4, 'cam:video'], [34.8, 'cam:trs'],
             [38.0, 'cam:sum'], [40.6, 'tabx'], [41.6, 'sb:sites'], [42.4, 'cam:sites'], [43.3, 'cam:prompt'], [44.3, 'tab:claude'], [T + 1, 'cam:claude']];
  function wpt(name) { var p = P[name]; if (!p) return null; return name.slice(-1) === '#' ? p : [p[0] + FR0[0], p[1] + FR0[1]]; }
  function cam(t) {
    var i = 0; while (i < CAM.length - 1 && t >= CAM[i + 1][0]) i++;
    var a = wpt(CAM[i][1]) || [740, 500], n = CAM[i + 1], b = n ? wpt(n[1]) || a : a, k = n ? sm(r(t, n[0] - .8, n[0])) : 0;
    return [a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k];
  }

  function press(el, t, tc) { // a button pressed at tc
    if (!el) return;
    var k = Math.sin(Math.PI * r(t, tc - .04, tc + .24));
    el.style.transform = k > 0 ? 'scale(' + (1 - .07 * k).toFixed(3) + ')' : '';
    el.style.filter = k > 0 ? 'brightness(' + (1 - .1 * k).toFixed(3) + ')' : '';
  }
  function presses(el, t, list) { var best = -1; list.forEach(function (tc) { if (Math.abs(t - tc) < Math.abs(t - best)) best = tc; }); press(el, t, best); }
  function glow(el, k, col) { if (el) el.style.boxShadow = k > .001 ? '0 0 0 ' + (2 + 4 * k).toFixed(1) + 'px rgba(' + (col || 'var(--accent-rgb)') + ',' + (.35 * k).toFixed(3) + ')' : ''; }
  function pq(el, map) {
    if (!el) return;
    el.removeAttribute('data-pq');
    ['home', 'send', 'spend'].forEach(function (k) { var s = el.querySelector('.pq-' + k); if (s) s.style.opacity = (map[k] || 0).toFixed(3); });
  }
  function prog(el, t, list) { // loading line under the address bar
    var k = -1; list.forEach(function (a) { if (t >= a && t < a + .75) k = (t - a) / .75; });
    if (!el) return;
    el.style.opacity = k < 0 ? '0' : (k > .8 ? ((1 - k) / .2).toFixed(2) : '1');
    el.style.width = k < 0 ? '0' : (eo(Math.min(1, k * 1.25)) * 100).toFixed(1) + '%';
  }
  var LEN = 214, NARROW = false;

  function at(t) {
    if (!S) return;
    // camera
    var s, tx = 0, ty = 0;
    if (NARROW) {
      s = VW / 720; var c = cam(t);
      tx = VW / 2 - c[0] * s; ty = VH / 2 - c[1] * s;
      tx = Math.min(0, Math.max(VW - 1540 * s, tx)); ty = Math.min(0, Math.max(VH - 1030 * s, ty));
    } else s = VW / 1540;
    world.style.transform = 'translate(' + tx.toFixed(1) + 'px,' + ty.toFixed(1) + 'px) scale(' + s.toFixed(5) + ')';

    // captions, one at a time
    S.caps.forEach(function (el, i) { var a = CAPS[i]; el.style.opacity = io(t, a[0], a[0] + .3, a[1] - .25, a[1]).toFixed(3) || '0'; if (a[0] === 0 && t < .3) el.style.opacity = '1'; if (a[1] >= T && t > T - .25) el.style.opacity = '1'; });
    if (t < .3) S.caps[S.caps.length - 1].style.opacity = '0';

    // the owner's window: out to the left for Maya's part, back in for the review
    var oOut = sm(r(t, 20.4, 21.0)), oIn = sm(r(t, 33.35, 33.95)), off = t < 27 ? oOut : 1 - oIn;
    S.frame.style.opacity = (1 - off).toFixed(3);
    S.frame.style.transform = NARROW ? 'translateX(' + (-off * 1700).toFixed(0) + 'px)' : 'translateX(' + (-off * 1700).toFixed(0) + 'px) rotateY(-7deg) rotateX(3deg)';
    var cur = scene(t);
    Object.keys(S.sc).forEach(function (k) {
      var o = 0;
      SCENES.forEach(function (sc) { if (sc[0] === k) o = Math.max(o, (sc[1] === 0 ? 1 : sm(r(t, sc[1] - .2, sc[1]))) * (1 - sm(r(t, sc[2] - .2, sc[2])))); });
      S.sc[k].style.opacity = Math.min(1, o).toFixed(3);
    });
    S.url.textContent = URL[cur];
    S.frame.setAttribute('data-theme', cur === 'watch' || cur === 'ins' ? 'dark' : 'light');
    S.tabs.claude.classList.add('show'); S.tabs.aero.classList.add('show');
    var siteTab = t >= 11.05 && t < 41.25;
    S.tabs.site.classList.toggle('show', siteTab);
    S.tabs.site.style.transform = siteTab ? 'scaleX(' + (.3 + .7 * eo(r(t, 11.05, 11.3))).toFixed(3) + ')' : '';
    S.tabs.site.classList.toggle('load', within(t, 11.05, 11.8));
    S.tabs.site.style.setProperty('--spin', ((t * 720) % 360).toFixed(0) + 'deg');
    Object.keys(S.tabs).forEach(function (k) { S.tabs[k].classList.toggle('on', (TABON[cur] || 'aero') === k); });
    prog(S.prog, t, LOADS);
    glow(S.urlBox, io(t, 11.05, 11.25, 12.6, 13.0));

    // 1 Claude: the prompt is pasted and sent; Claude publishes
    var pasted = t >= 1.5 && t < 3.55;
    S.inp.classList.toggle('pasted', pasted); S.paste.classList.toggle('on', pasted); S.paste.classList.toggle('sel', within(t, 1.5, 2.0));
    press(S.inp, t, 1.3); press(S.send, t, 3.5);
    var conv = t < 44.85 ? 1 : 0; // the next loop starts with a fresh chat turn
    S.sent.style.opacity = (sm(r(t, 3.55, 3.8)) * conv).toFixed(3);
    S.reply.style.opacity = (sm(r(t, 3.9, 4.1)) * conv).toFixed(3);
    var pub = t >= 5.6;
    S.work.style.display = pub ? 'none' : 'inline-flex';
    S.used.style.display = pub ? 'inline-flex' : 'none'; S.done.style.display = pub ? 'block' : 'none';
    S.done.style.opacity = sm(r(t, 5.6, 5.9)).toFixed(3);
    glow(S.used, io(t, 5.6, 5.75, 6.8, 7.2), '94,140,74');
    if (S.key && P.inp) { S.key.style.opacity = io(t, 1.35, 1.45, 2.0, 2.15).toFixed(3); S.key.style.transform = 'translate(' + (P.inp[0] + 24).toFixed(0) + 'px,' + (P.inp[1] - 54).toFixed(0) + 'px)'; }

    // 2 Aero: the prompt page has updated by itself; then the site's own page, live
    var fresh = t > 40; // the prompt page at the end of the loop is waiting again
    if (S.pdone) { S.pdone.style.display = fresh ? 'none' : ''; glow(S.pdone, io(t, 7.4, 7.6, 8.4, 8.7), '31,143,95'); }
    if (S.pwait) S.pwait.style.display = fresh ? '' : 'none';
    if (S.pcopy) { S.pcopy.classList.toggle('copied', within(t, 43.95, 45.0)); presses(S.pcopy, t, [43.9]); }
    if (S.banner) { var bk = eo(r(t, 8.9, 9.3)); S.banner.style.opacity = (t > 14 ? 1 : bk).toFixed(3); S.banner.style.transform = 'translateY(' + ((1 - (t > 14 ? 1 : bk)) * -10).toFixed(1) + 'px)'; }
    glow(S.live, io(t, 9.4, 9.6, 10.2, 10.6), '31,143,95'); if (S.live) S.live.style.borderRadius = '6px';
    press(S.visit, t, 11.0); presses(S.tabs.aero, t, [7.25, 14.45]); press(S.more, t, 15.4); press(S.mi, t, 16.4); press(S.copy, t, 17.9);
    presses(S.tabs.claude, t, [44.8]); press(S.tabX, t, 41.2); press(S.sbSites, t, 42.0); press(S.newsite, t, 43.0);
    // the live site: a blank page while it loads, then it renders
    if (S.blank) S.blank.style.opacity = (1 - sm(r(t, 11.6, 11.85))).toFixed(3);
    // 3 Test: the site's menu, "User test this site", copy the link, send it
    if (S.menu) { var on = within(t, 15.42, 16.5), mk = eo(r(t, 15.42, 15.6));
      S.menu.style.opacity = on ? '1' : '0';
      S.menu.style.clipPath = on ? 'inset(0 0 ' + ((1 - mk) * 100).toFixed(1) + '% 0 round 12px)' : '';
      S.menu.style.transform = on ? 'translateY(' + ((1 - mk) * -6).toFixed(1) + 'px)' : ''; }
    glow(S.made, io(t, 16.7, 16.9, 17.4, 17.8), '31,143,95');
    S.copied.style.opacity = io(t, 17.95, 18.1, 19.4, 19.7).toFixed(3);
    S.copied.style.transform = 'translateY(' + ((1 - eo(r(t, 17.95, 18.2))) * 8).toFixed(1) + 'px)';
    glow(S.link, io(t, 17.9, 18.05, 19.0, 19.4));
    var mI = eo(r(t, 18.6, 19.0)), mO = sm(r(t, 20.2, 20.5));
    S.msg.style.opacity = (mI * (1 - mO)).toFixed(3);
    S.msg.style.transform = 'translate(' + ((1 - mI) * -30 - mO * 400).toFixed(1) + 'px,' + ((1 - mI) * 14).toFixed(1) + 'px)';
    S.sentl.style.opacity = sm(r(t, 19.3, 19.45)).toFixed(3);

    // the cursor, its click rings and the paste keys
    var cp = curPos(t), cOn = 0;
    CURON.forEach(function (a) { cOn = Math.max(cOn, (a[0] === 0 ? 1 : sm(r(t, a[0], a[0] + .3))) * (1 - sm(r(t, a[1] - .3, a[1])))); });
    if (cp && cOn > 0) { S.cur.style.opacity = cOn.toFixed(3); S.cur.style.transform = 'translate(' + (cp[0] - 5).toFixed(1) + 'px,' + (cp[1] - 3).toFixed(1) + 'px)'; }
    else S.cur.style.opacity = '0';
    var ring = 0, rp = null;
    CLICKS.forEach(function (c) { var k = r(t, c[0], c[0] + .45); if (k > 0 && k < 1) { ring = k; rp = P[c[1]]; } });
    if (rp) { S.ring.style.opacity = (1 - ring).toFixed(3); S.ring.style.transform = 'translate(' + rp[0].toFixed(1) + 'px,' + rp[1].toFixed(1) + 'px) scale(' + (.5 + .7 * eo(ring)).toFixed(3) + ')'; }
    else S.ring.style.opacity = '0';

    // 4 Maya's own laptop comes in: the message arrives, she opens it, allows the microphone and the tab, and the
    // test runs in a second tab with the task plate on the left. Her words appear beside the laptop, not on screen.
    var lIn = eo(r(t, 20.85, 21.5)), lOut = sm(r(t, 33.0, 33.5)), lap = t < 27 ? lIn : 1 - lOut;
    S.maya.style.opacity = lap.toFixed(3);
    S.maya.style.transform = 'translateX(' + ((1 - lap) * (t < 27 ? 1500 : 1500)).toFixed(0) + 'px)';
    var nk = eo(r(t, 21.6, 22.0));
    S.note.style.opacity = (nk * (1 - sm(r(t, 23.0, 23.25)))).toFixed(3);
    S.note.style.transform = 'translateX(' + ((1 - nk) * 40).toFixed(0) + 'px)';
    press(S.note, t, 22.9);
    var wk = eo(r(t, 23.0, 23.4));
    S.mwin.style.opacity = wk.toFixed(3); S.mwin.style.transform = 'scale(' + (.96 + .04 * wk).toFixed(3) + ')';
    Object.keys(S.ms).forEach(function (k) {
      var o = 0; MS.forEach(function (m) { if (m[0] === k) o = Math.max(o, sm(r(t, m[1] - .15, m[1] + .05)) * (1 - sm(r(t, m[2] - .15, m[2])))); });
      S.ms[k].style.opacity = o.toFixed(3);
    });
    var testing = t >= 26.4;
    S.mtabs.pk.classList.toggle('show', testing); S.mtabs.ctl.classList.add('show');
    S.mtabs.ctl.classList.toggle('on', !testing); S.mtabs.pk.classList.toggle('on', testing);
    S.mtabs.pk.style.transform = testing ? 'scaleX(' + (.3 + .7 * eo(r(t, 26.4, 26.65))).toFixed(3) + ')' : '';
    prog(S.mprog, t, [23.0, 26.45]);
    press(S.mcont, t, 25.0); press(S.mshare, t, 26.3);
    if (S.rec) S.rec.style.opacity = eo(r(t, 26.7, 27.0)).toFixed(3);
    var sd = sm(r(t, 27.6, 27.85)) * (1 - sm(r(t, 29.3, 29.55))), sp = sm(r(t, 29.9, 30.15));
    pq(S.tpq, { home: 1 - Math.max(sd, sp), send: sd, spend: sp });
    var k2 = sm(r(t, 29.25, 29.5));
    S.tk1.style.opacity = (1 - k2).toFixed(3); S.tk2.style.opacity = k2.toFixed(3);
    press(S.done1, t, 29.0);
    S.sayi.style.opacity = io(t, 27.0, 27.3, 32.6, 32.9).toFixed(3);
    S.q[0].style.opacity = io(t, 27.2, 27.5, 29.6, 29.9).toFixed(3);
    S.q[1].style.opacity = io(t, 30.3, 30.6, 32.6, 32.9).toFixed(3);

    // 5 Review, in dark: the session plays with her words lit as they're said; then Insights. No cursor here.
    var sess = 80 + (152 - 80) * r(t, 33.9, 37.6);
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
    S.iss.forEach(function (el, i) { var k = eo(r(t, 37.9 + .3 * i, 38.4 + .3 * i)); el.style.opacity = k.toFixed(3); el.style.transform = 'translateY(' + ((1 - k) * 18).toFixed(1) + 'px)'; });

    // the steps along the bottom: the loop's Publish starts when the owner goes back to Aero (40.4 s)
    var u = (t - 40.4 + T) % T;
    [[0, 19.3], [19.3, 37.8], [37.8, 45.2]].forEach(function (ab, i) {
      var st = S.steps[i]; if (!st) return;
      st.querySelector('.hm-bar b').style.width = (r(u, ab[0], ab[1]) * 100).toFixed(1) + '%';
      st.classList.toggle('on', u >= ab[0] && u < ab[1]);
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
  // no visible pause button (it clashed with the tester screen): Space or Enter on the focused stage pauses
  var stage = $('.hm-stage');
  if (stage) stage.addEventListener('keydown', function (e) {
    if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); playing = !playing; kick(); }
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
    if (RM) { at(28.2); S && S.steps.forEach(function (s) { s.querySelector('.hm-bar b').style.width = '100%'; }); return; }
    at(0); kick();
  }
  W.addEventListener('resize', function () { fit(); rotW(); at(clock); });
  if (D.fonts && D.fonts.ready) D.fonts.ready.then(start); else W.addEventListener('load', start);
})();
