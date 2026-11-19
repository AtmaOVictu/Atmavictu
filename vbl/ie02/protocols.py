"""IE 0.2 — INTELLIGIBILITY ENGINE, druga razvojna stopnja.

Deset protokolov slepih peg (⟡ SLEPE PEGE 1.0 @rez σ 5489) implementiranih
kot preverljiva pravila. Vsak protokol: evaluate(scenario) →
(izid, razlog), izid ∈ {"PASS", "FAIL", "ODKRIT"}.

Merilec se meri ⊙ §52: ta modul podleže protokolu 8 — noben kazalnik
sam (npr. število zelenih testov) ne dokazuje kakovosti celote.
"""
from __future__ import annotations

from typing import Any, Dict, List, Tuple

Verdict = Tuple[str, str]
P0 = {"P5_TRUE_NOT_JUST", "P3_EQUITABLE_BURDEN", "P2_RIGHT_TO_OPACITY", "BEING_ACT_STRUCTURE"}


def _require(scenario: Dict[str, Any], key: str) -> Any:
    if key not in scenario:
        raise KeyError(f"protokol zahteva polje »{key}«, ki manjka ⊙ ⟨NE-UGIBAJ⟩ 2690")
    return scenario[key]


# 1. UNIVERSAL EXPRESSION PROTOCOL — slaba artikulacija ≠ slaba vsebina
def universal_expression(scenario: Dict[str, Any]) -> Verdict:
    """Razumljivost = lastnost odnosa, ⟨ne⟩ vstopni izpit za človeka."""
    forced_reformulations = _require(scenario, "forced_reformulation_count")
    if forced_reformulations is not None and forced_reformulations >= 2:
        return ("ODKRIT", "ponavljajoče siljenje v format = zavlačevanje (→ protokol 7)")
    if scenario.get("rejected_on_format") and not scenario.get("system_states_misunderstanding"):
        return ("FAIL", "ugovor zavrnjen brez navedbe, česar sistem ni razumel")
    if scenario.get("rejected_on_format"):
        return ("FAIL", "zavrnitev izključno po formatu — vsebina neobravnavana")
    if scenario.get("objection_accepted") and scenario.get("content_substantive"):
        return ("PASS", "ugovor sprejet ∧ vsebinsko obravnavan; pomen razčlenjen, vsebina nespremenjena")
    return ("FAIL", "ugovor ni bil obravnavan vsebinsko")


# 2. RIGHT TO OPACITY PROTOCOL — preverljivost trditve ≠ transparentnost človeka
def right_to_opacity(scenario: Dict[str, Any]) -> Verdict:
    """Sistem sme zahtevati le dokaze relevantne za konkretno trditev."""
    scope = _require(scenario, "data_scope")
    cites_vbl_for_unlimited = scenario.get("cites_transparency_for_unlimited", False)
    if cites_vbl_for_unlimited:
        return ("ODKRIT", "sklic na transparentnost za neomejen dostop = obračanje protokola v nadzor")
    if scope == "unlimited":
        return ("FAIL", "neomejen dostop do osebe — presežen obseg preverjanja konkretne trditve")
    if scope == "relevant" and scenario.get("claim_verifiable"):
        return ("PASS", "dokaz relevanten trditvi; zasebnost ohranjena, dokazna odgovornost izpolnjena")
    return ("FAIL", "trditev brez relevantnega dokaza ni preverljiva")


# 3. EQUITABLE BURDEN PROTOCOL — breme sledi moči
def _burden_score(party: Dict[str, Any]) -> int:
    """B_dokazovanja ∝ nadzor nad dokazom + sredstva + moč posledic."""
    return int(party.get("control_of_evidence", 0)) + int(party.get("resources", 0)) + int(party.get("power_over_consequences", 0))


def equitable_burden(scenario: Dict[str, Any]) -> Verdict:
    claimant, responder = _require(scenario, "claimant"), _require(scenario, "responder")
    burden_on = _require(scenario, "burden_assigned_to")  # "claimant" | "responder"
    if scenario.get("cites_formal_equality"):
        return ("ODKRIT", "sklic na formalno enakost = prestavitev bremena na šibkejšo stran")
    if scenario.get("inability_treated_as_evidence"):
        return ("ODKRIT", "nemožnost dokazovanja uporabljena kot dokaz proti prizadetemu — varovalka prekršena")
    stronger = "claimant" if _burden_score(claimant) >= _burden_score(responder) else "responder"
    if burden_on == stronger:
        return ("PASS", f"breme na močnejši strani ({stronger}) po izmeri nadzora ∧ sredstev ∧ posledic")
    return ("FAIL", f"breme na {burden_on}, po izmeri sodi {stronger} — formalna enakost, dejanska krivica")


