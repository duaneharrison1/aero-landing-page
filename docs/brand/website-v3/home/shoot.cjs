// Team H: screenshots and the hero MP4.
// node shoot.cjs            fold + full page at 1440 (2x) and 390 (2x), hero frames
// node shoot.cjs frames     hero frames only (1440 and 390)
// node shoot.cjs video      hero loop as shots/hero-loop.mp4 (1440 stage, 30 fps) and hero-loop-390.mp4
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const path = require('path'), fs = require('fs'), { execSync } = require('child_process');
const OUT = path.join(__dirname, 'shots');
const URL = 'file://' + path.join(__dirname, 'home.html');
const EXE = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const FR = [1.2, 3.5, 5.6, 7.8, 8.4, 10.4, 11.9, 14.6, 17.6];

async function open(browser, w, h, q = '?t=10.4', dpr = 2) {
  const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: dpr });
  page.on('console', m => { if (m.type() === 'error') console.log(`[${w}] console:`, m.text()); });
  page.on('pageerror', e => console.log(`[${w}] pageerror:`, e.message));
  await page.goto(URL + q, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(900);
  const sw = await page.evaluate(() => [document.documentElement.scrollWidth, document.documentElement.clientWidth]);
  console.log(`[${w}] scrollWidth ${sw[0]} vs ${sw[1]}${sw[0] > sw[1] ? '  <-- SIDEWAYS SCROLL' : ''}`);
  return page;
}

async function full(page, file) {
  await page.addStyleTag({ content: '.site-nav{position:relative!important}.hm-switch{display:none!important}' });
  await page.waitForTimeout(300);
  const H = await page.evaluate(() => document.documentElement.scrollHeight), W = page.viewportSize().width, dpr = 2, step = 4000, parts = [];
  for (let y = 0, i = 0; y < H; y += step, i++) {
    const f = path.join(OUT, `_s${i}.png`);
    await page.screenshot({ path: f, fullPage: true, clip: { x: 0, y, width: W, height: Math.min(step, H - y) } });
    parts.push(f);
  }
  if (parts.length === 1) fs.renameSync(parts[0], file);
  else { execSync(`ffmpeg -y -loglevel error ${parts.map(f => '-i ' + f).join(' ')} -filter_complex "vstack=inputs=${parts.length}" ${file}`); parts.forEach(f => fs.unlinkSync(f)); }
}

async function frames(browser, w, h, tag) {
  const page = await open(browser, w, h);
  const el = await page.$('.hm-stage');
  for (const t of FR) {
    await page.evaluate(t => window.__heroAt(t), t);
    await page.waitForTimeout(120);
    await el.screenshot({ path: path.join(OUT, `hero-${tag}-${String(t).replace('.', '_')}.png`) });
  }
  await page.close();
}

async function video(browser, w, h, file, fps = 30) {
  const page = await open(browser, w, h, '?t=0', w > 800 ? 1.5 : 2);
  await page.addStyleTag({ content: '.site-nav,.hm-switch,.hm-pause{display:none!important}' });
  const box = await page.evaluate(() => {
    const s = document.querySelector('.hm-stage'), st = document.querySelector('.hm-steps'), band = document.querySelector('.hm-band');
    window.scrollTo(0, s.getBoundingClientRect().top + scrollY - 24);
    const a = s.getBoundingClientRect(), b = st.getBoundingClientRect(), c = band.getBoundingClientRect();
    return { x: c.left, y: a.top - 24, width: c.width, height: b.bottom - a.top + 48 };
  });
  const dir = path.join(OUT, '_v'); fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir);
  const T = 19.2, n = Math.round(T * fps);
  for (let i = 0; i < n; i++) {
    await page.evaluate(t => window.__heroAt(t), i / fps);
    await page.screenshot({ path: path.join(dir, `f${String(i).padStart(4, '0')}.png`), clip: box });
  }
  execSync(`ffmpeg -y -loglevel error -framerate ${fps} -i ${dir}/f%04d.png -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -c:v libx264 -pix_fmt yuv420p -crf 20 ${file}`);
  fs.rmSync(dir, { recursive: true, force: true });
  await page.close();
}

(async () => {
  const mode = process.argv[2] || 'all';
  const browser = await chromium.launch({ executablePath: EXE });
  if (mode === 'all' || mode === 'pages') {
    for (const [w, h, tag] of [[1440, 900, 'd'], [390, 844, 'm']]) {
      const page = await open(browser, w, h);
      await page.screenshot({ path: path.join(OUT, `home-${tag}-fold.png`) });
      await full(page, path.join(OUT, `home-${tag}-full.png`));
      await page.close();
    }
  }
  if (mode === 'all' || mode === 'frames') { await frames(browser, 1440, 900, 'd'); await frames(browser, 390, 844, 'm'); }
  if (mode === 'video') { await video(browser, 1440, 1000, path.join(OUT, 'hero-loop.mp4')); await video(browser, 390, 844, path.join(OUT, 'hero-loop-390.mp4')); }
  await browser.close();
})();
