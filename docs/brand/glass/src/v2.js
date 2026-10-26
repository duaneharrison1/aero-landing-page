  /* ===== V2: Liquid glass, fixed =====
     liquid-glass.js (per-rim-point lighting, per-pixel hairline + short wash, edge refraction), with:
     - salience from OKLCH chroma and colour contrast instead of max(chroma, luminance difference),
       which is what drew a dark rim on a white button sitting next to a black one
     - the reflection takes the source's hue at a fixed lightness, so a dark navy never paints a dark line
     - ambient removed, a soft knee per point and a total budget for the rim */
  var CSSTXT = ':where(.g2){position:relative}.g2{display:inline-flex;align-items:center;justify-content:center;gap:6px;font:inherit;font-size:14px;font-weight:560;line-height:1.2;padding:9px 16px;border:0;border-radius:12px;color:var(--g2-fg);background:var(--g2-bg);box-shadow:var(--g2-sh);cursor:pointer;white-space:nowrap;-webkit-tap-highlight-color:transparent;touch-action:manipulation;transition:transform .45s cubic-bezier(.3,1.5,.5,1)}' +
    '.g2:active{transform:scale(1.025,.94);transition-duration:.1s}' +
    '.g2:focus-visible{outline:2px solid var(--g2-ring);outline-offset:3px}.g2:disabled{opacity:.45;cursor:not-allowed;transform:none}' +
    '.g2>canvas{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;border-radius:inherit}.g2>span{position:relative;display:inline-flex;align-items:center;gap:6px}' +
    '.g2-primary{--g2-bg:rgb(var(--g2-f));--g2-sh:0 1px 2px rgba(0,0,0,.14),inset 0 1px 0 rgba(255,255,255,.12);--g2-ring:rgb(var(--g2-f))}' +
    '.g2-secondary{--g2-bg:rgba(255,255,255,var(--g2-a,.45));--g2-sh:0 1px 2px rgba(0,0,0,.05),inset 0 0 0 .5px rgba(0,0,0,.12),inset 0 1px 0 rgba(255,255,255,.7);--g2-ring:#1D1D1F}' +
    '.g2-dark{--g2-bg:linear-gradient(rgba(255,255,255,.08),rgba(255,255,255,.02)),rgba(var(--g2-f),var(--g2-a,.3));--g2-sh:0 1px 2px rgba(0,0,0,.3),inset 0 0 0 .5px rgba(255,255,255,.16),inset 0 1px 0 rgba(255,255,255,.1);--g2-ring:#F5F5F7}' +
    '@media (prefers-reduced-motion:reduce){.g2,.g2:active{transition:none;transform:none}}';
  var styled = false;

  function glassV2(btn, o) {
    if (btn._g2) return btn._g2;
    o = o || {};
    if (!styled) { var st = D.createElement('style'); st.textContent = CSSTXT; D.head.appendChild(st); styled = true; }
    var B = setupButton(btn, o), cv = B.cv, ctx = B.ctx, prim = B.prim, dark = B.dark;
    var w = 0, h = 0, r = 12, dpr = 1, sized = '', rim = [], tgt = null, cur = null, alpha = null, band = null, img = null, ok = false;
    var api = { el: btn, variant: B.variant }, lab = null;

    api.scan = function () {
      var R = btn.getBoundingClientRect(); ok = !!(R.width && R.height); if (!ok) return;
      w = Math.round(R.width); h = Math.round(R.height);
      r = Math.min(parseFloat(getComputedStyle(btn).borderTopLeftRadius) || 0, h / 2);
      var bh = behind(btn, R, B.fg), surface = surfaceOf(B, bh.base, .45, .3);
      var S = sampleAround(btn, R, r, toLab(surface));
      var n = Math.max(24, Math.round((2 * w + 2 * h) / 3)), pts = rrPts(.5, .5, w - 1, h - 1, r - .5, n);
      var Lr = lightRim(pts, S, 22), a = rimAlpha(Lr, 2.4 * B.str * intensity() * (B.colour ? 1.6 : 1), .6, .11), Lt = prim || dark ? .82 : .72;
      var t = new Float32Array(n * 4);
      for (var i = 0; i < n; i++) { var c = reflectOn(B, Lr.A[i], Lr.B[i], Lt, .14); t[i * 4] = c[0]; t[i * 4 + 1] = c[1]; t[i * 4 + 2] = c[2]; t[i * 4 + 3] = a[i]; }
      if (!cur || cur.length !== t.length) cur = null;
      rim = pts; tgt = t;
      lab = liquidLabel(B, bh.worst); if (!prim) alpha = glassAlpha(B.fg, bh.worst, dark, B.fill, dark ? .3 : .42); else if (B.tint) alpha = glassAlpha(B.fg, bh.worst, true, B.fill, B.fa, B.dim);
    };
    api.write = function () {
      if (!ok || !tgt) return;
      var key = w + 'x' + h + 'r' + r + 'n' + rim.length + (liquid() ? 'L' : 'S') + (btn._busy ? 'b' : '');
      if (key !== sized) {
        sized = key; dpr = Math.min(W.devicePixelRatio || 1, 2);
        cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr);
        band = buildBand(w, h, r, dpr, rim, 8); img = ctx.createImageData(cv.width, cv.height); cur = null;
        applyRefract(api, B, btn, w, h, r, { bez: Math.min(16, h / 2 - 1), scale: (dark ? 14 : 18) * Math.min(B.str, 2.5), post: 'blur(.4px) saturate(1.25)', fallback: 'blur(2px) saturate(1.3)' });
      }
      if (alpha != null) btn.style.setProperty('--g2-a', alpha.toFixed(2));
      applyMode(btn, lab);
      if (!cur) cur = tgt.slice();
      anim.kick();
    };

    function draw(s) {
      ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.clearRect(0, 0, cv.width, cv.height);
      if (!cur || !band) return;
      var D2 = img.data, n = rim.length, i, lift = s.k * Math.min(B.str, 2), sig = 2 * 30 * 30, spec = new Float32Array(n);
      D2.fill(0);
      if (lift > .001) for (i = 0; i < n; i++) { var dx = rim[i].x - s.sx, dy = rim[i].y - s.sy; spec[i] = Math.exp(-(dx * dx + dy * dy) / sig) * lift * (prim ? .5 : .85); }
      for (var j = 0; j < band.ix.length; j++) {
        var d = band.d[j], ri = band.ri[j], q = ri * 4, cov = clamp(d * dpr + .5, 0, 1);
        var hair = Math.exp(-((d - .6) * (d - .6)) / .3), wash = Math.exp(-d / (prim ? 4.5 : 3.2));
        var a1 = Math.min(1, cur[q + 3] * (hair * (prim ? .8 : .95) + wash * (prim ? .42 : .34))) * cov, a2 = Math.min(1, spec[ri] * (hair + wash * .25)) * cov;
        var A = a1 + a2 - a1 * a2; if (A < .003) continue;
        var p = band.ix[j];
        D2[p] = (cur[q] * a1 * (1 - a2) + 255 * a2) / A; D2[p + 1] = (cur[q + 1] * a1 * (1 - a2) + 255 * a2) / A; D2[p + 2] = (cur[q + 2] * a1 * (1 - a2) + 255 * a2) / A; D2[p + 3] = A * 255;
      }
      ctx.putImageData(img, 0, 0);
      if (lift > .001) {
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0); ctx.save(); rrPath(ctx, 0, 0, w, h, r); ctx.clip();
        var g = ctx.createRadialGradient(s.sx, s.sy, 0, s.sx, s.sy, Math.max(w, h) * .6);
        g.addColorStop(0, rgba(WHITE, lift * (prim ? .07 : dark ? .08 : .28))); g.addColorStop(1, rgba(WHITE, 0));
        ctx.fillStyle = g; ctx.fillRect(0, 0, w, h); ctx.restore();
      }
    }
    var anim = animator(btn, draw, function (f) { return cur && tgt && cur.length === tgt.length ? easeArr(cur, tgt, f) : false; });
    api.update = function () { refresh(true); };
    api.destroy = function () { if (api.filter) api.filter.remove(); cv.remove(); delete btn._g2; };
    btn._g2 = api; register(api); refresh();
    return api;
  }
  boot(glassV2, 'GlassV2');
