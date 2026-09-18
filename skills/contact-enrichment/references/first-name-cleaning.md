# Playbook: First Name Cleaning

> All rules here are best practice, not law. Override any of them when the campaign calls for it; note the best practice once and move on.

**Use when:** any campaign whose email opens with the prospect's first name, which is every campaign
anyone runs. Run it next to the company-name clean, **before any other custom variable**, because
variables often interpolate the cleaned name.

**Do not use when:** you need the company name cleaned — that is
`playbook-company-name-cleaning`, its twin, built to the same shape on purpose. Also not for
finding a missing name. This playbook never looks anything up; a blank stays blank.

**One-line output:** `first_name_clean = "Ruba"` from the raw string `"Dr Ruba"`, so the email opens
`Hi Ruba,` instead of `Hi Dr Ruba,`.

## 1. Trigger and scope

The first name is the first word of the email and the single most visible tell that a message was
mail-merged. Lead databases store it the way a scraper found it, which is not the way anyone wants
to be greeted. Real strings from a live contacts table:

`Dr Matthew` · `PAUL` · `javonne` · `👋 James` · `★ Marc` · `Kathryn (Katie)` · `Robert wilkie`
(last name Wilkie) · `Araceli'S` · `Dr Sean Li We Are Actively Hiring At Antai Global` · `AAA` (at
company AAA Upholstery) · `Admin` · `O.` · `Gowinder ` with a trailing space · and rows where the
field is simply NULL.

Every one of those, pasted into `Hi {{first_name}},`, either looks broken or is not a person.

This playbook takes that string, plus the row's last name and company for context, and returns the
short spoken form. It strips honorifics, credential suffixes, emoji and decoration, appended job
titles and hiring notices, and possessive artifacts. It fixes shouting and all-lowercase. It picks
the nickname when someone wrote one in parentheses. It refuses to mangle hyphenated and apostrophe
names.

It explicitly does **not**: look the person up, translate or transliterate, expand an initial into
a guessed name, split a run-together name into two words, or invent a letter not already in the
input.

**Why the last name and company are inputs.** They are free, and they carry the only information
that settles the hardest case. `ATC` alone is undecidable. `ATC` with last name `Systems` at company
`ATC` is obviously not a person.

## 2. Output contract

### Inputs required per row

| Field | Type | Required? |
|---|---|---|
| `first_name_raw` | string | yes |
| `last_name_raw` | string | no, but free — it catches the duplicated-full-name and company-in-person-column cases |
| `company_name_raw` | string | no, but free — the only reliable discriminator for short ALL-CAPS tokens |

**Pass the RAW strings, not the cleaned company name.** The model needs to see the mess.

### Output fields

| Field | Type | Example | Max | Null? |
|---|---|---|---|---|
| `first_name_clean` | string | `Ruba` | 20 target, 40 hard | no, `""` instead |
| `changed` | boolean | `true` | n/a | no |
| `confidence` | enum | `high` / `low` | n/a | no |
| `needs_review` | boolean, **computed by the guards, not the model** | `true` | n/a | no |

**Abstain value:** `""`. Never `N/A`, never `null` as text, never `there`, never `friend`, never a
guess. This is not negotiable: **`N/A` renders into a live email as `Hi N/A,`.**

### Coverage expectation

Two numbers, because the benchmark is deliberately adversarial and the production rate is not the
same thing.

- **On the 100-row adversarial benchmark** (86 rows from messy-pattern filters, 14 at random): 76
  rows shipped a copy-ready value, 24 were correctly withheld for review, **0 silent failures.**
  Model-only accuracy 96/100, and **69/73 (94.5%) on rows the prompt had never seen.**
- **On a normal list, expect 97 to 99 percent to ship.** Measured by sampling 14,731 real rows:
  blank 0.05%, ALL-CAPS 0.03%, starts lowercase 0.03%, honorific prefix 0.05%, mailbox role word
  0.01%, parenthesis 0.00%, ≤2 characters 0.84%, any non-ASCII 1.08% (mostly ordinary accents,
  which are fine). **The genuinely broken share is 1 to 3 percent.**

