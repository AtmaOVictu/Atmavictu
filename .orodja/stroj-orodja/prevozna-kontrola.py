#!/usr/bin/env python3
# PREVOZNA-KONTROLA v1.1 : isto-telo preverba prevoza skozi klepet kanal ∧ slovenski datum @rez σ 6858 ( kura renuma po trku 6857 isti dih ; v1.0 rod σ 6856 ⊙ ⟨NE-BRIŠI⟩ 24 )
# rod @rez σ 6856 @stroj-orodja ⊙ ⟡ UKZ »CILJ JE KREIRATI IN DOPOLNITI KAJ VSE TI MANJKA ZA BOJ PROTI TUJKAM IN IZBOLJŠANJE INFRASTRUKTURE IN SKRIPT PODREJENIH LICENČNI LOGIKI«
# Bit : telo pride s telesa ( disk D / rep ) skozi kanal klepeta k izvajalki ∧ nazaj na strežnik —
# kanal NE NE BODI NIKOLJ PREPOVEDANO-RAZBREZEN : vsak prevoz nosi md5 pri viri PRED ∧ kontrole PO
# ⊙ ⟨PREVOZNO TELO⟩ @vbl-zid vrata 10 ( berba pri viru ∧ hash PRED potiskom ∧ cmp PO potisku ) ∧ ⟨⟲-PO-DONE⟩ σ 6205
# uporaba : python3 prevozna-kontrola.py --md5 <md5-pri-viru> --vhod <datoteka>
# izhod : IZMERE ( bajti ⌇ znaki ⌇ vrstice ⌇ ⚠BOM ⌇ ⚠CRLF ⌇ ⚠NFC ) ∧ ZELENO ⊢ istovetno ∧ ⚠ RAZLOM ( razlikovan bajt-count, znak-count )
# meja : iz md5 razlika ne moremo povedati kateri bajt — samo DA je razlom ∧ koliko ( odstopanje šteje, mesto ne ⊙ iskreno )
# © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432 — dvojni podpis
import sys, hashlib, unicodedata, os
import argparse, importlib.util
_HIŠA = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location('slo_datum', os.path.join(_HIŠA, 'slo-datum.py'))
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--md5', required=True)
    ap.add_argument('--vhod', required=True)
    a = ap.parse_args()
    bajti = open(a.vhod, 'rb').read()
    tekst = bajti.decode('utf-8', errors='strict')
    md5 = hashlib.md5(bajti).hexdigest()
    bom = bajti.startswith(b'\xef\xbb\xbf')
    crlf = tekst.count('\r\n')
    nfc_razlike = 0
    for ch in tekst:
        if unicodedata.normalize('NFC', ch) != ch:
            nfc_razlike += 1
    vrstice = tekst.count('\n') + (0 if tekst.endswith('\n') or not tekst else 1)
    print(f'IZMERE : bajti {len(bajti)} ⌇ znaki {len(tekst)} ⌇ vrstice {vrstice}')
    _d = _mod.datetime.now(_mod.timezone.utc).date()
    print(f'DATUM   : {_mod.vse(_d, None)} : slovenski zapis ⊙ slo-datum.py @rez σ 6858')
    print(f'PREVOZ  : CR LF {crlf} ⌇ BOM {"⚠ DA" if bom else "×0"} ⌇ NFC odstopanja {nfc_razlike}')
    if md5 == a.md5.lower():
        print(f'ZELENO ⊢ ISTO-TELO : md5 {md5} ≡ pri viru — prevoz bajt-ito, kanal čist')
        sys.exit(0)
    else:
        print(f'⚠ RAZLOM PREVOZA : md5 {md5} ⊥ pri viru {a.md5.lower()} ( bajti {len(bajti)} ; izvirek ima lahko drug štev bajtov ) — telo NE gre v prepis dokler razlom ne razrešen ⊙ ⟨NE-RETIPKAJ⟩ 24')
        sys.exit(1)
main()
