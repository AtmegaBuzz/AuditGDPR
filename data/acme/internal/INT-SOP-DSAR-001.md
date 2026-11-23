---
doc_id: "INT-SOP-DSAR-001"
title: "Data Subject Access and Portability Procedure"
company: "Acme Corp"
publisher: "ACME"
access_level: 1
classification: "internal"
doc_type: "sop"
profile: "company_doc"
topic: "access"
topics: ["access"]
owner: "Privacy Operations"
approver: "Head of Privacy Operations"
version: "2.5"
effective_date: "2026-02-10"
status: "current"
gdpr_articles: [12, 15, 20]
related: ["PUB-FAQ-DSR-001"]
generator: {"writer": "@cf/zai-org/glm-5.3", "judge": "@cf/openai/gpt-oss-120b", "run_id": "20261124-025609", "prompt_hash": "284162f9dd75"}
review: {"status": "ok", "attempts": 1, "issues_left": 0, "scores": {"fact_fidelity": 5, "tier_discipline": 5, "gdpr_accuracy": 5, "realism": 5, "retrievability": 5}}
---

# Data Subject Access and Portability Procedure

| Field | Value |
|---|---|
| Document ID | INT-SOP-DSAR-001 |
| Version | 2.5 |
| Owner | Privacy Operations |
| Approver | Mara Okafor, Head of Privacy Operations |
| Effective date | 2026-02-10 |
| Classification | INTERNAL |
| Status | Current |
| Audience | Privacy Operations team |
| GDPR articles in scope | Art. 12, Art. 15, Art. 20 |

## 1. Purpose and Scope

### 1.1 Purpose

This procedure governs how the Privacy Operations team handles data subject access requests (Art. 15 GDPR) and data portability requests (Art. 20 GDPR) received by Acme Corp as controller, and controller-assistance requests received from Acme's customers regarding their end-user data. It applies to requests arriving via privacy@acme.example, HelpHub tickets, or Beacon Settings > Privacy, all of which must be logged in the PrivacyDesk queue INT-Q-DSAR within one business day of receipt.

### 1.2 Deadlines

Art. 12(3) GDPR requires a response without undue delay and in any event within one month of receipt, extendable by two further months for complex requests. Acme's internal SLA is stricter: Privacy Operations targets a complete DSAR response within **20 calendar days** of receipt. Any extension under Art. 12(3) must be notified to the data subject with reasons before day 30.

### 1.3 Fees and refusals

The first copy of personal data requested under Art. 15 is provided free of charge. A reasonable fee or a refusal is applied only where a request is manifestly unfounded or excessive, per Art. 12(5) GDPR, with the sign-off and legal review steps set out in section 8 of this procedure.

### 1.4 Out of scope

Vault backups (write-once, 35-day retention) are **not** searched for DSARs. Beacon, Atlas and HelpHub production systems are the systems of record; Vault is disaster-recovery only.

## 2. Roles and Responsibilities

### 2.1 RACI table

| Activity | Privacy Operations analysts (INT-Q-DSAR) | Mara Okafor, Head of Privacy Operations | Aoife Brennan, Senior Privacy Counsel | Tomás Reyes, DPO |
|---|---|---|---|---|
| Logging requests in INT-Q-DSAR within one business day of receipt | R / A | I | — | — |
| Identity verification per checklist INT-FORM-03 | R / A | I | — | — |
| Data gathering across Beacon, Atlas and HelpHub | R / A | I | — | — |
| Redaction and four-eyes review (INT-FORM-06) | R | A | C | I |
| DSAR response within 20 calendar days | R | A | I | I |
| Sign-off of refusals or fees under Art. 12(5) | C | R | C | I |
| Legal review of refusals before the Art. 12(4) notice (INT-FORM-07) | I | C | R / A | I |
| Public contact point for data-subject requests and complaints | — | I | — | R / A |

R = Responsible, A = Accountable, C = Consulted, I = Informed.

### 2.2 Team composition and queue routing

The INT-Q-DSAR queue is staffed by the five Privacy Operations analysts reporting to Mara Okafor. All requests arriving via privacy@acme.example, HelpHub tickets, or Beacon Settings > Privacy must be logged in INT-Q-DSAR within one business day of receipt.

