---
doc_id: "INT-CHECK-PBD-001"
title: "Privacy-by-Design Launch Checklist"
company: "Acme Corp"
publisher: "ACME"
access_level: 1
classification: "internal"
doc_type: "checklist"
profile: "company_doc"
topic: "governance"
topics: ["governance", "dpia_ai"]
owner: "Privacy Office"
approver: "Data Protection Officer"
version: "1.5"
effective_date: "2026-03-20"
status: "current"
gdpr_articles: [25, 35]
related: ["INT-SOP-DPIA-001"]
generator: {"writer": "@cf/zai-org/glm-5.3", "judge": "@cf/openai/gpt-oss-120b", "run_id": "20261124-025609", "prompt_hash": "284162f9dd75"}
review: {"status": "ok", "attempts": 1, "issues_left": 0, "scores": {"fact_fidelity": 5, "tier_discipline": 5, "gdpr_accuracy": 5, "realism": 5, "retrievability": 5}}
---

# Privacy-by-Design Launch Checklist

| Field | Value |
|---|---|
| Document ID | INT-CHECK-PBD-001 |
| Version | 1.5 |
| Owner | Privacy Office (Mara Okafor, Head of Privacy Operations) |
| Approver | Tomás Reyes, Data Protection Officer |
| Effective date | 2026-03-20 |
| Classification | INTERNAL |
| Status | Current |
| Audience | Product and engineering teams |
| GDPR articles in scope | Art. 25 (data protection by design and by default), Art. 35 (data protection impact assessments) |
| Related documents | INT-SOP-DPIA-001 (DPIA Procedure and Screening Checklist); INT-CHARTER-01 (Privacy Governance Charter, v3); INT-FORM-07 (privacy review form); INT-FORM-11 (WP248 screening form); INT-FORM-12 (DPIA template) |

## 1. Document Control

| Field | Value |
|---|---|
| Document ID | INT-CHECK-PBD-001 |
| Version | 1.5 |
| Owner | Privacy Office (Mara Okafor, Head of Privacy Operations) |
| Approver | Tomás Reyes, Data Protection Officer |
| Effective date | 2026-03-20 |
| Classification | INTERNAL |
| Status | Current |

### 1.1 Purpose

This checklist implements Acme's public commitment, stated on its Trust Center, that all new products and features undergo data protection by design and by default reviews in line with Article 25 GDPR and EDPB Guidelines 04/2019 before launch. It gives product and engineering teams a single, verifiable set of pre-launch privacy checks for every Acme Beacon feature that processes personal data, so that privacy review form INT-FORM-07 can be completed and signed by the DPO or Mara Okafor before code freeze.

### 1.2 Scope

This checklist applies to every Beacon feature that processes personal data. It covers Article 25 design and default checks and the Article 35 DPIA pathway, including features such as the Beacon AI lead-scoring feature owned by Julia Moreau, which additionally requires a DPIA under Art. 35(3)(a) because it evaluates personal aspects based on automated processing. It does not cover non-personal-data features or post-launch monitoring.

## 2. Roles and Responsibilities

The RACI below reflects the privacy governance RACI in the Privacy Governance Charter (INT-CHARTER-01, v3) and applies to every launch using this checklist.

| Role | Person | RACI for this checklist |
|---|---|---|
| Data Protection Officer | Tomás Reyes | Accountable for DPIA sign-off (any residual risk scored 4+ on the INT-FORM-12 scale requires his sign-off before launch) and for DPO advice under Art. 35(2); signs INT-FORM-07 |
| Head of Privacy Operations | Mara Okafor | Records the screening decision (DPIA required / not required) for tickets in INT-Q-DPIA-SCREEN within 10 working days; signs INT-FORM-07 |
| VP Engineering | Lena Fischer | Responsible for privacy-by-design implementation in Beacon |
| Product Director, Beacon AI (example product owner) | Julia Moreau | Named product owner for the DPIA (e.g. INT-DPIA-2025-07); owns feature delivery against the checklist |
| Senior Privacy Counsel | Aoife Brennan | Privacy reviewer for full DPIAs drafted on INT-FORM-12; owns DPA and RoPA maintenance |
| CISO | Samir Haddad | Owns the Art. 32 security measures verified in this checklist |

