---
doc_id: "CONF-MIN-BRD-2026Q2"
title: "Board of Directors Minutes: Q2 2026 (Privacy and Risk Items)"
company: "Acme Corp"
publisher: "ACME"
access_level: 2
classification: "confidential"
doc_type: "minutes"
profile: "company_doc"
topic: "erasure"
topics: ["erasure", "retention", "governance"]
owner: "Company Secretary"
approver: "Chair of the Board"
version: "1.0"
effective_date: "2026-06-12"
status: "current"
gdpr_articles: [17, 24, 83]
related: ["INT-SOP-ERASE-002", "INT-RUN-ERASE-001"]
generator: {"writer": "@cf/zai-org/glm-5.3", "judge": "@cf/openai/gpt-oss-120b", "run_id": "20261124-025609", "prompt_hash": "284162f9dd75"}
review: {"status": "ok", "attempts": 1, "issues_left": 0, "scores": {"fact_fidelity": 5, "tier_discipline": 5, "gdpr_accuracy": 5, "realism": 5, "retrievability": 5}}
---

# Board of Directors Minutes: Q2 2026 (Privacy and Risk Items)

| Field | Detail |
|---|---|
| Document ID | CONF-MIN-BRD-2026Q2 |
| Version | 1.0 |
| Owner | Company Secretary |
| Approver | Margaret Ellison, Chair of the Board |
| Meeting Date | 2026-06-18 |
| Effective Date | 2026-06-12 |
| Classification | CONFIDENTIAL |
| Status | Current |
| Audience | Directors and executive leadership |
| GDPR Articles in Scope | Art. 17, Art. 24, Art. 83 |
| Chair | Margaret Ellison, Chair of the Board |
| Minute-taker | Company Secretary |

## 1. Meeting Details and Attendance

The Board of Directors of Acme Corp Ltd convened in Dublin on 12 June 2026, chaired by Margaret Ellison, Chair of the Board. The meeting reference is CONF-MIN-BRD-2026Q2. The Company Secretary acted as minute-taker. Quorum was confirmed, and the meeting was declared properly constituted.

**Directors present:**
- Margaret Ellison (Chair of the Board)
- Daniel Whitfield (Chief Executive Officer)
- Helen Zhou (Chief Financial Officer)

**Executive attendees (present for relevant items):**
- Priya Raman, General Counsel
- Tomás Reyes, Data Protection Officer
- Kwame Mensah, Head of Internal Audit
- Lena Fischer, VP Engineering
- Julia Moreau, Product Director, Beacon AI
- Mara Okafor, Head of Privacy Operations
- Aoife Brennan, Senior Privacy Counsel
- Samir Haddad, Chief Information Security Officer

Apologies: none. The agenda covered Q2 2026 privacy and risk items, including erasure-request performance and the Vault backup retention risk.

## 2. Apologies, Declarations of Interest and Minutes of the Previous Meeting

Apologies for absence were received from none of the invited directors or executive attendees; all were present.

The Chair invited declarations of interest in respect of the agenda items. No conflicts of interest were declared by any director or attendee.

The minutes of the board risk committee meeting of 19 March 2026 (CONF-BRD-2026-03-R2) were tabled for approval. The Chair noted that at that meeting the committee had deferred a decision on Atlas event-history retention, pending legal review; Priya Raman, General Counsel, had advised that the 24-month retention, originally justified by product analytics needs, lacked a documented necessity assessment.

**Resolution:** The minutes of CONF-BRD-2026-03-R2 were approved as an accurate record. Proposed: Daniel Whitfield; seconded: Helen Zhou; carried unanimously.

## 3. Agenda Item 1: DPO Compliance Report (Art. 24 Accountability)

### 3.1 Quarterly Art. 24 Self-Assessment

Tomás Reyes, Data Protection Officer, presented the quarterly self-assessment against Article 24 accountability obligations, conducted using checklist INT-CKL-24 and covering RoPA currency, DPIA coverage, training completion and breach-log completeness. He noted that results are filed with his quarterly report to the CEO under the Article 38(3) reporting line documented in INT-CHARTER-01. He stated that, taken together, the quarter's findings showed that while Acme's documented accountability framework remained in place, several operational indicators had deteriorated and required board attention.

### 3.2 DPC Complaint-Based Inquiry CONF-DPC-2026-0117

