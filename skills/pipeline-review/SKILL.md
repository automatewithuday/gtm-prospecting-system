---
name: pipeline-review
description: "Use when stage 20 of the prospecting system needs the weekly review — where the workflow is leaking leads between stages, which segments and sources are producing positive replies, and what to change in targeting next week. Also use standalone to diagnose outbound campaign performance."
license: MIT
metadata:
  author: automatewithuday
  source: martechs.io
  ported_from: gtm-flywheel/campaign-analytics/performance-analysis/SKILL.md
---

# Campaign Performance Analysis

## Pipeline contract

**Stage 20 of 20.** Reads the whole run folder. Writes `20-review-<YYYY-MM-DD>.md`.

1. Run `uv run scripts/check_run.py runs/<run>` — it prints the stage funnel (rows in → rows out) and flags the biggest drop. Start the review there.
2. Cut positive reply rate and meetings by `segment`, `source_type`, and `tier`. Below 30 sends in a cell, report the count and draw no conclusion.
3. Propose targeting changes (ICP filters, judge prompt, score weights, sources to add or drop) as a list for the human. Do not edit `02-client-profile.yaml`, the judge prompt, or weights yourself.
4. Approved changes start the next run at stage 2.

Weekly operating cadence: `references/cold-email-weekly-rhythm.md`. Benchmarks: `references/campaign-benchmarking.md`.

Files live in `runs/<run>/`. Column definitions: [`/prospecting-system`](../prospecting-system/SKILL.md). Standalone use: ignore this block.


## When to Use
- Reviewing campaign results after a send cycle completes
- Diagnosing why a campaign is underperforming
- Comparing campaign variants to identify winners
- Building performance reports for clients or leadership
- Making data-driven decisions about what to scale, pause, or kill

## Framework

### The Campaign Metrics Stack

Measure campaigns in layers. Each layer tells you something different about what's working and what isn't.

```
Layer 1: Deliverability     → Did the email reach the inbox?
Layer 2: Engagement         → Did they open and read it?
Layer 3: Response           → Did they reply?
Layer 4: Quality            → Was the reply positive?
Layer 5: Conversion         → Did the reply turn into a meeting?
Layer 6: Revenue            → Did the meeting turn into revenue?
```

**Critical insight:** Most teams obsess over Layer 2-3 (opens and replies) while ignoring Layer 1 (deliverability) and Layer 4-6 (quality and revenue). The full stack matters.

---

### Layer 1: Deliverability Metrics

| Metric | Target | Red Flag | What It Tells You |
|--------|--------|----------|-------------------|
| **Bounce rate** | < 3% | > 5% | List quality. High bounces = bad data or unverified emails. |
| **Spam complaint rate** | 0% | > 0.1% | Content or targeting issue. Immediate pause needed. |
| **Inbox placement rate** | > 95% | < 85% | Domain/IP reputation. May need warmup or domain rotation. |
| **Unsubscribe rate** | < 0.5% | > 1% | Targeting accuracy. Wrong people or too many touches. |

**If deliverability metrics are off, STOP. Do not optimize copy, subject lines, or targeting until deliverability is fixed.** You're optimizing something that never reaches the prospect.

#### Deliverability Diagnostic

```
Bounce rate > 5%?
├── YES → Verify email list. Switch to verified-only sends.
└── NO ↓

Inbox placement < 85%?
├── YES → Check domain reputation (Google Postmaster, MXToolbox)
│         → Reduce daily send volume
│         → Rotate sending domains
│         → Review email content for spam triggers
└── NO ↓

Spam complaints > 0?
├── YES → Review targeting. Are you emailing the right people?
│         → Check for spam trigger words in subject/body
│         → Ensure unsubscribe link is visible
└── NO → Deliverability is healthy. Move to Layer 2.
```

---

### Layer 2: Engagement Metrics

| Metric | Target | Red Flag | What It Tells You |
|--------|--------|----------|-------------------|
| **Open rate** | 60-80% | < 40% | Subject line + deliverability + send timing |
| **Open rate by step** | Declining 5-10% per step | Drops > 20% per step | Sequence fatigue or deliverability degradation |
| **Unique opens** | Track vs. total opens | Low unique/high total | Same people reopening, not new engagement |

