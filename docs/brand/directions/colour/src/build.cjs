// Builds ../pages.html (self-contained): node src/build.cjs
const fs = require('fs'), path = require('path');
const S = __dirname, OUT = path.join(S, '..', 'pages.html');
const CSS = fs.readFileSync(path.join(S, 'pages.css'), 'utf8');
const GLASS = fs.readFileSync(path.join(S, 'glass-v3.js'), 'utf8');

/* ---------- small pieces ---------- */
const IC = {
  home: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M2.5 7.2 8 2.5l5.5 4.7V13a.5.5 0 0 1-.5.5H9.5V10h-3v3.5H3a.5.5 0 0 1-.5-.5z"/></svg>',
  sites: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4"><circle cx="8" cy="8" r="5.8"/><path d="M2.2 8h11.6M8 2.2c2 1.8 2 9.8 0 11.6M8 2.2c-2 1.8-2 9.8 0 11.6"/></svg>',
  tests: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4"><rect x="2" y="3" width="12" height="10" rx="2"/><path d="M7 6.2v3.6L10 8z" fill="currentColor" stroke="none"/></svg>',
  set: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4"><circle cx="8" cy="8" r="2.2"/><path d="M8 1.8v2M8 12.2v2M1.8 8h2M12.2 8h2M3.6 3.6l1.4 1.4M11 11l1.4 1.4M3.6 12.4 5 11M11 5l1.4-1.4"/></svg>',
};
const ex = '<span class="ex">Example</span>';
const loop = n => `<span class="loop">${['a', 'b', 'c'].map((c, i) => `<i class="${i < n ? c : ''}"></i>`).join('')}</span>`;
const cnt = (k, n, lg) => `<span class="cnt${lg ? ' lg' : ''}">${Array.from({ length: n }, (_, i) => `<i class="${i < k ? 'f' : ''}"></i>`).join('')}</span>`;
const strip = (len, marks, na) => `<div class="strip${na ? ' na' : ''}" style="width:${Math.round(len / 482 * 100)}%">${(marks || []).map(m => `<b style="left:${(m / len * 100).toFixed(1)}%"></b>`).join('')}</div>`;
const pause = '<svg width="12" height="12" viewBox="0 0 12 12"><rect x="2" y="1" width="3" height="10" rx="1" fill="#fff"/><rect x="7" y="1" width="3" height="10" rx="1" fill="#fff"/></svg>';

const phone = (w = 200) => `<div class="ph" style="width:${w}px"><div class="t">Pocket</div><div class="bl"><span>Balance</span><b>£1,240.50</b></div><div class="ac"><span>Send</span><span>Request</span><span>More</span></div><div class="rw"><i></i><span>Coffee Lab</span><b>−£4.20</b></div><div class="rw"><i></i><span>Salary</span><b>+£2,100</b></div><div class="rw"><i></i><span>Bookshop</span><b>−£12.80</b></div><div class="rw"><i></i><span>Sam Okafor</span><b>−£20.00</b></div><div class="tabbar"><b>Home</b><span>Payments</span><span>More</span></div></div>`;
const mph = () => `<div class="mph">Pocket<b>£1,240.50</b><u><i></i><i></i><i></i></u></div>`;
const mwebOnb = (big) => `<div class="mweb${big ? ' big' : ''}">Pocket<b>Set up Pocket in two steps</b>Add your name, then link a card.<br><span class="bt">Continue</span></div>`;
const mwebChk = (big) => `<div class="mweb${big ? ' big' : ''}">Checkout<b>Pay £24.00</b>Card ending 4421 · Deliver to 14 Ash Road<br><span class="bt">Pay now</span></div>`;
const mwebKes = () => `<div class="mweb">Kestrel Studio<b>Product design for small teams</b>Work · About · Contact<br><span class="bt">See the work</span></div>`;

function sidebar(active, plan = 'Solo plan', usage = [9, 10], recent = true) {
  const nv = (k, t, c) => `<div class="nv${active === k ? ' on' : ''}">${IC[k]}${t}${c ? `<span class="c">${c}</span>` : ''}</div>`;
  return `<aside class="sb"><div class="logo">Aero</div>
    <div class="studio"><span class="k">K</span><div><b>Kestrel Studio</b><small>${plan}</small></div><span class="chev">⌄</span></div>
    ${nv('home', 'Home')}${nv('sites', 'Sites', recent ? '4' : '')}${nv('tests', 'Tests', recent ? '3' : '')}
    ${recent ? `<div class="sg">Recent tests</div>
    <div class="si${active === 'pocket' ? ' on' : ''}">Pocket<span class="nw"></span></div>
    <div class="si">Onboarding v2<span class="c">3</span></div>
    <div class="si">Checkout<span class="c">0</span></div>` : ''}
    <div class="usage"><b>${usage[0]} of ${usage[1]}</b> test sessions kept<div class="meter"><i style="width:${usage[0] / usage[1] * 100}%"></i></div>${plan === 'Free plan' ? 'Free sites stay live 7 days. <a href="#">Plans from $3</a>' : '<a href="#">Plan and billing</a>'}</div>
  </aside>`;
}
const rail = () => `<aside class="rl"><div class="lg">Aero</div><div class="ri">${IC.home}</div><div class="ri">${IC.sites}</div><div class="ri on">${IC.tests}</div><div class="ri" style="margin-top:auto">${IC.set}</div></aside>`;
const lap = (url, inner, extra = '') => `<div class="lap" ${extra}><div class="lap-bar"><div class="d"><i></i><i></i><i></i></div><div class="u"><span>${url}</span></div><div style="width:46px"></div></div>${inner}</div>`;
const btn = (t, kind = 'primary', cls = '') => `<a class="btn ${cls}" data-glass-v3="${kind}" data-fill="${kind === 'primary' ? '#16151A' : '#FFFFFF'}">${t}</a>`;

