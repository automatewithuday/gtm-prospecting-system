# Playbook: Hiring Surge

> All rules here are best practice, not law. Override any of them when the campaign calls for it; note the best practice once and move on.

**Use when:** the angle is "you are scaling this team right now".

**Do not use when:** you want the job ad itself (`playbook-job-posting-language`), the person who
just started (`playbook-new-in-role`), or money rather than people (`playbook-fundraising`).

**One-line output:** `hiring_surge_line = "your sales team has 8 people who started new roles in the last six months"`

## The three things you cannot get wrong

1. **It is role starts, not hires. Measured 28.3% internal moves.** The filter counts people whose
   *current role started* in the window — promotions, re-titles and lateral moves included. Ship
   `started new roles`; never `hired`, `added`, `brought on`.
2. **Never buy a LinkedIn URL with enrichment credits to feed this.** The company-enrichment action
   that returns one costs ~8 credits per company and was, by three orders of magnitude, the largest
   cost line here. Use a free LinkedIn URL off your intake payload where you have one, and the bare
   normalized domain everywhere else. Both are free.
3. **The gate is a ratio PLUS absolute floors:** `role_starts >= 2 && dept_total >= 4`. This cuts
   the qualifying segment from 14.6% to **5.2%**, so plan roughly **96,000 source rows per
   5,000-lead campaign**. Do not loosen it to hit volume; source more rows.

## 1. Trigger and scope

A hiring surge is a **department-level** fact, not a company-level one. "This company grew from 200
to 260 people" is almost useless in copy, because the reader cannot tell whether it means anything
to them. "Your sales team has 8 people who started new roles in the last six months" is specific,
checkable, and implies a budget owner. This playbook produces the second kind.

The whole signal comes from one Clay **table action**, `Find Employee Headcount by Criteria`, which
is **free on every Clay plan**. It counts how many people currently at a company match a filter
set, and it accepts a recency filter (`current_role_max_months_since_start_date`), so running it
twice per department gives you the department total and the department's last-6-months intake in
one pass. No other vendor does department-sliced recency counts at zero marginal cost. That is why
this playbook has exactly one source and no expensive fallback.

### Four things it does not do

- **It does not tell you who.** Counts only. Names are a different, non-free action.
- **It does not date the starts.** The copy can only ever say "in the last six months", never "in
  March".
- **It does not pick your departments.** Sales and marketing are the two shown here; the same
  pattern extends to engineering, RevOps, customer success or finance.
- **It does not prove anyone was HIRED.** Read this one before you write copy.

### The promotion confound, measured

The filter counts people whose **current role started** in the last 6 months. That set includes
external hires, internal promotions, title changes and lateral moves. LinkedIn also generates a new
role start date when someone merely edits or re-titles an existing position.

- Supported by the data: `your sales team has 8 people who started new roles in the last six months`
- **Not supported, do not ship:** `you added 8 people to the sales team in the last six months`

The second sentence is a factual claim about the reader's own team that they can disprove instantly
if three of those eight were promotions, and cold copy does not survive that.

**The over-count rate is measured: 28.3%.** Of 276 people whose current role started inside a
six-month window across 18 companies, **78 were already working at that company before the window
opened**. Sliced by title: sales-titled **24.4%**, marketing-titled **34.6%**. And that is a *lower
bound* — the detector only sees a prior role that started 7+ months ago, so a February joiner
promoted in July counts as a joiner. Real examples from the audit: a Business Development
Representative who became a Mid-Market Account Executive; a Manager of Customer Success who became
a Senior Manager; a Project Manager II who became a Project Manager III.

On one company in the audit, **5 of the 7 recent sales starters were internal moves** — "you hired
3 people for sales" would have been wrong about most of the evidence behind it.

Treat every count as an **upper bound** on hires. Roughly 1 reply in 4 has a right to say "nobody
joined my team, I was promoted", and the locked prompt is written so that reply contradicts
nothing you sent. If a client insists on "you hired", show them the 28.3% first. That is an
operator sign-off, not a default.

**Re-measuring the confound on a new ICP is free** (about 40 searches). Per company, run two people
searches: one for `current_role_max_months_since_start_date: 6` (the population the gate counts),
one for everyone already there before the window (`include_past_experiences: true` with a
`role_range_end_month` of `YYYY-MM`). Intersect on the LinkedIn profile URL: anyone in both started
a new role at a company they already worked at.

