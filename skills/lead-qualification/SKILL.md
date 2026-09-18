---
name: lead-qualification
description: "Use when stage 18 of the prospecting system has positive replies and each one needs a go / nurture / no-go decision before a meeting is booked — checking the person, the account, the timing, and the reply itself against the ICP. Also use when the ask is \"is this lead worth a call?\"."
license: MIT
metadata:
  author: automatewithuday
  source: martechs.io
---

# Lead Qualification

A positive reply is not a qualified lead. This stage spends a few minutes per replier so the calendar fills with the right meetings, and so the wrong ones get a useful answer instead of a call.

## Pipeline contract

**Stage 18 of 20.** Reads `17-replies.csv` (rows with `is_positive=true`), `10-scored.csv`, `09-signals.csv`, `02-client-profile.yaml`. Writes `18-qualified.csv` (adds `decision`, `decision_reason`, `open_questions`, `suggested_reply`).

Files live in `runs/<run>/`. Column definitions: [`/prospecting-system`](../prospecting-system/SKILL.md).

## Four checks

| Check | Question | Evidence |
|---|---|---|
| **Person** | Can they buy, champion, or introduce? | title vs the profile's `job_titles`; what they said about their role |
| **Account** | Does the company still pass the hard filters? | `screen` and `fit_components` from stage 10 — re-verify anything that was blank |
| **Timing** | Is there a reason to act now? | dated signals from stage 9; timing words in the reply ("next quarter", "evaluating now") |
| **Reply** | What did they actually ask for? | the reply text and its stage 17 label |

Record what is known and what is not. An unknown is an open question for the call, not a fail.

## Decision

- **go** — person and account pass, nothing in the reply contradicts fit. Book it. Hand to [`/account-notes`](../account-notes/SKILL.md).
- **nurture** — fit is real but timing is not ("reach out in Q3"). Log the re-engage date and the trigger that would bring it forward. Re-engagement rules: the Re-Qualification table in [`/lead-scoring`](../lead-scoring/SKILL.md).
- **refer** — `positive_referral`: the named person becomes a new lead. Add them to `08-leads.csv` with `source_type` unchanged and `source_detail=referral from <lead_id>`, and contact them the same day.
- **no-go** — a hard filter fails. Reply politely and close it. Do not book a meeting to find out.

`decision_reason` is one sentence naming the check that decided it. `suggested_reply` is a draft for the human; nothing is sent.

## Rules

- The hard filters are the human's. If a no-go feels wrong, say so in `decision_reason` and propose a filter change for stage 20 — do not quietly pass the lead.
- For Tier 1 accounts, build the full account brief (Level 3 in [`/lead-scoring`](../lead-scoring/SKILL.md)) before the call, via [`/account-notes`](../account-notes/SKILL.md).
- Every no-go and nurture reason is data. Stage 20 reads this file to see which segments and sources produce replies that do not qualify.
