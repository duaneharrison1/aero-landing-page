# CLAUDE.md

Rules for working on the Aero marketing website (aeroapp.ai). Read before making any change.

## What this repo is

The public Aero website, built with Astro and deployed on Vercel. The app (app.aeroapp.ai) is a separate repo, figmaApp (React + Firebase).

## Brand and design system (read before any page, copy or style work)

- `docs/brand/` is a **copy** of the brand folder in figmaApp, which is the source. **Read `docs/brand/DECISIONS.md` first**, then `BRAND.md`, `TONE_OF_VOICE.md` and `DESIGN_SYSTEM_PLAN.md`.
- **Two repos, one design system.** The same brand files (`docs/brand/**`, the tokens CSS and, later, the marketing kit) live in both repos in matching paths. Every synced file starts with a `version:` header. Before editing a synced file here, compare its version with figmaApp's. If figmaApp's is newer, take it first. If you change a synced file here, bump the version and copy it back to figmaApp in the same piece of work. A PR that changes a synced file without its twin is incomplete.
- **Marketing pieces are the real app components** in a demo mode with example data, not hand-drawn copies (see `docs/brand/DESIGN_SYSTEM_PLAN.md`).
- **Truth rules:**
  - Transcripts arrive about a minute after a session; never show them typing live.
  - Browser-tab recordings show no mouse; never show a moving cursor in a replay.
  - Keep Claude's, Figma's and other tools' interfaces visibly separate from Aero's.
  - Example names are made up and labelled "Example".
  - Plans and limits come only from `docs/brand/PRICING-FACTS.md`. Regional prices are intentional; never change currency or pricing logic.
  - No fake testimonials, logos or user counts. No stock photos of people.
- **Copy:** follow `docs/brand/TONE_OF_VOICE.md`. No em dashes, British spelling, sentence case. AI is never the headline. The three steps are Publish, Test, Review.
- When Duane decides something, add a line to `docs/brand/DECISIONS.md` (in figmaApp first, then copy it here).

## Commit rules

- Run `npm run build` before committing; it must pass.
- Work on a `claude/` branch and open a PR. Duane approves every merge.
