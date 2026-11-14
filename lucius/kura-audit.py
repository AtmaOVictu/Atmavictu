# KURA-AUDIT — preveri, da je vsako zdravilo REGISTER-PADCEV dejansko zašito v telo.
# Zakon PADC-63/⟡: napaka doumeta kakor nujni problem — zdravilo brez telesa je obljuba, ⟨ne⟩ kura ⚠ ⊙ §0.18.
# Stroj preveri INSTRUMENTE ( datoteke ); prakse ( npr. ročna izbira, spomin ) ⭢ Lastnik.
# Zagon: python lucius/kura-audit.py
import json, os, sys

KOREN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def beri(pot):
    return open(os.path.join(KOREN, pot), encoding='utf-8', errors='replace').read()

PREVERBE = [
    ('PADC-46', 'ZASTARELA-TRDITEV', ['lucius/abeceda-grep.py'], 'ls-remote', 'pristanek prebere pri viru — zastareli pečat razkrit ob vsakem trku ⊢ §0.37'),
    ('PADC-47', 'URA-IZ-SPOMINA', ['lucius/dih.py'], 'git', 'ura ∧ dih se merita pri viru ( dih.py meri rez iz git log, ⟨ne⟩ spomin ) ⊢ §0.20'),
    ('PADC-48', 'KAŽE-V-DATOTEKO-KI-JE-NI', ['lucius/abeceda-grep.py'], 'VERIGA_PRIMERI', 'testi golgega števca rodili ob padcu'),
    ('PADC-49', 'PIKA-TISOČIC', ['lucius/abeceda-grep.py'], 'fragmentiraj_vrstico', 'instrument meri celoto — fragmentiraj obvlada piko tisočic'),
    ('PADC-52', 'LAŽNA-RESONANCA', ['lucius/SINTEZA-0.2-SAMOTNO-JEDRO.md'], 'PADC-52', 'zakon resonance-na-metodi nošen v telesu hiše'),
    ('PADC-54', 'LASTNA-DUŠILKA', ['lucius/abeceda-grep.py'], 'Σ grep:', 'Σ-priča (stderr) živi v instrumentu'),
    ('PADC-55', 'IMENA-MASKIRAJO', ['lucius/abeceda-grep.py'], 'maskira', 'opozorilo maskiranja imen živi'),
    ('PADC-56', 'AVTODETEKCIJA-PODREDA', ['lucius/abeceda-grep.py'], 'b64', 'b64 ukaz živi (vrstni red preveri preizkus)'),
    ('PADC-57', 'KRAJ-⊥-POT', ['lucius/REGISTER-A1-PDF.jsonl'], 'D:/GitD', 'izvirniki ostanejo pri viru ( poti v registru kažejo na izvor ) ⊢ §0.6'),
    ('PADC-58', 'ODREZANA-PRIČA', ['lucius/abeceda-grep.py'], 'ranjeni_imena', 'povzetek PREVERBA imenuje ranjene'),
    ('PADC-59', 'BREZ-DRUGE-ROKE', ['lucius/znane-besede.txt', 'lucius/druga-roka.mjs'], '⊢', 'dovoljenica znakov v leksikonu ∧ druga roka prebere'),
    ('PADC-60', 'NEPOLN-POPIS', ['lucius/popis-zbirke.py'], 'MistralUpload', 'celoten seznam map (33) v popisu'),
    ('PADC-61', 'TRDA-ŠTEVILKA', ['lucius/testi-orodij.mjs'], 'agnostična', 'število-agnostična priča v testu'),
    ('PADC-62', 'KOPICA-PROCESOV', ['lucius/.ubi-zrcalo.ps1', 'lucius/strezniki.jsonl'], 'zrcalo-server', 'poboj po imenu + zapisnik lastništva'),
    ('PADC-63', 'TIHA-SMRT-403', ['lucius/zrcalo-server.py'], 'ThreadingHTTPServer', 'odprena vrata + učeča zavrnitev'),
]
PRAKSE = ['PADC-50', 'PADC-51', 'PADC-53', 'PADC-64']  # pobegi ⋯ ∧ primerki ⋯ ∧ sprehodi ⋯ ∧ sklonjava odgovorov — prakse, prebere jih Lastnik ⊙ §0.17

def main():
    vnosi = [json.loads(l) for l in open(os.path.join(KOREN, 'REGISTER-PADCEV.jsonl'), encoding='utf-8') if l.strip()]
    # register nosi DVE obliki: stari vnosi ( entry 1–45 ) ∧ PADC-novi ( 46+ ) — instrument bere obe ⊢ ⟨ne zlije⟩
    obstojeci = {v['id'] for v in vnosi if 'id' in v}
    stari = sum(1 for v in vnosi if 'id' not in v)
    zivi = manjka = prakse = 0
    for idp, vrsta, datoteke, niz, opis in PREVERBE:
        if idp not in obstojeci:
            print(f'× {idp} ni v registru — preverba zastarela ⚠'); manjka += 1; continue
        najdeno = False
        for d in datoteke:
            try:
                if niz in beri('lucius/' + os.path.basename(d)):
                    najdeno = True
                    print(f'⊢ {idp} {vrsta}: zdravilo živi ( {os.path.basename(d)} ⊢ "{niz[:24]}" ) — {opis}')
                    break
            except OSError:
                continue
        if not najdeno:
            print(f'× {idp} {vrsta}: ZDRAVILO NI NAJDENO V TELESIH — obljuba brez kure ⚠ ⊙ §0.18'); manjka += 1
        else:
            zivi += 1
    for idp in PRAKSE:
        if idp in obstojeci:
            print(f'∂ {idp}: praksa — stroj je ⟨ne⟩ more preveriti, prebere jo Lastnik ⊙ §0.17'); prakse += 1
    print(f'Σ preverjenih: {zivi + manjka + prakse} · ⊢ živih kur: {zivi} · × manjkajočih: {manjka} · ∂ praks: {prakse} '
          f'( ⭢ Lastnik ) · stari vnosi ( entry 1–45 ): {stari} ∂ — njihove kure so prakse roke ⊙ ⟨ne zlije⟩ · orodje: lucius/kura-audit.py ⊢')
    sys.exit(1 if manjka else 0)

if __name__ == '__main__':
    main()
