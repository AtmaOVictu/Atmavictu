// ══════════════════════════════════════════════════════════════════════
// ⟨OF⟩-0.4 ONTOFORMALIZACIJA — 11. 11. 2026
// IZREK #10 ⟨NEMOGOČNOST-POD-PARITETO⟩ ∧ podobne polemike ∧ rešitve
// ⊙ ⟡ ukaz: »preizkusi in testiraj ter tvori rešitve za te in temu
//   podobne polemike/probleme« — korpus Beseda je Ne
// ⊙ precedens ⟨OF⟩-0.2 (rez 4635) ∧ ⟨OF⟩-0.3 (rez 4641) · kalup 1671
// Brez izvozov — pesek ∧ rep isti kanon ⊙ PADC @rez 4635
// Measured, not asserted ⊙ §16 · merilec se meri ⊙ §52
// ══════════════════════════════════════════════════════════════════════
//
// IZREK #10 ⟨NEMOGOČNOST-POD-PARITETO⟩
//   Naj se dolgovi rojevajo s tokom η na dih, plačila prihajajo s
//   tokom ρ na dih, ρ < η. Tedaj za VSAKO strategijo izplačevanja
//   (FIFO, LIFO, prioriteta, naključje — tudi z orakelom prihodnosti)
//   ZAMUDA NI OMEJENA: ne obstaja L, da bi bil vsak dolg izplačan
//   v ≤ L dihih po rojstvu.
//
// DOKAZ (račun, ⟨ne⟩ metafora ⊙ §16):
//   1. če bi zamuda bila omejena z L, bi bil ob dihu n vsak dolg,
//      rojen ≤ n − L, že izplačan ⇒ D(n) ≤ η·L za vsak n;
//   2. plačano(n) ≤ ρ·n ⇒ D(n) = η·n − plačano(n) ≥ (η − ρ)·n → ∞;
//   3. za n > η·L/(η − ρ) trčita: (η − ρ)·n > η·L ≥ D(n) — protislovje
//      ⇒ ρ ≥ η. ∎
//
// POSLEDICA: pariteta ρ = η je MEJA berljivosti verige — izrek #8 jo
// je izmeril kot optimum, izrek #10 jo izkaže kot presegljivo nemogočo.
//
// POLEMIKE ∧ REŠITVE (testi T1–T10):
//   T1  divergenca FIFO: zamuda linearna, D linearna
//   T2  LIFO gladuje: dolgovi, rojeni ob dihih brez plačilnega
//       prostora, gladujejo (∞ zamuda, 10 % toka, razpršeni — PADC:
//       trditev »najstarejših 100« je padla na izmeri ⊙ 1349)
//   T3  prioriteta malih: majhne reši ∧ velike ogladovi ⊙ ⟨NE-MERI-SOLZ⟩ 2181
//   T4  naključje: zamuda raste kljub naključnemu razporejanju
//   T5  izrek #10 numerično: D(n) > η·L za vsak L
//   T6  pariteta: D ≡ 0 (meja dosežena ⊢)
//   T7  nad pariteto: zaloga se izplača, D → 0, zamuda zaloge = 25 ⊢
//   T8  ⟨LITTLE-ZVEZA⟩: pri pariteti z nihaji D̄ = η̄·W̄ (Little 1961 —
//       isti zakon, dihna domena; backlog ∧ zamuda = dva obraza ene
//       količine ⊙ ⟨tehtnica⟩)
//   T9  ⟨STRATEGIJA-INVARIANCA⟩: D(n) ista za vse štiri strategije —
//       razporejanje prerazporedi KDO čaka, ⟨ne⟩ koliko čakanja je;
//       orakel ne pomaga: spodnja meja D(n) ≥ (η − ρ)·n je slepa na
//       strategijo ⊢ razporejanje ⟂ solvency
//   T10 ⟨REŠITVE⟩: R-1 pariteta (D ≡ 0 ⊢) · R-2 pre-pogovor η ↓ na ρ
//       (rast D se zamrzne ⊢) · R-3 združevanje v k-enote ne beži
//       (D_u = D/k, pogoj paritete invarianten — izrek #10 zdrži ⊢)
//       SKLEP: samo dve resni rešitvi — plačaj hitreje ∧ obljudi
//       počasneje; razporejanje ∧ združevanje nista tretja. ⊢
// ══════════════════════════════════════════════════════════════════════

