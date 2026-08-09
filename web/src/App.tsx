import { AktivnaKnjigaPanel } from "./components/AktivnaKnjigaPanel";
import { KnjiznicaPanel } from "./components/KnjiznicaPanel";
import { ManifestStatusBar } from "./components/ManifestStatusBar";
import { VhodniTekstPanel } from "./components/VhodniTekstPanel";
import { workbenchApi } from "./api";
import { useWorkbench } from "./useWorkbench";

export function App() {
  const { manifest, verify, library, tree, extraLibrary, concepts, analysis, overview, error, isLoading, runAction } =
    useWorkbench();

  if (isLoading && manifest === null) {
    return <p className="loading">Nalagam manifest...</p>;
  }

  const draftFragments = manifest?.fragments.filter((fragment) => fragment.status === "draft") ?? [];
  const insertions = manifest?.insertions ?? [];

  return (
    <div className="workbench">
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
        />
      </main>
    </div>
  );
}
