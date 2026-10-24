// Screenshots of each section of pages.html at 1440 wide: shots/<id>.png
// Usage: node shoot-studio.cjs [id ...]
const { chromium } = require('/home/claude/e2e/node_modules/playwright');
const path = require('path');
const IDS = ['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'f1', 'm1'];
(async () => {
  const want = process.argv.slice(2).length ? process.argv.slice(2) : IDS;
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.join(__dirname, 'pages.html'), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(1200);
  const over = await page.evaluate(() => document.documentElement.scrollWidth);
  console.log('scrollWidth', over);
  for (const id of want) {
    const el = await page.$('#' + id);
    await el.scrollIntoViewIfNeeded();
    await page.waitForTimeout(300);
    await el.screenshot({ path: path.join(__dirname, 'shots', id + '.png') });
    console.log('shot', id);
  }
  await browser.close();
})();
