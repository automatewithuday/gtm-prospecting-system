# FAQ and troubleshooting

Most of this comes from the first live test run of the system.

## Setup

**The skills do not show up when I type `/`.**
Start Claude Code from inside the cloned folder. The skills load from `.claude/skills`, which is a link to `skills/`. On Windows, git may check the link out as a text file: clone with `git clone -c core.symlinks=true ...`, or copy `skills/` to `.claude/skills/`.

**Can I use this in Cursor, Codex or another agent?**
The skills are plain `SKILL.md` files in the open Agent Skills format, so any agent that reads that format can use them. The orchestration was written for and tested in Claude Code.

**Do I need every API key?**
No. See [COSTS-AND-KEYS.md](COSTS-AND-KEYS.md). With no keys at all, stages 1, 2, 9 to 16 and 18 to 20 still run, and your own list can enter at stage 6.

## During a run

**Claude says my customers do not share a pattern.**
Good. That is the honest answer when your five best customers are, say, two agencies, a fintech and two software companies. Run one cluster at a time. A lookalike search on mixed seeds returns noise, and you would pay for it.

**Stage 1 left most of the deal variables blank.**
Deal size, cycle length, trigger and champion are not public. Add what you know to `00-customers.csv` (or just tell Claude) and re-run the stage. Three real deal facts beat thirty inferred ones.

**I bought a follower list and nothing happened.**
GetLeads emails the CSV after checkout. Stage 5 is marked `blocked` with the page name until you save that file into `05-audience-raw/` and tell Claude. The account lane can carry on meanwhile.

**The account lane will not start.**
It needs `PROSPEO_API_KEY` and `OPENAI_API_KEY` in `.env`, plus Node.js 18+. Read `engine/list-builder/RUNBOOK.md`; re-running the same command resumes after any failure.

**The judge rejected companies that are obviously fine.**
That is what the 10-row approval loop in stage 6 is for. In our test the judge rejected restaurant software vendors as "not B2B software". The fix is one clearer sentence in the ICP ("vertical SaaS counts"), not editing rows. Fix the definition and re-run.

**Most of the signals Claude's researchers found were thrown away.**
Expected, and deliberate. In our test 17 signals came back and 4 survived: some were older than the window, two were about a different company with the same name, two had dead or unrelated links. Stage 9 verifies every signal before writing it, and logs each drop with the reason. A false signal in a first line costs you more than no signal.

**Every lead came out as a low priority tier.**
On a brand-new cold list, engagement is zero for everyone and intent data is thin, so absolute tier labels (P1 to P5) bunch at the bottom. The **order** is still meaningful: work the list from the top. Tiers spread out once replies and engagement start feeding back in. If you want different thresholds for cold runs, tell Claude and it will propose them for your approval.

**Company names look wrong in the drafts (`Performyard`, `Acme Inc Nasdaq Acme`).**
Providers return names like that. Stage 8 adds `company_name_clean` and `first_name_clean`, and the copy stages only merge the clean columns. If you see a raw name in copy, stage 8's cleaning step was skipped: re-run it.

**Can Claude send the emails for me?**
No, by design. The system drafts and exports. You load the CSVs into your sender, which is also where warm-up, sending limits and unsubscribes are handled properly.

**Can I email the addresses marked `unverified` or `catch_all`?**
No. Only `valid` (verifier-approved) addresses are send-ready. The others stay in the file for LinkedIn outreach.

## Money

**Could Claude overspend?**
The cap in `state.json` is hard: every paid call is estimated and counted first, and Claude stops to ask rather than pass it. Purchases of follower lists also require you to pay by hand in the GetLeads app. The one thing outside the system's view is a provider-side setting such as a wallet auto top-up; Claude checks for it and warns you before a purchase that would trigger it.

**What does a first test cost?**
One follower page is $8.75 at the time of writing. Our first test pulled 27 well-matched leads using 27 GetLeads plan credits and no cash, then ran every stage through copy on the Claude subscription alone.

## Changing things

**Can I edit the scoring weights, the templates, the frameworks?**
Yes, they are yours. Each lives in its skill's `SKILL.md`. Claude is instructed to propose changes to anything a human decided (ICP, judge prompt, weights, segments, copy frameworks) and never to edit them silently.

**After editing a skill**
Run `bash scripts/validate.sh`. After editing the file contract, run `uv run scripts/check_run.py --selftest`.

**Do not rename anything under `engine/`.**
Those scripts import each other by relative folder name.
