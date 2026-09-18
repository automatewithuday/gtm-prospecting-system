# The Claude Prospecting System

**Turn your 5 best customers into your next 500 prospects.** 20 Claude skills and one orchestrator that run the whole outbound workflow end to end — from "who are our best customers, really?" to a weekly review of where the pipeline leaks.

**Who it's for:** founders, SDR leaders, RevOps and agencies who run outbound and already use (or want to use) Claude Code. No coding needed to run it.

**Docs:** [Getting started](docs/GETTING-STARTED.md) · [The 20 stages](docs/STAGES.md) · [Costs and keys](docs/COSTS-AND-KEYS.md) · [FAQ](docs/FAQ.md) · [Sample run](examples/sample-run/)

Each skill does one job your team is doing by hand today. Together they are a single resumable run: every stage reads the previous stage's file and writes its own, with a spend cap and a human approval gate wherever a decision is yours.

```
 5 best customers
        │
        ▼
 1 customer-patterns ─▶ 2 icp-definition
        │                       │
        ├── accounts ───────────┼──▶ 3 lookalike-research ─────────────────┐
        │                       │                                          ▼
        └── audiences ──────────┴──▶ 4 audience-discovery ─▶ 5 follower-scrape ─▶ 6 audience-filter
                                                                           │
                                                                           ▼
                                      7 targeted-search ─▶ 8 contact-enrichment   (lanes merge, dedupe, verify)
                                                                           │
        9 buying-signals ─▶ 10 lead-scoring ─▶ 11 lead-prioritization ─▶ 12 segmentation
                                                                           │
        13 personalization ─▶ 14 cold-email ─▶ 15 linkedin-outreach ─▶ 16 follow-ups
                                                                           │
                                                          ── you send ──   │
                                                                           ▼
        17 reply-classification ─▶ 18 lead-qualification ─▶ 19 account-notes ─▶ 20 pipeline-review ─▶ back to 2
```

## Quick start

```bash
git clone https://github.com/automatewithuday/gtm-prospecting-system.git && cd gtm-prospecting-system
cp .env.example .env          # add your keys — see "What you need"
claude
```

Then say:

> Run the prospecting system. Our best customers are acme.com, globex.com, initech.com, umbrella.com and hooli.com.

Claude asks six intake questions (customers, website, target count, **spend cap**, lanes, where the copy goes), creates `runs/<name>-<date>/`, and works through the stages, stopping at each gate for your approval. Stop any time; say "resume the run" later.

The full walkthrough, including the 12 ICP interview questions Claude will ask you, is in [Getting started](docs/GETTING-STARTED.md).

Skills load automatically when you open the repo in Claude Code (`.claude/skills` points at `skills/`). To install them as a plugin instead: `/plugin marketplace add automatewithuday/gtm-prospecting-system`. Every skill also works on its own.

## The 20 skills

| # | Skill | The job it takes off your plate |
|---|---|---|
| 1 | [`customer-patterns`](skills/customer-patterns/SKILL.md) | Find what your best customers have in common: firmographics, triggers, champions, deal shape |
| 2 | [`icp-definition`](skills/icp-definition/SKILL.md) | Write the ICP down — hard filters vs soft preferences, offer, exclusions |
| 3 | [`lookalike-research`](skills/lookalike-research/SKILL.md) | Turn seed customer domains into hundreds of similar companies |
| 4 | [`audience-discovery`](skills/audience-discovery/SKILL.md) | Find the competitor, tool, community, and event pages your buyers already follow — sized and priced |
| 5 | [`follower-scrape`](skills/follower-scrape/SKILL.md) | Collect those audiences with GetLeads (followers), post engagers, or CSV import — source preserved |
| 6 | [`audience-filter`](skills/audience-filter/SKILL.md) | Build and tune the ICP judge with a human, then filter the raw audience before paying for enrichment |
| 7 | [`targeted-search`](skills/targeted-search/SKILL.md) | Account search at scale: Prospeo + lookalikes + AI judging + live-site verification, resumable |
| 8 | [`contact-enrichment`](skills/contact-enrichment/SKILL.md) | People and verified emails via a cost-ordered waterfall; both lanes merged and deduped |
| 9 | [`buying-signals`](skills/buying-signals/SKILL.md) | Funding, hiring, new-in-role, tech changes — each with a source URL and a real date |
| 10 | [`lead-scoring`](skills/lead-scoring/SKILL.md) | Screen out disqualifiers, then score fit with the components shown |
| 11 | [`lead-prioritization`](skills/lead-prioritization/SKILL.md) | Combine fit, intent, and engagement into one ranked queue with tiers |
| 12 | [`segmentation`](skills/segmentation/SKILL.md) | Group leads by use case so each group gets its own angle |
| 13 | [`personalization`](skills/personalization/SKILL.md) | Strongest angle per lead → short variables, generated in parallel after you approve a sample |
| 14 | [`cold-email`](skills/cold-email/SKILL.md) | First-touch email per segment: five frameworks, deliverability-safe, QA checklist |
| 15 | [`linkedin-outreach`](skills/linkedin-outreach/SKILL.md) | Connection note (≤300 chars) + DM from one of three fixed templates, picked by evidence |
| 16 | [`follow-ups`](skills/follow-ups/SKILL.md) | Sequence steps, timing, channel mix, escalation |
| 17 | [`reply-classification`](skills/reply-classification/SKILL.md) | Classify every reply and compute positive reply rate against the 1% bar |
| 18 | [`lead-qualification`](skills/lead-qualification/SKILL.md) | Go / nurture / refer / no-go on each positive reply before a meeting is booked |
| 19 | [`account-notes`](skills/account-notes/SKILL.md) | A five-minute pre-call brief for sales, every claim sourced |
| 20 | [`pipeline-review`](skills/pipeline-review/SKILL.md) | Weekly: where the workflow leaks, which segments and sources reply, what to change next |
| ★ | [`prospecting-system`](skills/prospecting-system/SKILL.md) | The orchestrator: run folder, handoffs, spend cap, gates, resume |

