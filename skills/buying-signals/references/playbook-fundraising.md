# Playbook: Fundraising

> All rules here are best practice, not law. Override any of them when the campaign calls for it; note the best practice once and move on.

**Use when:** the angle depends on the prospect having money to spend or a mandate to grow — either
a TAM filtered to funded companies, or a first line that names their round.

**Do not use when:** you want headcount growth or open roles as the signal (`playbook-hiring-surge`).
If you want the round as a pure list filter and no copy at all, you only need lane A in §3.

**One-line output:** `funding_line = "Saw you raised $52M in the Series B."` — the whole sentence
lives in the variable. §2's downstream gate explains why that matters more than it looks.

## 1. Trigger and scope

Three separate questions get called "fundraising", and they route to different sources. **Do not mix
them up: one is a solved free problem and one is not solved at all.**

- **Lane A, ever raised.** "Only show me companies with venture backing." A search filter applied
  when the list is built. Free, reliable, no per-row work.
- **Lane B, the copy line.** "Write a first line about their round." A per-row lookup producing
  `funding_line`. **This is the main deliverable and the tested path.**
- **Lane C, raised in the last 30 days.** "Who closed this month?" **The people-database funding
  indexes lag 3 to 4 months, measured.** Lane C has no proven end-to-end path and is documented
  honestly below rather than faked.

Not covered: valuation claims, investor-name personalization, and anything reported only as a rumor.

## 2. Output contract

### Inputs required per row

| Field | Type | Required? |
|---|---|---|
| `domain` (bare, lowercase, no `www`, no scheme) | string | yes |
| `company_name` | string | no, used only for the abstain log and QA |

### Output fields

| Field | Type | Example | Max | Null? |
|---|---|---|---|---|
| `funding_line` | string | `Saw you raised $52M in the Series B.` | 90 | no, use the abstain value |
| `funding_clause` | string | `you raised $52M in the Series B` | 80 | no, use `""` |
| `funding_evidence_url` | string | a funding-round URL | 300 | no, use `""` |
| `funding_confidence` | enum | `high` / `low` | 4 | no |

**Abstain value:** `""`. `funding_confidence` is `low` whenever the line is empty.

### Coverage expectation

**8/10 rows usable (80%)**, where "usable" counts a **correct abstain** on a company that genuinely
has no recent round.

**Read the second number too:** only **2/10 rows produced a non-empty line**, because the test set
was adversarial — three bootstrapped companies and three whose last round is years old. On a list
already filtered through lane A with a 365-day funding window, every row has a funding event by
construction, so the non-empty rate is governed by the equity-stage filter and the 12-month window
rather than by source coverage. **That rate was not measured. Measure it on your first real campaign
before letting copy depend on the variable being present.**

### Copy-fit rules

Two fields, two different jobs. Keep them straight.

- **`funding_clause` is what the model writes:** lowercase first letter, no trailing period, under
  80 characters, 5th-grade reading level, no em dashes. It must read grammatically inside
  `Saw <funding_clause>.`
- **`funding_line` is what gets pushed:** deterministic **code** wraps the clause into
  `"Saw " + funding_clause + "."`. When the clause is `""`, the line is `""` too. **The model never
  writes this field, a formula does, so the wrapping cannot be forgotten or hallucinated.**
- Neither field ever names a month, a season, a year, or a date, and neither names total funding,
  valuation, or investors. §7 explains why, with measured error rates.

### Downstream gate — read this before wiring the email body

⚠️ **Spintax is a RANDOM chooser, not a conditional.**

`{Saw {{funding_line}}. |}` picks one of its branches at random on every row, with **no knowledge of
whether the variable is populated.** On rows that abstain it renders `Saw .` about half the time,
and on rows that DO have a line it **throws the personalization away** about half the time.

**Spintax can never be used as an if-populated gate for any variable, in this playbook or any
other.** This generalizes past fundraising and is probably the single most useful thing in this
file.

There are exactly two mechanisms that work. Pick one per campaign:

