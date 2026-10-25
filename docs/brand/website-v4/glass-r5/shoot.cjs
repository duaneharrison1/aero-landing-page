// node shoot.cjs [what]  -> shots/*.png   (what: buttons | nav | all)
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
const dir = __dirname, out = path.join(dir, 'shots'); fs.mkdirSync(out, { recursive: true });
const what = process.argv[2] || 'all';
(async () => {
  const browser = await chromium.launch();
  const errs = [];
  async function open(q, vp, dsf = 2) {
    const page = await browser.newPage({ viewport: vp, deviceScaleFactor: dsf });
    page.on('pageerror', e => errs.push(q + ': ' + e.message)); page.on('console', m => { if (m.type() === 'error') errs.push(q + ': ' + m.text()); });
    await page.goto('file://' + dir + '/scene.html?' + q); await page.waitForTimeout(1500);
    return page;
  }
  if (what === 'buttons' || what === 'all') {
    for (const v of ['4', '5']) {
      const page = await open('v=' + v + '&s=buttons', { width: 1100, height: 1000 });
      await page.screenshot({ path: `${out}/btn-v${v}-all.png`, fullPage: true });
      for (const id of ['p0', 'p1', 'p2', 'p3', 'p4', 'p5']) { const el = await page.$('#' + id); await el.screenshot({ path: `${out}/btn-v${v}-${id}.png` }); }
      // real pointer hover on the hero pair, then keyboard focus
      for (const b of ['r0-ink', 'r0-clear']) {
        const bb = await (await page.$('#' + b)).boundingBox();
        await page.mouse.move(bb.x + bb.width * .25, bb.y + bb.height * .3); await page.waitForTimeout(700);
        await page.screenshot({ path: `${out}/btn-v${v}-ptr-${b}.png`, clip: { x: bb.x - 30, y: bb.y - 24, width: 330, height: bb.height + 48 } });
      }
      await page.mouse.move(2, 2); await page.waitForTimeout(500);
      await page.focus('#r0-clear'); await page.keyboard.press('Shift+Tab'); await page.keyboard.press('Tab'); await page.waitForTimeout(700);
      const fb = await (await page.$('#r0-ink')).boundingBox();
      await page.screenshot({ path: `${out}/btn-v${v}-focus.png`, clip: { x: fb.x - 30, y: fb.y - 24, width: 330, height: fb.height + 48 } });
      await page.close();
    }
  }
  if (what === 'nav' || what === 'all') {
    for (const v of ['4', '5']) {
      const page = await open('v=' + v + '&s=nav', { width: 1512, height: 789 });
      for (const y of [0, 330, 560, 900, 1300, 1560]) {
        await page.evaluate(y => scrollTo(0, y), y); await page.waitForTimeout(500);
        await page.screenshot({ path: `${out}/nav-v${v}-y${y}.png`, clip: { x: 0, y: 0, width: 1512, height: 150 } });
      }
      await page.evaluate(() => scrollTo(0, 0)); await page.waitForTimeout(400);
      await page.screenshot({ path: `${out}/fold-1512-v${v}.png` });
      await page.close();
    }
    const m = await open('v=5&s=nav', { width: 390, height: 844 }, 3);
    for (const y of [0, 560]) { await m.evaluate(y => scrollTo(0, y), y); await m.waitForTimeout(500); await m.screenshot({ path: `${out}/nav-390-y${y}.png`, clip: { x: 0, y: 0, width: 390, height: 120 } }); }
    await m.close();
  }
  console.log(errs.length ? 'ERRORS:\n' + errs.join('\n') : 'no errors');
  await browser.close();
})();