## 2. Output contract

### Inputs required per row

| Field | Type | Source | Required? |
|---|---|---|---|
| `company_linkedin_url` | string | your intake payload, as a free formula column | yes when present — this is the preferred and free identifier |
| `company_domain` (fallback) | string, bare lowercase, no `www` | your list, via `Normalize a Domain` | yes when no LinkedIn URL, which on a measured intake is **83.6%** of rows |

The action prefers a **LinkedIn company URL** — it is the identifier the underlying people dataset
is keyed on. A bare domain forces a resolution step that can silently land on a different company,
so the name-collision guard in §7 is **mandatory** on those rows.

The identifier waterfall, in order:

1. **Free LinkedIn URL from your intake payload.** Measured populated on **16.35%** of rows.
2. **Bare company domain** on the other 83.6%. Free. Accept the collision risk, apply the guard.
3. If a client genuinely needs LinkedIn URLs resolved at scale, resolve them **outside Clay** with a
   domain-to-LinkedIn enrichment endpoint and webhook them in. Never buy them with Clay credits.

Stated plainly: on the 83.6% bare-domain rows the identifier is weaker and some counts will land on
the wrong company. That is the right trade at 8 credits a row, but **nobody has measured how much
the bare-domain path degrades the 0.28% cell error rate** — every measurement below was taken on
rows identified by a purchased URL. Measure it if you run a large batch.

### Output fields

| Field | Type | Example | Null allowed? |
|---|---|---|---|
| `sales_headcount_total` | integer | `28` | no, `0` when nobody matches |
| `sales_hires_6mo` | integer | `8` | no, `0` |
| `marketing_headcount_total` | integer | `15` | no, `0` |
| `marketing_hires_6mo` | integer | `2` | no, `0` |
| `hiring_surge_dept` | string | `sales` | yes, `""` when the gate says NO |
| `hiring_surge_hires` | integer | `8` | yes, `0` when the gate says NO |
| `hiring_surge_line` | string | see above, max 90 chars | yes |

`hiring_surge_hires` counts **role starts**, not hires. Nothing downstream may relabel it —
including a copywriter editing the sequence by hand.

**Abstain value:** `""` for the line and the department, `0` for the count. The counts themselves
never abstain: a company with no sales team returns `0`, which is a real answer.

### Coverage expectation

Measured on **3,964 distinct companies**:

| Metric | 98-row sample | **3,964 companies** |
|---|---|---|
| Sales roster resolved (1+ person) | 52% | **35.1%** |
| Marketing roster resolved | 61% | **45.3%** |
| Either department resolved | 71% | **52.9%** |
| Ratio gate = YES | 17% | **14.6%** |
| Gate = YES **with the absolute floors** | not measured | **5.2%** |
| Action cell error rate | not measured | **0.28%** (11 of 4,000) |

Note how optimistic the 98-row sample was. **Plan list size on 5.2%, not 17%.** Filling a 5,000-lead
campaign takes roughly **96,000 source rows**.

The floors delete 64% of the gated segment, and that is the price of the precision they buy: on 20
held-out companies the gate with floors scores **17/20 (85%)** against **10/20 (50%)** without them.
The rows they delete are the ones that would tell a two-person law firm its marketing team is
scaling.

### Copy-fit rules

- Slots into: `Noticed {{hiring_surge_line}}.`
- **Second person only.** The clause must never contain the company name. That removes the
  dependency on name cleaning and a whole class of capitalization bugs — a v1 prompt that allowed
  the company name *and* required a lowercase first letter produced "silktide added 8 people".
- Starts lowercase, no trailing period, no em dashes, under 90 characters, 5th-grade reading level.
- The time phrase is always "in the last six months" or "over the past six months". Never a month
  name, never a date, because the source does not carry one.

### Downstream gate

If `hiring_surge_line` is empty: **exclude the row from this campaign.** This is one of the few
playbooks where empty means exclusion rather than a spintax drop, because the entire campaign
premise is the surge. Route excluded rows to a fallback campaign.

## 3. Source chain (cost-tagged)

