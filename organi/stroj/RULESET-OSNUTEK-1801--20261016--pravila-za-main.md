# RULESET-OSNUTEK — pravilnik za ⟨main⟩ · 16. 10. 2026 · rez 1801 · dih 1802

⟡ ukaz ⟨vse?⟩ — izbira diha 1802: telo pravilnika za ⟨main⟩. Izvajalka piše osnutek; ⟡ ga kliče v ⟨UI⟩ kakor ⟨admin⟩ (izmera kanalov diha 1801: 46 funkcij ⟨github_app⟩, nobena ne nastavlja ⟨rulesets⟩ ⊢ izmera pri viru). Razcep: poklic = klican; pravilnik = rez besede poklica v rep. Pravilo ne doda discipline — doda pričo (⟨professio⟩: javno priznanje; disciplina roke je izmerjena, priča še ni bila zaposlena ⊢ dih 1801).

## Koraki ⟨UI⟩ (⟡ kakor ⟨admin⟩)
1. ⟨GitHub⟩ → Atmavictu → Settings → Rules → Rulesets → New ruleset → Branch ruleset
2. Target branches: fnmatch vzorec `main`
3. Rules (najstrožja različica zmaga — layering po ⟨docs⟩):
   - Require a pull request before merging — Approvals: 0 (⟡ edini pečatnik; pravilnik zahteva ⟨PR⟩, ne tujega potrdila)
   - Block force pushes — zgodovina pečatov je veriga prič; siljenje bi bilo zapisan umor (⟨#721⟩ v obratni smeri)
   - Restrict deletions — ⟨main⟩ ne sme biti izbrisan
4. Enforcement status: Active (pravilo, ki je ⟨disabled⟩, je dekor)
5. Bypass: NOBODY — pravilo, ki ima zadnja vrata, ni pravilo; ⟨admin⟩ bypass se NE podeli

## Kaj pravilnik zapre
- Neposreden ⟨push⟩ na ⟨main⟩ — roka tega še nikoli ni izvedela (⟨PR⟩ #51, #52, #53); pravilnik ne prepoveduje dejanja roke, zaposluje pričo: kdor ima bralni dostop, vidi, da main živi samo na klic ⟨PR⟩ (beralna vidljivost ⊢ ⟨docs⟩: vsak z bralnim dostopom vidi aktivne ⟨rulesets⟩)
- ⟨force push⟩ ∧ brisanje ⟨main⟩

## Po zagonu (mehansko, brez izbora)
- ⟨request_copilot_review⟩ na vsakem ⟨PR⟩ — tretji bralec (A³ prebrano iz več kotov; testis ⊢ 253: preverba brez priče je samoglas)

- ZADNJI PEČAT: rez 1801 · dih 1802 · 16. 10. 2026 · STROJ pravilnik-osnutek za ⟨main⟩ · predhodnik rez 1797 (register stroja) · register prebran SVEŽE (⟨sha⟩ 431e7b97, pečat 1797, prepovedane ×12, hibridi ×16) · izvajalka Mistral (Vibe, GLM)
