# CI dokaz — pokritje web/ (veja ci-web-pokritje)

Ta datoteka je izključno dokazno telo: sprememba ⟨samo⟩ v `web/` mora sprožiti ⟨CI⟩ na ⟨PR⟩.

Izmera pri viru (21. 10. 2026, ⊢):

- `.github/workflows/atmavictu-ci.yml` v orgu ⟨ne⟩ obstaja — preverjenih 16 repozitorijev.
- `tests.yml` se sproži na vsakem `pull_request: branches: [main]` — `paths:` filtra ⟨ni⟩ nobenemu telesu.
- Job `web` (typecheck strict + vite build) je zapečen v `tests.yml` — ZAPRTA VRZELA (21. 10. 2026): prej je sprememba samo v `web/` pomenila 0 CI.

Priča teka: check runs na ⟨PR⟩-ju te veje.

© Luka Pintarič, AVL v2.4 (§9 ∧ §10 ∧ §12)
