# Costs and keys

The system is built so you decide every dollar. You set a hard spend cap at intake; every paid call is estimated and counted against it first; Claude stops and asks rather than passing it.

## What is free

Anything Claude does itself runs on your Claude subscription: customer patterns, the ICP interview, audience discovery, signal research, scoring, ranking, segmentation, personalization, all copy, reply classification, qualification, account notes and the weekly review. Per-row bulk work is sent to the small model (Haiku) in batches to keep usage low.

## What costs money

| Stage | Provider | What you pay for | Notes |
|---|---|---|---|
| 3 lookalike-research | DiscoLike | $0.10 per API call + $2.00 per 1,000 records. About $1.50 for 500 companies | Optional. Without a key, stage 7 runs its own lookalike pass |
| 4 audience-discovery | GetLeads | Nothing. Page size and price lookups are free | |
| 5 follower-scrape | GetLeads (prepaid wallet cash) | $0.0035 per follower, **2,500 minimum = $8.75 per page** | You pay in the GetLeads app; the CSV arrives by email. Leads that do not match your filters are refunded after delivery. **Check your wallet's auto top-up setting before buying** |
| 7 targeted-search | Prospeo + OpenAI | Prospeo company search credits; the AI judge on a nano model is roughly $1 to $3 per 10,000 companies | Narrow the pull with headcount and geography to save money, never by skipping the judge |
| 8 contact-enrichment | GetLeads plan credits, Blitz, Prospeo | GetLeads: 1 credit per contact returned or enriched. Prospeo people search is the most expensive and runs last | Cost-ordered waterfall: cheapest source first |
| 8 email verification | MillionVerifier | Per address verified | Required before sending. A provider saying "verified" is not enough |
| 9 buying-signals | GetLeads (optional) | 1 credit per funding or acquisition record | Web research alternative is free |

Prices are what the providers quoted when this was written. Claude confirms the live price with the provider's own lookup before every purchase and shows it to you.

A realistic small test: one follower page ($8.75) plus a few dozen enrichment credits. The first live test of this system pulled 27 leads with 27 GetLeads credits and no cash.

## Keys

Put them in `.env` at the repo root (`cp .env.example .env`). Never commit it, never paste a key into the chat. Claude checks whether a key is set without reading its value.

| Key | Needed for | Without it |
|---|---|---|
| `PROSPEO_API_KEY` | Stage 7 account search, stage 8 people search | The account lane cannot run. Use the audience lane or bring your own list |
| `OPENAI_API_KEY` | Stage 7 AI judge, stage 12 batch classifier | Small lists are judged and classified by Claude sub-agents instead |
| `MILLIONVERIFIER_API_KEY` | Verifying emails before sending | Emails stay `unverified` and must not be sent. LinkedIn outreach is unaffected |
| `DISCOLIKE_API_KEY` | Stage 3 | Stage 3 is skipped |
| `GETLEADS_API_KEY`, `BLITZ_API_KEY`, `EXA_API_KEY`, `PARALLEL_AI_API_KEY` | Extra sources inside the account engine | Each is skipped with a log line; the run continues |
| `SMARTLEAD_API_KEY` | Stage 17 reading replies directly | Export replies from any sender as `17-replies-raw.csv` instead |

The **GetLeads MCP server** (hosted, OAuth) is separate from the API key. It powers audience sizing, follower purchases, contact search and LinkedIn-to-email enrichment from inside Claude Code.

Also needed for the account engine: Node.js 18+ (`npx tsx`). For the run checker: [`uv`](https://docs.astral.sh/uv/).

## How the cap behaves

- No cap, no paid stage. `state.json` must hold `spend_cap_usd`.
- Before a paid call Claude adds the estimate to `spent_usd`. If that would pass the cap it stops and asks you. It will not split a purchase to slip under the cap and will not loop around a provider limit.
- Provider-side charges you set up yourself (for example a wallet auto top-up) are outside the system's view. Claude warns you when a purchase will trigger one.
- `uv run scripts/check_run.py runs/<run>` fails loudly if spend is over cap.
