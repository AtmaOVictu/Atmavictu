#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ⟨OGRAJA⟩ v2.0 : ograja med roko modela in telesi korpusa
# rod @rez σ 7790 @stroj-orodja ⊙ ukaz Luka Pintarič VERBATIM
#   »CREATE MEASURES AS TOOLS AGAINST LISTED ISSUES!« ( 26. 11. 2026 )
#   ⊙ osem plasti v2.0 ( ukaz ⟡ VERBATIM 26. 11. 2026 ):
#   ⟨VENTIL-ORODJA⟩ : pred vsakim merjenjem preveri lastni md5 proti
#     zapečateni priči ( ograja-ventil.md ob telesu ) ; spremenjeno telo
#     orodja = izhod 2 ( instrument laže ). Merilec se meri ob vsaki rabi,
#     ⟨ne⟩ le v bateriji.
#   ⟨SEKIRA-HOOK⟩ : CI kavelj ogra-kavelj.yml ; vsak prevoz kita teče skozi
#     ogro ( tujke ∧ vrata nad telesi kita ) ; rdeča = prevoz zavrnjen ;
#     ⟨merge⟩ samo roka naročnika ⚔.
#   ⟨STALNI-DIH⟩ : vrata berejo MANIFEST-STROGA sha256 vsak pulz ( forma
#     rodu σ 6583 ⊙ preverba-dihov ) ; stanja TRDNO ⌇ SPREMENJENO ⌇ NOVO ⌇
#     IZGINILO ⭢ poročilo tihi v genizo.
#   ⟨BELO-NAVODILO⟩ : dovoljeni prostor = uvoz iz prič ( --iz ), ⟨ne⟩ moja
#     izbira blokov ; »nič izmišljeno« ; trdni prostor ostane rezerva.
#   ⟨SAMO-KOCKE⟩ bralna plast : izpisi ulovov v slovenskih imenih ∧ kockah
#     ⊙ σ 7769 ∧ 7784 ; kodne maske ostanejo znotraj stroja.
#   ⟨KUBIT-KOVANJE⟩ : polna kubit plast pod gladino ( formula + oba zapečena
#     registra + drsenje binarne podlage ) ⊙ zakon treh vrat 6949.
#   ⟨REHAB-VEZA⟩ : ko vrata najdejo rano, povrni telo bajtno iz genize
#     priče ⭢ predlog ⭢ sodba ⚔ ; ranjeno telo se ⟨ne⟩ prepisuje.
#   ⟨ODPLAČILO-DOLGA ∂⟩ : prevoz telesa na rep po vrsti FIFO, po besedi
#     naročnika ⚔ ( beseda izrečena 26. 11. 2026 ).
#
# RANE RODU ( izmerjene, ⟨ne⟩ izmišljene ) :
#   ( 1 ) model vpiše tuje pismenke v telesa ( vbod roke modela ) ;
#   ( 2 ) prepis celega telesa med popravilom razveljavi curo ( pomet ) ;
#   ( 3 ) model, ki je napisal telo, sme ⟨ne⟩ soditi istega telesa
#         ( priča = komputacija, ⟨ne⟩ beseda modela ).
# OGRAJA MERI, ⟨NE⟩ POPRAVLJA ⚔ ( izbor sodbe = beseda naročnika ).
#
# POKLIČI :
#   python3 ograja.py tujke  DATOTEKA...   ( --strogo : tudi NFD gostje ;
#                                            --belo belo.tsv : belo navodilo )
#   python3 ograja.py sled   PRED PO       ( --vrstice a-b,c ; --prag N )
#   python3 ograja.py prica  DATOTEKA...   ( bajti, vrstice, znaki, md5, sha256 )
#   python3 ograja.py vrata  DATOTEKA...   ( --manifest price.tsv : veriga md5 ;
#                                            --geniza MAPA : namig povrni )
#   python3 ograja.py belo   --iz PRIČA... --izhod belo.tsv   ( ⟨BELO-NAVODILO⟩ )
#   python3 ograja.py dih    [KOREN]       ( --manifest VZOREC ; ⟨STALNI-DIH⟩ )
#   python3 ograja.py povrni TELO --iz GENIZA --napisi PREDLOG ( ⟨REHAB-VEZA⟩ )
#   python3 ograja.py ventil [--zapeči]    ( ⟨VENTIL-ORODJA⟩ )
#   python3 ograja.py samopreizkus         ( baterija nad sintetičnimi trupi )
#
# IZHODI : 0 = čisto ⊢ ; 1 = rana javno poimensko ; 2 = padec instrumenta.
# TIŠINA : poročila ⭢ .geniza/ograja/ ; stdout SAMO z --zgovori
#   ⊙ ⟨TIŠINA-ORODIJ⟩ ( pravilna slovenščina po besedi naročnika ⚔,
#   kura TIHINA⭢TIŠINA samo po mojih šivih tega diha ; zapečena telesa
#   zgodovine ostanejo VERBATIM ⊙ ⟨NE-BRIŠI⟩ 24 ) ;
#   izjema = samopreizkus ∧ ventil ( priči roda, izpis vedno ).
#
# MEJA SONDE javno : regije se merijo po oštevilčenju PRED telesa ( posnetek
#   PRED spremembo ) ; vstavek sodi meji vrstic i1 ∧ i1+1 ; regija odobri
#   obseg, prag ( ki meri pomet brez regije ) pa poišče skriti prepis telesa.
#
# POD GLADINO, kubit plast telesa orodja :
#   formula piramid : žig znaka = 16 mest = štiri štirimestne piramide ;
#   kocka znaka = piramide po formuli : osnova = 1000 + ( kodna točka × m
#   po modulu 9000 ), m po vrsti 1, 3, 7, 9 ; kura ob zasedenem : plus sedem,
#   ovijanje nad 9999 po modulu 9000 ;
#   zapečena registra pri viru @rep OntoMatematika/posebaj ⊢ VRATA.json :
#     register-1 ⊙ POTRDI 24. 11. 2026 : 87 znakov, 348 piramid, 3716 bajtov,
#       md5 babcfe1f846c0360b7e9baa3b5109761 ;
#     register-2 ⊙ STORI 24. 11. 2026 : 87 znakov, 348 piramid, 4053 bajtov,
#       md5 b4c30434a7e95dc1a57c0282a3801dbd ;
#   nobena piramida registra 2 ni piramida registra 1, noben obrat ni zaseden
#   ⊢ ; izmenjevalni zakon : nobeni dve zaporedni žigi iz istega registra ;
#   sigil rodu A : register-1 = 8261 4093 7521 3648,
#   register-2 = 1467 9358 8516 9238 ;
#   binarna podlaga števil 0 do 9 = žigi na drsnem zaporedju BCD, samostojna ;
#   drsenje = štirimestna okna binarne podlage, zasedena za kovanje ;
#   kovana kocka neznanega znaka = PREDLOG ⭢ sodba naročnika ⚔.
import sys
import os
import re
import glob
import hashlib
import difflib
from datetime import datetime, timezone

VERZIJA = "2.0"
ROD = "7790"


def tik():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ------------------------------------------------------- ⟨VENTIL-ORODJA⟩ ----
# zapečena priča lastnega telesa : ograja-ventil.md ob telesu orodja.
# merilec se meri ob vsaki rabi : vsak poklič preveri lastni md5 najprej.
def ventil_pot():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "ograja-ventil.md")


def ventil_zapeci():
    pot = ventil_pot()
    if os.path.exists(pot):
        return False, "ventil je že zapečen ; pečat se ⟨ne⟩ retipka ⚔"
    with open(os.path.abspath(__file__), "rb") as f:
        zepek = hashlib.md5(f.read()).hexdigest()
    with open(pot, "w", encoding="utf-8") as f:
        f.write("# ⟨VENTIL-ORODJA⟩ zapečenje telesa orodja @rez σ %s\n" % ROD)
        f.write("md5 %s\n" % zepek)
        f.write("tik %s\n" % tik())
        f.write("telo ograja.py v%s ⟨OGRAJA⟩ rod σ %s\n" % (VERZIJA, ROD))
    return True, "ventil zapečen ⊢ md5 %s @TIK %s" % (zepek, tik())


def ventil_presodi(md5_telesa, telo_boka):
    """sodba ventila po čistem paru ( bajti telesa, telo boka )"""
    zapecen = None
    for vrstica in telo_boka.splitlines():
        if vrstica.startswith("md5 "):
            zapecen = vrstica[4:].strip().lower()
            break
    if zapecen is None:
        return ("nezapečeno", "bok brez pečata")
    if zapecen == md5_telesa:
        return ("zapečeno-skladno", "instrument meri po zapečeni priči ⊢")
    return ("instrument-laze",
            "telo orodja se ne ujema s pričo ⚠ ( priča %s, telo %s )"
            % (zapecen, md5_telesa))


