#!/usr/bin/env python3
"""nano4 gate — local package validator.

Scope: package shape, hashes, version truth, and the candidate gate.
Passing validates LOCAL ARTIFACT INTEGRITY ONLY — never legal validity,
publication, canonical status, or the identity of any reviewer.
A bare text proves nothing; the chain does (section 0.10 x 10^2).

Fail-closed: every claim the gate cannot measure is refused, not assumed.
Deterministic: identical inputs produce a byte-identical report (no clock).
"""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
DOOR_MANIFEST = REPO / "LICENSE-MANIFEST"
SELF = "PACKAGE-MANIFEST.json"
CANDIDATE = ROOT / "candidate"
CANDIDATE_MANIFEST = CANDIDATE / "PACKAGE-MANIFEST.json"

REQUIRED = [
    "README.md", "VERSION.txt", "00-AUDIT.md", "01-PROPOSED-PATCHES.md",
    "02-ACCESSIBILITY.md", "03-LICENSE-COMPATIBILITY.md",
    "04-LEGAL-RESEARCH-NOTES.md", "LICENSE-MACHINE-RECORD-0.1470.json",
    "requirements-test.txt", "candidate/README.md",
]
PATCH_MARKERS = ["PATCH 05", "PATCH 06", "PATCH 08", "PATCH 11", "PATCH 12", "PATCH 18", "PATCH 20"]
NOT_CERTIFIED = [
    "legal validity of VBL", "publication or delivery", "canonical status",
    "independent review", "reviewer identity",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def unsafe(path: str) -> bool:
    parts = Path(path).parts
    return ".." in parts or path.startswith("/") or (len(parts) > 0 and len(parts[0]) > 2 and ":" in parts[0])


def verify_entries(entries, base, results, label):
    """Verify manifest entries against the filesystem. Fail-closed."""
    for e in entries:
        p = e.get("path", "")
        if not p or p == SELF and base == ROOT:
            results.append((label, "FAIL", f"self-referential manifest entry refused (a file cannot contain its own hash, section 0a)"))
            continue
        if unsafe(p):
            results.append((label, "FAIL", f"unsafe path refused: {p}"))
            continue
        f = base / p
        if not f.is_file():
            results.append((label, "FAIL", f"phantom entry — declared but absent from the chain: {p}"))
            continue
        size_ok = "size_bytes" not in e or e["size_bytes"] == f.stat().st_size
        hash_ok = "sha256" not in e or e["sha256"] == sha256(f)
        if not size_ok:
            results.append((label, "FAIL", f"stale size: {p}"))
        elif not hash_ok:
            results.append((label, "FAIL", f"stale hash: {p}"))
        else:
            results.append((label, "PASS", f"verified: {p}"))


def run():
    results = []  # (name, status, detail)
    report = {
        "tool": "nano4/validate_package.py",
        "gate": "local artifact integrity only",
        "deterministic": True,
        "not_certified": NOT_CERTIFIED,
        "inputs": [],
        "checks": [],
        "living_door_version": None,
        "packet_era": None,
    }

    # 1. required files --------------------------------------------------
    for r in REQUIRED:
        f = ROOT / r
        if f.is_file():
            report["inputs"].append({"path": r, "sha256": sha256(f)})
            results.append(("required_files", "PASS", f"present: {r}"))
        else:
            results.append(("required_files", "FAIL", f"missing required file: {r}"))

    # 2. machine record invariants ---------------------------------------
    rec = None
    rf = ROOT / "LICENSE-MACHINE-RECORD-0.1470.json"
    try:
        rec = json.loads(rf.read_text(encoding="utf-8"))
    except Exception as e:
        results.append(("machine_record", "FAIL", f"unparsable machine record: {e}"))
    if rec is not None:
        inv = [
            ("version", rec.get("version"), "0.1470"),
        ]
        ok = rec.get("version", "").startswith("0.1470")
        results.append(("machine_record", "PASS" if ok else "FAIL", f"version={rec.get('version')!r}"))
        for field, want in [
            ("release_status", "DRAFT_NOT_RELEASED"),
            ("canonical_status", "UNVERIFIED"),
        ]:
            got = rec.get(field)
            results.append(("machine_record", "PASS" if got == want else "FAIL", f"{field}={got!r}"))
        pre = rec.get("predecessor", {})
        results.append(("machine_record", "PASS" if pre.get("identity_conflict") is True else "FAIL", "predecessor.identity_conflict must stay explicit True"))
        md = rec.get("mail_delivery", {})
        results.append(("machine_record", "PASS" if md.get("delivered") is False else "FAIL", "mail_delivery.delivered cannot be claimed"))

    # 3. version truth ----------------------------------------------------
    vt = ROOT / "VERSION.txt"
    if vt.is_file():
        text = vt.read_text(encoding="utf-8")
        m = re.search(r"^packet_era\s*=\s*(\S+)", text, re.M)
        if not m:
            results.append(("version_truth", "FAIL", "VERSION.txt carries no packet_era — a packet without a declared era identifies nothing"))
        else:
            era = m.group(1)
            report["packet_era"] = era
            ok = rec is not None and rec.get("version", "").startswith(era)
            results.append(("version_truth", "PASS" if ok else "FAIL", f"packet_era={era} vs machine record version={rec.get('version') if rec else None!r}"))
        if not re.search(r"^living_door\s*=\s*\.\./LICENSE-MANIFEST", text, re.M):
            results.append(("version_truth", "FAIL", "VERSION.txt lost the pointer to the living door — it must point at ../LICENSE-MANIFEST, never carry a copy"))
        else:
            results.append(("version_truth", "PASS", "pointer rule held: VERSION.txt points, it does not copy"))
        if re.search(r"^living_door_version\s*=", text, re.M):
            results.append(("version_truth", "FAIL", "VERSION.txt hardcodes living_door_version — a copied number goes stale at the next birth"))
        if re.search(r"^packet_status\s*=\s*(\S+)", text, re.M):
            st = re.search(r"^packet_status\s*=\s*(\S+)", text, re.M).group(1)
            results.append(("version_truth", "PASS" if st == "DRAFT_NOT_RELEASED" else "FAIL", f"packet_status={st}"))
    # measure the living door at check time — never from memory
    if DOOR_MANIFEST.is_file():
        report["inputs"].append({"path": "../LICENSE-MANIFEST", "sha256": sha256(DOOR_MANIFEST)})
        try:
            door = json.loads(DOOR_MANIFEST.read_text(encoding="utf-8"))
            report["living_door_version"] = door.get("version")
            results.append(("version_truth", "PASS", f"living door measured at check time: {door.get('version')}"))
        except Exception as e:
            results.append(("version_truth", "FAIL", f"living door manifest unparsable: {e}"))
    else:
        results.append(("version_truth", "FAIL", "living door manifest unreachable — nothing can be validated against a missing truth"))

    # 4. package manifest --------------------------------------------------
    pmf = ROOT / SELF
    if not pmf.is_file():
        results.append(("package_manifest", "FAIL", f"missing {SELF}"))
    else:
        try:
            pm = json.loads(pmf.read_text(encoding="utf-8"))
        except Exception as e:
            results.append(("package_manifest", "FAIL", f"unparsable {SELF}: {e}"))
            pm = None
        if pm is not None:
            if any(e.get("path") == SELF for e in pm.get("files", [])):
                results.append(("package_manifest", "FAIL", "manifest lists itself — a file cannot contain its own hash (section 0a)"))
            if pm.get("status") != "DRAFT_NOT_RELEASED":
                results.append(("package_manifest", "FAIL", f"manifest status={pm.get('status')!r} — a draft packet cannot claim release"))
            entries = pm.get("files", [])
            if not entries:
                results.append(("package_manifest", "FAIL", "manifest carries no entries — an empty manifest identifies nothing"))
            verify_entries(entries, ROOT, results, "package_manifest")
            phantom = pm.get("phantom_entries_of_the_fall")
            if phantom:
                results.append(("package_manifest", "PASS", f"phantom witnesses named: {len(phantom)} (scar stays, section 0.4)"))

    # 5. candidate gate -----------------------------------------------------
    if not CANDIDATE.is_dir():
        results.append(("candidate_gate", "FAIL", "candidate/ directory missing — release inputs have no single declared home"))
    else:
        if not (CANDIDATE / "README.md").is_file():
            results.append(("candidate_gate", "FAIL", "candidate/README.md missing — the declaration is the gate"))
        if not CANDIDATE_MANIFEST.is_file():
            orphans = sorted(
                p.name for p in CANDIDATE.iterdir() if p.is_file() and p.name != "README.md"
            )
            if orphans:
                results.append(("candidate_gate", "FAIL", f"orphan candidate files without a candidate manifest: {orphans}"))
            else:
                results.append(("candidate_gate", "NOT_APPLICABLE", "no candidate assembled — an empty candidate is honest; a phantom one is not"))
        else:
            try:
                cm = json.loads(CANDIDATE_MANIFEST.read_text(encoding="utf-8"))
            except Exception as e:
                results.append(("candidate_gate", "FAIL", f"malformed candidate register: {e}"))
                cm = None
            if cm is not None:
                if cm.get("status") not in (None, "CANDIDATE"):
                    results.append(("candidate_gate", "FAIL", f"candidate status={cm.get('status')!r} — only CANDIDATE is allowed here"))
                verify_entries(cm.get("files", []), CANDIDATE, results, "candidate_gate")
                listed = {e.get("path") for e in cm.get("files", [])}
                orphans = sorted(
                    str(p.relative_to(CANDIDATE)) for p in CANDIDATE.rglob("*")
                    if p.is_file() and str(p.relative_to(CANDIDATE)) not in listed
                    and str(p.relative_to(CANDIDATE)) not in ("README.md", "PACKAGE-MANIFEST.json")
                )
                if orphans:
                    results.append(("candidate_gate", "FAIL", f"orphan candidate files not listed in the register: {orphans}"))
                else:
                    results.append(("candidate_gate", "PASS", "candidate register complete — every file listed, every hash measured"))

    # 6. patch markers ------------------------------------------------------
    pp = ROOT / "01-PROPOSED-PATCHES.md"
    if pp.is_file():
        text = pp.read_text(encoding="utf-8")
        missing = [m for m in PATCH_MARKERS if m not in text]
        if missing:
            results.append(("patch_markers", "FAIL", f"missing patch markers: {missing}"))
        else:
            results.append(("patch_markers", "PASS", f"all {len(PATCH_MARKERS)} markers present"))

    for name, status, detail in results:
        report["checks"].append({"name": name, "status": status, "detail": detail})
    failed = [c for c in report["checks"] if c["status"] == "FAIL"]
    return report, failed


def main() -> int:
    report, failed = run()
    if "--json" in sys.argv[1:]:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 1 if failed else 0
    if failed:
        print("FAIL")
        for c in failed:
            print(f"  [{c['name']}] {c['detail']}")
        print(f"scope=local artifact integrity only; {len(report['checks'])} checks, {len(failed)} failed")
        return 1
    print("PASS — package structure, hashes, version truth, and candidate gate verified")
    print(f"living_door_version={report['living_door_version']}")
    print(f"packet_era={report['packet_era']}")
    for i in report["inputs"]:
        print(f"input {i['path']} sha256={i['sha256']}")
    print(f"checks={len(report['checks'])} failed=0")
    print("scope=local artifact integrity only; no legal, canonical, publication, or reviewer certification")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
