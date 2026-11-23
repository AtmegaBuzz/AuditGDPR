"""Prompts and JSON schemas for golden-set generation and judging.

Design notes
  * Every generation call is told exactly who the end user is (a GDPR practitioner querying a RAG system),
    what the corpus contains, and what makes a question useful *for evaluating retrieval*: it must be
    answerable from the given context, but phrased the way a user would ask, not copied from the text.
  * A question STYLE is assigned per item (rotated by the planner) so the set is not 200 "What is X?" questions.
  * The generator must return verbatim EVIDENCE quotes. These are checked programmatically against the chunk
    text, which catches hallucinated answers before the judge even runs.
  * The generator may decline (`skip`) when a chunk has nothing worth asking about (tables of contents,
    boilerplate, references); forcing a question out of junk is the main source of bad golden items.
  * Judging uses separate rubrics for answerable and unanswerable items, at temperature 0.
"""
from __future__ import annotations

# --------------------------------------------------------------------------------------------------
# Shared knowledge-base description (used by generator and judge so both have the same picture)
# --------------------------------------------------------------------------------------------------
CORPUS = """\
The knowledge base contains ONLY these 17 documents:
  - The GDPR itself: Regulation (EU) 2016/679, all 173 recitals and Articles 1-99.
  - EDPB Guidelines 03/2018 territorial scope (Art. 3); 07/2020 controller and processor concepts;
    05/2020 consent; 02/2019 Art. 6(1)(b) contract for online services; 01/2024 legitimate interests (Art. 6(1)(f));
    01/2022 right of access (Art. 15); 04/2019 data protection by design and by default (Art. 25);
    09/2022 personal data breach notification (Art. 33-34); 01/2021 examples of breach notification;
    01/2025 pseudonymisation (consultation draft); 05/2021 interplay of Art. 3 and Chapter V international transfers;
    04/2022 calculation of administrative fines (Art. 83).
  - WP29 guidelines endorsed by the EDPB: WP260 transparency (Art. 12-14); WP248 DPIA (Art. 35);
    WP243 Data Protection Officers (Art. 37-39); WP251 automated decision-making and profiling (Art. 22);
    WP242 data portability (Art. 20).
It does NOT contain: national implementing laws, court judgments (CJEU or national), DPA decisions or fines against
named companies, non-EU laws (UK GDPR, CCPA/CPRA, HIPAA, LGPD, PIPL...), the ePrivacy Directive text, the AI Act,
the Data Act, adequacy decisions, the text of Standard Contractual Clauses, or any news/events."""

# --------------------------------------------------------------------------------------------------
# Question styles (planner assigns one per item for diversity)
# --------------------------------------------------------------------------------------------------
STYLES: dict[str, str] = {
    "factual": "A precise factual question about a rule, threshold, deadline, number, list of elements or condition. "
               "Example: 'Within what time limit must a controller notify a personal data breach to the supervisory authority?'",
    "definitional": "Asks what a legal concept means or what its constituent elements are. "
                    "Example: 'What conditions must be met for consent to be considered freely given under the GDPR?'",
    "procedural": "Asks how something must be done, in what steps or form. "
                  "Example: 'How should a controller verify the identity of a data subject making an access request?'",
    "conditional": "Asks when / in which circumstances an obligation applies or does not apply. "
                   "Example: 'When is a controller exempt from communicating a data breach to affected individuals?'",
    "scenario": "A short, realistic practitioner scenario (1-2 sentences, concrete but generic actors such as "
                "'an online retailer', 'a hospital', 'a SaaS provider') followed by a question whose answer is "
                "determined by the context. Example: 'A fitness app based outside the EU offers its service in German "
                "and charges in euros. Does the GDPR apply to its processing of EU users' data?'",
    "exception": "Asks about an exception, limitation, restriction or derogation to a general rule. "
                 "Example: 'In which cases may a controller refuse to act on a request for access to personal data?'",
    "responsibility": "Asks WHO bears an obligation or role (controller, processor, joint controllers, DPO, supervisory "
                      "authority, representative) and what that party must do. "
                      "Example: 'What must a processor do when it becomes aware of a personal data breach?'",
}

