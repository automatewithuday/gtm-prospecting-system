# Setup & Customization Checklist

## 1. Trigger setup

Fires from a **CRM deal-stage trigger** — the deal moving to Closed Won
(e.g. a HubSpot workflow trigger on stage change). Keep the trigger minimal:
pass the deal payload and load this skill.

- [ ] Trigger fires **once** per deal reaching Closed Won (guard against
      stage flapping — a deal moved out of and back into Closed Won should
      not run the play twice; check for the `closed-won-replication` tag or
      the review task from a prior run).
- [ ] The payload includes the deal, associated company, and contacts.

## 2. Placeholders

- [ ] `{{CRM}}`, `{{LOOKALIKE_COUNT}}`, `{{REVIEW_SURFACE}}` filled.
- [ ] Company-search / employee-search / enrichment tools connected — Steps
      2–3 depend on them.

## 3. Policy decisions

- [ ] **Human review before send** is the core safety of this play — drafts
      go to a batch review task, nothing sends automatically. Keep it.
- [ ] **Anonymized win references** — decide whether your customer
      contracts even allow anonymized case references; some logos require
      written consent for any reference, including anonymized. If in doubt,
      have legal bless the template phrasing.
- [ ] Opt-out/suppression list checked before drafting (Exit Conditions) —
      wire in your actual suppression source.

## 4. Behavioral invariants (do not remove)

- Never name the won customer, and never expose the replication mechanism
  ("we found you because X bought") in outreach.
- Lookalikes must be net-new to the CRM; existing customers/pipeline are
  skipped and replaced.
- Broaden search criteria one at a time; a short list is flagged, never
  silently padded with weak fits.
- One batch review task per win — not one task per lookalike.
