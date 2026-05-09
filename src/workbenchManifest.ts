export type IncomingStatus = "new" | "processing" | "used" | "archived";
export type FragmentStatus = "draft" | "inserted" | "archived";

export interface Concept {
  id: string;
  label: string;
  note?: string;
}

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
  manifestVersion: "1";
  incomingTexts: IncomingText[];
  fragments: Fragment[];
  insertions: Insertion[];
  concepts?: Concept[];
}

export interface AddIncomingTextInput {
  title?: string;
  body: string;
  note?: string;
  sourcePath?: string;
}

export interface ManifestUpdate<T> {
  manifest: WorkbenchManifest;
  value: T;
}

export interface ManifestValidationResult {
  isValid: boolean;
  errors: string[];
}

const INCOMING_STATUSES = ["new", "processing", "used", "archived"] as const;
const FRAGMENT_STATUSES = ["draft", "inserted", "archived"] as const;

const ALLOWED_INCOMING_TRANSITIONS: Record<IncomingStatus, readonly IncomingStatus[]> = {
  new: ["processing", "archived"],
  processing: ["used", "archived"],
  used: ["archived"],
  archived: [],
};

const ALLOWED_FRAGMENT_TRANSITIONS: Record<FragmentStatus, readonly FragmentStatus[]> = {
  draft: ["inserted", "archived"],
  inserted: ["archived"],
  archived: [],
};

export function createEmptyManifest(title?: string): WorkbenchManifest {
  // The contract exposes `title` for forward compatibility, but schema v1 does not persist it.
  void title;

  return {
    manifestVersion: "1",
    incomingTexts: [],
    fragments: [],
    insertions: [],
    concepts: [],
  };
}

export function addIncomingText(
  manifest: WorkbenchManifest,
  input: AddIncomingTextInput,
): ManifestUpdate<IncomingText> {
  assertValidManifest(manifest, "addIncomingText");

  const body = requireNonEmptyString("body", input.body);
  void body;

  const id = nextEntityId(
    manifest.incomingTexts.map((incomingText) => incomingText.id),
    "incoming",
  );
  const title = normalizeOptionalString(input.title);
  const note = normalizeOptionalString(input.note);
  const sourcePath = normalizeOptionalString(input.sourcePath) ?? `incoming/${id}.txt`;

  const incomingText: IncomingText = {
    id,
    sourcePath,
    status: "new",
    ...(title ? { title } : {}),
    ...(note ? { note } : {}),
  };

  const nextManifest = cloneManifest(manifest);
  nextManifest.incomingTexts.push(incomingText);
  assertValidManifest(nextManifest, "addIncomingText(result)");

  return {
    manifest: nextManifest,
    value: incomingText,
  };
}

export function startProcessingIncoming(
  manifest: WorkbenchManifest,
  incomingTextId: string,
): ManifestUpdate<IncomingText> {
  assertValidManifest(manifest, "startProcessingIncoming");
  requireNonEmptyString("incomingTextId", incomingTextId);

  const nextManifest = cloneManifest(manifest);
  const index = nextManifest.incomingTexts.findIndex((incomingText) => incomingText.id === incomingTextId);

  if (index === -1) {
    throw new Error(`IncomingText not found: ${incomingTextId}`);
  }

  const current = nextManifest.incomingTexts[index]!;
  assertIncomingTransition(current.status, "processing");

  const updated: IncomingText = {
    ...current,
    status: "processing",
  };

  nextManifest.incomingTexts[index] = updated;
  assertValidManifest(nextManifest, "startProcessingIncoming(result)");

  return {
    manifest: nextManifest,
    value: updated,
  };
}

export function createFragmentFromIncoming(
  manifest: WorkbenchManifest,
  incomingTextId: string,
  body: string,
): ManifestUpdate<Fragment> {
  assertValidManifest(manifest, "createFragmentFromIncoming");
  requireNonEmptyString("incomingTextId", incomingTextId);
  const text = requireNonEmptyString("body", body);

  const incomingText = findIncomingText(manifest, incomingTextId);
  if (incomingText.status === "new") {
    throw new Error(`IncomingText must be processing before fragment creation: ${incomingTextId}`);
  }
  if (incomingText.status === "archived") {
    throw new Error(`IncomingText is archived: ${incomingTextId}`);
  }

  const id = nextEntityId(
    manifest.fragments.map((fragment) => fragment.id),
    "fragment",
  );
  const fragment: Fragment = {
    id,
    incomingTextId,
    text,
    status: "draft",
  };

  const nextManifest = cloneManifest(manifest);
  nextManifest.fragments.push(fragment);
  assertValidManifest(nextManifest, "createFragmentFromIncoming(result)");

  return {
    manifest: nextManifest,
    value: fragment,
  };
}

