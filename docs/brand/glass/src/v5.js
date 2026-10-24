  /* ===== V5: Reference benchmark =====
     A faithful port of liquid-glass-react 1.1.1 (MIT, Max Rovensky, github.com/rdev/liquid-glass-react),
     at its published defaults: displacementScale 70, blurAmount 0.0625 (backdrop blur 4 + 0.0625*32 = 6px),
     saturation 140, aberrationIntensity 2, mode "standard" (its own embedded displacement map).
     Same structure as the library:
     - a warp layer with backdrop-filter blur(6px) saturate(140%) AND filter: url(#f) on top of it
     - the filter: three feDisplacementMap passes at -70, -77, -84 (R, G, B), screen-blended, blurred 0.3,
       kept only at the edge by a mask built from the map, the clean backdrop in the centre
     - two 1.5px masked gradient rims (screen at 0.2, and overlay) for the specular edge
     - 0 12px 40px rgba(0,0,0,.25) shadow, white label with a soft text shadow, overlay glow on hover
     Not ported: the elastic cursor-follow stretch (lab buttons stay put).
     One deviation, for AA: a dark tint layer under the label rises only as far as white text needs
     over the worst point behind it (the library has no contrast handling). Not part of the Subtle /
     Liquid switch: it always shows the library's own strength. */
  var MAP = '__MAP__', DS = 70, AB = 2;
  var CSSTXT = ':where(.g5){position:relative}.g5{display:inline-flex;align-items:center;justify-content:center;gap:8px;font:inherit;font-size:15px;font-weight:500;line-height:1;padding:12px 22px;border:0;border-radius:999px;background:transparent;color:var(--g5-fg);cursor:pointer;white-space:nowrap;overflow:hidden;box-shadow:0 12px 40px rgba(0,0,0,.25);transition:transform .2s ease-out}' +
    '.g5:active:not(:disabled){transform:scale(.96)}.g5:focus-visible{outline:2px solid var(--g5-fg);outline-offset:3px}.g5:disabled{opacity:.45;cursor:not-allowed}' +
    '.g5>canvas{display:none}.g5>svg{position:absolute;left:0;top:0;width:100%;height:100%;pointer-events:none}' +
    '.g5>.g5-w,.g5>.g5-t,.g5>.g5-h,.g5>.g5-r{position:absolute;inset:0;border-radius:inherit;pointer-events:none}' +
    '.g5>.g5-w{backdrop-filter:blur(6px) saturate(140%);-webkit-backdrop-filter:blur(6px) saturate(140%)}' +
    '.g5>.g5-t{background:var(--g5-tint,transparent)}' +
    '.g5>span.g5-l{position:relative;z-index:1;display:inline-flex;align-items:center;gap:6px;text-shadow:var(--g5-ts,0 2px 12px rgba(0,0,0,.4))}' +
    '.g5>.g5-r{padding:1.5px;-webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask-composite:exclude;box-shadow:0 0 0 .5px rgba(255,255,255,.5) inset,0 1px 3px rgba(255,255,255,.25) inset,0 1px 4px rgba(0,0,0,.35)}' +
    '.g5>.g5-r1{mix-blend-mode:screen;opacity:.2;background:linear-gradient(135deg,rgba(255,255,255,0) 0%,rgba(255,255,255,.12) 33%,rgba(255,255,255,.4) 66%,rgba(255,255,255,0) 100%)}' +
    '.g5>.g5-r2{mix-blend-mode:overlay;background:linear-gradient(135deg,rgba(255,255,255,0) 0%,rgba(255,255,255,.32) 33%,rgba(255,255,255,.6) 66%,rgba(255,255,255,0) 100%)}' +
    '.g5>.g5-h{opacity:0;background-image:radial-gradient(circle at 50% 0%,rgba(255,255,255,1) 0%,rgba(255,255,255,0) 100%);mix-blend-mode:overlay;transition:opacity .2s ease-out}' +
    '.g5:hover>.g5-h{opacity:.4}.g5:active>.g5-h{opacity:.8}' +
    '@media (prefers-reduced-motion:reduce){.g5,.g5:active{transition:none;transform:none}.g5>.g5-h{transition:none}}';
  var styled = false, fid = 0;
  function filterMarkup(id) { // liquid-glass-react GlassFilter, mode "standard"
    var m = function (v) { return '<feColorMatrix in="' + v[0] + '" type="matrix" values="' + v[1] + '" result="' + v[2] + '"/>'; };
    var dm = function (sc, res) { return '<feDisplacementMap in="SourceGraphic" in2="DISPLACEMENT_MAP" scale="' + sc + '" xChannelSelector="R" yChannelSelector="B" result="' + res + '"/>'; };
    return '<defs><filter id="' + id + '" x="-35%" y="-35%" width="170%" height="170%" color-interpolation-filters="sRGB">' +
      '<feImage x="0" y="0" width="100%" height="100%" result="DISPLACEMENT_MAP" href="' + MAP + '" preserveAspectRatio="xMidYMid slice"/>' +
      m(['DISPLACEMENT_MAP', '0.3 0.3 0.3 0 0 0.3 0.3 0.3 0 0 0.3 0.3 0.3 0 0 0 0 0 1 0', 'EDGE_INTENSITY']) +
      '<feComponentTransfer in="EDGE_INTENSITY" result="EDGE_MASK"><feFuncA type="discrete" tableValues="0 ' + (AB * .05) + ' 1"/></feComponentTransfer>' +
      '<feOffset in="SourceGraphic" dx="0" dy="0" result="CENTER_ORIGINAL"/>' +
      dm(-DS, 'RED_DISPLACED') + m(['RED_DISPLACED', '1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0', 'RED_CHANNEL']) +
      dm(DS * (-1 - AB * .05), 'GREEN_DISPLACED') + m(['GREEN_DISPLACED', '0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 1 0', 'GREEN_CHANNEL']) +
      dm(DS * (-1 - AB * .1), 'BLUE_DISPLACED') + m(['BLUE_DISPLACED', '0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 1 0', 'BLUE_CHANNEL']) +
      '<feBlend in="GREEN_CHANNEL" in2="BLUE_CHANNEL" mode="screen" result="GB_COMBINED"/><feBlend in="RED_CHANNEL" in2="GB_COMBINED" mode="screen" result="RGB_COMBINED"/>' +
      '<feGaussianBlur in="RGB_COMBINED" stdDeviation="' + Math.max(.1, .5 - AB * .1) + '" result="ABERRATED_BLURRED"/>' +
      '<feComposite in="ABERRATED_BLURRED" in2="EDGE_MASK" operator="in" result="EDGE_ABERRATION"/>' +
      '<feComponentTransfer in="EDGE_MASK" result="INVERTED_MASK"><feFuncA type="table" tableValues="1 0"/></feComponentTransfer>' +
      '<feComposite in="CENTER_ORIGINAL" in2="INVERTED_MASK" operator="in" result="CENTER_CLEAN"/>' +
      '<feComposite in="EDGE_ABERRATION" in2="CENTER_CLEAN" operator="over"/></filter></defs>';
  }
  function glassV5(btn, o) {
    if (btn._g5) return btn._g5;
    o = o || {};
    if (!styled) { var st = D.createElement('style'); st.textContent = CSSTXT; D.head.appendChild(st); styled = true; }
    var B = setupButton(btn, o), prim = B.prim, tintA = 0, fg = prim ? B.fg : WHITE, ok = false;
    B.cv.remove();
    var label = btn.querySelector(':scope>span'); label.classList.add('g5-l');
    function el(tag, cls) { var e = D.createElement(tag); e.className = cls; e.setAttribute('aria-hidden', 'true'); return e; }
    var id = 'g5lg' + (++fid), svg = D.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('aria-hidden', 'true'); svg.innerHTML = filterMarkup(id);
    var warp = el('span', 'g5-w'), tint = el('span', 'g5-t');
    if (!/Firefox\//.test(UA)) warp.style.filter = 'url(#' + id + ')'; // the library also skips the filter in Firefox
    btn.insertBefore(svg, label); btn.insertBefore(warp, label); btn.insertBefore(tint, label);
    btn.appendChild(el('span', 'g5-r g5-r1')); btn.appendChild(el('span', 'g5-r g5-r2')); btn.appendChild(el('span', 'g5-h'));
    var api = { el: btn, variant: B.variant };
    api.scan = function () {
      var R = btn.getBoundingClientRect(); ok = !!(R.width && R.height); if (!ok) return;
      var bh = behind(btn, R, fg);
      // primary: the fill as a tint layer (opaque fills stay opaque); clear: a dark tint only as far as AA needs
      tintA = prim ? (B.tint ? glassAlpha(fg, bh.worst, true, B.fill, B.fa) : 1) : glassAlpha(WHITE, bh.worst, true, [0, 0, 0], 0);
    };
    api.write = function () {
      if (!ok) return;
      btn.style.setProperty('--g5-fg', 'rgb(' + fg.join(',') + ')');
      btn.style.setProperty('--g5-tint', rgba(prim ? B.fill : [0, 0, 0], tintA));
      if (fg[0] < 128) btn.style.setProperty('--g5-ts', 'none');
    };
    api.update = function () { refresh(true); };
    btn._g5 = api; register(api); refresh();
    return api;
  }
  boot(glassV5, 'GlassV5');
