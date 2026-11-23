---
doc_id: "INT-SOP-ERASE-001"
title: "Erasure Request Handling Procedure (superseded v2.0)"
company: "Acme Corp"
publisher: "ACME"
access_level: 1
classification: "internal"
doc_type: "sop"
profile: "company_doc"
topic: "erasure"
topics: ["erasure"]
owner: "Privacy Operations"
approver: "Head of Privacy Operations"
version: "2.0"
effective_date: "2024-09-01"
status: "superseded"
gdpr_articles: [12, 17]
related: []
generator: {"writer": "@cf/zai-org/glm-5.3", "judge": "@cf/openai/gpt-oss-120b", "run_id": "20261124-025027", "prompt_hash": "284162f9dd75"}
review: {"status": "ok", "attempts": 1, "issues_left": 0, "scores": {"fact_fidelity": 5, "tier_discipline": 5, "gdpr_accuracy": 5, "realism": 5, "retrievability": 5}}
---

# Erasure Request Handling Procedure (superseded v2.0)

| Field | Value |
|---|---|
| Document ID | INT-SOP-ERASE-001 |
| Version | 2.0 |
| Owner | Privacy Operations |
| Approver | Mara Okafor, Head of Privacy Operations |
| Effective date | 2024-09-01 |
| Classification | INTERNAL |
| Status | SUPERSEDED — replaced by INT-SOP-ERASE-002 on 2026-03-01 |
| Audience | Privacy Operations team |
| GDPR articles in scope | Art. 12, Art. 17 |

> **Superseded document notice:** This version (v2.0) of the Erasure Request Handling Procedure was superseded on 2026-03-01 by INT-SOP-ERASE-002. It is retained for reference and audit purposes only and must not be used to handle live erasure requests. Requests received on or after 2026-03-01 are handled under the current procedure.

## 1. Purpose and Scope

This Standard Operating Procedure (SOP) governs how the Privacy Operations team at Acme Corp handles data-subject erasure requests under Article 17 GDPR. It covers erasure requests received from any individual whose personal data Acme processes as a controller, including customers of the Acme Beacon platform, website visitors, marketing contacts, and Acme employees.

Requests may arrive through two intake routes: the shared mailbox privacy@acme.example, or the self-service Beacon Settings > Privacy page, where account holders can delete their own account data. Both routes are in scope of this procedure.

Acme's privacy notice commits to responding to deletion requests within one month of receipt, as required by Article 12(3) GDPR. Internally, Privacy Operations applies a stricter service level: erasure requests must be completed within 30 calendar days from receipt. This SOP defines the steps, roles and records needed to meet that deadline consistently.

## 2. Roles and Responsibilities

The following RACI table assigns accountability for erasure request handling under this procedure. "R" = Responsible, "A" = Accountable, "C" = Consulted, "I" = Informed.

| Activity | Privacy Operations analysts (3, under Mara Okafor) | Mara Okafor, Head of Privacy Operations | Tomás Reyes, DPO | Lena Fischer, VP Engineering | Data Platform team |
|---|---|---|---|---|---|
| Intake and logging of erasure requests | R/A | A | I | – | – |
| Identity verification (email reply) | R | A | C | – | – |
| Art. 12(6) identity-verification decisions | C | C | R/A | – | – |
| Art. 17(3) exception review and refusals | C | C | R/A | – | – |
| Deletion execution (Beacon, Ledger, Atlas, HelpHub) | R/A | A | I | – | C |
| Atlas deletion job manual re-runs | I | I | – | C | R/A |
| Day-14 SLA escalation | R | A | I | – | – |
| Day-20 SLA breach reporting (weekly) | R | A | I | I | – |

### 2.1 Notes on assignments

- Identity verification is performed by Privacy Operations analysts. Requests where identity cannot be confirmed within 5 business days are escalated to Tomás Reyes, DPO, for a decision under Article 12(6) GDPR.
- Tickets breaching day 14 of the 30-day SLA are escalated to the Privacy Operations lead. Breaches of day 20 are reported weekly to the DPO and to Lena Fischer (VP Engineering) for system-level causes.
- The Atlas deletion job has a known defect: it fails on records with more than 500 linked event rows. The Data Platform team performs manual re-runs, which adds an average of 6 days to affected tickets. Privacy Operations analysts must flag affected tickets to the Data Platform team on detection.

