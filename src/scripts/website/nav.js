/* Aero website: the phone menu in the shared header (every page). */
(function () {
  'use strict';
  var D = document;
  var nav = D.querySelector('.site-nav'), bt = D.querySelector('.site-burger');
  if (!nav || !bt) return;
  bt.addEventListener('click', function () {
    var o = nav.classList.toggle('open'); bt.setAttribute('aria-expanded', o ? 'true' : 'false');
  });
  D.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && nav.classList.contains('open')) { nav.classList.remove('open'); bt.setAttribute('aria-expanded', 'false'); bt.focus(); }
  });
})();
