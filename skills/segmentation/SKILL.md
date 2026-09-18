---
name: segmentation
description: "Use when stage 12 of the prospecting system needs prioritized leads grouped by use case so each group gets its own angle and copy — segments proposed from the customer patterns, approved by a human, then assigned to every account in one classifier pass. Also use when the ask is \"split this list into segments\"."
license: MIT
compatibility: The batch classifier needs Node.js with tsx and OPENAI_API_KEY. Small lists can be classified by sub-agents with no key.
metadata:
  author: automatewithuday
  source: martechs.io
  wraps: engine/list-builder/scripts/classify-batch.ts
---

# Segmentation

One message for the whole list wastes a good list. This stage splits the list by **why they would buy**, so stages 13–16 write to a use case instead of an industry.

## Pipeline contract

**Stage 12 of 20.** Reads `11-prioritized.csv`, `01-customer-patterns.md`. Writes `12-segments.md` (definitions) and `12-segmented.csv` (adds `segment`, `segment_confidence`, `segment_reason`).

Files live in `runs/<run>/`. Column definitions: [`/prospecting-system`](../prospecting-system/SKILL.md).

## Steps

1. **Propose 2–5 segments from the customers, not from the list.** Each best customer bought for a reason; group those reasons. A segment is a use case + the trigger that makes it urgent ("replacing spreadsheets after a funding round"), not a firmographic bucket ("fintech, 50–200").
2. **Write `12-segments.md`**: for each segment a short label, a one-paragraph definition, which customer(s) it came from, what qualifies, what looks close but belongs elsewhere. Add a `partner` label if vendors or agencies that serve your buyers are in the list — stage 15 treats them differently.
3. **Human approves the segments.** They drive all copy downstream.
4. **Classify accounts, not people** — dedupe to unique `account_domain`, classify once, join back to leads.
   ```bash
   npx tsx engine/list-builder/scripts/classify-batch.ts --csv=<accounts.csv> \
     --prompt-file=<run>/12-segments-prompt.txt --labels=<label1,label2,...> \
     --out=<run>/12-classified.csv --scrape
   ```
   One nano pass assigns each company to ONE segment or `none`, with confidence and reason. `--scrape` fetches the homepage when the description is missing. Under ~200 accounts, or with no OpenAI key, use Haiku sub-agents in batches of 25 with the same prompt.
5. **Check 10 rows per segment by hand** before joining. If a segment is wrong more than it is right, fix the definition and re-run; do not patch rows.
6. **Report** leads per segment and per tier.

## Rules

- `none` is a valid answer. Leads in `none` get bucket copy in stage 13 or sit out; never force a fit.
- A segment with fewer than ~30 leads is not worth its own copy. Merge it or park it, and say which.
- More than 5 segments means the ICP is too broad; raise it in the stage 20 review rather than writing 8 campaigns.
- Tiering and multi-segment ICPs: `skills/icp-definition/references/icp-matrix-builder.md`.