## 3. Request Intake and Logging

Erasure requests reach Privacy Operations through two intake routes: the shared mailbox privacy@acme.example, or the self-service Beacon Settings > Privacy page, where account holders can delete their own account data directly. The Privacy Operations analyst on duty performs the following steps on the day of receipt:

1. Check the privacy@acme.example shared mailbox at least twice daily (morning and end of day) for new erasure requests.
2. For each request received by email, log the request in the DSR register with: date of receipt, requester account ID, and the systems to be checked (Beacon, Ledger, Atlas, HelpHub).
3. For requests originating from a Beacon Settings > Privacy self-service deletion, verify the corresponding account record and log the same register fields, recording the self-service route as the intake channel.
4. Acknowledge receipt to the requester by email reply from privacy@acme.example, confirming that the request has been received and stating the 30-calendar-day internal service level.
5. Flag any request missing the requester's account ID back to the requester as part of the acknowledgement, so identity verification (Section 4) can proceed without delay.

The date of receipt recorded in step 2 starts the 30-calendar-day clock for the request.

## 4. Identity Verification

Under this procedure, identity verification is performed by email reply only. The Privacy Operations analyst assigned to the request performs the following steps:

1. Reply to the requesting email address from privacy@acme.example, asking the requester to confirm their account details from the same address used to submit the request.
2. Treat the request as verified only when the requester replies from the original requesting address and the confirmed account details match the account record in Beacon.
3. Where reasonable doubts about identity persist after the email exchange, request additional information to confirm the identity of the requester, consistent with Article 12(6) GDPR and as described in Acme's privacy notice.
4. Record the verification outcome and date on the request in the DSR register.

Only verified requests start the 30-calendar-day internal SLA clock; unverified requests do not.

Requests where identity cannot be confirmed within 5 business days of receipt are escalated to Tomás Reyes, Data Protection Officer, for a decision under Article 12(6) GDPR. The DPO's decision — to verify, to request further information, or to refuse the request — is recorded on the request before any further processing steps are taken.

Identity verification is performed by the three Privacy Operations analysts under Mara Okafor, Head of Privacy Operations.

## 5. Erasure Execution

For verified erasure requests, the assigned Privacy Operations analyst triggers deletion jobs in four systems, in the following order:

1. **Beacon** — Delete account and profile data within 3 days of verification.
2. **Ledger** — Flag billing records for legal-exception review (see Section 5.2). Records not covered by an exception are deleted.
3. **Atlas** — Delete event and billing history via the Atlas deletion job. The job runs nightly; the analyst confirms successful completion on the next business day.
4. **HelpHub** — Delete support tickets within 5 days of verification.

The analyst records the completion date of each deletion job on the request in the DSR register.

### 5.1 Atlas deletion job defect

The Atlas deletion job has a known defect: it fails on records with more than 500 linked event rows. When a failure is detected, the analyst must immediately flag the ticket to the Data Platform team, which performs a manual re-run. Manual re-runs add an average of 6 days to affected tickets; the analyst records the delay and reason on the request and factors it into SLA monitoring (Section 2.1).

### 5.2 Article 17(3) exception checklist

Before executing erasure in any system, the analyst applies the exception checklist INT-CHK-ERASE:

- **Tax retention (Art. 17(3)(b))** — Ledger invoices are retained for 6 years to comply with Irish tax law. These records are excluded from deletion and marked as retained in the DSR register.
- **Legal hold (Art. 17(3)(e))** — Data subject to a legal hold is excluded from erasure, as it is necessary for the establishment, exercise or defence of legal claims.

Where erasure is refused in whole or in part under an exception, the analyst informs the data subject of the reasons for the refusal, and of their right to lodge a complaint with a supervisory authority and to seek a judicial remedy, within one month of receipt of the request, in accordance with Article 12(4) GDPR. The partial refusal is recorded on the request in the DSR register.

