// Full-size shots of each app frame in the app UI round (E), at 2x.
const { chromium } = require('/home/claude/e2e/node_modules/playwright');
const fs = require('fs');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: 1600, height: 1000 }, deviceScaleFactor: 2 });
  await p.goto('file:///home/claude/research/app-ui/screens.html', { waitUntil: 'networkidle' });
  await p.waitForTimeout(1200);
  await p.addStyleTag({ content: '#arb{display:none!important} .fit{width:auto!important;height:auto!important;overflow:visible!important} .fit__in{transform:none!important;position:static!important} .appr{display:block!important} .ap{width:auto!important;max-width:none!important}' });
  await p.waitForTimeout(600);
  const out = {};
  for (const s of ['s2','s3','s4','s7','s8','s9']) {
    const aps = await p.$$(`#${s} .ap`);
    out[s] = [];
    let i = 0;
    for (const ap of aps) {
      const app = await ap.$('.ae-app'); if (!app) continue;
      const label = await ap.evaluate(e => { const t = e.querySelector('.t'); return t ? t.textContent.trim().replace(/\s+/g,' ') : ''; });
      i++; const f = `e/${s}-${i}.png`;
      await app.screenshot({ path: f }); out[s].push([f, label]);
    }
  }
  fs.writeFileSync('e/index.json', JSON.stringify(out, null, 1));
  console.log(JSON.stringify(out, null, 1));
  await b.close();
})();