| # | Source | Cost | What it does | Stop rule |
|---|---|---|---|---|
| 0 | Company-wide growth pre-filter (list build only) | FREE | `POST /search-company` with `company_headcount_growth: {min:50}` | **optional and marginal.** Only when your TAM is 4x+ oversized |
| 0b | Department contact-count pre-filter (list build only) | FREE | a contacts `search/count` endpoint filtered by job function | drop companies with no department at all before they reach Clay |
| 1 | Free LinkedIn URL from intake | FREE | formula column | **16.35%** fill |
| 2 | Bare domain from `Normalize a Domain` | FREE | the fallback identifier | covers the other 83.6% |
| 3 | **Clay `Find Employee Headcount by Criteria` x4 columns** | **FREE** | the engine | only advance if the action is removed or made paid |
| 4 | Model phrasing pass, gated rows only | CHEAP | see §6 | only when `Hiring Surge Dept` is non-empty |
| 5 | A people-data-vendor employee-count action | METERED (~5 credits/row, **charged even on a miss**) | fallback | only if step 3 is unavailable and the operator signed off |

**Cost summary, per 1,000 source rows: four FREE columns plus about $0.0135 of model spend at the
14.6% gate rate, or $0.0048 at the floors' 5.2%. That is the entire cost.** There are no
enrichment credits in this chain. What remains is Clay table run time, which is why the free
pre-filters are still worth running on a large intake.

### On step 0, with the measurement

§1 argues company-level growth is nearly useless as a signal, and step 0 filters on exactly that.
It was measured by taking companies whose gate outcome was already known and asking which sit
inside the growth pool:

| Sample | In the `headcount_growth >= 50` pool |
|---|---|
| 200 gate-YES | 48 (24.0%) |
| 200 gate-NO | 44 (22.0%) |
| at 200 vs 200 | 2.0 points, z = 0.47, **p = 0.64, nothing** |
| 579 gate-YES | 158 of 575 (27.5%) |
| 579 gate-NO | 127 of 578 (22.0%) |
| at 579 vs 579 | 5.5 points, z = 2.17, **p = 0.03** |

Converted to what matters against a 14.6% base rate: **17.6% inside the pool clear the gate against
13.7% outside.** A 1.28x relative lift bought with about **76% of your TAM**. Use it only when the
TAM is at least 4x oversized. A `min:200` variant showed 9.0% vs 12.0%, pointing the wrong way — do
not use it.

**The method is reusable and worth stealing.** You do not need to run the expensive step on 400 new
companies to answer "does this pre-filter predict my gate". Take companies whose outcome you
already have, send their domains to the filter in batches of 200 to 500, and read the total count
with and without it. Four calls instead of four hundred.

### Rejected alternatives

- **Per-company department counting via a people-search API.** Measured: combining a company filter
  with a job-title filter returned `NO_RESULTS` on all three test companies while the unfiltered
  company query returned 53, 351 and 45 people. The title filter does not compose with the company
  filter the way you would expect, so a department count means paging the whole roster and regexing
  titles yourself. Fine for verification, far too slow for production.
- **A `company_headcount_by_department` filter.** The name is accepted but every inner shape tried
  returned `INVALID_FILTERS`. Shape unknown; worth a support ticket, since it would give a free
  department-level TAM pre-filter.
- **Per-company LinkedIn scraping.** It is per-company scraping where the Clay action gives a
  department count for free.
- **Richer "employee trends" enrichments.** ~10 credits per row for trend data you do not need for
  one clause. Only for a client who explicitly buys on headcount trend charts.

## 4. Verification

**VERDICT: PASS 17/20 (85%)** on held-out companies. The floors were **benched, not fitted**:
17/20 with them, 10/20 without, on 20 companies drawn blind from a batch created *after* the floors
were written.

The one miss was a wrong abstain in financial services — see §7.

## 5. Clay implementation

- **`clay-table.md`** — the full column build. This is the primary path: the whole chain runs in
  Clay, because the headcount action has **no API surface anywhere** and exists only as a table
  action. Read `clay-playbooks/clay-table-harness.md` first.
- **`clay-workflow.md`** — a CLI-buildable approximation, for the parts that *do* have workflow
  actions. Read `clay-playbooks/clay-cli-harness.md` first.

⚠️ Both are unbuilt specifications.

## 6. Locked prompt

**Model choice, with the arithmetic.** Measured on 10 gated rows per model. The prompt is **502
tokens** as sent.

