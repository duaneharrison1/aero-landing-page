// Saves each section of pages.html as shots/<id>.png at 1440 wide.
const { chromium } = require('/home/claude/e2e/node_modules/playwright');
const path = require('path');
(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.join(__dirname, 'pages.html'));
  await page.waitForLoadState('networkidle'); await page.evaluate(() => document.fonts.ready); await page.waitForTimeout(400);
  const ids = process.argv.slice(2).length ? process.argv.slice(2) : ['p1','p2','p3','p4','p5','p6','f1','m1'];
  for (const id of ids) { await page.locator('#' + id).screenshot({ path: path.join(__dirname, 'shots', id + '.png'), animations: 'disabled' }); console.log('shot', id); }
  const sw = await page.evaluate(() => document.documentElement.scrollWidth); console.log('scrollWidth', sw);
  await browser.close();
})();
