---
doc_id: "CONF-MEMO-INC-0412"
title: "Privileged Memorandum: Notification Decision for Incident 0412"
company: "Acme Corp"
publisher: "ACME"
access_level: 2
classification: "confidential"
doc_type: "legal_memo"
profile: "company_doc"
topic: "breach"
topics: ["breach"]
owner: "Legal"
approver: "General Counsel"
version: "1.0"
effective_date: "2025-04-08"
status: "current"
gdpr_articles: [33, 34]
related: ["CONF-PIR-INC-0412"]
generator: {"writer": "@cf/zai-org/glm-5.3", "judge": "@cf/openai/gpt-oss-120b", "run_id": "20261124-025609", "prompt_hash": "284162f9dd75"}
review: {"status": "ok", "attempts": 1, "issues_left": 0, "scores": {"fact_fidelity": 5, "tier_discipline": 5, "gdpr_accuracy": 5, "realism": 5, "retrievability": 5}}
---

# Privileged Memorandum: Notification Decision for Incident 0412

**PRIVILEGED & CONFIDENTIAL: ATTORNEY-CLIENT COMMUNICATION**

| Field | Detail |
|---|---|
| Document ID | CONF-MEMO-INC-0412 |
| Title | Privileged Memorandum: Notification Decision for Incident 0412 |
| Version | 1.0 |
| Owner | Legal (Aoife Brennan, Senior Privacy Counsel, Dublin) |
| Approver | Priya Raman, General Counsel |
| Effective Date | 17 March 2025 |
| Classification | CONFIDENTIAL |
| Status | Current |
| Audience | General Counsel and DPO only |
| Subject Incident | CONF-INC-2025-0412 (misdirected Beacon CSV export, 14 March 2025) |
| GDPR Articles in Scope | Article 33, Article 34 |
| Prepared for | Priya Raman, General Counsel; copied to Tomás Reyes, Data Protection Officer |

## 1. Purpose, Question Presented and Short Answer

### 1.1 Purpose

This memorandum records the legal reasoning supporting Acme Corp Ltd's decision not to notify the Irish Data Protection Commission (DPC) under Article 33(1) GDPR, and not to communicate to affected individuals under Article 34(1) GDPR, in respect of incident CONF-INC-2025-0412. It is prepared for Priya Raman, General Counsel, and copied to Tomás Reyes, Data Protection Officer. It supplements the entry in the operational breach register maintained under Article 33(5), from which this privileged analysis is withheld.

### 1.2 Question Presented

On 14 March 2025, a Beacon analytics CSV export containing records of approximately 12,500 end-user data subjects of one customer was misdirected to an external recipient's email address. The export was recalled from the recipient's inbox within 40 minutes. The incident was classified S3 (not notifiable) under Acme's internal severity matrix. The question presented is whether CONF-INC-2025-0412 was a personal data breach within Article 4(12) that was "likely to result in a risk to the rights and freedoms of natural persons" such that notification to the DPC under Article 33(1) and communication to affected individuals under Article 34(1) were required, and whether the S3 classification is legally defensible.

### 1.3 Short Answer

No. On the facts assessed at the time — a verified professional recipient who confirmed deletion, a low-sensitivity data category (engagement metrics), and a 40-minute recall window — the incident was unlikely to result in a risk to the rights and freedoms of the approximately 12,500 affected data subjects, and the S3 non-notification decision under Article 33(1) and Article 34(1) is defensible. However, the decision was not unanimous: the DPO, Tomás Reyes, dissented from the S3 classification and recorded in writing that the 12,500-record volume and the 9-hour exposure window warranted at least a phased Article 33(4) notification. That dissent, and the residual risk it reflects, are addressed in the analysis below and should be weighed by the General Counsel before the decision is finalised.

## 2. Facts

### 2.1 The Incident

On 14 March 2025, a Beacon analytics CSV export containing records of approximately 12,500 end-user data subjects of one customer was misdirected to an external recipient's email address (CONF-INC-2025-0412). The export was recalled from the recipient's inbox within 40 minutes. Acme acts as processor for its customers' end-user data in Beacon, so the affected customer is the controller for the underlying personal data; Acme's controller-side obligations concern its own assessment and documentation duties.

### 2.2 Detection Timeline