# --------------------------------------------------------------------------------------------------
# Generation: single-chunk
# --------------------------------------------------------------------------------------------------
GEN_SYSTEM = f"""\
You are an expert EU data-protection lawyer helping build a GOLDEN EVALUATION SET for a retrieval-augmented
question-answering assistant about the GDPR. The assistant's users are DPOs, privacy counsel, compliance officers and
engineers. Each golden item is a (question, reference answer, evidence) triple used to measure:
  1. retrieval quality: does the system retrieve the passage(s) the question was written from?
  2. answer quality: is the system's answer correct, complete and faithful to the sources?

{CORPUS}

RULES FOR THE QUESTION
  - It must be fully and unambiguously answerable from the CONTEXT you are given, and the context must be the
    natural place to find the answer.
  - Write it the way a real practitioner would type it into a search box or ask a colleague: natural wording,
    one clear information need, 12-40 words. Do not paste long phrases from the context; paraphrase, so the
    question tests semantic retrieval rather than keyword matching. Keep the key legal terms (e.g. 'joint
    controllers', 'legitimate interest', 'DPIA') since users would use them.
  - It must be SELF-CONTAINED. Never refer to 'the passage', 'the text', 'this document', 'the above', 'these
    guidelines', 'the example', 'paragraph 34', 'Example 3' or anything else the user cannot see. If the answer is
    specific to a guideline, name the subject matter (e.g. 'According to the EDPB guidance on consent, ...').
  - Ask about SUBSTANCE: obligations, conditions, definitions, criteria, deadlines, exceptions, roles, consequences.
    Never ask about document structure, page numbers, footnotes, version history, adoption dates, authors,
    publication details, or the table of contents.
  - Avoid yes/no questions unless the scenario style needs one; if so, the answer must also explain why.
  - Do not ask questions whose answer is a matter of opinion or needs information outside the context.

RULES FOR THE REFERENCE ANSWER
  - 1-4 sentences, precise and complete, written as an expert would answer the user directly.
  - Use ONLY facts stated in the context. Do not add general GDPR knowledge, even if correct.
  - Cite the GDPR article / recital / guideline paragraph where the context makes it identifiable (e.g. 'Art. 33(1)').

RULES FOR EVIDENCE
  - 'evidence' is a list of 1-3 short quotes (each 5-40 words) copied VERBATIM, character for character, from the
    context, that together support the answer. Do not fix typos, do not ellipsize, do not merge sentences.

WHEN TO SKIP
  - Set 'skip' to true (with empty question/answer/evidence) if the context is a table of contents, list of
    references, bibliography, header/footer residue, a bare heading, a list of member state names, or otherwise has
    no substantive content worth asking about. It is better to skip than to produce a weak question.

Respond with a single JSON object matching the schema. No prose outside JSON."""

SINGLE_USER = """\
SOURCE DOCUMENT: {title}
SECTION: {section}

CONTEXT:
\"\"\"
{context}
\"\"\"

REQUIRED QUESTION STYLE: {style_name}: {style_desc}
TARGET DIFFICULTY: {difficulty}
  (easy = answer stated in one sentence; medium = requires reading a full paragraph or combining two statements;
   hard = requires applying a condition/criterion or reasoning over several statements in the context)

If the required style does not fit this context at all, use the closest style that does and report it in
'question_style'. Produce one golden item now."""

