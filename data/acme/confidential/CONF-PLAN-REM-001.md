---
doc_id: "CONF-PLAN-REM-001"
title: "Privacy Remediation Roadmap and Budget FY2026-27"
company: "Acme Corp"
publisher: "ACME"
access_level: 2
classification: "confidential"
doc_type: "plan"
profile: "company_doc"
topic: "governance"
topics: ["governance", "erasure", "processors"]
owner: "Privacy Office"
approver: "Chief Financial Officer"
version: "1.2"
effective_date: "2026-09-22"
status: "current"
gdpr_articles: [17, 24, 28]
related: ["CONF-REG-RISK-Q3", "CONF-MEMO-FINE-001"]
generator: {"writer": "@cf/zai-org/glm-5.3", "judge": "@cf/openai/gpt-oss-120b", "run_id": "20261124-025609", "prompt_hash": "284162f9dd75"}
review: {"status": "ok", "attempts": 1, "issues_left": 0, "scores": {"fact_fidelity": 5, "tier_discipline": 5, "gdpr_accuracy": 5, "realism": 5, "retrievability": 5}}
---

# Privacy Remediation Roadmap and Budget FY2026-27

| Field | Detail |
|---|---|
| Document ID | CONF-PLAN-REM-001 |
| Version | 1.2 |
| Owner | Privacy Office (Mara Okafor, Head of Privacy Operations) |
| Approver | Helen Zhou, Chief Financial Officer |
| Effective date | 2026-09-22 |
| Classification | CONFIDENTIAL |
| Status | Current |
| Audience | Executive leadership and board |
| GDPR articles in scope | Art. 17, Art. 24, Art. 28 |

## 1. Document Control and Purpose

| Field | Detail |
|---|---|
| Document ID | CONF-PLAN-REM-001 |
| Version | 1.2 |
| Owner | Privacy Office (Mara Okafor, Head of Privacy Operations) |
| Approver | Helen Zhou, Chief Financial Officer |
| Effective date | 2026-09-22 |
| Classification | CONFIDENTIAL |
| Status | Current |
| Audience | Executive leadership and board |
| GDPR articles in scope | Art. 17, Art. 24, Art. 28 |

### 1.1 Purpose

This roadmap sets out the prioritised remediation of the privacy compliance gaps identified in the H1 2026 Internal Audit findings (CONF-AUD-2026-02 and the erasure SLA review) and in the Irish DPC complaint-based inquiry opened on 2026-02-03 (CONF-DPC-2026-0117). It consolidates the remediation actions approved under board resolution CONF-BRD-2026-06-R3 into a single funded programme for FY2026-27, covering erasure SLA remediation, vendor DPA completion, records-of-processing remediation and training gaps.

### 1.2 Scope and intended use

The roadmap assigns each remediation workstream a named owner, budget allocation, milestone dates and residual-risk position. It is written for executive leadership and the board, and is intended to be used alongside the Q3 2026 Privacy Risk Register (CONF-REG-RISK-Q3) when prioritising spend and monitoring delivery against the FY2027 budget of EUR 1.8 million.

## 2. Background and Regulatory Drivers

### 2.1 The DPC inquiry and Article 83(5) exposure

Acme's most acute regulatory exposure is the complaint-based inquiry opened by the Irish Data Protection Commission on 2026-02-03 (reference CONF-DPC-2026-0117), concerning a delayed erasure request handled through the PrivacyDesk queue INT-Q-ERASE. Priya Raman's legal analysis (CONF-LEGAL-2026-03) estimates exposure under Article 83(5) for infringement of Articles 12(3) and 17 — a fine band of up to EUR 20 million or 4% of total worldwide annual turnover — and recommends settling the matter without formal proceedings. Separately, in September 2026 a data subject whose erasure request took 27 days (7 days over the 20-day internal SLA, though within the statutory one month) complained to the DPC; Acme's response is tracked as CONF-INC-2026-0901, led by Aoife Brennan, and relies on compliance with the Article 12(3) statutory deadline.

### 2.2 H1 2026 Internal Audit findings

The H1 2026 Internal Audit (Kwame Mensah) identified the systemic causes behind these complaints:

