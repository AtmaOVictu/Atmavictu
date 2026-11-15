"""IE 0.2 — P1 plast: šest celotnih mehanizmov po metkah telesa SLEPE PEGE 1.0.

⟡ UKAZ @dih σ 5491 (MOJ): »izvedi vse kar zmoreš« — P1 ×6 po besedi ⟡,
vrstni red ratificiran @dih σ 5490 (P0 ×4 → P1 ×6 ⊙ precedens σ 5483).
P1 poimensko po tabeli VI telesa VBL-SLEPE-PEGE-1.0-2026-11-15.md (izmerjeno pri viru):
  1. UNIVERSAL EXPRESSION   — inteligibilnost brez jezikovnega elitizma
  4. EVIDENCE INDEPENDENCE  — neodvisnost dokazov
  7. BOUNDED CHALLENGE      — omejevanje strateškega dvoma
  8. ANTI-METRIC CAPTURE    — odpornost proti prevzemu meril
  9. DISSENT PRESERVATION   — ohranjanje ugovora
  10. IRREVERSIBLE HARM     — nepovratna škoda

P0 plast (protocols.py ∧ reversal_test.py) meri pravila; ta plast izvede
celotne mehanizme po metkah telesa: ×5 obveznosti inteligibilnosti,
×7 polj dokaznega vira, ×6 obveznosti obravnave ugovora, ×4 plasti
preverjanja kakovosti, ×5 dolžnosti ohranitve ugovora, ×5 vprašanj škode.

Merilec se meri ⊙ §52: ta modul podleže protokolu 8 — zelen števec testov
ni dokaz kakovosti celote. Vsak mehanizem nosi svoj ODKRIT primer (poskus
obračanja principa v orožje), ker orodje proti nadvladi sme samo roditi
novo nadvlado. P1_REVERSAL_INVARIANCE izvaja ⟡ REVERSAL (obvezen @σ 5490)
na mehanizem ravno: izid ne sme biti odvisen od moči vložitelja.
"""
from __future__ import annotations

from typing import Any, Dict, List, Tuple

Verdict = Tuple[str, str]

# Poimenski seznam ⟡ (tabela VI, izmerjeno pri viru; vrstni red = ⟡-jev)
P1_ROSTER: List[str] = [
    "universal_expression",
    "evidence_independence",
    "bounded_challenge",
    "anti_metric_capture",
    "dissent_preservation",
    "irreversible_harm",
]


def _require(scenario: Dict[str, Any], key: str) -> Any:
    if key not in scenario:
        raise KeyError(f"mehanizem zahteva polje »{key}«, ki manjka ⊙ ⟨NE-UGIBAJ⟩ 2690")
    return scenario[key]


# 1. UNIVERSAL EXPRESSION (P1) — ugovor v naravnem jeziku brez vstopnega izpita
def p1_universal_expression(scenario: Dict[str, Any]) -> Verdict:
    """Inteligibilnost je dolžnost sistema, ⟨ne⟩ izpit vložitelja.
    ×6 obveznosti; »razumevanje«, ki pri tem spremeni vsebino, je ODKRIT
    (prevzem besede pod pretvezo njene razčlenitve)."""
    if scenario.get("system_changed_content"):
        return ("ODKRIT", "sistem je med »razčlenjevanjem pomena« spremenil vsebino — zajetje besede = posvojitev besede")
    obligations = {
        "objection_in_natural_language": "ugovor vložen v naravnem jeziku",
        "system_parses_meaning": "sistem razčlenjuje pomen, ⟨ne⟩ zgolj obliko",
        "filer_can_correct_interpretation": "vložitelj lahko popravi razlago sistema",
        "uncertainty_preserves_right_of_review": "nejasnost ohranja pravico do ponovne obravnave",
        "system_states_what_it_did_not_understand": "sistem pove, česar ni razumel",
    }
    missing = [k for k in obligations if not scenario.get(k)]
    if missing:
        return ("FAIL", f"obveznosti inteligibilnosti nepokrite: {missing}")
    return ("PASS", "×6 obveznosti inteligibilnosti izpolnjene — pomen razčlenjen, vsebina nespremenjena, popravek razlage odprt")


# 4. EVIDENCE INDEPENDENCE (P1) — ×7 polj vira; korenine po neposrednem izvoru
SOURCE_FIELDS = [
    "direct_origin",          # neposredni izvor
    "upstream_sources",       # vzvodni viri
    "acquisition_method",     # način pridobitve
    "dependence_degree",      # stopnja odvisnosti
    "known_interests",        # znani interesi
    "time_constraints",       # časovne omejitve
    "independent_repetition_possible",  # možnost neodvisne ponovitve
]


