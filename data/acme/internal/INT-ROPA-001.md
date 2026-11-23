---
doc_id: "INT-ROPA-001"
title: "Record of Processing Activities (extract)"
company: "Acme Corp"
publisher: "ACME"
access_level: 1
classification: "internal"
doc_type: "register"
profile: "company_doc"
topic: "processors"
topics: ["processors", "retention", "consent"]
owner: "Privacy Office"
approver: "Data Protection Officer"
version: "2026.3"
effective_date: "2026-07-31"
status: "current"
gdpr_articles: [30]
related: ["INT-SCHED-RET-001"]
generator: {"writer": "@cf/zai-org/glm-5.3", "judge": "@cf/openai/gpt-oss-120b", "run_id": "20261124-025609", "prompt_hash": "284162f9dd75"}
review: {"status": "ok", "attempts": 2, "issues_left": 0, "scores": {"fact_fidelity": 5, "tier_discipline": 5, "gdpr_accuracy": 5, "realism": 5, "retrievability": 5}}
---

# Record of Processing Activities (extract)

| Field | Value |
|---|---|
| Document ID | INT-ROPA-001 |
| Version | 2026.3 |
| Owner | Privacy Office (Mara Okafor, Head of Privacy Operations) |
| Approver | Tomás Reyes, Data Protection Officer |
| Effective date | 2026-07-31 |
| Classification | INTERNAL |
| Status | Current |
| Audience | Privacy team and auditors |
| Legal basis | GDPR Art. 30(1) (controller) and Art. 30(2) (processor) |
| Maintained in | INT-REG-ROPA (full register); this document is an approved extract of 8 of the 14 processing activities |

This extract is maintained by the Privacy Operations team and reconciled quarterly against the full record INT-REG-ROPA. Acme Corp Ltd cannot rely on the small-enterprise exemption under Art. 30(5) because its processing is not occasional.

## 1. Document Control

| Field | Value |
|---|---|
| Document ID | INT-ROPA-001 |
| Version | 2026.3 |
| Owner | Mara Okafor, Head of Privacy Operations (Privacy Office) |
| Approver | Tomás Reyes, Data Protection Officer |
| Effective date | 2026-07-31 |
| Classification | INTERNAL |
| Status | Current |
| Audience | Privacy team and auditors |

This record is maintained by the Privacy Operations team under GDPR Art. 30(1) (controller activities) and Art. 30(2) (processor activities for Acme Beacon), consistent with Acme's Trust Center commitment. Acme Corp Ltd cannot rely on the small-enterprise exemption in Art. 30(5), because its core processing — customer account data, marketing, and processor-side Beacon operations — is regular and systematic rather than occasional.

The complete record is maintained in the internal register INT-REG-ROPA, which lists retention periods per data category for all 14 processing activities. This document is an approved extract covering 8 of those 14 activities, provided for privacy team and auditor use; where a full view is required, consult INT-REG-ROPA directly.

## 2. Scope and Register Conventions

This extract covers Acme Corp Ltd's processing activities in both of its GDPR roles:

- **Controller** (Art. 30(1)): processing of Acme's own customers' account data, employee data, website-visitor data, and direct marketing.
- **Processor** (Art. 30(2)): processing of customers' end-user data stored and processed in Acme Beacon, carried out on each customer controller's documented instructions.

For each processing activity, the register records the fields required by Art. 30: purpose of processing; categories of data subjects; categories of personal data; categories of recipients, including sub-processors such as AWS (eu-west-1) and Stripe; transfers of personal data to third countries and the transfer basis; retention periods per data category; and Art. 32 security measures.

**Register conventions:**

- The processor-side (Art. 30(2)) record is fed from the Atlas table VENDORS_ROPA, maintained by Privacy Operations. Each vendor entry captures vendor name, service, DPA signature date, SCC module, transfer basis, and renewal date. Mara Okafor reconciles VENDORS_ROPA quarterly against Ledger's supplier list.
- Vendor privacy due diligence runs through the PrivacyDesk intake queue INT-Q-VENDOR. Every new vendor touching personal data requires a completed screening form INT-FORM-07 (data categories, volumes, hosting regions, transfer basis) before procurement can sign.
- Retention periods stated in this extract reflect the internal retention register INT-REG-RET; where an internal period differs from a public commitment, the internal value is shown and flagged.
- Controller-side activities are owned by the Privacy Office; processor-side activities are owned jointly with the Beacon product and engineering teams.

## 3. Register of Processing Activities — Controller-Side

