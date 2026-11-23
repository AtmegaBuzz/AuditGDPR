---
doc_id: "INT-RUN-BREACH-001"
title: "Personal Data Breach Notification Runbook (72-hour clock)"
company: "Acme Corp"
publisher: "ACME"
access_level: 1
classification: "internal"
doc_type: "runbook"
profile: "company_doc"
topic: "breach"
topics: ["breach"]
owner: "Privacy Operations & Security"
approver: "Data Protection Officer"
version: "2.1"
effective_date: "2026-02-20"
status: "current"
gdpr_articles: [33, 34]
related: ["INT-IRP-001", "PUB-DPA-001"]
generator: {"writer": "@cf/zai-org/glm-5.3", "judge": "@cf/openai/gpt-oss-120b", "run_id": "20261124-025609", "prompt_hash": "284162f9dd75"}
review: {"status": "ok", "attempts": 3, "issues_left": 0, "scores": {"fact_fidelity": 5, "tier_discipline": 5, "gdpr_accuracy": 5, "realism": 5, "retrievability": 5}}
---

# Personal Data Breach Notification Runbook (72-hour clock)

| Field | Value |
|---|---|
| Document ID | INT-RUN-BREACH-001 |
| Version | 2.1 |
| Owner | Privacy Operations & Security |
| Approver | Tomás Reyes, Data Protection Officer |
| Effective date | 2026-02-20 |
| Classification | INTERNAL |
| Status | Current |
| Audience | Incident commanders, DPO office |
| GDPR articles in scope | Art. 33, Art. 34 |
| Related documents | INT-IRP-001 (Security Incident Response Plan); PUB-DPA-001 (Acme Customer Data Processing Addendum) |

## 1. Document Control and Purpose

| Field | Value |
|---|---|
| Document ID | INT-RUN-BREACH-001 |
| Version | 2.1 |
| Owner | Privacy Operations & Security |
| Approver | Tomás Reyes, Data Protection Officer |
| Effective date | 2026-02-20 |
| Classification | INTERNAL |
| Status | Current |

### 1.1 Purpose

This runbook operationalises the 72-hour notification clock under GDPR Article 33(1). Acme Corp Ltd notifies the Irish Data Protection Commission (DPC), its lead supervisory authority, of any personal data breach likely to result in a risk to individuals' rights and freedoms without undue delay and, where feasible, no later than 72 hours after becoming aware of it (F-BRE-01). Where a breach is likely to result in a high risk to affected individuals, Acme communicates it to those individuals without undue delay, as required by Article 34(1) (F-BRE-02).

### 1.2 Scope

This runbook covers two breach scenarios:

