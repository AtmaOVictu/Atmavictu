# ACCESSIBILITY.md — VBL accessibility specification

**Status:** implementation specification; not a legal compliance certificate.  
**Applies to:** the VBL body, its companions, registers, machine records, examples, audio/video, and distribution interfaces.

## 1. Core rule

Accessibility is part of faithful delivery, not a separate favour. A person is not excluded from the agreement because a format, channel, or sensory modality is unavailable to them. Provide equivalent access to the information and interaction wherever practicable, while documenting any content or interaction that cannot yet be made equivalent.

## 2. Text and structure

- Use semantic headings in a logical hierarchy; do not simulate headings only with bold text.
- Use descriptive link text, meaningful table headers, and lists that preserve reading order.
- Provide a plain-text and Markdown edition alongside rendered formats.
- Keep document language and language changes programmatically identifiable where the format supports it.
- Do not convey status by colour alone. Spell out `PASS`, `FAIL`, `UNVERIFIED`, `NOT_APPLICABLE`, and `NOT_CONFIGURED`.
- Ensure keyboard access, visible focus, predictable navigation, and no keyboard traps in interactive interfaces.
- Support reflow and text enlargement without loss of essential content.

## 3. Blind and low-vision access

- Provide text alternatives for informative images, charts, diagrams, and controls.
- Provide accessible mathematical notation with a linear reading and, where feasible, MathML or another screen-reader-compatible representation.
- Define every symbolic mark at first use and provide a machine-readable glossary.
- Offer high-contrast and scalable text options; never rely on visual position alone to communicate sequence or status.
- Test with at least one screen reader and keyboard-only navigation; name the software, version, platform, test scope, and limitations.
- Where Braille output is relevant, provide structured source text and document tested refreshable-Braille compatibility rather than asserting universal Braille support.

## 4. Deaf and hard-of-hearing access

- Provide accurate captions for speech and meaningful non-speech audio in audiovisual content.
- Provide a transcript for audio-only material.
- Do not use sound as the only notification or confirmation channel; provide visual and text equivalents.
- Where signed-language editions are produced, identify the sign language (not merely “sign language”), region/variant where relevant, translator, reviewer, source version, and any known omissions.
- Do not claim that a written transcript is equivalent to a signed-language translation.

## 5. Cognitive, language, and motor access

- Provide a plain-language guide that does not replace the legal text.
- Expand acronyms and define technical terms in a glossary.
- Keep instructions atomic and clearly ordered; provide error messages that identify the problem and a recovery path.
- Avoid time limits unless essential; permit users to pause and resume where possible.
- Ensure controls have accessible names, states, and keyboard operation.
- Provide translations with a source-version ID and documented review; do not silently substitute a machine translation for an approved legal translation.

## 6. Translation governance

Each translation record includes: `translation_id`, `source_version`, `source_sha256`, `target_language`, `format`, `translator`, `reviewer`, `created_at`, `reviewed_at`, `known_omissions`, `semantic_status`, and `sha256`. A translation is labelled `DRAFT`, `REVIEWED`, or `UNVERIFIED`. The governing-language clause, if any, must be stated explicitly and must not erase the value of other-language access.

## 7. Acceptance tests

A release candidate should test:

1. keyboard-only completion of every essential action;
2. screen-reader access to headings, links, tables, status, and math;
3. reflow at narrow viewport widths and enlarged text;
4. captions/transcripts for every published audio/video item;
5. no colour-only distinction;
6. language tagging and preservation of Č, Š, Ž, Đ and other script-specific characters;
7. translated sections linked to the exact source version;
8. a report listing failed, untested, and not-applicable checks.

Passing these tests is evidence for the tested scope only. It does not certify conformance to every applicable accessibility law or standard.
