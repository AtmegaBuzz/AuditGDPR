---
doc_id: "INT-IRP-001"
title: "Security Incident Response Plan"
company: "Acme Corp"
publisher: "ACME"
access_level: 1
classification: "internal"
doc_type: "policy"
profile: "company_doc"
topic: "breach"
topics: ["breach"]
owner: "Security"
approver: "CISO"
version: "4.0"
effective_date: "2026-01-15"
status: "current"
gdpr_articles: [32, 33]
related: ["PUB-TRUST-001"]
generator: {"writer": "@cf/zai-org/glm-5.3", "judge": "@cf/openai/gpt-oss-120b", "run_id": "20261124-025609", "prompt_hash": "284162f9dd75"}
review: {"status": "ok", "attempts": 3, "issues_left": 0, "scores": {"fact_fidelity": 5, "tier_discipline": 5, "gdpr_accuracy": 5, "realism": 5, "retrievability": 5}}
---

# Security Incident Response Plan

| Field | Value |
|---|---|
| Document ID | INT-IRP-001 |
| Version | 4.0 |
| Owner | Security |
| Approver | Samir Haddad, Chief Information Security Officer (CISO) |
| Effective date | 2026-01-15 |
| Classification | INTERNAL |
| Status | Current |

**Audience:** Incident responders, Engineering, and Legal.
**GDPR articles in scope:** Article 32 (security of processing), Article 33 (notification of a personal data breach to the supervisory authority).
**Related public document:** PUB-TRUST-001 "Trust Center: Security and Incident Response Overview" summarises the breach-response commitments in this plan for customers and prospects.

## 1. Purpose, Scope and Document Control

### 1.1 Purpose

This Security Incident Response Plan (INT-IRP-001) is Acme's internal policy for detecting, triaging, containing, remediating and notifying personal data breaches, in compliance with GDPR Article 32 (security of processing) and Article 33 (notification of a personal data breach to the supervisory authority). It defines how Acme Corp Ltd, as controller for its own account, employee, website-visitor and marketing data, and as processor for its customers' end-user data in the Beacon platform, responds when personal data is accidentally or unlawfully destroyed, lost, altered, disclosed to, or accessed by an unauthorised party (Article 4(12)).

The plan sets out Acme's internal targets, which are in places stricter than the legal deadlines: a 48-hour internal target for submitting an Article 33(1) notification to the Irish Data Protection Commission (DPC), Acme's lead supervisory authority, against the 72-hour legal deadline; and a 4-hour internal target for notifying an affected customer-controller of a processor-side breach, ahead of the 24-hour contractual commitment in Acme's standard Data Processing Agreement.

### 1.2 Scope

This plan applies to all Acme systems that process personal data:

- **Acme Beacon** — the customer-facing product
- **Atlas** — the analytics warehouse holding event and billing history
- **Ledger** — the billing and invoicing system
- **HelpHub** — the customer-support desk and ticketing system
- **Vault** — the write-once immutable backup system (retention 35 days for backups; 5 years for breach-register entries)

It covers both controller-side breaches (Acme Corp Ltd notifies the DPC directly) and processor-side breaches affecting customer end-user data in Beacon (Acme notifies the affected customer as controller, per Article 33(2)). Suspected breaches reported by any means — automated alerting in Beacon or Atlas, or a manual report to privacy@acme.example — are in scope.

### 1.3 Audience

Incident responders (the 24/7 security on-call rotation), Engineering, and Legal.

### 1.4 External counterpart

