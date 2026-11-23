---
doc_id: "CONF-CHAT-ATLAS-001"
title: "Executive Chat Export: Retaining Deleted Customers' Data in Atlas"
company: "Acme Corp"
publisher: "ACME"
access_level: 2
classification: "confidential"
doc_type: "chat_export"
profile: "company_doc"
topic: "erasure"
topics: ["erasure", "retention"]
owner: "Executive Team"
approver: "(n/a)"
version: "1.0"
effective_date: "2026-05-19"
status: "current"
gdpr_articles: [5, 17]
related: ["INT-SCHED-RET-001"]
generator: {"writer": "@cf/zai-org/glm-5.3", "judge": "@cf/openai/gpt-oss-120b", "run_id": "20261124-025609", "prompt_hash": "284162f9dd75"}
review: {"status": "ok", "attempts": 1, "issues_left": 0, "scores": {"fact_fidelity": 5, "tier_discipline": 5, "gdpr_accuracy": 5, "realism": 5, "retrievability": 5}}
---

# Executive Chat Export: Retaining Deleted Customers' Data in Atlas

**CONFIDENTIAL — EXECUTIVE CHAT EXPORT — LEGAL HOLD RECORD**

| Field | Value |
|---|---|
| Document ID | CONF-CHAT-ATLAS-001 |
| Title | Executive Chat Export: Retaining Deleted Customers' Data in Atlas |
| Version | 1.0 |
| Owner | Executive Team |
| Approver | (n/a) |
| Effective date | 2026-05-19 |
| Classification | CONFIDENTIAL |
| Status | Current |
| Audience | Legal hold record |
| GDPR articles in scope | Art. 5, Art. 17 |

*This export is preserved as a legal hold record. Participants are identified by first name only, per standard chat-export practice. Timestamps are UTC.*

## 1. Document Control and Export Metadata

| Field | Value |
|---|---|
| Document ID | CONF-CHAT-ATLAS-001 |
| Version | 1.0 |
| Owner | Executive Team |
| Approver | (n/a) |
| Effective date | 2026-05-19 |
| Classification | CONFIDENTIAL |
| Status | Current |

**Export metadata:**

- **Platform:** Acme internal executive messaging channel (exported 2026-05-19)
- **Participants:** Helen (CFO), Julia (Product Director, Beacon AI), Priya (General Counsel), Tomás (DPO), Lena (VP Engineering), Daniel (CEO)
- **Message count:** 14 messages
- **Retention basis:** Legal hold record — preserved under the board-approved residual-risk record CONF-BRD-2026-06-R3, which accepted that personal data of subjects whose erasure requests are granted remains in Vault immutable backups for up to 35 days after execution. This export is retained for the establishment, exercise or defence of legal claims (Art. 17(3)(e) GDPR) and is excluded from routine deletion jobs.

## 2. Chat Export: Executive Thread on Retaining Deleted Customers' Data in Atlas

*Thread from the Acme internal executive messaging channel. Original discussion 2026-05-19; follow-up messages appended to the same thread in August–September 2026 and captured in this export, which was finalised as a legal hold record. Participants identified by first name only. Timestamps UTC.*

**2026-05-19 09:12 — Helen:** Morning all. Julia and I have been looking at churn numbers and we keep hitting the same wall — once a customer account is closed, we delete the billing history and we lose the signal. If we kept deleted customers' billing history in Atlas we could build a proper churn model. Worth a discussion?

**2026-05-19 09:15 — Julia:** +1. The Beacon AI lead-scoring roadmap depends on historical patterns, and closed accounts are exactly the interesting population. Atlas already holds event + billing history, so retention there feels like the cheap option.

**2026-05-19 09:22 — Priya:** Flagging this before it goes any further: retaining personal data of subjects whose erasure requests were *granted* is a different animal from ordinary analytics retention. That's an Art. 17(1)(a) problem — data no longer necessary for the original purpose — and a storage-limitation problem under Art. 5(1)(e). We can't quietly keep raw identifiers in Atlas just because the model wants them.

**2026-05-19 09:26 — Helen:** Fair. But what's actually in Atlas today post-deletion? Are we even clean?

**2026-05-19 09:31 — Lena:** Honest answer: no. Atlas actually retains event history for up to 24 months after account closure, not the 30 days we publish. It's in the internal retention register (INT-REG-RET v3.2, Mara owns it), but the public promise says 30 days. That gap is already logged as CONF-RISK-07 and Aoife assessed it as material — Art. 5(1)(e) plus 5(2) accountability exposure.

**2026-05-19 09:34 — Priya:** And CONF-RISK-07 isn't theoretical. Priya here: at the March board risk committee (CONF-BRD-2026-03-R2) I advised that the 24-month retention was originally justified by product analytics but we have no documented necessity assessment. Committee deferred pending legal review. If we now *extend* retention deliberately for churn modelling, we widen the gap on purpose. That's hard to defend.

**2026-05-19 09:40 — Lena:** Also, for anyone thinking deletion is instant: the Atlas deletion job runs nightly but has a known defect — it fails on records with more than 500 linked event rows. Data Platform has to re-run those manually, adds ~6 days per affected ticket. So even our current erasure pipeline is creaking.

**2026-05-19 09:44 — Tomás:** While we're being honest about erasure gaps: Vault. Backups are write-once, 35-day retention, and we cannot execute erasure inside Vault. Deletion only propagates when each backup ages out. So for up to 35 days after we tell a data subject "done", their data still sits in Vault. The board paper CONF-BRD-2026-06-R3 going to the June board accepts that residual risk formally.

**2026-05-19 09:47 — Helen:** And you're comfortable with that acceptance?

