// Screenshots for Team A (system and make): one PNG per section, 1440 wide, 2x.
const { chromium } = require('/home/claude/e2e/node_modules/playwright');
const path = require('path');
(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 });
  await page.goto('file://' + path.join(__dirname, 'pages.html'));
  await page.addStyleTag({ content: '.theme-toggle{display:none}' });
  await page.waitForTimeout(2500);
  const ids = process.argv.slice(2).length ? process.argv.slice(2) : ['g0', 'm1', 'm2', 'm3', 'm4', 'm5', 'm6', 'm7', 'm8'];
  for (const id of ids) {
    const el = await page.$('#' + id);
    await el.screenshot({ path: `/home/claude/research/v3/hi/A-${id}.png` });
    console.log('shot', id);
  }
  await browser.close();
})();
