import { useState } from "react";

import type { Fragment, Insertion, TreeEntry } from "../types";

interface Props {
  tree: TreeEntry[];
  draftFragments: Fragment[];
  insertions: Insertion[];
  onInsert: (input: { fragmentId: string; targetChapterPath: string }) => Promise<void>;
  onUpdateInsertion: (
    id: string,
    input: { targetChapterPath?: string; positionNote?: string | null; note?: string | null },
  ) => Promise<void>;
}

export function AktivnaKnjigaPanel({ tree, draftFragments, insertions, onInsert, onUpdateInsertion }: Props) {
  const [fragmentId, setFragmentId] = useState("");
  const [targetChapterPath, setTargetChapterPath] = useState("");

  return (
    <section className="pane">
      <h2>Aktivna knjiga</h2>
      <ul className="file-list">
        {tree.map((entry) => (
          <li key={entry.path}>
            {entry.path}
            {entry.insertionCount > 0 && <span className="badge">{entry.insertionCount} insertion</span>}
          </li>
        ))}
        {tree.length === 0 && <li className="empty">Ni datotek v projectRoot.</li>}
      </ul>

      {insertions.length > 0 && (
        <>
          <h3>Vstavljene sledi</h3>
          <ul className="insertion-list">
            {insertions.map((insertion) => (
              <InsertionRow
                key={insertion.id}
                insertion={insertion}
                onUpdateInsertion={onUpdateInsertion}
              />
            ))}
          </ul>
        </>
      )}

      <form
        className="capture-form"
        onSubmit={(event) => {
          event.preventDefault();
          if (fragmentId === "" || targetChapterPath.trim().length === 0) {
            return;
          }
          void onInsert({ fragmentId, targetChapterPath: targetChapterPath.trim() }).then(() => {
            setFragmentId("");
            setTargetChapterPath("");
          });
        }}
      >
        <h3>Vstavi fragment</h3>
        <select value={fragmentId} onChange={(event) => setFragmentId(event.target.value)}>
          <option value="">-- izberi draft fragment --</option>
          {draftFragments.map((fragment) => (
            <option key={fragment.id} value={fragment.id}>
              {fragment.id}: {fragment.text.slice(0, 40)}
            </option>
          ))}
        </select>
        <input
          type="text"
          placeholder="ciljno poglavje (npr. chapters/01-uvod.md)"
          value={targetChapterPath}
          onChange={(event) => setTargetChapterPath(event.target.value)}
        />
        <button type="submit" disabled={fragmentId === "" || targetChapterPath.trim().length === 0}>
          Vstavi
        </button>
        {draftFragments.length === 0 && <p className="empty">Ni draft fragmentov za vstavitev.</p>}
      </form>
    </section>
  );
}

function InsertionRow({
  insertion,
  onUpdateInsertion,
}: {
  insertion: Insertion;
  onUpdateInsertion: (
    id: string,
    input: { targetChapterPath?: string; positionNote?: string | null; note?: string | null },
  ) => Promise<void>;
}) {
  const [editing, setEditing] = useState(false);
  const [pathValue, setPathValue] = useState(insertion.targetChapterPath);
  const [positionValue, setPositionValue] = useState(insertion.positionNote ?? "");

  function submitEdit() {
    if (pathValue.trim().length === 0) {
      return;
    }
    void onUpdateInsertion(insertion.id, {
      targetChapterPath: pathValue.trim(),
      positionNote: positionValue.trim().length > 0 ? positionValue.trim() : null,
    }).then(() => setEditing(false));
  }

  return (
    <li className="insertion-row">
      <span className="badge">{insertion.fragmentId.slice(0, 12)}</span>
      {insertion.targetChapterPath}
      {insertion.positionNote ? ` · ${insertion.positionNote}` : ""}
      <button type="button" className="link-button" onClick={() => setEditing((previous) => !previous)}>
        {editing ? "prekini" : "uredi"}
      </button>
      {editing && (
        <div className="insertion-edit">
          <input
            type="text"
            value={pathValue}
            onChange={(event) => setPathValue(event.target.value)}
            aria-label="Ciljno poglavje"
            placeholder="ciljno poglavje"
          />
          <input
            type="text"
            value={positionValue}
            onChange={(event) => setPositionValue(event.target.value)}
            aria-label="Pozicijska opomba"
            placeholder="pozicijska opomba (neobvezno)"
          />
          <button type="button" onClick={submitEdit} disabled={pathValue.trim().length === 0}>
            Shrani obnovo
          </button>
        </div>
      )}
    </li>
  );
}