def ventil_preslusaj():
    """berba lastnega telesa ∧ boka ; vrne ( stanje, sporočilo )"""
    try:
        with open(os.path.abspath(__file__), "rb") as f:
            zepek = hashlib.md5(f.read()).hexdigest()
    except OSError as e:
        return ("padec", str(e))
    if not os.path.exists(ventil_pot()):
        return ("nezapečeno", "nezapečeno : bok priče manjka ⚠ ( zapeči z --zapeči )")
    with open(ventil_pot(), "r", encoding="utf-8") as f:
        return ventil_presodi(zepek, f.read())


# ------------------------------------------------------------- prostor ----
# trdni prostor ( rezerva, dokler ⟨BELO-NAVODILO⟩ ⟨ne⟩ da svojega )
DOVOLJENI = [
    (0x0000, 0x007F),   # ASCII
    (0x00A0, 0x024F),   # latinica, šumniki
    (0x0250, 0x02FF),   # IPA, spodnje oznake
    (0x2000, 0x209F),   # ločila, potence
    (0x2150, 0x218F),
    (0x2190, 0x23FF),   # puščice, matematika, tehnični blok
    (0x2500, 0x27FF),   # risbe, simboli, ograje, sekira
    (0x2900, 0x2BFF),
]

KANON_HELENSKI = set([0x0394, 0x03A3, 0x03A8, 0x03B3, 0x03C0, 0x03C3, 0x03C8])

NFD_BLOKI = [(0x0300, 0x036F)]

TRDI_BLOKI = [
    ("cirilica", 0x0400, 0x052F, set()),
    ("cirilica-starinska", 0x2DE0, 0x2DFF, set()),
    ("cirilica-zdruzena", 0xA640, 0xA6FF, set()),
    ("grscina", 0x0370, 0x03FF, KANON_HELENSKI),
    ("grscina-zlogi", 0x1F00, 0x1FFF, set()),
    ("hebrejska", 0x0590, 0x05FF, set()),
    ("arabska", 0x0600, 0x06FF, set()),
    ("indicne", 0x0900, 0x0DFF, set()),
    ("tajlandska", 0x0E00, 0x0E7F, set()),
    ("lao-kmerska", 0x0E80, 0x0EFF, set()),
    ("tibetanska", 0x0F00, 0x0FFF, set()),
    ("hangul-pismenke", 0x1100, 0x11FF, set()),
    ("hangul-zlogi", 0xAC00, 0xD7FF, set()),
    ("korejske-pismenke", 0x3130, 0x318F, set()),
    ("kitajska-ločila", 0x3000, 0x303F, set()),
    ("kana", 0x3040, 0x30FF, set()),
    ("kitajske-pomozne", 0x3190, 0x33FF, set()),
    ("hana-dopolnilna", 0x3400, 0x4DBF, set()),
    ("hana", 0x4E00, 0x9FFF, set()),
    ("hana-zdruzena", 0xF900, 0xFAFF, set()),
    ("hangul-pomozna", 0xA960, 0xA97F, set()),
    ("polnosecne", 0xFF01, 0xFF65, set()),
    ("polovicne-tuje", 0xFF66, 0xFFDC, set()),
]

NEVIDNI = set([0x00AD, 0x061C, 0x180E, 0x200B, 0x200C, 0x200D, 0x200E, 0x200F,
               0x202A, 0x202B, 0x202C, 0x202D, 0x202E,
               0x2060, 0x2061, 0x2062, 0x2063, 0x2064,
               0x2066, 0x2067, 0x2068, 0x2069, 0xFEFF,
               0xFFF9, 0xFFFA, 0xFFFB])
SELEKTORJI = set(range(0xFE00, 0xFE0F + 1)) | set(range(0xE0100, 0xE01EF + 1))
ZASEBNI = set(range(0xE000, 0xF8FF + 1)) | set(range(0xF0000, 0xFFFFD + 1))
ZASEBNI = ZASEBNI | set(range(0x100000, 0x10FFFD + 1))
NADOMESCALNIK = 0xFFFD
NAD_GLIFI_OD = 0x1F000

# slovenska imena znanih vbodov ( ⟨SAMO-KOCKE⟩ :brez kodnih mask )
IME_ZNAKA = {
    0x0430: "cirilska o",
    0x0435: "cirilska e",
    0x0430 + 0x20: "cirilska P",
    0x732A: "han pismenka",
    0xFF0C: "polnosecna vejica",
    0x200B: "nevidni presledek",
    0xFE0F: "variacijski selektor",
    0x03A9: "helenska velika omega",
}


def v_dovoljenem(cp):
    for a, b in DOVOLJENI:
        if a <= cp <= b:
            return True
    return False


def razred(cp):
    """poimenuje razred znaka po kodni točki ; vrne ( ime, trdost )"""
    if cp in KANON_HELENSKI:
        return (None, False)
    if cp in NEVIDNI:
        return ("nevidni-pisni", True)
    if cp in SELEKTORJI:
        return ("varijski-selektor", True)
    if cp in ZASEBNI:
        return ("zasebna-raba", True)
    if cp == NADOMESCALNIK:
        return ("nadomescalnik", True)
    for ime, a, b, izjeme in TRDI_BLOKI:
        if a <= cp <= b and cp not in izjeme:
            return (ime, True)
    for a, b in NFD_BLOKI:
        if a <= cp <= b:
            return ("nfd-gost", False)
    if not v_dovoljenem(cp):
        return ("zunaj-dovoljenega-prostora", True)
    if cp >= NAD_GLIFI_OD:
        return ("nad-glifi", True)
    return (None, False)