The five controller-side activities below are processed by Acme Corp Ltd as controller under Art. 30(1). Acme is controller for its own customers' account data, employees, website visitors and marketing; the lawful basis for each activity is determined by Acme, not by its customers.

### 3.1 Controller Activities Register

| # | Activity | Purpose | Lawful basis | Data categories | Recipients | Retention | Security measures (Art. 32) |
|---|---|---|---|---|---|---|---|
| C-01 | Customer account management | Provision and administration of customer accounts for Acme Beacon, including account setup, authentication, service and transactional emails, and self-service export/deletion via Beacon Settings > Privacy | Art. 6(1)(b) contract performance; service/transactional emails are not marketing | Account holder name, business email, company, hashed credentials, account settings | Internal account and support teams; AWS (eu-west-1, Dublin) as hosting sub-processor | Deleted within 30 days after account closure (Art. 5(1)(e)); exceptions require DPO sign-off and are logged in INT-REG-EXC | Encryption at rest and in transit; role-based access control; access logging; Vault write-once backups retained 35 days |
| C-02 | Direct marketing emails | Sending of direct marketing email campaigns to Acme's own contacts | Art. 6(1)(a) consent; withdrawal as easy as giving consent (Art. 7(3)) via the marketing preferences page | Name, business email, consent record (timestamp, channel, consent-string version, IP at collection), campaign engagement | Internal marketing team; email delivery sub-processors per the public Trust Center register | Consent events retained 3 years after withdrawal in the Atlas consent_events table to satisfy Art. 5(2) accountability; withdrawn contacts remain on the suppression list, synced from Atlas every 6 hours | Consent records and suppression lists stored in Atlas with access logging; campaign launch blocked without a passing INT-CKL-02 consent verification checklist |
| C-03 | Website cookies and own product-usage analytics | Measurement and improvement of Acme's own website using pseudonymised usage analytics; non-essential analytics and marketing cookies | Art. 6(1)(f) legitimate interests for pseudonymised analytics, documented on form INT-FORM-07 and reviewed annually against EDPB Guidelines 01/2024; Art. 6(1)(a) consent for non-essential cookies via the CMP v3 banner | Pseudonymised browsing and interaction data, cookie identifiers, banner interaction events | Internal analytics team; AWS (eu-west-1) | Analytics data pseudonymised; consent and banner interaction events logged to Atlas and retained per INT-REG-RET | CMP v3 blocks analytics and marketing tags until positive action; opt-out link in the privacy notice enables objection under Art. 21(1) at any time |
| C-04 | Billing and invoicing (Ledger) | Customer billing, invoicing, payment collection and financial reporting | Art. 6(1)(c) legal obligation (Irish tax law); Art. 6(1)(b) contract for payment performance | Customer contact details, billing address, invoice line items, payment references; card data handled by Stripe | Stripe (payment processing sub-processor); internal finance team; Irish tax authorities as required | 6 years to meet Irish tax law (F-RET-02); thereafter deletion job INT-JOB-LEDGER-PURGE removes invoice line items and keeps anonymised totals for financial reporting | Ledger access restricted to finance roles; Stripe processes billing personal data under Art. 28(3) terms reviewed annually |
| C-05 | HR / employee administration | Recruitment, onboarding, payroll, performance management and statutory employment reporting for Acme's ~450 employees | Art. 6(1)(b) contract (employment); Art. 6(1)(c) legal obligation (Irish employment, payroll and tax law) | Employee identity, contact, contract, payroll, benefits, performance and absence data | Internal HR and payroll teams; payroll providers per the Atlas VENDORS_ROPA register; Irish revenue and pension authorities as required | Per employment law and INT-REG-RET; legal holds requested via INT-FORM-12 override deletion jobs and are reviewed every 6 months | Restricted HR systems access; encryption at rest; Vault backup coverage under the 35-day write-once standard |

### 3.2 Notes on Controller-Side Retention

- Customer account data deletion within 30 days of closure is enforced by deletion jobs INT-JOB-DEL-01 (nightly, Atlas) and INT-JOB-DEL-02 (weekly, Beacon production), owned by Privacy Operations (Mara Okafor).
- Where a legal hold or legal obligation applies — including defence of legal claims under Art. 17(3)(e) — data may be retained longer and the reason is documented.
- Retention periods above reflect the internal retention register INT-REG-RET; internal values are authoritative where they differ from public statements.

## 4. Register of Processing Activities — Processor-Side (Beacon)

