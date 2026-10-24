---
brand-sync: figmaApp docs/brand is the source. Copy this file unchanged to aero-landing-page/docs/brand/.
version: 2026-10-23.1
---

# Aero design system plan

**Goal (Duane, 23 Oct):** one design system shared by the app, the website, animations and videos. Marketing pieces are simpler versions of the real components and update as the app changes. The structure is built once, so the UI, the story and the copy can change without rebuilding everything.

## Layers

```
1. Tokens        src/styles/aero-design-system.css (+ docs/brand/tokens.json mirror)
                 colour, type, spacing, radius, shadow, motion, glass settings
2. Components    the app's React components (Aero*, Glass*, UT*), built only from tokens
3. Demo mode     the same components rendered with example data: /kit routes in the app
                 (for example /kit/session?scene=pocket). No login, no Firestore.
4. Marketing kit simplified variants of layer 2 (bigger type, hidden chrome, an
                 attention highlight), plus the scenes that animations play
5. Compositions  the homepage, content pages, videos and illustrations, built from 3 and 4
```

- **Scenes are data.** A scene is a JSON file of example data (studio name, site, test, sessions, transcript with word timings, friction points, insights) and a timeline of steps. Copy lives in the scene or page, not in the components.
- **Animations are timelines over real components.** The same timeline drives the website hero, the MP4 (recorded headless) and still frames. Changing a component updates all three.
- **Videos are rendered, not edited.** A script opens the kit pages in a headless browser, plays the timeline, records, then converts to H.264 with ffmpeg. The script name and the scene are recorded in each video's filename.

## Two repos

The app (figmaApp, React) and the website (aero-landing-page, Astro) are separate repos. Rule agreed 23 Oct:
1. **figmaApp is the source.** Tokens, the marketing kit build and `docs/brand/` live here.
2. **Copy, don't fork.** The website gets copies of the same files (tokens CSS, kit bundle, brand docs, logo) in matching paths.
3. **Every synced file has a `version:` header** (date plus a counter: 2026-10-23.1). Before editing a synced file in either repo, compare versions. If the other repo is newer, port its change back first. After editing, bump the version and copy the file to the other repo in the same piece of work.
4. **Both CLAUDE.md files carry this rule.** A pull request that touches a synced file without its twin is incomplete.

## Truth rules for anything built from the kit
- **Transcripts:** they arrive after the session; never animate typing during recording. A replay may highlight words as the audio plays, because word timings are stored.
- **No moving cursor in replays:** recordings of a browser tab do not show the tester's mouse.
- **Example data:** studio and tester names are made up (never Duane's) and labelled "Example". URLs look real: name.aeroapp.ai, aeroapp.ai/....
- **Third-party apps** (Claude, ChatGPT, Figma, Lovable): show their UI simplified and recognisable, clearly separate from Aero's.
- **No stock photos of people.** Use illustration.

## Order of work (agreed 23 Oct)
1. Tokens and the whole-app UI: every screen, section by section, comparing the best of the round 5 directions side by side, including the tester screen and every variation (no tasks, which tab opens, empty, error, loading).
2. The demo mode and the marketing kit, built from the agreed UI.
3. The website on the kit: homepage, Publish / Test / Review sections, content pages, the scene-by-scene video.
4. The SEO programme of task pages.

## Not decided yet
- Final palette, and the soft gradient per section (Publish, Test, Review).
- How the V3 glass is used inside the app (which buttons, the tester task panel).
- Whether the kit ships as a script loaded from app.aeroapp.ai or as files copied into the website repo. Copying is the agreed default.
