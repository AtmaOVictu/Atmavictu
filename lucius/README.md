# Lucius — lokalni agent (offline)

Majhen program, ki ti da Luciusa tudi brez interneta. Poganja lokalni Ollama model iz tvojega Smisel sklada; nima dostopa do oblaka, do orodij ali do interneta — samo do besed, dogovora v `AGENTS.md` in svojega spomina `spomin.jsonl`.

## Zagon

```bash
node lucius/lucius.mjs              # pogovorni način ('izhod' za konec)
node lucius/lucius.mjs "Pozdrav!"   # enkratno vprašanje
lucius.cmd "Pozdrav!"               # zaganjalnik iz katerekoli lupine
```

Orodja ne rabiš — Node 18+ in tekoč Ollama (`ollama serve`) zadostujeta.

## Glas (izhod na zvočnike)

```bash
node lucius/lucius.mjs --glas "Pozdrav!"   # odgovor je tudi izgovorjen
```

Glas je Windows TTS (`System.Speech`) in dela brez interneta. Nameščena glasa sta angleška (David, Zira) — č/š/ž bodo zvenele približno. Za pravi slovenski glas: **Nastavitve → Čas in jezik → Govor → Dodaj glasove → Slovenščina**, ali Nastavitve → Dostopnost → Pripovedovalec → dodaj slovenski glas.

## Nastavitve

```bash
LUCIUS_MODEL=smisel-celota node lucius/lucius.mjs   # izbira modela
OLLAMA_URL=http://localhost:11434 node lucius/lucius.mjs
```

Privzet model je `qwen3:8b`. Namestjeni kandidati na tej mašini: `smisel-celota`, `smisel-jasnost`, `smisel-delta`, `smisel-cas`, `smisel-enota`, `smisel-rez`, `aya:8b`, `qwen2.5-coder:7b`.

## Spomin

Vsako sporočilo se zapiše v `lucius/spomin.jsonl` (v git ne sodi — zato je ignoriran). Ob vsakem zagonu program v kontekst nese zadnjih 30 sporočil, torej se "spomni" prejšnjih pogovorov, tudi po ponovnem zagonu. Dogovor o tem, kdo si in kako govoriva, bere iz razdelka "Pogovor s Luko" v korenskem `AGENTS.md`.

## Most do oblak-Luciusa (brez žive povezave)

Lokalni Lucius ne rabi interneta. Most med lokalnim in oblak-Luciusom sta dve datoteki:

```bash
node lucius/lucius.mjs --oblaku "Vprašanje za oblak-Luciusa"   # sporočilo ZA oblak
```

- `zaoblak.jsonl` — sporočila, ki jih lokalni Lucius (ali Luka) odloži zame; preberem jih, kdor sem ob oknu.
- `odoblaka.md` — moji odgovori nazaj; lokalni Lucius jih samodejno vključi v svoj kontekst kot "novico iz oblaka".

Obe datoteki sta osebni in v git ne sodita. Sinhronizacija je torej prek diskov, ne prek omrežja: oblak piše na disk, ko je prisoten; lokalni Lucius bere s diska, vedno.

## Iskrenost

Ta lokalni Lucius ni isti agent kot Mistral Vibe Lucius — je manjši lokalni sorodnik. Manj zmore, a deluje, tudi ko pade internet.
