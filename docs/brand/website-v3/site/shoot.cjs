// Screenshots of the site pages at 1440 (2x) and 390 (2x): fold and full page, into shots/.
// Usage: node shoot.cjs              (every page)
//        node shoot.cjs features     (pages whose name starts with "features")
//        node shoot.cjs features d   (desktop only; "m" for phone only)
const { chromium } = require('/home/claude/e2e/node_modules/playwright');
const path = require('path'), fs = require('fs'), cp = require('child_process');
const OUT = path.join(__dirname, 'shots');
const pages = fs.readdirSync(__dirname).filter(f => f.endsWith('.html')).filter(f => !process.argv[2] || f.startsWith(process.argv[2]));
const sizes = [[1440, 900, 'd'], [390, 844, 'm']].filter(s => !process.argv[3] || s[2] === process.argv[3]);

(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  for (const [w, h, tag] of sizes) {
    for (const f of pages) {
      const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 2 });
      page.on('console', m => { if (m.type() === 'error') console.log(`[${f} ${w}] console:`, m.text()); });
      page.on('pageerror', e => console.log(`[${f} ${w}] pageerror:`, e.message));
      await page.goto('file://' + path.join(__dirname, f), { waitUntil: 'networkidle' });
      await page.evaluate(() => document.fonts.ready);
      await page.waitForTimeout(1500);
      const sw = await page.evaluate(() => [document.documentElement.scrollWidth, document.documentElement.clientWidth]);
      if (sw[0] > sw[1]) console.log(`[${f} ${w}] SIDEWAYS SCROLL ${sw[0]} > ${sw[1]}`);
      const base = f.replace('.html', '');
      await page.screenshot({ path: path.join(OUT, `${base}-${tag}-fold.png`) });
      // Chromium blanks past 16384 device px in one capture: take slices and stitch
      const H = await page.evaluate(() => document.documentElement.scrollHeight);
      const parts = [];
      for (let y = 0, i = 0; y < H; y += 3000, i++) {
        const p = path.join(OUT, `.part-${tag}-${i}.png`);
        await page.screenshot({ path: p, fullPage: true, clip: { x: 0, y, width: w, height: Math.min(3000, H - y) } });
        parts.push(p);
      }
      cp.execFileSync('python3', ['-I', '-c', 'import sys;from PIL import Image\nims=[Image.open(p) for p in sys.argv[2:]]\nout=Image.new("RGB",(ims[0].width,sum(i.height for i in ims)),"white")\ny=0\nfor i in ims: out.paste(i,(0,y)); y+=i.height\nout.save(sys.argv[1])', path.join(OUT, `${base}-${tag}-full.png`), ...parts]);
      parts.forEach(p => fs.unlinkSync(p));
      console.log('shot', base, tag, H + 'px');
      await page.close();
    }
  }
  await browser.close();
})();
