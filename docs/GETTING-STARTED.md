# Getting started

From zero to your first run. Plan on 30 to 60 minutes for the free stages; paid stages take as long as the providers take.

## 1. Install

You need [Claude Code](https://claude.com/claude-code). Everything else is optional and depends on which lanes you run (see [COSTS-AND-KEYS.md](COSTS-AND-KEYS.md)).

```bash
git clone https://github.com/automatewithuday/gtm-prospecting-system.git
cd gtm-prospecting-system
claude
```

That's it. The 21 skills load on their own because `.claude/skills` points at `skills/`. Type `/` in Claude Code and you will see them.

Want the paid lanes too?

```bash
cp .env.example .env    # then paste your keys into .env. Never commit this file.
```

and connect the [GetLeads](https://getleads.io) MCP server in Claude Code for follower audiences and contact search.

## 2. Start a run

Say this, with your own customers:

> Run the prospecting system. Our best customers are acme.com, globex.com, initech.com, umbrella.com and hooli.com.

Claude asks six things in one message:

| Question | Why it matters |
|---|---|
| Your 5 to 10 best customers, and anything you know about each deal | Everything downstream is built from these. Deal size, champion title and how they found you make the patterns far sharper |
| Your website | The ICP stage reads it to pre-fill answers |
| How many send-ready leads you want | A ceiling, not a quota. If 180 qualify you get 180 |
| **Spend cap in USD** | Required. No default. Nothing paid runs without it, and Claude stops and asks rather than going over |
| Which lanes | **Accounts** (lookalikes + search), **audiences** (followers, engagers, communities, events), or both |
| Where copy goes | Smartlead, HeyReach, another sender, or CSV. The system never sends |

Claude then creates `runs/<name>-<date>/` and starts.

## 3. What happens, and where you are asked to decide

**Stage 1, customer patterns.** Claude researches each customer and writes what they share. With 5 customers it will tell you plainly that these are hypotheses, and it leaves unknown deal facts blank instead of guessing. If your customers fall into two different groups, it says so and recommends running them separately.

**Stage 2, your ICP.** This is an interview. Claude reads your website, tells you what it understood, then asks one question at a time, pre-filling each answer for you to confirm or correct:

1. What do you sell, in one sentence?
2. Who is your single best customer? Name them.
3. What job title buys this?
4. Headcount range: hard minimum and hard maximum?
5. Industries: in or out?
6. Geography?
7. Any triggers that matter? (funding, hiring, tech, launches)
8. Any disqualifiers? (competitors, customers, partners)
9. Your offer: what are you asking them to do?
10. Lead magnet: what can you give away?
11. Tone?
12. Banned words or legal constraints?

Then, for each criterion: *"If someone matches everything except this, do you reach out anyway?"* Yes makes it a soft preference, no makes it a hard filter. This one question is what stops a 5,000-lead market shrinking to 200. You confirm the final `02-client-profile.yaml`.

**Stages 3 to 8, finding people.** Two lanes run side by side and merge at stage 8:

- *Accounts:* lookalikes of your customers, then a judged, verified account search, then everyone with the right title at the approved accounts.
- *Audiences:* Claude finds the competitor, tool, community and event pages your buyers follow, shows you each page's size and price, and **you pick**. Follower lists are paid for by you in the GetLeads app and arrive by email; you drop the CSV into the run folder. An ICP judge, tuned with you on 10 rows at a time, filters the raw audience before a cent is spent on enrichment.

**Stages 9 to 12, deciding who matters.** Buying signals (each with a source link and a real date, verified), a fit score with its components shown, a ranked queue, and segments by *why they would buy*.

**Stages 13 to 16, the copy.** You approve a sample of 10 personalized leads before the rest are generated. Then a first-touch email per segment, a LinkedIn note and DM, and the follow-up sequence. All drafts.

**You send.** The run pauses here.

**Stages 17 to 20, after sending.** Replies classified, positive replies qualified before a meeting is booked, a five-minute brief for each meeting, and a weekly review of where the workflow leaks and what to change.

## 4. Stopping, resuming, checking

Stop whenever you like. Later:

> Resume the prospecting run.

Claude reads `state.json` and carries on from the first unfinished stage. A paid stage whose output exists is never run twice.

Check a run yourself at any time:

```bash
uv run scripts/check_run.py runs/<your-run>
```

You get every stage's status, rows in and out, what was spent against your cap, and the stage losing the most leads. Try it now on the synthetic example: `uv run scripts/check_run.py examples/sample-run`.

## 5. Using one skill on its own

Every skill works without the pipeline. Examples:

> Use customer-patterns on this closed-won export.
> Use audience-discovery: whose followers should we target? Our site is example.com.
> Use cold-email to rewrite this sequence.
> Use reply-classification on Smartlead campaign 12345.

Ignore the "Pipeline contract" block at the top of a skill when you use it this way.

## No keys, no budget?

Stages 1, 2, 9 to 16 and 18 to 20 run on your Claude subscription alone, and any list you already own can enter at stage 6 as a CSV. That is a complete path from "who are our best customers" to reviewed outreach drafts at zero extra cost.
