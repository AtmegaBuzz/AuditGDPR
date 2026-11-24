---
doc_id: "CONF-PIR-INC-0412"
title: "Post-Incident Review: CONF-INC-2025-0412 Misdirected CSV Export"
company: "Acme Corp"
publisher: "ACME"
access_level: 2
classification: "confidential"
doc_type: "incident_review"
profile: "company_doc"
topic: "breach"
topics: ["breach"]
owner: "Security"
approver: "CISO"
version: "1.0"
effective_date: "2025-04-30"
status: "current"
gdpr_articles: [32, 33]
related: ["INT-IRP-001", "INT-RUN-BREACH-001"]
generator: {"writer": "@cf/zai-org/glm-5.3", "judge": "@cf/openai/gpt-oss-120b", "run_id": "20261124-025609", "prompt_hash": "284162f9dd75"}
review: {"status": "ok", "attempts": 1, "issues_left": 0, "scores": {"fact_fidelity": 5, "tier_discipline": 5, "gdpr_accuracy": 5, "realism": 5, "retrievability": 5}}
---

# Post-Incident Review: CONF-INC-2025-0412 Misdirected CSV Export

| Field | Value |
|---|---|
| Document ID | CONF-PIR-INC-0412 |
| Version | 1.0 |
| Owner | Security (CISO organisation) |
| Approver | Samir Haddad, Chief Information Security Officer (CISO) |
| Effective date | 2025-04-30 |
| Classification | CONFIDENTIAL |
| Status | Current |
| Audience | Incident review board |
| Related incident | CONF-INC-2025-0412 |
| Related documents | INT-IRP-001 (Security Incident Response Plan, v4.0); INT-RUN-BREACH-001 (Personal Data Breach Notification Runbook, v2.1) |
| GDPR articles in scope | Art. 32, Art. 33 |

## 1. Document Control and Purpose

| Field | Value |
|---|---|
| Document ID | CONF-PIR-INC-0412 |
| Version | 1.0 |
| Owner | Security (CISO organisation) |
| Approver | Samir Haddad, Chief Information Security Officer (CISO) |
| Effective date | 2025-04-30 |
| Classification | CONFIDENTIAL |
| Status | Current |
| Related incident | CONF-INC-2025-0412 |
| Related documents | INT-IRP-001 (Security Incident Response Plan, v4.0); INT-RUN-BREACH-001 (Personal Data Breach Notification Runbook, v2.1) |
| GDPR articles in scope | Art. 32, Art. 33 |

### 1.1 Purpose

This document is the post-incident review of CONF-INC-2025-0412, in which a Beacon analytics CSV export containing records of approximately 12,500 end-user data subjects of one customer was misdirected to an external recipient's email address on 14 March 2025, and recalled from the recipient's inbox within 40 minutes. The review examines the timeline, root cause, impact, and remedial actions, and supports Acme's Article 33(5) obligation to document every personal data breach, its effects and the remedial action taken.

### 1.2 Scope and Audience

The review covers the detection, triage, severity assessment and containment of CONF-INC-2025-0412, including the 9-hour detection delay and the gap in Beacon alerting coverage. The intended audience is the incident review board. This document is CONFIDENTIAL and is not for external distribution.

### 1.3 Methodology

The review was conducted by the Security organisation in line with INT-IRP-001 (v4.0) and INT-RUN-BREACH-001 (v2.1). Evidence sources comprised the Beacon and Atlas logs, the INT-Q-BREACH triage ticket, form INT-FORM-11 (Breach Assessment Record), and interviews with the responding teams. Findings were validated with Engineering and Privacy Operations before publication.

## 2. Incident Summary and Timeline

### 2.1 Summary

On 14 March 2025, a Beacon analytics CSV export containing records of approximately 12,500 end-user data subjects of one Acme customer was misdirected to an external recipient's email address. Acme acts as a processor for this customer's end-user data in Beacon, so the incident constituted a personal data breach under GDPR Art. 4(12) — an accidental unauthorised disclosure of personal data. The export was recalled from the recipient's inbox within 40 minutes of the misdirection being surfaced. However, the misdirection occurred at 09:20 and was only discovered at 18:25, when the recipient replied to the message, producing a 9-hour detection delay. The root cause of the delay was that the CSV export path bypassed the Beacon alerting rules, which cover database-level access only and do not cover CSV downloads.

