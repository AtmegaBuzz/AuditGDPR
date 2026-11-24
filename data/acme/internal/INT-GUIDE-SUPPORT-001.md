---
doc_id: "INT-GUIDE-SUPPORT-001"
title: "Support Agent Guide: Handling Privacy Requests"
company: "Acme Corp"
publisher: "ACME"
access_level: 1
classification: "internal"
doc_type: "guide"
profile: "company_doc"
topic: "erasure"
topics: ["erasure", "access"]
owner: "Customer Support"
approver: "Head of Customer Support"
version: "1.6"
effective_date: "2026-04-02"
status: "current"
gdpr_articles: [12, 15, 17]
related: ["INT-SOP-ERASE-002", "INT-SOP-DSAR-001"]
generator: {"writer": "@cf/zai-org/glm-5.3", "judge": "@cf/openai/gpt-oss-120b", "run_id": "20261124-025609", "prompt_hash": "284162f9dd75"}
review: {"status": "ok", "attempts": 1, "issues_left": 0, "scores": {"fact_fidelity": 5, "tier_discipline": 5, "gdpr_accuracy": 5, "realism": 5, "retrievability": 5}}
---

# Support Agent Guide: Handling Privacy Requests

| Field | Value |
|---|---|
| **Document ID** | INT-GUIDE-SUPPORT-001 |
| **Version** | 1.6 |
| **Owner** | Customer Support (Owen Gallagher, Head of Customer Support) |
| **Approver** | Head of Customer Support |
| **Effective Date** | 2026-04-02 |
| **Classification** | INTERNAL |
| **Status** | Current |

**Audience:** Front-line support agents (HelpHub).

**Purpose of this guide:** This guide tells support agents what to do — and what not to do — when a customer or individual raises a privacy request (data subject access, portability, or erasure) through any support channel. Support agents do not fulfil privacy requests themselves; requests are triaged into the PrivacyDesk queues (INT-Q-DSAR, INT-Q-DSAR-CUST, INT-Q-ERASE) and handled by Mara Okafor's Privacy Operations team. This guide covers how to recognise a privacy request, how to log and route it within one business day, what to say to the requester, and when to escalate.

**Related procedures:** INT-SOP-DSAR-001 (Data Subject Access and Portability Procedure) and INT-SOP-ERASE-002 (Erasure Request Handling Procedure) are the authoritative runbooks for request handling once a request is logged.

## 1. Purpose and Scope

This guide gives front-line support agents a single reference for recognising, logging and escalating privacy requests received through any support channel. It covers erasure requests, data subject access requests (DSARs), portability requests, and controller-assistance requests from Acme customers about their end users' data.

Support agents are the first point of contact, but they never fulfil privacy requests themselves. All privacy requests are triaged into the PrivacyDesk queues — INT-Q-DSAR, INT-Q-DSAR-CUST and INT-Q-ERASE — and completed by Mara Okafor's Privacy Operations team, following the runbooks INT-SOP-DSAR-001 and INT-SOP-ERASE-002.

**Audience:** All HelpHub support agents.

**Systems covered:** HelpHub (where requests may arrive as tickets), PrivacyDesk (where requests are logged and queued), and Beacon Settings > Privacy (the self-service page customers may be directed to for account exports or deletion).

**Out of scope:** Fulfilment, identity verification, exception handling and recipient notification, which are performed by Privacy Operations.

## 2. Roles and Responsibilities

