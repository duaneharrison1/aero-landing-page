import json
def T(k,label,img,idea,works,doesnt): return dict(key=k,label=label,img=img,idea=idea,works=works,doesnt=doesnt)
N='New'; R5='Round 5 version'
S=[]
S.append(dict(id='p1',num='01',short='Home',title='Home',question='What should the first screen say when you come back? Everyone agrees it opens on what is new. The difference is how loud the lead is.',
 take=['All four directions moved away from today\'s grid of tests to "what\'s new first". They differ in volume: A a quiet list, B coloured step cards, C one quote as a headline, D one playable moment.',
       'My read: A\'s quiet list, with D\'s "worth watching" moment as its first item when there is one. C\'s quote works as that moment\'s headline.'],
 tiles=[
  T('A','A · Studio',[['hi/studio-p1.png',N],['hi/r5-studio-1.png',R5]],'What\'s new as a list with real thumbnails and one dot per session; the first run puts the three inputs right on the page.',
    ['Calm, and the real thumbnails replace icon tiles','Session dots: status for six sessions in one glance','First run is the input itself (paste, drop, connect), not three cards'],
    ['Three columns compete (what\'s new, tests, sites)','The coloured squares beside each test in the sidebar are colour-coding again','Plan usage block at the bottom is noise on every page']),
  T('B','B · Colour',[['hi/colour-p1.png',N],['hi/r5-colour-1.png',R5]],'What\'s new split by step (Publish, Test, Review), each in its colour; a loop meter shows where each test has got to.',
    ['You know what kind of news it is before you read it','The loop meter is a nice, honest progress mark','No colour in the nav, as asked'],
    ['Three coloured cards in a row is close to the AI pattern','Tests and sites tables repeat each other','A lot of colour for a page you see daily']),
  T('C','C · Story',[['hi/story-p1.png',N],['hi/r5-story-1.png',R5]],'A front page: the newest thing a tester said is the headline, tests and sites as an index on the right. No sidebar.',
    ['The most human home: her words first','Top bar instead of sidebar gives the reading column room','Highlighter and tally marks instead of pills'],
    ['One lead story hides the rest when several tests run','Roman numerals and italics are decoration (the team agrees)','Without a sidebar the list of tests is one click further away']),
  T('D','D · Replay',[['hi/replay-p1.png',N],['hi/r5-replay-1.png',R5]],'Opens on one moment worth watching, cued to 03:08; tests drawn as reels; the loop line runs along the bottom.',
    ['Shows the product\'s value every visit','Reels: each bar is a session, to scale','The bottom line is the same thing as the homepage scrubber and the video'],
    ['Dark everywhere is heavy for daily admin work','Small, dense type','A playing clip can distract when you only came to copy a link']),
  T('E','E · App UI round',[['e/s2-1.png','Layout A'],['e/s2-2.png','Layout B'],['e/s2-3.png','Layout C']],'The previous round: three home layouts and every state (first run, loading, drafts, phone).',
    ['Covers every state, which the directions don\'t','Draft rule: only real input becomes a draft'],
    ['Looks like a generic template next to A to D','Icons in pastel boxes in the feed (the pattern you flagged)']),
  T('T','Today\'s app',[['today/t-dashboard.png','Live app, 22 Oct']],'',[],['Grid of empty drafts with made-up names','Numbers that say 0% before anything happened']),
 ]))
S.append(dict(id='p2',num='02',short='Sessions',title='Sessions',question='How do you see and move between the sessions of one test?',
 take=['A, B and C agree: a numbered list with each tester\'s first words, numbers that never change, and J / K to move. D adds something none of the others have: every session on one shared clock, so the 03:08 cluster across four testers shows before you press play.',
       'My read: C\'s list (their words, big numbers) with B\'s friction ticks per row, and D\'s shared clock as a "Compare" view on top.'],
 tiles=[
  T('A','A · Studio',[['hi/studio-p2.png',N]],'A calm table with a peek panel on the right; status is a word with its own mark.',
    ['Peek panel: read the summary without leaving the list','"First friction, in their words" column'],['The length strip on top adds little (the team would drop it)','Very close to today\'s structure; little new']),
  T('B','B · Colour',[['hi/colour-p2.png',N]],'Length drawn to scale with a tick per friction point; the test header turns mint on Review tabs.',
    ['Friction ticks per row are the clearest small signal','Selected row in the same blue as the dot'],['Header changing colour per tab feels jumpy (the team agrees)']),
  T('C','C · Story',[['hi/story-p2.png',N]],'A contents page: each session listed by its first line in the tester\'s words.',
    ['Most readable; you can choose what to watch from the words alone','"Next session" teaser at the end of each one'],['No sense of where in the session things went wrong','Feels like a document if there are 40 sessions']),
  T('D','D · Replay',[['hi/replay-p2.png',N]],'All sessions as tracks on one clock, like an editor; selected one previews on top.',
    ['Unique: shows patterns across testers before watching','Each status looks different (waveform, hatching, flat line)'],['Squashes when lengths vary a lot','Dark, editor-like; may feel technical']),
  T('E','E · App UI round',[['e/s7-1.png','A. Table'],['e/s7-2.png','B. Cards with a quote']],'',[],[]),
  T('T','Today\'s app',[['today/t-sessions.png','Live app: Sessions tab']],'',[],['Sessions tab can say "no sessions" while they exist (bug B2)']),
 ]))
