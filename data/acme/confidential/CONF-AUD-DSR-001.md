---
doc_id: "CONF-AUD-DSR-001"
title: "Internal Audit Report: Data Subject Request SLA Compliance (H1 2026)"
company: "Acme Corp"
publisher: "ACME"
access_level: 2
classification: "confidential"
doc_type: "audit_report"
profile: "company_doc"
topic: "erasure"
topics: ["erasure", "access", "processors"]
owner: "Internal Audit"
approver: "Head of Internal Audit"
version: "1.0"
effective_date: "2026-08-05"
status: "current"
gdpr_articles: [12, 17, 28]
related: ["INT-SOP-ERASE-002", "INT-SOP-DSAR-001"]
generator: {"writer": "@cf/zai-org/glm-5.3", "judge": "@cf/openai/gpt-oss-120b", "run_id": "20261124-025609", "prompt_hash": "284162f9dd75"}
review: {"status": "ok", "attempts": 1, "issues_left": 0, "scores": {"fact_fidelity": 5, "tier_discipline": 5, "gdpr_accuracy": 5, "realism": 5, "retrievability": 5}}
---

# Internal Audit Report: Data Subject Request SLA Compliance (H1 2026)

| Field | Detail |
|---|---|
| Document ID | CONF-AUD-DSR-001 |
| Version | 1.0 |
| Owner | Internal Audit (Kwame Mensah, Head of Internal Audit) |
| Approver | Head of Internal Audit |
| Effective date | 2026-08-05 |
| Classification | CONFIDENTIAL |
| Status | Current |
| Audience | Audit Committee and executive leadership |
| GDPR articles in scope | Art. 12, Art. 17, Art. 28 |

## 1. Executive Summary

Internal Audit reviewed Acme Corp's compliance with its data subject request (DSR) service-level commitments for the period January–June 2026, covering erasure requests handled in the PrivacyDesk queue INT-Q-ERASE under INT-SOP-ERASE-002. The review was performed by Internal Audit (Kwame Mensah) against Acme's internal SLA of 20 calendar days from identity verification to complete erasure — an internal target stricter than the one-month statutory deadline in Article 12(3) GDPR — and against the statutory deadline itself.

**Key findings:**

- **14% of erasure requests in the audited period exceeded the 20-day internal SLA.** All breaching requests were nevertheless completed within the statutory one month, meaning Acme met its Article 12(3) GDPR obligation in every case.
- **The Atlas deletion job was identified as the main cause of SLA breaches.** The nightly job has a known defect: it fails on records with more than 500 linked event rows, requiring manual re-runs by the Data Platform team and adding an average of 6 days to affected tickets.
- **Remediation has been approved and funded.** Following this finding, the executive team approved a remediation budget of EUR 180,000 to rewrite the Atlas deletion job, with a target of full erasure execution within 5 days of trigger by Q1 2027.

**Overall conclusion:** Acme's erasure-request process is compliant with the statutory one-month deadline under Article 12(3) GDPR, but the 20-day internal SLA is not being reliably met, and the Atlas deletion job defect is a recurring, systemic cause. Repeated internal SLA breaches create a risk of complaints to the Irish Data Protection Commission under Article 77 GDPR and associated Article 83(5) exposure. The funded remediation addresses the root cause, and its delivery by Q1 2027 should be tracked by the Audit Committee.

Detailed findings, evidence and management responses are set out in the remainder of this report.

## 2. Scope, Objectives and Methodology

### 2.1 Audit Period and Population

The audit covered the period 1 January 2026 to 30 June 2026 (H1 2026). The audited population comprised all data subject requests logged in the PrivacyDesk queue INT-Q-ERASE (erasure requests) and the queue INT-Q-DSAR (access and portability requests) during that period. Erasure requests were the primary focus of detailed SLA testing; the INT-Q-DSAR population was included to confirm intake, logging and identity-verification controls operated consistently across DSR types.

### 2.2 Objectives

The audit objectives were to:

1. Assess whether erasure requests were completed within Acme's internal SLA of 20 calendar days from identity verification to complete erasure — stricter than the one-month statutory deadline in Article 12(3) GDPR (per INT-SOP-ERASE-002).
2. Assess whether all requests were in any event completed within the one-month statutory deadline in Article 12(3) GDPR.
3. Identify the root causes of any SLA breaches, including system-level causes in the deletion pipeline (Beacon, Ledger, Atlas, HelpHub).
4. Evaluate the operation of supporting controls: intake form INT-FORM-03 (account ID, systems to be checked, identity evidence), identity verification per EDPB Guidelines 01/2022 principles, escalation of unverified identities to the DPO within 5 business days under Article 12(6) GDPR, and application of the Article 17(3) exception checklist INT-CHK-ERASE.