Tomás Reyes reported that the Irish Data Protection Commission opened a complaint-based inquiry, reference CONF-DPC-2026-0117, on 3 February 2026, concerning a delayed erasure request handled through the PrivacyDesk queue INT-Q-ERASE. He drew the board's attention to Priya Raman's legal analysis in CONF-LEGAL-2026-03, which estimates exposure under Article 83(5) — infringement of Articles 12(3) and 17, attracting fines of up to EUR 20 million or 4% of total worldwide annual turnover — and recommends settling the matter without formal proceedings. Priya Raman confirmed the recommendation and advised that early cooperation would weigh in Acme's favour under the Article 83(2) factors.

### 3.3 Internal Audit Findings CONF-AUD-2026-02

Kwame Mensah, Head of Internal Audit, presented the findings of CONF-AUD-2026-02. He reported that the record of processing activities maintained in INT-REG-ROPA was 40% out of date as of the June 2026 internal audit, and that Acme cannot rely on the Article 30(5) small-enterprise exemption because its processing is not occasional. He noted that an Article 30 infringement falls under Article 83(4), with fines of up to EUR 10 million or 2% of total worldwide annual turnover, and that the audit estimated realistic DPC fine exposure from the combined RoPA and training gaps at EUR 250,000–900,000. The board noted the estimate.

### 3.4 Training Completion and DSR Handling

Tomás Reyes reported that the 2025 annual training completion rate of 96%, achieved against the 2025-12-15 deadline, concealed a concentrated gap: 31% of Customer Support agents in Owen Gallagher's team had not completed INT-COURSE-SUP-115 by the deadline. He further reported that three of those agents mishandled data-subject request tickets received via HelpHub in January 2026, which he assessed as an Article 39(1)(b) monitoring failure on the part of his own office. He stated that the gap had been logged in the privacy risk register (INT-RISK-REG) as CONF-RISK-04, with remediation of the support-agent training pipeline assigned to Owen Gallagher's team.

### 3.5 Actions Arising from Agenda Item 1

| # | Action | Owner | Due Date |
|---|---|---|---|
| A1.1 | Provide the board with a written update on the CONF-DPC-2026-0117 settlement approach | Priya Raman | 2026-07-31 |
| A1.2 | Present a RoPA remediation plan addressing the 40% currency gap | Mara Okafor | 2026-07-31 |
| A1.3 | Report monthly on INT-COURSE-SUP-115 completion in Customer Support until closure of CONF-RISK-04 | Owen Gallagher | First report 2026-07-15 |

## 4. Agenda Item 2: Erasure Request Operations and the Atlas Deletion Job

### 4.1 Internal SLA Performance in INT-Q-ERASE

Mara Okafor, Head of Privacy Operations, reported on erasure-request operations against the internal SLA of 20 calendar days from identity verification, logged in the PrivacyDesk queue INT-Q-ERASE. She reminded the board that this internal target is stricter than the one-month statutory deadline in Article 12(3) GDPR. She described the escalation model: tickets breaching day 14 are escalated to the Privacy Operations lead, and breaches of day 20 are reported weekly to the DPO, Tomás Reyes, and to Lena Fischer, VP Engineering, for system-level causes.

### 4.2 Atlas Deletion Job Defect

Mara Okafor reported that the Atlas deletion job, which runs nightly, has a known defect: it fails on records with more than 500 linked event rows, requiring manual re-runs by the Data Platform team and adding an average of six days to affected tickets. Lena Fischer confirmed the defect is understood and reproducible, and that the Data Platform team prioritises affected re-runs, but that the failure mode recurs on high-volume event records.

### 4.3 H1 2026 Internal Audit Finding

Kwame Mensah, Head of Internal Audit, presented the H1 2026 audit finding: 14% of erasure requests in the audited period exceeded the 20-day internal SLA, with the Atlas deletion job identified as the main cause. He confirmed that all affected requests were nonetheless completed within the statutory one month under Article 12(3) GDPR, and that the finding is recorded in the audit report CONF-AUD-2026-02.

### 4.4 Remediation Budget

The board noted that the executive team had approved a remediation budget of EUR 180,000 to rewrite the Atlas deletion job, with a target of full erasure execution within five days of trigger and delivery by Q1 2027, owned by Lena Fischer. The justification, as presented, is that repeated SLA breaches risk complaints to the Irish Data Protection Commission under Article 77 GDPR and Article 83(5) exposure for infringement of Articles 12(3) and 17.

### 4.5 Actions Arising from Agenda Item 2

| # | Action | Owner | Due Date |
|---|---|---|---|
| A2.1 | Deliver the rewritten Atlas deletion job meeting the 5-day execution target | Lena Fischer | Q1 2027 |
| A2.2 | Report monthly to the board on INT-Q-ERASE SLA breach rates until the rewrite lands | Mara Okafor | First report 2026-07-15 |

