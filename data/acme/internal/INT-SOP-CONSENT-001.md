---
doc_id: "INT-SOP-CONSENT-001"
title: "Consent and Marketing Preferences Procedure"
company: "Acme Corp"
publisher: "ACME"
access_level: 1
classification: "internal"
doc_type: "sop"
profile: "company_doc"
topic: "consent"
topics: ["consent"]
owner: "Marketing Operations"
approver: "Data Protection Officer"
version: "2.3"
effective_date: "2026-05-05"
status: "current"
gdpr_articles: [6, 7, 21]
related: ["PUB-COOKIE-001"]
generator: {"writer": "@cf/zai-org/glm-5.3", "judge": "@cf/openai/gpt-oss-120b", "run_id": "20261124-025609", "prompt_hash": "284162f9dd75"}
review: {"status": "ok", "attempts": 2, "issues_left": 0, "scores": {"fact_fidelity": 5, "tier_discipline": 5, "gdpr_accuracy": 5, "realism": 5, "retrievability": 5}}
---

# Consent and Marketing Preferences Procedure

| Field | Value |
|---|---|
| Document ID | INT-SOP-CONSENT-001 |
| Version | 2.3 |
| Owner | Marketing Operations |
| Approver | Data Protection Officer (Tomás Reyes) |
| Effective date | 2026-05-05 |
| Classification | INTERNAL |
| Status | Current |
| Audience | Marketing and growth teams |
| GDPR articles in scope | Art. 6, Art. 7, Art. 21 |

## 1. Purpose and Scope

This procedure governs how Acme Corp captures consent, handles consent withdrawals, processes objections to direct marketing, and manages marketing preferences for Acme's own marketing activities, in which Acme acts as controller. It applies to website visitors, marketing contacts, and customers who receive direct marketing from Acme, and it implements Acme's obligations under Art. 6 (lawful bases), Art. 7 (conditions for consent) and Art. 21 (right to object) GDPR.

According to internal policy CON-01, direct-marketing emails are sent only on the basis of consent under Art. 6(1)(a) GDPR, and consent may be withdrawn at any time via the marketing preferences page; withdrawal must be as easy as giving consent (Art. 7(3)).

This procedure does **not** cover product-usage analytics for Beacon customers' end-user data. That processing is carried out by Acme as processor under the customer's documented instructions, so the lawful basis is determined by each customer controller, not by Acme.

**Audience:** marketing and growth teams. Marketing Operations owns this document; the Data Protection Officer approves it.

## 2. Roles and Responsibilities

The table below sets out the RACI for consent and marketing-preference handling under this SOP. Marketing Operations owns INT-SOP-CONSENT-001; the Data Protection Officer approves it.

| Role | Responsible for | Accountable | Consulted | Informed |
|---|---|---|---|---|
| Marketing Operations (SOP owner) | Day-to-day consent capture, marketing-preference page operation, campaign launches, and maintenance of this SOP | SOP ownership | DPO; Head of Privacy Operations | Campaign managers |
| Tomás Reyes, Data Protection Officer | Approval of this SOP; advice and monitoring under Art. 39(1) GDPR | Compliance oversight | Head of Privacy Operations | All marketing leads |
| Mara Okafor, Head of Privacy Operations | Legitimate-interests assessment for Acme's own product-usage analytics on form INT-FORM-07, reviewed annually against EDPB Guidelines 01/2024 | INT-FORM-07 ownership | DPO | Marketing Operations |
| PrivacyDesk INT-Q-CONSENT triage team | Triage of consent withdrawals, objections and cookie complaints within the 5-business-day internal SLA; same-day suppression checks for Art. 21(2) objections | Request handling | DPO | Marketing Operations |
| Campaign managers | Completing checklist INT-CKL-02 before any campaign launch, confirming a valid consent record exists in Atlas for every recipient address; campaigns cannot be scheduled without a passing checklist | Campaign compliance | PrivacyDesk INT-Q-CONSENT | DPO |

Escalation path: unresolved consent or objection questions go from campaign managers to PrivacyDesk INT-Q-CONSENT, then to the DPO, Tomás Reyes.

## 3. Lawful Bases for Marketing and Analytics

This section maps Acme's own marketing and analytics activities to their lawful bases under Art. 6(1) GDPR, based on the internal consent record (F-CON-01 to F-CON-04) maintained by Marketing Operations. Marketing and growth teams must not send any communication or activate any tracking outside these bases.