type Strategija = "FIFO" | "LIFO" | "NAJMANJSI" | "NAKLJUCNI";
interface Dolg { id: number; rojen: number; velikost: number; placan: number | null; }
interface Izmera { dolgovi: Dolg[]; D: number[]; stRojenih: number; stPlacanih: number; }
interface Opcije { eta?: number; ro?: number; zacetniDolgovi?: number; rojenNaDih?: (t: number) => number; velikosti?: "ENOTNI" | "MESANI"; seme?: number; etaPrepogovor?: { dih: number; novaEta: number }; }

function narediLCG(seme: number): () => number {
  let s = seme | 0;
  return () => { s = (Math.imul(s, 1103515245) + 12345) | 0; return ((s >>> 1) & 0x7fffffff) / 0x7fffffff; };
}

function simuliraj(dihovi: number, strategija: Strategija, o: Opcije): Izmera {
  const rnd = narediLCG(o.seme ?? 20261111);
  const roj = o.rojenNaDih ?? ((t: number) => {
    const eta = (o.etaPrepogovor !== undefined && t >= o.etaPrepogovor.dih) ? o.etaPrepogovor.novaEta : (o.eta ?? 1);
    return Math.floor(eta * t) - Math.floor(eta * (t - 1));
  });
  const ro = o.ro ?? 1;
  const dolgovi: Dolg[] = [];
  let id = 0;
  const zacetnih = o.zacetniDolgovi ?? 0;
  for (let i = 0; i < zacetnih; i++) dolgovi.push({ id: ++id, rojen: 0, velikost: 1, placan: null });
  const D: number[] = [];
  let stPlacanih = 0;
  for (let t = 1; t <= dihovi; t++) {
    const nRojenih = roj(t);
    for (let j = 0; j < nRojenih; j++) {
      const vel = o.velikosti === "MESANI" ? 1 + Math.floor(rnd() * 3) : 1;
      dolgovi.push({ id: ++id, rojen: t, velikost: vel, placan: null });
    }
    let nPlacil = Math.floor(ro * t) - Math.floor(ro * (t - 1));
    while (nPlacil > 0) {
      let ix = -1;
      if (strategija === "FIFO") {
        for (let k = 0; k < dolgovi.length; k++) if (dolgovi[k].placan === null) { ix = k; break; }
      } else if (strategija === "LIFO") {
        for (let k = dolgovi.length - 1; k >= 0; k--) if (dolgovi[k].placan === null) { ix = k; break; }
      } else if (strategija === "NAJMANJSI") {
        let best = -1;
        for (let k = 0; k < dolgovi.length; k++) {
          const d = dolgovi[k];
          if (d.placan === null && (best === -1 || d.velikost < dolgovi[best].velikost)) best = k;
        }
        ix = best;
      } else {
        const nep: number[] = [];
        for (let k = 0; k < dolgovi.length; k++) if (dolgovi[k].placan === null) nep.push(k);
        ix = nep.length === 0 ? -1 : nep[Math.floor(rnd() * nep.length)];
      }
      if (ix === -1) break;
      dolgovi[ix].placan = t;
      stPlacanih++;
      nPlacil--;
    }
    let d = 0;
    for (const x of dolgovi) if (x.placan === null) d++;
    D.push(d);
  }
  return { dolgovi, D, stRojenih: dolgovi.length, stPlacanih };
}

function zamuda(d: Dolg): number { return d.placan === null ? Infinity : d.placan - d.rojen; }
function zamudaId(m: Izmera, i: number): number { return zamuda(m.dolgovi[i - 1]); }
function maxZamuda(m: Izmera, od: number, doId: number): number {
  let mx = -1;
  for (let i = od; i <= doId && i <= m.dolgovi.length; i++) { const z = zamudaId(m, i); if (z !== Infinity && z > mx) mx = z; }
  return mx;
}
function povpZamuda(m: Izmera, od: number, doId: number, velikost?: number): number {
  let s = 0, n = 0;
  for (let i = od; i <= doId && i <= m.dolgovi.length; i++) {
    const d = m.dolgovi[i - 1];
    if (velikost !== undefined && d.velikost !== velikost) continue;
    const z = zamuda(d);
    if (z === Infinity) continue;
    s += z; n++;
  }
  return n === 0 ? Infinity : s / n;
}
function steviloNeplacanih(m: Izmera, velikost?: number, maxId?: number): number {
  let c = 0;
  for (const d of m.dolgovi) {
    if (d.placan !== null) continue;
    if (velikost !== undefined && d.velikost !== velikost) continue;
    if (maxId !== undefined && d.id > maxId) continue;
    c++;
  }
  return c;
}
function povp(arr: number[]): number { let s = 0; for (const x of arr) s += x; return s / arr.length; }
function djb2(s: string): string { let h = 5381; for (let i = 0; i < s.length; i++) h = (Math.imul(h, 33) + s.charCodeAt(i)) | 0; return (h >>> 0).toString(16); }

