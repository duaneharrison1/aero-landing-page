// C. Story: UI directions stage. Builds ../pages.html (self-contained).
// node src/build.cjs
const fs = require('fs'), path = require('path');
const OUT = path.join(__dirname, '..', 'pages.html');
const logo = fs.readFileSync('/home/claude/research/brand/fullstop-schibsted500/lockup.svg', 'utf8').replace('<svg ', '<svg class="logo" ');
const glass = fs.readFileSync('/home/claude/research/glass-lab/glass-v3.js', 'utf8');
const favsvg = fs.readFileSync('/home/claude/research/brand/fullstop-schibsted500/favicon.svg', 'utf8');
const fav = 'data:image/svg+xml,' + encodeURIComponent(favsvg);

/* ------------------------------------------------------------ example scene */
const SESS = [
  { n: 6, who: 'Tester F', when: 'Sunday 13:15', len: '05:02', st: 'proc' },
  { n: 5, who: 'Tester E', when: 'Sunday 13:02', len: '04:18', st: 'noaudio' },
  { n: 4, who: 'Tester D', when: 'Sunday 12:30', len: '06:21', st: 'ok', q: 'Where do I see what I spent this week?', fr: 2, nw: 1 },
  { n: 3, who: 'Tester C', when: 'Sunday 12:05', len: '04:58', st: 'ok', q: 'Found the cards straight away, but only because I opened More by accident.', fr: 1, nw: 1 },
  { n: 2, who: 'Tester B', when: 'Sunday 11:40', len: '07:12', st: 'ok', q: 'I thought my cards would be on the home screen. Is it under More?', fr: 3, on: 1 },
  { n: 1, who: 'Tester A', when: 'Saturday 16:10', len: '05:40', st: 'ok', q: "Send was easy. I wasn't sure the money had gone.", fr: 1 },
];
const TR = [
  { t: '00:04', task: 'Task 1 · Send £20 to Sam', x: 'Okay, this is Pocket. First thing, send twenty pounds to Sam.' },
  { t: '00:31', x: 'Home screen, balance, recent payments. That all makes sense.' },
  { t: '01:12', x: "Send, Sam, twenty. Easy enough, it's a bit like my bank." },
  { t: '02:41', x: "Right, sent. How do I get back? There's an arrow but it doesn't say where to.", fr: 'Send flow has no back label', c: '3 of 5' },
  { t: '03:02', task: 'Task 2 · Find your cards', x: 'Is the balance a button? I keep wanting to tap it.', fr: 'Balance looks tappable', c: '2 of 5' },
  { t: '03:08', x: 'I thought my cards would be on the home screen. Is it under More?', fr: 'Cards are hidden under More', c: '4 of 5', now: 10 },
  { t: '03:31', x: "Oh, there they are. Under More. I wouldn't have looked there." },
  { t: '04:12', x: "Can I freeze a card from here? Yes, okay, that's clear." },
];

