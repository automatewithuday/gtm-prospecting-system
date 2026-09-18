# The 20 stages

What each skill does, what it reads and writes, where it stops for you, and what it needs. File names are inside `runs/<run>/`. The exact column contract lives in [`skills/prospecting-system/SKILL.md`](../skills/prospecting-system/SKILL.md); a filled-in example of every file is in [`examples/sample-run/`](../examples/sample-run/).

**Needs** key: 🟢 Claude only · 🔵 GetLeads MCP · 🟠 API keys in `.env` · 💵 can cost money

## Understand your customers

### 1. customer-patterns 🟢
Researches each best customer and finds what they share across 12 deal variables: size, industry, stage, tech, trigger, champion, buyer, deal size, cycle and more.
**Reads** `00-customers.csv` → **Writes** `01-customer-patterns.md`, `01-seeds.csv`
With 5 customers and no lost deals it says so: findings are labelled with how many customers support them, and unknown deal facts stay blank. If your customers form two groups, it tells you to run them separately.

### 2. icp-definition 🟢 · gate: you confirm the ICP
A one-question-at-a-time interview, pre-filled from your website and stage 1. Separates **hard filters** (must match) from **soft preferences** (nice to have), and records your offer, tone, exclusions and banned words.
**Reads** stage 1 → **Writes** `02-client-profile.yaml`

## Find the accounts and the people

### 3. lookalike-research 🟠💵
Turns seed customer domains into similar companies with DiscoLike. Samples 50 to 100 first and checks them against the ICP judge before scaling, so bad seeds are caught cheaply.
**Reads** `01-seeds.csv`, profile → **Writes** `03-lookalikes.csv`

### 4. audience-discovery 🟢🔵 · gate: you pick the pages
Finds where buyers like your customers already gather: competitor pages, adjacent tool pages, communities, events. Starts from evidence at your named customers, then expands. Sizes and prices every LinkedIn page for free. Prefers narrow, on-problem pages over big ones.
**Reads** stage 1, profile → **Writes** `04-audiences.csv`

### 5. follower-scrape 🔵💵 · gate: you pay per page
Collects the people: LinkedIn page followers (GetLeads), post engagers, or a CSV you import for communities and events. Never drops the label saying where a person came from: `follower`, `engager`, `member` or `attendee`. One page first, judged, before buying the next.
**Reads** selected rows of `04-audiences.csv` → **Writes** `05-audience-raw/*.csv`

### 6. audience-filter 🟢 · gate: you approve the judge
Builds the ICP judge prompt with you, 10 rows at a time, until two batches come back clean. Then normalizes, dedupes (a person following three competitor pages becomes one row with `source_count=3`) and filters the raw audience. Rejected rows are kept with the reason.
**Reads** `05-audience-raw/`, profile → **Writes** `06-judge-prompt.txt`, `06-audience-qualified.csv`

### 7. targeted-search 🟠💵 · gate: the lane must finish READY
Account search at scale using the list-building engine in `engine/`: Prospeo company search, lookalike expansion, an AI judge over every candidate, live-website verification, all resumable with one command. Lookalikes from stage 3 and companies behind stage 6 enter the same judged list.
**Reads** seeds, profile, stages 3 and 6 → **Writes** `07-lane.json`, `07-accounts.csv`

### 8. contact-enrichment 🔵🟠💵 · gate: you approve the account list
Two lanes merge here. Accounts get every person with a matching title through a cost-ordered waterfall (GetLeads, then Blitz, then Prospeo). Audience members with only a LinkedIn URL get a work email. Then dedupe, name cleaning, and email verification. Only verifier-approved addresses are marked `valid`; catch-all and unknown stay in the file and get LinkedIn outreach only.
**Reads** stages 6 and 7 → **Writes** `08-leads.csv`

## Decide who matters

### 9. buying-signals 🟢 (🔵 optional)
Funding, hiring, new-in-role, tech changes, launches. One row per signal, each with a source URL and the date it happened. Every signal is verified before it is written: the URL must resolve, the page must be about this company and not a same-named one, the date must be in the window. No signal found means no row.
**Reads** `08-leads.csv` → **Writes** `09-signals.csv`