**2026-05-19 09:49 — Tomás:** No — and it's minuted. My dissent on CONF-BRD-2026-06-R3 is on the record: I think the 35-day Vault window should be disclosed in the privacy notice, and we should evaluate a shorter retention window or an encryption-key destruction approach. Aoife's memo (CONF-MEMO-2026-ERASE, 3 June draft) says the 35-day immutable retention is defensible as an Art. 32 / 5(1)(f)-style security backup practice — but only if we never access restored backups to resurrect erased profiles. Samir has restricted access to restored Vault data for erasure-related purposes on that basis.

**2026-05-19 09:53 — Lena:** The other condition Aoife attached: the suppression list (INT-FORM-07) has to be applied without exception so suppressed records are never restored to production. We already failed that once — CONF-INC-2025-0412, April 2025, three ex-employee records deleted despite active litigation holds. That was the legal-hold side, but it shows the mechanism breaks when process slips.

**2026-05-19 09:58 — Priya:** So, proposal to close this down: we do NOT retain raw identifiers for deleted customers in Atlas. Instead we pseudonymise — churn analytics on pseudonymised billing history, no raw identifiers. I'll take it to the risk register as the mitigation closing CONF-RISK-07. Lena owns implementation; Aoife does the compliance review.

**2026-05-19 10:02 — Julia:** Works for me. Pseudonymised history still trains the model; we just lose row-level lookups. Acceptable.

**2026-05-19 10:04 — Helen:** Agreed, and from a finance angle I'd rather fix the deletion pipeline than litigate it. What's the cost of rewriting the Atlas job properly?

**2026-05-19 10:08 — Lena:** Scoping now — target is full erasure execution within 5 days of trigger. I'll bring a budget line once Internal Audit's H1 numbers are in, because I suspect the SLA breaches are worse than we think.

---

*Appended messages, same thread:*

**2026-08-14 10:20 — Lena:** Update: CONF-RISK-07 formally closed this month with the pseudonymisation decision — implementation with my team, compliance review by Aoife due 31 Jan 2027. Also, Kwame's H1 audit found 14% of erasure requests in the period blew the 20-day internal SLA, Atlas deletion job the main cause. All still inside the statutory one month, but not comfortable.

**2026-08-14 10:26 — Helen:** Exec team approved the EUR 180,000 remediation budget to rewrite the Atlas deletion job. Q1 2027 target for the 5-day execution. My view: repeated SLA breaches are exactly what generates Art. 77 complaints to the DPC, and that's Art. 83(5) territory.

**2026-09-30 14:41 — Priya:** And it happened. One data subject whose erasure took 27 days — 7 over our internal SLA — has complained to the Irish DPC. Tracking as CONF-INC-2026-0901, Aoife leading the response. Our position is that we complied with the one-month statutory deadline under Art. 12(3); the 20-day target is internal only. Keeping this thread on legal hold given the DPC correspondence.

**2026-09-30 14:45 — Tomás:** Noted. For the record, my dissent on CONF-BRD-2026-06-R3 stands, and I want the disclosure question on the next board agenda.

*— End of export. 14 messages preserved. Retained for the establishment, exercise or defence of legal claims (Art. 17(3)(e) GDPR); excluded from routine deletion jobs._

## 3. Decisions and Actions Extracted from Thread

The following register extracts the decisions reached in the executive thread on retaining deleted customers' data in Atlas, and the open actions arising from them. This section is retained as part of the legal hold record CONF-CHAT-ATLAS-001.

### 3.1 Decisions Register

| # | Decision | Basis in thread | Related record |
|---|---|---|---|
| D-1 | Acme will not retain raw identifiers of deleted customers in Atlas for churn analytics; billing history will be pseudonymised instead (F-ERA-20) | Priya's proposal, 2026-05-19 09:58; accepted by Julia and Helen | CONF-RISK-07 (closed August 2026) |
| D-2 | EUR 180,000 remediation budget approved to rewrite the Atlas deletion job, targeting full erasure execution within 5 days of trigger by Q1 2027 (F-ERA-21) | Helen, 2026-08-14 10:26; exec team approval | H1 2026 Internal Audit finding (14% SLA breaches) |
| D-3 | Vault's 35-day residual retention stands; it is defensible only if the suppression list INT-FORM-07 is applied without exception and restored Vault data is never used to resurrect erased profiles (F-ERA-23, F-RET-20) | Tomás, 2026-05-19 09:49; Lena, 09:53 | CONF-BRD-2026-06-R3; CONF-MEMO-2026-ERASE; CONF-INC-2025-0412 |
| D-4 | No voluntary self-report to the Irish DPC on the retention gap until remediation completes (F-RET-21) | Priya's legal memo CONF-EST-2026-08 (2026-08-04) position reflected in thread closure | CONF-RISK-07; CONF-INC-2026-0901 |

### 3.2 Open Actions

| # | Action | Owner | Due date |
|---|---|---|---|
| A-1 | Implement pseudonymisation of deleted customers' billing history in Atlas (CONF-RISK-07 mitigation) | Lena Fischer (VP Engineering) | In progress |
| A-2 | Compliance review of the pseudonymisation implementation | Aoife Brennan (Senior Privacy Counsel) | 2027-01-31 |
| A-3 | Rewrite of the Atlas deletion job (5-day execution target) | Lena Fischer (VP Engineering) | Q1 2027 |
| A-4 | Vault 35-day disclosure question placed on the next board agenda | Tomás Reyes (DPO) | Next board cycle |

### 3.3 Standing Dissent

Tomás Reyes's dissent from CONF-BRD-2026-06-R3 remains on the record (2026-09-30 14:45): the 35-day Vault retention window should be disclosed in the privacy notice, and Acme should evaluate shorter backup retention or an encryption-key destruction approach.