Per INT-FORM-07 (F-GOV-09), no Beacon feature processing personal data reaches code freeze without a completed privacy review form signed by the DPO or Mara Okafor; each DPIA must have a named product owner and a named privacy reviewer per F-DPI-10.

## 3. Pre-Launch Checklist

Complete every item below, in order, for each Beacon feature that processes personal data. Items 3.1 to 3.3 are gating steps in the engineering workflow: the feature ticket cannot move from design to build until item 3.1 is complete.

### 3.1 Stage 1 — Screening (mandatory before design-to-build)

- [ ] Log the new processing idea in the PrivacyDesk queue **INT-Q-DPIA-SCREEN**.
- [ ] Complete the screening form **INT-FORM-11**, assessing the idea against all nine criteria in WP248 rev.01.
- [ ] Confirm the screening is completed before the feature ticket moves from design to build in the engineering workflow.
- [ ] Verify that Mara Okafor, Head of Privacy Operations, records the screening decision (DPIA required / not required) within 10 working days of the ticket entering INT-Q-DPIA-SCREEN.

### 3.2 Stage 2 — Escalation to full DPIA

- [ ] If the INT-FORM-11 screening scores two or more WP248 criteria as met, escalate the ticket to a full DPIA drafted on template **INT-FORM-12**.
- [ ] Confirm the DPIA has a named product owner and a named privacy reviewer before drafting begins (e.g. for the Beacon AI lead-scoring DPIA INT-DPIA-2025-07: owner Julia Moreau, Product Director, Beacon AI; reviewer Aoife Brennan, Senior Privacy Counsel).
- [ ] Seek DPO advice under Art. 35(2) at an early stage of the DPIA.

### 3.3 Stage 3 — DPIA content and risk scoring

- [ ] Verify the DPIA content mirrors the four minimum content elements of Art. 35(7) GDPR as set out in INT-FORM-12: (1) systematic description of the processing and purposes; (2) necessity and proportionality assessment; (3) assessment of risks to rights and freedoms; (4) mitigating measures.
- [ ] Confirm residual risks are scored on the internal 1-5 likelihood and severity scale in INT-FORM-12.
- [ ] Where any residual risk is scored 4 or higher on either dimension, confirm sign-off by Tomás Reyes (DPO) before the feature can launch.
- [ ] Where the DPIA shows residual high risk after mitigation, confirm the DPO prepares a recommendation on prior consultation with the Irish DPC under Art. 36(1) GDPR within 15 working days of DPIA sign-off, per checklist INT-CHK-DPIA-04.

### 3.4 Stage 4 — Automated-evaluation safeguards (Art. 22(3))

- [ ] Where the feature evaluates personal aspects based on automated processing, verify a mandatory human-review safeguard is implemented in the Acme Beacon workflow UI (for Beacon AI lead scoring: accounts scored below 30 on the 0-100 lead score cannot be auto-closed and must pass through queue **INT-Q-LEAD-REVIEW**, staffed by customer sales teams).
- [ ] Confirm the human-review SLA is met: a reviewer acts on a flagged low-fit lead within 5 working days, with the review outcome and reviewer identity logged in Atlas for audit.
- [ ] Confirm the individual can obtain human intervention, express a point of view, and contest the outcome, including a right-to-contest workflow in Beacon Settings > Privacy.

### 3.5 Stage 5 — Transparency and data location

- [ ] Confirm plain-language transparency content for end-users is published in **Beacon Settings > Privacy**, satisfying the Art. 13/14 transparency obligations identified in the DPIA.
- [ ] Confirm the data-location position for the feature's processing (e.g. Beacon AI model training and scoring runs in AWS eu-west-1, Ireland, with no personal data leaving the EEA, so no Chapter V transfer assessment was required for the scoring pipeline). Where personal data does leave the EEA, escalate to Aoife Brennan for a transfer assessment before launch.

### 3.6 Stage 6 — Privacy review sign-off before code freeze

