# Winning Copy Extraction

## When to Use
- After accumulating 30+ campaigns with performance data
- When onboarding a new copywriter or SDR who needs to learn "what works here"
- Building AI-assisted copy generation systems that learn from your data
- Creating a copy playbook for a specific vertical, persona, or campaign type
- Quarterly copy audits to identify trends and refresh stale templates

## Framework

### The Copy Extraction Pipeline

Winning copy doesn't come from brainstorming — it comes from data. Here's the systematic process for extracting what works from what you've already sent.

```
Step 1: Pull Campaign Data
    → All campaigns with 200+ sends and at least 14 days of data
    ↓
Step 2: Rank by Positive Reply Rate
    → Sort descending. Top 10% = your winners.
    ↓
Step 3: Analyze the Winners
    → What patterns emerge across your best copy?
    ↓
Step 4: Codify the Patterns
    → Turn patterns into reusable frameworks
    ↓
Step 5: Test Against New Copy
    → Use pattern-based copy in new campaigns. Measure.
    ↓
Step 6: Update the Playbook
    → Add new winners. Remove copy that stopped working.
```

---

### Step 1: Define "Winning" Copy

Before extracting patterns, define your threshold:

| Metric | Winning Threshold | Minimum Sample |
|--------|-------------------|---------------|
| **Positive reply rate** | Top 20% of all campaigns | 200+ sends |
| **Reply-to-meeting rate** | > 40% | 10+ replies |
| **Step 1 reply rate** | > 5% | 200+ sends on Step 1 |
| **Follow-up reply rate** | > 3% (Step 2-4) | 150+ sends per step |

**Why positive reply rate, not total reply rate?** Total reply rate includes "not interested" and "remove me." Positive reply rate measures genuine demand. A campaign with a 15% total reply rate and 1% positive reply rate is worse than a campaign with 8% total and 5% positive.

---

### Step 2: The Copy Anatomy Framework

For every winning email, break it down into its atomic components:

| Component | What to Capture | Example |
|-----------|----------------|---------|
| **Subject line** | Exact text, word count, format | `acme + outbound` (3 words, lowercase) |
| **Opening type** | How the first line works | Signal-based observation |
| **Opening line** | Exact first sentence | "Noticed you're hiring 3 SDRs in Austin" |
| **Pain articulation** | How the problem is framed | Problem/cost framing: "Most teams at your stage..." |
| **Value proposition** | How the solution is positioned | Outcome-focused: "Our clients see 3x pipeline in 90 days" |
| **Social proof type** | What credibility is used | Metric from similar company |
| **CTA type** | How the ask is structured | Low-friction question: "Worth exploring?" |
| **CTA text** | Exact CTA | "Would it help to see how {{similar_company}} handled this?" |
| **Tone** | Overall voice | Conversational, peer-to-peer |
| **Length** | Word count | 87 words |
| **Personalization level** | How tailored it feels | Level 4: Business event signal |
| **Archetype** | Which copy archetype it matches | The Observation (Archetype 1) |

---

### Step 3: Pattern Recognition

After analyzing 10-20 winning emails, look for patterns across these dimensions:

#### Subject Line Patterns

| Pattern | Example | Win Rate |
|---------|---------|----------|
| `{{company}} + topic` | "acme + outbound" | __% |
| `quick [role] question` | "quick vp sales question" | __% |
| `re: [trigger]` (real, not faked) | "re: your series b" | __% |
| `[topic] idea` | "pipeline idea" | __% |
| `[mutual element]` | "fellow YC founder" | __% |

Track which patterns your audience responds to. Different personas respond to different subject formulas.

#### Opening Line Patterns

| Pattern | Example | When It Works |
|---------|---------|--------------|
| **Signal observation** | "Saw you just raised..." | When you have a specific, timely signal |
| **Problem statement** | "Most VP Sales at Series B companies..." | When the pain is universal and well-known |
| **Compliment + pivot** | "Your post about X was great — we're seeing..." | When they've published relevant content |
| **Shared context** | "Fellow [industry/stage/community] member here" | When you have a genuine shared experience |
| **Direct value** | "We helped [similar company] achieve [result]" | When your proof point is strong enough to lead |

#### CTA Patterns

| Pattern | Example | When It Works |
|---------|---------|--------------|
| **Low-friction question** | "Worth a look?" | Default. Works almost everywhere. |
| **Resource offer** | "Want me to send the playbook?" | When you have a valuable resource |
| **Relevance check** | "Is this something you're thinking about?" | When you're unsure about timing |
| **Social proof question** | "Want to see how {{company}} handled this?" | When you have a strong case study |
| **Direct ask** | "Open to a quick conversation?" | When signals are very strong |

#### Length Patterns

Analyze the word count distribution of your winning emails:

```
Winning email length distribution:
< 60 words:    __% of winners  → Very concise, works for senior executives
60-90 words:   __% of winners  → Sweet spot for most audiences
90-120 words:  __% of winners  → Acceptable for complex value props
120-150 words: __% of winners  → Getting long, but can work with strong copy
> 150 words:   __% of winners  → Rarely wins. If it does, the content was exceptional.
```

---

### Step 4: Build the Copy Playbook

Turn patterns into a document your team can reference:

#### The Winning Copy Playbook Structure