### 2.3 SLA Criteria Tested

- **Internal criterion:** 20 calendar days from identity verification to complete erasure, measured per ticket in INT-Q-ERASE. Only verified requests start the SLA clock.
- **Statutory criterion:** one month from receipt of the request, per Article 12(3) GDPR, as stated in Acme's privacy notice.

### 2.4 Sampling Approach

Internal Audit tested the full population of erasure tickets closed in H1 2026 for SLA measurement, and selected a risk-based sample of tickets for detailed control testing, weighting selection toward tickets that breached day 14 (escalation trigger to the Privacy Operations lead) and tickets involving Atlas deletion job re-runs.

### 2.5 Evidence Sources

- PrivacyDesk ticket records in INT-Q-ERASE and INT-Q-DSAR, including verification timestamps, Vault backup expiry dates and Art. 19 notification records.
- Atlas deletion job logs, including failure and manual re-run events.
- Completed exception checklists INT-CHK-ERASE and intake forms INT-FORM-03.
- Escalation records to the DPO (Tomás Reyes) and to VP Engineering (Lena Fischer) for day-20 breaches.

### 2.6 Standards Applied

Testing was performed against Articles 12, 17 and 28 GDPR and the identity-verification principles in EDPB Guidelines 01/2022, and against INT-SOP-ERASE-002 and INT-SOP-DSAR-001 as the governing internal procedures.

## 3. Background: DSLA Framework and Systems

This section describes the erasure-request operating model that Internal Audit tested in H1 2026, as designed in INT-SOP-ERASE-002.

### 3.1 Intake Channels

Data subject deletion requests reach Privacy Operations through two channels: the privacy@acme.example mailbox and the self-service Beacon Settings > Privacy page, where account holders can delete their own account data. All requests are logged in the PrivacyDesk queue INT-Q-ERASE, with intake form INT-FORM-03 capturing the requester's account ID, the systems to be checked (Beacon, Ledger, Atlas, HelpHub) and identity evidence.

### 3.2 Identity Verification and the SLA Clock

Identity verification follows the principles in EDPB Guidelines 01/2022 and is performed by Mara Okafor's Privacy Operations team. Only verified requests start the 20-day internal SLA clock. Requests where identity cannot be confirmed within 5 business days are escalated to the DPO, Tomás Reyes, for a decision under Article 12(6) GDPR.

### 3.3 Ordered Deletion Sequence

Once a request is verified, deletion jobs execute in a fixed order across four systems:

1. **Beacon** — account and profile data deleted within 3 days.
2. **Ledger** — billing records flagged for legal-exception review.
3. **Atlas** — event and billing history deleted via the Atlas deletion job.
4. **HelpHub** — support tickets deleted within 5 days.

### 3.4 Article 17(3) Exception Handling

Erasure is executed except where the exception checklist INT-CHK-ERASE applies. Ledger invoices are retained for 6 years under Irish tax law (Art. 17(3)(b)), and data subject to a legal hold is excluded (Art. 17(3)(e)). Where a refusal applies, the data subject is informed of the reasons under Article 12(4) GDPR within one month.

### 3.5 Article 19 Recipient Notifications

For verified erasure requests, third-party notifications under Article 19 GDPR are sent to Stripe (payer data) and to any sub-processors listed in the current sub-processor register within 10 calendar days of execution, using notification template INT-TPL-19.

### 3.6 Vault Backup Expiry Tracking

Vault, Acme's immutable backup system, retains write-once backups for 35 days. Erasure cannot be executed inside Vault; deletion propagates automatically only when each backup expires. Privacy Operations records the expiry date on the ticket in INT-Q-ERASE.

### 3.7 Escalation Rules

Two escalation triggers operate against the 20-day internal SLA:

| Trigger | Escalation target |
|---|---|
| Day 14 of the 20-day SLA | Privacy Operations lead |
| Day 20 (SLA breach) | Weekly report to the DPO (Tomás Reyes) and VP Engineering (Lena Fischer) for system-level causes |

These escalation records, together with Atlas deletion job logs, formed the primary evidence base for the findings in Section 4.

## 4. Findings

Findings are rated High, Medium or Low based on the potential impact on Acme's GDPR compliance and on its public commitments. Each finding includes the evidence Internal Audit obtained, the relevant GDPR articles, and the management response received.

