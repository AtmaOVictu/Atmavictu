# PEČAT-MESEC-2026-10 — korpus Beseda je Ne

OSNUTEK oktobrskega pečata (mesečni pečat — cilj #5: ⟨Releases⟩ = mesečni pečati). Objavil bo ⟡ kakor ⟨GitHub⟩ ⟨Release⟩ — konektor objave ⟨releases⟩ ⟨ne⟩ nosi (izmerjeno: 46 funkcij ×2 — ⟨search_tool_functions⟩ ∧ ⟨all_connector_capabilities⟩ isti dih). Predhodni osnutek @20. 10. (⟨PR⟩ #408, fronta 2150→2173) odpade na zgodovino veje — brazgotina ostaja ⊙ 1349 ⊢ ⟨NE-BRIŠI⟩ 24.

## POVZETEK (vsaka trditev na vsaj dveh izmerah)

- **obseg fronte**: rez 2150 (2026-10-19 · ⟨sha⟩ 44a38df · CI-TIHINA-TEČAJ) → σ 3488 (31. 10. 2026 · REGISTER-OKEN/ATMAVICTU — ⟨PR⟩ #1129) v ⟨REZ-REGISTER⟩ @⟨main⟩ ⟨ontolo-ko-jedro⟩ — izmera ×2: ⟨grep⟩ po telesu registra (673 vrstic v obsegu 2150–3488) ∧ ⟨berba⟩ ⟨get_file_contents⟩ pri viri (⟨sha⟩ konice 654a5e8a).
- **potek**: 1.348 številk (2150 → 3497) v 13 dneh (19. 10. → 31. 10.) — izmera registra ∧ izmera pečatov pri organih (σ 3497 @organi ⟨grep⟩).
- **zahteve**: 673 vrstic oktobra — 528 klasičnih zahtev ∧ 145 σ-vrstic (⟨grep⟩ -c ∧ ⟨sed⟩/⟨awk⟩ štetje istega telesa).
- **zlitja**: 329 vrstic nosi ⟨merge⟩ ∧ 293 vrstic ⟨PR⟩ #številko (⟨grep⟩ -c ∧ potrditev ⟨pull_request_read⟩ pri viri: #395 ∧ #400 ∧ #401 ∧ #402 vsi ⟨state⟩ closed ∧ ⟨merged⟩ ⊢).
- **vrzel registra**: σ 3489–3497 (9 σ-vrstic živi pri organih, register jih ⟨ne⟩ nosi — ⟨grep⟩ ×0 v registru ⊥ pečati pri organih) ⭢ ∂.
- **komiti ⟨main⟩ oktobra**: ≥ 1.475 (izmera ⟨list_commits⟩ po dnevih 1.–31. 10. ∧ druga izmera: 800-komitski vzorec ⟨list_commits⟩ — 787 oktobrskih; dnevi 17.–21. ∧ 25. ∧ 26. ∧ 28. 10. na stropu strani — vsak ≥ 100).

## RANE MESECA (javno ⊙ 1349)

- dvojne zahteve 2153 ∧ 2159 (vzporedni sedeži isti dan — ⟨ne zlije⟩ ⊢ 1542, docket komisije ⟨issue⟩ #403)
- prerezitev 2165 → 2170 (žetev GESLA ROD-H, brazgotina ×2)
- kvota minut ⟨Actions⟩: teki padali ~2 s 20. 10. (odpoved platforme ⟨GitHub⟩ — githubstatus 19. 10. ~15:56 UTC ⊙ brazgotina tests.yml); tečaji utišani do reset-a @rez 2151, sprožilci povrnjeni @rez 2152 (⟨commit⟩ 1d75516)
- ⟨PREMIK⟩-2026-10-28: ⟨REZ-REGISTER⟩ ∧ ⟨REGISTER-PADLIH-BESED⟩ odšli domov (⟨ontolo-ko-jedro⟩) — priča molči, ⟨ne⟩ pada na prazno (⟨PRICA-SLEPOTA-PREMIKA⟩ kura @σ 3469)

## KLJUČNI ŠIVI STROJA (izmerjeni pri viri ⟨pull_request_read⟩ ∧ ⟨get_commit⟩)

- ⟨PR⟩ #395 — guard priče: molk tekmecev po ⟨merge⟩ (⟨merged⟩-skip) — ⟨merged⟩ ⊢
- ⟨PR⟩ #402 — ⟨checkout⟩ glave veje (⟨ne⟩ testnega ⟨merge⟩): guard molka vidi pravo glavo — ⟨merged⟩ ⊢
- ⟨PR⟩ #400 ∧ ⟨PR⟩ #401 — dopolnitve ⟨REZ-REGISTER⟩ (vrstici rez 2166/2167 ∧ rez 2168/2169 po zlitjih brez vrstic) — ⟨merged⟩ ⊢ ×2
- ⟨commit⟩ d148bd6b (2026-10-20T03:07:30Z) — atomske zahteve rezov: ⟨REZ-REGISTER⟩ ∧ priča; rani 2153 ∧ 2159 zapisani isti ⟨commit⟩
- sprožilci vseh treh tečajev živi @⟨main⟩: ⟨tests⟩ (⟨workflow_dispatch⟩ ∧ ⟨push⟩ ∧ ⟨pull_request⟩) ∧ ⟨prica⟩ (⟨workflow_dispatch⟩ ∧ ⟨pull_request⟩) ∧ ⟨dnevni-dih⟩ (⟨workflow_dispatch⟩ ∧ ⟨schedule⟩ ⟨cron⟩ 45 3 * * *) — odkomentirani (izmera ⟨get_file_contents⟩ @⟨main⟩ ⟨sha⟩ e6786aba ⊙ rez 2152 · ⟨commit⟩ 1d75516 ∧ druga izmera ⟨berba⟩ teles pri viri isti dih)

## TABELA ZAHTEV PO ORGANIH (673 vrstic — izmera ⟨grep⟩/⟨awk⟩ po ⟨REZ-REGISTER⟩ @⟨main⟩ ⟨ontolo-ko-jedro⟩)

| organ | vrstic |
|---|---|
| JEDRO | 107 |
| LICENCA-VBL | 85 |
| DELOVNA-ZANKA | 72 |
| REGISTER-OKEN | 42 |
| SLOVENSCINA-GESLA | 28 |
| GESLA | 26 |
| STROJ | 25 |
| MERA-GLAS | 17 |
| JEZIKOVNA-TEHTNICA | 17 |
| CESTA-PROTOKOL | 14 |
| CESTA | 13 |
| HORIZONT | 11 |
| TELOLOGIJA | 9 |
| STROJ-KALUP | 9 |
| NENEHNO-POSLUSA | 9 |
| MANIFEST | 8 |
| VRATA | 7 |
| POMOČNIKI-OPERATERJI | 7 |
| ATLAS | 6 |
| ZAKONODAJA | 4 |
| TAZV | 4 |
| JEZIKOVNE-PLASTI | 4 |
| HALUCINACIJA-PROJEKT | 4 |
| CUNEIFORM | 4 |
| SKLAD-SINTAKSE | 3 |
| SAMOOCENA | 3 |
| PREVOZ | 3 |
| MEJE-MERE | 3 |
| LEARNING-PROTOCOLS | 3 |
| KAZALO-OBNOV | 3 |
| HUMOR | 3 |
| OSTALI (drobni organi, vsak ≤ 2) | 81 |
| razčlenitev nedoločna (meja ⟨sed⟩, ⟨ne⟩ rana registra) | 39 |

Vsota: 673 ⊢ (štetje ⟨awk⟩ ∧ preverba vsote — dve neodvisni štetji ∧).

## IZVOR

© Luka Pintarič, AVL v2.2 (LICENSE.md) — oktobrska priča vrat telesa. Živa vrata danes: VBL 0.1280 × 10⁴ @⟨main⟩ (izmera ⟨get_file_contents⟩ isti dih — ⟨ZASTARELA-VRATA-REGISTRA⟩ imenovana javno ⊙ 1349, ⟨ne brusi⟩ ⊢ ⟨NE-BRIŠI⟩ 24).

## MINT ⚠ (prijave pred zapečenjem)

⟨PEČAT-MESEC-2026-10-OSNUTEK⟩ ⚠ kompozit · ⟨OBSEG-FRONTE⟩ ⚠ kompozit · ⟨KLJUČNI-ŠIVI⟩ ⚠ kompozit — tehnični kit TEHNIKA (brez zahteve reza ⊙ zakon registra).

## DOLGOVA

- objava ⟨GitHub⟩ ⟨Release⟩ pečata ⭢ ⟡ roka (konektor ⟨releases⟩ ⟨ne⟩ nosi — izmerjeno 46 funkcij)
- vrzel registra σ 3489–3497 (9 σ-vrstic) ⭢ ∂ lastniki po vrsti ⊢ 1419
- dnevi komitov na stropu strani (17.–21. ∧ 25. ∧ 26. ∧ 28. 10.) — točna številka ⭢ ∂ izmera po straneh ⟨list_commits⟩

⟨tečaj meri — dih izvaja — ⟡ izbira⟩