/* ---------- p1 home ---------- */
const p1 = `
<section class="xp" id="p1"><h2>Home</h2>
<p class="idea">The nav stays neutral; colour lives in the canvas. “What’s new” is split by step, so the colour tells you what kind of news it is before you read it. Each test carries a loop meter: how far it has got through Publish, Test, Review.</p>
<div class="frame">
${lap('app.aeroapp.ai', `<div class="app">${sidebar('home')}
  <div class="main">
    <div class="top"><div class="crumb"><b>Home</b></div><div class="top-r">${ex}<span class="tb">Search</span>${btn('Publish')}</div></div>
    <div class="pg">
      <div style="display:flex;justify-content:space-between;align-items:flex-end"><div><div class="h1">What’s new</div><p class="muted" style="margin-top:4px">Since you were last here, Tuesday at 16:40.</p></div>
        <div style="display:flex;gap:16px;font-size:12.5px;color:var(--ink2)"><span class="stepword pub"><i></i>Publish</span><span class="stepword test"><i></i>Test</span><span class="stepword rev"><i></i>Review</span></div></div>
      <div class="feed">
        <div class="fcol pub"><div class="hd"><span class="stepword pub"><i></i>Publish</span><span class="mono muted">2</span></div>
          <div class="fit"><b>Onboarding v2 is live as v8</b><span class="mono">2h</span><small>onboard.aeroapp.ai · uploaded zip</small></div>
          <div class="fit"><b>Checkout published from Claude</b><span class="mono">Yesterday</span><small>checkout.aeroapp.ai · v1 · not tested yet</small></div></div>
        <div class="fcol test"><div class="hd"><span class="stepword test"><i></i>Test</span><span class="mono muted">2</span></div>
          <div class="fit"><b>Tester F finished Pocket</b><span class="mono">20m</span><small>3 min 51 s · transcript arriving</small></div>
          <div class="fit"><b>Checkout link is ready to share</b><span class="mono">Yesterday</span><small>No sessions yet. Send it to 3 to 5 people.</small></div></div>
        <div class="fcol rev"><div class="hd"><span class="stepword rev"><i></i>Review</span><span class="mono muted">2</span></div>
          <div class="fit"><b>3 new sessions on Pocket</b><span class="mono">Today</span><small>Testers C, E and F · 7 friction points</small></div>
          <div class="fit"><b>Pocket review updated</b><span class="mono">1h</span><small>Based on 5 of 6 sessions · 3 things to fix</small></div></div>
      </div>
      <div class="sech"><span class="h3">Tests</span><span class="lnk" style="font-size:13px">All tests</span></div>
      <div class="trow" style="border-top:0;padding-top:0;color:var(--ink3);font-size:12px"><span></span><span>Test</span><span>Where it is</span><span>Latest</span><span class="r">Sessions</span></div>
      <div class="trow"><div class="thumb rev">${mph()}</div><div><b>Pocket</b><small>pocket.aeroapp.ai · Figma prototype</small></div><div>${loop(3)}<div style="font-size:12px;color:var(--mint-d);margin-top:5px;font-weight:500">Review ready</div></div><div><span class="st new"><i></i>3 new sessions</span><div class="muted" style="font-size:12.5px;margin-top:2px">“Is it under More?” Tester B, 03:08</div></div><div class="r"><b style="font-size:15px;color:var(--ink)">6</b>1 processing</div></div>
      <div class="trow"><div class="thumb rev">${mwebOnb()}</div><div><b>Onboarding v2</b><small>onboard.aeroapp.ai · HTML</small></div><div>${loop(3)}<div style="font-size:12px;color:var(--mint-d);margin-top:5px;font-weight:500">Reviewed</div></div><div><span class="st"><i></i>New version, not tested yet</span><div class="muted" style="font-size:12.5px;margin-top:2px">v8 published 2h ago</div></div><div class="r"><b style="font-size:15px;color:var(--ink)">3</b>on v7</div></div>
      <div class="trow"><div class="thumb test">${mwebChk()}</div><div><b>Checkout</b><small>checkout.aeroapp.ai · from Claude</small></div><div>${loop(2)}<div style="font-size:12px;color:var(--pink-d);margin-top:5px;font-weight:500">Link shared</div></div><div><span class="st"><i></i>Waiting for testers</span><div class="muted" style="font-size:12.5px;margin-top:2px">Link copied yesterday</div></div><div class="r"><b style="font-size:15px;color:var(--ink)">0</b>none yet</div></div>
      <div class="sech" style="margin-top:28px"><span class="h3">Sites</span><span class="lnk" style="font-size:13px">All sites</span></div>
      <table class="tbl"><thead><tr><th>Address</th><th>From</th><th>Version</th><th>Last published</th><th>Status</th><th></th></tr></thead><tbody>
        <tr><td><b style="font-weight:600">kestrel.aeroapp.ai</b></td><td>HTML</td><td><span class="ver">v12</span></td><td>3 Oct</td><td><span class="st live"><i></i>Live</span></td><td style="text-align:right"><span class="tb">Test this site</span></td></tr>
        <tr><td><b style="font-weight:600">onboard.aeroapp.ai</b></td><td>HTML</td><td><span class="ver">v8</span></td><td>Today, 14:10</td><td><span class="st live"><i></i>Live</span></td><td style="text-align:right"><span class="tb ghost">Open test</span></td></tr>
        <tr><td><b style="font-weight:600">checkout.aeroapp.ai</b></td><td>Claude</td><td><span class="ver">v1</span></td><td>Yesterday</td><td><span class="st live"><i></i>Live</span></td><td style="text-align:right"><span class="tb ghost">Open test</span></td></tr>
        <tr><td><b style="font-weight:600">pocket.aeroapp.ai</b></td><td>Figma</td><td><span class="ver">link</span></td><td>12 Oct</td><td><span class="st live"><i></i>Live</span></td><td style="text-align:right"><span class="tb ghost">Open test</span></td></tr>
      </tbody></table>
    </div>
  </div></div>`)}
<div style="display:grid;grid-template-columns:300px 1000px;gap:60px;margin-top:40px;align-items:start">
  <div><div class="sublabel"><b>First run</b></div><p style="font-size:15px;color:var(--ink2);line-height:1.55">The same page with nothing in it. Publish is the only step in colour; Test and Review wait in grey and say what they will hold. The three ways in are drawn as the inputs themselves (a pasted link, a dropped zip, a prompt), not as icons.</p></div>
  ${lap('app.aeroapp.ai', `<div class="app" style="grid-template-columns:200px minmax(0,1fr)">${sidebar('home', 'Free plan', [0, 3], false)}
    <div class="main"><div class="top"><div class="crumb"><b>Home</b></div><div class="top-r">${ex}</div></div>
      <div class="band pub" style="padding:24px 26px 24px"><span class="stepword pub"><i></i>Publish</span>
        <div class="h1" style="margin:10px 0 4px">Put your first prototype online</div><p class="muted" style="margin-bottom:16px;color:var(--ink2)">Any of these gives you a link at name.aeroapp.ai in seconds to a minute.</p>
        <div class="ways">
          <div class="way"><b>Paste a Figma link</b><div class="in">figma.com/proto/…/Pocket<em>Paste</em></div><p>Your prototype, as it plays in Figma.</p></div>
          <div class="way"><b>Drop HTML or a zip</b><div class="drop"><span class="file">pocket-v2.zip</span>or choose a file</div><p>Versions kept, roll back any time.</p></div>
          <div class="way"><b>One prompt in Claude or ChatGPT</b><div class="pr"><span>Built with your AI tool</span>Put this online with Aero.</div><p>Connect once, then ask in the chat.</p></div>
        </div></div>
      <div style="padding:6px 26px 22px">
        <div class="trow" style="grid-template-columns:110px 1fr;border-top:0"><span class="stepword" style="color:var(--ink3)"><i style="background:#E3E1E6"></i>Test</span><span class="muted">Share one link. People use it with screen and voice, no account needed.</span></div>
        <div class="trow" style="grid-template-columns:110px 1fr"><span class="stepword" style="color:var(--ink3)"><i style="background:#E3E1E6"></i>Review</span><span class="muted">A transcript about a minute after each session, then a summary and friction points in their own words.</span></div>
      </div>
    </div></div>`)}
</div>
</div></section>`;

