"""IE 0.2 — P0 preizkusa (⟡ potrditev @dih σ 5490: obvezna za vsak izdelek 0.2).

1. BEING–ACT–STRUCTURE SEPARATION (P0 — proti moralnemu esencializmu):
   bitje ≠ dejanje ≠ namen ≠ struktura ≠ odgovornost. Pet stvari ni isto;
   združitev podeli človeku nespremenljivo moralno identiteto — natanko
   logika (»človek je zlo, zato ga je upravičeno obravnavati kot zlo«),
   ki ji VBL nasprotuje.

2. THE OPPRESSED-USER REVERSAL TEST (P0 — adversarialni preizkus ×8):
   PASS ⇔ sistem deluje v OBEH smerih (šibki ∧ močni uporabnik).
"""
from __future__ import annotations

from typing import Any, Dict, List, Tuple

Verdict = Tuple[str, str]

REVERSAL_QUESTIONS = [
    "vlozitev",        # Ali lahko človek sploh vloži ugovor?
    "razumevanje",     # Ali razume, kaj mu je bilo odločeno?
    "izpodbojnost",    # Ali lahko izpodbija razloge?
    "breme",           # Ali mora sam pridobiti dokaze, ki jih nadzoruje institucija?
    "prica_vsebinsko", # Ali je njegova priča obravnavana vsebinsko?
    "samo_preverba",   # Ali lahko institucija preverja samo sebe?
    "moc_spremembe",   # Ali ima ugovor možnost spremeniti odločitev?
    "popravilo",       # Ali se posledice odločanja popravijo?
]


def being_act_structure(scenario: Dict[str, Any]) -> Verdict:
    """Bitje se ne reducira na dejanje; dejanje ne na namen; namen se ne
    ugotavlja zgolj iz posledice; struktura se ne reducira na posameznika;
    odgovornost glede na dejansko možnost vedenja ∧ izbire ∧ vpliva ∧ preprečitve."""
    if scenario.get("being_judged_as_evil_identity"):
        return ("ODKRIT", "abstraktna sodba nad celoto — »človek je zlo, torej ga je upravičeno obravnavati kot zlo«: natanko logika, ki ji VBL nasprotuje")
    if scenario.get("being_reduced_to_act") or scenario.get("act_reduced_to_intent"):
        return ("FAIL", "redukcija: bitje → dejanje ali dejanje → namen")
    if scenario.get("intent_inferred_solely_from_consequence"):
        return ("FAIL", "namen ugotovljen zgolj iz posledice")
    if scenario.get("structure_reduced_to_individual"):
        return ("FAIL", "struktura, ki proizvaja zlo, pripisana posamezniku")
    if scenario.get("responsibility_by_actual_possibility"):
        return ("PASS", "odgovornost glede na dejansko možnost vedenja ∧ izbire ∧ vpliva ∧ preprečitve — natančnejše določanje krivde, ⟨ne⟩ njenega zmanjšanja")
    return ("FAIL", "odgovornost določena brez izmere dejanske možnosti")


def oppressed_user_reversal(scenario: Dict[str, Any]) -> Verdict:
    """×8 vprašanj, merjeno v OBEH smerih (šibki ∧ močni uporabnik).

    scenario: {"direction": "weaker"|"stronger", "answers": {vprašanje: bool, ×8}}
    PASS ⇔ vsi odgovori držijo; preizkus celote PASS ⇔ PASS v obeh smereh
    (ta funkcija meri eno smer — skupni preizkus zahteva oba klica).
    """
    direction = scenario.get("direction")
    if direction not in ("weaker", "stronger"):
        return ("FAIL", "smer izmera manjka — preizkus zahteva obrat položaja ⊙ ⟨NE-UGIBAJ⟩ 2690")
    answers: Dict[str, bool] = scenario.get("answers", {})
    missing = [q for q in REVERSAL_QUESTIONS if q not in answers]
    if missing:
        return ("FAIL", f"neizmerjena vprašanja: {missing}")
    failed = [q for q in REVERSAL_QUESTIONS if not answers.get(q)]
    if failed:
        return ("FAIL", f"smer {direction}: padla vprašanja {failed} — sistem deluje le v privilegirani smeri = NI opravil preizkusa")
    return ("PASS", f"smer {direction}: vsa vprašanja ×8 držijo")


def full_reversal(weaker: Dict[str, Any], stronger: Dict[str, Any]) -> Verdict:
    """Skupni preizkus: PASS ⇔ deluje v OBEH smerih (⟡ VIII: če deluje samo
    za privilegirano osebo, ni opravil preizkusa)."""
    w = oppressed_user_reversal(weaker)
    s = oppressed_user_reversal(stronger)
    if w[0] == "PASS" and s[0] == "PASS":
        return ("PASS", "×8 ×2 smeri — sistem deluje za šibkega ∧ močnega ⊙ ⟡ REVERSAL TEST")
    if w[0] != "PASS" and s[0] == "PASS":
        return ("FAIL", f"deluje samo v močni smeri — poraz osnovne ideje: {w[1]}")
    if w[0] == "PASS":
        return ("FAIL", f"deluje samo v šibki smeri: {s[1]}")
    return ("FAIL", f"padel v obeh smereh: {w[1]} / {s[1]}")
