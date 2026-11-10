#!/usr/bin/env python3
"""Capture the guide pictures from the real Aero app.

The pictures on /guides are screenshots of figmaApp's own components, never drawn copies. They come from the
style guide page (/aero, src/pages/AeroShowcase in figmaApp), which renders the real Sites, Tests and Review
components with made-up Example data and no-op handlers, so nothing is read from or written to an account.

How it works:
  1. Builds figmaApp (unless --no-build and a build is already there).
  2. Serves the build on localhost and opens it in Playwright as https://app.aeroapp.ai, so the app takes its
     Aero branch. Every other request (Firebase, fonts from other hosts, analytics) is blocked.
  3. For each shot in SHOTS: opens /aero, finds the frame, does the listed clicks or typing (local state only:
     the style guide's handlers write nothing), and screenshots the listed part at device scale 2.
  4. Saves WebP files under public/guides/ (at most 1440px wide, about 150 KB or less) and their sizes in
     src/data/guide-image-files.json, which the guide pages read.

Run (see docs/website/README.md, "Guide pictures"):
  python3 scripts/guide-images/capture.py --app ../figmaApp            # build the app, then capture all
  python3 scripts/guide-images/capture.py --app ../figmaApp --no-build # reuse figmaApp/build
  python3 scripts/guide-images/capture.py --app ../figmaApp --only site-page,versions

Needs Python 3 with playwright (and its Chromium: python3 -m playwright install chromium) and Pillow.
"""
import argparse
import functools
import http.server
import io
import json
import os
import subprocess
import sys
import threading
import urllib.request

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT_DIR = os.path.join(ROOT, "public", "guides")
DIMS_FILE = os.path.join(ROOT, "src", "data", "guide-image-files.json")
APP_ORIGIN = "https://app.aeroapp.ai"
MAX_W = 1440          # 2x of the widest place a picture is shown (about 720px)
MAX_BYTES = 150_000

# Example links typed into fields. Local state only: nothing is saved.
FIGMA_DESKTOP = "https://www.figma.com/proto/ExAmPle1234/Pocket-example?node-id=1-2"

