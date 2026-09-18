# ICP Matrix Builder

## When to Use
- Launching outbound for a new company or product line
- Refining targeting after initial campaign data comes in
- Expanding into new verticals or market segments
- Building the foundation for any lead generation or ABM campaign

## Framework

### What an ICP Matrix Is (And Isn't)

An ICP Matrix is a structured scoring document that ranks and segments your ideal buyers across multiple dimensions. It's the bridge between "we sell to B2B companies" and "we target Series B SaaS companies with 100-500 employees who just hired their first VP of Sales."

**It IS:**
- A living document that evolves with campaign data
- A scoring framework that makes targeting decisions objective
- A segmentation tool that enables personalized outreach at scale

**It is NOT:**
- A one-time exercise you do during onboarding and forget
- A single persona description
- A firmographic filter (company size + industry alone is not an ICP)

---

### The 5 Dimensions of an ICP Matrix

Every complete ICP Matrix scores prospects across five dimensions:

#### Dimension 1: Firmographic Fit
*Does the company match your ideal customer profile structurally?*

| Attribute | Tier 1 (Best) | Tier 2 (Good) | Tier 3 (Acceptable) | Disqualified |
|-----------|---------------|---------------|---------------------|--------------|
| **Company size** | Define range | Define range | Define range | Too small/large |
| **Revenue** | Define range | Define range | Define range | Outside range |
| **Industry** | Primary verticals | Adjacent verticals | Emerging fit | No fit |
| **Geography** | Primary markets | Secondary markets | Expansion markets | Restricted |
| **Business model** | Exact match | Similar | Adaptable | Incompatible |
| **Growth stage** | Ideal stage | Adjacent stages | Possible fit | Wrong stage |

**How to fill this in:**
1. Start with your best 10 customers — what do they have in common?
2. Look at your worst 10 customers — what disqualified them (in hindsight)?
3. The patterns that appear in your best but NOT your worst = your Tier 1 criteria

#### Dimension 2: Technographic Fit
*Does their tech stack indicate they're a good fit?*

| Attribute | Signal Strength | Why It Matters |
|-----------|----------------|----------------|
| **Uses your integration partners** | Strong | Lower friction to adopt |
| **Uses a competitor** | Strong | Active buyer, proven budget |
| **Tech stack complexity matches** | Medium | Right sophistication level |
| **Recently adopted adjacent tools** | Medium | Active buying cycle |
| **No relevant tech stack** | Weak | May not understand the category |

#### Dimension 3: Buying Intent Signals
*Is this company likely to be in-market right now?*

| Signal | Intent Level | Scoring Weight |
|--------|-------------|----------------|
| **Hiring for the role your product serves** | Very High | 5x |
| **Recent funding round** | High | 4x |
| **Competitor evaluation (G2, review sites)** | Very High | 5x |
| **Content consumption (webinars, guides)** | Medium-High | 3x |
| **Website visits (if tracking available)** | High | 4x |
| **Leadership change in relevant dept** | Medium | 2x |
| **No detectable intent** | Low | 1x |

#### Dimension 4: Persona Mapping
*Who within the company should you target?*

For each ICP tier, define 2-3 target personas:

| Persona Attribute | What to Define |
|-------------------|---------------|
| **Title patterns** | VP Sales, Director of Revenue, Head of Growth (include variants) |
| **Department** | Sales, Marketing, RevOps, Growth |
| **Seniority level** | C-Suite, VP, Director, Manager |
| **Decision role** | Economic buyer, Champion, Influencer, Blocker |
| **Pain points** | 3-5 specific, measurable pains this persona faces |
| **Buying triggers** | What events push them to evaluate solutions |
| **Success metrics** | What KPIs they're measured on |
| **Common objections** | Top 3-5 reasons they say no |

#### Dimension 5: Engagement Readiness
*How likely is this company to respond to outbound?*

