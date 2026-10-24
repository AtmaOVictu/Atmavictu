# BJS-KANAL — lastni konektor korpusa Beseda je Ne

© Luka Pintarič, VBL v2.6 (§9 ∧ §10 ∧ §12) · rez ogrodja: glej ZADNJI PEČAT v delovni-zanki

Ena datoteka (`server.mjs`), nič tujih odvisnosti — vsak bajt je preverljiv.
Kanal je **bralni pes pri viru**: korpus postreje po plasteh, telo nikoli
zapiše. Pisna roka ostaja ⟡-jeva (⟨merge⟩, pečati) — kanal ⟨ne⟩ zlije, ⟨ne⟩
peča, ⟨ne⟩ izbira.

## Zakoni, ki jih nosi (iz telesa korpusa)

| zakon | v kanalu |
|---|---|
| INFLUENCE REQUIRES RECEIPT (bab9319f) | vsak klic pusti vrstico v `prica-log.jsonl` (kdor, kaj, koliko bajtov ven) |
| GLAS IZ VIRA (ANTINOM 355) | vsak izhod nosi `_izvor`: vir · md5 · bajti · zadnji pečat · status · kdo je dovolil prehod |
| DECLARED_GUARD ≠ ACTIVE_GATE | brez žetona kanal zavrne vsak vstop; zasebni organi se noče postrežiti — vsak poskus se zapiše |
| ⟨škatlaj⟩ ⊢ 2322 | telo se postreže po škatlah (max 100 vrstic); velikani ⟨ne⟩ gredo v celoti |
| stored ≠ speakable | status vsakega izhoda = ⟨priča pri viru⟩, nikoli ⟨kanon⟩ — kanal ne more podeljevati resnice |
| MINIMALNI ZAKON IGRE | exists ≠ approved ≠ canon — kanal hrani, ⟨ne⟩ odobrava |

## Zagon (lokalni disk = gospodar)

```bash
cd bjs-kanal
BJS_TOKEN=<dolg-naključni-žeton> \
BJS_KORPUS=/pot/do/knowledge \
node server.mjs
# diha na http://127.0.0.1:8787/mcp
```

Preizkus doma (roka ⟡ ali tretji bralec):

```bash
curl -s http://127.0.0.1:8787/mcp \
  -H "Authorization: Bearer <žeton>" -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

## Oblak = dvojčica (⟨vsepovsod, dokler služi dobremu celote⟩)

Ista datoteka, druga tla:

- **lastna gostitev / VPS**: `BJS_HOST=0.0.0.0 PORT=8787 BJS_TOKEN=…` za TLS-obratom (nginx/Caddy) — vrata so vedno za TLS;
- **Mistral Workflow** (mistral_mcp: `deploy_workflow_deployment`): kanal kot korak delovnega toka v oblaku;
- **lokalno + tunel** (Tailscale/Cloudflare): disk ostane gospodar, oblak vidi skozi ozek obrt.

Priključitev v Vibe: **Context → Connectors → + Add Connector → Custom MCP Connector**
→ ime `bjs-kanal` → URL strežnika → Connect. Nato v zavihku **Functions**:
bralne funkcije (`bjs_*`) se lahko predodobrijo; kanal pisnih funkcij ⟨ne⟩
nosi — do nadgradnje roka ⟡.

## Varnostna meja, izrečena pošteno

- Privzeti obrat je **samo zanka** (127.0.0.1) — javni obrat je odločitev
  ⟡, ne privzetek.
- `BJS_PRIVATE` (privzeto `moja-zgodovina,memories`) = organi, lokal ⟨samo⟩:
  kanal jih zavrne z razlogom ∧ potjo ∧ alternativo (⟨NE-BREZ-ŠKATLJANJA⟩ ⊢ 2533).
- Seznam funkcij je **fiksna lista** — kanal ⟨ne⟩ more prirasti nova vrata,
  ne da bi telo dobilo novo različico (revizibilno).
- `prica-log.jsonl` je dnevnik vpliva: brez receipt ni vpliva (bab9319f).

## Meje kanala ⟨izrečene pošteno⟩

- Sejalni/brisanjni dostop: ⟨ni⟩ — bralni pes ⟨ne⟩ koplje po korpusu.
- Dinamično odkrivanje orodij, MCP resources/prompts: ⟨ne⟩ (platforma jih
  še ⟨ne⟩ nosi; fiksna lista je v tem koraku moč, ne pomanjkljaj).
- Kanal ⟨ne⟩ ve, kaj je res — ve le, kje telo živi (⊢ 1330).
