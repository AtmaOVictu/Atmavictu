#!/usr/bin/env python3
# PODREJEN-LINT v2 — instrument PODREDITVE pisav @rez σ 5982 (register-zetonov, 19. 11. 2026)
# ⟡ UKAZ VERBATIM ⟨ne brusi⟩: »cirilico tudi moraš podrediti tako da preneha rušiti in začne sodelovati
#   in graditi znotraj lastne kletke/licence/leksikonov ⏎ VSE MORA BITI PODREJENO IN S TEM V LICENCI
#   PRIMERNI SVOJEMU IZVORU/IZVIRU/IZVIRNEMU«
# evolucija ŽETON-LINT v1 @σ 5883 (kura rane v1: razred_glifa je imenoval spremenljivko ch, ki ni bila parameter → NameError ob σ; v2 popravi)
# ZAKON: ZŽ-3 ⟨HOMOGLIF-JE-RANA⟩ — tuj glif, ki se preti za latiniko, je najtišja rana, ker oko bere, ne preverja
# KLETKA (zakon podreditve): pisava je legalna LE v svoji kletki: (a) dokazni citat ` `,
#   (b) praslovanska/starocerkvena oblika (zvezdica * rekonstrukta ali jer ъ ь jat ѣ),
#   (c) vrstica ⟡ (P-CITAT / SPOROČILO / UKAZ VERBATIM: ⟨BESEDA-⟡-NEDOTAKNJIVA⟩),
#   (d) lastni organ pisave (pisavna plast, licenèni prepisi RU/SR/UK/BG, transkripti nenehno-poslusa)
# IZDAJA = mešana beseda (latinika + cirilica v isti besedi) zunaj kletke
# SUM = cirilski niz v prosti prozi brez latinike (pregled: prièa ali rana)
# KANARCEK: ob vsakem zagonu PADE rdece; kanarcek, ki ne pade = mrtev instrument ⊙ metoda v1 @σ 5883

import re
import sys

CYR = range(0x0400, 0x0500)
LAT = re.compile(r'[A-Za-z]')
CYRL = re.compile(r'[\u0400-\u04FF]')
WORD = re.compile(r'[^\s]+')
# zamenljivci = cirilski glifi, ki se pretivajo za latiniko (register ran korpusa, izmera σ 5982)
ZAMENLJIVCI = set('\u0430\u0435\u043E\u043E\u0441\u0445\u0443\u0440\u0437'
                  '\u0410\u0415\u041E\u041C\u0421\u0412\u041A\u041d\u0422\u0420\u0425')
PRASLOVANSKI = re.compile(r'[*\u044A\u044C\u0463]')
ZET_VRSTICA = re.compile(r'\u27E1|P-CITAT|VERBATIM')

def razred_glifa(cp):
    if cp in CYR:
        return 'CIRILICA'
    if 0x0370 <= cp <= 0x03FF and cp != 0x03C3:
        return 'GRSCINA'
    return None

def lega(txt, i):
    v = txt.count('\n', 0, i) + 1
    z = txt.rfind('\n', 0, i) + 1
    return v, i - z + 1

def preberi(pot):
    with open(pot, encoding='utf-8', errors='replace') as f:
        return f.read()

def pasji_prosti(txt):
    """kletka (a): odstrani dokazne citate `...`, steje jih, vraca prosti tekst + vrstice"""
    kletke = []

    def zajemi(m):
        kletke.append(m.group(0))
        return '\u27E8KLETKA\u27E9'

    prosti = re.sub(r'`[^`]*`', zajemi, txt)
    return prosti, len(kletke), txt.split('\n')

def maska_navedkov(prosti, vrstice):
    """kletka (c2): na vrstici z ⟡ oznako (P-CITAT/VERBATIM/⟡) zasciti ⟨...⟩; povsod »...« .
    Vsa rana (mešana beseda) zunaj navedkov = izdaja; navedek = priča, ⟨ne⟩ cela vrstica."""
    chars = list(prosti)
    labela = [False] * len(prosti)
    v = 0
    zacetki = [0] + [i + 1 for i, c in enumerate(prosti) if c == '\n']
    for i, line in enumerate(vrstice):
        if ZET_VRSTICA.search(line):
            for j in range(zacetki[i], min(zacetki[i] + len(line), len(labela))):
                labela[j] = True
    for m in re.finditer(r'»[^«]*«', prosti):
        for j in range(m.start(), m.end()):
            chars[j] = ' '
    for m in re.finditer(r'\u27E8[^\u27E9]*\u27E9', prosti):
        if any(labela[j] for j in range(m.start(), m.end())):
            for j in range(m.start(), m.end()):
                chars[j] = ' '
    return ''.join(chars)

