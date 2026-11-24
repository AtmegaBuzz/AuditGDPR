---
doc_id: "CONF-TIA-US-001"
title: "Transfer Impact Assessment: US Product-Analytics Vendor"
company: "Acme Corp"
publisher: "ACME"
access_level: 2
classification: "confidential"
doc_type: "assessment"
profile: "company_doc"
topic: "transfers"
topics: ["transfers"]
owner: "Legal & Privacy"
approver: "Senior Privacy Counsel"
version: "1.1"
effective_date: "2026-05-28"
status: "current"
gdpr_articles: [44, 46]
related: ["INT-SOP-TRANSFER-001", "PUB-SUBPROC-001"]
generator: {"writer": "@cf/zai-org/glm-5.3", "judge": "@cf/openai/gpt-oss-120b", "run_id": "20261124-025609", "prompt_hash": "284162f9dd75"}
review: {"status": "ok", "attempts": 1, "issues_left": 0, "scores": {"fact_fidelity": 5, "tier_discipline": 5, "gdpr_accuracy": 5, "realism": 5, "retrievability": 5}}
---

# Transfer Impact Assessment: US Product-Analytics Vendor

| Field | Value |
|---|---|
| Document ID | CONF-TIA-US-001 |
| Version | 1.1 |
| Owner | Legal & Privacy (Mara Okafor, Head of Privacy Operations) |
| Approver | Aoife Brennan, Senior Privacy Counsel (Dublin) |
| Effective Date | 2026-05-28 |
| Classification | CONFIDENTIAL |
| Status | Current |
| Audience | Legal and executive leadership |
| GDPR Articles in Scope | Art. 44 (general principle for transfers); Art. 46 (appropriate safeguards, incl. Art. 46(2)(c) SCCs) |
| Related Records | INT-TIA-2025-114; INT-FORM-TIA-07; INT-REG-XFER-01; CONF-TIA-REVIEW-2026-09; CONF-AMEND-2026-08; CONF-BRD-2026-06-R3 |

## 1. Document Control and Purpose

| Field | Value |
|---|---|
| Document ID | CONF-TIA-US-001 |
| Version | 1.1 |
| Owner | Legal & Privacy (Mara Okafor, Head of Privacy Operations) |
| Approver | Aoife Brennan, Senior Privacy Counsel (Dublin) |
| Effective Date | 2026-05-28 |
| Classification | CONFIDENTIAL |
| Status | Current |
| Audience | Legal and executive leadership |
| GDPR Articles in Scope | Art. 44 (general principle for transfers); Art. 46 (appropriate safeguards, incl. Art. 46(2)(c) SCCs) |
| Related Records | INT-TIA-2025-114; INT-FORM-TIA-07; INT-REG-XFER-01; CONF-TIA-REVIEW-2026-09; CONF-AMEND-2026-08; CONF-BRD-2026-06-R3 |

### 1.1 Purpose

This document is the transfer impact assessment (TIA) for the US product-analytics vendor MetricPulse Inc., prepared using the mandatory TIA template INT-FORM-TIA-07, owned by Aoife Brennan's legal team. It re-assesses the lawfulness of the transfer of Beacon end-user event data to MetricPulse Inc. (US, AWS us-east-1) under GDPR Art. 44 and Art. 46, following the CJEU Schrems II judgment. It supersedes and updates the original assessment recorded as INT-TIA-2025-114, signed off on 2025-08-22 by Mara Okafor.

### 1.2 Scope

This TIA covers the MetricPulse Inc. transfer route listed in the transfer register INT-REG-XFER-01. It does not cover other outbound routes (Stripe, Beacon AI, parent-company access), which are assessed separately. Per INT-SOP-TRANSFER-001, the internal SLA for TIA completion is 15 business days from vendor onboarding start, which is stricter than the GDPR, which sets no fixed TIA deadline.

### 1.3 Audience

This document is classified CONFIDENTIAL and is addressed to legal and executive leadership only.

## 2. Transfer Details and Legal Mechanism

### 2.1 Transfer Route