S.append(dict(id='p3',num='03',short='Session review',title='Session review',question='Watch first or read first? This is the most important screen and the real choice of the round.',
 take=['A, B and D put the recording first; C puts her words first and docks the recording. You liked C\'s calm analysis view and D\'s timeline line, which pull in different directions.',
       'My read: C\'s article layout as the default (headline from her words, summary, transcript with friction points in the margin), with D\'s timeline as the player bar of the docked recording, and one switch to make the recording big.',
       'Note for C: the yellow rule down the left of the summary and the margin notes is a mild version of the side-stripe pattern; I would remove it.'],
 tiles=[
  T('A','A · Studio',[['hi/studio-p3.png',N],['hi/r5-studio-2.png',R5]],'Recording left on the Review wash, transcript right following the playback, summary and priorities under.',
    ['True to the app: word highlight only on playback, no cursor','Friction cards jump to their moment'],['Three areas compete for attention','Transcript is small and secondary']),
  T('B','B · Colour',[['hi/colour-p3.png',N],['hi/r5-colour-2.png',R5]],'Recording first; friction points are mint ticks on the timeline and mint times in the list.',
    ['Ticks on the timeline match the list','Clear task markers'],['Almost the same layout as A','The blue word highlight is harsh at reading size']),
  T('C','C · Story',[['hi/story-p3.png',N],['hi/r5-story-2.png',R5]],'The session reads like an article: her words as the headline, summary as the standfirst, transcript as the body, friction in the margin.',
    ['The calmest way to understand a session','Friction point sits beside the line that caused it','Headline is her own words'],['Yellow left rules (side-stripe pattern)','Recording is small; watching is secondary']),
  T('D','D · Replay',[['hi/replay-p3.png',N],['hi/r5-replay-2.png',R5]],'The recording is the page; tasks and friction points on its timeline; light variant included.',
    ['Watching is the core value, and this shows it','Timeline with tasks and markers is the best player bar of the four'],['Transcript squeezed into a column','Lots going on under the player']),
  T('E','E · App UI round',[['e/s8-1.png','A. Recording first'],['e/s8-3.png','B. Read like an article'],['e/s8-4.png','C. Theatre'],['e/s8-2.png','D. Proposed: cursor and clicks']],'',[],[]),
  T('T','Today\'s app',[['today/t-session-top.png','Live app: top of the session page'],['today/t-session-recording.png','Live app: scrolled down to the recording and transcript']],'',[],['Recording on a separate page from the findings']),
 ]))
S.append(dict(id='p4',num='04',short='From a prompt',title='Publish from a prompt',question='The connector flow: connect once, copy the prompt, wait for the chat, published. Which look and how much detail?',
 take=['All four land on the same flow, so this is a choice of look and detail, not of flow. All keep Claude in its own panel outside Aero.',
       'Detail ranges from C (calm, four lines) to D (a live log with clock times). D is the most reassuring while waiting, but its file sizes are too technical for most people.'],
 tiles=[
  T('A','A · Studio',[['hi/studio-p4.png',N],['hi/r5-studio-3.png',R5]],'One page that keeps its history; each step ticks off in place; ends on "Now test it".',['Ends on the next step, not a dashboard','Short "What the prompt does" notes'],['Shows the steps twice (cards and page)']),
  T('B','B · Colour',[['hi/colour-p4.png',N],['hi/r5-colour-3.png',R5]],'Publish is sunflower; four numbered steps; tabs switch between Figma, HTML and prompt.',['Clearest numbering','"Share the test" when the prompt already made one'],['The yellow is strong for a whole page']),
  T('C','C · Story',[['hi/story-p4.png',N],['hi/r5-story-3.png',R5]],'A short numbered log; the published site set like a title page.',['Calmest','Real thumbnail of the published page'],['Roman numerals']),
  T('D','D · Replay',[['hi/replay-p4.png',N],['hi/r5-replay-3.png',R5]],'While waiting, a log with clock times fills the empty player.',['Most reassuring while you wait','Empty player fills with your prototype when live'],['"Receiving files, 412 KB" is too technical','Dark']),
  T('E','E · App UI round',[['e/s3-1.png','A. Three tiles, one page'],['e/s3-2.png','B. One question at a time'],['e/s3-3.png','C. Prompt first']],'',[],[]),
  T('T','Today\'s app',[['today/t-create-modal.png','Live app: New test window']],'',[],['Lands on setup fields, not on the link to share']),
 ]))