1. **Default: the self-erasing variable.** Put the entire sentence in the variable — which is why
   `funding_line` carries the leading "Saw" and the trailing period. The body line is just
   `{{funding_line}}` on its own line. An empty variable renders nothing, so an abstaining row
   simply loses that sentence and the rest of the email is untouched.
   **QA step:** after upload, preview one *abstaining* lead and confirm the paragraph collapses
   cleanly without leaving a double blank line.
2. **Split at upload time.** Partition the list into populated and empty, and upload two campaigns
   or two variants — one with the funding sentence hard-coded into the body, one without. Use this
   whenever the funding angle changes the whole email rather than one line, and whenever the
   non-empty rate is low enough that a single body would read oddly for most recipients.

Only exclude abstaining rows entirely when the campaign angle **is** the round.

The usual word-level spintax block for wording variety is unrelated and still required. **Spintax is
for wording variety, never for conditional content.**

## 3. Source chain (cost-tagged)

### Lane A, ever raised / raised within 6 to 12 months (list building)

| # | Source | Cost | Call | Hit rate |
|---|---|---|---|---|
| 1 | A people/company search API's funding filter | FREE | add a `company_funding.stage` array of equity stages to your ICP filters; for recency add a `funding_date` of `365` or `180` | **76%** of a US software 50-500 segment had raised at any stage, **65%** at an equity stage |

Equity stage set: `Pre seed`, `Seed`, `Series unknown`, `Series A` through `Series E-J`, `Angel`,
`Corporate round`, `Convertible note`, `Equity crowdfunding`.

### Lane B, the copy line (per row) — THE TESTED PATH

| # | Source | Cost | What it does | Result |
|---|---|---|---|---|
| 1 | Company lookup by domain, read the funding block | FREE | `{"filters":{"company":{"websites":{"include":["acme.com"]}}},"page":1}` with a browser User-Agent | 6/10 domains returned a funding record, 9/10 resolved to the correct company |
| 2 | **domain-equality guard (code)** | FREE | assert the returned `company.domain` equals the requested domain | **removed 1 wrong company out of 10.** Mandatory, never skip |
| 3 | **equity-stage and 12-month filter (code)** | FREE | drop `Secondary market`, `Private equity`, `Debt financing`, `Grant`, `Undisclosed`, `Non equity assistance`, all `Post IPO *`, `Product crowdfunding`. Then require the newest survivor to be ≤12 months old | **removed 3 misleading "latest rounds" out of 6.** Mandatory |
| 4 | Model phrasing | CHEAP, $0.22/1k | §6. **Wording only, never arithmetic or eligibility** | 2/2 eligible rows produced clean copy |

⛔ **There is no step 5.** If the lookup returned no company record at all, **the row abstains** and
the line is empty, which is the correct outcome for a signal you cannot evidence. Do not add a paid
company-enrichment fallback: it costs roughly 8 credits per company and does not carry funding
fields anyway.

### Lane C, raised in the last 30 days — NOT SOLVED

| # | Source | Cost | Reality |
|---|---|---|---|
| 1 | A funding-signals feed | cheap, per record | dates ran through yesterday, so **freshness is real**. But only 9 of 25 rows carried a clean company name, and **none carried a domain** |
| 2 | Model cleanup plus domain resolution | CHEAP | read company name + source URL + round type + amount, return `{company_name, is_closed_round, is_acquisition}`, then resolve name→domain | **not tested** |
| 3 | A web-research "find all" API | **EXPENSIVE** | **not tested.** Write a stated reason into the run notes before firing it, and cap the run |
| 4 | A funding database's UI export, by hand | expensive (seat) | reliable but manual. One-off urgent lists only, never a recurring campaign |

### Rejected alternatives

- **A people-database funding-date filter for lane C.** Measured: a 90-day window over the entire US
  Software Development market returned `total_count = 1`. **The index lags 3 to 4 months.**
- **Semantic "entity search" APIs for lane C.** 0 of 20 returned companies had a round inside the
  requested window. It returned public companies, companies its own payload labelled `Unfunded`, and
  one labelled `Acqui-Hired`. **Entity search ranks on static attributes and has no event-date
  awareness, so a date-bounded objective degrades into "companies that look fundable".**
- **`total_funding` as a copy fact.** One company came back at `$550.9M` where the press reported
  $452M, because these totals fold in debt facilities and secondary sales.