const hlWords = (x, n) => { const w = x.split(' '); return `<span class="w on">${w.slice(0, n - 1).join(' ')} </span><span class="w cur">${w[n - 1]}</span> ${w.slice(n).join(' ')}`; };
/* ------------------------------------------------------------ drawn pieces */
function wave(n, seed, played, cls) {
  let s = seed || 7, h = '';
  const r = () => { s = (s * 9301 + 49297) % 233280; return s / 233280; };
  for (let i = 0; i < n; i++) {
    const env = .35 + .65 * Math.abs(Math.sin(i / n * Math.PI * 3.2 + 1));
    let v = Math.max(.14, Math.min(1, env * (.35 + .75 * r())));
    if (i % 17 === 16) v = .1;
    h += `<i style="height:${Math.round(v * 100)}%"${i < played * n ? ' class="p"' : ''}></i>`;
  }
  return `<div class="wave ${cls || ''}">${h}<b class="ph" style="left:${(played * 100).toFixed(1)}%"></b></div>`;
}
// thumbnails: the real prototype, small (type is signalled by the prototype itself)
const thumbPocket = (w, extra) => `<svg class="thumb ${extra || ''}" width="${w}" viewBox="0 0 60 116" aria-hidden="true"><rect width="60" height="116" rx="10" fill="#1B1A19"/><rect x="2.5" y="2.5" width="55" height="111" rx="8" fill="#FFF8F5"/><rect x="7" y="10" width="16" height="3.5" rx="1.5" fill="#1F1A17"/><circle cx="50" cy="12" r="3.5" fill="#FFE3D9"/><rect x="6" y="18" width="48" height="22" rx="5" fill="#FF7A59"/><rect x="10" y="23" width="10" height="2" rx="1" fill="#fff" opacity=".75"/><rect x="10" y="29" width="25" height="5.5" rx="1.5" fill="#fff"/><g fill="#fff" stroke="#F1E4DE" stroke-width=".8"><rect x="8" y="45" width="8" height="8" rx="2.5"/><rect x="20" y="45" width="8" height="8" rx="2.5"/><rect x="32" y="45" width="8" height="8" rx="2.5"/><rect x="44" y="45" width="8" height="8" rx="2.5"/></g><g><rect x="7" y="61" width="7" height="7" rx="2" fill="#F4ECE8"/><rect x="17" y="63.5" width="20" height="2.5" rx="1" fill="#CFC3BC"/><rect x="44" y="63.5" width="9" height="2.5" rx="1" fill="#1F1A17"/><rect x="7" y="71" width="7" height="7" rx="2" fill="#F4ECE8"/><rect x="17" y="73.5" width="16" height="2.5" rx="1" fill="#CFC3BC"/><rect x="46" y="73.5" width="7" height="2.5" rx="1" fill="#1F1A17"/><rect x="7" y="81" width="7" height="7" rx="2" fill="#F4ECE8"/><rect x="17" y="83.5" width="12" height="2.5" rx="1" fill="#CFC3BC"/><rect x="44" y="83.5" width="9" height="2.5" rx="1" fill="#1F1A17"/></g><rect x="2.5" y="99" width="55" height="14.5" fill="#fff"/><rect x="11" y="103" width="6" height="6" rx="2" fill="#FF7A59"/><rect x="27" y="103" width="6" height="6" rx="2" fill="#EADBD4"/><rect x="43" y="103" width="6" height="6" rx="2" fill="#EADBD4"/></svg>`;
const thumbOnb = (w) => `<svg class="thumb" width="${w}" viewBox="0 0 60 116" aria-hidden="true"><rect width="60" height="116" rx="10" fill="#1B1A19"/><rect x="2.5" y="2.5" width="55" height="111" rx="8" fill="#F6F5FF"/><circle cx="30" cy="40" r="17" fill="#8C88F5"/><circle cx="24" cy="36" r="5" fill="#fff" opacity=".85"/><rect x="11" y="66" width="38" height="4" rx="2" fill="#24215A"/><rect x="15" y="74" width="30" height="2.5" rx="1" fill="#B7B4E8"/><rect x="18" y="79" width="24" height="2.5" rx="1" fill="#B7B4E8"/><rect x="9" y="96" width="42" height="9" rx="4.5" fill="#24215A"/><circle cx="26" cy="89" r="1.5" fill="#24215A"/><circle cx="30" cy="89" r="1.5" fill="#CFCDF2"/><circle cx="34" cy="89" r="1.5" fill="#CFCDF2"/></svg>`;
const thumbCheckout = (w, bare) => `<svg class="thumb" width="${w}" viewBox="0 ${bare ? 11 : 0} 160 ${bare ? 89 : 100}" aria-hidden="true"><rect width="160" height="100" rx="${bare ? 0 : 6}" fill="#fff" stroke="${bare ? 'none' : '#E2DDD2'}"/>${bare ? '' : '<rect x="0.5" y="0.5" width="159" height="10" rx="5.5" fill="#F3F1EC"/><circle cx="7" cy="5.5" r="1.6" fill="#D9D4C8"/><circle cx="12" cy="5.5" r="1.6" fill="#D9D4C8"/><circle cx="17" cy="5.5" r="1.6" fill="#D9D4C8"/>'}<rect x="0.5" y="11" width="159" height="13" fill="#47B58A"/><rect x="8" y="15.5" width="22" height="4" rx="1.5" fill="#fff"/><rect x="8" y="31" width="14" height="14" rx="3" fill="#E6F3EC"/><rect x="26" y="33" width="40" height="3" rx="1" fill="#2B3B33"/><rect x="26" y="39" width="26" height="2.5" rx="1" fill="#B9C6BF"/><rect x="8" y="50" width="14" height="14" rx="3" fill="#E6F3EC"/><rect x="26" y="52" width="34" height="3" rx="1" fill="#2B3B33"/><rect x="26" y="58" width="22" height="2.5" rx="1" fill="#B9C6BF"/><rect x="98" y="31" width="54" height="52" rx="4" fill="#F5F8F6"/><rect x="104" y="37" width="28" height="3" rx="1" fill="#2B3B33"/><rect x="104" y="46" width="42" height="2.5" rx="1" fill="#B9C6BF"/><rect x="104" y="52" width="42" height="2.5" rx="1" fill="#B9C6BF"/><rect x="104" y="70" width="42" height="8" rx="4" fill="#1D2B24"/></svg>`;
const thumbStudio = (w) => `<svg class="thumb" width="${w}" viewBox="0 0 160 100" aria-hidden="true"><rect width="160" height="100" rx="6" fill="#FCFBF7" stroke="#E2DDD2"/><rect x="0.5" y="0.5" width="159" height="10" rx="5.5" fill="#F3F1EC"/><circle cx="7" cy="5.5" r="1.6" fill="#D9D4C8"/><circle cx="12" cy="5.5" r="1.6" fill="#D9D4C8"/><circle cx="17" cy="5.5" r="1.6" fill="#D9D4C8"/><rect x="10" y="22" width="76" height="8" rx="1.5" fill="#1D1D1F"/><rect x="10" y="34" width="58" height="8" rx="1.5" fill="#1D1D1F"/><rect x="10" y="50" width="50" height="2.5" rx="1" fill="#B3ADA1"/><rect x="10" y="56" width="44" height="2.5" rx="1" fill="#B3ADA1"/><rect x="96" y="20" width="54" height="68" rx="3" fill="#C9B79C"/><rect x="10" y="78" width="36" height="9" rx="4.5" fill="#1D1D1F"/></svg>`;

function pocketPhone(id) {
  return `<div class="phone"><div class="scr"><div class="sb"><span>9:41</span><span>&#9679;&#9679;&#9679;</span></div><div class="hd"><b>Pocket</b><span class="pav">TB</span></div><div class="bal"><small>Balance</small><strong>£2,480.15</strong></div><div class="qa"><span><i>&#8593;</i>Send</span><span><i>&#8595;</i>Request</span><span><i>&#8644;</i>Split</span><span><i>&#43;</i>Top up</span></div><div class="rl">RECENT</div><div class="tx"><i></i><span>Sam Okafor</span><em>-£20.00</em></div><div class="tx"><i></i><span>Corner Café</span><em>-£4.60</em></div><div class="tx"><i></i><span>Salary</span><em>+£2,100</em></div><div class="tab"><span class="on"><i></i>Home</span><span><i></i>Payments</span><span><i></i>More</span></div></div></div>`;
}

