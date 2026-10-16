import { useCallback, useEffect, useState } from "react";

import { WorkbenchApiError, workbenchApi } from "./api";
import type {
  ConceptWithCount,
  ExtraLibraryEntry,
  LibraryEntry,
  ManifestValidationResult,
  Overview,
  SourceAnalysis,
  TreeEntry,
  WorkbenchManifest,
} from "./types";

interface WorkbenchState {
  manifest: WorkbenchManifest | null;
  verify: ManifestValidationResult | null;
  library: LibraryEntry[];
  tree: TreeEntry[];
  concepts: ConceptWithCount[];
  analysis: SourceAnalysis[];
  overview: Overview | null;
  /** null = server has no extraLibraryRoot configured, not "still loading" or "empty." */
  extraLibrary: ExtraLibraryEntry[] | null;
  error: string | null;
  isLoading: boolean;
}

/**
 * Single source of read state for all three panes. Per SERVICE_CONTRACT.md,
 * the UI is never the source of truth for relations: every mutation is a
 * real API call, followed by a full refetch here, never a local optimistic
 * patch of `manifest`.
 */
export function useWorkbench() {
  const [state, setState] = useState<WorkbenchState>({
    manifest: null,
    verify: null,
    library: [],
    tree: [],
    concepts: [],
    analysis: [],
    overview: null,
    extraLibrary: null,
    error: null,
    isLoading: true,
  });

  const refetchAll = useCallback(async () => {
    setState((previous) => ({ ...previous, isLoading: true }));
    try {
      const [manifest, verify, library, tree, concepts, analysis, overview, extraLibrary] = await Promise.all([
        workbenchApi.getManifest(),
        workbenchApi.getVerify(),
        workbenchApi.getLibrary(),
        workbenchApi.getTree(),
        workbenchApi.getConcepts(),
        workbenchApi.getAnalysisSource(),
        workbenchApi.getOverview(),
        workbenchApi.getExtraLibrary(),
      ]);
      setState({
        manifest,
        verify,
        library,
        tree,
        concepts,
        analysis,
        overview,
        extraLibrary,
        error: null,
        isLoading: false,
      });
    } catch (error) {
      setState((previous) => ({ ...previous, error: describeError(error), isLoading: false }));
    }
  }, []);

  useEffect(() => {
    void refetchAll();
  }, [refetchAll]);

  const runAction = useCallback(
    async (action: () => Promise<unknown>) => {
      try {
        await action();
        await refetchAll();
      } catch (error) {
        setState((previous) => ({ ...previous, error: describeError(error) }));
      }
    },
    [refetchAll],
  );

  return { ...state, runAction };
}

function describeError(error: unknown): string {
  return error instanceof WorkbenchApiError ? error.message : "Unexpected error.";
}
