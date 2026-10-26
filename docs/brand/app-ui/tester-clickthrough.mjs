// Clicks the pulsing control on every step of every scenario in tester-flow.html (or Next when a step has none).
// Fails loudly if a step shows no screen, the hot control is missing, or a click doesn't advance.
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { chromium } = require('/home/claude/e2e/node_modules/playwright');
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
const errs = []; p.on('pageerror', e => errs.push(e.message));
await p.goto('file://' + process.cwd() + '/tester-flow.html', { waitUntil: 'networkidle' });
const flows = await p.evaluate(() => window.TESTER_FLOWS);
let problems = 0;
for (const [id, f] of Object.entries(flows)) {
  await p.click(`[data-f="${id}"]`);
  for (let i = 0; i < f.steps.length; i++) {
    const st = f.steps[i];
    const vis = await p.$eval(`[data-screen="${st.screen}"]`, e => !e.hidden).catch(() => false);
    const count = await p.textContent('[data-flow-count]');
    if (!vis || !count.startsWith(String(i + 1) + ' ')) { console.log('PROBLEM', id, i, st.label, vis, count); problems++; }
    if (i === f.steps.length - 1) break;
    const hot = await p.$(`[data-screen="${st.screen}"] .is-hot`);
    if (st.hot && !hot) { console.log('NO HOT', id, i, st.label, st.hot); problems++; }
    if (hot) { await hot.click({ force: true }); } else { await p.click('[data-flow-next]'); }
    await p.waitForTimeout(60);
  }
  console.log('ok', id, f.steps.length);
}
console.log('problems', problems, 'errors', errs);
await b.close();
