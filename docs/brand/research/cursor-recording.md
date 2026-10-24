---
brand-sync: figmaApp docs/brand is the source. Copy this file unchanged to aero-landing-page/docs/brand/.
version: 2026-10-23.2
---

# Can Aero show the tester's cursor? (investigation, 23 Oct 2026)

Duane asked whether Aero can record the tester's mouse, because session replays show none.

## Why it's missing today
- Testers share a **browser tab** (`getDisplayMedia` with `displaySurface: "browser"`, `preferCurrentTab: true` in `WelcomeFlow.js`; the tab picker in `UTHtmlController.js`).
- A tab recording is the page's own pixels. The mouse pointer is drawn by the operating system on top, so it isn't in the tab's picture.
- The browser reports the cursor setting through `track.getSettings().cursor` (`always`, `motion` or `never`), but it is read-only; there is no way to ask for it. Window and full-screen captures can include the pointer, tab captures don't. ([MDN, Screen Capture API](https://developer.mozilla.org/docs/Web/API/Screen_Capture_API))
- Nothing else tracks the mouse. The HTML overlay script only sends hello, task-done and finish.

## Options

### 1. HTML sites hosted on Aero: full cursor and clicks (recommended first)
- `api/site.js` already injects `src/ut-overlay` into every page of a site served for a test, and the overlay already talks to the controller page with `postMessage` (`source: 'aero-ut'`).
- Add to the overlay:
  - pointer moves (throttled to about 20 a second)
  - clicks and taps
  - scroll position
  - the viewport size
  - each with a timestamp
- The controller lines the timestamps up with the recording's start and saves the track as one compact JSON file next to the recording (not one Firestore write per move).
- The replay draws a cursor and click ripples over the video, scaled from the viewport to the video size.
- **Extras it unlocks:**
  - misclick and rage-click markers on the timeline
  - "clicked here" next to friction points
  - a click heatmap later
- **Limits:**
  - only on Aero-hosted HTML sites, not external URLs
  - iframes inside the prototype from other domains are blind spots
- **Effort:** medium (overlay, controller buffer and upload, player overlay). No change to what testers are asked for.

### 2. Figma prototypes: clicks and screen changes, not movement
- Today's embed is the legacy `www.figma.com/embed?embed_host=share` (`src/utils/figmaEmbedUrl.js`), which sends no events.
- Figma's Embed API ([docs](https://developers.figma.com/docs/embeds/embed-api)) sends `MOUSE_PRESS_OR_RELEASE` and `PRESENTED_NODE_CHANGED` to the page that embeds it. The click events include:
  - `handled`: whether the click hit a hotspot
  - the target layer
  - a position relative to that layer
- The Embed API needs a Figma OAuth app's **client id** on the embed URL, and Aero's origin added as an allowed embed origin.
- **Limits:**
  - There are no move events.
  - Positions are relative to the clicked layer, not the screen, so drawing an exact cursor needs extra mapping.
  - A Figma forum thread reports the position fields coming back null in some prototypes ([thread](https://forum.figma.com/ask-the-community-7/embed-kit-2-0-mouse-press-or-release-returns-null-positions-36790)).
- **What it still gives, reliably:**
  - a **click path** ("Home → More → Cards")
  - **misclicks**: clicks that hit nothing, a strong friction signal
  - screen names on the timeline
- **Effort:** medium, plus setting up the Figma OAuth app. Test with several real prototypes first.

### 3. Ask testers to share a window or the whole screen
- The pointer then appears in the video with no code.
- **Costs:**
  - a more confusing picker
  - more privacy exposure (other tabs, notifications)
  - for Figma tests, the embed tab would no longer be preselected
- Not recommended as the default. It could be an option for moderated or trusted testers.

## Recommendation
1. Build option 1 for HTML sites. It is the most complete, and it uses a channel that already exists.
2. Prototype option 2 to get click paths and misclicks for Figma.
3. Until either ships, every mockup, video and page stays true to the app: no moving cursor in a replay.

## How the Figma Embed API would work in Aero (added 23 Oct)
- **For designers:** nothing changes. They paste the same prototype link, and Aero rewrites `figma.com/proto/FILE/Name?node-id=…` to `embed.figma.com/proto/FILE/Name?node-id=…&embed-host=aero&client-id=AERO_ID`.
- **One-time setup by Duane:**
  - create a free OAuth app at figma.com/developers/apps
  - copy its client id into Aero's config
  - add aeroapp.ai as an allowed embed origin
- No per-user Figma login. Viewing rules are as today: link-viewable files embed; private files show Figma's login, and the embed sends `LOGIN_SCREEN_SHOWN`, so Aero can warn the designer.
- **Events:**
  - `PRESENTED_NODE_CHANGED`: screen path with times
  - `MOUSE_PRESS_OR_RELEASE` with `handled`: hits and misclicks
  - `NEW_STATE`: component variants
  - `INITIAL_LOAD`, `LOGIN_SCREEN_SHOWN`, `PASSWORD_SCREEN_SHOWN`
- **Commands:** `RESTART`, `NAVIGATE_TO_FRAME_AND_CLOSE_OVERLAYS`, `NAVIGATE_FORWARD`, `NAVIGATE_BACKWARD`, `CHANGE_COMPONENT_STATE`. Useful to start each task on the right screen.
- **Gaps:**
  - Events carry node ids, not frame names. Names need the REST API with the designer's Figma access. The lighter alternative is a thumbnail taken from Aero's own recording at each screen change.
  - Click positions are relative to the clicked layer and sometimes null, so misclicks become timeline markers, not exact dots on the video.
- **Rollout:** behind a flag. Test with several real prototypes. Fall back to the legacy embed if `INITIAL_LOAD` never arrives.
