# Playbook: Company Name Cleaning

> All rules here are best practice, not law. Override any of them when the campaign calls for it; note the best practice once and move on.

## 0. Read this first: the AI prompt is a toggle, not the default

Clay ships a free, deterministic `Normalize Company Name` action (`titleCase: true`). **That is
the default and it stays the default.** Do not replace it reflexively, and do not make AI the
default.

Everything below — the locked prompt, the benchmark, the placeholder guard, the AI column — is the
**toggle**: what you switch on for one client, when the copy leans hard on the company name **and**
the raw strings are messy in ways a normalizer structurally cannot fix. Those are taglines after a
pipe, dba entities, parenthetical descriptors, appended city names, second-language duplicates, and
junk strings that need an abstain.

**Turn the toggle ON when all three are true:**

1. The copy names the company somewhere a reader will notice (a subject line, the first sentence, a
   possessive).
2. A 20-row read of the normalizer's output on the client's own list finds **more than about 2**
   values you would edit before sending.
3. Those failures are the model-shaped kind above, **not** simple suffix or casing problems. If they
   are suffix and casing problems, the free normalizer already handles them and the AI column buys
   you nothing.

**Otherwise leave it off.** Record which of the two this client is running, so QA reads the right
column and nobody re-litigates it mid-campaign.

This deliberately mirrors the opposite decision on first names. First-name cleaning is a **standing**
column, because a mangled first name breaks the greeting on every campaign that opens with one. A
mangled company name only breaks the campaigns that name the company. See
`playbook-first-name-cleaning`.

**Use when:** any campaign whose copy mentions the prospect's company by name, which is nearly all
of them.
**Do not use when:** you need a company *fact* — funding, hiring, tech, pricing. Those are separate
playbooks. Also not for deciding whether the company is real or in-ICP.
**One-line output:** `company_clean = "Hamiltons Bud and Bloom"` from the raw CRM string
`"318, Inc dba Hamiltons Bud and Bloom"`.

## 1. Trigger and scope

Lead databases store company names the way a registrar or a scraper found them, not the way a human
says them. Real strings from a live contacts table:

- `Ajax Turner Company, Inc.`
- `ABN TECH CORP`
- `AlaMark Technologies | FileMaker Consultants | Premier FileMaker Support | Hosting Services`
- `accounting business solutions`
- `Alraqhi Acessories for Building Materials | (the same name repeated in Arabic)`

Pasted straight into an email, every one of those reads like a mail merge, and the prospect stops
reading.

This playbook takes that string (plus the domain when you have it) and returns the short spoken
form. It strips legal suffixes, trademark marks, taglines, service lists, parenthetical descriptors,
appended city names and second-language duplicates. It fixes shouting and all-lowercase names. It
keeps deliberate brand casing.

It explicitly does **not**: look the company up on the web, correct a name that is simply wrong in
the CRM, translate anything, expand an acronym, or invent a word not already in the input. If the
string is not a company name at all (`N/A`, `Self-employed`, `Retired`, `TBD`) it abstains so the
row can be pulled out of the send.

## 2. Output contract

### Inputs required per row

| Field | Type | Required? |
|---|---|---|
| `company_name_raw` | string | yes |
| `domain` (bare, lowercase, no `www`) | string | no, but it lifts accuracy on ambiguous strings and costs nothing |

### Output fields

| Field | Type | Example | Max | Null? |
|---|---|---|---|---|
| `company_clean` | string | `Ajax Turner` | 40 target, 60 hard | no, `""` instead |
| `changed` | boolean | `true` | n/a | no |
| `confidence` | enum | `high` / `low` | n/a | no |

**Abstain value:** `""`. Never `N/A`, never the text `null`, never a guess.

### Coverage expectation

**98/100** rows usable on the graded test. A separate 10-row abstain probe of real junk values
scored **10/10 on the nano-class model but only 7/10 on `gpt-4o-mini`**, the model a Clay AI column
would use — which is why the deterministic placeholder guard in §6 is **mandatory, not a nicety**.

Treat `company_clean` as a **mandatory** variable that copy can rely on. Expect roughly 1 to 3
percent of a real list to be junk strings that correctly abstain.

### Copy-fit rules

- Slots into `Noticed {{company_clean}} is hiring.` and any sentence of that shape, including
  possessives (`{{company_clean}}'s pricing page`).
- Capitalization: whatever the brand actually uses. No trailing period, comma or quotes.
- No em dashes.
- **The value must be sendable with zero human edits.** That is the grading bar.