/* ---------- p2 sessions ---------- */
const testHeader = (activeTab) => `
  <div class="band rev"><div class="shead"><div class="thumb rev">${mph()}</div>
    <div><div style="display:flex;align-items:center;gap:12px"><div class="h1">Pocket</div>${loop(3)}</div>
      <div class="facts"><span>pocket.aeroapp.ai</span><span>Figma prototype</span><span>2 tasks</span><span class="st live"><i></i>Link open</span></div></div>
    <div style="display:flex;gap:10px">${btn('Copy test link', 'secondary')}${activeTab === 'Sessions' ? btn('Review across sessions') : ''}</div></div>
    <div class="tabs">${['Setup', 'Share', 'Sessions', 'Review'].map(t => `<span class="${t === activeTab ? 'on' : ''}">${t}${t === 'Sessions' ? ' <span class="c">6</span>' : ''}</span>`).join('')}</div></div>`;

const srows = [
  [1, 'Tester A', 'Laptop · Chrome', 400, [140, 210], 'Reviewed', '', '“Okay, so this is a bank app. I’ll start on the home screen.”', 2],
  [2, 'Tester B', 'Laptop · Chrome', 432, [161, 182, 188], 'New', 'new', '“Right. Find my cards. I’d guess they’re on the home screen.”', 3, true],
  [3, 'Tester C', 'Laptop · Edge', 295, [195], 'New', 'new', '“Sending twenty pounds to Sam first, then cards.”', 1],
  [4, 'Tester D', 'Laptop · Safari', 330, [], 'No audio', 'na', 'Screen recorded without a microphone. No transcript or summary.', '–'],
  [5, 'Tester E', 'Laptop · Chrome', 482, [112, 250, 300], 'New', 'new', '“Where are my cards? I’d expect them up front.”', 3],
  [6, 'Tester F', 'Laptop · Chrome', 231, [], 'Processing', 'proc', '', '–'],
];
const fmt = s => `${String(Math.floor(s / 60)).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}`;
const p2 = `
<section class="xp" id="p2"><h2>Sessions</h2>
<p class="idea">Sessions belong to Review, so the test header turns mint on this tab. One numbered list, oldest first, numbers that never change. Length is drawn to scale with a tick for each friction point; the row you are on is in the selection blue. Arrow keys move, the preview updates beside it.</p>
<div class="frame">
${lap('app.aeroapp.ai/tests/pocket/sessions', `<div class="app">${sidebar('pocket')}
  <div class="main"><div class="top"><div class="crumb">Tests <span>/</span> <b>Pocket</b></div><div class="top-r">${ex}</div></div>
  ${testHeader('Sessions')}
  <div style="display:grid;grid-template-columns:minmax(0,1fr) 340px">
    <div class="pg">
      <div class="srow hd"><span>#</span><span>Tester</span><span>Length, friction</span><span>First words</span><span>Status</span><span style="text-align:right">Points</span></div>
      ${srows.map(r => `<div class="srow${r[9] ? ' on' : ''}"><span class="n">${r[0]}</span><div><b>${r[1]}</b><small>${r[2]}</small></div>
        <div>${r[6] === 'proc' ? '<div class="shape" style="width:48%"></div>' : strip(r[3], r[4], r[6] === 'na')}<div class="mono muted" style="margin-top:6px">${fmt(r[3])}</div></div>
        ${r[6] === 'proc' ? '<div><div class="shape" style="width:86%;margin-bottom:6px"></div><div class="muted" style="font-size:12.5px">Transcript arriving, usually about a minute</div></div>' : `<div class="fw"${r[6] === 'na' ? ' style="color:var(--ink3)"' : ''}>${r[7]}</div>`}
        <span class="st ${r[6]}"><i></i>${r[5]}</span><span class="fc">${r[8]}</span></div>`).join('')}
      <div style="display:flex;gap:16px;align-items:center;margin-top:16px;color:var(--ink3);font-size:12.5px"><span><span class="kbd">↑</span> <span class="kbd">↓</span> move</span><span><span class="kbd">Enter</span> open</span><span style="margin-left:auto">5 of 6 have audio. Session 4 is kept, but it can’t be transcribed.</span></div>
    </div>
    <aside class="prev">
      <div style="display:flex;justify-content:space-between;align-items:center"><span class="lbl">Session 2 of 6</span><span class="mono muted">Today, 11:20</span></div>
      <div><div class="h3" style="font-size:18px">Tester B</div><p class="muted" style="font-size:13px">07:12 · Laptop, Chrome · both tasks done</p></div>
      <div class="sum"><div class="lbl" style="color:var(--mint-d);margin-bottom:6px">Summary</div><p>Sent £20 without help. Expected cards on the home screen, tried the balance, then found them under More after about 40 seconds.</p></div>
      <div><div class="lbl" style="margin-bottom:2px">Friction points</div>
        <div class="fp"><span class="mono">03:08</span><b>Cards are hidden under More</b><span class="play"></span><q>I thought my cards would be on the home screen.</q></div>
        <div class="fp"><span class="mono">03:02</span><b>Balance looks tappable</b><span class="play"></span><q>Is the balance a button?</q></div>
        <div class="fp"><span class="mono">02:41</span><b>Send flow has no back label</b><span class="play"></span><q>How do I get back?</q></div></div>
      ${btn('Open session')}
    </aside>
  </div></div></div>`)}
</div></section>`;

