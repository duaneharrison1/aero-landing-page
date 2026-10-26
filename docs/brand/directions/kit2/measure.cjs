// Measures every [data-m] button: label colour against the worst pixel under its label, label hidden.
// Writes contrast.json, which build.py turns into the per-option tables.
const { chromium } = require('/home/claude/e2e/node_modules/playwright');
const path = require('path'), fs = require('fs');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.join(__dirname, 'pages.html'), { waitUntil: 'networkidle' });
  await p.evaluate(async () => { await document.fonts.ready; });
  await p.addStyleTag({ content: '.mhide,.mhide *{color:transparent!important;-webkit-text-fill-color:transparent!important}' });
  const n = await p.evaluate(() => document.querySelectorAll('[data-m]').length);
  const out = {};
  for (let i = 0; i < n; i++) {
    const info = await p.evaluate(async (i) => {
      const el = document.querySelectorAll('[data-m]')[i];
      el.scrollIntoView({ block: 'center' });
      await new Promise(r => setTimeout(r, 50));
      window.GlassV3 && GlassV3.refresh();
      await new Promise(r => setTimeout(r, 450));
      const root = el.querySelector('[data-lbl]') || el;
      const rects = [];
      const tw = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
      let t, colEl = null;
      while ((t = tw.nextNode())) { if (!t.textContent.trim()) continue; const r = document.createRange(); r.selectNodeContents(t); for (const q of r.getClientRects()) rects.push(q); colEl = colEl || t.parentElement; }
      if (!rects.length) { const s = el.querySelector('svg'); if (s) { rects.push(s.getBoundingClientRect()); colEl = s; } }
      const L = Math.min(...rects.map(r => r.left)), T = Math.min(...rects.map(r => r.top)), R = Math.max(...rects.map(r => r.right)), Bm = Math.max(...rects.map(r => r.bottom));
      const fg = getComputedStyle(colEl).color;
      el.classList.add('mhide');
      return { name: el.dataset.m, t: +el.dataset.t, sec: el.closest('section').id, fg, clip: { x: L, y: T + 1, width: R - L, height: Bm - T - 2 } };
    }, i);
    await p.waitForTimeout(80);
    const buf = await p.screenshot({ clip: info.clip });
    const res = await p.evaluate(async ({ b64, fg }) => {
      const img = new Image(); img.src = 'data:image/png;base64,' + b64; await img.decode();
      const c = document.createElement('canvas'); c.width = img.width; c.height = img.height; const x = c.getContext('2d'); x.drawImage(img, 0, 0);
      const d = x.getImageData(0, 0, c.width, c.height).data;
      const lin = v => { v /= 255; return v <= .04045 ? v / 12.92 : Math.pow((v + .055) / 1.055, 2.4); };
      const lum = c => .2126 * lin(c[0]) + .7152 * lin(c[1]) + .0722 * lin(c[2]);
      const m = /rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)(?:,\s*([\d.]+))?/.exec(fg); const f = [+m[1], +m[2], +m[3]], fa = m[4] == null ? 1 : +m[4];
      let worst = null, wr = 99, seen = new Set();
      for (let k = 0; k < d.length; k += 4) {
        const bg = [d[k], d[k + 1], d[k + 2]]; seen.add(bg.join(','));
        const ff = f.map((v, j) => v * fa + bg[j] * (1 - fa));
        const a = lum(ff) + .05, bb = lum(bg) + .05, r = a > bb ? a / bb : bb / a;
        if (r < wr) { wr = r; worst = bg; }
      }
      const hx = c => '#' + c.map(v => Math.round(v).toString(16).padStart(2, '0')).join('').toUpperCase();
      return { ratio: wr, bg: hx(worst), fg: hx(f), varied: seen.size > 3 };
    }, { b64: buf.toString('base64'), fg: info.fg });
    await p.evaluate((i) => document.querySelectorAll('[data-m]')[i].classList.remove('mhide'), i);
    (out[info.sec] = out[info.sec] || []).push({ name: info.name, t: info.t, ...res });
    console.log(info.sec, info.name, res.fg, res.bg, res.ratio.toFixed(2));
  }
  fs.writeFileSync(path.join(__dirname, 'contrast.json'), JSON.stringify(out, null, 1));
  await b.close();
})();