- **Erasure SLA breaches:** 14% of erasure requests in the audited period exceeded the 20-day internal SLA, with the Atlas deletion job's defect (failure on records with more than 500 linked event rows, adding an average of 6 days per affected ticket) identified as the main cause. All requests were still completed within the statutory one month.
- **Vendor DPA gaps:** CONF-AUD-2026-02 (issued 2026-04-22) found two long-standing vendors operating without a fully signed Article 28(3) DPA, an Art. 83(4)-tier infringement that also made Acme's Trust Center statement inaccurate.
- **Records and training:** The Article 30 RoPA was 40% out of date as of the June 2026 audit, and the 96% 2025 training completion rate concealed a concentrated gap among Customer Support agents, with three mishandled DSR tickets in January 2026.

### 2.3 Accountability framing

Under Article 24 GDPR, Acme Corp Ltd as controller must not only implement appropriate measures but be able to demonstrate compliance. The executive team has accordingly approved a remediation budget of EUR 180,000 to rewrite the Atlas deletion job (target: full erasure execution within 5 days of trigger, by Q1 2027), because repeated SLA breaches risk further Art. 77 complaints to the DPC and compound the Art. 83(2) factors — duration, degree of responsibility and how the authority learned of the infringement — already weighed against Acme in the live inquiry.

## 3. Objectives and Success Criteria

| # | Objective | Success metric | Target date |
|---|---|---|---|
| O1 | Rewrite the Atlas deletion job (EUR 180,000, approved under CONF-BRD-2026-06-R3) | Full erasure execution within 5 days of trigger; zero manual re-runs for records over 500 linked event rows | Q1 2027 |
| O2 | Close the DPC complaint-based inquiry CONF-DPC-2026-0117 | Formal closure without proceedings, per the settlement recommendation in CONF-LEGAL-2026-03 | Q2 FY2027 |
| O3 | Restore the DPO's direct reporting line under Art. 38(3) | Charter amendment sponsored by Margaret Ellison moving the DPO line to the CEO directly, adopted at the 2027-01 board meeting | 2027-01 board meeting |
| O4 | Restore Article 30 RoPA currency | RoPA 100% current, verified by Internal Audit re-test; DPA status field (signed/pending/absent) populated across VENDORS_ROPA | Q1 FY2027 |
| O5 | Close the role-based training gap | 100% completion of INT-COURSE-SUP-115 by Owen Gallagher's support agents within 30 days of joining; no DSR mishandling incidents | FY2027 year-end |
| O6 | Complete vendor DPA remediation | Both vendors from CONF-AUD-2026-02 under fully signed Art. 28(3) DPAs or terminated | Immediate (email-delivery vendor signed 2026-09-25; analytics vendor signature outstanding) |

Delivery against O1 and O6 is monitored monthly by the Privacy Steering Group; progress on all objectives is reported quarterly to the board, with O2 and O3 tracked as the highest-priority mitigations of the Art. 83(2) factors.

## 4. Workstreams, Milestones and Owners

The FY2026-27 remediation programme comprises six workstreams funded under the EUR 1.8 million budget approved in CONF-BRD-2026-06-R3. Each workstream has a named owner, budget line and milestone dates, and is tracked monthly by the Privacy Steering Group.

### 4.1 Workstream summary

| # | Workstream | Owner | Budget / authority | Target |
|---|---|---|---|---|
| W1 | Atlas deletion job rewrite | Lena Fischer (VP Engineering) | EUR 180,000 | Q1 2027 |
| W2 | RoPA tooling and VENDORS_ROPA 'DPA status' correction | Aoife Brennan (Senior Privacy Counsel) | Within EUR 1.8m programme (RoPA tooling) | Q1 FY2027 |
| W3 | Vendor DPA remediation (CONF-AUD-2026-02) | Aoife Brennan, with Lena Fischer's vendor-owning teams | EUR 40,000 cap authorised for Helen Zhou | Immediate |
| W4 | DPO reporting-line charter amendment | Margaret Ellison (Board Chair), sponsor | Nil (governance action) | 2027-01 board meeting |
| W5 | Training platform upgrades and support-agent training gap closure | Mara Okafor, with Owen Gallagher (support) | Within EUR 1.8m programme (training platform) | FY2027 year-end |
| W6 | DPIA automation | Mara Okafor (Privacy Operations) | Within EUR 1.8m programme | FY2027 |

