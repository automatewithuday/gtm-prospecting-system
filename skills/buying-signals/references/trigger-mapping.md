# Trigger Mapping

## When to Use
- Designing event-driven outbound campaigns (vs. list-based batch sending)
- Building automation rules for when to contact a prospect
- Creating playbooks for SDRs on which events to act on and how
- Setting up n8n, Zapier, or custom workflows that fire outreach on specific triggers

## Framework

### Trigger-Based vs. List-Based Outbound

| Approach | How It Works | Reply Rate | Scalability |
|----------|-------------|------------|-------------|
| **List-based** | Build a list → Write copy → Send to everyone | 2-5% | High volume, lower quality |
| **Trigger-based** | Detect event → Match to angle → Send targeted message | 8-20% | Lower volume, higher quality |
| **Hybrid** | Build qualified list → Wait for trigger → Send signal-matched message | 10-25% | Medium volume, highest quality |

The hybrid approach is the gold standard. You pre-qualify the list (ICP match), then monitor for triggers that tell you WHEN to reach out. This gives you the best of both worlds: targeted copy with perfect timing.

---

### The Trigger Map: 12 Core Business Events

Every trigger needs four components defined: the event, the detection method, the message angle, and the urgency window.

#### Trigger 1: New Funding Round

| Component | Detail |
|-----------|--------|
| **Event** | Company raises Seed, Series A, B, C, or PE investment |
| **Detection** | Crunchbase alerts, TechCrunch, LinkedIn announcements, press releases |
| **Why it matters** | New capital = growth mandate. Board expects 2-3x growth. Sales/marketing investment imminent. |
| **Urgency window** | Contact within 2 weeks of announcement. After 30 days, the signal is stale. |
| **Message angle** | "Post-{{round}}, most teams invest in [your category] within 90 days. Here's what works." |
| **Persona to target** | CEO (Seed), VP Sales/CRO (Series A+), RevOps (Series B+) |

#### Trigger 2: Hiring for Target Role

| Component | Detail |
|-----------|--------|
| **Event** | Company posts job opening for a role your product/service supports |
| **Detection** | LinkedIn Jobs, Indeed, Glassdoor, company careers page, PredictLeads |
| **Why it matters** | Hiring = active investment in that function. They're building the team that needs your solution. |
| **Urgency window** | Contact within 1 week of posting. After 4 weeks, the role may be filled or paused. |
| **Message angle** | "Hiring {{role}} usually means you're building the {{function}} engine. Here's what teams at your stage do first." |
| **Persona to target** | The hiring manager (listed on job post) or their boss |

#### Trigger 3: Leadership Change

| Component | Detail |
|-----------|--------|
| **Event** | New executive hired in your target department (VP Sales, CMO, CRO, etc.) |
| **Detection** | LinkedIn profile changes, press releases, company announcements |
| **Why it matters** | New leaders have a 90-day mandate to make changes. They're evaluating everything, including vendors. |
| **Urgency window** | Contact between day 14-60 of their new role. Too early = they're still onboarding. Too late = they've already decided. |
| **Message angle** | "Most new {{title}}s in the first 90 days need to [outcome you help with]. Here's what we see working." |
| **Persona to target** | The new executive directly |

#### Trigger 4: Tech Stack Change

| Component | Detail |
|-----------|--------|
| **Event** | Company adds, removes, or switches a technology in their stack |
| **Detection** | BuiltWith, Wappalyzer, job description requirements, G2 reviews |
| **Why it matters** | Tech changes indicate a strategic shift. Adjacent purchases often follow. |
| **Urgency window** | Contact within 2 weeks of detection. Stack changes take 3-6 months to settle. |
| **Message angle** | "Teams migrating to {{newTool}} usually also rethink their {{yourCategory}} approach." |
| **Persona to target** | The person who owns the stack (RevOps, VP Sales, CTO depending on category) |

#### Trigger 5: Competitor Churn

