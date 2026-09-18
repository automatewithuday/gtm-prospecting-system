# Campaign Benchmarking

## When to Use
- Evaluating whether a campaign's performance is good, average, or poor
- Setting targets for new campaigns before launch
- Reporting performance to stakeholders who need context (not just numbers)
- Comparing performance across clients, segments, verticals, or time periods
- Identifying systemic trends in your outbound operation

## Framework

### Why Benchmarks Matter

A 5% reply rate means nothing without context.
- 5% reply rate for a cold email campaign targeting C-suite at Fortune 500? **Exceptional.**
- 5% reply rate for a warm re-engagement campaign targeting SMB founders? **Terrible.**

Benchmarks provide the context. They tell you whether to celebrate, optimize, or panic.

---

### The Three Benchmark Layers

#### Layer 1: Industry Benchmarks (External)
*How does your performance compare to the market?*

These are broad averages based on aggregated data from email platforms, industry reports, and agency networks. Use them as a sanity check, not as targets.

| Metric | Poor | Average | Good | Excellent |
|--------|------|---------|------|-----------|
| **Open rate** | < 30% | 30-50% | 50-70% | > 70% |
| **Total reply rate** | < 3% | 3-8% | 8-15% | > 15% |
| **Positive reply rate** | < 1% | 1-3% | 3-8% | > 8% |
| **Bounce rate** | > 5% | 3-5% | 1-3% | < 1% |
| **Unsubscribe rate** | > 2% | 0.5-2% | 0.1-0.5% | < 0.1% |
| **Reply-to-meeting rate** | < 20% | 20-35% | 35-50% | > 50% |
| **Meeting show rate** | < 60% | 60-75% | 75-85% | > 85% |

**Important caveats:**
- These vary enormously by ICP, persona, industry, and deal size
- Enterprise campaigns have lower reply rates but higher deal values
- SMB campaigns have higher reply rates but lower deal values
- Signal-based campaigns should significantly outperform these averages
- These benchmarks assume standard 4-step email sequences

#### Layer 2: Internal Benchmarks (Your Portfolio)
*How does this campaign compare to YOUR other campaigns?*

This is the most actionable benchmark layer. You control all the variables.

Build your internal benchmark from:
```
For each metric, calculate across all campaigns with 200+ sends:
- Portfolio average (mean)
- Portfolio median (more useful — not skewed by outliers)
- Top quartile (75th percentile — your "good" baseline)
- Top decile (90th percentile — your "excellent" baseline)
- Bottom quartile (25th percentile — your "needs work" line)
```

| Metric | Your Bottom 25% | Your Median | Your Top 25% | Your Top 10% |
|--------|-----------------|-------------|-------------|-------------|
| Open rate | __% | __% | __% | __% |
| Positive reply rate | __% | __% | __% | __% |
| Reply-to-meeting rate | __% | __% | __% | __% |
| Cost per meeting | $__ | $__ | $__ | $__ |

**Update these quarterly.** As your team improves, your benchmarks should rise.

#### Layer 3: Segment Benchmarks (Apples to Apples)
*How does this campaign compare to similar campaigns?*

Generic benchmarks are misleading. A campaign targeting VP Sales at Series B SaaS should be compared to OTHER campaigns targeting VP Sales at Series B SaaS — not to campaigns targeting SMB founders.

Segment your benchmarks by:

| Segmentation | Why It Matters |
|-------------|---------------|
| **By persona** | VP-level targets respond differently than Founders |
| **By company size** | SMB vs. mid-market vs. enterprise = different benchmarks |
| **By industry** | B2B SaaS vs. healthcare vs. financial services = different norms |
| **By campaign type** | Signal-based vs. list-based vs. re-engagement = different baselines |
| **By channel** | Email-only vs. multi-channel = different metrics |
| **By client** (for agencies) | Different offers have different conversion rates |

```
SEGMENT BENCHMARK: VP Sales @ Series B SaaS Companies

Campaigns in this segment: 12
Total sends: 8,400
Date range: Last 6 months

Benchmark Table:
| Metric | 25th %ile | Median | 75th %ile | 90th %ile |
|--------|-----------|--------|-----------|-----------|
| Positive reply rate | __% | __% | __% | __% |
| Reply-to-meeting | __% | __% | __% | __% |
| Meetings booked per 1000 | __ | __ | __ | __ |
```

---

### The Benchmarking Report

#### Campaign Scorecard

For each campaign, calculate a relative performance index:

```
CAMPAIGN SCORECARD: {{campaign_name}}

Metric              | Actual  | Segment Benchmark | vs. Benchmark | Grade
--------------------|---------|-------------------|---------------|------
Open rate           | __%     | __%               | +/- __%       | A/B/C/D
Positive reply rate | __%     | __%               | +/- __%       | A/B/C/D
Reply-to-meeting    | __%     | __%               | +/- __%       | A/B/C/D
Meetings booked     | __      | __                | +/- __        | A/B/C/D
Cost per meeting    | $__     | $__               | +/- $__       | A/B/C/D

Overall Grade: ___
```

**Grading scale:**
| Grade | Criteria |
|-------|----------|
| **A** | Above 75th percentile for the segment |
| **B** | Between median and 75th percentile |
| **C** | Between 25th percentile and median |
| **D** | Below 25th percentile |

---

### Cross-Portfolio Analysis

For agencies managing multiple clients, or companies running multiple segments:

#### Client Comparison Dashboard

