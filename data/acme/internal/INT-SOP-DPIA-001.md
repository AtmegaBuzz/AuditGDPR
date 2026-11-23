---
doc_id: "INT-SOP-DPIA-001"
title: "DPIA Procedure and Screening Checklist"
company: "Acme Corp"
publisher: "ACME"
access_level: 1
classification: "internal"
doc_type: "sop"
profile: "company_doc"
topic: "dpia_ai"
topics: ["dpia_ai"]
owner: "Privacy Office"
approver: "Data Protection Officer"
version: "2.0"
effective_date: "2025-11-03"
status: "current"
gdpr_articles: [35, 36]
related: []
generator: {"writer": "@cf/zai-org/glm-5.3", "judge": "@cf/openai/gpt-oss-120b", "run_id": "20261124-025027", "prompt_hash": "284162f9dd75"}
review: {"status": "ok", "attempts": 1, "issues_left": 0, "scores": {"fact_fidelity": 5, "tier_discipline": 5, "gdpr_accuracy": 5, "realism": 5, "retrievability": 5}}
---

# DPIA Procedure and Screening Checklist

| Field | Value |
|---|---|
| Document ID | INT-SOP-DPIA-001 |
| Version | 2.0 |
| Owner | Privacy Office (Mara Okafor, Head of Privacy Operations) |
| Approver | Tomás Reyes, Data Protection Officer |
| Effective date | 2025-11-03 |
| Classification | INTERNAL |
| Status | Current |
| Audience | Product managers and engineering leads |
| GDPR articles in scope | Art. 35, Art. 36 |

## 1. Purpose and Scope

This SOP governs how Acme screens new processing ideas and carries out data protection impact assessments (DPIAs) under Article 35 GDPR. It applies to all new products and features that are likely to result in a high risk to the rights and freedoms of individuals, including Acme's AI features. As stated on the Acme Trust Center, Acme carries out DPIAs for all such new products and features, including the Beacon AI lead-scoring feature.

This SOP is written for product managers and engineering leads, who are responsible for logging new processing ideas for screening and for supplying the information needed to complete a DPIA. The Privacy Office (Mara Okafor, Head of Privacy Operations) operates the screening process, and the DPO (Tomás Reyes) is involved in every DPIA.