# Each shot:
#   frame   CSS selector of the style guide frame, with optional has_text / has (a selector inside it) and nth
#   width   frame width in CSS px for this shot (a narrower window; the components lay themselves out)
#   do      steps before the picture: ("click", selector), ("fill", selector, text), ("wait", ms)
#   crop    selectors inside the frame ("FRAME" for the whole frame); the picture is the box around all of them, plus pad
#   right_of  optional: end the picture at this element's right edge (+ right_pad), to leave out a side column
#   max_h   optional: cut the picture at this height (CSS px); the page fades the cut edge
SHOTS = [
    {
        "id": "new-site",
        "frame": {"sel": ".sc-create-frame"},
        "width": 860,
        "crop": [".aero-ph", ".createflow-page-tiles"],
        "pad": 20,
    },
    {
        "id": "new-site-prompt",
        "frame": {"sel": ".sc-create-frame"},
        "width": 860,
        "do": [("click", 'button:has-text("From Claude or ChatGPT")'), ("wait", 1200)],
        "crop": [".createflow-page-panel"],
        "pad": 16,
    },
    {
        "id": "new-site-upload",
        "frame": {"sel": ".sc-create-frame"},
        "width": 860,
        "do": [("click", 'button:has-text("Upload HTML")'), ("wait", 800)],
        "crop": [".createflow-page-panel", ".createflow-solo-actions"],
        "pad": 16,
    },
    {
        "id": "new-site-figma",
        "frame": {"sel": ".sc-create-frame"},
        "width": 860,
        "do": [
            ("click", 'button:has-text("From Figma")'),
            ("wait", 800),
            ("fill", 'input[placeholder^="https://www.figma.com"] >> nth=0', FIGMA_DESKTOP),
            ("wait", 600),
            ("click", 'button:has-text("Add breakpoint")'),
            ("wait", 400),
            ("click", '[role="menuitem"]:has-text("Phone"), button:has-text("Phone")'),
            ("wait", 600),
            ("blur",),
        ],
        "crop": [".createflow-page-panel"],
        "pad": 16,
    },
    {
        "id": "new-test",
        "frame": {"sel": ".sc-tests-frame", "has_text": "What do you want to test?"},
        "width": 860,
        "crop": [".aero-ph", ".createflow-page-tiles"],
        "pad": 20,
    },
    {
        "id": "site-page",
        "frame": {"sel": ".sc-sites-frame", "has": ".aero-sd-tabs", "nth": 0},
        "width": 1100,
        "crop": [".aero-ph", ".aero-sd-tabs", ".aero-sd-side .aero-sr-head", ':text("Preview updated")'],
        "pad": 16,
    },
    {
        "id": "versions",
        "frame": {"sel": ".sc-sites-frame", "has": ".aero-sd-tabs", "nth": 0},
        "width": 1100,
        "do": [("click", '.aero-sd-tab:has-text("Versions")'), ("wait", 800)],
        "crop": [".aero-ph", ".aero-sd-tabs", ".aero-sd-main"],
        "right_of": ".aero-sd-main",
        "right_pad": 24,
        "pad": 0,
    },
    {
        "id": "analytics",
        "frame": {"sel": ".sc-sites-frame", "has": ".aero-sd-tabs", "nth": 0},
        "width": 1100,
        "do": [("click", '.aero-sd-tab:has-text("Analytics")'), ("wait", 1000)],
        "crop": [".aero-ph", ".aero-sd-tabs", ".aero-sd-main"],
        "right_of": ".aero-sd-main",
        "right_pad": 24,
        "pad": 0,
        "max_h": 640,
    },
    {
        "id": "password",
        "frame": {"sel": ".sc-sites-frame", "has": ".aero-sd-tabs", "nth": 0},
        "width": 1100,
        "crop": ['.aero-sr-row:has-text("Visitors enter it once")'],
        "pad": 20,
    },
    {
        "id": "domain",
        "frame": {"sel": ".sc-sites-frame", "has": ".aero-sd-tabs", "nth": 0},
        "width": 1100,
        "do": [("fill", 'input[aria-label="Your own domain"]', "app.example.com"), ("wait", 400)],
        "crop": [".aero-sr-group:has-text(\"Your own domain\")"],
        "pad": 20,
    },
    {
        "id": "test-link",
        "frame": {"sel": ".sc-tests-frame", "has": ".aero-tlink", "nth": 0},
        "width": 1100,
        "crop": [".aero-tlink", '.aero-sr-row:has-text("Taking new sessions")'],
        "pad": 20,
    },
    {
        "id": "test-setup",
        "frame": {"sel": ".sc-tests-frame", "has": ".aero-tlink", "nth": 0},
        "width": 1100,
        "crop": [".aero-ph", ".aero-sd-tabs", ".aero-stk"],
        "pad": 0,
    },
    {
        "id": "task-edit",
        "frame": {"sel": ".sc-tests-frame", "has": ".aero-tlink", "nth": 0},
        "width": 1100,
        "do": [
            ("click", ".aero-stk-list > li:nth-child(2) .aero-card-menu-btn"),
            ("wait", 400),
            ("page_click", '.aero-card-menu-pop :text-is("Edit")'),
            ("wait", 400),
            ("fill", ".aero-stk-edit .aero-stk-desc", "Start from the account page. Example."),
            ("wait", 300),
        ],
        "crop": [".aero-stk"],
        "pad": 20,
    },
    {
        "id": "sessions",
        "frame": {"sel": ".sc-tests-frame", "has": ".aero-tlink", "nth": 0},
        "width": 820,
        "do": [("click", '.aero-sd-tab:has-text("Sessions")'), ("wait", 800)],
        "crop": [".aero-ph", ".aero-sd-tabs", ".aero-sd-body .aero-card"],
        "pad": 0,
    },
    {
        "id": "review-watch",
        "frame": {"sel": ".sc-review-frame", "has_text": "Watch, dark (the default)"},
        "seek": 0.3,
        "crop": [".aero-rv"],
        "pad": 0,
    },
    {
        "id": "review-timeline",
        "frame": {"sel": ".sc-review-frame", "has_text": "Watch, dark (the default)"},
        "seek": 0.3,
        "crop": [".aero-rv-ctl", ".aero-rv-tl"],
        "pad": 0,
    },
    {
        "id": "review-transcript",
        "frame": {"sel": ".sc-review-frame", "has_text": "Watch, dark (the default)"},
        "seek": 0.3,
        "crop": [".aero-rv-insp"],
        "pad": 0,
        "max_h": 640,
    },
    {
        "id": "review-arriving",
        "frame": {"sel": ".sc-review-frame", "has_text": "Transcript arriving"},
        "crop": [".aero-rv-insp"],
        "pad": 0,
        "max_h": 250,
    },
    {
        "id": "review-read",
        "frame": {"sel": ".sc-review-frame", "has_text": "Read, dark"},
        "crop": [".aero-rv"],
        "pad": 0,
        "max_h": 640,
    },
    {
        "id": "insights",
        "frame": {"sel": "[data-shot=insights]"},
        "width": 1000,
        "do": [("page_click", '.sc-ins-pills button:has-text("Example, up to date")'), ("wait", 1200)],
        "crop": ["FRAME"],
        "pad": 0,
        "max_h": 720,
    },
]


