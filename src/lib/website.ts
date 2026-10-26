// Aero website: builds each page body from its markup file and its words file.
//
// - src/markup/<page>.html   the page body (layout and the product illustrations)
// - src/data/copy/<page>.json the words. Every element with data-c="key" in the markup gets its text from here at build
//                             time, so changing a word means changing the JSON only.
// - src/data/pages.json        title, description, JSON-LD and body class per page
// - src/data/site.json         header, footer and the shared links (@login, @signup, @privacy, @terms)
// See docs/website/README.md.
import site from "../data/site.json";
import pages from "../data/pages.json";

const MARKUP = import.meta.glob("../markup/**/*.html", { query: "?raw", import: "default", eager: true }) as Record<string, string>;
const COPY = import.meta.glob("../data/copy/**/*.json", { import: "default", eager: true }) as Record<string, Record<string, unknown>>;

export type PageMeta = {
  route: string;
  title: string;
  description: string;
  bodyClass: string;
  jsonld?: unknown[];
};

export const LINKS = site.links as Record<string, string>;

/** "@signup" style shortcuts to real URLs (src/data/site.json links). */
export function link(href: string): string {
  if (href.startsWith("@")) {
    const v = LINKS[href.slice(1)];
    if (!v) throw new Error(`Unknown link ${href} (add it to src/data/site.json)`);
    return v;
  }
  return href;
}

const esc = (s: string) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

/** Look a key up: a flat key first ("hero.h1"), then a path ("p1.facts.0.1"). */
function lookup(copy: Record<string, unknown>, key: string): unknown {
  if (key in copy) return copy[key];
  return key.split(".").reduce<unknown>((o, p) => {
    if (o == null) return o;
    if (Array.isArray(o) && /^\d+$/.test(p)) return o[+p];
    return (o as Record<string, unknown>)[p];
  }, copy);
}

/** Put the words from the copy file into every leaf element marked data-c (a headline keeps its round dot). */
export function applyCopy(html: string, copy: Record<string, unknown>): string {
  return html.replace(
    /<([a-z][a-z0-9]*)((?:\s[^>]*?)?\sdata-c="([^"]+)"[^>]*)>([^<]*)(<span class="hd-dot">\.<\/span>)?<\/\1>/g,
    (all, tag, attrs, key, _text, dot) => {
      const v = lookup(copy, key);
      if (typeof v !== "string") return all;
      const t = dot ? v.replace(/\.$/, "") : v;
      return `<${tag}${attrs}>${esc(t)}${dot || ""}</${tag}>`;
    },
  );
}

export function resolveLinks(html: string): string {
  return html.replace(/href="(@[a-z]+)"/g, (_m, h) => `href="${link(h)}"`);
}

export function getPage(name: string) {
  const html = MARKUP[`../markup/${name}.html`];
  const copy = COPY[`../data/copy/${name}.json`];
  const meta = (pages as Record<string, PageMeta>)[name];
  if (html == null || !copy || !meta) throw new Error(`Website page "${name}" is missing its markup, copy or pages.json entry`);
  return { html: resolveLinks(applyCopy(html, copy)), copy, meta };
}