Per-stage detail (what it reads, writes, needs and where it stops for you): [docs/STAGES.md](docs/STAGES.md).

## What you end up with

After stage 16, in one folder:

- `11-prioritized.csv` — every lead ranked, with fit, intent and engagement scores shown separately and the evidence for each
- `09-signals.csv` — buying signals, each with a source link and a real date, verified before it was written
- `12-segmented.csv` — leads grouped by why they would buy
- `14-emails.csv`, `15-linkedin.csv`, `16-followups.csv` — first-touch email, LinkedIn note and DM, and the follow-up sequence, per lead
- `state.json` — what ran, what it cost against your cap, and how many leads each stage kept

See a filled-in example of every file in [examples/sample-run/](examples/sample-run/).

## How it behaves

- **Spend cap is hard.** You set a dollar cap at intake. Every paid call is estimated and counted first. Claude stops and asks rather than going over.
- **Nothing gets bought without you.** Follower lists, contact pulls, and verification each wait for a yes.
- **Nothing gets sent.** The system drafts and exports. You load the CSVs into your sender.
- **Cheap before deep.** Dedupe, free counts, and the ICP judge run before enrichment; research only on leads you will contact.
- **Unknown is not negative.** Missing data stays blank and is scored as unknown, never as a zero or a guess.
- **Fit, intent, and priority are separate columns**, each with its evidence, so you can see why a lead ranks where it does.
- **Never padded.** If 180 leads qualify, you get 180 and the reason.
- **Resumable.** `runs/<run>/state.json` records every stage; re-running never repeats a paid step.

Check any run:

```bash
uv run scripts/check_run.py runs/<run>
```

It validates the run against the file contract and prints the stage funnel with the biggest drop.

## What you need

| For | You need |
|---|---|
| Everything | [Claude Code](https://claude.com/claude-code) |
| Audience lane (stages 4–6, 8) | [GetLeads](https://getleads.io) MCP server connected, plus prepaid wallet cash for follower lists (about $0.0035 per follower, $8.75 minimum per page at the time of writing) |
| Account lane (stages 7–8) | Node.js 18+, `PROSPEO_API_KEY`, `OPENAI_API_KEY` (cheap nano judge) |
| Sending safely (stage 8) | `MILLIONVERIFIER_API_KEY` |
| Optional | DiscoLike, Blitz, Exa, Parallel, Smartlead keys — each stage degrades gracefully without them |
| The run checker | [`uv`](https://docs.astral.sh/uv/) |

No keys at all? Stages 1–2, 9–16, and 18–20 run on your Claude subscription alone, and any list you already have can enter at stage 6 as a CSV. Prices, what each key unlocks, and how the spend cap behaves: [docs/COSTS-AND-KEYS.md](docs/COSTS-AND-KEYS.md).


## Layout

```
skills/      the 20 stage skills + the orchestrator
engine/      the list-building engine stages 7, 8 and 12 drive (scripts import each other — do not rename)
scripts/     check_run.py (run validator + funnel), validate.sh (skill lint)
docs/        getting started, stage reference, costs and keys, FAQ
examples/    a sample 00-customers.csv and a synthetic sample run you can validate
runs/        your runs (git-ignored)
```

## Where these came from

Most of these skills were built and used in client work at [martechs.io](https://martechs.io) and are ported here from [GTM-Skills](https://github.com/automatewithuday/GTM-Skills), [gtm-flywheel](https://github.com/automatewithuday/gtm-flywheel), [gtm-os-kit](https://github.com/automatewithuday/gtm-os-kit), and [linkedin-competitor-icp-scorer](https://github.com/automatewithuday/linkedin-competitor-icp-scorer). Each ported skill names its origin in `metadata.ported_from`. Some reference files mention scripts that live in GTM-Skills (deliverability, inbox management, Smartlead upload) — install that repo alongside if you want them.

MIT licensed. Portions derive from third-party MIT work; see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