**Note on open tracking:** Open tracking uses invisible pixels that can hurt deliverability. If you're tracking opens, use it for diagnostic purposes but consider turning it off for production campaigns. Low open rate with high reply rate = your emails are landing but the pixel isn't loading (common with Outlook).

#### Subject Line Analysis

| Subject Line | Open Rate | Sample Size | Verdict |
|-------------|-----------|-------------|---------|
| Variant A | __% | __ sends | Winner / Loser / Inconclusive |
| Variant B | __% | __ sends | Winner / Loser / Inconclusive |
| Variant C | __% | __ sends | Winner / Loser / Inconclusive |

**Minimum sample size:** 200 sends per variant before drawing conclusions. Below 200, the variance is too high to trust.

---

### Layer 3: Response Metrics

| Metric | Target | Red Flag | What It Tells You |
|--------|--------|----------|-------------------|
| **Total reply rate** | 8-15% | < 5% | Copy relevance + offer strength + list quality |
| **Reply rate by step** | Step 1: highest, declining | Step 1 < 3% | Opening email isn't earning replies |
| **Reply timing** | Most replies within 24h | Delayed replies (3+ days) | Email is interesting but not urgent |
| **Auto-reply rate** | Track separately | > 10% | Many OOO or bounced-to-assistant |

#### Reply Rate Diagnostic

```
Reply rate < 5% overall?
├── Open rate > 60%?
│   ├── YES → Copy problem. Emails are being read but not compelling.
│   │         → Test new body copy variants
│   │         → Test new CTAs
│   │         → Review personalization quality
│   └── NO  → Subject line or deliverability problem.
│             → Fix opens first, then reassess replies.
│
Reply rate > 5% but meetings are low?
├── Most replies are negative ("not interested", "remove me")?
│   ├── YES → Targeting problem. You're reaching the wrong people.
│   │         → Review ICP and list quality
│   └── NO  → Qualification problem. Interested leads aren't converting.
│             → Review your meeting booking process
│             → Improve reply handling speed
```

---

### Layer 4: Quality Metrics (Most Important)

| Metric | Target | Red Flag | What It Tells You |
|--------|--------|----------|-------------------|
| **Positive reply rate** | 2-8% | < 1% | True message-market fit |
| **Negative reply rate** | < 3% | > 5% | Targeting accuracy |
| **Referral replies** | Track separately | — | Valuable — contact the referral |
| **"Not now" replies** | Track separately | — | Future pipeline. Add to nurture. |

#### Reply Classification Framework

Every reply should be classified:

| Category | Definition | Action | Example |
|----------|-----------|--------|---------|
| **Positive: Meeting** | Agreed to a call/meeting | Book immediately (< 1 hour) | "Sure, let's chat next week" |
| **Positive: Interest** | Interested but no commitment yet | Reply with value, ask for meeting | "Tell me more about this" |
| **Positive: Referral** | Directed you to someone else | Contact the referral, thank the original | "Talk to Sarah, she handles this" |
| **Neutral: Not Now** | Timing issue, not a rejection | Add to nurture, follow up in 30-60 days | "Not a priority right now" |
| **Neutral: OOO** | Out of office auto-reply | Re-send after they return | "I'm out until March 1" |
| **Negative: Not Interested** | Polite rejection | Respect it. Remove from sequence. | "Thanks, but we're all set" |
| **Negative: Angry** | Hostile response | Remove immediately. Review targeting. | "Stop emailing me" |
| **Negative: Unsubscribe** | Requests removal | Remove immediately. Legal requirement. | "Please remove me from your list" |

**The ratio that matters most:**
```
Positive Reply Rate = (Positive replies ÷ Total emails sent) × 100
```
This single metric is the truest measure of campaign effectiveness. It strips out noise (opens, negative replies) and measures real demand generation.

---

### Layer 5: Conversion Metrics

| Metric | Target | Red Flag | What It Tells You |
|--------|--------|----------|-------------------|
| **Reply-to-meeting rate** | 40-60% | < 25% | Reply handling quality + qualification |
| **Meeting show rate** | 80-90% | < 70% | Confirmation process + prospect quality |
| **Meeting-to-opportunity rate** | 30-50% | < 20% | Discovery call quality + true fit |
| **Cost per meeting** | Varies by ACV | Rising over time | Campaign efficiency trending |

---

### Layer 6: Revenue Metrics