```
COPY PLAYBOOK: {{Company/Product Name}}
Last Updated: {{date}}
Based on: {{number}} campaigns, {{number}} emails analyzed

--- SUBJECT LINES ---
Top 3 formulas:
1. {{formula}} — avg open rate: __%
2. {{formula}} — avg open rate: __%
3. {{formula}} — avg open rate: __%

Avoid: {{patterns that consistently underperform}}

--- OPENING LINES ---
Top 3 patterns:
1. {{pattern}} — used in __% of winning emails
2. {{pattern}} — used in __% of winning emails
3. {{pattern}} — used in __% of winning emails

--- BODY COPY ---
Winning archetypes (ranked):
1. {{archetype}} — avg positive reply rate: __%
2. {{archetype}} — avg positive reply rate: __%
3. {{archetype}} — avg positive reply rate: __%

--- CTAs ---
Top 3 CTAs:
1. "{{exact CTA}}" — conversion: __%
2. "{{exact CTA}}" — conversion: __%
3. "{{exact CTA}}" — conversion: __%

--- PROOF POINTS ---
Most effective:
1. {{proof point}} — used in campaign: {{name}}
2. {{proof point}} — used in campaign: {{name}}

--- TONE GUIDELINES ---
Voice: {{description}}
Do: {{list of tone elements that work}}
Don't: {{list of tone elements that fail}}

--- EMAIL LENGTH ---
Target: {{X-Y}} words
Never exceed: {{max}} words
```

---

### Step 5: Copy Decay Detection

Even winning copy stops working eventually. Monitor for these decay signals:

| Indicator | What It Means | Action |
|-----------|-------------|--------|
| Positive reply rate dropped 30%+ from peak | Copy fatigue or market shift | Test new variants |
| Same copy performing well for 3+ months | Unusual — validate the data | Enjoy it while it lasts |
| Step 1 replies declining but Step 2-3 stable | Subject line fatigue | Rotate subjects, keep body |
| All steps declining simultaneously | Larger issue — list quality, deliverability, or market | Full diagnosis needed |
| New competitor emerged in the space | Market dynamics changed | Update positioning and proof points |

**Copy refresh cadence:**
- Subject lines: rotate every 4-6 weeks
- Body copy: refresh every 8-12 weeks
- Full sequence: rebuild every quarter

---

### Step 6: Competitive Copy Analysis

Analyze the cold emails YOU receive to learn from competitors:

| What to Track | Why |
|--------------|-----|
| Subject line formula | See what competitors test |
| Opening approach | How are they personalizing? |
| Value proposition | What outcomes are they claiming? |
| CTA style | Direct vs. soft ask |
| Sequence length | How many touches before they stop? |
| Tone | Professional vs. casual |
| Unique angles | What are they saying that you aren't? |

**Build a swipe file:** Save every cold email you receive (good and bad). Annotate what worked, what didn't, and why. This becomes a creative resource for your team.

---

### Cross-Campaign Copy Intelligence

The most powerful analysis comes from comparing across campaigns:

#### By Persona
```
Which copy patterns work best for:
- VP Sales: {{patterns}}
- Founders: {{patterns}}
- RevOps: {{patterns}}
- Marketing: {{patterns}}
```

#### By Industry
```
Which angles resonate with:
- B2B SaaS: {{angles}}
- Agencies: {{angles}}
- E-commerce: {{angles}}
- Professional services: {{angles}}
```

#### By Company Stage
```
Which proof points convert at:
- Seed-Series A: {{proof_points}}
- Series B-C: {{proof_points}}
- Enterprise: {{proof_points}}
```

This cross-analysis is where the compounding happens. Every campaign you run makes every future campaign better — but only if you extract and codify the learnings.

## Templates

### Copy Analysis Worksheet
```
Campaign: {{name}}
Positive Reply Rate: __%
Sample Size: __ sends

Subject: {{exact subject}}
Subject Pattern: {{formula used}}

Opening Line: "{{exact text}}"
Opening Pattern: {{type}}

Body Archetype: {{archetype name}}
Key Pain Referenced: {{pain}}
Proof Point Used: {{proof}}
CTA: "{{exact CTA}}"
CTA Pattern: {{type}}

Word Count: __
Personalization Level: __/5

What made this work: ___
What could be improved: ___
Reusable for other campaigns? Y/N — Which: ___
```

## Tips
- Your top 5 campaigns contain 80% of the insights you need. Start there. Don't try to analyze 100 campaigns at once.
- The best copy extraction happens when you have at least 30 campaigns with 200+ sends each. Below that threshold, you're working with anecdotes, not patterns.
- Don't just copy your winning emails verbatim into new campaigns. Extract the PATTERN and apply it to the new context. "Saw you're hiring SDRs" isn't a template — "reference a specific hiring signal that indicates their investment in your category" is a template.
- Keep a running "quote bank" of exact phrases prospects use in positive replies. Their language for saying "yes" is your most valuable copy resource — use it in future emails.
- The fastest way to improve copy: write 10 variants of Step 1, send 200 of each, and let the data pick the winner. Your intuition about what works is often wrong. The data isn't.

---

*Progressive disclosure: load platform-specific data extraction guides and AI copy generation prompts only when actively analyzing campaign data from a specific sending tool.*