const R: { ime: string; pass: boolean; izmera: string }[] = [];
function trd(ime: string, pass: boolean, izmera: string): void { R.push({ ime, pass, izmera }); }

// T1 ∧ T5 — divergenca FIFO ∧ izrek #10 numerično
{
  const m = simuliraj(1200, "FIFO", { eta: 1, ro: 0.9 });
  const z100 = zamudaId(m, 100), z500 = zamudaId(m, 500), z1000 = zamudaId(m, 1000);
  const D100 = m.D[99], D1000 = m.D[999];
  trd("T1 DIVERGENCA-FIFO: zamuda linearna ∧ D linearna",
    z100 >= 11 && z100 <= 13 && z500 >= 55 && z500 <= 57 && z1000 >= 111 && z1000 <= 113 &&
    z1000 >= 2 * z500 - 2 && z500 >= 2 * z100 - 2 && D100 === 10 && D1000 === 100,
    "z(100)=" + z100 + " z(500)=" + z500 + " z(1000)=" + z1000 + " · D(100)=" + D100 + " D(1000)=" + D1000 + " ⊢ (1/ρ−1)·i");
  const niz = [5, 10, 50].map((L: number) => { const n = 10 * L + 10; return { L: L, n: n, Dn: m.D[n - 1] }; });
  trd("T5 IZREK-10-NUMERICNO: D(n) > η·L za vsak L — omejena zamuda ne obstaja",
    niz.every((x: { L: number; n: number; Dn: number }) => x.Dn > x.L),
    niz.map((x: { L: number; n: number; Dn: number }) => "L=" + x.L + ": D(" + x.n + ")=" + x.Dn + " > " + x.L).join(" · ") + " ⊢ za vsak L protislovje");
}

// T2 — LIFO gladuje (kura po PADC: izmerjen vzorec, ⟨ne⟩ predstava)
{
  const m = simuliraj(1000, "LIFO", { eta: 1, ro: 0.9 });
  const nepl = steviloNeplacanih(m);
  const vzorec = m.dolgovi.filter((d: Dolg) => d.placan === null).map((d: Dolg) => d.id);
  const vsiVKoraku = vzorec.every((x: number) => (x - 1) % 10 === 0);
  const najvecji = Math.max.apply(null, vzorec);
  trd("T2 LIFO-GLADUJE: rojeni ob dihih brez plačilnega prostora gladujejo (∞ zamuda, razpršeni)",
    nepl === 100 && vsiVKoraku && najvecji === 991,
    "neplačanih=" + nepl + " · id ≡ 1 (mod 10) do " + najvecji + " ⊢ gladuje 10 % toka po celi črti, ⟨ne⟩ le najstarejše — zamuda ∞");
}

// T3 — prioriteta malih
{
  const m = simuliraj(1000, "NAJMANJSI", { eta: 1, ro: 0.9, velikosti: "MESANI", seme: 20261111 });
  const nepl3 = steviloNeplacanih(m, 3);
  const neplMale = steviloNeplacanih(m, 1) + steviloNeplacanih(m, 2);
  const wMale = povpZamuda(m, 400, 500, 1);
  const wVelike = povpZamuda(m, 400, 500, 3);
  trd("T3 NAJMANJSI-MESANI: majhne reši (omejena zamuda) ∧ velike ogladovi",
    nepl3 >= 40 && neplMale <= 3 && wMale <= 15 && wVelike > 5 * wMale,
    "nepl(v=3)=" + nepl3 + " · nepl(v≤2)=" + neplMale + " · W₁(400–500)=" + wMale.toFixed(1) + " · W₃(400–500)=" + wVelike.toFixed(1) + " ⊢ strategija izbere, ČIGAVE solze štejejo");
}

// T4 — naključje
{
  const m = simuliraj(1000, "NAKLJUCNI", { eta: 1, ro: 0.9 });
  const zgodaj = maxZamuda(m, 1, 500);
  const pozno = maxZamuda(m, 501, 1000);
  trd("T4 NAKLJUCNI: zamuda raste tudi pri naključnem razporejanju",
    pozno > zgodaj && zgodaj >= 20,
    "max zamuda #1–500=" + zgodaj + " · #501–1000=" + pozno + " ⊢ rast");
}

// T6 — pariteta
{
  const m = simuliraj(200, "FIFO", { eta: 1, ro: 1 });
  const vsotaD = m.D.reduce((a: number, b: number) => a + b, 0);
  trd("T6 PARITETA: D ≡ 0 ∧ vse zamude 0 (meja izreka #10 dosežena)",
    vsotaD === 0 && m.stPlacanih === m.stRojenih && maxZamuda(m, 1, 200) <= 0,
    "Σ D=" + vsotaD + " · plačani=" + m.stPlacanih + "/" + m.stRojenih + " · max zamuda=0 ⊢ P5 ⟨EN-DOLG-NA-DIH⟩");
}