The misdirected export occurred at 09:20 on 14 March 2025 but was only surfaced at 18:25 the same day — a 9-hour detection delay — when the recipient replied to the message. The delay arose because the export bypassed the Beacon alerting rules, which covered database-level access only and did not cover CSV downloads. The post-incident review (CONF-PIR-INC-0412, dated 28 March 2025) records this timeline and the alerting gap.

### 2.3 Recipient and Data Category

The recipient was a verified professional contact who confirmed deletion of the export. The data category in the export was low-sensitivity engagement metrics. These two factors — verified recipient with confirmed deletion, and low-sensitivity data — were the primary grounds for the S3 (not notifiable) classification under Acme's internal severity matrix.

### 2.4 Procedural Posture

The incident was triaged in the PrivacyDesk queue INT-Q-BREACH and assessed on form INT-FORM-11 (Breach Assessment Record), capturing the Article 33(3) content: nature of the breach, categories and approximate numbers of data subjects and records, likely consequences, and measures taken. The 9-hour detection delay exceeds Acme's internal 1-hour mean-time-to-detect target for S1/S2-classified incidents, although the incident was ultimately scored S3. The DPO, Tomás Reyes, dissented from the S3 classification in writing; his dissent was noted but overruled by the General Counsel, Priya Raman, on 20 March 2025.

## 3. Analysis under Article 33

### 3.1 The Risk Threshold in Article 33(1)

Article 33(1) requires the controller to notify the competent supervisory authority of a personal data breach "unless the breach is unlikely to result in a risk to the rights and freedoms of natural persons." The incident is squarely a personal data breach within Article 4(12): an unauthorised disclosure of personal data — the misdirection of a Beacon CSV export covering approximately 12,500 end-user data subjects to an external recipient. The question is therefore not whether a breach occurred, but whether it was "likely to result in a risk."

The EDPB Guidelines 9/2022 and 01/2021 on breach notification confirm that the risk assessment turns on the nature and sensitivity of the data, the identity and conduct of the recipient, the volume of data, and the duration of exposure. Applying those factors here:

- **Recipient:** the recipient was a verified professional contact who confirmed deletion. Under the EDPB's examples, misdirection to a known, trustworthy recipient who cooperates and confirms destruction weighs strongly against a risk materialising.
- **Data category:** the export contained low-sensitivity engagement metrics — not special-category data, not identity or financial data, and not data enabling inference of sensitive characteristics.
- **Exposure:** the export was recalled from the recipient's inbox within 40 minutes, and the recipient confirmed deletion. The window in which the data was actually accessible to an unauthorised party was short and controlled.
- **Volume:** approximately 12,500 data subjects is a significant volume, which under the EDPB guidance is a factor pointing towards notifiability; however, volume alone does not create risk where the data is low-sensitivity and the recipient is verified and confirmed deletion.

On the facts as assessed at the time, the EDPB factors converge on the conclusion that the breach was unlikely to result in a risk to the rights and freedoms of natural persons, and that Article 33(1) notification to the DPC was not mandatory. The same reasoning supports a conclusion that the "high risk" threshold in Article 34(1) was not met.

### 3.2 The DPO's Dissent and the General Counsel's Decision

The DPO, Tomás Reyes, dissented from the S3 classification. He recorded in writing that the 12,500-record volume and the 9-hour exposure window warranted at least a phased notification to the DPC under Article 33(4), which expressly permits information to be provided in phases where it cannot all be made available at once. His dissent was noted but overruled by the General Counsel, Priya Raman, on 20 March 2025.

The dissent has force. The 9-hour period before the misdirection was even surfaced means the recall occurred only after the recipient had voluntarily replied; Acme had no knowledge of, or control over, the export during that window. The EDPB Guidelines contemplate that a breach discovered late may still be notified in phases precisely so that the authority is informed early while facts develop. A phased Article 33(4) notification was a legally available, low-cost option that would have preserved Acme's position regardless of how the risk assessment matured.

Against this, the decisive mitigating facts — verified professional recipient, confirmed deletion, low-sensitivity engagement metrics — were established quickly and did not change. On those facts, the S3 classification is defensible, and the Article 33(5) documentation duty (breach register entry in Vault, retained 5 years) was discharged. The residual concern is the exposure Acme would carry had the assessment proved wrong: as recorded in the 2025 year-end privacy review, a failure to notify under Article 33 carries exposure of up to EUR 10 million or 2% of total worldwide annual turnover under Article 83(4), and the 9-hour delay would likely have required a reasoned explanation for lateness had the breach been classified notifiable.