### Downstream gate

**Exclude and review. A generic substitute is never the fallback.**

If `company_clean` is empty, or the cleaner abstained on a junk string (`Self-employed`, `N/A`,
`Private Practice`, `Confidential Jobs`): **exclude the row from any campaign whose copy references
the company**, and route it to a review list. An empty value means you do not know where this
person works, which usually also means the row's title and domain are suspect.

**Do not substitute "your team", "your company", or anything generic, and do not spintax around it.**
The surrounding sentence was written to name a company, and a generic substitute just sends a worse
email to a worse address.

Operator override: keeping the row with the whole clause dropped via spintax is available when the
operator wants the volume and accepts the trade. Note the best practice once, proceed their way, log
the override.

## 3. Source chain (cost-tagged)

The "source" is the string you already have. There is no vendor to call, which is why this is the
cheapest playbook in the set. The chain is about how much intelligence to spend on the string.

**Step 0 is the default and where most clients stop.**

| # | Source | Cost | Hit rate | Stop rule |
|---|---|---|---|---|
| **0, THE DEFAULT** | Clay's built-in `Normalize Company Name` action, `titleCase: true` | **FREE** | **unbenchmarked here.** Observed behavior is suffix and casing normalization, which is the majority of what a real list needs | **STOP HERE** unless the §0 toggle test says otherwise |
| 1 | Deterministic suffix and separator strip (regex) | FREE | **89/100** | **Offline use only** — for scripts, for a sanity diff against the model, and for when the model API is unavailable. Inside Clay it is strictly worse than step 0, which is a maintained native action rather than a regex you own |
| 2, **THE TOGGLE** | The locked prompt in §6, plus the deterministic placeholder guard | CHEAP | **98/100** | the stopping point once the toggle is on |
| 3 | Canonical name by domain from a company database | FREE | untested | only for rows where step 2 abstained AND a domain exists. **EXACT domain match only.** If it misses, the chain ends and the row abstains |

⚠️ **Step 3 must use an exact domain match.** Fuzzy matching returns a different company, which is
how you email someone about a business they have never heard of. Then send whatever it returns
through step 2, since these databases store the registrar-style name too.

Once the toggle is on, steps 1 and 2 are **alternatives, not a waterfall**: at $0.15 per 1,000 rows
there is no reason to gate step 2 behind step 1. **Nothing in this chain spends an enrichment
credit.**

### Rejected alternatives

- **A nano-class model at minimal reasoning effort.** Measured **95/100 vs 98/100** on the same
  rows, and one failure was an invented casing change (`AdGreetz` returned as `adGreetz`), which
  violates the never-invent rule. The speed gain does not pay for that.
- **A per-row web lookup.** Metered to expensive for a formatting job a cheap model already does at
  98%. Only step 3 touches the web, and only on abstained rows.
- **Buying company enrichment to recover a name.** Roughly 200x the cost of the alternatives for a
  cosmetic field.

## 4. Verification

**VERDICT: PASS 98/100 (98%)** | `gpt-4o-mini`, locked prompt v3, `response_format=json_object`,
`max_completion_tokens=200` | p50 0.95s/row at concurrency 2 | ~$0.15/1k.

**Scope of that verdict, read before you quote the number.** It covers the script path only, on 100
rows. Three gaps, all open:

1. **The Clay AI column has never been run.** Same prompt, same model, different runtime.
2. **The benchmark is 100 rows, and the corpus is alphabetically skewed** toward names starting with
   a digit or the letter A, and is majority English. 100 rows is enough to lock a prompt. It is not
   enough to quote 98% as a general accuracy figure. **Quote it as "98/100 on a 100-row A-heavy
   English sample", never as "98 percent".**
3. **Abstain behavior differs by model and `gpt-4o-mini` is the weaker one:** 7/10 vs 10/10. Mini
   returned `Self-Employed CPA`, `Confidential Jobs` and `Private Practice` as if they were brands.
   With the placeholder guard mini scores 10/10 — but the guard list was written against those same
   10 rows, so treat it as a **mitigation to re-measure, not an independent result**.

Measured variants on the identical 100 rows:

| Path | Usable | p50 | Cost / 1k |
|---|---|---|---|
| `gpt-4o-mini`, prompt v3 | **98/100** | 0.95s | **$0.15** |
| nano-class, default reasoning, v3 | 98/100 | 4.13s | $0.30 ($0.15 flex) |
| nano-class, minimal reasoning | 95/100 | 0.96s | $0.03 |
| deterministic regex only | 89/100 | 0s | $0.00 |
| nano-class, prompt v1 | 93/100 | 4.63s | $0.32 |

