// /llms.txt: a plain-text guide to the site for AI assistants, written as the questions people ask.
// It is built from src/data/guides.json, so a new guide appears here without an edit. The plan and price lines come from
// docs/brand/PRICING-FACTS.md (the only source for plans and limits); update both together.
import type { APIRoute } from "astro";
import { GUIDES } from "../lib/guides";

const SITE = "https://aeroapp.ai";
const MANAGE = new Set([
  "password-protect-a-prototype",
  "put-a-prototype-on-your-own-domain",
  "see-who-visits-your-prototype",
  "roll-back-to-an-earlier-version",
  "update-a-published-site",
]);
const ARTIFACT_LINE =
  "Copy one prompt from Aero into the Claude chat where you made the artifact, and Claude publishes it to its own address.";

const line = (g: (typeof GUIDES)[number]) => `- [${g.title}](${SITE}/guides/${g.slug}): ${g.answer ?? ARTIFACT_LINE}`;
const list = (pick: (g: (typeof GUIDES)[number]) => boolean) => GUIDES.filter(pick).map(line).join("\n");

export const GET: APIRoute = () => {
  const body = `# Aero

> Aero puts a prototype online at its own address, gives you one link to send to testers, and brings back recordings, transcripts and a list of what to fix first. Testers need no account or software. It works with Claude artifacts, ChatGPT canvases, Figma prototypes, Lovable, Bolt and v0 apps, and plain HTML.

## What is Aero for?

People who make prototypes with AI tools or Figma and want to see real people use them. The three steps are Publish, Test and Review.
- [Home](${SITE}/): the three steps and a short demo.
- [Features](${SITE}/features): every feature, grouped by step.
- [Use cases](${SITE}/use-cases): who uses Aero and for what.
- [How Aero turns test sessions into findings](${SITE}/features/how-findings-are-made): how a session becomes a transcript, a summary and a list of problems.

## How do I put a prototype online?

${list((g) => g.group === "publish" && !MANAGE.has(g.slug))}

## How do I manage a published site?

${list((g) => MANAGE.has(g.slug))}

## How do I user test it?

${list((g) => g.group === "test")}

## How do I review the results?

${list((g) => g.group === "review")}

## How much does Aero cost?

Prices are in US dollars, monthly. Full details and a comparison with other tools are on [the pricing page](${SITE}/pricing).
- Free, $0: recordings, transcripts and summaries, 3 test sessions, sites stay live for 7 days.
- Basic, $3: 5 test sessions, your own aeroapp.ai address, password protection, custom favicon, no Aero badge.
- Solo, $6: 10 test sessions, plus a custom domain and site analytics.
- Pro, $19: 20 test sessions, plus priority support.
- Paid plans have a 7-day free trial, no call and no contract. The session numbers are totals on a plan, not monthly allowances.
- Checkout may show a regional price.

## What's new?

- [Blog](${SITE}/blog): dated notes on what changed in Aero.
`;
  return new Response(body, { headers: { "Content-Type": "text/plain; charset=utf-8" } });
};
