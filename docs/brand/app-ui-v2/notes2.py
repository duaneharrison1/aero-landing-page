import json
def T(k,label,img,idea='',works=None,doesnt=None,vkey=None):
    d=dict(key=k,label=label,img=img,idea=idea,works=works or [],doesnt=doesnt or [])
    if vkey: d['vkey']=vkey
    return d
def sec(id,num,short,title,q,shot,team,take=None,label=None):
    return dict(id=id,num=num,short=short,title=title,question=q,take=take or [],
                tiles=[T('A',label or 'A · Studio, v2 (light, then dark)',[[f'hi/{team}-{shot}.png','']],vkey='v2')])
S=[
 sec('home','01','Home','Home','"What\'s new" as a plain timeline of events, sites as preview blocks, tests as status lines. Layout A (timeline first) and B (sites on top).','m1','make',
     ['The team picks A: what changed is the reason to open Home. B suits someone who mostly publishes sites.','Site visits on Home need site analytics (Solo plan); check we store daily visits before building that event.']),
 sec('first','02','First run','First run, and only one site or test','Teaches Publish, Test, Review with a faint shape of what will appear, three ways in, and "Open the example". With one site or test, it sits in the sidebar.','m2','make'),
 sec('lists','03','Lists','Sites and Tests lists','Sites as blocks with a real preview (Live, Private, Free countdown); tests as status lines with a small preview and session dots.','m3','make'),
 sec('site','04','Site page','Site page','Everything on one page: preview, address, drop a new version, versions with roll back; settings (public or private, domain, favicon, badge, name) in a side column. "Test this site" explains it makes a copy with its own link.','m4','make'),
 sec('create','05','Create','Create: one guided flow per source','Pick the source first, then its own flow: upload (the wash picks up the site\'s colours after upload, then "Now test it"), prompt (copy it into Claude or ChatGPT, no connector; blue-dot loader while waiting), Figma link (publish only once the link is checked).','m5','make'),
 sec('setup','06','Test setup','Test setup and share','Name, optional tasks, welcome and thank-you; the link card, "Open as tester" (recorded as You), an open or closed switch for new sessions, the test\'s own domain and favicon.','m6','make'),
 sec('tester','07','Tester','Tester start screen and task pill','Asks for a first name (optional) before any browser prompt, then permissions. The task pill floats over the prototype: words on a frosted plate so they read over any colour, glass only on Done. Shown over five backgrounds.','m7','make'),
 sec('sessions','08','Sessions','Sessions','One row per tester: name, device, summary or quote, length, tasks 2 of 2, Issue / Confusion / Works well counts with severity, and Watch. "Transcript arriving", "No audio" and "You" rows.','s1','review'),
 sec('watch','09','Watch','Session review: Watch','Dark first. Recording left (a recorded tab, no pointer), one timeline with task regions and tag marks plus filter chips, follow-along transcript with the current word lit, click to jump, "Back to now", Summary per task, speeds, Skip silence, keyboard sheet, Download menu, previous and next tester.','s2','review',
     ['Built on the research: video left and transcript right (UserTesting, Lookback, Grain), one timeline with task and tag markers, Frame.io-style keys.']),
 sec('read','10','Read','Session review: Read','The same session as a calm read: her words as the headline, the summary as the opening, tags and notes in the margin, the video in a corner that keeps playing. One switch between Watch and Read.','s3','review'),
 sec('noaudio','11','No audio','No tasks, no audio','What changes when there are no tasks and no sound: no task lane, an honest "No sound in this recording", Transcript and Read switched off with a reason. Two half-cases beside it.','s4','review'),
 sec('insights','12','Insights','Insights, across sessions','Its own tab. Summary first, a score per task, Task 2 opened into a timeline (one bar per tester from their own start, with a median line), issues ranked "4 of 6 testers" with playable quote cards, what worked, where testers disagreed, a confidence note. By task, by theme, by priority; Copy as table.','s5','review'),
 sec('insempty','13','Insights empty','Insights: empty and early','0 sessions: three steps say what happens and when, beside a faded Example, with Copy test link and Open the example. 2 sessions: "Patterns appear from 3 sessions", low confidence, "Seen so far".','s6','review'),
 dict(id='mkt',num='14',short='Marketing',title='Marketing versions',question='The real components, bigger and simpler, and a homepage hero and a social card built only from them.',take=[],
      tiles=[T('A','Make team: site block, test link card, what\'s-new rows, hero',[['hi/make-m8.png','']],vkey='make'),T('A','Review team: session row, quote card, player, social card',[['hi/review-s7.png','']],vkey='review')]),
]
D=dict(sections=S,
 intro=['Round v2 on your pick, A Studio, with your notes from the directions board: ink buttons with quiet glass, "Aero." in Geist with the blue dot, dark mode, Sites and Tests separate with "Test this site" making a copy, testers with names, one guided flow per source, and the review screens built on the research into pro tools (Lookback, UserTesting, Grain, Maze, Dovetail, Frame.io).',
        'Two teams, one shared stylesheet, so it reads as one product. Every screen is shown in light and then dark. Mark each screen Keep, Parts of it or Drop, with a note; I read the marks before building.',
        'The questions that need your answer are at the bottom.'],
 roles=[['Information architect','sites, tests, insights as its own tab'],['UX researcher','what pro review tools do'],['UX and UI designers','screens, states, light and dark'],['Copywriter','every label'],['Marketer','marketing versions']],
 patterns=['Coloured side stripes on cards','Icons in pastel boxes','A moving cursor in a replay','A transcript typing live'],
 recommend=[
  'Home: layout A (timeline first) or B (sites on top)? Team picks A.',
  'Private site means: a password (a Basic plan feature today) or only people signed in? This decides whether Free gets the switch.',
  'Test link: aeroapp.ai/t/pocket-7k2 (as drawn) or its own name.aeroapp.ai?',
  'A test can have its own custom domain, separate from its site. On which plan?',
  'New: an open or closed switch for taking sessions on a test. Want it?',
  'After "Now test it", open the test on Setup (drawn) or Share?',
  'Your own "Open as tester" runs ("You"): count towards the session allowance? Keep them out of Insights by default?',
  'Every account gets a read-only Example study (Pocket) under Tests until dismissed?',
  'Figma link offered under New site as well, or only under Tests?',
  'Sessions newest first (drawn) or numbered from the first?',
  'Ranking in Insights: severity first (Minor, Major, Critical, editable), then how many testers?',
  'Watch as the default view, remembering each person\'s last choice of Watch or Read?',
  'For me to check in the code before building: the recorder logs task ticks with times; tasks still count with no audio; "Skip silence" can work from the audio; daily site visits are stored.'])
for s in D['sections']:
    s.setdefault('take',[])
json.dump(D,open('notes.json','w'),indent=1)