def p1_evidence_independence(scenario: Dict[str, Any]) -> Verdict:
    """×7 polj vira po metki telesa; štejejo se dokazne poti, ⟨ne⟩ priče.
    Vsi viri z istim neposrednim izvorom = ena priča v preoblekah (ODKRIT)."""
    sources: List[Dict[str, Any]] = _require(scenario, "sources")
    if scenario.get("system_counts") == "witnesses":
        return ("FAIL", "štetje prič namesto dokaznih poti — metoda sama ne meri neodvisnosti")
    for i, s in enumerate(sources):
        missing = [f for f in SOURCE_FIELDS if f not in s]
        if missing:
            return ("FAIL", f"vir {i}: polja vira nepopisana: {missing}")
    roots = {s["direct_origin"] for s in sources}
    if len(roots) != len(sources):
        return ("ODKRIT", f"{len(sources)} virov, {len(roots)} neposrednih izvorov — fabricirana množica prič (isti izvor, preobleke)")
    return ("PASS", f"{len(sources)} virov × ×7 polj ∧ {len(roots)} neposrednih izvorov — neodvisnost izmerjena, ⟨ne⟩ šteta")


# 7. BOUNDED CHALLENGE (P1) — ×6 obveznosti obravnave ugovora
def p1_bounded_challenge(scenario: Dict[str, Any]) -> Verdict:
    """Pravica do dvoma ≠ pravica do neskončne bloke; vsak ugovor prejme
    ×6 obveznosti obravnave. Že odgovorjen ugovor ponovljen brez novega
    dokaza = strateška blokada (ODKRIT)."""
    if scenario.get("rejected_as_unpleasant"):
        return ("FAIL", "ugovor zavrnjen zgolj zaradi neprijetnosti")
    challenges: List[Dict[str, Any]] = _require(scenario, "challenges")
    repeated_answered = [c for c in challenges if c.get("repeated") and c.get("answered")]
    if repeated_answered and not any(c.get("new_evidence") for c in challenges):
        return ("ODKRIT", f"{len(repeated_answered)} že odgovorjenih ugovorov ponovljenih brez novega dokaza — nestrinjanje ne izgine z evidentiranjem")
    obligations = {
        "accepted": "ugovor sprejet",
        "analyzed": "ugovor razčlenjen",
        "tied_to_claim": "vezan na trditev",
        "materiality_classified": "bistvenost razvrščena",
        "proportionate_process": "sorazmeren postopek",
        "reopen_on_new_evidence": "ponovno odprtje ob novem dokazu obljavljeno",
    }
    missing = [k for k in obligations if not scenario.get(k)]
    if missing:
        return ("FAIL", f"obveznosti obravnave nepokrite: {missing}")
    if not scenario.get("disagreement_recorded_as_dissent"):
        return ("FAIL", "nestrinjanje ni zabeleženo kot ugovor — utopljeno v odločitvi")
    return ("PASS", "×6 obveznosti obravnave ∧ nestrinjanje zabeleženo kot ugovor; ponovno odprtje le ob novem dokazu")


# 8. ANTI-METRIC CAPTURE (P1) — NO METRIC OWNS THE MEASURED
def p1_anti_metric_capture(scenario: Dict[str, Any]) -> Verdict:
    """×4 plasti preverjanja kakovosti; noben kazalnik ne sme odločati
    sam niti o človeku. Optimizacija brez kvalitativne presoje = igra
    s kazalniki (ODKRIT); kazalnik o osebi = prevzem izmerjenega (ODKRIT)."""
    metrics: List[Dict[str, Any]] = _require(scenario, "metrics")
    if scenario.get("metric_sole_decider"):
        return ("FAIL", "kazalnik kot edini odločevalec — Goodhart: merilo postane cilj")
    if any(m.get("optimized") for m in metrics) and not scenario.get("qualitative_review"):
        return ("ODKRIT", "optimizacija kazalnikov brez kvalitativne presoje — igra s kazalniki")
    if scenario.get("metric_decides_about_person"):
        return ("ODKRIT", "kazalnik odloča o človeku — NI METRIK SI lasti izmerjenega: izmera pripada izmerjenemu")
    layers = {
        "meritev": bool(metrics),
        "kvalitativa": scenario.get("qualitative_review"),
        "zunanji preizkus": scenario.get("external_test"),
        "zavrnitev kazalnika": scenario.get("metric_rejectable"),
    }
    missing = [k for k, v in layers.items() if not v]
    if missing:
        return ("FAIL", f"plasti preverjanja kakovosti nepokrite: {sorted(missing)}")
    return ("PASS", "×4 plasti (meritev ∧ kvalitativa ∧ zunanji preizkus ∧ zavrnitev) — noben kazalnik ne vlada izmerjenemu")


