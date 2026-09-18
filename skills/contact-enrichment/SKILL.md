---
name: contact-enrichment
description: "Use when stage 8 of the prospecting system needs people and verified emails — all matching titles at the approved accounts, plus work emails for qualified audience members who only have a LinkedIn URL — merged into one deduped lead file. Also use when the ask is \"find the contacts and emails for these companies\" or \"get emails for these LinkedIn profiles\"."
license: MIT
compatibility: Account lane needs Node.js with tsx and the keys in engine/list-builder/SKILL.md. Audience lane needs the GetLeads MCP server. Sending needs MILLIONVERIFIER_API_KEY.
metadata:
  author: automatewithuday
  source: martechs.io
  wraps: engine/list-builder/scripts/contacts.ts
---

# Contact Enrichment

Two lanes arrive here with different shapes: accounts that need people, and people that need emails. One file leaves.

## Pipeline contract

**Stage 8 of 20.** Reads `07-accounts.csv` + `07-lane.json` (account lane) and `06-audience-qualified.csv` (audience lane). Writes `08-leads.csv` with the lead columns.

Files live in `runs/<run>/`. Column definitions: [`/prospecting-system`](../prospecting-system/SKILL.md).

**Gate:** the human approves `07-accounts.csv` before any contact pull. This is where real money starts.

## Lane A — accounts → people

```bash
npx tsx engine/list-builder/scripts/contacts.ts --config=<run>/07-lane.json --run-dir=<abs path to run>/07-lane
```

Cost-ordered waterfall, resumable: GetLeads export (free on plan) → Blitz for domains GetLeads left at zero → Prospeo people search last (paid). It refuses to run unless the lane's `summary.md` says READY. Output is `leads-final.csv` in the lane dir.

The engine pulls **all matching titles at every company, uncapped** — that is its rule, keep it. The run's target is enforced later, at stage 11, by ranking; not here by dropping contacts.

Set `source_type` to `lookalike` for accounts that came from `03-lookalikes.csv`, else `search`.

## Lane B — audience members → emails

Rows in `06-audience-qualified.csv` with `qualified=true` and no email:

1. Has `linkedin_url` → GetLeads MCP `getleads_get_emails_from_linkedin_batch`.
2. No LinkedIn URL but name + company → `getleads_enrich_person_batch`.

Both charge one plan credit per successful row. Check `get_fair_use` first on large batches. Only enrich qualified rows — never the raw audience.

## Merge

1. Normalize both lanes to the lead columns. Build `lead_id`.
2. Dedupe by `linkedin_url`, else `account_domain+first_name+last_name`. When the same person arrives from both lanes, keep ONE row, keep the audience `source_type` (it is the stronger evidence), and add the sources up in `source_count`.
3. Drop `excluded_domains` and anyone on the do-not-contact list.

## Email verification — the send gate

A provider saying "verified" is a hint. Every address goes through MillionVerifier before it is send-ready (script and key setup: [cold-email-starter-kit](https://github.com/automatewithuday/GTM-Skills/tree/main/skills/cold-email-starter-kit)).

- `email_status=valid` only for MillionVerifier `ok`.
- Catch-all, unknown, and invalid are kept in the file with their status and are never emailed. They can still get LinkedIn outreach in stage 15.
- MillionVerifier rejects default Python/Node user agents — send a browser UA.

Verification is paid per address: add it to `spent_usd` first.

## Report

Rows per lane, duplicates merged, emails found, emails valid, cost. If valid emails are under the run's target, say so now — the fix is more accounts or another audience, not looser verification.
