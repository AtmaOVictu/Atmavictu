import type { ManifestValidationResult, WorkbenchManifest } from "../types";

interface Props {
  manifest: WorkbenchManifest | null;
  verify: ManifestValidationResult | null;
  error: string | null;
}

export function ManifestStatusBar({ manifest, verify, error }: Props) {
  return (
    <header className="status-bar">
      <strong>ATMAVICTU WORKBENCH</strong>
      {manifest && (
        <span>
          incoming: {manifest.incomingTexts.length} · fragments: {manifest.fragments.length} · insertions:{" "}
          {manifest.insertions.length}
        </span>
      )}
      {verify && (
        <span className={verify.isValid ? "status-ok" : "status-fail"}>
          VERIFY: {verify.isValid ? "PASS" : `FAIL (${verify.errors.length})`}
        </span>
      )}
      {error && <span className="status-error">{error}</span>}
    </header>
  );
}