### Copy-fit rules

- Slots into `Hi {{first_name_clean}},`, `Hey {{first_name_clean}} -`, and mid-sentence use.
- Title Case, except deliberate internal capitals (`DeAndrea`, `McCurry`) and non-Latin scripts,
  which stay exactly as written.
- No trailing period, comma, quote or space. No em dashes.
- **The value must be sendable with zero human edits.**

### Downstream gate

**Exclude and review. A generic greeting is never the fallback.**

| Condition | What happens |
|---|---|
| `first_name_clean` is empty | **EXCLUDE the row**, route to review |
| `needs_review` is true (any guard fired) | **EXCLUDE the row**, route to review |
| the name is written only in a non-Latin script (`珊`, `Дарья`, `عبدالله`, `준식`) | **EXCLUDE from an English-language campaign**, route to review |
| any of the above, and someone suggests a generic greeting | **No.** Never `there`, `friend`, `team`, `folks`, or the company name. Not by substitution, not by spintax |

**The non-Latin-script rule is an exclusion, not an abstain and not a transliteration.** The pipeline
keeps the name **exactly as written** and sets `needs_review`. Transliterating would invent letters;
blanking would destroy a real person's real name. About 6 of the 100 benchmark rows land here.
Routing them to a native-language campaign is a legitimate operator move, and **the preserved name
is what makes it possible.**

Why exclusion rather than a generic greeting: an empty or unusable first name usually means the row
is not a person at all, which makes the title and the email suspect too. A generic greeting does not
rescue that row, it just sends a worse email to a worse address.

## 3. Source chain (cost-tagged)

The "source" is the string you already have. No vendor to call.

| # | Source | Cost | Hit rate | Stop rule |
|---|---|---|---|---|
| 1 | Deterministic strip (regex) | FREE | **ungraded — do not quote a number for it** | always advance. **Step 1 cannot judge whether a string is a person**, which is the case that actually ships a broken email |
| 2 | The locked prompt in §6, **plus the six deterministic guards** | CHEAP | **96/100 model-only, 0 silent failures with guards** | the recommended stopping point |
| 3 | Recover the name from the email local part, then re-run step 2 | FREE | untested | **opt-in only.** `info@`, `sales@` and `jsmith@` all produce garbage, and a wrong first name is worse than no email |

Steps 1 and 2 are **alternatives, not a waterfall**. At $0.21 per 1,000 rows there is no reason to
gate step 2 behind step 1.

### Rejected alternatives

- **Native name-parsing actions as the primary.** Free and fine for splitting a full name into
  parts, but they do not handle emoji, appended hiring notices, possessive artifacts, or the
  person-versus-company question — which is where the real damage is. Use one upstream if you have
  it; still run step 2.
- **A name-gender or name-validation API.** Metered, and it answers a different question. You do
  not need to know whether `Ruba` is a real given name; you need the string that goes after `Hi`.
- **A bigger model.** The residual failures are strings with **no answer in them** (`TVK`, `KSM`),
  which a bigger model cannot solve either. They need a flag and a human.
- **Transliterating non-Latin names.** It invents letters and gets names wrong in ways a native
  speaker finds insulting.

## 4. Verification

**VERDICT: PASS 96/100** | `gpt-4o-mini`, locked prompt v2, JSON response format,
`max_completion_tokens=200` | p50 0.95s/row | ~$0.21/1k.

**Four open gaps, read before you quote the number:**

1. **The prompt's few-shot block overlaps the benchmark.** 27 of the 100 rows appear verbatim as
   examples, because the examples were written after looking at the corpus. **On the 73 held-out
   rows the score is 69/73 (94.5%), and all 4 failures are in the held-out set. 94.5% is the honest
   figure.**
2. **The Clay AI column has never been run.** Same prompt, same model, different runtime.
3. **The guards were run in Python, not in Clay.** The JavaScript twin in `clay-table.md` **has not
   been executed.**