const ICON = {
  play: '<svg viewBox="0 0 16 16" width="12" height="12"><path d="M4.5 3v10l8-5z" fill="currentColor"/></svg>',
  pause: '<svg viewBox="0 0 16 16" width="12" height="12"><path d="M4.5 3h2.6v10H4.5zM8.9 3h2.6v10H8.9z" fill="currentColor"/></svg>',
  arrow: '<svg viewBox="0 0 16 16" width="13" height="13" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 8h10M9 4l4 4-4 4"/></svg>',
  back: '<svg viewBox="0 0 16 16" width="13" height="13" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M13 8H3M7 4L3 8l4 4"/></svg>',
  tick: '<svg viewBox="0 0 16 16" width="13" height="13" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 8.5l3.2 3L13 4.5"/></svg>',
  copy: '<svg viewBox="0 0 16 16" width="13" height="13" fill="none" stroke="currentColor" stroke-width="1.4"><rect x="5" y="5" width="8" height="8" rx="1.6"/><path d="M3 10.5V4a1 1 0 011-1h6.5"/></svg>',
  ext: '<svg viewBox="0 0 16 16" width="12" height="12" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M6 3H3.5v9.5H13V10M9 3h4v4M13 3L7.5 8.5"/></svg>',
  lock: '<svg viewBox="0 0 16 16" width="10" height="10" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="3.5" y="7" width="9" height="6.5" rx="1.5"/><path d="M5.5 7V5a2.5 2.5 0 015 0v2"/></svg>',
  chev: '<svg viewBox="0 0 16 16" width="11" height="11" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="M4.5 6.5L8 10l3.5-3.5"/></svg>',
  dl: '<svg viewBox="0 0 16 16" width="13" height="13" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M8 2.5v8M4.5 7.5L8 11l3.5-3.5M3 13.5h10"/></svg>',
};

/* ------------------------------------------------------------ shell */
function topbar(on, opt) {
  opt = opt || {};
  const nav = ['Home', 'Tests', 'Sites'].map(n => `<a class="${n === on ? 'on' : ''}">${n}</a>`).join('');
  return `<div class="tb">${logo}<span class="studio">${opt.studio || 'Kestrel Studio'} ${ICON.chev}</span><nav>${nav}</nav><div class="r">${opt.usage === false ? '' : `<span class="usage">${opt.usage || 'Solo plan · 7 of 10 test sessions'}</span>`}<span class="btn dk">New</span><span class="me">${opt.me || 'MC'}</span></div></div>`;
}
const dateline = (l, r) => `<div class="dl"><span>${l}</span><span>${r || ''}</span></div>`;
const sec = (id, kick, title, idea, inner) => `<section class="xp" id="${id}"><div class="xh"><span class="xk">${kick}</span><h2>${title}</h2><p>${idea}</p></div>${inner}</section>`;
const hl = s => `<span class="mk">${s}</span>`;

/* ============================================================ P1 HOME */
const briefs = [
  ['13:15', `<b>Tester F</b> finished a session on Pocket. Transcript arriving, usually about a minute.`, '<span class="arr"><i></i><i></i></span>'],
  ['13:02', `<b>Tester E</b>'s session on Pocket has no audio, so there is nothing to transcribe. The screen recording is there to watch.`, '<a class="tl2">Watch</a>'],
  ['12:30', `<b>Tester D</b> on Pocket: <q>Where do I see what I spent this week?</q>`, '<span class="tc">06:21</span>'],
  ['Friday', `<b>Checkout</b>: test link shared. No sessions yet.`, `<a class="tl2">${ICON.copy} Copy link</a>`],
];
const p1 = sec('p1', 'p1', 'Home', 'A front page: the newest thing a tester said leads, in their words. Tests and sites sit in the side column as an index.', `
<div class="frame"><div class="win">${topbar('Home')}${dateline('Sunday 25 October · Example', 'Since your last visit, Friday 17:20: 6 sessions')}
<div class="home">
  <div class="hl-col">
    <div class="kick">Lead · Pocket · review ready</div>
    <blockquote class="lead-q">“I thought my cards would be on the home screen. ${hl('Is it under More?')}”</blockquote>
    <div class="byline"><span class="ini">TB</span><span><b>Tester B</b>, 03:08 into a 07:12 session · Sunday 11:40</span></div>
    <p class="lead-dek">The top friction point across Pocket so far: <b>4 of 5 testers</b> looked for their cards on the home screen. Two more points follow from the send flow and the balance.</p>
    <div class="acts"><span class="btn dk">Read the review</span><span class="btn">${ICON.play} Play 03:08</span><span class="mut">Transcribed and summarised at 11:48</span></div>
    <div class="rule-h"><span>Also new</span></div>
    <ul class="briefs">${briefs.map(b => `<li><span class="tc">${b[0]}</span><p>${b[1]}</p><span class="br-r">${b[2]}</span></li>`).join('')}</ul>
  </div>
  <aside class="idx">
    <div class="ih"><b>Tests</b><a class="tl2">New test</a></div>
    <ul class="ilist">
      <li>${thumbPocket(34)}<div><b>Pocket</b><span>6 sessions · 1 arriving</span></div><em class="st-y">Review ready</em></li>
      <li>${thumbOnb(34)}<div><b>Onboarding v2</b><span>1 session · no tasks</span></div><em>1 session</em></li>
      <li>${thumbCheckout(46)}<div><b>Checkout</b><span>3 tasks · desktop</span></div><em class="mut">Waiting for testers</em></li>
    </ul>
    <div class="ih"><b>Sites</b><a class="tl2">Publish</a></div>
    <ul class="ilist sites">
      <li><div><b class="addr">pocket.aeroapp.ai</b><span>Version 4 · from a prompt · 2 hours ago</span></div><em class="live">Live</em></li>
      <li><div><b class="addr">onboarding.aeroapp.ai</b><span>Version 2 · Figma link · Thursday</span></div><em class="live">Live</em></li>
      <li><div><b class="addr">checkout.aeroapp.ai</b><span>Version 2 · HTML upload · Friday</span></div><em class="live">Live</em></li>
      <li><div><b class="addr">kestrel.studio</b><span>Version 12 · custom domain · last week</span></div><em class="live">Live</em></li>
    </ul>
    <p class="fine">Live means anyone with the address can open it. Versions and rollback are on each site.</p>
  </aside>
</div></div></div>
<div class="sub2">
  <div class="frame small"><div class="win">${topbar('Home', { usage: 'Free plan · 0 of 3 test sessions', me: 'MC' })}${dateline('Sunday 25 October · first visit', '')}
    <div class="first">
      <div>
        <div class="kick">Nothing published yet</div>
        <h3 class="fr-h">Put a prototype online, then hear people use it<span class="dot">.</span></h3>
        <ol class="toc">
          <li><span class="rn">i</span><div><b>Paste a Figma prototype link</b><span>The share link of a Figma prototype.</span></div>${ICON.arrow}</li>
          <li><span class="rn">ii</span><div><b>Upload an HTML file or zip</b><span>Hosted at name.aeroapp.ai, with versions.</span></div>${ICON.arrow}</li>
          <li><span class="rn">iii</span><div><b>One prompt in Claude or ChatGPT</b><span>Built with your AI tool? It publishes from the chat.</span></div>${ICON.arrow}</li>
        </ol>
      </div>
      <aside class="next">
        <div class="kick">What happens next</div>
        <p><b>Publish.</b> It's live at its own address in seconds to a minute.</p>
        <p><b>Test.</b> Share one link. Testers need no account; they share a tab and talk.</p>
        <p><b>Review.</b> Each session is transcribed and summarised about a minute after it ends.</p>
        <p class="fine">Free to start: 3 test sessions, recordings included. Free sites stay live 7 days.</p>
      </aside>
    </div></div></div>
  <div class="side-cap"><b>First run.</b> With no sessions there is no lead story, so the front page becomes a contents page: three ways in, numbered, no icons. The right column says what will happen, in the same three words used everywhere: Publish, Test, Review.<br><br><b>Status without badges.</b> Type of prototype is shown by the prototype itself (a real thumbnail). Live is the brand's blue full stop. Waiting is grey text. New is a highlighter mark.</div>
</div>`);