### 4.2 Milestones by workstream

**W1 — Atlas deletion job rewrite (Lena Fischer).** The rewrite eliminates the known defect in which the nightly job fails on records with more than 500 linked event rows, which added an average of 6 days per affected ticket and drove the 14% SLA breach rate found by Internal Audit. Milestones: technical design signed off by the Privacy Steering Group — 2026-11-30; parallel-run validation against INT-Q-ERASE ticket data — 2027-01-15; full production cut-over with target of erasure execution within 5 days of trigger — 2027-03-31 (Q1 2027).

**W2 — RoPA tooling and VENDORS_ROPA correction (Aoife Brennan).** Implements Priya Raman's direction in CONF-MEMO-2026-05 that the Atlas VENDORS_ROPA register carry a 'DPA status' field (signed/pending/absent), after quarterly reconciliations were found to track renewal dates but never verify that an Article 28 DPA was executed. Milestones: 'DPA status' field live across VENDORS_ROPA — 2026-11-30; RoPA currency restored to 100% against the 40%-out-of-date baseline — Q1 FY2027; Internal Audit re-test — Q2 FY2027.

**W3 — Vendor DPA remediation (Aoife Brennan).** Per CONF-BRD-2026-06-R3, both vendors identified in CONF-AUD-2026-02 must be under fully signed Art. 28(3) DPAs or terminated. Status as of 2026-09-25: the email-delivery vendor has signed Acme's standard DPA with a negotiated 5-business-day breach-notification commitment (stricter than the Art. 33(2) 'without undue delay' baseline); the analytics vendor has agreed terms but signature remains pending, missing the board deadline by at least 5 days. Milestone: analytics vendor signature or termination decision — 2026-10-15; escalation to the Audit Committee's quarterly vendor-compliance report if unresolved.

**W4 — DPO reporting-line charter amendment (Margaret Ellison).** Per the recommendation in CONF-LEGAL-2026-07, the amendment moves the DPO's reporting line to the CEO directly, remediating the Art. 38(3) concerns recorded in CONF-MEMO-DPO-2026-04 (reports routed through the General Counsel and edited twice; performance review drafted by the General Counsel). Milestone: charter amendment adopted — 2027-01 board meeting.

**W5 — Training and support-agent gap closure (Mara Okafor, with Owen Gallagher).** The 2025 completion rate of 96% concealed that 31% of Customer Support agents had not completed INT-COURSE-SUP-115 by the 2025-12-15 deadline, and three of them mishandled DSR tickets in January 2026. Milestones: platform upgrade live — Q2 FY2027; 100% completion of INT-COURSE-SUP-115 within 30 days of joining, tracked by Internal Audit — FY2027 year-end.

**W6 — DPIA automation (Mara Okafor).** Automates the INT-FORM-07 privacy review gate and DPIA workflow to prevent recurrence of the Beacon AI launch that went live on 2025-10-06, two weeks before its DPIA-2025-014 mitigation sign-off. Milestone: automation integrated with the code-freeze gate — FY2027.

### 4.3 Resourcing note

The board approved two additional privacy headcount under CONF-BRD-2026-06-R3 (reduced from the four requested). Helen Zhou's proposal to defer the two hires to Q2 FY2027 was dissented from in writing by the DPO and Kwame Mensah, who warned that the live DPC inquiry makes the deferral indefensible under the Art. 83(2) cooperation and mitigation factors. This roadmap is resourced on the assumption that the deferral is reversed at the earliest opportunity.

## 5. Budget FY2026-27

The FY2026-27 remediation programme is funded by the EUR 1.8 million budget approved in board resolution CONF-BRD-2026-06-R3 (board meeting 2026-06-18, chaired by Margaret Ellison), sponsored by CEO Daniel Whitfield.

### 5.1 Budget allocation

