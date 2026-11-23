---
doc_id: "CONF-DPIA-AI-001"
title: "Data Protection Impact Assessment: Beacon AI Lead Scoring"
company: "Acme Corp"
publisher: "ACME"
access_level: 2
classification: "confidential"
doc_type: "assessment"
profile: "company_doc"
topic: "dpia_ai"
topics: ["dpia_ai"]
owner: "Privacy Office"
approver: "Data Protection Officer"
version: "1.3"
effective_date: "2026-07-20"
status: "current"
gdpr_articles: [22, 35, 36]
related: ["INT-SOP-DPIA-001", "PUB-AI-001"]
generator: {"writer": "@cf/zai-org/glm-5.3", "judge": "@cf/openai/gpt-oss-120b", "run_id": "20261124-025609", "prompt_hash": "284162f9dd75"}
review: {"status": "ok", "attempts": 1, "issues_left": 0, "scores": {"fact_fidelity": 5, "tier_discipline": 5, "gdpr_accuracy": 5, "realism": 5, "retrievability": 5}}
---

# Data Protection Impact Assessment: Beacon AI Lead Scoring

| Field | Detail |
|---|---|
| Document ID | CONF-DPIA-AI-001 |
| Version | 1.3 |
| Owner | Privacy Office |
| Approver | Tomás Reyes, Data Protection Officer |
| Effective date | 2026-07-20 |
| Classification | CONFIDENTIAL |
| Status | Current |
| Audience | DPIA review board and executive leadership |
| GDPR articles in scope | Art. 22, Art. 35, Art. 36 |
| Related DPIA record | INT-DPIA-2025-07 (signed off 2025-09-12) |
| Related risk record | CONF-RISK-07 |
| Governing procedure | INT-SOP-DPIA-001 (DPIA Procedure and Screening Checklist) |
| Template | INT-FORM-12 |
| Screening record | INT-SCREEN-2025-031 (four WP248 rev.01 criteria met) |
| Product owner | Julia Moreau, Product Director, Beacon AI |
| Privacy reviewer | Aoife Brennan, Senior Privacy Counsel (Dublin) |

## 1. Document Control and Identification

| Field | Detail |
|---|---|
| Document ID | CONF-DPIA-AI-001 |
| Version | 1.3 |
| Owner | Privacy Office |
| Approver | Tomás Reyes, Data Protection Officer |
| Effective date | 2026-07-20 |
| Classification | CONFIDENTIAL |
| Status | Current |

### 1.1 Purpose

This document is the Data Protection Impact Assessment (DPIA) for the Beacon AI lead-scoring feature. It assesses the risks to individuals arising from the feature's automated profiling of sales leads, and records the mitigating measures and residual risk in accordance with Article 35 GDPR. The DPIA record itself is logged as INT-DPIA-2025-07, signed off by the DPO on 2025-09-12.

### 1.2 Scope

This DPIA covers the Beacon AI lead-scoring feature only: model training, scoring, and the downstream sales-workflow prioritisation driven by the lead score. It was triggered by screening record INT-SCREEN-2025-031, which met four WP248 rev.01 criteria (evaluation based on automated processing, systematic processing of personal aspects, profiling, and innovative use of technology), requiring a full DPIA. The assessment is drafted on template INT-FORM-12, which mirrors the four minimum content elements of Article 35(7) GDPR: systematic description of processing, necessity and proportionality assessment, risk assessment, and mitigating measures.

### 1.3 Audience

The intended audience is the DPIA review board and executive leadership.

### 1.4 Roles and Related Records

- Product owner: Julia Moreau, Product Director, Beacon AI
- Privacy reviewer: Aoife Brennan, Senior Privacy Counsel (Dublin)
- DPO and approver: Tomás Reyes
- Screening queue: INT-Q-DPIA-SCREEN
- Governing procedure: INT-SOP-DPIA-001
- Related risk record: CONF-RISK-07

## 2. Systematic Description of the Processing (Art. 35(7)(a))