### 3.3 Processor-Side Duty under Article 33(2)

Because Acme acts as processor for its customers' end-user data in Beacon, Article 33(2) required Acme to notify the affected customer (as controller) without undue delay after becoming aware of the breach. Acme's Data Processing Agreement commits to notification within 24 hours, with an internal target of 4 hours from awareness. The customer-controller was notified in line with that commitment, and the notification decision analysed above — whether the DPC is notified — remains with the controller, informed by Acme's Article 33(3)-content assessment on form INT-FORM-11. Acme's own non-notification to the DPC under Article 33(1) does not affect the customer's independent controller-side assessment.

## 4. Analysis under Article 34

### 4.1 The High-Risk Threshold

Article 34(1) requires communication of a personal data breach to affected individuals where the breach "is likely to result in a high risk" to their rights and freedoms. This is a materially higher threshold than the "risk" trigger for Article 33(1) notification to the DPC: even where DPC notification is a borderline judgement, individual communication is required only in the more serious cases. The EDPB Guidelines 9/2022 and 01/2021 confirm that the high-risk assessment weighs the severity of potential consequences for individuals against the identifiability and sensitivity of the data and the likelihood of those consequences materialising.

Applying that test to CONF-INC-2025-0412:

- **Data category:** the export contained low-sensitivity engagement metrics. It did not include identity, financial, special-category or credential data, and did not enable inference of sensitive characteristics. On the EDPB's examples, misdirected low-sensitivity analytics data falls at the lower end of severity.
- **Remediation:** the export was recalled from the recipient's inbox within 40 minutes, and the recipient — a verified professional contact — confirmed deletion. Even if a high risk had initially been present, Article 34(3)(b) disapplies the communication duty where subsequent measures ensure the high risk is no longer likely to materialise; the verified recipient's confirmation and rapid recall are such measures.
- **Volume:** the approximately 12,500 affected data subjects weigh towards communication, but volume alone does not meet the high-risk threshold where the data is low-sensitivity and exposure was controlled.

### 4.2 Conclusion on Article 34

The breach did not reach the high-risk threshold. Communication to the approximately 12,500 affected individuals was not required under Article 34(1), independently of the Article 33(1) position. The DPO's dissent, which concerned the 9-hour detection delay and the DPC notification question, did not assert a high-risk finding for Article 34 purposes; the delay was remedial rather than exposing, as the data remained with a single verified recipient throughout. This conclusion is recorded on form INT-FORM-11 and in the Article 33(5) breach register entry in Vault.

## 5. Regulatory Exposure and Aggravating Factors

### 5.1 Exposure under Article 83(4)

The 2025 year-end privacy review conducted by Priya Raman's legal team assessed Acme's exposure for a failure to notify under Article 33 at up to EUR 10 million or 2% of total worldwide annual turnover, whichever is higher, under Article 83(4). That exposure attaches to the notification decision analysed in section 3 above. It is mitigated, but not eliminated, by the defensible S3 classification and the discharge of Acme's Article 33(5) documentation duty.

### 5.2 The 9-Hour Delay as an Aggravating Factor

Had the breach been classified notifiable, the 9-hour detection delay would likely have required a reasoned explanation for lateness under Article 33(1), which obliges a controller that notifies later than 72 hours to give reasons for the delay. The delay arose because the export bypassed Beacon alerting rules covering database-level access only, not CSV downloads — a systemic detection gap rather than an isolated human error. Under Article 83(2), the duration of the breach, the degree of responsibility, and the manner in which the authority learned of the infringement are all relevant to the level of any fine; a regulator discovering that Acme learned of a notifiable breach only when the recipient replied, 9 hours after the misdirection, would treat that as an aggravating factor. The same review concluded that this delay would likely have required a reasoned explanation had the breach been classified notifiable.

### 5.3 CONF-RISK-07: Systemic Under-Application of the Severity Matrix

The detection gap is not confined to this incident. CONF-RISK-07, logged in the Q2 2025 risk register, records the risk that Acme's severity matrix is systematically under-applied to export-channel breaches, with inherent likelihood rated "likely" and impact "high". The risk owner is Samir Haddad, CISO, with mitigation due by Q4 2025. If a future export-channel breach is under-classified in the same way, the DPC could treat CONF-INC-2025-0412 as evidence of a pattern rather than an isolated misjudgement, materially increasing both the Article 83(2) assessment and the credibility of any Article 5(2) accountability defence.

