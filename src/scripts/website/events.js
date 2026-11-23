/* Aero website: which button was pressed, and where. Runs on every page.
   1. Links into the app (sign up, log in, new test, sites) get ?from=<page>, so the app can record which page a
      sign-up came from. An existing ?from= (the home page demo links set one) is kept.
   2. One Plausible event, "CTA click", with props page and target, for the main buttons. Add "CTA click" as a goal
      in Plausible (aeroapp.ai) once, then filter it by the page and target props. Never throws; does nothing when
      Plausible is blocked. */
(function () {
  'use strict';
  var D = document, W = window, L = W.location;

  function pageName() {
    var p = (L.pathname || '/').replace(/^\/+|\/+$/g, '');
    return p ? p.replace(/\//g, '-') : 'home';
  }

  /* What a link is, from where it points. Anything else gets no event. */
  function kindOf(u) {
    var host = u.hostname.replace(/^www\./, ''), path = u.pathname.replace(/\/+$/, '');
    if (host === 'aeroapp.ai') {
      if (path === '/signup') return 'sign up';
      if (path === '/login') return 'log in';
      if (path === '/pricing') return 'pricing';
      if (path === '/new' || path === '/sites' || path.indexOf('/user-testing') === 0) return 'open app';
    }
    if (host === 'app.aeroapp.ai') return 'open app';
    if (host === 'figma.com' && path.indexOf('/community/plugin') === 0) return 'plugin install';
    return '';
  }

  function toUrl(a) {
    try { return new URL(a.getAttribute('href'), L.href); } catch (e) { return null; }
  }

  var from = pageName();
  var APP_PATHS = { '/signup': 1, '/login': 1, '/new': 1, '/sites': 1 };
  D.querySelectorAll('a[href]').forEach(function (a) {
    var u = toUrl(a);
    if (!u) return;
    var host = u.hostname.replace(/^www\./, ''), path = u.pathname.replace(/\/+$/, '');
    if ((host === 'aeroapp.ai' && APP_PATHS[path]) || host === 'app.aeroapp.ai') {
      if (!u.searchParams.has('from')) {
        u.searchParams.set('from', from);
        a.setAttribute('href', u.href);
      }
    }
  });

  D.addEventListener('click', function (e) {
    try {
      var a = e.target && e.target.closest ? e.target.closest('a[href]') : null;
      if (!a) return;
      var u = toUrl(a);
      if (!u) return;
      var kind = kindOf(u);
      if (!kind || typeof W.plausible !== 'function') return;
      W.plausible('CTA click', { props: { page: from, target: kind } });
    } catch (err) { /* tracking is best effort */ }
  }, true);
})();
