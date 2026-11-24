---
doc_id: "INT-RUN-ERASE-001"
title: "Erasure Execution Runbook (per system)"
company: "Acme Corp"
publisher: "ACME"
access_level: 1
classification: "internal"
doc_type: "runbook"
profile: "company_doc"
topic: "erasure"
topics: ["erasure"]
owner: "Privacy Operations & Engineering"
approver: "VP Engineering"
version: "2.4"
effective_date: "2026-03-15"
status: "current"
gdpr_articles: [17]
related: ["INT-SOP-ERASE-002"]
generator: {"writer": "@cf/zai-org/glm-5.3", "judge": "@cf/openai/gpt-oss-120b", "run_id": "20261124-025609", "prompt_hash": "284162f9dd75"}
review: {"status": "ok", "attempts": 1, "issues_left": 0, "scores": {"fact_fidelity": 5, "tier_discipline": 5, "gdpr_accuracy": 5, "realism": 5, "retrievability": 5}}
---

# Erasure Execution Runbook (per system)

| Field | Value |
|---|---|
| Document ID | INT-RUN-ERASE-001 |
| Version | 2.4 |
| Owner | Privacy Operations & Engineering |
| Approver | Lena Fischer, VP Engineering |
| Effective date | 2026-03-15 |
| Classification | INTERNAL |
| Status | Current |

**Audience:** Privacy Operations engineers
**GDPR articles in scope:** Article 17 (right to erasure), with supporting references to Articles 12(3), 12(4), 12(6), 17(3), and 19 as they arise during execution
**Parent procedure:** INT-SOP-ERASE-002 v3.1 (Erasure Request Handling Procedure) — this runbook provides the per-system execution detail for that procedure
**Related queue:** PrivacyDesk INT-Q-ERASE
**Contact:** privacy@acme.example

## 1. Document Control and Purpose

| Field | Value |
|---|---|
| Document ID | INT-RUN-ERASE-001 |
| Version | 2.4 |
| Owner | Privacy Operations & Engineering |
| Approver | Lena Fischer, VP Engineering |
| Effective date | 2026-03-15 |
| Classification | INTERNAL |
| Status | Current |

### 1.1 Purpose

This runbook gives Privacy Operations engineers step-by-step, per-system execution instructions for erasing personal data in response to verified GDPR Article 17 erasure requests. It covers the ordered deletion jobs across Beacon, Ledger, Atlas and HelpHub, Article 17(3) exception handling, Article 19 recipient notification, and Vault backup expiry tracking.

### 1.2 Scope

This runbook is limited to execution after identity verification has been completed and the request has been logged in the PrivacyDesk queue INT-Q-ERASE. It does not cover intake, identity verification, or end-to-end request handling; for those, follow the parent procedure INT-SOP-ERASE-002 (Erasure Request Handling Procedure), v3.1.

### 1.3 Audience

Privacy Operations engineers who execute deletion jobs and update INT-Q-ERASE tickets.

### 1.4 Deadlines and SLA

Acme's privacy notice commits to responding to erasure requests within one month of receipt, as required by Article 12(3) GDPR; where a request is complex or numerous, that period may be extended by two further months, with the data subject informed of the extension and its reasons within one month. Internally, Privacy Operations operates a stricter SLA: erasure must be complete within 20 calendar days from identity verification. The 20-day SLA starts only once the requester's identity has been verified per INT-SOP-ERASE-002.

## 2. Roles, Intake and Preconditions

### 2.1 Intake channels

Erasure requests reach Privacy Operations through two channels: the mailbox privacy@acme.example and the self-service Beacon Settings > Privacy page, where account holders can delete their own account data. All requests, regardless of channel, are logged in the PrivacyDesk queue INT-Q-ERASE before any execution work begins.

### 2.2 Intake form INT-FORM-03

Every request must be completed against intake form INT-FORM-03, which captures:

- the requester's account ID;
- the systems to be checked (Beacon, Ledger, Atlas, HelpHub);
- identity evidence supporting the verification step.

Requests missing any of these fields are returned to the requester for completion before verification starts.

### 2.3 Identity verification

Identity verification is performed by Mara Okafor's Privacy Operations team (three analysts), following the principles in EDPB Guidelines 01/2022. Where Acme has reasonable doubts about the requester's identity, additional information may be requested to confirm it, consistent with Article 12(6) GDPR.

Only verified requests start the 20-calendar-day internal SLA. The verification date, not the intake date, is the SLA start date recorded on the INT-Q-ERASE ticket.

If identity cannot be confirmed within 5 business days of intake, the analyst escalates the request to the DPO, Tomás Reyes, for a decision under Article 12(6) GDPR. The escalation note must be added to the ticket and the SLA clock remains unstarted pending the DPO's decision.

### 2.4 RACI for erasure execution

| System / activity | Responsible | Accountable | Consulted | Informed |
|---|---|---|---|---|
| Identity verification (INT-FORM-03) | Privacy Operations analyst (Mara Okafor's team) | Mara Okafor, Head of Privacy Operations | Tomás Reyes, DPO (Art. 12(6) escalations) | — |
| Beacon — account and profile data | Privacy Operations engineer | Privacy Operations lead | Beacon engineering | Mara Okafor |
| Ledger — billing records (legal-exception review) | Privacy Operations engineer | Privacy Operations lead | Aoife Brennan, Senior Privacy Counsel | Mara Okafor |
| Atlas — event and billing history | Data Platform team | Privacy Operations lead | Privacy Operations engineer | Mara Okafor |
| HelpHub — support tickets | Privacy Operations engineer | Privacy Operations lead | Owen Gallagher, Customer Support | Mara Okafor |
| Vault backup expiry tracking | Privacy Operations engineer | Privacy Operations lead | — | Mara Okafor |

### 2.5 Preconditions before execution

Before running any deletion job, the executing engineer confirms on the INT-Q-ERASE ticket that:

- [ ] Identity verification is complete and the verification date is recorded (SLA start).
- [ ] INT-FORM-03 is fully populated (account ID, systems to check, identity evidence).
- [ ] The Article 17(3) exception checklist INT-CHK-ERASE has been completed (see section 3).
- [ ] No legal hold applies to the requester's data.

If any precondition fails, execution does not start; the ticket is escalated per section 6.

## 3. Per-System Erasure Execution Procedure

Once the preconditions in section 2.5 are met, the executing engineer runs the deletion jobs in the fixed order below. The order matters: Beacon first (removes the live account and profile data), then Ledger, Atlas, and HelpHub. Each completed step is recorded on the INT-Q-ERASE ticket with a timestamp. All deadlines below run from the identity verification date (the SLA start), not the intake date.

### 3.1 Beacon — account and profile data (within 3 days)

Beacon deletion removes the requester's account and profile data from the customer-facing product. This job must complete within 3 calendar days of identity verification.

Steps:

1. Open the INT-Q-ERASE ticket and confirm the account ID from INT-FORM-03 matches the Beacon account.
2. Trigger the Beacon account and profile deletion job against the verified account ID.
3. Confirm the job completed and the account and profile data are no longer retrievable in Beacon.
4. Record the completion timestamp on the ticket.

Checklist:

- [ ] Beacon deletion job executed against the verified account ID.
- [ ] Account and profile data confirmed deleted in Beacon.
- [ ] Completion timestamp recorded on the INT-Q-ERASE ticket.

### 3.2 Ledger — billing records (flagged for legal-exception review)

Ledger holds billing and invoicing records. These are not deleted outright: they are flagged for legal-exception review, because Ledger invoices are retained 6 years for Irish tax law under the Article 17(3)(b) exception, and data subject to a legal hold is excluded (see INT-CHK-ERASE).

Steps:

1. Flag the requester's Ledger billing records for legal-exception review.
2. Route the flagged records to Aoife Brennan, Senior Privacy Counsel, for exception determination.
3. Where the Article 17(3)(b) tax-law retention or a legal hold applies, retain the records and record the exception on the ticket; the data subject is informed of the refusal and its reasons under Article 12(4) GDPR within one month.
4. Where no exception applies, delete the flagged records and record the completion timestamp.

Checklist:

- [ ] Ledger billing records flagged for legal-exception review.
- [ ] Legal-exception determination recorded (retain under Art. 17(3) or delete).
- [ ] Where refused, Art. 12(4) notification to the data subject scheduled within one month.
- [ ] Ticket updated with the outcome and timestamp.

### 3.3 Atlas — event and billing history (nightly deletion job)

Atlas holds event and billing history and is erased via the Atlas deletion job, which runs nightly. The executing engineer queues the deletion and monitors it to completion.

Known defect: the Atlas deletion job fails on records with more than 500 linked event rows. Failed jobs require manual re-runs by the Data Platform team, which adds an average of 6 days to affected tickets. Engineers must therefore check row counts at queue time and, where the >500-row threshold is likely, notify the Data Platform team immediately and set the ticket SLA clock accordingly (see section 6 escalation).

Steps:

1. Queue the Atlas deletion job for the verified account ID (the job runs on the next nightly run).
2. Check the linked event row count; if it exceeds 500 linked event rows, raise a manual re-run request with the Data Platform team at queue time, not after failure.
3. Confirm the nightly job completed successfully.
4. If the job failed on the >500-row defect, confirm the Data Platform team has re-run it and record the completion date, noting the expected ~6-day delay on the ticket.

Checklist:

- [ ] Atlas deletion job queued for the verified account ID.
- [ ] Linked event row count checked against the 500-row threshold.
- [ ] Data Platform manual re-run requested where the threshold is exceeded.
- [ ] Job completion (automated or manual re-run) confirmed and timestamped on the ticket.

### 3.4 HelpHub — support tickets (within 5 days)

HelpHub holds the requester's support tickets. Deletion must complete within 5 calendar days of identity verification.

Steps:

1. Identify all HelpHub support tickets associated with the verified account ID.
2. Delete the requester's personal data from those support tickets.
3. Confirm deletion in HelpHub and record the completion timestamp on the ticket.

Checklist:

- [ ] All HelpHub support tickets for the account ID identified.
- [ ] Requester's personal data deleted from those tickets.
- [ ] Completion timestamp recorded on the INT-Q-ERASE ticket.

### 3.5 Summary table — system, action, deadline

| Order | System | Action | Deadline (from verification) |
|---|---|---|---|
| 1 | Beacon | Delete account and profile data | Within 3 calendar days |
| 2 | Ledger | Flag billing records for legal-exception review; delete only where no Art. 17(3) exception applies | Reviewed before ticket closure |
| 3 | Atlas | Delete event and billing history via the nightly Atlas deletion job (manual Data Platform re-run where >500 linked event rows) | Complete within the 20-day SLA; expect ~6-day average delay on affected records |
| 4 | HelpHub | Delete requester's personal data from support tickets | Within 5 calendar days |

All four systems must be complete within the 20-calendar-day internal SLA from identity verification. Tickets at day 14 escalate to the Privacy Operations lead; day-20 breaches are reported weekly to the DPO, Tomás Reyes, and to Lena Fischer, VP Engineering, for system-level causes (see section 6).

## 4. Article 17(3) Exception Handling

Erasure requests may be refused in whole or in part where an exception under Article 17(3) GDPR applies, for example where data must be kept to comply with a legal obligation or for the establishment, exercise or defence of legal claims. At Acme, exception handling is driven by the exception checklist INT-CHK-ERASE, which the executing engineer completes before any deletion job runs (section 2.5).

### 4.1 Applicable exceptions

| Exception | Basis | Data affected | Action |
|---|---|---|---|
| Irish tax law retention | Art. 17(3)(b) — compliance with a legal obligation | Ledger invoices | Retained 6 years; not deleted |
| Legal hold | Art. 17(3)(e) — establishment, exercise or defence of legal claims | Any system data subject to a hold | Excluded from erasure |

### 4.2 Procedure

1. Complete checklist INT-CHK-ERASE for the verified account ID before executing deletion jobs.
2. Where the Art. 17(3)(b) tax-law exception applies, retain the Ledger invoices for the 6-year retention period and record the exception on the INT-Q-ERASE ticket.
3. Where data is subject to a legal hold under Art. 17(3)(e), exclude it from erasure and record the exclusion on the ticket.
4. Erase all remaining personal data not covered by an exception, per section 3.

Checklist:

- [ ] INT-CHK-ERASE completed for the account ID.
- [ ] Ledger invoices retained 6 years under Art. 17(3)(b) where applicable.
- [ ] Legal-hold data excluded under Art. 17(3)(e) where applicable.
- [ ] Exceptions and their bases recorded on the INT-Q-ERASE ticket.

### 4.3 Informing the data subject of a refusal

Where erasure is refused in whole or in part, the data subject must be informed of the refusal and the reasons for it under Article 12(4) GDPR within one month of receipt of the request. The notification must also state the data subject's right to lodge a complaint with a supervisory authority and to seek a judicial remedy. The engineer records the date the refusal notification was sent on the INT-Q-ERASE ticket before closure.

## 5. Recipient Notification under Article 19

Where personal data has been disclosed to other recipients and is erased at the data subject's request, Acme notifies each recipient of the erasure, unless notification is impossible or involves disproportionate effort, in line with Article 19 GDPR.

### 5.1 Recipients to notify

For every verified erasure request executed under section 3, the executing engineer sends Article 19 notifications within 10 calendar days of execution to:

| Recipient | Data category |
|---|---|
| Stripe | Payer data |
| All sub-processors listed in the current sub-processor register | Personal data disclosed to them for the affected account |

### 5.2 Procedure

1. Confirm all deletion jobs under section 3 have completed (or exceptions recorded under section 4) before notifying recipients.
2. Generate the notification from template INT-TPL-19 for each recipient.
3. Send the notification within 10 calendar days of the erasure execution date.
4. Record each notification, its recipient and its send date on the INT-Q-ERASE ticket before closure.

### 5.3 Checklist

- [ ] Stripe notified (payer data) using INT-TPL-19.
- [ ] Every sub-processor in the current sub-processor register notified using INT-TPL-19.
- [ ] All notifications sent within 10 calendar days of execution.
- [ ] Recipients and send dates recorded on the INT-Q-ERASE ticket.

Where notification is impossible or would involve disproportionate effort, record the justification on the ticket; the data subject may be informed of the recipients on request, per Article 19.

## 6. Vault Backup Expiry Handling

Vault is Acme's immutable backup system: backups are write-once and retained 35 days. Erasure cannot be executed inside Vault, so deleted data is removed from Vault only when each backup expires. Expiry propagates deletion automatically; no manual deletion action is possible or required in Vault.

### 6.1 Procedure

1. After all deletion jobs in section 3 are complete, identify the Vault backup generations that still contain the requester's personal data.
2. Record the latest relevant backup expiry date on the INT-Q-ERASE ticket.
3. Do not close the ticket at execution; the ticket remains open until expiry is confirmed.
4. Confirm, on or after the recorded expiry date, that the backups containing the requester's data have expired and the deletion has propagated automatically.
5. Record the expiry confirmation date on the ticket and close the ticket.

### 6.2 Checklist

- [ ] Backup generations containing the requester's data identified.
- [ ] Expiry date recorded on the INT-Q-ERASE ticket.
- [ ] Expiry confirmed after the 35-day retention period elapsed.
- [ ] Automatic propagation of the deletion verified.
- [ ] Ticket closed only after expiry confirmation, with the confirmation date recorded.

### 6.3 Notes

The 35-day Vault retention period is a property of the write-once backup architecture, not an erasure refusal; it does not trigger the Article 17(3) exception handling in section 4. However, because expiry can extend beyond the 20-calendar-day internal SLA from identity verification, engineers must record the expected expiry date on the ticket at execution time so that any day-14 escalation to the Privacy Operations lead (section 6 of the parent procedure) reflects the correct cause.

## 7. SLA Monitoring, Escalation and Records

### 7.1 Ticket logging and SLA tracking

Every erasure request is logged in the PrivacyDesk queue INT-Q-ERASE. The 20-calendar-day internal SLA (stricter than the one-month statutory deadline in Article 12(3) GDPR) runs from the identity verification date recorded on the ticket. Engineers must keep ticket timestamps current so that day-14 and day-20 monitoring is accurate.

### 7.2 Escalation

| Trigger | Action | Recipient |
|---|---|---|
| Day 14 of the 20-day SLA | Escalate the ticket | Privacy Operations lead |
| Day 20 (SLA breach) | Report the breach weekly | Tomás Reyes (DPO) and Lena Fischer (VP Engineering), for system-level causes |
| Atlas >500-linked-event-row defect | Flag the delay for engineering follow-up | Data Platform team, via the Privacy Operations lead |

Atlas deletion job failures on records with more than 500 linked event rows add an average of 6 days to affected tickets. Engineers must flag these delays on the ticket for engineering follow-up so that repeated occurrences are visible in the weekly day-20 breach report.

### 7.3 Extension for complex requests

Where a request is complex or numerous, the one-month response period may be extended by two further months under Article 12(3) GDPR. The data subject must be informed of the extension and its reasons within one month. Any extension decision is recorded on the INT-Q-ERASE ticket with its justification.

### 7.4 Records retained per ticket

- [ ] INT-FORM-03 (account ID, systems checked, identity evidence).
- [ ] Identity verification date (SLA start) and any Art. 12(6) escalation.
- [ ] Completed INT-CHK-ERASE checklist and any Art. 17(3) exceptions.
- [ ] Deletion job timestamps for Beacon, Ledger, Atlas and HelpHub.
- [ ] Art. 12(4) refusal notifications, where applicable.
- [ ] Art. 19 recipient notifications (recipients and send dates).
- [ ] Vault backup expiry date and expiry confirmation.
- [ ] Any Art. 12(3) extension and justification.

## 8. Exceptions and Related Documents

### 8.1 Deviations from this runbook

Any deviation from the steps, deadlines or order of operations in this runbook requires prior approval from the DPO, Tomás Reyes. The engineer requesting the deviation must record the DPO's approval, the reason for the deviation and the alternative action taken on the INT-Q-ERASE ticket before proceeding. Deviations affecting the 20-calendar-day internal SLA (F-ERA-07) must also be noted in the weekly day-20 breach report to the DPO and Lena Fischer, VP Engineering (see section 7.2).

Deviations are permitted only where this runbook cannot be followed as written; the internal 20-day SLA itself is never waived by a deviation and remains stricter than the one-month statutory deadline in Article 12(3) GDPR.

### 8.2 Related documents

| Document | Version | Relationship |
|---|---|---|
| INT-SOP-ERASE-002 — Erasure Request Handling Procedure | 3.1 | Governing end-to-end procedure for erasure requests; this runbook provides the per-system execution detail for it |
| INT-FORM-03 — DSR intake form | — | Captures account ID, systems to check and identity evidence |
| INT-CHK-ERASE — Article 17(3) exception checklist | — | Completed before execution (section 2.5) |
| INT-TPL-19 — Article 19 notification template | — | Used for recipient notifications (section 5) |

For intake, identity verification and end-to-end request handling not covered here, follow INT-SOP-ERASE-002 v3.1.