| Factor | High Readiness | Low Readiness |
|--------|---------------|---------------|
| **Previous interactions** | Engaged before (event, content, trial) | Cold — no prior touchpoint |
| **Outbound receptiveness** | SMB/mid-market, growth-stage | Enterprise, heavily gatekept |
| **Channel preference** | Active on LinkedIn, responsive to email | Dark social, unreachable online |
| **Sales cycle length** | < 60 days | 6+ months |
| **Committee size** | 1-3 decision makers | 5+ stakeholders |

---

### The Tiering Framework

After scoring all five dimensions, segment accounts into tiers:

| Tier | Criteria | Outreach Strategy | Volume |
|------|----------|-------------------|--------|
| **Tier 1: Bullseye** | 4-5 dimensions score "Strong" | Hyper-personalized, multi-channel, 8+ touches | 5-10% of list |
| **Tier 2: Strong Fit** | 3-4 dimensions score "Strong" | Signal-based personalization, email-first | 20-30% of list |
| **Tier 3: Good Fit** | 2-3 dimensions score "Strong" | Bucket personalization, email-only | 40-50% of list |
| **Tier 4: Stretch** | 1-2 dimensions score "Strong" | Test with small batch, generic angle | 10-20% of list |
| **Disqualified** | 0 dimensions score "Strong" OR has a DQ flag | Do not contact | Remove from list |

**Disqualification triggers** (immediate removal regardless of other scores):
- Company too small to have budget
- Industry you can't serve
- Already a customer
- Competitor or partner (unless intentional)
- Bad data (no valid email, wrong person)

---

### Building the Matrix: 6-Step Process

#### Step 1: Analyze Your Best Customers
Pull your top 10-20 customers by: revenue, retention, NPS, speed-to-close, or expansion rate.

For each, document:
- Firmographics (size, revenue, industry, geo)
- What triggered them to buy
- Who the champion was (title, seniority)
- How long the sales cycle took
- What their tech stack looked like at purchase

#### Step 2: Analyze Your Worst Customers
Pull 10-20 churned or low-value customers. Document the same attributes.

**The gap between best and worst = your ICP definition.**

#### Step 3: Identify Scoring Patterns
Look for attributes that appear in 70%+ of your best customers but less than 30% of your worst:

```
Best Customers Pattern Analysis:
- 80% were Series A-B stage → Weight: High
- 75% had 50-200 employees → Weight: High
- 70% were hiring SDRs when they bought → Weight: Very High
- 60% were in B2B SaaS → Weight: Medium-High
- 50% had a VP Sales title as buyer → Weight: Medium
```

#### Step 4: Build the Scoring Model
Assign point values to each attribute:

| Dimension | Attribute | Tier 1 Points | Tier 2 Points | Tier 3 Points |
|-----------|-----------|---------------|---------------|---------------|
| Firmographic | 50-200 employees | 10 | 5 | 2 |
| Firmographic | B2B SaaS | 8 | 4 | 2 |
| Technographic | Uses Salesforce | 6 | 3 | 1 |
| Intent | Hiring SDRs | 10 | 5 | 2 |
| Intent | Recent funding | 8 | 4 | 2 |
| Persona | VP Sales title | 6 | 3 | 1 |

**Total possible:** Sum of all Tier 1 points
**Tier thresholds:** Tier 1 = 80%+, Tier 2 = 60-79%, Tier 3 = 40-59%, Below 40% = DQ

#### Step 5: Validate with Campaign Data
After running your first campaigns, compare:
- Positive reply rate by ICP tier
- Meeting rate by ICP tier
- Close rate by ICP tier

If Tier 2 accounts are outperforming Tier 1, your scoring model needs adjustment. The data will tell you which attributes actually predict buying behavior vs. which ones you assumed would.

#### Step 6: Iterate Quarterly
Every quarter, re-run the analysis:
- Which attributes correlated with closed deals?
- Which new signals appeared in your best customers?
- Has your product evolved to serve a different segment better?