### 2.1 Nature of the Processing

Beacon AI lead scoring assigns each sales lead in a customer's Acme Beacon account a predicted engagement score on a 0-100 scale. The score is produced by a machine-learning model trained only on customer-provided CRM data and consented engagement events; no special-category data under Article 9 GDPR is used as a model input. The score is used to prioritise follow-up by human sales staff.

### 2.2 Scope of the Processing

| Element | Description |
|---|---|
| Categories of data subject | Sales leads whose contact records are held in customers' Beacon accounts |
| Categories of personal data | Customer-provided CRM data and consented engagement events; derived 0-100 lead score |
| Excluded data | No Article 9 special-category data is used as a model input |
| Purposes | Predicting lead engagement and prioritising human sales follow-up |
| Systems involved | Acme Beacon (scoring and sales-workflow UI); Atlas (review-outcome logging); AWS eu-west-1 (model training and scoring) |

### 2.3 Context and Infrastructure

Model training and scoring runs in AWS eu-west-1 (Ireland). No personal data used by Beacon AI leaves the EEA, so no Chapter V transfer assessment was required for the scoring pipeline.

### 2.4 Downstream Use of the Lead Score

The lead score drives prioritisation within the Acme Beacon sales-workflow UI. Where Beacon AI flags a lead as 'low fit' — an account scored below 30 on the 0-100 scale — the account cannot be auto-closed. Instead, the human-review safeguard applies: the flagged lead must pass through a mandatory review step in the sales-workflow UI and is routed to queue INT-Q-LEAD-REVIEW, staffed by customer sales teams.

### 2.5 Human-Review Safeguard and Audit Trail

The internal SLA for INT-Q-LEAD-REVIEW is that a human reviewer acts on a flagged low-fit lead within 5 working days. The review outcome and the reviewer's identity are logged in Atlas, the internal analytics warehouse, where they are available for audit by Internal Audit.

### 2.6 Controller and Processor Roles

For its own customers' account data, Acme Corp acts as controller. Where Beacon AI processes the end-user data of Acme's customers (the sales leads), Acme Corp acts as processor and its customers remain the controllers. This DPIA addresses the processing in both capacities, and the transparency information provided to end-users via the Beacon Settings > Privacy page reflects the obligations identified in this assessment.

### 2.7 Summary

In summary, the processing under assessment is the automated profiling of sales leads to produce a 0-100 predicted engagement score from customer-provided CRM data and consented engagement events, used to prioritise human sales follow-up, with a mandatory human-review step for scores below 30, operated entirely within the EEA on AWS eu-west-1 infrastructure.

## 3. Necessity and Proportionality Assessment (Art. 35(7)(b))

### 3.1 Necessity of Lead Scoring

Beacon AI lead scoring pursues the legitimate purpose of helping Acme's customers allocate scarce sales attention to the leads most likely to engage. Manual triage of large lead volumes is slow and inconsistent; a predicted engagement score derived by automated means is a proportionate and effective way to achieve that purpose, and no less intrusive method achieves a comparable outcome. For Acme's own account data, Acme Corp relies on performance of the customer contract (Art. 6(1)(b)) as the lawful basis; where Beacon AI processes customers' end-user lead data, Acme acts as processor and the customers, as controllers, determine the lawful basis.

### 3.2 Proportionality and Data Minimisation

The processing is limited to what is necessary for the purpose. The model is trained only on customer-provided CRM data and consented engagement events, and no special-category data under Article 9 GDPR is used as a model input. No personal data used by Beacon AI leaves the EEA, so no Chapter V transfer assessment was required for the scoring pipeline. The derived 0-100 score is the minimum output needed to prioritise follow-up; it is not used for any secondary purpose.

### 3.3 Transparency

Transparency is delivered through the Beacon Settings > Privacy page, which carries a plain-language explanation of lead scoring for end-users whose data is processed by Acme's customers. This was drafted to satisfy the Article 13/14 transparency obligations identified in this DPIA, so that affected individuals understand that a score is produced, what it is used for, and that no decision about an individual is made solely by automated means.