- **`raised_at` as a copy fact.** Off by 15 days for one company, one month for another, **two
  months** for a third.

## 4. Verification

**VERDICT: PASS 8/10 (80% usable) | claims 8/8 (100% correct)** | chain = company lookup by domain →
domain-equality guard → equity-stage + 12-month filter → model line writer | p50 3.0s/row | ~$0.22/1k.

**This is a claim-bearing playbook, so it carries two bars: 70% usable AND 90% claim correctness.**

The 90% is **coverage correctness, not coverage** — scored as `true claims / rows where a claim was
emitted`. A company that never raised, correctly abstained on, is a **correct outcome and leaves the
denominator entirely.** It is not a miss. The bar binds on truthfulness *when the signal exists*,
because **a fabricated round is the one failure nobody can fix after it sends.**

Both misses above were **coverage** misses (no record for one domain; a two-month date error pushed
one round outside the window), not false claims — which is why claim correctness is 8/8.

⚠️ **Lane A's end-to-end list quality was not graded. Lane C is untested end to end and must not be
described as working.**

## 5. Clay implementation

- **`clay-table.md`** — the 7-column build.
- **`clay-workflow.md`** — the CLI-buildable version.

## 6. Locked prompt

Model: the one this prompt was **graded** on. Params: `max_completion_tokens=3000` (never
`max_tokens` on a reasoning model), no `temperature`, `response_format={"type":"json_object"}`,
flex tier for batch.

⚠️ **No prompt-cache discount applies here.** The static prefix is ~520 tokens and caching engages
at 1,024+. `cached_tokens` was `0` on all 20 measured calls. **Do not budget for a cache discount.**

The prompt's JSON key is `funding_line` because that is byte-for-byte what was graded — but it holds
the **clause**. Code wraps it into the pushed sentence. **Do not edit the key to "fix" the naming;
that silently changes the tested prompt.**

```text
You write one short clause about a funding round for a cold email.

You will be given a JSON record for one company. Every fact in it has already been
checked. Your only job is wording. Do not do arithmetic and do not add facts.

Return JSON only, exactly these keys:
{"funding_line": "...", "evidence_url": "...", "confidence": "high|low"}

Rules:
- If eligible is false, return "" for funding_line and "low" for confidence. Nothing else.
- The clause must read grammatically inside this sentence: "Saw <funding_line>."
- Start with a lowercase letter. No trailing period. No em dashes. No quote marks.
- 5th-grade reading level. Under 80 characters.
- Use amount exactly as written in the record. Never change the number.
- If stage is not empty, name it. If stage is empty, say "round" instead.
- Never name a month, a season, a year, or a date. Never say "recently".
- Never mention total funding, valuation, or investors.
- Copy evidence_url from the record. Set confidence to the value in the record.

Examples:
Input: {"company":"Attio","amount":"$52M","stage":"Series B","eligible":true,"evidence_url":"https://www.crunchbase.com/funding_round/attio-series-b","confidence":"high"}
Output: {"funding_line":"you raised $52M in the Series B","evidence_url":"https://www.crunchbase.com/funding_round/attio-series-b","confidence":"high"}
Input: {"company":"Deel","amount":"$300M","stage":"","eligible":true,"evidence_url":"https://www.crunchbase.com/organization/deel","confidence":"high"}
Output: {"funding_line":"you closed a $300M round","evidence_url":"https://www.crunchbase.com/organization/deel","confidence":"high"}
Input: {"company":"Northwind Labs","amount":"","stage":"Series A","eligible":true,"evidence_url":"https://www.crunchbase.com/organization/northwind-labs","confidence":"high"}
Output: {"funding_line":"you closed the Series A","evidence_url":"https://www.crunchbase.com/organization/northwind-labs","confidence":"high"}
Input: {"company":"Acme Widgets","amount":"","stage":"","eligible":false,"evidence_url":"","confidence":"low"}
Output: {"funding_line":"","evidence_url":"","confidence":"low"}

PER-ROW DATA (appended last, as the user message)
<the eligibility record>
```

