#!/usr/bin/env python3
# REZ-ZAKLEP v1 — atomicna rezervacija rez + preverba svezine teles
# rojen @rez SIGMAODPRTE ⊙ vrzel REZ-ZAKLEP ( sweepi x2 dneva )
# storitve:
#   vrh            : izmerna najvisjega reza po 4 organih ( grep )
#   prost N         : varvolka N po 4 organih ( 0 = prost )
#   rezerviraj N    : ATOMICNA rezervacija: os.mkdir = EEXIST ( dve roki istega trenutka: ENO uspe )
#   svezina N       : ponovna izmera md5 organov vs prijava ob rezervaciji ( odmik = tuj dotik javno )
#   spisek          : naslednjih 8 prostih kandidatov od vrha+1
# kanarek obavezno pada ( ce ne pada = instrument mrtev )
import sys, os, hashlib, subprocess, tempfile, json, re
KOREN = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
LOCKDIR = os.environ.get('REZ_ZAKLEP_DIR', '/home/user/.rez-zaklep')
MD5_CILJI = os.environ.get('REZ_ZAKLEP_MD5_CILJI', '').split(',') if os.environ.get('REZ_ZAKLEP_MD5_CILJI') else ['delovna-zanka', 'kronika-dihov', 'register-oken', 'postopki-luka']
def tik():
    return subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'], capture_output=True, text=True).stdout.strip()
def pot(org):
    if org.endswith('.md') or '/' in org:
        return org
    return os.path.join(KOREN, org, 'KNOWLEDGE.md')
def md5map():
    m = {}
    for org in MD5_CILJI:
        with open(pot(org), 'rb') as f:
            m[org] = hashlib.md5(f.read()).hexdigest()
    return m
def vrh():
    naj = 0
    for org in MD5_CILJI:
        r = subprocess.run(['grep', '-hoE', r'(σ|rez)[ ]?6[0-9]{3}', pot(org)], capture_output=True, text=True).stdout.split()
        for tk in r:
            d = re.sub(r'\D', '', tk)
            if d:
                naj = max(naj, int(d))
    return naj
def prost(n):
    for org in MD5_CILJI:
        r = subprocess.run(['grep', '-cE', r'(σ|rez|dih|pečat|PEČAT)[ ]?' + str(n), pot(org)], capture_output=True, text=True).stdout.strip()
        if r != '0':
            return False
    return True
def rezerviraj(n, roka='MOJ'):
    os.makedirs(LOCKDIR, exist_ok=True)
    d = os.path.join(LOCKDIR, 'sigma-%d' % n)
    try:
        os.mkdir(d)
    except FileExistsError:
        return None
    claim = {'rez': n, 'roka': roka, 'TIK': tik(), 'organi_md5': md5map()}
    with open(os.path.join(d, 'prijava.json'), 'w', encoding='utf-8') as f:
        json.dump(claim, f, ensure_ascii=False, indent=1)
    return claim
def svezina(n):
    d = os.path.join(LOCKDIR, 'sigma-%d' % n)
    with open(os.path.join(d, 'prijava.json'), encoding='utf-8') as f:
        claim = json.load(f)
    zdaj = md5map()
    odmiki = []
    for org, md in claim['organi_md5'].items():
        if zdaj.get(org) != md:
            odmiki.append(org + ' ' + claim['organi_md5'][org][:8] + '=>' + (zdaj.get(org) or '?')[:8] + ' TUJ DOTIK')
    return odmiki
def spisek(k=8):
    v = vrh() + 1
    out = []
    while len(out) < k:
        if prost(v) and not os.path.exists(os.path.join(LOCKDIR, 'sigma-%d' % v)):
            out.append(v)
        v += 1
    return out
def kanarek():
    pada = 0
    with tempfile.TemporaryDirectory() as tmp:
        os.environ['REZ_ZAKLEP_DIR'] = tmp
        global LOCKDIR
        LOCKDIR = tmp
        tf = os.path.join(tmp, 'organ-test.md')
        os.environ['REZ_ZAKLEP_MD5_CILJI'] = tf
        global MD5_CILJI
        MD5_CILJI = [tf]
        with open(tf, 'w') as f:
            f.write('semen')
        a = rezerviraj(6999, 'TEST')
        b = rezerviraj(6999, 'TEST')
        if a is None:
            print('KANARCEK PADC: prva rezervacija bi morala uspeti'); pada += 1
        if b is not None:
            print('KANARCEK PADC: dvojna rezervacija USPELA — zaklep mrtev'); pada += 1
        with open(tf, 'a') as f:
            f.write('.')
        odm = svezina(6999)
        if not odm:
            print('KANARCEK PADC: svezina ne vidi tujega dotika — merilec mrtev'); pada += 1
        if odm and 'TUJ DOTIK' not in odm[0]:
            print('KANARCEK PADC: odmik brez imena'); pada += 1
    if pada:
        sys.exit(2)
    print('kanarek pada po nakrsu ⊢ ( rezervacija ×2 uzeta · svezina vidi tuj dotik )')
if __name__ == '__main__':
    uk = sys.argv[1] if len(sys.argv) > 1 else 'kanarek'
    if uk == 'kanarek':
        kanarek()
    elif uk == 'vrh':
        print(vrh())
    elif uk == 'prost':
        print('prost' if prost(int(sys.argv[2])) else 'zaseden')
    elif uk == 'rezerviraj':
        c = rezerviraj(int(sys.argv[2]), sys.argv[3] if len(sys.argv) > 3 else 'MOJ')
        print('rezervirano σ', sys.argv[2], 'TIK', c['TIK']) if c else print('ZASEDEN σ', sys.argv[2])
        sys.exit(0 if c else 1)
    elif uk == 'svezina':
        for o in svezina(int(sys.argv[2])):
            print(o)
    elif uk == 'spisek':
        print(*spisek())