| Metric | Target | What It Tells You |
|--------|--------|-------------------|
| **Pipeline generated** | Track per campaign | Total $ value of opportunities created |
| **Revenue closed** | Track per campaign | Actual revenue attributable to outbound |
| **Cost per opportunity** | Varies by ACV | Efficiency of the outbound motion |
| **CAC (Customer Acquisition Cost)** | < 1/3 of first-year ACV | Sustainability of the channel |
| **Time to close** | Track by campaign/segment | Which campaigns produce faster deals |

---

### The Performance Analysis Report

#### Campaign Summary Card

```
CAMPAIGN: {{campaign_name}}
Period: {{start_date}} — {{end_date}}
Total sends: {{total_sends}}

DELIVERABILITY
  Bounce rate: __% (target: <3%)
  Spam complaints: __ (target: 0)

ENGAGEMENT
  Open rate: __% (target: 60-80%)

RESPONSE
  Total reply rate: __% (target: 8-15%)
  Positive reply rate: __% (target: 2-8%)
  Negative reply rate: __%

CONVERSION
  Meetings booked: __
  Reply-to-meeting rate: __%
  Cost per meeting: $__

REVENUE
  Pipeline generated: $__
  Revenue closed: $__
  ROI: __x
```

#### Variant Comparison Table

```
| Metric | Variant A | Variant B | Variant C | Winner |
|--------|-----------|-----------|-----------|--------|
| Sends | __ | __ | __ | — |
| Open rate | __% | __% | __% | __ |
| Reply rate | __% | __% | __% | __ |
| Positive reply rate | __% | __% | __% | __ |
| Meetings | __ | __ | __ | __ |
```

#### Step Performance Breakdown

```
| Step | Sends | Opens | Open Rate | Replies | Reply Rate | Positive | Positive Rate |
|------|-------|-------|-----------|---------|------------|----------|---------------|
| 1 | __ | __ | __% | __ | __% | __ | __% |
| 2 | __ | __ | __% | __ | __% | __ | __% |
| 3 | __ | __ | __% | __ | __% | __ | __% |
| 4 | __ | __ | __% | __ | __% | __ | __% |
```

---

### Decision Framework: Scale, Optimize, or Kill

| Scenario | Diagnosis | Action |
|----------|----------|--------|
| Positive reply rate > 5% | Campaign is working | Scale: increase volume, clone for new segments |
| Positive reply rate 2-5% | Campaign has potential | Optimize: test new variants, improve personalization |
| Positive reply rate 1-2% | Campaign is marginal | Diagnose: is it copy, targeting, or timing? Fix one variable |
| Positive reply rate < 1% | Campaign isn't working | Kill: stop sending. Redesign from scratch or abandon the angle |

## Templates

### Weekly Campaign Report Template
```
# Weekly Campaign Report
# Period: {{week}}

## Summary
- Active campaigns: __
- Total sends this week: __
- Avg positive reply rate: __%
- Meetings booked: __

## Top Performing Campaign
{{campaign_name}} — {{positive_reply_rate}}% positive reply rate

## Underperforming (Action Needed)
{{campaign_name}} — {{issue}} → {{recommended_action}}

## Key Decisions
- Scale: {{campaign_to_scale}}
- Optimize: {{campaign_to_optimize}}
- Kill: {{campaign_to_kill}}

## Next Week Plan
- {{action_1}}
- {{action_2}}
```

## Tips
- Positive reply rate is the only metric that matters for campaign-level decisions. Everything else (opens, total replies) is diagnostic — useful for understanding WHY, but not for deciding WHAT to do.
- Always compare apples to apples. A campaign targeting VPs at enterprise companies will have different benchmarks than one targeting founders at SMBs. Segment your analysis.
- The most common analysis mistake: drawing conclusions from too-small samples. 50 sends with a 10% reply rate is not a winning campaign — it's noise. Wait for 200+ sends per variant.
- Track metrics over time, not just snapshots. A campaign with a 5% reply rate in week 1 and 2% in week 4 is degrading — the list might be exhausted or deliverability is dropping.
- Don't average across campaigns. One campaign with a 15% positive reply rate and one with 0.5% averages to 7.75% — but that hides the fact that one is amazing and one is terrible.

---

*Progressive disclosure: load platform-specific analytics integrations and automated reporting configs only when analyzing data from a specific sending platform.*