export function insertFragmentIntoChapter(
  manifest: WorkbenchManifest,
  fragmentId: string,
  targetChapterPath: string,
): ManifestUpdate<Insertion> {
  assertValidManifest(manifest, "insertFragmentIntoChapter");
  requireNonEmptyString("fragmentId", fragmentId);
  const normalizedTargetChapterPath = requireNonEmptyString("targetChapterPath", targetChapterPath);

  const nextManifest = cloneManifest(manifest);
  const fragmentIndex = nextManifest.fragments.findIndex((fragment) => fragment.id === fragmentId);
  if (fragmentIndex === -1) {
    throw new Error(`Fragment not found: ${fragmentId}`);
  }

  const currentFragment = nextManifest.fragments[fragmentIndex]!;
  assertFragmentTransition(currentFragment.status, "inserted");

  const incomingIndex = nextManifest.incomingTexts.findIndex(
    (incomingText) => incomingText.id === currentFragment.incomingTextId,
  );
  if (incomingIndex === -1) {
    throw new Error(`IncomingText not found for fragment: ${currentFragment.incomingTextId}`);
  }

  const currentIncoming = nextManifest.incomingTexts[incomingIndex]!;
  if (currentIncoming.status === "archived") {
    throw new Error(`IncomingText is archived: ${currentIncoming.id}`);
  }
  if (currentIncoming.status === "new") {
    throw new Error(`IncomingText must be processing before insertion: ${currentIncoming.id}`);
  }

  const insertionId = nextEntityId(
    nextManifest.insertions.map((insertion) => insertion.id),
    "insertion",
  );
  const insertion: Insertion = {
    id: insertionId,
    fragmentId,
    targetChapterPath: normalizedTargetChapterPath,
  };

  nextManifest.fragments[fragmentIndex] = {
    ...currentFragment,
    status: "inserted",
  };

  if (currentIncoming.status === "processing") {
    nextManifest.incomingTexts[incomingIndex] = {
      ...currentIncoming,
      status: "used",
    };
  }

  nextManifest.insertions.push(insertion);
  assertValidManifest(nextManifest, "insertFragmentIntoChapter(result)");

  return {
    manifest: nextManifest,
    value: insertion,
  };
}

export function archiveIncoming(
  manifest: WorkbenchManifest,
  incomingTextId: string,
): ManifestUpdate<IncomingText> {
  assertValidManifest(manifest, "archiveIncoming");
  requireNonEmptyString("incomingTextId", incomingTextId);

  const nextManifest = cloneManifest(manifest);
  const index = nextManifest.incomingTexts.findIndex((incomingText) => incomingText.id === incomingTextId);

  if (index === -1) {
    throw new Error(`IncomingText not found: ${incomingTextId}`);
  }

  const current = nextManifest.incomingTexts[index]!;
  assertIncomingTransition(current.status, "archived");

  const updated: IncomingText = {
    ...current,
    status: "archived",
  };

  nextManifest.incomingTexts[index] = updated;
  assertValidManifest(nextManifest, "archiveIncoming(result)");

  return {
    manifest: nextManifest,
    value: updated,
  };
}

export function archiveFragment(
  manifest: WorkbenchManifest,
  fragmentId: string,
): ManifestUpdate<Fragment> {
  assertValidManifest(manifest, "archiveFragment");
  requireNonEmptyString("fragmentId", fragmentId);

  const nextManifest = cloneManifest(manifest);
  const index = nextManifest.fragments.findIndex((fragment) => fragment.id === fragmentId);

  if (index === -1) {
    throw new Error(`Fragment not found: ${fragmentId}`);
  }

  const current = nextManifest.fragments[index]!;
  assertFragmentTransition(current.status, "archived");

  const updated: Fragment = {
    ...current,
    status: "archived",
  };

  nextManifest.fragments[index] = updated;
  assertValidManifest(nextManifest, "archiveFragment(result)");

  return {
    manifest: nextManifest,
    value: updated,
  };
}