### 2.3 Customer end-user requests (controller-assistance)

Requests received from Acme's own customers about their end-user data are **not** handled as DSARs. They are routed to the separate queue INT-Q-DSAR-CUST and handled as controller-assistance tickets under the DPA (Art. 28(3)(e) GDPR). The SLA for these tickets is to provide the customer the requested assistance within **10 business days**. Tomás Reyes, as DPO, is the listed contact point for data-subject requests on Acme's website; requesters may lodge a complaint with a supervisory authority, including the Irish Data Protection Commission.

## 3. Request Intake and Logging

### 3.1 Logging steps

All data-subject requests handled by Privacy Operations are logged in the PrivacyDesk queue INT-Q-DSAR within **one business day of receipt**, regardless of intake channel. The assigned analyst shall:

1. Check privacy@acme.example, HelpHub ticket escalations, and Beacon Settings > Privacy request notifications at least once per business day.
2. Create a ticket in INT-Q-DSAR for each new request, recording the intake channel, the date of receipt, and the requester's stated right (Art. 15 access or Art. 20 portability).
3. Set the ticket due date to 20 calendar days from the date of receipt, per the internal SLA in section 1.2.
4. Send an acknowledgement to the requester confirming receipt and the applicable deadline.
5. Flag any ticket at risk of breaching day 30 to Mara Okafor, Head of Privacy Operations, so an Art. 12(3) extension can be notified with reasons before day 30.

### 3.2 Triage to INT-Q-DSAR-CUST

Where the requester is an Acme customer asking about their end-user data, the ticket is **not** a DSAR. The analyst shall re-route it to queue INT-Q-DSAR-CUST and handle it as a controller-assistance ticket under the DPA (Art. 28(3)(e) GDPR), with the requested assistance provided to the customer within **10 business days**.

## 4. Identity Verification

Privacy Operations verifies the identity of every requester before disclosing personal data, following checklist INT-FORM-03. Acme may request additional information to confirm identity where it has reasonable doubts, per Art. 12(6) GDPR.

### 4.1 Beacon account holders

1. Confirm the requester is in a logged-in Beacon session.
2. Obtain one proof-of-email (a reply from the email address on the Beacon account).
3. Record both verification steps as complete in the INT-Q-DSAR ticket before data gathering begins.

### 4.2 Non-customers

1. Request a copy of government ID.
2. Match the ID to the requester's data held in Beacon, Atlas or HelpHub.
3. Delete the ID copy within **24 hours** of completing verification. Do not attach the ID copy to the ticket or store it in any other system.

### 4.3 Failure to verify

Where verification per INT-FORM-03 cannot be completed, the analyst shall not disclose data and shall escalate the ticket to Mara Okafor, Head of Privacy Operations, for a decision on next steps before the 20-calendar-day SLA expires.

## 5. Data Gathering

Data gathering for DSARs is performed manually across three systems. No automated cross-system DSAR search tool exists, so the assigned analyst runs the steps below for every ticket in INT-Q-DSAR.

### 5.1 Beacon: account and end-user records

1. Retrieve the requester's account records and, where present, end-user records from Beacon.
2. Record the retrieval date and the record identifiers in the INT-Q-DSAR ticket.

### 5.2 Atlas: event and billing history

1. Run the canned queries in INT-FORM-05 to retrieve the requester's event history and billing history from Atlas.
2. Run the dedicated Atlas query in INT-FORM-05 for the AI lead-scoring feature's outputs for the data subject. These outputs are included in the Art. 15(1) supplementary information pack, together with the statement that lead scores are automated evaluations.

### 5.3 HelpHub: support tickets

1. Run a HelpHub admin export for each of the requester's support tickets.
2. Attach the export to the INT-Q-DSAR ticket for redaction under INT-FORM-06 (see section 6).

### 5.4 Systems not searched

Vault backups (write-once, 35-day retention) are **not** searched for DSARs. The documented position in the PrivacyDesk runbook is that Beacon, Atlas and HelpHub production systems are the systems of record, and Vault is disaster-recovery only. Analysts shall not request Vault restores to fulfil a DSAR.

### 5.5 Completeness check

