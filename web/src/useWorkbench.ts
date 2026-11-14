import { useCallback, useEffect, useState } from "react";

import { WorkbenchApiError, tauriApi, workbenchApi } from "./api";
import type {
  ConceptWithCount,
  ExtraLibraryEntry,
  LibraryEntry,
  ManifestValidationResult,
  Overview,
  SourceAnalysis,
  TreeEntry,
  WreathReport,
  WreathVerification,
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
  extraLibrary: ExtraLibraryEntry[] | null;
  wreathVerify: WreathVerification | null;
  wreathReport: WreathReport | null;
  error: string | null;
  isLoading: boolean;
}

function isTauri(): boolean {
  return Boolean((window as Window & { __TAURI_INTERNALS__?: unknown }).__TAURI_INTERNALS__);
}

const EMPTY_STATE: Omit<WorkbenchState, "isLoading"> = {
  manifest: null, verify: null, library: [], tree: [], concepts: [], analysis: [], overview: null,
  extraLibrary: null, wreathVerify: null, wreathReport: null, error: null,
};

export function useWorkbench() {
  const [projectRoot, setProjectRoot] = useState<string | null>(null);
  const [state, setState] = useState<WorkbenchState>({ ...EMPTY_STATE, isLoading: true });

  const refetchAll = useCallback(async () => {
    setState((previous) => ({ ...previous, isLoading: true }));
    try {
      if (isTauri()) {
        if (!projectRoot) {
          setState({ ...EMPTY_STATE, isLoading: false });
          return;
        }
        const [manifest, verify, seal] = await Promise.all([
          tauriApi.readManifest(projectRoot), tauriApi.verifyManifest(projectRoot), tauriApi.readSeal(projectRoot),
        ]);
        const sealErrors = seal ? [] : ["book.workbench.seal.json is absent."];
        setState({
          ...EMPTY_STATE,
          manifest,
          verify: { isValid: verify.isValid && sealErrors.length === 0, errors: [...verify.errors, ...sealErrors] },
          wreathVerify: null,
          isLoading: false,
        });
        return;
      }
      const selectedProject = projectRoot ? { projectRoot } : await workbenchApi.getProject();
      setProjectRoot(selectedProject.projectRoot);
      const [manifest, verify, library, tree, concepts, analysis, overview, extraLibrary, wreathVerify, wreathReport] = await Promise.all([
        workbenchApi.getManifest(), workbenchApi.getVerify(), workbenchApi.getLibrary(), workbenchApi.getTree(),
        workbenchApi.getConcepts(), workbenchApi.getAnalysisSource(), workbenchApi.getOverview(),
        workbenchApi.getExtraLibrary(), workbenchApi.getWreathVerify(), workbenchApi.getWreathReport(),
      ]);
      setState({ manifest, verify, library, tree, concepts, analysis, overview, extraLibrary, wreathVerify, wreathReport, error: null, isLoading: false });
    } catch (error) {
      setState((previous) => ({ ...previous, error: describeError(error), isLoading: false }));
    }
  }, [projectRoot]);

  useEffect(() => { void refetchAll(); }, [refetchAll]);

  const runAction = useCallback(async (action: () => Promise<unknown>) => {
    try { await action(); await refetchAll(); }
    catch (error) { setState((previous) => ({ ...previous, error: describeError(error) })); }
  }, [refetchAll]);

  const selectProject = useCallback(async (root: string) => {
    if (!isTauri()) await workbenchApi.selectProject(root);
    setProjectRoot(root);
  }, []);

  return { ...state, runAction, projectRoot, selectProject };
}

function describeError(error: unknown): string {
  return error instanceof WorkbenchApiError ? error.message : error instanceof Error ? error.message : "Unexpected error.";
}
