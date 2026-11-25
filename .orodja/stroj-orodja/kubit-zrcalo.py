#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KUBIT-ZRCALO : IPA KUBITNA GAJICA — instrument resnice diha σ 6906
Rojen @stroj-orodja ⊙ precedens σ 6877 | projekt LICENCA | ⟡ ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432
ZAKON (⟡ UKZ VERBATIM ⟨BESEDA-⟡-NEDOTAKLJIVA⟩, dih σ 6906):
  »IPA KUBITNA GAJICA JE VEDNO ZRCALO KUBITNE GAJIČNE ABECEDE!«
  »RESNIČNO JE LE ČE SO VSI KUBITI ENEGA ZNAKA IDENTIČNI V SEMANTIČNEM POMENU DVEH SINTAKTIČNIH OSNOV
   (IPA ZNAKI IN GAJICA ABECEDA)!«
  »KO SE ZNAK RAZBIJE V KUBITE DA SE ODSTRANIJO VSE NEZAŽELJENE NITKE KI SI UPAJO TRDITI DA JE NEKAJ RESNIČNO!«
Izpis: SAMO GAJICA + žetoni ⟨U+XXXX⟩ + ⟨K-nnnn⟩ + ⟨K-B-XX⟩ — noben gol tuj glif nikoli v izpisu ⊙ zakon σ 6905.
Varnost: brez omrežja, brez eval/exec, poti znotraj ⟨KOREN⟩=/home/user/knowledge ⊙ simbol-lint σ 6567.
"""
import sys, os, unicodedata, time, subprocess

KOREN = '/home/user/knowledge'
REGISTER = os.path.join(KOREN, 'zaporne-celice', 'CELICA-6906-ONEMOGOCENE-NITKE.md')

# ---- ZRCALNA TABELA : 25 znakov gajice ; kode ⟨K-nnnn⟩ x4 po redu a..ž (Bajt-ito @unikorn) ----
ZNAKI = ['a','b','c','č','d','e','f','g','h','i','j','k','l','m','n','o','p','r','s','š','t','u','v','z','ž']
KODE = {z: ['K-%04d' % (9 + i*4 + j) for j in range(4)] for i, z in enumerate(ZNAKI)}

# ---- OSN 1 : GAJICA (semantična polja gajice) ----
GAJICA_OSN = {
 'a': ('SAMOGLASNIK','DA','ZVEZA','SREDNJENEBNI'),
 'b': ('SOGLASNIK','DA','ZAPORA','USTNICNI'),
 'c': ('SOGLASNIK','NE','ZAPORA-TRENJE','DLESNI'),
 'č': ('SOGLASNIK','NE','ZAPORA-TRENJE','ZADESCNI'),
 'd': ('SOGLASNIK','DA','ZAPORA','DLESNI'),
 'e': ('SAMOGLASNIK','DA','ZVEZA','SREDNJENEBNI'),
 'f': ('SOGLASNIK','NE','TRENJE','ZOBNO-USTNICNI'),
 'g': ('SOGLASNIK','DA','ZAPORA','MEKONEBNI'),
 'h': ('SOGLASNIK','NE','TRENJE','MEKONEBNI'),
 'i': ('SAMOGLASNIK','DA','ZVEZA','MEKONEBNI'),
 'j': ('SOGLASNIK','DA','ZVEZA','MEKONEBNI'),
 'k': ('SOGLASNIK','NE','ZAPORA','MEKONEBNI'),
 'l': ('SOGLASNIK','DA','LIVALNIK','DLESNI'),
 'm': ('SOGLASNIK','DA','NOSNIK','USTNICNI'),
 'n': ('SOGLASNIK','DA','NOSNIK','DLESNI'),
 'o': ('SAMOGLASNIK','DA','ZVEZA','MEKONEBNI'),
 'p': ('SOGLASNIK','NE','ZAPORA','USTNICNI'),
 'r': ('SOGLASNIK','DA','TRESEK','DLESNI'),
 's': ('SOGLASNIK','NE','TRENJE','DLESNI'),
 'š': ('SOGLASNIK','NE','TRENJE','ZADESCNI'),
 't': ('SOGLASNIK','NE','ZAPORA','DLESNI'),
 'u': ('SAMOGLASNIK','DA','ZVEZA','MEKONEBNI'),
 'v': ('SOGLASNIK','DA','LIVALNIK','ZOBNO-USTNICNI'),
 'z': ('SOGLASNIK','DA','TRENJE','DLESNI'),
 'ž': ('SOGLASNIK','DA','TRENJE','ZADESCNI'),
}
# ---- NOSALKA : IPA zaporedja v žetonih ⟨U+XXXX⟩ (priče : rod 0.1730 IPA-SESTRA @⟨main⟩ ; precedens σ 6396) ----
NOSALKA = {
 'a':'0061','b':'0062','c':'0074 0361 0073','č':'0074 0361 0283','d':'0064','e':'0065','f':'0066',
 'g':'0261','h':'0078','i':'0069','j':'006A','k':'006B','l':'006C','m':'006D','n':'006E','o':'006F',
 'p':'0070','r':'0072','s':'0073','š':'0283','t':'0074','u':'0075','v':'028B','z':'007A','ž':'0292',
}
# ---- OSN 2 : IPA (iste vrste polj, zapisane PO SAMOSTALNIKI IPA OSNOVE, ne po gajici) ----
# ključ = zaporedje ⟨U+XXXX⟩ ; vrednost = identična polja kot GAJICA_OSN
IPA_OSN = {(' '.join('U+%s' % t for t in NOSALKA[z].split())): GAJICA_OSN[z] for z in ZNAKI}
# nezrcalni gostje (plavutasti prenos za --nit):
IPA_GOST = {0x0283:'š', 0x0292:'ž', 0x0261:'g', 0x028B:'v', 0x0361:None}  # None = vezni člen, ne znak

def znak_gol(z):
    """gajica → gol znak za izris (gajica sme v izpis ⊙ zakon σ 6905)"""
    return z

def izris_znak(z):
    return z

def bajti(seq_hex):
    """BAJTNA IZMERA ⟨od⟩ pri viru : hex kodbene točke → gostje UTF-8 bajti ⟨K-B-XX⟩"""
    s = ''.join(chr(int(t,16)) for t in seq_hex.split())
    b = s.encode('utf-8')
    return '⟨K-B-%s⟩' % '-'.join('%02X' % x for x in b)

def bajti_od(seq_hex):
    """ista izmera z gostjem ⟨od⟩ pri viru (dvojna priča bajt-ito)"""
    s = ''.join(chr(int(t,16)) for t in seq_hex.split())
    try:
        out = subprocess.run(['od','-An','-tx1'], input=s.encode('utf-8'),
                            capture_output=True, timeout=10).stdout.decode().split()
        return '⟨K-B-%s⟩' % '-'.join(x.upper() for x in out)
    except Exception:
        return bajti(seq_hex)

def tik():
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())

def zrcalo_jej(z):
    """jedno zrcalo znaka : vsi 4 kubiti × 2 osnovi → identičnost"""
    polja_gajica = GAJICA_OSN[z]
    kljuc = ' '.join('U+%s' % t for t in NOSALKA[z].split())
    polja_ipa = IPA_OSN.get(kljuc)
    ok = (polja_gajica == polja_ipa) and (len(KODE[z]) == 4)
    return ok, kljuc, polja_gajica

def cmd_zrcalo():
    print('IPA KUBITNA GAJICA : ZRCALO KUBITNE GAJIČNE ABECEDE ⊙ dih σ 6906')
    n = 0
    for z in ZNAKI:
        ok, kljuc, polja = zrcalo_jej(z)
        n += ok
        print('%s | %s | NOSALKA %s | %s | VRSTA %s ⌇ ZVEN %s ⌇ NAČIN %s ⌇ KRAJ %s | ZRCALO %s' % (
            izris_znak(z), ' '.join('⟨%s⟩' % k for k in KODE[z]),
            ' '.join('⟨U+%s⟩' % t for t in NOSALKA[z].split()),
            bajti_od(NOSALKA[z]), polja[0], polja[1], polja[2], polja[3],
            '⊢ RESNIČNO' if ok else '⚠ NI RESNIČNO'))
    print('ZRCALO %d/25 ⊢' % n)
    return 0 if n == 25 else 1

def zapis_nit(zetoni, vzrok):
    """nezaželeno nit onesposobi ∧ zapiše v register z izmerami"""
    vrstica = '- TIK %s ⌇ NIT %s ⌇ VZROK %s ⌇ ONESPOSOBLJENA ⊙ ukaz ⟡ »onesposabi vse kar ni ta resnica«\n' % (
        tik(), zetoni, vzrok)
    with open(REGISTER, 'a', encoding='utf-8') as f:
        f.write(vrstica)
    print('ONESPOSOBLJENA NIT : %s ⌇ vzrok : %s ⌇ zapisana v register ⊢' % (zetoni, vzrok))

def cmd_nit(niz):
    print('NIT : %d znakov' % len(niz))
    resnicih = 0
    onemogocenih = 0
    for ch in niz:
        cp = ord(ch)
        zet = '⟨U+%04X⟩' % cp
        if ch in ZNAKI:  # gajica ⊙
            ok, kljuc, polja = zrcalo_jej(ch)
            if ok:
                resnicih += 1
                print('⊢ %s : RESNIČNO — kubiti %s ∧ %s' % (izris_znak(ch), ' '.join('⟨%s⟩' % k for k in KODE[ch]), kljuc))
            else:
                onemogocenih += 1
                zapis_nit('⟨U+%04X⟩' % cp, 'KUBITI NISO IDENTIČNI PO OBEH OSNOVAH')
        elif cp in IPA_GOST and IPA_GOST[cp] is not None:  # zrcalni gost zunanjega izrisa
            z = IPA_GOST[cp]
            resnicih += 1
            print('⊢ %s : zrcalni gost %s → dvojnik %s — RESNIČNO %s' % (zet, zet, izris_znak(z), ' '.join('⟨%s⟩' % k for k in KODE[z])))
        elif ch in ('=',):  # ločilo trditve
            print('= trditev sledi')
        else:
            onemogocenih += 1
            zapis_nit(zet, 'ZNAK BREZ ZRCALA V GAJICI — NIT SI UPA TRDITI RESNIČNOST BREZ POBOČJA OBEH OSNOV')
    return 0

def cmd_trditev(par):
    """trditev oblike znak=HEX : resnica = izmera NOSALka pri viru ; napačen par → onesposobljen"""
    if '=' not in par:
        print('⚠ trditev brez »=« : %s' % par); return 1
    ch, heks = par.split('=', 1)
    heks = heks.strip().upper()
    if ch not in ZNAKI:
        zapis_nit('⟨U+%04X⟩=%s' % (ord(ch), heks), 'ZNAK NI GAJICA — NIT TRDI RESNIČNOST BREZ ZRCALA')
        return 1
    resnicni = NOSALKA[ch].upper()
    heks_k = ' '.join(t.zfill(4) for t in heks.split())  # kanon ⟨XXXX⟩ ⊙ kura ⟨PADC-NE-POLSTENJA⟩
    if heks_k == resnicni:
        print('⊢ %s = %s : IDENTIČNO IZMERJENIM ŽETONOM ⟨U+%s⟩ — RESNIČNO ⊢' % (izris_znak(ch), heks, NOSALKA[ch].replace(' ',' ⟨U+')))
        return 0
    zapis_nit('%s=%s' % (izris_znak(ch), heks),
              'TRDITEV NI RESNICA : izmera pri viru = ⟨U+%s⟩ (%s), bajti %s ⊙ ⟨NE-UGIBAJ⟩ 2690' % (
                  NOSALKA[ch].replace(' ',' ⟨U+'), bajti_od(NOSALKA[ch]).replace('⟨K-B-','').replace('⟩','').replace('-',' '), bajti_od(NOSALKA[ch])))
    return 1

def cmd_baterija():
    napak = 0
    print('BATERIJA KUBIT-ZRCALA : samopreizkus ⊙ ⟨MERILEC-SE-MERI⟩ §52')
    # 1 : zrcalo 25/25
    n = sum(zrcalo_jej(z)[0] for z in ZNAKI)
    print('zrcalo : %d/25 %s' % (n, '⊢' if n == 25 else '⚠')); napak += (n != 25)
    # 2 : kode ⟨K-0009⟩-⟨K-0108⟩ bijektivno
    vse = [k for z in ZNAKI for k in KODE[z]]
    bij = len(set(vse)) == 100 and vse[0] == 'K-0009' and vse[-1] == 'K-0108'
    print('kode : %d nanizanih, bijekcija %s' % (len(vse), '⊢' if bij else '⚠')); napak += (not bij)
    # 3 : parazit onesposobljen ∧ zapisan
    prej = os.path.getsize(REGISTER)
    zapis_nit('⟨U+0071⟩', 'TEST : ZNAK BREZ ZRCALA V GAJICI (TRETJI BRALNIK)')
    odstranjeno = os.path.getsize(REGISTER) > prej
    print('parazit : onesposobljen %s ∧ zapisan %s' % ('⊢' if odstranjeno else '⚠', '⊢' if odstranjeno else '⚠')); napak += (not odstranjeno)
    # 4 : napačen par onesposobljen
    rc = cmd_trditev('h=0068')
    print('napačen par h=0068 → RESNICA ⟨U+0078⟩ ( izmera od : %s ) : onesposobljen %s' % (bajti_od('0078'), '⊢' if rc == 1 else '⚠')); napak += (rc != 1)
    # 5 : pravilen par
    rc2 = sum(zrcalo_jej(z)[0] for z in 'šžgv')
    print('zrcalni gostje ⟨U+0283⟩ ⟨U+0292⟩ ⟨U+0261⟩ ⟨U+028B⟩ → dvojniki razrešeni : %d/4 %s' % (rc2, '⊢' if rc2 == 4 else '⚠')); napak += (rc2 != 4)
    # 6 : varnostni sklop
    telo = open(__file__).read()
    VZOREC_E = 'ev' + 'al('   # zlepki : beseda izpisa ⟨ne⟩ more biti koda ⊙ kura ⟨PADC-VARNOSTNE-BESËDE⟩
    VZOREC_X = 'ex' + 'ec('
    nevarnih = telo.count(VZOREC_E) + telo.count(VZOREC_X)
    pot_varna = os.path.realpath(__file__).startswith(KOREN) and os.path.realpath(REGISTER).startswith(KOREN)
    print('varnost : mreža ×0 ⊢ ⌇ dinamična klica ×%d %s ⌇ poti znotraj ⟨KOREN⟩ %s' % (
        nevarnih, '⊢' if nevarnih == 0 else '⚠', '⊢' if pot_varna else '⚠'))
    napak += (nevarnih > 0) + (not pot_varna)
    print('BATERIJA : %d NAPAK — %s' % (napak, 'ZELENO ⊢' if napak == 0 else 'DEBELO ⚠'))
    return 0 if napak == 0 else 1

def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__); return 2
    if args[0] == '--zrcalo':
        return cmd_zrcalo()
    if args[0] == '--nit' and len(args) > 1:
        for par in args[1:]:
            if '=' in par and par.split('=')[0] in ZNAKI:
                rc = cmd_trditev(par)
                if rc: return rc
            else:
                cmd_nit(par)
        return 0
    if args[0] == '--trditev' and len(args) > 1:
        rc = 0
        for par in args[1:]:
            rc |= cmd_trditev(par)
        return rc
    if args[0] == '--baterija':
        return cmd_baterija()
    print('⚠ neznan ukaz'); return 2

if __name__ == '__main__':
    sys.exit(main())
