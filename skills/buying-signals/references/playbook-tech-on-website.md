# Playbook: Technology On Website

> All rules here are best practice, not law. Override any of them when the campaign calls for it; note the best practice once and move on.

## 1. Trigger and scope

**Use when:** the offer only makes sense to companies running a specific piece of software on their
site — a Shopify app, a Klaviyo migration, a HubSpot implementation, a WordPress maintenance offer.
Works in both directions: **discovery** ("build me a list of every company on Shopify") and
**enrichment** ("here are 4,000 domains, which run Klaviyo").

**Do not use when:** you want the software a company *sells*, or mail-infrastructure targeting.

**Default output:** `tech_confirmed`, `tech_stack_verified` (JSON array), `tech_evidence`,
`tech_checked_at`. Abstain = `false` / `[]` / `""`.
**On request only:** `tech_on_website_line`, 110 chars.

> **The sentence is opt-in.** The job is the **verdict**: does this company run the technology, and
> how do we know. That is what a list gets gated on, and for most campaigns it is the entire
> deliverable. Write the clause only when the brief explicitly asks. **Never let an unrequested
> sentence be the reason a row costs a model call.**

### The thing that makes this playbook necessary

**A technographic database tells you what a crawler saw at some unstated point in the past, and it
is wrong often enough to embarrass you.**

In the graded test, **4 of the 10 companies a provider returned from its own Shopify filter were not
on Shopify. Two were not ecommerce at all.**

The homepage verifier is not a quality step. **It is the gate.** Nothing reaches copy without it.
Plan for roughly **60% of a provider-sourced list to survive verification, so pull 1.7x what you
need.**

## 2. Run it: tandem discovery, then the gate

**The two discovery lanes run IN TANDEM and the result is a union.** Not a waterfall, not a choice.

Measured: two providers' first pages returned **74 domains and 60 domains with zero overlap.**
Whichever single provider you pick, you leave most of the market on the table.

Watch two things when you compare them:

- A contact-oriented provider returns **contacts**, so page it with a per-company cap of 1. **Never
  compare its raw count to a company-oriented provider's company count.**
- Both cap per filter combination (commonly 25,000 and 50,000). **Shard by state or headcount band**
  and let the union dedupe.

**No cache. Recompute — it is cheap.** Every source is free except the rendering proxy, which only
touches rows flagged `blocked`, so re-verifying a domain a previous campaign saw costs one homepage
GET.

```bash
# 1. TANDEM DISCOVERY. Both lanes, together.
discover-tech --provider a Shopify --all --out a.txt
discover-tech --provider b Shopify --all --out b.txt

# 1c. union + dedupe, printing the per-source overlap
union-domains a.txt b.txt --out domains.txt --provenance sources.csv

# 2. THE GATE
verify-tech-html domains.txt > verified.jsonl

# 3. rescue ONLY the blocked rows (metered, explicit confirm)
jq -r 'select(.blocked == true) | .domain' verified.jsonl > blocked.txt
proxy-rescue blocked.txt --confirm --max 500 > rescued.jsonl

# 4. merge: a rescued row replaces its blocked counterpart, one row per domain
jq -s -c 'group_by(.domain) | map(sort_by(.blocked) | .[0]) | .[]' \
  verified.jsonl rescued.jsonl > final.jsonl

# 5. put target_tech on every row
attach-row-context final.jsonl --target-tech Shopify > ready.jsonl

# 6. THE DEFAULT LAST STEP: the verdict. No model calls, no cost.
tech-verdict ready.jsonl > verdicts.jsonl
```

**Stop there unless a sentence was requested.** `verdicts.jsonl` is the deliverable.

## 3. The gate

A browser-UA homepage GET at concurrency 2, matching fingerprints over **HTML and response
headers**. Two behaviors carry the whole playbook.

### Blocked is a flag, never an inference

**A bot wall is not an answer.**

This is subtle and it bites: a common CDN matches on its own `server:` header, so a 403 used to come
back as a *successful* fetch with a non-empty detection list — which reads downstream as "we looked
and found nothing." **A silent false abstain.**

The verifier emits `"blocked": true` with a `blocked_reason` on HTTP 401/403/405/429/503, any other
4xx/5xx, **a body under 2,000 bytes**, or a transport error — and strips infrastructure and
analytics hits out of the detection list.

