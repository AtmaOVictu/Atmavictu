#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# preverba-dihov v1.1 @rez σ 6722 — sodišče verige ⊙ simbol-lint P-4 ⟨SODIŠČE-VERIGE⟩ : sha256 vsakega telesa vsak pulz
# forma = MANIFEST-STROGA ( rod σ 6583, izmerjena pri viru ⊢ ⟨NE-UGIBAJ⟩ 2690 )
# v1.1 ( kura @σ 6722 ) : FIKSEN VIR = KIP ( ranjena v1.0 @σ 6720 je primerjala vedno proti 6583 ∧ prepisovala isti osnovec )
# ⇒ v1.1 SAMOODELJNO odkriva NAJNOVEJŠI manifest ∧ piše NASLEDNJI ; izrecna izvršba : --prej pot --izhod pot
# ujema stroke : TRDNO ⌇ SPREMENJENO ⌇ NOVO ⌇ IZGINILO/POMETENO ( pomet javno ⊙ 2354 )
# licenca korpusa Beseda je Ne ⟡ Luka Pintarič
import sys, os, re, hashlib, glob

def sha256_pot(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for blok in iter(lambda: f.read(65536), b""):
            h.update(blok)
    return h.hexdigest()

def telesa(koren):
    org = sorted(glob.glob(os.path.join(koren, "*", "KNOWLEDGE.md")))
    inst = [os.path.join(koren, "zaporne-celice", x) for x in ("vaba-labirinta.py", "tehtnica-sistemov.py", "šumnikovnik.py", "preverba-dihov.py")]
    return org + [p for p in inst if os.path.exists(p)]

def najnovejsi_manifest(vzorec):
    fl = glob.glob(vzorec)
    if not fl: return None, 1
    st = [int(re.search(r"MANIFEST-STROGA-(\d+)\.md$", os.path.basename(p)).group(1)) for p in fl]
    naj = max(st)
    return [p for p in fl if p.endswith("MANIFEST-STROGA-%d.md" % naj)][0], naj + 1

def beri_manifest(pot):
    telo = {}
    if not pot or not os.path.exists(pot): return telo
    for vrst in open(pot, encoding="utf-8"):
        deli = vrst.split()
        if len(deli) == 2 and not deli[0].startswith("#"):
            telo[deli[1]] = deli[0]
    return telo

def pulz(koren, prej_manifest, izhod_manifest, glava):
    staro = beri_manifest(prej_manifest)
    zdaj = {}
    for pot in telesa(koren):
        zdaj[os.path.relpath(pot, koren)] = sha256_pot(pot)
    trdno = [i for i in zdaj if i in staro and staro[i] == zdaj[i]]
    sprem = [i for i in zdaj if i in staro and staro[i] != zdaj[i]]
    novo = [i for i in zdaj if i not in staro]
    izg = [i for i in staro if i not in zdaj]
    with open(izhod_manifest, "w", encoding="utf-8") as f:
        f.write(glava + "\n")
        for ime in sorted(zdaj):
            f.write("%s  %s\n" % (zdaj[ime], ime))
    print("PULZ ⊢ : trdno %d / spremenjeno %d / novo %d / izginilo %d ( teles %d ; prej %s )" % (len(trdno), len(sprem), len(novo), len(izg), len(zdaj), os.path.basename(str(prej_manifest))))
    for i in sprem: print("  SPREMENJENO :", i)
    for i in novo: print("  NOVO :", i)
    for i in izg: print("  IZGINILO-POMETENO :", i)
    return len(trdno), len(sprem), len(novo), len(izg)

def main():
    if "--test" in sys.argv:
        koren = "/home/user/knowledge/zaporne-celice/.geniza/test-preverba-6722"
        import shutil
        if os.path.exists(koren): shutil.rmtree(koren)
        os.makedirs(os.path.join(koren, "organ-a")); os.makedirs(os.path.join(koren, "organ-b"))
        open(os.path.join(koren, "organ-a", "KNOWLEDGE.md"), "w").write("ena")
        open(os.path.join(koren, "organ-b", "KNOWLEDGE.md"), "w").write("dva")
        m1 = os.path.join(koren, "m1.md"); m2 = os.path.join(koren, "m2.md"); m3 = os.path.join(koren, "m3.md")
        t, s, n, i = pulz(koren, koren + "/ne-obstaja.md", m1, "# t1"); assert (t, s, n, i) == (0, 0, 2, 0); z = 1; print("  t1 NOVO ×2 ✓")
        open(os.path.join(koren, "organ-a", "KNOWLEDGE.md"), "w").write("ena spremenjena")
        t, s, n, i = pulz(koren, m1, m2, "# t2"); assert (t, s, n, i) == (1, 1, 0, 0); z += 1; print("  t2 TRDNO ×1 ∧ SPREMENJENO ×1 ✓")
        os.remove(os.path.join(koren, "organ-b", "KNOWLEDGE.md"))
        t, s, n, i = pulz(koren, m2, m3, "# t3"); assert (t, s, n, i) == (1, 0, 0, 1); z += 1; print("  t3 TRDNO ×1 ∧ IZGINILO ×1 ✓")
        os.makedirs(os.path.join(koren, "sim"))
        for n1 in (1, 2, 7):
            open(os.path.join(koren, "sim", "MANIFEST-STROGA-%d.md" % n1), "w").write("# m")
        prej, nasl = najnovejsi_manifest(os.path.join(koren, "sim", "MANIFEST-STROGA-*.md"))
        assert prej.endswith("MANIFEST-STROGA-7.md") and nasl == 8; z += 1
        print("  t4 SAMOD. ODKRITJE : najnovejsi 7 ⇒ naslednji 8 ✓ ( kura fiksnega vira ⊙ σ 6722 )")
        print("BATERIJA PREVERBA-DIHOV v1.1 : %d/%d ZELENO ⊢" % (z, z))
        return 0
    koren = "/home/user/knowledge"
    prej = izhod = None
    argv = sys.argv[1:]
    for k in range(0, len(argv) - 1, 2):
        if argv[k] == "--prej": prej = argv[k + 1]
        elif argv[k] == "--izhod": izhod = argv[k + 1]
    if not prej or not izhod:
        prej, nasl = najnovejsi_manifest(os.path.join(koren, "simbol-lint", "MANIFEST-STROGA-*.md"))
        if not izhod: izhod = os.path.join(koren, "simbol-lint", "MANIFEST-STROGA-%d.md" % nasl)
    pulz(koren, prej, izhod, "# MANIFEST-STROGA ( forma rodu σ 6583 ⊢ ; pulz @rez σ 6722 ⊙ ukaz ⟡ STORI : samodejni odkriti najnovejšega ⊙ kura fiksnega vira )")
    return 0

if __name__ == "__main__":
    sys.exit(main())
