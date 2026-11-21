// Comparison pages ("alternatives"): one data file, one template. See docs/website/README.md, "Alternatives".
import data from "../data/alternatives.json";

export type Alt = {
  slug: string;
  name: string;
  metaTitle: string;
  description: string;
  h1: string;
  answer: string;
  facts: string[];
  chooseThem: string[];
  chooseAero: string[];
  rows: [string, string, string][];
  notes: string[];
  sources: [string, string][];
  faq: [string, string][];
};

export const ALTS = data as Alt[];
export const altBySlug = (s: string) => ALTS.find((a) => a.slug === s);

export function altJsonLd(a: Alt) {
  return [
    {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      mainEntity: a.faq.map(([q, ans]) => ({ "@type": "Question", name: q, acceptedAnswer: { "@type": "Answer", text: ans } })),
    },
    {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      itemListElement: [
        { "@type": "ListItem", position: 1, name: "Alternatives", item: "https://aeroapp.ai/alternatives" },
        { "@type": "ListItem", position: 2, name: `${a.name} alternative` },
      ],
    },
  ];
}
