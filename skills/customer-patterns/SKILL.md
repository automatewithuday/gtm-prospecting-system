---
name: customer-patterns
description: "Use when stage 1 of the prospecting system needs to turn a handful of best customers (or a closed-won/closed-lost export) into the patterns they share — firmographics, triggers, champions, deal shape. Also use standalone to analyze why deals are won and lost."
license: MIT
metadata:
  author: automatewithuday
  source: martechs.io
  ported_from: gtm-flywheel/sales-intelligence/deal-patterns/SKILL.md
---

# Deal Pattern Analysis

## Pipeline contract

**Stage 1 of 20.** Reads `00-customers.csv` (`domain` required; `company_name, deal_size, close_date, champion_title, source, notes` optional). Writes `01-customer-patterns.md` and `01-seeds.csv` (`domain`).

- With only ~5 customers and no loss data, run Analysis 1 and 5 only and say so in the output. Five rows is a hypothesis, not a pattern — label every finding with how many customers support it.
- Research each customer's website before filling the 12 variables; leave a variable blank rather than guessing.
- Done when `01-customer-patterns.md` ends with an "Ideal Deal Profile" the human has read.

Files live in `runs/<run>/`. Column definitions: [`/prospecting-system`](../prospecting-system/SKILL.md). Standalone use: ignore this block.


## When to Use
- Quarterly business reviews when analyzing sales performance
- Refining your ICP based on which deals actually close (vs. which you thought would close)
- Building predictive models for deal scoring and pipeline forecasting
- Training new sales hires on what "good" looks like at your company
- Diagnosing a pipeline problem: "We have meetings but can't close"

## Framework

### The Deal Pattern Hypothesis

Every company has hidden patterns in their deal data. The companies that find and exploit these patterns close 2-3x more efficiently than those that don't.

**The core question:** What do your best deals have in common that your worst deals don't?

If you can answer that question with data, you can:
1. Target more prospects that look like your best deals
2. Disqualify prospects that look like your worst deals
3. Optimize your sales process around what actually drives closes
4. Forecast revenue more accurately based on deal characteristics

---

### The Deal Anatomy: 12 Variables

For every closed deal (won or lost), capture these 12 variables:

#### Deal Profile Variables

| Variable | What to Capture | Why It Matters |
|----------|----------------|---------------|
| **1. Deal size** | Final contract value | Revenue per deal affects everything downstream |
| **2. Sales cycle length** | Days from first touch to close | Longer cycles = higher cost to serve |
| **3. Source channel** | Outbound, inbound, referral, event, partner | Which channels produce the best deals |
| **4. Number of touches** | Emails, calls, meetings before close | Effort required per deal |
| **5. Decision committee size** | How many people were involved | More stakeholders = slower, riskier deals |

#### Account Profile Variables

| Variable | What to Capture | Why It Matters |
|----------|----------------|---------------|
| **6. Company size** | Employee count at time of deal | Which company sizes close best |
| **7. Industry** | Vertical/sector | Which industries convert best |
| **8. Growth stage** | Seed, Series A/B/C, PE-backed, public | Stage affects urgency and budget |
| **9. Tech stack** | Relevant tools they were using | Tech affinity patterns |
| **10. Trigger event** | What triggered the evaluation | Which events produce deals |

#### Stakeholder Variables

| Variable | What to Capture | Why It Matters |
|----------|----------------|---------------|
| **11. Champion title** | Who internally pushed for the deal | Which personas champion most effectively |
| **12. Economic buyer title** | Who signed the check | Which titles have budget authority |

---

### Analysis 1: Win Pattern Analysis

Pull your last 20-50 closed-won deals and analyze:

#### Firmographic Patterns

```
CLOSED-WON ANALYSIS: {{N}} deals

Company Size Distribution:
| Size Bucket | Deals Won | % of Wins | Avg Deal Size | Avg Cycle (days) |
|------------|-----------|-----------|---------------|-----------------|
| 1-50 emp | __ | __% | $__ | __ |
| 51-200 emp | __ | __% | $__ | __ |
| 201-500 emp | __ | __% | $__ | __ |
| 501-1000 emp | __ | __% | $__ | __ |
| 1000+ emp | __ | __% | $__ | __ |

Sweet spot: {{size range with highest win concentration and best unit economics}}
```