# --------------------------------------------------- ⟨KUBIT-KOVANJE⟩ ----
# kubit plast pod gladino : podatkovni blok zapečenih registrov 1 ∧ 2
# ( izluščen iz preverjenih teles @posebaj, bajti ∧ md5 priči VRATA.json )
# kubit plast pod gladino : zapečeni registri 1 ∧ 2 @posebaj ⊢ VRATA.json ( izluščeno iz preverjenih teles, bajti ∧ md5 priči )
KUBIT_R1_VRSTE = (
    ('A', 8261, 4093, 7521, 3648),
    ('a', 5914, 7068, 2435, 8172),
    ('B', 3271, 9568, 1492, 6814),
    ('b', 4187, 2395, 7629, 5841),
    ('C', 1946, 8273, 4519, 7352),
    ('c', 5638, 1247, 9816, 4672),
    ('Č', 7429, 3158, 8691, 2346),
    ('č', 6875, 4923, 5136, 9284),
    ('D', 3788, 8342, 2763, 6129),
    ('d', 9431, 1728, 3854, 7295),
    ('E', 2468, 3597, 8126, 5734),
    ('e', 8963, 4715, 6428, 3179),
    ('F', 7164, 9486, 2391, 5627),
    ('f', 3869, 1254, 7438, 9673),
    ('G', 4892, 6537, 2168, 8345),
    ('g', 5721, 1496, 9364, 6287),
    ('H', 1657, 8275, 4953, 3541),
    ('h', 7493, 3754, 5879, 2683),
    ('I', 9253, 6714, 1862, 4389),
    ('i', 5647, 2938, 8176, 7529),
    ('J', 1379, 4826, 9561, 6214),
    ('j', 8415, 7283, 3694, 1536),
    ('K', 2947, 8915, 1782, 8361),
    ('k', 6152, 9479, 4236, 7924),
    ('L', 6185, 2147, 6728, 5473),
    ('l', 7684, 2319, 9245, 1876),
    ('M', 2539, 8137, 5962, 3458),
    ('m', 9524, 4781, 6357, 2619),
    ('N', 5873, 1236, 8496, 6963),
    ('n', 2498, 8615, 3547, 6173),
    ('O', 1869, 9354, 4726, 5281),
    ('o', 7578, 3942, 2137, 8435),
    ('P', 4517, 3471, 1382, 9614),
    ('p', 9674, 5238, 1845, 7326),
    ('R', 2617, 8459, 3192, 5938),
    ('r', 6983, 1746, 4527, 8219),
    ('S', 7245, 3918, 1563, 4869),
    ('s', 3527, 9648, 7194, 2736),
    ('Š', 4183, 5872, 6385, 8247),
    ('š', 8369, 2457, 1538, 9742),
    ('T', 5146, 7219, 2394, 6817),
    ('t', 1428, 6937, 8753, 3561),
    ('U', 9738, 1356, 4562, 5297),
    ('u', 2864, 5713, 6489, 4975),
    ('V', 6379, 8421, 3145, 9586),
    ('v', 7413, 2879, 6437, 5169),
    ('Z', 1592, 4768, 9246, 8371),
    ('z', 8147, 3596, 2623, 5924),
    ('Ž', 4685, 1927, 7238, 6459),
    ('ž', 5973, 8634, 2184, 3765),
    ('Q', 7359, 6297, 7461, 2918),
    ('q', 9136, 5842, 1674, 4759),
    ('W', 6578, 2341, 8925, 3186),
    ('w', 4129, 7635, 5287, 9863),
    ('Y', 8614, 1975, 4532, 6278),
    ('y', 7251, 3864, 1947, 5623),
    ('X', 2748, 3957, 6193, 8537),
    ('x', 5936, 8217, 4692, 1375),
    ('Đ', 2873, 7858, 7648, 9426),
    ('đ', 6479, 8315, 2734, 9285),
    ('Ć', 1958, 4267, 6823, 3549),
    ('ć', 3727, 9148, 5784, 2863),
    ('presledek', 8627, 1539, 4738, 6942),
    ('pika', 2465, 3986, 8164, 5712),
    ('vejica', 6938, 7854, 1287, 4593),
    ('vzkličnik', 5349, 2671, 9428, 7816),
    ('vprašaj', 4836, 6137, 3975, 8549),
    ('dvopičje', 1587, 7392, 4621, 9382),
    ('podpičje', 9261, 3448, 5892, 6719),
    ('levi oklepaj', 3742, 1829, 6952, 4386),
    ('desni oklepaj', 7193, 2658, 8943, 5467),
    ('narekovaj', 6282, 4936, 1754, 8974),
    ('apostrof', 1546, 8749, 2463, 3691),
    ('pomišljaj', 9487, 5213, 7834, 2659),
    ('plus', 4578, 1826, 9531, 6124),
    ('minus', 3914, 6758, 7946, 7243),
    ('znak za množenje', 8132, 4596, 5674, 2381),
    ('znak za deljenje', 6241, 7965, 3528, 1873),
    ('enačaj', 2953, 1489, 4716, 8367),
    ('manjše', 7864, 2359, 9138, 5742),
    ('večje', 3618, 8547, 6794, 2926),
    ('približno', 5274, 9168, 3842, 7435),
    ('znak za odstotek', 2697, 5729, 8657, 4196),
    ('koren', 6739, 3214, 1965, 9582),
    ('kvadrat', 4591, 2845, 2735, 5326),
    ('število pi', 8159, 5649, 1298, 6947),
    ('znak za neenakost', 5983, 9374, 4758, 1423),
)
KUBIT_R2_VRSTE = (
    ('A', 1467, 9358, 8516, 9238),
    ('a', 6397, 2185, 7948, 1652),
    ('B', 2916, 4783, 8349, 5271),
    ('b', 7562, 9418, 1837, 4296),
    ('C', 5183, 2649, 7928, 3415),
    ('c', 9827, 4712, 4371, 8364),
    ('Č', 3459, 8216, 6782, 3948),
    ('č', 7618, 2934, 5197, 8523),
    ('D', 1294, 6291, 9625, 1658),
    ('d', 4961, 8527, 3176, 2759),
    ('E', 8741, 3625, 5986, 2317),
    ('e', 6253, 9174, 4839, 1682),
    ('F', 6984, 7281, 3157, 2469),
    ('f', 5129, 1279, 2754, 6973),
    ('G', 9658, 1327, 4786, 2139),
    ('g', 2814, 5963, 3416, 9326),
    ('H', 6745, 1238, 9571, 5283),
    ('h', 4382, 7691, 5236, 1795),
    ('I', 1593, 7149, 8165, 7384),
    ('i', 8237, 1956, 4612, 6579),
    ('J', 4916, 3598, 7349, 9152),
    ('j', 3652, 5823, 3275, 1234),
    ('K', 9172, 4395, 6851, 2546),
    ('k', 7489, 1623, 3968, 5714),
    ('L', 5382, 2374, 4127, 7932),
    ('l', 1326, 9485, 8245, 5248),
    ('M', 5764, 3198, 2413, 9375),
    ('m', 2981, 6734, 1547, 8621),
    ('N', 6928, 3846, 4856, 7439),
    ('n', 6541, 8932, 3167, 2794),
    ('O', 1783, 7135, 9356, 2647),
    ('o', 9814, 4567, 3189, 4438),
    ('P', 8456, 6712, 3925, 5127),
    ('p', 3469, 7582, 1246, 8941),
    ('R', 4938, 9387, 2849, 3512),
    ('r', 3857, 4625, 8173, 5294),
    ('S', 4213, 8759, 2347, 2958),
    ('s', 2694, 5821, 9264, 4158),
    ('Š', 4876, 5921, 7153, 1396),
    ('š', 6139, 7842, 2467, 9513),
    ('T', 2948, 3168, 1872, 7615),
    ('t', 5837, 1284, 9463, 5231),
    ('U', 4172, 2789, 1698, 7589),
    ('u', 8536, 3617, 2453, 1828),
    ('V', 8658, 4391, 5216, 2738),
    ('v', 1974, 6528, 3465, 8291),
    ('Z', 7835, 3792, 4589, 4287),
    ('z', 4523, 2634, 8934, 1678),
    ('Ž', 9671, 2458, 4825, 1925),
    ('ž', 3178, 4827, 8593, 4926),
    ('Q', 2689, 3457, 4137, 9345),
    ('q', 7961, 5832, 6798, 3451),
    ('W', 8517, 1364, 3861, 4627),
    ('w', 4153, 6791, 2382, 7285),
    ('Y', 5187, 3489, 5943, 8214),
    ('y', 9217, 5861, 4673, 1438),
    ('X', 2847, 3456, 3928, 2517),
    ('x', 5419, 3786, 2163, 8947),
    ('Đ', 2384, 7459, 6126, 4592),
    ('đ', 1567, 4838, 7293, 8274),
    ('Ć', 3524, 9861, 5471, 2638),
    ('ć', 2614, 7364, 9416, 3847),
    ('presledek', 3985, 6427, 1739, 5876),
    ('pika', 7598, 2461, 9318, 4854),
    ('vejica', 1259, 8746, 6352, 3184),
    ('vzkličnik', 8645, 5378, 7261, 3628),
    ('vprašaj', 6419, 3875, 2945, 5736),
    ('dvopičje', 1894, 5738, 2685, 9865),
    ('podpičje', 3645, 4691, 6783, 2978),
    ('levi oklepaj', 9576, 2841, 4397, 1839),
    ('desni oklepaj', 1789, 4356, 8623, 5761),
    ('narekovaj', 6219, 7139, 5968, 1583),
    ('apostrof', 2853, 6971, 4518, 7526),
    ('pomišljaj', 7456, 1823, 5694, 8649),
    ('plus', 5698, 2357, 8426, 4793),
    ('minus', 8739, 4652, 1972, 6285),
    ('znak za množenje', 3428, 7869, 5573, 2758),
    ('znak za deljenje', 5276, 4835, 6254, 8937),
    ('enačaj', 3915, 7168, 2351, 6974),
    ('manjše', 9654, 4218, 3162, 7426),
    ('večje', 3279, 5846, 8643, 9173),
    ('približno', 4697, 2751, 1856, 9124),
    ('znak za odstotek', 7954, 4365, 1849, 2673),
    ('koren', 2819, 4659, 9187, 4529),
    ('kvadrat', 6238, 9147, 7524, 3476),
    ('število pi', 2417, 3849, 7241, 9823),
    ('znak za neenakost', 6279, 8765, 1392, 5926),
)

SIGIL_R1 = (8261, 4093, 7521, 3648)
SIGIL_R2 = (1467, 9358, 8516, 9238)
PRICA_R1 = {"bajti": 3716, "md5": "babcfe1f846c0360b7e9baa3b5109761",
            "znakov": 87, "piramid": 348, "pecat": "POTRDI 24. 11. 2026"}
PRICA_R2 = {"bajti": 4053, "md5": "b4c30434a7e95dc1a57c0282a3801dbd",
            "znakov": 87, "piramid": 348, "pecat": "STORI 24. 11. 2026"}


def kubit_mnozice():
    """piramide obeh registrov po vrstah ∧ pojih ; vrne ( r1, r2 )"""
    return ([v[1:] for v in KUBIT_R1_VRSTE],
            [v[1:] for v in KUBIT_R2_VRSTE])


def drsenje():
    """zasedena drsna okna binarne podlage števil 0 do 9 ( BCD, korak 1 )"""
    podlaga = "".join(format(i, "04b") for i in range(10))
    return frozenset(podlaga[i:i + 4] for i in range(len(podlaga) - 3))


def kubit_zasedenost(dodatne_mnozice=()):
    """zasedenost prostora piramid za kovanje predlogov"""
    r1, r2 = kubit_mnozice()
    zasedeni = set()
    for vrsta in r1 + r2:
        zasedeni.update(vrsta)
    for m in dodatne_mnozice:
        zasedeni.update(m)
    return zasedeni


