# AuditGDPR

RAG application over a curated GDPR regulatory corpus.

## Data corpus (`data/`)

17 PDFs, grouped by topic. Naming convention:
`<publisher>_<doc-type>_<number>-<year>_<topic>_<version>.pdf`
(`edpb_guidelines_*` = European Data Protection Board; `wp29_*` = legacy Article 29 Working Party, endorsed by EDPB).
Only final/adopted versions are included, except where noted.

### `01_base_law/`
| File | Content |
|---|---|
| `gdpr_regulation_2016-679.pdf` | The GDPR itself (Regulation (EU) 2016/679): all recitals and Articles 1-99. The primary source of law. |

### `02_edpb_scope_and_roles/`
| File | Content |
|---|---|
| `edpb_guidelines_03-2018_territorial_scope_art3_v2.0.pdf` | When the GDPR applies: establishment in the EU, targeting EU individuals, non-EU controllers/processors, and the EU representative requirement (Art. 3). |
| `edpb_guidelines_07-2020_controller_processor_v2.1.pdf` | How to tell controller, joint controller, processor and sub-processor apart, and their obligations and contracts (Art. 4(7)-(8), 26, 28). |

### `03_edpb_lawful_bases/`
| File | Content |
|---|---|
| `edpb_guidelines_05-2020_consent_v1.1.pdf` | Valid consent: freely given, specific, informed, unambiguous, withdrawal, children, cookie walls (Art. 4(11), 6(1)(a), 7). |
| `edpb_guidelines_02-2019_contract_art6-1-b_online_services_v2.0.pdf` | Using "necessary for a contract" as a lawful basis, specifically for online services (Art. 6(1)(b)). |
| `edpb_guidelines_01-2024_legitimate_interests_art6-1-f_v2.0.pdf` | Legitimate interests: the three-step test (interest, necessity, balancing) (Art. 6(1)(f)). Version 2.0, adopted 10 Nov 2026. |

### `04_edpb_rights_and_security/`
| File | Content |
|---|---|
| `edpb_guidelines_01-2022_right_of_access_v2.1.pdf` | Right of access: scope, how to respond to requests, limits and refusals (Art. 15). |
| `edpb_guidelines_04-2019_data_protection_by_design_and_default_v2.0.pdf` | Data protection by design and by default: principles, technical and organisational measures (Art. 25). |
| `edpb_guidelines_09-2022_breach_notification_v2.0.pdf` | Personal data breach notification: when and how to notify the authority and individuals, the 72-hour rule (Art. 33-34). |
| `edpb_guidelines_01-2021_breach_notification_examples_v2.0.pdf` | Practical breach scenarios (ransomware, exfiltration, human error, etc.) with notification and mitigation advice. |
| `edpb_guidelines_01-2025_pseudonymisation_v1.0_consultation.pdf` | Pseudonymisation as a safeguard, and when pseudonymised data is still personal data (Art. 4(5), 25, 32). **v1.0 is the consultation draft**; no final version is published on the EDPB page. |

### `05_edpb_transfers_and_fines/`
| File | Content |
|---|---|
| `edpb_guidelines_05-2021_art3_chapter_v_transfers_interplay_v2.0.pdf` | When a disclosure counts as an international transfer, and how Art. 3 interacts with Chapter V (Art. 44-46). |
| `edpb_guidelines_04-2022_administrative_fines_calculation_v2.1.pdf` | The EDPB's methodology for calculating administrative fines (Art. 83). |

### `06_wp29_legacy/`
Pre-GDPR working party guidelines that the EDPB endorsed. All are the revised (`rev.01`) final versions.

| File | Content |
|---|---|
| `wp29_wp260rev01_transparency.pdf` | Transparency obligations: what to tell data subjects and how (Art. 12-14). |
| `wp29_wp248rev01_dpia.pdf` | Data Protection Impact Assessments: when one is required and how to carry it out (Art. 35). |
| `wp29_wp243rev01_dpo.pdf` | Data Protection Officers: when to appoint one, their role, independence and tasks (Art. 37-39). |
| `wp29_wp251rev01_automated_decisions_profiling.pdf` | Automated individual decision-making and profiling (Art. 22). |
| `wp29_wp242rev01_data_portability.pdf` | The right to data portability (Art. 20). |

### Not included
The two plain-English HTML guides (European Commission business guidance and the EDPB SME guide) are web pages, not PDFs, so they are not in `data/`.