#### Source Channel Analysis

```
Channel Performance:
| Channel | Deals Won | Avg Deal Size | Avg Cycle | Win Rate | Revenue |
|---------|-----------|---------------|-----------|----------|---------|
| Outbound (cold) | __ | $__ | __ days | __% | $__ |
| Inbound (content/SEO) | __ | $__ | __ days | __% | $__ |
| Referral | __ | $__ | __ days | __% | $__ |
| Events/conferences | __ | $__ | __ days | __% | $__ |
| Partner | __ | $__ | __ days | __% | $__ |

Best channel by revenue: ___
Best channel by win rate: ___
Best channel by speed: ___
```

#### Trigger Event Analysis

```
What triggered the winning deals:
| Trigger | Frequency | Avg Deal Size | Avg Cycle |
|---------|-----------|---------------|-----------|
| ___ | __% | $__ | __ days |
| ___ | __% | $__ | __ days |
| ___ | __% | $__ | __ days |

Insight: {{which triggers predict the largest, fastest deals}}
```

#### Champion Analysis

```
Who championed the winning deals:
| Champion Title | Frequency | Avg Deal Size | Avg Cycle | Win Rate |
|---------------|-----------|---------------|-----------|----------|
| ___ | __% | $__ | __ days | __% |
| ___ | __% | $__ | __ days | __% |
| ___ | __% | $__ | __ days | __% |

Best champion: {{title that leads to the highest win rate and largest deals}}
```

---

### Analysis 2: Loss Pattern Analysis

Equally important — analyze your last 20-50 closed-lost deals:

#### Loss Reason Distribution

```
| Loss Reason | Frequency | Avg Deal Size | Stage Lost | Could Have Prevented? |
|------------|-----------|---------------|-----------|---------------------|
| Went with competitor | __% | $__ | ___ | Y/N — How: ___ |
| No decision / status quo | __% | $__ | ___ | Y/N — How: ___ |
| Budget not approved | __% | $__ | ___ | Y/N — How: ___ |
| Timing — pushed to next quarter | __% | $__ | ___ | Y/N — How: ___ |
| Champion left the company | __% | $__ | ___ | Y/N — How: ___ |
| Requirements changed | __% | $__ | ___ | Y/N — How: ___ |
```

#### Preventable Losses

The most actionable analysis: which losses could have been prevented with better targeting, qualification, or sales process?

| Loss Category | Prevention Strategy |
|-------------|-------------------|
| Lost to competitor | Improve competitive positioning. Build battlecards. Address differentiators earlier. |
| No decision (stuck) | Better qualification upfront. Identify urgency drivers earlier. Set mutual action plans. |
| Budget rejected | Validate budget authority earlier. Build ROI models. Multi-thread (reach the economic buyer). |
| Champion left | Multi-thread from day one. Never rely on a single contact. |
| Bad fit discovered late | Tighten qualification criteria. Disqualify faster. |

---

### Analysis 3: Speed-to-Close Patterns

Which deal characteristics correlate with faster closes?

```
SPEED ANALYSIS:

Deals that closed in < 30 days:
- Common traits: ___
- Avg committee size: ___
- Typical trigger: ___
- Champion title: ___

Deals that took 90+ days:
- Common traits: ___
- Avg committee size: ___
- Typical friction point: ___
- What slowed them down: ___

Speed accelerators:
1. {{factor that correlates with faster closes}}
2. {{factor}}
3. {{factor}}

Speed killers:
1. {{factor that correlates with slower closes}}
2. {{factor}}
3. {{factor}}
```

---

### Analysis 4: Deal Size Patterns

What predicts larger deal sizes?

```
DEAL SIZE ANALYSIS:

Deals > ${{threshold}} (top quartile):
- Company size: ___
- Industry: ___
- Champion title: ___
- Trigger: ___
- Average number of stakeholders: ___

Deals < ${{threshold}} (bottom quartile):
- Company size: ___
- Industry: ___
- Champion title: ___
- Trigger: ___
- Average number of stakeholders: ___

What correlates with larger deals:
1. ___
2. ___
3. ___
```