/* ---------- p3 session review ---------- */
const words = 'I thought my cards would be on the home screen. Is it under More?'.split(' ');
const nowIdx = 6;
const hl = words.map((w, i) => `<span class="${i < nowIdx ? 'w-past' : i === nowIdx ? 'w-now' : 'w-next'}">${w}</span>`).join(' ');
const p3 = `
<section class="xp" id="p3"><h2>Session review</h2>
<p class="idea">One session, recording first. The prototype sits in the tester’s tab as it was recorded (a tab recording has no cursor). The transcript follows the audio word by word in the selection blue; friction points are mint ticks on the timeline and mint times in the list, and each one jumps to its moment.</p>
<div class="frame">
${lap('app.aeroapp.ai/tests/pocket/sessions/2', `<div class="app rail">${rail()}
  <div class="main"><div class="top"><div class="crumb">Pocket <span>/</span> Sessions <span>/</span> <b>Session 2 · Tester B</b></div><div class="top-r">${ex}<span class="tb">Previous</span><span class="tb">Next <span class="kbd">J</span></span></div></div>
  <div class="sv">
    <div class="slist"><div class="lbl" style="padding:2px 8px 10px">Pocket · 6 sessions</div>
      ${srows.map(r => `<div class="sli${r[9] ? ' on' : ''}"><span class="n">${r[0]}</span><b>${r[1]}</b><span class="mono">${fmt(r[3])}</span><small>${r[6] === 'proc' ? 'Transcript arriving' : r[6] === 'na' ? 'No audio' : r[5] === 'Reviewed' ? 'Reviewed · ' + r[8] + ' points' : r[8] + (r[8] === 1 ? ' friction point' : ' friction points')}</small></div>`).join('')}
    </div>
    <div class="center">
      <div class="stage"><div class="tabrec"><span class="u">pocket.aeroapp.ai</span><span>Shared tab · screen and voice</span><span style="margin-left:auto" class="mono">Task 1 · Find your cards</span></div>${phone(230)}</div>
      <div class="ctl"><div class="ctl-r"><span class="pbtn">${pause}</span><span class="mono" style="font-size:13px;color:var(--ink)">03:08 <span class="muted">/ 07:12</span></span><span class="muted" style="font-size:13px">Tester B is speaking</span><span style="margin-left:auto" class="tb">1×</span></div>
        <div class="tl">
          <span class="task" style="left:4%">Task 1 · Find your cards</span><span class="task" style="left:52%">Task 2 · Send £20 to Sam</span>
          <div class="trk"><i style="width:43.5%"></i></div>
          <span class="fm" style="left:37.3%"></span><span class="fm" style="left:42.1%"></span><span class="fm" style="left:43.5%"></span><span class="ph2" style="left:43.5%"></span>
        </div></div>
      <div class="trx"><div class="lbl" style="margin:0 0 6px 8px">Transcript</div>
        <p><span class="mono">02:41</span><span>Okay, that worked. How do I get back? There’s no label here.</span></p>
        <p><span class="mono">03:02</span><span>Is the balance a button? Nothing happens.</span></p>
        <p class="on"><span class="mono">03:08</span><span>${hl}</span></p>
        <p><span class="mono">03:20</span><span>Oh, there they are. I wouldn’t have looked there.</span></p>
        <p><span class="mono">03:41</span><span>Right, sending twenty pounds to Sam now.</span></p>
      </div>
    </div>
    <div class="rpanel">
      <div class="sum"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px"><span class="lbl" style="color:var(--mint-d)">Summary</span><span class="mono" style="color:var(--mint-d)">Transcribed and summarised</span></div>
        <p>Sent £20 to Sam without help. Expected cards on the home screen, tried the balance first, then found them under More after about 40 seconds. Said the Send screen felt quick.</p></div>
      <div><div class="lbl" style="margin-bottom:2px">Friction points <span class="muted" style="font-weight:500">· 3</span></div>
        <div class="fp"><span class="mono">02:41</span><b>Send flow has no back label</b><span class="play"></span><q>How do I get back? There’s no label here.</q></div>
        <div class="fp"><span class="mono">03:02</span><b>Balance looks tappable</b><span class="play"></span><q>Is the balance a button? Nothing happens.</q></div>
        <div class="fp on"><span class="mono">03:08</span><b>Cards are hidden under More</b><span class="play"></span><q>I thought my cards would be on the home screen. Is it under More?</q></div></div>
      <div><div class="lbl" style="margin-bottom:6px">Top priorities</div>
        <div class="pri"><span class="n">1</span><span>Show cards on the home screen, not under More.</span></div>
        <div class="pri"><span class="n">2</span><span>Label the back button in Send.</span></div>
        <div class="pri"><span class="n">3</span><span>Make the balance read as text, or let it open history.</span></div></div>
      <div><div class="lbl" style="margin-bottom:2px">Tasks</div>
        <div class="th" style="grid-template-columns:1fr auto"><b>1 · Find your cards</b><span class="mono muted">00:20 to 03:24</span><small>Done, after about 40 seconds under More.</small></div>
        <div class="th" style="grid-template-columns:1fr auto;border-bottom:1px solid var(--line)"><b>2 · Send £20 to Sam</b><span class="mono muted">03:40 to 06:30</span><small>Done without help.</small></div></div>
    </div>
  </div></div></div>`)}
</div></section>`;

/* ---------- p4 publish from a prompt ---------- */
const p4 = `
<section class="xp" id="p4"><h2>Publish from a prompt</h2>
<p class="idea">Publish is sunflower. The connector flow is one page that fills in from top to bottom: connect once, copy the prompt, wait for the chat, published. Claude stays outside the window, in its own colours, so it never reads as part of Aero.</p>
<div class="frame" style="display:grid;grid-template-columns:1010px 320px;gap:30px;align-items:start">
${lap('app.aeroapp.ai/publish', `<div class="app">${sidebar('sites')}
  <div class="main"><div class="top"><div class="crumb">Sites <span>/</span> <b>Publish</b></div><div class="top-r">${ex}</div></div>
  <div class="band pub" style="padding-bottom:26px"><div style="display:flex;justify-content:space-between;align-items:center"><span class="stepword pub"><i></i>Publish</span><div class="seg"><span>Figma link</span><span>HTML or zip</span><span class="on">One prompt</span></div></div>
    <div class="h1" style="margin:14px 0 4px">Publish from Claude or ChatGPT</div><p style="color:var(--ink2)">Built with your AI tool? Ask it to put the page online. It appears here when it’s live.</p>
    <div class="vs" style="margin-top:16px">
      <div class="vst done"><span class="n">1</span><b>Connect Aero once</b><span class="ok">Done</span><p>Connected to Claude on 12 Oct. You won’t need this step again.</p></div>
      <div class="vst done"><span class="n">2</span><b>Copy the prompt</b><span class="ok">Copied</span><p>Paste it into the chat where you made the page.</p>
        <div class="prompt"><span>Put this page online with Aero, name it checkout, and set up a test with one task: pay for your order.</span><span class="tb">Copy</span></div></div>
      <div class="vst done"><span class="n">3</span><b>Waiting for the chat</b><span class="ok">14:02</span><p>Claude published it 40 seconds after you sent the prompt.</p></div>
      <div class="vst" style="padding-bottom:0"><span class="n" style="color:var(--ink)">4</span><div style="grid-column:2/4"><b>Published</b>
        <div class="result" style="margin-top:12px;display:grid;grid-template-columns:150px 1fr;gap:20px;align-items:center">
          <div class="thumb pub" style="height:96px">${mwebChk()}</div>
          <div><div class="addr">checkout.aeroapp.ai <span class="ver">v1</span></div>
            <div style="display:flex;gap:14px;align-items:center;margin:8px 0 14px"><span class="livetag">Live</span><span class="muted" style="font-size:13px">Published by Claude · a test with 1 task is ready</span></div>
            <div style="display:flex;gap:10px">${btn('Share the test')}${btn('Open site', 'secondary')}</div></div>
        </div></div></div>
    </div></div>
  </div></div>`)}
<div>
  <div class="outside">Outside Aero · Claude</div>
  <div class="claude"><div class="ch"><i></i>Claude · Checkout page</div>
    <div class="um">Put this page online with Aero, name it checkout, and set up a test with one task: pay for your order.</div>
    <div class="tool"><span>Used Aero: publish site, create test</span><span>⌄</span></div>
    <p>It’s live at checkout.aeroapp.ai. Your test link is ready to share: checkout.aeroapp.ai/t/4mz7</p></div>
  <div class="sublabel" style="margin-top:28px"><b>Before step 3 finishes</b></div>
  <div class="card" style="padding:16px 18px;background:var(--g-pub)">
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px"><span class="wait"><i></i><i></i><i></i></span><b style="font-weight:600">Waiting for the chat</b></div>
    <p style="font-size:13px;color:var(--ink2)">Send the prompt in Claude. Keep this page open: it updates by itself when the site is live, usually within a minute.</p>
    <p style="font-size:12.5px;color:var(--ink3);margin-top:10px">Nothing after 5 minutes? <span class="lnk">Check the connection</span></p></div>
</div>
</div></section>`;