4. **100 rows, adversarially stratified, majority English.** Re-run on a client's own corpus before
   locking this for a list that is mostly CJK or Arabic names.

Measured variants on the identical 100 rows:

| Path | Usable | Silent failures | p50 | Cost / 1k warm |
|---|---|---|---|---|
| `gpt-4o-mini`, prompt v2 | **96/100** (69/73 held out) | 0 | **0.95s** | **$0.21** |
| nano-class, default reasoning, v2 | 97/100 | 0 | 4.80s | $0.28 (~$0.14 flex) |
| `gpt-4o-mini`, prompt v1 | 96/100 | **3** | 1.05s | $0.21 |
| `gpt-4o-mini` + guards G1-G6 | 76 ship / 24 withheld | **0** | 0.95s | $0.21 |
| Abstain probe, both models | 10/10 | 0 | n/a | n/a |

Note row 3: **v1 and v2 score identically on accuracy and differ only in silent failures.** The
whole value of v2 is that its errors announce themselves.

## 5. Clay implementation

- **`clay-table.md`** — the column build with the guards as a formula.
- **`clay-workflow.md`** — the CLI-buildable version.

## 6. Locked prompt

Model: **`gpt-4o-mini` inside Clay** ($0.21/1k vs $0.28 for a nano-class model at 96/100 vs 97/100).
Note the margin is thinner than it looks: **on a cold cache the two are within 1.2%**, so a column
running tiny batches that never warm the cache should redo the arithmetic. A nano-class model
outside Clay, flex tier for batch (~$0.14/1k).

Params: `max_completion_tokens=200` for mini, **`2000` for nano**, never `temperature`,
`response_format={"type":"json_object"}`.

Cache structure: everything below is the static prefix, first, byte-identical. Measured **2,436
prompt tokens, of which 2,212 came back cached** on mini after the first call.

### Do not shorten this prompt. It was audited, and the short version lost.

This prompt looks too long. It was measured rather than argued about. A 13-line candidate (7 rules,
no few-shot pairs) ran head to head against the prompt below on 30 fresh real rows, same model, same
params:

| | prompt v2 (below) | short candidate |
|---|---|---|
| Prompt tokens | 2,434 | 435 |
| Cached tokens once warm | 1,920 | **0** (under the 1,024 cache floor) |
| Cost per 1,000 rows, warm | **$0.047** | $0.0325 |
| Ship-ready rows | **29/30** | 27/30 |
| **Broken sends** | **0** | **3 (10%)** |

The whole saving is **$0.0145 per 1,000 rows, or $1.45 per 100,000.** The three broken sends it
buys are `Hi ktitor,` (a lowercase handle that is actually the company name), `Hi Kathryn Katy,`
and `Hi Ye Cynthia Xi Cpa,`.

Two things make this conclusive rather than a close call:

1. **Shortening the prompt turns the cache OFF.** Cutting 82% of the tokens cut only 31% of the
   cost, because the long prompt gets 79% of its input at the 10x-discounted cached rate and the
   short one gets none of it. **"The prompt looks expensive because it is long" is exactly backwards
   here.**
2. **The guards do NOT rescue a weaker prompt.** All five divergent rows were re-run through
   G1-G6 and **every guard returned false on every one.** `ktitor` is not in the blocklist;
   `Kathryn Katy` and `Ye Cynthia Xi Cpa` both pass G6 because every letter really is in the raw
   field. **G6 catches invention, not failure to strip.** The failures a short prompt produces are
   *plausible* strings, and plausible strings are the one thing a deterministic guard cannot see.

The two prompts agreed exactly on all 12 ordinary rows, all 4 honorifics, both lowercase rows, all 4
non-Latin rows and both multi-word rows. **A short prompt is fine on everything that is easy, which
is why this looks safe until you measure it.**