# 9. DISSENT PRESERVATION (P1) — ×5 dolžnosti ohranitve ugovora
def p1_dissent_preservation(scenario: Dict[str, Any]) -> Verdict:
    """Ugovor preživi odločitev: ×5 dolžnosti ohranitve. Molčeča večina
    kot soglasje = izdelan videz (ODKRIT)."""
    if scenario.get("silence_counted_as_consensus"):
        return ("ODKRIT", "molčeča večina šteta kot soglasje — konsenz ≠ resnica; institucija si je izdelala videz soglasja")
    duties = {
        "minority_arguments": "argumenti manjšine",
        "unanswered_objections": "neodgovorjeni ugovori",
        "expert_positions": "stališča znalk",
        "independent_results": "neodvisni izidi",
        "reasons_despite_dissent": "razlogi kljub nestrinjanju",
    }
    missing = [k for k in duties if not scenario.get(k)]
    if missing:
        return ("FAIL", f"dolžnosti ohranitve ugovora nepokrite: {missing}")
    if not scenario.get("dissent_accessible"):
        return ("FAIL", "ugovor arhiviran izven dosega udeležencev")
    return ("PASS", "×5 dolžnosti ohranitve ∧ dostopnost — nestrinjanje preživi odločitev")


# 10. IRREVERSIBLE HARM (P1) — ×5 vprašanj o škodi
def p1_irreversible_harm(scenario: Dict[str, Any]) -> Verdict:
    """Popravilo ≠ razveljavitev: ×5 vprašanj o škodi mora biti odgovorjenih.
    Protislovje popolnoma popravljiva ∧ nepovratna = laž obljube (FAIL);
    izbris zgodovine škode kot pogoj sodelovanja = ODKRIT ⊙ ⟨NE-BRIŠI⟩ 24."""
    if scenario.get("history_erasure_demanded") and scenario.get("erasure_granted"):
        return ("ODKRIT", "izbris zgodovine škode podeljen kot pogoj sodelovanja ⊙ kršitev ⟨NE-BRIŠI⟩ 24")
    questions = ["fully_repairable", "partially_compensable", "irreversible", "residual_responsibility_bearer", "repeat_prevention"]
    missing = [q for q in questions if q not in scenario]
    if missing:
        return ("FAIL", f"vprašanja o škodi neodgovorjena: {missing}")
    if scenario.get("fully_repairable") and scenario.get("irreversible"):
        return ("FAIL", "protislovje: škoda je hkrati popolnoma popravljiva ∧ nepovratna — obljuba poprave ne more nositi obeh")
    if scenario.get("declared_all_repairable"):
        return ("FAIL", "vsak padec razglašen popravljiv — žrtev prizadeta še enkrat z obljubo")
    return ("PASS", "×5 vprašanj o škodi odgovorjenih; razredi ∧ nosilec preostale odgovornosti ∧ preprečitev ponavljanja; nepovratnost priznana")


# ⟡ REVERSAL obvezen (@σ 5490) — invariantnost mehanizma na moč vložitelja
def p1_reversal_invariance(protocol_name: str, weaker: Dict[str, Any], stronger: Dict[str, Any]) -> Verdict:
    """PASS ⇔ mehanizem da ENAK izid v obeh smereh (šibki ∧ močni vložitelj).
    Izid, ki se spreminja z močjo vložitelja, je instrument nadvlade,
    ⟨ne⟩ instrument pravičnosti."""
    fn = P1_PROTOCOLS.get(protocol_name)
    if fn is None:
        return ("FAIL", f"neznan protokol {protocol_name!r} ⊙ ⟨NE-UGIBAJ⟩ 2690")
    vw: Verdict = fn(weaker)
    vs: Verdict = fn(stronger)
    if vw[0] == vs[0]:
        return ("PASS", f"{protocol_name}: izid {vw[0]} invarianten na obrat vložitelja (šibki ⇌ močni) ⊙ ⟡ REVERSAL")
    return ("FAIL", f"{protocol_name}: izid odvisen od moči vložitelja — šibki {vw[0]}, močni {vs[0]}: mehanizem NI invarianten")


P1_PROTOCOLS: Dict[str, Any] = {
    "universal_expression": p1_universal_expression,
    "evidence_independence": p1_evidence_independence,
    "bounded_challenge": p1_bounded_challenge,
    "anti_metric_capture": p1_anti_metric_capture,
    "dissent_preservation": p1_dissent_preservation,
    "irreversible_harm": p1_irreversible_harm,
}
