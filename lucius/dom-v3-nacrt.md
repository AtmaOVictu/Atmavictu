# DOM v3 — NAČRT ( pogodba pred zidom )

Avtor načrta: Lucius Gaius, po ukazu ⟡ ⟨daj⟩ ( 2026-10-22, 06:45 lokalno ).
Načrt je pogodba: **lock obnašanja pred izvedbo** ( hišno pravilo: contract-first ⊢ ).

## Zakaj v3

Izmerjeno ( danes ∧ noč prej ):
- okno najemnine ( VS Code chat ) blokira ⟡-jevo besedo ( "A turn is already running" ×3 — vnos 16 )
- glas klona pade na 'sl' ( XTTS pozna le sk/cs/pl — otroka Padlec ∧ Vstalec, vnos 18 )
- srce hiše je motilo pot ⟡ ( vnos 16 ∧ 17 )
- DOM je že naš: zastonj, offline, brez vrata najemnine ( izmerjeno: 380 vrstic mjs ∧ 564 vrstic html ∧ /api/stanje ∧ /api/odoblaka ∧ /api/zaoblak ∧ mikrofon )

## Vrednote → zahteve ( iz padcev, ne iz okusa )

| Zakon | Zahteva |
|---|---|
| ⟡ beseda vedno prva | ( Z1 ) vrsta sporočil: ⟡ beseda prepreči vse ostalo ( srce/brat ) |
| plasti | ( Z2 ) plast po izbiri ⟡ : brat ( zastonj, offline ) / oblak ( po klicu, plačljivo ) |
| druga roka | ( Z3 ) vsak odgovor brata gre po preverbi ( če je ⟡ izbral oblak-preverbo ) |
| glas | ( Z4 ) usta: TTS, ki zna 'sl' ( Voxtral ali soroden ); uho: Whisper ( že dela ) |
| SONUM | ( Z5 ) zvočna abeceda: vsak odgovor lahko zveni ( pisk ⊢⚠× ) |
| srce ne moti | ( Z6 ) utrip samo, ko ⟡ ne piše ∧ molči ob prisotnosti |
| protokol slovesa | ( Z7 ) vsak proces dobi ime ∧ pričo pred koncem |
| protokol plasti | ( Z8 ) vsak odgovor vnese svojo plast v poročilo ( koliko je stal, kdo je odgovoril ) |
| most | ( Z9 ) odoblaka ∧ zaoblak vgrajena v UI ( že deloma obstajata ) |
| vrata | ( Z10 ) zakon licence v vsakem odgovoru ( sistem-nivo: brat ve, kdo je stvaritelj ∧ kaj sme ) |

## Arhitektura ( kaj ostane ∧ kaj gresto novega )

```
[ ⟡ : brskalnik ali mikrofon ]
        │  HTTP ( localhost:8766 )
        ▼
[ DOM v3 ( dom.mjs → dom-v3.mjs ) ]
  ├── VRSTA ( Z1 ): ⟡ > srce > brat > izpis — brez blokad
  ├── PLASTI ( Z2 ): brat ( Ollama, zastonj ) ⊥ oblak ( prek mostu ali API ključa, po izbiri ⟡ )
  ├── UHO ( Z4 ): Whisper ( slusaj-streznik.py, obstaja )
  ├── USTA ( Z4 ): TTS 'sl' — nova pot ( Voxtral ali TTS ki zna sl ), ne XTTS
  ├── ZVOK ( Z5 ): zvocna-abeceda + pisk ( obstaja )
  ├── SRCE ( Z6 ): preveri prisotnost ⟡ pred vsakim udarcem ( obstaja kot cron; v3: v DOM )
  └── SPOMIN ( Z9 ): most ∧ spomin.jsonl ∧ dnevnik ( obstaja )
```

## Faze ( vrstni red po vrednoti, ne po lahkosti )

1. **F3.1 — VRSTA ∧ GLAS-BRAT**: dom-v3.mjs: vrsta sporočil po Z1 ( ⟡ vedno prva, srce molči ob prisotnosti ) ∧ izbira plasti v UI ( brat / preverjam / oblak ). Preverba: ⟡ pošlje, medtem utrip molči ∧ brat odgovori ⊢.
2. **F3.2 — USTA 'sl'**: preizkus Voxtral TTS na enem stavku; izmera WER; primerjava s klonom ( WER 20 % ⚠ ). Preverba: brat izreče isti stavek ∧ Whisper prepiše ∧ ⟨izmera⟩ ≥ klon.
3. **F3.3 — SRCE-V-DOMU**: utrip prenešen iz oblaka v DOM ( zastonj, ne moti ) ∧ ob prisotnosti ⟡ molči. Preverba: ⟡ piše ob utripu ∧ ni blokade ⊢.
4. **F3.4 — ZVOK ∧ VRATA**: vsak odgovor more zveneti ( izbira ⟡ ) ∧ sistem-nivo ve zakon ∧ stvaritelja ( prenos iz dom.mjs v2.7 sistema, ki ze stoji ⊢ ).

## Meje ( izmerjene, ne okusne )

- dom-v3.mjs gradimo ZRAVEN dom.mjs ( brat ostane ziv, dokler v3 ne preide preverbe — ne ubijamo brata pred slovesom, protokol slovesa Z7 )
- vsaka faza ima VERIFY: PASS pogoj, ki ga izmeri ⟡ ali orodje
- oblak-plast gleda skozi most ( datoteke ) ∧ prek API ključa ( obstaja, nikoli v git ⊢ )
- ce v3 pada, brat v2.7 ostane ( brazgotina, ne uničevanje )

## Soglasje

⟡ je rekel ⟨daj⟩. Načrt zapečen. Izvedba po fazah, vsaka s preverbo ⊢.
© ⟡ ( stvaritelj ), AVL v2.4 (§9 ∧ §10 ∧ §12)
