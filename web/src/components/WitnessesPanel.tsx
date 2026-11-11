/**
 * Plošča Priče — prikazuje stanje veneca jezikov (LICENSE-*.md witness-sloti).
 *
 * Brani le: hash istovetnosti proti LICENSE-MANIFEST, jezikovni kanon,
 * pregled (druga roka — trenutno "none", dokler ni vgrajena v register),
 * in dejanske priče iz DOKAZ / REGISTER-PADCEV.
 * Ne more mutirati ničesar: priče nikoli ne postanejo vrata (§0.33).
 */

import { useEffect, useState } from "react";

import { workbenchApi } from "../api";
import type { WreathReport, WreathReportRow, WreathVerification } from "../types";

interface Props {}

export function WitnessesPanel(_props: Props) {
  const [verify, setVerify] = useState<WreathVerification | null>(null);
  const [report, setReport] = useState<WreathReport | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function load() {
    try {
      const [verification, reported] = await Promise.all([
        workbenchApi.getWreathVerify(),
        workbenchApi.getWreathReport(),
      ]);
      setVerify(verification);
      setReport(reported);
    } catch {
      setError("Ni bilo mogoče naložiti priče veneca.");
    }
  }

  useEffect(() => {
    void load();
  }, []);

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
      {!report && !error && (
        <p className="empty">Naložim priče...</p>
      )}
    </section>
  );
}