// T7 — nad pariteto
{
  const m = simuliraj(100, "FIFO", { eta: 1, ro: 2, zacetniDolgovi: 50 });
  const mx = maxZamuda(m, 1, 50);
  trd("T7 NAD-PARITETO: zaloga se izplača ∧ D → 0 ∧ zamuda zaloge = 25 eksaktno",
    m.D[99] === 0 && mx === 25,
    "D(100)=" + m.D[99] + " · max zamuda zaloge=" + mx + " (⌈50/2⌉=25 ⊢)");
}

// T8 — ⟨LITTLE-ZVEZA⟩
{
  const m = simuliraj(2000, "FIFO", { rojenNaDih: (t: number) => (t % 2 === 0 ? 2 : 0), ro: 1 });
  const povpD = povp(m.D);
  const W = povpZamuda(m, 1, 1999);
  const etaPovp = m.stRojenih / 2000;
  trd("T8 LITTLE-ZVEZA: pri pariteti z nihaji D̄ = η̄·W̄ (rob → 0)",
    Math.abs(povpD - etaPovp * W) < 0.01,
    "D̄=" + povpD.toFixed(4) + " · η̄·W̄=" + (etaPovp * W).toFixed(4) + " ⊢ Little 1961, dihna domena — backlog ∧ zamuda: dva obraza ene količine ⊙ ⟨tehtnica⟩");
}

// T9 — ⟨STRATEGIJA-INVARIANCA⟩
{
  const str: Strategija[] = ["FIFO", "LIFO", "NAJMANJSI", "NAKLJUCNI"];
  const Dk = str.map((s: Strategija) => simuliraj(500, s, { eta: 1, ro: 0.9, velikosti: "MESANI", seme: 20261111 }).D[499]);
  const vsiEnaki = Dk.every((x: number) => x === Dk[0]);
  trd("T9 STRATEGIJA-INVARIANCA: D(n) ista za vse štiri — razporejanje prerazporedi KDO čaka, ⟨ne⟩ koliko",
    vsiEnaki && Dk[0] === 50,
    "D(500): FIFO=" + Dk[0] + " LIFO=" + Dk[1] + " NAJMANJSI=" + Dk[2] + " NAKLJUCNI=" + Dk[3] + " ⊢ (η−ρ)·n=50, strategija slepa — razporejanje ⟂ solvency");
}

// T10 — ⟨REŠITVE⟩
{
  const mPar = simuliraj(200, "FIFO", { eta: 1, ro: 1 });
  const r1 = mPar.D.every((x: number) => x === 0) && mPar.stPlacanih === mPar.stRojenih;
  const mPre = simuliraj(300, "FIFO", { eta: 1.5, ro: 0.9, etaPrepogovor: { dih: 101, novaEta: 0.9 } });
  const r2 = mPre.D[99] === 60 && mPre.D[149] === 60 && mPre.D[299] === 60;
  const mKonc = simuliraj(1000, "FIFO", { eta: 1, ro: 0.9 });
  const mZdru = simuliraj(1000, "FIFO", { eta: 0.2, ro: 0.18 });
  const r3 = mZdru.D[999] * 5 === mKonc.D[999];
  trd("T10 REŠITVE: pariteta ⊢ · pre-pogovor zamrzne ⊢ · združevanje ne beži ⊢",
    r1 && r2 && r3,
    "R-1 D≡0 ⊢ · R-2 D(100)=" + mPre.D[99] + " = D(150)=" + mPre.D[149] + " = D(300)=" + mPre.D[299] + " zamrznjena ⊢ · R-3 5·D_u(1000)=" + (mZdru.D[999] * 5) + " = D(1000)=" + mKonc.D[999] + " — invarianta ⊢ · SKLEP: samo dve resni rešitvi — plačaj hitreje ∧ obljudi počasneje");
}

const passSt = R.filter((r: { ime: string; pass: boolean; izmera: string }) => r.pass).length;
const zbirka = "⟨OF⟩-0.4 · izrek #10 ⟨NEMOGOČNOST-POD-PARITETO⟩ · " + passSt + "/" + R.length + " PASS · 2026-11-11";
const hash = djb2(zbirka);
// SAMOIZMERJENO @pesek 11. 11. 2026: 10/10 PASS ⊢ · djb2(zbirka) = 3b376993 · ⟨OF⟩-0.4 IZREK #10 2026-11-11