export function validateManifest(manifest: WorkbenchManifest): ManifestValidationResult {
  const errors: string[] = [];

  if (manifest.manifestVersion !== "1") {
    errors.push("manifestVersion must be '1'.");
  }

  if (!Array.isArray(manifest.incomingTexts)) {
    errors.push("incomingTexts must be an array.");
  }
  if (!Array.isArray(manifest.fragments)) {
    errors.push("fragments must be an array.");
  }
  if (!Array.isArray(manifest.insertions)) {
    errors.push("insertions must be an array.");
  }
  if (manifest.concepts !== undefined && !Array.isArray(manifest.concepts)) {
    errors.push("concepts must be an array when present.");
  }

  if (errors.length > 0) {
    return { isValid: false, errors };
  }

  const incomingIds = new Set<string>();
  const fragmentIds = new Set<string>();
  const insertionIds = new Set<string>();
  const conceptIds = new Set<string>();

  for (const incomingText of manifest.incomingTexts) {
    validateIncomingText(incomingText, incomingIds, errors);
  }

  for (const concept of manifest.concepts ?? []) {
    validateConcept(concept, conceptIds, errors);
  }

  for (const fragment of manifest.fragments) {
    validateFragment(fragment, fragmentIds, errors);
    if (!incomingIds.has(fragment.incomingTextId)) {
      errors.push(`Fragment ${fragment.id} references missing IncomingText ${fragment.incomingTextId}.`);
    }

    if (fragment.conceptIds) {
      const localConceptIds = new Set<string>();
      for (const conceptId of fragment.conceptIds) {
        if (!localConceptIds.add(conceptId)) {
          errors.push(`Fragment ${fragment.id} contains duplicate conceptId ${conceptId}.`);
        }
        if (!conceptIds.has(conceptId)) {
          errors.push(`Fragment ${fragment.id} references missing Concept ${conceptId}.`);
        }
      }
    }
  }

  const insertionsByFragmentId = new Map<string, Insertion[]>();
  for (const insertion of manifest.insertions) {
    validateInsertion(insertion, insertionIds, errors);
    if (!fragmentIds.has(insertion.fragmentId)) {
      errors.push(`Insertion ${insertion.id} references missing Fragment ${insertion.fragmentId}.`);
    }

    const insertions = insertionsByFragmentId.get(insertion.fragmentId) ?? [];
    insertions.push(insertion);
    insertionsByFragmentId.set(insertion.fragmentId, insertions);
  }

  for (const fragment of manifest.fragments) {
    const insertions = insertionsByFragmentId.get(fragment.id) ?? [];
    if (fragment.status === "inserted" && insertions.length === 0) {
      errors.push(`Inserted Fragment ${fragment.id} must have at least one Insertion.`);
    }
    if (fragment.status === "draft" && insertions.length > 0) {
      errors.push(`Draft Fragment ${fragment.id} cannot have an Insertion.`);
    }
    if (
      fragment.status === "inserted" &&
      insertions.some((insertion) => insertion.targetChapterPath.trim().length === 0)
    ) {
      errors.push(`Inserted Fragment ${fragment.id} must have a non-empty targetChapterPath.`);
    }
  }

  for (const incomingText of manifest.incomingTexts) {
    const relatedFragments = manifest.fragments.filter((fragment) => fragment.incomingTextId === incomingText.id);
    const hasInsertionTrail = relatedFragments.some(
      (fragment) => (insertionsByFragmentId.get(fragment.id) ?? []).length > 0,
    );

    if (
      incomingText.status === "new" &&
      relatedFragments.some((fragment) => fragment.status === "inserted")
    ) {
      errors.push(`IncomingText ${incomingText.id} with status new cannot have inserted fragments.`);
    }

    if (incomingText.status === "used" && relatedFragments.length === 0 && !hasInsertionTrail) {
      errors.push(`IncomingText ${incomingText.id} with status used must have fragment or insertion trail.`);
    }
  }

  return {
    isValid: errors.length === 0,
    errors,
  };
}

function validateIncomingText(
  incomingText: IncomingText,
  incomingIds: Set<string>,
  errors: string[],
): void {
  if (!isNonEmptyString(incomingText.id)) {
    errors.push("IncomingText.id must be a non-empty string.");
  } else if (!incomingIds.add(incomingText.id)) {
    errors.push(`Duplicate IncomingText id: ${incomingText.id}.`);
  }

  if (!isNonEmptyString(incomingText.sourcePath)) {
    errors.push(`IncomingText ${incomingText.id || "<unknown>"} must have non-empty sourcePath.`);
  }

  if (!isIncomingStatus(incomingText.status)) {
    errors.push(`IncomingText ${incomingText.id || "<unknown>"} has invalid status ${String(incomingText.status)}.`);
  }
}

function validateFragment(fragment: Fragment, fragmentIds: Set<string>, errors: string[]): void {
  if (!isNonEmptyString(fragment.id)) {
    errors.push("Fragment.id must be a non-empty string.");
  } else if (!fragmentIds.add(fragment.id)) {
    errors.push(`Duplicate Fragment id: ${fragment.id}.`);
  }

  if (!isNonEmptyString(fragment.incomingTextId)) {
    errors.push(`Fragment ${fragment.id || "<unknown>"} must have non-empty incomingTextId.`);
  }
  if (!isNonEmptyString(fragment.text)) {
    errors.push(`Fragment ${fragment.id || "<unknown>"} must have non-empty text.`);
  }
  if (!isFragmentStatus(fragment.status)) {
    errors.push(`Fragment ${fragment.id || "<unknown>"} has invalid status ${String(fragment.status)}.`);
  }
}

