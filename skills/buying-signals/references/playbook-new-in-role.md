# Playbook: New in Role

> All rules here are best practice, not law. Override any of them when the campaign calls for it; note the best practice once and move on.

**Use when:** the campaign angle depends on the buyer being new in the seat, because a new leader
is rebuilding their stack, has budget to reallocate, and has not yet formed a vendor preference.

**Do not use when:** you want people who moved to a **new company** regardless of title, or you
want the company-level hiring story. Use `playbook-hiring-surge` for headcount growth and
`playbook-fundraising` for the "they just raised, so they are buying" angle.

**One-line output:** `new_in_role_line = "you stepped into the COO seat at Northwind in April"`

## 1. Trigger and scope

This playbook answers one question: **which people in my target market took their current job
title in the last N months, and what one sentence can I open an email with?**

It is a **filter-at-source** signal, not an enrichment. You do not buy a list and then ask a
vendor "is this person new?". You ask the people database to only return people whose current
role started recently, and the answer comes back with the start date already attached. That is
why it costs essentially nothing and why the false-positive rate on tenure is near zero.

Two things it explicitly does not do. It does not tell you whether the move was a step **up**,
only that the person changed titles — a President who becomes COO trips the same signal, and the
locked prompt is written so the copy stays true either way. It does not find the person's email;
run your email waterfall first so you never spend enrichment on rows that will fail the email gate.

### Pick your recency window

**Default: 90 days**, expressed as `person_time_in_current_role: {min:0, max:3}` (the filter is
month-level, so 3 months is the month-level expression of 90 days).

**Know the volume cost before you build the lane, because it is steep.** Measured on one base
(US, `VP of Operations`, headcount 50 to 1000):

| Window | Rows |
|---|---|
| unfiltered | 1,662 |
| 0 to 6 months | 22 |
| 0 to 3 months | 2 |

Tightening from 6 months to 90 days cost about **90% of the rows** on that base. A single title at
90 days is a handful of people, not a campaign.

**Widen when the list is too thin, in this order:**

1. **Widen the title family.** A measured five-title operations family returned 1,925 rows at 6
   months versus 22 for one title on a comparable base. Titles multiply volume far harder than the
   window does. This is almost always the right fix.
2. **Drop the headcount floor or widen the geography.**
3. **Widen the window to 6 months**, and only then. Above 9 months the "just started" premise
   stops being credible and the copy starts lying, so **9 months is the ceiling** regardless of
   how thin the list is.

Record the widening and the reason in the campaign brief.

### Cheap pass or robust pass

Decide before you build. These are not the same product.

| | **Cheap pass (default)** | **Robust pass (opt in)** |
|---|---|---|
| Source | Prospeo `/search-person` | a LinkedIn Sales Navigator scraper on Apify |
| Cost | effectively $0 for the data, $0.053 per 1,000 rows for the model | metered: roughly **$3.20 per 1,000 profiles** discovered plus **$4 per 1,000** hydrated to full profiles |
| Tenure precision | **month-level.** `{min:0, max:6}` is an exact month range | **coarse.** A "changed jobs in the last 90 days" boolean, and a bucket that bottoms out at "less than 1 year". You cannot ask for 0 to 6 months |
| Freshness | database snapshot, can lead a public announcement by about a month | LinkedIn-live, but **LinkedIn keeps stale results**, so a cleanup pass is mandatory |
| Use it when | almost always | the client is high value, the vertical is one the database is thin on, or the campaign's whole premise is the job change |

Worth internalizing, because it generalizes past this playbook: **the expensive LinkedIn-live
source has a coarser tenure filter than the free database.** You buy freshness and coverage, and
you pay for it in precision plus a mandatory cleanup pass. Never run the robust pass silently
because the cheap pass came back thin. Say what it will cost, get a yes, then run it.

## 2. Output contract

### Inputs required per row

| Field | Type | Source | Required? |
|---|---|---|---|
| target job titles | string[] | campaign brief / ICP | yes, this is the search input |
| headcount range | {min,max} int | ICP | yes |
| geography | string[] | ICP, as location strings like `"United States #US"` | yes |
| recency window (months) | int | operator, default 3, ceiling 9 | yes |
| `company_domain` (bare, lowercase, no `www`) | string | returned by the search | produced, not supplied |