/* ============================================================ P2 SESSIONS */
function testHead(tab) {
  const tabs = [['Setup', ''], ['Share', ''], ['Sessions', '6'], ['Review', '']].map(t => `<a class="${t[0] === tab ? 'on' : ''}">${t[0]}${t[1] ? ` <small>${t[1]}</small>` : ''}</a>`).join('');
  return `<div class="th-head"><div class="thl">${thumbPocket(44)}<div><div class="crumb">Tests /</div><h3 class="t-h">Pocket</h3><div class="t-dek"><span class="addr">pocket.aeroapp.ai</span> · version 4, from a prompt · 2 tasks: Send £20 to Sam, Find your cards · desktop</div></div></div><div class="thr"><span class="btn">${ICON.copy} Copy test link</span><span class="btn">Open as a tester</span></div></div><div class="tabs">${tabs}</div>`;
}
const srow = s => {
  let mid, right;
  if (s.st === 'proc') { mid = `<div class="sq proc"><span class="shape" style="width:78%"></span><span class="shape" style="width:46%"></span><small>Transcript arriving, usually about a minute</small></div>`; right = `<span class="mut">Arriving</span>`; }
  else if (s.st === 'noaudio') { mid = `<div class="sq na"><p>No audio on this one. The screen was recorded, so you can watch it, but there is nothing to transcribe.</p></div>`; right = `<a class="tl2">${ICON.play} Watch</a>`; }
  else { mid = `<div class="sq"><q>${s.q}</q></div>`; right = `<span class="frc">${s.fr} friction point${s.fr > 1 ? 's' : ''}</span>`; }
  return `<li class="${s.on ? 'on' : ''}"><span class="no">${s.n}</span><div class="who"><b>${s.who}${s.nw ? ' <span class="new">New</span>' : ''}</b><span>${s.when}</span></div>${mid}<span class="tc">${s.len}</span>${right}</li>`;
};
const p2 = sec('p2', 'p2', 'Sessions', 'The sessions of one test as a contents page: each one listed by its first line in the tester\'s words, numbered from the first, newest at the top.', `
<div class="frame"><div class="win">${topbar('Tests')}
<div class="tpage">${testHead('Sessions')}
<div class="sgrid">
  <div>
    <div class="slh"><span>No.</span><span>Tester</span><span>In their words</span><span>Length</span><span></span></div>
    <ol class="slist">${SESS.map(srow).join('')}</ol>
    <p class="fine pad">Numbers are kept in the order sessions arrived, so “No. 2” always means Tester B. All sessions on laptop, Chrome; HTML tests run on desktop.</p>
  </div>
  <aside class="sside">
    <div class="kick">This test so far</div>
    <div class="nums"><div><b>6</b><span>sessions</span></div><div><b>5</b><span>with audio</span></div><div><b>9</b><span>friction points</span></div></div>
    <p class="sp">Three themes so far. The biggest: cards are hard to find, <b>4 of 5</b>.</p>
    <span class="btn dk wide">Read the review ${ICON.arrow}</span>
    <div class="kick mt">Moving between sessions</div>
    <p class="sp">Open one and read it like an article. Its last line is the next session, the way a magazine ends a story with the next one.</p>
    <div class="endcard"><span class="kick">Next session</span><b>No. 3 · Tester C</b><q>Found the cards straight away, but only because I opened More by accident.</q></div>
    <p class="fine"><span class="kbd">J</span> <span class="kbd">K</span> next and previous · <span class="kbd">Space</span> play</p>
  </aside>
</div></div></div></div>`);

