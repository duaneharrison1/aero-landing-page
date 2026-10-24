// node shoot-xp.cjs dir : each section.xp of dir/pages.html at 2x into hi/<dir>-<id>.png
const { chromium } = require('/home/claude/e2e/node_modules/playwright');
(async () => {
  const dir = process.argv[2];
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 2 });
  await p.goto(`file:///home/claude/research/explore/${dir}/pages.html`, { waitUntil: 'networkidle' });
  await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=700){scrollTo(0,y);await new Promise(r=>setTimeout(r,60))}scrollTo(0,0)});
  await p.waitForTimeout(2500);
  for (const el of await p.$$('section.xp[id]')) {
    const id = await el.getAttribute('id');
    await el.screenshot({ path: `hi/${dir}-${id}.png` }); console.log(dir, id);
  }
  await b.close();
})();
