---
name: lead-prioritization
description: "Use when stage 11 of the prospecting system needs fit, intent, and engagement combined into one ranked queue with tiers. Also use standalone to build a weighted lead priority model."
license: MIT
metadata:
  author: automatewithuday
  source: martechs.io
  ported_from: gtm-flywheel/signal-scoring/lead-prioritization/SKILL.md
---

# Lead Prioritization

## Pipeline contract

**Stage 11 of 20.** Reads `10-scored.csv`, `09-signals.csv`. Writes `11-prioritized.csv` (adds `intent_score`, `engagement_score`, `priority_score`, `tier`), sorted best first.

- Engagement for a cold list = audience evidence: `source_type` (engager > follower > member/attendee > search) and `source_count`.
- Keep the three component scores next to `priority_score` so anyone can see why a lead ranks where it does.
- Rows with `screen=fail` are carried through unranked, not deleted.
- Cap the outreach set here (default: top 500, or fewer if fewer qualify — never pad).

Files live in `runs/<run>/`. Column definitions: [`/prospecting-system`](../prospecting-system/SKILL.md). Standalone use: ignore this block.


## When to Use
- Processing a new lead list and need to decide who to contact first
- Building a priority queue for SDR teams to work through daily
- Designing lead scoring models for CRM or marketing automation
- Optimizing campaign ROI by focusing outreach on highest-probability prospects

## Framework

### Why Prioritization Matters

Without prioritization, your team works leads in the order they were imported — alphabetically, randomly, or whoever the SDR happens to click on first. This guarantees that your best prospects get the same treatment as your worst ones.

With prioritization, your team contacts the highest-probability leads first, every day. The result: same effort, 2-3x more meetings.

```
Without prioritization:
100 emails/day × 3% reply rate = 3 replies/day (random quality)

With prioritization (best leads first):
100 emails/day × 8% reply rate (top leads) = 8 replies/day
```

---

### The Lead Priority Score

A composite score that combines three dimensions:

```
Priority Score = (Fit Score × 0.30) + (Intent Score × 0.45) + (Engagement Score × 0.25)
```

**Why intent is weighted highest:** A perfectly-fit company with no intent is a cold target. A moderately-fit company with strong intent is likely in-market. Intent is the strongest predictor of near-term conversion.

---

### Dimension 1: Fit Score (30% of total)

How well does this lead match your ICP? (Derived from your ICP Matrix)

| Component | Max Points | Scoring |
|-----------|-----------|---------|
| Company size match | 20 | Tier 1 = 20, Tier 2 = 14, Tier 3 = 8 |
| Industry match | 15 | Primary = 15, Adjacent = 10, Tangential = 5 |
| Revenue range match | 15 | In range = 15, Near range = 10, Far = 5 |
| Persona title match | 20 | Exact match = 20, Close variant = 14, Adjacent = 8 |
| Geography match | 10 | Primary market = 10, Secondary = 6, Tertiary = 3 |
| Tech stack match | 10 | Uses partners/competitors = 10, Some overlap = 5, None = 0 |
| Growth stage match | 10 | Ideal stage = 10, Adjacent = 6, Mismatch = 2 |

**Total Fit Score: 0-100**

#### Fit Score Tiers

| Score | Fit Level | Interpretation |
|-------|-----------|---------------|
| 80-100 | Excellent | Perfect ICP match. Prioritize regardless of other scores. |
| 60-79 | Strong | Good fit. Proceed with outreach if intent or engagement present. |
| 40-59 | Moderate | Acceptable fit. Only pursue if intent signals are strong. |
| 20-39 | Weak | Marginal fit. Test in small batches only. |
| 0-19 | No Fit | Disqualify. Do not contact. |

---

### Dimension 2: Intent Score (45% of total)

How likely is this lead to be in-market right now?

