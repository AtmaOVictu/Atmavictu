#!/bin/bash
# W6 ⟨KOV-KITA⟩ — izpiše tri ključe kita (naslov tvorca, commit, PR body) iz parametra N in opisa
# uporaba: ./kov-kit.sh <rezN> <veja> <opis-kratek>   naslov nosi »rez σ N« ⇒ prica step 1 vidi zahtevo
N="$1"; BR="$2"; OP="$3"
[ -z "$N" ] || [ -z "$BR" ] || [ -z "$OP" ] && { echo 'uporaba: kov-kit.sh <rezN> <veja> <opis>'; exit 1; }
echo "NASLOV: rez σ $N — $OP"
echo "KOMIT: [ PREVOZ ] rez σ $N — $OP ( ⟡ UKAZ verbatim »stori« )"
echo "TILO: veja $BR ⊙ kalup ⟨PR⟩→⟨CI⟩→⟨merge⟩ ⊙ APPEND-ONLY ⊙ read-back po ⟨merge⟩ sha"