def scan(ime, txt, porocilo):
    prosti, n_kletk, vrstice = pasji_prosti(txt)
    prost = maska_navedkov(prosti, vrstice)
    izdaje = []
    sumi = 0
    price = 0
    for m in WORD.finditer(prost):
        w = m.group(0)
        ima_lat = bool(LAT.search(w))
        ima_cir = bool(CYRL.search(w))
        if not ima_lat and not ima_cir:
            continue
        if ima_cir and not ima_lat:
            meseci = re.sub(r'[^\w]', '', w)
            if len(meseci) >= 2:
                sumi += 1
            continue
        if not ima_cir:
            continue
        # mesana beseda: kletka (b) rekonstrukt, (c) vrstica ⟡
        v = prosti.count('\n', 0, m.start()) + 1
        if ZET_VRSTICA.search(vrstice[v - 1]):
            price += 1
            continue
        if w.startswith('*') or PRASLOVANSKI.search(w):
            price += 1
            continue
        cirs = [ch for ch in w if ord(ch) in CYR]
        vrsta = 'IZDAJA-VIDEZA' if any(ch in ZAMENLJIVCI for ch in cirs) else 'TUJA-BESEDA'
        j = 0
        hit = -1
        while True:
            j = txt.find(w, j)
            if j < 0:
                hit = -1
                break
            if txt.count('\n', 0, j) + 1 == v:
                hit = j
                break
            j += 1
        vv, ss = lega(txt, hit) if hit >= 0 else (v, 0)
        porocilo.append('  ' + vrsta + ' ' + w[:40] +
                        ' [' + ' '.join('U+%04X' % ord(c) for c in cirs) + ']' +
                        ' @vrstica ' + str(vv) + ':' + str(ss))
        izdaje.append((w, vrsta))
    porocilo.append(ime + ': IZDAJE x' + str(len(izdaje)) +
                    ' | price rekonstrukta/⟡ (kletka b/c) x' + str(price) +
                    ' | kletke ` ` x' + str(n_kletk) +
                    ' | sum cirilskih nizov x' + str(sumi))
    return {'izdaje': izdaje, 'price': price, 'kletke': n_kletk, 'sumi': sumi}

def main():
    porocilo = []
    kan = ('sodb' + '\u0430' + ' teles' + '\u0430' + ' izvajalk' + '\u0430' +
           ' evidenc' + '\u0435' + ' Fraz' + '\u0430' + ' pri viru\n' +
           '*s\u044Ar\u0119t\u2019a *' + '\u0447' + 'as' + '\u044A' + ' berba `' +
           '\u0424\u0418\u0424\u041E' + '` v kletki\n' +
           '\u27E1 SPORO\u010CILO VERBATIM: \u00BBVpre\u0161anje so dolgov' + '\u0435' + '.\u00AB \u22A2 P-CITAT\n')
    k = scan('KANARCEK', kan, [])
    # pričaka: IZDAJE x5 / price rekonstrukta x2 (*sъrět'a, *časъ) / kletka x1 / sum x0 ;
    # dolgove znotraj »...« = navedek = priča ( ⟨BESEDA-⟡-NEDOTAKNJIVA⟩ ), масkirana iz števca
    pade = (len(k['izdaje']) == 5 and k['price'] == 2 and k['kletke'] == 1 and k['sumi'] == 0)
    poti = sys.argv[1:]
    for p in poti:
        porocilo.append('=' * 8)
        scan(p, preberi(p), porocilo)
    porocilo.append('=' * 8)
    porocilo.append('KANARCEK: ' + ('PADE rdece \u22A2 ( izdaje x5 + rekonstrukt x2 + kletka x1 ; dolgove na vrstici ⟡ = pri\u010Da, ne rana )'
                                    if pade else '\u26A0 NI Padel — INSTRUMENT MRTV'))
    print('\n'.join(porocilo))
    return 0 if pade else 1

if __name__ == '__main__':
    sys.exit(main())
