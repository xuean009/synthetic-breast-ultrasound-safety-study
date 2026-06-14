#!/usr/bin/env python3
"""Validate repository scope, metadata integrity, and accidental secrets."""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path


FORBIDDEN_SUFFIXES = {".docx", ".xlsx", ".xls", ".pdf", ".zip", ".dcm"}
FORBIDDEN_NAMES = ("survey", "questionnaire", "manuscript", "cover_letter")
SECRET_PATTERNS = (
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\bgh[oprsu]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"(?i)(api[_-]?key|authorization)\s*=\s*[\"'][^\"']{16,}[\"']"),
)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    failures = []
    files = [path for path in root.rglob("*") if path.is_file() and ".git" not in path.parts]
    for path in files:
        relative = path.relative_to(root).as_posix()
        lower = relative.lower()
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            failures.append(f"Forbidden file type: {relative}")
        if any(name in lower for name in FORBIDDEN_NAMES):
            failures.append(f"Forbidden filename: {relative}")
        if path.suffix.lower() in {".md", ".txt", ".py", ".csv", ".cff", ""}:
            text = path.read_text(encoding="utf-8-sig", errors="ignore")
            for pattern in SECRET_PATTERNS:
                if pattern.search(text):
                    failures.append(f"Potential secret: {relative}")

    manifest_path = root / "metadata" / "synthetic_image_manifest.csv"
    with manifest_path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required = {
        "synthetic_id",
        "filename",
        "target_birads",
        "generation_prompt",
        "sha256",
        "bytes",
    }
    if len(rows) != 300:
        failures.append(f"Expected 300 metadata rows, found {len(rows)}")
    if set(rows[0]) != required:
        failures.append(f"Unexpected metadata fields: {set(rows[0])}")
    if len({row["filename"] for row in rows}) != 300:
        failures.append("Filenames are not unique")
    if any(not re.fullmatch(r"[0-9a-f]{64}", row["sha256"]) for row in rows):
        failures.append("Invalid SHA-256 value")

    if failures:
        print("\n".join(f"FAIL: {item}" for item in failures))
        raise SystemExit(1)
    print(f"PASS: {len(files)} files checked; 300 synthetic records validated.")


if __name__ == "__main__":
    main()

