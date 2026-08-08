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

export interface WorkbenchManifest {
  manifestVersion: "2";
  incomingTexts: IncomingText[];
  fragments: Fragment[];
  insertions: Insertion[];
}

export interface ManifestValidationResult {
  isValid: boolean;
  errors: string[];
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