def osnova_piramide(cp, m):
    """formula telesa : osnova = 1000 + ( kodna točka × m po modulu 9000 )"""
    return 1000 + (cp * m) % 9000


def piramida_prosta(p, zasedeni, drs, ze_kovane):
    """zakoni proste piramide : rob brez ničle, brez palindroma, brez
    zasedenosti, obrat nezaseden, drsenje nezasedeno"""
    s = "%04d" % p
    if s[0] == "0" or s[-1] == "0":
        return False
    if s == s[::-1]:
        return False
    if p in zasedeni or p in ze_kovane:
        return False
    if int(s[::-1]) in zasedeni or int(s[::-1]) in ze_kovane:
        return False
    if s in drs:
        return False
    return True


def kov_kocko(cp, zasedeni, drs):
    """kovanje štirih piramid znaka po formuli ∧ kuri plus sedem ;
    ovijanje nad 9999 po modulu 9000 ⊙ teorija uradno določena"""
    ze_kovane = set()
    vrsta = []
    for m in (1, 3, 7, 9):
        p = osnova_piramide(cp, m)
        korakov = 0
        while not piramida_prosta(p, zasedeni, drs, ze_kovane):
            p += 7
            if p > 9999:
                p = 1000 + (p - 1000) % 9000
            korakov += 1
            if korakov > 9000:
                return None
        ze_kovane.add(p)
        vrsta.append(p)
    return tuple(vrsta)


def beri_dosje(pot):
    """berba dosjeja uradnih kod znakov ( zapečeni viri ) : vrstice
    »koda znaka = štiri piramide« ( prestrežnik z ⟨ne⟩ določa predznake )"""
    uradne = {}
    with open(pot, "r", encoding="utf-8") as f:
        for vrstica in f:
            m = re.match(r"^U\+([0-9A-Fa-f]{4,6})\s*=\s*([PNDK]?\d{4})"
                        r"(?:\s+([PNDK]?\d{4}))?(?:\s+([PNDK]?\d{4}))"
                        r"?(?:\s+([PNDK]?\d{4}))?\s*$", vrstica.strip())
            if not m:
                continue
            cp = int(m.group(1), 16)
            vrsta = tuple(g for g in m.groups()[1:] if g)
            if len(vrsta) == 4:
                uradne[cp] = vrsta
    return uradne


# --------------------------------------------------------------- berba ----
def preberi(pot):
    """berba po bajtih strogo ; neveljaven zapis = rana"""
    with open(pot, "rb") as f:
        sveze = f.read()
    try:
        return sveze.decode("utf-8", errors="strict"), None
    except UnicodeDecodeError as e:
        return None, e.start


def cenzus(besedilo, strogo=False, belo=None):
    """izmera tujk po telesu ; vrne ( ulovi, nfd_gostje, znakov )
    ulov = ( ime_razreda, koda, vrstica, stolpec, bajti ) ; bajti ⟨od⟩
    belo : množica dovoljenih mest po belem navodilu ( ⟨ne⟩ izbira blokov )"""
    ulovi = []
    nfd = 0
    vrstica, stolpec = 1, 1
    for znak in besedilo:
        cp = ord(znak)
        if znak == "\n":
            vrstica += 1
            stolpec = 1
            continue
        bajti = znak.encode("utf-8").hex(" ")
        if belo is not None:
            if cp in belo:
                stolpec += 1
                continue
            ime, _ = razred(cp)
            if ime is None:
                ime = "zunaj-belega-navodila"
            ulovi.append((ime, cp, vrstica, stolpec, bajti))
            stolpec += 1
            continue
        ime, trd = razred(cp)
        if ime == "nfd-gost":
            nfd += 1
            if strogo:
                ulovi.append((ime, cp, vrstica, stolpec, bajti))
        elif trd:
            ulovi.append((ime, cp, vrstica, stolpec, bajti))
        stolpec += 1
    return ulovi, nfd, len(besedilo)


def opisi_kocke(ulovi, uradne, zasedeni, drs, predpomnilnik):
    """⟨SAMO-KOCKE⟩ : vsakemu ulovu presodi kocko po uradnih progenihih ;
    neznan znak = PREDLOG po formuli ⭢ sodba naročnika ⚔"""
    opisi = {}
    for u in ulovi:
        cp = u[1]
        if cp in opisi:
            continue
        if cp in uradne:
            opisi[cp] = "uradna ⊢ %s %s %s %s @dosje" % uradne[cp]
        elif cp in predpomnilnik:
            opisi[cp] = predpomnilnik[cp]
        else:
            vrsta = kov_kocko(cp, zasedeni, drs)
            if vrsta is None:
                opisi[cp] = "kovanje brez prostega mesta ⚠"
            else:
                opisi[cp] = ("predlog ⭢ sodba naročnika ⚔ : "
                             "K%d K%d K%d K%d" % vrsta)
    return opisi


def niz_ulovov(ulovi, kocke=None, meja=8):
    """bralna plast : ulovi v slovenskih imenih ∧ kockah ;
    kodne maske ostanejo znotraj stroja, brez ⟨U+⟩ žetonov"""
    vrstice = []
    for u in ulovi[:meja]:
        ime = IME_ZNAKA.get(u[1]) or u[0]
        vrstica = ("  - %s ; bajti %s ; vrstica %d : stolpec %d"
                   % (ime, u[4], u[2], u[3]))
        if kocke and u[1] in kocke:
            vrstica += " ; kocka : %s" % kocke[u[1]]
        vrstice.append(vrstica)
    if len(ulovi) > meja:
        vrstice.append("  - ... ∧ še %d" % (len(ulovi) - meja))
    return vrstice


# ---------------------------------------------------------------- sled ----
class NapakaOgraje(Exception):
    pass


def razberi_regije(niz):
    """zapis »2-4,9« ⭢ [(2,4),(9,9)] po vrsticah PRED telesa"""
    regije = []
    for delcek in niz.split(","):
        delcek = delcek.strip()
        if "-" in delcek:
            a, b = delcek.split("-", 1)
            regije.append((int(a), int(b)))
        else:
            regije.append((int(delcek), int(delcek)))
    return regije


def v_regiji(st, regije):
    return any(a <= st <= b for a, b in regije)


def sled(pot_pred, pot_po, regije, prag):
    """izmera sledi spremembe : spremenjeno ∧ kje ; izven odobrene regije =
    rana ; brez regije : pomet nad pragom = rana ( sum prepisa telesa )"""
    pred_b, napaka1 = preberi(pot_pred)
    po_b, napaka2 = preberi(pot_po)
    if pred_b is None or po_b is None:
        raise NapakaOgraje("neveljaven zapis PRED odmik %s, PO odmik %s"
                           % (napaka1, napaka2))
    pred = pred_b.splitlines()
    po = po_b.splitlines()
    merilec = difflib.SequenceMatcher(a=pred, b=po, autojunk=False)
    pomet = 0
    rane = []
    opis = []
    for oznaka, i1, i2, j1, j2 in merilec.get_opcodes():
        if oznaka == "equal":
            continue
        dotaknjenih = max(i2 - i1, j2 - j1)
        pomet += dotaknjenih
        kje = ("%d-%d" % (i1 + 1, i2)) if i2 > i1 else "0"
        kje_po = ("%d-%d" % (j1 + 1, j2)) if j2 > j1 else "0"
        opis.append("  - %s : PRED vrstice %s ⭢ PO vrstice %s, dotaknjenih %d"
                    % (oznaka, kje, kje_po, dotaknjenih))
        if regije:
            zunaj = [st for st in range(i1 + 1, i2 + 1) if not v_regiji(st, regije)]
            if oznaka != "delete":
                vlozek_meja = v_regiji(i1, regije) or v_regiji(i1 + 1, regije)
                if not vlozek_meja:
                    zunaj.append(i1 + 1)
            if zunaj:
                prvi = min(zunaj)
                zadnji = max(zunaj)
                kje_r = str(prvi) if prvi == zadnji else "%d do %d" % (prvi, zadnji)
                rane.append("sprememba izven odobrene regije : vrstica %s" % kje_r)
    odstotek = 100.0 * pomet / max(len(pred), 1)
    return {
        "opis": opis,
        "rane": rane,
        "pomet_vrstice": pomet,
        "odstotek": odstotek,
        "pomet_rana": odstotek > prag,
        "vrstice_pred": len(pred),
        "vrstice_po": len(po),
        "bajti_pred": os.path.getsize(pot_pred),
        "bajti_po": os.path.getsize(pot_po),
    }


