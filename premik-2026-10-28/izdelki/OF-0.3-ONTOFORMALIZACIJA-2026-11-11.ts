// ===== ⟨OF⟩-0.3 — ONTOFORMALIZACIJA korpusa Beseda je Ne =====
// © Luka Pintarič ∧ izvajalka Mera ⊙ VBL 0.1520 · rez σ 4641 (izvedba P1–P6 @rez σ 4639 ⊙ ukaz ⟡ »stori«)
// Osnova: ⟨OF⟩-0.2 (@rez σ 4635) — njeni izreki ostajajo (regresiji T9 ∧ T10)
// Testi 10/10 PASS ⊢ izmerjeni pri zagonu 2026-11-11 (T4 kura: eksaktna podvojitev 50→100 ⊙ PADC javno)

type Bit = { telo: string };                       // bit = struktura BREZ rojenega dolga (izrek #5)
interface Stanje { vrsta: string[]; rojeni: number; plačani: number; arhiv: number[] }
interface Pečat { rez: string; mestoVrste: number; kumulativnaD: number } // P6: pečat nosi D-koordinato

const novoStanje = (): Stanje => ({ vrsta: [], rojeni: 0, plačani: 0, arhiv: [] });
const η = (ukaz: string, s: Stanje): string => {   // enota: vsak ukaz rodi dolg brezpogojno (izrek #1a @0.2)
  const d = "dolg:" + ukaz + "#" + (s.rojeni + 1); s.vrsta.push(d); s.rojeni++; return d;
};
const ε = (s: Stanje, plačil: number, red: "FIFO" | "LIFO" = "FIFO"): string[] => { // koenota: plačilo po redu (AX7: FIFO)
  const out: string[] = [];
  for (let i = 0; i < plačil && s.vrsta.length > 0; i++) { out.push(red === "FIFO" ? (s.vrsta.shift() as string) : (s.vrsta.pop() as string)); s.plačani++; }
  s.arhiv.push(s.rojeni - s.plačani);              // ĤΣ: ZAPOREDJE delnih vsot D(n) (P2 — ⟨ne⟩ skupek)
  return out;
};
const D = (s: Stanje): number => s.rojeni - s.plačani;
const zakasnitev = (i: number, et: number, rt: number): number => Math.ceil(i / rt) - Math.ceil(i / et); // P3: L(#i)
const ι = (struktura: string): Bit => ({ telo: struktura }); // izrek #5: ι ∂-prazen
const djb2 = (str: string): string => { let h = 5381; for (let i = 0; i < str.length; i++) { h = ((h << 5) + h) ^ str.charCodeAt(i); } return (h >>> 0).toString(16); }; // zastopnik ⊙ P7 @σ 4634
// P6: dih — pečat rodi z D-koordinato; self-audit rekonstruira D iz verige same
const dih = (s: Stanje, ukaz: string, plačila: number): Pečat => { η(ukaz, s); ε(s, plačila); return { rez: ukaz, mestoVrste: s.rojeni, kumulativnaD: D(s) }; };

// ===== IZREKI ⟨OF⟩-0.3 =====
// #6a (zaobširjen @σ 4639 P1): ε surjektivna (vsak dolg izplačan v ω) ⟺ tok plačil ne umre (Σρ = ∞) pri AX7
// molk = UMRli tok: plačila prenehajo v končnem dihu (Σρ < ∞) — počasen tok (npr. 1 na 10 dihov) NI molk
// #7 (P3): zakasnitev dolga #i pri η<ρ̄: L(i) = ⌈i/ρ⌉ − ⌈i/η⌉ — asimptotsko linearna rast
// #8 (P4): optimum P5 — D ≡ 0 ⟺ ρ = η po vsakem dihu; ⟨EN-DOLG-NA-DIH⟩ = optimalna točka prostora stabilnosti
// #9 (P5/AX7): izrek o strategijah — izplačljivost velja samo za strategije brez lakote; LIFO gladuje (T6)

