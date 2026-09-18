# Playbook: Job Posting Language

> All rules here are best practice, not law. Override any of them when the campaign calls for it; note the best practice once and move on.

**Use when:** the angle is "you are hiring for this, and that is exactly what we help with". The
client names the roles or the description language that signals a fit, and every row needs a
specific, current opening to reference.

**Do not use when:** you want *how many* people they hired or headcount growth over time
(`playbook-hiring-surge`). If you want to **find** companies hiring a role rather than enrich a list
you already have, that is discovery mode — see note E.

**One-line output:** `job_posting_line_safe = "you're hiring an account executive for private equity"`

⚠️ **Never bind copy to the ungated `job_posting_line`.** The `_safe` field is the same value blanked
whenever the posting is older than 30 days. §6 explains why that gate is not optional.

## 1. Trigger and scope

A company posts jobs. Those postings say what the company is **about to spend money on** and what
problems it is trying to staff around. If a client sells to sales teams, "this company posted an SDR
job three weeks ago and the description talks about cold calling" is a better opening line than
anything you could invent.

This takes a list of domains you already have and puts one sentence fragment on each row. It covers
**job-board-sourced postings only**. It does not scrape career pages by default, does not count hires
over time, and does not find new companies.

It also carries a decision people get wrong constantly: **filter with keywords first, and only add an
AI classifier if a measurement proves keywords are not enough.** Note C is that measurement, already
run.

## 2. Output contract

### Inputs required per row

| Field | Type | Required? |
|---|---|---|
| `company_domain` (bare, lowercase) | string | yes |
| `company_name` | string | yes — used by the mandatory name-match gate in §7 |
| `keyword_set` | string[] | yes, **set once per campaign, not per row** |
| `role_titles` | string[] | no, see note C |
| `window_days` | number | no. **Default 60 to detect, 30 for claims in copy** |

### Output fields

| Field | Type | Example | Null? |
|---|---|---|---|
| `job_posting_line_safe` | string, ≤90 chars | `you're hiring an account executive for private equity` | no, use `""` |
| `job_posting_line` | string | same | **ungated. Audit and debugging only, never in a send** |
| `job_role_named` | string | `account executive for private equity` | no, `""` |
| `job_evidence_url` | string | the posting URL | no, `""` |
| `job_posted_date` | date | `2026-07-30` | no, `""` |
| `job_confidence` | `high` / `low` | `high` | no |

### Coverage expectation

**7/8 rows usable (87.5%).** Broken down honestly, because campaign setup needs the real shape: 5 of
8 produced a written line, 3 abstained, **all 3 abstains were correct.**

Expect roughly **60% of a healthy B2B software TAM to produce a line before the freshness gate.**

