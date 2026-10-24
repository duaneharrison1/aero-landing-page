// node shoot-h2.cjs absHtml prefix [width] : clips page between consecutive h2 headings
const { chromium } = require('/home/claude/e2e/node_modules/playwright');
(async () => {
  const [, , file, prefix, w = '1440'] = process.argv;
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: +w, height: 900 } });
  await p.goto('file://' + file, { waitUntil: 'networkidle' });
  await p.waitForTimeout(1500); await p.addStyleTag({content:'#arb{display:none!important}'});
  await p.addStyleTag({ content: '.review-bar,#rv-bar,[data-review-bar]{display:none!important}' });
  const boxes = await p.evaluate(() => {
    const hs = [...document.querySelectorAll('h2')];
    const H = document.documentElement.scrollHeight;
    return hs.map((h, i) => { const y = h.getBoundingClientRect().top + scrollY - 16; const n = hs[i + 1]; const y2 = n ? n.getBoundingClientRect().top + scrollY - 16 : H; return { t: h.textContent.trim().slice(0, 60), y, h: y2 - y }; });
  });
  let i = 0;
  for (const bx of boxes) { i++; if (bx.h < 80) continue; await p.screenshot({ path: `shots/${prefix}-${i}.png`, clip: { x: 0, y: bx.y, width: +w, height: Math.min(bx.h, 3000) }, fullPage: true }); console.log(prefix + '-' + i, bx.t, Math.round(bx.h)); }
  await b.close();
})();