**Verifier pass: not needed, and deliberately so.** The usual reason to add one is that the model
might hallucinate a date or an amount. Here it is **structurally incapable** of it: eligibility, the
12-month arithmetic, the stage filter and the rounding all happen in code before the call, and the
prompt forbids dates, totals, valuations and investors outright. The only facts in play are a stage
string and a pre-formatted amount string, both copied verbatim. Spend the verifier budget on lane C
instead, where headline parsing genuinely can invent a round.

**Truncation guard:** `finish_reason=length` with empty content means **retry**, never abstain. A
reasoning model burns reasoning tokens before emitting content and can hit the ceiling on a trivial
prompt. Retry up to 3 times.

**What an unlocked prompt looks like:** the v1 of this prompt scored **4/10** and shipped
`you closed the Series E-J back in October` and `you have raised north of $550M to date`. Both are
exactly the failures the locked rules now forbid.

## 7. Edge cases and failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Lookup returns a **completely different company** | A website filter matches *other* listed websites too, so a vendor that lists your target as a customer wins the match. Observed live, with a total count of 1 and **no warning** | Assert the returned domain equals the requested domain. There is often no strict-domain filter available — a `company_domain` filter 400s |
| A first line calls a **secondary sale** a fundraise | The funding-events array includes `Secondary market` rows, sometimes with a large recent amount. One company had a $300,000,000 secondary | Filter to the equity stage set **before** sorting for the latest event. **Existing shareholders selling is not money the company raised, and a founder will notice** |
| A first line calls a **PE minority stake** a fundraise | Databases record a PE firm's purchase of a stake as a `Private equity` round | **Exclude `Private equity` by default.** Buying shares from existing holders is not money into the company, so calling it a raise is a false claim. Toggleable per campaign for a PE-adjacent offer; note the override |
| Copy contains `Series E-J` | That is a database bucket label for late-stage rounds, not a real round name | Blank it and fall back to the word "round". Same for `Series unknown` |
| The month in the copy is wrong | `raised_at` is systematically early. Measured: off 15 days, one month, and **two months** on three companies | **Never put a month or a date in the line.** The locked prompt forbids it |
| The total raised does not match the press | Database totals fold in debt facilities and secondary sales | **Never quote total funding.** Quote the round amount, which checked out exactly on 4 of 4 |
| A company that clearly raised gets an empty line | No record at that domain, or the round is newer than the index (3 to 4 month lag) | **Expected. Abstain is correct**, and the whole-sentence variable renders as nothing. Do not "fix" it by loosening the guard |
| An email goes out reading `Saw .` | Somebody wrapped the clause in spintax as an if-populated gate | **Spintax is a random chooser.** Use the whole-sentence variable or split at upload |
| A recency filter returns HTTP 400 | Some APIs return `400` with `NO_RESULTS` instead of an empty list | Treat `400 + NO_RESULTS` as zero matches, **not an outage.** A client that raises on any 400 looks broken |
| A "last 30 days" list is full of acquisitions and rumors | Funding feeds mix in acquisitions, VC **fund** closes (a firm raising its own fund), and rumors ("in talks to", "reportedly raising") | The cleanup step must return `is_closed_round` and `is_acquisition`, and you must filter on both |
| A "last 30 days" amount is absurd | Headline parsing produced **$600,000,000,000** from an article about AI budgets, and `0.261` USD tagged as debt | Require the amount to reconcile with the linked article, or drop the amount and name only the round |
| Empty model response with `finish_reason=length` | Reasoning overran the ceiling | Retry up to 3 times. **Never record it as an abstain** |
| Vendor timeout mid-batch | Transient | Retry once, then mark the row `error` and **exclude it from any hit-rate denominator. An API error is never a data verdict** |

### Hard rules

- **Pace company lookups at about 1 request per second.** Zero rate-limit errors were observed at
  0.8 req/s across 37 requests.
- **Funding-signal feeds usually charge per record returned.** A `limit: 200` call spends 200
  credits.
- **Spintax is a random chooser and must never gate a personalization variable.**
- **Never ship a model you have not graded on this prompt.** A cheaper model may look better on
  paper; if the abstain rule, the character cap, the lowercase-first rule and the no-date rule were
  never verified on it, it is untested. A $0.11 saving per 1,000 rows is not worth that.
