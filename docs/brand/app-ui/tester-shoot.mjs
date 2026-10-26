// node tester-shoot.mjs <page> <width> <out> [full=1] [height=900] [hash]
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { chromium } = require('/home/claude/e2e/node_modules/playwright');
const [, , pg, w = '1440', out, full = '1', h = '900', hash = ''] = process.argv;
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const p = await b.newPage({ viewport: { width: +w, height: +h }, deviceScaleFactor: +w < 500 ? 2 : 1, reducedMotion: 'reduce' });
const errs = [];
p.on('pageerror', e => errs.push(e.message)); p.on('console', m => m.type() === 'error' && !/components\.css|ERR_FILE_NOT_FOUND|glass\/glass-v3/.test(m.text()) && errs.push(m.text()));
await p.goto('file://' + new URL(pg, 'file://' + process.cwd() + '/').pathname + (hash ? '#' + hash : ''), { waitUntil: 'networkidle' });
await p.evaluate(async () => { await document.fonts.ready; window.testerFit && window.testerFit(); });
await p.waitForTimeout(2500);
const sw = await p.evaluate(() => [document.documentElement.scrollWidth, innerWidth, document.documentElement.scrollHeight]);
await p.screenshot({ path: out, fullPage: full === '1' });
console.log(out, 'scrollW/innerW/H', sw.join('/'), errs.length ? 'ERR ' + errs.join(' | ') : '');
await b.close();