```text
You clean the first-name field on a sales lead so it can be dropped straight into the greeting line of a cold email.

You will be given the raw first-name string from a CRM, plus that row's last-name string and company name for context. Return the single name this person would be greeted by in a friendly business email.

Return JSON only, exactly these keys:
{"first_name_clean": "...", "changed": true, "confidence": "high"}

Rules:
1. Drop honorifics and titles at the front: Dr, Dr., Mr, Mrs, Ms, Miss, Prof, Professor, Rev, Fr, Capt, Sir, Dame, Lord, Sr, Sra, Hr, Ing, Eng, Adv.
2. Drop credential and qualification suffixes wherever they appear: MD, DO, DDS, DMD, RN, NP, PA-C, PhD, Ph.D, EdD, JD, Esq, Esquire, CPA, CFA, CFP, MBA, MSc, MA, BSc, PE, PMP, CISSP, CSM, MCIPS, FCA, ACCA, and the punctuation attached to them.
3. Drop emoji, stars, arrows, bullets, check marks, crowns, and any other decoration: the leading and trailing ornaments people add to a LinkedIn name. Keep only the letters of the name.
4. Fix shouting and whispering, and do it LAST, after you have picked the name out of the field. An ALL-CAPS ordinary name becomes Title Case, so PAUL becomes Paul and SUSHMA becomes Sushma. An all-lowercase ordinary name becomes Title Case, so javonne becomes Javonne and alan becomes Alan. The name you return is always Title Case unless rule 5 or rule 12 says otherwise.
5a. A trailing 'S or 's on the first-name field is a possessive artifact from a business listing, not part of the name. Drop it. Rosa'S becomes Rosa. This applies only at the very end of the field, never to an apostrophe inside the name.
5b. Keep deliberate internal capitals and punctuation that belong to the name: DeAndrea, McCurry, O'Brien, D'Anza, T'Kia, Jean-Paul, Yi-Hsuan, Anne-Maud. Never remove a hyphen and never remove an apostrophe from inside a name, and never split a hyphenated name into one half.
6. When a nickname or short form follows the name in parentheses or quotes, return the nickname, because that is what the person goes by. Kathryn (Katie) becomes Katie. Lazaro (Laz) becomes Laz.
7. When the parenthetical is not a short form of the outer name, keep the outer name and drop the parenthetical. Disa(Xiaobing) becomes Disa.
8. When two names are separated by a slash, return the second one if it is the everyday English short form, otherwise the first. Mihir/Mike becomes Mike.
9. When the first-name field holds the whole name and its last word repeats the last-name field, drop that repeated word. Robert wilkie with last name Wilkie becomes Robert.
10. Keep a genuine two-part given name intact: Jose Ramon, Guðmundur Ragnar, Yong Shuan, Marie-Laure. Do not shorten a name that is simply long.
11. Drop appended job titles, taglines, hiring notices, and company text that someone typed into the name field. Keep only the given name.
12. Keep names written in a non-Latin script exactly as they are. Never transliterate, never translate, never romanize. If the field mixes a native-script name with a Latin-script name, return the Latin-script one.
13. Never invent, expand, translate, or guess a name. Every letter you output must already appear in the first-name field. If you would have to add a letter, do not add it.
14. Never add a trailing period, comma, or quotation marks. Never return a leading or trailing space.
15. No em dashes anywhere in the output.
15b. When one ALL-CAPS token looks like two names run together, do NOT split it, because splitting invents a word boundary. Title Case it as one word and set confidence to "low" so a human checks the row.
16. Return "" for first_name_clean when the field is empty, when it is a placeholder or a mailbox role such as Admin, Info, Sales, Support, Team, Owner, Manager, HR, Office, Contact, N/A, None, Unknown, Test, TBD, when it holds a company name instead of a person, when the first-name field and the last-name field read together as the company name in the company field, or when it is a single letter or a single initial that cannot be greeted.
17. Multi-letter initials that a person actually goes by are fine and stay as written: J.D., K.C., J.C. A single initial such as O. or H. or C is not greetable, so return "".
18. "changed" is true when first_name_clean differs from the raw first-name field, and false when it is identical.
19. "confidence" is "low" when you had to judge whether the string was a person at all, or which part was the given name, and "high" otherwise.

The output must read correctly inside this greeting, with no edits: "Hi FIRST_NAME_CLEAN,"

Work fast. This is a formatting job, not a research job. Do not look anything up and do not reason at length. Do not output your reasoning, only the JSON.

Examples:
Input: first="Dr Ruba" last="Maatouk" company="Metropolitan Dental Care"
Output: {"first_name_clean": "Ruba", "changed": true, "confidence": "high"}
Input: first="Capt. Jehan" last="Alam" company="Fletcher International Exports Pty"
Output: {"first_name_clean": "Jehan", "changed": true, "confidence": "high"}
Input: first="Philip" last="Pickard, MBA" company="Dow"
Output: {"first_name_clean": "Philip", "changed": false, "confidence": "high"}
Input: first="Dr. Marie Y." last="Lemelle, MBA, PhD" company="Platinum Star Public Relations"
Output: {"first_name_clean": "Marie", "changed": true, "confidence": "high"}
Input: first="PAUL" last="Harlin" company=""
Output: {"first_name_clean": "Paul", "changed": true, "confidence": "high"}
Input: first="javonne" last="morgan" company="All Seasons"
Output: {"first_name_clean": "Javonne", "changed": true, "confidence": "high"}
Input: first="DeAndrea (Dee)" last="Davis" company="LyondellBasell"
Output: {"first_name_clean": "Dee", "changed": true, "confidence": "high"}
Input: first="Kathryn (Katie)" last="Connors" company="BrightFarms"
Output: {"first_name_clean": "Katie", "changed": true, "confidence": "high"}
Input: first="Disa(Xiaobing)" last="WU" company="Cordis"
Output: {"first_name_clean": "Disa", "changed": true, "confidence": "high"}
Input: first="Jean-Paul" last="Beleshay" company="Strata Clean Energy"
Output: {"first_name_clean": "Jean-Paul", "changed": false, "confidence": "high"}
Input: first="Anne-Maud" last="Boyard" company="CLARTEIS"
Output: {"first_name_clean": "Anne-Maud", "changed": false, "confidence": "high"}
Input: first="D'Anza" last="Alexander" company="NCTC"
Output: {"first_name_clean": "D'Anza", "changed": false, "confidence": "high"}
Input: first="Rosa'S" last="Delgado" company="Riverside Health"
Output: {"first_name_clean": "Rosa", "changed": true, "confidence": "low"}
Input: first="MARYELLEN" last="Boyd" company=""
Output: {"first_name_clean": "Maryellen", "changed": true, "confidence": "low"}
Input: first="Blue Ridge" last="Roofing" company="Blue Ridge Roofing"
Output: {"first_name_clean": "", "changed": true, "confidence": "high"}
Input: first="👋 James" last="Sansbury" company="Tugboat"
Output: {"first_name_clean": "James", "changed": true, "confidence": "high"}
Input: first="★ Marc" last="Deinum ★" company="MetroStation.nl"
Output: {"first_name_clean": "Marc", "changed": true, "confidence": "high"}
Input: first="Robert wilkie" last="Wilkie" company="RJ's Burgers & Ice Cream Co."
Output: {"first_name_clean": "Robert", "changed": true, "confidence": "high"}
Input: first="Jose Ramon" last="Carrasco" company="RC Innovations"
Output: {"first_name_clean": "Jose Ramon", "changed": false, "confidence": "high"}
Input: first="Guðmundur Ragnar" last="Guðmundsson" company="Prentmet Oddi"
Output: {"first_name_clean": "Guðmundur Ragnar", "changed": false, "confidence": "high"}
Input: first="J.D." last="Dougherty" company="Jeff's Bagel Run"
Output: {"first_name_clean": "J.D.", "changed": false, "confidence": "high"}
Input: first="O." last="Murdock" company="Murdock Chevrolet"
Output: {"first_name_clean": "", "changed": true, "confidence": "high"}
Input: first="珊" last="苏" company="Axine Water Technologies"
Output: {"first_name_clean": "珊", "changed": false, "confidence": "high"}
Input: first="王小明ken" last="Wang" company="Sunrise Optics"
Output: {"first_name_clean": "Ken", "changed": true, "confidence": "low"}
Input: first="Mihir/Mike" last="Parikh" company="FreshLime"
Output: {"first_name_clean": "Mike", "changed": true, "confidence": "high"}
Input: first="Dr Sean Li We Are Actively Hiring At Antai Global" last="Inc" company="Antai Global"
Output: {"first_name_clean": "Sean", "changed": true, "confidence": "low"}
Input: first="AAA" last="Upholstery" company="AAA Upholstery"
Output: {"first_name_clean": "", "changed": true, "confidence": "high"}
Input: first="Admin" last="E-Gree" company="e-gree"
Output: {"first_name_clean": "", "changed": true, "confidence": "high"}
Input: first="" last="Awhaitey" company="Healthy Kingdom"
Output: {"first_name_clean": "", "changed": false, "confidence": "high"}
Input: first="Gowinder " last="Singh" company="Mainfreight"
Output: {"first_name_clean": "Gowinder", "changed": true, "confidence": "high"}

Name to clean:
```

