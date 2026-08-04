import { useState } from "react";

import { workbenchApi } from "../api";
import type { ExtraLibraryEntry, LibraryEntry } from "../types";

interface Props {
  library: LibraryEntry[];
  extraLibrary: ExtraLibraryEntry[] | null;
  onCapture: (input: { title?: string; body: string }) => Promise<void>;
}

/**
 * The one pane with no contract-doc precedent (see ARCHITECTURE.md): browses
 * projectRoot for candidate source material, plus an optional second,
 * read-only source (extraLibraryRoot — e.g. a Smisel WorkShade `drafts/`
 * folder passed at server startup; null here just means none was configured,
 * not an error or "still loading").
 */
export function KnjiznicaPanel({ library, extraLibrary, onCapture }: Props) {
  const [title, setTitle] = useState("");
  const [body, setBody] = useState("");
  const [loadError, setLoadError] = useState<string | null>(null);

  function useAsCapture(prefillTitle: string, content: string) {
    setTitle(prefillTitle);
    setBody(content);
    setLoadError(null);
  }

  async function loadContentInto(fetchContent: () => Promise<{ content: string }>, prefillTitle: string) {
    try {
      const { content } = await fetchContent();
      useAsCapture(prefillTitle, content);
    } catch {
      setLoadError(`Ni bilo mogoče prebrati: ${prefillTitle}`);
    }
  }

  return (
    <section className="pane">
      <h2>Knjiznica</h2>
      <ul className="file-list">
        {library.map((entry) => (
          <li key={entry.path}>
            <button
              type="button"
              className="link-button"
              onClick={() => void loadContentInto(() => workbenchApi.getLibraryContent(entry.path), entry.path)}
            >
              {entry.path}
            </button>
            {entry.captured && <span className="badge">captured</span>}
          </li>
        ))}
        {library.length === 0 && <li className="empty">Ni datotek v projectRoot.</li>}
      </ul>

      {extraLibrary !== null && (
        <>
          <h3>Zunanji vir (npr. Delo osnutki)</h3>
          <ul className="file-list">
            {extraLibrary.map((entry) => (
              <li key={entry.path}>
                <button
                  type="button"
                  className="link-button"
                  onClick={() =>
                    void loadContentInto(() => workbenchApi.getExtraLibraryContent(entry.path), entry.path)
                  }
                >
                  {entry.path}
                </button>
                {entry.deloProvenance && (
                  <span className="badge" title={entry.deloProvenance.nextAction ?? ""}>
                    delo:{entry.deloProvenance.outputType}
                  </span>
                )}
              </li>
            ))}
            {extraLibrary.length === 0 && <li className="empty">Zunanji vir je prazen.</li>}
          </ul>
        </>
      )}

      {loadError && <p className="status-error">{loadError}</p>}

      <form
        className="capture-form"
        onSubmit={(event) => {
          event.preventDefault();
          if (body.trim().length === 0) {
            return;
          }
          const trimmedTitle = title.trim();
          void onCapture({ ...(trimmedTitle.length > 0 ? { title: trimmedTitle } : {}), body }).then(() => {
            setTitle("");
            setBody("");
          });
        }}
      >
        <h3>Zajemi vhodni tekst</h3>
        <input
          type="text"
          placeholder="Naslov (neobvezno)"
          value={title}
          onChange={(event) => setTitle(event.target.value)}
        />
        <textarea
          placeholder="Vsebina"
          value={body}
          onChange={(event) => setBody(event.target.value)}
          rows={4}
        />
        <button type="submit" disabled={body.trim().length === 0}>
          Zajemi
        </button>
      </form>
    </section>
  );
}