The table below shows who does what for privacy requests reaching support. Support agents recognise, log and route requests; Privacy Operations (Mara Okafor's team) performs identity verification and executes the request; DPO Tomás Reyes decides escalations; Lena Fischer (VP Engineering) receives SLA-breach reports for system-level causes.

| Activity | Support Agent (Owen Gallagher's team) | Privacy Operations (Mara Okafor) | DPO (Tomás Reyes) | VP Engineering (Lena Fischer) |
|---|---|---|---|---|
| Recognise and log request in correct PrivacyDesk queue | **R** | I | – | – |
| Route within one business day of receipt | **R** | I | – | – |
| Identity verification (per INT-FORM-03) | C | **R** | A | – |
| Execute deletion / prepare DSAR response | I | **R** | A | C |
| Decide Art. 12(6) escalation where identity cannot be confirmed within 5 business days | I | C | **R/A** | – |
| Escalate tickets breaching day 14 of the 20-day SLA | I | **R** | I | – |
| Report day-20 SLA breaches (weekly, system-level causes) | I | **R** | I | **I (recipient)** |

R = Responsible, A = Accountable, C = Consulted, I = Informed.

**Controller vs processor context:** Acme acts as controller for its own customers' account data and as processor for customers' end-user data in Beacon. Requests from individuals about their own account data are handled under Acme's controller obligations; requests from Acme customers about their end users' data are routed to INT-Q-DSAR-CUST and handled as controller-assistance tickets under the DPA (Art. 28(3)(e) GDPR).

## 3. Recognising a Privacy Request

A privacy request is any message — email, HelpHub ticket, chat or phone follow-up — in which an individual asks Acme to do something with their personal data. Requests do **not** need to cite the GDPR or use legal terms; a request counts even if the person just describes what they want in plain language.

Recognisable categories:

| Category | GDPR right | Example wording agents may encounter |
|---|---|---|
| Erasure | Art. 17 | "Delete my account and all my data", "I want everything you hold on me removed" |
| Access (DSAR) | Art. 15 | "Send me a copy of the data you have about me", "What information do you store?" |
| Portability | Art. 20 | "Export my data", "Give me my data in a file I can take elsewhere" |
| Complaint | Art. 77 | "I want to complain about how you handle my data" |

**Channels:** Requests arrive via email to privacy@acme.example, as HelpHub tickets, or are submitted directly by the individual through Beacon Settings > Privacy (where account holders can export or delete their own account data). Self-service submissions are logged automatically; anything arriving by email or ticket must be logged by an agent in the correct PrivacyDesk queue within one business day.

**Rule of thumb:** if a message is about a person's own data — access, portability, deletion, or a complaint about it — treat it as a privacy request and route it. Do not attempt to fulfil it yourself.

## 4. Logging and Routing Requests

Every privacy request reaching a support channel must be logged in PrivacyDesk within **one business day of receipt**. Logging starts the clock for the Privacy Operations team; a request that sits in HelpHub unlogged is a compliance risk, not a backlog item.

### 4.1 Queue Selection

| Request type | PrivacyDesk queue | SLA once logged |
|---|---|---|
| Erasure request (individual asks to delete their own data) | INT-Q-ERASE | 20 calendar days from identity verification (internal SLA, stricter than the one-month Art. 12(3) GDPR deadline) |
| DSAR / portability request (individual's own account data) | INT-Q-DSAR | 20 calendar days internal SLA |
| Customer request about their **end users'** data | INT-Q-DSAR-CUST | Assistance provided to the customer within 10 business days (controller-assistance under the DPA, Art. 28(3)(e) GDPR) |

### 4.2 Logging Steps

1. Confirm the request type and select the correct queue from the table above.
2. Copy the requester's wording verbatim into the ticket — do not paraphrase or summarise.
3. Record the date of receipt (email date, ticket creation date, or chat timestamp). The one-business-day logging clock runs from this date.
4. Do **not** attempt identity verification, data gathering or deletion — these belong to Privacy Operations per INT-FORM-03.
5. Set the PrivacyDesk ticket to "New — awaiting Privacy Ops triage".

### 4.3 Rules

- **Never close a privacy request as a normal support ticket.** Privacy tickets are closed only by Privacy Operations after the request is fulfilled or formally refused.
- If the requester submits via Beacon Settings > Privacy, the submission is logged automatically — do not create a duplicate.
- If the request type is unclear, log it in INT-Q-DSAR and note the ambiguity; Privacy Operations will re-route if needed.
- Requests arriving by any channel — privacy@acme.example, HelpHub tickets, or Beacon Settings > Privacy — must reach the correct queue within one business day.

## 5. What the Agent Must (and Must Not) Collect

When logging a privacy request, the agent completes the intake form **INT-FORM-03** in PrivacyDesk. The form has three parts, and agents collect exactly these — nothing more:

| INT-FORM-03 field | What the agent records |
|---|---|
| Requester's account ID | The Beacon account identifier, if the requester is an account holder |
| Systems to be checked | Tick as applicable: Beacon, Ledger, Atlas, HelpHub (for erasure requests; DSARs cover Beacon, Atlas and HelpHub) |
| Identity evidence | What the requester has already provided (e.g. "sent from account email") — recorded as a note only |

**Identity evidence — hard limits:**

- Agents must **not** request identity documents or additional proofs. Identity verification is performed solely by Privacy Operations, following the EDPB Guidelines 01/2022 principles built into INT-FORM-03.
- For Beacon account holders, Privacy Ops verifies via a logged-in session plus one proof-of-email. The agent does not carry out either step.
- For non-customers, Privacy Ops may request government ID matched to the requester's data; any ID copy is handled by Privacy Ops and **deleted within 24 hours of verification**. Agents must never ask for, receive, or store ID copies in HelpHub.
- Only verified requests start the 20-day internal SLA, so do not tell a requester the clock has started before verification is complete.

**If a requester volunteers identity documents in a ticket:** do not open or store the attachment. Log the request, note "identity evidence provided — unopened", and route to the queue within one business day so Privacy Operations can handle it under INT-FORM-03.

## 6. Identity Verification and the SLA Clock

Identity verification for privacy requests is performed **solely by Privacy Operations** (Mara Okafor's team), following checklist INT-FORM-03. Support agents never verify identity and never tell a requester that verification is complete.

**How verification works (Privacy Ops, not the agent):**

- **Beacon account holders:** verification via a logged-in session plus one proof-of-email.
- **Non-customers:** government ID matched to the requester's data; the ID copy is deleted within 24 hours of verification.

**The SLA clock:** Acme's internal SLA is **20 calendar days** to complete an erasure request or DSAR — stricter than the one-month statutory deadline in Art. 12(3) GDPR. Critically, the 20-day clock starts **only from identity verification**, not from receipt. Agents must therefore **never tell a requester that the clock has started** before Privacy Ops confirms verification on the ticket. Until then, the correct wording is: "Your request has been logged and is with our privacy team, who will confirm your identity and respond within the applicable deadline."

**Unverifiable identity:** if Privacy Ops cannot confirm the requester's identity within **5 business days**, the request is escalated to the DPO, Tomás Reyes, for a decision under Art. 12(6) GDPR (Acme may request additional information where it has reasonable doubts about identity). Agents do not chase or resolve these escalations — the DPO decides.

## 7. Customer Scripts and Expectation Setting

When acknowledging a privacy request, agents use only the approved wording below. Do not improvise commitments.

**Approved acknowledgement script:**

> "Thank you for your request. We will respond within one month of receiving it, as required by Article 12(3) GDPR. If your request is complex or numerous, this period may be extended by a further two months, in which case we will inform you of the extension and the reasons within one month."

**For access (Art. 15) requests, add:**

> "The first copy of your personal data is provided free of charge."

**If the requester asks about complaining, say:**

> "You may lodge a complaint with a supervisory authority, including the Irish Data Protection Commission. Our Data Protection Officer, Tomás Reyes, is our contact point for data-subject requests."

**What agents must never say:**

- **Never promise an exact deletion or delivery date.** Do not cite the internal 20-day SLA to requesters; the statutory commitment is one month under Art. 12(3) GDPR.
- **Never describe backup behaviour.** Do not mention Vault, backup retention, or when data "fully disappears" from all systems. Erasure execution details belong to Privacy Operations.
- **Never waive or rule out exceptions.** Do not promise that "all data will be deleted" — erasure may be refused in whole or in part where an Article 17(3) exception applies, for example legal-obligation retention of Ledger invoices or legal holds, and the requester is then informed under Art. 12(4) GDPR.
- **Never confirm the SLA clock has started** before Privacy Ops verifies identity (see section 6).

If a requester pushes for commitments beyond these scripts, escalate the ticket to Privacy Operations rather than improvising.

## 8. Escalation and Exceptions

**Escalate immediately (same business day) to Privacy Operations and copy the DPO, Tomás Reyes, if a request involves:**

- [ ] A legal hold or ongoing/anticipated litigation (erasure may be refused in whole or in part under Art. 17(3)(e) GDPR)
- [ ] Media, regulator, or supervisory-authority involvement
- [ ] Threats or hostile language from the requester

**SLA breach risk — recognise, do not act:** Tickets breaching **day 14** of the 20-day internal SLA are escalated to the Privacy Operations lead, and **day-20 breaches** are reported weekly to the DPO and Lena Fischer (VP Engineering) for system-level causes. These escalations are Privacy Ops responsibilities. If an agent notices a ticket nearing day 14, flag it to Privacy Ops — do not contact the requester about timing.

**Agents never refuse a request.** Erasure may be refused in whole or in part where an Art. 17(3) exception applies — for example, Ledger invoices retained 6 years for Irish tax law, or data subject to a legal hold, where the subject is informed of the refusal under Art. 12(4) GDPR within one month. Only Privacy Operations applies exceptions; agents must never cite Art. 17(3) or tell a requester their data "cannot be deleted". Route the question to INT-Q-ERASE or INT-Q-DSAR instead.

## 9. Records and Related Documents

**What the agent records on each ticket:** When logging a privacy request, the agent records the requester's wording verbatim, the date of receipt, the channel (privacy@acme.example, HelpHub ticket, or Beacon Settings > Privacy), the INT-FORM-03 intake fields (account ID, systems to be checked, identity-evidence note), and the PrivacyDesk queue the request was routed to (INT-Q-DSAR, INT-Q-DSAR-CUST or INT-Q-ERASE).

**Ticket retention:** Privacy tickets are retained in PrivacyDesk per the retention schedule for DSR records. Agents must not delete or archive privacy tickets in HelpHub; the HelpHub source ticket is closed only once the PrivacyDesk record is confirmed.

**Related documents:**

- **INT-SOP-ERASE-002** (Erasure Request Handling Procedure) — the authoritative runbook for erasure requests in INT-Q-ERASE, including Art. 17(3) exceptions and Art. 19 recipient notification.
- **INT-SOP-DSAR-001** (Data Subject Access and Portability Procedure) — the authoritative runbook for DSARs and portability requests in INT-Q-DSAR.
- **Acme's privacy notice** — the customer-facing commitments agents can rely on when acknowledging requests (one-month response under Art. 12(3) GDPR, first copy free under Art. 15, complaint rights including the Irish DPC).
