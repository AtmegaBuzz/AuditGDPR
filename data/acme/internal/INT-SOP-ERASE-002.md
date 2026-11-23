---
doc_id: "INT-SOP-ERASE-002"
title: "Erasure Request Handling Procedure"
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
version: "3.1"
effective_date: "2026-03-01"
status: "current"
gdpr_articles: [12, 17, 19]
related: ["PUB-FAQ-DSR-001"]
generator: {"writer": "@cf/zai-org/glm-5.3", "judge": "@cf/openai/gpt-oss-120b", "run_id": "20261124-025609", "prompt_hash": "284162f9dd75"}
review: {"status": "ok", "attempts": 1, "issues_left": 0, "scores": {"fact_fidelity": 5, "tier_discipline": 5, "gdpr_accuracy": 5, "realism": 5, "retrievability": 5}}
---

# Erasure Request Handling Procedure

| Field | Value |
|---|---|
| Document ID | INT-SOP-ERASE-002 |
| Version | 3.1 |
| Owner | Privacy Operations |
| Approver | Mara Okafor, Head of Privacy Operations |
| Effective date | 2026-03-01 |
| Classification | INTERNAL |
| Status | Current |
| Audience | Privacy Operations team and Customer Support leads |
| GDPR articles in scope | Art. 12, Art. 17, Art. 19 |

## 1. Purpose and Scope

This Standard Operating Procedure (SOP) governs how Privacy Operations handles erasure (data-subject deletion) requests at Acme Corp. It defines the intake, verification, execution and notification steps required so that Acme responds to erasure requests within one month of receipt, as required by Article 12(3) GDPR and as stated in Acme's privacy notice.

Erasure requests may reach Acme through two intake channels:

- **privacy@acme.example** – requests received by email are logged in the PrivacyDesk queue INT-Q-ERASE.
- **Beacon Settings > Privacy** – the self-service page where account holders can delete their own account data directly.

This SOP covers Acme's handling of requests in both its controller role (for its own customers' account data, employees, website visitors and marketing data) and, where customers instruct Acme as a processor, its supporting role for end-user data stored in Beacon. Where Acme acts as processor, erasure of end-user data is executed on the customer controller's documented instructions.

This SOP applies to the Privacy Operations team (including its three analysts) and to Customer Support leads who receive or triage erasure requests. It does not cover access or portability requests, which are handled under separate procedures.

## 2. Roles and Responsibilities

The RACI table below assigns accountability for erasure request handling in the PrivacyDesk queue INT-Q-ERASE. "R" = Responsible, "A" = Accountable, "C" = Consulted, "I" = Informed.

| Activity | Privacy Ops analysts | Head of Privacy Operations (Mara Okafor) | DPO (Tomás Reyes) | Privacy Ops lead | VP Engineering (Lena Fischer) | Data Platform team |
|---|---|---|---|---|---|---|
| Intake logging and triage in INT-Q-ERASE | R | A | I | I | – | – |
| Identity verification (EDPB Guidelines 01/2022 principles) | R | A | C | I | – | – |
| Article 12(6) decision where identity cannot be confirmed within 5 business days | C | A | R | I | – | – |
| Erasure execution in Beacon, Ledger, Atlas and HelpHub | R | A | – | I | C | C |
| Legal-exception review under checklist INT-CHK-ERASE (Art. 17(3)) | R | A | C | I | – | – |
| Day-14 SLA escalation | I | A | I | R | – | – |
| Day-20 SLA breach reporting (weekly, system-level causes) | I | A | R | C | R | C |
| Atlas deletion job manual re-runs | I | I | – | I | A | R |
| Article 19 recipient notification (Stripe and sub-processors) | R | A | I | I | – | – |

### 2.1 Key role notes

