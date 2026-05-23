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

interface ValidatedIncomingText {
  id: string | undefined;
  sourcePath: string | undefined;
  status: IncomingStatus | undefined;
}

interface ValidatedFragment {
  id: string | undefined;
  incomingTextId: string | undefined;
  status: FragmentStatus | undefined;
  conceptIds: string[] | undefined;
}

interface ValidatedInsertion {
  id: string | undefined;
  fragmentId: string | undefined;
  targetChapterPath: string | undefined;
}

interface ValidatedConcept {
  id: string | undefined;
}

const INCOMING_STATUSES = ["new", "processing", "used", "archived"] as const;
const FRAGMENT_STATUSES = ["draft", "inserted", "archived"] as const;
const WORKBENCH_MANIFEST_KEYS = ["manifestVersion", "incomingTexts", "fragments", "insertions", "concepts"] as const;
const INCOMING_TEXT_KEYS = ["id", "sourcePath", "title", "status", "note"] as const;
const FRAGMENT_KEYS = ["id", "incomingTextId", "text", "status", "conceptIds", "note"] as const;
const INSERTION_KEYS = ["id", "fragmentId", "targetChapterPath", "positionNote", "note"] as const;
const CONCEPT_KEYS = ["id", "label", "note"] as const;

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

export function validateManifestTransition(
  previousManifest: WorkbenchManifest,
  nextManifest: WorkbenchManifest,
): ManifestValidationResult {
  const errors: string[] = [];
  const previousResult = validateManifest(previousManifest);
  const nextResult = validateManifest(nextManifest);

  if (!previousResult.isValid) {
    errors.push(...previousResult.errors.map((error) => `previousManifest: ${error}`));
  }
  if (!nextResult.isValid) {
    errors.push(...nextResult.errors.map((error) => `nextManifest: ${error}`));
  }

  const previousIncomingStatuses = collectIncomingStatuses(previousManifest);
  const nextIncomingStatuses = collectIncomingStatuses(nextManifest);
  for (const [incomingId, previousStatus] of previousIncomingStatuses) {
    const nextStatus = nextIncomingStatuses.get(incomingId);
    if (nextStatus !== undefined && nextStatus !== previousStatus) {
      if (!ALLOWED_INCOMING_TRANSITIONS[previousStatus].includes(nextStatus)) {
        errors.push(`Invalid IncomingText transition for ${incomingId}: ${previousStatus} -> ${nextStatus}`);
      }
    }
  }

  const previousFragmentStatuses = collectFragmentStatuses(previousManifest);
  const nextFragmentStatuses = collectFragmentStatuses(nextManifest);
  for (const [fragmentId, previousStatus] of previousFragmentStatuses) {
    const nextStatus = nextFragmentStatuses.get(fragmentId);
    if (nextStatus !== undefined && nextStatus !== previousStatus) {
      if (!ALLOWED_FRAGMENT_TRANSITIONS[previousStatus].includes(nextStatus)) {
        errors.push(`Invalid Fragment transition for ${fragmentId}: ${previousStatus} -> ${nextStatus}`);
      }
    }
  }

  return {
    isValid: errors.length === 0,
    errors,
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
  assertValidManifestTransition(manifest, nextManifest, "startProcessingIncoming(result)");

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
  assertValidManifestTransition(manifest, nextManifest, "insertFragmentIntoChapter(result)");

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
  assertValidManifestTransition(manifest, nextManifest, "archiveIncoming(result)");

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
  assertValidManifestTransition(manifest, nextManifest, "archiveFragment(result)");

  return {
    manifest: nextManifest,
    value: updated,
  };
}

export function validateManifest(manifest: WorkbenchManifest): ManifestValidationResult {
  const errors: string[] = [];
  const manifestValue = manifest as unknown;

  if (!isPlainObject(manifestValue)) {
    return {
      isValid: false,
      errors: ["WorkbenchManifest must be an object."],
    };
  }

  validateUnexpectedProperties("WorkbenchManifest", manifestValue, WORKBENCH_MANIFEST_KEYS, errors);

  if (manifestValue.manifestVersion !== "1") {
    errors.push("manifestVersion must be '1'.");
  }

  if (!Array.isArray(manifestValue.incomingTexts)) {
    errors.push("incomingTexts must be an array.");
  }
  if (!Array.isArray(manifestValue.fragments)) {
    errors.push("fragments must be an array.");
  }
  if (!Array.isArray(manifestValue.insertions)) {
    errors.push("insertions must be an array.");
  }
  if (manifestValue.concepts !== undefined && !Array.isArray(manifestValue.concepts)) {
    errors.push("concepts must be an array when present.");
  }

  if (errors.length > 0) {
    return { isValid: false, errors };
  }

  const incomingTexts = manifestValue.incomingTexts as unknown[];
  const fragments = manifestValue.fragments as unknown[];
  const insertions = manifestValue.insertions as unknown[];
  const concepts = (manifestValue.concepts ?? []) as unknown[];
  const incomingIds = new Set<string>();
  const fragmentIds = new Set<string>();
  const insertionIds = new Set<string>();
  const conceptIds = new Set<string>();
  const incomingEntries: ValidatedIncomingText[] = [];
  const fragmentEntries: ValidatedFragment[] = [];

  for (const incomingText of incomingTexts) {
    incomingEntries.push(validateIncomingText(incomingText, incomingIds, errors));
  }

  for (const concept of concepts) {
    validateConcept(concept, conceptIds, errors);
  }

  for (const fragment of fragments) {
    const fragmentEntry = validateFragment(fragment, fragmentIds, errors);
    fragmentEntries.push(fragmentEntry);

    if (fragmentEntry.incomingTextId && !incomingIds.has(fragmentEntry.incomingTextId)) {
      errors.push(`Fragment ${fragmentEntry.id ?? "<unknown>"} references missing IncomingText ${fragmentEntry.incomingTextId}.`);
    }

    if (fragmentEntry.conceptIds) {
      const localConceptIds = new Set<string>();
      for (const conceptId of fragmentEntry.conceptIds) {
        if (!localConceptIds.add(conceptId)) {
          errors.push(`Fragment ${fragmentEntry.id ?? "<unknown>"} contains duplicate conceptId ${conceptId}.`);
        }
        if (!conceptIds.has(conceptId)) {
          errors.push(`Fragment ${fragmentEntry.id ?? "<unknown>"} references missing Concept ${conceptId}.`);
        }
      }
    }

    if (concepts.length === 0 && (fragmentEntry.conceptIds?.length ?? 0) > 0) {
      errors.push(`Fragment ${fragmentEntry.id ?? "<unknown>"} cannot reference conceptIds when concepts are absent.`);
    }
  }

  const insertionsByFragmentId = new Map<string, ValidatedInsertion[]>();
  for (const insertion of insertions) {
    const insertionEntry = validateInsertion(insertion, insertionIds, errors);
    if (insertionEntry.fragmentId && !fragmentIds.has(insertionEntry.fragmentId)) {
      errors.push(`Insertion ${insertionEntry.id ?? "<unknown>"} references missing Fragment ${insertionEntry.fragmentId}.`);
    }

    if (insertionEntry.fragmentId && isPlainObject(insertion)) {
      const nextInsertions = insertionsByFragmentId.get(insertionEntry.fragmentId) ?? [];
      nextInsertions.push(insertionEntry);
      insertionsByFragmentId.set(insertionEntry.fragmentId, nextInsertions);
    }
  }

  for (const fragment of fragmentEntries) {
    if (!fragment.id || !fragment.status) {
      continue;
    }

    const relatedInsertions = insertionsByFragmentId.get(fragment.id) ?? [];
    if (fragment.status === "inserted" && relatedInsertions.length === 0) {
      errors.push(`Inserted Fragment ${fragment.id} must have at least one Insertion.`);
    }
    if (fragment.status === "draft" && relatedInsertions.length > 0) {
      errors.push(`Draft Fragment ${fragment.id} cannot have an Insertion.`);
    }
    if (
      (fragment.status === "inserted" || fragment.status === "archived") &&
      relatedInsertions.some((insertion) => (insertion.targetChapterPath ?? "").trim().length === 0)
    ) {
      errors.push(`Inserted Fragment ${fragment.id} must have a non-empty targetChapterPath.`);
    }
  }

  for (const incomingText of incomingEntries) {
    if (!incomingText.id || !incomingText.status) {
      continue;
    }

    const relatedFragments = fragmentEntries.filter((fragment) => fragment.incomingTextId === incomingText.id);
    const hasInsertionTrail = relatedFragments.some(
      (fragment) => fragment.id !== undefined && (insertionsByFragmentId.get(fragment.id) ?? []).length > 0,
    );

    if (incomingText.status === "new" && relatedFragments.length > 0) {
      errors.push(`IncomingText ${incomingText.id} with status new cannot have related fragments`);
    }

    if (incomingText.status === "used" && !hasInsertionTrail) {
      errors.push(`IncomingText ${incomingText.id} with status used must have an insertion trail`);
    }

    if (
      incomingText.status === "archived" &&
      relatedFragments.some((fragment) => fragment.status === "draft")
    ) {
      errors.push(`IncomingText ${incomingText.id} with status archived cannot have draft fragments`);
    }
  }

  return {
    isValid: errors.length === 0,
    errors,
  };
}

function validateIncomingText(
  incomingText: unknown,
  incomingIds: Set<string>,
  errors: string[],
): ValidatedIncomingText {
  if (!isPlainObject(incomingText)) {
    errors.push("IncomingText must be an object.");
    return { id: undefined, sourcePath: undefined, status: undefined };
  }

  const incomingId = readOptionalString(incomingText.id);
  validateUnexpectedProperties("IncomingText", incomingText, INCOMING_TEXT_KEYS, errors, incomingId);

  if (!isNonEmptyString(incomingText.id)) {
    errors.push("IncomingText.id must be a non-empty string.");
  } else if (!incomingIds.add(incomingText.id)) {
    errors.push(`Duplicate IncomingText id: ${incomingText.id}.`);
  }

  if (!isNonEmptyString(incomingText.sourcePath)) {
    errors.push(`IncomingText ${incomingText.id || "<unknown>"} must have non-empty sourcePath.`);
  } else if (isAbsolutePathValue(incomingText.sourcePath)) {
    errors.push(`IncomingText ${incomingText.id || "<unknown>"} sourcePath must be a relative path`);
  } else if (containsTraversalSegment(incomingText.sourcePath)) {
    errors.push(`IncomingText ${incomingText.id || "<unknown>"} sourcePath cannot contain traversal segments`);
  }

  if (!isIncomingStatus(incomingText.status)) {
    errors.push(`IncomingText ${incomingText.id || "<unknown>"} has invalid status ${String(incomingText.status)}.`);
  }

  validateOptionalStringProperty("IncomingText", incomingText.id, "title", incomingText.title, errors);
  validateOptionalStringProperty("IncomingText", incomingText.id, "note", incomingText.note, errors);

  return {
    id: isNonEmptyString(incomingText.id) ? incomingText.id : undefined,
    sourcePath: isNonEmptyString(incomingText.sourcePath) ? incomingText.sourcePath : undefined,
    status: isIncomingStatus(incomingText.status) ? incomingText.status : undefined,
  };
}

function validateFragment(fragment: unknown, fragmentIds: Set<string>, errors: string[]): ValidatedFragment {
  if (!isPlainObject(fragment)) {
    errors.push("Fragment must be an object.");
    return { id: undefined, incomingTextId: undefined, status: undefined, conceptIds: undefined };
  }

  const fragmentId = readOptionalString(fragment.id);
  validateUnexpectedProperties("Fragment", fragment, FRAGMENT_KEYS, errors, fragmentId);

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

  validateOptionalStringProperty("Fragment", fragment.id, "note", fragment.note, errors);

  if (fragment.conceptIds !== undefined && !Array.isArray(fragment.conceptIds)) {
    errors.push(`Fragment ${fragment.id || "<unknown>"} conceptIds must be an array when present.`);
  }

  return {
    id: isNonEmptyString(fragment.id) ? fragment.id : undefined,
    incomingTextId: isNonEmptyString(fragment.incomingTextId) ? fragment.incomingTextId : undefined,
    status: isFragmentStatus(fragment.status) ? fragment.status : undefined,
    conceptIds: Array.isArray(fragment.conceptIds)
      ? fragment.conceptIds.filter((conceptId): conceptId is string => typeof conceptId === "string")
      : undefined,
  };
}

function validateInsertion(insertion: unknown, insertionIds: Set<string>, errors: string[]): ValidatedInsertion {
  if (!isPlainObject(insertion)) {
    errors.push("Insertion must be an object.");
    return { id: undefined, fragmentId: undefined, targetChapterPath: undefined };
  }

  const insertionId = readOptionalString(insertion.id);
  validateUnexpectedProperties("Insertion", insertion, INSERTION_KEYS, errors, insertionId);

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
  } else if (isAbsolutePathValue(insertion.targetChapterPath)) {
    errors.push(`Insertion ${insertion.id || "<unknown>"} targetChapterPath must be a relative path`);
  } else if (containsTraversalSegment(insertion.targetChapterPath)) {
    errors.push(`Insertion ${insertion.id || "<unknown>"} targetChapterPath cannot contain traversal segments`);
  }

  validateOptionalStringProperty("Insertion", insertion.id, "positionNote", insertion.positionNote, errors);
  validateOptionalStringProperty("Insertion", insertion.id, "note", insertion.note, errors);

  return {
    id: isNonEmptyString(insertion.id) ? insertion.id : undefined,
    fragmentId: isNonEmptyString(insertion.fragmentId) ? insertion.fragmentId : undefined,
    targetChapterPath: isNonEmptyString(insertion.targetChapterPath) ? insertion.targetChapterPath : undefined,
  };
}