---

### Analysis 5: The Ideal Deal Profile

Combine all analyses into a single "ideal deal" composite:

```
THE IDEAL DEAL PROFILE

Company:
- Size: {{range}}
- Industry: {{verticals}}
- Stage: {{growth stage}}
- Trigger: {{what happened}}

Stakeholders:
- Champion: {{title}} — enters at {{stage}}
- Economic buyer: {{title}} — enters at {{stage}}
- Committee size: {{number}}

Deal characteristics:
- Expected size: ${{range}}
- Expected cycle: {{days}} days
- Source channel: {{channel}}
- Number of touches to close: {{range}}

Red flags (walk away if):
- {{red flag 1}}
- {{red flag 2}}
- {{red flag 3}}

Green flags (accelerate if):
- {{green flag 1}}
- {{green flag 2}}
- {{green flag 3}}
```

---

### Feeding Deal Patterns Back into Outbound

The ultimate purpose of deal pattern analysis is to improve your targeting and messaging:

| Pattern Insight | Outbound Action |
|----------------|----------------|
| Best deals come from Series B companies | Prioritize Series B in your ICP matrix |
| Deals triggered by "new VP Sales" close 2x faster | Build a trigger campaign for leadership changes |
| VP Sales as champion has highest win rate | Target VP Sales as primary persona |
| Deals with 4+ stakeholders take 3x longer | Qualify for committee size early, multi-thread from day one |
| Referral deals close 40% faster | Build a referral ask into your sequence Step 4 |
| Lost deals often cite competitor X | Address competitor X positioning in Step 2-3 |

---

### Analysis Cadence

| Frequency | Analysis | Minimum Sample |
|-----------|----------|---------------|
| **Monthly** | Quick review of new wins and losses | All deals that closed this month |
| **Quarterly** | Full deal pattern analysis (all 5 analyses) | Last 50+ closed deals |
| **Annually** | Trend analysis: how are deal patterns shifting? | Full year of data |
| **Ad hoc** | Specific investigation (e.g., "why are enterprise deals stalling?") | Relevant subset |

## Templates

### Deal Pattern Report
```
# Deal Pattern Report
# Period: {{date_range}}
# Deals Analyzed: {{won}} won, {{lost}} lost
# Analyst: {{name}}

## Key Findings

### The Ideal Deal Looks Like:
{{1-2 sentence summary of the ideal deal profile}}

### Top 3 Win Predictors:
1. {{predictor}} — {{evidence}}
2. {{predictor}} — {{evidence}}
3. {{predictor}} — {{evidence}}

### Top 3 Loss Predictors:
1. {{predictor}} — {{evidence}}
2. {{predictor}} — {{evidence}}
3. {{predictor}} — {{evidence}}

### Recommended Changes
| Area | Current | Recommended | Expected Impact |
|------|---------|-------------|----------------|
| Targeting | ___ | ___ | ___ |
| Qualification | ___ | ___ | ___ |
| Messaging | ___ | ___ | ___ |
| Process | ___ | ___ | ___ |
```

## Tips
- You need at least 30 closed deals (combined wins and losses) for patterns to be statistically meaningful. Below that, treat findings as hypotheses, not conclusions.
- The most common mistake: only analyzing wins. Your losses contain just as much — often more — actionable intelligence. The pattern of WHY deals die is the pattern of what to fix.
- Don't confuse correlation with causation. If your biggest deals come from referrals, it might be because referrals come pre-qualified — not because the referral channel itself is magic. Test before restructuring.
- Share deal pattern insights with everyone, not just sales. Marketing needs to know which triggers to target. Product needs to know which features close deals. Leadership needs to know which segments to invest in.
- The ideal deal profile should directly inform your ICP matrix, your trigger campaigns, your persona development, and your lead prioritization. If your deal patterns say one thing and your targeting says another, one of them is wrong.

---

*Progressive disclosure: load CRM-specific data extraction queries and advanced statistical analysis frameworks only when running deal pattern analysis on a specific dataset.*
