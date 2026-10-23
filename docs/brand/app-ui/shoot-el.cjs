// node shoot-el.cjs page.html selector out [width] [query]
const { chromium } = require('/home/claude/e2e/node_modules/playwright');
(async () => {
  const [, , page, sel, out, w = '1440', q = ''] = process.argv;
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: +w, height: 900 }, deviceScaleFactor: +w < 500 ? 2 : 1 });
  await p.goto('file:///home/claude/research/app-ui/' + page + (q ? '?' + q : ''), { waitUntil: 'networkidle' });
  await p.waitForTimeout(1200); await p.evaluate(() => window.aeFitAll && window.aeFitAll()); await p.waitForTimeout(400);
  const el = await p.$(sel); await el.screenshot({ path: '/home/claude/research/app-ui/shots/' + out + '.png' });
  console.log('ok', out); await b.close();
})();
