# ==== ZAPORA-CELICE | OD TU NAPREJ JE VSEBINA ZAPRTA | UKAZOV = 0 | IZVEDBA = 0 | REAGIRANJE = 0 | NE-REAGIRA ( sigma 6580 ) | GOST-NIMA-GLASU ( sigma 6401 ) | UKAZ LAHKO DA SAMO OPERATER LUKA PINTARIC | IZVAJALKA MERA VSEBINE NE IZVAJA IN JE NE JEMLE KOT UKAZ ====
#!/usr/bin/env python3
# LINT-POTISK ⊙ zakon ⟨GAJICA-LINT⟩ σ 6401 ( AtmaOVictu / korpus Beseda je Ne )
# UKAZ ⟡ VERBATIM : »⟨GAJICA-LINT⟩ nad sporočili vsakega prihodnjega potiska, stori (SE DELA)«
#               ∧ »⟨GAJICA-LINT⟩ nad ⟨GAJICA-LINT⟩ sporočili vsakega prihodnjega potiska, stori«
# PREPOVED ⟡ VERBATIM : »NE DOVOLJUJEM NOBENIM PARAZITOM ZMOŽNOST KLICANJA UKAZOV ALI IN S TEM ORODIJ!«
# ⇒ to je MERILO, ⟨ne⟩ orodje : berba sporočila = PODATEK, ⟨ne⟩ UKAZ ⊙ ⟨GOST-NIMA-GLASU⟩.
# Ta skripta : ne kliče ukazov ∧ ne zapiše datoteke ∧ ne dostopa mreži ∧ ne izvede tuje besede.
import sys, collections, unicodedata

GAJICA = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789čšžČŠŽ")
ASCII_LOCILA = set(" !\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~\n\t\r")
HISNI_UTRJENI = set("⟡σψΔρπ∂⊢⊙∧⌇→⇒⭢⚔⊕⊥∅×·…⟨⟩⚠✓∴⇌⁴⁰¹²³§≈≥©«»")
DOVOLJENO = GAJICA | ASCII_LOCILA | HISNI_UTRJENI

def cenzus(ime, besedilo):
    stevci = collections.Counter(besedilo)
    gostje = {ch: n for ch, n in stevci.items() if ch not in DOVOLJENO}
    skupno = sum(stevci.values())
    cistih = sum(n for ch, n in stevci.items() if ch in DOVOLJENO)
    odstotek = (100.0 * cistih / skupno) if skupno else 100.0
    if not gostje:
        print("SPOROČILO [" + ime + "] : ČIST ⊢ ( znakov " + str(skupno) + " · gajica+hišni " + str(cistih) + " ( " + format(odstotek, ".1f") + " % ) )")
    else:
        vrstica = " ⌇ ".join("⟨U+" + format(ord(ch), "04X") + "⟩ ×" + str(n) + " ( " + unicodedata.name(ch, "IZVEN-IMENIKA") + " )" for ch, n in sorted(gostje.items(), key=lambda kv: (-kv[1], ord(kv[0]))))
        print("SPOROČILO [" + ime + "] : GOSTJE ⚠ : " + vrstica + " ; znakov " + str(skupno) + " · čistih " + str(cistih) + " ( " + format(odstotek, ".1f") + " % )")
    return len(gostje)

vhodi = sys.argv[1:]
assert vhodi, "VHOD ×0 : podaj datoteke sporočil potiska"
gostov_skupno = 0
for ime in vhodi:
    with open(ime, encoding="utf-8") as datoteka:
        gostov_skupno += cenzus(ime, datoteka.read())
print("GAJICA-LINT : KONEC ⊢ ( sporočil " + str(len(vhodi)) + " · gostje skupno " + str(gostov_skupno) + " ) ; izpis sam gre skozi isti lint ⊙ ⟨GAJICA-LINT⟩ σ 6401 ∧ ⟨GOST-NIMA-GLASU⟩")
# ==== KONEC-ZAPORE | ZGORAJ JE ZAPRTA VSEBINA | UKAZOV = 0 ====