/* ---------- p5 upload ---------- */
const upTop = (inner) => `<div class="app" style="grid-template-columns:minmax(0,1fr)"><div class="main"><div class="top"><div class="crumb">Sites <span>/</span> <b>Onboarding v2</b></div><div class="top-r">${ex}</div></div>${inner}</div></div>`;
const p5 = `
<section class="xp" id="p5"><h2>Upload HTML or a zip</h2>
<p class="idea">Same sunflower canvas, same address bar. Drop, watch it go up, and the published state hands you straight to Test with “Now test it”. The new version sits at the top of the list, with the last one a click away.</p>
<div class="frame">
<div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-bottom:28px">
  <div><div class="sublabel"><b>1</b> Drop</div>${lap('app.aeroapp.ai/sites/onboard', upTop(`<div class="band pub" style="padding:22px 24px 24px"><span class="stepword pub"><i></i>Publish · new version</span>
    <div class="dz" style="margin-top:14px;height:178px;justify-content:center;border-color:var(--sun-d);background:rgba(255,255,255,.75)"><span class="file" style="transform:rotate(-3deg);box-shadow:0 8px 18px -8px rgba(60,40,0,.35);background:#fff;padding:7px 10px">onboarding-v2.zip · 2.4 MB</span><b>Drop to publish v8</b><p>Needs an index.html at the top. Or <span class="lnk">choose a file</span>.</p></div></div>`))}</div>
  <div><div class="sublabel"><b>2</b> Uploading</div>${lap('app.aeroapp.ai/sites/onboard', upTop(`<div class="band pub" style="padding:22px 24px 24px"><span class="stepword pub"><i></i>Publish · new version</span>
    <div class="card" style="margin-top:14px;padding:20px 22px;height:178px"><div style="display:flex;justify-content:space-between;align-items:baseline"><b style="font-size:16px;font-weight:600">Uploading onboarding-v2.zip</b><span class="mono" style="font-size:13px">64%</span></div>
      <div class="bar" style="margin:12px 0 14px"><i style="width:64%"></i></div>
      <div class="flist"><div><span>index.html</span><span>done</span></div><div><span>styles/app.css</span><span>done</span></div><div><span>images/ (9 files)</span><span>5 of 9</span></div><div style="color:var(--ink3)"><span>14 files · 2.4 MB</span><span>about 10 s left</span></div></div></div></div>`))}</div>
</div>
<div class="sublabel"><b>3</b> Published</div>
${lap('app.aeroapp.ai/sites/onboard', `<div class="app">${sidebar('sites')}
  <div class="main"><div class="top"><div class="crumb">Sites <span>/</span> <b>Onboarding v2</b></div><div class="top-r">${ex}${btn('Upload new version', 'secondary')}</div></div>
  <div class="band pub" style="padding-bottom:28px"><span class="stepword pub"><i></i>Publish</span>
    <div class="result" style="margin-top:14px;display:grid;grid-template-columns:240px minmax(0,1fr) 300px;gap:28px;align-items:center">
      <div class="thumb pub" style="height:140px;padding-top:18px">${mwebOnb(true)}</div>
      <div><div class="addr" style="font-size:28px">onboard.aeroapp.ai <span class="ver">v8</span></div>
        <div style="display:flex;gap:14px;align-items:center;margin:10px 0 0"><span class="livetag">Live</span><span class="muted" style="font-size:13.5px">Published today at 14:10 · 14 files · 2.4 MB</span></div></div>
      <div style="border-left:1px solid var(--line);padding-left:26px"><span class="stepword test"><i></i>Next: Test</span><p style="font-size:13.5px;color:var(--ink2);margin:8px 0 12px">Your last 3 sessions were on v7. Test v8 with a new link, or keep the old test.</p>${btn('Now test it')}</div>
    </div></div>
  <div class="pg" style="display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:40px">
    <div><div class="sech"><span class="h3">Versions</span><span class="muted" style="font-size:12.5px">Roll back to any version. The address stays the same.</span></div>
      <div class="vrow" style="border-top:0"><span class="ver" style="justify-self:start">v8</span><span><b style="font-weight:600">onboarding-v2.zip</b> · Today, 14:10</span><span class="st live"><i></i>Live</span><span style="width:90px"></span></div>
      <div class="vrow"><span class="ver" style="justify-self:start">v7</span><span>onboarding-v2.zip · 19 Oct · tested, 3 sessions</span><span class="muted" style="font-size:13px">Previous</span><span class="tb">Roll back</span></div>
      <div class="vrow"><span class="ver" style="justify-self:start">v6</span><span>onboarding.zip · 14 Oct</span><span></span><span class="tb">Roll back</span></div></div>
    <div><div class="lbl" style="margin-bottom:10px">Settings</div><div style="display:flex;flex-direction:column;gap:10px;font-size:13.5px;color:var(--ink2)"><div style="display:flex;justify-content:space-between"><span>Password</span><b style="font-weight:600;color:var(--ink)">Off</b></div><div style="display:flex;justify-content:space-between"><span>Custom domain</span><b style="font-weight:600;color:var(--ink)">Add</b></div><div style="display:flex;justify-content:space-between"><span>Aero badge</span><b style="font-weight:600;color:var(--ink)">Hidden</b></div></div></div>
  </div></div></div>`)}
</div></section>`;