### 10. lead-scoring 🟢 · gate: you approve weights once
Level 1 screens out hard disqualifiers. Level 2 scores **fit** with every component shown. Missing data is scored as unknown, never as zero, and the file says how much of the score was knowable.
**Reads** leads, profile → **Writes** `10-scored.csv`

### 11. lead-prioritization 🟢
Combines fit, intent and engagement into one ranked queue, keeping all three scores visible. Audience evidence counts as engagement (an engager outranks a follower). Caps the outreach set at your target and never pads it.
**Reads** stages 9 and 10 → **Writes** `11-prioritized.csv`

### 12. segmentation 🟢 (🟠 for large lists) · gate: you approve segments
Groups leads by **why they would buy**, derived from your customers rather than from the list. 2 to 5 segments; `none` is a valid answer; a segment under about 30 leads is merged or parked.
**Reads** `11-prioritized.csv`, stage 1 → **Writes** `12-segments.md`, `12-segmented.csv`

## Write the outreach

### 13. personalization 🟢 · gate: you approve a batch of 10
Picks the strongest angle per lead in this order: a dated signal, then audience evidence (which page, what they commented), then segment bucket copy. Records which one was used. One lead, then batches of 10 with your approval, then fan-out. Never invents a fact.
**Reads** stages 9 and 12 → **Writes** `13-personalized.csv`

### 14. cold-email 🟢 · gate: you approve copy
First-touch email per segment from five frameworks, written to land in the primary inbox: under 90 words, one interest-based CTA, no links or calendar in email one, banned-word and spam checks, pre-send QA checklist.
**Reads** stage 13, profile → **Writes** `14-emails.csv`

### 15. linkedin-outreach 🟢 · gate: you approve copy
A connection note (300 characters, counted) and a first DM (5 sentences max) from one of three fixed templates, chosen by the evidence behind the lead and never blended. The template name is saved so reply rates can be compared.
**Reads** stage 13 → **Writes** `15-linkedin.csv`

### 16. follow-ups 🟢
Steps, timing, channel mix and escalation. Every follow-up adds a new angle, proof or resource; a bump that only says "following up" does not ship.
**Reads** stages 14 and 15 → **Writes** `16-sequence.md`, `16-followups.csv`

**You send. The run pauses.**

## Learn from the replies

### 17. reply-classification 🟢 (🟠 Smartlead optional)
Classifies every reply into 11 labels and computes positive reply rate against the 1% bar. Unsubscribes and hostile replies go to the do-not-contact list in the same session.
**Reads** Smartlead or `17-replies-raw.csv` → **Writes** `17-replies.csv`, `17-reply-score.json`

### 18. lead-qualification 🟢
Four checks on each positive reply (person, account, timing, the reply itself) and a decision: **go**, **nurture**, **refer** or **no-go**, with a one-sentence reason and a drafted response. A referral becomes a new lead the same day.
**Reads** stages 10 and 17 → **Writes** `18-qualified.csv`

### 19. account-notes 🟢
A pre-meeting brief a rep can read in five minutes: why they were targeted, what was sent, what they replied, competitive context, pain hypotheses, questions. Every claim carries its source; unknown stays unknown.
**Reads** stage 18 and the lead's history → **Writes** `19-account-notes/<domain>.md`

### 20. pipeline-review 🟢 · gate: you approve targeting changes
Starts from the stage funnel (`scripts/check_run.py`) to see where leads are lost, then cuts positive replies and meetings by segment, source and tier. Under 30 sends in a cell it reports the count and draws no conclusion. Proposes changes to filters, judge, weights and sources; it never edits them itself. Approved changes start the next run at stage 2.
**Reads** the whole run → **Writes** `20-review-<date>.md`

## ★ prospecting-system 🟢
The orchestrator. Intake, the run folder, handoffs, the spend cap, the gates, resume. It does no prospecting itself.