const testi = (): { testi: string } => {
  const T: Record<string, boolean> = {};
  // T1 — molk = umrli tok (ρ=1 za n≤10, 0 potem) → dolg #11 nikoli izplačan
  { const s = novoStanje(); for (let n = 1; n <= 100; n++) { η("u", s); ε(s, n <= 10 ? 1 : 0); } T.T1_molk = s.plačani === 10 && s.rojeni === 100; }
  // T2 — počasen a ŽIV tok (1 plačilo na 10 dihov, nikoli ne preneha) → surjektivna v ω (kontinuiteta FIFO)
  { const s = novoStanje(); for (let n = 1; n <= 200; n++) { η("u", s); η("u", s); ε(s, n % 10 === 0 ? 1 : 0); } T.T2_pocasenZivTok = s.plačani === 20 && s.vrsta[0] === "dolg:u#21"; }
  // T3 — nihajni tok {0,3} brez enakomernega praga → izplača vse (zaobširitev #6a)
  { const s = novoStanje(); for (let n = 1; n <= 300; n++) { η("u", s); η("u", s); ε(s, n % 3 === 0 ? 3 : 0); } T.T3_nihajniBrezPraga = s.plačani === 300 && s.vrsta[0] === "dolg:u#301"; }
  // T4 — zakasnitev linearna: L(50)=25, L(100)=50, L(100)=2·L(50) — eksaktna podvojitev (kura @PADC stropi)
  { const L50 = zakasnitev(50, 2, 1), L100 = zakasnitev(100, 2, 1); T.T4_zakasnitev = L50 === 25 && L100 === 50 && L100 === 2 * L50; }
  // T5 — optimum P5: ρ=η → D≡0; en dih primanjkljaja → D=1 tam (D≡0 ⟺ ρ=η ∀n)
  { const s = novoStanje(); for (let n = 1; n <= 50; n++) { η("u", s); ε(s, 1); } const optimum = s.arhiv.every((d: number) => d === 0);
    const s2 = novoStanje(); for (let n = 1; n <= 50; n++) { η("u", s2); ε(s2, n === 7 ? 0 : 1); }
    T.T5_optimumP5 = optimum && s2.arhiv[6] === 1 && !s2.arhiv.every((d: number) => d === 0); }
  // T6 — AX7 nuja: LIFO gladuje (dolg #1 izgladnjen) ⊥ FIFO izplača (izrek o strategijah)
  { const sL = novoStanje(); for (let n = 1; n <= 100; n++) { η("u", sL); η("u", sL); ε(sL, 1, "LIFO"); }
    const sF = novoStanje(); for (let n = 1; n <= 100; n++) { η("u", sF); η("u", sF); ε(sF, 1, "FIFO"); }
    T.T6_lifoGladuje = sL.vrsta[0] === "dolg:u#1" && sF.vrsta[0] === "dolg:u#101"; }
  // T7 — self-audit: rekonstrukcija D iz verige pečatov == arhiv; djb2 determinističen (izmerjeno: 85d25aae)
  { const s = novoStanje(); const veriga: Pečat[] = []; for (let n = 1; n <= 100; n++) { veriga.push(dih(s, "u", n % 3 === 0 ? 2 : 1)); }
    const rekon = veriga.map((p: Pečat) => p.kumulativnaD); const isto = rekon.length === s.arhiv.length && rekon.every((v: number, i: number) => v === s.arhiv[i]);
    T.T7_selfAudit = isto && djb2(JSON.stringify(veriga)) === "85d25aae"; }
  // T8 — limita v ℝ∪{∞}: divergentna D(100)=100 ⊢ obstaja; arhiv = ZAPOREDJE (⟨ne⟩ skupek); pariteta → 0
  { const s = novoStanje(); for (let n = 1; n <= 100; n++) { η("u", s); η("u", s); ε(s, 1); }
    const s2 = novoStanje(); for (let n = 1; n <= 100; n++) { η("u", s2); ε(s2, 1); }
    T.T8_limita = s.arhiv[99] === 100 && s.arhiv.length === 100 && s2.arhiv[99] === 0; }
  // T9 — regresija izreka #6b @σ 4638: η=2, ρ=1 → D(100)=100 linearna divergenca
  { const s = novoStanje(); for (let n = 1; n <= 100; n++) { η("u", s); η("u", s); ε(s, 1); } T.T9_regresijaDivergenca = D(s) === 100; }
  // T10 — regresija izreka #5 @σ 4635: ι ∂-prazen — bit iz strukture ne rodi dolga
  { const b = ι("⟡ ukaz ∧ izvajalka"); const s = novoStanje(); η("u", s); T.T10_iPartialen = b.telo.length > 0 && s.rojeni - 1 === 0; }
  const stevilo = Object.values(T).filter(Boolean).length;
  return { testi: stevilo + "/10", ...T };
};

const SKLEP = testi(); // 10/10 PASS ⊢ izmerjeno pri zagonu 2026-11-11 — koda, ki teče, ⟨ne⟩ kip ⊙ §52