## 6. Third-Party Recipient Notification

Where personal data has been disclosed to other recipients and is erased at the data subject's request, Acme notifies each recipient of the erasure, in line with Article 19 GDPR, unless this is impossible or would involve disproportionate effort, as described in Acme's privacy notice.

For verified erasure requests, the assigned Privacy Operations analyst sends notification within 10 calendar days of execution of the deletions in Section 5, using notification template INT-TPL-19, to:

1. **Stripe** — payer data.
2. **Any sub-processors** listed in the current sub-processor register.

The analyst records on the request in the DSR register the recipients notified, the notification date, and any recipient for whom notification was not performed, with the reason (impossibility or disproportionate effort).

Where a data subject asks which recipients were notified, the analyst informs the data subject of those recipients on request, in accordance with Article 19 GDPR.

## 7. SLA Management, Extensions and Escalation

Under this procedure, Privacy Operations applies an internal SLA of 30 calendar days from identity verification to complete erasure of the request. This sits within the one-month statutory deadline in Article 12(3) GDPR, to which Acme's privacy notice commits.

The assigned Privacy Operations analyst monitors every open request against the 30-day clock and records the current day count on the request in the DSR register at each status update.

**Escalation.** Tickets breaching day 14 of the 30-day SLA are escalated to the Privacy Operations lead. Breaches of day 20 are reported weekly to Tomás Reyes, DPO, and to Lena Fischer, VP Engineering, for investigation of system-level causes.

**Extensions.** Where a request is complex or numerous, the one-month response period may be extended by up to two further months, as provided by Article 12(3) GDPR and described in Acme's privacy notice. Before any extension is applied:

1. The analyst records on the request the complexity or volume reasons justifying the extension.
2. The data subject is informed of the extension and its reasons within one month of receipt of the request.
3. The extension decision is approved by the Privacy Operations lead and noted in the DSR register.

Extensions must not be used to accommodate avoidable internal delays, including Atlas deletion job failures (Section 5.1).

## 8. Records and Quality Checks

The assigned Privacy Operations analyst completes the following records checklist for every erasure request:

- [ ] Intake log entry (date of receipt, account ID, intake channel, systems to be checked)
- [ ] Identity verification correspondence and outcome (Section 4)
- [ ] Execution evidence per system: completion dates for Beacon, Ledger, Atlas and HelpHub deletions
- [ ] Article 17(3) exception decisions, including any refusal notified to the data subject under Article 12(4) GDPR (e.g. legal-hold exclusions or refusals for the establishment, exercise or defence of legal claims)
- [ ] Third-party notifications sent under Article 19 GDPR using template INT-TPL-19, with recipients and dates

These records are kept in the DSR register for no longer than necessary for demonstrating compliance with erasure obligations, consistent with the storage-limitation principle in Article 5(1)(e) GDPR, and enable Acme to demonstrate compliance under the accountability principle in Article 5(2) GDPR.

The Privacy Operations lead reviews all open tickets weekly, checking record completeness and day counts against the 30-day SLA.

## 9. Exceptions and Document Status

### 9.1 Refusals under Article 17(3) GDPR

Erasure requests may be refused in whole or in part where an exception under Article 17(3) GDPR applies — for example, where data must be kept to comply with a legal obligation (Art. 17(3)(b), such as the 6-year Ledger invoice retention for Irish tax law) or for the establishment, exercise or defence of legal claims (Art. 17(3)(e)). Any refusal must be explained to the requester, together with their right to lodge a complaint with a supervisory authority and to seek a judicial remedy, within one month of receipt, in accordance with Article 12(4) GDPR. All refusal decisions are recorded in the DSR register (see Sections 5.2 and 8).

### 9.2 Superseded status

This document (INT-SOP-ERASE-001, v2.0) is **SUPERSEDED**. It was replaced by INT-SOP-ERASE-002, effective 2026-03-01, and must not be used to handle live erasure requests on or after that date. It is retained for reference and audit purposes only.