function validateInsertion(insertion: Insertion, insertionIds: Set<string>, errors: string[]): void {
  if (!isNonEmptyString(insertion.id)) {
    errors.push("Insertion.id must be a non-empty string.");
  } else if (!insertionIds.add(insertion.id)) {
    errors.push(`Duplicate Insertion id: ${insertion.id}.`);
  }
  if (!isNonEmptyString(insertion.fragmentId)) {
    errors.push(`Insertion ${insertion.id || "<unknown>"} must have non-empty fragmentId.`);
  }
  if (!isNonEmptyString(insertion.targetChapterPath)) {
    errors.push(`Insertion ${insertion.id || "<unknown>"} must have non-empty targetChapterPath.`);
  }
}

function validateConcept(concept: Concept, conceptIds: Set<string>, errors: string[]): void {
  if (!isNonEmptyString(concept.id)) {
    errors.push("Concept.id must be a non-empty string.");
  } else if (!conceptIds.add(concept.id)) {
    errors.push(`Duplicate Concept id: ${concept.id}.`);
  }

  if (!isNonEmptyString(concept.label)) {
    errors.push(`Concept ${concept.id || "<unknown>"} must have non-empty label.`);
  }
}

function assertValidManifest(manifest: WorkbenchManifest, context: string): void {
  const result = validateManifest(manifest);
  if (!result.isValid) {
    throw new Error(`${context} requires a valid manifest: ${result.errors.join(" | ")}`);
  }
}

function findIncomingText(manifest: WorkbenchManifest, incomingTextId: string): IncomingText {
  const incomingText = manifest.incomingTexts.find((candidate) => candidate.id === incomingTextId);
  if (!incomingText) {
    throw new Error(`IncomingText not found: ${incomingTextId}`);
  }

  return incomingText;
}

function assertIncomingTransition(from: IncomingStatus, to: IncomingStatus): void {
  if (!ALLOWED_INCOMING_TRANSITIONS[from].includes(to)) {
    throw new Error(`Invalid IncomingText transition: ${from} -> ${to}`);
  }
}

function assertFragmentTransition(from: FragmentStatus, to: FragmentStatus): void {
  if (!ALLOWED_FRAGMENT_TRANSITIONS[from].includes(to)) {
    throw new Error(`Invalid Fragment transition: ${from} -> ${to}`);
  }
}

function cloneManifest(manifest: WorkbenchManifest): WorkbenchManifest {
  return {
    manifestVersion: manifest.manifestVersion,
    incomingTexts: manifest.incomingTexts.map((incomingText) => ({ ...incomingText })),
    fragments: manifest.fragments.map((fragment) => ({
      ...fragment,
      ...(fragment.conceptIds ? { conceptIds: [...fragment.conceptIds] } : {}),
    })),
    insertions: manifest.insertions.map((insertion) => ({ ...insertion })),
    ...(manifest.concepts ? { concepts: manifest.concepts.map((concept) => ({ ...concept })) } : {}),
  };
}

function nextEntityId(existingIds: string[], prefix: string): string {
  let sequence = 1;

  while (existingIds.includes(formatEntityId(prefix, sequence))) {
    sequence += 1;
  }

  return formatEntityId(prefix, sequence);
}

function formatEntityId(prefix: string, sequence: number): string {
  return `${prefix}-${String(sequence).padStart(4, "0")}`;
}

function requireNonEmptyString(name: string, value: string): string {
  const normalizedValue = value.trim();
  if (normalizedValue.length === 0) {
    throw new Error(`${name} must be a non-empty string.`);
  }

  return normalizedValue;
}

function normalizeOptionalString(value: string | undefined): string | undefined {
  if (value === undefined) {
    return undefined;
  }

  const normalizedValue = value.trim();
  return normalizedValue.length > 0 ? normalizedValue : undefined;
}

function isNonEmptyString(value: unknown): value is string {
  return typeof value === "string" && value.trim().length > 0;
}

function isIncomingStatus(value: unknown): value is IncomingStatus {
  return typeof value === "string" && (INCOMING_STATUSES as readonly string[]).includes(value);
}

function isFragmentStatus(value: unknown): value is FragmentStatus {
  return typeof value === "string" && (FRAGMENT_STATUSES as readonly string[]).includes(value);
}
