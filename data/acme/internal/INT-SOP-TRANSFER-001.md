---
doc_id: "INT-SOP-TRANSFER-001"
title: "International Transfers Procedure (SCCs and TIA)"
company: "Acme Corp"
publisher: "ACME"
access_level: 1
classification: "internal"
doc_type: "sop"
profile: "company_doc"
topic: "transfers"
topics: ["transfers"]
owner: "Legal & Privacy"
approver: "Senior Privacy Counsel"
version: "1.8"
effective_date: "2026-03-30"
status: "current"
gdpr_articles: [44, 46]
related: ["PUB-SUBPROC-001"]
generator: {"writer": "@cf/zai-org/glm-5.3", "judge": "@cf/openai/gpt-oss-120b", "run_id": "20261124-025609", "prompt_hash": "284162f9dd75"}
review: {"status": "ok", "attempts": 1, "issues_left": 0, "scores": {"fact_fidelity": 5, "tier_discipline": 5, "gdpr_accuracy": 5, "realism": 5, "retrievability": 5}}
---

# International Transfers Procedure (SCCs and TIA)

| Field | Value |
|---|---|
| Document ID | INT-SOP-TRANSFER-001 |
| Version | 1.8 |
| Owner | Legal & Privacy (Privacy Operations, led by Mara Okafor) |
| Approver | Aoife Brennan, Senior Privacy Counsel (Dublin) |
| Effective date | 2026-03-30 |
| Classification | INTERNAL |
| Status | Current |
| Audience | Legal, Security and Vendor Owners |
| GDPR Articles in scope | Art. 44 (general principle for transfers), Art. 46 (appropriate safeguards) |
| Related records | Transfer register INT-REG-XFER-01 (Atlas); TIA template INT-FORM-TIA-07; TIA INT-TIA-2025-114; RoPA entry INT-ROPA-22; checklist INT-CHK-09; sub-processor notice PUB-SUBPROC-001 |

## 1. Purpose and Scope

This procedure (INT-SOP-TRANSFER-001) governs every outbound transfer of personal data from Acme Corp Ltd (Dublin) to recipients outside the European Economic Area. It implements the GDPR Art. 44 general principle that personal data may only be transferred to third countries where the level of protection guaranteed by the Regulation is not undermined, and the Art. 46 appropriate safeguards that make such transfers lawful — in Acme's case, primarily Art. 45 adequacy (including the EU-US Data Privacy Framework for US recipients) and Art. 46(2)(c) standard contractual clauses, as stated in Acme's privacy notice (version dated 2026-03-15).

This procedure applies to all systems and flows that can move personal data outside the EEA, including:

- **Acme Beacon** — EU customer data is hosted on AWS eu-west-1 (Ireland) and is not stored in the United States for primary processing;
- **Atlas** — the analytics warehouse, including its non-EEA replicas;
- **Ledger** — billing flows, including Stripe cardholder-data processing;
- **Vendor flows** — including sub-processors and intra-group transfers to Acme Corp Inc. (Austin, Texas).

The intended audience is legal, security and vendor owners. Vault backups are out of scope because they remain exclusively in eu-west-1 (see checklist INT-CHK-09).

## 2. Roles and Responsibilities

Responsibility for international transfers under this procedure is allocated as follows. The transfer register INT-REG-XFER-01 in Atlas, which lists the 11 outbound transfer routes outside the EEA (as of 2026-09-15) each mapped to its legal mechanism, is maintained by Privacy Operations, led by Mara Okafor.

| Activity | Responsible | Accountable | Consulted | Informed |
|---|---|---|---|---|
| Maintain transfer register INT-REG-XFER-01 (Atlas) | Mara Okafor, Privacy Operations | Aoife Brennan, Senior Privacy Counsel | Vendor owners | DPO |
| Own and update TIA template INT-FORM-TIA-07 | Aoife Brennan's legal team | Aoife Brennan, Senior Privacy Counsel | Mara Okafor; Samir Haddad (CISO) | Vendor owners |
| Complete TIA before a new non-EEA vendor goes live (15-business-day SLA from onboarding start) | Vendor owner, with Privacy Operations support | Mara Okafor | Aoife Brennan's legal team | DPO |
| Review parent-access log monthly (queue INT-Q-PARENT-ACCESS, logged in Atlas) | Tomás Reyes, DPO | Tomás Reyes, DPO | Mara Okafor | Aoife Brennan |
| Define and own supplementary technical measures (e.g. TLS 1.3 in transit, AES-256 at rest, pseudonymisation before export to Atlas replicas) | Samir Haddad, CISO | Samir Haddad, CISO | Lena Fischer, VP Engineering | Privacy Operations |
| Supply vendor information for TIAs (destination-law position, government-access challenge commitment, hosting locations) | Vendor owner | Mara Okafor | Legal & Privacy | DPO |