S.append(dict(id='p5',num='05',short='Upload HTML',title='Upload HTML or zip',question='Drop, uploading, published with address and version, then "Now test it".',
 take=['Again the same flow everywhere. Worth keeping from all: the version list with roll back, and "Now test it" as the one next step.',
       'The upload limits the teams wrote (50 MB, 100 MB) are placeholders. The code has a 4.5 MB request cap on one path; the real limit needs checking before any copy uses a number.'],
 tiles=[
  T('A','A · Studio',[['hi/studio-p5.png',N]],'',['Version table with roll back on each row','Calm file list while uploading'],['Limit placeholder']),
  T('B','B · Colour',[['hi/colour-p5.png',N]],'',['Settings (password, domain, badge) beside versions'],['Sunflower drop zone close to a pastel box']),
  T('C','C · Story',[['hi/story-p5.png',N]],'',['Published page reads like a title page'],['Drawn preview of the site is simplified']),
  T('D','D · Replay',[['hi/replay-p5.png',N]],'',['The bottom line doubles as the upload progress bar','The live site shown as testers will see it'],['Dark frame around a light site']),
  T('E','E · App UI round',[['e/s4-1.png','A. Header and tabs'],['e/s4-2.png','B. One page']],'',[],[]),
  T('T','Today\'s app',[['today/t-site-detail.png','Live app: a live site'],['today/t-sites.png','Live app: Sites list']],'',[],['Free sites say "Live" after they have gone offline (B13)']),
 ]))
S.append(dict(id='p6',num='06',short='Across sessions',title='Review across sessions',question='What to fix first, across six sessions.',
 take=['My read: C\'s plain-English headline ("People found sending easy. Almost nobody found their cards."), then a numbered "what to fix first" with counts shown as A\'s session dots or B\'s squares and playable quotes. D\'s "where people got stuck" chart as an optional view.',
       'D\'s ordering by "how long it held them" and "where testers disagreed" need data we do not save today; treat them as proposals.'],
 tiles=[
  T('A','A · Studio',[['hi/studio-p6.png',N]],'',['Session dots show who said what, so "4 of 5" is visible'],['Summary wash box at the top is soft but vague']),
  T('B','B · Colour',[['hi/colour-p6.png',N]],'',['Count squares are clear','What worked and where testers disagreed, side by side'],['Mint header again']),
  T('C','C · Story',[['hi/story-p6.png',N]],'',['The headline sentence is the best summary of a test in any version'],['Little visual proof; it is all words']),
  T('D','D · Replay',[['hi/replay-p6.png',N]],'',['Overlay on one clock is strong visual proof','Quotes as playable clips'],['Needs data not saved today']),
  T('E','E · App UI round',[['e/s9-1.png','A. What to fix first'],['e/s9-2.png','B. Written summary']],'',[],[]),
  T('T','Today\'s app',[['today/t-insights.png','Live app: Insights tab']],'',[],['Insights stuck or crashing (B3 to B5)']),
 ]))
S.append(dict(id='f1',num='07',short='The flow',title='The flow: from prompt to first session',question='Four different flows. This is an information architecture choice, not a visual one.',
 take=['A and C arrived separately at the same idea: one page per prototype that fills in as you go (published, test link, sessions, review). Today Sites and Tests are separate places.',
       'My read: decide this first. If yes, "Pocket" is one object with Publish, Test and Review tabs, and Sites and Tests stop being separate lists. B\'s stepper and D\'s timeline are then ways of showing progress on that page.'],
 tiles=[
  T('A','A · Studio: one page that fills in',[['hi/studio-f1.png',N]],'',['Nothing to navigate; each step lands as a row'],['Merges Sites and Tests: a real IA change']),
  T('B','B · Colour: a colour stepper',[['hi/colour-f1.png',N]],'',['The canvas colour tells you which step you are in'],['More screens; feels like a wizard']),
  T('C','C · Story: a page that keeps a log',[['hi/story-f1.png',N]],'',['Times on every step; history stays readable'],['Log can get long']),
  T('D','D · Replay: player-first, one line',[['hi/replay-f1.png',N]],'',['The whole journey is one timeline; best for the video'],['As app navigation it is abstract']),
  T('E','E · App UI round',[['shots/ex-flows.png','Flows']],'',[],[]),
 ]))
