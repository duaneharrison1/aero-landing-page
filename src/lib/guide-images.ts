// Guide pictures: real app screens captured by scripts/guide-images/capture.py (see docs/website/README.md,
// "Guide pictures"). src/data/guide-images.json says which picture goes under which step and gives its alt text;
// src/data/guide-image-files.json (written by the capture script) gives each file's size.
import placements from "../data/guide-images.json";
import files from "../data/guide-image-files.json";

type File = { src: string; width: number; height: number; cut: boolean; dark: boolean };
const FILES = files as Record<string, File>;
const ALT = placements.images as Record<string, string>;
const GUIDES = placements.guides as Record<string, Record<string, string>>;

const attr = (s: string) => s.replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;");

/** The <figure> for one picture, on the step colour's wash. Shown at most at its captured size (files are 2x). */
export function guidePicHtml(id: string, group: string): string {
  const f = FILES[id];
  const alt = ALT[id];
  if (!f || !alt) throw new Error(`Guide picture "${id}" has no file or no alt text (run the capture script, check guide-images.json)`);
  const w = Math.round(f.width / 2);
  const h = Math.round(f.height / 2);
  const cls = ["s-gimg", f.cut ? "cut-b" : "", f.dark ? "dark" : ""].filter(Boolean).join(" ");
  return (
    `<figure class="s-step-pic s-gpic w-${group}">` +
    `<img class="${cls}" src="${f.src}" width="${w}" height="${h}" style="--w:${w}px" alt="${attr(alt)}" loading="lazy" decoding="async">` +
    `</figure>`
  );
}

/** The picture id under a guide's step (1-based), if any. */
export function stepPic(slug: string, step: number): string | undefined {
  return GUIDES[slug]?.[String(step)];
}
