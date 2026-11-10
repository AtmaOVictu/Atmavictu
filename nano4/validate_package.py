#!/usr/bin/env python3
"""Local package validator. Passing validates package shape and hashes only."""
from pathlib import Path
import hashlib, json, sys

ROOT = Path(__file__).resolve().parent
REQUIRED = [
    ROOT / "README.md", ROOT / "00-AUDIT.md", ROOT / "01-PROPOSED-PATCHES.md",
    ROOT / "02-ACCESSIBILITY.md", ROOT / "03-LICENSE-COMPATIBILITY.md",
    ROOT / "schemas/event.schema.json", ROOT / "schemas/LICENSE-MACHINE-RECORD-0.1470.json",
    ROOT / "schemas/LICENSE-MANIFEST.template.json", ROOT / "schemas/event.example.UNVERIFIED.json",
    ROOT / "04-LEGAL-RESEARCH-NOTES.md", ROOT / "requirements-test.txt", ROOT / "source/Pasted-markdown-attachment-tail.md",
]

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def main() -> int:
    errors = []
    for p in REQUIRED:
        if not p.is_file(): errors.append(f"missing required file: {p.relative_to(ROOT)}")
    if errors:
        print("FAIL")
        print("\n".join(errors))
        return 1
    try:
        event = json.loads((ROOT/"schemas/event.schema.json").read_text(encoding="utf-8"))
        record = json.loads((ROOT/"schemas/LICENSE-MACHINE-RECORD-0.1470.json").read_text(encoding="utf-8"))
        manifest = json.loads((ROOT/"schemas/LICENSE-MANIFEST.template.json").read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAIL: invalid JSON: {e}")
        return 1
    if event.get("$schema") != "https://json-schema.org/draft/2020-12/schema": errors.append("event schema draft mismatch")
    if event.get("$id") != "urn:vbl:event:1.0.0": errors.append("event schema id mismatch")
    if record.get("version") != "0.1470 × 10⁴": errors.append("machine record version mismatch")
    if record.get("release_status") != "DRAFT_NOT_RELEASED": errors.append("release status must remain draft")
    if record.get("canonical_status") != "UNVERIFIED": errors.append("canonical status must remain UNVERIFIED")
    if record.get("predecessor", {}).get("identity_conflict") is not True: errors.append("source identity conflict must remain explicit")
    if record.get("mail_delivery", {}).get("delivered") is not False: errors.append("mail delivery cannot be claimed")
    if manifest.get("generated_from_exact_final_bytes") is not False: errors.append("manifest template must not claim final-byte generation")
    if manifest.get("entries") != []: errors.append("manifest template must not invent file entries")
    src = ROOT/"source/Pasted-markdown-attachment-tail.md"
    observed = sha256(src)
    if observed != record.get("source_attachment", {}).get("sha256"): errors.append("source attachment hash mismatch")
    if src.stat().st_size != record.get("source_attachment", {}).get("size_bytes"): errors.append("source attachment size mismatch")
    patch = (ROOT/"01-PROPOSED-PATCHES.md").read_text(encoding="utf-8")
    for marker in ["PATCH 05", "PATCH 06", "PATCH 08", "PATCH 11", "PATCH 12", "PATCH 18", "PATCH 20"]:
        if marker not in patch: errors.append(f"missing patch marker: {marker}")
    if errors:
        print("FAIL")
        print("\n".join(errors))
        return 1
    print("PASS — package structure and declared source hash verified")
    print(f"source_bytes={src.stat().st_size}")
    print(f"source_sha256={observed}")
    print("scope=local artifact integrity only; no legal, canonical, repository, or independent-review certification")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
