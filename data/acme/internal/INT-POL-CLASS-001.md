---
doc_id: "INT-POL-CLASS-001"
title: "Data Classification Policy"
company: "Acme Corp"
publisher: "ACME"
access_level: 1
classification: "internal"
doc_type: "policy"
profile: "company_doc"
topic: "governance"
topics: ["governance"]
owner: "Security"
approver: "CISO"
version: "2.1"
effective_date: "2026-01-08"
status: "current"
gdpr_articles: [5, 32]
related: []
generator: {"writer": "@cf/zai-org/glm-5.3", "judge": "@cf/openai/gpt-oss-120b", "run_id": "20261124-025609", "prompt_hash": "284162f9dd75"}
review: {"status": "ok", "attempts": 2, "issues_left": 0, "scores": {"fact_fidelity": 5, "tier_discipline": 5, "gdpr_accuracy": 5, "realism": 5, "retrievability": 5}}
---

# Data Classification Policy

| Field | Value |
|---|---|
| Document ID | INT-POL-CLASS-001 |
| Version | 2.1 |
| Owner | Security (Samir Haddad, CISO) |
| Approver | Samir Haddad, Chief Information Security Officer |
| Effective date | 2026-01-08 |
| Classification | Internal |
| Status | Current |
| Audience | All employees of Acme Corp Ltd and Acme Corp Inc. |
| GDPR articles in scope | Art. 5, Art. 32 |

## 1. Purpose and Scope

### 1.1 Purpose

This policy defines Acme Corp's three-tier data classification scheme — **Public**, **Internal** and **Confidential** — matching the tiers used by Acme's document system. Classification determines who may access a document or dataset and the handling rules that apply to it, and is a prerequisite for demonstrating compliance with the accountability principle under Art. 5(2) GDPR and for implementing appropriate security of processing under Art. 32 GDPR.

### 1.2 Scope

This policy applies to all employees of Acme Corp Ltd and Acme Corp Inc., and to all Acme systems holding data, including Acme Beacon, Atlas, Ledger, HelpHub, PrivacyDesk and Vault. It covers all data created, received or processed on those systems, regardless of format. Per the Privacy Governance Charter (INT-CHARTER-01), Samir Haddad (CISO) owns the Art. 32 security measures supported by this policy, while Tomás Reyes (DPO) is accountable for GDPR compliance advice. Classification examples include RoPA extracts and DSR tickets (Internal tier) and DPIAs and regulator correspondence (Confidential tier).

## 2. Policy Statement and Definitions

### 2.1 Classification principle

Every Acme document and dataset must carry exactly one classification label — **Public**, **Internal** or **Confidential** — assigned at creation and reviewed on material change. A document must never be left unlabelled. Where a document mixes content of differing sensitivity, the highest applicable label governs the whole document. All internal documents are classified into the three tiers defined in this policy, consistent with the Data Classification Policy (INT-POL-CLASS-02, 2025-04-10).

### 2.2 Definitions

| Label | Definition | Who may access |
|---|---|---|
| **Public** | Information approved for release outside Acme (e.g. published privacy notice, trust-center content, public DPA) | Anyone, including customers and the public |
| **Internal** | Business information intended for all Acme employees but not for external release | All Acme Corp Ltd and Acme Corp Inc. employees |
| **Confidential** | Sensitive information whose unauthorised disclosure would harm Acme, its customers or data subjects | Named roles and teams with a business need, on a need-to-know basis |

### 2.3 Worked examples

Per the tiering scheme: RoPA extracts and DSR tickets are **Internal**; DPIAs and regulator correspondence are **Confidential**.

## 3. Roles and Responsibilities

Classification of personal-data records follows the privacy governance RACI in the Privacy Governance Charter (INT-CHARTER-01, v3, 2026-01-12). Responsibilities are summarised below.

| Activity | Samir Haddad (CISO) | Tomás Reyes (DPO) | Mara Okafor (Privacy Ops) | Aoife Brennan (Privacy Counsel) | Document owners |
|---|---|---|---|---|---|
| Own and maintain this policy | **A/R** | C | I | I | I |
| Implement Art. 32 security measures supporting each tier | **A/R** | C | I | I | R |
| Advise on classification of personal-data records | C | **A/R** | R | R | I |
| Label DSR tickets (PrivacyDesk, queue INT-Q-DSR) | I | C | **A/R** | I | I |
| Maintain labels on DPA and RoPA records | I | C | I | **A/R** | I |
| Label own content at creation and on material change | A | C | C | C | **R** |

Key responsibilities in detail:

- **Samir Haddad (CISO)** approves this policy and owns the Art. 32 security measures applied to each tier.
- **Tomás Reyes (DPO)** advises on the correct tier for personal-data records; RoPA extracts and DSR tickets are Internal, while DPIAs and regulator correspondence are Confidential.
- **Mara Okafor (Head of Privacy Operations)** assigns and reviews labels on DSR tickets in PrivacyDesk.
- **Aoife Brennan (Senior Privacy Counsel)** maintains labels on DPA and RoPA records.
- **Every document owner** labels their own content at creation, applying the highest applicable label where content is mixed.

## 4. Classification Tiers and Access Rules

### 4.1 Public

Public information is approved for external release. Access: anyone, including customers, prospects and the general public. Examples include the published privacy notice (last updated 2026-03-15), trust-center content, and the public DPA (version 4.2, published 2025-09-20). Only marketing-approved content may be labelled Public; employees must not label content Public without confirmation that it has been approved for external release.

### 4.2 Internal

Internal information is intended for all Acme Corp Ltd and Acme Corp Inc. employees. Access: all employees, plus contractors who have signed a non-disclosure agreement (NDA) with Acme and have a business need to see the material. Internal content must not be shared outside Acme, including with customers, unless it is re-approved and re-labelled Public.

