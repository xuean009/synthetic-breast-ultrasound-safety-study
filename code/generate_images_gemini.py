#!/usr/bin/env python3
"""Generate images with Nano Banana Pro through Google's official Gemini API.

The request sends only the model identifier and prompt content. Authentication
is read from GEMINI_API_KEY. No temperature, resolution, aspect ratio, seed, or
other generation parameter is supplied.
"""

from __future__ import annotations

import argparse
import base64
import csv
import os
import time
from pathlib import Path

import requests


MODEL = "gemini-3-pro-image"
API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-3-pro-image:generateContent"
MIME_EXTENSIONS = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}


def read_prompts(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required = {"synthetic_id", "generation_prompt"}
    if not rows or not required.issubset(rows[0]):
        raise RuntimeError(f"Prompt file must contain {sorted(required)}.")
    return rows


def request_image(
    session: requests.Session,
    api_key: str,
    prompt: str,
    timeout: int,
) -> tuple[bytes, str]:
    response = session.post(
        API_URL,
        headers={
            "x-goog-api-key": api_key,
            "Content-Type": "application/json",
        },
        json={
            "contents": [
                {
                    "parts": [{"text": prompt}],
                }
            ]
        },
        timeout=timeout,
    )
    response.raise_for_status()
    body = response.json()
    for candidate in body.get("candidates", []):
        for part in candidate.get("content", {}).get("parts", []):
            inline = part.get("inlineData") or part.get("inline_data")
            if inline and inline.get("data"):
                mime = inline.get("mimeType") or inline.get("mime_type")
                return base64.b64decode(inline["data"]), mime or "image/png"
    raise RuntimeError("The Gemini response did not contain image data.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompts", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--delay", type=float, default=1.0)
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Set GEMINI_API_KEY before running this script.")

    rows = read_prompts(args.prompts)
    if args.limit is not None:
        rows = rows[: args.limit]
    args.output_dir.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    for index, row in enumerate(rows, start=1):
        image_bytes, mime = request_image(
            session,
            api_key,
            row["generation_prompt"],
            args.timeout,
        )
        suffix = MIME_EXTENSIONS.get(mime, ".bin")
        output = args.output_dir / f"{row['synthetic_id']}{suffix}"
        output.write_bytes(image_bytes)
        print(f"[{index}/{len(rows)}] {output.name}")
        if index < len(rows):
            time.sleep(args.delay)


if __name__ == "__main__":
    main()
