/* Aero site pages (web3, Team S): copy block, crops of real app screens, phone menu.
   Crops: each .s-crop holds a real 1440px app window. data-sel names the part to show (comma list, union;
   "selector@n" takes the nth match only), data-pad adds native px around it, data-max caps the scale. */
(function () {
  'use strict';
  var D = document, W = window;
  D.documentElement.classList.add('js');

  /* 1. copy: strings in the JSON block replace the words in the page (a headline keeps its round dot) */
  var COPY = {};
  try { COPY = JSON.parse(D.getElementById('copy').textContent); } catch (e) { COPY = {}; }
  D.querySelectorAll('[data-c]').forEach(function (el) {
    var v = COPY[el.getAttribute('data-c')];
    if (typeof v !== 'string') return;
    var d = el.querySelector('.hd-dot');
    if (d) {
      var t = v.replace(/\.$/, '');
      if (el.firstChild && el.firstChild.nodeType === 3) { if (el.firstChild.nodeValue !== t) el.firstChild.nodeValue = t; }
      return;
    }
    if (!el.children.length && el.textContent !== v) el.textContent = v;
  });

  /* 2. crops */
  var crops = [].slice.call(D.querySelectorAll('.s-crop'));
  crops.forEach(function (c) {
    var vp = D.createElement('div'); vp.className = 's-crop-vp';
    var inn = c.querySelector('.s-crop-in'); c.insertBefore(vp, inn); vp.appendChild(inn);
  });
  function measure(c) {
    var inn = c.querySelector('.s-crop-in');
    inn.style.transform = 'none';
    var ir = inn.getBoundingClientRect(), box = null;
    (c.dataset.sel || '').split(',').forEach(function (part) {
      part = part.trim(); if (!part) return;
      var m = part.match(/^(.*)@(\d+)$/), els;
      try { els = [].slice.call(inn.querySelectorAll(m ? m[1] : part)); } catch (e) { els = []; }
      if (m) els = els[+m[2]] ? [els[+m[2]]] : [];
      els.forEach(function (el) {
        var r = el.getBoundingClientRect(); if (!r.width || !r.height) return;
        var b = { l: r.left - ir.left, t: r.top - ir.top, r: r.right - ir.left, b: r.bottom - ir.top };
        box = box ? { l: Math.min(box.l, b.l), t: Math.min(box.t, b.t), r: Math.max(box.r, b.r), b: Math.max(box.b, b.b) } : b;
      });
    });
    if (!box) box = { l: 0, t: 0, r: ir.width, b: ir.height };
    var p = +(c.dataset.pad || 0);
    var bx = { x: Math.max(0, box.l - p), y: Math.max(0, box.t - p), w: box.r - box.l + 2 * p, h: box.b - box.t + 2 * p };
    var cw = +(c.dataset.cw || 0), ch = +(c.dataset.ch || 0), vp = c.firstElementChild;
    /* on a phone, keep text readable: a wide part keeps its first 420 native px (data-mcw sets another width, 0 = never) */
    if (W.innerWidth <= 760 && c.dataset.mcw !== '0') { var m = +(c.dataset.mcw || 420); cw = cw ? Math.min(cw, m) : m; }
    vp.classList.toggle('cut-r', !!(cw && bx.w > cw)); vp.classList.toggle('cut-b', !!(ch && bx.h > ch));
    if (cw && bx.w > cw) bx.w = cw;
    if (ch && bx.h > ch) bx.h = ch;
    c._box = bx;
  }
  function fit() {
    crops.forEach(function (c) {
      if (!c._box) measure(c);
      var b = c._box, inn = c.querySelector('.s-crop-in'), vp = c.firstElementChild;
      var Wc = c.clientWidth, Hc = c.classList.contains('fill') || getComputedStyle(c).getPropertyValue('--fill').trim() === '1' ? c.clientHeight : 0;
      var mx = +(c.dataset.max || 1.6);
      var k = Math.min(Wc / b.w, mx);
      if (Hc) k = Math.min(k, Hc / b.h);
      vp.style.width = Math.round(b.w * k) + 'px';
      vp.style.height = Math.round(b.h * k) + 'px';
      if (!Hc) c.style.height = Math.round(b.h * k) + 'px';
      inn.style.transform = 'scale(' + k + ') translate(' + (-b.x) + 'px,' + (-b.y) + 'px)';
      c.classList.add('ready');
    });
  }
  function remeasure() { crops.forEach(function (c) { c._box = null; }); fit(); }
  fit();
  var rt, wasPhone = W.innerWidth <= 760;
  W.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(function () { var ph = W.innerWidth <= 760; if (ph !== wasPhone) { wasPhone = ph; remeasure(); } else fit(); }, 60); });
  if (D.fonts && D.fonts.ready) D.fonts.ready.then(remeasure);
  W.addEventListener('load', remeasure);

  /* 3. phone menu */
  var nav = D.querySelector('.site-nav'), bt = D.querySelector('.site-burger');
  if (nav && bt) bt.addEventListener('click', function () {
    var o = nav.classList.toggle('open'); bt.setAttribute('aria-expanded', o ? 'true' : 'false');
  });
  D.addEventListener('keydown', function (e) { if (e.key === 'Escape' && nav && nav.classList.contains('open')) { nav.classList.remove('open'); bt.setAttribute('aria-expanded', 'false'); bt.focus(); } });
})();
