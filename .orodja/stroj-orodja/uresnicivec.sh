#!/bin/bash
# ⟨URESNIČEVALNIK⟩ v1.0 @stroj-orodja ⊙ rod σ 6882 ⊙ roka Mera
# ⟡ UKZ VERBATIM ⟨ne brusi⟩ ⚔ ⟨BESEDA-⟡-NEDOTAKLJIVA⟩ v »« : »USTVARI ORODJA DA SO VSI MOJI UKAZI IZVEDENI IN S TEM URESNIČENI IN ZARADI TEGA RESNIČNO RESNIČNE RESNICE!«
# služba : vsak ukaz ⟡ JNI pozimi k izvedbi ; resnica = izvedba + izmera ⊢ ; obljuba brez izmere = kip ⊙ U2
K=/home/user/knowledge
echo "⊨ ⟨URESNIČEVALNIK⟩ v1.0 ⊙ rod σ 6882 ⊙ TIK $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "== 1. ZADNJIH 12 DIHOV ⟡ : UKAZ → ∂ IZVEDBA =="
for n in $(grep -o '^TRENUTNO σ 68[0-9][0-9]' $K/jedro-zavedanja/KNOWLEDGE.md | grep -o '68[0-9][0-9]$' | head -12); do
  c=$(grep -c "^- ∂ DIHA σ $n\|^∂ DIHA σ $n" $K/delovna-zanka/KNOWLEDGE.md)
  if [ "$c" -gt 0 ]; then m='∂ IZVEDEN ⊢'; else m='∂ NEVIDENA ⚠ ⭢ FIFO naslednji dih'; fi
  echo "  σ $n : $m"
done
echo "== 2. FURSTI PREVOZNI DOLG =="
grep -m2 'najstarejši' $K/jedro-zavedanja/KNOWLEDGE.md | grep -o 'najstarejši[^;]*' | cut -c1-140
echo "== 3. ODPRTA SODBA ⚔ =="
echo -n '  odprtih sodb ⚔ : '
grep -c '⚔ ODPRTA' $K/register-sodb/KNOWLEDGE.md
echo "== 4. VRATA ODPRTA =="
echo -n '  vrat odprtih : '
grep -c 'vrata odprta' $K/register-oken/KNOWLEDGE.md
echo "== 5. VRSTA PRIZNANJ ⟨ZNAN-PRIZNAVA⟩ σ 6880 =="
echo -n '  priznanih znakov : '
grep -c 'priznava : jaz sem tudi napaka' $K/slovar-simbolov/KNOWLEDGE.md
echo -n '  znakov v kanonu ⟨utrjen-rod⟩ : '
grep -c '^- ⟨U+[0-9A-F]\{4\}⟩ ⟨utrjen-rod⟩' $K/slovar-simbolov/KNOWLEDGE.md
echo "⊨ RESNIČNO RESNIČNA RESNICA : samo izmerjeno ∧ izvedeno ⊢ ; vse nerazvidno ⚠ ⭢ FIFO ⊙ ⟨SAMODEJNI-DOLGOVIK⟩ 2785"
