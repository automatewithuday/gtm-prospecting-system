# Playbook: Case-Study Lookalikes (filter mining, not raw lookalike)

> All rules here are best practice, not law. Override any of them when the campaign calls for it; note the best practice once and move on.

**Use when:** a client has a case study, a flagship logo, or one obviously happy customer, and you
want the list of companies for whom that story is the strongest thing you could say.

**Do not use when:** you are building a whole market from an ICP sentence with no standout customer
to anchor on; or you want to name a customer off the **prospect's own** case-study page ("saw your
work with Intercom") — that is the opposite direction and belongs to `playbook-case-study-page`.

See also `disco-like` in this repo for plain seed-domain lookalike discovery. **This playbook is the
higher-precision version**: it mines *why* the story resonates before it searches.

**One-line output:** `case_study_ref = "attentive"` with
`lookalike_case_study_line = "a marketing platform about your size"`.

### ⚠️ Merge-field collision warning

`playbook-case-study-page` pushes a lead-level field literally named `case_study_line`, whose value
completes a **different** sentence (`Saw your work with Intercom.`). This playbook's descriptor is
therefore named **`lookalike_case_study_line`**. **Never rename it back.** If both playbooks run on
the same campaign, a shared field name silently overwrites and renders
**"We did this for your work with Intercom."**

## 1. Trigger and scope

A case study only works on someone who **recognises themselves in it**. "We took an SMS marketing
platform from 3 meetings a month to 22" lands hard on another marketing software company with a
similar go-to-market, and lands on nobody else. So build the list **backwards from the story**, not
forwards from the client's broadest ICP.

**The naive move is to paste the case-study company into a lookalike engine and ship what comes
back. That was measured at 40% usable**: the vector matched on "is about marketing" and returned
agencies, a marketing trade publication, and a Power BI blog alongside real software vendors.

**What this playbook does instead:** write down the 2 to 5 attributes that are the real reason the
story resonates — in the worked example: B2B software vendor, product is marketing technology, US,
50 to 2,000 people — express each as a database filter, **intersect those filters with the lookalike
anchor**, and read the result.

**That intersection measured 100% usable.** It is also small, which is the point: **the intersection
is how you learn the filters and train the judge. It is not the final list.**

## 2. Output contract

### Inputs

| Field | Type | Required? |
|---|---|---|
| `case_study_domain` | string, bare, lowercase | yes |
| `case_study_text` | 200 to 2,000 words | yes — this is what the decomposer reads |
| `client_offer_summary` | 3 to 6 lines | yes |
| `geography`, `headcount_band` | strings | yes, always legal pre-filters |
| `domain`, `company_description` | strings | yes, for the labelling half |
| `exclusion_list` | CSV of domains | no, but **always ask** |

### Output fields

| Field | Type | Example | Null? |
|---|---|---|---|
| `case_study_ref` | slug | `attentive` | no inside the segment |
| `lookalike_case_study_line` | generic descriptor, ≤70 chars | `a marketing platform about your size` | yes |
| `case_study_match_reason` | ≤140 chars, **QA only, never sent** | `sells customer engagement software to consumer brands` | yes |
| `attribute_card` | JSON, **one per case study, not per row** | see §6 | no |

**Abstain value:** `""`. The gate is `qualified: false` paired with an empty `case_study_ref` — the
two always agree.

### The descriptor is generic on purpose

`lookalike_case_study_line` is deliberately a **generic descriptor, not the case-study company's
brand name.** Naming a third party's brand in cold copy is a client-facing decision, and the
descriptor form costs almost nothing: **"we did this for a marketing platform about your size"
carries the same recognition as the brand name, and it never creates a permissions problem.**

Flip it to brand-naming only when the client explicitly okays it for a publicly published case
study.

### Coverage expectation

**10/10 usable (100%)** on the intersection path.

⚠️ **Read that number correctly. Coverage is near-total *by construction*, because the segment is
defined by the filters, so every row in it matches the case study.**

**The metric that actually varies is segment size.** The tested intersection returned **21
companies**. The number to watch in production is not hit rate — it is whether the widening steps get
you to campaign volume **without precision falling back to the 70% that unanchored keyword filtering
produced.**

## 3. Source chain (cost-tagged)

Steps 1 and 2 fingerprint the case study. **Step 3 is the precision core.** Steps 4 and 5 are where
volume comes from.

