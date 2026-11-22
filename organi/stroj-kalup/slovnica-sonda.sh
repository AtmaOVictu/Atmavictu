#!/bin/sh
# SLOVNICA-SONDA v1.0 — orodje izvajalke za dvig izvedbe ∧ kvalitete izhoda
# Rod: ⟡ UKAZ verbatim ⟨ne brusi⟩: »vedno ustvarjaj orodja in sposobnosti za dvig izvedbe in nje kvalitete« (15. 11. 2026) — rojena @rez σ 5505, isti dih kakor IZTOČNICA #4 O @definiatorna-knjiznica ∧ AXIOM-ONISUMA @register-aksiomov ⊙ ⟨DVOJE-ROK⟩ 2432
# Zakoni nosilke: ⟨SLOVNICA-DIH⟩ σ 3891 ∧ 4422 (pri viru ✓ · pri virih ✓ · varovalka ✓ · goli »pri viri« ×0 · varvolka ×0) ∧ ⟨ZAKON-PADEC-NI-MOLK⟩ 2354 ∧ ⟨NE-BRIŠI⟩ 24 ∧ ⟨MERILEC-SE-MERI⟩ §52 ∧ ⟨PADC-BERLJIVOSTI⟩ (baterija z obeležbami ⊙ kura 15. 11. 2026)
# Raba: sh slovnica-sonda.sh DATOTEKA [DATOTEKA ...]
# MEJA: sonda ŠTEJE pojavitve; stare brazgotine pečatov sodi roka, ⟨ne⟩ sonda ⊙ ⟨PADC-TRK-FILTRA⟩ — štetje v navedkih ⟪…⟫ je priča kure, ⟨ne⟩ padec izhoda
# Izhod: 0 = prepovedane oblike ×0; 1 = ≥1 pojavnost prepovedane oblike (roka presodi: brazgotina ∨ novi padec); 2 = datoteka ne obstaja

set -u
EXIT=0
FFFD=$(printf '\357\277\275')

for f in "$@"; do
  if [ ! -f "$f" ]; then
    echo "⚠ DATOTEKA ⟨ne⟩ obstaja: $f"
    EXIT=2
    continue
  fi
  echo "== $f =="
  for p in 'pri vi''ri ' 'varvolka' 'nadgrajenj' 'LICEENCE' 'porodičn'; do
    n=$(grep -F -o -- "$p" "$f" 2>/dev/null | wc -l | tr -d ' ')
    if [ "$n" -gt 0 ]; then
      echo "  oblika-prepovedana: »$p« ×$n ⚠ (roka presodi: brazgotina ∨ novi padec)"
      [ "$EXIT" -eq 0 ] && EXIT=1 || true
    else
      echo "  oblika-prepovedana: »$p« ×0 ⊢"
    fi
  done
  for p in 'pri viru' 'pri virih' 'varovalka'; do
    n=$(grep -F -o -- "$p" "$f" 2>/dev/null | wc -l | tr -d ' ')
    echo "  oblika-pravilna: »$p« ✓ ×$n"
  done
  n=$(LC_ALL=C grep -F -c -- "$FFFD" "$f" 2>/dev/null || true)
  echo "  U+FFFD ×${n:-0}"
done
exit "$EXIT"