/* ============================================================ P3 SESSION */
const trLine = l => {
  let txt = l.x;
  if (l.now) {
    txt = hlWords(l.x, l.now);
  }
  return (l.task ? `<div class="task"><span>${l.task}</span></div>` : '') +
    `<div class="ln${l.now ? ' now' : ''}${l.fr ? ' frl' : ''}"><span class="tc">${l.t}</span><p>${txt}</p>${l.fr ? `<div class="mn"><b>${l.fr}</b>Friction point · ${l.c} testers</div>` : '<div></div>'}</div>`;
};
const p3 = sec('p3', 'p3', 'Session review', 'The session reads like an article: her words are the headline, the summary is the standfirst, the transcript is the body. The recording is docked beside it and the line playing now is highlighted word by word.', `
<div class="frame"><div class="win">${topbar('Tests')}
<div class="sess">
  <article class="art">
    <div class="crumbs"><span>Pocket / Sessions /</span><b>No. 2</b><span class="pn"><a>${ICON.back} No. 1</a><a>No. 3 ${ICON.arrow}</a></span></div>
    <h3 class="a-h">“Is it under More?”</h3>
    <div class="a-by"><span class="ini">TB</span><span><b>Tester B</b> · Sunday 11:40 · 07:12 · laptop, Chrome · screen and voice</span></div>
    <div class="stand"><span class="kick">Summary</span>Sent £20 to Sam without help. Expected her cards on the home screen and found them under More after 23 seconds. Unsure how to leave the send flow, and tried to tap the balance twice.<small>Transcribed and summarised at 11:48</small></div>
    <div class="tr-head"><span class="kick">Transcript</span><span class="mut">Follows the recording. Click a line to play from it.</span></div>
    <div class="tr">${TR.map(trLine).join('')}</div>
    <div class="nextstory"><span class="kick">Next session</span><div><b>No. 3 · Tester C · Sunday 12:05</b><q>Found the cards straight away, but only because I opened More by accident.</q></div>${ICON.arrow}</div>
  </article>
  <aside class="dock">
    <div class="rec">
      <div class="bw"><div class="bwb"><span class="lights"><i></i><i></i><i></i></span><span class="url">${ICON.lock} pocket.aeroapp.ai</span></div><div class="bws">${pocketPhone()}</div></div>
      <div class="ctl"><div class="row"><span class="pp">${ICON.pause}</span><span class="tc big">03:11 <i>/ 07:12</i></span><span class="sp1">1x</span></div>
      ${wave(96, 11, 191 / 432, 'sm')}
      <div class="mks"><i style="left:37.3%"></i><i style="left:42.1%"></i><i style="left:43.5%"></i></div>
      <p class="fine">Her browser tab and her voice. The tab recording has no pointer.</p></div>
    </div>
    <div class="kick mt">Top priorities</div>
    <ol class="prio">
      <li><span>Move cards onto the home screen</span><span class="tc">03:08</span></li>
      <li><span>Label the back arrow in Send</span><span class="tc">02:41</span></li>
      <li><span>Make the balance look less like a button</span><span class="tc">03:02</span></li>
    </ol>
    <div class="kick mt">Tasks</div>
    <ol class="prio tasks">
      <li><span>Send £20 to Sam <small>Done without help</small></span><span class="tc">02:41</span></li>
      <li><span>Find your cards <small>Found under More, after 23 seconds</small></span><span class="tc">03:31</span></li>
    </ol>
    <div class="dk-acts"><span class="btn">${ICON.dl} Download summary</span><span class="btn">Share</span></div>
  </aside>
</div></div></div>`);

/* ============================================================ P4 PROMPT */
const p4 = sec('p4', 'p4', 'Publish from a prompt', 'The connector flow written as a short numbered log on one page: each step stays visible once done, so you can see how you got here. Claude\'s side is drawn apart, outside Aero.', `
<div class="frame split"><div class="win w900">${topbar('Sites')}
<div class="pp-page">
  <div class="crumb">Sites / New /</div>
  <h3 class="t-h">Publish from a prompt</h3>
  <p class="t-dek2">Built with your AI tool? Ask it to publish to Aero. This page follows along and updates on its own.</p>
  <ol class="log">
    <li class="done"><span class="rn">i</span><div><b>Connect Aero to Claude or ChatGPT</b><span>Connected to Claude · Sunday 10:02. You only do this once.</span></div><span class="ok">${ICON.tick} Done</span></li>
    <li class="done"><span class="rn">ii</span><div><b>Paste this in the chat where you built it</b><div class="pq"><span>“Put this prototype online with Aero and set up a test.”</span><span class="btn">${ICON.tick} Copied</span></div><span>Your own words work too, as long as they mention Aero.</span></div><span class="ok">${ICON.tick} Done</span></li>
    <li class="done"><span class="rn">iii</span><div><b>Waiting for your chat</b><span>Claude published it at 10:04.</span></div><span class="ok">${ICON.tick} Done</span></li>
    <li class="pub"><span class="rn">iv</span><div class="pubb">
      <div class="pubt">${thumbPocket(70)}<div><span class="kick">Published</span><div class="addr-big">pocket.aeroapp.ai</div><div class="pmeta"><span class="live">Live</span> · Version 1 · from Claude · 10:04</div><p class="sp">A test was set up too, with 2 tasks.</p></div></div>
      <div class="acts"><span class="btn dk">Now test it ${ICON.arrow}</span><span class="btn">${ICON.ext} Open site</span><span class="btn">${ICON.copy} Copy address</span></div>
    </div></li>
  </ol>
</div></div>
<div class="outside">
  <div class="olabel">Outside Aero · Claude, simplified</div>
  <div class="claude">
    <div class="cl-top"><span class="cl-name">Claude</span><span class="cl-ch">Pocket prototype</span></div>
    <div class="cl-u">Put this prototype online with Aero and set up a test.</div>
    <div class="cl-tool"><span>Used Aero</span> publish_site, create_test</div>
    <div class="cl-a">It's live at pocket.aeroapp.ai. I set up a test with two tasks: send £20 to Sam, and find your cards. Your test link is ready to share.</div>
    <div class="cl-in">Reply to Claude</div>
  </div>
  <div class="olabel mt">Aero, two minutes earlier</div>
  <div class="mini-wait"><span class="rn">iii</span><div><b>Waiting for your chat</b><span>Paste the prompt in Claude or ChatGPT. Nothing to do here; this page updates when it's live.</span><div class="dots3"><i></i><i></i><i></i></div></div></div>
</div></div>`);

