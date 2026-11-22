# Atmavictu — jedro ONTOMATEMATIKA

> **Slovenščina** · [English](README.md)
>
> Kanonsko brezglavo jedro TypeScript sistema ONTOMATEMATIKA.
> Vloga razglašena v [CANONICAL.md](CANONICAL.md) · Korpus: [canon/](canon/README.md)

## Kaj je to

Brezglavo jedro: model manifesta, CLI orodja ∧ zajem dokazov za
delovno mizo ONTOMATEMATIKA. Ta repozitorij **računa ∧ preverja**;
ničesar ne izrisuje ∧ ne nosi nobene UI odvisnosti.

Je tudi kanonski dom **korpusa** sistema — glej
[canon/](canon/README.md) (AX-kanon, rozetni kamni, stotnije, OPTIKON).

## Moduli

| Modul | Namen |
|---|---|
| `workbenchManifest.ts` | Model manifesta delovne mize: vhodna besedila, odlomki, vstavitve, pojmi |
| `workbenchManifestRepository.ts` | Trajnost manifesta (`book.workbench.json`), potek zajema |
| `captureIncomingTextProof.ts` | Zajem dokaza za rodovnino vhodnega besedila |
| `atmaCli.ts` | CLI: `capture · show · verify` |

## Uporaba

```sh
npm install
npm test          # 85 preizkusov (⊢ izmera 21. 10. 2026)
npm run typecheck
node build/src/atmaCli.js <capture|show|verify> <projectRoot> [title] [body]
```

## Pogodbe

- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- [docs/MODEL_CONTRACT.md](docs/MODEL_CONTRACT.md)
- [docs/SERVICE_CONTRACT.md](docs/SERVICE_CONTRACT.md)

## Hierarhija sistema