Update the matrix. Adjust scoring weights. Re-tier your target accounts.

---

### Multiple ICP Segments

Most companies have 2-4 distinct ICP segments. Each needs its own matrix:

```
ICP Segment Map:
├── Segment A: "Growth-Stage SaaS" (Primary)
│   ├── Company: 50-500 employees, Series A-C, B2B SaaS
│   ├── Buyer: VP Sales / Head of Growth
│   └── Trigger: Hiring SDRs or scaling outbound
│
├── Segment B: "Agency Scaling" (Secondary)
│   ├── Company: 10-50 employees, digital agency, $2M-$10M revenue
│   ├── Buyer: Founder / CEO
│   └── Trigger: Hit referral ceiling, need predictable pipeline
│
└── Segment C: "Enterprise RevOps" (Emerging)
    ├── Company: 500-5000 employees, tech or professional services
    ├── Buyer: Director of RevOps / VP Sales Operations
    └── Trigger: Tech consolidation or efficiency mandate
```

**Rule:** Each segment gets its own campaigns, its own copy, and its own personalization strategy. Never blend segments in a single campaign.

## Templates

### ICP Matrix Template
```
# ICP Matrix: {{Company/Product Name}}
# Version: {{version}} | Last Updated: {{date}}

## Segment: {{segment_name}}

### Firmographic Profile
| Attribute | Tier 1 | Tier 2 | Tier 3 | DQ |
|-----------|--------|--------|--------|----|
| Company size | ___ | ___ | ___ | ___ |
| Revenue | ___ | ___ | ___ | ___ |
| Industry | ___ | ___ | ___ | ___ |
| Geography | ___ | ___ | ___ | ___ |
| Business model | ___ | ___ | ___ | ___ |
| Growth stage | ___ | ___ | ___ | ___ |

### Target Personas (Ranked by Priority)
| Rank | Title Pattern | Seniority | Decision Role | Key Pain |
|------|--------------|-----------|---------------|----------|
| P1 | ___ | ___ | ___ | ___ |
| P2 | ___ | ___ | ___ | ___ |
| P3 | ___ | ___ | ___ | ___ |

### Intent Signals (Ranked by Weight)
| Signal | Weight (1-5) | Detection Source |
|--------|-------------|-----------------|
| ___ | ___ | ___ |
| ___ | ___ | ___ |
| ___ | ___ | ___ |

### Scoring Thresholds
| Tier | Min Score | Outreach Strategy |
|------|-----------|-------------------|
| Tier 1 | ___ | ___ |
| Tier 2 | ___ | ___ |
| Tier 3 | ___ | ___ |
| DQ | Below ___ | Do not contact |

### Validation Metrics (Update Quarterly)
| Metric | Tier 1 | Tier 2 | Tier 3 |
|--------|--------|--------|--------|
| Positive reply rate | ___ | ___ | ___ |
| Meeting rate | ___ | ___ | ___ |
| Close rate | ___ | ___ | ___ |
| Avg deal size | ___ | ___ | ___ |
```

## Tips
- Your ICP is not who you CAN sell to — it's who you SHOULD sell to. The narrower your ICP, the higher your conversion rates.
- Start with 1 segment, not 4. Validate one ICP completely before expanding to adjacent segments.
- The #1 mistake in ICP development: using only firmographic data. A 100-person SaaS company that just raised Series B and is hiring 5 SDRs is a completely different prospect than a 100-person SaaS company that's been flat for 3 years. Same firmographics, wildly different intent.
- Interview your sales team. They know which deals close fast and which are painful — that pattern recognition is your ICP definition.
- If you don't have 10 customers to analyze yet, start with competitor customer analysis. Who are THEIR best customers? That's your starting ICP.
- Update your matrix every time you close (or lose) a significant deal. What did you learn? Did it match your scoring model?

---

*Progressive disclosure: load industry-specific ICP templates and scoring benchmarks only when building a matrix for a specific vertical.*