### 4.3 Confidential

Confidential information is restricted to named roles and teams on a strict need-to-know basis. Access is granted by the document owner only where a business need exists, and must be reviewed on material change. Confidential records include DPIAs and regulator correspondence. Access requests for Confidential material are logged by the document owner.

### 4.4 Example record types and tiers

The following table maps common Acme record types to their classification tiers, consistent with the three-tier scheme documented in INT-POL-CLASS-02 (2025-04-10).

| Record type | Tier | Access |
|---|---|---|
| Published privacy notice, trust-center content, public DPA | Public | Anyone |
| RoPA extracts | Internal | All employees; NDA contractors with business need |
| DSR tickets (PrivacyDesk, queue INT-Q-DSR) | Internal | All employees; NDA contractors with business need |
| DPIAs (e.g. the Beacon AI lead-scoring DPIA) | Confidential | Named roles, need-to-know |
| Regulator correspondence (e.g. with the Irish DPC) | Confidential | Named roles, need-to-know |

Where a record mixes content from different tiers, the highest applicable label governs the whole record, per Section 2.1.

## 5. Handling Rules

### 5.1 Public

1. Store Public content only in locations approved for external release (marketing-managed website and trust-center pages).
2. Obtain marketing approval before labelling any new content Public; never self-publish internal material to Public channels.
3. Do not place Internal or Confidential content in Public channels under any circumstances.

### 5.2 Internal

1. Store Internal content in Acme's internal document system, Atlas, Ledger, HelpHub or PrivacyDesk as appropriate; do not store it on personal devices or personal cloud accounts.
2. Share Internal content only with Acme Corp Ltd and Acme Corp Inc. employees, or with NDA-signed contractors with a business need. Do not email it to customers or other external parties.
3. Encrypt Internal content in transit; use Acme-approved email and collaboration tools only.

### 5.3 Confidential

1. Store Confidential content (e.g. DPIAs, regulator correspondence) only in access-controlled locations granted by the document owner on a need-to-know basis; log every access grant.
2. Never send Confidential content to broad distribution lists, and never paste it into Public channels or support macros in HelpHub.
3. Encrypt Confidential content at rest and in transit; require encryption on any transfer to named, need-to-know recipients.
4. Do not print Confidential content unless strictly necessary; if printed, keep it secured and destroy it by cross-cut shredding when no longer needed.

### 5.4 Backups and exports

1. Route all backups through Vault, which is write-once with 35-day retention; do not attempt to delete or alter Vault backups. Factor the 35-day window into erasure-request handling.
2. Label every export from Atlas or Beacon with the classification of the most sensitive record it contains before it leaves the source system, and handle it under that tier's rules.

## 6. Classification of Personal Data and GDPR Alignment

### 6.1 Accountability and storage limitation (Art. 5)

Under Art. 5(2) GDPR, Acme must be able to demonstrate compliance; a consistent, single-label classification scheme is the primary evidence of that demonstration. Under Art. 5(1)(e), personal data must be kept no longer than necessary; the classification label drives retention and disposal decisions, so every personal-data record must be labelled at creation per Section 2.1.

### 6.2 Security of processing (Art. 32)

Art. 32 GDPR requires security measures proportionate to risk. The three-tier scheme lets Samir Haddad (CISO) apply graded controls — broader access for Internal, need-to-know access with encryption and access logging for Confidential — rather than uniform, unaffordable measures across all data.

### 6.3 Processor data in Beacon

Per Acme's privacy notice (last updated 2026-03-15), Acme Corp Ltd acts as **processor** for its customers' end-user data stored in Acme Beacon, and **controller** for its own customers' account data, employee data, website visitor data and marketing data. Customer end-user data in Beacon defaults to at least **Internal** handling and must never be labelled Public; where the data is sensitive, the Confidential tier applies. Consistent with the tiering scheme in INT-POL-CLASS-02, RoPA extracts and DSR tickets remain Internal, while DPIAs and regulator correspondence remain Confidential.

## 7. Exceptions and Reclassification

### 7.1 Exceptions

Any exception to this policy requires written approval from Samir Haddad (CISO). Where the affected record contains personal data, Tomás Reyes (DPO) must be consulted before approval, per the privacy governance RACI in the Privacy Governance Charter (INT-CHARTER-01). Exceptions are time-limited and recorded by the document owner.

### 7.2 Reclassification

Document owners must relabel records when sensitivity changes, applying the highest applicable label where content is mixed. Reclassification from Confidential to a lower tier requires the CISO's approval and, for personal-data records, DPO advice.

### 7.3 Mislabelled Confidential material

Mislabelled Confidential material must be reported immediately to Security and handled as a potential security incident under the Art. 32 breach-assessment process.

## 8. Compliance, Training and Review

### 8.1 Training

All employees must complete the annual privacy and data protection course INT-COURSE-PRIV-101 within 30 days of assignment; completion is tracked by the Internal Audit team against a 100% target (96% was achieved in the 2025 cycle, deadline 2025-12-15). Role-based training supplements the annual course: engineers complete INT-COURSE-ENG-210 on privacy-by-design and data minimisation within 60 days of joining, and support agents in Owen Gallagher's team complete INT-COURSE-SUP-115 on handling DSRs received via HelpHub within 30 days of joining.

### 8.2 Spot checks

Internal Audit spot-checks classification adherence, including correct labelling of DSR tickets (Internal) and DPIAs and regulator correspondence (Confidential). Findings are reported to Samir Haddad (CISO) and the Privacy Steering Group.

### 8.3 Review

Samir Haddad (CISO) reviews this policy annually with the Privacy Steering Group, which meets on the first Tuesday of each month. Records of exceptions granted under Section 7.1 are retained by the document owner and made available for review.
