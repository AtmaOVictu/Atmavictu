# Architecture and fit-for-purpose licence selection

**STATUS: PROPOSAL ONLY. Author approval and legal review required before adoption.**

## 1. Separate four layers

### A. Legal licence

Contains only legally operative rights and conditions: subject matter, rights-holder authority, scope of grant, attribution, modification notices, distribution, termination, cure, warranty, liability, governing-law provisions if selected, third-party exclusions, and patent/trademark treatment.

### B. VBL protocol

Contains verifiable operational procedures: manifests, hashes, timestamps, event records, append-only registers, test definitions, review roles, reproducible builds, and release evidence.

### C. Ethical charter

Contains commitments about dignity, non-degradation, accountability, repair, proportionality, and the right to challenge. A charter is not automatically an enforceable licence condition. Where a rule is intended to have legal effect, it must be deliberately placed in the legal instrument and reviewed for clarity, compatibility, and enforceability.

### D. Accessibility and language

Contains accessible formats, translations, captions, transcripts, sign-language versions, screen-reader support, Braille-ready text, plain-language explanations, and translation-review records. Each version states whether it is legally authoritative or explanatory.

A change in B, C, or D must not silently rewrite the legal grant in A. Each layer has its own version, date, source, and evidence record.

## 2. Licensing policy by material type

The correct licence depends on the asset and the outcome sought. Do not apply VBL automatically to every file.

| Material | Provisional default to evaluate | Choose a different route when |
|---|---|---|
| Software and executable code | Apache-2.0 where broad reuse, attribution notices, change notices, and an express contributor patent grant are desirable | Choose GPL-3.0-or-later when reciprocal sharing of distributed derivative software is the priority; evaluate AGPL for network-service source-sharing goals |
| Documentation, essays, diagrams, audio and other authored media | CC BY 4.0 where broad reuse with attribution and change marking is desired | Choose CC BY-SA 4.0 when share-alike is a real requirement; choose a noncommercial licence only when that restriction is intentional and its effect on reuse is accepted |
| Data and databases | Decide only after provenance, database rights, privacy, confidentiality, and third-party terms are audited | A data-specific licence may be needed; do not treat personal data as freely licensable merely because a dataset is in a repository |
| VBL protocol specification | CC BY 4.0 is a practical candidate for a freely reusable specification; the implementation receives its own software licence | A custom restrictive use condition means it should not be represented as ordinary open content or open-source software without a formal compatibility assessment |
| Ethical charter | Publish separately, preferably under a clear text licence; state whether it is aspirational, contractual, or incorporated by reference into a signed agreement | If enforceability is intended, obtain jurisdiction-specific legal review and define scope, procedure, remedies, and conflicts |

Apache-2.0 expressly grants broad copyright permissions and a defined contributor patent licence, and requires preservation of licence/attribution notices and prominent change notices. The Apache Software Foundation warns that substantively changing its text creates a different licence, not Apache-2.0. See the [Apache licence text](https://www.apache.org/licenses/LICENSE-2.0.html) and [ASF licence FAQ](https://apache.googlesource.com/www-site/%2B/e26295ca9a46d1da6280f3646830914b20075615/content/foundation/license-faq.md).

CC BY 4.0 requires attribution and retention of supplied notices, and requires indicating modifications. CC BY 4.0 is not a substitute for a software licence. See the [CC BY 4.0 legal code](https://creativecommons.org/licenses/by/4.0/legalcode). GPL-3.0 has reciprocal source-distribution requirements and a structured reinstatement mechanism after certain violations are cured; see the [GPL-3.0 text](https://www.gnu.org/licenses/gpl-3.0.en.html).

The Open Source Definition prohibits discrimination against persons/groups and against fields of endeavour. A field-of-use or ethical restriction can therefore make a custom licence incompatible with the ordinary open-source definition. Do not claim OSI approval or open-source status without formal confirmation. See the [Open Source Definition](https://opensource.org/osd).

For a custom licence not listed in SPDX, use an honest project-specific identifier such as `LicenseRef-VBL-<version>` where the relevant tooling supports it. This identifies a custom licence; it does not certify legal validity, OSI approval, or compatibility.

## 3. One decision must be made before each release

For every asset group, record:

1. What is the asset? Code, documentation, media, data, protocol, or charter.
2. Who owns or controls each relevant right?
3. What reuse is intended: commercial, non-commercial, modification, redistribution, model training, public display, or network use?
4. Is reciprocity required?
5. Is a patent grant needed?
6. Are there third-party, privacy, confidentiality, personality, database, or trademark rights?
7. Which standard licence is the closest fit?
8. What exact additional legal restriction is genuinely needed, and what compatibility does it sacrifice?

Do not combine unrelated assets under a single custom licence merely for visual or philosophical unity.

## 4. AI-use policy must be explicit per asset

The protocol should record, rather than infer, separate decisions for:

- training;
- fine-tuning;
- evaluation and benchmarking;
- retrieval and indexing;
- inference-time input processing;
- redistribution of the source material;
- outputs reproducing protected expression;
- commercial exploitation.

Allowed values: `PERMITTED`, `PROHIBITED`, `PERMISSION_REQUIRED`, `NOT_APPLICABLE`, `UNDECIDED`.

If the field is `UNDECIDED`, the release must not claim that VBL grants a special AI permission or restriction. Apply the actual selected legal licence and applicable law. Attribution does not by itself answer every question about training, privacy, database rights, or generated outputs.
