// Usage: node shoot.cjs page.html [width] [outname] [query] [clipY clipH]
const { chromium } = require('/home/claude/e2e/node_modules/playwright');
(async () => {
  const [, , page = 'components.html', w = '1440', out = 'shot', q = '', full = 'full'] = process.argv;
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: +w, height: 900 }, deviceScaleFactor: +w < 500 ? 2 : 1 });
  const errs = [];
  p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('file:///home/claude/research/app-ui/' + page + (q ? '?' + q : ''), { waitUntil: 'networkidle' });
  await p.waitForTimeout(1200);
  await p.evaluate(() => window.aeFitAll && window.aeFitAll());
  await p.waitForTimeout(500);
  const sw = await p.evaluate(() => document.documentElement.scrollWidth);
  await p.screenshot({ path: '/home/claude/research/app-ui/shots/' + out + '.png', fullPage: full === 'full' });
  const h = await p.evaluate(() => document.documentElement.scrollHeight);
  console.log(out, 'scrollWidth', sw, 'height', h, errs.length ? 'ERRORS: ' + errs.join(' | ') : 'no errors');
  await b.close();
})();