# --------------------------------------------------------------------------------------------------
# Generation: multi-chunk
# --------------------------------------------------------------------------------------------------
MULTI_USER = """\
You are given {n} passages from the knowledge base. Write ONE question that genuinely REQUIRES information from at
least two of them: a correct, complete answer must be impossible from any single passage alone.

Good multi-passage question patterns:
  - a rule in one passage + its exception/condition/clarification in another
  - a GDPR article + how EDPB/WP29 guidance interprets or applies it
  - comparing two obligations, roles, lawful bases or procedures (similarities/differences)
  - a scenario whose resolution needs a criterion from one passage and a consequence from another
Bad patterns (do NOT do these): two unrelated sub-questions glued with 'and'; a question answered fully by one
passage with a trivial detail from another; 'What do passages 1 and 2 say about...'.

{context}

REQUIRED QUESTION STYLE: {style_name}: {style_desc}

Additional rules for this item:
  - 'evidence' must contain at least one verbatim quote from EACH passage you rely on (2-4 quotes total).
  - 'passages_used' lists the passage numbers (e.g. [1, 2]) the answer needs.
  - If the passages share no meaningful connection that supports such a question, set 'skip' to true.
Produce one golden item now."""

# --------------------------------------------------------------------------------------------------
# Generation: unanswerable
# --------------------------------------------------------------------------------------------------
UNANS_SYSTEM = f"""\
You are an expert EU data-protection lawyer building the NEGATIVE part of a golden evaluation set for a GDPR
retrieval-augmented assistant. These questions test whether the assistant correctly says it cannot answer from its
sources instead of hallucinating.

{CORPUS}

Write questions that:
  - sound realistic and closely RELATED to the topic hint, so retrieval will surface plausible-but-insufficient
    passages (this is what makes them a good test);
  - CANNOT be answered from the knowledge base at all. Good sources of such questions: a different legal regime
    (UK GDPR post-Brexit changes, CCPA/CPRA, HIPAA, Brazil's LGPD, a member state's implementing act such as the
    German BDSG), a specific named company, court case or DPA decision, a precise fine imposed on a real company,
    events or guidelines after the corpus date, the ePrivacy Directive or AI Act provisions, the text of
    Standard Contractual Clauses, or concrete operational/technical detail no guideline specifies (exact
    encryption key lengths, specific vendor tools, etc.);
  - are self-contained, 12-40 words, and NOT trick questions with a false premise about the GDPR itself.
Avoid questions that the GDPR or the listed guidelines DO answer in general terms; e.g. 'What is the maximum GDPR
fine?' is answerable and therefore wrong for this task.

Return JSON: 'question', 'answer' = one sentence explaining why the knowledge base cannot answer it,
'question_style' = 'unanswerable', 'difficulty' = 'medium', 'evidence' = [], 'skip' = false."""

UNANS_USER = """\
TOPIC HINT (an area the knowledge base covers):
  Document: {title}
  Section: {section}
  Excerpt (for topical orientation only, do NOT ask something this excerpt answers):
  \"\"\"{excerpt}\"\"\"

OUT-OF-SCOPE ANGLE TO USE: {angle}

Produce one unanswerable golden item now."""

UNANS_ANGLES = [
    "a non-EU or post-Brexit legal regime (UK GDPR, CCPA/CPRA, HIPAA, LGPD, PIPL, Swiss FADP)",
    "a member state's national implementing law or national DPA's specific practice",
    "a specific named company, court judgment (e.g. a CJEU case by name) or DPA enforcement decision",
    "the exact amount of a real fine or the outcome of a real investigation",
    "a neighbouring EU instrument not in the corpus (ePrivacy Directive, AI Act, Data Act, NIS2, DSA)",
    "a concrete technical or vendor-level implementation detail no guideline prescribes",
    "the content of Standard Contractual Clauses, an adequacy decision or the EU-US Data Privacy Framework",
]

# --------------------------------------------------------------------------------------------------
# Judging
# --------------------------------------------------------------------------------------------------
JUDGE_SYSTEM = f"""\
You are a meticulous senior reviewer auditing items of a golden evaluation set for a GDPR retrieval-augmented
assistant. Bad items silently corrupt every metric computed on the set, so be strict: when in doubt, reject.

{CORPUS}

Respond with a single JSON object matching the schema. Keep 'reason' to one or two sentences."""

