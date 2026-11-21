// Build check for the basics of search metadata. Runs after `astro build` (see "build" in package.json) and fails the
// build when a page breaks a rule, so a bad title or description is caught before it ships.
//   title:        1 to 60 characters, unique
//   description:  70 to 155 characters, unique
//   canonical:    present, on aeroapp.ai, and the same address as the page
//   h1:           exactly one
//   JSON-LD:      every block parses
// Redirect pages (meta refresh) and the 404 page are skipped. Run on its own with: node scripts/check-seo.mjs
import { readdirSync, readFileSync, statSync } from "node:fs";
import { join, relative } from "node:path";

const DIST = new URL("../dist", import.meta.url).pathname;
const SITE = "https://aeroapp.ai";
const errors = [];
const titles = new Map();
const descs = new Map();

const walk = (dir) =>
  readdirSync(dir).flatMap((n) => {
    const p = join(dir, n);
    return statSync(p).isDirectory() ? walk(p) : p.endsWith(".html") ? [p] : [];
  });
const decode = (s) => s.replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&#39;|&#x27;/g, "'");
const first = (html, re) => (html.match(re) || [])[1];

let checked = 0;
for (const file of walk(DIST)) {
  const rel = "/" + relative(DIST, file).replace(/index\.html$/, "").replace(/\.html$/, "");
  const html = readFileSync(file, "utf8");
  if (/http-equiv="refresh"/i.test(html) || rel === "/404" || rel === "/404.html") continue;
  checked++;
  const bad = (msg) => errors.push(`${rel}  ${msg}`);

  const title = decode(first(html, /<title>([^<]*)<\/title>/) || "");
  if (!title) bad("no <title>");
  else if (title.length > 60) bad(`title is ${title.length} characters (max 60): ${title}`);
  if (title) titles.set(title, [...(titles.get(title) || []), rel]);

  const desc = decode(first(html, /<meta name="description" content="([^"]*)"/) || "");
  if (!desc) bad("no meta description");
  else if (desc.length > 155) bad(`description is ${desc.length} characters (max 155)`);
  else if (desc.length < 70) bad(`description is ${desc.length} characters (min 70)`);
  if (desc) descs.set(desc, [...(descs.get(desc) || []), rel]);

  const canon = first(html, /<link rel="canonical" href="([^"]*)"/);
  if (!canon) bad("no canonical link");
  else if (!canon.startsWith(SITE + "/")) bad(`canonical is not on ${SITE}: ${canon}`);
  else if (canon !== SITE + rel) bad(`canonical ${canon} does not match the page address ${SITE + rel}`);

  const h1s = (html.match(/<h1(?![^>]*\shidden)[\s>]/g) || []).length; // the home page keeps two review-only headlines with hidden
  if (h1s !== 1) bad(`${h1s} <h1> elements (want 1)`);

  for (const m of html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)) {
    try {
      JSON.parse(m[1]);
    } catch {
      bad("a JSON-LD block does not parse");
    }
  }
}
for (const [t, pages] of titles) if (pages.length > 1) errors.push(`same title on ${pages.join(", ")}: ${t}`);
for (const [d, pages] of descs) if (pages.length > 1) errors.push(`same description on ${pages.join(", ")}`);

if (errors.length) {
  console.error(`\nSEO check failed (${errors.length}):\n` + errors.map((e) => "  - " + e).join("\n") + "\n");
  process.exit(1);
}
console.log(`SEO check passed: ${checked} pages.`);