| Model and params | Clean JSON | p50 latency | Completion tokens | Reasoning tokens | Per 1,000 source rows at 5.2% |
|---|---|---|---|---|---|
| **`gpt-4o-mini`**, `max_tokens=300` | **10/10** | **0.93s** | 28 | 0 | **$0.0048** |
| `gpt-5-nano`, 1200 tokens, default effort | **0/10** | 9.58s | 1200 (capped) | 1200 | unusable |
| `gpt-5-nano`, 3000 tokens, default effort | 3/3 | 11.6s | 1445 | 1408 | $0.031 |
| `gpt-5-nano`, **`reasoning_effort="minimal"`** | 1/1 | 2.70s | 37 | **0** | **$0.0021** |

Two things matter here:

**A small reasoning model at default effort returns empty content on this prompt.** Ten of ten rows
came back `finish_reason=length` with an empty message after burning the entire 1,200-token budget
on reasoning. `reasoning_effort="minimal"` is the fix and makes it both reliable and the cheapest
option in the table.

**Inside Clay, ship `gpt-4o-mini`.** Clay's AI column does not expose `reasoning_effort`, so inside
Clay the nano-class model is the default-effort row above: 6.5x more expensive than mini and empty
on every row at 1,200 tokens. **Outside Clay, use the nano-class model with minimal effort**, which
is 2.3x cheaper than mini.

Params: `max_completion_tokens=1200` (never `max_tokens` on a reasoning model) plus
`reasoning_effort="minimal"`, no `temperature`, flex tier for batch outside Clay.

```text
STATIC PREFIX (byte-identical across calls, keep first)

You write one short clause for a cold email. The clause tells a company that we noticed people on one of their teams recently started new roles.

You are given a department name and how many people on that team started their current role in the last 6 months. The number is already verified. Your only job is wording.

IMPORTANT: the number counts people who STARTED A NEW ROLE. Some of them were hired from outside and some were promoted or moved internally. You cannot tell which. So never say the company hired, added, brought on, recruited, or grew by those people. Say that those people started new roles, or are new in their roles, or joined that team.

Return JSON only, no prose, no code fence:
{"hiring_surge_line": "...", "confidence": "high|low"}

Rules:
- The clause must read correctly inside this sentence: "Noticed <hiring_surge_line>."
- Write it in second person, about "you" or "your team". Never write the company name.
- Start with a lowercase letter. No trailing period. No em dashes. 5th grade reading level.
- Use the exact number you are given. Never invent a number, a job title, a person, or a date.
- Say "in the last six months" or "over the past six months". Never a specific month or date.
- Never claim the company hired anyone. Say people started new roles.
- Keep it under 90 characters.
- confidence is "high" when the number is 3 or more, otherwise "low".

Examples:
Input: {"department":"sales","role_starts_last_6_months":8}
Output: {"hiring_surge_line":"your sales team has 8 people who started new roles in the last six months","confidence":"high"}
Input: {"department":"marketing","role_starts_last_6_months":3}
Output: {"hiring_surge_line":"on your marketing team, 3 people started new roles in the past six months","confidence":"high"}
Input: {"department":"sales","role_starts_last_6_months":2}
Output: {"hiring_surge_line":"you have 2 people on the sales team who started new roles in the last six months","confidence":"low"}

PER-ROW DATA (appended last)
{"department":"{{Hiring Surge Dept}}","role_starts_last_6_months":{{Hiring Surge Hires}}}
```

Notice what the prompt refuses to let the model say: that anyone was hired. The input field is
named `role_starts_last_6_months` rather than `hires` for the same reason, so a future editor
cannot casually reintroduce the claim.

Notice what is **not** in this prompt: the abstain decision, the department choice, and the company
name. All three were in v1 and all three caused failures. The abstain and department logic moved
into deterministic formulas; the company name was removed from the output shape entirely.

**Cache note.** At ~460 tokens this sits below the 1,024-token prompt-cache floor, so measured
`cached_tokens` was 0 on every call. Expected and fine at this size. Keep the static prefix first
anyway — if a client variant grows it past 1,024 the discount switches on for free.

**Verifier pass: not needed, and this is the rare playbook where that is genuinely true.** The
number is copied from a deterministic count the model is told not to change, and the only date
reference is a fixed six-month phrase. There is no free-text claim to fabricate. What *can* go
wrong is upstream — wrong company matched, stale data, the promotion confound — and a second model
call sees none of that, because it only sees the same number. Spend the effort on the §7 identity
checks instead.

**Truncation guard:** `finish_reason == "length"` with empty content means retry at 3,000 tokens,
never abstain. Setting `reasoning_effort="minimal"` takes the truncation rate to zero and is the
shipped fix; keep the retry ladder as a second line of defence, not as the plan.

