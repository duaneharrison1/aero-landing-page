// Screenshots of home.html: full page and fold at 1440 (2x) and 390 (2x), plus hero replay frames.
// Usage: node shoot.cjs            (all)    node shoot.cjs quick   (1440 fold + full only)
const { chromium } = require('/home/claude/e2e/node_modules/playwright');
const path = require('path');
const OUT = path.join(__dirname, 'shots');
const URL = 'file://' + path.join(__dirname, 'home.html');

async function open(browser, w, h, q = '?t=189') {
  const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 2 });
  page.on('console', m => { if (m.type() === 'error') console.log(`[${w}] console:`, m.text()); });
  page.on('pageerror', e => console.log(`[${w}] pageerror:`, e.message));
  await page.goto(URL + q, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(1200);
  const sw = await page.evaluate(() => [document.documentElement.scrollWidth, document.documentElement.clientWidth]);
  console.log(`[${w}] scrollWidth ${sw[0]} vs ${sw[1]}${sw[0] > sw[1] ? '  <-- SIDEWAYS SCROLL' : ''}`);
  return page;
}

(async () => {
  const quick = process.argv[2] === 'quick';
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  for (const [w, h, tag] of quick ? [[1440, 900, 'd']] : [[1440, 900, 'd'], [390, 844, 'm']]) {
    const page = await open(browser, w, h);
    await page.screenshot({ path: path.join(OUT, `home-${tag}-fold.png`) });
    // reveal everything before the full-page shot
    await page.evaluate(() => document.querySelectorAll('.h-tlx').forEach(e => e.classList.add('in')));
    await page.waitForTimeout(2800);
    // Chromium blanks anything past 16384 device px in one capture, so the full page is taken in slices and stitched
    const H = await page.evaluate(() => document.documentElement.scrollHeight);
    const parts = [];
    for (let y = 0, i = 0; y < H; y += 3000, i++) {
      const f = path.join(OUT, `.part-${tag}-${i}.png`);
      await page.screenshot({ path: f, fullPage: true, clip: { x: 0, y, width: w, height: Math.min(3000, H - y) } });
      parts.push(f);
    }
    require('child_process').execFileSync('python3', ['-I', '-c', 'import sys;from PIL import Image\nims=[Image.open(p) for p in sys.argv[2:]]\nout=Image.new("RGB",(ims[0].width,sum(i.height for i in ims)),"white")\ny=0\nfor i in ims: out.paste(i,(0,y)); y+=i.height\nout.save(sys.argv[1])', path.join(OUT, `home-${tag}-full.png`), ...parts]);
    parts.forEach(p => require('fs').unlinkSync(p));
    console.log('shot', tag);
    await page.close();
  }
  if (!quick) {
    // the replay: three moments of the loop, at 1440
    const page = await open(browser, 1440, 900, '?t=150');
    for (const t of [150, 189, 212]) {
      await page.goto(URL + '?t=' + t, { waitUntil: 'networkidle' });
      await page.waitForTimeout(900);
      const el = await page.$('.h-stage');
      await el.screenshot({ path: path.join(OUT, `hero-replay-${t}.png`) });
    }
    // and the live loop running for a few seconds, to check it moves without errors
    await page.goto(URL, { waitUntil: 'networkidle' });
    await page.waitForTimeout(6000);
    await (await page.$('.h-stage')).screenshot({ path: path.join(OUT, 'hero-live-6s.png') });
    console.log('replay shots');
  }
  await browser.close();
})();
