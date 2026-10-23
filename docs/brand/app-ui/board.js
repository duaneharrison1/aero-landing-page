/* Board behaviour: scale app frames, palette / theme / layout switches, a playable transcript demo, flow steppers.
   Presentation only. version: 2026-10-23.1 */
(function () {
  var Q = new URLSearchParams(location.search);
  function store(k, v) { try { if (v === undefined) return localStorage.getItem('aeui-' + k); localStorage.setItem('aeui-' + k, v); } catch (e) { return null; } }
  var root = document.documentElement;

  /* palette, theme, layout */
  var pal = Q.get('palette') || store('palette') || 'morning';
  var lay = Q.get('layout') || store('layout') || 'side';
  function applyPal(p) { if (p === 'clear') root.setAttribute('data-palette', 'clear'); else root.removeAttribute('data-palette'); pal = p; store('palette', p); mark(); }
  function applyLay(l) { document.body.classList.toggle('is-large', l === 'large'); lay = l; store('layout', l); mark(); fitAll(); }
  function mark() {
    document.querySelectorAll('[data-set-pal]').forEach(function (b) { b.classList.toggle('is-active', b.getAttribute('data-set-pal') === pal); });
    document.querySelectorAll('[data-set-lay]').forEach(function (b) { b.classList.toggle('is-active', b.getAttribute('data-set-lay') === lay); });
  }
  document.addEventListener('click', function (e) {
    var p = e.target.closest('[data-set-pal]'); if (p) applyPal(p.getAttribute('data-set-pal'));
    var l = e.target.closest('[data-set-lay]'); if (l) applyLay(l.getAttribute('data-set-lay'));
  });

  /* fit: render each app at its real width, scaled to the column. Phones get the natural (container) layout. */
  function fit(el) {
    var inner = el.firstElementChild; if (!inner) return;
    var w = +el.getAttribute('data-w') || 1180, h = +el.getAttribute('data-h') || 760;
    var W = el.clientWidth;
    var natural = W < 600 && !el.hasAttribute('data-fixed');
    el.classList.toggle('is-natural', natural);
    if (natural) {
      inner.style.width = ''; inner.style.height = ''; inner.style.transform = '';
      var mh = +el.getAttribute('data-mh') || 860;
      inner.style.minHeight = Math.min(mh, 640) + 'px';
      el.style.height = Math.min(inner.scrollHeight, mh) + 'px';
    } else {
      var k = W / w;
      inner.style.width = w + 'px'; inner.style.height = h + 'px'; inner.style.minHeight = '';
      inner.style.transform = 'scale(' + k + ')';
      el.style.height = Math.round(h * k) + 'px';
    }
  }
  function fitAll() { document.querySelectorAll('.fit').forEach(fit); if (window.GlassV3 && window.GlassV3.refresh) window.GlassV3.refresh(); }
  window.addEventListener('resize', fitAll);
  document.addEventListener('DOMContentLoaded', function () { applyPal(pal); applyLay(lay); fitAll(); setTimeout(fitAll, 300); });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(fitAll);
  window.aeFitAll = fitAll;

  /* transcript demo: play highlights words by their stored timings. No cursor is drawn on the stage. */
  function demo(box) {
    var playBtn = box.querySelector('.ae-play'), tr = box.querySelector('.ae-transcript'), head = box.querySelector('.ae-scrub__head'), fill = box.querySelector('.ae-scrub__fill'), time = box.querySelector('.ae-player__time b');
    if (!playBtn || !tr) return;
    var len = (+box.getAttribute('data-len') || 432) * 1000, t = +box.getAttribute('data-start') || 188000, timer = null;
    var ws = [].slice.call(tr.querySelectorAll('.ae-w')), lines = [].slice.call(tr.querySelectorAll('.ae-tline'));
    function fmt(ms) { var s = Math.floor(ms / 1000); return ('0' + Math.floor(s / 60)).slice(-2) + ':' + ('0' + s % 60).slice(-2); }
    function paint() {
      tr.classList.add('is-playing');
      var now = null;
      ws.forEach(function (w) { var wt = +w.getAttribute('data-t'); w.classList.toggle('is-past', wt < t - 350); var n = wt <= t && wt >= t - 350; w.classList.toggle('is-now', n); if (n) now = w; });
      lines.forEach(function (l, k) { var lt = +l.getAttribute('data-t'), nx = lines[k + 1] ? +lines[k + 1].getAttribute('data-t') : lt + 9000; l.classList.toggle('is-now', t >= lt && t < nx); });
      var p = Math.min(100, t / len * 100); if (head) head.style.left = p + '%'; if (fill) fill.style.width = p + '%'; if (time) time.textContent = fmt(t);
    }
    function play() { if (timer) return stop(); playBtn.innerHTML = '<svg class="ae-i" style="fill:currentColor;stroke:none"><use href="#i-pause"/></svg>'; timer = setInterval(function () { t += 120; if (t > len) t = 0; paint(); }, 120); }
    function stop() { clearInterval(timer); timer = null; playBtn.innerHTML = '<svg class="ae-i" style="fill:currentColor;stroke:none"><use href="#i-play"/></svg>'; }
    playBtn.addEventListener('click', play);
    lines.forEach(function (l) { l.addEventListener('click', function () { t = +l.getAttribute('data-t'); paint(); }); });
    box.querySelectorAll('[data-jump]').forEach(function (j) { j.addEventListener('click', function () { t = +j.getAttribute('data-jump'); paint(); box.querySelectorAll('.ae-friction').forEach(function (f) { f.classList.toggle('is-active', f === j); }); }); });
    if (playBtn) playBtn.innerHTML = '<svg class="ae-i" style="fill:currentColor;stroke:none"><use href="#i-play"/></svg>';
  }
  document.addEventListener('DOMContentLoaded', function () { document.querySelectorAll('[data-demo="session"]').forEach(demo); });

  /* flows: clickable step sequences with a progress line */
  function flow(f) {
    var frames = [].slice.call(f.querySelectorAll('.flow__frame')), steps = [].slice.call(f.querySelectorAll('.flow__steps li')), caps = [].slice.call(f.querySelectorAll('.flow__capt'));
    var cnt = f.querySelector('.flow__count'), fill = f.querySelector('.ae-flowline__fill'), k = 0;
    function go(n) {
      k = Math.max(0, Math.min(frames.length - 1, n));
      frames.forEach(function (x, j) { x.classList.toggle('is-on', j === k); });
      steps.forEach(function (x, j) { x.classList.toggle('is-on', j === k); });
      caps.forEach(function (x, j) { x.style.display = j === k ? '' : 'none'; });
      if (cnt) cnt.textContent = (k + 1) + ' / ' + frames.length;
      if (fill) fill.style.width = ((k + 1) / frames.length * 100) + '%';
      fitAll();
    }
    f.querySelector('[data-prev]').addEventListener('click', function () { go(k - 1); });
    f.querySelector('[data-next]').addEventListener('click', function () { go(k + 1); });
    steps.forEach(function (s, j) { s.addEventListener('click', function () { go(j); }); });
    f.addEventListener('keydown', function (e) { if (e.key === 'ArrowRight') go(k + 1); if (e.key === 'ArrowLeft') go(k - 1); });
    var st = +(Q.get(f.id) || 0); go(st);
  }
  document.addEventListener('DOMContentLoaded', function () { document.querySelectorAll('.flow').forEach(flow); });
})();