- **Privacy Operations analysts (three analysts, Mara Okafor's team):** perform identity verification for every erasure request. Only verified requests start the 20-calendar-day internal SLA (stricter than the one-month statutory deadline in Art. 12(3) GDPR).
- **DPO (Tomás Reyes):** decides on requests where identity cannot be confirmed within 5 business days, under Article 12(6) GDPR; receives weekly reports of tickets breaching day 20 of the SLA.
- **Privacy Operations lead:** handles escalations of tickets that reach day 14 of the 20-day SLA.
- **VP Engineering (Lena Fischer):** receives weekly reports of day-20 breaches where system-level causes are identified.
- **Data Platform team:** performs manual re-runs of the Atlas deletion job when it fails on records with more than 500 linked event rows.

## 3. Intake and Logging

Erasure requests reach Acme through two channels, and every request must be logged in the PrivacyDesk queue INT-Q-ERASE on the day of receipt. Acme responds to erasure requests within one month of receipt, as required by Article 12(3) GDPR and as stated in Acme's privacy notice.

### 3.1 Intake channels

- **Email:** requests sent to privacy@acme.example are triaged by the first available Privacy Operations analyst and logged in INT-Q-ERASE with the date and time of receipt recorded on the ticket.
- **Self-service:** account holders can delete their own account data directly through the Beacon Settings > Privacy page. Self-service deletions generate an automated entry in INT-Q-ERASE for tracking and completion confirmation.

Customer Support leads who receive an erasure request through any other channel (for example a HelpHub ticket) must forward it to privacy@acme.example the same business day; the PrivacyDesk ticket records the original receipt date, not the forwarding date.

### 3.2 Logging requirements

Every INT-Q-ERASE ticket must record:

- The requester's account ID and the systems to be checked (Beacon, Ledger, Atlas, HelpHub), as captured on intake form INT-FORM-03.
- The date of receipt, which fixes the start of the one-month statutory response period under Article 12(3) GDPR.
- The identity-verification status. Only verified requests start Acme's internal SLA of 20 calendar days from identity verification to complete erasure, which is stricter than the one-month statutory deadline.

### 3.3 Statutory deadline and extensions

The statutory response deadline is one month from receipt of the request. Where a request is complex or numerous, the deadline may be extended by two further months under Article 12(3) GDPR. If Privacy Operations extends a deadline, the data subject must be informed of the extension and its reasons within one month of receipt. The analyst records the extension decision and the notification date on the INT-Q-ERASE ticket.

## 4. Identity Verification

Every erasure request logged in the PrivacyDesk queue INT-Q-ERASE must pass identity verification before any deletion work begins. Identity verification is performed by the Privacy Operations analysts (Mara Okafor's team of three analysts) and follows the principles set out in EDPB Guidelines 01/2022. Consistent with Article 12(6) GDPR and Acme's privacy notice, Acme may request additional information to confirm the identity of the requester where it has reasonable doubts about that identity.

### 4.1 Verification using intake form INT-FORM-03

The analyst completes intake form INT-FORM-03 for every request. The form requires:

- The requester's account ID.
- The systems to be checked: Beacon, Ledger, Atlas and HelpHub.
- Identity evidence supporting the link between the requester and the account.

The analyst compares the submitted identity evidence against the account records held in Beacon before marking the request as verified on the INT-Q-ERASE ticket.

### 4.2 Starting the 20-day internal SLA

Only verified requests start Acme's internal SLA of 20 calendar days from identity verification to complete erasure. This SLA is stricter than the one-month statutory deadline in Article 12(3) GDPR. The statutory one-month period runs from receipt of the request regardless of verification status, so verification must not be used to delay the statutory clock; any refusal or further information request must itself be communicated within one month of receipt.

### 4.3 Escalation where identity cannot be confirmed

Where identity cannot be confirmed within 5 business days of receipt, the analyst escalates the ticket to the DPO, Tomás Reyes, for a decision under Article 12(6) GDPR. The escalation must be recorded on the INT-Q-ERASE ticket, including:

- [ ] The verification steps already attempted and their outcomes.
- [ ] The specific doubts about the requester's identity.
- [ ] The DPO's decision and its date.

The DPO's decision (for example, a request for additional information or a refusal under Article 12(6) GDPR) is communicated to the requester within one month of receipt of the original request.

## 5. Erasure Execution

Once an erasure request is verified, the Privacy Operations analyst triggers deletion jobs in four systems, in the following order: Beacon, Ledger, Atlas, and HelpHub. All deletions are tracked on the INT-Q-ERASE ticket with a completion timestamp per system.

### 5.1 Beacon (account and profile data)

- [ ] Trigger the Beacon deletion job for the requester's account and profile data.
- [ ] Confirm completion within **3 calendar days** of verification and record the timestamp on the INT-Q-ERASE ticket.

### 5.2 Ledger (billing records)

- [ ] Trigger the Ledger deletion job, which flags billing records for legal-exception review.
- [ ] Run the Article 17(3) exception checklist INT-CHK-ERASE against the flagged records (see Section 6 for the exception procedure, including the 6-year retention of Ledger invoices required by Irish tax law).
- [ ] Record on the ticket which records are erased and which are retained under a legal exception.

### 5.3 Atlas (event and billing history)

- [ ] Trigger the Atlas deletion job for event and billing history.
- [ ] Confirm completion. The Atlas deletion job runs nightly; check the next run's output for the ticket's records.

**Known defect:** the Atlas deletion job fails on records with more than 500 linked event rows. Where the nightly run fails for this reason, the analyst must request a manual re-run from the Data Platform team and record the request date on the ticket. Manual re-runs add an average of **6 calendar days** to affected tickets. Analysts must factor this delay into SLA monitoring (Section 7) and, where the 20-day internal SLA is at risk, consider an Article 12(3) extension with reasons notified to the data subject within one month of receipt.

### 5.4 HelpHub (support tickets)

- [ ] Trigger deletion of the requester's support tickets in HelpHub.
- [ ] Confirm completion within **5 calendar days** of verification and record the timestamp on the ticket.

### 5.5 Vault backups

Erasure cannot be executed inside Vault, the immutable backup system. Vault backups are write-once and retained for 35 days, so deletion propagates automatically only when each backup expires. The analyst records the backup expiry date on the INT-Q-ERASE ticket and closes the ticket only after confirming expiry, or documents the expiry date as a pending item where the ticket is otherwise complete.

## 6. Exceptions and Refusals

Erasure requests logged in the PrivacyDesk queue INT-Q-ERASE are executed in full except where the Article 17(3) exception checklist INT-CHK-ERASE applies. Consistent with Acme's privacy notice, erasure may be refused in whole or in part where an exception under Article 17(3) GDPR applies, for example where data must be kept to comply with a legal obligation or for the establishment, exercise or defence of legal claims.

### 6.1 Applying checklist INT-CHK-ERASE

The Privacy Operations analyst runs checklist INT-CHK-ERASE against every erasure request during the Ledger step (Section 5.2), covering the Article 17(3)(b) and Article 17(3)(e) exceptions:

- [ ] Identify any Ledger invoices linked to the requester. Ledger invoices are retained for **6 years** under Irish tax law (Article 17(3)(b) exception).
- [ ] Identify any data subject to a legal hold. Legal-hold data is excluded from erasure (Article 17(3)(e) exception).
- [ ] Record on the INT-Q-ERASE ticket each retained record, the specific exception relied on, and the retention end date where known.

### 6.2 Partial erasure

Where an exception applies to some but not all of the requester's data, the analyst proceeds with erasure of all non-excepted data in Beacon, Atlas and HelpHub per Section 5, and records the partial refusal on the ticket. The exception does not pause the 20-day internal SLA for the non-excepted deletions.

### 6.3 Notifying the data subject of a refusal

Where erasure is refused in whole or in part, Privacy Operations informs the data subject of the reasons for the refusal and of their right to lodge a complaint with a supervisory authority and to seek a judicial remedy, in line with Article 12(4) GDPR. This notification must be sent **within one month of receipt of the request**. The analyst records the notification date and the channel used on the INT-Q-ERASE ticket.

### 6.4 Consultation

Where the application of INT-CHK-ERASE is unclear (for example, the scope of a legal hold), the analyst consults the DPO, Tomás Reyes, before finalising the refusal decision.

## 7. Recipient Notification (Article 19)

Where personal data has been disclosed to other recipients and is erased at the data subject's request, Acme notifies each recipient of the erasure, unless this is impossible or involves disproportionate effort, in line with Article 19 GDPR and Acme's privacy notice. For every verified erasure request in the PrivacyDesk queue INT-Q-ERASE, notification is sent within **10 calendar days of execution of the erasure**, using notification template INT-TPL-19.

### 7.1 Recipients to be notified

- [ ] **Stripe** – payer data associated with the requester.
- [ ] **Every sub-processor** listed in the current sub-processor register. The analyst retrieves the register as at the date of execution and records the version used on the INT-Q-ERASE ticket.

### 7.2 Notification steps

1. Populate template INT-TPL-19 with the requester's account ID, the data categories erased, the execution date and the recipient's role.
2. Send the notification to each recipient and record the send date on the INT-Q-ERASE ticket.
3. Confirm all notifications are dispatched within 10 calendar days of execution; record any exceptions (impossibility or disproportionate effort) with reasons on the ticket.

### 7.3 Informing the data subject

Where the data subject asks which recipients were notified, Privacy Operations provides that information, as required by Article 19 GDPR. The analyst logs the request and response on the INT-Q-ERASE ticket.

### 7.4 Exception handling

Where notification is impossible or would involve disproportionate effort, the analyst documents the assessment and the reasons on the ticket and informs the DPO, Tomás Reyes, before closing the notification step.

## 8. Backups and Vault Handling

Vault is Acme's immutable backup system. Vault backups are write-once and retained for **35 days**. Erasure cannot be executed inside Vault, so deletion of a requester's personal data propagates automatically only when each backup containing that data expires. This is a technical limitation of the write-once design, not a discretionary delay, and Privacy Operations must account for it when tracking erasure requests in the PrivacyDesk queue INT-Q-ERASE.

### 8.1 Recording the backup expiry date

For every verified erasure request, the Privacy Operations analyst records the relevant Vault backup expiry date on the INT-Q-ERASE ticket. The expiry date is the latest date on which any backup containing the requester's data reaches the end of its 35-day retention period.

### 8.2 Ticket closure

- [ ] Confirm all in-system deletions in Beacon, Ledger, Atlas and HelpHub are complete (Section 5).
- [ ] Confirm Article 19 recipient notifications are dispatched (Section 7).
- [ ] Confirm the Vault backup expiry date has passed and deletion has propagated.
- [ ] Record the expiry confirmation date on the INT-Q-ERASE ticket before closure.

The ticket must not be closed as fully complete until backup expiry is confirmed. Where the ticket is otherwise complete but the backup has not yet expired, the analyst documents the expiry date as a pending item on the ticket and sets a follow-up for the expiry date.

## 9. SLA Monitoring and Escalation

Acme's internal SLA for erasure requests is **20 calendar days from identity verification to complete erasure**, tracked on every ticket in the PrivacyDesk queue INT-Q-ERASE. This SLA is stricter than the one-month statutory deadline in Article 12(3) GDPR, which runs from receipt of the request. Only verified requests start the 20-day internal SLA; the statutory one-month clock runs from receipt regardless of verification status.

### 9.1 Day-14 escalation

- [ ] Run a daily review of INT-Q-ERASE tickets approaching day 14 of the internal SLA.
- [ ] Escalate any ticket that reaches **day 14** without completed erasure to the Privacy Operations lead.
- [ ] Record the escalation date and the blocking cause (for example, a pending Atlas manual re-run under Section 5.3) on the ticket.

### 9.2 Day-20 breach reporting

- [ ] Log any ticket that breaches **day 20** of the internal SLA as an SLA breach on the ticket.
- [ ] Report SLA breaches **weekly** to the DPO, Tomás Reyes.
- [ ] Report breaches with **system-level causes** to Lena Fischer (VP Engineering) in the same weekly report, so that Engineering can address underlying system defects.

### 9.3 Statutory deadline check

Even where the internal 20-day SLA is breached, the statutory one-month deadline under Article 12(3) GDPR must still be met. Where a breach puts the statutory deadline at risk, the analyst considers a two-month extension under Article 12(3) GDPR and notifies the data subject of the extension and its reasons within one month of receipt (Section 3.3).

## 10. Records and Quality Checks

Every ticket in the PrivacyDesk queue INT-Q-ERASE must contain a complete record set so that Acme can demonstrate accountability for each erasure request under Article 5(2) GDPR.

### 10.1 Records kept per ticket

| Record | Source | Purpose |
|---|---|---|
| Completed intake form INT-FORM-03 (account ID, systems to be checked: Beacon, Ledger, Atlas, HelpHub, identity evidence) | Section 4.1 | Demonstrates lawful intake and verification basis |
| Identity-verification evidence and outcome | Section 4 | Demonstrates Art. 12(6) handling where doubts existed |
| Deletion confirmation timestamps for Beacon, Ledger, Atlas and HelpHub | Section 5 | Demonstrates execution within the 20-day internal SLA |
| Article 17(3) exception decisions under checklist INT-CHK-ERASE (6-year Ledger invoice retention, legal holds) | Section 6 | Demonstrates refusal grounds and Art. 12(4) notification date |
| Article 19 recipient notifications (Stripe and sub-processors), template INT-TPL-19 | Section 7 | Demonstrates recipient notification within 10 calendar days |
| Vault backup expiry date and expiry confirmation | Section 8 | Demonstrates propagation of erasure from immutable backups |

### 10.2 Closing checklist

Before resolving any INT-Q-ERASE ticket, the Privacy Operations analyst confirms:

- [ ] All Section 10.1 records are attached and legible on the ticket.
- [ ] Every system deletion timestamp (Beacon, Ledger, Atlas, HelpHub) is recorded.
- [ ] Any retained record is matched to a specific Article 17(3)(b)/(e) exception with the data subject notified under Article 12(4) within one month.
- [ ] Article 19 notifications are dispatched and dated, or an exception is documented with reasons.
- [ ] Vault expiry is confirmed, or the expiry date is logged as a pending item with a follow-up set.

The Privacy Operations lead spot-checks a sample of closed tickets monthly to confirm record completeness.