### 3.4 Remediation of the Internal Audit Finding (CONF-AUD-2026-05)

Internal Audit review CONF-AUD-2026-05, led by Kwame Mensah, Head of Internal Audit, found that 3 of the 18 DPIAs completed in 2025 — including this DPIA (INT-DPIA-2025-07) — lacked a documented necessity and proportionality assessment meeting the Article 35(7)(b) standard at first sign-off. This section was remediated in version 1.3 of this document (effective 2026-07-20) to record the necessity and proportionality analysis set out above, addressing that finding.

## 4. Risk Assessment: Article 22 Automated Decision-Making (Art. 35(7)(c))

### 4.1 Risk Identified

The core risk recorded as CONF-RISK-07 is that the Beacon AI lead score is derived by solely automated profiling and drives decisions with similarly significant effects for individuals — loss of sales follow-up and account closure — engaging Article 22(1) GDPR. Under Article 22(1), individuals have the right not to be subject to a decision based solely on automated processing, including profiling, which produces legal or similarly significant effects. The residual risk under Article 22 was assessed as HIGH under Article 35(1), the highest residual score of any DPIA Acme has completed to date.

### 4.2 Evidence: Tension with the Public Human-Review Promise

Acme publicly commits that every lead flagged as 'low fit' can be reviewed by a human before any account is deprioritised or closed, with the Article 22(3) safeguards of human intervention, expression of a point of view, and contesting outcomes. Operational evidence shows tension with that promise:

- **SLA performance:** The internal SLA for INT-Q-LEAD-REVIEW requires a human reviewer to act on a flagged low-fit lead within 5 working days. In Q1 2026 this SLA was met for only 61% of flagged leads.
- **Routing logic:** In practice, low-fit accounts are deprioritised by routing logic before any human sees them, meaning the effective prioritisation decision is made by automated means ahead of the human-review step.

### 4.3 Dissenting View

Lena Fischer, VP Engineering, dissents from the assessment that the optional human-review step cures the Article 22(1) issue. Her recorded view is that the routing-logic deprioritisation is technically 'solely automated' in the Article 22(1) sense and cannot be cured by the optional human-review step as currently implemented. This dissent is recorded here in accordance with the requirement that DPIA review capture divergent expert views, and it is reflected in the residual risk scoring below.

### 4.4 Risk Scoring (INT-FORM-12 Scale)

Residual risks are scored on the internal 1-5 scale in INT-FORM-12 for likelihood and severity. Any residual risk scored 4 or higher on either dimension must be signed off by Tomás Reyes (DPO) before the feature can launch.

| Risk | Likelihood (1-5) | Severity (1-5) | Rating | Mitigations |
|---|---|---|---|---|
| Solely automated profiling drives account deprioritisation/closure without effective human review (Art. 22(1)) | 4 | 4 | HIGH | Mandatory review step in sales-workflow UI; INT-Q-LEAD-REVIEW queue with 5-working-day SLA; review outcomes and reviewer identity logged in Atlas for Internal Audit; Beacon Settings > Privacy transparency explanation |
| Individuals cannot in practice obtain human intervention (Art. 22(3)) | 4 | 4 | HIGH | Human-review safeguard for accounts scored below 30; routing-logic deprioritisation identified as a gap requiring remediation |

### 4.5 Residual Risk and DPO Sign-Off

After mitigation, the residual Article 22 risk is scored 4 (likelihood) x 4 (severity) on the INT-FORM-12 scale. Because this exceeds the threshold of 4 on either dimension, DPO sign-off was required before launch: Tomás Reyes signed off this DPIA (INT-DPIA-2025-07) on 2025-09-12 with the residual Article 22 risk at 4x4, the highest residual score of any DPIA Acme has completed to date.

### 4.6 Consequence of the High Residual Risk

