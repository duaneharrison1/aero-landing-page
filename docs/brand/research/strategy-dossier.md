
# Aero research and strategy
 · 
Steps 1 and 2 of the brand playbook (the same process HeyBooking went through), run on Aero. Read this, react, then I start art direction.
## The answer
**Why Aero:** it is the only tool that puts your prototype online and tests it with real people from the same link, on a monthly plan a solo designer will pay for.
- 
**Cheap self-serve testing is gone.** Maze dropped its $99 plan in April 2026. Lyssna starts at $166 a month. UserTesting, Ballpark and Outset start with a sales call. Aero tests start free and paid plans start at $3.
- 
**Nobody joins hosting and testing.** Hosts (Tiiny, Static.app, Vercel) don't test. Testers (Lyssna, Ballpark) make you host somewhere else and paste a URL.
- 
**AI-built prototypes are the newest, least-crowded searches.** "Test a Lovable prototype with users" has almost no one ranking for it.
**But the website doesn't say any of this.** It leads with AI agents and a terminal command, shows no product, has placeholder FAQ copy, Figmafolio leftovers on pricing, and blank Privacy and Terms pages. The July decisions ("Publish prototypes and run real user tests", AI as a quiet helper) were made but drifted.
**Recommended lead:** the loop, with user testing as the reason to pay and hosting as the way in. Working line: Publish your prototype. Watch people use it. Same link.
## What Aero is today
Read from the code, not the website. This becomes docs/PRODUCT.md.
Part
What it does
Status
User testing
Testers open a link, follow tasks and think aloud. Screen and voice recorded, transcribed, AI insights per session plus a summary across sessions
Live. HTML tests are desktop only; Figma tests on a phone record voice only
Sites
Drop in HTML or a zip, paste a Figma prototype link, or have your own Claude or ChatGPT build and deploy it. Live at name.aeroapp.ai, with versions and rollback
Live
Site extras
Pick your own address, password, favicon, no badge (Basic up). Custom domain and analytics (Solo up)
Live
Agent API and MCP
Coding agents can deploy sites, create tests and read results
Works, but nothing in the app mentions MCP
Figma plugins
User Testing plugin (preview tests, 30 second transcripts)
Live
Responsive
Figma plugin that makes desktop frames mobile
Parked, hidden
Iterate
AI editing in Figma
"Coming soon" placeholder only
**Plans (US prices):** Free $0, Basic $3, Solo $6, Pro $19 a month, 7 day trial on paid plans.
- 
Test sessions: 3 / 5 / 10 / 20, counted as **stored at once**, not per month.
- 
Free sites stay live for 7 days, then show "This site is unavailable". Free recordings are deleted about 14 days after sign-up. The app never says either.
- 
Site counts per plan (1 / 3 / unlimited) are shown but not enforced.
## Competitors
Prices checked Sept to Oct 2026, USD unless stated. Third-party estimates marked ~.
**User testing**
Tool
Cheapest paid
Model
Free plan
What they hide
Maze
No self-serve paid plan since Apr 2026. Enterprise ~$29k/yr median
Sales quote
About 1 study a month, Maze branding
Prototype and mobile testing tagged Enterprise
Lyssna
$166/mo yearly, $199 monthly
Flat, 5 seats
No recordings, 15 responses viewable
Think-aloud recordings only on Growth; panel credits extra
UserTesting
~$25k to $35k/yr
Sales quote
None
Every plan says "Request pricing"
Userbrain
$49/mo, 3 testers
Flat monthly
30 day trial
More testers means upgrading to $249
Useberry
€83/mo, yearly only
Flat, response caps
10 responses a month
Euro only, no monthly billing
Lookback
$299/yr, 10 sessions
Annual only
60 day trial
No monthly option
Ballpark
Enterprise, demo first
Unlimited users
14 day trial
Tests Lovable/v0/Bolt by pasted URL, desktop best
**Hosting prototypes, HTML and AI builds**
Tool
Cheapest paid
Free plan
Catch
Figma Sites
$16/mo Full seat
Can't publish
Still beta; existing prototypes need rebuilding
Framer
$10/site/mo yearly
Subdomain only
Rebuild in Framer; editors $20/mo each
Tiiny.host
$5/mo; custom domain $13 to $18
1 site, banner
Free Claude MCP connector on every plan
Static.app
$6/mo, 2 sites
7 day trial
MCP on paid plans
Vercel
$20/seat/mo
Non-commercial only
Password protection $20 per project a month
Netlify
$9/mo credits
300 credits
Sites pause when credits run out
Cargo
$14/mo yearly
Subdomain
One flat price, little hidden
Also: Bento shut down on 13 Feb 2026, leaving its portfolio users looking for a home.
## The gap Aero can own
- 
**Host it and test it in one link.** No competitor does both. Testers open the same address the designer shares with clients.
- 
**Self-serve testing between $0 and $166.** No sales call, no annual contract, cancel any time. Only Userbrain ($49) and Useberry (€83, yearly) sit anywhere near.
- 
**Recordings on the free plan.** Lyssna's free plan has none. Aero's free plan records screen and voice for 3 sessions.
- 
**Your existing Figma prototype, live as it is.** Figma Sites and Framer both make you rebuild. Aero takes the prototype link.
- 
**Cheap client previews.** Password and custom domain at $6, where Vercel charges $20 a project for passwords.
**Where not to fight:** tester panels, SOC 2, seats and research ops. That is the enterprise game. Aero's line is "bring your own testers": a client, a friend, a classmate.
**MCP is not a moat.** Tiiny gives a free Claude connector on every plan. Aero's agent angle is the loop: an agent deploys, real people test, the insights come back to the agent. Keep it as one of three ways in, not the headline.
## Testing an AI build: how it works today
Most AI builders block their pages from being shown inside another site (checked 22 Oct), so Aero's "any URL" test can't simply wrap them. What works:
You built it in
Can Aero frame the link?
How to test it in Aero today
Claude (artifact)
No, claude.ai blocks it
Ask Claude to publish it to Aero (the one-prompt flow), then create a test on that site
Lovable
The editor no; a published *.lovable.app app often yes
Paste the published link as a URL test, or download the code and upload the zip
v0
Only allows Notion and a few others
Deploy to Vercel and paste that link, or upload the build
Bolt
No
Download and upload the zip
Figma prototype
Yes, through Figma's embed
Paste the prototype link
**What this means:** "Publish to Aero, then test" is the reliable route, and it is exactly the loop no competitor has. Each row is a ready-made SEO page: Test a Claude artifact with real users, Test a Lovable app, and so on. One catch to fix: tests of sites hosted on Aero are desktop only today.
## Aero against each alternative, by job
Job
Aero today
Main alternative (price)
Aero wins
Aero loses
Test a Figma prototype
Screen + voice + transcript + AI notes, $0 to $19
Maze (no paid self-serve), Userbrain ($49), Lyssna ($166)
Price, monthly, recordings on Free
No click paths or heatmaps, no tester panel
Test an AI-built prototype
Publish and test in one place
Ballpark (sales call), Lyssna (paste a URL)
Only tool that hosts it too
Desktop only for hosted sites
Host an HTML file or AI build
Drop, link or prompt; versions
Tiiny (free 1 site forever), Static.app ($6)
Versions, testing, one-prompt publish
Free sites go offline after 7 days
Figma prototype as a live site or portfolio
Paste the link, live in a minute
Figma Sites ($16 seat, beta), Framer ($10/site), Cargo ($14)
No rebuild, cheapest
It's an embedded prototype, not a real web page: slower to load, not found by Google
Client preview with password and domain
Both from $6
Vercel ($20 seat + $20 per project), Tiiny ($13+)
A third of the price
Fewer hosting features (no forms, no server code)
Deploy from an AI agent
REST and MCP, then test
Tiiny MCP (free), Netlify, Vercel
Agent gets real user feedback back
Tiiny's is free and better known
**Bento:** Linktree bought it in 2023 and closed it on 13 Feb 2026, calling it a "planned transition". Links now forward to Linktree. Its users wanted a simple grid portfolio; Aero fits only if they have a Figma design to publish.
## What's wrong today
Checked on the live site (logged out, desktop and phone) and in the code. The first group should be fixed whatever the brand becomes.
**Fix soon, not brand work**
- 
Privacy and Terms pages are blank on both domains. Sign-up links to them.
- 
Homepage FAQ shows "Placeholder copy — final answers to be refined" to visitors; 3 of 4 answers are empty.
- 
Aero pricing lists Figmafolio features: "Free Figmafolio domain", "Removes 'Made with Figmafolio' label", "Free portfolio review".
- 
Pricing never mentions user testing (the 3 / 5 / 10 / 20 sessions), half of what people pay for.
- 
Demo page says the free plan has 5 sessions (it's 3) and uses a different brand ("Aero Usertesting", a blue "A" logo).
- 
"Save 20%" yearly is about 13% on Pro.
- 
Free users aren't told their site goes offline after 7 days, or that recordings are deleted after about 14.
- 
Sign-in footer promises "responsive generation, and AI editing, all in Figma": both are parked.
- 
Share tab says testers "can open it on any device": HTML tests are desktop only.
**Brand and story problems**
- 
Three different Aero looks today: the marketing site (Inter, black headlines), the app (glass, serif "Aero."), the demo ("A" square, Poppins). Nothing is ownable yet.
- 
The homepage leads with AI agents and a terminal command, which shuts out most designers and goes against the July decision.
- 
No product is shown anywhere on the site: no test, no recording, no insight.
- 
Blog: 2 posts, one from 2022 about Figmafolio.
## Strategy
**Position (one line):** Aero puts your prototype online and shows you real people using it, for less than a lunch a month.
**Working headline:** Publish your prototype. Watch people use it. Same link. (A sharper cut of July's locked "Publish prototypes and run real user tests".)
**Three proof points**
- 
**Live in minutes, however you made it.** A Figma prototype link, an HTML file, or a build from Claude, Lovable or v0. One address you can share.
- 
**Watch, then read.** Testers' screen and voice are recorded. Every session comes back as a transcript and the friction points, quoted in their own words.
- 
**Priced for one designer.** Free to start with recordings included. Paid plans from $3 a month, monthly, no call, no contract.
**Who it's for, in order**
Who
What they want
Way in
Page
People who made something but don't know how to host it
Get a Claude, Lovable or HTML page online and share it
One prompt or drag and drop
/sites/html, /sites/claude-artifact
UI and product designers
Quick feedback on a Figma prototype before a review
Paste the prototype link, add tasks
/test/figma-prototype
UX researchers
Cheap unmoderated think-aloud sessions without a Maze contract
Test with screen and voice
/test/think-aloud, /test/maze-alternative
Product managers and founders
See if the thing built with AI makes sense to anyone
Publish and test in one go
/test/ai-prototype
Students and job seekers
A live portfolio or case study, with proof it was tested
Figma prototype as a site
/for/students
Freelancers and small studios
Client previews with a password and their own domain
Sites
/sites/client-preview
**AI's place:** behind the scenes, named at two moments only: "built with your AI tool" on the way in, "transcribed and summarised" on the way out. Never the headline.
**Figmafolio:** stays as its own portfolio product for now. The Aero site mentions it only where it helps ("your Figmafolio account works here").
## Pricing check
**Recommendation: keep the prices, fix how they're told.** Aero is already far below every self-serve competitor, so price isn't the problem; the page is.

Aero Solo
Userbrain
Lyssna
Tiiny (custom domain)
Vercel (password)
Monthly price
$6
$49
$199
$18
$20 seat + $20 per project
Recorded test sessions
10 stored
3 testers a month
Pay per credit
None
None
Hosting, custom domain, password
Yes
No
No
Domain only
Yes
What the pricing page should say that it doesn't today:
- 
How many test sessions each plan holds, and that deleting old ones frees room.
- 
That Free sites stay live for 7 days and Free recordings are kept for about 2 weeks.
- 
The real yearly saving per plan.
- 
"No call, no contract, cancel any time", the line no competitor in testing can say.
Two things to consider later, not now: a session pack for people who need more than 20, and whether Basic ($3) and Solo ($6) are too close to tell apart (support has seen "Basic is premium?" confusion). Regional prices stay exactly as they are.
### Do the limits make sense?
Costs first: a 10 minute test costs about 2.5 cents (transcription is almost all of it; AI notes are about $0.0002). Static hosting is close to free.
Limit today
Problem
Options
Test sessions 3 / 5 / 10 / 20, stored at once
A researcher running 5 people a round fills Pro in 4 rounds, then has to delete old results to keep going. Deleting your research to make room feels wrong
Keep and explain it; or switch to a monthly allowance and keep history (for example 3 / 10 / 30 / 100 a month: Pro's worst case costs about $2.50 of its $19)
Free sites go offline after 7 days
People searching "host html free" land, publish, and their link dies a week later. Tiiny's free site lasts forever with a banner
Keep 7 days; 30 days; or 1 free site forever with the "Made with Aero" badge (the badge is free advertising)
Site counts 1 / 3 / unlimited
Shown on pricing but never enforced
Enforce them, or drop the numbers and sell on features
Free recordings deleted after about 14 days
Nobody is told
Say it in the app and on pricing, or keep Free recordings 30 days
All of these touch billing rules, so nothing changes without your go-ahead.
## Website and SEO
**Use-case pages, not country pages.** HeyBooking needed /hk/ and /ph/ because its customers search locally. Aero's search by job to be done, in English, worldwide. One site, USD by default, regional prices still shown at checkout.
Each page answers one search, built from PRODUCT.md so it stays true. Competition is a rough read of who ranks today, not keyword-tool volumes.
Page
Search it answers
Competition
Who ranks now
/test/ai-prototype
test lovable / v0 / bolt prototype with users
Low
Ballpark docs, a few blogs
/test/figma-prototype
test figma prototype with users
High
Maze, Userbrain, Great Question
/test/maze-alternative
maze alternative, cheap maze alternative
Medium, rising
Listicles from competitors
/test/think-aloud
screen and voice recording usability test
Low to medium
Lyssna, UXtweak
/sites/figma-prototype
publish figma prototype as website, share without login
Medium
Figma forum threads
/sites/html
host html file free
High
Static.app, sharable.link
/sites/claude-artifact
share claude artifact as website
Medium
Tiiny, Static.app
/sites/client-preview
password protect html page
Medium
Hostsmith, StatiCrypt
/sites/figma-sites-alternative
figma sites alternative
Low to medium
Siter.io
/for/students
figma portfolio website, bento alternative
High / short-lived
Figma, uxdesign.cc
/agents
mcp server deploy website
Low to medium
Netlify, Tiiny
**Order to build:** the low-competition testing pages first (AI prototype, think-aloud, Maze alternative), because that's where Aero is unique and the field is empty. Hosting pages second: they bring volume, then hand people to testing.
Every page gets FAQ and SoftwareApplication schema, a real screenshot or feature card, and no fake testimonials or metrics.
## Decisions
Decided 22 Oct 2026.
Question
Decision
Homepage lead
The loop. Headline "Publish your prototype. Watch people use it. Same link." Hero shows one prompt going live, then a test on it
Free sites
Keep the 7 day window. Say it clearly on pricing and in the app
Test sessions
Switch to a monthly allowance and keep history (proposed 3 / 10 / 30 / 100 a month, numbers to confirm when built)
Upload your own video for analysis
Later, after the rebrand: hidden inside a test, paid plans only, capped at about 60 minutes, consent checkbox
Fix-soon list
Fix now as separate small changes, each approved by Duane
Site counts per plan
Enforce them. People already over keep their sites and can't add more until they upgrade or delete
Scope of the passes
Website and the app dashboard and first-run
Pro extras
Keep priority support, drop the portfolio review
About page and founder
No founder or "one person" on the site. If an About page helps SEO: made by UX and UI designers with backgrounds in airline, banking and travel apps; no names or locations
Code shared with Figmafolio
Change Aero files freely; flag anything shared before merging (Clark owns Figmafolio)
Next: step 3, art direction. 4 to 6 directions as full mini pages, stacked, for Duane to pick from.
## Sources
Internal: the figmaApp code (feature and plan inventory), the live aeroapp.ai and app.aeroapp.ai pages captured 22 Oct 2026, and past project decisions from July 2026 (headline, no AI lead, Astro stays, regional pricing). Maze's prices are third-party estimates; its own page shows no numbers.
- 
Maze pricing changes (PricingSaaS)
- 
Maze pricing 2026 (Koji)
- 
Lyssna pricing
- 
UserTesting plans
- 
UserTesting pricing 2026 (Koji)
- 
Userbrain pricing
- 
Useberry
- 
Lookback pricing 2026 (Koji)
- 
Ballpark pricing
- 
Ballpark: test AI prototypes
- 
Figma Sites
- 
Figma Sites custom domains (CMSWire)
- 
Framer website builder
- 
Tiiny.host: host a Claude artifact
- 
Static.app: Claude hosting
- 
Vercel Pro plan
- 
Netlify pricing and limits
- 
Cargo rates
- 
Bento shutting down (AlternativeTo)
- 
Great Question: Lovable user testing