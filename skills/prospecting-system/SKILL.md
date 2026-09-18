---
name: prospecting-system
description: "Use when the ask is \"here are my best customers, find me more like them\", \"run the prospecting system\", \"turn these 5 customers into prospects\", or when resuming a run in runs/. Coordinates all 20 stage skills end to end — customer patterns, ICP, lookalikes, follower audiences, enrichment, signals, scoring, segmentation, copy, reply handling, and the weekly review — with a resumable run folder, a spend cap, and human approval gates."
license: MIT
metadata:
  author: automatewithuday
  source: martechs.io
---

# Prospecting System

Turn your 5 best customers into your next 500 prospects. This skill does no prospecting itself: it runs the 20 stage skills in order, moves files between them, tracks spend, and stops at the gates where a human decides.

## Intake (ask all of it in one message)

1. **Best customers** — 5 to 10 domains, plus anything known about each deal (size, champion title, how they found you). Saved as `00-customers.csv`.
2. **Your website** — for the ICP stage.
3. **Target** — how many send-ready leads (default 500). It is a ceiling, not a quota: if 180 qualify, deliver 180 and say why.
4. **Spend cap for this run, in USD** — required. No default. Covers every paid call: follower scrapes, DiscoLike, Prospeo, enrichment credits, email verification.
5. **Lanes** — accounts (lookalikes + search), audiences (followers, engagers, communities, events), or both (default).
6. **Where copy goes** — Smartlead, HeyReach, another sender, or CSV only. This system never sends.

Then create `runs/<customer-slug>-<YYYY-MM-DD>/` with `00-customers.csv` and `state.json`.

## The stages

| # | Skill | Reads | Writes | Gate |
|---|---|---|---|---|
| 1 | [`/customer-patterns`](../customer-patterns/SKILL.md) | `00-customers.csv` | `01-customer-patterns.md`, `01-seeds.csv` | |
| 2 | [`/icp-definition`](../icp-definition/SKILL.md) | 01 | `02-client-profile.yaml` | human confirms the ICP |
| 3 | [`/lookalike-research`](../lookalike-research/SKILL.md) | 01, 02 | `03-lookalikes.csv` | |
| 4 | [`/audience-discovery`](../audience-discovery/SKILL.md) | 01, 02 | `04-audiences.csv` | human picks pages |
| 5 | [`/follower-scrape`](../follower-scrape/SKILL.md) | 04 | `05-audience-raw/*.csv` | human pays per page |
| 6 | [`/audience-filter`](../audience-filter/SKILL.md) | 05, 02 | `06-judge-prompt.txt`, `06-audience-qualified.csv` | human approves the judge |
| 7 | [`/targeted-search`](../targeted-search/SKILL.md) | 01, 02, 03, 06 | `07-lane.json`, `07-accounts.csv` | lane must be READY |
| 8 | [`/contact-enrichment`](../contact-enrichment/SKILL.md) | 06, 07 | `08-leads.csv` | human approves the account list |
| 9 | [`/buying-signals`](../buying-signals/SKILL.md) | 08 | `09-signals.csv` | |
| 10 | [`/lead-scoring`](../lead-scoring/SKILL.md) | 08, 02 | `10-scored.csv` | human approves weights once |
| 11 | [`/lead-prioritization`](../lead-prioritization/SKILL.md) | 10, 09 | `11-prioritized.csv` | |
| 12 | [`/segmentation`](../segmentation/SKILL.md) | 11 | `12-segmented.csv` | human approves segments |
| 13 | [`/personalization`](../personalization/SKILL.md) | 12, 09 | `13-personalized.csv` | human approves a batch of 10 |
| 14 | [`/cold-email`](../cold-email/SKILL.md) | 13, 02 | `14-emails.csv` | human approves copy |
| 15 | [`/linkedin-outreach`](../linkedin-outreach/SKILL.md) | 13 | `15-linkedin.csv` | human approves copy |
| 16 | [`/follow-ups`](../follow-ups/SKILL.md) | 14, 15 | `16-sequence.md`, `16-followups.csv` | |
| — | **Human sends the campaign. The run pauses here.** | | | |
| 17 | [`/reply-classification`](../reply-classification/SKILL.md) | sender or `17-replies-raw.csv` | `17-replies.csv`, `17-reply-score.json` | |
| 18 | [`/lead-qualification`](../lead-qualification/SKILL.md) | 17, 10 | `18-qualified.csv` | |
| 19 | [`/account-notes`](../account-notes/SKILL.md) | 18 | `19-account-notes/<domain>.md` | |
| 20 | [`/pipeline-review`](../pipeline-review/SKILL.md) | whole run | `20-review-<date>.md` | human approves targeting changes |