## 5. Agenda Item 3: Vault Backup Erasure Risk and Resolution CONF-BRD-2026-06-R3

### 5.1 Presentation of the Vault Erasure Risk

Samir Haddad, Chief Information Security Officer, presented the residual erasure risk arising from the Vault backup system. He explained that Vault backups are write-once and retained for a fixed 35 days, and that erasure cannot be executed inside Vault. As a result, when an erasure request is granted, deletion propagates into Vault only when each backup expires naturally; Privacy Operations records the expiry date on the ticket in INT-Q-ERASE. Personal data of data subjects whose erasure requests have been granted therefore remains in Vault immutable backups for up to 35 days after execution.

Samir Haddad further described the compensating controls: erased records are recorded on the suppression list INT-FORM-07, so suppressed records are never restored to production, and Vault ages out naturally without manual deletion. Access to restored Vault data for erasure-related purposes is restricted by the CISO.

### 5.2 Legal Analysis: CONF-MEMO-2026-ERASE

Aoife Brennan, Senior Privacy Counsel, presented her legal memorandum of 3 June 2026, filed as CONF-MEMO-2026-ERASE. She concluded that Vault's 35-day immutable retention is defensible as a security backup practice in the manner of Articles 32 and 5(1)(f) GDPR, but only on two conditions: first, that Acme does not access restored backups to resurrect erased profiles, which is enforced through the CISO's access restrictions; and second, that the suppression list INT-FORM-07 is applied without exception. She noted that the erasure cannot be fully realised for up to 35 days, and that this is defensible under Article 17 as disproportionate effort, but only if the suppression list operates without exception — a condition that failed in CONF-INC-2025-0412, the April 2025 incident in which an Internal Audit test found the legal-hold process had failed for three ex-employee records, which were deleted on schedule despite active litigation holds.

### 5.3 Resolution CONF-BRD-2026-06-R3

The Chair invited the board to consider formal acceptance of the residual risk that personal data of subjects whose erasure requests are granted remains in Vault immutable backups for up to 35 days after execution.

**Resolution CONF-BRD-2026-06-R3:** The board formally accepted the residual risk that personal data of data subjects whose erasure requests are granted remains in Vault immutable backups for up to 35 days after execution, subject to the ongoing application of the INT-FORM-07 suppression list and the CISO's access restrictions on restored Vault data. Proposed: Daniel Whitfield; seconded: Helen Zhou; carried, with one dissent recorded below.

### 5.4 DPO Dissent (Minuted)

Tomás Reyes, Data Protection Officer, dissented from Resolution CONF-BRD-2026-06-R3 and asked that his dissent be minuted. He argued that the 35-day retention of erased data in Vault should be disclosed in Acme's privacy notice, and that Acme should evaluate moving to a shorter backup retention period or an encryption-key destruction approach that would render backup data unintelligible on erasure. He cautioned that accepting an undisclosed residual gap between executed erasure and actual deletion weakens Acme's Article 24 accountability position while the DPC inquiry CONF-DPC-2026-0117 remains open. The board thanked the DPO for his position and noted that the trust center already states that backups are retained for 35 days and that data deleted at a customer's request is not restored from backup.

### 5.5 Actions Arising from Agenda Item 3

| # | Action | Owner | Due Date |
|---|---|---|---|
| A3.1 | Review whether the privacy notice should expressly disclose the 35-day Vault backup expiry window, and report to the board | Aoife Brennan | 2026-09-30 |
| A3.2 | Evaluate a shorter backup retention period or an encryption-key destruction approach for Vault, with a costed feasibility assessment | Samir Haddad | 2026-10-31 |
| A3.3 | Confirm in writing that INT-FORM-07 suppression-list application is tested quarterly, with results reported to the Privacy Steering Group | Mara Okafor | First report 2026-07-15 |

## 6. Agenda Item 4: Atlas Event-History Retention and Beacon AI

### 6.1 Proposal to Extend Atlas Event-History Retention

Daniel Whitfield, Chief Executive Officer, and Helen Zhou, Chief Financial Officer, proposed extending Atlas event-history retention from the current 24 months to 36 months, in order to provide a longer training window for the Beacon AI lead-scoring model. Julia Moreau, Product Director, Beacon AI, confirmed that the lead-scoring model, which was subject to DPIA-2025-014, would benefit from the extended event history, and noted that this proposal had previously been raised in the executive discussion recorded as CONF-RISK-07, which she had initiated jointly with Helen Zhou.