| Component | Detail |
|-----------|--------|
| **Event** | Company stops using a competitor's product |
| **Detection** | BuiltWith (tech removal), G2 negative reviews, LinkedIn posts about switching |
| **Why it matters** | They had the need, spent the budget, and are now actively looking for alternatives. |
| **Urgency window** | Immediate. This is the highest-urgency trigger. Contact within 48 hours if possible. |
| **Message angle** | "Teams moving off {{competitor}} typically care most about {{differentiator}}. Here's how we handle that." |
| **Persona to target** | The person who made the original purchase decision |

#### Trigger 6: Product Launch

| Component | Detail |
|-----------|--------|
| **Event** | Company launches a new product, feature, or service |
| **Detection** | Press releases, Product Hunt, company blog, social media |
| **Why it matters** | New products mean new go-to-market motions, new ICPs, and new pipeline needs. |
| **Urgency window** | Contact 1-4 weeks after launch. During launch week, they're too busy. |
| **Message angle** | "New product launches usually mean new audience, new pipeline targets. How's the GTM plan?" |
| **Persona to target** | VP Marketing, VP Sales, or Product Marketing lead |

#### Trigger 7: Earnings/Revenue Event

| Component | Detail |
|-----------|--------|
| **Event** | Missed targets, layoffs, reorgs, or strong growth quarter |
| **Detection** | SEC filings, press releases, Glassdoor, LinkedIn |
| **Why it matters** | Revenue pressure creates urgency. Growth creates opportunity. Both open doors. |
| **Urgency window** | 1-3 weeks after announcement |
| **Message angle (miss)** | "When the board is asking about pipeline, efficiency becomes the priority." |
| **Message angle (growth)** | "Scaling from ${{X}}M to ${{Y}}M usually means outbound becomes a must-have." |

#### Trigger 8: Conference/Event Attendance

| Component | Detail |
|-----------|--------|
| **Event** | Prospect is attending, speaking, or sponsoring a relevant conference |
| **Detection** | Event websites, speaker lists, LinkedIn posts about attending |
| **Why it matters** | They're investing time and money in the topic. They're in learning mode. |
| **Urgency window** | Contact 1-2 weeks BEFORE the event or within 1 week after. |
| **Message angle (before)** | "Ahead of {{event}} — thought you'd want to see this relevant to {{topic}}." |
| **Message angle (after)** | "Hope {{event}} was great. Based on the sessions, you might find this useful." |

#### Trigger 9: Content Publication

| Component | Detail |
|-----------|--------|
| **Event** | Prospect publishes a LinkedIn post, blog article, or podcast episode on a relevant topic |
| **Detection** | LinkedIn feed monitoring, Google Alerts, podcast directories |
| **Why it matters** | They're actively thinking about this topic. Your email arrives in a moment of relevance. |
| **Urgency window** | Within 48 hours of publication. Reference stale content and you look like a stalker, not a peer. |
| **Message angle** | "Your [post/article] about {{topic}} resonated. We're seeing the same pattern across our clients." |

#### Trigger 10: Award or Recognition

| Component | Detail |
|-----------|--------|
| **Event** | Company or individual wins an award, makes a "Top X" list, or receives public recognition |
| **Detection** | Press releases, industry publications, LinkedIn |
| **Why it matters** | Positive momentum. They're growing and feeling good — receptive to investment conversations. |
| **Urgency window** | Within 1-2 weeks. Congratulations expire quickly. |
| **Message angle** | "Congrats on {{award}}. Companies at your trajectory usually need {{what you offer}} next." |

#### Trigger 11: M&A Activity

| Component | Detail |
|-----------|--------|
| **Event** | Company acquires, is acquired, or merges with another company |
| **Detection** | Press releases, SEC filings, Crunchbase, news alerts |
| **Why it matters** | M&A creates chaos and opportunity. Integration needs, new targets, efficiency mandates. |
| **Urgency window** | 30-90 days post-announcement (integration planning phase) |
| **Message angle** | "Post-acquisition teams usually need to consolidate tools and scale faster. Here's what helps." |

#### Trigger 12: Regulatory/Market Change

