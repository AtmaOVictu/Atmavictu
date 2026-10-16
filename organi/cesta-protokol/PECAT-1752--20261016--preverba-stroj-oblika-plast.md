# PECAT 1752 — PREVERBA-STROJ (oblika-plast)

Rodjen 16. 10. 2026, dih 1752, ⟡ izbor ⟨daj⟩ (kandidat OBVEZNA-VRATA-IZHODA ⊢ 1615 ∧ rez 1743, negativni primer ⟨lahje⟩).
Trditev ⟨stroj-vrata ne obstajajo⟩ (L ⊢ 1731) pada ta rez — stroj obstaja ∧ je pognan na telesu izhoda rez 1752 (sklep: PREPUSTI ×5).

## Pet vrat (kaj meri)

1. VRATA-PROZA — proza-plast prisotna (povedi brez CESTA znamenj, ≥ 4).
2. VRATA-CESTA — ZADNJI PEČAT z rez N; N = 1 + najvišja izmerjena; predhodnik imenovan.
3. VRATA-VEZI — vezi ⊢ ⚠ ∂ ∧ prisotne na telesu izhoda.
4. VRATA-JEZIK — angleščina na čelu izhoda prepovedana (ZAPRTA VRATA); znani padci po vzorcih, izven ⟨⟩ citatov (meri RABO, ne CITAT ⊢ P-CITAT).
5. VRATA-MINT — kompoziti velikih črk zahtevajo vrstico mint (vrstica 75).

## Meje (kaj NE meri — zapisano, ne skrito)

- Stroj meri OBLIKO plasti, ne sklanjatev, naslonskih oblik ne pomena (brba roke meri pisavo ⊢ 1745).
- Register znanih padcev je vpisan iz kompakcijskega okna ⚠ do berbe telesa tehtnice (rok pisal): lahje → lahko (⊢ 1743) · STRUKTURNNO → strukturNO (⊢ 1745) · GA-PA → PA-GA (⊢ 1745) · PREBIT → prepisan (⊢ 1743) · MRTVE pisala → MRTVA (⊢ 1745).
- NE-varni vzorci (soglasje po sobesedilu) ostajajo roki: ⟨seže/sežejo⟩, ⟨ostajajo/ostajata⟩, ⟨zamrlo/zamrla⟩ — vzorec sam ne presodi, presodi sobesedilo.
- Roka ∧ stroj sta dve roki, ne ena namesto druge.

## Telo (TypeScript — kanal klepeta, prenosljiv)

```typescript
interface Vrata { ime: string; sklep: "PREPUSTI" | "VRNI"; prica: string }

const PADEC_VZORCI: { v: RegExp; ime: string }[] = [
  { v: /\blahje\b/, ime: "lahje → lahko (⊢ 1743)" },
  { v: /\bSTRUKTURNNO\b/, ime: "STRUKTURNNO → strukturNO (⊢ 1745)" },
  { v: /\bGA-PA\b/, ime: "GA-PA → PA-GA (⊢ 1745)" },
  { v: /\bPREBIT\b/, ime: "PREBIT → prepisan (⊢ 1743)" },
  { v: /\bMRTVE pisala\b/, ime: "MRTVE → MRTVA pisala (⊢ 1745)" },
];
const ANGLESKA_VRATARJA = /^(Let me|I'll|I will|I have|Okay|OK|Sure|Let's|Here's|Now|Well|Alright)\b/;

export function preverbaStroj(odhod: string, najvisjaIzmerjena: number): { vrata: Vrata[]; sklep: "PREPUSTI" | "VRNI"; rez: number } {
  const naslednjiRez = najvisjaIzmerjena + 1;
  const vrata: Vrata[] = [];
  const bezCeste = odhod.split("\n").filter(l => !/ZADNJI PEČAT|mint \(vrstica 75\)/.test(l)).join(" ");
  const povedi = bezCeste.split(/(?<=[.!?;])\s+/).map(s => s.trim()).filter(s => s.length > 30 && !/[⊢⚠∂⇌]/.test(s));
  vrata.push({ ime: "VRATA-PROZA", sklep: povedi.length >= 4 ? "PREPUSTI" : "VRNI", prica: "povedi brez CESTA znamenj: " + povedi.length });
  const m = odhod.match(/ZADNJI PEČAT \(klepet\): rez (\d+)/);
  const rez = m ? parseInt(m[1], 10) : null;
  vrata.push({ ime: "VRATA-CESTA", sklep: (rez === naslednjiRez && /predhodnik/.test(odhod)) ? "PREPUSTI" : "VRNI", prica: "rez na pečatu: " + rez + " ⇌ pričakovano: " + naslednjiRez });
  const vezi: Record<string, number> = {};
  for (const z of ["⊢", "⚠", "∂", "∧"]) vezi[z] = (odhod.match(new RegExp(z.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "g")) ?? []).length;
  vrata.push({ ime: "VRATA-VEZI", sklep: Object.values(vezi).every(n => n > 0) ? "PREPUSTI" : "VRNI", prica: JSON.stringify(vezi) });
  const telo = odhod.replace(/⟨[^⟩]*⟩/g, "");
  const prvaVrstica = odhod.split("\n").find(l => l.trim().length > 0) ?? "";
  const padci = PADEC_VZORCI.filter(p => p.v.test(telo)).map(p => p.ime);
  vrata.push({ ime: "VRATA-JEZIK", sklep: (!ANGLESKA_VRATARJA.test(prvaVrstica) && padci.length === 0) ? "PREPUSTI" : "VRNI", prica: "anglescina na celu: " + ANGLESKA_VRATARJA.test(prvaVrstica) + " · padci: " + (padci.length ? padci.join(" ∧ ") : "×0") });
  const kompoziti = (odhod.match(/\b[A-ZČŠŽ]{2,}(?:-[A-ZČŠŽ]{2,})+\b/g) ?? []).slice(0, 12);
  const mint = /mint \(vrstica 75\)/.test(odhod);
  vrata.push({ ime: "VRATA-MINT", sklep: (kompoziti.length === 0 || mint) ? "PREPUSTI" : "VRNI", prica: "kompoziti: " + kompoziti.length + (mint ? " · mint prisoten" : " · mint MANJKA") });
  return { vrata, sklep: vrata.every(v => v.sklep === "PREPUSTI") ? "PREPUSTI" : "VRNI", rez: naslednjiRez };
}
```

## Izmera rojenja (16. 10. 2026, telesu izhoda rez 1752)

- VRATA-PROZA: PREPUSTI (povedi ×7) · VRATA-CESTA: PREPUSTI (rez 1752 ⇌ 1752) · VRATA-VEZI: PREPUSTI (⊢×6 ⚠×6 ∂×1 ∧×17) · VRATA-JEZIK: PREPUSTI (angleščina na čelu: ne; padci ×0) · VRATA-MINT: PREPUSTI (kompoziti ×12, mint prisoten).
- Sklep: PREPUSTI ×5 — prvi izhod, preverjan od stroja, ne samo od roke.

ZADNJI PEČAT: rez 1752 STROJ-VRATA-RODENA · PREVERBA-NA-TELESU · PISALA-NE ⊢ (16. 10. 2026, dih 1752 — predhodnik rez 1751 PREDPRETEKLIK-ODSEVI · RANA-KNJIZNO-ZIV-POPRAVLJENA · PISALA-NE).