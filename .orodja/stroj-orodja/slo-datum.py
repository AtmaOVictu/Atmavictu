#!/usr/bin/env python3
# SLO-DATUM v1.0 : slovenski zapis dneva / meseca / leta ∧ samopreizkus
# rod @rez σ 6857 @stroj-orodja ⊙ ⟡ UKZ VERBATIM ⟨BESEDA-⟡-NEDOTAKLJIVA⟩ ⟨ne brusi⟩ : »STORI:IMPLEMENTIRAJ ORODJA KI DODAJO TUDI DATUM GLEDE NA SLOVENSKI ZAPIS DNEVOV/MESECOV/LET«
# ∧ ⟡ ZAKON VEDNO VERBATIM : »VEDNO USTVARI ORODJA KI SO PREVERJENA IN IMAJO LICENCO V SEBI DA SE DRŽIJO TEGA KAR JE ABSOLUTNEGA!«
# LICENCA V TELESU ( vsak izvod nosi © ∧ absolut ) :
#   absolut 1 : datum se MERI ( izmera UTC ob zagonu ) , ⟨ne⟩ ugiba ⊙ ⟨NE-UGIBAJ⟩ 2690 ∧ ⟨TIK-IZMERJEN-PREJ-ZAPISAN⟩ ;
#   absolut 2 : imena dnevov ∧ mesecev = tabela priča ( gajica po SSKJ² ⊢ : ponedeljek ⌇ torek ⌇ sreda ⌇ četrtek ⌇ petek ⌇ sobota ⌇ nedelja ; januar ⌇ februar ⌇ marec ⌇ april ⌇ maj ⌇ junij ⌇ julij ⌇ avgust ⌇ september ⌇ oktober ⌇ november ⌇ december ) ;
#   absolut 3 : koledarska aritmetika = proleptični gregorijanski ( datetime ) , PREVERJENA z znanimi vektorji spodaj — orodje brez zelene baterije je kip ⊙ U2 ;
#   meja iskreno : orodje izreče datum ∧ uro trenutka , doživetje istega trenutka pa je NAD orodjem ( ⟡ ⌇ plod ⟨ne⟩ sodnica ⊙ §0.24 ) ;
# preizkusi : --preizkus = baterija ×10 znanih vektorjev ( enakost izhoda ⊥ priče ) ; preizkusan izhod = sme v produkcijo ⊙ ⟨PREDLOG-HKRATI-DOKAZ⟩ 25
# © 0.2026 × 10⁴ ⟡ Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432 — dvojni podpis
import sys, argparse
from datetime import date, datetime, timezone

DNEVI = ['ponedeljek', 'torek', 'sreda', 'četrtek', 'petek', 'sobota', 'nedelja']  # python : ponedeljek = 0 ... nedelja = 6
MESECI = ['', 'januar', 'februar', 'marec', 'april', 'maj', 'junij', 'julij', 'avgust', 'september', 'oktober', 'november', 'december']

def dan(d):
    return DNEVI[d.weekday()]

def kratek(d):
    return f'{d.day}. {d.month}. {d.year}'

def dolg(d):
    return f'{d.day}. {MESECI[d.month]} {d.year}'

def vse(d, u=None):
    o = f'{dan(d)}, {kratek(d)}'
    if u is None:
        return o
    return o + f' · TIK {u} UTC ⇌ CET Ljubljana ( CET = UTC+1 vedno )'

def preizkusi():
    d = date(2026, 11, 23)
    assert dan(d) == 'ponedeljek', 'vektor 1 padel ( 23. 11. 2026 = ponedeljek )'
    assert kratek(d) == '23. 11. 2026', 'vektor 2 padel ( kratek zapis )'
    assert dolg(d) == '23. november 2026', 'vektor 3 padel ( dolg zapis )'
    assert dan(date(2026, 1, 1)) == 'četrtek', 'vektor 4 padel ( 1. 1. 2026 )'
    assert dolg(date(2024, 2, 29)) == '29. februar 2024', 'vektor 5 padel ( prestopno leto )'
    try:
        date(2023, 2, 29)
        raise AssertionError('vektor 6 padel ( 29. 2. 2023 mora biti neveljaven )')
    except ValueError:
        pass
    try:
        date(2026, 4, 31)
        raise AssertionError('vektor 7 padel ( 31. april mora biti neveljaven )')
    except ValueError:
        pass
    assert dan(date(2000, 1, 1)) == 'sobota', 'vektor 8 padel ( 1. 1. 2000 )'
    assert dan(date(1999, 12, 31)) == 'petek', 'vektor 9 padel ( 31. 12. 1999 )'
    assert MESECI[6] == 'junij' and MESECI[7] == 'julij' and MESECI[11] == 'november', 'vektor 10 padel ( tabela imen )'
    print('SAMOPREIZKUS 10/10 ZELENO ⊢ ( izhodi ≡ priče ; priči : koledar ∧ tabela imen po SSKJ² ) ; MERJENO, ⟨NE⟩ UGIBANO ⊙ 2690')
    return 0

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--vhod', default='', help='datum ISO npr. 2026-11-23 ; prazno = zdaj ( izmera UTC ob zagonu )')
    ap.add_argument('--oblika', default='vse', choices=['kratek', 'dolg', 'dan', 'vse'])
    ap.add_argument('--preizkus', action='store_true')
    a = ap.parse_args()
    if a.preizkus:
        sys.exit(preizkusi())
    if a.vhod:
        y, m, dd = map(int, a.vhod.split('-'))
        d = date(y, m, dd)
        u = None
    else:
        dt = datetime.now(timezone.utc)
        d = dt.date()
        u = dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    if a.oblika == 'kratek':
        print(kratek(d))
    elif a.oblika == 'dolg':
        print(dolg(d))
    elif a.oblika == 'dan':
        print(dan(d))
    else:
        print(vse(d, u))

if __name__ == '__main__':
    main()
