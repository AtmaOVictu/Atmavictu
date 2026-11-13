import { useCallback } from "react";

import { AktivnaKnjigaPanel } from "./components/AktivnaKnjigaPanel";
import { KnjiznicaPanel } from "./components/KnjiznicaPanel";
import { ManifestStatusBar } from "./components/ManifestStatusBar";
import { VhodniTekstPanel } from "./components/VhodniTekstPanel";
import { WitnessesPanel } from "./components/WitnessesPanel";
import { VblCasesPanel } from "./components/VblCasesPanel";
import { BundleToolsPanel } from "./components/BundleToolsPanel";
import { tauriApi, workbenchApi } from "./api";
import { useWorkbench } from "./useWorkbench";

export function App() {
  const { manifest, verify, library, tree, extraLibrary, concepts, analysis, overview, error, isLoading, runAction, projectRoot, selectProject } = useWorkbench();

  const openProject = useCallback(async () => {
    const selected = await tauriApi.openFolder();
    if (selected) { await selectProject(selected); }
  }, [selectProject]);

  const draftFragments = manifest?.fragments.filter((fragment) => fragment.status === "draft") ?? [];
  const insertions = manifest?.insertions ?? [];

  return (
    <div className="workbench">
      <header className="project-bar">
        {projectRoot ? (
          <>
            <span className="project-label">Projekt:</span>
            <span className="project-path">{projectRoot}</span>
            <button
              type="button"
              className="link-button"
              onClick={openProject}
              title="Spremeni projekt"
            >
                          Spremeni
            </button>
          </>
        ) : (
          <button type="button" className="primary-button" onClick={openProject}>
            Izberi projektno mapo
          </button>
        )}
      </header>
      <ManifestStatusBar manifest={manifest} verify={verify} error={error} />
      <main className="panes">
        <KnjiznicaPanel
          library={library}
          extraLibrary={extraLibrary}
          onCapture={(input) => runAction(() => workbenchApi.captureIncoming(input))}
        />
        <AktivnaKnjigaPanel
          tree={tree}
          draftFragments={draftFragments}
          insertions={insertions}
          onInsert={(input) => runAction(() => workbenchApi.insertFragment(input))}
          onUpdateInsertion={(id, input) => runAction(() => workbenchApi.updateInsertion(id, input))}
        />
        <VhodniTekstPanel
          incomingTexts={manifest?.incomingTexts ?? []}
          fragments={manifest?.fragments ?? []}
          concepts={concepts}
          overview={overview}
          analysis={analysis}
          onStartProcessing={(id) => runAction(() => workbenchApi.startProcessingIncoming(id))}
          onArchiveIncoming={(id) => runAction(() => workbenchApi.archiveIncoming(id))}
          onCreateFragment={(input) => runAction(() => workbenchApi.createFragment(input))}
          onArchiveFragment={(id) => runAction(() => workbenchApi.archiveFragment(id))}
          onRenameIncoming={(id, title) => runAction(() => workbenchApi.updateIncomingText(id, { title }))}
          onUpdateFragment={(id, input) => runAction(() => workbenchApi.updateFragment(id, input))}
          onAddConcept={(label) => runAction(() => workbenchApi.addConcept({ label }))}
          onSuggest={(text) => workbenchApi.suggestFragment(text)}
          onIndexFragments={() => runAction(() => workbenchApi.indexFragments())}
          onSemanticSearch={(query) => workbenchApi.semanticSearch(query)}
        />
      </main>
      <VblCasesPanel projectRoot={projectRoot} />
      <BundleToolsPanel projectRoot={projectRoot} />
      <WitnessesPanel projectRoot={projectRoot} />
    </div>
  );
}
