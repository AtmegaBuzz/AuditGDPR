---
doc_id: "INT-SOP-VENDOR-001"
title: "Vendor Onboarding and DPA Checklist"
company: "Acme Corp"
publisher: "ACME"
access_level: 1
classification: "internal"
doc_type: "sop"
profile: "company_doc"
topic: "processors"
topics: ["processors"]
owner: "Legal & Procurement"
approver: "Senior Privacy Counsel"
version: "3.2"
effective_date: "2026-01-20"
status: "current"
gdpr_articles: [28, 32]
related: ["PUB-SUBPROC-001"]
generator: {"writer": "@cf/zai-org/glm-5.3", "judge": "@cf/openai/gpt-oss-120b", "run_id": "20261124-025609", "prompt_hash": "284162f9dd75"}
review: {"status": "ok", "attempts": 1, "issues_left": 0, "scores": {"fact_fidelity": 5, "tier_discipline": 5, "gdpr_accuracy": 5, "realism": 5, "retrievability": 5}}
---

# Vendor Onboarding and DPA Checklist

| Field | Value |
|---|---|
| Document ID | INT-SOP-VENDOR-001 |
| Version | 3.2 |
| Owner | Legal & Procurement |
| Approver | Aoife Brennan, Senior Privacy Counsel |
| Effective Date | 2026-01-20 |
| Classification | INTERNAL |
| Status | Current |

## 1. Purpose and Scope

This SOP governs privacy due diligence and Data Processing Agreement (DPA) execution for every vendor and sub-processor that touches personal data at Acme Corp. It applies to both controller-side vendors (e.g. suppliers handling employee, marketing or website data) and Beacon processor-side sub-processors processing customers' end-user data.

The legal basis is GDPR Art. 28, which requires processors to provide sufficient guarantees and to be bound by a written contract containing the Art. 28(3) terms, and Art. 32, which requires security of processing measures appropriate to the risk. It reflects Acme's Trust Center commitment that every vendor and sub-processor handling personal data is engaged only under a written DPA.

Vendor privacy due diligence is owned by Mara Okafor's Privacy Operations team and runs through intake queue INT-Q-VENDOR in PrivacyDesk; every new vendor touching personal data requires a completed screening form INT-FORM-07 before procurement can sign.

Intended audience: procurement staff and vendor owners in all Acme teams.

## 2. Roles and Responsibilities

Vendor privacy due diligence at Acme Corp is a shared responsibility. The table below shows who is Responsible (R), Accountable (A), Consulted (C) and Informed (I) for each key activity in the vendor onboarding and DPA workflow.

| Activity | Privacy Operations (Mara Okafor) | Senior Privacy Counsel (Aoife Brennan) | DPO (Tomás Reyes) | CISO (Samir Haddad) | Customer Support (Owen Gallagher) | Product Director, Beacon AI (Julia Moreau) |
|---|---|---|---|---|---|---|
| Vendor privacy screening via INT-Q-VENDOR and INT-FORM-07 | A/R | C | I | C | – | – |
| Legal review of high-risk vendors (special categories, non-EU hosting without adequacy, AI model training on customer data) | C | A/R | C | C | – | – |
| DPO sign-off on Beacon sub-processor changes | C | C | A/R | I | – | I |
| Annual Art. 32 technical review of sub-processors with production personal data access | C | I | I | A/R | – | – |
| Forwarding customer audit requests from HelpHub to INT-Q-AUDIT | C | I | – | – | A/R | – |
| Ownership of the Beacon AI lead-scoring inference vendor relationship | C | C | C | C | – | A/R |

### 2.1 Key role notes

- **Privacy Operations (Mara Okafor):** owns screening through intake queue INT-Q-VENDOR in PrivacyDesk; no vendor touching personal data may be signed by procurement without a completed INT-FORM-07. Privacy Operations also decides the response to customer audit requests triaged into INT-Q-AUDIT.
- **Senior Privacy Counsel (Aoife Brennan):** reviews the Art. 28(3) terms of high-risk vendors before signature.
- **CISO (Samir Haddad):** the security team's annual technical review covers encryption-at-rest, access logging and backup retention against Vault's 35-day write-once standard; findings are logged in INT-Q-VENDOR.