The public Trust Center page PUB-TRUST-001 "Trust Center: Security and Incident Response Overview" is the customer-facing counterpart of this plan. Where this plan and PUB-TRUST-001 differ in level of detail, this plan governs internal operations; PUB-TRUST-001 states only the external commitments (72-hour DPC notification, high-risk individual notification, processor-to-controller notification, breach documentation, and how to report a suspected breach to the DPO's office).

## 2. Roles and Responsibilities

### 2.1 Overview

Every personal data breach at Acme has a clearly accountable owner for each stage of the response. The table below assigns responsibility using RACI (Responsible, Accountable, Consulted, Informed) for the key activities defined in this plan. Named individuals hold these roles as of the effective date of version 4.0.

### 2.2 RACI matrix

| Activity | CISO (Samir Haddad) | DPO (Tomás Reyes) | Head of Privacy Ops (Mara Okafor) | Senior Privacy Counsel (Aoife Brennan) | Head of Customer Support (Owen Gallagher) | VP Engineering (Lena Fischer) | Internal Audit |
|---|---|---|---|---|---|---|---|
| Breach detection and 24/7 security on-call (Beacon and Atlas alert rules) | A/R | I | I | — | — | C | — |
| Triage of suspected breaches in PrivacyDesk queue INT-Q-BREACH | I | C | A/R | — | — | — | — |
| Severity scoring (S1–S4) using the internal severity matrix | C | C | A/R | C | — | — | — |
| Completion of Breach Assessment Record (INT-FORM-11) | I | C | A/R | C | — | — | — |
| Sign-off and submission of Article 33(1) notification to the DPC | C | A/R | R (drafts) | C | — | — | — |
| Notification of affected customer-controller (processor-side breaches) | I | C | C | C | A/R | — | — |
| Article 34(1) communication to affected individuals | I | C | R (drafts) | A (legal review) | R (issues, handles inbound) | — | — |
| Breach register maintenance in Vault (5-year retention) | I | C | A/R | — | — | — | C |
| Detection-gap review (manual discoveries) | C | I | C | — | — | A/R | — |
| Quarterly review of the breach register | I | I | C | — | — | — | A/R |

R = Responsible, A = Accountable, C = Consulted, I = Informed.

### 2.3 Key role notes

- **Samir Haddad (CISO)** owns breach detection: Beacon and Atlas alert rules feed a 24/7 security on-call rotation, with an internal mean-time-to-detect target of 1 hour for S1/S2-classified incidents (F-BRE-09).
- **Tomás Reyes (DPO)** is the contact point for reports of suspected breaches via privacy@acme.example (F-BRE-05) and signs off every Article 33(1) notification to the DPC before submission via the DPC portal.
- **Mara Okafor (Head of Privacy Operations)** owns the INT-Q-BREACH triage queue and the S1–S4 severity matrix. Triage SLA: initial assessment within 2 hours of the ticket being raised during business hours, and within 6 hours outside business hours.
- **Aoife Brennan (Senior Privacy Counsel, Dublin)** provides legal review of Article 34(1) individual-communication drafts before they are issued.
- **Owen Gallagher (Head of Customer Support)** sends customer-controller notifications using HelpHub templates (4-hour internal target, ahead of the 24-hour contractual commitment in the Data Processing Agreement) and staffs inbound questions from affected individuals in HelpHub.
- **Lena Fischer (VP Engineering)** owns detection-gap reviews, completed within 10 working days when a breach is discovered by any means other than automated alerting in Beacon or Atlas.
- **Internal Audit** reviews quarterly extracts of the Article 33(5) breach register maintained in Vault.

## 3. Detection and Reporting of Suspected Breaches

### 3.1 Detection architecture

Breach detection at Acme is owned by the CISO, Samir Haddad. Automated alert rules are configured in **Beacon** (the customer-facing product) and **Atlas** (the analytics warehouse holding event and billing history), and both rule sets feed Acme's 24/7 security on-call rotation. The on-call rotation is the first responder for any alert that may indicate a personal data breach as defined by GDPR Article 4(12) — accidental or unlawful destruction, loss, alteration, unauthorised disclosure of, or access to, personal data.

Acme's internal target for mean time to detect (MTTD) is **1 hour** for incidents classified S1 or S2 under the internal severity matrix (see section 2.3). On-call responders must treat any alert with plausible S1/S2 characteristics as time-critical until the severity assessment in the INT-Q-BREACH queue determines otherwise.

### 3.2 Reporting channels

Detection is not limited to automated alerting. Any person — employee, customer, or external party — can report a suspected personal data breach to **privacy@acme.example**, which is monitored by the office of the Data Protection Officer, Tomás Reyes. Reports received by any channel are raised as tickets in the PrivacyDesk queue **INT-Q-BREACH**, owned by Mara Okafor, Head of Privacy Operations, and triaged under the SLAs in section 2.3 (initial assessment within 2 hours during business hours, 6 hours outside business hours).

On-call responders who identify a suspected breach while investigating an alert must raise an INT-Q-BREACH ticket themselves; they must not rely on the alert pipeline alone to record the incident.

### 3.3 Escalation and detection-gap review

If a personal data breach is discovered by any means other than the automated alerting in Beacon or Atlas — for example a manual report to privacy@acme.example, a support escalation, or an internal audit finding — the incident is flagged for a **detection-gap review** by Lena Fischer's Engineering organisation. The review must be completed within **10 working days** of the breach being identified.

The detection-gap review examines why the alert rules in Beacon or Atlas did not surface the breach, and produces concrete remediation actions (for example, new or tuned alert rules). The CISO is informed of the outcome, and the DPO is kept informed throughout.

### 3.4 Detection and reporting checklist

- [ ] Alert rules in Beacon and Atlas active and feeding the 24/7 security on-call rotation
- [ ] MTTD of 1 hour achieved for S1/S2-classified incidents
- [ ] All suspected breaches, from any channel, raised in INT-Q-BREACH
- [ ] Manually discovered breaches flagged for a detection-gap review within 10 working days

## 4. Triage and Severity Assessment

### 4.1 Triage in the INT-Q-BREACH queue

All suspected personal data breaches — whether raised by the 24/7 security on-call rotation, by a manual report to privacy@acme.example, or by any other channel — are triaged in the PrivacyDesk queue **INT-Q-BREACH**, owned by Mara Okafor, Head of Privacy Operations. Every suspected breach must have an INT-Q-BREACH ticket; no breach is handled outside the queue.

The triage SLA is an **initial assessment within 2 hours** of the ticket being raised during business hours, and **within 6 hours** outside business hours. The initial assessment determines whether the incident involves personal data as defined by GDPR Article 4(1), and whether it constitutes a personal data breach under Article 4(12) — a breach of security leading to accidental or unlawful destruction, loss, alteration, unauthorised disclosure of, or access to, personal data.

### 4.2 Severity matrix (S1–S4)

Severity is scored S1–S4 using the internal severity matrix maintained by Mara Okafor's Privacy Operations team:

| Severity | Definition | DPC notification | Article 33(1) clock |
|---|---|---|---|
| S1 | High risk to individuals' rights and freedoms | Mandatory | Triggered (72-hour legal deadline; 48-hour internal target) |
| S2 | Risk to individuals' rights and freedoms | Case-by-case | Triggered (72-hour legal deadline; 48-hour internal target) |
| S3 | No likely risk to individuals | Not required | Not triggered |
| S4 | Near miss / no personal data involved | Not required | Not triggered |

The severity determination is the trigger for all downstream notification obligations: an S1 or S2 classification starts the 72-hour Article 33(1) clock from the point Acme becomes aware of the breach, against Acme's stricter internal target of 48 hours to submit the DPC notification. S3 and S4 classifications do not trigger the clock, but every breach regardless of severity is documented in the breach register (see section 6).

Where the severity matrix leaves the classification uncertain, the triage lead classifies at the higher of the two plausible severities and consults the DPO, Tomás Reyes, before downgrading.

### 4.3 Breach Assessment Record (INT-FORM-11)

Every severity assessment is recorded on form **INT-FORM-11 (Breach Assessment Record)**, which captures the content required by GDPR Article 33(3):

- the nature of the breach, including the categories and approximate numbers of data subjects and of personal data records concerned;
- the name and contact details of the Data Protection Officer, Tomás Reyes (privacy@acme.example);
- the likely consequences of the breach for affected individuals; and
- the measures taken or proposed to address the breach, including measures to mitigate possible adverse effects.

INT-FORM-11 must be completed for all severities, including S3 and S4, so that the Article 33(5) breach register contains the facts, effects and remedial action for every incident.

### 4.4 Triage checklist

- [ ] Ticket raised in INT-Q-BREACH with time of awareness recorded
- [ ] Initial assessment completed within 2 hours (business hours) / 6 hours (outside business hours)
- [ ] Personal data breach confirmed or ruled out under Article 4(12)
- [ ] Severity scored S1–S4 against the internal severity matrix
- [ ] INT-FORM-11 completed with all Article 33(3) content
- [ ] For S1/S2: Article 33(1) clock recorded and DPO informed immediately

## 5. Containment, Investigation and Remediation

### 5.1 Containment (on-call responder)

1. Contain the breach immediately: revoke compromised credentials, block offending IP ranges, disable affected integrations, or isolate affected systems as needed.
2. Preserve evidence before destructive remediation: capture logs, snapshots and alert payloads to the incident workspace. Do not wipe or reimage systems before evidence is captured.
3. Confirm an INT-Q-BREACH ticket exists for the incident; if not, raise one immediately and record the time of awareness.
4. Notify the PrivacyDesk triage lead so the severity assessment under section 4.2 can begin in parallel. Do not wait for containment to complete before escalating.
5. Where data recovery is needed, restore from **Vault**, Acme's write-once immutable backup system. Vault backups are retained for 35 days; initiate any restore within that window. Because Vault is write-once, backups themselves cannot be altered by an attacker and are a trusted recovery source and evidence store.

### 5.2 Investigation (incident lead)

1. Determine the scope of the breach: which systems (Beacon, Atlas, Ledger, HelpHub), which categories of data subjects, and the approximate numbers of records affected.
2. Establish the timeline: point of initial compromise, duration of exposure, and point of awareness (which starts the Article 33(1) clock for S1/S2).
3. Record every finding and action on the **Breach Assessment Record (INT-FORM-11)**, updating it as the investigation proceeds so the Article 33(3) content (nature, categories and numbers, DPO contact details, likely consequences, measures taken) remains current for notification drafting.
4. If the breach was discovered by any means other than automated alerting in Beacon or Atlas, flag it for a detection-gap review by Lena Fischer's Engineering organisation (10 working days, section 3.3).

### 5.3 Remediation

1. Implement corrective measures addressing root cause, not symptoms, in line with GDPR Article 32 (security of processing, including encryption and the ability to restore availability).
2. Verify containment held and monitor for recurrence for at least 14 days.
3. Close out INT-FORM-11 with final remedial action taken; the incident is not closed until the entry is filed in the breach register (section 6).

### 5.4 Checklist

- [ ] Breach contained and evidence preserved before destructive action
- [ ] Vault restore initiated within the 35-day backup window (if recovery required)
- [ ] Scope, timeline and record counts established and recorded on INT-FORM-11
- [ ] Manual discoveries flagged for detection-gap review
- [ ] Root-cause remediation implemented and verified

## 6. Notification to the DPC (Article 33(1))

### 6.1 When notification is required

For any personal data breach classified **S1 or S2** under the internal severity matrix (section 4.2), Acme Corp Ltd notifies the Irish Data Protection Commission (DPC), its lead supervisory authority, without undue delay and, where feasible, no later than **72 hours** after becoming aware of the breach, in line with GDPR Article 33(1). S1 breaches (high risk to individuals) carry mandatory notification; S2 breaches (risk to individuals) are notified case by case, with the DPO consulted on the decision. S3 and S4 breaches do not trigger DPC notification, but are still documented in the breach register (section 7).

Acme's internal target is to submit the notification within **48 hours** of awareness — stricter than the 72-hour legal deadline — to preserve margin for DPO review and portal submission.

### 6.2 Sign-off and submission

Every Article 33(1) notification is signed off by the DPO, **Tomás Reyes**, before submission via the **DPC portal**. Privacy Operations drafts the notification from the Breach Assessment Record (**INT-FORM-11**); the DPO reviews, approves and submits. No notification goes to the DPC without DPO sign-off.

### 6.3 Notification content (Article 33(3))

The notification draws its content from INT-FORM-11, which captures the Article 33(3) requirements:

- the nature of the breach, including the categories and approximate numbers of data subjects and personal data records concerned;
- the DPO's name and contact details (Tomás Reyes, privacy@acme.example);
- the likely consequences of the breach for affected individuals; and
- the measures taken or proposed to address the breach and mitigate adverse effects.

### 6.4 Phased notification (Article 33(4))

Where the facts are incomplete at the 48-hour internal target, Acme submits an initial notification via the DPC portal within the target and supplements it in phases under Article 33(4), with reasons for any delay recorded.

### 6.5 Checklist

- [ ] S1/S2 classification confirmed on INT-FORM-11
- [ ] 48-hour internal target met (72-hour legal deadline observed)
- [ ] DPO sign-off obtained before DPC portal submission
- [ ] Article 33(3) content complete, or phased submission with reasons documented

## 7. Processor-to-Controller Notification (Article 33(2))

### 7.1 When notification is required

Where a personal data breach affects customer end-user data held in **Beacon**, Acme acts as processor for the affected customer (as controller). Under GDPR Article 33(2) and Acme's standard Data Processing Agreement, Acme must notify the affected customer-controller **without undue delay** after becoming aware of the breach. The DPA sets a 24-hour contractual commitment; Acme's internal target is to notify the affected customer-controller within **4 hours of awareness**, ahead of that contractual commitment.

### 7.2 Who sends the notification

Customer-controller notifications are sent by the **Customer Support team led by Owen Gallagher**, using the approved **HelpHub** notification templates. Privacy Operations (Mara Okafor) supplies the breach facts from the Breach Assessment Record (**INT-FORM-11**); the DPO, Tomás Reyes, is informed of every processor-side notification.

### 7.3 Procedure

1. On confirmation that a breach affects customer end-user data in Beacon, the incident lead notifies Owen Gallagher's team immediately.
2. Customer Support identifies all affected customer-controllers and issues the notification from HelpHub within the 4-hour internal target, including the facts needed for the customer to meet its own Article 33(1) obligations as controller.
3. If facts are incomplete at 4 hours, send an initial notification and supplement it in phases, mirroring Article 33(4).
4. Record the notification time, recipients and content on INT-FORM-11 for the breach register (section 8).

### 7.4 Checklist

- [ ] Affected customer-controllers identified
- [ ] Notification sent from HelpHub within 4 hours of awareness
- [ ] DPO informed; notification logged on INT-FORM-11

## 8. Communication to Affected Individuals (Article 34(1))

### 8.1 When communication is required

Where a personal data breach classified **S1** under the internal severity matrix (section 4.2) is likely to result in a **high risk to the rights and freedoms of affected individuals**, Acme Corp Ltd communicates the breach to those individuals **without undue delay**, as required by GDPR Article 34(1). S2, S3 and S4 breaches do not trigger Article 34(1) communication unless the severity assessment is revised upwards.

### 8.2 Drafting, review and issuance

1. Privacy Operations (Mara Okafor's team) prepares the draft notice, drawing on the Breach Assessment Record (**INT-FORM-11**).
2. The draft is reviewed by **Aoife Brennan, Senior Privacy Counsel (Dublin)**, before issuance.
3. The notice is issued **by email from privacy@acme.example**.
4. **Owen Gallagher's Customer Support team staffs the resulting inbound questions in HelpHub**, using an approved FAQ prepared alongside the notice.

### 8.3 Article 34(3) exemptions

Individual communication is not required where:

- the affected personal data was **unintelligible** to any unauthorised party, for example because it was protected by strong encryption;
- **subsequent measures** ensure the high risk is no longer likely to materialise; or
- individual communication would involve **disproportionate effort**, in which case Acme makes the communication public by comparable means.

Any reliance on an Article 34(3) exemption must be assessed against INT-FORM-11 and approved by the DPO, Tomás Reyes, with the reasoning recorded in the breach register (section 9).

### 8.4 Checklist

- [ ] S1 classification and high-risk determination confirmed on INT-FORM-11
- [ ] Notice drafted by Privacy Operations and reviewed by Aoife Brennan
- [ ] Notice issued from privacy@acme.example without undue delay
- [ ] HelpHub inbound staffing in place with approved FAQ
- [ ] Any Article 34(3) exemption documented and DPO-approved

## 9. Breach Register and Record-Keeping (Article 33(5))

### 9.1 Documentation requirement

Every personal data breach at Acme — regardless of severity, and whether or not it is notified to the Irish Data Protection Commission (DPC) or to affected individuals — is documented with its facts, effects and remedial action taken, in line with GDPR Article 33(5) and Acme's accountability obligation under Article 5(2). S3 and S4 incidents, including near misses, are documented to the same standard as S1 and S2 breaches.

### 9.2 Register location and retention

The complete Article 33(5) breach register is maintained in **Vault**, Acme's write-once immutable backup system. Because Vault entries cannot be altered after the fact, the register provides tamper-evident evidence of Acme's breach-handling record. Each register entry is retained for **5 years**. Each entry is compiled from the closed Breach Assessment Record (**INT-FORM-11**) and includes the notification decisions and their outcomes.

### 9.3 Quarterly review

Quarterly extracts of the breach register are reviewed by the **Internal Audit team**, which examines completeness, classification consistency and adherence to the SLAs in this plan. Findings are reported to the CISO, Samir Haddad, and the DPO, Tomás Reyes.

### 9.4 Checklist

- [ ] Every breach, all severities, entered in the Vault register
- [ ] Facts, effects and remedial action recorded for each entry
- [ ] 5-year retention applied to each entry
- [ ] Quarterly extract provided to Internal Audit

## 10. Post-Incident Review, Exceptions and Related Documents

### 10.1 Post-incident review

Every personal data breach classified S1 or S2 receives a post-incident review chaired by the CISO, Samir Haddad, within **10 working days** of the incident being closed in INT-Q-BREACH. The review covers the timeline from detection to notification, adherence to the SLAs in this plan (2-hour/6-hour triage, 48-hour DPC target, 4-hour customer-controller target), and the effectiveness of remediation. The DPO, Tomás Reyes, and Mara Okafor attend; the outcome is recorded against the INT-FORM-11 entry and filed in the Vault breach register (section 9).

### 10.2 Mandatory detection-gap review

Where a breach is discovered by any means other than the automated alerting in **Beacon** or **Atlas** — for example a manual report to privacy@acme.example or a support escalation — the incident is flagged for a **detection-gap review** by Lena Fischer's Engineering organisation, completed within **10 working days** (F-BRE-14). The review examines why the alert rules did not surface the breach and produces concrete remediation actions, such as new or tuned alert rules. The CISO is informed of the outcome.

- [ ] Detection-gap review completed within 10 working days
- [ ] Alert-rule remediation actions assigned with owners

### 10.3 Exceptions

Any deviation from this plan (for example, a missed internal target with a documented reason, or reliance on an Article 34(3) exemption) must be documented on the incident's INT-FORM-11 entry and **approved by the DPO, Tomás Reyes**. Undocumented exceptions are escalated to the CISO. Exceptions are reviewed by Internal Audit as part of the quarterly breach-register review (section 9.3).

### 10.4 Records generated under this plan

| Record | System | Retention |
|---|---|---|
| INT-Q-BREACH tickets | PrivacyDesk | 5 years |
| Breach Assessment Record (INT-FORM-11) | Vault breach register | 5 years |
| DPC notifications and customer-controller notifications | Vault breach register | 5 years |
| Detection-gap and post-incident review outcomes | Vault breach register | 5 years |

### 10.5 Related documents

- **PUB-TRUST-001** "Trust Center: Security and Incident Response Overview" — the public-facing counterpart of this plan, summarising Acme's breach-response commitments under GDPR Articles 32–34 for customers and prospects. This plan governs internal operations; PUB-TRUST-001 states only the external commitments.
