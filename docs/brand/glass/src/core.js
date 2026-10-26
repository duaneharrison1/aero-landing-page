  /* ===== shared core (copied into every variant by build.mjs) ===== */
  var RM = W.matchMedia ? W.matchMedia('(prefers-reduced-motion: reduce)') : { matches: false };
  var UA = navigator.userAgent;
  // SVG filters inside backdrop-filter only render in Chromium. Safari reports support and draws nothing,
  // Firefox accepts the syntax and draws nothing, so a UA check is needed on top of CSS.supports.
  var REFRACT = !!(W.CSS && CSS.supports && CSS.supports('backdrop-filter', 'url(#a)')) && /Chrome\/\d/.test(UA) && !/Firefox\//.test(UA);
  var WHITE = [255, 255, 255], INK = [29, 29, 31];
  var probe = D.createElement('canvas').getContext('2d', { willReadFrequently: true });
  var colCache = {}, pxCache = new WeakMap();

  function clamp(x, a, b) { return x < a ? a : x > b ? b : x; }
  function sstep(a, b, x) { x = clamp((x - a) / (b - a), 0, 1); return x * x * (3 - 2 * x); }
  function intensity() { var g = W.GLASS_INTENSITY; return g == null || !isFinite(+g) ? 1 : clamp(+g, 0, 3); }

  /* ---------- colour ---------- */
  function parse(s) {
    if (!s || s === 'none' || s === 'transparent') return null;
    if (colCache[s]) return colCache[s];
    var m = /^rgba?\(([\d.]+)[, ]+([\d.]+)[, ]+([\d.]+)(?:[,/ ]+([\d.]+%?))?\)$/.exec(s), c;
    if (m) c = [+m[1], +m[2], +m[3], m[4] == null ? 1 : parseFloat(m[4]) / (/%/.test(m[4]) ? 100 : 1)];
    else {
      probe.clearRect(0, 0, 1, 1); probe.fillStyle = '#000'; probe.fillStyle = s; probe.fillRect(0, 0, 1, 1);
      var d = probe.getImageData(0, 0, 1, 1).data; c = d[3] ? [d[0] * 255 / d[3], d[1] * 255 / d[3], d[2] * 255 / d[3], d[3] / 255] : null;
    }
    return (colCache[s] = c);
  }
  function hex(h) { h = String(h || '').trim().replace('#', ''); if (h.length === 3) h = h.replace(/./g, '$&$&'); var n = parseInt(h, 16); return h.length === 6 && !isNaN(n) ? [n >> 16 & 255, n >> 8 & 255, n & 255] : null; }
  function toHex(c) { return '#' + c.map(function (v) { return ('0' + Math.round(clamp(v, 0, 255)).toString(16)).slice(-2); }).join(''); }
  function mix(a, b, k) { return [a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k, a[2] + (b[2] - a[2]) * k]; }
  function lin(v) { v /= 255; return v <= .04045 ? v / 12.92 : Math.pow((v + .055) / 1.055, 2.4); }
  function lum(c) { return .2126 * lin(c[0]) + .7152 * lin(c[1]) + .0722 * lin(c[2]); }
  function contrast(a, b) { var x = lum(a) + .05, y = lum(b) + .05; return x > y ? x / y : y / x; }
  function rgba(c, a) { return 'rgba(' + (c[0] | 0) + ',' + (c[1] | 0) + ',' + (c[2] | 0) + ',' + clamp(a, 0, 1).toFixed(3) + ')'; }
  // OKLab: perceptual, so "how colourful" and "how different" mean what they look like
  function toLab(c) {
    var r = lin(c[0]), g = lin(c[1]), b = lin(c[2]);
    var l = Math.cbrt(.4122214708 * r + .5363325363 * g + .0514459929 * b), m = Math.cbrt(.2119034982 * r + .6806995451 * g + .1073969566 * b), s = Math.cbrt(.0883024619 * r + .2817188376 * g + .6299787005 * b);
    return [.2104542553 * l + .793617785 * m - .0040720468 * s, 1.9779984951 * l - 2.428592205 * m + .4505937099 * s, .0259040371 * l + .7827717662 * m - .808675766 * s];
  }
  function fromLab(L) {
    var l = L[0] + .3963377774 * L[1] + .2158037573 * L[2], m = L[0] - .1055613458 * L[1] - .0638541728 * L[2], s = L[0] - .0894841775 * L[1] - 1.291485548 * L[2];
    l = l * l * l; m = m * m * m; s = s * s * s;
    return [4.0767416621 * l - 3.3077115913 * m + .2309699292 * s, -1.2684380046 * l + 2.6097574011 * m - .3413193965 * s, -.0041960863 * l - .7034186147 * m + 1.707614701 * s]
      .map(function (v) { v = clamp(v, 0, 1); return 255 * (v <= .0031308 ? 12.92 * v : 1.055 * Math.pow(v, 1 / 2.4) - .055); });
  }
  /* How much a colour seen near the button should register on it.
     - colourfulness: OKLCH chroma. Grey, white and black are ~0, so they never tint the glass.
     - contrast with the button: distance in the colour (a,b) plane from the button's own surface,
       so a yellow note does not tint a yellow button, plus a small boost when lightness differs.
     A black button next to a white one therefore scores 0: the old engine scored it ~0.9. */
  function salience(lab, surf) {
    var C = Math.sqrt(lab[1] * lab[1] + lab[2] * lab[2]), wc = sstep(.035, .16, C);
    if (!wc) return 0;
    var dab = Math.sqrt((lab[1] - surf[1]) * (lab[1] - surf[1]) + (lab[2] - surf[2]) * (lab[2] - surf[2]));
    return wc * sstep(.02, .13, dab) * (.65 + .35 * sstep(0, .35, Math.abs(lab[0] - surf[0])));
  }
  // The colour glass shows for a reflection: the source's hue, its lightness pulled to suit the glass, chroma capped
  function reflectColour(a, b, L, Cmax) { var C = Math.sqrt(a * a + b * b), k = C > Cmax ? Cmax / C : 1; return fromLab([L, a * k, b * k]); }
  // Soft knee: linear for small values, never above cap
  function knee(x, cap) { return cap * (1 - Math.exp(-x / cap)); }

  /* ---------- reading the page (read-only) ---------- */
  function pixel(el, x, y) {
    var key = el.tagName === 'IMG' ? el.currentSrc || el.src : 'c', now = Date.now(), e = pxCache.get(el);
    if (!e || e.key !== key || (key === 'c' && now - e.t > 500)) {
      e = { key: key, t: now, d: null };
      if (el.tagName !== 'IMG' || (el.complete && el.naturalWidth)) {
        try { var c = D.createElement('canvas'); c.width = c.height = 24; var x2 = c.getContext('2d', { willReadFrequently: true }); x2.drawImage(el, 0, 0, 24, 24); e.d = x2.getImageData(0, 0, 24, 24).data; }
        catch (err) { e.d = null; } // tainted: fall back to the element's own colour
      }
      pxCache.set(el, e);
    }
    if (!e.d) return null;
    var r = el.getBoundingClientRect(), u = clamp(((x - r.left) / r.width * 24) | 0, 0, 23), v = clamp(((y - r.top) / r.height * 24) | 0, 0, 23), i = (v * 24 + u) * 4;
    return e.d[i + 3] > 128 ? [e.d[i], e.d[i + 1], e.d[i + 2]] : null;
  }
  function gradAvg(s) {
    var m = s.match(/(rgba?\([^)]*\)|#[0-9a-f]{3,8}\b|(?:oklch|oklab|hsla?|color)\([^)]*\))/gi); if (!m) return null;
    var t = [0, 0, 0], n = 0; m.forEach(function (x) { var c = parse(x); if (c && c[3] > .05) { t[0] += c[0]; t[1] += c[1]; t[2] += c[2]; n++; } });
    return n ? [t[0] / n, t[1] / n, t[2] / n] : null;
  }
  function glassOf(el) { return el && el.closest ? el.closest('[data-glass-kind]') : null; }
  function colorOf(el, x, y, memo) {
    if (!el) return null;
    if (memo.has(el)) return memo.get(el);
    var c = null, own = true, cs = getComputedStyle(el), tag = el.tagName, g = glassOf(el);
    var dc = el.getAttribute && hex(el.getAttribute('data-color'));
    if (dc) c = dc;
    else if (g && g.getAttribute('data-glass-kind') === 'solid') c = hex(g.getAttribute('data-glass-fill'));
    else if (tag === 'IMG' || tag === 'CANVAS' || tag === 'VIDEO') { c = pixel(el, x, y); own = false; }
    else if (W.SVGGraphicsElement && el instanceof SVGGraphicsElement && tag.toLowerCase() !== 'svg') { var f = parse(cs.fill); if (f && f[3] > .1) c = mix(colorOf(el.parentNode, x, y, memo) || WHITE, f, f[3] * (+cs.opacity || 1)); own = false; }
    if (!c) {
      var bi = cs.backgroundImage, bg = parse(cs.backgroundColor), ga = bi && bi !== 'none' && gradAvg(bi);
      if (ga) c = bg && bg[3] > .5 ? mix(bg, ga, .7) : ga;
      else if (bg && bg[3] > .03) c = bg[3] > .97 ? bg.slice(0, 3) : mix(colorOf(el.parentElement, x, y, memo) || WHITE, bg, bg[3]);
      else if (el === D.documentElement) c = WHITE;
      else { c = colorOf(el.parentElement, x, y, memo) || WHITE; own = false; }
      var fs = parseFloat(cs.fontSize), tc = fs >= 20 && parse(cs.color);
      if (tc && [].some.call(el.childNodes, function (n) { return n.nodeType === 3 && n.data.trim(); })) c = mix(c, tc, Math.min(.6, fs / 60));
    }
    if (own) memo.set(el, c);
    return c;
  }
  function isClear(el) { var g = glassOf(el); return g && g.getAttribute('data-glass-kind') === 'clear'; }
  // does this element paint anything itself? Transparent wrappers (a toolbar row, a flex container) do not,
  // so the hit test looks through them to what is visually underneath instead of walking up the DOM.
  function paints(el) {
    if (el === D.documentElement || el === D.body) return true;
    var tag = el.tagName;
    if (tag === 'IMG' || tag === 'CANVAS' || tag === 'VIDEO' || el.hasAttribute('data-color')) return true;
    var g = glassOf(el); if (g && g.getAttribute('data-glass-kind') === 'solid') return true;
    if (W.SVGGraphicsElement && el instanceof SVGGraphicsElement && tag.toLowerCase() !== 'svg') return true;
    var cs = getComputedStyle(el), bg = parse(cs.backgroundColor);
    if ((bg && bg[3] > .03) || (cs.backgroundImage && cs.backgroundImage !== 'none')) return true;
    return parseFloat(cs.fontSize) >= 20 && [].some.call(el.childNodes, function (n) { return n.nodeType === 3 && n.data.trim(); });
  }
  function hitAt(x, y, self) {
    var st = D.elementsFromPoint(x, y);
    for (var i = 0; i < st.length; i++) { var e = st[i]; if (self.contains(e) || isClear(e)) continue; if (paints(e)) return e; }
    return null;
  }
  function colorAt(x, y, self, memo) {
    if (x < 0 || y < 0 || x >= W.innerWidth || y >= W.innerHeight) return null;
    return colorOf(hitAt(x, y, self), x, y, memo) || WHITE;
  }
  // large text right behind the label: glyph edges stay sharp through clear glass, so it gets more frost
  function textBehind(el) {
    if (!el || el.tagName === 'IMG' || el.tagName === 'CANVAS' || (W.SVGElement && el instanceof SVGElement)) return false;
    var cs = getComputedStyle(el), bg = parse(cs.backgroundColor);
    return !(bg && bg[3] > .03) && parseFloat(cs.fontSize) >= 20;
  }

  /* ---------- rounded-rect geometry ---------- */
  function rrPts(x, y, w, h, r, n) {
    r = Math.max(0, Math.min(r, w / 2, h / 2));
    var a = w - 2 * r, b = h - 2 * r, q = Math.PI * r / 2, L = 2 * a + 2 * b + 4 * q, out = [], H = Math.PI / 2;
    function arc(cx, cy, t) { out.push({ x: cx + r * Math.cos(t), y: cy + r * Math.sin(t), nx: Math.cos(t), ny: Math.sin(t) }); }
    for (var i = 0; i < n; i++) {
      var s = i * L / n;
      if (s < a) out.push({ x: x + r + s, y: y, nx: 0, ny: -1 });
      else if ((s -= a) < q) arc(x + w - r, y + r, -H + s / Math.max(r, 1e-6));
      else if ((s -= q) < b) out.push({ x: x + w, y: y + r + s, nx: 1, ny: 0 });
      else if ((s -= b) < q) arc(x + w - r, y + h - r, s / Math.max(r, 1e-6));
      else if ((s -= q) < a) out.push({ x: x + w - r - s, y: y + h, nx: 0, ny: 1 });
      else if ((s -= a) < q) arc(x + r, y + h - r, H + s / Math.max(r, 1e-6));
      else if ((s -= q) < b) out.push({ x: x, y: y + h - r - s, nx: -1, ny: 0 });
      else { s -= b; arc(x + r, y + r, Math.PI + s / Math.max(r, 1e-6)); }
    }
    return out;
  }
  function rrPath(ctx, x, y, w, h, r) {
    r = Math.max(0, Math.min(r, w / 2, h / 2)); ctx.beginPath(); ctx.moveTo(x + r, y);
    ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r); ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath();
  }
  // signed geometry of a point inside a rounded rect: depth from the edge and the outward normal
  function rrDepth(x, y, w, h, r) {
    var px = x - w / 2, py = y - h / 2, sx = px < 0 ? -1 : 1, sy = py < 0 ? -1 : 1, qx = Math.abs(px) - (w / 2 - r), qy = Math.abs(py) - (h / 2 - r);
    if (qx > 0 && qy > 0) { var l = Math.sqrt(qx * qx + qy * qy) || 1; return [r - l, sx * qx / l, sy * qy / l]; }
    return qx > qy ? [r - qx, sx, 0] : [r - qy, 0, sy];
  }

  /* ---------- sampling the surroundings ---------- */
  // Rings of hit-test points hugging the button shape. Each sample keeps its OKLab colour and salience.
  var RINGS = [4, 12, 24, 42, 68, 104, 150, 210];
  function sampleAround(btn, R, r, surf) {
    var w = R.width, h = R.height, reach = Math.min(Math.max(2.2 * w, 170), 340) - w / 2, memo = new Map(), out = [];
    RINGS.forEach(function (off) {
      if (off > reach) return;
      var W2 = w + 2 * off, H2 = h + 2 * off, n = clamp(Math.round((2 * W2 + 2 * H2) / (16 + off * .5)), 12, 30);
      rrPts(R.left - off, R.top - off, W2, H2, r + off, n).forEach(function (p) {
        var c = colorAt(p.x, p.y, btn, memo); if (!c) return;
        var lab = toLab(c);
        out.push({ x: p.x - R.left, y: p.y - R.top, off: off, lab: lab, s: salience(lab, surf) });
      });
    });
    return { samples: out, reach: reach };
  }
  /* Light arriving at each rim point.
     weight f = facing^1.3 / (1 + (d/d0)^2), faded to 0 at the reach. Every sample adds f to the total,
     coloured ones add f*salience to the colour, so intensity = salient share of what the rim point "sees".
     That one ratio gives all three behaviours: distance (near samples dominate), coverage (a small chip
     among white page is a small share) and colourfulness (neutrals add weight but no colour). */
  function lightRim(pts, S, d0) {
    var n = pts.length, I = new Float32Array(n), A = new Float32Array(n), B = new Float32Array(n), Ls = new Float32Array(n), sm = S.samples, far = S.reach + 30, i, j;
    for (i = 0; i < n; i++) {
      var p = pts[i], F = 0, FS = 0, a = 0, b = 0, l = 0;
      for (j = 0; j < sm.length; j++) {
        var s = sm[j], vx = s.x - p.x, vy = s.y - p.y, d = Math.sqrt(vx * vx + vy * vy) || 1, cos = (vx * p.nx + vy * p.ny) / d;
        if (cos <= 0) continue;
        var q = d / d0, f = Math.pow(cos, 1.3) / (1 + q * q) * (1 - Math.pow(Math.min(1, d / far), 3));
        F += f;
        if (s.s > 0) { var fs = f * s.s; FS += fs; a += s.lab[1] * fs; b += s.lab[2] * fs; l += s.lab[0] * fs; }
      }
      I[i] = F > 1e-6 ? FS / F : 0;
      if (FS > 1e-6) { A[i] = a / FS; B[i] = b / FS; Ls[i] = l / FS; }
    }
    // soften along the rim (colour and intensity), weighting colour by intensity so dark gaps do not grey it
    function smooth(arr, wt) {
      var o = new Float32Array(n), K = [1, 2, 3, 2, 1];
      for (var i = 0; i < n; i++) { var t = 0, tw = 0; for (var k = -2; k <= 2; k++) { var m = (i + k + n) % n, ww = K[k + 2] * (wt ? wt[m] + 1e-4 : 1); t += arr[m] * ww; tw += ww; } o[i] = t / tw; }
      return o;
    }
    A = smooth(A, I); B = smooth(B, I); Ls = smooth(Ls, I); I = smooth(I);
    // ambient = what surrounds the button on all sides (it sits on a colour card). It is taken out of the
    // rim so uniform surroundings never draw an outline; variants may show it as a faint body tint instead.
    var sorted = Array.prototype.slice.call(I).sort(function (x, y) { return x - y; }), amb = sorted[Math.floor(n * .2)] || 0;
    var ta = 0, tb = 0, tw = 0, peak = 0, pk = 0;
    for (i = 0; i < n; i++) { ta += A[i] * I[i]; tb += B[i] * I[i]; tw += I[i]; if (I[i] > peak) { peak = I[i]; pk = i; } }
    return { I: I, A: A, B: B, L: Ls, amb: amb, ambA: tw ? ta / tw : 0, ambB: tw ? tb / tw : 0, peak: peak, peakAt: pk };
  }
  /* Turn rim light into drawable alpha with the clamps:
     - directional part only (ambient removed)
     - soft knee to `cap`
     - total budget: if the lit share of the rim gets large, everything is scaled down, so the rim can
       never become a full coloured outline. */
  function rimAlpha(Lr, gain, cap, budget) {
    var n = Lr.I.length, out = new Float32Array(n), sum = 0, i;
    for (i = 0; i < n; i++) { out[i] = knee(Math.max(0, Lr.I[i] - .9 * Lr.amb) * gain, cap); sum += out[i]; }
    var mean = sum / n;
    if (mean > budget) for (i = 0; i < n; i++) out[i] *= budget / mean;
    return out;
  }

  /* ---------- per-pixel edge band ---------- */
  function buildBand(w, h, r, dpr, rim, depth) {
    var CW = Math.round(w * dpr), CH = Math.round(h * dpr), ix = [], ri = [], dd = [], nx = [], ny = [], n = rim.length;
    for (var Y = 0; Y < CH; Y++) for (var X = 0; X < CW; X++) {
      var x = (X + .5) / dpr, y = (Y + .5) / dpr, g = rrDepth(x, y, w, h, r);
      if (g[0] > depth || g[0] * dpr < -.5) continue;
      var best = 0, bd = 1e9;
      for (var i = 0; i < n; i++) { var dx = rim[i].x - x, dy = rim[i].y - y, d = dx * dx + dy * dy; if (d < bd) { bd = d; best = i; } }
      ix.push((Y * CW + X) * 4); ri.push(best); dd.push(g[0]); nx.push(g[1]); ny.push(g[2]);
    }
    return { ix: ix, ri: ri, d: dd, nx: nx, ny: ny, CW: CW, CH: CH };
  }

  /* ---------- refraction maps ---------- */
  var mapCache = {}, defs = null, uid = 0;
  // profile(d) -> 0..1 displacement magnitude at depth d px from the edge; encoded R/G = 128 +- 127, pointing inward
  // mag > 0 adds a lens term: every pixel samples a little toward the centre, so the middle magnifies
  function dispMap(w, h, r, key, profile, mag) {
    mag = mag || 0;
    var k = w + 'x' + h + 'r' + r + key + 'm' + mag; if (mapCache[k]) return mapCache[k];
    var c = D.createElement('canvas'); c.width = w; c.height = h;
    var x2 = c.getContext('2d'), im = x2.createImageData(w, h), d = im.data;
    for (var y = 0; y < h; y++) for (var x = 0; x < w; x++) {
      var g = rrDepth(x + .5, y + .5, w, h, r), m = profile(Math.max(0, g[0])), i = (y * w + x) * 4;
      var ux = (x + .5 - w / 2) / (w / 2), uy = (y + .5 - h / 2) / (h / 2);
      d[i] = clamp(128 - (g[1] * m + ux * mag) * 127, 0, 255); d[i + 1] = clamp(128 - (g[2] * m + uy * mag) * 127, 0, 255); d[i + 2] = 128; d[i + 3] = 255;
    }
    x2.putImageData(im, 0, 0);
    return (mapCache[k] = c.toDataURL());
  }
  function svgFilter(api, w, h, inner) {
    if (!defs) {
      var svg = D.createElementNS('http://www.w3.org/2000/svg', 'svg');
      svg.setAttribute('aria-hidden', 'true'); svg.style.cssText = 'position:absolute;width:0;height:0;overflow:hidden';
      defs = D.createElementNS(svg.namespaceURI, 'defs'); svg.appendChild(defs); D.body.appendChild(svg);
    }
    var f = api.filter;
    if (!f) { f = api.filter = D.createElementNS('http://www.w3.org/2000/svg', 'filter'); f.id = PFX + 'f' + (++uid); defs.appendChild(f); }
    f.setAttribute('x', 0); f.setAttribute('y', 0); f.setAttribute('width', w); f.setAttribute('height', h);
    f.setAttribute('filterUnits', 'userSpaceOnUse'); f.setAttribute('primitiveUnits', 'userSpaceOnUse'); f.setAttribute('color-interpolation-filters', 'sRGB');
    f.innerHTML = inner;
    return f.id;
  }
  /* Snell profile for a convex squircle lip (after kube.io's write-up): surface height z(t) = (1-(1-t)^4)^(1/4),
     t = depth / bezel. A vertical ray hits a surface tilted by a = atan(z'), bends to b = asin(sin a / n), and
     lands displaced by (glass height) * tan(a - b). Normalised so the edge is 1. */
  function snellProfile(bezel, n) {
    var N = 64, tab = new Float32Array(N + 1), mx = 0;
    for (var i = 0; i <= N; i++) {
      var t = Math.max(.004, i / N), u = 1 - t, base = 1 - u * u * u * u, z = Math.pow(base, .25), dz = Math.pow(base, -.75) * u * u * u;
      var a = Math.atan(dz * .55), b = Math.asin(Math.sin(a) / n), v = (z + .25) * Math.tan(a - b);
      tab[i] = v; if (v > mx) mx = v;
    }
    for (i = 0; i <= N; i++) tab[i] /= mx || 1;
    return function (d) { if (d >= bezel) return 0; var x = d / bezel * N, i0 = x | 0; return tab[i0] + (tab[Math.min(N, i0 + 1)] - tab[i0]) * (x - i0); };
  }

  /* ---------- strength: "subtle" (everyday buttons) or "liquid" (reference-level refraction) ---------- */
  function liquid() { return W.GLASS_MODE === 'liquid'; }
  function powerProfile(bez) { return function (d) { var t = Math.min(1, d / bez); return Math.pow(1 - t, 2.2); }; }
  /* Refraction, built the way liquid-glass-react does it: a warp layer inside the button carries the glass
     colour and a plain backdrop-filter (blur, saturate), and an SVG filter is applied to that layer with
     filter: url(). Putting url() inside backdrop-filter instead makes Chromium render an offset part of
     the box (visible as a hard-edged patch), so it is not used.
     o (subtle settings): { snell, bez, scale, split, post, fallback }. Liquid mode, after liquid-glass-react's
     defaults scaled to button height: a Snell lip ~45% of the height deep, displacement ~1.1x height
     (cap 70, their default), a lens magnification term, a chromatic split of +-10% (their aberration 2),
     a 1.5px frost and saturate 1.6. */
  function refractParts(api, B, w, h, r, o) {
    var L = liquid(), bez, prof, sc, split, mag, post;
    if (L) { bez = Math.max(8, Math.min(h / 2 - 1, h * .45)); prof = snellProfile(bez, 1.5); sc = clamp(h * 1.1, 28, 70); split = .1; mag = .16; post = 'blur(1.5px) saturate(1.6)'; }
    else { bez = o.bez; prof = o.snell ? snellProfile(bez, 1.5) : powerProfile(bez); sc = o.scale; split = o.split || 0; mag = 0; post = o.post; }
    var map = dispMap(w, h, Math.round(r), (L ? 'L' : o.snell ? 's' : 'p') + bez.toFixed(1), prof, mag);
    var inner = '<feImage href="' + map + '" x="0" y="0" width="' + w + '" height="' + h + '" preserveAspectRatio="none" result="m"/>';
    if (split) { // per-channel displacement, recombined by screen as liquid-glass-react does
      var ch = function (k, mtx, res) { return '<feDisplacementMap in="SourceGraphic" in2="m" scale="' + (sc * k).toFixed(1) + '" xChannelSelector="R" yChannelSelector="G" result="d' + res + '"/><feColorMatrix in="d' + res + '" type="matrix" values="' + mtx + '" result="' + res + '"/>'; };
      inner += ch(1 + split, '1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0', 'cr') + ch(1, '0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 1 0', 'cg') + ch(1 - split, '0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 1 0', 'cb') +
        '<feBlend in="cg" in2="cb" mode="screen" result="gb"/><feBlend in="cr" in2="gb" mode="screen"/>';
    } else inner += '<feDisplacementMap in="SourceGraphic" in2="m" scale="' + sc.toFixed(1) + '" xChannelSelector="R" yChannelSelector="G"/>';
    if (api.el._busy) post = post.replace(/blur\(([\d.]+)px\)/, function (m, v) { return 'blur(' + Math.max(+v, 4) + 'px)'; });
    return { filter: 'url(#' + svgFilter(api, w, h, inner) + ')', backdrop: post.trim() + (B.tint ? B.bfx : '') };
  }
  // o: subtle settings, or null for a variant that only refracts in Liquid mode (V1)
  function applyRefract(api, B, btn, w, h, r, o) {
    var glassy = !B.prim || B.tint, use = REFRACT && glassy && (o || liquid()), wp = btn.querySelector(':scope>.' + PFX + '-warp'), bd = btn.querySelector(':scope>.' + PFX + '-body');
    if (!use) {
      btn.classList.remove(PFX + '-warped'); if (wp) wp.remove(); if (bd) bd.remove();
      var fb = glassy ? (liquid() ? 'blur(3px) saturate(1.6)' : o ? o.fallback : '') : '';
      if (fb && B.tint) fb += B.bfx; else if (!fb && B.tint) fb = 'blur(14px)' + B.bfx;
      btn.style.backdropFilter = btn.style.webkitBackdropFilter = fb;
      return;
    }
    if (!wp) {
      bd = D.createElement('span'); bd.className = PFX + '-body'; bd.setAttribute('aria-hidden', 'true'); btn.insertBefore(bd, btn.firstChild);
      wp = D.createElement('span'); wp.className = PFX + '-warp'; wp.setAttribute('aria-hidden', 'true'); btn.insertBefore(wp, bd);
    }
    var p = refractParts(api, B, w, h, r, o || {});
    wp.style.filter = p.filter; wp.style.backdropFilter = wp.style.webkitBackdropFilter = p.backdrop;
    btn.style.backdropFilter = btn.style.webkitBackdropFilter = '';
    btn.classList.add(PFX + '-warped');
  }
  /* Liquid mode, clear glass: pick the label the way vibrancy does. Either ink on thin white glass or white
     on thin smoked glass, whichever reaches AA with less opacity over what is behind. */
  function liquidLabel(B, worst) {
    if (!liquid() || B.prim || B.dark) return null;
    var a1 = glassAlpha(INK, worst, false, WHITE, .1), a2 = glassAlpha(WHITE, worst, true, [22, 22, 24], .1);
    return a1 <= a2 + .05 ? { fg: INK, gc: WHITE, a: a1 } : { fg: WHITE, gc: [22, 22, 24], a: a2 };
  }
  function applyMode(btn, lab) {
    btn.classList.toggle(PFX + '-liquid', liquid());
    if (lab) { btn.style.setProperty('--' + PFX + '-bg', rgba(lab.gc, lab.a)); btn.style.color = 'rgb(' + lab.fg.join(',') + ')'; }
    else { btn.style.removeProperty('--' + PFX + '-bg'); btn.style.color = ''; }
  }

  /* ---------- button setup ---------- */
  /* Fill colour: any CSS colour, including rgba() and 8-digit hex. Returns [r,g,b,a]. */
  function parseFill(v) { if (!v) return null; var h = hex(v); if (h) return h.concat(1); var c = parse(String(v).trim()); return c ? [c[0], c[1], c[2], c[3] == null ? 1 : c[3]] : null; }
  /* Label colour for a solid fill: white when the fill can reach 4.5:1 with a small darkening
     (at most 3 nudges, so the brand colour survives), otherwise ink. Then nudge the fill until AA holds. */
  function solidLabel(fill, force) {
    var fg = force, f = fill, i = 0;
    if (!fg) {
      var t = fill; for (i = 0; i <= 1 && contrast(WHITE, t) < 4.5; i++) t = mix(t, [0, 0, 0], .06);
      fg = contrast(WHITE, t) >= 4.5 ? WHITE : INK;
    }
    for (i = 0; i < 40 && contrast(fg, f) < 4.5; i++) f = mix(f, fg[0] > 128 ? [0, 0, 0] : WHITE, .03);
    return { fg: fg, fill: f };
  }
  var tintStyled = false;
  function setupButton(btn, o) {
    var variant = o.variant || btn.getAttribute(ATTR) || 'secondary';
    if (!/^(primary|secondary|dark)$/.test(variant)) variant = 'secondary';
    var prim = variant === 'primary', dark = variant === 'dark';
    var fc = parseFill(o.fill || btn.getAttribute('data-fill')), fa = fc ? clamp(fc[3], 0, 1) : 1;
    var fill = fc ? fc.slice(0, 3) : (dark ? [22, 22, 24] : prim ? INK : WHITE);
    var tint = prim && fa < .97, ff = btn.getAttribute('data-fg'), force = ff === 'white' ? WHITE : ff === 'ink' ? INK : null, fg;
    if (tint) fg = force || (lum(fill) < .35 ? WHITE : INK); // translucent: keep the colour, raise opacity for AA instead
    else if (prim) { var sl = solidLabel(fill, force); fg = sl.fg; fill = sl.fill; }
    else fg = dark ? [245, 245, 247] : INK;
    if (!tintStyled) {
      var st = D.createElement('style'), P = '.' + PFX;
      // liquid rim: a bright specular ring, strongest top-left and bottom-right, as on Apple's glass
      st.textContent = P + P + '-tint{--' + PFX + '-bg:rgba(var(--' + PFX + '-f),var(--' + PFX + '-a,.6))}' +
        P + P + '-warped{background:transparent;backdrop-filter:none;-webkit-backdrop-filter:none}' +
        // the warp carries only the backdrop (its own background would be lost by the filter);
        // the glass colour and inner ring sit on an unfiltered layer right above it
        P + '>' + P + '-warp,' + P + '>' + P + '-body{position:absolute;inset:0;z-index:0;display:block;border-radius:inherit;pointer-events:none}' +
        P + '>' + P + '-body{background:var(--' + PFX + '-bg);box-shadow:inset 0 0 0 .5px rgba(0,0,0,.12),inset 0 1px 0 rgba(255,255,255,.55)}' +
        P + P + '-dark>' + P + '-body,' + P + P + '-tint>' + P + '-body{box-shadow:inset 0 0 0 .5px rgba(255,255,255,.16),inset 0 1px 0 rgba(255,255,255,.12)}' +
        P + P + '-liquid{box-shadow:var(--' + PFX + '-sh),0 8px 24px rgba(0,0,0,.14)}' +
        P + P + '-liquid::before{content:"";position:absolute;inset:0;z-index:4;border-radius:inherit;padding:1.5px;pointer-events:none;' +
        'background:linear-gradient(135deg,rgba(255,255,255,.85) 0%,rgba(255,255,255,.25) 30%,rgba(255,255,255,.08) 55%,rgba(255,255,255,.6) 100%);' +
        '-webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask-composite:exclude}';
      D.head.appendChild(st); tintStyled = true;
    }
    btn.classList.add(PFX, PFX + '-' + variant); if (tint) btn.classList.add(PFX + '-tint');
    btn.setAttribute('data-glass-kind', prim && !tint ? 'solid' : 'clear');
    if (prim) btn.setAttribute('data-glass-fill', toHex(fill));
    btn.style.setProperty('--' + PFX + '-f', fill.map(Math.round).join(','));
    btn.style.setProperty('--' + PFX + '-fg', 'rgb(' + fg.join(',') + ')');
    if (tint) btn.style.setProperty('--' + PFX + '-a', fa.toFixed(2));
    if (!btn.querySelector(':scope>span')) { var sp = D.createElement('span'); while (btn.firstChild) sp.appendChild(btn.firstChild); btn.appendChild(sp); }
    var cv = D.createElement('canvas'); btn.insertBefore(cv, btn.firstChild);
    // reflections are added light: on a solid fill they screen onto it, so blue + a yellow neighbour
    // brightens toward warm instead of averaging to grey-green. Not on translucent fills: a blended
    // child isolates the button, and the glass then sees an empty backdrop.
    if (prim && !tint) cv.style.mixBlendMode = 'screen';
    // translucent dark fills dim and saturate what shows through (like Apple's dark glass), so they can stay
    // see-through and still hold AA; light ones brighten it
    var dim = tint ? (fg[0] > 128 ? .6 : 1.12) : 1;
    var bfx = tint ? (dim !== 1 ? ' brightness(' + dim + ')' : '') + ' saturate(1.7)' : '';
    var flab = toLab(fill), colour = prim && Math.sqrt(flab[1] * flab[1] + flab[2] * flab[2]) > .05;
    return { variant: variant, prim: prim, dark: dark, tint: tint, fa: fa, fill: fill, flab: flab, colour: colour, dim: dim, bfx: bfx, fg: fg, cv: cv, ctx: cv.getContext('2d'), str: +(o.strength || btn.getAttribute('data-strength') || 1) };
  }
  // what the button's own surface looks like (for salience): fill, or fill over the backdrop
  function surfaceOf(B, base, kClear, kDark) { return B.prim ? (B.tint ? mix(base, B.fill, B.fa) : B.fill) : B.dark ? mix(base, B.fill, kDark) : mix(base, WHITE, kClear); }
  /* Reflection colour on this button. Neutral fills: the source hue at a fixed lightness.
     Coloured fills: keep the SOURCE hue at full-ish chroma, a little lighter than the fill. Mixing the two
     hues in Lab would pass through grey (blue + yellow = mud); a vivid thin edge over the fill reads as
     a warm catch instead. Same-hue neighbours were already scored near zero by salience(). */
  function reflectOn(B, a, b, L, Cmax) {
    if (!B.colour) return reflectColour(a, b, L, Cmax);
    var C = Math.sqrt(a * a + b * b) || 1e-6, Ct = clamp(C, .09, .17);
    return fromLab([clamp(B.flab[0] + .12, .62, .94), a / C * Ct, b / C * Ct]);
  }
  // glass opacity that keeps the label at 4.6:1 or better over the worst thing behind it
  function behind(btn, R, fg) {
    var memo = new Map(), base = null, worst = null; btn._busy = false;
    [.15, .5, .85].forEach(function (f) {
      var x = R.left + R.width * f, y = R.top + R.height / 2, c = colorAt(x, y, btn, memo) || WHITE;
      if (x >= 0 && y >= 0 && x < W.innerWidth && y < W.innerHeight && textBehind(hitAt(x, y, btn))) btn._busy = true;
      if (f === .5) base = c;
      if (!worst || contrast(fg, c) < contrast(fg, worst)) worst = c;
    });
    return { base: base, worst: worst };
  }
  function glassAlpha(fg, worst, dark, fill, start, dim) {
    if (dim) worst = worst.map(function (v) { return clamp(v * dim, 0, 255); });
    var a = start; while (a < .94 && contrast(fg, mix(worst, dark ? fill : WHITE, a)) < 4.6) a += .03;
    return a;
  }
  function easeArr(cur, tgt, f) {
    var more = false;
    for (var i = 0; i < cur.length; i++) { var dv = tgt[i] - cur[i]; if (Math.abs(dv) > .0015) { cur[i] += dv * f; more = true; } else cur[i] = tgt[i]; }
    return more;
  }
  // hover state + an rAF loop that only runs while something is easing
  function animator(btn, draw, ease) {
    var s = { k: 0, goal: 0, px: 0, py: 0, sx: 0, sy: 0 }, raf = 0, last = 0;
    function tick(now) {
      raf = 0;
      var dt = Math.min(48, last ? now - last : 16), more = false; last = now;
      if (RM.matches) { s.k = s.goal = 0; ease(1); draw(s); last = 0; return; }
      if (s.k !== s.goal) { s.k = s.goal > s.k ? Math.min(s.goal, s.k + dt / 180) : Math.max(s.goal, s.k - dt / 260); more = true; }
      var f = 1 - Math.exp(-dt / 80);
      if (Math.abs(s.px - s.sx) + Math.abs(s.py - s.sy) > .3) { s.sx += (s.px - s.sx) * f; s.sy += (s.py - s.sy) * f; more = true; }
      if (ease(f)) more = true;
      draw(s);
      if (more) raf = requestAnimationFrame(tick); else last = 0;
    }
    s.kick = function () { if (!raf) raf = requestAnimationFrame(tick); };
    function at(e) { var b = btn.getBoundingClientRect(); s.px = e.clientX - b.left; s.py = e.clientY - b.top; }
    btn.addEventListener('pointerenter', function (e) { if (btn.disabled || RM.matches) return; at(e); if (!s.k) { s.sx = s.px; s.sy = s.py; } s.goal = 1; s.kick(); });
    btn.addEventListener('pointermove', function (e) { if (!s.goal) return; at(e); s.kick(); }, { passive: true });
    btn.addEventListener('pointerleave', function () { s.goal = 0; s.kick(); });
    return s;
  }

  /* ---------- batched, throttled refresh: every read, then every write ---------- */
  var all = [], pend = 0, timer = 0, lastRun = 0, GAP = 60, io = null, ro = null;
  function run() {
    pend = 0; lastRun = performance.now();
    var vis = all.filter(function (a) { return a.visible; });
    vis.forEach(function (a) { a.scan(); });
    vis.forEach(function (a) { a.write(); });
  }
  function refresh(now) {
    if (pend) return;
    var wait = now ? 0 : GAP - (performance.now() - lastRun);
    if (wait <= 0) { clearTimeout(timer); timer = 0; pend = requestAnimationFrame(run); }
    else if (!timer) timer = setTimeout(function () { timer = 0; pend = requestAnimationFrame(run); }, wait);
  }
  function register(api) {
    all.push(api); api.visible = true;
    if (W.IntersectionObserver) {
      io = io || new IntersectionObserver(function (es) { es.forEach(function (e) { var a = e.target['_' + PFX]; if (a) a.visible = e.isIntersecting; }); refresh(); }, { rootMargin: '80px' });
      io.observe(api.el);
    }
    if (W.ResizeObserver) { ro = ro || new ResizeObserver(function () { refresh(); }); ro.observe(api.el); }
  }
  W.addEventListener('resize', function () { refresh(); }, { passive: true });
  W.addEventListener('scroll', function () { refresh(); }, { passive: true, capture: true });
  W.addEventListener('load', function () { refresh(true); });
  D.addEventListener('load', function (e) { if (e.target && e.target.tagName === 'IMG') refresh(); }, true);
  if (D.fonts && D.fonts.ready) D.fonts.ready.then(function () { refresh(true); });
  function boot(fn, name) {
    fn.init = function (root) { var l = [].map.call((root || D).querySelectorAll('[' + ATTR + ']'), function (b) { return fn(b); }); refresh(true); return l; };
    fn.refresh = function () { refresh(true); };
    fn.refraction = REFRACT;
    W[name] = fn;
    if (D.readyState === 'loading') D.addEventListener('DOMContentLoaded', function () { fn.init(); }); else fn.init();
  }
  /* ===== end core ===== */