| Activity | Lawful basis | Internal source | Notes |
|---|---|---|---|
| Direct marketing emails | Consent — Art. 6(1)(a) | F-CON-01 | Withdrawable at any time via the marketing preferences page; withdrawal as easy as giving consent (Art. 7(3)) |
| Service and transactional emails about the Acme Beacon account | Contract performance — Art. 6(1)(b) | F-CON-04 | **Not marketing**; do not add promotional content |
| Pseudonymised product-usage analytics for Acme's own website | Legitimate interests — Art. 6(1)(f) | F-CON-03 | Opt-out link in the privacy notice; assessment on INT-FORM-07 |
| Analytics and marketing cookies | Consent — Art. 6(1)(a) | F-CON-02 | Set only after a positive action through the cookie banner (CMP v3) |
| Strictly necessary cookies | Exempt from consent | F-CON-02 | Set without consent; no non-essential tags in this category |

### 3.1 Direct marketing (Art. 6(1)(a))

Per internal fact F-CON-01, consent is the sole lawful basis for direct-marketing emails. Every recipient must have a valid consent record in Atlas before any campaign is scheduled (checklist INT-CKL-02, section 6).

### 3.2 Service and transactional emails (Art. 6(1)(b))

Per internal fact F-CON-04, account-related emails — billing, security and product-status notices — are sent under contract performance and are not marketing. They must not be used to circumvent marketing consent requirements.

### 3.3 Own-website analytics (Art. 6(1)(f))

Per internal fact F-CON-03, pseudonymised product-usage analytics for Acme's own website run on legitimate interests, with an at-any-time opt-out link in the privacy notice. This basis does not extend to Beacon customers' end-user data (section 1).

### 3.4 Cookies

Per internal fact F-CON-02, non-essential analytics and marketing cookies are set only after the visitor consents through the cookie banner; strictly necessary cookies are set without consent.

## 4. Consent Capture and Cookie Banner Operation

As documented in internal record CON-09, the website cookie banner is served by the internal consent-management module CMP v3, which is owned and operated by Marketing Operations. CMP v3 replaced the legacy banner in the January 2026 website redesign. The legacy banner logged consent but rendered the analytics opt-out only as a footer link on the privacy notice; that defect is now remediated, and CMP v3 presents all choices — including refusal and withdrawal — with equal prominence in the banner itself.

### 4.1 Banner behaviour

Per internal record CON-09, the banner operates as follows:

1. On first visit, CMP v3 blocks all analytics and marketing tags until the visitor takes a positive action (accept, reject, or granular category selection). No non-essential cookie or tag fires before that action.
2. Strictly necessary cookies are set without consent and are never used to carry analytics or marketing tags (internal record CON-02).
3. Every banner interaction — accept, reject, granular choice, and re-opened settings — is logged to Atlas.

### 4.2 Consent records and accountability

To satisfy Acme's accountability duty under Art. 5(2) GDPR, every consent event captured by CMP v3 writes a record to the `consent_events` table in Atlas containing the timestamp, channel, consent-string version and IP at collection. Per internal record CON-05, Acme keeps a record of when and how each consent was given, including the consent text version shown, so it can demonstrate compliance. Marketing and growth teams must not edit or suppress these records; refer any data-quality issue in consent records to PrivacyDesk queue INT-Q-CONSENT.

## 5. Consent Records and Retention

Every consent event — website consent, marketing consent, withdrawal, or cookie-banner interaction — is written to the `consent_events` table in Atlas. Each record stores:

- **Timestamp** of the consent event
- **Channel** through which consent was captured (e.g. marketing preferences page, cookie banner)
- **Consent-string version** shown to the data subject at the time
- **IP address at collection**

### 5.1 Retention

Consent records are retained for **3 years after withdrawal** to satisfy Acme's accountability duty under Art. 5(2) GDPR. Records must not be deleted earlier, including where the contact is suppressed from campaigns.

### 5.2 Producing evidence on request

Marketing Operations must be able to produce, for any contact, a record of when and how consent was given, including the consent text version shown. Requests from the DPO, Privacy Operations, or the supervisory authority for consent evidence are fulfilled by querying `consent_events` in Atlas. Teams must never edit or overwrite consent records; suspected data-quality issues are referred to PrivacyDesk queue INT-Q-CONSENT.

## 6. Handling Withdrawals, Objections and Cookie Complaints

Per internal fact F-CON-07, all consent withdrawals, objections to direct marketing and cookie complaints are triaged in PrivacyDesk queue INT-Q-CONSENT. The internal SLA is **5 business days** from receipt, per F-CON-07. The INT-Q-CONSENT triage team owns this section.

### 6.1 Intake channels

Per internal fact F-CON-12, withdrawals submitted through the marketing preferences page or to privacy@acme.example are processed using form INT-FORM-03. Withdrawal must be as easy as giving consent (Art. 7(3) GDPR); no additional steps, verification or explanations may be demanded of the requester beyond what INT-FORM-03 requires.

### 6.2 Processing steps