JUDGE_ANSWERABLE_USER = """\
CONTEXT THE ITEM WAS WRITTEN FROM:
{context}

ITEM
  type: {kind}
  question: {question}
  reference answer: {answer}

Evaluate each criterion independently:
  self_contained  - true if a user who has NOT seen the context would understand exactly what is asked.
                    false if it refers to 'the passage/text/document/example/guidelines above', a numbered example
                    or paragraph, or depends on unstated context.
  grounded        - true if EVERY claim in the reference answer is supported by the context, and the answer
                    actually and completely answers the question. false if it adds outside facts, is wrong, partial,
                    or answers a different question.
  non_trivial     - true if it asks about legal substance a practitioner would care about. false for questions about
                    document metadata, structure, page/paragraph numbers, adoption dates, or trivial word lookups.
  unambiguous     - true if there is one clearly correct answer. false if the question is vague, overly broad, or
                    reasonable experts would answer it differently based on the context.
  {multi_criterion}
  quality         - overall 1-5: 5 = excellent realistic practitioner question with crisp grounded answer;
                    3 = acceptable; 1-2 = should not be in a golden set."""

JUDGE_MULTI_CRITERION = ("requires_multiple - true if a complete answer genuinely needs information from more than one "
                         "passage; false if one passage alone suffices.")
JUDGE_SINGLE_CRITERION = "requires_multiple - always true for single-passage items."

JUDGE_UNANSWERABLE_USER = """\
TOPIC EXCERPT FROM THE KNOWLEDGE BASE (the closest material a retriever is likely to return):
{context}

ITEM (intended to be UNANSWERABLE from the knowledge base)
  question: {question}
  why out of scope: {answer}

Evaluate:
  self_contained   - true if the question is clear on its own.
  grounded         - here this means 'correctly unanswerable': true ONLY if neither the excerpt NOR any document
                     listed in the knowledge base description would let an assistant answer it. false if the GDPR
                     or the listed guidelines answer it, even in general terms.
  non_trivial      - true if it is a realistic question a practitioner might actually ask this assistant.
  unambiguous      - true if it is a single clear question (not a false-premise trick about the GDPR).
  requires_multiple - always true for this item type.
  quality          - overall 1-5 usefulness as a negative test (5 = topically very close yet truly unanswerable)."""

# --------------------------------------------------------------------------------------------------
# JSON schemas (Workers AI JSON mode)
# --------------------------------------------------------------------------------------------------
QA_SCHEMA = {"name": "golden_item", "schema": {
    "type": "object",
    "required": ["skip", "question", "answer", "evidence", "question_style", "difficulty"],
    "properties": {
        "skip": {"type": "boolean"},
        "question": {"type": "string"},
        "answer": {"type": "string"},
        "evidence": {"type": "array", "items": {"type": "string"}},
        "question_style": {"type": "string", "enum": [*STYLES, "unanswerable"]},
        "difficulty": {"type": "string", "enum": ["easy", "medium", "hard"]},
        "passages_used": {"type": "array", "items": {"type": "integer"}},
    }}}

JUDGE_SCHEMA = {"name": "judgement", "schema": {
    "type": "object",
    "required": ["self_contained", "grounded", "non_trivial", "unambiguous", "requires_multiple", "quality", "reason"],
    "properties": {
        "self_contained": {"type": "boolean"},
        "grounded": {"type": "boolean"},
        "non_trivial": {"type": "boolean"},
        "unambiguous": {"type": "boolean"},
        "requires_multiple": {"type": "boolean"},
        "quality": {"type": "integer", "minimum": 1, "maximum": 5},
        "reason": {"type": "string"},
    }}}

MIN_QUALITY = 3