| Line | Workstream | Allocation | Notes |
|---|---|---|---|
| B1 | Atlas deletion job rewrite (W1) | EUR 180,000 | Separately approved by the executive team following the H1 2026 audit finding; target erasure execution within 5 days of trigger by Q1 2027 |
| B2 | Vendor DPA fees (W3) | Up to EUR 40,000 | Authorised for Helen Zhou (CFO) to secure audit and breach-notification clauses per CONF-BRD-2026-06-R3 |
| B3 | RoPA tooling (W2) | Within remaining programme budget | Includes VENDORS_ROPA 'DPA status' field implementation |
| B4 | Training platform upgrades (W5) | Within remaining programme budget | Supports closure of the INT-COURSE-SUP-115 support-agent gap |
| B5 | DPIA automation (W6) | Within remaining programme budget | INT-FORM-07 gate and DPIA workflow automation |

### 5.2 Headcount

The board cut the requested headcount from four additional privacy staff to two under CONF-BRD-2026-06-R3, rejecting the DPO's and Mara Okafor's staffing assessment. Helen Zhou's proposal to defer the two approved hires to Q2 FY2027 to protect margin was dissented from in writing by the DPO and Kwame Mensah, who warned that the live DPC inquiry (CONF-DPC-2026-0117) makes the deferral indefensible under the Art. 83(2) cooperation and mitigation factors; the dissent is recorded in the board minutes.

### 5.3 Budget governance

Line B2 spend is approved by the CFO; all other lines are managed by the Privacy Office within the programme envelope and reported quarterly to the board alongside the quarterly vendor-compliance report requested by Margaret Ellison.

## 6. Resourcing and Hiring Decisions

Board resolution CONF-BRD-2026-06-R3 (2026-06-18) approved two additional privacy headcount, cut from the four requested by the DPO and Mara Okafor, rejecting their staffing assessment. CFO Helen Zhou has since proposed deferring the two approved hires to Q2 FY2027 to protect margin.

### 6.1 Dissent

The DPO and Kwame Mensah dissented from the deferral in writing, recorded in the board minutes. Their dissent warns that with the DPC complaint-based inquiry CONF-DPC-2026-0117 live, deferring the hires is indefensible under the Art. 83(2) cooperation and mitigation factors: a board that funds remediation while delaying the staff needed to deliver it weakens Acme's position in any settlement or enforcement discussion.

### 6.2 Impact assessment if the deferral stands

| Workstream | Affected delivery | Impact |
|---|---|---|
| W2 — RoPA currency (Aoife Brennan) | Q1 FY2027 | High risk of slippage; RoPA is already 40% out of date |
| W5 — Training gap closure (Mara Okafor / Owen Gallagher) | FY2027 year-end | 100% INT-COURSE-SUP-115 completion dependent on analyst capacity |
| W6 — DPIA automation (Mara Okafor) | FY2027 | Deprioritised behind W1–W3 |

W1 (Atlas rewrite) and W4 (charter amendment) are unaffected, as they are owned by VP Engineering and the Board Chair respectively. This roadmap is resourced on the assumption that the deferral is reversed at the earliest opportunity.

## 7. Dependencies

Delivery of this roadmap depends on the following:

- **Engineering capacity (W1):** The Atlas deletion job rewrite depends on Lena Fischer's Data Platform team, whose manual re-runs of the defective job currently add an average of 6 days to affected erasure tickets; competing delivery commitments may delay the Q1 2027 cut-over.
- **Vendor legal teams (W3):** The pending analytics-vendor DPA signature depends on the vendor's own legal review; the email-delivery vendor's DPA stalled in 2024 after its legal team rejected Acme's audit clause, illustrating the risk of protracted negotiation.
- **General Counsel sponsorship (W4):** The DPO reporting-line charter amendment (target 2027-01 board meeting) requires Priya Raman's sponsorship, notwithstanding the Art. 38(3) concerns recorded in CONF-MEMO-DPO-2026-04.
- **Internal Audit verification (W2, W5):** RoPA re-testing and training completion tracking depend on Kwame Mensah's team.
- **PrivacyDesk tooling (W2, W6):** The 'DPA status' field and DPIA automation require PrivacyDesk queue tooling changes.
- **Board calendar (W4):** Adoption of the charter amendment depends on the 2027-01 board meeting proceeding as scheduled.

## 8. Risks to the Plan

