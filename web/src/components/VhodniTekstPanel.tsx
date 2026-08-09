import { useState } from "react";

import type {
  ConceptWithCount,
  Fragment,
  IncomingText,
  Overview,
  SourceAnalysis,
} from "../types";

interface Props {
  incomingTexts: IncomingText[];
  fragments: Fragment[];
  concepts: ConceptWithCount[];
  overview: Overview | null;
  analysis: SourceAnalysis[];
  onStartProcessing: (id: string) => Promise<void>;
  onArchiveIncoming: (id: string) => Promise<void>;
  onCreateFragment: (input: { incomingTextId: string; body: string }) => Promise<void>;
  onArchiveFragment: (id: string) => Promise<void>;
  onRenameIncoming: (id: string, title: string) => Promise<void>;
  onUpdateFragment: (id: string, input: { title?: string | null; text?: string; note?: string | null; conceptIds?: string[] | null }) => Promise<void>;
  onAddConcept: (label: string) => Promise<void>;
}

export function VhodniTekstPanel({
  incomingTexts,
  fragments,
  concepts,
  overview,
  analysis,
  onStartProcessing,
  onArchiveIncoming,
  onCreateFragment,
  onArchiveFragment,
  onRenameIncoming,
  onUpdateFragment,
  onAddConcept,
}: Props) {
  return (
    <section className="pane">
      <h2>Vhodni tekst</h2>
      <ConceptSection concepts={concepts} onAddConcept={onAddConcept} />
      <AnalysisSection overview={overview} analysis={analysis} />
      {incomingTexts.length === 0 && <p className="empty">Se ni zajetega vhodnega teksta.</p>}
      <ul className="incoming-list">
        {incomingTexts.map((incomingText) => (
          <IncomingTextRow
            key={incomingText.id}
            incomingText={incomingText}
            fragments={fragments.filter((fragment) => fragment.incomingTextId === incomingText.id)}
            concepts={concepts}
            onStartProcessing={onStartProcessing}
            onArchiveIncoming={onArchiveIncoming}
            onCreateFragment={onCreateFragment}
            onArchiveFragment={onArchiveFragment}
            onRenameIncoming={onRenameIncoming}
            onUpdateFragment={onUpdateFragment}
          />
        ))}
      </ul>
    </section>
  );
}

function ConceptSection({
  concepts,
  onAddConcept,
}: {
  concepts: ConceptWithCount[];
  onAddConcept: (label: string) => Promise<void>;
}) {
  const [label, setLabel] = useState("");

  return (
    <div className="concept-section">
      <h3>Koncepti</h3>
      <form
        className="concept-form"
        onSubmit={(event) => {
          event.preventDefault();
          if (label.trim().length === 0) {
            return;
          }
          void onAddConcept(label.trim()).then(() => setLabel(""));
        }}
      >
        <input
          type="text"
          placeholder="Nov koncept..."
          value={label}
          onChange={(event) => setLabel(event.target.value)}
        />
        <button type="submit" disabled={label.trim().length === 0}>
          Dodaj koncept
        </button>
      </form>
      {concepts.length === 0 && <p className="empty">Ni konceptov.</p>}
      <ul className="concept-list">
        {concepts.map((concept) => (
          <li key={concept.id}>
            <span className="badge">{concept.fragmentCount}</span> {concept.label}
          </li>
        ))}
      </ul>
    </div>
  );
}