Because the DPIA indicates a high residual risk that cannot be fully mitigated, Article 36(1) GDPR requires prior consultation with the Irish Data Protection Commission before processing. Per internal checklist INT-CHK-DPIA-04, the DPO prepares a recommendation on Article 36(1) prior consultation within 15 working days of DPIA sign-off. The Article 36 consultation decision remains unresolved as of the effective date of this version, and is addressed in section 5.

## 5. Mitigating Measures (Art. 35(7)(d))

### 5.1 Measures in Place

The following measures address the Article 22(1) risk identified in section 4:

| # | Measure | Description |
|---|---|---|
| M1 | Mandatory human-review step | Implemented in the Acme Beacon sales-workflow UI; accounts scored below 30 on the 0-100 lead score cannot be auto-closed |
| M2 | Review queue | Flagged low-fit leads must pass through INT-Q-LEAD-REVIEW, staffed by customer sales teams, with a 5-working-day SLA for reviewer action |
| M3 | Audit trail | Review outcome and reviewer identity are logged in Atlas, available for audit by Internal Audit |
| M4 | Transparency | Plain-language explanation of lead scoring on the Beacon Settings > Privacy page, satisfying the Article 13/14 obligations identified in this DPIA |
| M5 | Screening discipline | All new processing ideas, including Beacon AI, are screened against the nine WP248 rev.01 criteria via INT-Q-DPIA-SCREEN before build |

### 5.2 Effectiveness Assessment

The measures are assessed against the operational evidence in section 4.2:

- **M1 and M2 (human review):** The mandatory review step and INT-Q-LEAD-REVIEW queue give effect to the Article 22(3) safeguards Acme publicly commits to — human intervention, expression of a point of view, and contesting outcomes. However, the 5-working-day SLA for INT-Q-LEAD-REVIEW was met for only 61% of flagged leads in Q1 2026. A safeguard that operates for a minority of flagged leads within its own SLA cannot be relied on as an effective human intervention.
- **Routing logic:** In practice, low-fit accounts are deprioritised by routing logic before any human sees them. The effective prioritisation decision therefore occurs by solely automated means ahead of the review step, so M1 does not cure the Article 22(1) issue as currently implemented. This is consistent with the dissenting view of Lena Fischer, VP Engineering, recorded in section 4.3.
- **M3 (Atlas logging):** The audit trail enables monitoring of reviewer action, and it is the source of the SLA data above; it detects non-compliance but does not prevent it.
- **M4 (transparency):** The Beacon Settings > Privacy explanation informs individuals but does not by itself provide human intervention.
- **M5 (screening):** Screening discipline ensures risks are identified before launch, but does not mitigate the identified risk.

### 5.3 Conclusion on Residual Risk

The measures in place do not fully mitigate the residual Article 22 risk. The routing-logic deprioritisation and the 61% SLA performance mean the residual risk remains HIGH under Article 35(1), scored 4 (likelihood) x 4 (severity) on the INT-FORM-12 scale. Remediation of the human-review workflow is required, and the Article 36(1) prior-consultation question is addressed in section 6.

## 6. Article 36 Prior Consultation: Open Position

### 6.1 Status of the Decision

As of 2026-10-01, the decision whether to seek prior consultation with the Irish Data Protection Commission (DPC) under Article 36(1) GDPR for Beacon AI lead scoring remains unresolved. Article 36(1) requires prior consultation with the supervisory authority where a DPIA indicates that the processing would result in a high residual risk that the controller cannot mitigate by reasonable means. As recorded in section 5.3, the residual Article 22 risk in this DPIA (INT-DPIA-2025-07) is HIGH under Article 35(1) and cannot be fully mitigated by the measures currently in place. DPO Tomás Reyes recommends consultation with the DPC on that basis.

### 6.2 Internal Checklist Requirement (INT-CHK-DPIA-04)

Internal checklist INT-CHK-DPIA-04 requires that where a DPIA shows residual high risk after mitigation, the DPO prepares a recommendation on prior consultation with the DPC under Article 36(1) GDPR within 15 working days of the DPIA sign-off. The DPIA was signed off by Tomás Reyes on 2025-09-12; the recommendation pathway under INT-CHK-DPIA-04 is therefore engaged, and the open position recorded in this section is the item requiring resolution.

