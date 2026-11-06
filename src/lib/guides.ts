// Task guides (SEO pages): one data file, one template. See docs/website/README.md, "Guides".
import data from "../data/guides.json";

export type GuideStep = { name: string; text: string };
export type Guide = {
  slug: string;
  group: "publish" | "test" | "review";
  title: string;
  /** Present only on guides that keep their own hand-built page (publish-a-claude-artifact). */
  existing?: boolean;
  metaTitle?: string;
  description?: string;
  answer?: string;
  facts?: string[];
  needs?: string[];
  steps?: GuideStep[];
  alt?: { h: string; p: string };
  gets?: string[];
  faq?: [string, string][];
  related?: string[];
  next?: { slug: string } | null;
  cta?: string;
};

export const GUIDES = data as Guide[];
export const bySlug = (s: string) => GUIDES.find((g) => g.slug === s);
export const inGroup = (g: "publish" | "test" | "review") => GUIDES.filter((x) => x.group === g);

const tick = '<svg class="i" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m3.5 8.5 3 3 6-7"/></svg>';
const arr = '<svg class="i" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4"/></svg>';
export const ICON = { tick, arr };
export const PILL = {
  publish: '<span class="pill pill-publish"><svg class="i" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M8 13.5v-8M4.5 9 8 5.5 11.5 9M3 2.5h10"/></svg>Publish</span>',
  test: '<span class="pill pill-test"><svg class="i" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 9.5a2.5 2.5 0 0 0 3.5 0l2-2a2.5 2.5 0 0 0-3.5-3.5l-.6.6M9 6.5a2.5 2.5 0 0 0-3.5 0l-2 2A2.5 2.5 0 0 0 7 12l.6-.6"/></svg>Test</span>',
  review: '<span class="pill pill-review"><svg class="i" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2.5 13.5h11M4.5 11V8M8 11V4.5M11.5 11V6.5"/></svg>Review</span>',
};
const esc = (s: string) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
export { esc };

/** A card linking to a guide (used on /guides and under "Related guides"). */
export function cardHtml(g: Guide, withPill = false): string {
  return `<a class="s-gcard${withPill ? "" : " np"}" href="/guides/${g.slug}">${withPill ? PILL[g.group] : ""}<b>${esc(g.title)}</b><span class="s-garr">${arr}</span></a>`;
}

/** HowTo, FAQPage and BreadcrumbList JSON-LD for a guide. */
export function jsonLd(g: Guide) {
  return [
    {
      "@context": "https://schema.org",
      "@type": "HowTo",
      name: g.title,
      description: g.answer,
      step: g.steps!.map((s, i) => ({ "@type": "HowToStep", position: i + 1, name: s.name, text: s.text })),
    },
    {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      mainEntity: g.faq!.map(([q, a]) => ({ "@type": "Question", name: q, acceptedAnswer: { "@type": "Answer", text: a } })),
    },
    {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      itemListElement: [
        { "@type": "ListItem", position: 1, name: "Guides", item: "https://aeroapp.ai/guides" },
        { "@type": "ListItem", position: 2, name: g.title },
      ],
    },
  ];
}
