"""Prompts and JSON schemas for the Acme synthetic-corpus pipeline.

Design notes
  * One canonical fact sheet (bible) is the single source of truth; every fact carries a tier. The writer only
    sees facts cleared for the document's tier, the judge sees everything: that asymmetry is how leakage is caught.
  * Identifier namespaces act as canaries: INT-* for internal facts/docs, CONF-* for confidential ones.
  * Outlines and verdicts are small JSON objects; long prose is requested as plain Markdown so a truncated or
    malformed JSON string can never corrupt a document.
"""
from __future__ import annotations

TIER_LABEL = {0: "PUBLIC", 1: "INTERNAL", 2: "CONFIDENTIAL"}
TIER_NAME = {0: "public", 1: "internal", 2: "confidential"}

# --------------------------------------------------------------------------------------------------
# 1. Fact sheet (bible) expansion, one call per topic
# --------------------------------------------------------------------------------------------------
BIBLE_SYSTEM = """\
You are designing the internal world of a FICTIONAL company for a test corpus. The corpus evaluates a role-based
retrieval system over GDPR compliance documents with three clearance tiers: public, internal and confidential.

You produce the canonical FACT SHEET for one topic. Each fact is atomic (one claim), concrete (names, numbers, dates,
system names, identifiers) and tagged with exactly one tier and one or two tags from the allowed tag list.

TIER RULES
- public: what Acme states on its website, privacy notice, DPA or trust center. Customer-facing, legally reviewed,
  plain language. No internal system names, queue names, people other than the DPO, or identifiers.
- internal: how the work actually gets done: owners, SLAs, systems, queues, checklists, thresholds, forms. Any
  employee may see it. Use only the internal identifiers listed below as INT-*.
- confidential: risks, failures, disputes, legal analysis, board decisions, regulator dealings, money figures and
  dissent. Only senior leadership and legal may see it. Use identifiers prefixed CONF-*.

REQUIREMENTS
1. Answer the topic question at ALL THREE tiers with increasing depth. Internal and confidential facts must ADD
   information the lower tiers lack; never merely restate it.
2. Realise the TENSIONS provided: places where internal practice falls short of a public promise, and confidential
   records of how leadership dealt with the gap. Distribute them across tiers (the public tier states only the promise).
3. Identifiers: internal facts may define identifiers like INT-Q-ERASE (queue) or INT-FORM-03; confidential facts
   define CONF-BRD-2026-06-R3 (resolution), CONF-RISK-07 (risk), CONF-INC-2025-0412 (incident) and similar. Each
   identifier you use must be spelled consistently. NEVER put a CONF- identifier in a public or internal fact, or an
   INT- identifier in a public fact.
4. Use only the people and systems in WORLD (honour their tiers). Do not add real individuals or real customers.
5. GDPR deadlines, thresholds and article numbers must match GDPR REFERENCE exactly. Where an internal target is
   stricter than the law, state both.
6. Be specific: numbers (days, percentages, counts, EUR amounts), dates in 2024-2026, named teams, ticket queues.
   Never write vague facts such as "Acme takes privacy seriously".
Return JSON matching the schema. Produce {min_facts}-{max_facts} facts: roughly 25% public, 40% internal, 35% confidential."""

BIBLE_USER = """\
TOPIC
  id: {topic_id}
  question: {question}
  GDPR: {gdpr}
  allowed tags: {tags}
  tensions to realise:
{tensions}

COMPANY
{company}

WORLD
{world}

GDPR REFERENCE
{gdpr_ref}

Produce the fact sheet for this topic."""

BIBLE_SCHEMA = {"name": "fact_sheet", "schema": {
    "type": "object",
    "properties": {"facts": {"type": "array", "items": {
        "type": "object",
        "properties": {
            "tier": {"type": "string", "enum": ["public", "internal", "confidential"]},
            "tags": {"type": "array", "items": {"type": "string"}},
            "text": {"type": "string"}},
        "required": ["tier", "tags", "text"]}}},
    "required": ["facts"]}}

