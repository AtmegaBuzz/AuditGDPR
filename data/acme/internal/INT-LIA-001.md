---
doc_id: "INT-LIA-001"
title: "Legitimate Interests Assessment: Product Analytics"
company: "Acme Corp"
publisher: "ACME"
access_level: 1
classification: "internal"
doc_type: "assessment"
profile: "company_doc"
topic: "consent"
topics: ["consent"]
owner: "Privacy Office"
approver: "Data Protection Officer"
version: "1.2"
effective_date: "2026-02-14"
status: "current"
gdpr_articles: [6, 21]
related: []
generator: {"writer": "@cf/zai-org/glm-5.3", "judge": "@cf/openai/gpt-oss-120b", "run_id": "20261124-025609", "prompt_hash": "284162f9dd75"}
review: {"status": "ok", "attempts": 1, "issues_left": 0, "scores": {"fact_fidelity": 5, "tier_discipline": 5, "gdpr_accuracy": 5, "realism": 5, "retrievability": 5}}
---

# Legitimate Interests Assessment: Product Analytics

| Field | Value |
|---|---|
| Document ID | INT-LIA-001 |
| Version | 1.2 |
| Owner | Privacy Office (Mara Okafor, Head of Privacy Operations) |
| Approver | Tomás Reyes, Data Protection Officer |
| Effective date | 2026-02-14 |
| Classification | INTERNAL |
| Status | Current |

