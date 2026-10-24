  /* ===== V1: Original, tuned =====
     The drawing is glassEngine.js: drawCombined (body tint, edge glow, thickness bevel, rim shadow) plus
     drawCaustic's RGB-split edge line, at the original str = 0.25. What changed is what feeds it:
     sources are no longer [data-color] elements scored by distance alone, but eight directional bins of
     real page samples, scored by distance, coverage, chroma and contrast, with ambient light removed. */
  var CSSTXT = ':where(.g1){position:relative}.g1{display:inline-flex;align-items:center;justify-content:center;gap:6px;font:inherit;font-size:14px;font-weight:500;letter-spacing:.01em;line-height:1.2;padding:9px 16px;border-radius:8px;cursor:pointer;white-space:nowrap;overflow:hidden;isolation:isolate;color:var(--g1-fg);border:1px solid var(--g1-bd,rgba(0,0,0,.08));background:var(--g1-bg);box-shadow:var(--g1-sh);backdrop-filter:blur(15px) saturate(140%);-webkit-backdrop-filter:blur(15px) saturate(140%);transition:transform .15s,box-shadow .15s}' +
    '.g1:hover:not(:disabled){transform:translateY(-.5px)}' +
    '.g1:focus-visible{outline:2px solid var(--g1-ring,#1D1D1F);outline-offset:2px}.g1:disabled{opacity:.5;cursor:not-allowed}' +
    '.g1>canvas{position:absolute;inset:0;width:100%;height:100%;z-index:1;pointer-events:none;border-radius:inherit}.g1>span{position:relative;z-index:5;display:inline-flex;align-items:center;gap:6px}' +
    '.g1::after{content:"";position:absolute;inset:0;z-index:4;border-radius:inherit;pointer-events:none;background:linear-gradient(170deg,rgba(255,255,255,var(--g1-sn,.5)) 0%,rgba(255,255,255,calc(var(--g1-sn,.5)*.12)) 28%,transparent 55%);box-shadow:inset 0 1px 0 rgba(255,255,255,var(--g1-hi,.65)),inset 0 -1px 0 rgba(255,255,255,.08),inset 1px 0 0 rgba(255,255,255,.1),inset -1px 0 0 rgba(255,255,255,.1)}' +
    '.g1-primary{--g1-bg:rgb(var(--g1-f));--g1-bd:rgba(255,255,255,.1);--g1-sn:.16;--g1-hi:.2;--g1-ring:rgb(var(--g1-f))}' +
    '.g1-secondary{--g1-bg:rgba(255,255,255,var(--g1-a,.55))}' +
    '.g1-dark{--g1-bg:rgba(var(--g1-f),var(--g1-a,.35));--g1-bd:rgba(255,255,255,.12);--g1-sn:.12;--g1-hi:.14;--g1-ring:#F5F5F7}' +
    '@media (prefers-reduced-motion:reduce){.g1,.g1:hover{transition:none;transform:none}}';
  var styled = false, DIRS = [];
  for (var di = 0; di < 8; di++) DIRS.push([Math.cos(di * Math.PI / 4), Math.sin(di * Math.PI / 4)]);

  function glassV1(btn, o) {
    if (btn._g1) return btn._g1;
    o = o || {};
    if (!styled) { var st = D.createElement('style'); st.textContent = CSSTXT; D.head.appendChild(st); styled = true; }
    var B = setupButton(btn, o), cv = B.cv, ctx = B.ctx, prim = B.prim, dark = B.dark;
    var w = 0, h = 0, r = 8, dpr = 1, sized = '', tgt = new Float32Array(36), cur = null, alpha = null, shadow = '', ok = false;
    var api = { el: btn, variant: B.variant }, lab = null;

    api.scan = function () {
      var R = btn.getBoundingClientRect(); ok = !!(R.width && R.height); if (!ok) return;
      w = Math.round(R.width); h = Math.round(R.height);
      r = Math.min(parseFloat(getComputedStyle(btn).borderTopLeftRadius) || 0, h / 2);
      var bh = behind(btn, R, B.fg), surface = surfaceOf(B, bh.base, .55, .35);
      var S = sampleAround(btn, R, r, toLab(surface));
      var F = new Float32Array(8), FS = new Float32Array(8), A = new Float32Array(8), Bb = new Float32Array(8), k, i;
      S.samples.forEach(function (s) {
        var ex = (s.x - w / 2) / (w / 2 + s.off), ey = (s.y - h / 2) / (h / 2 + s.off);
        var b = ((Math.round(Math.atan2(ey, ex) / (Math.PI / 4)) % 8) + 8) % 8, q = s.off / 24, f = 1 / (1 + q * q);
        F[b] += f; if (s.s > 0) { var fs = f * s.s; FS[b] += fs; A[b] += s.lab[1] * fs; Bb[b] += s.lab[2] * fs; }
      });
      var cov = [], amb = 1, ta = 0, tb = 0, tw = 0, gain = 2.4 * B.str * intensity() * (B.colour ? 1.6 : 1), sum = 0;
      for (k = 0; k < 8; k++) { cov[k] = F[k] ? FS[k] / F[k] : 0; amb = Math.min(amb, cov[k]); ta += A[k]; tb += Bb[k]; tw += FS[k]; }
      var Lt = prim || dark ? .8 : .72, body = tw ? reflectOn(B, ta / tw, tb / tw, Lt, .12) : WHITE;
      for (k = 0; k < 8; k++) {
        var s = knee(Math.max(0, cov[k] - .9 * amb) * gain, 1), c = FS[k] > 1e-6 ? reflectOn(B, A[k] / FS[k], Bb[k] / FS[k], Lt, .13) : body;
        tgt[k * 4] = c[0]; tgt[k * 4 + 1] = c[1]; tgt[k * 4 + 2] = c[2]; tgt[k * 4 + 3] = s; sum += s;
      }
      if (sum > 1.6) for (k = 0; k < 8; k++) tgt[k * 4 + 3] *= 1.6 / sum; // budget: at most ~two sides fully lit
      var mean = 0; for (k = 0; k < 8; k++) mean += cov[k] / 8;
      tgt[32] = body[0]; tgt[33] = body[1]; tgt[34] = body[2]; tgt[35] = knee(mean * gain, .8);
      lab = liquidLabel(B, bh.worst); if (!prim) alpha = glassAlpha(B.fg, bh.worst, dark, B.fill, dark ? .35 : .55); else if (B.tint) alpha = glassAlpha(B.fg, bh.worst, true, B.fill, B.fa, B.dim);
      for (i = 0; i < 36; i++) if (isNaN(tgt[i])) tgt[i] = 0;
    };
    api.write = function () {
      if (!ok) return;
      var key = w + 'x' + h + (liquid() ? 'L' : 'S') + (btn._busy ? 'b' : '');
      if (key !== sized) {
        sized = key; dpr = Math.min(W.devicePixelRatio || 1, 2); cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr); cur = null;
        // V1 has no refraction of its own (the original never had it); Liquid mode borrows the shared one
        applyRefract(api, B, btn, w, h, r, null);
      }
      if (alpha != null) btn.style.setProperty('--g1-a', alpha.toFixed(2));
      applyMode(btn, lab);
      if (!cur) cur = tgt.slice();
      anim.kick();
    };

    function edgeBand(ctx, e, d, col, a) { // glassEngine edge glow / bevel: gradient band entering from edge e
      var v = e === 't' || e === 'b', far = e === 'b' ? h : e === 'r' ? w : 0, sg = far ? -1 : 1;
      var g = v ? ctx.createLinearGradient(0, far, 0, far + sg * d) : ctx.createLinearGradient(far, 0, far + sg * d, 0);
      g.addColorStop(0, rgba(col, a)); g.addColorStop(1, rgba(col, 0)); ctx.fillStyle = g;
      if (v) ctx.fillRect(0, far ? h - d : 0, w, d); else ctx.fillRect(far ? w - d : 0, 0, d, h);
    }
    function caustic(ctx, e, centre, col, a) { // glassEngine drawCaustic: R / colour / B split line, faded at both ends
      if (a < .006) return;
      var v = e === 't' || e === 'b', L = v ? w : h, base = e === 't' || e === 'l' ? .5 : (v ? h : w) - .5, inw = e === 't' || e === 'l' ? 1 : -1;
      var a1 = Math.max(1, centre - L * .35), a2 = Math.min(L - 1, centre + L * .35);
      var cols = [[Math.min(255, col[0] + 50), Math.max(0, col[1] - 40), Math.max(0, col[2] - 40)], col, [Math.max(0, col[0] - 40), Math.max(0, col[1] - 40), Math.min(255, col[2] + 50)], WHITE];
      var ks = [.5, .7, .5, .35], off = [-1.5, 0, 1.5, 0], lw = [.7, 1.4, .7, .35];
      ctx.lineCap = 'round';
      for (var i = 0; i < 4; i++) {
        var p = base + inw * Math.max(0, off[i] + 1.5) * .6, A = a * ks[i];
        var g = v ? ctx.createLinearGradient(a1, p, a2, p) : ctx.createLinearGradient(p, a1, p, a2);
        g.addColorStop(0, rgba(cols[i], 0)); g.addColorStop(.18, rgba(cols[i], A)); g.addColorStop(.82, rgba(cols[i], A)); g.addColorStop(1, rgba(cols[i], 0));
        ctx.strokeStyle = g; ctx.lineWidth = lw[i]; ctx.beginPath();
        if (v) { ctx.moveTo(a1, p); ctx.lineTo(a2, p); } else { ctx.moveTo(p, a1); ctx.lineTo(p, a2); }
        ctx.stroke();
      }
    }
    function draw(s) {
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0); ctx.clearRect(0, 0, w, h);
      if (!cur || !w) return;
      var str = .25, src = [], k;
      for (k = 0; k < 8; k++) if (cur[k * 4 + 3] > .01) src.push({ c: [cur[k * 4], cur[k * 4 + 1], cur[k * 4 + 2]], dx: DIRS[k][0], dy: DIRS[k][1], s: cur[k * 4 + 3] });
      src.sort(function (a, b) { return b.s - a.s; });
      var bodyS = cur[35], body = [cur[32], cur[33], cur[34]];
      if (bodyS > .004) { // body tint, centre pulled toward the strongest source
        var s0 = src[0], cx = w / 2 + (s0 ? s0.dx * w * .12 : 0), cy = h / 2 + (s0 ? s0.dy * h * .12 : 0);
        var rg = ctx.createRadialGradient(cx, cy, 0, cx, cy, Math.max(w, h) * .75);
        rg.addColorStop(0, rgba(body, str * .22 * bodyS)); rg.addColorStop(.5, rgba(body, str * .1 * bodyS)); rg.addColorStop(1, rgba(body, str * .03 * bodyS));
        ctx.fillStyle = rg; ctx.fillRect(0, 0, w, h);
      }
      function edges(sc, fn) { // a diagonal bin lights both of its edges, weighted by direction
        if (Math.abs(sc.dx) > .3) fn(sc.dx > 0 ? 'r' : 'l', Math.abs(sc.dx));
        if (Math.abs(sc.dy) > .3) fn(sc.dy > 0 ? 'b' : 't', Math.abs(sc.dy));
      }
      ctx.globalCompositeOperation = 'lighter';
      src.slice(0, 3).forEach(function (sc) { edges(sc, function (e, wt) { edgeBand(ctx, e, Math.max(3, 8 * sc.s), sc.c, sc.s * wt * str * .3); }); });
      ctx.globalCompositeOperation = 'source-over';
      src.slice(0, 2).forEach(function (sc) { edges(sc, function (e, wt) { edgeBand(ctx, e, 5, sc.c, sc.s * wt * str * .18); }); });
      if (dark || prim) ctx.globalCompositeOperation = 'lighter';
      src.slice(0, 2).forEach(function (sc, i) {
        edges(sc, function (e, wt) { var v = e === 't' || e === 'b', L = v ? w : h; caustic(ctx, e, L / 2 + (v ? sc.dx : sc.dy) * L * .3, sc.c, sc.s * wt * str * (i ? .25 : .65)); });
      });
      ctx.globalCompositeOperation = 'source-over';
      if (s.k > .001) { // hover: a soft pool of light under the pointer
        var pg = ctx.createRadialGradient(s.sx, s.sy, 0, s.sx, s.sy, Math.max(w, h) * .55);
        pg.addColorStop(0, rgba(WHITE, s.k * (prim || dark ? .08 : .22))); pg.addColorStop(1, rgba(WHITE, 0));
        ctx.fillStyle = pg; ctx.fillRect(0, 0, w, h);
      }
      // rim shadow (glassEngine), only for a strong source and kept very faint
      var sh = [];
      src.slice(0, 2).forEach(function (sc) { var a = sc.s * str * .18; if (a > .02) sh.push(Math.round(sc.dx * 2) + 'px ' + Math.round(sc.dy * 1.5) + 'px ' + Math.round(3 + sc.s * 5) + 'px ' + rgba(sc.c, a)); });
      var base = prim ? '0 1px 2px rgba(0,0,0,.14)' : dark ? '0 1px 2px rgba(0,0,0,.35)' : '0 1px 3px rgba(0,0,0,.05)';
      var full = sh.length ? base + ',' + sh.join(',') : base;
      if (full !== shadow) { shadow = full; btn.style.setProperty('--g1-sh', full); }
    }
    var anim = animator(btn, draw, function (f) { return cur ? easeArr(cur, tgt, f) : false; });
    api.update = function () { refresh(true); };
    btn._g1 = api; register(api); refresh();
    return api;
  }
  boot(glassV1, 'GlassV1');
