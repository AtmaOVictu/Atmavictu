"""Test helper: build a sandbox copy of the package with the living door."""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent          # nano4/
REPO = PKG.parent                                     # repo root
DOOR = REPO / "LICENSE-MANIFEST"


def make_sandbox():
    tmp = Path(tempfile.mkdtemp(prefix="nano4-sb-"))
    shutil.copytree(PKG, tmp / "nano4",
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    shutil.copy2(DOOR, tmp / "LICENSE-MANIFEST")
    return tmp


def run_validator(sandbox, *args):
    return subprocess.run(
        [sys.executable, "nano4/validate_package.py", *args],
        cwd=sandbox, capture_output=True, text=True)


def door_version():
    return json.loads(DOOR.read_text(encoding="utf-8")).get("version")


def checks(report):
    return {c["name"]: c["status"] for c in report["checks"]}


def fails(report):
    return [c for c in report["checks"] if c["status"] == "FAIL"]