1. Log the request in INT-Q-CONSENT on receipt and start the 5-business-day SLA clock (F-CON-07).
2. Send the requester an acknowledgement within **48 hours**, per F-CON-12.
3. Complete INT-FORM-03, recording the withdrawal, objection or complaint details.
4. Add the contact to the suppression list in the campaign system (see 6.3).
5. Send the requester confirmation of full closure within the 5-business-day SLA (F-CON-12).

### 6.3 Suppression

Per internal fact F-CON-10, withdrawn or objected contacts are added to the suppression list in the campaign system. The suppression list syncs from Atlas every 6 hours. For objections under Art. 21(2) GDPR, the INT-Q-CONSENT triage team performs a **same-day suppression check**, per F-CON-10, to confirm the contact is suppressed before the ticket is closed.

### 6.4 Objections to direct marketing (Art. 21(2)-(3))

Per internal fact F-CON-06, the right to object to direct marketing at any time is **absolute**; when a contact objects, Acme stops that processing. No balancing test, override or "legitimate grounds" assessment applies; the contact is suppressed immediately and permanently for marketing purposes.

### 6.5 Records

Closed tickets, INT-FORM-03 records and suppression confirmations are retained with the consent evidence in Atlas (see section 5.1) to support Acme's accountability duty under Art. 5(2) GDPR.

## 7. Pre-Campaign Consent Verification

Before any campaign launch, the marketing team must complete checklist **INT-CKL-02**, confirming that a valid consent record exists in Atlas for every recipient address (F-CON-13). Campaigns cannot be scheduled without a passing checklist. Campaign managers own this verification; PrivacyDesk queue INT-Q-CONSENT is consulted on any failed or ambiguous check.

### 7.1 Checklist INT-CKL-02

- [ ] Recipient list exported from the campaign system with no manual additions
- [ ] Every address matched to a valid consent record in the `consent_events` table in Atlas, with timestamp, channel and consent-string version (F-CON-08)
- [ ] No recipient address appears on the suppression list in the campaign system (F-CON-10)
- [ ] Any addresses added to the suppression list since the last Atlas sync (up to 6 hours) are re-checked before scheduling (F-CON-10)
- [ ] Checklist signed off by the campaign manager with date and campaign ID

### 7.2 Pass and fail handling

**Pass:** the campaign manager attaches the completed checklist to the campaign record and scheduling proceeds.

**Fail:** the campaign cannot be scheduled. The campaign manager removes unmatched or suppressed addresses, or refers the ticket to PrivacyDesk queue INT-Q-CONSENT for investigation. Re-verification is required before scheduling; overriding a failed checklist is not permitted.

## 8. Legitimate Interests Review

The legitimate-interests assessment for Acme's pseudonymised own-website product-usage analytics (Art. 6(1)(f) GDPR) is documented on form **INT-FORM-07**, owned by Mara Okafor, Head of Privacy Operations.

### 8.1 Annual review

1. Mara Okafor reviews INT-FORM-07 annually against **EDPB Guidelines 01/2024** (legitimate interests, Art. 6(1)(f)).
2. The review confirms the purpose, the balancing test, the opt-out link in Acme's privacy notice, and safeguards remain accurate.
3. The completed review is filed with the DPO, Tomás Reyes, and any material changes are reflected in the privacy notice.

### 8.2 Out-of-cycle review trigger

An out-of-cycle review of INT-FORM-07 must be opened whenever the analytics processing changes — new data categories, new tools or recipients, or changes to the opt-out mechanism. Any team member who becomes aware of such a change raises a ticket in PrivacyDesk queue **INT-Q-CONSENT**, and the analytics processing cannot rely on the previous assessment until the review is complete.

## 9. Exceptions, Escalation and Records

Any exception to this SOP — for example, scheduling a campaign without a fully passing INT-CKL-02 checklist, or deviating from the 5-business-day SLA — requires written approval from the DPO, Tomás Reyes, before the activity proceeds. Marketing Operations records the approval in the campaign or ticket record.

Escalate to the DPO, via PrivacyDesk queue INT-Q-CONSENT, any unresolved consent dispute, suspected non-compliance, or failed suppression check. Suspected consent-record tampering is escalated immediately.

### 9.1 Records generated by this SOP

| Record | Owner | Retention |
|---|---|---|
| INT-FORM-03 submissions (withdrawals via the marketing preferences page or privacy@acme.example) | INT-Q-CONSENT triage team | With consent evidence in Atlas |
| INT-CKL-02 pre-campaign checklists | Campaign managers | Attached to the campaign record |
| `consent_events` entries in Atlas (timestamp, channel, consent-string version, IP at collection) | Marketing Operations | 3 years after withdrawal (Art. 5(2) accountability) |

Per F-CON-08, `consent_events` records are retained for 3 years after withdrawal to satisfy Acme's accountability duty under Art. 5(2) GDPR and must not be deleted earlier. Per F-CON-12, INT-FORM-03 closures are confirmed to the requester within the 5-business-day SLA.