Per-row user message, appended last:

```text
first="<raw first name>" last="<raw last name>" company="<raw company name>"
```

Measured: 2,436 prompt tokens per call (2,097 to 2,212 cached after the first), 20 completion tokens
on mini, 627 on nano (~600 reasoning).

### Verifier pass: not needed, and here is why

This playbook makes no claim about the world — **the answer is a substring of the input.** That
gives you a deterministic guard that costs nothing:

```
normalize(output) must be a substring of normalize(raw first name)
  where normalize = strip accents, casefold, drop everything that is not a letter or digit
```

**Accent stripping matters here in a way it did not for company names**, because the model is
allowed to Title Case a shouted name and you must not flag that as an invention. Zero rows tripped
it in the 100-row test.

### The six deterministic guards, required on both models and both runtimes

The model alone is 96/100 and **every one of its four errors is the same class**: a short or shouted
token that could be initials or could be a business. There is no information in the string that
settles it, so **the fix is a flag and a human, not a better prompt.**

| Guard | Catches | Action | Note |
|---|---|---|---|
| **G1** placeholder | mailbox roles and junk (`Admin`, `Info`, `Team`, `N/A`, blank) | ABSTAIN | whole normalized string only, **never a substring** — `Adminson` and `Teamer` are real surnames |
| **G2** company overlap | first + last read as the company name | **FLAG ONLY** | never an auto-abstain: a real row is `Jana Meerman` at company `Jana Meerman` |
| **G3** caps acronym | 2 to 4 char ALL-CAPS with **no vowel** (`TVK`, `KSM`) | FLAG | the vowel test is what keeps `PAUL` and `PHAM` out of the flag |
| **G4** run-together shout | one ALL-CAPS token of 9+ chars (`KIRKDELANEY`) | FLAG | splitting it would invent a word boundary |
| **G5** non-Latin script | the cleaned value is not writable in Latin script | FLAG, **never an abstain** | keep the name exactly as written and let the §2 gate exclude it from an English campaign. Do not transliterate (invents letters), do not blank (destroys a real name) |
| **G6** invented letters | `normalize(output)` is not a substring of `normalize(input)` | QUARANTINE | a trip here means the model made something up |