| Signal | Max Points | Scoring | Decay Rate |
|--------|-----------|---------|------------|
| Competitor evaluation (G2, reviews) | 20 | Detected = 20 | -5/week |
| Hiring for target role | 15 | Active posting = 15, Recently filled = 8 | -3/week |
| Recent funding | 15 | < 30 days = 15, 30-90 days = 10, 90-180 = 5 | -2/month |
| Website visit (pricing/product pages) | 15 | Multiple visits = 15, Single = 8 | -5/week |
| Leadership change in target dept | 10 | < 60 days = 10, 60-120 days = 5 | -2/month |
| Content consumption (your content) | 10 | Multiple pieces = 10, Single = 5 | -3/week |
| Social signals (posts about pain) | 10 | Specific post = 10, Engagement = 5 | -5/week |
| Tech stack change | 5 | Detected = 5 | -1/month |

**Total Intent Score: 0-100**

**Critical concept: Signal Decay.** Intent signals lose value over time. A funding round from last week is urgent. A funding round from 6 months ago is a fact, not a signal. Apply decay rates to keep your scoring model honest.

#### Intent Score Tiers

| Score | Intent Level | Interpretation |
|-------|-------------|---------------|
| 70-100 | Very High | Multiple strong signals. Contact immediately. |
| 50-69 | High | Clear buying indicators. Contact within the week. |
| 30-49 | Medium | Some signals present. Include in next campaign batch. |
| 10-29 | Low | Minimal intent detected. Monitor for changes. |
| 0-9 | None | No intent signals. Do not prioritize. |

---

### Dimension 3: Engagement Score (25% of total)

How has this lead interacted with your outreach and content?

| Activity | Max Points | Scoring |
|----------|-----------|---------|
| Replied positively to previous outreach | 30 | Yes = 30 |
| Replied "not now" (timing objection) | 20 | Yes = 20 |
| Opened multiple emails | 10 | 3+ opens = 10, 1-2 = 5 |
| Clicked links in email | 15 | Yes = 15 |
| Connected on LinkedIn | 10 | Yes = 10 |
| Engaged with LinkedIn content (like/comment) | 10 | Yes = 10 |
| Attended webinar or event | 15 | Live = 15, On-demand = 8 |
| Downloaded content (guide, report) | 10 | Yes = 10 |
| Previous conversation (met at event, warm intro) | 20 | Yes = 20 |

**Total Engagement Score: 0-100** (capped at 100 even if multiple activities exceed)

**Note:** For net-new leads with zero engagement history, the engagement score is 0, and the priority is determined entirely by fit + intent. This is expected — cold outbound starts with fit and intent. Engagement builds over time.

---

### Computing the Final Priority Score

```
Priority Score = (Fit × 0.30) + (Intent × 0.45) + (Engagement × 0.25)
Maximum possible: 100
```

#### Priority Tiers

| Priority Score | Tier | Label | Action | SLA |
|---------------|------|-------|--------|-----|
| 80-100 | P1 | Hot | Immediate multi-channel outreach | Contact within 24 hours |
| 60-79 | P2 | Warm | Priority email sequence | Contact within 3 days |
| 40-59 | P3 | Active | Standard campaign inclusion | Contact within 1 week |
| 20-39 | P4 | Passive | Low-priority or nurture | Monthly check-ins |
| 0-19 | P5 | Cold | Do not contact or archive | Review quarterly |

---

### The Daily Priority Queue

Transform your scoring model into a working system:

```
DAILY PRIORITY QUEUE

Morning Routine (9:00 AM):
1. Pull all leads with Priority Score > 60
2. Sort by score (highest first)
3. Check for new signals on top 20 leads
4. Re-score any lead with a new signal detected

Outreach Allocation:
├── P1 (Hot): 40% of daily capacity → personalized, multi-channel
├── P2 (Warm): 35% of daily capacity → signal-based email
├── P3 (Active): 25% of daily capacity → campaign sequences
└── P4-P5: Not in daily queue (automated nurture only)

End-of-Day Review:
- Update engagement scores based on replies/opens
- Move any newly-engaged leads up in priority
- Log new signals detected during outreach
```

