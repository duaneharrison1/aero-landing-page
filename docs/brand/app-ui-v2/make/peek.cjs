// Inspection helper: shoots each frame (.x-theme) of one section into the scratchpad.
const { chromium } = require('/home/claude/e2e/node_modules/playwright');
const path = require('path');
const out = process.env.OUT;
(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.join(__dirname, 'pages.html'));
  await page.addStyleTag({ content: '.theme-toggle{display:none}' });
  await page.waitForTimeout(2000);
  for (const id of process.argv.slice(2)) {
    const els = await page.$$('#' + id + ' .x-theme');
    for (let i = 0; i < els.length; i++) { await els[i].screenshot({ path: `${out}/${id}-${i}.png` }); }
    console.log(id, els.length);
  }
  await browser.close();
})();