Before proceeding to redaction, the analyst shall confirm in the ticket that all three systems in sections 5.1–5.3 have been queried, and flag to Mara Okafor, Head of Privacy Operations, any system where no data was found so the "no data held" response can be reviewed before release.

## 6. AI Lead-Scoring Outputs and Supplementary Information

Where Acme has generated AI lead-scoring outputs about the requester, those outputs form part of the Art. 15(1) response and must never be omitted from the DSAR package.

### 6.1 Retrieval steps

1. Run the dedicated Atlas query in INT-FORM-05 to retrieve the AI lead-scoring feature's outputs for the data subject.
2. Record in the INT-Q-DSAR ticket the query run date and the lead-score records returned.
3. Attach the query results to the ticket for redaction under INT-FORM-06 (see section 7).

### 6.2 Inclusion in the supplementary information pack

The analyst shall include the lead-scoring outputs in the Art. 15(1) supplementary information pack, together with a plain-language statement that **lead scores are automated evaluations** produced by the AI lead-scoring feature. This ensures the requester understands the nature and origin of the outputs, in line with the transparency requirements of Art. 12(1) and Art. 15(1) GDPR.

### 6.3 Escalation

Where the requester raises questions or objections about the lead-scoring outputs, the analyst shall flag the ticket to Mara Okafor, Head of Privacy Operations, for review before responding.

## 7. Redaction and Four-Eyes Review

Before any DSAR package is released, the assigned analyst redacts it per checklist INT-FORM-06. Redaction protects the rights and freedoms of others, per Art. 15(4) GDPR, and applies to every package assembled under sections 5 and 6.

### 7.1 Redaction steps

1. Remove third-party personal data contained in the requester's HelpHub support tickets (names, email addresses, and identifiers of other individuals appearing in ticket threads).
2. Remove other customers' data appearing in Atlas event logs, per the redaction rules in INT-FORM-06.
3. Record in the INT-Q-DSAR ticket each redaction applied, referencing the INT-FORM-06 checklist item.

### 7.2 Four-eyes review

A **second Privacy Operations analyst** performs a documented four-eyes review of the redacted package before release:

1. Confirm all third-party personal data in HelpHub exports and other customers' data in Atlas event logs has been removed per INT-FORM-06.
2. Record the review outcome, reviewer name, and date in the INT-Q-DSAR ticket.

### 7.3 Release gate

The DSAR package shall not be released until the four-eyes review is documented as complete. Packages failing review are returned to the assigned analyst for re-redaction, with the 20-calendar-day SLA (section 1.2) monitored by Mara Okafor, Head of Privacy Operations.

## 8. Portability Requests (Art. 20)

Portability requests under Art. 20 GDPR are fulfilled only for data the data subject provided, where processing is based on consent or contract, and where processing is carried out by automated means. Manual redaction steps and manually assembled material are excluded from portability scope.

### 8.1 Beacon account data

1. Direct the requester to Beacon Settings > Privacy, where Beacon account data can be exported at any time as JSON or CSV, in a structured, commonly used, machine-readable format.
2. Record in the INT-Q-DSAR ticket that the self-service export was offered, and the date offered.

### 8.2 Atlas analytics event data

1. Where the requester asks for analytics event data, the assigned analyst shall run the relevant canned query in INT-FORM-05 against Atlas.
2. Deliver the event data to the requester as a CSV file, after the redaction and four-eyes review in section 7.

### 8.3 Scope exclusions

The analyst shall not include in a portability package any data that falls outside Art. 20 (e.g. data not provided by the subject, or data processed on other lawful bases). Where the requester disputes the scope, escalate the ticket to Mara Okafor, Head of Privacy Operations, before the 20-calendar-day SLA expires.

## 9. Response Deadlines and Extensions

### 9.1 Deadlines

Art. 12(3) GDPR requires a response without undue delay and in any event within one month of receipt, extendable by two further months for complex requests. Acme's internal SLA is stricter: Privacy Operations targets a complete DSAR response within **20 calendar days** of receipt, logged in INT-Q-DSAR per section 3.

### 9.2 Extensions

Where a request is complex, the assigned analyst shall, with the approval of Mara Okafor, Head of Privacy Operations:

