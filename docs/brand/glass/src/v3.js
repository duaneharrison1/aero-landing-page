  /* ===== V3: From research =====
     A capsule of glass modelled the way kube.io and liquid-glass-react describe it:
     - refraction: a convex squircle lip, Snell's law (n = 1.5) gives the displacement per depth, baked into
       an feDisplacementMap used by backdrop-filter (Chromium; elsewhere a plain frost)
     - reflection: the environment is reflected only where the lip is steep, by a Schlick Fresnel term,
       so colour sits in a fine line right at the edge and nowhere else
     - specular: a fixed key light from the top left catches the lip (and faintly the opposite lip, as
       light passing through), plus a soft pointer light on hover */
  var CSSTXT = ':where(.g3){position:relative}.g3{display:inline-flex;align-items:center;justify-content:center;gap:6px;font:inherit;font-size:14px;font-weight:590;letter-spacing:-.005em;line-height:1.2;padding:10px 18px;border:0;border-radius:999px;color:var(--g3-fg);background:var(--g3-bg);box-shadow:var(--g3-sh);cursor:pointer;white-space:nowrap;-webkit-tap-highlight-color:transparent;transition:transform .5s cubic-bezier(.25,1.6,.45,1)}' +
    '.g3:hover:not(:disabled){transform:scale(1.02)}.g3:active:not(:disabled){transform:scale(.97);transition-duration:.12s}' +
    '.g3:focus-visible{outline:2px solid var(--g3-ring);outline-offset:3px}.g3:disabled{opacity:.45;cursor:not-allowed;transform:none}' +
    '.g3>canvas{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;border-radius:inherit}.g3>span{position:relative;display:inline-flex;align-items:center;gap:6px}' +
    '.g3-primary{--g3-bg:rgb(var(--g3-f));--g3-sh:0 1px 2px rgba(0,0,0,.16),0 4px 12px rgba(0,0,0,.06);--g3-ring:rgb(var(--g3-f))}' +
    '.g3-secondary{--g3-bg:rgba(255,255,255,var(--g3-a,.38));--g3-sh:0 1px 2px rgba(0,0,0,.05),0 4px 14px rgba(0,0,0,.05),inset 0 0 0 .5px rgba(0,0,0,.1);--g3-ring:#1D1D1F}' +
    '.g3-dark{--g3-bg:rgba(var(--g3-f),var(--g3-a,.28));--g3-sh:0 1px 2px rgba(0,0,0,.35),inset 0 0 0 .5px rgba(255,255,255,.14);--g3-ring:#F5F5F7}' +
    '@media (prefers-reduced-motion:reduce){.g3,.g3:hover,.g3:active{transition:none;transform:none}}';
  var styled = false, KEY = [-.42, -.91]; // key light: from the top left

  function glassV3(btn, o) {
    if (btn._g3) return btn._g3;
    o = o || {};
    if (!styled) { var st = D.createElement('style'); st.textContent = CSSTXT; D.head.appendChild(st); styled = true; }
    var B = setupButton(btn, o), cv = B.cv, ctx = B.ctx, prim = B.prim, dark = B.dark;
    var w = 0, h = 0, r = 20, dpr = 1, sized = '', rim = [], tgt = null, cur = null, alpha = null, band = null, img = null, ok = false, opt = null;
    var api = { el: btn, variant: B.variant }, lab = null;

    api.scan = function () {
      var R = btn.getBoundingClientRect(); ok = !!(R.width && R.height); if (!ok) return;
      w = Math.round(R.width); h = Math.round(R.height);
      r = Math.min(parseFloat(getComputedStyle(btn).borderTopLeftRadius) || 0, h / 2);
      var bh = behind(btn, R, B.fg), surface = surfaceOf(B, bh.base, .38, .28);
      var S = sampleAround(btn, R, r, toLab(surface));
      var n = Math.max(24, Math.round((2 * w + 2 * h) / 3)), pts = rrPts(.5, .5, w - 1, h - 1, r - .5, n);
      var Lr = lightRim(pts, S, 22), a = rimAlpha(Lr, 2.4 * B.str * intensity() * (B.colour ? 1.6 : 1), .62, .11), Lt = prim || dark ? .84 : .7;
      var t = new Float32Array(n * 4);
      for (var i = 0; i < n; i++) { var c = reflectOn(B, Lr.A[i], Lr.B[i], Lt, .15); t[i * 4] = c[0]; t[i * 4 + 1] = c[1]; t[i * 4 + 2] = c[2]; t[i * 4 + 3] = a[i]; }
      if (!cur || cur.length !== t.length) cur = null;
      rim = pts; tgt = t;
      lab = liquidLabel(B, bh.worst); if (!prim) alpha = glassAlpha(B.fg, bh.worst, dark, B.fill, dark ? .28 : .38); else if (B.tint) alpha = glassAlpha(B.fg, bh.worst, true, B.fill, B.fa, B.dim);
    };
    // per band pixel optics: Fresnel reflectance and specular weight, from the lip's slope at that depth
    function optics() {
      var bez = Math.min(14, h / 2 - 1), m = band.ix.length, fr = new Float32Array(m), sp = new Float32Array(m), F0 = .04, e0 = null;
      function slope(d) { var t = Math.max(.004, d / bez), u = 1 - t, base = 1 - u * u * u * u; return Math.atan(Math.pow(base, -.75) * u * u * u * .55); }
      function fres(d) { var c = Math.cos(slope(d)); return F0 + (1 - F0) * Math.pow(1 - c, 2); }
      e0 = fres(.35);
      for (var j = 0; j < m; j++) {
        var d = Math.max(0, band.d[j]), al = slope(d), nl = band.nx[j] * KEY[0] + band.ny[j] * KEY[1], sn = Math.sin(al);
        fr[j] = Math.min(1, fres(d) / e0);
        sp[j] = sn * sn * sn * (Math.pow(Math.max(0, nl), 2) + .35 * Math.pow(Math.max(0, -nl), 2));
      }
      return { fr: fr, sp: sp, bez: bez };
    }
    api.write = function () {
      if (!ok || !tgt) return;
      var key = w + 'x' + h + 'r' + r + 'n' + rim.length + (liquid() ? 'L' : 'S') + (btn._busy ? 'b' : '');
      if (key !== sized) {
        sized = key; dpr = Math.min(W.devicePixelRatio || 1, 2);
        cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr);
        band = buildBand(w, h, r, dpr, rim, Math.min(14, h / 2 - 1)); img = ctx.createImageData(cv.width, cv.height); opt = optics(); cur = null;
        applyRefract(api, B, btn, w, h, r, { snell: true, bez: opt.bez, scale: (dark ? 16 : 20) * Math.min(B.str, 2.5), post: 'blur(.3px) saturate(1.4)', fallback: 'blur(3px) saturate(1.5) brightness(1.03)' });
      }
      if (alpha != null) btn.style.setProperty('--g3-a', alpha.toFixed(2));
      applyMode(btn, lab);
      if (!cur) cur = tgt.slice();
      anim.kick();
    };

    function draw(s) {
      ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.clearRect(0, 0, cv.width, cv.height);
      if (!cur || !band) return;
      var D2 = img.data, lift = s.k * Math.min(B.str, 2), sig = 2 * 26 * 26, keyA = prim ? .3 : dark ? .38 : .7;
      var envK = prim ? 1.7 : 1.6;
      D2.fill(0);
      for (var j = 0; j < band.ix.length; j++) {
        var d = band.d[j], ri = band.ri[j], q = ri * 4, cov = clamp(d * dpr + .5, 0, 1);
        var a1 = Math.min(1, cur[q + 3] * opt.fr[j] * envK) * cov; // reflected environment
        var sp = opt.sp[j] * keyA;                                   // key light on the lip
        if (lift > .001) { var dx = rim[ri].x - s.sx, dy = rim[ri].y - s.sy; sp += Math.exp(-(dx * dx + dy * dy) / sig) * lift * .9 * opt.fr[j]; }
        var a2 = Math.min(1, sp) * cov, A = a1 + a2 - a1 * a2; if (A < .003) continue;
        var p = band.ix[j];
        D2[p] = (cur[q] * a1 * (1 - a2) + 255 * a2) / A; D2[p + 1] = (cur[q + 1] * a1 * (1 - a2) + 255 * a2) / A; D2[p + 2] = (cur[q + 2] * a1 * (1 - a2) + 255 * a2) / A; D2[p + 3] = A * 255;
      }
      ctx.putImageData(img, 0, 0);
      if (lift > .001) {
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0); ctx.save(); rrPath(ctx, 0, 0, w, h, r); ctx.clip();
        var g = ctx.createRadialGradient(s.sx, s.sy, 0, s.sx, s.sy, Math.max(w, h) * .55);
        g.addColorStop(0, rgba(WHITE, lift * (prim ? .06 : dark ? .07 : .22))); g.addColorStop(1, rgba(WHITE, 0));
        ctx.fillStyle = g; ctx.fillRect(0, 0, w, h); ctx.restore();
      }
    }
    var anim = animator(btn, draw, function (f) { return cur && tgt && cur.length === tgt.length ? easeArr(cur, tgt, f) : false; });
    api.update = function () { refresh(true); };
    btn._g3 = api; register(api); refresh();
    return api;
  }
  boot(glassV3, 'GlassV3');