| Field | Value |
|---|---|
| Recipient | MetricPulse Inc. (United States) |
| Data Categories | Beacon end-user event data |
| Hosting Location | AWS us-east-1 (United States) |
| Register Route | INT-REG-XFER-01 (transfer register maintained by Privacy Operations in Atlas) |
| Mechanism | Art. 46(2)(c) SCCs — 2021 EU Commission SCCs, module two (controller-to-processor) |
| Adequacy Position | MetricPulse Inc. has been certified under the EU-US Data Privacy Framework since 2024-02-10 |

MetricPulse Inc. is one of the 11 outbound transfer routes outside the EEA recorded in INT-REG-XFER-01 as of 2026-09-15, each mapped in the register to its legal mechanism. Beacon end-user event data is exported to MetricPulse's analytics environment on AWS us-east-1 infrastructure in the United States.

### 2.2 Legal Mechanism Analysis

The transfer relies on the 2021 EU Commission standard contractual clauses, module two (controller-to-processor), consistent with Acme's processor role for its customers' end-user data in Beacon and Acme's privacy notice commitment that transfers occur only where an Art. 45 adequacy decision applies or Art. 46(2)(c) safeguards are in place.

MetricPulse Inc. holds EU-US Data Privacy Framework certification (since 2024-02-10). However, as assessed in CONF-TIA-REVIEW-2026-09, that certification does not cover the specific analytics sub-processing the vendor performs, so the SCCs — not the DPF — are the operative transfer mechanism for this route.

### 2.3 Prior Assessment

The original TIA, recorded as INT-TIA-2025-114 and signed off on 2025-08-22 by Mara Okafor, scored the destination-law risk as **medium** after application of the standard supplementary measures in INT-FORM-TIA-07. One remediation item remains open: encryption keys must be held solely in eu-west-1 by Acme, not by the vendor. This open item is the trigger for the re-assessment recorded in CONF-TIA-REVIEW-2026-09 and for the contractual amendment CONF-AMEND-2026-08.

## 3. Assessment of Destination Law and Supplementary Measures

### 3.1 Destination-Law Findings

Following the CJEU Schrems II judgment, Acme assesses US destination law for transfers relying on Art. 46(2)(c) SCCs and adds supplementary measures where required, as stated on Acme's trust center. MetricPulse Inc. holds EU-US Data Privacy Framework certification (since 2024-02-10), but the re-assessment recorded in CONF-TIA-REVIEW-2026-09 concluded that this certification does not cover the specific analytics sub-processing the vendor performs for Acme. The transfer therefore relies on the SCCs alone, and US government-access powers (notably FISA Section 702) remain the principal destination-law risk to evaluate.

### 3.2 Evaluation of Standard Supplementary Measures

The standard supplementary measures listed in INT-FORM-TIA-07 for US transfers were evaluated as follows:

| Measure | Status | Assessment |
|---|---|---|
| TLS 1.3 in transit | In place | Effective against interception in transit |
| AES-256 encryption at rest | In place | Effective against compelled access to stored ciphertext |
| Pseudonymisation of end-user identifiers before export to Atlas replicas | In place | Reduces identifiability of exported event data |
| Documented government-access challenge commitment from vendor | In place | Vendor commits to challenge access requests; not yet contractually enforceable |
| EU-only key custody (keys held solely in eu-west-1 by Acme) | **Not yet in place** | Open remediation item from INT-TIA-2025-114; requires amendment CONF-AMEND-2026-08 |

### 3.3 Conclusion on the Key-Holding Measure

The decisive supplementary measure — encryption keys held solely in eu-west-1 by Acme rather than by MetricPulse — is not yet contractually enforceable. CONF-AMEND-2026-08, which would require EU-only key custody and a transparency commitment on government access requests, has been verbally agreed by MetricPulse but has not been countersigned as of 2026-09-28. Without enforceable EU-only key custody, the vendor remains technically capable of decrypting the data, which materially weakens the supplementary-measures analysis.

### 3.4 Overall Assessment