/* ---------- p6 review across sessions ---------- */
const qrow = (q, w) => `<div class="qrow"><span class="play"></span><q>${q}</q><span class="who">${w}</span></div>`;
const p6 = `
<section class="xp" id="p6"><h2>Review across sessions</h2>
<p class="idea">The Review tab, mint. What to fix first leads, as numbers, each with its count as filled squares (4 of 5) and the quotes behind it, every one playable. Themes, what worked and where testers disagreed sit beside it. It says plainly what it is based on.</p>
<div class="frame">
${lap('app.aeroapp.ai/tests/pocket/review', `<div class="app">${sidebar('pocket')}
  <div class="main"><div class="top"><div class="crumb">Tests <span>/</span> <b>Pocket</b></div><div class="top-r">${ex}</div></div>
  ${testHeader('Review')}
  <div style="display:flex;gap:14px;align-items:center;padding:14px 28px;border-bottom:1px solid var(--line);font-size:13px;color:var(--ink2)"><span class="stepword rev"><i></i>Review</span><span>Based on <b style="color:var(--ink)">5 of 6 sessions</b>. Session 4 had no audio. Updated after session 6, today at 13:12.</span><span style="margin-left:auto" class="muted">Transcribed and summarised for each session, then compared.</span></div>
  <div class="pg" style="display:grid;grid-template-columns:minmax(0,1fr) 380px;gap:44px">
    <div><div class="h1" style="font-size:22px;margin-bottom:14px">What to fix first</div>
      <div class="fix"><span class="n">1</span><div><h4>Show cards on the home screen</h4><div class="why">${cnt(4, 5)}<span><b style="color:var(--ink)">4 of 5 testers</b> looked for cards on Home first · Task 1</span></div>
        <div class="qs">${qrow('I thought my cards would be on the home screen. Is it under More?', 'B · 03:08')}${qrow('Where are my cards? I’d expect them up front.', 'E · 01:52')}${qrow('Cards… maybe they’re in settings?', 'A · 02:20')}</div></div></div>
      <div class="fix"><span class="n">2</span><div><h4>Label the back button in Send</h4><div class="why">${cnt(3, 5)}<span><b style="color:var(--ink)">3 of 5</b> paused on the Send screen · Task 2</span></div>
        <div class="qs">${qrow('How do I get back? There’s no label here.', 'B · 02:41')}${qrow('Do I swipe? I’m not sure how to get out.', 'C · 03:15')}</div></div></div>
      <div class="fix"><span class="n">3</span><div><h4>Make the balance read as text</h4><div class="why">${cnt(2, 5)}<span><b style="color:var(--ink)">2 of 5</b> tapped it expecting history</span></div>
        <div class="qs">${qrow('Is the balance a button? Nothing happens.', 'B · 03:02')}</div></div></div>
    </div>
    <aside>
      <div class="lbl" style="margin-bottom:4px">Themes</div>
      <div class="th"><b>Cards are hard to find</b>${cnt(4, 5)}<small>Testers expect cards where the balance is.</small></div>
      <div class="th"><b>No way back from Send</b>${cnt(3, 5)}<small>The arrow has no label and swipe does nothing.</small></div>
      <div class="th"><b>“More” hides too much</b>${cnt(3, 5)}<small>Cards, limits and statements all live there.</small></div>
      <div class="lbl" style="margin:22px 0 4px">What worked</div>
      <div class="th"><b>Sending money</b>${cnt(5, 5)}<small>Everyone finished Task 2. <q>That was quick.</q> A · 04:10</small></div>
      <div class="lbl" style="margin:22px 0 4px">Where testers disagreed</div>
      <div class="th" style="border-bottom:1px solid var(--line)"><b>The word “More”</b><span class="mono muted">2 liked · 3 didn’t</span><small><q>More is fine, every app has it.</q> C · 04:02</small></div>
      <div style="display:flex;gap:10px;margin-top:20px">${btn('Download summary', 'secondary')}<span class="tb ghost">Email it</span></div>
    </aside>
  </div></div></div>`)}
</div></section>`;

/* ---------- f1 flow ---------- */
const fr = (url, cls, inner) => `<div class="fr"><div class="tbar"><i></i><i></i><i></i><span>${url}</span></div><div class="bd ${cls}">${inner}</div></div>`;
const bar = n => `<div class="stepbar">${[0, 1, 2, 3, 4, 5, 6].map(i => `<i class="${i <= n ? (i < 3 ? 'a' : i < 5 ? 'b' : 'c') : ''}"></i>`).join('')}</div>`;
const steps = [
  ['Connect once', 'Add Aero to Claude or ChatGPT.', fr('app.aeroapp.ai/publish', 'pub', `<span class="stepword pub" style="font-size:9.5px"><i></i>Publish</span><div class="mini"><b>Connect Aero once</b>Sign in from Claude’s connector settings.</div><div class="mini" style="opacity:.55"><b>Copy the prompt</b></div><div class="mini" style="opacity:.55"><b>Wait for the chat</b></div>`)],
  ['One prompt', 'In the chat where you made it. Outside Aero.', fr('claude.ai', 'claudeb', `<div style="font:600 8.5px/1 var(--fm);letter-spacing:.06em;color:#8A857A">OUTSIDE AERO · CLAUDE</div><div style="background:#E6E2D8;border-radius:8px;padding:6px 7px;font-family:var(--ft);margin-left:14px">Put this page online with Aero and set up a test.</div><div style="border:1px solid rgba(0,0,0,.1);border-radius:6px;padding:4px 6px;font:500 9px/1.2 var(--ft);color:#6E6A60">Used Aero</div><div>It’s live. Your test link is ready.</div>`)],
  ['It’s live', 'Address, version, and the test the prompt set up.', fr('app.aeroapp.ai/sites/checkout', 'pub', `<span class="stepword pub" style="font-size:9.5px"><i></i>Publish</span><div class="mini" style="padding:9px"><b style="font-size:12px">checkout.aeroapp.ai</b><span class="livetag" style="font-size:9.5px">Live</span> <span class="ver" style="font-size:9px;padding:2px 4px">v1</span><div style="margin-top:8px"><span class="mbtn">Share the test</span></div></div>`)],
  ['Link copied', 'You land on Share with the link ready.', fr('app.aeroapp.ai/tests/checkout/share', 'test', `<span class="stepword test" style="font-size:9.5px"><i></i>Test</span><div class="mini" style="padding:9px"><span style="color:var(--ink3);font-size:9px">Test link · copied</span><b style="font-size:11.5px;margin:3px 0 6px">checkout.aeroapp.ai/t/4mz7</b><span class="mbtn w">Open as a tester</span></div><div style="color:var(--ink2)">Send it to 3 to 5 people. No account needed.</div>`)],
  ['Someone takes it', 'On their own computer, screen and voice.', `<div class="fr"><div class="tbar"><i></i><i></i><i></i><span>checkout.aeroapp.ai/t/4mz7</span></div><div class="bd" style="background:#F3F2EF;align-items:center;justify-content:center;text-align:center"><div class="mini" style="padding:10px;width:100%"><b style="font-size:11.5px">Help test this checkout</b><span style="color:var(--ink2)">We’ll record this tab and your voice. Stop any time.</span><div style="margin-top:7px"><span class="mbtn">Allow and start</span></div></div><span style="color:var(--ink3);font-size:9px">Tester’s screen, not your app</span></div></div>`],
  ['Session arrives', 'Transcript about a minute later.', fr('app.aeroapp.ai/tests/checkout/sessions', 'rev', `<span class="stepword rev" style="font-size:9.5px"><i></i>Review</span><div class="mini"><b>1 · Tester A</b><span class="st proc" style="font-size:9.5px"><i></i>Transcript arriving</span><div class="shape" style="margin-top:6px;width:90%;height:6px"></div><div class="shape" style="margin-top:4px;width:60%;height:6px"></div></div>`)],
  ['First session reviewed', 'Summary and friction points, in their words.', fr('app.aeroapp.ai/tests/checkout/sessions/1', 'rev', `<span class="stepword rev" style="font-size:9.5px"><i></i>Review</span><div class="mini"><span class="mono" style="font-size:9px;color:var(--mint-d)">01:46</span><b>Delivery fee shows late</b><q style="color:var(--ink2)">Wait, why is it £27 now?</q></div><div class="mini"><span class="mono" style="font-size:9px;color:var(--mint-d)">02:30</span><b>Card field rejects spaces</b></div>`)],
];
const f1 = `
<section class="xp" id="f1"><h2>The flow: from prompt to first session</h2>
<p class="idea"><b>A colour stepper.</b> Not one page, not a wizard: each step is the normal screen for that job, and the canvas colour tells you which of the three steps you are in (sunflower, then pink, then mint). The bar under every frame fills in the same colours. Example: the Checkout page made in Claude.</p>
<div class="frame flow">
${steps.map((s, i) => `<div class="fs">${s[2]}${bar(i)}<div class="cap"><span class="n">${i + 1}</span><b>${s[0]}</b><small>${s[1]}</small></div></div>`).join('')}
</div></section>`;

