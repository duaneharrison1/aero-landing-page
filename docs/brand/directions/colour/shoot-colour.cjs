// node shoot-colour.cjs [id ...]  -> shots/<id>.png at 1440 wide (each section)
const { chromium } = require('/home/claude/e2e/node_modules/playwright');
const path = require('path');
(async () => {
  const ids = process.argv.slice(2).length ? process.argv.slice(2) : ['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'f1', 'm1'];
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  await p.goto('file://' + path.join(__dirname, 'pages.html'), { waitUntil: 'networkidle' });
  await p.waitForTimeout(1800);
  const over = await p.evaluate(() => document.documentElement.scrollWidth);
  if (over > 1440) console.warn('page scrollWidth', over);
  for (const id of ids) {
    const el = await p.$('#' + id);
    await el.screenshot({ path: path.join(__dirname, 'shots', id + '.png') });
    console.log('shot', id);
  }
  await b.close();
})();
