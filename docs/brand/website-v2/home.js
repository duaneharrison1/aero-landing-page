/* Aero homepage behaviour: copy block, scaled app windows, the made-with rotator, the hero replay loop, reveals.
   ?t=189 freezes the hero replay at that second of the session (used for screenshots). */
(function () {
  'use strict';
  var D = document, W = window, root = D.documentElement;
  root.classList.add('js');
  var RM = W.matchMedia && W.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var Q = new URLSearchParams(location.search);
  var FREEZE = Q.has('t') ? parseFloat(Q.get('t')) : null;

  /* ---------- 1. copy: the JSON block at the top is the source for every word */
  var COPY = {};
  try { COPY = JSON.parse(D.getElementById('copy').textContent); } catch (e) { COPY = {}; }
  function txt(el, v) { if (el && typeof v === 'string' && el.textContent !== v) el.textContent = v; }
  D.querySelectorAll('[data-c]').forEach(function (el) {
    var k = el.getAttribute('data-c'), v = COPY[k];
    if (typeof v === 'string') { txt(el, v); return; }
    var m = k.match(/^(.*)\.(\d+)$/);
    if (m && Array.isArray(COPY[m[1]])) { txt(el, COPY[m[1]][+m[2]]); return; }
    if (!Array.isArray(v)) return;
    if (k === 'hero.h1.made') {
      el.innerHTML = '';
      v.forEach(function (w, i) { var s = D.createElement('span'); s.className = 'h-w' + (i ? '' : ' on'); s.textContent = w; el.appendChild(s); });
    } else if (k === 'fast.steps') {
      el.querySelectorAll('.h-st').forEach(function (s, i) { if (!v[i]) return; txt(s.querySelector('.tm'), v[i][0]); txt(s.querySelector('b'), v[i][1]); txt(s.querySelector('p'), v[i][2]); });
    } else if (k === 'who.items') {
      el.querySelectorAll('.h-who-i').forEach(function (s, i) { if (!v[i]) return; txt(s.querySelector('b'), v[i][0]); txt(s.querySelector('p'), v[i][1]); });
    } else if (k === 'faq.items') {
      el.querySelectorAll('details').forEach(function (s, i) { if (!v[i]) return; txt(s.querySelector('summary'), v[i][0]); txt(s.querySelector('p'), v[i][1]); });
    } else if (k === 'price.plans') {
      el.querySelectorAll('.h-plan').forEach(function (s, i) {
        var p = v[i]; if (!p) return;
        txt(s.querySelector('.pn b'), p[0]); txt(s.querySelector('.pn .lbl'), p[5]);
        var pr = s.querySelector('.pr'); if (pr && pr.firstChild) pr.firstChild.nodeValue = p[1]; txt(s.querySelector('.pr small'), p[2]);
        var lis = s.querySelectorAll('li'); lis.forEach(function (li, j) { if (p[3][j] != null) li.lastChild.nodeValue = p[3][j]; else li.remove(); });
        var b = s.querySelector('.btn'); if (b && !b.querySelector('canvas')) txt(b, p[4]);
      });
    }
  });

  /* ---------- 2. app windows: real 1440px screens, scaled to their column (a phone shows a chosen part) */
  var shots = [].slice.call(D.querySelectorAll('.shot'));
  function phone() { return W.innerWidth <= 760; }
  function fit() {
    var ph = phone();
    shots.forEach(function (s) {
      var d = s.dataset, vw = +(ph ? d.mw : d.w), vh = +(ph ? d.mh : d.h), x = ph ? +d.mx : 0, y = ph ? +d.my : 0;
      s.style.aspectRatio = vw + ' / ' + vh;
      var k = s.clientWidth / vw, inn = s.firstElementChild;
      inn.style.width = (ph && s.classList.contains('hero-shot') ? vw : +d.w) + 'px';
      inn.style.transform = 'scale(' + k + ') translate(' + (-x) + 'px,' + (-y) + 'px)';
    });
  }
  fit();
  W.addEventListener('resize', fit);
  if (D.fonts && D.fonts.ready) D.fonts.ready.then(fit);

  /* ---------- 3. made-with rotator: Claude artifact, Figma prototype, Lovable app, HTML site */
  var rot = D.querySelector('.h-rot');
  if (rot) {
    var words = [].slice.call(rot.querySelectorAll('.h-w')), cur = 0;
    var size = function () { var w = words[cur]; rot.style.width = w.getBoundingClientRect().width + 'px'; };
    if (D.fonts && D.fonts.ready) D.fonts.ready.then(size); size();
    W.addEventListener('resize', size);
    if (!RM && FREEZE === null && words.length > 1) setInterval(function () {
      var a = words[cur]; cur = (cur + 1) % words.length; var b = words[cur];
      a.classList.add('out'); a.classList.remove('on'); b.classList.remove('out'); b.classList.add('on'); size();
      setTimeout(function () { a.classList.remove('out'); }, 600);
    }, 2600);
  }

  /* ---------- 4. hero: a recorded session playing back. Only the highlight moves; the whole transcript is already there. */
  var hs = D.querySelector('.hero-shot');
  if (hs) {
    var LEN = 432, T0 = 134, T1 = 232, SPEED = 2, WPS = 2.6;
    var TASKS = [[18, 156, '1', 'Send £20 to Sam'], [156, 350, '2', 'Find your cards']];
    var mmss = function (s) { s = Math.max(0, Math.floor(s)); return ('0' + Math.floor(s / 60)).slice(-2) + ':' + ('0' + s % 60).slice(-2); };
    var lines = [].slice.call(hs.querySelectorAll('.insp2 .tl:not(.task)')).map(function (el) {
      var mono = el.querySelector('.mono'), p = el.querySelector('.tx p'), t = mono.textContent.split(':');
      var words = p.textContent.trim().split(/\s+/);
      p.innerHTML = words.map(function (w) { return '<span class="w">' + w.replace(/&/g, '&amp;').replace(/</g, '&lt;') + '</span>'; }).join(' ');
      return { el: el, s: +t[0] * 60 + +t[1], w: [].slice.call(p.querySelectorAll('.w')), tq: el.querySelector('.tq') };
    });
    lines.forEach(function (l, i) { var nx = lines[i + 1] ? lines[i + 1].s : LEN; l.d = Math.min(nx - l.s - .4, l.w.length / WPS + .4); });
    var scroller = hs.querySelector('.trs.scroll');
    var marks = [].slice.call(hs.querySelectorAll('.tline .marks .m')).map(function (m) { return { el: m, s: parseFloat(m.style.left) / 100 * LEN }; });
    var bars = [].slice.call(hs.querySelectorAll('.tline .wave i'));
    var tasks = [].slice.call(hs.querySelectorAll('.tline .tasks .task'));
    var head = hs.querySelector('.tline .ph-line'), tc = hs.querySelector('.pctl .tc'), pill = hs.querySelector('.vpill .taskpill');
    var note = hs.querySelector('.addnote .input'), ph = hs.querySelector('.video .ph'), lastCur = null, scrollY = scroller ? scroller.scrollTop : 0;

    var render = function (t, instant) {
      var cur = null;
      lines.forEach(function (l) { if (l.s <= t) cur = l; });
      lines.forEach(function (l) {
        var st = l === cur ? 'cur' : (l.s < t ? 'past' : 'future');
        if (!l.el.classList.contains(st)) { l.el.classList.remove('cur', 'past', 'future'); l.el.classList.add(st); }
        if (l === cur) {
          var n = Math.floor((t - l.s) * WPS) + 1, done = t - l.s > l.d;
          l.w.forEach(function (w, i) { w.classList.toggle('s', done || i < n - 1); w.classList.toggle('n', !done && i === n - 1); });
        }
        if (l.tq) l.tq.classList.toggle('lit', t >= l.s && t < l.s + 9);
      });
      marks.forEach(function (m) { m.el.classList.toggle('hot', t >= m.s - .5 && t < m.s + 9); });
      var n = Math.round(bars.length * t / LEN);
      bars.forEach(function (b, i) { b.classList.toggle('p', i < n); });
      if (head) head.style.left = (t / LEN * 100) + '%';
      if (tc && tc.firstChild) tc.firstChild.nodeValue = mmss(t) + ' ';
      var tk = TASKS[t < 156 ? 0 : 1];
      tasks.forEach(function (el, i) { el.classList.toggle('on', i === (t < 156 ? 0 : 1)); });
      if (pill) { var pm = pill.querySelector('.mono'); if (pm) pm.textContent = 'Task ' + tk[2] + ' of 2'; if (pill.lastChild) pill.lastChild.nodeValue = tk[3]; }
      if (ph) ph.classList.toggle('s-sheet', t >= 205);
      if (note && note.childNodes[1]) note.childNodes[1].nodeValue = 'Add a note at ' + mmss(t);
      if (scroller && cur) {
        var target = Math.max(0, cur.el.offsetTop - scroller.offsetTop - scroller.clientHeight * .32);
        if (cur !== lastCur || instant) lastCur = cur;
        scrollY = instant ? target : scrollY + (target - scrollY) * .06;
        scroller.scrollTop = scrollY;
      }
    };

    if (FREEZE !== null || RM) {
      render(FREEZE !== null ? FREEZE : 189, true);
    } else {
      var t = T0, last = null, visible = true, fading = false;
      if ('IntersectionObserver' in W) new IntersectionObserver(function (es) { visible = es[0].isIntersecting; }).observe(hs);
      render(t, true);
      var tick = function (now) {
        if (last === null) last = now;
        var dt = Math.min(.1, (now - last) / 1000); last = now;
        if (visible && !D.hidden && !fading) {
          t += dt * SPEED;
          if (t >= T1) {
            fading = true; hs.classList.add('fade');
            setTimeout(function () { t = T0; render(t, true); hs.classList.remove('fade'); setTimeout(function () { fading = false; }, 500); }, 550);
          }
        }
        if (!fading) render(t, false);
        requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    }
  }

  /* ---------- 5. reveals */
  var els = D.querySelectorAll('.h-tlx');
  if (RM || !('IntersectionObserver' in W) || FREEZE !== null) els.forEach(function (e) { e.classList.add('in'); });
  else {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }); }, { rootMargin: '0px 0px -12% 0px' });
    els.forEach(function (e) { io.observe(e); });
  }
})();
