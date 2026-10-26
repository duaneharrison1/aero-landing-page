// Screenshots each section of pages.html at 1440 wide into shots/<id>.png
const { chromium } = require('/home/claude/e2e/node_modules/playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1 });
  const errs = [];
  p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('file://' + path.join(__dirname, 'pages.html'), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(1500);
  const only = process.argv[2];
  for (const id of ['b1', 'b2', 'l1', 'l2', 'r1']) {
    if (only && only !== id) continue;
    const el = await p.$('#' + id);
    await el.scrollIntoViewIfNeeded(); await p.waitForTimeout(700);
    await el.screenshot({ path: path.join(__dirname, 'shots', id + '.png') });
  }
  console.log(errs.length ? errs.join('\n') : 'no errors');
  await b.close();
})();