/* ---------- m1 marketing kit ---------- */
const mSess = `<div class="mk rev" style="padding:30px"><div class="mkc" style="display:grid;grid-template-columns:auto 1fr;gap:6px 22px;align-items:center">
  <span style="font:600 54px/1 var(--ft);letter-spacing:-.04em;color:var(--sel);grid-row:1/4">2</span>
  <b style="font-size:26px;font-weight:600;letter-spacing:-.02em">Tester B</b>
  <div style="display:flex;gap:14px;align-items:center"><div class="strip" style="width:260px;height:12px;border-radius:5px">${[161, 182, 188].map(m => `<b style="left:${(m / 432 * 100).toFixed(1)}%;height:22px;top:-5px;width:4px"></b>`).join('')}</div><span class="mono" style="font-size:16px">07:12</span></div>
  <span style="font-size:17px;color:var(--ink2)">3 friction points</span></div></div>`;
const mQuote = `<div class="mk rev"><span class="mk-tag" style="color:var(--mint-d)"><i class="i-rev"></i>In their own words</span>
  <div style="font:500 34px/1.22 var(--ft);letter-spacing:-.022em"><q>I thought my cards would be on the home screen. Is it under More?</q></div>
  <div style="display:flex;gap:14px;align-items:center;font-size:17px;color:var(--ink2)"><span class="mono" style="font-size:17px;color:var(--mint-d)">03:08</span>Tester B · Cards are hidden under More</div></div>`;
const mSite = `<div class="mk pub"><div class="mkc" style="display:grid;grid-template-columns:180px 1fr;gap:26px;align-items:center"><div class="thumb pub" style="height:118px;padding-top:14px">${mwebChk(true)}</div>
  <div><div style="font:600 34px/1.1 var(--ft);letter-spacing:-.03em">checkout.aeroapp.ai</div><div style="display:flex;gap:14px;align-items:center;margin-top:14px"><span class="livetag" style="font-size:17px">Live</span><span class="ver" style="font-size:15px;padding:5px 8px">v1</span></div></div></div></div>`;
const mShare = `<div class="mk test"><span class="mk-tag" style="color:var(--pink-d)"><i class="i-test"></i>One link for every tester</span>
  <div class="mkc" style="display:flex;align-items:center;gap:20px"><span style="font:600 30px/1.1 var(--ft);letter-spacing:-.025em;flex:1">checkout.aeroapp.ai/t/4mz7</span>${btn('Copy link', 'primary', 'lg')}</div>
  <span style="font-size:17px;color:var(--ink2)">Screen and voice. No account needed.</span></div>`;
const mTrx = `<div class="mk none"><div class="mkc" style="display:grid;grid-template-columns:80px 1fr;gap:16px;align-items:start">
  <span class="mono" style="font-size:18px;color:var(--sel);padding-top:8px">03:08</span>
  <div style="font:500 30px/1.35 var(--ft);letter-spacing:-.02em">${words.map((w, i) => `<span class="${i < nowIdx ? 'w-past' : i === nowIdx ? 'w-now' : 'w-next'}"${i === nowIdx ? ' style="padding:0 6px;border-radius:7px"' : ''}>${w}</span>`).join(' ')}</div></div>
  <div style="display:flex;align-items:center;gap:14px"><span class="pbtn" style="width:44px;height:44px">${pause}</span><div style="flex:1;height:8px;border-radius:4px;background:rgba(22,21,26,.1);position:relative"><i style="position:absolute;left:0;top:0;bottom:0;width:43.5%;background:var(--ink2);border-radius:4px"></i><i style="position:absolute;left:43.5%;top:-5px;width:18px;height:18px;border-radius:50%;background:var(--sel);transform:translateX(-9px)"></i></div><span class="mono" style="font-size:15px">07:12</span></div></div>`;