### 2.2 Timeline of Events (14 March 2025)

| Time | Event |
|---|---|
| 09:20 | A Beacon analytics CSV export containing records of approximately 12,500 end-user data subjects of one customer is sent to an external recipient's email address in error. No alert fires: the Beacon alerting rules cover database-level access only, and the CSV download path is outside their scope. |
| 09:20 – 18:25 | The misdirected export remains undetected for 9 hours. The 24/7 security on-call rotation receives no signal, as neither Beacon nor Atlas alerting covers the export channel. |
| 18:25 | The external recipient replies to the misdirected email, which surfaces the incident. The breach is discovered by manual report rather than by automated alerting in Beacon or Atlas. |
| 18:25 onward | The incident is raised into the PrivacyDesk queue INT-Q-BREACH for triage under the Security Incident Response Plan (INT-IRP-001) and the Personal Data Breach Notification Runbook (INT-RUN-BREACH-001). |
| Within 40 minutes of discovery | The misdirected export is recalled from the recipient's inbox. The recipient is confirmed to be a verified professional contact who subsequently confirmed deletion of the data. |

### 2.3 Detection Delay

The elapsed time between the misdirection at 09:20 and discovery at 18:25 was 9 hours, against Acme's internal target of mean time to detect of 1 hour for S1/S2-classified incidents. Because the breach was discovered by manual report (the recipient's reply) rather than by automated alerting, the incident was flagged for a detection-gap review by Lena Fischer's Engineering organisation within 10 working days, per Acme's missed-detection escalation standard. The detection gap and the remedial programme it triggered are covered in Section 4 of this review.

## 3. Detection Gap Analysis

### 3.1 Root Cause of the 9-Hour Detection Delay

The root cause of the 9-hour detection delay in CONF-INC-2025-0412 was a coverage gap in the Beacon alerting rules. Those rules are configured to cover database-level access only; the CSV export path used for analytics downloads sits outside their scope. The misdirected export at 09:20 on 14 March 2025 therefore generated no alert in either Beacon or Atlas, and the 24/7 security on-call rotation received no signal of any kind during the 9-hour exposure window. The incident was surfaced manually at 18:25 only when the external recipient replied to the misdirected email.

### 3.2 Manual Discovery and the Detection-Gap Review Obligation

Because the breach was discovered by a manual report rather than by the automated alerting in Beacon or Atlas, the incident was flagged for a detection-gap review by Lena Fischer's Engineering organisation within 10 working days, in line with Acme's missed-detection escalation standard. The review confirmed that the gap is structural: any CSV download from Beacon analytics — irrespective of recipient, volume or data category — is invisible to the alerting layer that Security relies on to meet its 1-hour mean-time-to-detect target for S1/S2-classified incidents.

### 3.3 Implications

The gap means that detection of export-channel breaches depends entirely on chance factors, such as a recipient replying, rather than on the monitoring controls described in the Security Incident Response Plan (INT-IRP-001, v4.0). For a breach of this profile — approximately 12,500 records of end-user data subjects — a 9-hour exposure window before discovery materially increases the potential consequences that must be assessed under Art. 33(3) before a notification decision is made. The remedial programme to extend alerting and Data Loss Prevention coverage to CSV export paths is set out in Section 4 of this review.

## 4. Severity Classification and Notification Decision

### 4.1 Severity Assessment: S3 (Not Notifiable)

CONF-INC-2025-0412 was assessed as **S3 (no likely risk to individuals; not notifiable)** under the internal severity matrix maintained by Mara Okafor's Privacy Operations team. The assessment was recorded on form INT-FORM-11 (Breach Assessment Record), which captures the Art. 33(3) content: the nature of the breach, the categories and approximate numbers of data subjects and records (approximately 12,500 end-user data subjects of one customer), the DPO contact details, the likely consequences, and the measures taken or proposed.

The S3 classification rested on two grounds:

- **Recipient profile.** The external recipient was a verified professional contact who confirmed deletion of the misdirected export, and the export was recalled from the recipient's inbox within 40 minutes of discovery.
- **Data category.** The exported records were low-sensitivity engagement metrics, not special-category or otherwise high-risk data.

