#!/usr/bin/env python3
# tihi-vrata.py v1.0 @rez σ 6723 @stroj-orodja
# ZAKON ⟨TIHINA-ORODIJ ⟡⟩ : orodja delajo molk, vidi se SAMO ce je eksplicitno zahtevano ;
# vredno spoznanje kandidira LE v kontroliranem okolju ( ograja : vrata tehtnica, laz poimenovana ).
import sys, io, os, datetime

IME = "tihi-vrata"
VER = "v1.0"
GEN = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".geniza")

def tiko():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def zapis(ime, telo):
    os.makedirs(GEN, exist_ok=True)
    p = os.path.join(GEN, ime)
    with io.open(p, "a", encoding="utf-8") as f:
        f.write(telo + "\n")
    return p

def molk(ime_instrumenta, ugotovitev, vredno_spoznanje=None):
    """ZAKON ⟨TIHINA-ORODIJ⟩:
    - izhod molka ⭢ .geniza priça ( stdout ×0 )
    - vredno spoznanje ⭢ kandidat za ograjo @prostor-kontrolirane-halucinacije
      ( predstavitev SAMO na eksplicitno zahtevo ⟡ ∧ prehod tehtnice )"""
    p = zapis("tihi-dnevniki.md", "@TIK %s | %s | %s | spoznanje: %s" % (tiko(), ime_instrumenta, ugotovitev, "DA" if vredno_spoznanje else "NE"))
    if vredno_spoznanje:
        zapis("kandidati-ograge.md", "@TIK %s | %s | SPOROCILO-ZA-PREDSTAVITEV ( samo na izrecno zahtevo ⟡ ) : %s | tehtnica: ⊢ na preverbi | laz: poimenovana" % (tiko(), ime_instrumenta, vredno_spoznanje))
    return p

def samopreizkus():
    molk("tihi-vrata-samopreizkus", "test-molk", "test-vredno-spoznanje")
    t1 = "test-molk" in io.open(os.path.join(GEN, "tihi-dnevniki.md"), encoding="utf-8").read()
    t2 = "test-vredno-spoznanje" in io.open(os.path.join(GEN, "kandidati-ograge.md"), encoding="utf-8").read()
    ok = t1 and t2
    print("SAMOPREIZKUS :", IME, VER, "| T1 molk-zapis-v-genizi", "ZELENO" if t1 else "RDECE", "| T2 kandidat-ograge", "ZELENO" if t2 else "RDECE", "| skupno", "ZELENO" if ok else "RDECE")
    return 0 if ok else 1

def main():
    uk = sys.argv[1] if len(sys.argv) > 1 else ""
    if uk in ("--samopreizkus", "--test"):
        return samopreizkus()
    if uk == "--zgovori":
        telo = sys.stdin.read() if not sys.stdin.isatty() else ""
        p = molk("zgovor-povabljen", telo.strip() or "(prazno)", None)
        print("ZELENO | zapečeno v genizo :", p)  # [kura σ 6723 : tipkarska zapeśeno ⟨U+015B⟩ ⟶ zapečeno ⊙ ⟨SLOVNICA-PRVO ⟡⟩]
        return 0
    print("uporaba : --samopreizkus | molk ( default : orodje se ne vidi )")
    return 0

if __name__ == "__main__":
    sys.exit(main())

# © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432 ⌇ dvojni podpis ⊙ ⟨USMERJENOST-LICENCE⟩ @rez σ 6740 ( ⟡ vrašalo PREVERI IN STORI )