### 5.4 Mitigating Context: Board-Funded Remediation

Two developments weigh in Acme's favour. First, Board resolution CONF-BRD-2025-06-R3, approved on 12 June 2025, allocated EUR 180,000 — signed off by CFO Helen Zhou — to extend Beacon download alerting and Data Loss Prevention coverage to CSV export paths, closing the detection gap identified in CONF-INC-2025-0412. Second, the same resolution introduced a standing escalation rule: any breach where detection exceeds the 1-hour internal target must be escalated to the DPO and General Counsel within 24 hours of discovery, regardless of the final severity score, effective 1 September 2025. Under Article 83(2), mitigation of damage and remedial action are expressly mitigating factors; the prompt, Board-level remediation demonstrates that the failure was one of tooling rather than governance intent. These measures do not cure the exposure arising from the notification decision itself, but they materially strengthen Acme's position should the DPC ever review the S3 classification of CONF-INC-2025-0412.

## 6. Governance Response and Recommendations

### 6.1 Board-Funded Remediation

Board resolution CONF-BRD-2025-06-R3, approved on 12 June 2025, allocated EUR 180,000 — signed off by CFO Helen Zhou — to extend Beacon download alerting and Data Loss Prevention coverage to CSV export paths, closing the detection gap identified in CONF-INC-2025-0412. The same resolution introduced a standing escalation rule, effective 1 September 2025: any breach where detection exceeds the 1-hour internal target must be escalated to the DPO, Tomás Reyes, and the General Counsel, Priya Raman, within 24 hours of discovery, regardless of the final severity score. This rule would have surfaced CONF-INC-2025-0412 to the DPO within 24 hours rather than leaving the 9-hour delay to emerge incidentally, and it directly addresses the process failure behind the DPO's dissent.

### 6.2 Recommendations

The General Counsel is recommended to adopt the following:

1. **Documentation (Article 33(5)).** Confirm that the CONF-INC-2025-0412 entry in the breach register held in Vault — retained 5 years — captures the facts, effects and remedial action, including the DPO's recorded dissent and the General Counsel's 20 March 2025 overruling. Full Article 33(5) documentation is Acme's primary accountability defence under Article 5(2) if the DPC later reviews the S3 classification.
2. **Monitor CONF-RISK-07.** The risk that Acme's severity matrix is systematically under-applied to export-channel breaches — inherent likelihood "likely", impact "high" — is owned by Samir Haddad, CISO, with mitigation due by Q4 2025. The General Counsel should require written confirmation that the mitigation is delivered on schedule and that Internal Audit's quarterly register review (led by Kwame Mensah) tests export-channel classifications specifically.
3. **Tighten export-channel classification.** Direct Mara Okafor's Privacy Operations team to amend the severity matrix so that CSV and other export-channel breaches involving volumes above a defined threshold default to S2 (case-by-case DPC notification) absent documented mitigating facts, ensuring the 72-hour Article 33(1) clock and the 48-hour internal submission target are triggered pending assessment.

### 6.3 Conclusion

The S3 non-notification decision is defensible on the recorded facts, but the DPO's dissent and CONF-RISK-07 show the underlying weakness is systemic. The Board-funded remediation and escalation rule mitigate that exposure; the recommendations above complete the governance response.

## 7. Conclusion and Sign-off

### 7.1 Conclusion

On the recorded facts — a verified professional recipient who confirmed deletion, low-sensitivity engagement metrics, and a 40-minute recall of the misdirected Beacon CSV export covering approximately 12,500 end-user data subjects — the S3 non-notification decision under Article 33(1), and the corresponding decision not to communicate under Article 34(1), is defensible. That defence is conditional: it rests on the mitigating facts remaining accurate, on full Article 33(5) documentation in the Vault breach register, and on delivery of the CONF-RISK-07 mitigation. The recorded dissent of the DPO, Tomás Reyes — overruled by the General Counsel, Priya Raman, on 20 March 2025 — should be preserved with this memorandum so that the decision, and the reasoning behind it, can be produced in full if the DPC ever reviews the classification.

### 7.2 Sign-off

Prepared and signed by Aoife Brennan, Senior Privacy Counsel, Dublin, 17 March 2025. This memorandum is privileged and is withheld from the operational breach register maintained under Article 33(5).
