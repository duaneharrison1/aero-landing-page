// Screenshots of each section of pages.html at 1440 wide, 2x: ../hi/review-<id>.png
// Usage: node shoot-review.cjs [id ...]
const { chromium } = require('/home/claude/e2e/node_modules/playwright');
const path = require('path');
const IDS = ['s1', 's2', 's3', 's4', 's5', 's6', 's7'];
(async () => {
  const want = process.argv.slice(2).length ? process.argv.slice(2) : IDS;
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 2 });
  page.on('console', m => { if (m.type() === 'error') console.log('console:', m.text()); });
  page.on('pageerror', e => console.log('pageerror:', e.message));
  await page.goto('file://' + path.join(__dirname, 'pages.html'), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(1500);
  await page.addStyleTag({ content: '.theme-toggle{display:none}' });
  console.log('scrollWidth', await page.evaluate(() => document.documentElement.scrollWidth));
  for (const id of want) {
    const el = await page.$('#' + id);
    await el.scrollIntoViewIfNeeded();
    await page.waitForTimeout(300);
    await el.screenshot({ path: path.join(__dirname, '..', 'hi', 'review-' + id + '.png') });
    console.log('shot', id);
  }
  await browser.close();
})();