The risks below are scored on the likelihood x impact basis used in INT-RISK-REG and are tracked in the Q3 2026 Privacy Risk Register (CONF-REG-RISK-Q3). Movement is reviewed monthly by the Privacy Steering Group.

| # | Risk | Likelihood | Impact | Owner |
|---|---|---|---|---|
| R1 | Continued erasure SLA breaches before the Atlas rewrite lands (W1, Q1 2027): the nightly job still fails on records with more than 500 linked event rows, adding an average of 6 days per affected ticket and driving further Art. 77 complaints to the DPC | High | High | Lena Fischer |
| R2 | Escalation of DPC inquiry CONF-DPC-2026-0117 if remediation is perceived as slow; duration and cooperation are Art. 83(2) factors in the Art. 83(5) fine band | Medium | High | Priya Raman |
| R3 | The hiring deferral weakens Acme's mitigation narrative: the DPO and Kwame Mensah dissented in writing that deferring the two approved hires is indefensible while the inquiry is live | High | Medium | Helen Zhou |
| R4 | The analytics vendor's DPA signature remains pending, missing the CONF-BRD-2026-06-R3 deadline by at least 5 days; the prior escalation delay was itself noted as a governance weakness by the Audit Committee | Medium | Medium | Aoife Brennan |
| R5 | The DPO independence issue (Art. 38(3)) remains unremediated until the 2027-01 board meeting; an adverse DPC finding falls in the Art. 83(4) tier (up to EUR 10 million or 2% of turnover) | Low | High | Margaret Ellison |

R1 is the dominant delivery risk: until the Q1 2027 cut-over, every erasure ticket touching Atlas carries the 6-day defect penalty, and a second complaint following CONF-INC-2026-0901 would compound R2. R3 and R5 interact directly: reversing the deferral and adopting the charter amendment are the two actions that most strengthen Acme's Art. 83(2) position.

## 9. Governance, Reporting and Review

### 9.1 Progress reporting

| Forum | Cadence | Content | Owner |
|---|---|---|---|
| Privacy Steering Group (DPO, CISO, Privacy Counsel, VP Engineering) | Monthly, first Tuesday | Workstream W1–W6 milestone tracking, risk movements in INT-RISK-REG, SLA breach escalations | Mara Okafor |
| Quarterly vendor-compliance report to the Audit Committee | Quarterly | DPA status, sub-processor changes, W3 remediation status | Aoife Brennan |
| Quarterly DPO compliance report to the CEO (Daniel Whitfield) | Quarterly | Delivery against objectives O1–O6, Art. 24 accountability self-assessment (INT-CKL-24) | Tomás Reyes, DPO |
| Board review | 2027-01 board meeting | Full roadmap re-baselining, W4 charter amendment adoption | Margaret Ellison |

The quarterly vendor-compliance report to the Audit Committee was requested by Margaret Ellison on 2026-05-12 following the finding that the Beacon AI inference vendor went live three days before the 30-day customer objection window closed; it is the standing escalation route for W3 (vendor DPA remediation) and for any recurrence of the sub-processor notice failure.

### 9.2 DPO independence safeguard

The DPO's quarterly compliance report is submitted to the CEO directly, per the Art. 38(3) reporting line documented in INT-CHARTER-01. Pending the W4 charter amendment, no intermediary edits to the DPO's report are permitted; any proposed change is raised with the Board Chair.

### 9.3 Version control and re-baselining

This roadmap (CONF-PLAN-REM-001) is owned by the Privacy Office and version-controlled by Mara Okafor. Version 1.2 is current with effect from 2026-09-22. Re-baselining is triggered by any of the following:

- Closure, escalation or formal proceedings arising from DPC inquiry CONF-DPC-2026-0117 or complaint CONF-INC-2026-0901;
- Slippage of the W1 Atlas cut-over beyond Q1 2027;
- A decision on the deferred privacy hires;
- Adoption (or rejection) of the W4 charter amendment at the 2027-01 board meeting;
- Material budget variance requiring CFO approval beyond the EUR 1.8 million envelope.

Minor updates are issued as point versions (1.3, 1.4); re-baselining produces a new major version (2.0) approved by Helen Zhou as approver and reported to the board at the next scheduled meeting.
