// Screenshots each section of pages.html to ../hi/kit2-<id>.png (1440 wide, 2x).
// Tall sections are shot one viewport at a time (Chromium blanks single captures over 16k px) and stitched by stitch.py.
const { chromium } = require('/home/claude/e2e/node_modules/playwright');
const path = require('path'), fs = require('fs'), { execFileSync } = require('child_process');
const TMP = process.env.KIT2_TMP || path.join(__dirname, '_tmp');
(async () => {
  fs.mkdirSync(TMP, { recursive: true });
  const ids = process.argv.slice(2).length ? process.argv.slice(2) : ['o1', 'o2', 'o3', 'o4', 'cmp', 'rec'];
  const VH = 1000;
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: 1440, height: VH }, deviceScaleFactor: 2 });
  p.on('pageerror', e => console.log('pageerror', e.message));
  await p.goto('file://' + path.join(__dirname, 'pages.html'), { waitUntil: 'networkidle' });
  await p.evaluate(async () => { await document.fonts.ready; const h = document.body.scrollHeight; for (let y = 0; y < h; y += 700) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 40)); } window.scrollTo(0, 0); });
  await p.waitForTimeout(800);
  for (const id of ids) {
    const box = await p.evaluate(id => { const r = document.getElementById(id).getBoundingClientRect(); return { x: r.left, y: r.top + scrollY, w: r.width, h: r.height }; }, id);
    const parts = [];
    for (let y = 0, k = 0; y < box.h; y += VH, k++) {
      const top = box.y + y;
      await p.evaluate(t => window.scrollTo(0, t), top);
      await p.evaluate(() => window.GlassV3 && GlassV3.refresh());
      await p.waitForTimeout(450);
      const sy = await p.evaluate(() => scrollY);
      const f = path.join(TMP, `${id}-${k}.png`);
      await p.screenshot({ path: f, clip: { x: box.x, y: top - sy, width: box.w, height: Math.min(VH - (top - sy), box.h - y) } });
      parts.push(f);
    }
    execFileSync('python3', ['-I', path.join(__dirname, 'stitch.py'), path.join(__dirname, '..', 'hi', `kit2-${id}.png`), ...parts]);
    console.log('shot', id, parts.length, 'parts');
  }
  await b.close();
})();
