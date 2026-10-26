// node shoot-story.cjs  -> shots/<id>.png for every section, at 1440 wide
const { chromium } = require('/home/claude/e2e/node_modules/playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.join(__dirname, 'pages.html'), { waitUntil: 'networkidle' });
  await p.waitForTimeout(1500);
  const sw = await p.evaluate(() => document.documentElement.scrollWidth);
  if (sw > 1440) console.log('WARN page scrollWidth', sw);
  const ids = process.argv.slice(2).length ? process.argv.slice(2) : ['p1','p2','p3','p4','p5','p6','f1','m1'];
  for (const id of ids) {
    const el = await p.$('#' + id);
    // pad the shot to the full 1440 width
    const box = await el.boundingBox();
    await p.screenshot({ path: path.join(__dirname, 'shots', id + '.png'), clip: { x: 0, y: box.y, width: 1440, height: box.height + 40 }, fullPage: true });
    console.log(id, Math.round(box.height));
  }
  await b.close();
})();