function validateConcept(concept: unknown, conceptIds: Set<string>, errors: string[]): ValidatedConcept {
  if (!isPlainObject(concept)) {
    errors.push("Concept must be an object.");
    return { id: undefined };
  }

  const conceptId = readOptionalString(concept.id);
  validateUnexpectedProperties("Concept", concept, CONCEPT_KEYS, errors, conceptId);

  if (!isNonEmptyString(concept.id)) {
    errors.push("Concept.id must be a non-empty string.");
  } else if (!conceptIds.add(concept.id)) {
    errors.push(`Duplicate Concept id: ${concept.id}.`);
  }

  if (!isNonEmptyString(concept.label)) {
    errors.push(`Concept ${concept.id || "<unknown>"} must have non-empty label.`);
  }

  validateOptionalStringProperty("Concept", concept.id, "note", concept.note, errors);

  return {
    id: isNonEmptyString(concept.id) ? concept.id : undefined,
  };
}

function assertValidManifest(manifest: WorkbenchManifest, context: string): void {
  const result = validateManifest(manifest);
  if (!result.isValid) {
    throw new Error(`${context} requires a valid manifest: ${result.errors.join(" | ")}`);
  }
}

function assertValidManifestTransition(
  previousManifest: WorkbenchManifest,
  nextManifest: WorkbenchManifest,
  context: string,
): void {
  const result = validateManifestTransition(previousManifest, nextManifest);
  if (!result.isValid) {
    throw new Error(`${context} requires a valid manifest transition: ${result.errors.join(" | ")}`);
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

function readOptionalString(value: unknown): string | undefined {
  return typeof value === "string" ? value : undefined;
}

function isIncomingStatus(value: unknown): value is IncomingStatus {
  return typeof value === "string" && (INCOMING_STATUSES as readonly string[]).includes(value);
}

function isFragmentStatus(value: unknown): value is FragmentStatus {
  return typeof value === "string" && (FRAGMENT_STATUSES as readonly string[]).includes(value);
}

function isPlainObject(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function validateUnexpectedProperties(
  entityName: string,
  value: Record<string, unknown>,
  allowedKeys: readonly string[],
  errors: string[],
  entityId?: string,
): void {
  for (const key of Object.keys(value)) {
    if (!allowedKeys.includes(key)) {
      if (entityName === "WorkbenchManifest") {
        errors.push(`Unexpected WorkbenchManifest property: ${key}`);
      } else {
        errors.push(`${entityName} ${entityId ?? "<unknown>"} has unexpected property ${key}`);
      }
    }
  }
}

function validateOptionalStringProperty(
  entityName: string,
  entityId: unknown,
  propertyName: string,
  value: unknown,
  errors: string[],
): void {
  if (value !== undefined && typeof value !== "string") {
    errors.push(`${entityName} ${isNonEmptyString(entityId) ? entityId : "<unknown>"} ${propertyName} must be a string when present`);
  }
}

function containsTraversalSegment(pathValue: string): boolean {
  return pathValue.split(/[/\\]+/).some((segment) => segment === "..");
}

function isAbsolutePathValue(pathValue: string): boolean {
  return /^[A-Za-z]:[/\\]/.test(pathValue) || pathValue.startsWith("/") || pathValue.startsWith("\\");
}

function collectIncomingStatuses(manifest: WorkbenchManifest): Map<string, IncomingStatus> {
  const statuses = new Map<string, IncomingStatus>();
  const manifestValue = manifest as unknown;
  if (!isPlainObject(manifestValue) || !Array.isArray(manifestValue.incomingTexts)) {
    return statuses;
  }

  for (const incomingText of manifestValue.incomingTexts) {
    if (isPlainObject(incomingText) && isNonEmptyString(incomingText.id) && isIncomingStatus(incomingText.status)) {
      statuses.set(incomingText.id, incomingText.status);
    }
  }

  return statuses;
}

function collectFragmentStatuses(manifest: WorkbenchManifest): Map<string, FragmentStatus> {
  const statuses = new Map<string, FragmentStatus>();
  const manifestValue = manifest as unknown;
  if (!isPlainObject(manifestValue) || !Array.isArray(manifestValue.fragments)) {
    return statuses;
  }

  for (const fragment of manifestValue.fragments) {
    if (isPlainObject(fragment) && isNonEmptyString(fragment.id) && isFragmentStatus(fragment.status)) {
      statuses.set(fragment.id, fragment.status);
    }
  }

  return statuses;
}