/* ============================================================ P5 UPLOAD */
const upHead = (st) => `<div class="crumb">Sites / New /</div><h3 class="t-h sm">Upload an HTML file or zip</h3>`;
const p5 = sec('p5', 'p5', 'Upload HTML or zip', 'One page, three moments: the drop area, the upload as a single quiet rule filling, then the published site set like a title page with its address, version and the next step.', `
<div class="pair">
  <div><div class="mini-lab">a · Drop</div><div class="frame half"><div class="win">${topbar('Sites', { usage: false })}<div class="up">${upHead()}
    <div class="drop"><div class="dz-t">Drop a file or a zipped folder here</div><div class="dz-s">An <b>index.html</b> at the top level, plus its files. Or <a class="tl2">choose a file</a>.</div></div>
    <div class="field"><span class="fl">Address</span><span class="fi"><b>checkout</b>.aeroapp.ai</span><span class="ok">${ICON.tick} Available</span></div>
    <p class="fine">Tests of HTML sites run on desktop.</p></div></div></div></div>
  <div><div class="mini-lab">b · Uploading</div><div class="frame half"><div class="win">${topbar('Sites', { usage: false })}<div class="up">${upHead()}
    <div class="upl"><div class="uf"><b>checkout.zip</b><span class="tc">2.4 of 3.8 MB</span></div><div class="bar"><i style="width:63%"></i></div>
    <ul class="files"><li><span class="ok">${ICON.tick}</span>index.html</li><li><span class="ok">${ICON.tick}</span>styles.css</li><li><span class="ok">${ICON.tick}</span>basket.js</li><li class="mut"><span>·</span>11 more files</li></ul></div>
    <div class="field"><span class="fl">Address</span><span class="fi"><b>checkout</b>.aeroapp.ai</span><span class="mut">Replacing version 1</span></div>
    <p class="fine">You can leave this page. It carries on.</p></div></div></div></div>
</div>
<div class="mini-lab">c · Published</div>
<div class="frame"><div class="win">${topbar('Sites')}
<div class="pubpage">
  <div class="pv"><div class="bw big"><div class="bwb"><span class="lights"><i></i><i></i><i></i></span><span class="url">${ICON.lock} checkout.aeroapp.ai</span></div><div class="pvs">${thumbCheckout(560, true)}</div></div></div>
  <div class="pvt">
    <div class="crumb">Sites /</div>
    <span class="kick">Published · Friday 16:40</span>
    <div class="addr-xl">checkout.aeroapp.ai</div>
    <div class="pmeta big"><span class="live">Live</span> · Version 2 · checkout.zip, 14 files, 3.8 MB</div>
    <div class="acts"><span class="btn dk">Now test it ${ICON.arrow}</span><span class="btn">${ICON.ext} Open site</span><span class="btn">${ICON.copy} Copy address</span></div>
    <p class="sp">A test gets its own link. People open it, share the tab and talk you through it. HTML tests run on desktop.</p>
    <div class="kick mt">Versions</div>
    <ol class="vers">
      <li><span class="vn">2</span><span>Friday 16:40 · checkout.zip</span><span class="live">Live</span></li>
      <li><span class="vn">1</span><span>Thursday 09:15 · checkout.zip</span><a class="tl2">Roll back to this</a></li>
    </ol>
  </div>
</div></div></div>`);

