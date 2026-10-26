// Measures the colour test: for every tile, the task title's colour against the worst pixel behind it.
// The title text is hidden, the box is screenshotted, and every pixel is checked. Writes src/tester-contrast.json.
// node tester-measure.mjs
import { createRequire } from 'module';
import fs from 'fs';
const require = createRequire(import.meta.url);
const { chromium } = require('/home/claude/e2e/node_modules/playwright');
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const p = await b.newPage({ viewport: { width: 2800, height: 1200 }, reducedMotion: 'reduce' });
await p.goto('file://' + process.cwd() + '/tester.html', { waitUntil: 'networkidle' });
await p.evaluate(async () => { await document.fonts.ready; });
await p.waitForTimeout(2500);
// measure at real size: undo the board's scaling
await p.addStyleTag({ content: '.tb-wrap{max-width:none!important}.tb-ct{grid-template-columns:120px repeat(4,600px)!important}' });
await p.evaluate(() => { document.querySelectorAll('[data-tile]').forEach(t => { const s = t.closest('.tb-scale'); s.style.transform = 'none'; s.parentElement.style.height = 'auto'; s.parentElement.style.overflow = 'visible'; }); window.GlassV3 && GlassV3.refresh(); });
await p.waitForTimeout(1500);
const keys = await p.$$eval('[data-tile]', ts => ts.map(t => t.dataset.tile));
const out = {};
async function measure(key, sel) {
  const tile = p.locator(`[data-tile="${key}"]`);
  await tile.scrollIntoViewIfNeeded();
  await p.waitForTimeout(250);
  const el = tile.locator(sel).first();
  const fg = await el.evaluate(e => getComputedStyle(e).color);
  await el.scrollIntoViewIfNeeded();
  await el.evaluate(e => { e.style.visibility = 'hidden'; });
  await p.waitForTimeout(120);
  const host = tile.locator('[data-measure]').first();
  const hb = await host.boundingBox(), eb = await el.boundingBox();
  const full = await host.screenshot();
  const crop = { x: Math.round(eb.x - hb.x), y: Math.round(eb.y - hb.y), w: Math.round(eb.width), h: Math.round(eb.height) };
  if (process.env.DUMP) fs.writeFileSync(process.env.DUMP + "/" + key.replace(":", "-") + sel.replace(/[^a-z]/g, "") + ".png", full);
  const bf = await el.evaluate(e => getComputedStyle(e.closest('.tx-panel,.tx-mini')).backdropFilter);
  await el.evaluate(e => { e.style.visibility = ''; });
  const r = await p.evaluate(async ({ b64, fg, crop }) => {
    const img = new Image(); img.src = 'data:image/png;base64,' + b64; await img.decode();
    const c = document.createElement('canvas'); c.width = img.width; c.height = img.height;
    const x = c.getContext('2d'); x.drawImage(img, 0, 0); const d = x.getImageData(crop.x, crop.y, crop.w, crop.h).data;
    const m = fg.match(/[\d.]+/g).map(Number); const a = m[3] == null ? 1 : m[3];
    const lin = v => { v /= 255; return v <= .04045 ? v / 12.92 : Math.pow((v + .055) / 1.055, 2.4); };
    const L = (r, g, b) => .2126 * lin(r) + .7152 * lin(g) + .0722 * lin(b);
    let min = 99, worst = null;
    for (let i = 0; i < d.length; i += 4) {
      // text with alpha blends over the pixel
      const tr = m[0] * a + d[i] * (1 - a), tg = m[1] * a + d[i + 1] * (1 - a), tb = m[2] * a + d[i + 2] * (1 - a);
      const l1 = L(tr, tg, tb), l2 = L(d[i], d[i + 1], d[i + 2]);
      const cr = (Math.max(l1, l2) + .05) / (Math.min(l1, l2) + .05);
      if (cr < min) { min = cr; worst = [d[i], d[i + 1], d[i + 2]]; }
    }
    return { min: Math.round(min * 100) / 100, fg, worst };
  }, { b64: full.toString('base64'), fg, crop });
  r.bf = bf; return r;
}
for (const key of keys) {
  const style = key.split(':')[1];
  const sel = style === 'mini' ? '.tx-mini-t' : 'h2';
  out[key] = await measure(key, sel);
  // secondary text too (instructions), for the panels
  if (style !== 'mini') out[key].ins = (await measure(key, '.tx-ins')).min;
  console.log(key, out[key].min, JSON.stringify(out[key].worst), out[key].bf, 'ins', out[key].ins ?? '-', out[key].fg);
}
// a more opaque plate (.94), for comparison
await p.evaluate(() => document.querySelectorAll('[data-tile$=":plate"] .tx-panel').forEach(e => e.style.setProperty('--tx-plate', 'rgba(255,255,255,.94)')));
for (const key of keys.filter(k => k.endsWith(':plate'))) {
  const r = await measure(key, '.tx-ins'); out[key.replace('plate', 'plate94')] = { min: (await measure(key, 'h2')).min, ins: r.min };
  console.log(key, '@.94', out[key.replace('plate', 'plate94')]);
}
fs.writeFileSync('src/tester-contrast.json', JSON.stringify(out, null, 1));
await b.close();