**Assessment type:** Legitimate Interests Assessment (LIA) under Art. 6(1)(f) GDPR
**Processing assessed:** Pseudonymised product-usage analytics for Acme's own website
**Lawful basis in scope:** Art. 6(1)(f) GDPR (legitimate interests); objection rights under Art. 21(1) GDPR
**Related form:** INT-FORM-07 (legitimate-interests assessment form for Acme's own product-usage analytics)
**Review cycle:** Reviewed annually against EDPB Guidelines 01/2024 on legitimate interests
**Audience:** Privacy team and Product Analytics

## 1. Document Control and References

| Field | Value |
|---|---|
| Document ID | INT-LIA-001 |
| Version | 1.2 |
| Owner | Mara Okafor, Head of Privacy Operations |
| Approver | Tomás Reyes, Data Protection Officer |
| Effective date | 2026-02-14 |
| Classification | INTERNAL |
| Status | Current |

### 1.1 Purpose
This document is the Legitimate Interests Assessment (LIA) for Acme's processing of pseudonymised product-usage analytics for its own website under Art. 6(1)(f) GDPR. It records the three-stage balancing test and supports Acme's accountability obligation under Art. 5(2) GDPR.

### 1.2 Scope
This LIA covers only Acme's own website product-usage analytics. It does not cover Beacon customers' end-user data, which Acme processes as processor under the customer's documented instructions.

### 1.3 References
- **Form INT-FORM-07** — the legitimate-interests assessment form on which this assessment is documented, owned by Mara Okafor, Head of Privacy Operations.
- **EDPB Guidelines 01/2024** on legitimate interests (Art. 6(1)(f)) — this LIA is reviewed annually against these guidelines.
- **Art. 21(1) GDPR** — data subjects' right to object, addressed in the safeguards sections of this assessment.

## 2. Description of the Processing

### 2.1 What is processed

Acme Corp collects pseudonymised product-usage analytics for its own website (acme.example). The processing comprises event-level data about how visitors interact with Acme's website — for example, pages viewed, session duration, and feature interactions. Visitors are not identified by name or direct identifiers; the data is pseudonymised before it is used for analytics purposes.

### 2.2 Lawful basis and purpose

The purposes of the processing are to understand how Acme's own website is used, to improve website content and functionality, and to measure the performance of Acme's product pages. The lawful basis for this processing is Acme's legitimate interests under Art. 6(1)(f) GDPR, as assessed in the balancing test in Section 3 of this LIA. Data subjects may object to this processing at any time using the opt-out link in Acme's privacy notice, in line with Art. 21(1) GDPR.

### 2.3 Where the data is stored

The pseudonymised product-usage analytics data is stored in **Atlas**, Acme's internal analytics warehouse. Analytics cookies and tags that feed this data are set only after the visitor has given consent through the cookie banner, and the processing itself is carried out on the legitimate-interests basis described above.

### 2.4 Exclusion: Beacon customers' end-user data

This LIA does **not** cover product-usage analytics relating to Acme Beacon customers' end-user data. Acme processes that data strictly as a **processor** under the customer's documented instructions, in accordance with Art. 4(8) and Art. 28 GDPR. The lawful basis for that processing is determined by each customer as controller, not by Acme, and any legitimate-interests analysis for it is the customer controller's responsibility. This assessment therefore applies exclusively to Acme's own-website analytics, where Acme is the controller.

## 3. The Three-Part Legitimate Interests Test

This section applies the three-stage test required by Art. 6(1)(f) GDPR and structured in EDPB Guidelines 01/2024: (1) identification of a legitimate interest, (2) necessity of the processing, and (3) balancing of the interest against the data subjects' rights and freedoms.

### 3.1 Stage 1 — Acme's legitimate interest

Acme has a legitimate interest in understanding how visitors use its own website in order to improve website content, functionality and product pages. This interest is real, present and lawfully pursued: Acme operates a B2B SaaS platform, and the quality, discoverability and performance of its marketing and product pages directly affect its ability to serve existing customers and attract new ones. Website analytics allow the Product Analytics team to identify underused content, broken journeys and friction points, and to prioritise improvements on evidence rather than assumption. EDPB Guidelines 01/2024 confirm that a controller's business improvement interests can be legitimate interests; this assessment adopts that framing for Acme's own-website analytics only.

### 3.2 Stage 2 — Necessity of the processing

The processing is necessary for the identified interest because there is no less intrusive way for Acme to obtain comparable insight into how its website is used. Acme has considered the alternatives:

- **Consent (Art. 6(1)(a))** is not an appropriate basis for this analytics processing. Analytics cookies and tags are in any event set only after the visitor has given consent through the cookie banner, so the intrusive step of collection is already consent-gated; however, the ongoing use of the resulting pseudonymised data for website improvement is a matter of Acme's own operational interest, and the legitimate-interests basis — with an unconditional right to object — is the better fit under EDPB Guidelines 01/2024.
- **Contract (Art. 6(1)(b))** is not available: website visitors who browse Acme's public pages are not necessarily parties to a contract with Acme, and website-improvement analytics are not necessary for performing any contract with them.
- **Less intrusive means** are insufficient: aggregate-only or sample-based measurement cannot reliably reveal page-level friction and feature-interaction patterns, and the pseudonymisation already applied means the data cannot be used to single out individual visitors.

Necessity is therefore established: the processing achieves the interest with the least interference consistent with that interest.

### 3.3 Stage 3 — Balancing test

The balance favours continuing the processing on the legitimate-interests basis, for the following reasons:

- **Nature of the data.** The data is pseudonymised before analytics use. Visitors are not identified by name or direct identifiers, which materially limits any interference with their rights and freedoms.
- **Reasonable expectations.** Website visitors can reasonably expect a commercial website operator to measure usage of its own site. Acme's privacy notice discloses this processing and provides an opt-out link, so expectations are informed rather than merely assumed.
- **Impact on data subjects.** The processing does not produce decisions about individuals, involves no profiling with legal or similarly significant effects, and does not disclose data to third parties. The realistic impact on any visitor is minimal.
- **Safeguards.** Data subjects may object to this processing at any time using the opt-out link in Acme's privacy notice, in line with Art. 21(1) GDPR. Objections are triaged in the PrivacyDesk queue INT-Q-CONSENT within the internal SLA of 5 business days — stricter than the one-month deadline in Art. 12(3) GDPR. When a data subject objects, Acme stops the processing for that data subject.

**Conclusion of the balancing test:** the impact on website visitors' rights and freedoms is limited and safeguarded, and does not override Acme's legitimate interest in understanding and improving its own website. The legitimate-interests basis under Art. 6(1)(f) GDPR is therefore appropriate for this processing.

## 4. Right to Object and Opt-Out Mechanism

### 4.1 The right to object under Art. 21(1) GDPR

Website visitors have the right to object, on grounds relating to their particular situation, to Acme's processing of their pseudonymised product-usage analytics, which is carried out on the legitimate-interests basis under Art. 6(1)(f) GDPR (Art. 21(1) GDPR). Visitors may object at any time using the opt-out link in Acme's privacy notice. Where an objection is made, Acme stops the processing for that data subject unless it demonstrates compelling legitimate grounds which override the visitor's interests, rights and freedoms. For this analytics processing, Acme has identified no such overriding grounds and does not contest objections.

### 4.2 Triage in PrivacyDesk

Objections submitted via the opt-out link are triaged in the PrivacyDesk queue **INT-Q-CONSENT**, together with consent withdrawals and cookie complaints. Acme's internal SLA for this queue is **5 business days** — stricter than the one-month deadline permitted by Art. 12(3) GDPR.

### 4.3 What happens when a visitor objects

1. The objection is logged in INT-Q-CONSENT on receipt.
2. Privacy Operations verifies the objection relates to Acme's own-website product-usage analytics.
3. Processing of the objector's pseudonymised analytics data stops; the visitor is added to the analytics suppression controls.
4. The visitor receives confirmation of closure within the 5-business-day SLA.

Acme does not charge for, question, or place conditions on objections to this processing. This mechanism applies only to Acme's own-website analytics; it does not extend to Beacon customers' end-user data, for which Acme acts as processor.

## 5. Safeguards and Data Minimisation

The safeguards below are the technical and organisational measures relied on in the Stage 3 balancing test (Section 3.3 of this LIA).

### 5.1 Pseudonymisation

Visitors are not identified by name or direct identifiers. Product-usage analytics data is pseudonymised before it is used for analytics, consistent with Art. 32 GDPR, which limits the interference with data subjects' rights and freedoms.

### 5.2 Consent gating of analytics tags (CMP v3)

Analytics and marketing cookies and tags are set on Acme's website only after the visitor has given consent through the cookie banner; strictly necessary cookies are set without consent. The banner is served by the internal consent-management module **CMP v3**, which blocks analytics and marketing tags until the visitor takes a positive action. Analytics tags therefore fire only after banner consent is given. CMP v3 replaced the legacy banner in the January 2026 website redesign; the legacy banner had rendered the analytics opt-out only as a footer link on the privacy notice, whereas CMP v3 presents opt-out choices at the point of collection.

### 5.3 Logging and accountability

Each banner interaction is logged to **Atlas**, Acme's internal analytics warehouse. These logs, together with the consent records described in Acme's privacy notice disclosures, allow the Privacy Office to demonstrate compliance with the transparency and accountability obligations in Art. 5(2) GDPR.

### 5.4 Storage limitation

Analytics records are retained only as long as necessary for the website-improvement purposes described in Section 2.2, in line with Art. 5(1)(e) GDPR. Retention periods are reviewed at the annual review of this LIA against EDPB Guidelines 01/2024; data exceeding the retention period is deleted from Atlas.

### 5.5 Opt-out safeguard

The opt-out link in Acme's privacy notice and the INT-Q-CONSENT triage process described in Section 4 remain the operational safeguard of last resort for any visitor whose data has already been collected.

## 6. Risk Assessment and Residual Risk

### 6.1 Risk table

| # | Risk | Likelihood | Severity | Mitigations | Residual risk |
|---|---|---|---|---|---|
| R1 | Re-identification of a website visitor from pseudonymised analytics data in Atlas | Low | Medium | Pseudonymisation before analytics use (Section 5.1); no direct identifiers collected; access limited to Product Analytics | Low |
| R2 | Failure to honour an objection to this processing (Art. 21(1) GDPR) | Low | Medium | Opt-out link in the privacy notice; INT-Q-CONSENT triage with 5-business-day SLA — stricter than the one-month deadline in Art. 12(3) GDPR; same-day suppression checks | Low |
| R3 | Scope creep — use of the analytics data for non-essential purposes beyond website improvement | Low | High | Processing purposes fixed in Section 2.2; annual review of this LIA against EDPB Guidelines 01/2024; any new purpose requires a fresh assessment on form INT-FORM-07 before processing begins | Low |

### 6.2 Assessment against DPIA triggers

None of the criteria in Art. 35(3) GDPR is met for this processing: there is no systematic and extensive evaluation of personal aspects producing legal or similarly significant effects (Art. 35(3)(a)), no large-scale processing of special categories or criminal-offence data (Art. 35(3)(b)), and no systematic monitoring of a publicly accessible area on a large scale (Art. 35(3)(c)). Applying the WP248 rev.01 criteria, at most one criterion (website monitoring, pseudonymised and small-scale) is present, which does not indicate that a DPIA is required.

### 6.3 Conclusion

With the mitigations in Section 5 and Section 6.1 in place, the residual risk to website visitors' rights and freedoms from Acme's legitimate-interests analytics processing is **low**. The Art. 6(1)(f) GDPR basis, with the unconditional Art. 21(1) objection mechanism, remains proportionate and appropriate. No DPIA trigger under Art. 35(3) GDPR or WP248 rev.01 is met, and no prior consultation under Art. 36 GDPR is required. This conclusion is re-tested at each annual review of this LIA by the Privacy Office.

## 7. Conclusion, Sign-Off and Review

### 7.1 Conclusion

The three-part test in Section 3 is satisfied. Acme's interest in understanding and improving its own website is legitimate, the pseudonymised product-usage analytics are necessary for that interest, and the balance in Section 3.3 favours the processing given the pseudonymisation safeguards and the unconditional opt-out in the privacy notice. Legitimate interests under Art. 6(1)(f) GDPR is therefore a valid lawful basis for Acme's own-website product-usage analytics. This conclusion does not extend to Beacon customers' end-user analytics, for which Acme acts as processor under the customer's documented instructions and the lawful basis is determined by each customer controller.

### 7.2 Sign-off

| Role | Name | Date |
|---|---|---|
| Approver (Data Protection Officer) | Tomás Reyes | 2026-02-14 |

### 7.3 Review commitment

This LIA is reviewed annually by Mara Okafor, Head of Privacy Operations, against EDPB Guidelines 01/2024 on legitimate interests, and documented on form INT-FORM-07. Any change to the purposes, systems or safeguards described in this assessment triggers an out-of-cycle review before processing continues.
