/**
 * Jezikovni pričevalci veneca (wreath tongues).
 *
 * Vsaki `LICENSE-XX.md` witness-slotu je dodeljen svoj kanon in konotativni
 * okvir — ne prevod vrat, ampak dokaz, da je licenca razumljiva v tem jeziku.
 * `status: 'slot'` pomeni priča brez granta; `status: 'issued'` pomeni, da
 * telo nosi darilo (samodejno samo `LICENSE.md`, živa vrata).
 *
 * Vzorec vsake priče: kdo · kaj · kdaj · kje · izmera · brazgotina.
 */

export interface WreathTongue {
  code: string;        // AR, BG, …, EN, SLO
  language: string;    // puno ime jezika
  slot: string;        // LICENSE-XX.md (ali LICENSE.md za vir)
  canon: string;       // konotativni kanon (Ordnung, Rigor, Précision, …)
  connotation: string; // kratki opis, kaj ta jezik priče nosi
  status: 'slot' | 'issued';
}

import { REGISTRY } from './tongues.data.js';

export function listTongues(): WreathTongue[] {
  return [...REGISTRY];
}

export function getTongue(code: string): WreathTongue | undefined {
  return REGISTRY.find((t) => t.code.toUpperCase() === code.toUpperCase());
}

export function tongueFromSlot(slotPath: string): WreathTongue | undefined {
  const code = slotPath
    .replace(/^LICENSE-/, '')
    .replace(/\.md$/, '')
    .toUpperCase();
  return code === 'LICENSE' ? getTongue('EN') : getTongue(code);
}