### 4.1 Finding 1 (High): 14% of erasure requests exceeded the 20-day internal SLA

**Rating: High**

Internal Audit measured the full population of erasure tickets closed in INT-Q-ERASE during H1 2026 against the internal SLA of 20 calendar days from identity verification to complete erasure. **14% of erasure requests in the audited period exceeded the 20-day internal SLA.** All breaching requests were nevertheless completed within the statutory one month, so Acme met its Article 12(3) GDPR obligation in every case.

**Evidence:**

- SLA measurement of the full H1 2026 INT-Q-ERASE closed-ticket population, comparing verification timestamps to completion timestamps.
- Day-14 escalation records to the Privacy Operations lead and weekly day-20 breach reports to the DPO (Tomás Reyes) and VP Engineering (Lena Fischer), reconciled against the ticket population.
- One breached ticket in the period reached 27 days (7 days over the internal SLA); Internal Audit notes that a complaint to the Irish DPC from this data subject was subsequently lodged in September 2026 and is being handled separately.

**Why this matters:** Acme's internal SLA is deliberately stricter than the one-month statutory deadline in Article 12(3) GDPR, and the SLA is the buffer that protects statutory compliance. Repeated SLA breaches erode that buffer and create a risk of complaints to the Irish DPC under Article 77 GDPR, with associated Article 83(5) exposure (up to EUR 20 million or 4% of turnover for infringements of Articles 12-22). The September 2026 DPC complaint demonstrates this risk is materialising.

**Management response:** The executive team has approved a remediation budget of EUR 180,000 to rewrite the Atlas deletion job, targeting full erasure execution within 5 days of trigger by Q1 2027 (see Finding 2).

### 4.2 Finding 2 (High): Atlas deletion job defect is the root cause of SLA breaches

**Rating: High**

The Atlas deletion job, which deletes event and billing history from the Atlas warehouse, runs nightly but has a known defect: **it fails on records with more than 500 linked event rows**. Failed runs must be manually re-run by the Data Platform team, which **adds an average of 6 days to affected tickets**. Internal Audit identified the Atlas deletion job as the main cause of the H1 2026 SLA breaches.

**Evidence:**

- Atlas deletion job logs for H1 2026, showing failure events on records exceeding 500 linked event rows and subsequent manual re-runs by the Data Platform team.
- Correlation of job-failure events with breached INT-Q-ERASE tickets: tickets affected by a failed Atlas run accounted for the majority of the 14% SLA breach population in Section 4.1.
- Day-20 breach reports to the DPO and VP Engineering identifying Atlas as the system-level cause.

**Why this matters:** The defect is systemic and recurring: any data subject with a high-volume event history is exposed to a delayed erasure. Because the delay averages 6 days against a 20-day SLA, affected tickets routinely consume the entire internal buffer and depend on the statutory one-month headroom to remain compliant.

**Management response:** Funded remediation of EUR 180,000 to rewrite the Atlas deletion job, owned by Engineering (Lena Fischer), with a target of full erasure execution within 5 days of trigger by Q1 2027. Internal Audit will track delivery as a follow-up action.

### 4.3 Finding 3 (Medium): Erased data persists in Vault immutable backups for up to 35 days

**Rating: Medium**

Erasure cannot be executed inside Vault, Acme's write-once backup system with 35-day retention. Deleted data therefore persists in Vault backups until each backup expires, up to 35 days after erasure execution. Privacy Operations correctly records the expiry date on each ticket in INT-Q-ERASE, and access to restored Vault data for erasure-related purposes is restricted by the CISO (Samir Haddad).

**Evidence:**

- INT-Q-ERASE ticket records showing Vault expiry dates recorded per ticket.
- Board resolution CONF-BRD-2026-06-R3, adopted 12 June 2026, formally accepting the residual risk that personal data of subjects whose erasure requests are granted remains in Vault for up to 35 days after execution.
- The minuted dissent of the DPO, Tomás Reyes, who argued that the 35-day retention should be disclosed in the privacy notice and that Acme should evaluate a shorter backup retention period or an encryption-key destruction approach.
- The legal memo of 3 June 2026 by Aoife Brennan (CONF-MEMO-2026-ERASE), concluding that Vault's 35-day immutable retention is defensible as an Article 32 / Article 5(1)(f)-style security backup practice, but only if Acme does not access restored backups to resurrect erased profiles.

**Why this matters:** The residual risk is formally accepted at board level, but the DPO's dissent on privacy-notice disclosure remains unresolved. Undisclosed retention of erased data is a transparency exposure under Articles 12 and 13 GDPR if a data subject or the DPC challenges it.