### 6.2 Objections from General Counsel and the DPO

Priya Raman, General Counsel, objected to the proposed extension. She advised that the gap between the public 30-day deletion promise and Atlas's actual 24-month event-history retention — a discrepancy documented in the internal retention register INT-REG-RET v3.2, owned by Mara Okafor — is already an Article 5(1)(e) storage-limitation and Article 5(2) accountability exposure, assessed by Aoife Brennan as material and recorded in CONF-RISK-07. Extending retention to 36 months would widen that gap and weaken Acme's accountability position.

Tomás Reyes, Data Protection Officer, supported the objection. He reminded the board that the 24-month retention had been justified by product analytics needs but lacks a documented necessity assessment, as advised by Priya Raman at the board risk committee on 19 March 2026 (CONF-BRD-2026-03-R2), where the decision was deferred pending legal review. He added that an enlarged gap would compound the exposure while the DPC inquiry CONF-DPC-2026-0117 remains open.

### 6.3 Resolution CONF-BRD-2026-06-R3 (Retention Outcome)

The board rejected the proposed 36-month extension of Atlas event-history retention. In place of the extension, the board approved a 90-day remediation plan to cut Atlas event-history retention from 24 months to 12 months and to align the public privacy notice with actual practice. Delivery is owned by Lena Fischer's engineering team, with completion by 2026-12-31.

### 6.4 FY2027 Privacy Remediation Budget and Headcount

The board approved a privacy remediation budget of EUR 1.8 million for FY2027, covering RoPA tooling, DPIA automation and training platform upgrades. The board, however, cut the requested privacy headcount from four additional staff to two, rejecting the staffing assessment submitted by Tomás Reyes and Mara Okafor.

Helen Zhou, Chief Financial Officer, argued that the two approved privacy hires could be deferred to Q2 FY2027 to protect margin.

### 6.5 Dissent (Minuted)

Tomás Reyes, Data Protection Officer, and Kwame Mensah, Head of Internal Audit, dissented in writing from the headcount reduction and the proposed deferral, and asked that their dissent be minuted. They warned that the open DPC inquiry CONF-DPC-2026-0117 makes the deferral indefensible under the Article 83(2) factors, which weigh mitigation and cooperation in Acme's favour only if remediation is demonstrably resourced and delivered. The board noted the dissent and confirmed the budget and reduced headcount as resolved.

### 6.6 Actions Arising from Agenda Item 4

| # | Action | Owner | Due Date |
|---|---|---|---|
| A4.1 | Deliver the 90-day remediation plan cutting Atlas event-history retention to 12 months | Lena Fischer | 2026-12-31 |
| A4.2 | Align the public privacy notice with actual Atlas retention practice as part of the remediation plan | Lena Fischer | 2026-12-31 |
| A4.3 | Update CONF-RISK-07 to record the board's rejection of the 36-month extension and the 12-month remediation decision | Mara Okafor | 2026-07-15 |
| A4.4 | Provide a written plan for onboarding the two approved privacy hires, with the deferral question revisited at the next board meeting | Helen Zhou | 2026-07-31 |

## 7. Agenda Item 5: Beacon AI Lead-Scoring DPIA and Launch-Gate Breach

### 7.1 CONF-RISK-11: Launch Before DPIA Sign-Off

Julia Moreau, Product Director, Beacon AI, and Lena Fischer, VP Engineering, reported on CONF-RISK-11. They confirmed that the Beacon AI lead-scoring feature launched on 6 October 2025, two weeks before the mitigation sign-off for DPIA-2025-014 was complete, in breach of Acme's own privacy review gate: every Beacon feature that processes personal data requires a completed privacy review form INT-FORM-07, signed by the DPO or Mara Okafor, before code freeze. Julia Moreau acknowledged that the feature additionally required a DPIA under Article 35(3)(a) GDPR because it evaluates personal aspects based on automated processing.

### 7.2 DPIA-2025-014 and Art. 22(3) Safeguards

Julia Moreau summarised DPIA-2025-014, completed on 29 August 2025 and led by her with DPO advice under Article 35(2). The DPIA concluded that the processing is high-risk but mitigable, and mandated human-review safeguards under Article 22(3), including a right-to-contest workflow in Beacon Settings > Privacy. The board noted that these safeguards remain in operation.

### 7.3 Retroactive Acceptance and Completed Remediation

Tomás Reyes reported that the Privacy Steering Group accepted the launch retroactively on 28 October 2025, with a six-week remediation deadline, which Lena Fischer's engineering team met on 5 December 2025. The board noted the closure of the remediation and that CONF-RISK-11 remains logged in INT-RISK-REG.