Vendor owners must supply complete and accurate vendor information to Privacy Operations on request; an incomplete TIA cannot be signed off and the vendor must not go live.

## 3. Legal Mechanisms for Transfers

Acme Corp Ltd relies on three lawful mechanisms for outbound transfers of personal data outside the EEA, in line with the privacy notice (version dated 2026-03-15) and the GDPR Art. 44 general principle.

### 3.1 Art. 45 Adequacy Decisions

Personal data may be transferred to a country covered by an adequacy decision without further safeguards. For US recipients, Acme relies on the EU-US Data Privacy Framework where the recipient is certified — for example, MetricPulse Inc. has been DPF-certified since 2024-02-10. Vendor owners must verify and evidence the recipient's current certification before relying on this mechanism.

### 3.2 Art. 46(2)(c) Standard Contractual Clauses

Where no adequacy decision applies, transfers must be covered by the 2021 EU Commission standard contractual clauses. Acme uses the module matching the relationship: module two (controller-to-processor) for sub-processors such as MetricPulse Inc., and module one (controller-to-controller) for intra-group flows such as the Beacon AI lead-scoring transfer to Acme Corp Inc. (RoPA entry INT-ROPA-22). Following the CJEU Schrems II judgment, every SCC-based transfer requires a completed transfer impact assessment (see section 4) and supplementary measures where required.

### 3.3 Art. 49 Derogations

Art. 49 derogations (for example, explicit consent or necessity for contract performance) are interpreted restrictively and may not support routine, systematic transfers. Any reliance on a derogation requires prior approval from Aoife Brennan, Senior Privacy Counsel, and must be recorded in the transfer register INT-REG-XFER-01.

### 3.4 Transfers That Do Not Arise

EU customer data in the Acme Beacon platform is hosted on AWS infrastructure in eu-west-1 (Ireland) and is not stored in the United States for primary processing, so no Chapter V transfer arises for primary hosting. Vault backups (35-day retention, write-once) remain exclusively in eu-west-1; checklist INT-CHK-09 confirms no Vault backup is replicated outside the EEA, so no Chapter V transfer applies to backups.

## 4. Transfer Register and Onboarding Procedure

This section sets out how a new non-EEA transfer route is added at Acme Corp Ltd. Privacy Operations, led by Mara Okafor, maintains the transfer register INT-REG-XFER-01 in Atlas, which lists all outbound transfer routes outside the EEA (11 routes as of 2026-09-15), each mapped to its legal mechanism (Art. 45 adequacy, Art. 46(2)(c) SCCs module, or Art. 49 derogation).

### 4.1 Steps to Add a New Non-EEA Transfer Route

1. **Notify.** The vendor owner notifies Privacy Operations (privacy@acme.example) before onboarding begins, identifying the vendor, data categories, processing location and purpose.
2. **Complete the TIA.** The vendor owner completes the TIA template INT-FORM-TIA-07, owned by Aoife Brennan's legal team, within **15 business days of vendor onboarding start**. This is Acme's internal SLA and is stricter than the GDPR, which sets no fixed TIA deadline. The vendor must not go live until the TIA is signed off.
3. **Confirm the legal mechanism.** Privacy Operations confirms the Art. 45 adequacy, Art. 46(2)(c) SCCs module or Art. 49 derogation relied on (see section 3).
4. **Record the route.** Privacy Operations records the route in register INT-REG-XFER-01 in Atlas, mapped to its legal mechanism.
5. **Update the sub-processor list.** The sub-processor list is updated and customers are notified of the change in advance, per Acme's stated commitment that a current list of sub-processors and their processing countries is available on request via privacy@acme.example.

### 4.2 Onboarding Checklist

- [ ] Vendor owner notification received by Privacy Operations
- [ ] TIA INT-FORM-TIA-07 completed within 15 business days
- [ ] Legal mechanism confirmed and evidenced
- [ ] Route recorded in INT-REG-XFER-01 (Atlas)
- [ ] Sub-processor list updated; customers notified in advance