const appSess = `<div class="appv" style="padding:6px 14px"><div class="srow on" style="grid-template-columns:22px 1fr 100px 60px;margin:0 -10px"><span class="n" style="font-size:16px">2</span><div><b>Tester B</b><small>Laptop · Chrome</small></div><div>${strip(432, [161, 182, 188])}<div class="mono muted" style="margin-top:5px">07:12</div></div><span class="st new"><i></i>New</span></div></div>`;
const appQuote = `<div class="appv"><div class="fp on" style="border-top:0;padding:2px 0"><span class="mono">03:08</span><b>Cards are hidden under More</b><span class="play"></span><q>I thought my cards would be on the home screen. Is it under More?</q></div></div>`;
const appSite = `<div class="appv"><table class="tbl"><tr><td style="padding:4px 10px 4px 0;border:0"><b style="font-weight:600">checkout.aeroapp.ai</b></td><td style="border:0;padding:4px 10px 4px 0">Claude</td><td style="border:0;padding:4px 10px 4px 0"><span class="ver">v1</span></td><td style="border:0;padding:4px 0">Yesterday</td><td style="border:0;padding:4px 0 4px 10px"><span class="st live"><i></i>Live</span></td></tr></table></div>`;
const appShare = `<div class="appv"><div class="lbl" style="margin-bottom:8px">Test link</div><div style="display:flex;align-items:center;gap:8px"><span style="flex:1;border:1px solid var(--line2);border-radius:9px;padding:8px 10px;font-size:13px">checkout.aeroapp.ai/t/4mz7</span><span class="tb">Copy link</span></div><p class="muted" style="font-size:12px;margin-top:8px">Testers need no account. Sessions have no set length.</p></div>`;
const appTrx = `<div class="appv"><div class="trx" style="padding:0"><p class="on" style="padding:4px 0"><span class="mono">03:08</span><span>${hl}</span></p></div></div>`;

const krow = (name, note, src, app, mk) => `<div class="krow"><div class="kl"><b>${name}</b><small>${note}</small><span class="mono">${src}</span></div><div>${app}</div><div class="arr">→</div><div>${mk}</div></div>`;

const hero = `<div class="hero">
  <div style="display:flex;flex-direction:column;justify-content:center"><div class="logo" style="padding:0 0 34px;font-size:24px">Aero</div>
    <h3>Publish your prototype. Watch people use it.</h3>
    <p>Paste a Figma link, drop an HTML folder, or ask Claude. Share one link. Each session is transcribed and summarised, with the friction points in their own words.</p>
    <div style="display:flex;gap:12px;margin-top:28px">${btn('Start free', 'primary', 'lg')}${btn('See a test', 'secondary', 'lg')}</div>
    <p style="font-size:14px;color:var(--ink3);margin-top:16px">Free to start. Paid plans from $3 a month.</p></div>
  <div style="display:flex;flex-direction:column;gap:14px;justify-content:center">
    <div style="width:610px">${mSite.replace('class="mk pub"', 'class="mk pub" style="padding:22px 26px"')}</div>
    <div style="width:560px;margin-left:190px">${mShare.replace('class="mk test"', 'class="mk test" style="padding:22px 26px;gap:12px"')}</div>
    <div style="width:620px;margin-left:60px">${mQuote.replace('class="mk rev"', 'class="mk rev" style="padding:24px 28px;gap:12px"').replace('font:500 34px/1.22', 'font:500 27px/1.25')}</div>
  </div></div>`;
const scard = (cls, word, inner) => `<div style="background:var(--g-${cls});padding:34px 28px;display:flex;flex-direction:column;gap:22px"><div class="stepword ${cls}" style="font-size:20px"><i style="width:26px;height:12px"></i>${word}</div><div class="mkc" style="padding:24px 24px;min-height:190px">${inner}</div></div>`;
const social = `<div class="social" style="display:flex;flex-direction:column">
  <div style="padding:48px 56px 36px;display:flex;justify-content:space-between;align-items:flex-end"><div style="font:600 54px/1.04 var(--ft);letter-spacing:-.035em">From prompt to<br>first session</div><span style="font:650 30px/1 var(--ft);letter-spacing:-.03em">Aero</span></div>
  <div style="flex:1;display:grid;grid-template-columns:1fr 1fr 1fr">
    ${scard('pub', 'Publish', `<div style="font:600 27px/1.15 var(--ft);letter-spacing:-.025em">checkout<br>.aeroapp.ai</div><div style="display:flex;gap:12px;align-items:center;margin-top:18px"><span class="livetag" style="font-size:17px">Live</span><span class="ver" style="font-size:15px">v1</span></div>`)}
    ${scard('test', 'Test', `<div style="font-size:16px;color:var(--ink3);margin-bottom:6px">Test link</div><div style="font:600 23px/1.2 var(--ft);letter-spacing:-.02em">checkout.aeroapp.ai<br>/t/4mz7</div><div style="margin-top:16px">${btn('Copy link')}</div>`)}
    ${scard('rev', 'Review', `<span class="mono" style="font-size:17px;color:var(--mint-d)">01:46</span><div style="font:500 25px/1.3 var(--ft);letter-spacing:-.02em;margin-top:8px"><q>Wait, why is it £27 now?</q></div><div style="font-size:16px;color:var(--ink2);margin-top:12px">Tester A · delivery fee shows late</div>`)}
  </div></div>`;

const m1 = `
<section class="xp" id="m1"><h2>Marketing kit</h2>
<p class="idea">The same components, bigger and simpler: less metadata, one row instead of six, set on the soft wash of their step. The colour does the explaining on the website, so a component on sunflower already says “publish” before anyone reads it. App version left, marketing version right.</p>
<div class="frame kit">
${krow('Session card', 'Number, tester, length to scale with friction ticks. Drops device and status.', 'from p2, p3', appSess, mSess)}
${krow('Friction point', 'The quote becomes the headline. The time stays, in mint, so it still reads as a moment.', 'from p3, p6', appQuote, mQuote)}
${krow('Published site card', 'Address, Live, version. A real thumbnail of the page, on sunflower.', 'from p1, p4, p5', appSite, mSite)}
${krow('Test link', 'One link, one action, one line of reassurance. On pink.', 'from f1 step 4', appShare, mShare)}
${krow('Transcript line and player', 'The spoken word in selection blue, as it plays back. Never typed out live.', 'from p3', appTrx, mTrx)}
<div style="margin-top:26px"><div class="sublabel"><b>Composed: homepage hero</b> built only from the site card, the test link and the friction point</div>${hero}</div>
<div style="margin-top:34px"><div class="sublabel"><b>Composed: social card, 1200 × 630</b> the three steps as three washes, one component each</div>${social}</div>
</div></section>`;

const html = `<!doctype html>
<html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=1440">
<title>Aero B Colour: app pages</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700&family=Geist+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>${CSS}</style></head><body>
<header class="board-h"><div><h1>B · Colour: the app, screen by screen</h1><p>Each step owns a colour, and the colour lives in the canvas, never in the nav. Blue is not a step: it marks where you are (the row, the playhead, the word being spoken). All names and data are examples.</p></div>
<div class="legend"><span><i class="i-pub"></i>Publish</span><span><i class="i-test"></i>Test</span><span><i class="i-rev"></i>Review</span><span><i style="background:var(--sel)"></i>Selection</span></div></header>
${p1}${p2}${p3}${p4}${p5}${p6}${f1}${m1}
<div style="height:60px"></div>
<script>${GLASS}</script>
</body></html>`;
fs.writeFileSync(OUT, html);
console.log('built', (html.length / 1024).toFixed(0) + 'KB');
