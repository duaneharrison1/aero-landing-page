const { chromium } = require('playwright');
const dir = __dirname;
(async () => {
  const b = await chromium.launch(), errs = [];
  const p = await b.newPage({ viewport: { width: 1512, height: 789 }, deviceScaleFactor: 2 });
  p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('file://' + dir + '/index.html'); await p.waitForTimeout(1800);
  await p.screenshot({ path: dir + '/shots/01-fold-1512.png' });
  const clickBtn = (pg, name) => pg.evaluate(n => { const b = [...document.querySelectorAll('#gp-body .gp-seg button')].find(b => b.firstChild && b.firstChild.textContent.trim() === n); if (!b) throw new Error('no button ' + n); b.click(); }, name);
  const preset = async (name) => { await clickBtn(p, name); await p.waitForTimeout(900); };
  for (const [n, f] of [['V3 as picked', 'p-v3'], ['Agreed glass', 'p-agreed'], ['Round 4', 'p-r4'], ['Round 5', 'p-r5'], ['Subtle', 'p-subtle']]) {
    await preset(n); await p.evaluate(() => scrollTo(0, 0)); await p.waitForTimeout(400);
    const bb = await (await p.$('.s-hero .ctas')).boundingBox();
    await p.screenshot({ path: `${dir}/shots/${f}-hero.png`, clip: { x: bb.x - 20, y: bb.y - 20, width: 360, height: 100 } });
    await p.evaluate(() => scrollTo(0, 980)); await p.waitForTimeout(600);
    await p.screenshot({ path: `${dir}/shots/${f}-nav.png`, clip: { x: 0, y: 0, width: 1132, height: 110 } });
    await p.evaluate(() => document.querySelector('.band').scrollIntoView({ block: 'center' })); await p.waitForTimeout(600);
    const b2 = await (await p.$('.band .ctas')).boundingBox();
    await p.screenshot({ path: `${dir}/shots/${f}-wash.png`, clip: { x: b2.x - 20, y: b2.y - 20, width: 400, height: 90 } });
  }
  await preset('Round 5');
  for (const [n, f] of [['Lighting only', 'solo-light'], ['Caustic only', 'solo-caustic'], ['Refraction only', 'solo-refr'], ['Slab only', 'solo-slab'], ['Everything', 'solo-all']]) {
    await clickBtn(p, n); await p.waitForTimeout(800); await p.evaluate(() => scrollTo(0, 0)); await p.waitForTimeout(300);
    const bb = await (await p.$('.s-hero .ctas')).boundingBox();
    await p.screenshot({ path: `${dir}/shots/${f}.png`, clip: { x: bb.x - 20, y: bb.y - 20, width: 360, height: 100 } });
  }
  await clickBtn(p, 'Hover'); await p.waitForTimeout(800);
  const bb = await (await p.$('.s-hero .ctas')).boundingBox();
  await p.screenshot({ path: `${dir}/shots/hold-hover.png`, clip: { x: bb.x - 20, y: bb.y - 20, width: 360, height: 100 } });
  await clickBtn(p, 'Rest'); await p.waitForTimeout(300);
  // a slider: wall to 0
  await p.evaluate(() => { const i = document.getElementById('gp-wall'); i.value = 0; i.dispatchEvent(new Event('input')); }); await p.waitForTimeout(800);
  await p.screenshot({ path: `${dir}/shots/wall0.png`, clip: { x: bb.x - 20, y: bb.y - 20, width: 360, height: 100 } });
  // app spots and panel scrolled
  await p.evaluate(() => document.querySelectorAll('.app-spot')[0].scrollIntoView({ block: 'start' })); await p.waitForTimeout(800);
  await p.screenshot({ path: `${dir}/shots/02-app-1512.png` });
  await p.evaluate(() => document.getElementById('gp-body').scrollTop = 900); await p.waitForTimeout(300);
  await p.screenshot({ path: `${dir}/shots/03-panel-scrolled.png`, clip: { x: 1132, y: 0, width: 380, height: 789 } });
  const json = await p.evaluate(() => document.querySelector('.gp-json').value);
  console.log('json', json.slice(0, 160));
  const m = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 3 });
  m.on('pageerror', e => errs.push('m ' + e.message));
  await m.goto('file://' + dir + '/index.html'); await m.waitForTimeout(1500);
  await m.screenshot({ path: dir + '/shots/04-phone-closed.png' });
  await m.click('#gp-tab'); await m.waitForTimeout(800);
  await m.screenshot({ path: dir + '/shots/05-phone-open.png' });
  console.log(errs.length ? 'ERRORS\n' + errs.join('\n') : 'no errors');
  await b.close();
})();
