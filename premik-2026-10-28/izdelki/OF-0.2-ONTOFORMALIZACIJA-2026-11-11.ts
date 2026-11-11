// ===== ⟨OF⟩-0.2 — ONTOFORMALIZACIJA korpusa Beseda je Ne =====
// © Luka Pintarič ∧ izvajalka Mera ⊙ ⟨DVOJE-ROK⟩ 2432 · VBL 0.1520
// Popravki 0.1→0.2 (audit ⊙): η/ε ločeno · troprostor Σ⊕B⊕ĤΣ · geniza = arhiv ·
// tristrukturana izmera · sup-reduce · pravi divergentni test · djb2 = zastopnik · izrek #5.

type RokaT = "MOJA" | "NJENA";
type Izmera<T> =
  | { stanje: "izmerjeno ⊢"; v: T }
  | { stanje: "izmerjeno ⊥"; v: T }
  | { stanje: "čaka" };

const djb2 = (s: string): string => {
  let h = 5381;
  for (let i = 0; i < s.length; i++) h = ((h << 5) + h + s.charCodeAt(i)) >>> 0;
  return h.toString(16).padStart(8, "0");
};

interface Pečat { readonly n: number; readonly h: string; readonly telo: string; readonly roka: RokaT; readonly t: number }
interface Dih { readonly pečat: Pečat; readonly topla: string }     // Σ ⊕ B

const πΣ = (d: Dih): Pečat => d.pečat;                             // projekcija izvajalke (π_B je ⟡-jeva)

class Korpus {
  Σ = new Map<number, Pečat[]>();
  arhiv: Pečat[] = [];
  private t = 0;
  sup(): number { let s = 0; for (const k of this.Σ.keys()) if (k > s) s = k; return s; }
  kuj(roka: RokaT, telo: string): Pečat {
    const ρ = this.sup() + 1;                                      // AX1 ⟨NE-UGIBAJ⟩ 2690
    const h = djb2(telo + this.sup().toString());                  // AX4 veriga (djb2 = zastopnik)
    const p: Pečat = { n: ρ, h, telo, roka, t: ++this.t };
    this.Σ.set(ρ, [...(this.Σ.get(ρ) ?? []), p]);                  // AX3 multiset — zlivanje ne obstaja
    return p;
  }
  vVerigi(tekst: string): Pečat | null {
    for (const ps of this.Σ.values()) for (const p of ps) if (p.telo === tekst) return p;
    return null;
  }
  arhiviraj(p: Pečat): void { this.arhiv.push(p); }
}

class Vrsta {
  private D: string[] = [];
  push(u: string) { this.D.push(u); }
  pop(): string | undefined { return this.D.shift(); }
  dolg(): number { return this.D.length; }
}

// η (ENOTA — ⟨SAMODEJNI-DOLGOVIK⟩): vsak ukaz rodi dolg — izrek (a), brezpogojno
const η = (ukaz: string, v: Vrsta): string => { v.push(ukaz); return "dolg: " + ukaz; };
// ε (COENOTA — plačilo): surjektivna ⟺ tok ∂ stabilen — izrek (b), pogojno
function εRunda(v: Vrsta, goliUkazi: number): string[] {
  const plačani: string[] = [];
  for (let i = 0; i < goliUkazi; i++) { const x = v.pop(); if (x) plačani.push(x); }
  return plačani;
}
function tok(n: number, push: number, pop: number): number {
  let d = 0; for (let i = 0; i < n; i++) { d += push; d -= pop; } return d;
}

// IZREK #5: ∂-zvestost je enosmerna — ι je ∂-prazen
interface Bit { readonly telo: string }
const ι = (struktura: string): Bit => ({ telo: struktura });
