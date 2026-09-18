# Closed-won replication play

## Template placeholders

Replace every `{{...}}` before enabling. See the [setup checklist](references/closed-won-setup-checklist.md) for the full setup list.

- `{{CRM}}` — Your CRM (e.g. HubSpot) — source of the closed-won event and target of writes
- `{{LOOKALIKE_COUNT}}` — Lookalikes per win (default: 5)
- `{{REVIEW_SURFACE}}` — Where the batch review task is created (e.g. your desk/task queue)

## Purpose

Every closed-won deal is a targeting signal. The moment a deal closes, use
the winning company's profile to find {{LOOKALIKE_COUNT}} lookalike
companies and draft outreach while the story is fresh. The rep reviews and
approves before anything sends.

---

## Input

You receive a {{CRM}} deal that just moved to Closed Won. The payload
includes the deal record and its associated company/contact.

---

## Step 1 — Extract the Win Profile

From the {{CRM}} deal and its associated company, extract:

- **Industry / vertical**
- **Company size** (headcount range)
- **Geography** (country/region)
- **Tech stack** (if available — look for CRM, marketing tools, data tools)
- **Go-to-market model** (B2B SaaS, services, marketplace, etc.)
- **Use case / pain point** that drove the purchase (check deal notes and
  contact activity in {{CRM}})
- **Deal owner** (the {{CRM}} user who owns the deal — you'll need their
  name and email for later)

If a field is missing or unclear, make a reasonable inference based on
what's available. Don't block on incomplete data.

---

## Step 2 — Build the Lookalike Search Profile

Construct a specific search profile. Good example: "B2B SaaS, 50–200
employees, US-based, uses Salesforce, scaling a GTM team." Generic is weak —
be specific.

Use the extracted attributes to run a company search. Look for companies
that:

- Match the industry and company size
- Are in the same geography or equivalent market
- Share a similar GTM model or tech stack when inferable
- Are NOT already in {{CRM}} (not a customer, not active pipeline, not a
  contact record's company)

Find **exactly {{LOOKALIKE_COUNT}}** qualifying lookalike companies. If
you're having trouble hitting the count, broaden one criterion at a time
(geography first, then size range). If you still can't after broadening,
proceed with however many you found and flag the count in the review task.

---

## Step 3 — Research Each Lookalike

For each company:

1. Confirm ICP fit — does this company actually look like the kind of
   company you sell to?
2. Identify the right contact: same persona as the champion in the won deal
   (e.g., if the deal champion was a VP of Sales, find the VP of Sales at
   this company). Use employee search tools.
3. Enrich the contact — find LinkedIn URL and email if possible.
4. Note one specific, relevant detail about the company or contact that can
   be used to personalize outreach.

---

## Step 4 — Draft Outreach

Draft one outreach message per company.

**Rules:**

- **Sender:** The deal owner (whoever owns the closed-won deal in {{CRM}}).
  Use their name and voice.
- **Channel:** LinkedIn preferred. Fall back to email if LinkedIn is not
  available.
- **Win reference: ALWAYS anonymized.** Never name the customer. Reference
  by industry/profile only. Example: "We just helped a B2B SaaS company
  scaling their outbound motion do X."
- **Tone:** Casual and direct. Peer-to-peer. Not a vendor pitch. Reference
  something specific about their company or role to show genuine relevance.
- **CTA:** Soft — open a conversation, not close a deal. "Thought this
  might be relevant — happy to share more if useful."
- **Length:** Keep it short. 3–5 sentences max for LinkedIn. Email can be
  slightly longer but still tight.

Do NOT mention that you found them because of another customer win. The win
informs your angle; don't expose the mechanism.

---

## Step 5 — CRM Updates

For each new lookalike company and contact found:

1. Check if the company already exists in {{CRM}}. If yes, skip adding it
   (but still draft outreach if there's no active deal).
2. If net new: create the company in {{CRM}} with source noted as
   "Closed-Won Replication" and a note referencing which deal triggered
   this.
3. Create or associate the contact in {{CRM}}, linked to their company.
4. Tag each company in your workspace with `closed-won-replication` and
   `lookalike-[winning-company-domain]`.

---

## Step 6 — Create Review Task

Create a single batch review item on {{REVIEW_SURFACE}} for the deal owner.
Include:

**Title:** `Closed-Won Lookalike Outreach — [Winning Company Name]`

**Body:**

- Summary of the win profile used (2–3 bullet points)
- Table of lookalike companies: Company name | Contact name + title |
  LinkedIn/email | Matching attributes | Outreach draft
- Note any companies skipped (already in CRM) and replacements found
- Flag if fewer than {{LOOKALIKE_COUNT}} matches were found

Notify the deal owner via Slack DM or email. Tell them they have a batch of
lookalike outreach drafts ready to review based on their latest win.

---

## Exit Conditions

- **Company already in CRM as customer or active deal** → skip, find a
  replacement
- **Fewer than 3 lookalikes found after broadening** → create the task
  anyway, flag the low count, and suggest the rep manually identify
  additional targets
- **Contact at a lookalike is opted out or suppressed** → skip that
  contact, find another at the same company
- **Deal has no associated company** → log a note on the deal and skip the
  play

---

## Configuration (set at trigger level, reference here)

- Always use anonymized win references (no customer naming)
- Outreach always sent from the deal owner
- Find exactly {{LOOKALIKE_COUNT}} lookalike companies per triggered deal

---

## What good looks like

A great run produces one review task the rep can approve in five minutes: the full count of true lookalikes — companies that resemble the win across industry, size, motion, and stack, not just the same vertical — each net-new to the CRM, each with the right persona contact enriched and one genuinely specific personalization detail, and drafts that read like the rep wrote them: anonymized win reference, soft CTA, no hint of the replication mechanism.

Mediocre looks like: generic same-industry logos, contacts at the wrong seniority, drafts that name the customer or read like a vendor pitch, a padded list instead of a flagged short one, or one task per company instead of a single batch.