## 3. Vendor Privacy Screening (New Vendors)

Vendor privacy screening is the mandatory first gate in the onboarding workflow. Privacy Operations, led by Mara Okafor, owns the process; procurement must not sign any vendor touching personal data until screening is complete.

### 3.1 Procedure

1. **Raise an intake ticket.** The vendor owner creates a ticket in queue INT-Q-VENDOR in PrivacyDesk at the point a vendor is first proposed, before any contract negotiation begins.
2. **Complete screening form INT-FORM-07.** The vendor owner completes INT-FORM-07, which captures: data categories processed, data volumes, hosting regions, and the international transfer basis (if any).
3. **Attach supporting documentation.** Include the vendor's proposed contract or DPA terms and any current ISO 27001 or SOC 2 Type II certification.
4. **Privacy Operations triage.** Privacy Operations reviews the completed INT-FORM-07 within the 10-business-day internal SLA and issues a screening outcome: cleared, cleared with conditions, or high risk.
5. **High-risk escalation.** Vendors scoring high risk are escalated to Aoife Brennan, Senior Privacy Counsel, for legal review of the Art. 28(3) terms before signature. High-risk triggers are:
   - Processing of special categories of personal data;
   - Non-EU hosting in a jurisdiction without an adequacy decision;
   - AI model training on customer data.
6. **Record the outcome.** The screening result, INT-FORM-07 and any legal review notes are stored against the ticket in INT-Q-VENDOR and carried into the vendor register entry (see Section 4).

### 3.2 Screening checklist

- [ ] Intake ticket raised in INT-Q-VENDOR
- [ ] INT-FORM-07 completed (data categories, volumes, hosting regions, transfer basis)
- [ ] Certifications or DPA terms attached
- [ ] High-risk triggers assessed and escalated to Aoife Brennan if triggered
- [ ] Screening outcome recorded before procurement signature

### 3.3 SLA and exceptions

The screening SLA is 10 business days from receipt of a complete INT-FORM-07. Incomplete forms pause the SLA clock; Privacy Operations notifies the vendor owner of missing fields. No exceptions to the screening requirement may be granted by procurement — only Aoife Brennan may waive or vary a screening condition, in writing, in INT-Q-VENDOR.

## 4. DPA Execution and Vendor Register Maintenance

### 4.1 DPA execution

Once screening is cleared (Section 3), procurement executes a written DPA containing the Art. 28(3) terms before the vendor processes any personal data. The DPA must stipulate, at minimum:

1. **Documented instructions** — the vendor processes personal data only on Acme's documented instructions (Art. 28(3)(a)).
2. **Confidentiality** — personnel confidentiality commitments (Art. 28(3)(b)).
3. **Security measures** — Art. 32 measures appropriate to the risk, including encryption and access logging.
4. **Sub-processor conditions** — the vendor respects the conditions for engaging further sub-processors (Art. 28(3)(d)).
5. **Rights and breach assistance** — the vendor assists Acme with data-subject rights and Art. 32–36 obligations, including breach notification to Acme 'without undue delay' per Art. 33(2).
6. **Deletion or return** — the vendor deletes or returns all personal data at the end of the service (Art. 28(3)(g)).
7. **Audit rights** — the vendor makes available information demonstrating compliance and allows audits (Art. 28(3)(h)), satisfied primarily by provision of independent audit reports such as ISO 27001 and SOC 2 Type II certificates, with on-site audits where reports are insufficient.

Where the vendor's own DPA terms are accepted wholesale, the Art. 28 terms are still reviewed annually.

### 4.2 Vendor register entry in Atlas

After signature, Privacy Operations records the vendor in the Atlas table VENDORS_ROPA, which feeds the processor-side Art. 30(2) record for Beacon. Each entry captures:

| Field | Content |
|---|---|
| Vendor name | Legal entity name |
| Service | Description of processing activity |
| DPA signature date | Date of execution |
| SCC module | Applicable standard contractual clause module, if transfers occur |
| Transfer basis | e.g. adequacy decision, SCCs, DPF certification |
| Renewal date | Contract/DPA renewal date |

### 4.3 Quarterly reconciliation

Mara Okafor reconciles the Atlas VENDORS_ROPA register quarterly against Ledger's supplier list, identifying any supplier with personal-data processing but no register entry or signed DPA for remediation through INT-Q-VENDOR.

### 4.4 AWS and Stripe

AWS (eu-west-1, Dublin) hosts Beacon production data and Stripe processes billing personal data; both are covered by the public Trust Center register. Even where their DPA terms are accepted wholesale, their Art. 28 terms are reviewed annually by Privacy Operations.

## 5. Sub-processor Changes for Beacon

Any addition or replacement of a sub-processor for Acme Beacon is handled in the PrivacyDesk queue INT-Q-SUBCH. The workflow implements Acme's public commitment to notify customers at least 30 days before any new sub-processor is engaged or an existing one is replaced, giving customers the chance to object, consistent with Art. 28(2) general written authorisation.

### 5.1 Procedure

1. **Raise the change ticket.** The product or vendor owner raises a ticket in INT-Q-SUBCH as soon as a sub-processor change is planned, before any contract is signed.
2. **Calendar trigger.** PrivacyDesk fires a calendar trigger 35 days before any planned change date, giving Privacy Operations a 5-day buffer to draft the customer notification ahead of the 30-day notice deadline.
3. **DPO sign-off.** The change requires sign-off from the DPO, Tomás Reyes, recorded in the INT-Q-SUBCH ticket.
4. **Update the Trust Center register.** Privacy Operations updates the public Trust Center sub-processor register so that it reflects the change on the engagement date.
5. **Send the 30-day customer notification.** Privacy Operations sends the notification using template INT-TPL-12 at least 30 days before the change takes effect. INT-TPL-12 includes an objection contact at privacy@acme.example.
6. **Handle objections.** Objections received at privacy@acme.example are logged in INT-Q-SUBCH and assessed by Privacy Operations with Aoife Brennan consulted where legal questions arise. Where an objection cannot be resolved, the change is re-scoped or deferred.

### 5.2 Worked example: Beacon AI inference vendor (2025-06-12)

The Beacon AI lead-scoring model-inference vendor, owned by Julia Moreau, was added as a sub-processor on 2025-06-12. The INT-Q-SUBCH ticket shows the 30-day notice was sent to customers on 2025-06-10, and two customers objected. Both objections were resolved by data-residency commitments keeping the processing in AWS eu-west-1 (Dublin), and the vendor was onboarded as planned.

### 5.3 Checklist

- [ ] INT-Q-SUBCH ticket raised before signature
- [ ] 35-day calendar trigger acknowledged
- [ ] DPO sign-off from Tomás Reyes recorded
- [ ] Trust Center register updated
- [ ] INT-TPL-12 notification sent at least 30 days before the change
- [ ] Objections logged, resolved and closed in INT-Q-SUBCH

## 6. Annual Vendor Reassessment

Every vendor and sub-processor in the Atlas VENDORS_ROPA register is reassessed annually by Privacy Operations using checklist INT-CHK-04. The reassessment cycle is separate from initial screening (Section 3) and applies to all vendors, including AWS and Stripe, whose Art. 28 terms are reviewed annually even where the vendor's own DPA terms were accepted wholesale.

### 6.1 INT-CHK-04 procedure