### 4.3 Records

Onboarding records (notification, completed TIA, register entry and customer notification evidence) are retained by Privacy Operations to demonstrate Art. 5(2) accountability.

## 5. Transfer Impact Assessments and Supplementary Measures

Following the CJEU Schrems II judgment, Acme carries out transfer impact assessments for every transfer relying on standard contractual clauses and adds supplementary measures where required, as stated on the Acme trust center. The TIA template INT-FORM-TIA-07, owned by Aoife Brennan's legal team, must be completed and signed off before any new non-EEA vendor goes live (15-business-day SLA, section 4.1).

### 5.1 TIA Methodology

The vendor owner, supported by Privacy Operations, completes INT-FORM-TIA-07 by assessing:

1. The destination country's surveillance and government-access laws affecting the vendor and its hosting providers;
2. Whether those laws, in practice, could undermine the Art. 44 level of protection despite SCCs;
3. The technical and contractual supplementary measures needed to close any gap;
4. A residual destination-law risk rating (low / medium / high) and sign-off by Mara Okafor.

### 5.2 Standard Supplementary Measures for US Transfers

INT-FORM-TIA-07 lists the standard measures applied to US transfers:

- TLS 1.3 for data in transit;
- AES-256 encryption at rest;
- Pseudonymisation of end-user identifiers before export to Atlas replicas;
- A documented government-access challenge commitment from the vendor.

Samir Haddad (CISO) owns the technical measures; the vendor owner supplies the challenge commitment.

### 5.3 Worked Example: MetricPulse Inc.

The TIA for MetricPulse Inc. (US product-analytics vendor processing Beacon end-user event data on AWS us-east-1 under 2021 SCCs module two, DPF-certified since 2024-02-10) is recorded as INT-TIA-2025-114 and was signed off by Mara Okafor on 2025-08-22. Applying the standard supplementary measures, the destination-law risk was scored as **medium** after mitigation. One remediation item remains open: encryption keys must be held solely in eu-west-1 by Acme, not by the vendor. The vendor must not process data under keys it controls until this item closes.

### 5.4 Periodic Review

Mara Okafor runs a quarterly TIA review cycle. The 2026-Q3 review (2026-09-05) re-approved 10 of the 11 transfer routes and flagged INT-TIA-2025-114 (MetricPulse) for re-assessment before 2026-12-31. The vendor owner must close the key-custody item before that re-assessment.

## 6. Named Transfer Routes

The transfer register INT-REG-XFER-01 (Atlas) lists 11 outbound transfer routes as of 2026-09-15. The four key routes below are the ones legal, security and vendor owners will most frequently encounter; each is mapped to its legal mechanism under Art. 45 or Art. 46(2)(c).

| Route | Recipient and location | Data and purpose | Legal mechanism | Key controls |
|---|---|---|---|---|
| MetricPulse Inc. (product analytics) | US; hosted on AWS us-east-1 | Beacon end-user event data | 2021 SCCs, module two (controller-to-processor); vendor DPF-certified since 2024-02-10 | TIA INT-TIA-2025-114; standard supplementary measures (section 5.2); key-custody remediation open |
| Stripe (billing via Ledger) | US recipient; EU cardholder data | Cardholder data for billing and invoicing | Stripe's SCC-based transfer framework | Tokenisation applied before any non-EEA processing; no raw card numbers leave the EEA |
| Beacon AI lead scoring | Acme Corp Inc., Austin, Texas | Pseudonymised feature vectors for model training (not raw customer records) | 2021 SCCs, module one (controller-to-controller) | Documented in RoPA entry INT-ROPA-22; directed by Julia Moreau |
| Parent-company access | Acme Corp Inc., Austin, Texas | Limited personal data for group administration and product support | EU-US Data Privacy Framework or SCCs, as disclosed in the privacy notice | Routed through queue INT-Q-PARENT-ACCESS; logged in Atlas |

### 6.1 Parent-Company Access Controls

Parent-company access by Acme Corp Inc. staff in Austin is never ad hoc: it must be requested through the ticket queue INT-Q-PARENT-ACCESS with a named business justification, and every access is logged in Atlas. Tomás Reyes (DPO) reviews the access log monthly. Vendor owners and support leads must not grant US-based staff direct access outside this queue.

### 6.2 Route Changes

