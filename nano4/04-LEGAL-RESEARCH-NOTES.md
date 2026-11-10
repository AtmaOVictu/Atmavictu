# Legal research notes for the VBL 0.1470 proposal

**Checked:** 5 November 2026  
**Scope:** public Slovenian and EU sources; issue-spotting only, not legal advice.

## 1. Slovenian copyright and rights provenance

The Slovenian Government's copyright overview states that copyright arises by creation without a registration formality; it distinguishes moral and economic interests and notes that authorship under Slovenian law belongs to a natural person. It also explains that co-authors can hold joint rights where a collaborative work is an inseparable whole, and that the author is assessed case by case. This supports the patch to §0a: a file path and hash identify bytes, but they do not establish authorship, ownership, consent, authority to license, or third-party permissions. A registry deposit may preserve evidence but does not create the rights.

The Slovenian Government page also distinguishes ideas/principles from protectable expression and lists examples of material forms, non-material forms, and modified forms of exploitation. The VBL scope clause should therefore avoid claiming that general ideas, facts, methods, or functionality become licensed expression merely because they are in the same repository or system.

Sources:
- GOV.SI, “Copyright and related rights” (last edited 25 November 2025): https://www.gov.si/en/topics/copyright-and-related-rights/
- PISRS, ZASP consolidated text page: https://pisrs.si/Pis.web/pregledPredpisa?id=ZAKO4148

## 2. Text and data mining is not a single universal right

Directive (EU) 2019/790 Article 3 concerns text and data mining for scientific research by research organisations and cultural heritage institutions with lawful access, including secure retention for research verification. Article 4 provides a separate text-and-data-mining exception for lawfully accessible works and other subject matter, subject to the rightsholder not having expressly reserved the relevant rights in an appropriate manner; the Directive mentions machine-readable reservation for publicly available online content. National implementation and the precise scope matter.

Therefore VBL §0.3 should not assert that a private licence clause automatically overrides every statutory text-and-data-mining exception or lawful use. It may express a reservation where legally effective and appropriately communicated, but the exact reservation mechanism and consequences need Slovenian/EU counsel review and a machine-readable implementation if relied upon.

Sources:
- Directive (EU) 2019/790, Article 3: https://www.legislation.gov.uk/eudr/2019/790/article/3?view=plain
- Directive (EU) 2019/790, Article 4: https://www.legislation.gov.uk/eudr/2019/790/article/4?view=plain
- EUR-Lex consolidated act: https://eur-lex.europa.eu/eli/dir/2019/790/oj

## 3. Termination and cure: do not claim equivalence with GPL

GPLv3 Section 8 has a specific termination and reinstatement structure, including provisional reinstatement when violations cease and permanent reinstatement under defined notice conditions. It also has a first-notice cure path. VBL's fixed thirty-day cure mechanism is different in wording and structure. Do not call it “the GPL cure”, claim GPL equivalence, or infer compatibility from the shared idea of cure.

Sources:
- GNU GPLv3, official text: https://www.gnu.org/licenses/gpl-3.0.en.html
- Open Source Initiative GPL-3.0 licence page: https://opensource.org/license/GPL-3.0

## 4. Accessibility in Slovenia: current statute and scope

PISRS lists the Slovenian ZDPSI with amendments published in Official Gazette 14/26, and says it applies from 28 June 2025. The consolidated information describes covered product and service categories and general accessibility requirements. Its application is scoped; it should not be represented as applying automatically to every private licence text or every file in a repository. Assess the actual product/service, provider, user group, exceptions, and national requirements.

The accessibility companion in this package is a technical and ethical baseline. It is not a certificate of compliance with ZDPSI, Directive (EU) 2019/882, or WCAG. Where a VBL implementation is a covered product or service, perform a separate legal and technical conformity assessment against the applicable current requirements.

Sources:
- PISRS, ZDPSI consolidated information, including 2026 amendment: https://pisrs.si/pregledPredpisa?sop=2023-01-0238
- Official Gazette RS 14/2026, ZDPSI-A: https://pisrs.si/api/uradni-list/objava/u2026014.pdf
- Directive (EU) 2019/882: https://eur-lex.europa.eu/eli/dir/2019/882/oj

## 5. Practical legal boundary

This research does not determine whether VBL is enforceable, whether its terms form a valid contract in a particular transaction, whether every proposed restriction is effective, or whether the chosen work is better licensed under VBL or a standard licence. Before publication, obtain a review of the exact final text under Slovenian law and the laws relevant to intended distribution, including copyright, contract, consumer, data-protection, accessibility, and any applicable patent/trademark issues.