## 7. Edge cases and failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Prospect replies "nobody joined my team, I was promoted" | 28.3% of role starts are internal moves | The locked prompt says "started new roles", true of promotions and joins alike, so the reply contradicts nothing. Never ship a hire claim |
| A 45,000-person enterprise fires the gate on below-average churn | The `roleCount > 6` absolute override has no upper bound. Observed: a 1,896-person sales function with 95 six-month role starts — 5.3%, **below** normal churn. **1.0% of gated companies** | ⚠️ Unvalidated guard: require the ratio clause (not the `>6` override) on any department with 200+ people, or drop the override entirely. **Bench it on a fresh blind draw before shipping**, exactly as the floors were benched |
| An agency fires the sales gate on client-service staff | At marketing and creative agencies, `Account Executive` and `Account Manager` are client service, and the `Sales` function counts them | ⚠️ Unvalidated guard: exclude those titles when the industry is Marketing Services, Advertising or Design, or route agencies through `job_title_keywords` instead |
| A financial-services company abstains when it should not | In finance and professional services the sellers are titled `Principal`, `Business Development` or `Client Relationship`, which `job_functions=["Sales"]` does not catch. **This was the only miss in the bench** | Add a third department column bound to `job_title_keywords: ["business development","client relationship","partnerships"]` for those ICPs |
| Every row returns "No Role Found" for a department | `job_functions` got a value outside the enum. **A wrong enum value does not error, it silently returns zero** | Only `"Sales"` and `"Marketing and Public Relations"` are confirmed. Test any new value on 10 known-good companies first, or use free-text `job_title_keywords` |
| Copy reads "silktide added 8 people" with a lowercase company name | v1 allowed the company name in a clause that also required a lowercase first letter | v2 removes the company name entirely. **Never put a company name in a clause with a lowercase-first rule** |
| A 4-person marketing team that added 1 person is flagged YES | The raw percentage check has no absolute floor: 1/(4-1) is 33%, over the 15% threshold | The `hires >= 2 && total >= 4` floors |
| Growth percent shows `Infinity` | The whole department started inside the window, so `total - recent == 0`. **This is a real surge, not an error** | The check treats `"Infinity"` as YES on purpose. Leave it |
| Counts belong to a different company with the same short name | Two different companies can share a short name, and a bare domain invites the collision. This is the identifier on ~83.6% of rows | **Mandatory guard:** sanity-check the returned count against your list's known headcount, abstain when a department count exceeds the company's known total, and abstain on any company whose name is a short generic token |
| A LinkedIn URL contains a raw `&` | Observed: `https://www.linkedin.com/company/cr&t` | Percent-encode company URLs before any bulk URL operation |
| Model returns empty with `finish_reason=length` | Reasoning overrun. Happens when the prompt asks the model to make a **judgment call** rather than just phrase something | Retry once at 3,000 tokens. If it still empties, **the prompt is the problem: move the decision into a formula** |
| A growth filter seems not to filter | An unrecognized inner key is **silently ignored** rather than rejected | Always sanity-check a filter by comparing total counts with and without it before trusting it |
| A company record's AI-generated description describes a completely different business | Observed on a real record | Never use a vendor's AI description field for copy. Use the human-written description |
| 47% of companies resolve no department at all | Small, non-US or LinkedIn-thin companies genuinely have no visible department roster. **This is a correct abstain, not a failure** | Plan around the 5.2% rate. Do not "fix" it by loosening the gate. Pre-filter with the free count in step 0b so these rows never consume Clay run time |
| Counts look plausible but no second vendor confirms the recency half | Contact-database snapshots lag, so their recency counts run about a third low (observed 3 vs 6, 8 vs 23) | Verify the recency half against the same people dataset that produced it, which returns names, titles and role start dates |

### Hard rules

- **Do not buy company enrichment to get a LinkedIn URL here.** ~8 credits per company. Related
  trap: `Find Employee Headcount by Criteria` is a **free** Clay action, but a similarly named
  third-party `Get Employee Count by Criteria` costs **5 credits even when it finds nothing**.
  Check which one your column is bound to.
- **One lead is never in two of your campaigns at once.** If you also run `playbook-new-in-role`,
  the push gate must exclude people who personally just started, or the same person gets two
  different sequences from you.
- **The count is role starts, not hires.** No copy, no variable name, no client-facing summary may
  call it hires.
