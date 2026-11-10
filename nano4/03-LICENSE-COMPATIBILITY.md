# LICENSE-COMPATIBILITY.md — method and initial classification

**Status:** working method; no combined-work compatibility has been certified.

## 1. Do not compare labels alone

For each component, record its exact licence/instrument name, version, text hash, rights holder, jurisdiction if material, covered material, modification state, distribution model, patent terms, attribution/notice duties, source-disclosure duties, trademark restrictions, data/database rights, and third-party exclusions.

## 2. Separate the legal objects

| Family / example | What it generally governs | What must be checked |
|---|---|---|
| Permissive software licences (MIT, BSD, Apache-2.0) | Copyright permissions; Apache-2.0 also contains express patent terms | Exact licence version, notices, patent grants/termination, trademarks, third-party files |
| Copyleft software licences (GPL, AGPL, LGPL) | Conditions on conveying/combining/modifying covered software | Exact version, linking/combination facts, source obligations, network interaction, compatibility clauses |
| Creative Commons licences | Copyright and related rights for eligible works; not a general software licence | Exact CC version, BY/SA/NC/ND conditions, database rights, attribution and adaptations |
| Public-domain tools (CC0, jurisdictional public-domain status, Unlicense) | Different mechanisms intended to waive or license rights to the extent permitted | Local legal effect, fallback licence, moral rights, third-party rights; do not assume all tools are identical |
| Patent grants / FRAND terms | Patent rights and conditions | Patent claims, essentiality, scope, reciprocity, termination and jurisdiction |
| Trademark permissions | Use of names, logos, marks, branding | Mark owner, goods/services, quality control, nominative use and territory |
| Privacy and data-protection law (e.g. GDPR) | Processing of personal data and legal duties, not a copyright licence | Controller/processor roles, legal basis, purpose, minimisation, retention, rights and security |
| Trade-secret / confidentiality terms | Non-public information and duties of confidence | What is secret, reasonable protection, exclusions, permitted disclosures and duration |
| Government / procurement / export-control terms | Public-sector contract duties or regulated transfer/use | Specific contract, legislation, controlled item, destination, user and authorisation |
| Sector/use categories (dual-use, games, sacred works, collective works) | Context or risk category, not necessarily a licence family | The underlying rights instrument and sector-specific law |

## 3. Compatibility decision states

Use `COMPATIBLE`, `INCOMPATIBLE`, `CONDITIONALLY_COMPATIBLE`, `NOT_APPLICABLE`, or `UNVERIFIED`. Every decision cites the exact source texts, versions, clauses, combination facts, and reviewer. Never infer compatibility from an acronym or from a broad category.

## 4. VBL-specific review

VBL is a proposed bespoke licence with unusual attribution, machine-use, cure, ethics, and versioning provisions. Do not assume it is OSI-approved, OSI-compliant, OSI-compatible, legally enforceable, or compatible with GPL/Apache/CC from the name alone. Before deployment, decide whether the specific work is better served by a standard recognised licence plus a separate ethical policy or covenant. Preserve the user's VBL principles independently from the legal instrument selected.

## 5. Sources for legal review

- Slovenian Government overview of copyright and related rights: https://www.gov.si/en/topics/copyright-and-related-rights/
- Directive (EU) 2019/790, including TDM Articles 3 and 4: https://eur-lex.europa.eu/eli/dir/2019/790/oj
- GNU GPL version 3, section 8 on termination and reinstatement: https://www.gnu.org/licenses/gpl-3.0.en.html
- Directive (EU) 2019/882 on accessibility requirements: https://eur-lex.europa.eu/eli/dir/2019/882/oj

These are research starting points, not a legal opinion on VBL. Verify current consolidated national law and the exact licence texts before release.