/* ============================================================ P6 REVIEW */
const tally = (n, of) => `<span class="tal">${Array.from({ length: of }, (_, i) => `<i class="${i < n ? 'f' : ''}"></i>`).join('')}</span>`;
const fix = (n, title, c, of, quotes) => `<li><span class="fx-n">${n}</span><div><div class="fx-t"><h4>${title}</h4><span class="cnt">${tally(c, of)} ${c} of ${of} testers</span></div>${quotes.map(q => `<div class="fq"><q>${q[0]}</q><span><b>${q[1]}</b> <a class="tl2">${ICON.play} ${q[2]}</a></span></div>`).join('')}</div></li>`;
const p6 = sec('p6', 'p6', 'Review across sessions', 'A review reads like a short report: what to fix first, each point argued in the testers\' own words with a count and the moment to play. Themes and disagreements sit in the margin.', `
<div class="frame"><div class="win">${topbar('Tests')}
<div class="tpage">${testHead('Review')}
<div class="rgrid">
  <div class="rmain">
    <div class="r-dl"><span class="kick">Based on 5 sessions with audio, out of 6</span><span class="mut">Updated Sunday 13:17</span></div>
    <h3 class="r-h">People found sending easy. Almost nobody found their cards<span class="dot">.</span></h3>
    <p class="stand2">Five testers sent money without help. Four of them looked for their cards on the home screen first, and three were unsure how to get back after sending.</p>
    <div class="kick">What to fix first</div>
    <ol class="fixes">
      ${fix(1, 'Move cards onto the home screen', 4, 5, [['I thought my cards would be on the home screen. Is it under More?', 'Tester B', '03:08'], ['Cards. Cards. Not in Payments either.', 'Tester F', '01:47']])}
      ${fix(2, 'Label the back arrow in Send', 3, 5, [["There's an arrow but it doesn't say where to.", 'Tester B', '02:41'], ["I wasn't sure the money had gone.", 'Tester A', '03:30']])}
      ${fix(3, 'Make the balance look less like a button', 2, 5, [['I tapped the balance expecting a breakdown.', 'Tester D', '00:58']])}
    </ol>
  </div>
  <aside class="rside">
    <div class="kick">Themes</div>
    <ul class="themes">
      <li><span>Cards hard to find</span><span class="cnt">${tally(4, 5)} 4 of 5</span></li>
      <li><span>No way back from Send</span><span class="cnt">${tally(3, 5)} 3 of 5</span></li>
      <li><span>Balance looks tappable</span><span class="cnt">${tally(2, 5)} 2 of 5</span></li>
      <li><span>Wants weekly spending</span><span class="cnt">${tally(1, 5)} 1 of 5</span></li>
    </ul>
    <div class="kick mt">Where they disagreed</div>
    <p class="sp">The balance: Testers B and D tried to tap it; A, C and F never mentioned it. Worth one more round before changing it.</p>
    <div class="kick mt">Sessions in this review</div>
    <ul class="inrev">${SESS.slice().reverse().map(s => `<li><span>No. ${s.n} · ${s.who}</span><span class="${s.st === 'ok' || s.st === 'proc' ? '' : 'mut'}">${s.st === 'noaudio' ? 'No audio, not included' : 'Included'}</span></li>`).join('')}</ul>
    <div class="dk-acts"><span class="btn">${ICON.dl} Download summary</span><span class="btn">Email it</span></div>
  </aside>
</div></div></div></div>`);

/* ============================================================ F1 FLOW */
const ENTRIES = [
  ['10:02', 'Connected to Claude'],
  ['10:04', 'Live at pocket.aeroapp.ai · version 1'],
  ['10:05', 'Test added · 2 tasks'],
  ['10:06', 'Test link copied'],
  ['11:40', 'Tester B opened the link'],
  ['11:48', 'Transcribed and summarised'],
];
function flowFrame(k, body) {
  const ents = ENTRIES.slice(0, k).map((e, i) => `<li class="${i === k - 1 ? 'cur' : ''}"><span class="tc">${e[0]}</span><span>${e[1]}</span></li>`).join('');
  return `<div class="ff"><div class="ffbar"><span class="ffl">Aero<span class="dot">.</span></span><span>Pocket</span></div><div class="ffb"><div class="ffk">Sunday · the Pocket page</div><ol class="ffl2">${ents}</ol><div class="ffx">${body}</div></div></div>`;
}
const FLOW = [
  [1, `<div class="fx-q">“Put this prototype online with Aero and set up a test.”</div><span class="fbtn">Copy prompt</span>`, '<b>1 · Prompt.</b> The page starts with the one line to paste. Connecting is a single step, once.'],
  [2, `<div class="fx-site">${thumbPocket(26)}<div><b>pocket.aeroapp.ai</b><span><i class="live">Live</i> · v1</span></div></div>`, '<b>2 · Live.</b> Claude publishes. The page writes its next entry; nothing navigates away.'],
  [3, `<div class="fx-task"><span>1</span>Send £20 to Sam</div><div class="fx-task"><span>2</span>Find your cards</div>`, '<b>3 · Test.</b> The test was set up from the same prompt. Tasks are listed, editable in place.'],
  [4, `<div class="fx-link">aeroapp.ai/t/8kq2</div><span class="fbtn">Copied</span>`, '<b>4 · Share.</b> One link to send. Testers need no account.'],
  [5, `<div class="fx-wait"><b>Tester B is in a session</b><span>Started 11:40. The transcript arrives about a minute after she finishes.</span></div>`, '<b>5 · First session.</b> Shown as an entry with a time. No live transcript, nothing typing.'],
  [6, `<div class="fx-quote">“I thought my cards would be on the home screen. <span class="mk">Is it under More?</span>”</div><span class="fx-by">Tester B · 03:08</span>`, '<b>6 · Review.</b> The log ends on her words. The page you started on is now the story of the test.'],
];
const f1 = sec('f1', 'f1', 'The flow: from prompt to first session', 'One page that keeps a log. The test page is written entry by entry with a time, newest at the bottom, from the prompt to the first quote. No stepper, no new screens: you read your way down.', `
<div class="frame flow">${FLOW.map(f => `<figure>${flowFrame(f[0], f[1])}<figcaption>${f[2]}</figcaption></figure>`).join('')}</div>
<p class="fine flowcap">Times are an example of one Sunday. The same log is the Pocket page's history later: once the first session is in, it folds into one “History” line at the top of the Pocket page, and the sessions take its place.</p>`);