### 7.4 Actions Arising from Agenda Item 5

| # | Action | Owner | Due Date |
|---|---|---|---|
| A5.1 | Confirm in writing that INT-FORM-07 gate compliance is tested for all new Beacon features, reporting to the board quarterly | Lena Fischer | First report 2026-09-30 |

## 8. Resolutions Adopted

The following resolutions were adopted at the meeting of 12 June 2026, chaired by Margaret Ellison:

1. **CONF-BRD-2026-06-R3 — Vault residual erasure risk acceptance.** The board formally accepted the residual risk that personal data of data subjects whose erasure requests are granted remains in Vault immutable backups for up to 35 days after execution, subject to the INT-FORM-07 suppression list and the CISO's access restrictions on restored Vault data. Carried with one dissent, recorded in section 5.4 (Tomás Reyes, DPO).

2. **Atlas event-history retention.** The board rejected the proposed extension of Atlas event-history retention from 24 to 36 months and approved a 90-day remediation plan to reduce retention to 12 months and align the public privacy notice with actual practice, owned by Lena Fischer, due 2026-12-31.

3. **FY2027 privacy remediation budget.** The board approved a privacy remediation budget of EUR 1.8 million for FY2027 covering RoPA tooling, DPIA automation and training platform upgrades, with additional privacy headcount reduced from four to two. The written dissent of Tomás Reyes and Kwame Mensah on the headcount reduction and deferral is recorded in section 6.5.

## 9. Actions Arising

The Company Secretary consolidated all actions arising from the meeting into the consolidated action register below.

| # | Action | Owner | Due Date |
|---|---|---|---|
| A9.1 | Deliver the 90-day remediation plan cutting Atlas event-history retention to 12 months, including alignment of the public privacy notice with actual practice (CONF-RISK-07) | Lena Fischer | 2026-12-31 |
| A9.2 | Deliver the rewritten Atlas deletion job, funded at EUR 180,000, meeting the 5-day erasure execution target | Lena Fischer | Q1 2027 |
| A9.3 | Complete the compliance review of the CONF-RISK-07 pseudonymisation approach (raw identifiers not retained in Atlas analytics) | Aoife Brennan | 2027-01-31 |
| A9.4 | Maintain restricted access to restored Vault data for erasure-related purposes, per the conditions in CONF-MEMO-2026-ERASE | Samir Haddad | Ongoing |
| A9.5 | Update the internal retention register INT-REG-RET to reflect the 12-month Atlas retention and the privacy notice alignment | Mara Okafor | 2026-12-31 |
| A9.6 | File the written dissents of Tomás Reyes (Resolution CONF-BRD-2026-06-R3) and of Tomás Reyes and Kwame Mensah (headcount reduction) with the board records | Company Secretary | 2026-06-30 |

Progress against actions A9.1–A9.5 will be reported at the next scheduled board meeting.

## 10. Recorded Dissents

The Company Secretary recorded the following dissents for the board record.

**10.1 Dissent of Tomás Reyes, Data Protection Officer — Resolution CONF-BRD-2026-06-R3.** Tomás Reyes dissented from the board's acceptance of the residual Vault erasure risk. He argued that the 35-day retention of erased personal data in Vault immutable backups should be disclosed in Acme's privacy notice, and that Acme should evaluate a shorter backup retention period or an encryption-key destruction approach that would render backup data unintelligible on erasure. The full text is at section 5.4.

**10.2 Joint written dissent of Tomás Reyes and Kwame Mensah — privacy headcount deferral.** Tomás Reyes and Kwame Mensah dissented in writing from the reduction of additional privacy headcount from four to two and from Helen Zhou's proposal to defer the two approved hires to Q2 FY2027. They warned that, with the DPC inquiry CONF-DPC-2026-0117 open, the deferral is indefensible under the Article 83(2) factors, which weigh mitigation and cooperation in Acme's favour only if remediation is demonstrably resourced. The board noted the dissent and confirmed its resolution as recorded at section 6.5.

Both written dissents are filed with the board records per action A9.6.

## 11. Close of Meeting and Certification

There being no further business, the Chair closed the meeting at 12 June 2026. The Company Secretary certified these minutes as a true record of the proceedings, pending approval by Margaret Ellison, Chair of the Board. These minutes are classified CONFIDENTIAL under the Data Classification Policy INT-POL-CLASS-02 and distribution is restricted to directors and executive leadership.