Rows are **produced by** this playbook, not fed into it. If you already have a list and want to
know which of those people are new in role, restrict the same call with
`company: { websites: { include: [ ...up to 500 domains... ] } }`.

### Output fields

| Field | Type | Example | Max length | Null allowed? |
|---|---|---|---|---|
| `new_in_role_line` | string | `you stepped into the COO seat at Northwind in April` | 90 chars | yes, empty string |
| `role_change_type` | enum | `promotion` or `new_hire` | 9 | no |
| `role_start_month` | string | `April 2026` | 20 | no |
| `months_in_role` | int | `4` | n/a | no |
| `prior_title` | string | `Chief Business Officer` | 120 | yes, empty string |

`role_change_type`, `role_start_month`, `months_in_role` and `prior_title` are computed
**deterministically** from the source's `job_history` array. The model never decides them. Only
`new_in_role_line` is written by the model.

**Abstain value:** `""` (empty string). Never "N/A", never "null", never a guess.

### Coverage expectation

Read these as **three separate numbers**. They are not the same thing, and campaign sizing depends
on telling them apart. Measured on 10 rows:

| Metric | Measured | What it means |
|---|---|---|
| **Produced rate** (non-empty line) | **10/10** | Of the rows that clear the title gate, essentially all get a line. This is **not** a rate over the raw pull — the title-gate drop rate was not recorded, so size the campaign off rows that survive the gate |
| **Factual-error rate** | **1/10** | About 1 in 10 prospects could receive a confident but wrong statement about their own job title. This is the real exposure |
| **Empty rate** (model abstained) | **0/10** | The abstain path exists but did not fire |
| **Usable rate** (produced and correct) | **9/10** | The headline number |

The single error was **not** a missing value and **not** a tenure error. The database asserted a
title the company's own site contradicts, and the model faithfully turned that wrong fact into
polished copy. **No downstream verifier over your own output can catch this**, because the output
is a correct rewrite of a wrong input. See §6 for the optional cross-check.

The "zero false positives" result below refers **only to tenure**. It is not a statement about
title accuracy.

Because the signal is a source-side filter, coverage on the rows it returns is high by
construction. The number that varies is **volume**, not hit rate.

### Copy-fit rules

- Slots into: `Saw {{new_in_role_line}}.` as the first sentence of email 1.
- **Starts lowercase.** No trailing punctuation — the frame supplies the period.
- Maximum 90 characters, 5th-grade reading level, no em dashes.
- Company name must be the short spoken form. "ATG", not "ATG (Auction Technology Group)".

### Downstream gate

If `new_in_role_line` is empty: **drop the personalized clause via spintax and keep the row** — the
row still matches the ICP. Do not leave a blank gap in the email. If the campaign's entire premise
is the job change (a "congrats on the new seat" campaign), exclude the row instead and say so in
the brief.

The empty case is the *cheap* case. The expensive case is the ~10% wrong-title case above, which
arrives as a **non-empty, well-formed line** and therefore passes every structural QC.

There are two controls and **they address different failures. Do not confuse them:**

1. **Title gate (free, mandatory) — controls loose-contains noise only.** `person_job_title` is a
   loose contains match that can hit a **past** role, so the pull returns people whose current
   title is unrelated to the search (measured: a `Chief Operating Officer` query returned an
   "Adult Basic Education Instructor"). The gate drops those. **It cannot catch a wrong source
   title** — the one observed factual error had a `job_history` current title that *did* contain
   the target keyword, so the gate passed it and the wrong line shipped. Running the gate does not
   reduce the ~10% factual-error rate at all.
2. **Leadership-page cross-check (cheap, optional) — the only control for a wrong source title.**
   Cross-check the title against the company's own leadership page (see
   `playbook-google-site-search`). Turn this on for any client sensitive to being wrong about a
   prospect's title. If you skip it, budget for roughly 1 in 10 prospects receiving a confident but
   wrong statement about their own job.

## 3. Source chain (cost-tagged)