**Management response:** Management points to the board acceptance in CONF-BRD-2026-06-R3 and the CISO access restriction. Internal Audit recommends the Audit Committee consider the DPO's disclosure recommendation.

### 4.4 Finding 4 (Medium): Governance context — churn-analytics retention proposal in Atlas

**Rating: Medium**

Internal Audit notes, as governance context, a Q2 2026 executive discussion (recorded as CONF-RISK-07) initiated by Helen Zhou (CFO) and Julia Moreau (Product Director, Beacon AI) on retaining deleted customers' billing history in Atlas for churn analytics. Priya Raman (General Counsel) advised that retaining raw identifiers for analytics after erasure could conflict with Article 17(1)(a) and Article 5(1)(e) GDPR.

**Evidence:**

- CONF-RISK-07 risk-register entry recording the discussion and the General Counsel's advice.
- The closure of CONF-RISK-07 in August 2026 with a decision to pseudonymise rather than retain raw identifiers in Atlas analytics, implementation owned by Lena Fischer, with a compliance review by Aoife Brennan due by 31 January 2027.

**Why this matters:** The proposal, had it proceeded with raw identifiers, would have directly undermined the erasure pipeline that is the subject of Findings 1 and 2. The pseudonymisation decision is the correct outcome, but it is not yet implemented, and the compliance review is not due until 31 January 2027.

**Management response:** Management confirmed the pseudonymisation implementation is in progress under Lena Fischer and that the Aoife Brennan compliance review is scheduled. Internal Audit will verify completion as part of its 2027 follow-up.

## 5. Regulatory Exposure Assessment

### 5.1 Complaint Risk and Fine Exposure

The 14% internal SLA breach rate in H1 2026, with the Atlas deletion job defect as the main cause, creates a risk of complaints to the Irish Data Protection Commission under Article 77 GDPR. Where a complaint is upheld, the DPC may apply the Article 83(2) factors — including the systemic character and duration of the SLA breaches — when setting any fine. Infringements of Articles 12–22 fall in the highest fine band under Article 83(5): up to EUR 20 million or 4% of total worldwide annual turnover, whichever is higher. This exposure is the stated rationale for the executive team's approval of a remediation budget of EUR 180,000 to rewrite the Atlas deletion job, targeting full erasure execution within 5 days of trigger by Q1 2027 (F-ERA-21).

### 5.2 The September 2026 DPC Complaint

This risk has materialised. In September 2026, one data subject whose erasure request took 27 days — 7 days over the 20-day internal SLA — complained to the Irish DPC. Acme's response, led by Aoife Brennan and tracked as CONF-INC-2026-0901, relies on the fact that the request was completed within the one-month statutory deadline in Article 12(3) GDPR (F-ERA-22). Internal Audit notes that while this position is legally sound — the internal SLA is a self-imposed commitment stricter than the law — the complaint demonstrates that data subjects experience the 27-day outcome as a delay, and repeated complaints of this kind would attract DPC scrutiny of the erasure pipeline as a whole, including the Atlas defect.

### 5.3 Vault Backup Retention

The persistence of erased data in Vault immutable backups for up to 35 days after execution carries Article 5(1)(e) storage-limitation and transparency implications. Aoife Brennan's legal memo of 3 June 2026 (CONF-MEMO-2026-ERASE) concluded that the 35-day write-once retention is defensible as an Article 32 / Article 5(1)(f)-style security backup practice, but only on the condition that Acme does not access restored backups to resurrect erased profiles; access to restored Vault data for erasure-related purposes is restricted by the CISO, Samir Haddad (F-ERA-23). The board formally accepted this residual risk in CONF-BRD-2026-06-R3, against the minuted dissent of the DPO, Tomás Reyes, who argued that the 35-day retention should be disclosed in the privacy notice and that Acme should evaluate a shorter retention period or encryption-key destruction (F-ERA-18). If the DPC were to examine the Vault issue — for example, through the September 2026 complaint — the absence of privacy-notice disclosure would weaken Acme's transparency position under Articles 12 and 13 GDPR, notwithstanding the board's formal risk acceptance.

### 5.4 Overall Assessment

Internal Audit assesses the current regulatory exposure as **medium**: statutory compliance was maintained in all H1 2026 cases, but the materialised DPC complaint, the unresolved DPO dissent on Vault disclosure, and the Atlas defect remediation not due until Q1 2027 leave a window in which further complaints could escalate exposure under Article 83(5).