**Route on the flag, never on an empty list.**

### Platform hits are graded

A `Shopify` fingerprint fires on HTML-only strings like `cdn.shopify.com` and
`<store>.myshopify.com` — **which every Shopify agency portfolio, app-review roundup and Buy-Button
B2B site also carries.** So platform hits require header or oracle evidence:

| Evidence | Grade | Result |
|---|---|---|
| response header (`x-shopid`, `x-shopify-stage`, `powered-by: shopify`) | **confirmed** | eligible for a clause |
| a technology oracle answered yes (`/products.json`, `/wp-json/`) | **confirmed** | eligible for a clause |
| HTML string only, no header, no oracle | **unconfirmed** | excluded from the stack, no clause |

Only Shopify and WordPress have oracles today, so an HTML-only match on any other platform stays
`unconfirmed` **by design. That costs recall and buys correctness.**

### Three outcomes that are NOT negatives

Getting this wrong is how a campaign quietly mails the wrong people.

| `confidence` | Meaning | Action |
|---|---|---|
| `blocked` | **the page was never read** | proxy rescue. **Never a negative** |
| `unconfirmed` | matched HTML only — the agency / Buy-Button shape | re-check by hand or with a tech-specific endpoint |
| `api_error` | a model call failed; **clause path only** | re-run those rows. **A provider error is never a verdict** |

`target_tech` is read **per row**, with a global default only. If neither is set, the script should
**error rather than grade everything against the wrong technology.**

### Adding a technology

**Never write a fingerprint from memory.** Learn it from a live sample: rank candidate strings by
specificity (support ≥30%, leakage ≤5%) against a control set.

⚠️ **The control set must control for the co-occurring platform, not just "any website".** A Klaviyo
sample surfaced `cdn.shopify.com` at **78% support / 0% leakage** — because most Klaviyo users are
Shopify stores. Control against Shopify stores, not against the open web.

Then: never add a bare vendor domain (`/klaviyo\.com/` matches every page that links to them);
prefer response headers; a platform-kind technology also needs an oracle; and pass a
3-positives / 3-negatives ritual before marking it validated.

### Downstream gate

If `tech_confirmed` is false: drop the clause through spintax and keep the row — **unless the whole
campaign premise is the technology** (a Shopify app), in which case exclude the row rather than send
a generic email a company will read as a mistake. **The brief must state which applies before the
list is built.**

## 4. Locked prompt (OPT-IN)

> **Skip this whole section by default.** If the brief did not ask for a personalization line, the
> run ends at the verdict: no prompt, no model calls, no guards.

Model: `gpt-4o-mini` inside Clay, a nano-class model elsewhere. Note the inversion: **nano's ~512
reasoning tokens make it the *more* expensive option for this prompt inside Clay.** Params:
`max_completion_tokens=2000`, `reasoning_effort="low"`, no `temperature`, JSON response format.

Everything above `PER-ROW DATA` is the static prefix and must stay byte-identical. **It took five
correction rounds to get clean, so start from this version rather than from scratch.**