| # | Source | Cost | Exact call | Stop rule |
|---|---|---|---|---|
| 1 | Prospeo `/search-person` | **FREE** to CHEAP | `POST https://api.prospeo.io/search-person`, header `X-KEY: $PROSPEO_API_KEY`, body below | always start here |
| 2 | Clay **Find people** source, built in a new workbook through the UI | FREE to METERED | set job title, location, headcount and the recent-role-change filter in the UI, run, then export or webhook the rows out | only if step 1 returned fewer rows than the campaign needs |
| 3 | Apify LinkedIn Sales Navigator scraper (the robust pass) | **EXPENSIVE** | actor with `recentlyChangedJobs: true`, `currentJobTitles`, `locations`, `companyHeadcount`, `profileScraperMode: "Full"` | only when the operator chose the robust pass and knows the cost |
| 4 | Model line writer | CHEAP ($0.053 / 1,000 rows) | `POST https://api.openai.com/v1/chat/completions`, params in §6 | always runs, on whichever source produced the facts |

Step 1's body:

```json
{ "page": 1,
  "filters": {
    "person_location_search": { "include": ["United States #US"] },
    "person_job_title": { "include": ["Chief Operating Officer"] },
    "company_headcount_custom": { "min": 50, "max": 2000 },
    "person_time_in_current_role": { "min": 0, "max": 3 }
  } }
```

`max:6` is what was graded; `max:3` is the default. The hit rate does not move with the window,
only the volume does.

### Rejected alternatives, and why

- ⛔ **A CLI "find people" substitution.** It returns only the latest experience, **no job
  history**, so `role_change_type`, `prior_title` and `prior_company` cannot be derived at all and
  the promotion-versus-new-hire branch disappears. Worth generalizing: **"needs no browser" is not
  automatically the better path.** When a substitution changes what comes back, that is a contract
  change, not a convenience.
- ⛔ **Generic LinkedIn search APIs with no tenure filter.** Common ones expose title, company,
  industry, location and school filters and **no tenure, months-in-role, or start-date filter**, so
  they cannot express this signal at any price. No subscription tier fixes that.
- **Per-person "enrich" endpoints** that would make a clean tenure check are frequently gated off
  standard plans. Check before designing around one.
- **Scraping LinkedIn for tenure.** Career history is already a structured field on the people
  database, so scraping is pure cost.
- **`person_time_in_current_company` as the primary.** It answers "how long at the company", which
  misses every internal promotion — and internal promotions were **8 of the 10** rows in the live
  test. Use it only as a secondary filter to separate new hires from promotions.

## 4. Verification

**VERDICT: PASS 9/10 (90%)** | best call = Prospeo `/search-person` with
`person_time_in_current_role` → model line writer at minimal reasoning effort | p50 latency
1.1s/row | ~$0.05 per 1,000 rows | tested on 10 graded rows.

A separate true-negative test confirmed 3 of 3 long-tenure incumbents (30, 43 and 145 months in
seat) are present in the database and correctly excluded by the filter. Zero false positives on
tenure.

**This verdict covers exactly one path:** the script path calling Prospeo `/search-person` and then
the model at minimal reasoning effort, graded end to end against a second source per row.