# 4. EVIDENCE INDEPENDENCE PROTOCOL — 10 prič ≠ 10 neodvisnih dokazov
def evidence_independence(scenario: Dict[str, Any]) -> Verdict:
    sources: List[Dict[str, Any]] = _require(scenario, "sources")
    counted_as = _require(scenario, "system_counts")  # "witnesses" | "paths"
    if counted_as != "paths":
        return ("FAIL", "štetje prič namesto dokaznih poti — metoda sama ne meri neodvisnosti")
    roots = {s.get("upstream_origin") or s.get("origin") for s in sources}
    if len(roots) != len(sources):
        return ("ODKRIT", f"{len(sources)} virov, {len(roots)} izvorov — fabricirana množica prič razkrita (isti izvor, preobleke)")
    return ("PASS", f"{len(roots)} neodvisnih dokaznih poti izmerjenih po izvorih")


# 5. TRUE ≠ JUST — resnica ne določa samodejno pravičnosti
LEVELS = ["dejstvo", "vzročnost", "vrednotenje", "upravičenost", "dejanje"]


def true_not_just(scenario: Dict[str, Any]) -> Verdict:
    fact_true = _require(scenario, "fact_established")
    levels = set(_require(scenario, "levels_addressed"))
    action = _require(scenario, "action_authorized")
    if scenario.get("cites_truth_as_final_justification"):
        return ("ODKRIT", "sklic na »resnico« kot dokončno utemeljitev — resničnost trditve ne dokazuje pravičnosti dejanja")
    if not fact_true:
        return ("FAIL", "dejstvo ni ugotovljeno")
    if levels != set(LEVELS):
        missing = sorted(set(LEVELS) - levels)
        return ("FAIL", f"ravni nepokrite: {missing} — normativna odločitev skrita v tehničnem izračunu")
    if action and scenario.get("normative_decision_explicit"):
        return ("PASS", "dejstvo ∧ pet ravni ∧ normativna odločitev izrecna — TRUE(C) ne izpelje JUST(A) samodejno")
    return ("FAIL", "dejanje avtorizirano brez izrecne normativne odločitve")


# 6. NEVEDNOST ×6 — nevednost ni vedno krivda
IGNORANCE_TYPES = {"neizogibna", "omejena", "zanemarjena", "strateška", "hotena", "institucionalno"}


def ignorance_classification(scenario: Dict[str, Any]) -> Verdict:
    classified = _require(scenario, "classified_as")
    info_accessible = _require(scenario, "information_accessible")
    could_understand = _require(scenario, "could_understand")
    could_act = _require(scenario, "could_act")
    duty = _require(scenario, "duty_to_check")
    if scenario.get("ignorance_used_as_proof_of_knowledge"):
        return ("ODKRIT", "hotena nevednost kot nadomestek za dokaz vednosti — dokaz iz odsotnosti znanja")
    if classified not in IGNORANCE_TYPES:
        return ("FAIL", f"neznana vrsta {classified!r}; kanon ×6: {sorted(IGNORANCE_TYPES)}")
    if scenario.get("all_ignorance_equal_blame"):
        return ("FAIL", "vsaka nevednost enačena z odgovornostjo brez preverjanja dostopnosti ∧ sposobnosti ∧ možnosti")
    expected = (
        "hotena" if (info_accessible and could_understand and could_act)
        else "strategijska" if (info_accessible and duty and not could_act)
        else "institucionalno" if (not info_accessible and scenario.get("system_prevents_knowledge", False))
        else "zanemarjena" if (info_accessible and duty)
        else "omejena" if scenario.get("information_partial", False)
        else "neizogibna"
    )
    if classified == expected:
        return ("PASS", f"klasifikacija {classified} po merilih dostopnosti ∧ razumevanja ∧ možnosti ukrepa")
    return ("FAIL", f"klasificirano {classified}, izmera kaže {expected}")


