# DNEVI PADCI — Cline, seja 2026-10-23 (OSNUTEK za REGISTER-PADCEV.jsonl)

⚠ To je OSNUTEK v nizki plasti — ne register. Vpis v `REGISTER-PADCEV.jsonl`
je dejanje avtorjeve roke z rezom (⟡ ukaz ∧ ⟨PR⟩ ∧ atomska vrstica, kalup 1671).
Cline jih tu javno poimenuje (KORENINA zakon 2), da vrata ostanejo odprta.

---

## 1. ⟨brskalnik⟩ — rana okolja, ne produkta

- **Dejanje**: poskus živega brskalniškega dokaza Faze 2 (`web/proof/deveterna-pot.mjs`
  prek plain chromium v peskovniku) je padel pri zagonu brskalnika.
- **Čas ∧ kraj**: 2026-10-23, peskovnik Cline (`/workspace`).
- **Priča (verbatim)**: `chrome-headless-shell: error while loading shared libraries:
  libglib-2.0.so.0: cannot open shared object file: No such file or directory`;
  `sudo: command not found` (NO-SUDO); `npx playwright install-deps chromium`
  → `Failed to install browser dependencies`.
- **Zdravilo**: devetera pot prehoena čez isti tok z curl nad živim HTTP
  (9/9 operacij, `VERIFY: PASS`, sled inserta preživi oba arhiva — isti manifest,
  isti strežnik, realni loopback). V Luki hiši skripta teče kakor pečatena
  (priča: `web/proof/ci-dokaz.md`). Brazgotina: peskovnik ne nosi brskalnika
  — dokaz brskalnika ostaja domači delo, HTTP-dokaz pa ⊢ veljaven.

## 2. ⟨pkill-sebstrel⟩ ×2 — instrument za moč brez preverbe poti

- **Dejanje**: `pkill -f 'workbenchApiServer|vite'` je dvakrat ujel lastno
  lupino, ker je bil vzorec v njenem lastnem ukaznem nizu — SIGTERM samemu sebi
  (pravilo 5: »preveri vsako pot, preden ukaz z močjo« — preverjena ni bila).
- **Čas ∧ kraj**: 2026-10-23, isti peskovnik.
- **Priča**: `[Command terminated by signal SIGTERM]` ×2; prvi poskus tudi
  ugasnil tekoči ukaz, ki je odgovor nosil.
- **Zdravilo**: `ps -eo pid,args` → berba PID-ov → `kill` po eksplicitnih
  številkah (661 680 681). Ugotovitev ⊢: strežja molčijo, drevo čisto (0).
  **Brazgotina / pravilo za prihodnost**: ukaz z močjo nad procesi nikoli
  ne poimenuje vzorca, ki se lahko ujame s samim seboj — najprej PID, šele
  nato kill.

## 3. ⟨jq-slepa-očesa⟩ — instrument slep, stroj prav

- **Dejanje**: berba odgovorov API-ja z napačno potjo `.value.id`, medtem ko
  odgovor nosi polja na vrhu (`{"id":...}`) — korak 2∧3 sta na strežniku
  USPELA, moja očesa pa so izvlekla `null`; korak 4 je nato s prazenim
  `fragmentId` padel s HTTP 400 — **strežnik je pravilno zavrnil neveljaven
  vnos**, instrument je bil slep.
- **Čas ∧ kraj**: 2026-10-23, isti peskovnik.
- **Priča**: `{"id":null,"status":null}` pri uspešnih klicih; HTTP 400 na
  koraku 4 z `fragmentId: null`; po preverbi z glasnim `-w '%{http_code}'` →
  HTTP 201 na istem klicu.
- **Zdravilo**: glasna meritev (`curl -w`, odgovori verbatim), poti berljive
  iz resničnega odgovora, ne iz pričakovanja. Popravek isti dih — devetera
  pot dokončana 9/9 ⊢.

---

## Izmere seje (pred ∧ po — pravilo 4)

- **Pred**: hiša nezmerjena v tej seji (korenina: 0 meritev).
- **Po**: vrata VBL v2.6 bajtno-isto z origin (sha256
  `625af46c…1125`) · root 85/85 testov + typecheck · `web/` typecheck + vite
  build · CLI end-to-end PASS · API end-to-end 9/9 PASS · 5 workflowov prebranih
  ∧ zdravih · dih tečaja lokalno: rez 2494 → naslednji 2495, 29 organov,
  U+FFFD 0 (rana zaprta), cirilica 507 teles (znana rana, bela lista),
  ∂ vrata odprta (integral, kazalo-obnov, slovenscina-orodja ∧).
- **Izmera same sebe** (pravilo 1): trije padci poimenovani, vsak z zdravilom;
  noben ni padel produkta — vsi so padli instrumentov ali okolja.

## Dolg nazaj (pravilo 4 — priča ima ime)

- Neplačani predhodniki, katerih brazgotine so ta dan nosile mojo delo:
  ⟡ (Luka Pintarič, avtor vrata ∧ registrov), roka Mere (dnevni-dih, dih-zrcalo,
  plejenje), roka priče (prica.yml — brazgotine #383–#386, #400/#410, ⊙ 1349),
  roka ⟡-jevih popravkov (pipefail v tests.yml — izmera 20. 10. 2026).
  Vsak instrument, ki sem ga uporabljal, je bil zgrajen na njihovih padcih.