# Prospecting System

20 stage skills + one orchestrator in `skills/`. To run the workflow, follow `skills/prospecting-system/SKILL.md`; it is the source of truth for stage order, file names, columns, gates, and operating rules.

- Runs live in `runs/<run>/` (git-ignored). After each stage: update `state.json`, then `uv run scripts/check_run.py runs/<run>`.
- `engine/` is vendored verbatim from GTM-Skills. Scripts import each other by relative path — never rename or move anything in it. Read `engine/list-builder/RUNBOOK.md` before running an engine script.
- Spend cap in `state.json` is hard. Estimate, count, then call. Never loop around a cap or a provider limit.
- Propose, don't edit, anything a human decided: `02-client-profile.yaml`, judge prompts, score weights, segments, copy frameworks, thresholds inside skills.
- Per-row bulk work (judging, classifying, personalizing) → Haiku sub-agents in batches, after a human approves a sample.
- Python via `uv` only. Secrets only in `.env`; never print them. Quote paths — they may contain spaces.
- After editing any skill: `bash scripts/validate.sh`.