| Component | Detail |
|-----------|--------|
| **Event** | New regulation, market shift, or industry disruption affects the prospect |
| **Detection** | Industry news, regulatory filings, analyst reports |
| **Why it matters** | External forces create urgency that wasn't there before. "We need to adapt" = buying energy. |
| **Urgency window** | 2-8 weeks after the change is announced |
| **Message angle** | "With {{regulation/change}}, most {{industry}} teams are rethinking {{category}}. Here's what we're seeing." |

---

### Trigger Prioritization Matrix

When multiple triggers fire simultaneously, prioritize by:

| Priority | Trigger Type | Why |
|----------|-------------|-----|
| 1 | Competitor churn | Active buyer, proven budget, immediate need |
| 2 | Hiring for target role | Budget allocated, timeline set |
| 3 | First-party signals (website visit, content download) | Direct engagement with your brand |
| 4 | Leadership change (< 60 days) | Evaluation window open |
| 5 | Funding round (< 30 days) | Capital available, growth mandate |
| 6 | Tech stack change | Strategic shift underway |
| 7 | Content/social signals | Problem is top of mind |
| 8 | Events/conferences | Learning mode, networking mindset |
| 9 | Product launch | New GTM needs |
| 10 | Awards/recognition | Positive momentum |

---

### Building Trigger-Based Campaigns

#### Campaign Architecture

```
TRIGGER CAMPAIGN: {{triggerName}}

Trigger: {{event description}}
Detection: {{how you find out}}
Filter: {{ICP criteria that must also be true}}
Volume estimate: {{expected triggers per month}}

Sequence:
Step 1 (Day 0): Trigger-specific email
Step 2 (Day 3): New value angle (resource, case study)
Step 3 (Day 7): Social proof or different angle
Step 4 (Day 14): Breakup / referral

Personalization requirement:
- Step 1: Must reference the specific trigger + company
- Steps 2-4: Can use bucket personalization

Success metrics:
- Target reply rate: 10-20% (trigger campaigns should beat list-based by 2-3x)
- Target positive reply rate: 5-12%
```

## Templates

### Trigger Map Document
```
# Trigger Map: {{Company/Product Name}}
# Updated: {{date}}

| # | Trigger | Detection Source | Urgency Window | Message Angle | Target Persona | Est. Monthly Volume |
|---|---------|-----------------|----------------|---------------|----------------|---------------------|
| 1 | ___ | ___ | ___ | ___ | ___ | ___ |
| 2 | ___ | ___ | ___ | ___ | ___ | ___ |
| 3 | ___ | ___ | ___ | ___ | ___ | ___ |
```

### Trigger Playbook (For SDR Team)
```
TRIGGER: {{trigger name}}

When you see this:
{{description of the event}}

Do this immediately:
1. Verify the lead passes ICP filter (size, industry, stage)
2. Find the right contact ({{suggested title}})
3. Check if they're already in an active campaign
4. If clear → Add to {{campaign name}} sequence
5. If in existing campaign → Flag for review

Template to use:
Subject: {{subject line template}}
Body: {{body template with variables}}

DON'T:
- {{common mistake 1}}
- {{common mistake 2}}
```

## Tips
- Build trigger campaigns for your top 3 triggers first. Don't try to monitor everything. The Pareto principle applies: 3 triggers will generate 80% of your signal-based pipeline.
- Trigger-based campaigns should always outperform list-based campaigns. If they don't, either your signal detection is lagging (stale triggers) or your message doesn't connect the trigger to your value.
- The urgency window is real. A "congrats on the funding round" email 3 months after the announcement isn't relevant — it's lazy. Set up monitoring so you catch triggers within 48 hours.
- Combine trigger-based outreach with ongoing list-based campaigns. Trigger campaigns are your high-ROI sniper shots. List campaigns are your air cover. You need both.
- Track trigger-to-meeting conversion by trigger type. This data is gold — it tells you exactly which business events create the most pipeline for your specific product.

---

*Progressive disclosure: load trigger automation workflows and integration configs only when building a specific trigger campaign.*