```
| Client | Campaigns | Avg Positive Reply Rate | vs. Portfolio Median | Trend (3mo) |
|--------|-----------|------------------------|---------------------|-------------|
| ___ | __ | __% | +/- __% | ↑ ↓ → |
| ___ | __ | __% | +/- __% | ↑ ↓ → |
| ___ | __ | __% | +/- __% | ↑ ↓ → |
```

#### Time Series Analysis

Track metrics over time to identify trends:

```
Monthly Performance Trend:
| Month | Campaigns | Sends | Avg Open Rate | Avg Positive Reply Rate | Meetings |
|-------|-----------|-------|--------------|------------------------|----------|
| Jan   | __ | __ | __% | __% | __ |
| Feb   | __ | __ | __% | __% | __ |
| Mar   | __ | __ | __% | __% | __ |
```

**What to watch for:**
- **Rising trend:** Your system is improving. Document what changed.
- **Flat trend:** Plateaued. Time to test new approaches.
- **Declining trend:** Something broke. Could be deliverability, list quality, market saturation, or copy fatigue.
- **Seasonal patterns:** Many B2B metrics dip in December and August. Don't overreact to predictable cycles.

---

### Benchmark-Driven Decisions

Use benchmarks to drive specific actions:

| Scenario | Benchmark Context | Decision |
|----------|------------------|----------|
| New campaign at 4% positive reply rate | Segment median is 2.5% | **Above benchmark. Scale.** |
| New campaign at 4% positive reply rate | Segment median is 6% | **Below benchmark. Optimize before scaling.** |
| Client asking "how are we doing?" | Their campaigns are at the 60th percentile | **"Above average for your segment. Here's what the top 10% looks like."** |
| All campaigns declining month-over-month | Portfolio-wide trend, not isolated | **Systemic issue. Check deliverability, domain health, or market shift.** |
| One campaign dramatically outperforming | 3x the segment median | **Extract the winning patterns. Replicate across other campaigns.** |

---

### Setting Targets for New Campaigns

Use benchmarks to set realistic, data-driven targets:

```
TARGET SETTING: {{new_campaign_name}}

Segment: {{persona}} @ {{company_type}}
Historical data available: {{number}} similar campaigns

Target Benchmarks:
- Positive reply rate: __%  (segment median: __%, stretch: __%)
- Meetings per 1000 sends: __  (segment median: __, stretch: __)
- Reply-to-meeting rate: __%  (segment median: __%, stretch: __%)
- Cost per meeting: $__  (segment median: $__, stretch: $__)

Review timeline: Day 14 for initial read, Day 30 for full assessment
Minimum sends before evaluation: 200 per variant
```

**First-time segment (no historical data):**
When you're targeting a new persona or vertical for the first time, use industry benchmarks (Layer 1) as initial targets, then adjust based on real data after 2-4 weeks.

---

### Advanced: Efficiency Metrics

Beyond reply rates, benchmark your operational efficiency:

| Metric | What It Measures | How to Calculate |
|--------|-----------------|-----------------|
| **Sends per meeting** | How many emails to generate one meeting | Total sends ÷ meetings booked |
| **Cost per meeting** | Total cost (tools, time, email accounts) per meeting | Total campaign cost ÷ meetings booked |
| **Meetings per 1000 sends** | Normalized meeting production | (Meetings ÷ sends) × 1000 |
| **Pipeline per 1000 sends** | Dollar value generated per outreach unit | (Pipeline $ ÷ sends) × 1000 |
| **Revenue per 1000 sends** | Closed revenue per outreach unit | (Revenue $ ÷ sends) × 1000 |
| **Time to first meeting** | Speed from campaign launch to first meeting | Date of first meeting - launch date |

These efficiency metrics matter more than vanity metrics. A campaign with a 3% reply rate that generates $500K in pipeline is more valuable than a campaign with a 10% reply rate that generates $50K.

## Templates

### Benchmark Reference Card
```
# Benchmark Reference: {{Company/Product Name}}
# Updated: {{date}}
# Based on: {{N}} campaigns, {{N}} sends

## Portfolio Benchmarks (All Campaigns)
| Metric | 25th %ile | Median | 75th %ile | 90th %ile |
|--------|-----------|--------|-----------|-----------|
| Open rate | __% | __% | __% | __% |
| Positive reply rate | __% | __% | __% | __% |
| Reply-to-meeting | __% | __% | __% | __% |
| Meetings/1000 sends | __ | __ | __ | __ |
| Cost per meeting | $__ | $__ | $__ | $__ |

## Segment Benchmarks
### Segment: {{name}}
[Same table format, filtered to segment]

### Segment: {{name}}
[Same table format, filtered to segment]
```

## Tips
- Internal benchmarks are 10x more valuable than industry benchmarks. Your data reflects YOUR offer, YOUR ICP, YOUR team's execution. Industry averages don't.
- Never benchmark a new campaign against your all-time best campaign. Benchmark against the median for that segment. Expecting every campaign to be your best is a recipe for disappointment and bad decisions.
- The best benchmark question isn't "are we good?" — it's "are we improving?" A 3% positive reply rate that was 1.5% six months ago is a bigger win than a 5% rate that's been flat.
- When reporting to clients or leadership, always provide context. "4% positive reply rate" means nothing. "4% positive reply rate, which puts you in the top 25% of campaigns in your segment" tells a story.
- Build your benchmarking database from day one. Even if you only have 5 campaigns, start tracking. The compound value of historical benchmarks grows with every campaign you run.
- Watch out for survivorship bias. If you only benchmark against campaigns that ran their full course (and ignore the ones you killed early), your benchmarks will be inflated.

---

*Progressive disclosure: load platform-specific data aggregation queries and automated benchmark calculation scripts only when building benchmarks from a specific data source.*
