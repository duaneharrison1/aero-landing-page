// Screenshots and the hero loop video for the homepage round.
// node shoot.cjs [shots|video|all]   (default all)
const { chromium } = require('/home/claude/e2e/node_modules/playwright');
const path = require('path');
const fs = require('fs');
const { execFileSync } = require('child_process');
const DIR = __dirname;
const OUT = path.join(DIR, 'shots');
const URL = 'file://' + path.join(DIR, 'home.html');
const what = process.argv[2] || 'all';
fs.mkdirSync(OUT, { recursive: true });

// Chromium can't paint one image taller than 16384 px, so long pages are shot in slices and stitched.
async function fullShot(page, file, w, dpr) {
  const H = await page.evaluate(() => document.documentElement.scrollHeight);
  const step = Math.floor(12000 / dpr);
  const parts = [];
  for (let y = 0; y < H; y += step) {
    const f = `${file}.part${parts.length}.png`;
    await page.screenshot({ path: f, fullPage: true, clip: { x: 0, y, width: w, height: Math.min(step, H - y) } });
    parts.push(f);
  }
  execFileSync('python3', ['-c', `
import sys
from PIL import Image
ims=[Image.open(f) for f in sys.argv[2:]]
out=Image.new('RGB',(ims[0].width,sum(i.height for i in ims)),'white')
y=0
for i in ims: out.paste(i,(0,y)); y+=i.height
out.save(sys.argv[1])`, file, ...parts]);
  parts.forEach(f => fs.unlinkSync(f));
}

async function settle(page) {
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(900);
}

(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  if (what === 'shots' || what === 'all') {
    for (const hero of ['a', 'b']) {
      for (const [w, h, dpr, tag] of [[1440, 900, 2, 'd1440'], [390, 844, 3, 'm390']]) {
        const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: dpr });
        const page = await ctx.newPage();
        await page.goto(`${URL}?hero=${hero}&shoot=1&state=4&still=1`);
        await settle(page);
        const sw = await page.evaluate(() => { scrollTo(600, 0); const x = scrollX; scrollTo(0, 0); return [innerWidth + x, innerWidth]; });
        if (sw[0] > sw[1]) console.log(`!! sideways scroll hero ${hero} ${tag}: ${sw[0]} > ${sw[1]}`);
        await page.screenshot({ path: `${OUT}/home-${hero}-${tag}-fold.png` });
        await fullShot(page, `${OUT}/home-${hero}-${tag}-full.png`, w, dpr);
        await ctx.close();
      }
    }
    // the hero loop states, desktop, hero A
    const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
    const page = await ctx.newPage();
    for (const s of [0, 1, 2, 3, 4]) {
      await page.goto(`${URL}?hero=a&shoot=1&state=${s}&still=1`);
      await settle(page);
      const el = await page.$('.hp-stage');
      await el.screenshot({ path: `${OUT}/loop-state-${s}.png` });
    }
    await ctx.close();
    console.log('shots done');
  }
  if (what === 'video' || what === 'all') {
    const vdir = path.join(DIR, 'shots', '_video');
    fs.rmSync(vdir, { recursive: true, force: true });
    const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1, recordVideo: { dir: vdir, size: { width: 1440, height: 900 } } });
    const page = await ctx.newPage();
    await page.goto(`${URL}?hero=a&shoot=1`);
    await page.evaluate(() => document.fonts.ready);
    // frame the app window: scroll so the stage sits in view
    await page.evaluate(() => { const s = document.querySelector('.hp-stage'); scrollTo(0, s.getBoundingClientRect().top + scrollY - 40); });
    await page.waitForTimeout(16500);
    await ctx.close();
    const webm = fs.readdirSync(vdir).find(f => f.endsWith('.webm'));
    execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-ss', '1.0', '-i', path.join(vdir, webm), '-t', '15', '-vf', 'fps=30,scale=1440:-2', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-movflags', '+faststart', path.join(OUT, 'hero-loop.mp4')]);
    fs.rmSync(vdir, { recursive: true, force: true });
    console.log('video done');
  }
  await browser.close();
})();