⚠️ **After the mandatory 30-day gate, plan on 35 to 40%.** Any row whose only posting is 31 to 60
days old blanks by design. On the live-test set that was **2 of the 5 generating rows** — one at 53
days (correctly killed, the role is gone from the company's live board) and one at 49 days that was
**verified genuinely open** and the gate kills anyway.

**That second row is the cost of a blunt proxy: a real open role, killed by its age.** A source with a
true "is this still open" boolean would keep it. The age proxy is what you have unless your source
exposes live status.

So `job_posting_line_safe` **cannot be a mandatory variable in copy.**

### Copy-fit rules

- Slots into `Saw {{job_posting_line_safe}}.` and nothing else. **Test every generated value in that
  exact frame.**
- Starts with the word "you", lowercase, no trailing period.
- 12 words or fewer, 5th-grade reading level, no em dashes.
- **Raw job titles are not copy.** `Partner Development Representative | Advisory and Services` has to
  become `a partner development representative`. **That rewrite is the only thing the AI step exists
  for.**

### Downstream gate

If empty: drop the clause through spintax and keep the row. Do not exclude the row unless the client
asked for a hiring-only segment — in which case exclude **at list build time, not at send time.**

## 3. Source chain (cost-tagged)

| # | Source | Cost | Call | Result |
|---|---|---|---|---|
| 1 | **A jobs API keyed on the company's job-board profile** | often FREE / unlimited | resolve `domain → company profile`, then query postings with `date_posted.last_days: 60` and `description.include: [keywords]` | 5/8 companies returned a matched posting; **7/8 rows produced a correct final value** |
| 2 | A second jobs provider, queried by bare domain | FREE on some plans | skips the profile-resolution step that step 1 can get wrong | run on every row step 1 could not answer, **or whose company name failed the name-match gate** |
| 3 | A company-search API's open-jobs filters | FREE on some plans | company-level "are they hiring for this title" | **it gates and sizes, it does not quote** — it cannot produce an evidence URL |
| 4 | A search API over the company's own careers page | METERED | one search per row | ⛔ **only when the operator explicitly asks. Never by default.** Career-page scraping is a different job with a different failure surface, and steps 1 to 3 are free |
| 5 | The line writer | CHEAP (~$0.14-0.21/1k) | §6 | 8/8 parsed after the params fix |

### Note A: filter server-side, always

Most jobs APIs return `title`, `date_posted`, `url`, `company_name` and a summary per posting — **but
never the full job description.** The description is only reachable **through the filter.**

Measured on the same 8 companies with the same 8 keywords:

| Approach | Companies matched |
|---|---|
| scanning the **returned fields** locally | **1 of 8** |
| the identical keyword set passed to the **description filter** | **5 of 8** |

**If you scan locally you will conclude the signal does not exist.**

### Note B: filter grammar, and silent stripping

```jsonc
{
  "company_linkedin_url": "...",                    // per-row enrichment endpoint
  "job": {
    "date_posted":     { "last_days": 60 },          // required inside date_posted
    "title":           { "include": [], "exclude": [] },
    "description":     { "include": [], "exclude": [] },
    "location":        { "include": [], "exclude": [] },
    "seniority":       { "include": [], "exclude": [] },
    "employment_type": { "include": [], "exclude": [] }
  },
  "max_results": 25,
  "cursor": "..."
}
```

⚠️ **Unknown keys are silently stripped and you get an unfiltered result set that looks successful.**
If a filter appears to do nothing, you spelled the key wrong.

### Note C: keyword versus AI — already measured, do not re-litigate casually

**The rule: keyword filter first, AI only when a measurement proves keywords insufficient.**

Measured over a whole jobs index, 30-day window, on the SDR cold-calling example:

| Query | Postings | Recall |
|---|---|---|
| `title.include = ["Sales Development Representative"]` | 7,422 | baseline |
| plus `description.include = [8 cold-outreach phrases]` | 5,004 | **67.4%** |
| plus `description.exclude = [same 8 phrases]` | 2,418 | the misses |

Sampling 25 of the misses and asking a cheap model whether the role still does cold outbound:
**18 of 25 said yes.** So keyword-only true recall is about **74%**, not the 90% assumed.

**But the useful conclusion is not "add AI":**

- **When the role name is the signal, filter on title and skip AI detection entirely.** All 7,422 of
  those postings are SDR jobs. **Title recall is effectively complete.**
- **Only filter on description when the signal is a practice titles do not name** ("mentions
  Salesforce", "mentions HIPAA"). Expect to lose about a third of your recall.
- **Add an AI classifier only when both are true:** the signal cannot be expressed as a title, **and**
  description recall measured under 90%. Put it behind a gate that only fires on rows the keyword
  filter missed.

**Re-run this measurement for every new keyword set.** It is three API calls plus a 25-row sample,
well under a cent. The decision rule:

| Measured recall | Do this |
|---|---|
| ≥90% | keywords only, no AI column |
| 60-90%, misses mostly true positives | add the AI column **behind a gate** |
| <60% | **your keyword set is wrong. Fix the keywords before reaching for AI** |

### Note D: phrase-token matching, not substring

Description filters typically match **whole phrase tokens**, case-insensitively — no substring, no
stemming. Measured on the same window:

| Phrase | Matches |
|---|---|
| `cold call` | 996 |
| `cold calling` | 2,065 |
| `cold outreach` | 2,339 |
| `outbound prospecting` | 2,796 |
| `cold email` | 1,877 |
| `coldcall` | **0** |

**`cold call` matching fewer postings than `cold calling` is the proof**: under substring matching the
shorter phrase would be the larger set.

**Enumerate plural and gerund forms yourself.** A 5-phrase set got 59.8% recall where the 8-phrase set
got 67.4%.

### Note E: discovery mode is a different endpoint

A market-wide jobs search endpoint typically has **no company-domain filter at all**, so it cannot
answer "does this one domain have a posting". Use it only for discovery: pull every posting matching
your filters, paginate on the cursor, and join back to your TAM on the company identifier. **That is
a list-building move, not this playbook.**

### Note F: no cache, by decision

An earlier draft opened with a cache table. It is gone. The winning path is two free calls plus a
cheap line write, so **start at step 1 and re-hit the API every run.** If a big list feels expensive,
**dedup the input on bare domain for that run** instead.

## 4. Verification

**VERDICT: PASS 7/8 (87.5%)** | domain → company profile → postings filtered server-side by
description → line writer → **30-day freshness gate**.

The one failure quoted a 53-day-old posting that is no longer live — which is exactly what the
freshness gate now prevents.

## 5. Clay implementation

- **`clay-table.md`** — the column build, including the freshness-gate column you must not skip.
- **`clay-workflow.md`** — the CLI-buildable version.

## 6. Locked prompt

Model: a nano-class reasoning model **outside** Clay; `gpt-4o-mini` **inside** Clay. Two different
answers for two different reasons.

**Outside Clay:** `max_completion_tokens=2500`, **`reasoning_effort="low"`**, never `temperature`,
never `max_tokens`, flex tier for batch.

⚠️ **The reasoning-effort setting is not optional.** At a 900-token cap with default effort, **all 8
generating rows returned `finish_reason=length` with empty content**, and both retries failed
identically.

**And note how that failure hides: rows that had nothing to say still succeeded.** Your abstains look
healthy, and only the rows worth having die silently.

**Inside Clay: `gpt-4o-mini`, because Clay's model integration does not expose reasoning effort or the
completion-token cap.** That is the whole argument — every guard above is unavailable in a native AI
column, so a nano-class model inside Clay reproduces exactly this failure. If you want nano inside
Clay anyway, the only safe route is an HTTP column where you control the body. **That is a documented
parameter-coverage exception, not a licence to reach for HTTP at your model provider generally.**

**`gpt-4o-mini` is also cheaper here, which is easy to get backwards:**

| | input tok/row | **billed** output tok/row | total /1k |
|---|---|---|---|
| nano-class | 607 | **440** (~80 visible JSON + ~360 hidden reasoning) | **$0.21** |
| `gpt-4o-mini` | 607 | **~80** (no reasoning tokens) | **~$0.14** |

An earlier draft charged the mini-class model for 440 output tokens too and concluded nano was
cheaper. **That 440 is `usage.completion_tokens` measured on a reasoning model, and on a reasoning
model that number includes hidden reasoning tokens, which are billed as output.** A non-reasoning
model does not generate them, so charging it 440 overstates its cost by about 5x.

```text
STATIC PREFIX (byte-identical across calls, keep first)

You write one short clause for a cold email. You are given open job postings that a company published on LinkedIn in the last 60 days. Every posting shown already matched the client's keyword filter, so the hiring signal is real. Your only job is to name the role in plain words.

Return JSON only, exactly these keys:
{"job_posting_line": "...", "role_named": "...", "evidence_url": "...", "confidence": "high|low"}

Rules for job_posting_line:
- It must read correctly inside this sentence: "Saw <job_posting_line>."
- Start with "you" and a lowercase letter. No capital letter at the start. No period at the end.
- Name one role only. If several postings are shown, pick the most senior sales or outbound role, otherwise the first one.
- Rewrite the raw job title into words a person would say out loud. Drop pipes, dashes, requisition codes, bracketed tags, city names, and words like REFER.
- 5th-grade reading level. 12 words or fewer.
- No em dashes. No en dashes. Hyphens are fine inside a normal word.
- Never invent a role that is not in the postings shown.
- If no posting is shown, return "" for job_posting_line and "low" for confidence.

Set role_named to the cleaned role words only. Set evidence_url to the LinkedIn URL of the posting you used. Set confidence to "high" when one posting clearly names a role, "low" when the titles are vague or conflicting.

Examples:
Input: Company: Gong | Postings: [{"title":"Mid Market Account Executive, Financial Services","url":"https://www.linkedin.com/jobs/view/x1"}]
Output: {"job_posting_line": "you're hiring a mid market account executive", "role_named": "mid market account executive", "evidence_url": "https://www.linkedin.com/jobs/view/x1", "confidence": "high"}
Input: Company: Ramp | Postings: [{"title":"Sales Enablement | SDR","url":"https://www.linkedin.com/jobs/view/x2"}]
Output: {"job_posting_line": "you're bringing on a new sales development rep", "role_named": "sales development rep", "evidence_url": "https://www.linkedin.com/jobs/view/x2", "confidence": "high"}
Input: Company: Acme | Postings: []
Output: {"job_posting_line": "", "role_named": "", "evidence_url": "", "confidence": "low"}

PER-ROW DATA (appended last)
Company: <company domain> | Postings: <deduped postings JSON>
```

**This prompt earns no cache discount.** `cached_tokens` came back 0 on all 16 calls, because the
prefix is ~490 tokens and caching engages at 1,024. **Do not pad the prompt to game that; just do not
budget for the discount.**

### Verifier pass: not needed for the claim. A freshness gate IS mandatory.

The model quotes a title from a payload it was handed and returns the source URL, so **there is
nothing to fabricate** — the live test confirmed it: every evidence URL grepped back to the raw
source verbatim, zero inventions.

**What the model cannot know is whether the role is still open.** A `date_posted` is when the
provider *observed* the posting, not proof the job is live.

So: **detect on 60 days, but suppress the line in copy when the posting is older than 30 days.** That
is a **formula, not a model call**, and it must be the field bound into copy. **Build the table
without it and you have rebuilt the one failure in the live test.**

**Truncation guard:** `finish_reason == "length"` with empty content means retry, never abstain.
Transport errors need their **own separate retry with backoff — they are not verdicts either.**

## 7. Edge cases and failure modes

| Symptom | Cause | Fix |
|---|---|---|
| A filter appears to do nothing and results look fine | **Unknown keys are silently stripped** | Check the spelling. Compare counts with and without the filter before trusting it |
| The signal "does not exist" in your market | You scanned returned fields instead of filtering server-side | Note A: **1 of 8 vs 5 of 8** on identical keywords |
| Recall is much lower than expected | Phrase-token matching, and you enumerated only the base form | Note D. `coldcall` matches **0** |
| The line quotes a role that is no longer open | A `date_posted` is an observation date, not a liveness check | **The 30-day gate.** Accept it kills some genuinely open roles |
| Empty content on exactly the rows that had postings | Reasoning burned the completion budget. **Rows with nothing to say still succeeded, so the abstains look healthy** | Low reasoning effort and a 2500-token cap outside Clay; a non-reasoning model inside Clay |
| The line quotes another company's posting | The domain→profile resolution landed on the wrong company | **A name-match gate is mandatory**: compare the returned company name to your list's company name before using any posting |
| Copy contains a requisition code or a pipe | The raw title reached the output | The rewrite rules. Raw titles are not copy |
| An AI classifier is proposed before any measurement | Habit | Run the three-call recall test first. **Under 60% recall means your keywords are wrong, and AI will not save them** |

### Hard rules

- **Filter server-side. Never scan returned fields for description language.**
- **Bind copy to the freshness-gated field, never the raw one.**
- **A name-match gate runs on every row** whose posting came from a domain→profile resolution.
- **Send a browser User-Agent**; several of these APIs sit behind a CDN that 403s default runtime
  agents while allowing `curl`.