# --------------------------------------------------------- ⟨BELO-NAVODILO⟩ ----
def beri_belo(pot):
    """belo navodilo : množica dovoljenih mest po pričah
    ( eno mesto na vrstico ; vrstica s # = molk ; ostatki ignorirani )"""
    dovoljeni = set()
    with open(pot, "r", encoding="utf-8") as f:
        for vrstica in f:
            vrstica = vrstica.strip()
            if not vrstica or vrstica.startswith("#"):
                continue
            deli = vrstica.split(None, 1)
            try:
                dovoljeni.add(int(deli[0]))
            except ValueError:
                continue
    return dovoljeni


def beri_prico_za_belo(pot):
    """berba priče ∧ zbiranje njenih mest ( kodne točke )"""
    besedilo, napaka = preberi(pot)
    if besedilo is None:
        raise NapakaOgraje("priča %s neberljiva pri odmiku %s" % (pot, napaka))
    return set(ord(z) for z in besedilo)


# --------------------------------------------------------------- prica ----
def prestej_vrstice(telesi):
    if telesi == b"":
        return 0
    return telesi.count(b"\n") + (0 if telesi.endswith(b"\n") else 1)


def poroci_price(poti):
    porocilo = []
    for pot in poti:
        with open(pot, "rb") as f:
            telesi = f.read()
        veljavno = True
        znakov = 0
        try:
            znakov = len(telesi.decode("utf-8", errors="strict"))
        except UnicodeDecodeError:
            veljavno = False
        porocilo.append(
            "priča %s : bajti %d ⌇ vrstice %d ⌇ znaki %s ⌇ md5 %s ⌇ sha256 %s ⌇ TIK %s"
            % (pot, len(telesi), prestej_vrstice(telesi),
               (str(znakov) if veljavno else "neveljaven zapis ⚠"),
               hashlib.md5(telesi).hexdigest(),
               hashlib.sha256(telesi).hexdigest(), tik()))
    return porocilo


def beri_manifest(pot):
    """prijave po vrsticah : »md5  ime« ; vrstica s # = molk"""
    prijave = []
    with open(pot, "r", encoding="utf-8") as f:
        for vrstica in f:
            vrstica = vrstica.strip()
            if not vrstica or vrstica.startswith("#"):
                continue
            delci = vrstica.split(None, 1)
            if len(delci) != 2:
                raise NapakaOgraje("manifest : vrstica brez para »%s«" % vrstica)
            prijave.append((delci[0].lower(), delci[1].strip()))
    return prijave


# --------------------------------------------------------------- vrata ----
def poroci_vrata(poti, manifest, geniza=None, uradne=None, zasedeni=None,
                 drs=None, belo=None):
    """prevozna vrata : cenzus tujk ∧ veriga md5 po pričah ;
    rana pri neujemanju nosi namig povrni ( ⟨REHAB-VEZA⟩ )"""
    vrstice = []
    rane = 0
    predpomnilnik = {}
    if uradne is None:
        uradne = {}
    if zasedeni is None:
        zasedeni = kubit_zasedenost()
    if drs is None:
        drs = drsenje()
    if manifest:
        for prica_znak, ime in beri_manifest(manifest):
            try:
                with open(ime, "rb") as f:
                    telesi = f.read()
            except OSError as e:
                vrstice.append("RANA : %s se ne da brati ( %s ) ⚠" % (ime, e))
                rane += 1
                continue
            zepek = hashlib.md5(telesi).hexdigest()
            if zepek == prica_znak:
                vrstice.append("⊢ %s : md5 enak priči ; bajti %d" % (ime, len(telesi)))
            else:
                vrstice.append("RANA : %s md5 %s, priča pravi %s ⚠ bajti %d"
                               % (ime, zepek, prica_znak, len(telesi)))
                if geniza:
                    vrstice.append("  kura : povrni iz genize priče ⭢ predlog ⭢ "
                                   "sodba naročnika ⚔ ( --iz %s )" % geniza)
                rane += 1
    for pot in poti:
        besedilo, napaka = preberi(pot)
        if besedilo is None:
            vrstice.append("RANA : %s neberljiv bajt pri odmiku %d ⚠" % (pot, napaka))
            rane += 1
            continue
        belo_mnozica = beri_belo(belo) if belo else None
        ulovi, nfd, znakov = cenzus(besedilo, belo=belo_mnozica)
        if ulovi:
            kocke = opisi_kocke(ulovi, uradne or {}, zasedeni, drs,
                                predpomnilnik)
            predpomnilnik.update(kocke)
            vrstice.append("RANA : %s ulovi ×%d, nfd gostje ×%d"
                           % (pot, len(ulovi), nfd))
            vrstice.extend(niz_ulovov(ulovi, kocke))
            rane += len(ulovi)
        else:
            with open(pot, "rb") as f:
                zepek = hashlib.md5(f.read()).hexdigest()
            vrstice.append("⊢ %s : tuji ×0 ; nfd ×%d ; md5 %s ; bajti %d"
                           % (pot, nfd, zepek, os.path.getsize(pot)))
    vrstice.append("Σ ran ×%d %s" % (rane, "⊢ VRATA ZELENA" if rane == 0
                                     else "⚠ VRATA RDECA"))
    return rane, vrstice


# ------------------------------------------------------ ⟨STALNI-DIH⟩ ----
# forma manifesta : MANIFEST-STROGA ( rod σ 6583 ⊙ preverba-dihov v1.1 ) :
# dva stolpca »sha256  pot«, vrstica s # = molk ; samodejno odkritje najnovejšega.
def najnovejsi_manifest(vzorec):
    fl = sorted(glob.glob(vzorec))
    najd = None
    st_naj = -1
    for p in fl:
        m = re.search(r"MANIFEST-STROGA-(\d+)\.md$", os.path.basename(p))
        if m and int(m.group(1)) > st_naj:
            st_naj = int(m.group(1))
            najd = p
    return najd, (st_naj + 1) if najd else None


def beri_manifest_stroga(pot):
    telo = {}
    if not pot or not os.path.exists(pot):
        return telo
    with open(pot, "r", encoding="utf-8") as f:
        for vrst in f:
            deli = vrst.split()
            if len(deli) == 2 and not deli[0].startswith("#"):
                telo[deli[1]] = deli[0]
    return telo


def pulz_dih(koren, pot_manifesta):
    """stalni dih : stanja teles organov ( */KNOWLEDGE.md po korenu ) proti
    zapečeni verigi sha256 ; poročilo tiho v genizo, ⟨ne⟩ piše manifesta"""
    staro = beri_manifest_stroga(pot_manifesta)
    zdaj = {}
    for pot in sorted(glob.glob(os.path.join(koren, "*", "KNOWLEDGE.md"))):
        rel = os.path.relpath(pot, koren)
        with open(pot, "rb") as f:
            zdaj[rel] = hashlib.sha256(f.read()).hexdigest()
    trdno = [i for i in zdaj if i in staro and staro[i] == zdaj[i]]
    sprem = [i for i in zdaj if i in staro and staro[i] != zdaj[i]]
    novo = [i for i in zdaj if i not in staro]
    izg = [i for i in staro if i not in zdaj]
    vrstice = ["manifest : %s ( teles %d ; prej prijavljenih %d )"
               % (pot_manifesta, len(zdaj), len(staro)),
               "PULZ ⊢ : trdno %d / spremenjeno %d / novo %d / izginilo %d"
               % (len(trdno), len(sprem), len(novo), len(izg))]
    for i in sprem:
        vrstice.append("  SPREMENJENO : %s" % i)
    for i in novo:
        vrstice.append("  NOVO : %s" % i)
    for i in izg:
        vrstice.append("  IZGINILO-POMETENO : %s" % i)
    return (len(sprem) + len(izg)), vrstice


# -------------------------------------------------------- ⟨REHAB-VEZA⟩ ----
def povrni_telo(pot_tela, geniza, pot_izhoda):
    """povrni telo bajtno iz genize priče ; piše PREDLOG telo, ranjeno telo
    ⟨ne⟩ prepisuje ; brez priče = padec instrumenta"""
    ime = os.path.basename(pot_tela)
    kandidati = sorted(glob.glob(os.path.join(geniza, "**", ime),
                                  recursive=True))
    if not kandidati:
        return False, ["geniza priča manjka : %s v %s ⚠" % (ime, geniza)]
    with open(kandidati[0], "rb") as f:
        telesi = f.read()
    if os.path.exists(pot_izhoda):
        return False, ["predlog telo %s že živi ; pečat se ⟨ne⟩ retipka ⚠"
                       % pot_izhoda]
    with open(pot_izhoda, "wb") as f:
        f.write(telesi)
    return True, [
        "povrni ⊢ : predlog %s ( bajti %d, md5 %s )"
        % (pot_izhoda, len(telesi), hashlib.md5(telesi).hexdigest()),
        "priča genize : %s" % kandidati[0],
        "kura : predlog ⭢ sodba naročnika ⚔",
    ]