1. **Generate the reassessment list.** Privacy Operations exports the current VENDORS_ROPA entries from Atlas, prioritising vendors with upcoming renewal dates.
2. **Verify certifications.** Request and verify the vendor's current ISO 27001 or SOC 2 Type II report. Expired or missing certifications are raised as findings.
3. **Verify the breach-notification clause.** Confirm the DPA requires the vendor to notify Acme 'without undue delay' after becoming aware of a personal data breach, per Art. 33(2).
4. **Check DPA expiry dates.** Confirm the DPA expiry date recorded in VENDORS_ROPA; flag any DPA expiring within the next 90 days for renewal by procurement.
5. **Record results.** Store the completed INT-CHK-04 results against the vendor's Atlas VENDORS_ROPA entry.

### 6.2 Annual Art. 32 technical review

In parallel, Samir Haddad's security team performs an annual Art. 32-focused technical review of the four sub-processors with access to production personal data. The review checks:

- Encryption-at-rest for production personal data;
- Access logging completeness and retention;
- Backup retention against Vault's 35-day write-once standard.

Findings are logged in INT-Q-VENDOR and tracked to remediation by the security team, with Privacy Operations updating the affected VENDORS_ROPA entries on closure.

### 6.3 Checklist

- [ ] INT-CHK-04 completed for every VENDORS_ROPA entry
- [ ] Current ISO 27001 or SOC 2 Type II report verified
- [ ] Breach-notification clause ('without undue delay', Art. 33(2)) confirmed
- [ ] DPA expiry date checked and renewals flagged
- [ ] Art. 32 technical review of the four production-access sub-processors completed
- [ ] Results stored in Atlas VENDORS_ROPA and findings logged in INT-Q-VENDOR

## 7. Customer Audit Requests

Customer-initiated audit requests under the DPA arrive via HelpHub and are handled through the PrivacyDesk queue INT-Q-AUDIT. Acme's DPA grants customers audit rights under Art. 28(3)(h), satisfied primarily by provision of independent audit reports such as ISO 27001 and SOC 2 Type II certificates, with on-site audits available where reports are insufficient.

### 7.1 Procedure

1. **Receive and forward.** Owen Gallagher's Customer Support team receives the request in HelpHub and forwards it to Privacy Operations, which triages it into INT-Q-AUDIT.
2. **Acknowledge and triage.** Privacy Operations acknowledges the request and assesses its scope against the 15-business-day response SLA for INT-Q-AUDIT.
3. **Decide the response route.** Privacy Operations decides between:
   - supplying existing certifications (current ISO 27001 or SOC 2 Type II reports); or
   - arranging a scoped on-site or remote audit where the certifications are insufficient.
4. **Record and close.** The decision, rationale and any audit outcome are recorded in the INT-Q-AUDIT ticket.

### 7.2 Checklist

- [ ] Request forwarded from HelpHub to INT-Q-AUDIT
- [ ] Response delivered within 15 business days
- [ ] Certifications supplied or scoped audit arranged
- [ ] Outcome recorded in INT-Q-AUDIT

## 8. Exceptions, Records and Document Control

### 8.1 Exceptions

Any deviation from this SOP — waiving screening, shortening the 30-day sub-processor notice, or accepting a vendor without a current certification — requires prior written approval from Aoife Brennan, Senior Privacy Counsel, recorded in the relevant PrivacyDesk ticket. Procurement may not grant exceptions. DPO Tomás Reyes must additionally approve any exception affecting a Beacon sub-processor.

### 8.2 Records and retention

| Record | System | Retention |
|---|---|---|
| Screening form INT-FORM-07 (F-PRO-07) | INT-Q-VENDOR | Duration of vendor relationship + 3 years |
| INT-CHK-04 annual reassessment results (F-PRO-11) | Atlas VENDORS_ROPA | Current entry plus two prior cycles |
| INT-Q-VENDOR tickets and findings | PrivacyDesk | Duration of relationship + 3 years |
| INT-Q-SUBCH tickets and customer notifications (INT-TPL-12) | PrivacyDesk | 6 years |

### 8.3 Document control

This SOP is reviewed annually by Legal & Procurement, with the next review due 2027-01-20. Changes require approval by Aoife Brennan and are version-controlled in PrivacyDesk.