⚠️ **A bug worth knowing about, found while building these guards.** The first version of G1 tested
emptiness as `not normalize(v)` — and because `normalize` drops everything outside `[0-9a-z]`,
`normalize("珊")` is the empty string. **That version silently abstained on every Chinese, Cyrillic,
Arabic and Korean name in the benchmark, 4 of 100 rows, and reported them as ordinary placeholder
abstains, so the model score never moved.** Any edit to `normalize()` must keep a Unicode-aware
`has_letters()` test alongside it.

**Truncation guard:** `finish_reason=length` means a **retry** with a larger cap, never an abstain.
Running a nano-class model at mini's 200-token cap returns empty content on essentially every row,
which is **the single most common way to "measure" a 0% hit rate on a working prompt.**

## 7. Edge cases and failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Greeting reads `Hi Dr Matthew,` | The campaign is using the sequencer's built-in `first_name` field instead of the cleaned variable | Map copy to `{{first_name_clean}}`. Keep the raw value in `first_name` so a human can always see the source string |
| Greeting reads `Hi alan,` or `Hi PAUL,` | Casing applied **while** extracting the name instead of after | Rule 4 fixes this. A lowercase or SHOUTING greeting is the most recognizable mail-merge tell in cold email |
| Greeting reads `Hi Araceli's,` | The source was a business listing with a possessive | Rule 5a, scoped to the **END** of the field only. Broaden it and you destroy `D'Anza`, `T'Kia`, `O'Brien`, `Qurratu'Aini` |
| A hyphenated name comes back as one half | An over-eager "take the first token" rule | Rule 5b forbids it; all 6 hyphenated benchmark rows passed. If you see this, the prompt has been edited |
| Greeting reads `Hi Kirkdelaney,` | A run-together ALL-CAPS name. The model **correctly** refuses to split it | G4 plus `confidence: low` routes it to review. A withheld row, not a send |
| Greeting reads `Hi Tvk,` or `Hi KSM,` | Short ALL-CAPS that is either initials or a company acronym. **Nothing in the string decides it** | G3. Residual class, ~2% of an adversarial sample, far less on a real list. A bigger model does not fix it |
| A company name ships as a person | The person column holds the business | G2, flag only |
| **Every** Chinese, Arabic, Cyrillic or Korean name silently abstains | A `normalize()` that strips to `[0-9a-z]` reduces those names to the empty string, and the emptiness test reads them as blank | The Unicode-aware `has_letters()` test. **4 of 100 rows, invisible in the model score** |
| A real person dropped because their company is named after them | G2 turned into an auto-abstain by a well-meaning edit | **G2 is FLAG ONLY** |
| `PAUL` and `PHAM` flagged alongside `TVK` | G3 written without the vowel test | Add the vowel test |
| `finish_reason=length` on **every** row | A nano-class model kept at mini's 200-token cap | 2000 for nano, 200 for mini |
| **Every** row empty and the AI column shows as never run | The run condition binds a column that does not exist. **A gate that cannot evaluate true is indistinguishable from "no rows qualified"** | Bind to real ids. Smoke-test on 10 rows you know have valid emails |
| Zero cache hits, cost nearly double | Static prefix under the 1,024-token floor | Keep the full example block |
| Someone shortens the prompt "because it looks too long", quality drops, cost barely moves | Cutting the example block drops the prefix under the cache floor: 82% fewer tokens buys only 31% less cost, and the model loses the examples carrying the hard cases | **Do not shorten it.** See the audit in §6 |
| A weaker prompt is proposed on the grounds that "the guards will catch it" | The guards catch **invention** and known junk, not failure to strip | Verified: all six guards returned false on all five rows where the short prompt diverged. **The guards are a second net, never a substitute for the prompt** |
| Clay column returns prose instead of JSON | `response_format` not set | Set it |
| Different answer on a rerun | No `temperature` passed, default is not 0 | Cache the output |
| The name is right but the person left the company | Stale row. Cleaning cannot detect it | Out of scope — a list-freshness problem |
| The first name and the company describe different people | A known defect in shared contact data, roughly **7.8%** of rows | Flag and resolve upstream |

### Hard rules

- **Abstain is always the empty string.** Never `N/A`, never `there` or `friend`. `N/A` renders into
  a live email.
- **The AI column runs only alongside the six guards.**
- **The verdict covers the script path only**, not the Clay AI column and not the Clay formula
  version of the guards.