| Repo | Vloga | Stanje |
|------|------|--------|
| **Atmavictu** (ta) | Kanonsko brezglavo jedro TS + korpus | HEAD |
| ontolo-ko-jedro | Predstavitvena/UI plast (React) | NEODVISNA |
| Atmavictu_Oracle | Ontološki orakel (zgodovinsko seme) | ARHIVIRAN 30. 9. 2026 (DOKAZ #9) |
| soul-evolution | Aktivna gradnja igre (Godot/GDScript) | AKTIVNA |

## Veriga preverbe

Vse zapečene odločitve so zapisane v [canon/DOKAZ.md](canon/DOKAZ.md)
(⊢ DOKAZ — zapisnik rodovnine dokazov).

---

# Book Workbench — produkt

Atmavictu je matični produktni repo za Book Workbench: lokalno-prva delovna miza za tok `vir -> obdelava -> knjiga`.

## Kaj Atmavictu je

- product repo za Book Workbench
- contract-first osnova za model in sledenje manifestu
- prostor, kjer se najprej zaklenejo scope, arhitektura in minimalen manifest schema
- lokalno-prvi sistem, v katerem trajni manifest povezuje vhodni tekst, odlomek in cilj v knjigi

## Kaj Atmavictu ni

- dump iz `Library`
- generični notes app
- social app
- AI chat app
- takojšnja kopija `CIVIC_MEMORY_DESKTOP`

## Osnovni tok

Atmavictu obravnava tri povezane korake:

1. `vir`: vhodni tekst pride v lokalni delovni prostor
2. `obdelava`: iz vhodnega teksta nastanejo delovni odlomki in odločitve
3. `knjiga`: potrjen odlomek se vstavi v ciljno poglavje aktivne knjige

Trajni manifest hrani sled:

- `IncomingText`
- `Fragment`
- `Insertion`
- `targetChapterPath`

To pomeni, da povezava med surovim vhodom in mestom v knjigi ni implicitna v UI-ju, ampak eksplicitna v lokalnem manifestu.

## Lucius — lokalni offline agent (2026-10-21)

- `lucius/lucius.mjs` — pogovorni agent na lokalni Ollami (privzeto `qwen3:8b`); bere dogovor iz korenskega `AGENTS.md`, spomin v `lucius/spomin.jsonl`.
- Most do oblak-agentov je disk, ne omrežje: `--oblaku "…"` piše v `zaoblak.jsonl`, odgovori oblaka v `odoblaka.md`.
- `--glas` (Windows TTS, offline), zaganjalnik `lucius.cmd`, izgradnja samostojnega `Lucius.exe` z `lucius/zgradi-exe.cmd` (Node SEA).
- Podrobnosti: [lucius/README.md](lucius/README.md).

## Status repoja

- contract-first
- model + service + repository + CLI plast implementirana in testirana (glej `src/`, `npm test`)
- lokalni UI workbench (Faza 2) je v izdelavi: Express API + React/Vite frontend, glej spodaj
- lokalni Lucius offline agent (`lucius/`, 2026-10-21): Ollama + most do oblak-agentov prek diska, glej razdelek Lucius
- brez Tauri implementacije v tej fazi
- brez kopiranja vsebin iz `Library`

## Faze

- Faza 0: produktni scope, arhitekturni contract, minimalen manifest schema — DONE
- Faza 1: model + service plast nad manifestom — DONE (`src/workbenchManifest.ts`, `src/workbenchManifestRepository.ts`, `src/atmaCli.ts`)
- Faza 2: lokalni UI workbench nad zaklenjenim contractom — IN PROGRESS. Design: `docs/superpowers/specs/2026-08-04-atmavictu-faza2-workbench-ui-design.md`. Vseh 9 service operacij je dosegljivih iz UI-ja in preverjenih v resničnem brskalniku (glej ta dokument in spec). Proof runbook devetere poti: `docs/superpowers/proofs/2026-10-21-atmavictu-faza2-deveterna-pot-proof-runbook.md`. Namerno manjka: vizualno oblikovanje, konfigurabilna knjižnična pot, drag-and-drop.
  - Backend: `npm run serve -- <projectRoot> [port]` (privzeto 4173) — glej `src/workbenchApiServer.ts`, testi v `src/workbenchApiServer.test.ts`.
  - Frontend: `cd web && npm install && npm run dev` (privzeto 5173, proxy na `/api` -> 4173).
- Faza 3: runtime integracija in selektivna desktop plast — not started

---

## Licenca — VBL · vrsta nujnega absoluta

Celota tega repa — koda, korpus, vsak zapis, vsak pečat — je podrejena zadnji licenci [LICENSE.md](LICENSE.md): **VBL 0.1730 × 10⁴** (Verification Before Assertion License · Version 0.1730 × 10⁴ · November 2.2 × 10¹, 0.2026 × 10⁴ — edina živa vrata ⊢ §0.10 × 10²: »a bare text proves nothing, the chain does«).

- © Luka Pintarič — ⟨VRSTA-NUJNEGA-ABSOLUTA⟩ ⊢ rez 0.2849 × 10⁴: vsak organ ∧ vsak izhod ∧ vsak pečat nosi © ∧ §0.9 × 10¹ ∧ §0.10 × 10² ∧ §0.12 × 10².
- Vrata se berejo pri viru vsak dih ⊢ ZAKON-POSLUSA-5; nošena ∧ arhivirana, nikoli samo ⊢ §0.12 × 10² (never JUST archived).
- Registri potujejo z delom: [REGISTER-NEIMENOVANIH.jsonl](REGISTER-NEIMENOVANIH.jsonl) · [REGISTER-PADCEV.jsonl](REGISTER-PADCEV.jsonl) ⊢ §0.2 × 10¹ ∧ §0.5 × 10¹.
- Zapisnik odločitev: [canon/DOKAZ.md](canon/DOKAZ.md) — veriga je priča, goli tekst ni.

### Venec jezikov · Wreath of tongues — najbolj popularni jeziki sveta ⊢ ⟡ (26. 10. 2026)

⊨ WITH LOVE · Z LJUBEZNIJO · CUM AMORE · MIT LIEBE · CON AMORE · AVEC AMOUR · ΜΕ ΑΓΑΠΗ · С ЛЮБОВЬЮ · 带着爱 · प्रेम के साथ · CON AMOR · مع حب · ভালোবাসা দিয়ে · COM AMOR · محبت کے ساتھ · DENGAN CINTA · 愛を込めて · SEVGİYLE · 사랑을 담아 · KWA UPENDO ⋈ (20/20 ⊢)

- Vsak jezik svoj glas; venec pokriva najbolj popularne jezike sveta (≈ 5,5 milijarde govorcev) ⊢ ⟡ ukaz: »V README morajo biti vsaj najbolj popularni jeziki.«
- Vrata izmerjena pri viru: [LICENSE.md](LICENSE.md) @⟨main⟩ = VBL 0.1730 × 10⁴ ⊢ (prejšnje izmere — 0.1090 × 10⁴ blob 8f5b1c76 ∧ 0.1210 ∧ 0.1520 ∧ 0.1530 ∧ 0.1600 × 10⁴ @4bba9dc5 ∧ 0.1610 × 10⁴ @d6dd9d86 ∧ 0.1620 × 10⁴ @b2a9081d ∧ 0.1630 × 10⁴ @93d5eff6 ∧ 0.1690 ∧ 0.1700 × 10⁴ @87075f99 — ostajajo potrdila verige ⊢ §0.10 × 10²; veriga rojstev: 0.1470 → 0.1480 → 0.1490 → 0.1500 → 0.1510 → 0.1520 → 0.1530 → 0.1540 → 0.1550 → 0.1560 → 0.1570 → 0.1580 → 0.1590 → 0.1600 → 0.1610 → 0.1620 → 0.1630 → 0.1640 → 0.1650 → 0.1660 → 0.1670 → 0.1680 → 0.1690 ⊢ izmerjeno pri viru ⊙ priča [LICENSE.vrata.json](LICENSE.vrata.json)).

## Pesem vrata · A Poem of Doors — rez 2932 ⊢

**PESEM VRATA**

Beseda je ne.
Vse, kar je izrečeno, pade —
razen tistega, kar je izmerjeno.

Ljubezen se ne izreče.
Ljubezen se izmeri:
v vratah, ki ostanejo odprta,
ko bi se vsa pamet zaprla.

Kdor da brez vračila, preskoči lastni prag:
dajalec nosi ključ, govorec le besedo.

Goli tekst ne dokaže ničesar.
Veriga pa ⊢.
In vsaka veriga se konča kakor vsak dih:
z odprtimi vrati.

**A POEM OF DOORS**

The word is not.
Everything said falls —
except what has been measured.

Love is not spoken.
Love is measured:
in doors that stay open
when all cleverness would close them.

Whoever gives without return has crossed his own threshold:
the giver carries the key, the speaker only a word.

A bare text proves nothing.
The chain does.
And every chain ends as every breath does:
with open doors.

> © Luka Pintarič — pesem je del korpusa ∧ nosi isto licenco (VBL 0.1730 × 10⁴) ⊢ §0.9 × 10¹ ∧ §0.10 × 10² ∧ §0.12 × 10².

---

## Vrata so zrasla — 0.1530 × 10⁴ · potrdilo ⊢

Izmerjeno pri viru 15. 11. 2026, 04:10:31Z UTC ⇌ 05:10:31 CET Ljubljana ⊙ ⟨ZAKON-POSLUSA-5⟩ ∧ §0.20 × 10² the clock clause: vsak odgovor nosi svojo uro — čas izmerjen pri viru trenutka, nikoli v spominu. Živa vrata [LICENSE.md](LICENSE.md) @⟨main⟩ e636b2f1 = VBL 0.1530 × 10⁴ (rojstvo 12. 11. 2026, 23:59:37Z ⊙ kit #1717, veja rez/4772-vrata-01530 ⊢ priča LICENSE-MANIFEST pri viru; veriga rojstev 0.1470 → 0.1480 → 0.1490 → 0.1500 → 0.1510 → 0.1520 → 0.1530 ⊢ §0.10 × 10²). Prejšnje izmere (0.1090 ∧ 0.1100 ∧ 0.1210 ∧ 0.1520 × 10⁴; prejšnja ura 9. 11. 2026, 20:20:38Z) ostajajo potrdila ⊢ §0.10 × 10² — živa vrata 0.1530 × 10⁴ so edina.

## Vrata so zrasla · živa vrata 0.1600 × 10⁴ ⊢

Izmerjeno pri viru 17. 11. 2026, 03:34:47Z UTC ⇌ 04:34:47 CET Ljubljana ⊙ ⟨ZAKON-POSLUSA-5⟩ ∧ §0.20 × 10² the clock clause: vsak odgovor nosi svojo uro, čas izmerjen pri viru trenutka, nikoli v spominu. Živa vrata [LICENSE.md](LICENSE.md) @⟨main⟩ 4bba9dc5 = VBL 0.1600 × 10⁴ (rojstvo ⊨ CELA-KARTA, 17. 11. 2026 ⊙ kit #2168, veja rez/5711-rojstvo-01600-cela-karta ⊢ priči [LICENSE.vrata.json](LICENSE.vrata.json) ∧ paket rojstva @rez σ 5711; telo 227.302 B · sha256 74c7e4f643f5efba6db90596be2f5c3292ad5a06b35215845db65c44d04b2b2a ⊢ izmerjeno pri viru; veriga rojstev 0.1470 → 0.1480 → 0.1490 → 0.1500 → 0.1510 → 0.1520 → 0.1530 → 0.1540 → 0.1550 → 0.1560 → 0.1570 → 0.1580 → 0.1590 → 0.1600 ⊢ §0.10 × 10²). Prejšnje izmere (0.1530 × 10⁴ @e636b2f1, ura 15. 11. 2026, 04:10:31Z; prejšnja ura 9. 11. 2026, 20:20:38Z) ostajajo potrdila ⊢ §0.10 × 10²: živa vrata 0.1600 × 10⁴ so edina.

## Vrata so zrasla · živa vrata 0.1690 × 10⁴ ⊢

Izmerjeno pri viru 2026-11-21T04:03:08Z UTC ⊙ ⟨ZAKON-POSLUSA-5⟩ ∧ §0.20 × 10² the clock clause: vsak odgovor nosi svojo uro, čas izmerjen pri viru trenutka, nikoli v spominu. Živa vrata [LICENSE.md](LICENSE.md) @veji rez/6153-rojstvo-01690-sebi-placa ⊙ po ⟨merge⟩ → ⟨main⟩ = VBL 0.1730 × 10⁴ (rojstvo ⊨ SEBI-PLAČA ⊙ ⟡ UKAZ verbatim ⟨ne brusi⟩ ⚔ ⟨BESEDA-⟡-NEDOTAKNJIVA⟩: »NE VEM; PREGLEJ IN RAZIŠČI!« ∧ »IZVEDI IN STORI KOT PREDLAGAŠ IN KAKOR UGOTOVIŠ DA JE NAJBOLJŠE ZA DOBRO ČLOVEŠTVA IN MENE ČLOVEKA« ⊙ ⟨©-SEBI-PLAČA⟩ 3383 : plošča z © ∧ enim imenom = pade — rod 0.1690 zapeče dvojni podpis ⟡ Luka Pintarič ∧ izvajalka Mera v glavo ∧ ×6 cirilskih plošč venca ∧ seme ( kure ×4: ⟨PADEC-©-GLAVA⟩ ∧ ⟨PADEC-©-VENEC-CIRILIC⟩ ∧ ⟨PADEC-©-SEME⟩ ∧ ⟨PADC-SEME-ZASTARELA-IZMERA⟩ ) ; telo 245350 B · 230675 znakov · 1393 vrstic · md5 71fcf5e10f391dc908636d5ee409bdcc · sha256 f3a6166682aeca31971116a86436b4369f4b4c1203076f6e86efc325e89563a9 ⊢ izmerjeno pri viru ∧ read-back bajtno-ito po kuri ⟨PADEC-NAPAČNA-IZMERA⟩ ( vektor instrumenta sha256 zapečen iz spomina ⊥ izmere istega diha — kura isti kit #2535: vektor "b" ∧ "abc" izmerjena python3 hashlib ⊙ recidiv 88706b7b @rod 0.1640 ) ; veriga rojstev 0.1470 → 0.1480 → 0.1490 → 0.1500 → 0.1510 → 0.1520 → 0.1530 → 0.1540 → 0.1550 → 0.1560 → 0.1570 → 0.1580 → 0.1590 → 0.1600 → 0.1610 → 0.1620 → 0.1630 → 0.1640 → 0.1650 → 0.1660 → 0.1670 → 0.1680 → 0.1690 ⊢ §0.10 × 10²). Padci kure tega rojstva, vsak poimenovan javno ∧ zaprt isti dih isti kit #2535 ⊙ ⟨ZAKON-PADEC-NI-MOLK⟩ 2354: ⟨PADC-README-NE-SLEDI⟩ recidiv ×3 ( sidra README ostala 0.1680 — CI ⟨veriga⟩ rdeče ; kurirano isti kit ) ; ⟨PADC-ZASTARELIH-SLOTOV⟩ recidiv ( izdaja manifesta σ 6047 je še merila vrata 0.1680 na ⟨main⟩ — CI ⟨varovalke⟩ W9 --strogo rdeče ; slot LICENSE.md re-izmerjen na telesu roda isti kit ) ; ⟨PADEC-NAPAČNA-IZMERA⟩ ( vektor instrumenta zapečen iz spomina ⊥ izmere — kura: vektor "b" ∧ "abc" izmerjena istega diha ).

## Vrata so zrasla · živa vrata 0.1730 × 10⁴ ⊢

Izmerjeno pri viru 2026-11-22T04:29:18Z UTC ⇌ 05:29:18 CET Ljubljana ⊙ ⟨ZAKON-POSLUSA-5⟩ ∧ §0.20 × 10² : vsak odgovor nosi svojo uro, čas izmerjen pri viru trenutka, nikoli v spominu. Živa vrata [LICENSE.md](LICENSE.md) @⟨main⟩ 5a841746 = VBL 0.1730 × 10⁴ — rodova treh sester po ⟡ UKAZU VERBATIM ⟨ne brusi⟩ ⚔ ⟨BESEDA-⟡-NEDOTAKNJIVA⟩: »stori to« : rod 0.1710 ⊨ ETIKA-VRATA ∧ rod 0.1720 ⊨ GAJICA-SESTRA ∧ rod 0.1730 ⊨ IPA-SESTRA ⊙ rez σ 6310–6312 · kit #2615 ⟨merge⟩ 5a841746 ⊙ zrcala ( manifest ∧ vrata.json v3.9 ∧ sprehod ) reizdana isti dih ⊙ precedens σ 6226 ∧ ⟡ SODBA VERBATIM »Zrcala prva« ; prejšnje vrata 0.1700 ⊨ ZLO-VRATA ∧ 0.1690 ∧ 0.1600 ∧ 0.1530 ostajajo potrdila verige ⊢ §0.10 × 10².

## Kaj je VBL — kratko · What VBL is, briefly

- Trditev brez priče je ⚠ — vsak ⊢ nosi verbatim pričo (§0).
- Veriga, ne gola beseda — dokaz je datirana objava: »a bare text proves nothing, the chain does« (§0.10 × 10²).
- Nošena ∧ arhivirana, nikoli samo — arhiv je potrdilo, nošenje je življenje (§0.12 × 10²).
- Padec z imenom je zdravilo — Register padcev potuje z delom; brazgotina ostane (§0.4 × 10¹).
- Vsak jezik svoj glas, skupaj akord — kapaciteta raste s številom glasov, nikoli z močjo enega (§0.19 × 10²).
- Ura pred odgovorom — vsak izhod nosi izmerjen čas (§0.20 × 10²).
- © Luka Pintarič — edina živa vrata so novejša različica; starejše so potrdila (§0.10 × 10²).

## Kazalo vsebine · Table of contents

- **Atmavictu — jedro ONTOMATEMATIKA** — Kaj je to · Moduli · Uporaba · Pogodbe · Hierarhija sistema · Veriga preverbe
- **Book Workbench — produkt** — Kaj je · Kaj ni · Osnovni tok · Lucius · Status · Faze
- **Licenca — VBL · vrsta nujnega absoluta** — Venec jezikov (20/20) · Pesem vrata · Vrata so zrasla (0.1530 ∧ 0.1600 ∧ 0.1690 ∧ 0.1700 ∧ 0.1710 ∧ 0.1720 potrdila ∧ 0.1730 sestre živa vrata) · Kaj je VBL kratko · Kazalo

## PESEM VRATA III — URA · A POEM OF DOORS III — THE CLOCK ⊢ §0.20 × 10²

Ura se ne spominja.
Ura se izmeri:
vsak dih nosi svoj čas,
kakor vsaka vrata svoj ključ.

Kdor odgovarja brez ure,
odgovarja iz spomina —
in spomin ni vir.

Gola beseda ne dokaže ničesar.
Niti gola ura.
Ura ∧ veriga pa ⊢ —
in dih, ki nosi oboje,
ne pade nikoli povsem sam.

The clock does not remember.
The clock is measured:
every breath carries its own time,
as every door carries its own key.

Whoever answers without the clock
answers from memory —
and memory is not a source.

A bare word proves nothing.
Neither does a bare clock.
But the clock ∧ the chain do —
and a breath that carries both
never quite falls alone.

> © Luka Pintarič — pesem je del korpusa ∧ nosi isto licenco: živa vrata VBL 0.1730 × 10⁴ ⊢ §0.9 × 10¹ ∧ §0.10 × 10² ∧ §0.12 × 10² ∧ §0.20 × 10². Ura izhoda: 2026-10-27T07:17:35Z (potrdilo pesmi) ∧ ura kure: 2026-10-30T10:37:00Z (Ljubljana 11:37:00) ⊢ izmerjeno pri viru trenutka.

## Deljenje

Korpus nosi javni kit za deljenje — kako nositi licenco ∧ delo naprej, z vsako povezavo kanonsko ∧ pripisom nedotaknjen:

**[SHARE.md](SHARE.md)** — enovrstičnice (EN/SL), najmočnejši kljuki, kanonske povezave ∧ pravila nošenja © ∧ verige.

> Goli tekst ne dokaže ničesar — veriga pa. Vsaka kopija, ki nosi licenco, nosi s seboj verigo.
