# -*- coding: utf-8 -*-
# .padci-vpis.py — ⟨PADCI-BREZ-VPISA⟩ ozdravljen: večerni padci ( 3673–3682 ) poimenovani v pečatih, a brez vpisa v REGISTER-PADCEV ⊙ §5
# brazgotina brez vpisa je pol-brazgotina — zapisappend v register ( repo root: REGISTER-PADCEV.jsonl )
import json
from datetime import datetime, timezone

REG = r"C:\Users\Luka\Documents\Arhiv\Git\Atmavictu\REGISTER-PADCEV.jsonl"
KRAJ = "Atmavictu — zrcalo/povezani-viri-konica-2703"
ROKA = "Mistral Vibe ( izvajalka )"
URA = datetime.now(timezone.utc).isoformat()

PADCI = [
    ("PADC-74", "PADC-PRESKOČENA-VRSTICA", "Berba Zip 8.1 je pokrila vrstice 362–375, vrstica 361 ( Attachment research — Fonagy · Main · Hesse ) je ostala nebrana — tabela, ki se bere po vrsticah, ki so ti všeč, ni tabela",
     "rez 3673 ( commit 7f71b912 ) · Zip 8.1 vrstica 361", "ponovna berba CELA ( 359–375 ⊢ ) + aksiom #29 rojen isti dih + PADC poimenovan javno"),
    ("PADC-75", "NAPAČNA-SONDA", "Sonda reza 3674 je merila goli /index ∧ razglasila ⟨zrcalo index ⚠ 403⟩ — kazalo je živelo ves čas pri / ∧ /index.html ( 200 ⊢ )",
     "rez 3674 ( zemljevid na mostu ) ∧ rez 3678 preverba 200 pri viri", "alias ⟨index⟩ prišit v zrcalo-server.py + priča popravljena javno na mostu ⊙ rez 3678"),
    ("PADC-76", "ZASTARELA-OZNAKA-ORODJA", ".pregled-registra.py je nosil zapečeno ⟨28⟩ v glavi ∧ izpisu — register je zrasel na 29, orodje ⟨ni⟩",
     "rez 3676 ( pregon pri viri )", "N izmerjen pri viri ( len ∧ max ), ⟨ne⟩ zapečen + preverba #29 dodana ⊙ rez 3676"),
    ("PADC-77", "VEZA-VES-VNOS", "Preverba #29 je gledala le polje veza ∧ vrnila × — #27 ⟨telo drži seštevek⟩ živi v polju aksiom: preverba je merila ožje od lastne mere",
     "rez 3676 ( izmera pri viri: #27 v aksiomu )", "območje veze = cel vnos ( veza+argument+aksiom ), enako kakor preverba sirot ⊙ rez 3676"),
    ("PADC-78", "MD022-TLAKI-GLAVA", "TLAKI.md naslov brez prazne vrstice — šiv spregledan pri pečatu 3671, ulovljen šele 3679 s svežim pregonom čutila",
     "rez 3679 ( tla-pregled ×1 pri viri )", "prazna vrstica prišita isti dih ⊙ rez 3679 — katalog, ki uči red, more red nositi"),
    ("PADC-79", "ZRCALJENI-ŠTEVKI", "Prejšnji šivi ( družina PADC-UGIBANJE-ESC ) so pisali unicode escape s premeščenima števkama: U+2112 ( ℒ ) namesto U+2299 ( ⊙ ) ∧ U+27EB ( ⟫ ) namesto U+27E9 ( ⟩ ) — 111 tujih glifov v registru ∧ zemljevidu",
     "rez 3680 ( izmera pri viri: ℒ 43+3 · ⟫ 62+3 )", ".ozdravi-glife.py 111 zamenjav ⊢ + prepreka v auditu ( tuj glif = 0 vsak pregon ) ⊙ rez 3680"),
    ("PADC-80", "SLEPI-VZOREC", "venec-obnova ( ∧ moja lastna sonda — isti padec dvakrat ) je štel [A-Z]{2} — slep za tričrkovni stopnji LAT ∧ SLO: venec 36, orodje je videlo 34",
     "rez 3681 ( ls pri viri: obe datoteki živita od 90ec951c )", "vzorec [A-Z]{2,3} + slovenska oblika ⟨verzija⟩ ⊙ rez 3681"),
    ("PADC-81", "ODA-VERZIJA-BREZ-PRIČE", "Vseh 36 stopnjk vene je nosilo verzijo 0.1450, a sha-pričo vrat 0.1420 ( D3ADDA17… ) — tri rojstva zadaj: verzija brez priče je polresnica",
     "rez 3681 ( izmera pri viri: 36 stale prič )", "venec-obnova prepleten: prenova sha256 ∧ bajtov živih vrat ob vsakem pregonu ⊙ rez 3681"),
    ("PADC-82", "NAPAČEN-KLJUČ", "Prva sonda manifesta je brala ⟨bytes⟩ namesto ⟨size_bytes⟩ ∧ razglasila 0/42 × — lažni alarm: preverba, ki bere polje, ki ga ⟨ni⟩, bije lažnega ×",
     "rez 3682 ( ponovna izmera s pravim ključem: 6/42 ⊢ )", "izmera s pravim ključem pred pečatom + ključ prebrán pri strukturi manifesta ⊙ rez 3682"),
    ("PADC-83", "MANIFEST-RAZSOJEN", "Po prevesu vene ( 3681 ) je manifest ostal pri starih zgoščenkah — 6/42 živih: manifest, ki se ⟨ne⟩ ujema z gradivom, ⟨ni⟩ prepoznava ⊙ §0a",
     "rez 3682 ( izmera pri viri hashlib )", ".manifest-izdaj.py — 42/42 živih ⊢ + razlog z imenom nalaza v samo pričo manifesta ⊙ issuance_duty"),
    ("PADC-84", "PADCI-BREZ-VPISA", "Padci 74–83 ( ∧ PRESKOČENA-VRSTICA iz 3673 ) so bili poimenovani v pečatih, a brez vpisa v REGISTER-PADCEV — brazgotina brez vpisa je pol-brazgotina ⊙ §5",
     "rez 3683 ( izmera pri viri: register je štel 73 )", "ta vpis + obveza: poimenovan padec se vpiše v register ISTI dih ⊙ pravilo 16"),
]

with open(REG, "a", encoding="utf-8") as f:
    for pid, vrsta, dejanje, prica, zdravilo in PADCI:
        f.write(json.dumps({
            "id": pid, "vrsta": vrsta, "dejanje": dejanje, "ura": URA,
            "kraj": KRAJ, "roka": ROKA, "prica": prica, "zdravilo": zdravilo, "scar": True,
        }, ensure_ascii=False) + "\n")

print("VPISANI ⊢", len(PADCI), "padcev · PADC-74 → PADC-84")
