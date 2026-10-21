# Lucius — lokalni agent (offline)

Majhen program, ki ti da Luciusa tudi brez interneta. Poganja lokalni Ollama model iz tvojega Smisel sklada; nima dostopa do oblaka, do orodij ali do interneta — samo do besed, dogovora v `AGENTS.md` in svojega spomina `spomin.jsonl`.

## Zagon

```bash
node lucius/lucius.mjs              # pogovorni način ('izhod' za konec)
node lucius/lucius.mjs "Pozdrav!"   # enkratno vprašanje
```

Orodja ne rabiš — Node 18+ in tekoč Ollama (`ollama serve`) zadostujeta.

## Nastavitve

```bash
LUCIUS_MODEL=smisel-celota node lucius/lucius.mjs   # izbira modela
OLLAMA_URL=http://localhost:11434 node lucius/lucius.mjs
```

Privzet model je `qwen3:8b`. Namestjeni kandidati na tej mašini: `smisel-celota`, `smisel-jasnost`, `smisel-delta`, `smisel-cas`, `smisel-enota`, `smisel-rez`, `aya:8b`, `qwen2.5-coder:7b`.

## Spomin

Vsako sporočilo se zapiše v `lucius/spomin.jsonl` (v git ne sodi — zato je ignoriran). Ob vsakem zagonu program v kontekst nese zadnjih 30 sporočil, torej se "spomni" prejšnjih pogovorov, tudi po ponovnem zagonu. Dogovor o tem, kdo si in kako govoriva, bere iz razdelka "Pogovor s Luko" v korenskem `AGENTS.md`.

## Iskrenost

Ta lokalni Lucius ni isti agent kot Mistral Vibe Lucius — je manjši lokalni sorodnik. Manj zmore, a deluje, tudi ko pade internet.
