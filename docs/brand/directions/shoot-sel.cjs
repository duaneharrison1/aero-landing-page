// node shoot-sel.cjs absHtml selector prefix [width]
const { chromium } = require('/home/claude/e2e/node_modules/playwright');
(async () => {
  const [, , file, sel, prefix, w = '1440'] = process.argv;
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: +w, height: 900 } });
  await p.goto('file://' + file, { waitUntil: 'networkidle' });
  await p.waitForTimeout(1500); await p.addStyleTag({content:'#arb{display:none!important}'});
  const els = await p.$$(sel); let i = 0;
  for (const e of els) { i++; await e.screenshot({ path: `shots/${prefix}-${i}.png` }); console.log(prefix + '-' + i); }
  await b.close();
})();
