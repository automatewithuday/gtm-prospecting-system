---
name: audience-filter
description: "Use when stage 6 of the prospecting system has a raw audience — page followers, post engagers, community members, event attendees, or discovered companies — and the ICP judge prompt has to be built, tuned with a human, and applied before any money is spent on enrichment. Also use when a list came back with obvious bad fits."
license: MIT
metadata:
  author: automatewithuday
  source: martechs.io
  ported_from: GTM-Skills/skills/icp-prompt-builder/SKILL.md
---

# ICP Prompt Builder

## Pipeline contract

**Stage 6 of 20.** Reads `05-audience-raw/*.csv` and `02-client-profile.yaml`. Writes `06-judge-prompt.txt` and `06-audience-qualified.csv`.

- Normalize every raw CSV to the lead columns in [`/prospecting-system`](../prospecting-system/SKILL.md) first. Keep `source_type` (follower / engager / member / attendee) and `source_detail` (which page) on every row.
- Dedupe by `linkedin_url`, else `domain+first_name+last_name`, BEFORE judging. A person following three competitor pages is one row with three sources — that overlap is a signal, keep the count in `source_count`.
- Drop rows whose company is in `excluded_domains`.
- The judge sees people here, not only companies: title + company description. Same 10-row approval loop.
- Output adds `qualified` (true/false), `judge_reason`. Rejected rows stay in the file.

Files live in `runs/<run>/`. Column definitions: [`/prospecting-system`](../prospecting-system/SKILL.md). Standalone use: ignore this block.


Before you pay to pull 5,000 companies, tune a qualification prompt on 10-50 of them. This skill walks you through the iterative loop.

## Why this exists

List-builder skills (DiscoLike, Blitz, Prospeo, Google Maps) return COMPANIES, but they don't know whether those companies match your ICP. If your list-builder returns 5,000 companies and 80% are wrong fits, you'll waste money enriching them for emails that go nowhere.

The fix: build an AI qualification prompt BEFORE scaling. Pull 10 companies, have the prompt score them, compare to your judgment, refine, repeat. Once the prompt agrees with you 2 rounds in a row with zero corrections, lock it in and apply it at scale.

## Always uses Task sub-agents (no API key)

This skill runs entirely inside Claude Code via the Task tool. No Anthropic SDK calls, no OpenAI calls — Claude Code does the scoring itself. This is intentional:

- **No extra API spend.** Uses your Claude Code plan.
- **No key management.** Works out of the box.
- **Scaleable within reason.** For 20-100 evaluations, parallel Task sub-agents batch 10-20 companies per agent.

At very large scale (5,000+ companies per batch), you may want to export the tuned prompt and run it through the OpenAI / Anthropic API with parallelism for speed. But TUNING happens inside Claude Code.

## The loop (8 steps)

### Step 1 — Gather ICP context

Claude asks the user (or reads `client-profile.yaml` from [`/icp-definition`](../icp-definition/SKILL.md)):
- Website of the client selling (to scrape for context)
- Who IS a good customer? What makes them a good fit?
- Who is NOT a good customer? What disqualifies them?
- Any specific signals? (B2B only, revenue range, tech stack, hiring status, recent fundraise, etc.)
- Any HARD disqualifiers? (competitor domains, existing customer domains, certain industries/geographies)

### Step 2 — Select 10 test companies

Pull 10 companies from the list-builder output:
- Mix likely-good and likely-bad fits
- Variety in industry, size, location
- Each company needs at minimum: `domain, company_name, industry, headcount, description`
- Richer fields (Clay-derived: Business Type, Scale Scope, Revenue) make scoring better

### Step 3 — Build the initial qualification prompt

Template:

```
You are an ICP evaluator for {CLIENT_NAME}.

## Target ICP
{ICP description from user or client-profile.yaml}

## Qualification criteria (MUST be true)
- {criterion 1}
- {criterion 2}
- ...

## Disqualification criteria (ANY match = disqualify)
- {disqualifier 1}
- {disqualifier 2}
- ...

## Input
You will receive a company with these fields:
- domain, name, industry, headcount, description
- (optional) Business Type, Revenue, Scale Scope

## Output
For each company, return JSON:
{
  "qualified": true | false,
  "confidence": 0.0-1.0,
  "reason": "one-sentence explanation"
}
```

### Step 4 — Run the prompt on the 10 companies

Via the Task tool. Launch one Task sub-agent that reads the prompt + 10 companies, returns 10 JSON scores.

### Step 5 — Present results to the user

Format as a table:

```
Company                   | Qualified | Conf | Reason
--------------------------+-----------+------+----------------------------------------
acme-corp.com             | YES       | 0.92 | B2B SaaS, 200 employees, target industry
random-nonprofit.org      | NO        | 0.95 | Nonprofit, not a business customer
edge-case-company.com     | YES       | 0.55 | Could fit but revenue model unclear
```

### Step 6 — Collect user feedback

Ask specifically:
- Which evaluations are wrong? (e.g., "acme-corp should be NO because they're a competitor")
- Which are right but for the wrong reason?
- Any patterns the prompt missed?
- Any new disqualifiers to add?

If the user has zero corrections, log this round as "approved."

### Step 7 — Refine the prompt (or move on)

If the user gave corrections:
- Add/remove qualification criteria
- Tighten/loosen disqualifiers
- Add specific examples of edge cases ("companies like X are NOT a fit because Y")
- Adjust confidence thresholds if everything is coming back 0.5