### 6.3 Legal Advice: CONF-MEMO-2026-08

Aoife Brennan, Senior Privacy Counsel (Dublin), prepared legal memo CONF-MEMO-2026-08 dated 2026-08-19. The memo advises that launching Beacon AI lead scoring without Article 36 consultation carries exposure under Article 83(4) GDPR of up to EUR 10 million or 2% of total worldwide annual turnover, whichever is higher, for infringements of the Article 35-36 obligations. This exposure figure must be weighed by the decision-makers alongside the commercial considerations recorded below.

### 6.4 Board Discussion of 2026-09-15

At the board meeting of 2026-09-15, Julia Moreau, Product Director, Beacon AI, and CEO Daniel Whitfield argued that consulting the DPC would delay the Beacon AI general-availability launch. The estimated delay is at least the eight-week written-advice window under Article 36(2) GDPR, plus a possible six-week extension, with an estimated EUR 1.4 million in deferred annual recurring revenue (ARR). This commercial position is recorded alongside the DPO's recommendation and the legal exposure in CONF-MEMO-2026-08 so that the decision-makers have the full picture.

### 6.5 Board Resolution CONF-BRD-2026-09-R2

Board resolution CONF-BRD-2026-09-R2 deferred the Article 36 consultation decision to General Counsel Priya Raman and the DPO, Tomás Reyes. The resolution requires them to present a mitigation plan for risk record CONF-RISK-07 — including remediation of the INT-Q-LEAD-REVIEW SLA breach (61% SLA performance in Q1 2026 against the 5-working-day target, and routing-logic deprioritisation ahead of human review) — at the next board meeting in December 2026. Priya Raman and Tomás Reyes must therefore reach their consultation decision with that deadline in view.

### 6.6 Draft Communication to the DPC (CONF-DRAFT-DPC-01)

A draft communication to the DPC, CONF-DRAFT-DPC-01, was prepared by Aoife Brennan in September 2026 and remains unsent pending the Priya Raman / Tomás Reyes decision. The draft proposes remediation of the human-review workflow — closing the routing-logic gap and restoring reliable INT-Q-LEAD-REVIEW SLA performance — as an alternative to suspending the lead-scoring feature. If consultation proceeds, CONF-DRAFT-DPC-01 forms the basis of the Article 36 submission; under Article 36(2), the DPC would provide written advice within eight weeks, extendable by six weeks.

### 6.7 Summary of the Open Position

| Item | Position |
|---|---|
| Decision required | Whether to seek Article 36(1) prior consultation with the DPC |
| Decision owners | Priya Raman (General Counsel) and Tomás Reyes (DPO), per CONF-BRD-2026-09-R2 |
| DPO recommendation | Consult — high residual risk cannot be fully mitigated |
| Legal exposure | Up to EUR 10 million or 2% of worldwide turnover (Art. 83(4)), per CONF-MEMO-2026-08 |
| Commercial cost of consultation | Est. EUR 1.4 million deferred ARR from launch delay of at least eight weeks plus possible six-week extension |
| Mitigation plan deadline | December 2026 board meeting |
| Ready instrument | CONF-DRAFT-DPC-01 (unsent draft DPC communication) |

## 7. Residual Risk Summary and Sign-Off

### 7.1 Consolidated Residual Risk Table

The residual risks in DPIA INT-DPIA-2025-07 are scored on the internal 1-5 INT-FORM-12 scale for likelihood and severity (see section 4.4). The Article 22 risk at 4 (likelihood) x 4 (severity) is the highest residual score of any DPIA Acme has completed to date.