S.append(dict(id='m1',num='08',short='Marketing kit',title='Marketing versions of components',question='The step that was missing: five real components (session card, friction quote, site card, test link, transcript line) at 1.5 to 2x, with less detail, then a hero and a social card built only from them.',
 take=['B\'s rule is the one to keep whatever the look: a component never picks its own colour; it takes the colour of the step it sits on. That is what lets one session card work in the app, on the site and in a video.',
       'The friction quote with the word highlight is the strongest marketing piece in all four; it is also "In their own words".'],
 tiles=[
  T('A','A · Studio',[['hi/studio-m1.png',N]],'',['Washes carry from app to site unchanged','"In their own words" social card'],['Hero stack is a little busy']),
  T('B','B · Colour',[['hi/colour-m1.png',N]],'',['Step colour explains before you read','Three-column social card'],['Close to three pastel cards']),
  T('C','C · Story',[['hi/story-m1.png',N]],'',['The highlighted quote is the hero','Most restrained'],['Little colour; may look plain on social']),
  T('D','D · Replay',[['hi/replay-m1.png',N]],'',['Dark tiles stand out on a light page','Player and waveform are ready for video'],['Dark everything in marketing']),
 ]))
S.append(dict(id='btn',num='09',short='Buttons',title='Buttons in the app',question='Not decided. Four realistic options, each drawn on the same seven real moments: dashboard, session review with the player, share modal, delete confirm, new test modal, tester task panel, disabled and loading. The stock blue is gone.',
 take=['Option 3 (ink everywhere you read, accessible glass only where controls float over a recording or prototype) is the team\'s pick and mine. On the dashboard and in modals it is identical to option 1 on purpose.',
       'The accessible glass: panels you read use a frosted plate (86% white); glass stays on small floating controls. Over a dark recording it turns smoky grey to stay readable (4.7 to 7.6:1 against the worst pixel behind the label). It passes AA, but it looks less glassy than the lab version.',
       'Every option passes AA: ink 16.8:1, deep blue 8.6:1, graphite 9.6:1. The logo blue itself is too light for white text (4.1:1), so option 2 uses it darker and greyer.'],
 tiles=[
  T('K','Side by side: dashboard header and share modal',[['hi/kit2-cmp.png','']],'',[],[]),
  T('K','1 · Ink',[['hi/kit2-o1.png','']],'Near-black primary, white secondary with a hairline, red only for delete.',['Calm; the blue dot stays the one bright thing','Highest contrast'],['Can feel severe on large empty pages']),
  T('K','2 · Deep Aero blue',[['hi/kit2-o2.png','']],'The logo dot\'s hue, darker and greyer (#254A8D).',['Ties the button to the logo','Clear call to action'],['Blue everywhere competes with links and the playhead']),
  T('K','3 · Ink, glass where it floats',[['hi/kit2-o3.png','']],'Option 1, plus the accessible glass only on the player controls and the tester\'s task panel.',['Glass where Aero cannot know what is behind a control','One family with two states'],['Glass over dark recordings reads as smoky grey']),
  T('K','4 · Soft graphite',[['hi/kit2-o4.png','']],'Warm graphite pills, warm stone secondary.',['Softest, friendliest'],['Publish and row actions look alike','Hairlines and stone below 3:1']),
  T('K','The team\'s recommendation',[['hi/kit2-rec.png','']],'',[],[]),
  T('K','Reference: the eight families from the first kit',[['hi/kit-b1.png','']],'',[],[]),
 ]))
S.append(dict(id='logo',num='10',short='Logo',title='Logo in use',question='Not decided. Seven options, at size, 24px, favicon 32 and 16, then in the sidebar, tester footer, share email, browser tab and site nav.',
 take=['Today\'s app sets "Aero." in a serif (see the Today pictures above); every option here is a sans, so whichever wins, the app logo changes.','In a browser tab every option becomes the same tile, so the favicon matters more than the wordmark; "A." is the strongest at 16px.',
       '"Made with Aero." puts a full stop mid-sentence. If "Aero." wins, the tester footer may need the wordmark without the dot, or the dot mark.'],
 tiles=[
  T('K','Logo options',[['hi/kit-l1.png','']],'',[],[]),
  T('K','Logo in use',[['hi/kit-l2.png','']],'',[],[]),
  T('K','Kit team\'s three pairings',[['hi/kit-r1.png','']],'',[],[]),
 ]))