| Path | State |
|---|---|
| Script: Prospeo → model API | **GRADED, PASS 9/10** |
| Clay table recipe (`clay-table.md`) | ⚠️ **specification, never built** |
| Clay workflow recipe (`clay-workflow.md`) | ⚠️ **specification, never built** |
| Clay "Find people" source (#2) | ⚠️ never built — row shape and tenure granularity unknown |
| Apify robust pass (#3) | ⚠️ never run — filter grammar read from the actor schema only |

Re-test if the usable rate drops below 60% for two consecutive campaigns, if the filter schema
changes, or if a campaign reports a "you just started" line landing on a long-tenured incumbent.

## 5. Clay implementation

Two ways to run this continuously:

- **`clay-table.md`** — build it as columns on a table. Read `clay-playbooks/clay-table-harness.md` first.
- **`clay-workflow.md`** — build it as a workflow from the CLI. Read `clay-playbooks/clay-cli-harness.md` first.

Both are unbuilt specifications. The script path in §4 is the verified one.

## 6. Locked prompt

Model: a small reasoning model (`gpt-5-nano` class). On a measured 732 input and 42 output tokens
per row it is roughly 3x cheaper than a mini-tier model with no quality gap on a pure rewrite.

Params: `max_completion_tokens=2000`, **`reasoning_effort="minimal"`**, no `temperature`, and a
flex/batch service tier for overnight runs.

```text
You write one short opening clause for a cold email, about a person who recently changed jobs.

You will be given verified facts about one person. The facts are already true. Your only job is to turn them into one natural clause.

Return JSON only, exactly these keys:
{"new_in_role_line": "...", "role_change_type": "promotion|new_hire", "confidence": "high|low"}

Rules for new_in_role_line:
- It must read correctly inside this sentence: "Saw <new_in_role_line>."
- Start with a lowercase letter. No period at the end. No quotation marks.
- Maximum 90 characters.
- Say the seat and the company and roughly when. Use the month name given, or say "earlier this year" if the month is more than 4 months ago.
- Only say "earlier this year" if the start year given is the CURRENT year. If the start year is any earlier year, say the month and the year, for example "in September 2026". Never say "earlier this year" about a date in a previous year.
- If role_change_type is promotion, say they stepped into or took over the seat. Do not say they joined the company. Never say "moved up", "got promoted", or "was promoted": an internal move is not always a step up and we cannot prove it was.
- If role_change_type is new_hire, you may say they joined.
- Use the shortest natural form of the company name. Drop anything inside parentheses, drop legal suffixes like LLC, Inc, PLC, Ltd, and drop trailing descriptive phrases after a comma. "ATG (Auction Technology Group)" becomes "ATG". "A.Y. Strauss, LLC" becomes "A.Y. Strauss".
- 5th-grade reading level. Short words.
- No em dashes. No en dashes. Hyphens are fine only inside a number range.
- Never invent a fact. Only use the facts given. Do not mention headcount, industry, funding, or anything not in the facts.
- If the facts are missing the title, the company, or the start month, return "" for new_in_role_line and "low" for confidence.

Examples:
Facts: first_name=Dana | current_title=VP of Operations | company_name=Gymshark | role_start_month=March 2026 | months_in_role=3 | role_change_type=new_hire | prior_title=Director of Supply Chain | prior_company=Represent
Output: {"new_in_role_line": "you joined Gymshark as VP of Operations back in March", "role_change_type": "new_hire", "confidence": "high"}
Facts: first_name=Marcus | current_title=Chief Operating Officer | company_name=Irby Utilities, LLC | role_start_month=February 2026 | months_in_role=6 | role_change_type=promotion | prior_title=Senior Vice President | prior_company=Irby Utilities, LLC
Output: {"new_in_role_line": "you stepped into the COO seat at Irby earlier this year", "role_change_type": "promotion", "confidence": "high"}
Facts: first_name=Priya | current_title= | company_name=Northwind Labs | role_start_month= | months_in_role= | role_change_type=new_hire | prior_title= | prior_company=
Output: {"new_in_role_line": "", "role_change_type": "new_hire", "confidence": "low"}

PER-ROW DATA (appended last, as the user message, never merged into the block above)
Facts: first_name={{First Name}} | current_title={{Current Title (from job_history)}} | company_name={{Company Name Clean}} | role_start_month={{Role Start Month Label}} | months_in_role={{Months In Role}} | role_change_type={{Role Change Type}} | prior_title={{Prior Title}} | prior_company={{Prior Company}}
```

**The cross-year guard is load-bearing.** The "earlier this year" rule was originally unqualified,
which generates **factually false copy** for any role that started in the previous calendar year.
With a 6-month window, every run between January and May hits those rows: a run in February sees
roles that started in September, five months earlier, and the model would write "earlier this
year" about last year. Both `months_in_role` and the year are already in the facts, so the guard
is free. This case is **unmeasured** — the graded run happened in August, so no graded row had a
previous-year start. Re-grade 5 rows the first time you run a window that crosses a year boundary.

**Date format, one rule:** `role_start_month` is always the **month-name form** (`April 2026`),
never `2026-04`. The prompt says "use the month name given", so a numeric month would force the
model to convert it silently, which is exactly the drift the locked prompt exists to prevent.

**The model's `role_change_type` is discarded.** The prompt still asks for it — that is the exact
prompt that was graded, so it stays byte-identical — but it is an echo, not a decision. The real
value is computed deterministically from `job_history`. If the model's value were ever allowed
through, a flipped `promotion` to `new_hire` would make the copy claim someone "joined" a company
they have worked at for years.

Everything above the `PER-ROW DATA` marker is the static prefix and stays static.

⚠️ **No prompt-cache discount applies here, and the cost math must not assume one.** Automatic
prompt caching engages at 1,024+ prompt tokens. This prompt is 732, so it never qualifies and the
effective floor stays **$0.053 per 1,000 rows**. Padding the prefix past 1,024 tokens costs more
input tokens than the discount returns at this size. Keep the static-prefix-first structure
anyway — it starts paying the moment the prompt grows.

**Verifier pass: not needed, by design.** The model is never given the open web and is never asked
to establish a fact. Every fact in its input was already proven by the structured `job_history`,
and the deterministic fields are computed in code before the call. The residual risk is that the
**source is wrong about the title**, which no verifier over your own output would catch. If a
client is sensitive to that, add the leadership-page cross-check rather than a verifier over the
generated line.

**Truncation guard:** `finish_reason=length` means retry, never abstain. This fired on **10/10
rows** at default reasoning effort, returning empty content while burning the full budget on
reasoning. `reasoning_effort:"minimal"` is the fix and is not optional.

## 7. Edge cases and failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Every call returns HTTP 400 `INVALID_FILTERS` | You used `person_time_in_current_position` | The real key is **`person_time_in_current_role`**, value `{min,max}` integer **months**, 0 to 600. There is no string range form; `"0-6"` is rejected |
| Filter silently does nothing, list is full of 10-year incumbents | A script swallowed the 400 above and shipped the unfiltered result | Assert that `pagination.total_count` dropped versus the unfiltered baseline, and fail the run on any non-200 |
| A made-up filter name returns the same error as a real one | `INVALID_FILTERS` does not distinguish "unknown key" from "bad value" | Do not discover keys by probing. Read the filter docs |
| `error_code: NO_RESULTS` kills the whole run | An empty result set comes back as **HTTP 400** with `{"error":true,"error_code":"NO_RESULTS"}`, so `if (j.error) throw` crashes on a normal empty pull — common on the narrow windows this playbook recommends | Branch on `error_code === "NO_RESULTS"` **before** the generic error branch and return zero rows. Do not retry it |
| `company_domain` filter returns `INVALID_FILTERS` | Wrong key shape | Use `company: { websites: { include: ["acme.com"] } }`, max 500 domains |
| Result has a current title unrelated to the search | `person_job_title` is a loose contains match and can hit a **past** role | Gate in code on `job_history[current].title`, never on `person.current_job_title`. **The gate list must include abbreviations** ("COO", "VP Ops"), not just the searched titles |
| Line says "moved up" but the prior title was more senior | `positions_at_company > 1` proves an internal move, never its direction | The locked prompt bans "moved up" and always says "stepped into". Do not relax this |
| Line contains a legal suffix or a parenthetical | Raw company name reached the prompt | Run `playbook-company-name-cleaning` first. The prompt strips them as a second line of defence |
| Copy says a month one off the press release | Start month can precede the public announcement by about a month | Acceptable. The prompt may say "earlier this year" for anything over 4 months old |
| LinkedIn URL does not resolve, or resolves to a different person | Stale slug (measured on 1 of 10 rows) | Never key the email waterfall solely on the returned LinkedIn URL; work from name plus domain too |
| Model returns empty strings for every row | `finish_reason=length`, reasoning ate the budget | `reasoning_effort:"minimal"`. Retry on `length`, never record it as an abstain |
| Volume collapses to almost nothing | Expected at the 90-day default | Widen the **title list** first, then headcount or geography, then the window to 6 months. Never past 9 |
| The robust pass returns people who changed jobs a year ago | **LinkedIn keeps stale results.** The 90-day flag is LinkedIn's own and it is not aggressively retired | **Cleanup is mandatory on every robust-pass run, budget for it before you quote the job.** Hydrate to full profiles, read the current experience start date, drop every row outside your window. Treat the filter as a cheap pre-filter, not the gate |

### Hard rules

- **Prospeo pacing:** 2 to 2.5 requests per second is the vendor ceiling. 25 results per page,
  1,000 pages maximum, so **25,000 results per filter combination** — split by US state to go past
  that. Credits are charged per request that returns at least 1 result, and repeating identical
  filters plus page within 30 days returns free.
- **Many data vendors sit behind Cloudflare** and return 403 to a default Python or Node user
  agent while allowing `curl`. Send a browser User-Agent on every call, or your batch silently
  403s while your manual test passes.
- **A provider's own `email_status: "VERIFIED"` is not send-ready.** Everything still goes through
  your own validation waterfall.