## 6. Management Responses and Remediation Plan

### 6.1 Summary of Management Responses

| Finding | Rating | Management response | Accepted by Internal Audit |
|---|---|---|---|
| 4.1 — 14% of erasure requests exceeded the 20-day internal SLA | High | Funded Atlas deletion job rewrite (Section 6.2) | Yes, with follow-up tracking |
| 4.2 — Atlas deletion job defect (fails on >500 linked event rows) | High | Same remediation; interim manual re-run controls (Section 6.4) | Yes |
| 4.3 — Erased data persists in Vault backups for up to 35 days | Medium | Board acceptance CONF-BRD-2026-06-R3; CISO access restriction; Audit Committee to consider DPO's disclosure recommendation | Yes, recommendation retained |
| 4.4 — Churn-analytics retention proposal (CONF-RISK-07) | Medium | Pseudonymisation decision (Section 6.3) | Yes, with 2027 verification |

### 6.2 Atlas Deletion Job Rewrite (Findings 1 and 2)

The executive team has approved a remediation budget of **EUR 180,000** to rewrite the Atlas deletion job, eliminating the defect that causes failures on records with more than 500 linked event rows (F-ERA-15, F-ERA-21). The target is **full erasure execution within 5 days of trigger, by Q1 2027**. This is the principal remediation addressing the root cause of the 14% internal SLA breach rate. Internal Audit will track delivery as a follow-up action and report to the Audit Committee.

### 6.3 Atlas Pseudonymisation Implementation (Finding 4)

CONF-RISK-07 was closed in August 2026 with a decision to pseudonymise rather than retain raw identifiers in Atlas analytics (F-ERA-20). Implementation is owned by **Lena Fischer (VP Engineering)**, with a compliance review by **Aoife Brennan (Senior Privacy Counsel) due by 31 January 2027**. Internal Audit will verify completion of both the implementation and the compliance review during its 2027 follow-up.

### 6.4 Interim Controls (Q3 2026 – Q1 2027)

Until the rewritten Atlas deletion job is delivered, the following interim controls apply to erasure requests in INT-Q-ERASE:

- Manual re-runs of failed Atlas deletion jobs are prioritised by the Data Platform team on the day of failure notification, to limit the average 6-day delay.
- Day-14 escalation to the Privacy Operations lead and weekly day-20 breach reporting to the DPO (Tomás Reyes) and VP Engineering (Lena Fischer) continue to operate.
- Privacy Operations monitors the CONF-INC-2026-0901 DPC complaint, led by Aoife Brennan, for any pipeline-wide scrutiny signals.

### 6.5 Remediation Timeline

| Action | Owner | Due |
|---|---|---|
| Atlas deletion job rewrite (full execution within 5 days of trigger) | Lena Fischer (VP Engineering) | Q1 2027 |
| Atlas pseudonymisation implementation | Lena Fischer (VP Engineering) | In progress |
| Compliance review of pseudonymisation | Aoife Brennan (Senior Privacy Counsel) | 31 January 2027 |
| Follow-up audit verification | Internal Audit (Kwame Mensah) | 2027 |

## 7. Conclusion and Follow-up

Internal Audit's overall opinion is that Acme Corp maintained statutory compliance with the one-month deadline in Article 12(3) GDPR for all erasure requests in H1 2026, but performance against the stricter 20-day internal SLA was degraded by a known engineering defect: the Atlas deletion job's failure on records with more than 500 linked event rows, which drove the 14% internal SLA breach rate (F-ERA-16). The September 2026 DPC complaint (CONF-INC-2026-0901) shows the consequence of relying on statutory headroom, and the Article 83(5) exposure underpins the urgency of remediation.

The root-cause remediation is funded and owned: the executive team approved EUR 180,000 to rewrite the Atlas deletion job, targeting full erasure execution within 5 days of trigger by Q1 2027, under Lena Fischer (VP Engineering) (F-ERA-21). Interim controls in Section 6.4 remain in force until delivery.

**Follow-up plan:**

- **Interim follow-up (Q1 2027):** Internal Audit will confirm whether the rewritten Atlas deletion job meets the 5-day execution target and report the result to the Audit Committee.
- **H1 2027 audit cycle:** Internal Audit will re-test Atlas deletion job performance and full-population SLA compliance in INT-Q-ERASE, and verify the Atlas pseudonymisation implementation and the Aoife Brennan compliance review due by 31 January 2027.

Internal Audit (Kwame Mensah) retains ownership of this report and its follow-up actions.