| # | Source | Cost | What it does | Stop rule |
|---|---|---|---|---|
| 1 | An internal company database, the case-study company's own record | FREE | read its description and offerings | always run. `found: 0` just means the decomposer works from the case-study text alone |
| 2 | A company-search API on the case-study domain itself | FREE | **this is how the database tags it, which is the taxonomy your filters must speak** | always run, **then run the industry-enum bake-off below.** The returned industry is a **candidate, never automatically the filter** |
| 3 | **The lookalike anchor intersected with the mined attribute card. THE RECOMMENDED CALL** | FREE | `company_lookalike` + `company_industry` + `company_keywords` + headcount + location | **10/10 usable, 21 companies.** Advance whenever the count is below campaign volume, which is almost always |
| 4 | The same attribute card **with the lookalike anchor removed**, then every row through the model judge | CHEAP | paginate to completion, judge each row | **7/10 raw, ~95% after the gate.** Always run when step 3 is short. **Never skip the judge — the raw 70% is what makes unanchored filters dangerous** |
| 5 | **Snowball:** re-run the step 3 call once per confirmed member as a new seed, union, repeat | FREE | adds 30 to 100% on top of step 4 | stop when net-new drops below 2 to 3% per round |
| 6 | An entity-search API | METERED | last resort | only if 3 to 5 are still short, or the category is genuinely absent. ⚠️ **These pad to the match limit with junk, so never trust one without the judge**, and they often return profile URLs rather than domains |

### The industry-enum bake-off (do not skip)

**A database's industry tag on the case-study company is frequently NOT the enum you want to filter
on.**

Measured: one marketing-software vendor is tagged **`Advertising Services`** — but the winning 10/10
call filters on **`Software Development`**. `Advertising Services` is **the bucket the agencies live
in**, and it is exactly the bucket that produced the 40% failure this playbook exists to avoid.

So the database's own tag is a candidate, never the answer. The procedure is free, because a page-1
total count costs nothing:

1. **Collect candidates:** the case-study company's own industry, plus the industries assigned to the
   3 to 5 companies in the raw lookalike page an operator reads as obviously right.
2. **For each candidate, run the step 3 call once with only that enum swapped in.** Record the total
   count and eyeball the first 10 names and descriptions.
3. **Keep the candidate whose sample is dominated by companies of the right TYPE** — product vendor
   vs agency vs publisher. Break ties towards the larger count.
4. If two enums both look right, **include both.** It is a union.

**Write the chosen enum, and the ones you rejected and why, into the run notes.** That one sentence
is what stops the next operator repeating the bake-off.

## 4. Verification

**VERDICT: PASS 10/10** on the intersection path. The unanchored arm measured **40% usable**, and
keyword-only filtering without the judge measured **70%**.

⚠️ Cost is an **estimate, not a measurement**: the live test made 3 database calls and **zero model
calls.** Comparable prompts in sibling playbooks measured $0.05 to $0.27 per 1k. **Treat any figure
under that as a floor and measure on a 50-row batch before quoting it.**

## 5. Clay implementation

- **`clay-table.md`** — the labelling half as columns.
- **`clay-workflow.md`** — the CLI-buildable version.

## 6. Locked prompts

Two prompts. **Prompt A runs once per case study. Prompt B runs per row.**

This prompt is **input-heavy**, so pick the model with the cheapest input rate at standard pricing.
Params: `max_completion_tokens=300`, never `temperature`, flex tier for batch.

### Prompt A — the decomposer (once per case study)

```text
STATIC PREFIX (byte-identical across calls, keep first)

You are a B2B list-building analyst. You will be given one customer case study, a profile
of the company the case study is about, and a summary of what the seller offers. Your job
is to explain why this story would resonate with a company, in attributes that a company
database can filter on.

Return JSON only:
{"resonance_reasons": ["..."], "industry_enum_candidates": ["..."], "keywords_include": ["..."],
 "keywords_exclude": ["..."], "headcount_min": 0, "headcount_max": 0, "geography": "...",
 "descriptor": "...", "confidence": "high|low"}

Rules:
- resonance_reasons: 2 to 5 short reasons, each one testable against a company description.
  "sells software to marketers" is testable. "is innovative" is not. Drop untestable ones.
- industry_enum_candidates: 2 to 4 CANDIDATE enum strings, ranked best first, for a human to
  bake off against total_count. Include the exact industry string the database assigns to the
  case-study company, but do NOT assume it is correct: databases often tag a software vendor
  by who it sells to. Rank first the enum that names what the company IS, then the database's
  own tag, then at most 2 adjacent ones.
- keywords_include: 3 to 6 phrases that name what the product IS. Prefer 2 and 3 word
  phrases. Never include a word so common in the category that every company carries it.
- keywords_exclude: words that pull in agencies, publishers, marketplaces, and staffing
  firms in the same topic space.
- descriptor: how to describe the case-study company in cold copy WITHOUT naming its brand,
  4 to 10 words, lowercase, no trailing period. It must read correctly inside this
  sentence: "We did this for DESCRIPTOR."
- Never invent a fact. If the case study does not say it, it is not a reason.
- No em dashes.

Examples:
Input: case study about an SMS and email marketing platform selling to consumer brands,
1,500 people, US; seller runs cold email campaigns for B2B software companies.
Output: {"resonance_reasons":["sells marketing technology as a product, not as a service","sells to marketing leaders at consumer brands","US company big enough to have a dedicated demand generation team"],"industry_enum_candidates":["Software Development","Advertising Services","Marketing Services"],"keywords_include":["marketing platform","marketing automation","customer engagement platform"],"keywords_exclude":["agency","staffing","conference"],"headcount_min":50,"headcount_max":2000,"geography":"United States","descriptor":"a marketing platform about your size","confidence":"high"}

PER-CASE-STUDY DATA (appended last)
Case study text: <case study text>
Case study company profile: <profile>
Seller offer summary: <offer summary>
```