Then go back to Step 4 with a NEW batch of 10 companies.

### Step 8 — Stop condition + save

The loop ends when **2 consecutive rounds have zero corrections from the user**. When that happens:

1. Save the final tuned prompt to `~/cold-email-ai-skills/profiles/<business-slug>/icp-prompt.txt`
2. Append metadata to `client-profile.yaml`:

```yaml
icp_qualification_prompt:
  path: profiles/<slug>/icp-prompt.txt
  tuned_at: YYYY-MM-DD
  rounds_to_convergence: 3
  final_batch_size: 10
```

3. Print a one-liner for the next skill:

```
Prompt locked. To score your 5000 companies:
  npx tsx ~/cold-email-ai-skills/skills/icp-prompt-builder/scripts/score-batch.ts \
    --prompt-file=profiles/<slug>/icp-prompt.txt \
    --companies=path/to/companies.csv \
    --out=scored.csv
```

## Approval-loop rules (important)

- **Never auto-approve.** Even if the prompt looks right, require the user to explicitly say "approved" or give zero corrections for 2 consecutive rounds.
- **Reset counter on any correction.** One correction resets the streak to 0.
- **Don't skip the batches.** Running 30 companies all at once feels faster but masks errors. 10 at a time is the right batch size — small enough to eyeball.
- **Show the prompt each round.** After each refinement, display the current full prompt back to the user so they can see what changed.
- **Always use Task tool sub-agents** for the scoring inside each round. Never call external APIs.

## Using the tuned prompt at scale

Once saved, the prompt is applied to the full list via `scripts/score-batch.ts`. Options:

**Option A (free, slow)** — run through Claude Code Task sub-agents in batches of 20 companies per agent. Good for <500 total.

**Option B (paid, fast)** — export prompt + companies to OpenAI / Anthropic API with parallelism. Good for 500-50,000.

The script supports both. Default is Option A to keep everything inside Claude Code.

## Recommended flow

1. [`/icp-definition`](../icp-definition/SKILL.md) → produce `client-profile.yaml`
2. [`/lookalike-research`](../lookalike-research/SKILL.md) OR [`/blitz-list-builder`](https://github.com/automatewithuday/GTM-Skills/tree/main/skills/blitz-list-builder) OR [`/prospeo-full-export`](https://github.com/automatewithuday/GTM-Skills/tree/main/skills/prospeo-full-export) → pull a sample of 50-100 companies
3. [`/audience-filter`](../audience-filter/SKILL.md) → tune qualification prompt on that sample (3-5 rounds typical)
4. Scale the list-builder to 5,000+ companies
5. Apply the tuned prompt to the full list → only keep `qualified: true` with `confidence >= 0.6`
6. [`/blitz-list-builder`](https://github.com/automatewithuday/GTM-Skills/tree/main/skills/blitz-list-builder) or `/email-waterfall` on the qualified subset
7. Upload to Smartlead

## Data points the prompt can use

From most list-builder outputs:
- domain, company_name, industry, headcount, description, LinkedIn URL

Additional fields (if enrichment skills have been run):
- Business Type (B2B / B2C / B2B2C)
- Annual Revenue range
- Scale Scope (Enterprise / Mid-Market / SMB)
- SubIndustry (more specific than primary industry)
- Tech stack (Clearbit, BuiltWith data)
- Recent signals (funding, hiring, news)

Tell the AI about the fields you have access to in the prompt preamble.

## Common mistakes

- **Building the prompt too tight on round 1.** Start broad, narrow with feedback.
- **Not including negative examples.** "Companies like Netflix are NOT a fit because they're B2C" is more powerful than generic "must be B2B".
- **Using only "qualified: true/false" without confidence.** Always ask for confidence — 0.5-0.7 borderline cases are where you learn the most.
- **Scoring 50 at once "to save time."** Defeats the point of the loop.
- **Not saving the prompt.** The point of tuning is reuse. If you don't save, you'll re-tune next time.

## Scripts

- `scripts/score-batch.ts` — apply tuned prompt to a CSV of companies

## What to do next

**Apply the tuned prompt to your full list** (the list-building skill you came from — Prospeo, Blitz, DiscoLike, Google Maps, or Competitor Engagers — will walk through this). Then [`/list-quality-scorecard`](https://github.com/automatewithuday/GTM-Skills/tree/main/skills/list-quality-scorecard) to grade the filtered output.

**Or wait:** if the prompt didn't converge within 5 rounds (you kept making corrections), your source data may be too thin. Enrich with more fields (company description, headcount, tech stack) before retrying.

## Related skills

- [`/icp-definition`](../icp-definition/SKILL.md) — run FIRST to produce client-profile.yaml
- [`/lookalike-research`](../lookalike-research/SKILL.md), [`/blitz-list-builder`](https://github.com/automatewithuday/GTM-Skills/tree/main/skills/blitz-list-builder), [`/google-maps-list-builder`](https://github.com/automatewithuday/GTM-Skills/tree/main/skills/google-maps-list-builder), [`/prospeo-full-export`](https://github.com/automatewithuday/GTM-Skills/tree/main/skills/prospeo-full-export) — pull the companies this skill qualifies
- [`/personalization`](../personalization/SKILL.md) — same approval-loop pattern, applied to copy personalization
