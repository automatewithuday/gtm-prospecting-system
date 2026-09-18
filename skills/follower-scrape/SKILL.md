---
name: follower-scrape
description: "Use when stage 5 of the prospecting system needs the people behind the selected audiences collected — LinkedIn page followers via GetLeads, post engagers, community members, or event attendees — with the source of every person preserved. Also use when the ask is \"get me the followers of this company page\"."
license: MIT
compatibility: Follower collection needs the GetLeads MCP server (hosted, OAuth) and prepaid GetLeads wallet cash. CSV import needs nothing.
metadata:
  author: automatewithuday
  source: martechs.io
---

# Follower Scrape

Collects the raw audience. It does not judge fit — that is stage 6 — and it never drops the label saying where a person came from.

## Pipeline contract

**Stage 5 of 20.** Reads `04-audiences.csv` (rows with `selected=true`). Writes one file per audience to `05-audience-raw/<audience_type>-<name-slug>.csv`.

Files live in `runs/<run>/`. Column definitions: [`/prospecting-system`](../prospecting-system/SKILL.md).

Every output row gets `source_type` and `source_detail` added:

| Collected how | `source_type` |
|---|---|
| follows a LinkedIn page | `follower` |
| reacted to or commented on a post | `engager` |
| member of a community | `member` |
| registered for or attended an event | `attendee` |

A follower is a weaker signal than an engager. Keep them distinct; stage 11 ranks on it.

## Route A — LinkedIn page followers (GetLeads)

Works the same for competitor, tool, and event pages: each is a LinkedIn company page.

1. `lookup_company_linkedin_followers` with the page URL and the ICP filters (`company_sizes`, `seniorities`, `countries` from `02-client-profile.yaml`). Free. Billing is on the requested count; non-matching leads are refunded after delivery.
2. Show the human: follower count, price, and the run's remaining spend cap. **Ask how many followers to buy and which email receives the CSV.** Minimum order is 2,500 leads ($8.75); smaller pages are billed the minimum.
3. Add the cost to `spent_usd` in `state.json`. If it would pass the cap, stop and ask.
   Also call `get_wallet_balance`: if the purchase would drop the wallet below an enabled auto top-up threshold, tell the human the card will be charged the top-up amount as well. That charge is outside the run's cap.
4. `prepare_company_followers_checkout` returns a payment link. **The human pays in the GetLeads app** — do not attempt checkout yourself.
5. The CSV arrives by email. The human saves it to `05-audience-raw/`. Mark the stage `blocked` with note `waiting for follower CSV: <page>` until it lands, and carry on with the account lane (stages 3 and 7) meanwhile.

One page first. Run its CSV through stage 6 on a sample before buying the next page — if the judge rejects most of it, the page was wrong, and buying its siblings repeats the mistake.

## Route B — Post engagers

People who commented on or reacted to a competitor's posts. Two options:

- GetLeads MCP `scrape_linkedin_post_once` for a specific post (`estimate_scrape_cost` first; wallet cash).
- The full harvester with scoring: [linkedin-competitor-icp-scorer](https://github.com/automatewithuday/linkedin-competitor-icp-scorer) (Apify). Drop its `ranked_engagers.csv` into `05-audience-raw/` and keep `comment_excerpt` — stage 13 uses it.

## Route C — CSV import (communities, events, anything else)

Member exports, attendee lists, sponsor-provided lists, a Reddit author pull. Save the file to `05-audience-raw/` as-is and add `source_type` + `source_detail`. Only import lists you are permitted to use for outreach; note where each came from in `source_detail`.

## Rules

- Never edit or trim a raw file. Normalizing and deduping happen in stage 6.
- No purchase without the human saying yes to that specific page and count.
- A paid stage whose output file exists is never re-run.
