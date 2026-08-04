import { useState } from "react";

import type { Fragment, IncomingText } from "../types";

interface Props {
  incomingTexts: IncomingText[];
  fragments: Fragment[];
  onStartProcessing: (id: string) => Promise<void>;
  onArchiveIncoming: (id: string) => Promise<void>;
  onCreateFragment: (input: { incomingTextId: string; body: string }) => Promise<void>;
  onArchiveFragment: (id: string) => Promise<void>;
}

export function VhodniTekstPanel({
  incomingTexts,
  fragments,
  onStartProcessing,
  onArchiveIncoming,
  onCreateFragment,
  onArchiveFragment,
}: Props) {
  return (
    <section className="pane">
      <h2>Vhodni tekst</h2>
      {incomingTexts.length === 0 && <p className="empty">Se ni zajetega vhodnega teksta.</p>}
      <ul className="incoming-list">
        {incomingTexts.map((incomingText) => (
          <IncomingTextRow
            key={incomingText.id}
            incomingText={incomingText}
            fragments={fragments.filter((fragment) => fragment.incomingTextId === incomingText.id)}
            onStartProcessing={onStartProcessing}
            onArchiveIncoming={onArchiveIncoming}
            onCreateFragment={onCreateFragment}
            onArchiveFragment={onArchiveFragment}
          />
        ))}
      </ul>
    </section>
  );
}

function IncomingTextRow({
  incomingText,
  fragments,
  onStartProcessing,
  onArchiveIncoming,
  onCreateFragment,
  onArchiveFragment,
}: {
  incomingText: IncomingText;
  fragments: Fragment[];
} & Omit<Props, "incomingTexts" | "fragments">) {
  const [fragmentBody, setFragmentBody] = useState("");
  const canCreateFragment = incomingText.status === "processing" || incomingText.status === "used";
  const canArchiveIncoming = incomingText.status !== "archived";

  return (
    <li className="incoming-row">
      <div className="incoming-header">
        <strong>{incomingText.title ?? incomingText.id}</strong>
        <span className="badge">{incomingText.status}</span>
      </div>
      <div className="source-path">{incomingText.sourcePath}</div>

      <div className="actions">
        {incomingText.status === "new" && (
          <button type="button" onClick={() => void onStartProcessing(incomingText.id)}>
            Zacni obdelavo
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
            <li key={fragment.id}>
              <span className="badge">{fragment.status}</span> {fragment.text.slice(0, 60)}
              {fragment.status !== "archived" && (
                <button type="button" className="link-button" onClick={() => void onArchiveFragment(fragment.id)}>
                  arhiviraj
                </button>
              )}
            </li>
          ))}
        </ul>
      )}
    </li>
  );
}