Because the incident was scored S3, it did not trigger the 72-hour Art. 33(1) clock or the internal 48-hour DPC notification target. Under Art. 33(1), notification to the lead supervisory authority is required unless the breach is unlikely to result in a risk to the rights and freedoms of natural persons; the assessment concluded that this was such a case.

### 4.2 Supporting Legal Memorandum

The legal reasoning supporting the non-notification decision is set out in a privileged memorandum by Aoife Brennan, Senior Privacy Counsel, dated 17 March 2025. That memorandum is privileged and is withheld from the operational breach register; the register entry for CONF-INC-2025-0412 records the outcome of the classification but not the privileged analysis.

### 4.3 DPO Dissent and General Counsel Determination

DPO Tomás Reyes dissented from the S3 classification, recording in writing that the 12,500-record volume and the 9-hour exposure window warranted at least a phased notification to the Irish Data Protection Commission under Art. 33(4), which permits information to be provided in phases where it cannot all be made available at once. His dissent was noted but overruled by Priya Raman, General Counsel, on 20 March 2025. The final classification of record is therefore S3, not notifiable, with the DPO's dissent documented.

### 4.4 Documentation Under Art. 33(5)

Irrespective of the non-notification decision, the breach was fully documented — its facts, effects and remedial action — in line with Art. 33(5), which requires documentation of every personal data breach whether or not it is notified to a supervisory authority. The documentation comprises the INT-FORM-11 record, the INT-Q-BREACH triage ticket, and the entry in the Vault-based Art. 33(5) breach register (5-year retention, quarterly Internal Audit review).

## 5. What Went Well and What Went Badly

### 5.1 What Went Well

- **Rapid containment once discovered.** The misdirected CSV export was recalled from the external recipient's inbox within 40 minutes of the incident being surfaced at 18:25 on 14 March 2025, and the recipient — a verified professional contact — confirmed deletion of the data.
- **Correct process routing.** The incident was raised into the PrivacyDesk queue INT-Q-BREACH and handled under INT-IRP-001 (v4.0) and INT-RUN-BREACH-001 (v2.1), with the severity assessment recorded on form INT-FORM-11 capturing the Art. 33(3) content.
- **Full documentation despite non-notification.** The breach was documented in the Vault-based Art. 33(5) breach register with 5-year retention, and the DPO's dissent was recorded in writing rather than suppressed, preserving accountability under Art. 5(2).

### 5.2 What Went Badly

- **9-hour detection delay.** The misdirected export occurred at 09:20 and was only surfaced at 18:25, when the recipient replied. This compares against Acme's internal target of mean time to detect of 1 hour for S1/S2-classified incidents, maintained through Beacon and Atlas alert rules feeding the 24/7 security on-call rotation. Had the incident been classified S1 or S2, the delay would have been nine times the detection target.
- **Alerting blind spot.** The Beacon alerting rules cover database-level access only; the CSV download path is entirely outside their scope. Detection depended on chance — the recipient replying — rather than on the monitoring controls Security relies on. The incident was correctly flagged for a detection-gap review by Lena Fischer's Engineering organisation within 10 working days.
- **Systematic severity-matrix risk.** The review notes CONF-RISK-07, logged in the Q2 2025 risk register: the risk that Acme's severity matrix is systematically under-applied to export-channel breaches, with inherent likelihood rated 'likely' and impact 'high'. The risk owner is Samir Haddad, with mitigation due by Q4 2025. This risk was validated by the S3 classification of a 12,500-record export with a 9-hour exposure window, which the DPO considered warranted at least a phased Art. 33(4) notification to the DPC.

## 6. Remediation Actions and Governance Response

### 6.1 Board Resolution CONF-BRD-2025-06-R3: Detection-Gap Funding

Board resolution CONF-BRD-2025-06-R3, approved on 12 June 2025, allocated **EUR 180,000** to extend Beacon download alerting and Data Loss Prevention (DLP) coverage to CSV export paths, closing the detection gap identified in CONF-INC-2025-0412. The budget was signed off by Helen Zhou, Chief Financial Officer. This programme directly addresses the root cause described in Section 3: CSV downloads from Beacon analytics will no longer sit outside the alerting layer that feeds the 24/7 security on-call rotation, restoring Security's ability to meet the 1-hour mean-time-to-detect target for S1/S2-classified incidents on the export channel.