| # | Residual risk | Likelihood | Severity | Rating | Basis |
|---|---|---|---|---|---|
| R1 | Solely automated profiling drives account deprioritisation/closure without effective human review (Art. 22(1)) | 4 | 4 | HIGH | CONF-RISK-07: the lead score is derived by solely automated profiling and drives decisions with similarly significant effects (loss of sales follow-up, account closure) |
| R2 | Individuals cannot in practice obtain the Art. 22(3) safeguards | 4 | 4 | HIGH | 61% INT-Q-LEAD-REVIEW SLA performance in Q1 2026; routing-logic deprioritisation ahead of human review |

### 7.2 Sign-Off Record

| Field | Detail |
|---|---|
| DPIA record | INT-DPIA-2025-07 |
| DPO sign-off | Tomás Reyes, Data Protection Officer — 2025-09-12 |
| Residual Art. 22 risk at sign-off | 4 (likelihood) x 4 (severity) — highest residual score of any Acme DPIA to date |
| Version 1.3 update | Effective 2026-07-20, reflecting the CONF-RISK-07 findings and remediation of the CONF-AUD-2026-05 finding (documented necessity and proportionality assessment added at section 3) |
| Status | Current |

Because the residual score of 4 exceeds the sign-off threshold on both dimensions, DPO sign-off was required before launch and was given by Tomás Reyes on 2025-09-12.

### 7.3 Post-Sign-Off Position

The residual Article 22 risk remains HIGH under Article 35(1) GDPR and cannot be fully mitigated by the measures currently in place (section 5.3). As of 2026-10-01, the decision whether to seek prior consultation with the DPC under Article 36(1) GDPR remains unresolved: DPO Tomás Reyes recommends consultation, and the decision is deferred to Priya Raman (General Counsel) and the DPO under board resolution CONF-BRD-2026-09-R2, with a mitigation plan for CONF-RISK-07 due at the December 2026 board meeting. This DPIA must be re-issued for fresh DPO sign-off if the processing changes materially or upon resolution of the Article 36 question.

## 8. Records, Review and Next Steps

### 8.1 Records Generated by and Relating to This DPIA

| Record | Description | Location / Owner |
|---|---|---|
| INT-SCREEN-2025-031 | WP248 rev.01 screening record (four criteria met), triggering this DPIA | INT-Q-DPIA-SCREEN; Mara Okafor, Head of Privacy Operations |
| INT-DPIA-2025-07 (this document, CONF-DPIA-AI-001) | Full DPIA on template INT-FORM-12 | Privacy Office |
| Review-outcome logs | Human-review outcome and reviewer identity for INT-Q-LEAD-REVIEW flagged leads | Atlas; audited by Internal Audit |
| CONF-RISK-07 | Risk record for the residual Article 22 risk | Privacy Office |
| CONF-MEMO-2026-08 | Legal memo on Art. 83(4) exposure (Aoife Brennan, 2026-08-19) | Legal |
| CONF-BRD-2026-09-R2 | Board resolution deferring the Art. 36 decision | Board records |
| CONF-DRAFT-DPC-01 | Unsent draft DPC communication proposing human-review workflow remediation (Aoife Brennan, September 2026) | Legal |

### 8.2 Next Steps

1. Priya Raman (General Counsel) and Tomás Reyes (DPO) decide whether to seek Article 36(1) prior consultation with the DPC; if consultation proceeds, CONF-DRAFT-DPC-01 forms the basis of the submission.
2. Priya Raman and Tomás Reyes present the CONF-RISK-07 mitigation plan at the December 2026 board meeting, per CONF-BRD-2026-09-R2. The plan must include remediation of the INT-Q-LEAD-REVIEW SLA breach (61% performance in Q1 2026 against the 5-working-day target) and closure of the routing-logic deprioritisation gap identified in section 4.2.
3. The Privacy Office re-issues this DPIA for fresh DPO sign-off upon resolution of the Article 36 question.

### 8.3 Review Triggers

This DPIA must be reviewed and re-issued for fresh DPO sign-off if any of the following change: the lead-scoring model, the data inputs (CRM data or consented engagement events), or the sales-workflow routing logic. Absent such changes, the next scheduled review follows the December 2026 board meeting.
