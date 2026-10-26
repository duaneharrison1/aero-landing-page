// Shoots every light frame of make and review pages, at 1x, into frames/<team>-<section>-<n>.png
const { chromium } = require('/home/claude/e2e/node_modules/playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  for (const [team, sel] of [['make', '.x-theme[data-theme="light"]'], ['review', '[data-theme="light"].frame']]) {
    const p = await b.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
    await p.goto(`file:///home/claude/research/v3/${team}/pages.html`, { waitUntil: 'networkidle' });
    await p.waitForTimeout(2000);
    const els = await p.$$(sel); const n = {};
    for (const el of els) {
      const sid = await el.evaluate(e => (e.closest('section') || {}).id || 'x');
      n[sid] = (n[sid] || 0) + 1;
      await el.screenshot({ path: `frames/${team}-${sid}-${n[sid]}.png` });
    }
    console.log(team, JSON.stringify(n));
  }
  await b.close();
})();