class _Handler(http.server.SimpleHTTPRequestHandler):
    """Static files with the single-page fallback (every unknown path is index.html)."""

    def log_message(self, *a):
        pass

    def send_head(self):
        if not os.path.exists(self.translate_path(self.path)):
            self.path = "/index.html"
        return super().send_head()


def serve(build_dir):
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(_Handler, directory=build_dir))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv.server_address[1]


def save_webp(png_bytes, path):
    im = Image.open(io.BytesIO(png_bytes)).convert("RGB")
    if im.width > MAX_W:
        im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
    for q in (84, 80, 76, 72, 68, 64, 60, 55, 50):
        buf = io.BytesIO()
        im.save(buf, "WEBP", quality=q, method=6)
        if buf.tell() <= MAX_BYTES:
            break
    with open(path, "wb") as f:
        f.write(buf.getvalue())
    return im.width, im.height, buf.tell(), q


def union(boxes):
    x0 = min(b["x"] for b in boxes)
    y0 = min(b["y"] for b in boxes)
    x1 = max(b["x"] + b["width"] for b in boxes)
    y1 = max(b["y"] + b["height"] for b in boxes)
    return {"x": x0, "y": y0, "width": x1 - x0, "height": y1 - y0}


def shoot(page, port_url, shot):
    page.goto(f"{APP_ORIGIN}/aero", wait_until="domcontentloaded")
    page.wait_for_selector(".sc-sites-frame", timeout=120000)
    page.wait_for_selector(".sc-review-frame", timeout=60000)
    page.wait_for_timeout(2500)
    page.add_style_tag(content="*,*::before,*::after{animation:none!important;transition:none!important;caret-color:transparent!important}")

    fs = shot["frame"]
    loc = page.locator(fs["sel"])
    if fs.get("has_text"):
        loc = loc.filter(has_text=fs["has_text"])
    if fs.get("has"):
        loc = loc.filter(has=page.locator(fs["has"]))
    # Mark the frame, so it stays found after a click changes what is inside it.
    loc.nth(fs.get("nth", 0)).evaluate("el => el.setAttribute('data-guide-shot', '1')")
    frame = page.locator("[data-guide-shot]")
    frame.scroll_into_view_if_needed()
    if shot.get("width"):
        frame.evaluate("(el, w) => { el.style.width = w + 'px'; el.style.maxWidth = 'none'; }", shot["width"])
        page.wait_for_timeout(400)

    for step in shot.get("do", []):
        kind = step[0]
        if kind == "click":
            frame.locator(step[1]).first.click()
        elif kind == "page_click":
            page.locator(step[1]).first.click()
        elif kind == "fill":
            frame.locator(step[1]).first.fill(step[2])
        elif kind == "fill_empty":
            inputs = frame.locator(step[1])
            for i in range(inputs.count()):
                if not inputs.nth(i).input_value():
                    inputs.nth(i).fill(step[2])
                    break
        elif kind == "blur":
            page.evaluate("document.activeElement && document.activeElement.blur()")
        elif kind == "wait":
            page.wait_for_timeout(step[1])

    if shot.get("seek") is not None:
        # Move the recording the way an owner would: a click on the timeline track.
        track = frame.locator(".aero-rv-tl-track").first
        bb = track.bounding_box()
        if bb:
            page.mouse.click(bb["x"] + bb["width"] * shot["seek"], bb["y"] + bb["height"] / 2)
            page.wait_for_timeout(1500)
        page.mouse.move(0, 0)  # no hover card in the picture
        page.wait_for_timeout(300)

    frame.scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    boxes = []
    for sel in shot["crop"]:
        b = frame.bounding_box() if sel == "FRAME" else frame.locator(sel).first.bounding_box()
        if not b:
            raise RuntimeError(f"{shot['id']}: nothing matches {sel}")
        boxes.append(b)
    fb = frame.bounding_box()
    r = union(boxes)
    pad = shot.get("pad", 0)
    x0 = max(fb["x"], r["x"] - pad)
    y0 = max(fb["y"], r["y"] - pad)
    x1 = min(fb["x"] + fb["width"], r["x"] + r["width"] + pad)
    if shot.get("right_of"):
        rb = frame.locator(shot["right_of"]).first.bounding_box()
        x1 = min(x1, rb["x"] + rb["width"] + shot.get("right_pad", 0))
    y1 = min(fb["y"] + fb["height"], r["y"] + r["height"] + pad)
    cut = False
    if shot.get("max_h") and y1 - y0 > shot["max_h"]:
        y1 = y0 + shot["max_h"]
        cut = True
    clip = {"x": x0, "y": y0, "width": x1 - x0, "height": y1 - y0}
    if clip["y"] < 0 or clip["y"] + clip["height"] > page.viewport_size["height"]:
        page.evaluate("(y) => window.scrollBy(0, y)", clip["y"] - 40)
        page.wait_for_timeout(300)
        return shoot_clip_again(page, frame, shot, clip, fb)
    return page.screenshot(clip=clip, animations="disabled"), cut


