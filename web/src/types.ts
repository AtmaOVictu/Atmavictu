// Mirrors the wire shape of src/workbenchManifest.ts on the API server.
// Deliberately duplicated rather than imported: the frontend depends on the
// JSON contract the API returns, not on backend TS internals.

export type IncomingStatus = "new" | "processing" | "used" | "archived";
export type FragmentStatus = "draft" | "inserted" | "archived";

export interface IncomingText {
  id: string;
  sourcePath: string;
  title?: string;
  status: IncomingStatus;
  note?: string;
}

export interface Fragment {
  id: string;
  incomingTextId: string;
  text: string;
  status: FragmentStatus;
  conceptIds?: string[];
  title?: string;
  note?: string;
}

export interface Insertion {
  id: string;
  fragmentId: string;
  targetChapterPath: string;
  positionNote?: string;
  note?: string;
}

export interface Concept {
  id: string;
  label: string;
  note?: string;
}

export interface WorkbenchManifest {
  manifestVersion: "2";
  incomingTexts: IncomingText[];
  fragments: Fragment[];
  insertions: Insertion[];
  concepts?: Concept[];
}

export interface ManifestValidationResult {
  isValid: boolean;
  errors: string[];
}

export interface ConceptWithCount {
  id: string;
  label: string;
  note?: string;
  fragmentCount: number;
}

export interface SourceAnalysis {
  id: string;
  title?: string;
  sourcePath: string;
  status: IncomingStatus;
  fragmentCount: number;
  draftCount: number;
  insertedCount: number;
  archivedCount: number;
}

export interface Overview {
  manifestVersion: "2";
  incomingTotal: number;
  fragmentTotal: number;
  insertionTotal: number;
  conceptTotal: number;
  chapters: Array<{ path: string; count: number }>;
}

export interface LibraryEntry {
  path: string;
  captured: boolean;
}

export interface DeloArtifactProvenance {
  artifactId: string;
  outputType: string;
  nextAction?: string;
  createdAt?: string;
}

export interface ExtraLibraryEntry {
  path: string;
  deloProvenance: DeloArtifactProvenance | null;
}

export interface TreeEntry {
  path: string;
  insertionCount: number;
}

export type ClaimStatus = "UNVERIFIED" | "SUPPORTED" | "DISPUTED" | "INCONCLUSIVE";
export interface BundlePreview { valid: boolean; errors: string[]; fileCount: number; caseCount: number; caseIds: string[] }
export interface VblCaseEvent { eventId: string; caseId: string; sequence: number; type: string; occurredAt: string; actor: string; previousHash: string | null; payload: Record<string, unknown>; hash: string; }
export interface VblCase {
  id: string; title: string; claim: string; reporter: string; status: ClaimStatus; createdAt: string;
  latestReview?: { reviewer: string; executor: string; outcome: "SUPPORTED" | "DISPUTED" | "INCONCLUSIVE"; scope: string; findings: string[]; eventId: string };
  evidence: Array<{ id: string; label: string; source: string; contentHash: string; addedBy: string; eventId: string }>;
  actions: Array<{ id: string; description: string; owner: string; status: "OPEN" | "DONE"; eventId: string }>;
  events: VblCaseEvent[]; integrity: { valid: boolean; errors: string[] };
}

export interface WreathDriftResult { drift: boolean; door_hash: string | null; manifest_slot_hash: string | null; details: string[]; }

export type WreathStatus = "PASS" | "FAIL" | "UNVERIFIED";

export interface WreathSlotResult {
  path: string;
  size_bytes: number;
  sha256: string;
  status: string;
  language?: string;
  note?: string;
  matched: boolean;
  actualSize: number;
  actualSha256: string;
}

export interface WreathVerification {
  manifestSlots: WreathSlotResult[];
  results: WreathSlotResult[];
  matched: number;
  total: number;
  status: WreathStatus;
}

export interface WreathTongue {
  code: string;
  language: string;
  slot: string;
  canon: string;
  connotation: string;
  status: "slot" | "issued";
}

export interface WreathReportRow {
  code: string;
  language: string;
  slot: string;
  canon: string;
  connotation: string;
  tongueStatus: "slot" | "issued";
  hash: "✓" | "✗";
  matched: boolean;
  review: "none" | "first" | "second";
  deed: "⊢" | "—";
}

export interface WreathReport {
  total: number;
  matched: number;
  status: WreathStatus;
  rows: WreathReportRow[];
  deedCount: number;
  livingDoor: boolean;
}

export interface WreathDriftResult {
  drift: boolean;
  door_hash: string | null;
  manifest_slot_hash: string | null;
  details: string[];
}
