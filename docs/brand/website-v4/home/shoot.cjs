// Team H, round 5: screenshots and the hero MP4.
// node shoot.cjs            fold + full page at 1512x789 and 390x844 (2x), after the section loops have run; hero frames
// node shoot.cjs frames     hero frames only
// node shoot.cjs loops      checks the section loops keep their height while running (the round 4 collapse bug)
// node shoot.cjs video      hero loop as shots/hero-loop.mp4 (1512 stage, 30 fps) and hero-loop-390.mp4
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs'), { execSync } = require('child_process');
const OUT = path.join(__dirname, 'shots');
const URL = 'file://' + path.join(__dirname, 'home.html');
const FR = [1.4, 3.4, 5.4, 6.4, 8.2, 9.4, 10.3, 12.7, 13.4, 15.2, 16.2, 18.4, 20.8, 24.2, 27.4];
const VPS = [[1512, 789, 'd'], [390, 844, 'm']];
fs.mkdirSync(OUT, { recursive: true });

async function open(browser, w, h, q = '', dpr = 2) {
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

// scroll each section loop into view, let it run, and compare its height with the height before it started
async function loops(page, tag) {
  const n = await page.evaluate(() => document.querySelectorAll('.hm-img').length);
  for (let i = 0; i < n; i++) {
    const before = await page.evaluate(i => { const el = document.querySelectorAll('.hm-img')[i]; el.scrollIntoView({ block: 'center' }); return el.getBoundingClientRect().height; }, i);
    await page.waitForTimeout(3500);
    const after = await page.evaluate(i => { const el = document.querySelectorAll('.hm-img')[i]; return [el.getBoundingClientRect().height, el.classList.contains('is-running'), getComputedStyle(el).display]; }, i);
    console.log(`[${tag}] loop ${i}: height ${before.toFixed(0)} -> ${after[0].toFixed(0)}, running ${after[1]}, display ${after[2]}${Math.abs(before - after[0]) > 2 ? '  <-- COLLAPSED' : ''}`);
    await page.screenshot({ path: path.join(OUT, `loop-${tag}-${i}.png`) });
  }
}

async function full(page, file) {
  await page.addStyleTag({ content: '.site-nav{position:relative!important}.hm-switch{display:none!important}' });
  // every loop running (they run while in view; a full-page shot shows them all at once)
  await page.evaluate(() => { window.scrollTo(0, 0); document.querySelectorAll('.hm-img').forEach(e => e.classList.add('is-running')); });
  await page.waitForTimeout(3600);
  const H = await page.evaluate(() => document.documentElement.scrollHeight), W = page.viewportSize().width, step = 4000, parts = [];
  for (let y = 0, i = 0; y < H; y += step, i++) {
    const f = path.join(OUT, `_s${i}.png`);
    await page.screenshot({ path: f, fullPage: true, clip: { x: 0, y, width: W, height: Math.min(step, H - y) } });
    parts.push(f);
  }
  if (parts.length === 1) fs.renameSync(parts[0], file);
  else { execSync(`ffmpeg -y -loglevel error ${parts.map(f => '-i ' + f).join(' ')} -filter_complex "vstack=inputs=${parts.length}" ${file}`); parts.forEach(f => fs.unlinkSync(f)); }
}

async function frames(browser, w, h, tag) {
  const page = await open(browser, w, h, '?t=0');
  await page.addStyleTag({ content: '.site-nav,.hm-switch{display:none!important}' });
  const el = await page.$('.hm-stage');
  for (const t of FR) {
    await page.evaluate(t => window.__heroAt(t), t);
    await page.waitForTimeout(120);
    await el.screenshot({ path: path.join(OUT, `hero-${tag}-${String(t).replace('.', '_')}.png`) });
  }
  await page.close();
}

async function video(browser, w, h, file, fps = 30) {
  const page = await open(browser, w, h, '?t=0', w > 800 ? 1.25 : 2);
  await page.addStyleTag({ content: '.site-nav,.hm-switch,.hm-pause{display:none!important}' });
  const box = await page.evaluate(() => {
    const s = document.querySelector('.hm-stage'), st = document.querySelector('.hm-steps');
    window.scrollTo(0, s.getBoundingClientRect().top + scrollY - 24);
    const a = s.getBoundingClientRect(), b = st.getBoundingClientRect();
    const x = Math.max(0, a.left - 16);
    return { x, y: Math.max(0, a.top - 16), width: Math.min(innerWidth - x, a.width + 32), height: b.bottom - a.top + 40 };
  });
  const dir = path.join(OUT, '_v'); fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir);
  const T = await page.evaluate(() => window.__heroT), n = Math.round(T * fps);
  for (let i = 0; i < n; i++) {
    await page.evaluate(t => window.__heroAt(t), i / fps);
    await page.screenshot({ path: path.join(dir, `f${String(i).padStart(4, '0')}.png`), clip: box });
  }
  execSync(`ffmpeg -y -loglevel error -framerate ${fps} -i ${dir}/f%04d.png -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -c:v libx264 -pix_fmt yuv420p -crf 21 ${file}`);
  fs.rmSync(dir, { recursive: true, force: true });
  await page.close();
}

(async () => {
  const mode = process.argv[2] || 'all';
  const browser = await chromium.launch();
  if (mode === 'all' || mode === 'pages' || mode === 'loops') {
    for (const [w, h, tag] of VPS) {
      const page = await open(browser, w, h);
      if (mode !== 'loops') {
        await page.waitForTimeout(4000); // the hero has been running a few seconds
        await page.screenshot({ path: path.join(OUT, `home-${tag}-fold.png`) });
      }
      await loops(page, tag);
      if (mode !== 'loops') await full(page, path.join(OUT, `home-${tag}-full.png`));
      await page.close();
    }
  }
  if (mode === 'all' || mode === 'frames') { await frames(browser, 1512, 789, 'd'); await frames(browser, 390, 844, 'm'); }
  if (mode === 'video' || mode === 'video-d') await video(browser, 1512, 1000, path.join(OUT, 'hero-loop.mp4'));
  if (mode === 'video' || mode === 'video-m') await video(browser, 390, 844, path.join(OUT, 'hero-loop-390.mp4'));
  await browser.close();
})();
