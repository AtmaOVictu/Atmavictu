import { useCallback, useEffect, useState } from "react";

import { WorkbenchApiError, workbenchApi } from "./api";
import type { LibraryEntry, ManifestValidationResult, TreeEntry, WorkbenchManifest } from "./types";

interface WorkbenchState {
  manifest: WorkbenchManifest | null;
  verify: ManifestValidationResult | null;
  library: LibraryEntry[];
  tree: TreeEntry[];
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
    error: null,
    isLoading: true,
  });

  const refetchAll = useCallback(async () => {
    setState((previous) => ({ ...previous, isLoading: true }));
    try {
      const [manifest, verify, library, tree] = await Promise.all([
        workbenchApi.getManifest(),
        workbenchApi.getVerify(),
        workbenchApi.getLibrary(),
        workbenchApi.getTree(),
      ]);
      setState({ manifest, verify, library, tree, error: null, isLoading: false });
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
