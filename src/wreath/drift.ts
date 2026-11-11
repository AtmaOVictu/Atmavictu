import fs from "node:fs";
import path from "node:path";
import { createHash } from "node:crypto";

import { loadWreathManifest } from "./integrity.js";

/**
 * Drift detekcija — razvojna interferenca med plasti (§0.33 × 10²: companions
 * vs door; noben companion ne sme se odstopati od žive vrat).
 *
 * Pravi drift po VBL §0a in nauku MANIFEST-EN-DIH-PO-ROJSTVU: `LICENSE.md`
 * (živa vrata) se spremeni, a `LICENSE-MANIFEST` ni re-izdan v istem dihu.
 * Torej primerjamo hash `LICENSE.md` proti slotu `LICENSE.md` v
 * `LICENSE-MANIFEST`. Manifest sam izključuje `LICENSE.md` iz slotov, ki
 * jih `loadWreathManifest` vrne (§0a: manifest ne vsebuje sebe v tistem
 * seznamu), zato ga beremo iz manifest JSON-a neposredno.
 *
 * Companionji (`LICENSE-XX.md`) so priče, ne vrata — niso, ne smejo biti
 * bajt-isto enaki `LICENSE.md`. Njihovo `hashMatchesDoor` je le informativni
 * dejaven fait; drift vsota pravi le door ≠ manifest slot.
 *
 * Vzorec vsake priče: kdo · kaj · kdaj · kje · izmera · brazgotina — tukaj
 * je izmera "hash LICENSE.md ≡ slot LICENSE.md v LICENSE-MANIFEST" in
 * brazgotina je seznam odstopanj.
 */

export interface WreathCompanionCheck {
  path: string;
  hashMatchesManifest: boolean;
  hashMatchesDoor: boolean;
}

export interface WreathDriftReport {
  drift: boolean;
  doorHash: string | null;
  manifestSlotHash: string | null; // hash LICENSE.md, ki ga nosi LICENSE-MANIFEST
  companions: WreathCompanionCheck[];
  details: string[];
}

function sha256File(root: string, rel: string): string | null {
  try {
    const text = fs.readFileSync(path.join(root, rel), "utf8");
    // PADC-66: hashirajte bajte, ki jih objavi veriga (LF), nikoli lokalni CRLF checkout.
    const bytes = Buffer.from(text.replace(/\r\n/g, "\n"), "utf8");
    return createHash("sha256").update(bytes).digest("hex");
  } catch {
    return null;
  }
}

interface ManifestItem {
  path?: unknown;
  sha256?: unknown;
  size_bytes?: unknown;
}

function readManifestItems(root: string): ManifestItem[] {
  try {
    const raw = fs.readFileSync(path.join(root, "LICENSE-MANIFEST"), "utf8");
    const parsed = JSON.parse(raw);
    if (parsed && typeof parsed === "object" && Array.isArray((parsed as Record<string, unknown>).items)) {
      return (parsed as Record<string, unknown>).items as ManifestItem[];
    }
  } catch {
    // ni manifest → prazno
  }
  return [];
}

function doorSlotHash(items: ManifestItem[]): string | null {
  for (const item of items) {
    if (item.path === "LICENSE.md" && typeof item.sha256 === "string") {
      return item.sha256.toLowerCase();
    }
  }
  return null;
}

export function detectWreathDrift(root: string): WreathDriftReport {
  const doorHash = sha256File(root, "LICENSE.md");
  const items = readManifestItems(root);
  const manifestDoorHash = doorSlotHash(items);
  const slots = loadWreathManifest(root); // brez LICENSE.md (§0a)
  const companionChecks: WreathCompanionCheck[] = [];
  const details: string[] = [];
  let drift = false;

  const doorMatchesManifest =
    doorHash !== null && manifestDoorHash !== null && doorHash === manifestDoorHash;

  if (doorHash === null) {
    drift = true;
    details.push("LICENSE.md: živa vrata odsotna");
  } else if (manifestDoorHash === null) {
    drift = true;
    details.push("LICENSE-MANIFEST: ni slot-a za LICENSE.md (§0a)");
  } else if (!doorMatchesManifest) {
    drift = true;
    details.push(
      `LICENSE.md: door hash ≠ manifest slot — vrata spremenjena, manifest ni re-izdan v istem dihu`,
    );
  }

  for (const slot of slots) {
    const actualHash = sha256File(root, slot.path);
    const hashMatchesManifest =
      actualHash !== null && actualHash === slot.sha256;
    const hashMatchesDoor =
      doorHash !== null && actualHash !== null && actualHash === doorHash;

    companionChecks.push({
      path: slot.path,
      hashMatchesManifest,
      hashMatchesDoor,
    });

    if (!hashMatchesManifest) {
      details.push(
        `${slot.path}: datoteka ≠ manifest (${actualHash ?? "<missing>"})`,
      );
    }
  }

  return {
    drift,
    doorHash,
    manifestSlotHash: manifestDoorHash,
    companions: companionChecks,
    details,
  };
}