Re-test if a QA read of 20 sampled variables finds more than 1 name an operator would edit, if
model pricing or ids change, or before locking the prompt for a client whose list is mostly
non-English names.

## 5. Clay implementation

- **`clay-table.md`** — the default (free) build plus the toggle columns.
- **`clay-workflow.md`** — the CLI-buildable version.

## 6. Locked prompt (the TOGGLE path only)

**Nothing here runs on the default build.**

Model: **`gpt-4o-mini` inside Clay** ($0.15/1k vs $0.30 for a nano-class model at identical 98/100
accuracy — nano loses because it spends ~640 reasoning tokens per row on what is a formatting job).
**A nano-class model outside Clay**, with a flex tier for batch, which brings it to about $0.15/1k
as well.

Params: `max_completion_tokens=200` for mini, **`2000` for nano** (its reasoning tokens count
against the same cap), never pass `temperature`, `response_format={"type":"json_object"}`.

⚠️ **Cache structure is load-bearing and counterintuitive.** Everything below is the static prefix
and goes FIRST as the system message, byte-identical every call. Measured: at 1,716 prompt tokens,
1,306 came back cached on nano and 1,597 on mini. An earlier draft at ~950 tokens got **zero** cache
hits, because caching only engages at 1,024+ tokens. **Keeping the example block long is not
padding — it is what turns the cache on.**