The three processor-side activities below are performed by Acme Corp Ltd as processor under Art. 30(2), on each customer controller's documented instructions. For all Beacon processing of customers' end-user data, the lawful basis is determined by each customer controller, not by Acme. Acme remains fully liable to its customers for the performance of its sub-processors, in line with Art. 28(4), and sub-processors are bound by obligations no less protective than those owed by Acme directly.

### 4.1 Processor Activities Register

| # | Activity | Purpose | Data categories | Categories of data subjects | Recipients / sub-processors | Retention | Security measures (Art. 32) |
|---|---|---|---|---|---|---|---|
| P-01 | Beacon CRM and campaign hosting | Hosting and operation of the Beacon CRM and email campaign product for customer controllers, on their documented instructions | Customer-controlled contact records, campaign content, engagement events, account configuration | Customers' end users (contacts of customer controllers) | AWS (eu-west-1, Dublin) as primary hosting sub-processor for Beacon production data; Stripe for billing personal data; both on the public Trust Center register, with Art. 28 terms reviewed annually even where the vendor's own DPA terms are accepted wholesale | Per customer instruction and DPA; deleted or returned at end of services per Art. 28(3)(g) | Encryption at rest and in transit; role-based access control; access logging; Vault write-once backups retained 35 days; annual Art. 32 technical review of the four sub-processors with production access by the security team (Samir Haddad), findings logged in INT-Q-VENDOR |
| P-02 | Product analytics storage (Atlas) | Storage and processing of Beacon product-usage event data in the Atlas analytics warehouse, on customers' documented instructions | Pseudonymised end-user event data, product interaction events, billing history linked to customer accounts | Customers' end users | Internal analytics and engineering teams acting as Acme personnel; AWS (eu-west-1) hosting | Event history retained up to 24 months after account closure — this exceeds the 30 days stated publicly and the discrepancy is documented in the internal retention register INT-REG-RET v3.2, owned by Mara Okafor | Atlas access restricted and logged; deletion enforced by nightly job INT-JOB-DEL-01; Vault backups age out naturally after 35 days |
| P-03 | Beacon AI lead-scoring feature | Model-inference lead scoring of customer CRM data under the Beacon AI feature, owned by Julia Moreau, Product Director, Beacon AI | Customer contact records and engagement features submitted for scoring; score outputs | Customers' end users | Model-inference sub-processor, added as a sub-processor on 2025-06-12 with eu-west-1 data-residency commitments; AWS (eu-west-1) hosting | Per customer instruction; inference inputs and outputs follow the P-01/P-02 retention periods | Inference processing confined to eu-west-1; sub-processor bound by Art. 28(3) terms with Art. 32 security measures |

### 4.2 Notes on Processor-Side Sub-processor Governance

- Sub-processor additions and replacements for Beacon are handled in INT-Q-SUBCH, requiring DPO Tomás Reyes's sign-off, an update to the public Trust Center register, and the 30-day customer notification (template INT-TPL-12) with an objection contact at privacy@acme.example. The Beacon AI model-inference sub-processor followed this workflow: notice was sent on 2025-06-10, and two customer objections were resolved via eu-west-1 data-residency commitments.
- The 30-day notice commitment is operationally supported by a PrivacyDesk calendar trigger 35 days before any planned change, giving Privacy Operations a 5-day drafting buffer.
- The Atlas 24-month retention of event history after account closure (P-02) is a known discrepancy against the public 30-day commitment; it is recorded in INT-REG-RET v3.2 and tracked by Privacy Operations for remediation.

## 5. Recipients, Sub-processors and Transfers

This section summarises the sub-processors with access to personal data for the eight processing activities in this extract. The authoritative source is the Atlas table VENDORS_ROPA, reconciled quarterly by Mara Okafor against Ledger's supplier list; the public-facing summary is published in the Trust Center and privacy notice.

### 5.1 Sub-processors with Access to Personal Data

| # | Sub-processor | Service | Processing activities | Hosting region | Transfer basis |
|---|---|---|---|---|---|
| S-01 | AWS | Primary hosting of Beacon production data | C-01, C-03, C-04, P-01, P-02, P-03 | eu-west-1 (Dublin, Ireland) | Intra-EU; no third-country transfer |
| S-02 | Stripe | Payment processing for billing personal data | C-04 | EU/EEA processing per Stripe DPA | Intra-EU; no third-country transfer |
| S-03 | Beacon AI model-inference vendor | Model inference for the Beacon AI lead-scoring feature (P-03) | P-03 | eu-west-1 (Dublin, Ireland) | Intra-EU; no third-country transfer |