def shoot_clip_again(page, frame, shot, old_clip, old_fb):
    fb = frame.bounding_box()
    dy = fb["y"] - old_fb["y"]
    clip = dict(old_clip, y=old_clip["y"] + dy)
    cut = bool(shot.get("max_h")) and abs(clip["height"] - shot["max_h"]) < 1
    return page.screenshot(clip=clip, animations="disabled"), cut


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--app", required=True, help="path to a figmaApp checkout (its master shows the current UI)")
    ap.add_argument("--no-build", action="store_true", help="reuse <app>/build")
    ap.add_argument("--only", default="", help="comma-separated shot ids")
    args = ap.parse_args()

    app = os.path.abspath(args.app)
    build = os.path.join(app, "build")
    if not args.no_build or not os.path.isdir(build):
        print("Building figmaApp (a few minutes)…")
        subprocess.run(["npm", "run", "build"], cwd=app, check=True, env=dict(os.environ, GENERATE_SOURCEMAP="false"))
    port = serve(build)
    local = f"http://127.0.0.1:{port}"
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

    only = {s for s in args.only.split(",") if s}
    os.makedirs(OUT_DIR, exist_ok=True)
    dims = {}
    if os.path.exists(DIMS_FILE):
        dims = json.load(open(DIMS_FILE))

    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1440, "height": 2400}, device_scale_factor=2,
                                  color_scheme="light", reduced_motion="reduce",
                                  locale="en-GB", timezone_id="Europe/London")

        def route(r):
            u = r.request.url
            if u.startswith(APP_ORIGIN):
                try:
                    res = opener.open(u.replace(APP_ORIGIN, local), timeout=60)
                    r.fulfill(status=200, body=res.read(), headers={"content-type": res.headers.get("Content-Type", "text/html")})
                except Exception as e:  # noqa: BLE001
                    print("  could not serve", u, e)
                    r.abort()
            elif u.startswith("data:") or u.startswith("blob:"):
                r.continue_()
            else:
                r.abort()  # Firebase, analytics, other hosts: nothing leaves the machine

        ctx.route("**/*", route)
        failed = []
        for shot in SHOTS:
            if only and shot["id"] not in only:
                continue
            page = ctx.new_page()
            page.set_default_timeout(8000)
            try:
                png, cut = shoot(page, local, shot)
            except Exception as e:  # noqa: BLE001
                print(f"  {shot['id']}: FAILED {str(e).splitlines()[0]}")
                failed.append(shot["id"])
                page.close()
                continue
            page.close()
            path = os.path.join(OUT_DIR, f"{shot['id']}.webp")
            w, h, size, q = save_webp(png, path)
            dims[shot["id"]] = {"src": f"/guides/{shot['id']}.webp", "width": w, "height": h, "cut": cut,
                                "dark": shot["id"].startswith("review-")}
            print(f"  {shot['id']}: {w}x{h}, {size // 1024} KB (q{q}){', cut' if cut else ''}")
        browser.close()

    with open(DIMS_FILE, "w") as f:
        json.dump(dict(sorted(dims.items())), f, indent=2)
        f.write("\n")
    print(f"Wrote {DIMS_FILE}")
    if failed:
        print("Failed:", ", ".join(failed))
        return 1


if __name__ == "__main__":
    sys.exit(main())