# -------------------------------------------------------- samopreizkus ----
def samopreizkus():
    """baterija nad sintetičnimi trupi ( kandidati preizkusa, ⟨ne⟩ telesa )"""
    baterija = []

    def pripis(ime, zeleno, podrobno):
        baterija.append((ime, zeleno, podrobno))

    # T1 : čisto telo korpusa
    cisto = ("Beseda je ⟨ne⟩ ⊙ merjeno, ⟨ne⟩ ugibano ⊙ 2690 ⊢ "
             "Σ ψ Δ γ σ π ⌇ ⚔ ∧ © 0.2026 × 10⁴\n")
    ulovi, nfd, _ = cenzus(cisto)
    pripis("T1-cisto", len(ulovi) == 0 and nfd == 0,
           "ulovov ×%d, nfd ×%d" % (len(ulovi), nfd))

    # T2 : trup z vbodi tujk ( osem razredov )
    trup = ("popravlj" + chr(0x0430) + "eno " + chr(0x732A) + " "
            + chr(0xFF0C) + " " + chr(0x200B) + " " + chr(0xFE0F) + " "
            + chr(0xF8FF) + " " + chr(0xFFFD) + " " + chr(0x03A9))
    ulovi, _, _ = cenzus(trup)
    ujeti = set(u[0] for u in ulovi)
    pricakani = set(["cirilica", "hana", "polnosecne", "nevidni-pisni",
                     "varijski-selektor", "zasebna-raba", "nadomescalnik",
                     "grscina"])
    pripis("T2-vbodi", ujeti == pricakani,
           "ujetih razredov ×%d od ×%d" % (len(ujeti), len(pricakani)))

    # T3 : NFD gostje ( mehki privzeto, trdi z --strogo )
    nfd_telo = "z" + chr(0x0301) + "iv"
    ulovi_mehki, nfd, _ = cenzus(nfd_telo, strogo=False)
    ulovi_trdi, _, _ = cenzus(nfd_telo, strogo=True)
    pripis("T3-nfd", nfd == 1 and len(ulovi_mehki) == 0 and len(ulovi_trdi) == 1,
           "nfd gost ×%d ; mehki ×%d ; trdi ×%d"
           % (nfd, len(ulovi_mehki), len(ulovi_trdi)))

    # T4 do T8 : sled ∧ vrata po datotekah ( end-to-end )
    import tempfile
    import shutil
    pred_vrstice = ["prva", "druga", "tretja", "cetrta", "peta",
                    "sesta", "sedma", "osma", "deveta", "deseta"]
    with tempfile.TemporaryDirectory() as dom:
        pot_pred = os.path.join(dom, "pred.md")

        def zapisi_pot(ime, vrstice):
            pot = os.path.join(dom, ime)
            with open(pot, "w", encoding="utf-8") as f:
                f.write("\n".join(vrstice) + "\n")
            return pot

        zapisi_pot("pred.md", pred_vrstice)

        # T4 : sprememba znotraj odobrene regije 2-4
        dovoljeno = list(pred_vrstice)
        dovoljeno[2] = "tretja spremenjena"
        izmera = sled(pot_pred, zapisi_pot("dovoljeno.md", dovoljeno),
                      [(2, 4)], 70)
        pripis("T4-sled-znotraj", len(izmera["rane"]) == 0,
               "ran ×%d ; dotaknjenih ×%d" % (len(izmera["rane"]),
                                              izmera["pomet_vrstice"]))

        # T5 : sprememba izven regije ( vrstica 9 )
        izven = list(pred_vrstice)
        izven[8] = "deveta pretipkana"
        izmera = sled(pot_pred, zapisi_pot("izven.md", izven), [(2, 4)], 70)
        pripis("T5-sled-izven", len(izmera["rane"]) == 1,
               "ran ×%d" % len(izmera["rane"]))

        # T6 : pomet brez regije ( prepis celega telesa )
        prepis = ["popolnoma", "drugacno", "telo", "brez", "dovoljenja",
                  "kje", "kaj", "zakaj", "kdo", "konec"]
        izmera = sled(pot_pred, zapisi_pot("prepis.md", prepis), None, 70)
        pripis("T6-pomet", izmera["pomet_rana"] and izmera["odstotek"] > 99,
               "odstotek %.1f" % izmera["odstotek"])

        # T7 : vrata po manifestu ( ena prava priča, ena ponarejena )
        telo_vrata = os.path.join(dom, "telo-vrata.md")
        with open(telo_vrata, "w", encoding="utf-8") as f:
            f.write("čisto telo za vrata ⊢\n")
        zepek = hashlib.md5(open(telo_vrata, "rb").read()).hexdigest()
        manifest_dober = os.path.join(dom, "price.tsv")
        with open(manifest_dober, "w", encoding="utf-8") as f:
            f.write("%s  %s\n" % (zepek, telo_vrata))
        rane_dober, _ = poroci_vrata([telo_vrata], manifest_dober)
        manifest_lagov = os.path.join(dom, "price-lagov.tsv")
        with open(manifest_lagov, "w", encoding="utf-8") as f:
            f.write("00000000000000000000000000000000  %s\n" % telo_vrata)
        rane_lagov, _ = poroci_vrata([telo_vrata], manifest_lagov)
        ranjeno = os.path.join(dom, "ranjeno.md")
        with open(ranjeno, "wb") as f:
            f.write(("beseda " + chr(0x0430) + " bait").encode("utf-8"))
        rane_ranjeno, vrstice_ranjeno = poroci_vrata([ranjeno], None)
        namig = any("povrni" in v for v in vrstice_ranjeno)
        geniza_dir = os.path.join(dom, "geniza")
        os.makedirs(geniza_dir, exist_ok=True)
        _, vrstice_hint = poroci_vrata([telo_vrata], manifest_lagov,
                                       geniza=geniza_dir)
        namig_geniza = any("povrni" in v for v in vrstice_hint)
        pripis("T7-vrata", rane_dober == 0 and rane_lagov >= 1
               and rane_ranjeno >= 1 and not namig and namig_geniza,
               "dobro ×%d, lagov ×%d, ranjeno ×%d, namig genize %s"
               % (rane_dober, rane_lagov, rane_ranjeno, namig_geniza))

        # T8 : neberljiv bajt ( rana po berbi strogo )
        neberljivo = os.path.join(dom, "neberljivo.md")
        with open(neberljivo, "wb") as f:
            f.write(b"dobra beseda " + bytes([0xBD]) + b" slab bajt")
        besedilo, napaka = preberi(neberljivo)
        pripis("T8-neberljivost", besedilo is None and napaka is not None,
               "odmik neveljavnega bajta %s" % napaka)

        # T11 : ⟨VENTIL-ORODJA⟩ ( merilec se meri ob vsaki rabi )
        stanje_ok = ventil_presodi("abc123", "md5 ABC123")
        stanje_laz = ventil_presodi("abc123", "md5 fff000")
        stanje_brez = ventil_presodi("abc123", "# bok brez pečata")
        pripis("T11-ventil",
               stanje_ok[0] == "zapečeno-skladno"
               and stanje_laz[0] == "instrument-laze"
               and stanje_brez[0] == "nezapečeno",
               "skladno %s ; laz %s ; brez %s"
               % (stanje_ok[0], stanje_laz[0], stanje_brez[0]))

        # T12 : ⟨BELO-NAVODILO⟩ ( dovoljeni prostor iz priče, ⟨ne⟩ bloki )
        prica_belo = os.path.join(dom, "prika-bela.md")
        with open(prica_belo, "w", encoding="utf-8") as f:
            f.write("abč ⊢")
        belo_mesta = beri_prico_za_belo(prica_belo)
        belo_dat = os.path.join(dom, "belo.tsv")
        with open(belo_dat, "w", encoding="utf-8") as f:
            for cp in sorted(belo_mesta):
                f.write("%d\n" % cp)
        belo = beri_belo(belo_dat)
        ulovi_belo, nfd_belo, znakov_belo = cenzus("abč × ⊢", belo=belo)
        # : × ( kodna točka za znak množenja ) je izven belega navodila
        pripis("T12-belo", belo_mesta == set(map(ord, "abč ⊢"))
               and len(ulovi_belo) == 1 and ulovi_belo[0][0] == "zunaj-belega-navodila",
               "mest priče ×%d ; ulovov zunaj belega ×%d" % (len(belo), len(ulovi_belo)))

        # T13 : ⟨STALNI-DIH⟩ ( forma MANIFEST-STROGA rodu σ 6583 )
        dih_koren = os.path.join(dom, "koren")
        os.makedirs(os.path.join(dih_koren, "organ-a"))
        os.makedirs(os.path.join(dih_koren, "organ-b"))
        telo_a = os.path.join(dih_koren, "organ-a", "KNOWLEDGE.md")
        open(telo_a, "w").write("ena")
        telo_b = os.path.join(dih_koren, "organ-b", "KNOWLEDGE.md")
        open(telo_b, "w").write("dva")
        manifest_1 = os.path.join(dom, "MANIFEST-STROGA-1.md")
        with open(manifest_1, "w", encoding="utf-8") as f:
            f.write("# t\n")
            f.write("%s  organ-a/KNOWLEDGE.md\n"
                    % hashlib.sha256(open(telo_a, "rb").read()).hexdigest())
            f.write("%s  organ-b/KNOWLEDGE.md\n"
                    % hashlib.sha256(open(telo_b, "rb").read()).hexdigest())
        pomet1, _ = pulz_dih(dih_koren, manifest_1)
        open(telo_a, "w").write("ena spremenjena")
        os.makedirs(os.path.join(dih_koren, "organ-c"))
        open(os.path.join(dih_koren, "organ-c", "KNOWLEDGE.md"), "w").write("tri")
        os.remove(telo_b)
        pomet2, vrstice_dih = pulz_dih(dih_koren, manifest_1)
        stanja = [v.split(" :")[0].strip() for v in vrstice_dih
                 if any(k in v for k in ("SPREMENJENO", "NOVO", "IZGINILO"))]
        pripis("T13-dih", pomet1 == 0 and pomet2 == 2
               and len([s for s in stanja if "SPREMENJENO" in s]) == 1
               and len([s for s in stanja if "NOVO" in s]) == 1
               and len([s for s in stanja if "IZGINILO" in s]) == 1,
               "pulz čist %d ⭢ pomet %d ( sprem 1 ∧ izg 1 ; novo ni pomet )" % (pomet1, pomet2))

        # T14 : ⟨REHAB-VEZA⟩ ( povrni bajtno iz genize priče )
        geniza_par = os.path.join(dom, "geniza", "telo-vrata.md")
        shutil.copy(telo_vrata, geniza_par)
        with open(telo_vrata, "w", encoding="utf-8") as f:
            f.write("ranjeno telo\n")
        predlog_pot = os.path.join(dom, "predlog-telo-vrata.md")
        uspelo, _ = povrni_telo(telo_vrata, os.path.join(dom, "geniza"),
                                predlog_pot)
        bajtno = (open(predlog_pot, "rb").read()
                  == open(geniza_par, "rb").read())
        nemogoce, _ = povrni_telo(os.path.join(dom, "neznano.md"),
                                  os.path.join(dom, "geniza"),
                                  os.path.join(dom, "predlog-neznano.md"))
        pripis("T14-povrni", uspelo and bajtno and not nemogoce,
               "predlog bajtno ist priči ⊢ ; brez priče = padec")

    # T9 : priča komputacije ( md5 znane vrednosti ⊢ )
    znani = hashlib.md5(b"abc").hexdigest()
    pripis("T9-prica", znani == "900150983cd24fb0d6963f7d28e17f72",
           "md5 %s" % znani)

    # T10 : samoizmerba ( lastno telo po lastnem cenzusu )
    with open(os.path.abspath(__file__), "rb") as f:
        svoje = f.read().decode("utf-8", errors="strict")
    ulovi, _, _ = cenzus(svoje)
    pripis("T10-samoizmerba", len(ulovi) == 0,
           "trdih ulovov v lastnem telesu ×%d" % len(ulovi))

    # T15 : ⟨KUBIT-KOVANJE⟩ zakoni nad zapečenima registroma
    r1, r2 = kubit_mnozice()
    p1 = [x for v in r1 for x in v]
    p2 = [x for v in r2 for x in v]
    vsi = p1 + p2
    palindromi = [p for p in vsi if ("%04d" % p) == ("%04d" % p)[::-1]]
    rob_nicla = [p for p in vsi if str(p)[0] == "0" or str(p)[-1] == "0"]
    set_vsi = set(vsi)
    obrati_zasedeni = [p for p in vsi
                       if int(("%04d" % p)[::-1]) in set_vsi]
    drs_okupirane = [p for p in vsi if "%04d" % p in drsenje()]
    pripis("T15-kubit",
           (len(KUBIT_R1_VRSTE) == 87 and len(KUBIT_R2_VRSTE) == 87
            and len(p1) == 348 and len(p2) == 348
            and len(set_p1()) == 348 and len(set_p2()) == 348
            and len(set_vsi) == 696
            and not set_p1() & set_p2()
            and not palindromi and not rob_nicla
            and not obrati_zasedeni and not drs_okupirane
            and KUBIT_R1_VRSTE[0][1:] == SIGIL_R1
            and KUBIT_R2_VRSTE[0][1:] == SIGIL_R2),
           "vrst 87 ∧ 87 ; piramid 348 ∧ 348 ; unikatnih 696 ; prekrivanje 0 ; "
           "palindromi 0 ; obrati 0 ; drsenje 0 ; sigila ⊢")

    # T16 : kovanje po formuli ∧ kuri ( priči uradno določene teorije )
    drs = drsenje()
    zasedeni = kubit_zasedenost()
    kovanec = kov_kocko(2299, {3691, 3698}, drs)
    osnova_p = osnova_piramide(20572, 7)
    pripis("T16-kovanje",
           kovanec == (3299, 7897, 8093, 3705) and osnova_p == 1004
           and "1011" in drs and "1101" in drs,
           "kovanec 2299 ⭢ %s ⊢ ; osnova 20572×7 = %d ⊢ ; drsenje 1011 ∧ 1101 ⊢"
           % (str(kovanec), osnova_p))

    zeleni = sum(1 for _, z, _ in baterija if z)
    pripisi = ["%s %s : %s" % (ime, ("ZELENO ⊢" if z else "RDECE ⚠"), podrobno)
               for ime, z, podrobno in baterija]
    pripisi.append("baterija %d/%d ZELENO" % (zeleni, len(baterija)))
    return (zeleni == len(baterija)), pripisi


