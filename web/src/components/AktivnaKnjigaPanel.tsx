import { useState } from "react";

import type { Fragment, TreeEntry } from "../types";

interface Props {
  tree: TreeEntry[];
  draftFragments: Fragment[];
  onInsert: (input: { fragmentId: string; targetChapterPath: string }) => Promise<void>;
}

export function AktivnaKnjigaPanel({ tree, draftFragments, onInsert }: Props) {
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
