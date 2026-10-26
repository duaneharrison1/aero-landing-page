# Aero homepage round on the v3 UI (23 Oct 2026)

You are the website team: art director, marketer, copywriter, UX and UI designer, IA, animator and SEO adviser together. Build the homepage for aeroapp.ai from the real v3 app UI.

## Read first
- `/home/claude/figmaapp/docs/brand/DECISIONS.md`: all of it, especially "next phase, the website", "after the round 5 mockups" and the truth rules.
- `/home/claude/figmaapp/docs/brand/research/conversation-audit.md` sections "Website and IA", "Copy", "Likes and dislikes".
- `/home/claude/figmaapp/docs/brand/TONE_OF_VOICE.md`, `PRICING-FACTS.md` (the ONLY source for plans and prices; keep regional pricing as is), `BRAND.md`.
- The v3 UI: `/home/claude/research/v3/shared/aero.css` (tokens, washes, components), `/home/claude/research/v3/make/pages.html`, `/home/claude/research/v3/review/pages.html`, screenshots in `/home/claude/research/v3/hi/`. Marketing component versions: make m8 and review s7 there.
- What he liked before: A Studio's homepage `/home/claude/research/mockups/studio/home.html` (the base), C Story's quote moment `/home/claude/research/mockups/story/home.html`, D Replay's progress line `/home/claude/research/mockups/replay/home.html`. Screenshots in `/home/claude/research/mockups/review/*-home-*.png`.
- Today's live site is in the repo `/home/claude/aero-landing-page` (Astro) for content, FAQ and pricing wording.

## The page
1. **Nav**: "Aero." logo (Geist 500, blue dot), plain links, ink button. No colour in the nav.
2. **Hero**: a rotating headline: "Publish your [Claude artifact | Figma prototype | Lovable app | HTML site]. Watch people use it." The bracketed part changes every few seconds (calm crossfade or type-in, no gimmick; respects reduced motion; the full sentence is readable to screen readers). Sub line and two buttons (Start free, See an example). Then **one big real app window** (v3 UI, light) on the hero wash with a **short calm loop**: a site is published, then a session arrives and its first quote appears. Truth rules: no moving cursor, no transcript typing live; Claude's UI only as a small separate panel labelled outside Aero if shown at all.
3. **Publish / Test / Review**: three sections, each on its step wash (tokens from aero.css), each showing the real component(s) for that step large and simplified (the marketing versions), with one line of copy each. Use "One prompt and it's live." in Publish, "In their own words." in Review.
4. **A little real context**: C's moment, one example tester on a Sunday morning, her words with the word highlight as it plays back, and D's progress line along the bottom of the hero or the three steps.
5. Versions, sites stay live 7 days on Free (say it clearly), price comparison only if honest.
6. **Pricing** from PRICING-FACTS exactly. **FAQ** (real answers). Footer.
7. Light only. No stock photos; illustration or real UI. No founder or "one person". Never lead with AI ("built with your AI tool", "transcribed and summarised" only).
8. Build so copy, UI and story can change without a rebuild: content in one data block at the top of the file.

Show two hero options (A: app window centred under the headline; B: headline left, app window right, larger, bleeding off the edge) as separate frames, everything else shared. Desktop 1440 and phone 390, no sideways scroll.

## Deliver
- `/home/claude/research/web/home.html` (self-contained apart from Google Fonts; copy aero.css and any assets into `/home/claude/research/web/`), with `?hero=a|b` switching the hero.
- `/home/claude/research/web/NOTES.md`: choices, copy deck (every line), open questions.
- Your own Playwright script in that folder; full-page screenshots at 1440 (2x) and 390 for both heroes into `/home/claude/research/web/shots/`, plus a short MP4 of the hero loop if you can (ffmpeg is available; record frames with Playwright). Look at every screenshot and fix what's broken.
- Work only in `/home/claude/research/web/`. Report back with the files and anything that needs Duane.
