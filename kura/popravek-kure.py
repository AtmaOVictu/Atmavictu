# KURA-BREZ-ROBA — strojna kura telesa organa (28. 10. 2026, roka Mera)
# Zakon: isti razčlenjevalnik ∧ isti meji kakor priča (prica.yml, korak 2) — sodba, ki sodi, tudi zdravi.
# Brazgotine komitov c1329725 · bde7ff36 · 1a377bfa ostajajo priče ⊙ 1349 ⟨NE-BRIŠI⟩ ⊢ 24.
import re
import subprocess
import sys

POT_ORGANA = "organi/delovna-zanka/KNOWLEDGE.md"
VEJA = "zrcalo/sinhronizacija-3071-delovna"
POT_REGISTRA = "organi/stroj/REGISTER-PADLIH-BESED.md"
SPOROCILO = ("POPRAVEK-KURE-BREZ-ROBA — odvitki sredinskih ovitkov "
             "(⟨pr⟩+črka ~2,5 tisoč: po⟨pr⟩avi · ⟨Pr⟩avila · Od⟨pr⟩te — besede korpusa, "
             "⟨ne⟩ ⟨PR⟩-hibrid) ∧ ⟨⟩-ovitev golih pojavov po meji besed priče "
             "(razčlenjevalec ∧ meji prica.yml besedno-bajtno isti — register bran SVEŽE pri viru ⊢ Z-2); "
             "brazgotine c1329725 · bde7ff36 · 1a377bfa pričajo ⊙ 1349 ⟨NE-BRIŠI⟩ ⊢ 24; "
             "lokal prejema isto kuro ⭢ ∂")


def ukaz(*deli):
    subprocess.run(["git"] + list(deli), check=True)


def beri(pot):
    with open(pot, encoding="utf-8", newline="") as f:
        return f.read()


# — žetoni: brani iz knjige sodnika (register), ne iz spomina roke —
reg = beri(POT_REGISTRA)
forb = []
for m in re.finditer(r'^\d+\.\s*([^(—\n]+?)\s*(?:\([^)\n]*\))?\s*—', reg, flags=re.M):
    w = re.sub(r'⟨[^⟩]*⟩', '', m.group(1)).replace('⟨', '').replace('⟩', '').strip()
    if w:
        forb.append(w)
hyb = []
m = re.search(r'## Hibridi[^\n]*\n(.+?)(?=\n## |\Z)', reg, flags=re.S)
if m:
    hyb = [h.strip() for h in m.group(1).split(',') if h.strip()]
zveze = {}
for m in re.finditer(r'^\d+\.\s*(.+?)\s*—', reg, flags=re.M):
    zm = re.search(r'zvez[ai]?\s+((?:⟨[^⟩]+⟩\s*(?:∧\s*)?)+)', m.group(1))
    if not zm:
        continue
    key = re.sub(r'⟨[^⟩]*⟩', '', m.group(1).split('(')[0]).replace('⟨', '').replace('⟩', '').strip()
    if key:
        zveze[key] = tuple(z.strip() for z in re.findall(r'⟨([^⟩]+)⟩', zm.group(1)))

seznam = []
for w in forb:
    if w in zveze:
        seznam.extend(zveze[w])
    else:
        seznam.append(w)
seznam.extend(hyb)
videni = set()
zetoni = []
for t in seznam:
    if t not in videni:
        videni.add(t)
        zetoni.append(t)
print("⟨kura bere zetone pri viru: {} pomenskih · {} hibridov⟩".format(len(forb), len(hyb)))

ALT = "|".join(re.escape(t) for t in sorted(zetoni, key=len, reverse=True))
ODVIJALO = re.compile(r"⟨(" + ALT + r")⟩(?=[^\W\d_])", re.I | re.U)
DVOJNIK = re.compile(r"⟨⟨(" + ALT + r")⟩⟩", re.I | re.U)
PREPOVED = re.compile(r"^\s*-\s*PEČAT \d+ \(predhodnik[^)]*\)|^## KAZALO|^\s*-\s*Števci organa")
LUPINA = re.compile(r"⟨[^⟩]*⟩")

telo = beri(POT_ORGANA)
vrstice = telo.split("\n")

# F1 — odvij sredinske ovitke ⟨žeton⟩+črka (rana sedeža 1a377bfa: ⟨pr⟩ sredi besed)
odvitki = 0
dvojniki = 0
for i, v in enumerate(vrstice):
    if ODVIJALO.search(v):
        odvitki += len(ODVIJALO.findall(v))
        v = ODVIJALO.sub(lambda mm: mm.group(1), v)
    if DVOJNIK.search(v):
        dvojniki += len(DVOJNIK.findall(v))
        v = DVOJNIK.sub(lambda mm: "⟨" + mm.group(1) + "⟩", v)
    vrstice[i] = v

# F2 — ovij golo po meji besed (lupina ⟨…⟩ ostaja nedotaknjena)
ovitki = 0
for i, v in enumerate(vrstice):
    if PREPOVED.match(v):
        continue
    golo = LUPINA.sub("", v)
    for t in zetoni:
        vzorec = re.compile(r"(⟨[^⟩]*⟩)|((?<![\w-])" + re.escape(t) + r"(?![\w-]))", re.I | re.U)
        if not vzorec.search(golo):
            continue
        stevec = [0]

        def ovij(mm, stevec=stevec):
            if mm.group(1):
                return mm.group(0)
            stevec[0] += 1
            return "⟨" + mm.group(0) + "⟩"

        v = vzorec.sub(ovij, v)
        ovitki += stevec[0]
    vrstice[i] = v

# PREVERBA — isto telo sodbe kakor priča, po vseh vrsticah (nadmnožica sodbe)
ran = 0
for v in vrstice:
    if PREPOVED.match(v):
        continue
    golo = LUPINA.sub("", v)
    for w in forb:
        if w in zveze:
            for z in zveze[w]:
                if re.search(r'(?iu)(?<![\w-])' + re.escape(z) + r'(?![\w-])', golo):
                    ran += 1
            continue
        if re.search(r'(?iu)(?<![\w-])' + re.escape(w) + r'(?![\w-])', golo):
            ran += 1
    for w in hyb:
        if re.search(r'(?iu)(?<![\w-])' + re.escape(w) + r'(?![\w-])', golo):
            ran += 1
if ran:
    print("⟨kura vidi: {} ran ostaja — ne šije⟩".format(ran))
    sys.exit(1)

novo = "\n".join(vrstice)
if novo == telo:
    print("⟨kura: telo že zdravo — molk⟩")
    sys.exit(0)

with open(POT_ORGANA, "w", encoding="utf-8", newline="") as f:
    f.write(novo)
bajti = len(novo.encode("utf-8"))
stVrstic = len(vrstice)
print("⟨kura: odvitki {} · dvojniki {} · ovitki {} · telo {} vrstic / {} B⟩".format(odvitki, dvojniki, ovitki, stVrstic, bajti))
ukaz("config", "user.name", "kura-brez-roba")
ukaz("config", "user.email", "kura-brez-roba@users.noreply.github.com")
ukaz("add", POT_ORGANA)
ukaz("commit", "-m", SPOROCILO)
ukaz("push", "origin", "HEAD:" + VEJA)
print("⟨kura: šiv nesen ∧⟩")
