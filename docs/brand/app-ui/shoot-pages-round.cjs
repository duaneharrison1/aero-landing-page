// Usage: node shoot-pages-round.cjs <html path> <out dir> [width]
// Renders the full board and each section (#glance, #s1 to #s9) to PNG with Playwright (Chromium).
const { chromium } = require('/home/claude/e2e/node_modules/playwright');
const path = require('path');
(async () => {
  const [, , file, out, w = '1440'] = process.argv;
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: +w, height: 900 }, deviceScaleFactor: 1 });
  const errs = [];
  p.on('pageerror', e => errs.push(e.message));
  await p.goto('file://' + path.resolve(file) + '?layout=large', { waitUntil: 'networkidle' });
  await p.addStyleTag({content:'.b-top{position:static !important}'});
  await p.waitForTimeout(2000);
  await p.evaluate(() => window.aeFitAll && window.aeFitAll());
  await p.waitForTimeout(600);
  const suffix = +w < 600 ? '-390' : '';
  if (+w >= 600) await p.screenshot({ path: out + '/pages-round-full.png', fullPage: true });
  for (const id of ['glance', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9']) {
    const el = await p.$('#' + id);
    if (el) await el.screenshot({ path: `${out}/${id}${suffix}.png` });
  }
  console.log('done', errs.length ? errs.join(' | ') : 'no errors', 'scrollWidth', await p.evaluate(() => document.documentElement.scrollWidth));
  await b.close();
})();
