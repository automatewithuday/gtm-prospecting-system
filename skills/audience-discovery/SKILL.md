---
name: audience-discovery
description: "Use when stage 4 of the prospecting system needs the places where buyers like your best customers already gather — competitor pages, adjacent tool pages, communities, and events — found, sized, and ranked before any audience is bought or scraped. Also use when the ask is \"whose followers should we target?\"."
license: MIT
metadata:
  author: automatewithuday
  source: martechs.io
---

# Audience Discovery

Your next customers already follow someone. This skill finds who, and how much it costs to reach that audience, so stage 5 only buys the ones worth buying.

## Pipeline contract

**Stage 4 of 20.** Reads `01-customer-patterns.md`, `02-client-profile.yaml`. Writes `04-audiences.csv`.

Files live in `runs/<run>/`. Column definitions: [`/prospecting-system`](../prospecting-system/SKILL.md).

## Four source types

| `audience_type` | What to look for | How people get collected in stage 5 |
|---|---|---|
| `competitor` | Direct competitors and the vendor your customers replaced | LinkedIn page followers; post engagers |
| `tool` | Software your customers already use that signals the problem exists (from the tech/stack findings in stage 1) | LinkedIn page followers |
| `community` | Slack/Discord groups, subreddits, newsletters, LinkedIn groups your customers' champions are in | member export or CSV import; Reddit authors |
| `event` | Conferences, webinars, meetups your customers attend or sponsor | event LinkedIn page followers; attendee CSV |

## Steps

1. **Start from evidence, not brainstorming.** For each customer in `00-customers.csv`: which competitor did they replace or evaluate, which tools are on their site and job posts, which events do they sponsor or speak at, which communities do their champions mention on LinkedIn. One row of evidence per find.
2. **Expand.** For each evidenced page, find 2–3 siblings (the competitor's competitors, the tool's category peers). Mark these `evidence=inferred`.
3. **Resolve the LinkedIn company page URL** for every competitor, tool, and event row. No page found = leave `linkedin_company_url` blank and keep the row.
4. **Size and price each page** with GetLeads MCP `lookup_company_linkedin_followers` (free lookup; pass the profile's headcount, seniority, and country filters). Record `follower_count` and `est_cost_usd` ($0.0035 per follower, $8.75 minimum per page — confirm against the lookup result, prices change).
5. **Rank.** Prefer pages that are narrow and on-problem over pages that are big. A 4,000-follower niche competitor beats a 900,000-follower platform: the big page costs more and the judge will reject most of it.
6. **Present the table and let the human pick.** Show total cost of the picks against the run's remaining spend cap. Set `selected=true` only on what they chose.

## Output: `04-audiences.csv`

`audience_type, name, url, linkedin_company_url, evidence, evidence_detail, follower_count, est_cost_usd, collection_method, selected`

- `evidence` — `customer` (seen at a named customer) or `inferred`.
- `collection_method` — `getleads_followers`, `post_engagers`, `csv_import`, or `reddit`.

## Gotchas

- A customer's own page is not an audience — its followers are their customers, not yours.
- Skip pages whose followers are mostly job seekers (large employers, recruiters' favourites) unless the judge sample proves otherwise.
- Communities rarely allow member export. Record them anyway: they are where stage 9 finds signals and where stage 13 finds language.
- Do not buy anything in this stage.