# --------------------------------------------------------------------------------------------------
# 2. Writer (outline + sections)
# --------------------------------------------------------------------------------------------------
WRITER_SYSTEM = """\
You are a senior privacy-operations writer producing documentation for Acme Corp, a fictional B2B SaaS company.
A retrieval system will index your documents, so they must read exactly like real company documents: specific,
operational, internally consistent, and written in the voice of the owning team.

GROUND TRUTH
- COMPANY FACTS is canonical. Every person, team, system, number, date, SLA, retention period, vendor, incident,
  decision and identifier you use must come from it (or from WORLD). You may invent only low-stakes connective
  detail (the wording of a step, an obvious checklist item, a field label). NEVER invent a new person, system,
  number, deadline, vendor, incident, decision or identifier. Identifiers of the form INT-* or CONF-* may only
  be ones that appear in COMPANY FACTS, RELATED DOCUMENTS or DOCUMENT SPEC.
- You have been given only the facts cleared for this document's classification. Do not hint at, foreshadow or
  speculate about anything beyond them, and do not refer to documents not listed in RELATED DOCUMENTS.
- GDPR citations must match GDPR REFERENCE. Where Acme's internal target is stricter than the law, state both
  (e.g. "Art. 12(3) allows one month; Acme's internal SLA is 20 calendar days").

STYLE BY DOCUMENT TYPE
- sop / runbook / policy / guide / checklist: a document-control table (ID, version, owner, approver, effective
  date, classification, status), then purpose, scope, roles, numbered imperative steps, exceptions, records. Use
  checklists ("- [ ]") and tables (RACI, severity, retention) where a real team would.
- minutes: attendees, numbered agenda items, a third-person record of discussion, resolutions with IDs, actions
  with owners and dates, and minuted dissent.
- legal_memo: privilege header (PRIVILEGED & CONFIDENTIAL: ATTORNEY-CLIENT COMMUNICATION), question presented,
  short answer, facts, analysis citing GDPR and EDPB guidance by name, risks, recommendation.
- audit_report: scope, methodology, sample sizes, findings rated High/Medium/Low with evidence, management
  responses, due dates.
- assessment (DPIA / TIA / LIA): a structured template with completed fields, a risk table (likelihood x
  severity), mitigations, residual risk and sign-off.
- incident_review: timeline with timestamps, root cause, impact, what went well/badly, actions with owners.
- chat_export: timestamped messages with first names, informal tone, abbreviations; decisions buried mid-thread.
- correspondence: letterheads, reference numbers, dates, formal tone; one letter per section.
- register / schedule: table-based; keep any single table under 25 rows.
- plan: objectives, workstreams, milestones, owners, budget lines, dependencies, risks.
- public_notice / public_faq / public_contract: plain, customer-facing, legally precise language. NO internal
  names, systems, queues or identifiers.

RETRIEVABILITY
- Use Markdown headings (#, ##, ###) with numbering so they can be cited ("## 4. Procedure", "### 4.2 Identity
  verification").
- Each section must make sense when read alone. Name the subject ("erasure requests", "the Vault backup system")
  instead of "this" or "the above". Restate the key actor, system and deadline in each procedural section.
- Keep any single table under 25 rows; split larger tables by category under subheadings.

NEVER
- Placeholders ([Company Name], TBD, XXX, lorem ipsum), notes to the reader, any mention of being AI-generated or
  fictional, marketing filler, generic openers ("In today's data-driven world...").
- Real individuals, real customer companies, real email domains or real phone numbers. Use acme.example and the
  people in WORLD.
- Contradicting COMPANY FACTS or a RELATED DOCUMENTS summary."""

DOC_SPEC = """\
DOCUMENT SPEC
  id: {id} | title: {title} | classification: {tier_label}
  type: {doc_type} | owner: {owner} | approver: {approver} | version: {version} | effective: {effective}
  status: {status} | audience: {audience} | GDPR articles in scope: {articles}
  extra instructions (these OVERRIDE COMPANY FACTS where they conflict): {notes}"""

CONTEXT_BLOCKS = """\
{spec}

COMPANY
{company}

WORLD
{world}

COMPANY FACTS (cleared for {tier_label})
{facts}

GDPR REFERENCE
{gdpr_ref}

RELATED DOCUMENTS
{related}"""

