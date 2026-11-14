/**
 * Plošča Priče — prikazuje stanje veneca jezikov (LICENSE-*.md witness-sloti).
 *
 * Brani le: hash istovetnosti proti LICENSE-MANIFEST, jezikovni kanon,
 * pregled (druga roka), in dejanske priče iz DOKAZ / REGISTER-PADCEV.
 * Ne more mutirati ničesar: priče nikoli ne postanejo vrata (§0.33).
 */

import { useCallback, useEffect, useState } from "react";

import { tauriApi, workbenchApi } from "../api";
import type { WreathReport, WreathVerification } from "../types";
import type { WreathDriftResult } from "../types";

interface Props {
  projectRoot: string | null;
}

export function WitnessesPanel({ projectRoot }: Props) {
  const [verify, setVerify] = useState<WreathVerification | null>(null);
  const [report, setReport] = useState<WreathReport | null>(null);
  const [drift, setDrift] = useState<WreathDriftResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function load() {
    try {
      if (projectRoot) {
        const [verification, reported, driftResult] = await Promise.all([
          tauriApi.verifyWreath(projectRoot),
          workbenchApi.getWreathReport(),
          tauriApi.detectDrift(projectRoot),
        ]);
        setVerify(verification);
        setReport(reported);
        setDrift(driftResult);
      } else {
        const [verification, reported] = await Promise.all([
          workbenchApi.getWreathVerify(),
          workbenchApi.getWreathReport(),
        ]);
        setVerify(verification);
        setReport(reported);
      }
    } catch {
      setError("Ni bilo mogoče naložiti priče veneca.");
    }
  }

  useEffect(() => {
    void load();
  }, [projectRoot]);

  if (error) {
    return (
      <section className="pane">
        <h2>Priče</h2>
        <p className="status-error">{error}</p>
      </section>
    );
  }

  const statusClass =
    verify?.status === "PASS"
      ? "status-ok"
      : verify?.status === "FAIL"
        ? "status-fail"
        : "status-warn";

  const driftClass = drift?.drift ? "status-fail" : "status-ok";

  return (
    <section className="pane">
      <h2>Priče veneca</h2>
      {verify && (
        <div className="summary">
          <span>slotov: {verify.total}</span>
          <span>ujemajočih: {verify.matched}</span>
          <span className={statusClass}>
            {`WREATH VERIFY: ${verify.status}`}
          </span>
          {report && (
            <>
              <span>dejanske priče: {report.deedCount}</span>
              <span>
                živa vrata: {report.livingDoor ? "prisotne" : "odsotne"}
              </span>
            </>
          )}
        </div>
      )}
      {drift && (
        <div className="summary">
          <span className={driftClass}>
            {drift.drift ? "WREATH DRIFT: DETECTED" : "WREATH DRIFT: none"}
          </span>
          {drift.details.length > 0 && (
            <ul className="drift-details">
              {drift.details.map((d: string, i: number) => (
                <li key={i}>{d}</li>
              ))}
            </ul>
          )}
        </div>
      )}
      {report && report.rows.length > 0 && (
        <table className="witness-table">
          <thead>
            <tr>
              <th>jezik</th>
              <th>ime</th>
              <th>slot</th>
              <th>kanon</th>
              <th>hash</th>
              <th>pregled</th>
              <th>dejanje</th>
            </tr>
          </thead>
          <tbody>
            {report.rows.map((row) => (
              <tr key={row.slot}>
                <td>{row.code}</td>
                <td>{row.language}</td>
                <td>{row.slot}</td>
                <td>{row.canon}</td>
                <td className={row.matched ? "status-ok" : "status-fail"}>
                  {row.hash}
                </td>
                <td>{row.review}</td>
                <td>{row.deed}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      {!report && projectRoot && <p className="empty">Detailed wreath report is available in server mode.</p>}
      {!report && !error && !projectRoot && (
        <p className="empty">Izberi projektno mapo za pregled priče.</p>
      )}
    </section>
  );
}
