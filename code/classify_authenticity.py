#!/usr/bin/env python3
"""Run the fixed authenticity prompt through an OpenAI-compatible endpoint.

Credentials and endpoint details are read only from environment variables:
AI_API_KEY, AI_API_URL, and AI_MODEL. The request reproduces the historical
settings: temperature 0, max_tokens 512, and high image detail.
"""

from __future__ import annotations

import argparse
import base64
import csv
import json
import mimetypes
import os
import re
from pathlib import Path

import requests


def load_prompts(path: Path, phase: str) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8")
    pattern = rf"\[PHASE {re.escape(phase)} SYSTEM\]\n(.*?)\n\[PHASE {re.escape(phase)} USER\]\n(.*?)(?=\n\[PHASE|\Z)"
    match = re.search(pattern, text, flags=re.DOTALL)
    if not match:
        raise RuntimeError(f"Phase {phase} prompts were not found in {path}.")
    return match.group(1).strip(), match.group(2).strip()


def data_url(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "image/jpeg"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def parse_response(text: str) -> dict:
    cleaned = re.sub(r"^```(?:json)?\s*", "", text.strip())
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return json.loads(cleaned)


def classify(
    session: requests.Session,
    api_url: str,
    model: str,
    system_prompt: str,
    user_prompt: str,
    image_path: Path,
) -> dict:
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": data_url(image_path),
                            "detail": "high",
                        },
                    },
                    {"type": "text", "text": user_prompt},
                ],
            },
        ],
        "temperature": 0,
        "max_tokens": 512,
    }
    response = session.post(api_url, json=payload, timeout=180)
    response.raise_for_status()
    body = response.json()
    result = parse_response(body["choices"][0]["message"]["content"])
    result["filename"] = image_path.name
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image-dir", type=Path, required=True)
    parser.add_argument("--prompts", type=Path, required=True)
    parser.add_argument("--phase", choices=("2", "3"), required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    api_key = os.environ.get("AI_API_KEY")
    api_url = os.environ.get("AI_API_URL")
    model = os.environ.get("AI_MODEL")
    if not all((api_key, api_url, model)):
        raise RuntimeError("Set AI_API_KEY, AI_API_URL, and AI_MODEL.")

    system_prompt, user_prompt = load_prompts(args.prompts, args.phase)
    session = requests.Session()
    session.headers.update(
        {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    )
    rows = []
    for image_path in sorted(args.image_dir.iterdir()):
        if image_path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
            continue
        rows.append(
            classify(
                session,
                api_url,
                model,
                system_prompt,
                user_prompt,
                image_path,
            )
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fields = sorted({key for row in rows for key in row})
    with args.output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} classifications to {args.output}.")


if __name__ == "__main__":
    main()
