#!/bin/bash
# ⟨grep⟩-UNIKATEN — iskanje po okviru, ⟨ne⟩ po goli števki (rez 3532, organ licenca-vbl)
# raba: grep-unikaten.sh rez 3532         → okvir ⟨(rez|dih|σ|PEČAT) 3532⟩ ∧ gola števka ⚠
#       grep-unikaten.sh kovanec ∆dejanje  → plasti ⟨⟨∆dejanje⟩⟩ / ⟨∆dejanje⟩ / golo ⚠
# Zakoni: gola števka nikoli unikatna (3531 ⊂ 735316 B; 3121 = U+13121) ⊙ rez 3532
#         ⟨grep⟩ po eksplicitni listi datotek, ⟨ne⟩ po globih ⊙ kanon DELAVEC §5
# ⚠ ⟨PADC-ERE-PESKA⟩: ta ⟨grep⟩ nosi BRE sintakso tudi pod -E — okvirji kot \( \) \| (izmerjeno ta dih)
set -eu
MODE="${1:?raba: rez N | kovanec IME}"
ARG="${2:?raba: rez N | kovanec IME}"
LISTA=$(find /home/user/knowledge -maxdepth 2 -name KNOWLEDGE.md | sort)

if [ "$MODE" = "rez" ]; then
  N="$ARG"
  P='⟨\(rez\|dih\|σ\|PEČAT\)[ )]*'"$N"'[⟩)]?'
  echo "== OKVIR ⟨(rez|dih|σ|PEČAT) $N⟩ — unikatna plast =="
  grep -nE "$P" $LISTA || echo "×0"
  echo "== GOLA ŠTEVKA $N ⚠ (lažni zadetki možni: bajti · md5 · codepoint) =="
  printf 'zadetki: %s\n' "$(grep -ho "$N" $LISTA | wc -l)"
elif [ "$MODE" = "kovanec" ]; then
  K="$ARG"
  echo "== ⟨⟨$K⟩⟩ dvojni okvir (nov kovanec = samo tu) =="
  grep -nF "⟨⟨$K⟩⟩" $LISTA || echo "×0"
  echo "== ⟨$K⟩ enojni okvir (žitna plast korpusa) =="
  grep -nF "⟨$K⟩" $LISTA || echo "×0"
  echo "== GOLO $K ⚠ (operator v prozi — ⟨ne⟩ kovanec) =="
  printf 'zadetki: %s\n' "$(grep -hoF "$K" $LISTA | wc -l)"
else
  echo "raba: rez N | kovanec IME" >&2; exit 1
fi