1. **Controller-side breaches** — personal data Acme processes as controller (its own customers' account data, employees, website visitors and marketing).
2. **Processor-side breaches** — breaches affecting customers' end-user data in the Acme Beacon platform, where Acme acts as processor. In these cases Acme must notify the affected customer (as controller) without undue delay after becoming aware of the breach, per Article 33(2) and Acme's Data Processing Agreement (F-BRE-03).

Every personal data breach, whether or not it is reported to a supervisory authority, must be documented with its facts, effects and remedial action taken, in line with Article 33(5) (F-BRE-04).

### 1.3 Audience

Incident commanders and the DPO office. This runbook implements the breach-notification stages of INT-IRP-001 v4.0 (Security Incident Response Plan) and should be read alongside it. Suspected breaches may be reported to privacy@acme.example, monitored by the office of the Data Protection Officer, Tomás Reyes.

## 2. Roles and Responsibilities

### 2.1 RACI for breach notification

R = Responsible, A = Accountable, C = Consulted, I = Informed.

| Actor | Detection & triage | Severity scoring (S1–S4) | DPC notification (Art. 33(1)) | Customer-controller notification (Art. 33(2)) | Individual communication (Art. 34(1)) | Breach register (Art. 33(5)) |
|---|---|---|---|---|---|---|
| Samir Haddad, CISO | R/A (24/7 on-call) | C | I | I | I | C |
| Mara Okafor, Head of Privacy Operations | C | R/A (INT-Q-BREACH) | R (drafts) | C | R (drafts notice) | R (maintains) |
| Tomás Reyes, DPO | I | C | A (signs off before submission) | C | A | A |
| Aoife Brennan, Senior Privacy Counsel | I | C | C | C | R (reviews notice) | C |
| Owen Gallagher, Customer Support | I | I | I | R (issues via HelpHub) | R (inbound handling) | I |
| Lena Fischer, VP Engineering | R (detection-gap review) | I | I | I | I | I |
| Internal Audit | I | I | I | I | I | R (quarterly review) |

### 2.2 Key responsibilities

- **Samir Haddad (CISO)** owns breach detection: Beacon and Atlas alert rules feed a 24/7 security on-call rotation, with an internal target mean time to detect of 1 hour for S1/S2-classified incidents.
- **Mara Okafor (Head of Privacy Operations)** owns the PrivacyDesk queue INT-Q-BREACH, where all suspected breaches are triaged. The triage SLA is initial assessment within 2 hours of the ticket being raised during business hours, and within 6 hours outside business hours. She also maintains the internal S1–S4 severity matrix.
- **Tomás Reyes (DPO)** signs off every Article 33(1) notification to the DPC before submission via the DPC portal. Acme's internal target is submission within 48 hours of awareness, stricter than the 72-hour legal deadline.
- **Aoife Brennan (Senior Privacy Counsel)** reviews every draft Article 34(1) communication to affected individuals before it is issued from privacy@acme.example.
- **Owen Gallagher (Customer Support)** issues processor-side notifications to affected customer-controllers using HelpHub templates (internal target: 4 hours from awareness, ahead of the 24-hour contractual commitment) and staffs inbound individual questions in HelpHub.
- **Lena Fischer (VP Engineering)** owns detection-gap reviews: any breach discovered by means other than automated Beacon or Atlas alerting (e.g. a manual report) is flagged for review within 10 working days.
- **Internal Audit** reviews quarterly extracts of the Vault breach register.

### 2.3 Contact point

Suspected breaches may be reported to privacy@acme.example, monitored by the office of the Data Protection Officer, Tomás Reyes.

## 3. Detection and Triage

### 3.1 Automated detection (Beacon and Atlas)

Samir Haddad (CISO) owns breach detection. Alert rules configured on the Beacon platform and the Atlas analytics warehouse feed the 24/7 security on-call rotation. The internal target for mean time to detect is **1 hour** for incidents classified S1 or S2 under the severity matrix maintained by Mara Okafor's team. On-call responders document the initial detection timestamp in the incident record; this timestamp starts the awareness clock for the Article 33(1) 72-hour deadline and the internal 48-hour DPC notification target.

### 3.2 Manual reports

Suspected personal data breaches may be reported by any employee, customer or third party to **privacy@acme.example**, which is monitored by the office of the Data Protection Officer, Tomás Reyes (F-BRE-05). Reports arriving by any other manual means (e.g. a support ticket in HelpHub or a direct report to a team member) are routed to the same queue.

- [ ] On receipt of a manual report, raise a ticket in the PrivacyDesk queue **INT-Q-BREACH**, owned by Mara Okafor (F-BRE-06).
- [ ] Record the time the report was received; this is the awareness timestamp for the 72-hour clock.

### 3.3 Triage SLA

All suspected breaches are triaged in INT-Q-BREACH (F-BRE-06):

| Report received | Initial assessment SLA |
|---|---|
| During business hours | Within 2 hours of the ticket being raised |
| Outside business hours | Within 6 hours of the ticket being raised |

Initial assessment determines whether the incident meets the Article 4(12) definition of a personal data breach and assigns a provisional severity score (S1–S4) using form INT-FORM-11. Only S1 and S2 classifications trigger the 72-hour Article 33(1) clock and this runbook's notification stages.

### 3.4 Detection-gap review

If a breach is discovered by any means other than the automated alerting in Beacon or Atlas (e.g. a manual report), flag the incident for a **detection-gap review** by Lena Fischer's Engineering organisation within **10 working days** (F-BRE-14). Record the flag in the INT-Q-BREACH ticket so the review outcome feeds back into alert-rule tuning.

## 4. Severity Assessment and the 72-Hour Clock

### 4.1 Severity scoring (S1–S4)

Every suspected personal data breach triaged in INT-Q-BREACH is scored S1–S4 using the internal severity matrix maintained by Mara Okafor's team, Privacy Operations (F-BRE-07):

| Severity | Definition | Article 33(1) clock | DPC notification |
|---|---|---|---|
| S1 | High risk to individuals' rights and freedoms | Starts — 72-hour deadline | Mandatory |
| S2 | Risk to individuals' rights and freedoms | Starts — 72-hour deadline | Case-by-case, decided with the DPO |
| S3 | No likely risk to individuals | Does not start | Not required |
| S4 | Near miss / no personal data involved | Does not start | Not required |

Only S1 and S2 classifications trigger the 72-hour Article 33(1) clock and the notification stages of this runbook. S3 and S4 incidents are still documented in the breach register under Article 33(5) (see Section 6) but do not trigger DPC notification.

### 4.2 Recording the assessment on INT-FORM-11

The severity assessment is recorded on form **INT-FORM-11 (Breach Assessment Record)**, which captures the content required by Article 33(3) (F-BRE-10):

- [ ] Nature of the breach (e.g. unauthorised disclosure, loss, alteration — per Article 4(12))
- [ ] Categories and approximate numbers of data subjects affected
- [ ] Categories and approximate numbers of personal data records affected
- [ ] DPO contact details (Tomás Reyes, DPO office)
- [ ] Likely consequences for the affected individuals
- [ ] Measures taken or proposed to address the breach

The completed INT-FORM-11 is attached to the INT-Q-BREACH ticket and forms the basis of the DPC notification content.

### 4.3 The 72-hour clock and the 48-hour internal target

For S1 and S2 breaches, GDPR Article 33(1) requires notification to the Irish Data Protection Commission (DPC), Acme's lead supervisory authority, without undue delay and, where feasible, no later than **72 hours** after Acme becomes aware of the breach. Acme's internal target is stricter: submission of the Article 33(1) notification within **48 hours** of awareness (F-BRE-08).

- [ ] Record the awareness timestamp (detection or manual-report receipt) in the INT-Q-BREACH ticket at triage.
- [ ] Set the internal 48-hour submission deadline in the ticket immediately on S1/S2 classification.
- [ ] Draft the notification from the completed INT-FORM-11.
- [ ] Obtain sign-off from Tomás Reyes, DPO, before submission. The DPO signs off every notification before it is submitted via the DPC portal.
- [ ] Submit via the DPC portal and record the submission timestamp in the ticket.

If notification cannot be provided within 72 hours, Article 33(1) requires the reasons for the delay to be given to the DPC.

### 4.4 Phased information (Article 33(4))

Where and insofar as it is not possible to provide all Article 33(3) information at the same time, Article 33(4) allows the information to be provided in phases without undue further delay. If full detail (e.g. approximate numbers of affected records) is not yet available at the 48-hour internal target, submit the initial notification with the information held, and supplement it via the DPC portal as the investigation progresses. Phase the information in consultation with Tomás Reyes, DPO, and Aoife Brennan, Senior Privacy Counsel; do not delay the initial submission to await complete detail.

## 5. DPC Notification Procedure (Article 33(1))

This section applies to breaches classified **S1 or S2** under the severity matrix (see Section 4.1). Only these classifications trigger the 72-hour Article 33(1) clock. S1 breaches require mandatory DPC notification; S2 breaches require notification case-by-case, decided with the DPO, Tomás Reyes.

### 5.1 Steps

1. Confirm the awareness timestamp recorded in the INT-Q-BREACH ticket at triage (see Sections 3.2–3.3) and calculate the deadlines: **48-hour internal target** and the **72-hour legal maximum** under Article 33(1).
2. Assemble the completed INT-FORM-11 (Breach Assessment Record) from the ticket. The form must contain all Article 33(3) content items listed in Section 5.2.
3. Draft the DPC notification from the INT-FORM-11 content. Privacy Operations (Mara Okafor's team) drafts; Aoife Brennan, Senior Privacy Counsel, is consulted on wording.
4. Send the draft to Tomás Reyes, DPO, for sign-off. The DPO signs off **every** notification before submission — no notification goes to the DPC without his approval.
5. Submit the signed-off notification via the **DPC portal** and record the submission timestamp in the INT-Q-BREACH ticket.
6. If full Article 33(3) detail is not yet available at the 48-hour internal target, submit the initial notification with the information held and supplement it in phases under Article 33(4) (see Section 4.4). Do not delay the initial submission to await complete detail.
7. If submission will pass the 72-hour legal maximum, prepare the **reasons for the delay** for inclusion with the notification, as Article 33(1) requires.

### 5.2 Article 33(3) content checklist

- [ ] Nature of the breach (per Article 4(12): unauthorised disclosure, loss, alteration, destruction, or access)
- [ ] Categories and approximate numbers of data subjects affected
- [ ] Categories and approximate numbers of personal data records affected
- [ ] DPO contact details (Tomás Reyes, DPO office)
- [ ] Likely consequences for affected individuals
- [ ] Measures taken or proposed to address the breach

### 5.3 Record

File the signed-off draft, the DPC portal submission confirmation and the submission timestamp in the INT-Q-BREACH ticket. These feed the Article 33(5) breach register (Section 6).

## 6. Customer-Controller Notification (Processor-Side Breaches)

This section applies to breaches affecting customers' end-user data stored in the Acme Beacon platform, where Acme acts as **processor**. Because Acme acts as a processor for its customers' end-user data in Beacon, Acme's Data Processing Agreement commits it to notify the affected customer (as controller) without undue delay after becoming aware of any personal data breach, per GDPR Article 33(2) and the Data Processing Addendum (PUB-DPA-001). The contractual commitment in the standard DPA is 24 hours; Acme's internal target is stricter: notify the affected customer-controller within **4 hours of awareness**.

### 6.1 Steps

1. On S1/S2 classification of a Beacon customer-data breach, identify the affected customer (controller) from the incident record in the INT-Q-BREACH ticket.
2. Owen Gallagher's Customer Support team issues the notification using the approved **HelpHub breach-notification template**. The internal target is **4 hours from the awareness timestamp** recorded at triage (Section 3).
3. Record the notification timestamp and the HelpHub ticket reference in the INT-Q-BREACH ticket.
4. Do not include details of other customers' data or Acme's internal remediation detail beyond what the controller needs to meet its own Article 33 obligations.

### 6.2 Notification content checklist

- [ ] Confirmation that a personal data breach affecting the customer's end-user data in Beacon has occurred
- [ ] Date and time of awareness and, where known, of the breach itself
- [ ] Nature of the breach and categories of data affected
- [ ] Approximate number of affected data subjects and records, where known
- [ ] Likely consequences and measures taken or proposed
- [ ] Contact point for follow-up questions (privacy@acme.example)

### 6.3 Record

File the sent notification and HelpHub ticket reference in the INT-Q-BREACH ticket; these feed the Article 33(5) breach register (Section 7).

## 7. Communicating to Affected Individuals (Article 34(1))

This section applies to breaches classified **S1** under the severity matrix (Section 4.1), where the breach is likely to result in a **high risk** to affected individuals. In those cases Acme communicates the breach to the affected individuals without undue delay, as required by GDPR Article 34(1) (F-BRE-02). Communication is not required for S2, S3 or S4 breaches unless the severity assessment is revised upward.

### 7.1 Steps

1. Confirm the S1 classification and the high-risk determination recorded on INT-FORM-11 in the INT-Q-BREACH ticket.
2. Privacy Operations (Mara Okafor's team) drafts the individual notice, covering the nature of the breach, the categories of data affected, likely consequences, and measures taken or proposed.
3. Send the draft to Aoife Brennan, Senior Privacy Counsel, for review before issue.
4. Issue the approved notice **by email from privacy@acme.example** (F-BRE-12). Record the issue timestamp in the INT-Q-BREACH ticket.
5. Owen Gallagher's Customer Support team staffs the resulting inbound questions in HelpHub.

### 7.2 Article 34(3) exemptions

Before issuing the notice, check with Aoife Brennan whether an Article 34(3) exemption applies:

- [ ] The affected personal data was unintelligible (e.g. rendered unintelligible by strong encryption)
- [ ] Subsequent measures ensure the high risk is no longer likely to materialise
- [ ] Communication would involve disproportionate effort — in that case, issue a **public communication** instead

Document the exemption decision and its grounds in the INT-Q-BREACH ticket; the decision feeds the Article 33(5) breach register (Section 8).

## 8. Breach Register and Documentation (Article 33(5))

Acme Corp Ltd documents **every** personal data breach — including its facts, effects and the remedial action taken — whether or not the breach is reported to the Irish Data Protection Commission (DPC) or communicated to individuals, in line with GDPR Article 33(5) (F-BRE-04). This section therefore applies to all severities, S1 through S4, including near misses classified S4.

### 8.1 Register location and retention

The complete breach register required by Article 33(5) is maintained in **Vault**, Acme's write-once immutable backup system (F-BRE-13). Because Vault backups are write-once, entries cannot be altered after creation, supporting the controller's Article 5(2) accountability obligation.

| Record | System | Retention period | Owner |
|---|---|---|---|
| Breach register entry (facts, effects, remedial action) | Vault (write-once) | 5 years per entry | Mara Okafor, Privacy Operations |
| INT-Q-BREACH ticket, INT-FORM-11, notification records | PrivacyDesk | Duration of the incident lifecycle, then copied to Vault | Mara Okafor, Privacy Operations |
| Quarterly extract review records | Internal Audit files | Current year plus 2 years | Internal Audit |

### 8.2 Quarterly audit review

The Internal Audit team reviews **quarterly extracts** of the Vault breach register (F-BRE-13). The review confirms that every INT-Q-BREACH ticket closed in the quarter has a corresponding register entry and that S3/S4 incidents are documented even though they do not trigger notification.

### 8.3 Closure checklist

Complete before closing any INT-Q-BREACH ticket:

- [ ] INT-FORM-11 (Breach Assessment Record) completed with all Article 33(3) content
- [ ] Facts, effects and remedial action recorded
- [ ] DPC notification decision documented (S1/S2), including reasons if not notified
- [ ] Customer-controller notification (processor-side breaches) and any Article 34(1) communication or Art. 34(3) exemption decision recorded
- [ ] Detection-gap review flagged and outcome noted, where applicable
- [ ] Register entry written to Vault and 5-year retention confirmed

## 9. Exceptions, Records and Related Documents

### 9.1 Exceptions

- **Delayed DPC notification.** If the Article 33(1) notification to the DPC cannot be submitted within the 72-hour legal maximum, the reasons for the delay must accompany the notification, as Article 33(1) requires. The internal 48-hour target does not remove this obligation.
- **S3 and S4 breaches.** S3 (no likely risk) and S4 (near miss / no personal data) breaches do not trigger the 72-hour clock or DPC notification, but they are still documented in the Vault breach register with facts, effects and remedial action, per Article 33(5) (F-BRE-04).
- **Article 34(3) exemptions.** Where individual communication is exempted (unintelligible data, mitigated risk, or disproportionate effort requiring public communication), the decision and its grounds are documented in the INT-Q-BREACH ticket (see Section 7.2).

### 9.2 Records generated by this runbook

| Record | System | Retention | Owner |
|---|---|---|---|
| INT-FORM-11 (Breach Assessment Record) (F-BRE-10) | PrivacyDesk | Incident lifecycle, then Vault | Mara Okafor |
| INT-Q-BREACH tickets | PrivacyDesk | Incident lifecycle, then Vault | Mara Okafor |
| Breach register entries (F-BRE-13) | Vault (write-once) | 5 years | Mara Okafor |
| DPC portal receipts and signed-off drafts | PrivacyDesk / Vault | Copied to Vault | Tomás Reyes |
| HelpHub customer-controller notification logs | HelpHub | Per HelpHub retention | Owen Gallagher |

### 9.3 Related documents

- **INT-IRP-001 v4.0** — Security Incident Response Plan (detection, triage, severity scoring, notification lifecycle).
- **PUB-DPA-001 v4.1** — Acme Customer Data Processing Addendum (processor breach-notification duties, effective 2026-02-01).