- [ ] Complete privacy review form **INT-FORM-07** for every Beacon feature that processes personal data.
- [ ] Obtain the signature of Tomás Reyes (DPO) or Mara Okafor on INT-FORM-07 before code freeze.
- [ ] File the completed INT-FORM-07, INT-FORM-11 screening and any INT-FORM-12 DPIA with the Privacy Office records for the feature.

## 4. Worked Example: Beacon AI Lead Scoring

This section shows the checklist applied end-to-end to the Beacon AI lead-scoring feature, the highest-residual-risk DPIA Acme has completed to date.

**Stage 1 — Screening.** The feature was logged in INT-Q-DPIA-SCREEN and screened on INT-FORM-11. Screening INT-SCREEN-2025-031 met four of the nine WP248 rev.01 criteria: evaluation based on automated processing, systematic processing of personal aspects, profiling, and innovative use of technology. Two or more criteria met, so Stage 2 escalation was mandatory.

**Stage 2 — Full DPIA.** The screening triggered full DPIA INT-DPIA-2025-07, drafted on INT-FORM-12 with the four Art. 35(7) content elements. The DPIA is owned by Julia Moreau (Product Director, Beacon AI) and reviewed by Aoife Brennan (Senior Privacy Counsel), with DPO advice sought under Art. 35(2).

**Stage 3 — Risk scoring and sign-off.** The DPIA concluded the processing is high-risk but mitigable. The residual Art. 22 risk was scored 4 (likelihood) x 4 (severity) on the INT-FORM-12 scale — the highest residual score of any Acme DPIA — requiring DPO sign-off. Tomás Reyes signed off INT-DPIA-2025-07 on 2025-09-12.

**Stage 4 — Art. 22(3) safeguards.** A mandatory human-review step is implemented in the Acme Beacon sales-workflow UI: accounts scored below 30 on the 0-100 lead score cannot be auto-closed and must pass through queue INT-Q-LEAD-REVIEW, staffed by customer sales teams. The SLA is 5 working days for a reviewer to act on a flagged low-fit lead; review outcomes and reviewer identities are logged in Atlas for Internal Audit.

**Stage 5 — Data location.** Model training and scoring run in AWS eu-west-1 (Ireland). INT-DPIA-2025-07 records that no personal data used by Beacon AI leaves the EEA, so no Chapter V transfer assessment was required for the scoring pipeline.

**Stage 6 — Sign-off.** INT-FORM-07 was completed and signed before code freeze, with the DPIA and screening filed with the Privacy Office.

## 5. Exceptions and Records

### 5.1 Exceptions

Any deviation from a checklist item in section 3 requires documented justification, approved by Tomás Reyes (DPO) before code freeze. The exception record must state the item waived, the reason, any compensating measure, and an expiry date. Waivers of DPIA-related items (sections 3.1 to 3.3) are not permitted where the INT-FORM-11 screening meets two or more WP248 rev.01 criteria; the full DPIA procedure in INT-SOP-DPIA-001 then applies without exception. All approved exceptions are logged in the privacy risk register (INT-RISK-REG) by Mara Okafor; risk acceptance decisions above a residual score of 15 additionally require CEO sign-off, and risks scored 9-15 are accepted by the Privacy Steering Group, with acceptances carrying an expiry date no more than 12 months out.

### 5.2 Records and retention

The Privacy Office retains, per the records schedule:

- [ ] Completed INT-CHECK-PBD-001 checklists for each feature.
- [ ] INT-FORM-11 screenings and screening decisions from INT-Q-DPIA-SCREEN.
- [ ] Full DPIAs on INT-FORM-12, including INT-DPIA-2025-07.
- [ ] Signed INT-FORM-07 privacy review forms and any DPO-approved exceptions.

### 5.3 Feeding governance

These records feed the DPO's quarterly self-assessment against Art. 24 accountability obligations using checklist INT-CKL-24, covering DPIA coverage and training completion, and are filed with the quarterly compliance report to the CEO. Residual risks identified at Stage 3 are entered into INT-RISK-REG, reviewed monthly by the Privacy Steering Group, each with a named mitigation owner.
