---
brand-sync: figmaApp docs/brand is the source. Copy this folder unchanged to aero-landing-page/docs/brand/.
version: 2026-10-24.1
---

# Website round 4 (24 Oct 2026)

Built from Duane's 24 Oct feedback (see DECISIONS.md, "24 Oct 2026: feedback on the homepage rework") and BRIEF.md here.

- `home/`: the homepage. Three-step hero loop (Claude builds Pocket and one prompt publishes it; the test link is sent and Maya tests on her own computer with her voice; the review in dark mode, then Insights), a timeline along the bottom, then Publish (blue), Test (green) and Review (orange) with their own small loops, the Figmafolio strip, use cases, a like-for-like price comparison, a two-column FAQ. Headlines `#p1`, `#p2`, `#p3`.
- `site/`: Features, Pricing, Use cases, Guides, one guide page (Publish a Claude artifact) and the Blog with 10 dated posts.
- `shared/`: the stylesheet with the new step colours and website block, `washes.py`, `glass-v3.js` with the "key light follows + lift" hover, and the logo with the slightly bigger dot. Not yet approved; the app's tokens are unchanged.

Each page keeps its copy in one JSON block at the top. Review page with the hero video and Duane's questions: https://claude.ai/artifact/WVmgopxaz1V7bJQmr2YkDs
