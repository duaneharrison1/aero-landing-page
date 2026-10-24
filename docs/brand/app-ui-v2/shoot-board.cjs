const { chromium } = require('/home/claude/e2e/node_modules/playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  for (const w of [1440, 390]) {
    const p = await b.newPage({ viewport: { width: w, height: 1000 } });
    await p.goto('file:///home/claude/research/v2/board/index.html', { waitUntil: 'networkidle' });
    await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=800){scrollTo(0,y);await new Promise(r=>setTimeout(r,30))}scrollTo(0,0)});
    await p.waitForTimeout(800);
    const sw = await p.evaluate(() => [document.documentElement.scrollWidth, innerWidth]);
    console.log(w, sw);
    await p.screenshot({ path: `bshot-${w}-top.png` });
    await p.evaluate(()=>document.getElementById('watch').scrollIntoView());
    await p.screenshot({ path: `bshot-${w}-p3.png` });
  }
  await b.close();
})();
