import argparse
import base64
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


API_URL = "https://api.openai.com/v1/images/generations"


def slugify(value: str, max_len: int = 60) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "_", value).strip("_")
    if not value:
        return "image"
    return value[:max_len]


def load_payload(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_payload(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def openai_generate_image_b64(
    *,
    api_key: str,
    prompt: str,
    model: str,
    size: str,
    quality: str,
    background: str,
) -> str:
    body = {
        "model": model,
        "prompt": prompt,
        "size": size,
        "quality": quality,
        "background": background,
        "n": 1,
    }
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=data,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenAI Images API HTTP {e.code}: {detail}") from e
    except Exception as e:
        raise RuntimeError(f"OpenAI Images API request failed: {e}") from e

    data_items = payload.get("data")
    if not isinstance(data_items, list) or not data_items:
        raise RuntimeError(f"Unexpected Images API response: missing data[]. Got keys={list(payload)}")

    first = data_items[0]
    b64 = first.get("b64_json")
    if not isinstance(b64, str) or not b64.strip():
        raise RuntimeError("Unexpected Images API response: missing data[0].b64_json")
    return b64


def build_prompt(*, lo_title: str, content_title: str, key_facts: str) -> str:
    excerpt = re.sub(r"\s+", " ", (key_facts or "").strip())
    excerpt = excerpt[:1200]

    return "\n".join(
        [
            "Create a clean, instructional diagram or simple illustration for trainees.",
            f"Learning outcome context: {lo_title}",
            f"Specific content focus: {content_title}",
            "",
            "Constraints:",
            "- White or light background; no watermarks; no logos; no branding.",
            "- Prefer diagram/infographic style over photorealism.",
            "- Use minimal labels (3–6) only if they improve clarity; keep text short.",
            "- Keep it accurate and aligned to the specific content focus.",
            "",
            "Reference (excerpt from Key Facts):",
            excerpt,
        ]
    )


def iter_contents(payload: dict):
    unit = payload.get("current_unit") or {}
    unit_index = unit.get("index")
    learning_outcomes = unit.get("learning_outcomes") or []
    for lo in learning_outcomes:
        lo_index = lo.get("index")
        lo_title = lo.get("title", "")
        for content in lo.get("contents") or []:
            yield unit_index, lo_index, lo_title, content


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate 1 instructional image per content item (Key Facts) using OpenAI Images API, and write image paths back into a payload JSON."
    )
    parser.add_argument("payload_json", type=Path)
    parser.add_argument("--outdir", type=Path, default=Path("state/images"))
    parser.add_argument("--model", default="gpt-image-1")
    parser.add_argument("--size", default="1024x1024")
    parser.add_argument("--quality", default="medium")
    parser.add_argument("--background", default="opaque")
    parser.add_argument("--force", action="store_true", help="Regenerate even if key_facts_image_path is already set.")
    parser.add_argument("--inplace", action="store_true", help="Overwrite the input payload JSON instead of writing a copy.")
    parser.add_argument("--sleep-s", type=float, default=0.0, help="Optional delay between calls (rate limit friendliness).")
    args = parser.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Missing OPENAI_API_KEY environment variable.", file=sys.stderr)
        return 2

    payload_path: Path = args.payload_json
    payload = load_payload(payload_path)

    unit = payload.get("current_unit") or {}
    unit_index = unit.get("index", "X")
    unit_title = slugify(str(unit.get("unit_of_competency") or f"Unit_{unit_index}"))
    outdir = args.outdir / f"{unit_index}_{unit_title}"
    outdir.mkdir(parents=True, exist_ok=True)

    generated = 0
    skipped = 0

    for unit_idx, lo_idx, lo_title, content in iter_contents(payload):
        if not isinstance(content, dict):
            continue

        existing = content.get("key_facts_image_path")
        if existing and not args.force:
            skipped += 1
            continue

        content_index = content.get("index", "Z")
        content_title = str(content.get("title") or f"Content_{content_index}")
        key_facts = str(content.get("key_facts") or "")

        prompt = build_prompt(lo_title=str(lo_title or ""), content_title=content_title, key_facts=key_facts)
        b64 = openai_generate_image_b64(
            api_key=api_key,
            prompt=prompt,
            model=args.model,
            size=args.size,
            quality=args.quality,
            background=args.background,
        )

        image_bytes = base64.b64decode(b64)
        filename = f"UC{unit_idx}_LO{lo_idx}_C{content_index}_{slugify(content_title)}.png"
        image_path = outdir / filename
        image_path.write_bytes(image_bytes)

        content["key_facts_image_path"] = os.path.relpath(image_path, start=payload_path.parent)
        content["key_facts_image_caption"] = f"Figure {unit_idx}.{lo_idx}-{content_index} — {content_title}"
        content["key_facts_image_prompt"] = prompt

        generated += 1
        if args.sleep_s > 0:
            time.sleep(args.sleep_s)

    if args.inplace:
        out_payload_path = payload_path
    else:
        out_payload_path = payload_path.with_name(payload_path.stem + "_with_images.json")

    save_payload(out_payload_path, payload)
    print(f"Wrote: {out_payload_path}")
    print(f"Images generated: {generated}; skipped: {skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

