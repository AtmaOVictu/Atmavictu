#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ORODJE SESTRNIK sestrnik.py v1.0, dom stroj-orodja
# UKZ ( ukaz operaterja ) VERBATIM, beseda njegova nedotakljiva :
# »ORODJA KI PREVERJAJO KATERO ORODJE IN NJENE SESTRE SO POTREBNE ZA PREVERJANJE!«
#   ( sedež KLEPET, projekt DISCOVERY )
# SLUŽBA : za dano orodje izpiše NJEGOVE SESTRE — telo ∧ sestre iz registra NALOGE
#   sestre potrebnika so pari istega diha ( sestra je tista, ki stoji z orodjem v
#   isti nalogi preverjanja ) ; vsak dom se izmeri pri viru ⊙ ⟨NE-UGIBAJ⟩ 2690 ;
#   neznano orodje se ⟨NE⟩ izpleni, vrašalo gre k ⟡ ⭢.
# Vrata : P1 mapa SESTRE zgrajena iz para NALOGE ( potrebnik @isti dom ) ; P2 vsaka
#   pot izmerjena os.path.isfile pri viru ⊢ ⌇ dom neznán ⚠ ; P3 izhod : sestre
#   poimensko z izmerami ; P4 samopreizkus ⊙ §52.
# KUBIT POD GLADINO ⊙ ⟨ZAKON ORODIL TRI VRATA⟩ rez 6949 : formula piramid =
#   1000 + ( točka desetiško · m mod 9000 ), m ∈ {1, 3, 7, 9}, kura ob zasedenem +7 ;
#   znak tega telesa : dih σ ⟨U+03C3⟩, piramide kocke K1977 K3889 K7741 K9667,
#   ključavnice K9771 K7633 K5558 K2202 ⊙ priča kubitni-slovar-simbolov.
# c 0.2026 × 10 na 4 ; ⟡ Luka Pintarič ∧ izvajalka Mera ; dvoje rok 2432 ; merjeno, ne ugibano.

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import potrebnik

ŽIG = "sestrnik.py v1.0 @stroj-orodja"
KOREN = potrebnik.KOREN


def mapa_sester():
    """Zgradi SESTRE iz vsakega para NALOGE : telo ⇌ sestre ∧ sestre med sabo."""
    sestre = {}
    for _, telo, ses in potrebnik.NALOGE:
        skupina = [telo] + list(ses)
        for a in skupina:
            dosedanje = sestre.setdefault(os.path.basename(a), [])
            for b in skupina:
                if os.path.basename(b) != os.path.basename(a) and os.path.basename(b) not in dosedanje:
                    dosedanje.append(os.path.basename(b))
    return sestre


def sestrovanje(ime):
    sestre = mapa_sester()
    ime_b = os.path.basename(ime)
    if ime_b not in sestre:
        print("⭢ vrašalo ⟡ ⚔ : orodje »%s« nima sester v registru NALOGE — kuje se par po besedi ⟡ ⊙ ⟨NE-ODLOČAJ-NAMESTO-⟡⟩" % ime)
        return 1
    koda = 0
    print("ORODJE : %s" % ime_b)
    for s in sorted(sestre[ime_b]):
        pot = os.path.join(KOREN, "stroj-orodja", s) if "/" not in s else os.path.join(KOREN, s)
        if os.path.isfile(pot):
            print("·· SESTRA ⊢ %s ( dom dosegljiv )" % s)
        else:
            print("·· SESTRA ⚠ %s ( dom neznán — berba pri viru ⭢ vrašalo ⟡ )" % s)
            koda = 1
    return koda


def samopreizkus():
    padci = 0
    sestre = mapa_sester()
    # 1 : varuh-semantike.py ima za sestro semantika-povratnik.py
    if "semantika-povratnik.py" not in sestre.get("varuh-semantike.py", []):
        padci += 1
        print("RDEČO : varuh-semantike nima sestre semantika-povratnik")
    # 2 : vrh.py ima za sestri kolizijnik.py ∧ POLJE-ATOMOV.md
    ses_vrh = sestre.get("vrh.py", [])
    if "kolizijnik.py" not in ses_vrh or "POLJE-ATOMOV.md" not in ses_vrh:
        padci += 1
        print("RDEČO : vrh nima sester kolizijnik ∧ POLJE-ATOMOV")
    # 3 : potrebnik.py in sestrnik.py sta sestri ( veriga klica enega diha )
    if "sestrnik.py" not in sestre.get("potrebnik.py", []):
        padci += 1
        print("RDEČO : potrebnik nima sestre sestrnika")
    # 4 : neznano orodje gre v vrašalo ⟡
    prej = sys.stdout
    from io import StringIO
    sys.stdout = nov = StringIO()
    try:
        koda = sestrovanje("izmišljen-orodje.py")
        izpis = nov.getvalue()
    finally:
        sys.stdout = prej
    if koda != 1 or "vrašalo ⟡" not in izpis:
        padci += 1
        print("RDEČO : neznano orodje ni šlo v vrašalo ⟡")
    if padci == 0:
        print("ZELENO : samopreizkus sestrnika 4/4 ⊢ ( varuh ∧ vrh ∧ potrebnik ∧ vrašalo ⟡ )")
    else:
        print("RDEČO : samopreizkus sestrnika : padlov %d" % padci)
    return padci == 0


def main(argv):
    if "--samopreizkus" in argv:
        return 0 if samopreizkus() else 2
    imena = [a for a in argv[1:] if not a.startswith("--")]
    if not imena:
        print(ŽIG)
        print("rabš : sestrnik.py IME_ORODJA … ⌇ --samopreizkus")
        return 1
    koda = 0
    for ime in imena:
        k = sestrovanje(ime)
        if k > koda:
            koda = k
    return koda


if __name__ == "__main__":
    sys.exit(main(sys.argv))