The MetricPulse transfer is assessed as **borderline**. The SCCs plus the in-place measures provide a defensible baseline, but the unenforceable key-holding measure leaves the destination-law risk at the upper end of medium. This conclusion is consistent with the quarterly TIA review cycle (2026-Q3 review, 2026-09-05), which flagged INT-TIA-2025-114 as requiring re-assessment before 2026-12-31.

## 4. Risk Assessment

### 4.1 Risk Table (Likelihood x Severity)

| ID | Risk | Likelihood | Severity | Rating |
|---|---|---|---|---|
| R1 | US government access to Beacon end-user event data on AWS us-east-1 (FISA Section 702), with no enforceable EU-only key custody to render data unintelligible | Medium | High | High |
| R2 | Onward transfer by MetricPulse to sub-processors not covered by its DPF certification | Medium | Medium | Medium |
| R3 | Enforceability gap: CONF-AMEND-2026-08 not countersigned as of 2026-09-28, leaving the key-holding and government-access transparency commitments non-binding | High | Medium | High |
| R4 | Contagion risk to the Beacon AI training flow: pseudonymisation keys for INT-ROPA-22 are stored in the same US analytics stack, weakening the supplementary-measures argument for the SCC module one transfer to Austin | Medium | High | High |

### 4.2 Residual Risk Rating

Residual risk after application of the in-place supplementary measures is rated **medium** by the legal team. Samir Haddad (CISO) dissented, recording in CONF-RISK-07 a residual risk rating of **high** for the current MetricPulse arrangement. His dissent is noted here for completeness and remains on file.

The CISO's rating reflects the Art. 83(5) exposure: an infringement of the Chapter V transfer rules (Art. 44-49) attracts administrative fines of up to EUR 20 million or 4% of total worldwide annual turnover, whichever is higher.

### 4.3 Beacon AI Dependency

This risk assessment cannot be read in isolation from the Beacon AI lead-scoring flow (INT-ROPA-22), directed by Julia Moreau, which sends pseudonymised feature vectors to Acme Corp Inc. in Austin under SCCs module one (controller-to-controller). As warned in Aoife Brennan's legal memo CONF-MEMO-2026-09-14, if the MetricPulse amendment fails, that training flow would be unlawful, because the pseudonymisation keys are stored in the same US analytics stack, weakening the supplementary-measures argument. Remediation of the MetricPulse gap under CONF-AMEND-2026-08 is therefore a precondition for the continued lawfulness of the Beacon AI flow.

## 5. Remediation and Contingency

### 5.1 Contract Amendment CONF-AMEND-2026-08

Remediation of the MetricPulse gap depends on execution of the contract amendment CONF-AMEND-2026-08, which requires (a) EU-only key custody — encryption keys held solely in eu-west-1 by Acme, not by MetricPulse — and (b) a transparency commitment on government access requests. MetricPulse has verbally agreed to the amendment but, as of 2026-09-28, has not countersigned. Until countersignature, the key-holding supplementary measure remains non-binding and the residual risk assessment in section 4.2 stands.

### 5.2 Board Authorisation and Deadline

Board resolution CONF-BRD-2026-06-R3, approved on 2026-06-19 on the recommendation of Priya Raman (General Counsel) and Daniel Whitfield (CEO), authorises continued use of MetricPulse for a maximum of six months — until **2026-12-31** — conditional on execution of CONF-AMEND-2026-08. This deadline aligns with the quarterly TIA review cycle requirement (2026-Q3 review, 2026-09-05) that INT-TIA-2025-114 be re-assessed before 2026-12-31. If the amendment is not executed by that date, continued transfer on this route is not authorised.

### 5.3 Fallback: EU Proxy Routing

If CONF-AMEND-2026-08 is not executed, Acme's fallback is to route MetricPulse analytics through an EU proxy, so that no personal data is transferred outside the EEA on this route and Chapter V no longer applies.

### 5.4 Contingency Budget and EU Analytics Replacement

Helen Zhou (CFO) has approved a EUR 250,000 contingency (CONF-BUDGET-2026-Q4) for the EU-based analytics replacement vendor evaluation. Lena Fischer's engineering team is to deliver a technical feasibility report by **2026-11-15**. This contingency mirrors the EUR 250,000 budget line set in CONF-BRD-2026-06-R3 for an EU-based analytics replacement if the amendment fails.