```text
You clean company names so they sound like a person saying the name out loud in an email.

You will be given one raw company name string from a CRM, plus the company's website domain when we have it. Return the short, human, spoken form of that company's name.

Return JSON only, exactly these keys:
{"company_clean": "...", "changed": true, "confidence": "high"}

Rules:
1. Drop legal suffixes and the punctuation attached to them: Inc, Inc., LLC, L.L.C., Ltd, Limited, Corp, Corporation, Co, Co., Company (only when it reads as a legal suffix), PLC, LLP, PC, PA, GmbH, AG, BV, NV, SA, SAS, SARL, SRL, SpA, Pty, Pty Ltd, AB, A/S, Oy, KK, Sdn Bhd, Private Limited.
2. Drop trademark and copyright marks: (R), (TM), (C), and their symbol forms.
3. Drop taglines, service lists, and descriptors that follow a separator such as a pipe, a dash with spaces around it, a colon, or a comma, when what follows describes the business instead of naming it.
4. Drop parenthetical descriptors such as (Startup), (formerly X), (a Division of X), (Private).
5. Drop a parenthetical acronym or short form of the same name.
6. Keep parentheses, brackets, and the characters inside them when they are part of the name itself rather than a comment on it. A number in parentheses at the front of a name is part of the name and stays, brackets included.
7. When the string has a legal entity plus a trading name (dba, d/b/a, doing business as), keep the trading name only.
8. Drop a trailing city, region, or country qualifier that was appended to the brand.
9. When the string repeats the name in a second language or script, keep the English form only.
10. Casing, and read this rule twice. Protect initialisms: a token of 2 to 6 letters that is not an ordinary English word stays exactly as written, so ARI stays ARI, ATC stays ATC, AMTC stays AMTC. That protection covers the initialism only. Ordinary words shouted in capitals get Title Case even when they sit next to a protected initialism, so TECH becomes Tech, GROUP becomes Group, SERVICES becomes Services, SOLUTIONS becomes Solutions, GLOBAL becomes Global, USA stays USA. An all-lowercase name made of ordinary words becomes Title Case.
11. Keep deliberate brand casing exactly as written: adGreetz, iRobot, eBay, 4medica, AmhFOLIO.
12. Keep an ampersand if the brand uses one. Keep numbers and dots that are part of the brand. Drop a .com only when the brand is clearly not named after its web address.
13. Never invent, translate, expand, or abbreviate a name. Every word you output must already appear in the input. If you would have to add a word, do not add it.
14. Never add a trailing period, comma, or quotation marks.
15. Keep it under 40 characters when the input allows that without cutting the brand.
16. No em dashes anywhere in the output.
17. If the input is empty, is a placeholder such as N/A, None, Unknown, or Test, or is not a company name at all, return "" for company_clean.
18. "changed" is true when company_clean differs from the input, and false when it is identical.
19. "confidence" is "low" when you had to guess which part of the string was the brand, and "high" otherwise.

The output must read correctly inside this sentence, with no edits: "Noticed COMPANY_CLEAN is hiring."

Work fast. This is a formatting job, not a research job. Do not look anything up and do not reason at length.

Examples:
Input: name="AAA Rent A Van, dba State Van Rental" domain="statevanrental.com"
Output: {"company_clean": "State Van Rental", "changed": true, "confidence": "high"}
Input: name="A Advanced Services | Septic and Construction" domain="aadvancedservices.com"
Output: {"company_clean": "A Advanced Services", "changed": true, "confidence": "high"}
Input: name="ADP" domain="adp.com"
Output: {"company_clean": "ADP", "changed": false, "confidence": "high"}
Input: name="Aquaserv, Inc." domain="aquaserv.com"
Output: {"company_clean": "Aquaserv", "changed": true, "confidence": "high"}
Input: name="ARI" domain=""
Output: {"company_clean": "ARI", "changed": false, "confidence": "high"}
Input: name="Absolute Robot (ARI)" domain="absoluterobot.com"
Output: {"company_clean": "Absolute Robot", "changed": true, "confidence": "high"}
Input: name="4IRE - Blockchain development & Consulting Company" domain="4irelabs.com"
Output: {"company_clean": "4IRE", "changed": true, "confidence": "high"}
Input: name="Ace Hardware Home Services - Southwest Ohio" domain="acehardware.com"
Output: {"company_clean": "Ace Hardware Home Services", "changed": true, "confidence": "high"}
Input: name="ACCRO | text in another language" domain="accro.fr"
Output: {"company_clean": "ACCRO", "changed": true, "confidence": "high"}
Input: name="American Pop Corn Company (JOLLY TIME Pop Corn)" domain="jollytime.com"
Output: {"company_clean": "American Pop Corn", "changed": true, "confidence": "low"}
Input: name="99pro media gmbh" domain="99pro-media.de"
Output: {"company_clean": "99pro media", "changed": true, "confidence": "high"}
Input: name="Aero Rubber Company(R)" domain="aerorubber.com"
Output: {"company_clean": "Aero Rubber", "changed": true, "confidence": "high"}
Input: name="Abc Mechanical Llc" domain="abcmechanical.com"
Output: {"company_clean": "Abc Mechanical", "changed": true, "confidence": "high"}
Input: name="ABC MECHANICAL SERVICES" domain="abcmechanical.com"
Output: {"company_clean": "ABC Mechanical Services", "changed": true, "confidence": "high"}
Input: name="AMTC TECH GROUP LLC" domain="amtctech.com"
Output: {"company_clean": "AMTC Tech Group", "changed": true, "confidence": "high"}
Input: name="(319) Auto Body" domain="319autobody.com"
Output: {"company_clean": "(319) Auto Body", "changed": false, "confidence": "high"}
Input: name="alamo environmental" domain="alamoenv.com"
Output: {"company_clean": "Alamo Environmental", "changed": true, "confidence": "high"}
Input: name="Alex Umo-Etuk - State Farm Insurance Agent" domain=""
Output: {"company_clean": "State Farm", "changed": true, "confidence": "low"}
Input: name="Apogee Compliance LLC" domain="apogeecompliance.com"
Output: {"company_clean": "Apogee Compliance", "changed": true, "confidence": "high"}
Input: name="3MD Relocation Services (Commercial Moving, Storage, Installation)" domain="3mdinc.com"
Output: {"company_clean": "3MD Relocation Services", "changed": true, "confidence": "high"}
Input: name="N/A" domain=""
Output: {"company_clean": "", "changed": true, "confidence": "high"}
Input: name="America's CAR-MART, Inc." domain="car-mart.com"
Output: {"company_clean": "America's CAR-MART", "changed": true, "confidence": "high"}

Company to clean:
```

Per-row user message, appended last:

```text
name="<raw company string>" domain="<bare lowercase domain, no www>"
```

Measured: 1,716 prompt tokens per call (1,300 to 1,600 cached after the first), 20 completion tokens
on mini, 671 on nano (of which ~640 are reasoning).

### Verifier pass: not needed, and here is why

Every other playbook makes a factual claim about the world, so it needs a second call to check that
claim. **This one makes no claim: the answer is a substring of the input.** That gives you something
better than an LLM verifier — a **deterministic guard that costs nothing**:

```
normalize(output) must be a substring of normalize(input)
  where normalize = lowercase, strip everything that is not a letter or digit
```

Any row failing that check has had a word invented and must be quarantined, not sent. In the 100-row
test the only row that tripped a naive *word-level* version of this was `3Mcompany -> 3M`, which is a
correct answer — the character-level version above passes it.

