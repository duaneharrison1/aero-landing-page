/* Tester board and flow helpers. No dependencies.
   - Scales every .tb-shot[data-w] to its column (screens are authored at real size: 1280x800 or 390x844).
   - Re-runs the V3 glass after scaling.
   - Drives tester-flow.html: one screen at a time, hotspots with [data-go]. */
(function () {
  'use strict';
  function fit() {
    document.querySelectorAll('.tb-shot[data-w]').forEach(function (s) {
      var w = +s.dataset.w, h = +s.dataset.h, k = s.clientWidth / w;
      if (!k) return;
      var sc = s.firstElementChild;
      sc.style.transform = 'scale(' + k + ')';
      s.style.height = Math.round(h * k) + 'px';
    });
    if (window.GlassV3 && window.GlassV3.refresh) { try { window.GlassV3.refresh(); } catch (e) { /* glass is decoration */ } }
  }
  var t;
  window.addEventListener('resize', function () { clearTimeout(t); t = setTimeout(fit, 80); });
  document.addEventListener('DOMContentLoaded', fit);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(fit);
  window.addEventListener('load', function () { fit(); setTimeout(fit, 400); });
  window.testerFit = fit;

  /* ---------- flow player ---------- */
  function flow() {
    var root = document.querySelector('[data-flow-root]');
    if (!root || !window.TESTER_FLOWS) return;
    var flows = window.TESTER_FLOWS, ids = Object.keys(flows);
    var state = { f: (window.innerWidth < 600 && flows.phone) ? 'phone' : ids[0], i: 0 };
    try { var h = new URLSearchParams(location.hash.slice(1)); if (flows[h.get('f')]) { state.f = h.get('f'); state.i = Math.min(+h.get('s') || 0, flows[state.f].steps.length - 1); } } catch (e) { }
    var picker = document.querySelector('[data-flow-picker]'), dots = document.querySelector('[data-flow-dots]'),
      note = document.querySelector('[data-flow-note]'), count = document.querySelector('[data-flow-count]'),
      title = document.querySelector('[data-flow-title]');
    picker.innerHTML = ids.map(function (id) { return '<button type="button" data-f="' + id + '">' + flows[id].name + '</button>'; }).join('');
    picker.addEventListener('click', function (e) { var b = e.target.closest('[data-f]'); if (b) { state.f = b.dataset.f; state.i = 0; show(); } });
    function show() {
      var fl = flows[state.f], st = fl.steps[state.i];
      root.querySelectorAll('[data-screen]').forEach(function (s) { s.hidden = s.dataset.screen !== st.screen; });
      var cur = root.querySelector('[data-screen="' + st.screen + '"]');
      picker.querySelectorAll('[data-f]').forEach(function (b) { b.classList.toggle('is-on', b.dataset.f === state.f); b.setAttribute('aria-pressed', b.dataset.f === state.f); });
      dots.innerHTML = fl.steps.map(function (s, k) { return '<button type="button" data-k="' + k + '" class="' + (k === state.i ? 'is-on' : '') + '" aria-label="Step ' + (k + 1) + ': ' + s.label + '"><span>' + s.label + '</span></button>'; }).join('');
      note.innerHTML = st.note || '';
      count.textContent = (state.i + 1) + ' of ' + fl.steps.length;
      title.textContent = fl.name;
      try { history.replaceState(null, '', '#f=' + state.f + '&s=' + state.i); } catch (e) { }
      // hotspot: the element that moves this step on pulses once
      root.querySelectorAll('.is-hot').forEach(function (x) { x.classList.remove('is-hot'); });
      if (cur && st.hot) { var hs = cur.querySelectorAll(st.hot); var el = hs[st.hotIndex || 0]; if (el) { el.classList.add('is-hot'); el.setAttribute('data-go', 'next'); } }
      fit();
    }
    dots.addEventListener('click', function (e) { var b = e.target.closest('[data-k]'); if (b) { state.i = +b.dataset.k; show(); } });
    function go(d) { var n = flows[state.f].steps.length; state.i = Math.max(0, Math.min(n - 1, state.i + d)); show(); }
    document.querySelector('[data-flow-prev]').addEventListener('click', function () { go(-1); });
    document.querySelector('[data-flow-next]').addEventListener('click', function () { go(1); });
    root.addEventListener('click', function (e) { if (e.target.closest('.is-hot')) { e.preventDefault(); go(1); } });
    document.addEventListener('keydown', function (e) { if (e.key === 'ArrowRight') go(1); if (e.key === 'ArrowLeft') go(-1); });
    show();
  }
  document.addEventListener('DOMContentLoaded', flow);
})();