### Prompt B — the row judge and labeller (per row)

```text
STATIC PREFIX (byte-identical across calls, keep first)

You are grading whether one company would recognise itself in a specific customer story.
You will be given the attribute card that defines the story's audience, and one company's
name and description.

Return JSON only:
{"qualified": true|false, "case_study_ref": "...", "case_study_match_reason": "...", "confidence": "high|low"}

Rules:
- qualified is the gate. Set qualified true and return the case_study_ref given in the
  attribute card ONLY if the company satisfies EVERY resonance reason in the card.
  Otherwise set qualified false and return "" for case_study_ref. These two always agree:
  qualified false always pairs with an empty case_study_ref, never with a non-empty one.
- A company in the right industry with the wrong product does not match. A services firm,
  agency, publisher, marketplace, or community does not match a software product story.
- case_study_match_reason: under 140 characters, quote the part of the description that
  decided it. Always populate it, on qualified false rows too.
  This is internal QA text, never sent to anyone.
- Never invent a fact about the company. Judge only what the description says. A thin or
  empty description means qualified false, case_study_ref "", and confidence "low".
- No em dashes.

Examples:
Input card reasons: ["sells marketing technology as a product","sells to marketing leaders"]. Company: Customer.io, "Create personalized customer journeys that engage and convert with our versatile customer engagement platform."
Output: {"qualified":true,"case_study_ref":"attentive","case_study_match_reason":"customer engagement platform sold as a product to marketing teams","confidence":"high"}
Input card reasons: ["sells marketing technology as a product","sells to marketing leaders"]. Company: Fivetran, "Fivetran, the global leader in data movement, helps customers use their data to power everything from AI applications to analytics."
Output: {"qualified":false,"case_study_ref":"","case_study_match_reason":"data movement infrastructure, not marketing technology","confidence":"high"}

PER-ROW DATA (appended last)
Attribute card: <attribute card>
Company: <company name>
Domain: <domain>
Description: <company description>
```

### The verifier pass you DO need: liveness

**Not needed for fact hallucination** — prompt B only judges text it was handed and returns the
reason it used.

**What is needed is a liveness pass, because company databases happily describe companies that no
longer trade.** Fetch each live homepage, classify dead / parked / live, and **re-judge live sites on
their current content.**

**Always run it. Database descriptions qualify dead companies otherwise.**

## 7. Edge cases and failure modes

| Symptom | Cause | Fix |
|---|---|---|
| The list is full of agencies, publishers and blogs | You pasted the case-study company into a lookalike engine and shipped the output. **Measured 40% usable** | Mine the attributes first and **intersect** with the anchor |
| The right industry filter returns the wrong kind of company | **The database tags a software vendor by who it sells to** | The industry-enum bake-off. The database's own tag is a candidate, never the answer |
| The segment is tiny | **Expected.** The tested intersection returned 21 companies | Widen by dropping the lookalike anchor and judging every row — never by loosening the attributes |
| Precision collapses when you widen | Unanchored keyword filtering measured **70% raw** | **Never skip the judge.** ~95% after the gate |
| An entity-search API returns exactly the number you asked for | **These pad to the match limit with junk** | Never trust one without the judge |
| Dead companies qualify | Database descriptions outlive the business | The liveness pass |
| Copy renders "We did this for your work with Intercom" | Two playbooks pushed a field with the same name | Keep `lookalike_case_study_line` distinct from `case_study_line` |
| The judge qualifies a thin row | An empty description is not evidence | The prompt sets `qualified: false`, `confidence: "low"` on thin descriptions. Keep that rule |