Any change to a route in the table above (new data categories, new hosting location, change of SCC module) triggers a new or updated TIA under section 5 and an update to INT-REG-XFER-01 before the change goes live.

## 7. Quarterly Review and Re-Assessment

Mara Okafor (Privacy Operations) runs a quarterly TIA review cycle covering every route in the transfer register INT-REG-XFER-01 (Atlas). Each quarterly review re-checks the legal mechanism, the destination-law position, the vendor's EU-US Data Privacy Framework certification status (where relied on) and the open remediation items from each TIA.

### 7.1 2026-Q3 Review Outcome

The 2026-Q3 review, completed 2026-09-05, re-approved 10 of the 11 transfer routes. It flagged TIA INT-TIA-2025-114 (MetricPulse Inc.) for re-assessment before 2026-12-31, because its open remediation item — encryption keys held solely in eu-west-1 by Acme, not by the vendor — remains unclosed. The MetricPulse route continues to operate under its medium residual risk rating and standard supplementary measures (section 5.2) until re-assessment.

### 7.2 Out-of-Cycle Re-Assessment Triggers

A route must be re-assessed outside the quarterly cycle whenever:

- The vendor changes (new hosting location, sub-processor chain, or data categories);
- New destination-law facts emerge (legislation, court rulings, regulator guidance);
- The vendor's DPF certification status changes or lapses;
- An open remediation item passes its due date without closure.

The vendor owner notifies privacy@acme.example immediately; Mara Okafor decides whether processing continues pending re-assessment. Unresolved high-risk findings are escalated to Aoife Brennan (Senior Privacy Counsel) and, if suspension of the route is contemplated, to Tomás Reyes (DPO) and Samir Haddad (CISO).

## 8. Exceptions, Records and Compliance

### 8.1 Exceptions

Any exception to this procedure requires prior written approval from Aoife Brennan, Senior Privacy Counsel (Dublin). Art. 49 derogations may be used only for specific situations and are interpreted restrictively; they may not support routine or systematic transfers. Every approved exception and any reliance on an Art. 49 derogation must be recorded in the transfer register INT-REG-XFER-01 (Atlas).

### 8.2 Records

To demonstrate Art. 5(2) accountability, Privacy Operations retains:

- Completed transfer impact assessments (template INT-FORM-TIA-07) and sign-offs;
- The transfer register INT-REG-XFER-01 (Atlas), listing all 11 outbound transfer routes outside the EEA (as of 2026-09-15) with their legal mechanisms;
- Parent-company access logs from queue INT-Q-PARENT-ACCESS, logged in Atlas with named business justifications;
- Minutes and outcomes of the quarterly TIA review cycle run by Mara Okafor.

### 8.3 DPO Oversight

Tomás Reyes (DPO) reviews the parent-access log monthly and reports findings to Privacy Operations.

### 8.4 Escalation

Any breach of this procedure — including a non-EEA vendor going live without a completed TIA (INT-FORM-TIA-07, 15-business-day SLA) — must be escalated to Tomás Reyes, DPO, without delay, and to Aoife Brennan where legal remediation is required.

## 9. Document Control and Revision History

| Field | Value |
|---|---|
| Document ID | INT-SOP-TRANSFER-001 |
| Version | 1.8 |
| Owner | Legal & Privacy (Privacy Operations, led by Mara Okafor) |
| Approver | Aoife Brennan, Senior Privacy Counsel (Dublin) |
| Effective date | 2026-03-30 |
| Classification | INTERNAL |
| Status | Current |
| Next scheduled review | Quarterly, aligned to the TIA review cycle run by Mara Okafor |

### 9.1 Revision History

| Version | Date | Summary of change |
|---|---|---|
| 1.8 | 2026-03-30 | Current version. Clarified the 15-business-day TIA SLA for new non-EEA vendors (INT-FORM-TIA-07) and aligned the onboarding checklist with the transfer register INT-REG-XFER-01. |
| 1.7 | 2026-01-15 | Added section 6.1 parent-company access controls (queue INT-Q-PARENT-ACCESS) and monthly DPO log review. |
| 1.6 | 2025-09-10 | Incorporated the quarterly TIA review cycle and out-of-cycle re-assessment triggers following the Schrems II TIA methodology. |

### 9.2 Change Requests

Proposed changes to this procedure are submitted to privacy@acme.example and require approval from Aoife Brennan, Senior Privacy Counsel, before a new version takes effect.
