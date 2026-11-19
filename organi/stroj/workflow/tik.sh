#!/bin/bash
# W4 ⟨TIK-IZMERJEN-PREJ-ZAPISAN⟩ — TIK kalup izmerjen ⟨date -u⟩, CET = UTC+1 vedno @σ 3961
# uporaba: ./tik.sh            izpiše: TIK 2026-11-19T10:17:31Z UTC ⇌ 11:17:31 CET
U=$(date -u +%Y-%m-%dT%H:%M:%SZ); C=$(date -u -d '+1 hour' +%H:%M:%S)
echo "TIK $U UTC ⇌ $C CET"
