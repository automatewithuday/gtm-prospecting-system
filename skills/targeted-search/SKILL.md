---
name: targeted-search
description: "Use when stage 7 of the prospecting system needs qualified target accounts found at scale — Prospeo company search, lookalike expansion, AI judging, live-website verification, and snowballing — driven from the ICP and seed customers. Also use when the ask is \"build me an account list for this ICP\"."
license: MIT
compatibility: Needs Node.js 18+ with tsx, PROSPEO_API_KEY and OPENAI_API_KEY in .env at the repo root. Other keys are optional and degrade gracefully (see engine/list-builder/SKILL.md).
metadata:
  author: automatewithuday
  source: martechs.io
  wraps: engine/list-builder
---

# Targeted Search

A thin stage wrapper around the list-builder engine in `engine/list-builder/`. The engine owns the process; this skill owns getting the run's ICP into it and its result back out.

**Read `engine/list-builder/RUNBOOK.md` before running anything.** Run the commands there; do not improvise. `engine/list-builder/SKILL.md` documents every phase and env var.

## Pipeline contract

**Stage 7 of 20.** Reads `01-seeds.csv`, `02-client-profile.yaml`, `03-lookalikes.csv`, and the company domains in `06-audience-qualified.csv`. Writes `07-judge-spec.json`, `07-lane.json`, `07-accounts.csv`.

Files live in `runs/<run>/`. Column definitions: [`/prospecting-system`](../prospecting-system/SKILL.md).

## Steps

1. **Build `07-lane.json`** from the profile (shape documented at the top of `engine/list-builder/scripts/run-lane.ts`):
   - `seeds` ← `01-seeds.csv`
   - `emp_min` / `emp_max`, `states`, `industries` ← `icp_hard_filters`. Industry names must be valid Prospeo names (`skills/icp-definition/references/prospeo-industries.md`).
   - `keywords` ← the discriminating phrases from `01-customer-patterns.md`
   - `seniorities` ← the profile's titles
   - `extra_candidates` ← absolute paths to `03-lookalikes.csv` and a `domain`-column CSV of the companies behind `06-audience-qualified.csv`. This is how both lanes land in one judged list.
2. **Judge prompt** — reuse the ICP and disqualifiers the human approved in stage 6. Write `07-judge-spec.json` and generate the prompt with `make-judge.ts`. Never hand-write it; the template's mandatory blocks prevent known false-negative classes.
3. **Test, then run.** A 50–100 row test first. Then:
   ```bash
   npx tsx engine/list-builder/scripts/make-judge.ts --spec=<run>/07-judge-spec.json --out=<run>/07-judge-prompt.txt
   npx tsx engine/list-builder/scripts/run-lane.ts   --config=<run>/07-lane.json --run-dir=<abs path to run>/07-lane
   ```
   `--run-dir` keeps the lane's artifacts inside the run folder (default is `~/output/list-builder/lanes/`). `prompt` in `07-lane.json` must be the absolute path to `07-judge-prompt.txt`.
   Re-running the same command resumes after any failure.
4. **Read `summary.md` in the lane dir.** Line 1 is `# READY` or `# NOT READY` with the next command. Only READY moves on. The failure playbook is in the RUNBOOK.
5. **Copy the final qualified companies to `07-accounts.csv`** (`domain` required, keep every other column) and record rows pulled → rows qualified in `state.json`.

## Scope for this system

The engine is built to find the largest list possible (`snowball.ts` sweeps until a round adds under 3% net-new). For a 500-lead run that is usually more than needed:

- Skip `snowball.ts` unless the lane finishes READY with too few accounts for the target.
- The engine's own cost gate asks before sweeps above ~500k companies. This system's spend cap is stricter and wins: estimate the pull (free Prospeo counts), add it to `spent_usd`, stop if it passes the cap.
- Judging is cheap (roughly $1–3 per 10k companies on the nano judge) — do not sample or skip scoring to save money. Save money by narrowing the pull with the hard band and geography.

## Do not

- Rename or move anything under `engine/` — the scripts import each other by relative path.
- Hand-edit stream CSVs or files inside a lane run dir.
- Pull contacts here. That is stage 8, after the human approves `07-accounts.csv`.