---

### Dynamic Re-Scoring

Lead priority is not static. Re-score when:

| Event | Re-Score Action |
|-------|----------------|
| New intent signal detected | Add points to Intent Score, recalculate |
| Lead replies (positive or "not now") | Add points to Engagement Score |
| Signal ages past decay threshold | Subtract points from Intent Score |
| Company data changes (layoffs, funding) | Recalculate Fit Score |
| Lead moves to nurture (no response after full sequence) | Reset Engagement Score, halve Intent Score |
| New data enrichment completes | Recalculate all three dimensions |

---

### Prioritization for Different Campaign Types

| Campaign Type | Priority Formula Adjustment | Why |
|--------------|---------------------------|-----|
| **ABM (1-50 accounts)** | Fit × 0.40 + Intent × 0.40 + Engagement × 0.20 | Fit matters more — you've already hand-picked accounts |
| **Trigger-based** | Fit × 0.20 + Intent × 0.60 + Engagement × 0.20 | Intent IS the campaign — weight it highest |
| **Re-engagement** | Fit × 0.20 + Intent × 0.30 + Engagement × 0.50 | Previous engagement is the strongest signal for re-engagement |
| **Scaled outbound** | Fit × 0.35 + Intent × 0.40 + Engagement × 0.25 | Balance fit and intent at scale |

---

### Common Prioritization Mistakes

| Mistake | Why It's Wrong | Fix |
|---------|---------------|-----|
| Prioritizing by company size only | Big companies aren't better leads without intent | Use the full scoring model |
| Treating all signals equally | A G2 research signal is 10x more valuable than a LinkedIn like | Apply proper weighting |
| Never re-scoring | A lead that was hot 3 months ago may be cold today | Apply signal decay |
| Ignoring engagement history | A lead who replied "not now" 6 months ago is warmer than a net-new lead | Track and score engagement |
| Over-prioritizing large lists | A 10,000-lead list with no scoring = random outreach | Score before sending anything |

## Templates

### Lead Scoring Model Template
```
# Lead Scoring Model: {{Company/Product Name}}
# Version: {{version}} | Updated: {{date}}

## Fit Score Components (30% weight)
| Component | Tier 1 (pts) | Tier 2 (pts) | Tier 3 (pts) |
|-----------|-------------|-------------|-------------|
| ___ | ___ | ___ | ___ |

## Intent Score Components (45% weight)
| Signal | Points | Decay Rate | Source |
|--------|--------|------------|--------|
| ___ | ___ | ___ | ___ |

## Engagement Score Components (25% weight)
| Activity | Points |
|----------|--------|
| ___ | ___ |

## Priority Tiers
| Tier | Score Range | Action | SLA |
|------|-----------|--------|-----|
| P1 | ___ | ___ | ___ |
| P2 | ___ | ___ | ___ |
| P3 | ___ | ___ | ___ |
```

## Tips
- Simplicity beats complexity. A 3-factor scoring model that your team actually uses beats a 15-factor model that lives in a spreadsheet nobody opens. Start simple, add complexity only when data shows it improves outcomes.
- The best validation for your scoring model: run a correlation analysis between lead priority scores and actual close rates. If P1 leads aren't closing at 2-3x the rate of P3 leads, your model is wrong.
- Signal decay is the most overlooked concept in lead scoring. Without it, your "hot leads" list fills up with stale data that was hot 6 months ago. Build decay into your model from day one.
- Don't let perfect be the enemy of good. If you don't have intent data, skip that dimension and weight fit + engagement more heavily. Some prioritization always beats no prioritization.
- Review and adjust your weights quarterly. As your product, market, and sales motion evolve, the relative importance of fit vs. intent vs. engagement shifts.

---

*Progressive disclosure: load CRM-specific scoring implementation guides and automation workflows only when building scoring for a specific tool.*