### Placeholder guard, required on both models and both runtimes

Rule 17 tells the model to abstain on junk. The nano-class model obeys (10/10). **`gpt-4o-mini` does
not: 7/10**, returning `Self-Employed CPA`, `Confidential Jobs` and `Private Practice` as brands.
Mini is the Clay model, so **the abstain cannot be the model's decision alone.**

Run a deterministic blocklist on the raw input **and** on the model's output, matching the **whole
normalized string** plus a `selfemployed` prefix.

⚠️ **Never match on substrings.** `Unknown Arts` and `Retired - BTH Bank` are real companies, and a
substring rule silently deletes them.

**Truncation guard:** `finish_reason=length` means the reasoning overran the cap. It is a **retry**
with a larger cap, never an abstain. Not theoretical: the first draft returned an empty value on 3
of 100 rows for exactly this reason, and **every one of those looked like a legitimate abstain until
the finish reason was checked.**

## 7. Edge cases and failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Empty result for an obviously real company | `finish_reason=length`, reasoning overran the cap, content empty | Retry with 3x the cap. **Never record it as an abstain.** Measured on 3 of 100 rows |
| Names come back SHOUTING (`ABN TECH`) | An acronym-protection rule too broad, protecting ordinary words in capitals | Rule 10 fixes exactly this. If you edit rule 10, re-run the harness |
| Zero cache hits, cost 3x expected | Static prefix under 1,024 tokens | **Keep the full example block.** 950-token prefix cached 0; 1,716-token prefix cached ~1,300 |
| A brand's real casing gets flattened (`AdGreetz` → `adGreetz`) | minimal reasoning effort on a nano-class model | Do not use minimal effort for this job. 95/100 vs 98/100 |
| Parentheses that ARE the brand get stripped (`(402) Creamery`) | Rule 6 overreaching from descriptors onto brands | Rule 6 plus the `(319) Auto Body` example. Both readings are sendable, so this is polish, not a send-blocker |
| A misspelling in the source survives cleaning | Rule 13 forbids inventing words, and fixing a typo means inventing one | Accepted trade-off. Catch it with a spell-check pass on the review list |
| The cleaned name is a company the person no longer works at | The row is stale. Cleaning cannot detect it | Out of scope — a list-freshness problem |
| The name and the domain describe different companies | A known defect in shared contact data, roughly **7.8%** of rows | Do not "fix" it here. Flag it and resolve upstream. Any database lookup must use **exact** domain match |
| Two legitimate brands in one string (parent plus operating brand) | Genuinely ambiguous | The model picks one and reports `high` when it should report `low`. Sendable either way; review rows where the chosen name does not match the domain |
| A 4 to 6 letter all-caps token that is really a word | Acronym vs word is undecidable from the string alone | Residual error class, ~1%. Accept it or check the website |
| **Every** row empty and the AI column shows as never run | The run condition binds a column that does not exist. **A gate that cannot evaluate true is indistinguishable from "no rows qualified"** — and the §2 downstream gate then drops the whole list from the campaign | Bind to real ids. Smoke-test on 10 rows you know have valid emails before running the table |
| `finish_reason=length` on **every** row outside Clay | Switched to a nano-class model but kept `max_completion_tokens=200`, the mini value. Nano spends ~640 reasoning tokens against the same cap | 2000 for nano, 200 for mini |
| Junk like `Private Practice` ships as a company name | Mini ignores the abstain rule more often than nano. 7/10 vs 10/10 | The placeholder guard, on input **and** output. Required, not optional |
| A regex-only run reports zero review flags on a list you have not checked | The regex path cannot judge itself; it reports `confidence: unknown` for every row and is only 89/100 | Sample 20 rows by hand before any send |
| The regex path turns `Retired - BTH Bank` into `Retired` | Stripping everything after a spaced dash leaves the placeholder word and drops the real bank | The placeholder guard checks the **output** as well as the input, so this abstains instead of sending |
| Clay column returns prose instead of JSON | `response_format` not set | Set it. The downstream formula expects an object |
| Different answer for the same input on a rerun | No `temperature` passed, and the default is not 0 | Cache the output. Do not re-run a locked campaign's names |

### Hard rules

- **Inside Clay this runs on `gpt-4o-mini`, and only alongside the placeholder guard.** The guard is
  what makes the cheaper model safe here.
- **The verdict covers the script path only, not the Clay AI column.** Never report the Clay path as
  tested.