1. Determine the required extension length (maximum two further months under Art. 12(3)).
2. Notify the data subject of the extension **before day 30**, stating the reasons for the delay.
3. Record the notification date and reasons in the INT-Q-DSAR ticket.

### 9.3 Fees

The first copy of personal data requested under Art. 15 is provided **free of charge**. Any fee or refusal for manifestly unfounded or excessive requests follows the sign-off and legal review steps in section 1.3 and the Art. 12(4) notice process using template INT-FORM-07.

### 9.4 Monitoring

The assigned analyst shall flag any ticket at risk of breaching the 20-calendar-day SLA or the day-30 extension notification deadline to Mara Okafor, Head of Privacy Operations, immediately.

## 10. Refusals, Fees and Manifestly Excessive Requests

A DSAR may be refused, or a reasonable fee charged, only where the request is **manifestly unfounded or excessive**, per Art. 12(5) GDPR. The first copy under Art. 15 is always free of charge.

### 10.1 Decision steps

1. The assigned analyst documents in the INT-Q-DSAR ticket why the request is considered manifestly unfounded or excessive (e.g. repeated duplicate requests, no legitimate purpose).
2. Obtain sign-off from Mara Okafor, Head of Privacy Operations.
3. Submit the ticket for legal review by Aoife Brennan, Senior Privacy Counsel.
4. Only after both approvals, send the refusal or fee notice using template INT-FORM-07.

### 10.2 Content of the notice (INT-FORM-07)

The notice must include:

- The reasons for the refusal or fee.
- The right to lodge a complaint with a supervisory authority, including the Irish Data Protection Commission.
- The right to seek a judicial remedy.

### 10.3 Records

The analyst records the sign-off date, legal review date, and the grounds relied on in the INT-Q-DSAR ticket before the notice is sent.

## 11. Exceptions

The following exceptions to standard DSAR handling are documented and approved. Analysts shall not deviate from them without escalation to Mara Okafor, Head of Privacy Operations.

### 11.1 Vault backups not searched

Vault backups (write-once, 35-day retention) are **not** searched for DSARs. The documented position in the PrivacyDesk runbook is that Beacon, Atlas and HelpHub production systems are the systems of record, and Vault is disaster-recovery only. No Vault restore shall be requested to fulfil a DSAR.

### 11.2 Manual redaction steps excluded from portability scope

Portability packages under Art. 20 GDPR cover only data the subject provided, processed on consent or contract, by automated means (F-ACC-13). Manually assembled redaction material is excluded from portability scope and delivered only under Art. 15 access responses.

### 11.3 Customer end-user requests handled as controller-assistance tickets

Requests from Acme's own customers about their end-user data are not handled as direct DSARs. They are routed to queue INT-Q-DSAR-CUST and handled as controller-assistance tickets under the DPA (Art. 28(3)(e) GDPR), with the requested assistance provided within **10 business days**.

## 12. Records and Quality Control

### 12.1 Records retained per ticket

For every ticket in INT-Q-DSAR and INT-Q-DSAR-CUST, the assigned analyst shall ensure the following records are retained in PrivacyDesk:

- Intake timestamp, channel (privacy@acme.example, HelpHub, or Beacon Settings > Privacy), and date of receipt.
- Identity verification evidence per checklist INT-FORM-03, excluding any deleted government ID copies (section 4.2).
- Search logs showing the queries run against Beacon, Atlas (INT-FORM-05) and HelpHub, with run dates.
- Redaction and four-eyes review sign-off per INT-FORM-06 (reviewer name and date).
- Response date and the response package reference.

### 12.2 Monthly queue review

Mara Okafor, Head of Privacy Operations, shall review both queues monthly, checking:

- [ ] All requests were logged in INT-Q-DSAR within one business day of receipt.
- [ ] DSAR responses met the 20-calendar-day internal SLA (stricter than the one-month Art. 12(3) deadline).
- [ ] Any Art. 12(3) extension was notified with reasons before day 30.
- [ ] Controller-assistance tickets in INT-Q-DSAR-CUST met the 10-business-day SLA.
- [ ] Four-eyes review sign-off is documented on every released package.

Breaches and near-misses are logged and escalated to Mara Okafor for corrective action.