| Action | Owner | Funding / Deadline |
|---|---|---|
| Extend Beacon download alerting to CSV export paths | Lena Fischer (VP Engineering), delivery | EUR 180,000 allocated under CONF-BRD-2025-06-R3 |
| Extend DLP coverage to CSV export paths | Samir Haddad (CISO), sponsor | Approved 12 June 2025; budget signed off by Helen Zhou (CFO) |

### 6.2 Audit Committee Directive: Mandatory 24-Hour Escalation

Also under CONF-BRD-2025-06-R3, the Board's audit committee directed that **any breach where detection exceeds the 1-hour internal target must be escalated to the DPO (Tomás Reyes) and the General Counsel (Priya Raman) within 24 hours of discovery, regardless of the final severity score**. This directive is effective 1 September 2025 and responds directly to CONF-INC-2025-0412, where a 9-hour detection delay was processed at S3 without escalation to the DPO or General Counsel until the DPO raised his dissent.

The directive removes severity as a gate for escalation: a long-undetected breach must reach the DPO and General Counsel within 24 hours of discovery even if it is ultimately scored S3 or S4, ensuring that the classification debates recorded in Section 4.3 occur early rather than after the fact.

### 6.3 Residual Risk Tracking

The underlying classification risk remains tracked as CONF-RISK-07 in the Q2 2025 risk register (owner: Samir Haddad; mitigation due by Q4 2025). Progress on the CONF-BRD-2025-06-R3 remediation programme will be reported to the incident review board until the CSV export alerting and DLP coverage is live and the CONF-RISK-07 mitigation can be closed.

## 7. Residual Risk and Legal Exposure

### 7.1 Article 83(4) Exposure Assessment

The confidential 2025 year-end privacy review, conducted by Priya Raman's legal team, assessed Acme's exposure for a failure to notify under Art. 33 at up to **EUR 10 million or 2% of total worldwide annual turnover**, the ceiling for infringements of Art. 25-39 obligations set by Art. 83(4). The review further concluded that the 9-hour detection delay in CONF-INC-2025-0412 would likely have required a reasoned explanation for lateness under Art. 33(1) — which requires reasons to be given where notification is made later than 72 hours — had the breach been classified as notifiable.

### 7.2 Documentation Position Under Art. 33(5)

Acme's compliance position is strengthened by complete Art. 33(5) documentation. CONF-INC-2025-0412 is documented — its facts, effects and remedial action — in the Vault-based Art. 33(5) breach register, which is maintained in Vault, Acme's write-once immutable backup system, with each entry retained for 5 years. Quarterly extracts are reviewed by Kwame Mensah's Internal Audit team. This register demonstrates accountability under Art. 5(2) whether or not a breach is notified.

### 7.3 Residual Risk Statement

The residual risk from CONF-INC-2025-0412 is two-fold: (a) the classification risk tracked as CONF-RISK-07 (Section 6.3), under which export-channel breaches may be systematically under-scored; and (b) the detection risk that a notifiable export-channel breach could again go undetected for hours, compressing the 48-hour internal DPC notification target and triggering the Art. 33(1) lateness-explanation obligation. Both risks are mitigated by the CONF-BRD-2025-06-R3 programme and the mandatory 24-hour escalation directive effective 1 September 2025 (Section 6.2), and will remain on the incident review board's agenda until the CSV export alerting and DLP coverage is live.

## 8. Sign-off and Review Board Approval

This post-incident review of CONF-INC-2025-0412 was reviewed and approved by the incident review board and signed off by Samir Haddad, CISO, on 30 April 2025. In line with Art. 33(5) and Acme's breach-documentation standard, this review and its underlying records (INT-FORM-11, the INT-Q-BREACH ticket and the register entry) are retained in the Vault-based breach register for 5 years, subject to quarterly Internal Audit review. The incident review board will next review progress on the CONF-RISK-07 mitigation — severity-matrix under-application to export-channel breaches, owner Samir Haddad — at its follow-up before the Q4 2025 mitigation due date.
