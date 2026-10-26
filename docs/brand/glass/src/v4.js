  /* ===== V4: Hybrid =====
     The original's character on V2/V3's engine:
     - original: the 170deg sheen and inset highlights, the body tint pulled toward the strongest source,
       the R / colour / B caustic split (here per pixel: red sits outermost, blue innermost, sub-pixel apart),
       and the pointer caustic (a highlight under the pointer plus a fainter focus mirrored across the button)
     - V2: per-rim-point sampling with distance, coverage, chroma and contrast, ambient removed, clamped
     - V3: Snell-law lip refraction, here with a slight chromatic split (three displacement scales) */
  var CSSTXT = ':where(.g4){position:relative}.g4{display:inline-flex;align-items:center;justify-content:center;gap:6px;font:inherit;font-size:14px;font-weight:550;letter-spacing:.005em;line-height:1.2;padding:9px 17px;border:0;border-radius:10px;cursor:pointer;white-space:nowrap;isolation:isolate;color:var(--g4-fg);background:var(--g4-bg);box-shadow:var(--g4-sh);-webkit-tap-highlight-color:transparent;transition:transform .18s cubic-bezier(.2,.8,.2,1)}' +
    '.g4:hover:not(:disabled){transform:translateY(-.5px)}.g4:active:not(:disabled){transform:scale(.975);transition-duration:.1s}' +
    '.g4:focus-visible{outline:2px solid var(--g4-ring);outline-offset:3px}.g4:disabled{opacity:.45;cursor:not-allowed;transform:none}' +
    '.g4>canvas{position:absolute;inset:0;width:100%;height:100%;z-index:1;pointer-events:none;border-radius:inherit}.g4>span{position:relative;z-index:5;display:inline-flex;align-items:center;gap:6px}' +
    '.g4::after{content:"";position:absolute;inset:0;z-index:4;border-radius:inherit;pointer-events:none;background:linear-gradient(170deg,rgba(255,255,255,var(--g4-sn)) 0%,rgba(255,255,255,calc(var(--g4-sn)*.12)) 28%,transparent 55%);box-shadow:inset 0 1px 0 rgba(255,255,255,var(--g4-hi)),inset 0 -1px 0 rgba(255,255,255,.06)}' +
    '.g4-primary{--g4-bg:rgb(var(--g4-f));--g4-sn:.14;--g4-hi:.18;--g4-sh:0 1px 2px rgba(0,0,0,.15),0 3px 10px rgba(0,0,0,.05);--g4-ring:rgb(var(--g4-f))}' +
    '.g4-secondary{--g4-bg:rgba(255,255,255,var(--g4-a,.42));--g4-sn:.5;--g4-hi:.75;--g4-sh:0 1px 2px rgba(0,0,0,.05),0 3px 12px rgba(0,0,0,.04),inset 0 0 0 .5px rgba(0,0,0,.12);--g4-ring:#1D1D1F}' +
    '.g4-dark{--g4-bg:rgba(var(--g4-f),var(--g4-a,.3));--g4-sn:.12;--g4-hi:.14;--g4-sh:0 1px 2px rgba(0,0,0,.35),inset 0 0 0 .5px rgba(255,255,255,.14);--g4-ring:#F5F5F7}' +
    '@media (prefers-reduced-motion:reduce){.g4,.g4:hover,.g4:active{transition:none;transform:none}}';
  var styled = false;

  function glassV4(btn, o) {
    if (btn._g4) return btn._g4;
    o = o || {};
    if (!styled) { var st = D.createElement('style'); st.textContent = CSSTXT; D.head.appendChild(st); styled = true; }
    var B = setupButton(btn, o), cv = B.cv, ctx = B.ctx, prim = B.prim, dark = B.dark;
    var w = 0, h = 0, r = 10, dpr = 1, sized = '', rim = [], tgt = null, cur = null, alpha = null, band = null, img = null, ok = false;
    var api = { el: btn, variant: B.variant }, lab = null;

    api.scan = function () {
      var R = btn.getBoundingClientRect(); ok = !!(R.width && R.height); if (!ok) return;
      w = Math.round(R.width); h = Math.round(R.height);
      r = Math.min(parseFloat(getComputedStyle(btn).borderTopLeftRadius) || 0, h / 2);
      var bh = behind(btn, R, B.fg), surface = surfaceOf(B, bh.base, .42, .3);
      var S = sampleAround(btn, R, r, toLab(surface));
      var n = Math.max(24, Math.round((2 * w + 2 * h) / 3)), pts = rrPts(.5, .5, w - 1, h - 1, r - .5, n);
      var gain = 2.4 * B.str * intensity() * (B.colour ? 1.6 : 1), Lr = lightRim(pts, S, 22), a = rimAlpha(Lr, gain, .6, .11), Lt = prim || dark ? .82 : .72;
      var t = new Float32Array(n * 4 + 7), i;
      for (i = 0; i < n; i++) { var c = reflectOn(B, Lr.A[i], Lr.B[i], Lt, .14); t[i * 4] = c[0]; t[i * 4 + 1] = c[1]; t[i * 4 + 2] = c[2]; t[i * 4 + 3] = a[i]; }
      // body tint (original drawCombined): overall colour, its centre pulled toward the brightest rim point
      var bc = reflectOn(B, Lr.ambA, Lr.ambB, Lt, .12), pk = pts[Lr.peakAt] || { nx: 0, ny: 0 }, mean = 0;
      for (i = 0; i < n; i++) mean += Lr.I[i] / n;
      t[n * 4] = bc[0]; t[n * 4 + 1] = bc[1]; t[n * 4 + 2] = bc[2]; t[n * 4 + 3] = knee(mean * gain, .7);
      t[n * 4 + 4] = pk.nx; t[n * 4 + 5] = pk.ny; t[n * 4 + 6] = 0;
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
        applyRefract(api, B, btn, w, h, r, { snell: true, bez: Math.min(12, h / 2 - 1), scale: (dark ? 13 : 16) * Math.min(B.str, 2.5), split: .07, post: 'blur(.35px) saturate(1.35)', fallback: 'blur(12px) saturate(1.4)' });
      }
      if (alpha != null) btn.style.setProperty('--g4-a', alpha.toFixed(2));
      applyMode(btn, lab);
      if (!cur) cur = tgt.slice();
      anim.kick();
    };

    function g(d, c) { var x = d - c; return Math.exp(-x * x / .28); }
    function draw(s) {
      ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.clearRect(0, 0, cv.width, cv.height);
      if (!cur || !band) return;
      var D2 = img.data, n = rim.length, i, lift = s.k * Math.min(B.str, 2), sig = 2 * 22 * 22, spec = new Float32Array(n);
      D2.fill(0);
      if (lift > .001) { // pointer caustic: a highlight under the pointer and a fainter focus mirrored across the button
        var mx = w - s.sx, my = h - s.sy;
        for (i = 0; i < n; i++) {
          var dx = rim[i].x - s.sx, dy = rim[i].y - s.sy, ex = rim[i].x - mx, ey = rim[i].y - my;
          spec[i] = (Math.exp(-(dx * dx + dy * dy) / sig) + .45 * Math.exp(-(ex * ex + ey * ey) / sig)) * lift * (prim ? .45 : .8);
        }
      }
      for (var j = 0; j < band.ix.length; j++) {
        var d = band.d[j], ri = band.ri[j], q = ri * 4, cov = clamp(d * dpr + .5, 0, 1), L = cur[q + 3];
        // caustic split: each channel has its own hairline depth, red outermost, blue innermost
        var hr = g(d, .35), hg = g(d, .75), hb = g(d, 1.15), wash = Math.exp(-d / (prim ? 4.5 : 3)), hm = (hr + hg + hb) / 3;
        var a1 = Math.min(1, L * (hm * (prim ? .85 : 1) + wash * (prim ? .4 : .32))) * cov;
        var a2 = Math.min(1, spec[ri] * (hg + wash * .25)) * cov, A = a1 + a2 - a1 * a2; if (A < .003) continue;
        var k = (hm + wash * .2) || 1, cr = cur[q] * (hr + wash * .2) / k, cg = cur[q + 1] * (hg + wash * .2) / k, cb = cur[q + 2] * (hb + wash * .2) / k, p = band.ix[j];
        D2[p] = Math.min(255, (cr * a1 * (1 - a2) + 255 * a2) / A); D2[p + 1] = Math.min(255, (cg * a1 * (1 - a2) + 255 * a2) / A); D2[p + 2] = Math.min(255, (cb * a1 * (1 - a2) + 255 * a2) / A); D2[p + 3] = A * 255;
      }
      ctx.putImageData(img, 0, 0);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0); ctx.save(); rrPath(ctx, 0, 0, w, h, r); ctx.clip();
      var o = n * 4, bodyS = cur[o + 3];
      if (bodyS > .004) { // original body tint, at the original str 0.25
        var cx = w / 2 + cur[o + 4] * w * .14, cy = h / 2 + cur[o + 5] * h * .14, body = [cur[o], cur[o + 1], cur[o + 2]];
        var rg = ctx.createRadialGradient(cx, cy, 0, cx, cy, Math.max(w, h) * .75);
        rg.addColorStop(0, rgba(body, .25 * .22 * bodyS)); rg.addColorStop(.5, rgba(body, .25 * .1 * bodyS)); rg.addColorStop(1, rgba(body, .25 * .03 * bodyS));
        ctx.fillStyle = rg; ctx.fillRect(0, 0, w, h);
      }
      if (lift > .001) {
        var pg = ctx.createRadialGradient(s.sx, s.sy, 0, s.sx, s.sy, Math.max(w, h) * .55);
        pg.addColorStop(0, rgba(WHITE, lift * (prim ? .07 : dark ? .08 : .24))); pg.addColorStop(1, rgba(WHITE, 0));
        ctx.fillStyle = pg; ctx.fillRect(0, 0, w, h);
      }
      ctx.restore();
    }
    var anim = animator(btn, draw, function (f) { return cur && tgt && cur.length === tgt.length ? easeArr(cur, tgt, f) : false; });
    api.update = function () { refresh(true); };
    btn._g4 = api; register(api); refresh();
    return api;
  }
  boot(glassV4, 'GlassV4');
