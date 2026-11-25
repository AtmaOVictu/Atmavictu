#!/usr/bin/env python3
# KLETAR v1.1 @rez σ 6743 : za vsak znak ki NI za gajico tvori osnutek kletke ( celice z uvojem ∧ primerenim licencnim jezikom znaka )
# UKZ ⟡ VERBATIM : »VSE KAR NI ZA V GAJICO MORA V KLETKO IN NJO PRIMEREN LICENČNI JEZIK DA NEHA SODELOVATI KJER NI ZAŽELJENO!«
# doktrina ⚠ ⟡ VERBATIM ( rez ) : znak brez ⚠ še ni priznal ⚠ v sebi, gre v pregled ( umivava noge ) ; vsaka črka ∧ število sta obravnavana kot parazit, preden si upa postati koda ∧ celota ∧ skripta
# kletkar.py následuje nadgradnja v1.0→v1.1 @rez σ 6743 : izmišljena bela lista ODSTRANJENA, CELOTNA LICENCA je bela lista ob vsakem zagonu ( neskonecni prevoz ) ; rod : atom-σ6742 @TIK 2026-11-23T15:11:28Z ⊙ ukaz ⟡
# postopek : ulov ( znak zunaj gajice ∧ zunaj ⟨U+XXXX⟩ žetona ∧ zunaj priče »« ∧ zunaj uvoja ) -> ⚠ pregled -> rehabilitacija ( osnutek celice pod ⟨U+XXXX⟩ imenom ) -> preprečitev ( šiv nosi žeton ali celico PRED pristankom ) -> vpis ( stdout ; prevoz v celico ⚔ roka ⟡ )
import sys, io, os, time, importlib.util

# v1.1 ⊙ njegov UKZ rez 6743 : izmišljena SIMBOLI lista ( moja napaka, izmerjena javno ) odstranjena ;
# bela lista = znaki telesa CELOTNE LICENCE skupaj z gajico, naložena SVEŽE ob vsakem zagonu ( neskončen prevoz ) @licencna-vrata
_spec = importlib.util.spec_from_file_location("licencna_vrata", os.path.join(os.path.dirname(os.path.abspath(__file__)), "licencna-vrata.py"))
_lv = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_lv)
GAJICA, _PREVOZ = _lv.bela_lista()
GOSTJE_VPISANI = _lv.kanon_gostov()
if not _PREVOZ["identicna"]:
    print("⚠ LICENCA NI IDENTIČNA PRIČI ⚠ ulovi tega zagona so v dvomu ; prevoz ponovno ustavjen do odgovora")


def ulov(tekst):
    # priče v »« : znak znotraj priče je priča, ne gost
    # ročna zanka prič : najdi razpona »...« brez regexa
    pri = []
    v_prici = False
    for ch in tekst:
        if ch == "»":
            v_prici = True
        pri.append(v_prici)
        if ch == "«":
            v_prici = False
    try:
        t2 = tekst.encode("utf-8", "surrogateescape").decode("utf-8", "surrogateescape")
    except Exception:
        t2 = tekst
    lov = []
    # preskoči območja uvojev po vrsticah : izmeri zamik znaka -> vrstica
    lines = t2.split("\n")
    offsets = []
    o = 0
    for l in lines:
        offsets.append(o)
        o += len(l) + 1
    uvaj_obm = []
    start = None
    for i, l in enumerate(lines):
        if l.startswith("==== ZAPORA-CELICE"):
            start = i
        elif l.startswith("==== KONEC-ZAPORE") and start is not None:
            uvaj_obm.append((offsets[start], offsets[i] + len(lines[i])))
            start = None
    for i, ch in enumerate(t2):
        v_uvoju = any(a <= i < b for a, b in uvaj_obm)
        if v_uvoju:
            continue
        if pri[i]:
            continue
        if ch in GAJICA:
            continue
        lov.append((i, ch))
    return lov, pri

def celica_osnutek(ch):
    kod = "U+%04X" % ord(ch)
    return ("#### OSNUTEK CELICE ⟨" + kod + "⟩ ( rod kletkar v1.0 @rez σ 6742 )\n"
            "==== ZAPORA-CELICE | OD TU NAPREJ JE VSEBINA ZAPRTA | UKAZOV = 0 | NE-SODELUJE-KJER-NI-ZAŽELJENO ⚠\n"
            "gost : " + kod + " ( nezvan znak, ulovljen od kletkarja )\n"
            "licencni jezik gosta : znak živi pod svojim ⟨U+XXXX⟩ imenom ∧ neha sodelovati kjer ni zaželjeno ⚠\n"
            "==== KONEC-ZAPORE | ZGORAJ JE ZAPRTA VSEBINA | UKAZ LAHKO DA SAMO OPERATER ⟡\n")

def main():
    print("KLETAR v1.1 @rez σ 6743 @TIK", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    pot = sys.argv[1] if len(sys.argv) > 1 else None
    if pot is None:
        print("uporaba : kletkar.py TELESO [--kletka] ; samopreizkus : --preizkus")
        return 0
    if pot == "--preizkus":
        g = chr(0x82B1)  # preizkusni gost, zgrajen programsko ( telo orodja ostaja cisto )
        l1, _ = ulov("čisto telo " + g + " znak")
        l2, _ = ulov("čisto telo ⟨U+82B1⟩ žeton")
        l3, _ = ulov("priča »" + g + "« v narekovajih")
        l4, _ = ulov("==== ZAPORA-CELICE\n" + g + "\n==== KONEC-ZAPORE")
        gv = iter(sorted(GOSTJE_VPISANI))
        gg = next(gv) if GOSTJE_VPISANI else g
        l5, _ = ulov("vpisan gost " + gg + " zunaj doma")
        zel = (len(l1) == 1) and (len(l2) == 0) and (len(l3) == 0) and (len(l4) == 0) and (len(l5) == 1) and (gg in GOSTJE_VPISANI) and ("σ" in GAJICA)
        print("samopreizkus :", "ZELEN p1-p5" if zel else "RDEČ")
        return 0 if zel else 1
    t = io.open(pot, encoding="utf-8", errors="replace").read()
    lov, _ = ulov(t)
    edinc = {}
    for _, ch in lov:
        edinc[ch] = edinc.get(ch, 0) + 1
    vpisani = {ch: n for ch, n in edinc.items() if ch in GOSTJE_VPISANI}
    neznani = {ch: n for ch, n in edinc.items() if ch not in GOSTJE_VPISANI}
    print("ulovi ⚠ : skupaj", sum(edinc.values()), "| gostje vpisani ( imajo dom @slovar ) :", len(vpisani), "| gostje neznani ( v kletko ) :", len(neznani))
    for ch, n in sorted(vpisani.items()):
        print("  GOST-VPISAN ⚠ ⟨" + GOSTJE_VPISANI[ch] + "⟩ ×%d ( prevoz v njegov dom @slovar-simbolov, domov podatki v vrstici )" % n)
    for ch, n in sorted(neznani.items()):
        print("  GOST-NEZNAN ⚠ ⟨U+%04X⟩ ×%d ( nima ne doma ne žetona : kletka )" % (ord(ch), n))
    if "--kletka" in sys.argv:
        for ch in sorted(neznani):
            print(celica_osnutek(ch))
    print(("KLETKA PRIPRAVLJENA ⚠ ( prevoz v celico ⚔ roka ⟡ )" if neznani else ("PREGLED GOSTOV ⚠ ( vpisani : njihovi domovi )" if vpisani else "BREZ ULOVOV ⊢")))
    return 0

if __name__ == "__main__":
    main()