TODAY={
 'p1':('Today\'s dashboard is a grid of tests with four counters on top.',['Simple and familiar; filters and search work','"New test" is easy to find'],['Grid fills with drafts named lone-arch, cool-flamingo','Counters say 0% before anything happens','"AI-generated insights" in the subtitle (AI as the headline)','Blue-tinted buttons look washed out']),
 'p2':('A list of sessions with a one-line summary, length and status; themes on the right.',['Each row has a summary and a length','Themes with counts beside the list'],['Every tester is "Anonymous Tester" and every row says "Friction"','The tester\'s own words are missing','"No sentiment yet" panel is always empty']),
 'p3':('Summary, priorities and friction points at the top; recording and transcript far below.',['All the findings are there, with quotes and a recommendation','Priorities are numbered'],['Recording is hidden behind "Watch recording", about 1,800px down','Transcript is one block with no times','Red Delete button sits next to the title','"AI insights" label']),
 'p4':('A New test window with four ways in.',['Four clear ways in, including an existing site','Opening it saves nothing'],['Icons in pastel boxes: the pattern you flagged is in today\'s app','The window uses a different font (Poppins) from the app (Inter)','No sense of what happens next']),
 'p5':('A live site page with a preview, a drop zone, auto-publish and an agent prompt.',['Drop to publish a new version, right on the page','Auto-publish switch and "Get prompt" are useful'],['Sites list is mostly drafts with made-up names','Copy and Visit buttons look different from each other','Subtitle copy has an em dash']),
 'p6':('An executive summary, then priority fixes, with themes on the right.',['A summary and a fix list exist'],['Long summary paragraph','"L" badges mean nothing to a reader','No quotes or "how many testers" per fix']),
}
for sec in S:
    tt=[t for t in sec['tiles'] if t['key']=='T']
    if tt:
        t=tt[0]; sec['tiles'].remove(t); sec['tiles'].insert(0,t)
        if sec['id'] in TODAY:
            t['idea'],t['works'],t['doesnt']=TODAY[sec['id']]
        t['label']='Today: the live app'

# make K tile keys unique for voting
for s in S:
    n=0
    for t in s['tiles']:
        if t['key']=='K':
            n+=1; t['vkey']=f'K{n}'
D=dict(sections=S,
 intro=['You said a step was missing: seeing each main screen in every direction and deciding what works before tightening components. This is that step.',
        'Each row is one screen and starts with today\'s live app (captured at 2x), as the base. Then A, B, C and D, the four round 5 directions, each redrawn across the whole app by its own team (the round 5 version underneath where there was one), then E, the app UI round, each layout at full size. Then the flow, the marketing kit, buttons in the app, and the logo.',
        'Pictures are full width; use "Side by side" at the top if you want two per row. Click any picture to open it on its own. Mark each tile Keep, Parts of it or Drop, with a note if it helps; I read your marks before the next round. The live pages (with real glass and hover) are linked at the bottom.'],
 roles=[['Information architect','home, sessions and the one-page-per-prototype question'],['UX designer','flows, states, moving between sessions'],['UI designer','layout, type, status without pills or icon boxes'],['Brand and graphic designer','logo, colour, washes'],['Copywriter','every label against the tone of voice'],['Animator','motion notes on each screen'],['Marketer','the marketing kit and composed hero and card']],
 patterns=['White cards with a coloured stripe down one side','Icons in pastel rounded boxes','Sparkle icons, purple gradients, emoji','Rows of three identical icon cards','Pills on everything; stock photos of people'],
 recommend=['Use A (Studio) as the app\'s look: light, calm, colour only in soft washes. It held up on every screen.',
  'Take C\'s session as an article (her words as the headline, friction in the margin) and C\'s plain-English review headline.',
  'Take D\'s timeline line (player bar, loop line, flow line) and the "worth watching" moment on Home; offer D\'s shared clock as a Compare view.',
  'Take B\'s rule: components take the colour of the step they sit on. Use count squares or session dots for "4 of 5".',
  'Decide the IA question first: one page per prototype, with Publish, Test and Review on it, instead of separate Sites and Tests.',
  'Buttons: ink solid; glass only where controls float over a prototype. Logo: keep "Aero." with an "A." favicon, and check the tester footer wording.',
  'Then tighten the app UI round into these components and their marketing versions, and add them to the /aero showcase.'])
json.dump(D,open('/home/claude/research/explore/notes.json','w'),indent=1)