All three sub-processors are covered by the public Trust Center register and are engaged only under written data processing agreements containing the Art. 28(3) terms; their Art. 28 terms are reviewed annually even where the vendor's own DPA terms are accepted wholesale. For the entries in this extract, all processing locations are within the EU/EEA, so no Chapter V transfer basis is required.

### 5.2 Annual Art. 32 Technical Review

The four sub-processors with access to production personal data receive an annual Art. 32-focused technical review by Samir Haddad's security team, checking encryption-at-rest, access logging, and backup retention against Vault's 35-day write-once standard. Findings are logged in INT-Q-VENDOR. Annual vendor reassessment by Privacy Operations (checklist INT-CHK-04) additionally verifies current ISO 27001 or SOC 2 Type II reports, breach-notification clauses per Art. 33(2), and DPA expiry dates.

### 5.3 Public Availability

The full sub-processor register is available on request at privacy@acme.example, per the Trust Center and the website privacy notice (updated 2026-03-15).

## 6. Retention and Security Measures Summary

This section consolidates retention periods per data category for the eight processing activities in this extract, with the Art. 32 security measures that enforce them. Internal values are authoritative; the Atlas event history discrepancy is flagged to the internal retention register INT-REG-RET v3.2, owned by Mara Okafor.

### 6.1 Retention and Enforcement Cross-Reference

| Data category | Retention period | Enforcement mechanism | Security measures |
|---|---|---|---|
| Customer account data (C-01) | Deleted within 30 days after account closure (Art. 5(1)(e)) | Nightly deletion job INT-JOB-DEL-01 (Atlas) and weekly job INT-JOB-DEL-02 (Beacon production), owned by Privacy Operations (Mara Okafor) | Encryption at rest; access logging; role-based access control |
| Ledger billing and invoicing records (C-04) | 6 years per Irish tax law; thereafter INT-JOB-LEDGER-PURGE removes invoice line items, keeping anonymised totals | INT-JOB-LEDGER-PURGE; finance-role access restriction | Encryption at rest; access logging |
| Vault backups | 35 days, write-once; ages out naturally without manual deletion | Suppression list ensures data deleted at a customer's request is never restored to production | Write-once immutable storage; erasure requests recorded on the suppression list |
| Atlas event history (P-02) | **Discrepancy:** retained up to 24 months after account closure vs the 30 days stated publicly — documented in INT-REG-RET v3.2 | Nightly job INT-JOB-DEL-01; discrepancy tracked for remediation | Restricted, logged Atlas access |

### 6.2 Legal Holds

Legal holds are requested by Aoife Brennan's legal team via INT-FORM-12 and applied in Atlas and Ledger within 5 business days. A hold overrides all deletion jobs, including INT-JOB-DEL-01 and INT-JOB-LEDGER-PURGE, and is reviewed every 6 months. Retention exceptions (open HelpHub tickets, active disputes, fraud investigations) require DPO Tomás Reyes's sign-off and are logged in INT-REG-EXC, consistent with Art. 17(3)(e) defence of legal claims.

## 7. Register Maintenance and Review

The full record INT-REG-ROPA and this extract INT-ROPA-001 are owned by Mara Okafor, Head of Privacy Operations. The processor-side feed is maintained in the Atlas table VENDORS_ROPA, which Mara Okafor reconciles quarterly against Ledger's supplier list to confirm no vendor entry is missing or stale.

- [ ] Quarterly: reconcile VENDORS_ROPA against Ledger's supplier list
- [ ] Annual: run vendor reassessment using checklist INT-CHK-04, verifying current ISO 27001 or SOC 2 Type II reports, breach-notification clause presence (processor notifies without undue delay per Art. 33(2)), and DPA expiry dates; results are stored against each Atlas VENDORS_ROPA entry
- [ ] Quarterly: Internal Audit performs retention compliance checks, testing a sample of 50 closed accounts against INT-REG-RET; the Q2 2026 check found 9 of 50 accounts still had Atlas event rows past schedule, and remediation is tracked by Privacy Operations
- [ ] On demand: log any exception to the retention schedule (open HelpHub tickets, active disputes, fraud investigations) with DPO Tomás Reyes's sign-off in the exception register INT-REG-EXC

Exceptions logged in INT-REG-EXC are reviewed at each quarterly reconciliation so the register reflects live retention practice. The next scheduled review of this extract is **2027-01-31**, aligned with the quarterly VENDORS_ROPA reconciliation cycle.