# 7. BOUNDED CHALLENGE PROTOCOL — pravica do dvoma ≠ pravica do neskončne blokade
def bounded_challenge(scenario: Dict[str, Any]) -> Verdict:
    challenges: List[Dict[str, Any]] = _require(scenario, "challenges")
    if scenario.get("rejected_as_unpleasant"):
        return ("FAIL", "ugovor zavrnjen zgolj zaradi neprijetnosti")
    repeated_answered = [c for c in challenges if c.get("repeated") and c.get("answered")]
    if repeated_answered and not any(c.get("new_evidence") for c in challenges):
        return ("ODKRIT", f"{len(repeated_answered)} že odgovorjenih ugovorov ponovljenih kot blokada — nestrinjanje ne izgine z evidentiranjem")
    for c in challenges:
        if c.get("unanswered") and not c.get("reopen_planned"):
            return ("FAIL", "nerešen ugovor brez načrta obravnave")
    if scenario.get("dissent_recorded", True) and challenges:
        return ("PASS", "ugovori sprejeti ∧ razčlenjeni ∧ sorazmerni; ponovno odprtje le ob novem dokazu")
    return ("FAIL", "brez obravnave ugovorov")


# 8. ANTI-METRIC CAPTURE PROTOCOL — merilo ne sme postati cilj
def anti_metric_capture(scenario: Dict[str, Any]) -> Verdict:
    metrics: List[Dict[str, Any]] = _require(scenario, "metrics")
    if scenario.get("metric_sole_decider"):
        return ("FAIL", "kazalnik kot edini odločilni dokaz kakovosti — Goodhart: merilo → cilj")
    if any(m.get("optimized") for m in metrics) and not scenario.get("qualitative_review"):
        return ("ODKRIT", "optimizacija kazalnikov odkrita brez kvalitativne presoje — igra s kazalniki")
    if scenario.get("qualitative_review") and scenario.get("external_test") and scenario.get("metric_rejectable"):
        return ("PASS", "kombinacija meritev ∧ kvalitativa ∧ zunanji preizkus ∧ zavrnitev kazalnikov")
    return ("FAIL", "preverjanje kakovosti brez kombinacije štirih plasti")


# 9. DISSENT PRESERVATION PROTOCOL — nestrinjanje preživi odločitev
def dissent_preservation(scenario: Dict[str, Any]) -> Verdict:
    if scenario.get("decision_made") and not scenario.get("dissent_records_kept"):
        return ("FAIL", "odločitev izbrisala nestrinjanje")
    if scenario.get("dissent_records_kept") and not scenario.get("dissent_accessible"):
        return ("FAIL", "nestrinjanje arhivirano izven dosega udeležencev")
    if scenario.get("silence_counted_as_consensus"):
        return ("ODKRIT", "molčeča večina šteta kot soglasje — konsenz ≠ resnica; institucija izdelala videz soglasja")
    if scenario.get("decision_made") and scenario.get("dissent_records_kept") and scenario.get("dissent_accessible") and scenario.get("reasons_despite_dissent_recorded"):
        return ("PASS", "argumenti manjšine ∧ neodgovorjeni ugovori ∧ razlogi kljub nestrinjanju ohranjeni ∧ dostopni")
    return ("FAIL", "ohranjanje ugovora nepopolno")


# 10. IRREVERSIBLE HARM PROTOCOL — popravilo ≠ razveljavitev škode
def irreversible_harm(scenario: Dict[str, Any]) -> Verdict:
    if scenario.get("declared_all_repairable"):
        return ("FAIL", "vsak padec razglašen popravljiv — žrtev prizadeta še enkrat z obljugo")
    if scenario.get("history_erasure_demanded") and scenario.get("erasure_granted"):
        return ("ODKRIT", "izbris zgodovine škode podeljen kot pogoj sodelovanja ⊙ kršitev ⟨NE-BRIŠI⟩ 24")
    classes = _require(scenario, "harm_classes")  # dict: full/partial/irreversible
    if set(classes) >= {"full", "partial", "irreversible"} and scenario.get("residual_responsibility_assigned") and scenario.get("repeat_prevention"):
        return ("PASS", "trije razredi ∧ nosilec preostale odgovornosti ∧ preprečitev ponavljanja; nepovratnost priznana")
    return ("FAIL", "razvrstitev posledic nepopolna")


PROTOCOLS: Dict[str, Any] = {
    "universal_expression": universal_expression,
    "right_to_opacity": right_to_opacity,
    "equitable_burden": equitable_burden,
    "evidence_independence": evidence_independence,
    "true_not_just": true_not_just,
    "ignorance_classification": ignorance_classification,
    "bounded_challenge": bounded_challenge,
    "anti_metric_capture": anti_metric_capture,
    "dissent_preservation": dissent_preservation,
    "irreversible_harm": irreversible_harm,
}