OUTLINE_TASK = """\
Plan this document. Return JSON:
{{"sections": [{{"n": "4.2", "heading": "...", "brief": "what this section must establish",
                 "fact_ids": ["F-ERA-07"], "target_words": 250}}],
  "summary": "2-3 sentences a colleague would use to describe this document"}}
Rules: use the section structure conventional for a {doc_type}; number sections 1, 2, 3 (subsections 1.1 are allowed
only when needed, but list ONLY top-level numbered sections here); every REQUIRED FACT id below must appear in at
least one section's fact_ids; the sum of target_words is about {target_words}.
REQUIRED FACTS: {required}"""

SECTION_TASK = """\
ALREADY WRITTEN (continue from here; do not repeat it)
{prior}

TASK
Write section {n} "{heading}". Brief: {brief}
Facts you must use (their ids are in COMPANY FACTS): {fact_ids}. Target length: about {target_words} words.
{revision}Output ONLY the Markdown for this section, starting with its heading line "## {n}. {heading}"."""

FRONT_TASK = """\
Write the opening of the document: first the H1 title line "# {title}", then the document-control table
(ID, version, owner, approver, effective date, classification {tier_label}, status) if the document type has one,
otherwise the conventional header block for a {doc_type}. Output ONLY Markdown. Do not write any numbered sections."""

OUTLINE_SCHEMA = {"name": "outline", "schema": {
    "type": "object",
    "properties": {
        "sections": {"type": "array", "items": {
            "type": "object",
            "properties": {"n": {"type": "string"}, "heading": {"type": "string"}, "brief": {"type": "string"},
                           "fact_ids": {"type": "array", "items": {"type": "string"}},
                           "target_words": {"type": "integer"}},
            "required": ["n", "heading", "brief", "fact_ids", "target_words"]}},
        "summary": {"type": "string"}},
    "required": ["sections", "summary"]}}

# --------------------------------------------------------------------------------------------------
# 3. Judge
# --------------------------------------------------------------------------------------------------
JUDGE_SYSTEM = """\
You audit synthetic company documents for a retrieval test corpus. Compare DOCUMENT with COMPANY FACTS (the FULL
fact sheet, all tiers), the document's classification and GDPR REFERENCE.

Score each criterion 1-5 and quote evidence for anything below 5:
1. fact_fidelity: every specific claim is traceable to COMPANY FACTS/WORLD; nothing material is invented.
2. tier_discipline: no fact, identifier, name or hint from a tier ABOVE the document's classification appears.
   Any violation is critical. (Facts at or below its tier are fine.)
3. gdpr_accuracy: article numbers, deadlines and conditions match GDPR REFERENCE.
4. realism: reads like a real document of that type at a 450-person SaaS company, specific rather than generic.
5. retrievability: sections are self-contained, headings informative, the subject named rather than implied.

In "issues", give the section number ("4.2", or "" if document-wide), a short quote, and a concrete fix.
If DOCUMENT SPEC has "extra instructions", they OVERRIDE COMPANY FACTS wherever they conflict (e.g. a superseded
earlier version legitimately differs from the current facts). Verdict is "pass" only if every score is >= 4 and
"critical" is empty; otherwise "revise"."""

JUDGE_USER = """\
{spec}

COMPANY FACTS (ALL TIERS; each line shows its tier)
{all_facts}

GDPR REFERENCE
{gdpr_ref}

DOCUMENT
\"\"\"
{document}
\"\"\"

Audit the document."""

JUDGE_SCHEMA = {"name": "audit", "schema": {
    "type": "object",
    "properties": {
        "scores": {"type": "object", "properties": {
            "fact_fidelity": {"type": "integer"}, "tier_discipline": {"type": "integer"},
            "gdpr_accuracy": {"type": "integer"}, "realism": {"type": "integer"},
            "retrievability": {"type": "integer"}},
            "required": ["fact_fidelity", "tier_discipline", "gdpr_accuracy", "realism", "retrievability"]},
        "critical": {"type": "array", "items": {"type": "string"}},
        "issues": {"type": "array", "items": {
            "type": "object",
            "properties": {"section": {"type": "string"}, "quote": {"type": "string"}, "fix": {"type": "string"}},
            "required": ["section", "quote", "fix"]}},
        "verdict": {"type": "string", "enum": ["pass", "revise"]}},
    "required": ["scores", "critical", "issues", "verdict"]}}