/* ============================================================ M1 MARKETING */
const appSess = `<div class="a-sess"><span class="no">2</span><div class="who"><b>Tester B</b><span>Sunday 11:40</span></div><q>I thought my cards would be on the home screen. Is it under More?</q><span class="tc">07:12</span></div>`;
const mkSess = `<div class="m-sess"><div class="m-sess-top"><span class="m-no">No. 2</span><span class="m-ex">Example</span></div><q>I thought my cards would be on the home screen. Is it under More?</q><div class="m-by"><span class="ini lg">TB</span><b>Tester B</b><span>07:12 · 3 friction points</span></div></div>`;
const appFric = `<div class="ln frl a-fr"><span class="tc">03:08</span><p><span class="mk">I thought my cards would be on the home screen. Is it under More?</span></p><div class="mn"><b>Cards are hidden under More</b>Friction point · 4 of 5 testers</div></div>`;
const mkFric = `<div class="m-fric"><span class="m-k">Friction point · 03:08</span><q>I thought my cards would be on the home screen. <span class="mk">Is it under More?</span></q><div class="m-note"><b>Cards are hidden under More</b><span>4 of 5 testers</span></div></div>`;
const appSite = `<div class="a-site"><div><b class="addr">pocket.aeroapp.ai</b><span>Version 4 · from a prompt · 2 hours ago</span></div><em class="live">Live</em></div>`;
const mkSite = `<div class="m-site">${thumbPocket(84)}<div><div class="m-addr">pocket.aeroapp.ai</div><div class="m-meta"><span class="live">Live</span><span>Version 4</span></div></div></div>`;
const appLink = `<div class="a-link"><span class="kick">Test link</span><div class="a-lrow"><span class="addr">aeroapp.ai/t/8kq2</span><span class="btn">${ICON.copy} Copy</span></div><span class="fine">No account needed. Screen and voice.</span></div>`;
const mkLink = `<div class="m-link"><span class="m-k">Your test link</span><div class="m-lrow"><span class="m-url">aeroapp.ai/t/8kq2</span><span class="m-copy">${ICON.copy} Copy</span></div><p>Send it to a friend, a client or a classmate. They open it, share the tab and talk.</p></div>`;
const appLine = `<div class="ln now a-ln"><span class="tc">03:08</span><p>${hlWords('I thought my cards would be on the home screen. Is it under More?', 10)}</p><div></div></div>`;
const mkLine = `<div class="m-line"><div class="m-lt"><span class="m-play">${ICON.pause}</span><span class="tc">03:11 / 07:12</span><span class="m-ex">Example</span></div><p>${hlWords('I thought my cards would be on the home screen. Is it under More?', 10)}</p>${wave(70, 5, .62, 'm')}</div>`;
const kitRow = (n, name, use, a, m) => `<div class="kit"><div class="kit-l"><span class="xk">${n}</span><h4>${name}</h4><p>${use}</p></div><div class="kit-a"><span class="kl">In the app</span><div class="kpa">${a}</div></div><div class="kit-m"><span class="kl">Marketing version</span><div class="kpm">${m}</div></div></div>`;
const m1 = sec('m1', 'm1', 'Marketing kit', 'Five real components, simplified and set larger for the website, video and social cards. Fewer rows, no small metadata, the same type and the same highlighter. Then two pieces composed only from them.', `
<div class="frame kitf">
${kitRow('1', 'Session card', 'Homepage “Review” section, video end frame. Drops the date and status; keeps the number, the quote and the length.', appSess, mkSess)}
${kitRow('2', 'Friction-point quote', 'The hero of the Review section and of social cards. The margin note becomes a label under the quote.', appFric, mkFric)}
${kitRow('3', 'Published site card', 'Publish section and the prompt scene in the video. The real thumbnail stays; the time goes.', appSite, mkSite)}
${kitRow('4', 'Test link card', 'Test section and the share scene. The link is set big enough to read in a video.', appLink, mkLink)}
${kitRow('5', 'Transcript line, playing', 'The signature moment: words highlight as the recorded session plays back. Never shown during a live session.', appLine, mkLine)}
</div>
<div class="mini-lab">Composed: homepage hero block, 1360 wide</div>
<div class="frame hero">
  <div class="h-l">
    <span class="kick">Sunday, 11:40 · one tester, one link</span>
    <h3 class="h-h">Publish your prototype. Watch people use it<span class="dot">.</span></h3>
    <p class="h-s">Paste a Figma link, drop an HTML folder, or ask Claude. Share one link and hear real people use it, in their own words.</p>
    <div class="h-a"><a class="cta">Start free</a><a class="cta sec">See a test</a></div>
    <p class="fine">Free to start, recordings included. Paid from $3.</p>
  </div>
  <div class="h-r">
    <div class="h-site">${mkSite}</div>
    <div class="h-fric">${mkFric}</div>
    <div class="h-link">${mkLink}</div>
  </div>
</div>
<div class="mini-lab">Composed: social card, 1200 × 630</div>
<div class="frame og"><div class="ogc">
  <div class="og-top">${logo}<span class="m-ex">Example session</span></div>
  <div class="og-line">${mkLine}</div>
  <div class="og-bot"><span class="og-tag">In their own words<span class="dot">.</span></span><span class="og-sub">Tester B, Pocket, 03:08 · transcribed and summarised</span></div>
</div></div>`);

/* ============================================================ CSS */
const css = fs.readFileSync(path.join(__dirname, 'pages.css'), 'utf8');

const html = `<!doctype html>
<html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Aero, Story: the app</title>
<link rel="icon" href="${fav}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:ital,wght@0,400..700;1,400..600&family=Geist:wght@400..600&family=Geist+Mono:wght@400;500&display=swap">
<style>${css}</style></head>
<body>
<header class="ph"><div>${logo}</div><div><span class="xk">Direction C · Story</span><h1>The whole app, read like a calm article<span class="dot">.</span></h1><p>Every main screen leads with what the tester said and lets you read it slowly. Warm paper, hairline rules, one highlighter, the blue full stop. No cards with stripes, no icon tiles. All names and data are examples.</p></div></header>
${p1}${p2}${p3}${p4}${p5}${p6}${f1}${m1}
</body></html>`;
fs.writeFileSync(OUT, html);
const txt = html.replace(/<script[\s\S]*?<\/script>/g, '').replace(/<style[\s\S]*?<\/style>/g, '').replace(/<[^>]+>/g, ' ');
const bad = txt.match(/[–—!]/g) || [];
console.log('pages.html', (html.length / 1024).toFixed(0) + 'KB', bad.length ? 'DASH/EXCL: ' + bad.join('') : 'copy ok');
