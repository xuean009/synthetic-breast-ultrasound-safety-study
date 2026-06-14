#!/usr/bin/env python3
"""Package or verify the public synthetic breast ultrasound image archive."""

from __future__ import annotations

import argparse
import csv
import hashlib
import tempfile
import zipfile
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_manifest(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 300:
        raise RuntimeError(f"Expected 300 manifest rows, found {len(rows)}.")
    if len({row["filename"] for row in rows}) != 300:
        raise RuntimeError("Manifest filenames are not unique.")
    return rows


def verify_directory(image_dir: Path, rows: list[dict[str, str]]) -> None:
    expected = {row["filename"] for row in rows}
    observed = {path.name for path in image_dir.iterdir() if path.is_file()}
    if expected != observed:
        raise RuntimeError(
            f"Image set mismatch. Missing={sorted(expected-observed)[:10]}, "
            f"extra={sorted(observed-expected)[:10]}"
        )
    for row in rows:
        path = image_dir / row["filename"]
        if sha256(path) != row["sha256"]:
            raise RuntimeError(f"Checksum mismatch: {row['filename']}")
        if path.stat().st_size != int(row["bytes"]):
            raise RuntimeError(f"File-size mismatch: {row['filename']}")


def create_archive(image_dir: Path, manifest: Path, output: Path) -> None:
    rows = read_manifest(manifest)
    verify_directory(image_dir, rows)
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for row in rows:
            archive.write(image_dir / row["filename"], f"images/{row['filename']}")
    print(f"Created {output} with {len(rows)} verified images.")


def verify_archive(archive_path: Path, manifest: Path) -> None:
    rows = read_manifest(manifest)
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        with zipfile.ZipFile(archive_path) as archive:
            archive.extractall(root)
        verify_directory(root / "images", rows)
    print(f"Verified {archive_path} against {len(rows)} manifest rows.")


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    create = subparsers.add_parser("create")
    create.add_argument("--image-dir", type=Path, required=True)
    create.add_argument("--manifest", type=Path, required=True)
    create.add_argument("--output", type=Path, required=True)

    verify = subparsers.add_parser("verify")
    verify.add_argument("--archive", type=Path, required=True)
    verify.add_argument("--manifest", type=Path, required=True)

    args = parser.parse_args()
    if args.command == "create":
        create_archive(args.image_dir, args.manifest, args.output)
    else:
        verify_archive(args.archive, args.manifest)


if __name__ == "__main__":
    main()