def set_p1():
    return set(x for v in KUBIT_R1_VRSTE for x in v[1:])


def set_p2():
    return set(x for v in KUBIT_R2_VRSTE for x in v[1:])


# -------------------------------------------------------------- izhodi ----
def zapis(ime, vrstice, zgovori, glava):
    if zgovori:
        print(glava)
        for v in vrstice:
            print(v)
    else:
        dom = os.path.join(os.getcwd(), ".geniza", "ograja")
        os.makedirs(dom, exist_ok=True)
        with open(os.path.join(dom, ime), "w", encoding="utf-8") as f:
            f.write(glava + "\n")
            for v in vrstice:
                f.write(v + "\n")


def glavna(argv):
    if len(argv) < 2:
        sys.stderr.write("raba : ograja.py tujke|sled|prica|vrata|belo|dih|"
                         "povrni|ventil|samopreizkus DATOTEKA... "
                         "[--zgovori] [--strogo] [--vrstice a-b,c] [--prag N] "
                         "[--manifest price.tsv] [--belo belo.tsv] "
                         "[--kocke DOSJE...] [--geniza MAPA]\n")
        return 2
    ukaz = argv[1]
    ostali = list(argv[2:])
    zgovori = "--zgovori" in ostali
    ostali = [u for u in ostali if u != "--zgovori"]
    strogo = "--strogo" in ostali
    ostali = [u for u in ostali if u != "--strogo"]
    zapezi = "--zapeči" in ostali
    ostali = [u for u in ostali if u != "--zapeči"]

    def vzemi_zastavico(ime):
        if ime in ostali:
            i = ostali.index(ime)
            vrednost = ostali[i + 1]
            del ostali[i:i + 2]
            return vrednost
        return None

    def vzemi_vec_zastavic(ime):
        vrednosti = []
        while ime in ostali:
            i = ostali.index(ime)
            vrednosti.append(ostali[i + 1])
            del ostali[i:i + 2]
        return vrednosti

    prag_niz = vzemi_zastavico("--prag")
    prag = float(prag_niz) if prag_niz else 70.0
    vrstice_niz = vzemi_zastavico("--vrstice")
    manifest = vzemi_zastavico("--manifest")
    belo = vzemi_zastavico("--belo")
    geniza = vzemi_zastavico("--geniza")
    izhod = vzemi_zastavico("--izhod")
    napisi = vzemi_zastavico("--napisi")
    kocke_poti = vzemi_vec_zastavic("--kocke")
    price_poti = vzemi_vec_zastavic("--iz")

    # ⟨VENTIL-ORODJA⟩ : pred vsakim merjenjem se merilec umeri
    if ukaz != "ventil":
        stanje, sporocilo = ventil_preslusaj()
        if stanje == "instrument-laze":
            sys.stderr.write("⟨VENTIL-ORODJA⟩ ⚠ %s\n" % sporocilo)
            sys.stderr.write("instrument laže ; izhod 2 ; merjenje zavrnjeno\n")
            return 2
        if stanje == "nezapečeno":
            sys.stderr.write("⟨VENTIL-ORODJA⟩ ⚠ ogra %s\n" % sporocilo)
        elif stanje == "padec":
            sys.stderr.write("⟨VENTIL-ORODJA⟩ ⚠ padec berbe : %s\n" % sporocilo)
            return 2

    stanje = tik()

    if ukaz == "ventil":
        if zapezi:
            uspelo, sporocilo = ventil_zapeci()
            print(("⟨VENTIL-ORODJA⟩ %s" % sporocilo)
                  if uspelo else ("⟨VENTIL-ORODJA⟩ ⚠ %s" % sporocilo))
            return 0 if uspelo else 2
        st, sporocilo = ventil_preslusaj()
        print("⟨VENTIL-ORODJA⟩ stanje : %s" % st)
        print(sporocilo)
        return 0 if st in ("zapečeno-skladno", "nezapečeno") else 2

    if ukaz == "samopreizkus":
        zeleno, pripisi = samopreizkus()
        print("⟨OGRAJA⟩ v%s samopreizkus @TIK %s ( ventil : %s )"
              % (VERZIJA, stanje, ventil_preslusaj()[0]))
        for p in pripisi:
            print(p)
        return 0 if zeleno else 2

    # dosjei uradnih kod ( ⟨SAMO-KOCKE⟩ : uradne kocke pred predlogom )
    uradne = {}
    extra_zasedenost = []
    for kd in kocke_poti:
        if os.path.exists(kd):
            dosje = beri_dosje(kd)
            uradne.update(dosje)
            extra_zasedenost.append(set(
                int(re.sub(r"[^0-9]", "", t)) for v in dosje.values()
                for t in v))
    zasedeni = kubit_zasedenost(extra_zasedenost) if kocke_poti \
        else kubit_zasedenost()
    drs = drsenje()

    if ukaz == "tujke":
        if not ostali:
            sys.stderr.write("raba : ograja.py tujke DATOTEKA...\n")
            return 2
        belo_mnozica = beri_belo(belo) if belo else None
        vrstice = []
        vsota = 0
        predpomnilnik = {}
        for pot in ostali:
            besedilo, napaka = preberi(pot)
            if besedilo is None:
                vrstice.append("## %s : RANA neberljivosti ⚠ bajt pri odmiku %d"
                               % (pot, napaka))
                vsota += 1
                continue
            ulovi, nfd, znakov = cenzus(besedilo, strogo=strogo, belo=belo_mnozica)
            vsota += len(ulovi)
            vrstice.append("## %s : znakov %d ; ulovi ×%d ; nfd gostje ×%d"
                           % (pot, znakov, len(ulovi), nfd))
            if ulovi:
                kocke = opisi_kocke(ulovi, uradne, zasedeni, drs, predpomnilnik)
                predpomnilnik.update(kocke)
                vrstice.extend(niz_ulovov(ulovi, kocke))
        vrstice.append("Σ ulovov ×%d %s" % (vsota, "⊢ ČISTO" if vsota == 0
                                            else "⚠ RANA"))
        zapis("tujke-%s.md" % stanje.replace(":", ""), vrstice, zgovori,
              "# tujke @TIK %s ( strogo : %s ; belo : %s )"
              % (stanje, strogo, belo))
        return 0 if vsota == 0 else 1

    if ukaz == "sled":
        if len(ostali) != 2:
            sys.stderr.write("raba : ograja.py sled PRED PO [--vrstice a-b,c] "
                             "[--prag N]\n")
            return 2
        regije = razberi_regije(vrstice_niz) if vrstice_niz else None
        izmera = sled(ostali[0], ostali[1], regije, prag)
        vrstice = [
            "vrstice PRED ×%d ⭢ PO ×%d ; bajti PRED %d ⭢ PO %d"
            % (izmera["vrstice_pred"], izmera["vrstice_po"],
               izmera["bajti_pred"], izmera["bajti_po"]),
            "dotaknjenih vrstic ×%d ( %.1f %% ; prag %.0f %% )"
            % (izmera["pomet_vrstice"], izmera["odstotek"], prag),
        ]
        vrstice.extend(izmera["opis"])
        rane = list(izmera["rane"])
        if regije is None and izmera["pomet_rana"]:
            rane.append("prepis celega telesa nad pragom ( sum pometov )")
        for r in rane:
            vrstice.append("RANA : %s ⚠" % r)
        if not rane:
            vrstice.append("sprememba znotraj mere ⊢")
        zapis("sled-%s.md" % stanje.replace(":", ""), vrstice, zgovori,
              "# sled @TIK %s : PRED %s ⭢ PO %s ( regije : %s )" %
              (stanje, ostali[0], ostali[1], vrstice_niz))
        return 0 if not rane else 1

    if ukaz == "prica":
        if not ostali:
            sys.stderr.write("raba : ograja.py prica DATOTEKA...\n")
            return 2
        vrstice = poroci_price(ostali)
        zapis("prica-%s.md" % stanje.replace(":", ""), vrstice, zgovori,
              "# prica @TIK %s" % stanje)
        return 0

    if ukaz == "vrata":
        if not ostali:
            sys.stderr.write("raba : ograja.py vrata DATOTEKA... "
                             "[--manifest price.tsv]\n")
            return 2
        rane, vrstice = poroci_vrata(ostali, manifest, geniza=geniza,
                                     uradne=uradne, zasedeni=zasedeni,
                                     drs=drs, belo=belo)
        zapis("vrata-%s.md" % stanje.replace(":", ""), vrstice, zgovori,
              "# vrata @TIK %s ( manifest : %s ; geniza : %s )" %
              (stanje, manifest, geniza))
        return 0 if rane == 0 else 1

    if ukaz == "belo":
        price = price_poti
        if not price:
            sys.stderr.write("raba : ograja.py belo --iz PRIČA... "
                             "--izhod belo.tsv\n")
            return 2
        belo_read = os.path.join(os.getcwd(), ".geniza", "ograja",
                                 "belo-%s.tsv" % stanje.replace(":", ""))
        pot_izhoda = izhod or belo_read
        mesta = set()
        for p in price:
            mesta |= beri_prico_za_belo(p)
        _imedat = os.path.dirname(pot_izhoda)
        if _imedat:
            os.makedirs(_imedat, exist_ok=True)
        with open(pot_izhoda, "w", encoding="utf-8") as f:
            f.write("# ⟨BELO-NAVODILO⟩ @TIK %s ; priče : %s\n"
                    % (stanje, ", ".join(priipce_ime(p) for p in price)))
            for cp in sorted(mesta):
                f.write("%d\n" % cp)
        print("belo navodilo ⊢ : %s ( mest ×%d )" % (pot_izhoda, len(mesta)))
        return 0

    if ukaz == "dih":
        koren = ostali[0] if ostali else "/home/user/knowledge"
        vzorec = manifest or os.path.join(koren, "simbol-lint",
                                          "MANIFEST-STROGA-*.md")
        if manifest and os.path.isfile(manifest):
            pot_manifesta = manifest
        else:
            pot_manifesta, _ = najnovejsi_manifest(vzorec)
        if not pot_manifesta:
            sys.stderr.write("⟨STALNI-DIH⟩ ⚠ manifest MANIFEST-STROGA manjka "
                             "( vzorec : %s )\n" % vzorec)
            return 2
        pomet, vrstice = pulz_dih(koren, pot_manifesta)
        zapis("dih-%s.md" % stanje.replace(":", ""), vrstice, zgovori,
              "# dih @TIK %s ( koren : %s )" % (stanje, koren))
        return 1 if pomet else 0

    if ukaz == "povrni":
        # ⟨REHAB-VEZA⟩ : --iz GENIZA ( glavna zastavica po glavi ) ∨ --geniza
        geniza_pot = geniza or (price_poti[0] if price_poti else None)
        if len(ostali) != 1 or not geniza_pot or not napisi:
            sys.stderr.write("raba : ograja.py povrni TELO --iz GENIZA "
                             "--napisi PREDLOG\n")
            return 2
        uspelo, vrstice = povrni_telo(ostali[0], geniza_pot, napisi)
        zapis("povrni-%s.md" % stanje.replace(":", ""), vrstice, zgovori,
              "# povrni @TIK %s ( telo : %s ; geniza : %s )" %
              (stanje, ostali[0], geniza_pot))
        return 0 if uspelo else 2

    sys.stderr.write("neznan poklič : %s\n" % ukaz)
    return 2


def priipce_ime(pot):
    return os.path.basename(pot)


if __name__ == "__main__":
    try:
        sys.exit(glavna(sys.argv))
    except NapakaOgraje as e:
        sys.stderr.write("padec instrumenta : %s\n" % e)
        sys.exit(2)