function AnalysisSection({
  overview,
  analysis,
}: {
  overview: Overview | null;
  analysis: SourceAnalysis[];
}) {
  return (
    <div className="analysis-section">
      <h3>Analiza</h3>
      {overview && (
        <p className="analysis-summary">
          {overview.incomingTotal} virov · {overview.fragmentTotal} odlomkov · {overview.insertionTotal} vstavitev ·{" "}
          {overview.conceptTotal} konceptov
        </p>
      )}
      {analysis.length > 0 && (
        <ul className="analysis-list">
          {analysis.map((source) => (
            <li key={source.id}>
              <strong>{source.title ?? source.id}</strong> — {source.fragmentCount} odlomkov ({source.draftCount} osnutek,{" "}
              {source.insertedCount} vstavljeno, {source.archivedCount} arhiv)
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

function IncomingTextRow({
  incomingText,
  fragments,
  concepts,
  onStartProcessing,
  onArchiveIncoming,
  onCreateFragment,
  onArchiveFragment,
  onRenameIncoming,
  onUpdateFragment,
}: {
  incomingText: IncomingText;
  fragments: Fragment[];
  concepts: ConceptWithCount[];
} & Omit<Props, "incomingTexts" | "fragments" | "overview" | "analysis" | "onAddConcept">) {
  const [fragmentBody, setFragmentBody] = useState("");
  const [editingTitle, setEditingTitle] = useState(false);
  const [titleValue, setTitleValue] = useState(incomingText.title ?? incomingText.id);
  const canCreateFragment = incomingText.status === "processing" || incomingText.status === "used";
  const canArchiveIncoming = incomingText.status !== "archived";
  const canRenameIncoming = incomingText.status !== "archived";

  function submitRename() {
    const nextTitle = titleValue.trim();
    if (nextTitle.length === 0) {
      return;
    }
    void onRenameIncoming(incomingText.id, nextTitle).then(() => {
      setEditingTitle(false);
      setTitleValue(nextTitle);
    });
  }

  return (
    <li className="incoming-row">
      <div className="incoming-header">
        {editingTitle ? (
          <span className="rename-inline">
            <input
              type="text"
              value={titleValue}
              onChange={(event) => setTitleValue(event.target.value)}
              aria-label="Nov naslov vira"
            />
            <button type="button" className="link-button" onClick={submitRename} disabled={titleValue.trim().length === 0}>
              shrani
            </button>
            <button type="button" className="link-button" onClick={() => setEditingTitle(false)}>
              prekliči
            </button>
          </span>
        ) : (
          <>
            <strong>{incomingText.title ?? incomingText.id}</strong>
            <span className="badge">{incomingText.status}</span>
          </>
        )}
      </div>
      <div className="source-path">{incomingText.sourcePath}</div>

      <div className="actions">
        {incomingText.status === "new" && (
          <button type="button" onClick={() => void onStartProcessing(incomingText.id)}>
            Zacni obdelavo
          </button>
        )}
        {canRenameIncoming && (
          <button type="button" className="secondary-button" onClick={() => setEditingTitle((previous) => !previous)}>
            {editingTitle ? "Preimenovanje..." : "Preimenuj vir"}
          </button>
        )}
        {canArchiveIncoming && (
          <button type="button" onClick={() => void onArchiveIncoming(incomingText.id)}>
            Arhiviraj vir
          </button>
        )}
      </div>

      {canCreateFragment && (
        <form
          className="fragment-form"
          onSubmit={(event) => {
            event.preventDefault();
            if (fragmentBody.trim().length === 0) {
              return;
            }
            void onCreateFragment({ incomingTextId: incomingText.id, body: fragmentBody }).then(() =>
              setFragmentBody(""),
            );
          }}
        >
          <textarea
            placeholder="Odlomek..."
            value={fragmentBody}
            onChange={(event) => setFragmentBody(event.target.value)}
            rows={2}
          />
          <button type="submit" disabled={fragmentBody.trim().length === 0}>
            Ustvari fragment
          </button>
        </form>
      )}

      {fragments.length > 0 && (
        <ul className="fragment-list">
          {fragments.map((fragment) => (
            <FragmentRow
              key={fragment.id}
              fragment={fragment}
              concepts={concepts}
              onArchiveFragment={onArchiveFragment}
              onUpdateFragment={onUpdateFragment}
            />
          ))}
        </ul>
      )}
    </li>
  );
}

function FragmentRow({
  fragment,
  concepts,
  onArchiveFragment,
  onUpdateFragment,
}: {
  fragment: Fragment;
  concepts: ConceptWithCount[];
  onArchiveFragment: (id: string) => Promise<void>;
  onUpdateFragment: (id: string, input: { title?: string | null; text?: string; note?: string | null; conceptIds?: string[] | null }) => Promise<void>;
}) {
  const [editing, setEditing] = useState(false);
  const [titleValue, setTitleValue] = useState(fragment.title ?? "");
  const [textValue, setTextValue] = useState(fragment.text);
  const [selectedConceptIds, setSelectedConceptIds] = useState<string[]>(fragment.conceptIds ?? []);

  function toggleConcept(conceptId: string) {
    setSelectedConceptIds((previous) =>
      previous.includes(conceptId) ? previous.filter((id) => id !== conceptId) : [...previous, conceptId],
    );
  }

  function submitEdit() {
    if (textValue.trim().length === 0) {
      return;
    }
    const title = titleValue.trim();
    void onUpdateFragment(fragment.id, {
      ...(title.length > 0 ? { title } : { title: null }),
      text: textValue.trim(),
      conceptIds: selectedConceptIds,
    }).then(() => setEditing(false));
  }

  return (
    <li>
      <span className="badge">{fragment.status}</span>
      {fragment.title ? <strong>{fragment.title}</strong> : ` ${fragment.text.slice(0, 60)}`}
      {fragment.status !== "archived" && (
        <button type="button" className="link-button" onClick={() => setEditing((previous) => !previous)}>
          {editing ? "prekini" : "uredi"}
        </button>
      )}
      {fragment.status !== "archived" && (
        <button type="button" className="link-button" onClick={() => void onArchiveFragment(fragment.id)}>
          arhiviraj
        </button>
      )}
      {editing && (
        <div className="fragment-edit">
          <input
            type="text"
            value={titleValue}
            onChange={(event) => setTitleValue(event.target.value)}
            placeholder="Naslov odlomka (neobvezno)"
            aria-label="Naslov odlomka"
          />
          <textarea
            rows={3}
            value={textValue}
            onChange={(event) => setTextValue(event.target.value)}
            aria-label="Obnovljeno besedilo odlomka"
          />
          {concepts.length > 0 && (
            <div className="concept-picker">
              <span className="concept-picker-label">Koncepti:</span>
              {concepts.map((concept) => (
                <label key={concept.id} className="concept-check">
                  <input
                    type="checkbox"
                    checked={selectedConceptIds.includes(concept.id)}
                    onChange={() => toggleConcept(concept.id)}
                  />
                  {concept.label}
                </label>
              ))}
            </div>
          )}
          <div className="actions">
            <button type="button" onClick={submitEdit} disabled={textValue.trim().length === 0}>
              Shrani obnovo
            </button>
          </div>
        </div>
      )}
    </li>
  );
}