The SOP covers Acme's processing in both of its GDPR roles: as controller (for example, customers' account data, employee data and marketing) and as processor (for customers' end-user data stored in Beacon). Consistent with Acme's public AI transparency commitment, all AI features are screened against the nine criteria in WP248 rev.01, and where two or more criteria are met, a full DPIA is completed before launch.

## 2. Roles and Responsibilities

The DPIA process at Acme Corp relies on clearly assigned ownership. Every DPIA has a named product owner and a named privacy reviewer, as recorded on template INT-FORM-12. For example, the DPIA for Beacon AI lead scoring (INT-DPIA-2025-07) is owned by Julia Moreau, Product Director, Beacon AI, and reviewed by Aoife Brennan, Senior Privacy Counsel.

| Activity | Product owner | Privacy reviewer | Mara Okafor (Privacy Ops) | Tomás Reyes (DPO) |
|---|---|---|---|---|
| Log new processing idea in INT-Q-DPIA-SCREEN | A | I | R | — |
| Complete screening form INT-FORM-11 | R | C | A | I |
| Record screening decision (DPIA required / not required) | I | C | R/A | I |
| Draft DPIA on INT-FORM-12 | R | R | C | I |
| Score residual risks (1-5 scale) | C | R | C | I |
| Sign off residual risks scored 4 or higher | I | I | I | R/A |
| Approve launch of assessed feature | R | C | I | A |

R = Responsible, A = Accountable, C = Consulted, I = Informed.

### 2.1 DPO involvement

As Acme publicly commits on its Trust Center, the DPO, Tomás Reyes, is involved in every DPIA, consistent with Article 35(2) GDPR (the controller must seek the advice of the DPO). Tomás Reyes must personally sign off any DPIA in which a residual risk is scored 4 or higher on either the likelihood or severity dimension of the INT-FORM-12 scale before the feature can launch.

### 2.2 Screening decisions

Mara Okafor, Head of Privacy Operations, records the screening decision (DPIA required / not required) within 10 working days of a ticket entering INT-Q-DPIA-SCREEN.

## 3. Stage 1: Screening Against the WP248 Criteria

Every new processing idea must be logged in the PrivacyDesk queue INT-Q-DPIA-SCREEN by the product owner before the feature ticket can move from design to build in the engineering workflow. Screening against the nine criteria in WP29 guidance WP248 rev.01 is performed using screening form INT-FORM-11. This screening must be completed before build starts: no feature ticket may progress from design to build with an open, unscreened entry in INT-Q-DPIA-SCREEN. This reflects Acme's public AI transparency commitment that all AI features are screened against the nine WP248 rev.01 criteria.

### 3.1 The nine WP248 rev.01 criteria

The product owner completes INT-FORM-11 by marking each criterion as met or not met:

- [ ] 1. Evaluation or scoring based on automated processing (including profiling)
- [ ] 2. Systematic processing of personal aspects
- [ ] 3. Decision-making with legal or similarly significant effects
- [ ] 4. Systematic monitoring of a publicly accessible area on a large scale
- [ ] 5. Matching or combining of datasets
- [ ] 6. Processing of special-category data (Art. 9) or criminal-offence data
- [ ] 7. Processing of data on a large scale
- [ ] 8. Innovative use of new or existing technologies
- [ ] 9. Processing that prevents data subjects from exercising a right or using a service

### 3.2 Escalation rule

Where the INT-FORM-11 screening scores **two or more** WP248 criteria as met, the processing idea is escalated to a full DPIA (Stage 2). Where fewer than two criteria are met, Mara Okafor records the screening decision as "DPIA not required", with the completed INT-FORM-11 attached to the ticket as the record of that decision.

### 3.3 Worked example: Beacon AI lead scoring (INT-SCREEN-2025-031)

The screening for the Beacon AI lead-scoring feature, recorded as INT-SCREEN-2025-031, met four WP248 criteria:

| WP248 criterion | Met? |
|---|---|
| Evaluation/scoring based on automated processing | Yes |
| Systematic processing of personal aspects | Yes |
| Profiling | Yes |
| Innovative use of technology | Yes |

Four criteria met exceeds the two-criterion threshold, so INT-SCREEN-2025-031 triggered full DPIA INT-DPIA-2025-07, drafted on template INT-FORM-12 (see Section 4).

## 4. Stage 2: Screening Decision and Escalation

The escalation rule for screening decisions is straightforward: where a screening under INT-FORM-11 scores **two or more** of the nine WP248 rev.01 criteria as met, the processing idea is escalated to a full DPIA under Article 35 GDPR (Stage 3, Section 5).

Mara Okafor, Head of Privacy Operations, records the screening decision — **DPIA required** or **DPIA not required** — within **10 working days** of the ticket entering the PrivacyDesk queue INT-Q-DPIA-SCREEN. The decision, together with the completed INT-FORM-11, is attached to the ticket so that Acme can demonstrate accountability for the screening outcome (Art. 5(2) GDPR).

### 4.1 Tickets not escalated

Where fewer than two WP248 criteria are met, Mara Okafor records the decision as "DPIA not required" and the ticket is returned to the engineering workflow, allowing the feature ticket to move from design to build. No further privacy assessment is triggered at this stage.

### 4.2 Tickets escalated

Where the decision is "DPIA required", a full DPIA is opened on template INT-FORM-12 before launch, with a named product owner and a named privacy reviewer assigned (see Section 5). As with the Beacon AI lead-scoring screening INT-SCREEN-2025-031, which met four criteria, the escalation is logged against the originating ticket in INT-Q-DPIA-SCREEN for traceability.

## 5. Stage 3: Conducting the Full DPIA

A full DPIA is drafted on template **INT-FORM-12**, which mirrors the four minimum content elements of Article 35(7) GDPR:

1. **Systematic description** of the processing operations and purposes, including the data flows, systems involved, categories of data subjects and personal data, and retention periods.
2. **Necessity and proportionality assessment**, covering the lawful basis, the less-intrusive alternatives considered, and the data-protection-by-design choices embedded in the feature (Art. 25 GDPR).
3. **Risk assessment** of the risks to the rights and freedoms of data subjects, with each residual risk scored on the internal 1-5 scale for likelihood and severity.
4. **Mitigating measures** taken to address the identified risks.

Every DPIA must have a **named product owner** and a **named privacy reviewer**, both recorded on INT-FORM-12. The product owner drafts the systematic description and supplies the technical detail; the privacy reviewer drafts the necessity, proportionality and risk analysis. The DPO, Tomás Reyes, is involved in every DPIA, as Acme publicly commits on its Trust Center (Art. 35(2) GDPR).

### 5.1 Worked example: DPIA INT-DPIA-2025-07 (Beacon AI lead scoring)

The DPIA for Beacon AI lead scoring, recorded as **INT-DPIA-2025-07**, was owned by Julia Moreau, Product Director, Beacon AI, and reviewed by Aoife Brennan, Senior Privacy Counsel. It was triggered by screening INT-SCREEN-2025-031, which met four WP248 criteria (see Section 3.3).

Key findings recorded in INT-DPIA-2025-07:

- The lead-scoring model is trained only on customer-provided CRM data and consented engagement events; no special-category data under Article 9 GDPR is used as a model input.
- Model training and scoring run in **AWS eu-west-1 (Ireland)**. The DPIA records that no personal data used by Beacon AI leaves the EEA, so **no Chapter V transfer assessment was required** for the scoring pipeline.
- The residual Article 22 risk was scored 4 (likelihood) x 4 (severity) — the highest residual score of any DPIA Acme has completed to date — requiring DPO sign-off under Section 2.1 and, where residual high risk remains after mitigation, consideration of prior consultation under Article 36(1) GDPR (see Section 6).

## 6. Risk Scoring and Sign-Off

Every residual risk identified in a DPIA drafted on INT-FORM-12 is scored on the internal **1-5 scale** for both **likelihood** and **severity**. The product owner and the named privacy reviewer score each risk jointly after mitigating measures are applied; the scores, together with the rationale, are recorded on INT-FORM-12 so that Acme can demonstrate accountability for the outcome (Art. 5(2) GDPR).

### 6.1 The 4+ sign-off rule

Any residual risk scored **4 or higher on either the likelihood or the severity dimension** must be signed off by the DPO, Tomás Reyes, **before the feature can launch**. A launch gate check against this rule is part of the DPIA close-out on INT-FORM-12. Where a residual risk remains high after mitigation, the DPO prepares a recommendation on prior consultation with the Irish Data Protection Commission under Article 36(1) GDPR within 15 working days of DPIA sign-off, as required by the privacy team's checklist INT-CHK-DPIA-04.

### 6.2 Worked example: DPIA INT-DPIA-2025-07

DPIA INT-DPIA-2025-07 (Beacon AI lead scoring) was signed off by Tomás Reyes on **2025-09-12**, with the residual Article 22 risk scored **4 (likelihood) x 4 (severity)** — the highest residual score of any DPIA Acme has completed to date. Because both dimensions reached 4, the DPIA could not close without the DPO's personal sign-off, and the sign-off record is retained on INT-FORM-12 as evidence of the launch decision.

## 7. Residual High Risk and Prior Consultation

Where a DPIA drafted on INT-FORM-12 shows a residual **high risk after mitigation** — that is, a residual risk scored 4 or higher on the likelihood or severity dimension that the mitigating measures do not bring down — the privacy team's checklist **INT-CHK-DPIA-04** applies.

Under INT-CHK-DPIA-04, the DPO, Tomás Reyes, prepares a **recommendation on prior consultation with the Irish Data Protection Commission (DPC)**, Acme's lead supervisory authority, under Article 36(1) GDPR within **15 working days of the DPIA sign-off**. The recommendation must state the residual risk scores, the mitigating measures already applied, and the DPO's advice on whether the high risk can or cannot be mitigated by further measures.

If prior consultation proceeds, Article 36(2) GDPR provides that the DPC gives written advice within **eight weeks**, extendable by **six weeks** where necessary. The feature must not launch until the consultation outcome is recorded on INT-FORM-12 and the DPO has signed off the final launch decision.

## 8. Post-Launch Obligations and Safeguards

A DPIA does not end at sign-off: the mitigating measures recorded on INT-FORM-12 must be implemented and verified before and after launch. Product owners must confirm at DPIA close-out that each safeguard has an owner, a system of record and, where applicable, an internal SLA.

### 8.1 Human review of automated scoring (Beacon AI example)

The human-review safeguard identified in DPIA INT-DPIA-2025-07 is implemented as a mandatory review step in the Acme Beacon sales-workflow UI. Accounts scored below 30 on the 0-100 lead score cannot be auto-closed and must pass through queue **INT-Q-LEAD-REVIEW**, staffed by customer sales teams. This operationalises the Article 22(3) GDPR safeguards that Acme publicly commits to on its Trust Center: every lead flagged as "low fit" can be reviewed by a human before any account is deprioritised or closed, and customers can request human intervention, express a point of view, and contest outcomes.

The internal SLA for INT-Q-LEAD-REVIEW is that a human reviewer acts on a flagged low-fit lead within **5 working days**. Product owners of scored features must report SLA adherence to the Privacy Office on request.

### 8.2 Audit logging

For the Beacon AI safeguard, the review outcome and the reviewer identity are logged in **Atlas** for audit by Internal Audit. Product owners of any feature launched with a DPIA must ensure the equivalent safeguard evidence is recorded in a queryable system and retained for audit.

### 8.3 Transparency for end-users

DPIAs also feed Acme's transparency obligations. The **Beacon Settings > Privacy** page includes a plain-language explanation of lead scoring for end-users whose data is processed by Acme's customers, drafted to satisfy the Article 13/14 transparency obligations identified in DPIA INT-DPIA-2025-07. It explains that the score is used to prioritise follow-up by human sales staff and that no decision about an individual is made solely by automated means. Product owners launching new scored features must arrange equivalent end-user transparency content with the Privacy Office before launch.

## 9. Exceptions, Records and Review

### 9.1 Exceptions

Any deviation from this SOP — for example, launching a feature before DPIA close-out, or extending the 10-working-day screening deadline — must be approved in writing by the DPO, Tomás Reyes. Exception requests are logged in INT-Q-DPIA-SCREEN against the originating ticket with the rationale, compensating controls and expiry date. The DPO is involved in every DPIA, so no exception may remove DPO involvement. Verbal or retroactive approvals are not valid.

### 9.2 Records generated by this SOP

| Record | System of record | Retention |
|---|---|---|
| Completed screening form INT-FORM-11 | INT-Q-DPIA-SCREEN | 6 years |
| Screening decision (DPIA required / not required) | INT-Q-DPIA-SCREEN | 6 years |
| Full DPIA on INT-FORM-12 (e.g. INT-DPIA-2025-07) | INT-Q-DPIA-SCREEN | 6 years after feature retirement |
| DPO sign-off of residual risks scored 4+ | INT-FORM-12 | 6 years after feature retirement |
| Art. 36(1) prior-consultation recommendation (per INT-CHK-DPIA-04) | INT-FORM-12 | 6 years |

Retention supports Acme's accountability obligation (Art. 5(2) GDPR) and its Trust Center commitment that customers may request a summary of the DPIA for the Beacon AI lead-scoring feature by emailing privacy@acme.example.

### 9.3 Review

Mara Okafor, Head of Privacy Operations, reviews this SOP annually, or sooner if GDPR guidance, the WP248 rev.01 criteria or Acme's Trust Center commitments change. Changes are approved by Tomás Reyes and issued as a new version.

## 10. Document Control

| Field | Value |
|---|---|
| Document ID | INT-SOP-DPIA-001 |
| Version | 2.0 |
| Owner | Privacy Office (Mara Okafor, Head of Privacy Operations) |
| Approver | Tomás Reyes, Data Protection Officer |
| Effective date | 2025-11-03 |
| Classification | INTERNAL |
| Status | Current |

### 10.1 Version history

| Version | Status | Summary of changes |
|---|---|---|
| 1.0 | Superseded | Initial issue of the DPIA Procedure and Screening Checklist. |
| 2.0 | Current | Added the worked example for Beacon AI lead scoring (INT-SCREEN-2025-031, INT-DPIA-2025-07), the DPO sign-off rule for residual risks scored 4 or higher, and the prior-consultation step under checklist INT-CHK-DPIA-04. |

### 10.2 Change log and contact

Version 2.0 was prepared by the Privacy Office and approved by the DPO, Tomás Reyes, whose involvement in every DPIA is a public Trust Center commitment. Questions about this SOP should be sent to privacy@acme.example.