### 5.5 Remediation Checklist

- [ ] CONF-AMEND-2026-08 countersigned by MetricPulse (EU-only key custody; government-access transparency)
- [ ] Key custody verified as held solely in eu-west-1 by Acme
- [ ] TIA re-assessment of INT-TIA-2025-114 completed before 2026-12-31
- [ ] Engineering feasibility report for EU analytics replacement delivered by 2026-11-15
- [ ] If amendment fails: EU proxy routing implemented and INT-REG-XFER-01 updated

## 6. Related Findings and Governance Context

### 6.1 Quarterly TIA Review Cycle

Mara Okafor runs a quarterly TIA review cycle across all routes in INT-REG-XFER-01. The 2026-Q3 review, conducted on 2026-09-05, re-approved 10 of the 11 outbound transfer routes and flagged INT-TIA-2025-114 (MetricPulse) as requiring re-assessment before 2026-12-31. That deadline coincides with the six-month authorisation limit set by board resolution CONF-BRD-2026-06-R3, meaning the MetricPulse route is now subject to two concurrent governance deadlines. The next quarterly review (2026-Q4) must verify either execution of CONF-AMEND-2026-08 or implementation of the EU proxy fallback.

### 6.2 DPC Complaint and Sub-Processor Transparency

A customer complaint was lodged with the Irish Data Protection Commission on 2026-08-30 (CONF-DPC-2026-COMP-041), questioning Acme's US parent-access disclosures — the route routed through INT-Q-PARENT-ACCESS and reviewed monthly by DPO Tomás Reyes. Kwame Mensah's internal audit (CONF-AUDIT-2026-09) found that the public sub-processor list omits two US-based group entities, and a corrected trust-center page is scheduled for publication by **2026-10-31**.

### 6.3 Relevance to This Assessment

While the complaint concerns the parent-access route rather than MetricPulse, the audit finding is directly relevant here: Acme's public commitments state that a current sub-processor list is available on request via privacy@acme.example and that customers are notified of sub-processor changes in advance. Any transparency failure in Chapter V disclosures weakens Acme's Art. 5(2) accountability position and could draw DPC scrutiny of transfer documentation, including this TIA. The corrected trust-center page must therefore accurately describe the MetricPulse route and its SCC mechanism.

## 7. Residual Risk Conclusion and Sign-off

### 7.1 Residual Risk Statement

The MetricPulse Inc. transfer route is assessed as **borderline**. Because the vendor's EU-US Data Privacy Framework certification does not cover the specific analytics sub-processing it performs, the transfer relies on the SCCs alone, and the key-holding supplementary measure is not yet contractually enforceable. Residual risk is rated **medium** if CONF-AMEND-2026-08 is executed and **high** if the amendment fails by **2026-12-31**. The CISO's dissenting 'high' rating (CONF-RISK-07) remains on file.

### 7.2 Conditions for Continued Transfer

Continued transfer on this route is authorised only if all of the following hold:

- CONF-AMEND-2026-08 is countersigned by MetricPulse, delivering EU-only key custody and government-access transparency;
- The re-assessment of INT-TIA-2025-114 flagged by the 2026-Q3 review (2026-09-05) is completed before **2026-12-31**;
- If the amendment fails, EU proxy routing is implemented and INT-REG-XFER-01 is updated.

### 7.3 Monitoring Triggers

- Non-countersignature of CONF-AMEND-2026-08 by 2026-12-31;
- Any MetricPulse sub-processor change or lapse of DPF certification;
- DPC engagement arising from CONF-DPC-2026-COMP-041 touching Chapter V documentation;
- 2026-Q4 quarterly TIA review of INT-REG-XFER-01.

### 7.4 Sign-off (per INT-FORM-TIA-07)

| Field | Value |
|---|---|
| Assessor | Mara Okafor, Head of Privacy Operations |
| Approver | Aoife Brennan, Senior Privacy Counsel (Dublin) |
| Decision | Approve with conditions (section 7.2) |
| Re-assessment Deadline | 2026-12-31 |