```text
You write one short clause for a cold email, based only on technology that was verified on a company website.

Return JSON only: {"line": "...", "evidence": "...", "confidence": "high|low"}

Rules:
- The clause must read grammatically inside this exact sentence: "Noticed LINE."
- Write it in second person. Always "you" or "your". Never "our", "we", "they", or the company name.
- The clause must contain a verb.
- Do not include the word Noticed. The clause is only the part that follows it.
- Name each product at most once. Never repeat a product name inside one clause.
- Spell every product name exactly as it appears in VERIFIED_TECH, including its capital letters.
- Do not capitalize the first word unless that word is a product name.
- No trailing period. Maximum 110 characters.
- 5th-grade reading level. No em dashes. No exclamation marks.
- Only name technology that appears in VERIFIED_TECH. Never infer a tool that is not listed.
- If VERIFIED_TECH does not contain the technology named in TARGET_TECH, return "" for line and "none" for confidence.
- Copy EVIDENCE into the "evidence" key exactly as given. Never put words from EVIDENCE into "line".
- Banned words in "line": header, html, tag, script, pixel, scraped, crawled, detected, database, tool, stack.
- When a second tool is listed alongside the target, name both. Two named tools read as real research, one reads as a guess.

Examples:
Input: TARGET_TECH: Shopify | COMPANY: Bombas | VERIFIED_TECH: Shopify, Klaviyo, Gorgias | EVIDENCE: x-shopid
Output: {"line":"you run Klaviyo and Gorgias on top of your Shopify store","evidence":"x-shopid","confidence":"high"}
Input: TARGET_TECH: Shopify | COMPANY: Leverify | VERIFIED_TECH: Shopify | EVIDENCE: x-shopid
Output: {"line":"your storefront runs on Shopify","evidence":"x-shopid","confidence":"high"}
Input: TARGET_TECH: Shopify | COMPANY: Lulu and Georgia | VERIFIED_TECH: Shopify, Klaviyo, Attentive, Zendesk | EVIDENCE: x-shopid
Output: {"line":"you send with Klaviyo and Attentive on your Shopify store","evidence":"x-shopid","confidence":"high"}
Input: TARGET_TECH: HubSpot | COMPANY: Northwind Logistics | VERIFIED_TECH: HubSpot, WordPress | EVIDENCE: js.hs-scripts.com
Output: {"line":"you run your site on WordPress with HubSpot behind the forms","evidence":"js.hs-scripts.com","confidence":"high"}
Input: TARGET_TECH: Shopify | COMPANY: Acme Consulting | VERIFIED_TECH: WordPress, HubSpot | EVIDENCE: none
Output: {"line":"","evidence":"","confidence":"none"}

PER-ROW DATA (appended last)
TARGET_TECH: {{target_tech}} | COMPANY: {{Company Name}} | VERIFIED_TECH: {{Tech Verified}} | EVIDENCE: {{tech_evidence}}
```

**Post-guards run in code after the model, because a prompt rule is a request and a regex is a
guarantee.** A rejected row ships the abstain value and records why.

**No second verifier model call:** the claim is already grounded in a live fetch of the company's own
site seconds earlier. That is a genuinely stronger guarantee than an LLM judge, and it is why this
playbook does not have one.

**Truncation guard:** `finish_reason=length` means retry, never abstain.

## 5. Verification

**VERDICT: PASS 10/10 (100%)** | tandem discovery, unioned → homepage gate → verdict |
**$0.00/1k on the default verdict path**, ~$0.25/1k when the clause is requested.

**The number to carry into planning: the provider's raw precision was 6/10. The path scores 100%
because the gate catches the other 4.**

⚠️ **This verdict covers Shopify only.** Every other fingerprint is unvalidated. Re-run if the
confirmed rate drops below 50% for two consecutive campaigns, if Shopify stops setting its
identifying header, or when adding an unvalidated technology.

## 6. Clay implementation

- **`clay-table.md`** — the column build, including how to reach a verifier from Clay.
- **`clay-workflow.md`** — the CLI-buildable version.

## 7. Hard rules

- **A blocked row is never a negative.** `blocked: true` means "we could not look", not "there is
  nothing there". Whatever you persist must keep `blocked` and `blocked_reason` **beside** the
  verdict, or a bot-wall 403 reads as a confident "no technology found". Same for `unconfirmed` and
  `api_error`.
- **Exact array-element match, never a substring test.** `"Shopify Buy Button".includes("Shopify")`
  is `true` — **and that is exactly how a B2B software company gets a storefront clause.** Drop
  embed-kind hits before the model. A platform-kind target additionally needs header or oracle
  evidence.
- **Only one fingerprint has been validated end to end.** Never let a client hear the tested number
  applied to an untested fingerprint.
- **No output sentence unless the operator asks.**
- **Pacing and targeting:** the rendering proxy runs only on blocked rows — that is an accuracy rule,
  not a budget one. Count before you pull where counts are free. Shard past per-filter caps rather
  than paging into them. Browser User-Agent on every homepage fetch, concurrency 2.
- **Sequencer update-in-place usually requires the email address in the request body**, or the write
  silently no-ops and every row keeps its old clause. Upload responses over-count — true net-new is
  a lead-count delta (often returned as a string, so cast it).