Read the stage's SKILL.md before running it. Its "Pipeline contract" block is the handoff; the rest of the file is how to do the work.

Stages 3–6 (audience lane) and 3+7 (account lane) are independent until stage 8 merges them. A lane the user declined is marked `skipped`.

## Operating rules

1. **Spend cap is hard.** Before any paid call, estimate its cost, add it to `spent_usd`, and stop if the total would pass `spend_cap_usd`. Ask the human; never work around it, never split a purchase to slip under it.
2. **Dedupe before you pay.** Against the run so far, `excluded_domains`, and the do-not-contact list.
3. **Cheap before deep.** Free counts and the ICP judge run before enrichment; enrichment before research; research only on leads that will be contacted.
4. **Unknown is not negative.** A blank field stays blank and is scored as unknown. Never turn missing data into a zero or a guess.
5. **Fit, intent, and priority stay in separate columns**, each with its evidence.
6. **Every signal has a source URL and a real event date**, or it is not written.
7. **Never pad.** Fewer qualified leads than the target is a result; report the constraint.
8. **Drafts only.** Nothing in this system uploads to a sender or sends a message.
9. **Bulk per-row work goes to Haiku sub-agents** (judging, classifying, personalizing), in batches, after a human has approved a sample. Strategy, ICP, and copy frameworks stay on the main model.
10. **Human decisions are proposed, not edited**: the ICP yaml, the judge prompt, score weights, segments, copy frameworks.

## state.json

```json
{
  "run": "acme-2026-01-15",
  "target_leads": 500,
  "spend_cap_usd": 150,
  "spent_usd": 0,
  "stages": {
    "01-customer-patterns": {"status": "done", "rows_in": 5, "rows_out": 5, "cost_usd": 0, "finished_at": "2026-01-15", "note": ""}
  }
}
```

Stage keys are `<NN>-<skill-name>` (`04-audience-discovery`, `08-contact-enrichment`, ...). `status` is `pending`, `done`, `skipped`, or `blocked` (with the reason in `note`). Update it when a stage finishes, then run:

```bash
uv run scripts/check_run.py runs/<run>
```

It validates files and columns against this contract and prints the stage funnel. Fix what it reports before starting the next stage.

**Resuming:** read `state.json`, run the checker, continue from the first stage that is not `done` or `skipped`. Never redo a paid stage whose output file exists.

## Lead columns

From `06-audience-qualified.csv` and `08-leads.csv` onward, every lead file carries these columns; stages only ADD columns.

| Column | Meaning |
|---|---|
| `lead_id` | stable id: `linkedin_url` if known, else `account_domain:first_name:last_name`, lowercased |
| `account_domain` | normalized company domain, no subdomain |
| `company_name`, `first_name`, `last_name`, `title`, `linkedin_url` | as provided; blank if unknown |
| `email`, `email_status` | `email_status` is `valid` only after a verifier says so; provider "verified" is `unverified` here |
| `source_type` | `lookalike`, `search`, `follower`, `engager`, `member`, `attendee` |
| `source_detail` | which page, post, community, event, or lane produced the row |
| `source_count` | how many distinct sources surfaced this person |

Account files (`03`, `07`) need `domain`; signals need the columns in [`/buying-signals`](../buying-signals/SKILL.md).

## What "done" looks like

After stage 16: a ranked, segmented, verified lead list with first-touch email, LinkedIn note, and follow-ups per lead, plus a run summary — leads by source and tier, spend against cap, and what limited the count. After stage 20: a dated review with proposed targeting changes for the next run.
