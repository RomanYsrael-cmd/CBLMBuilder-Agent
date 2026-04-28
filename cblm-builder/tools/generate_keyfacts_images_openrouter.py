import argparse
import base64
import io
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image


API_URL = "https://openrouter.ai/api/v1/chat/completions"


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


def parse_data_url(data_url: str) -> tuple[str, bytes]:
    """
    Returns (file_ext, bytes).
    Supports: data:image/png;base64,....
    """
    if not data_url.startswith("data:"):
        raise ValueError("Expected a data: URL")
    header, b64 = data_url.split(",", 1)
    mime = header[5:].split(";", 1)[0].strip().lower()
    if ";base64" not in header.lower():
        raise ValueError("Expected base64-encoded data URL")

    ext = "png"
    if mime == "image/jpeg":
        ext = "jpg"
    elif mime == "image/webp":
        ext = "webp"
    elif mime == "image/png":
        ext = "png"

    return ext, base64.b64decode(b64)


def normalize_image_bytes_to_png(image_bytes: bytes) -> bytes:
    """
    Ensure the returned bytes are a real PNG image (python-docx does not support WEBP).
    """
    with Image.open(io.BytesIO(image_bytes)) as im:
        im.load()
        out = io.BytesIO()
        if im.mode in ("RGBA", "LA"):
            im.save(out, format="PNG")
        else:
            im.convert("RGB").save(out, format="PNG")
        return out.getvalue()


def openrouter_chat_generate_image_data_url(
    *,
    api_key: str,
    model: str,
    prompt: str,
    modalities: list[str],
    aspect_ratio: str | None,
    image_size: str | None,
    http_referer: str | None,
    x_title: str | None,
) -> str:
    body: dict = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "modalities": modalities,
        "stream": False,
    }
    if aspect_ratio or image_size:
        body["image_config"] = {}
        if aspect_ratio:
            body["image_config"]["aspect_ratio"] = aspect_ratio
        if image_size:
            body["image_config"]["image_size"] = image_size

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    if http_referer:
        headers["HTTP-Referer"] = http_referer
    if x_title:
        headers["X-Title"] = x_title

    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(API_URL, data=data, method="POST", headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            raw = resp.read()
            text = raw.decode("utf-8", errors="replace")
            try:
                payload = json.loads(text)
            except json.JSONDecodeError as e:
                snippet = text[:800].replace("\r", "\\r")
                raise RuntimeError(
                    "OpenRouter returned a non-JSON response. "
                    f"bytes={len(raw)}; snippet={snippet!r}"
                ) from e
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenRouter HTTP {e.code}: {detail}") from e
    except Exception as e:
        raise RuntimeError(f"OpenRouter request failed: {e}") from e

    choices = payload.get("choices")
    if not isinstance(choices, list) or not choices:
        raise RuntimeError(f"Unexpected OpenRouter response: missing choices[]. Got keys={list(payload)}")

    message = (choices[0] or {}).get("message") or {}
    images = message.get("images")
    if not isinstance(images, list) or not images:
        raise RuntimeError("Unexpected OpenRouter response: missing choices[0].message.images[]")

    first = images[0] or {}
    image_url = first.get("image_url") or first.get("imageUrl") or {}
    url = image_url.get("url")
    if not isinstance(url, str) or not url.strip():
        raise RuntimeError("Unexpected OpenRouter response: missing images[0].image_url.url")
    return url


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
            "- Use minimal labels (3-6) only if they improve clarity; keep text short.",
            "- Keep it accurate and aligned to the specific content focus.",
            "",
            "Reference (excerpt from Key Facts):",
            excerpt,
        ]
    )


def is_transient_openrouter_error(message: str) -> bool:
    text = (message or "").lower()
    transient_markers = [
        "winerror 10054",
        "timed out",
        "timeout",
        "temporarily unavailable",
        "service unavailable",
        "bad gateway",
        "gateway timeout",
        "connection reset",
        "connection aborted",
        "connection refused",
        "remote host",
        "429",
        "rate limit",
    ]
    return any(marker in text for marker in transient_markers)


def openrouter_chat_generate_image_data_url_with_retries(
    *,
    retries: int,
    retry_sleep_s: float,
    **kwargs,
) -> str:
    last_exc: Exception | None = None
    attempts = max(1, int(retries) + 1)
    for attempt in range(1, attempts + 1):
        try:
            return openrouter_chat_generate_image_data_url(**kwargs)
        except Exception as e:
            last_exc = e
            if attempt >= attempts or not is_transient_openrouter_error(str(e)):
                raise
            sleep_s = float(retry_sleep_s) * attempt
            if sleep_s > 0:
                time.sleep(sleep_s)
    raise RuntimeError(f"OpenRouter failed after {attempts} attempts") from last_exc


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
        description="Generate 1 instructional image per content item (Key Facts) using OpenRouter image generation models, and write image paths back into a payload JSON."
    )
    parser.add_argument("payload_json", type=Path)
    parser.add_argument("--outdir", type=Path, default=Path("state/images"))
    parser.add_argument("--model", default=os.environ.get("OPENROUTER_IMAGE_MODEL") or "sourceful/riverflow-v2-max-preview")
    parser.add_argument(
        "--aspect-ratio",
        dest="aspect_ratio",
        default=os.environ.get("OPENROUTER_IMAGE_ASPECT_RATIO") or None,
        help='e.g. "1:1", "16:9" (if supported)',
    )
    parser.add_argument(
        "--image-size",
        dest="image_size",
        default=os.environ.get("OPENROUTER_IMAGE_SIZE") or "1K",
        help='e.g. "1K", "2K", "4K" (if supported)',
    )
    parser.add_argument(
        "--modalities",
        default=os.environ.get("OPENROUTER_IMAGE_MODALITIES") or "image",
        help='Comma-separated list; for image-only models use "image" (default).',
    )
    parser.add_argument("--force", action="store_true", help="Regenerate even if key_facts_image_path is already set.")
    parser.add_argument("--inplace", action="store_true", help="Overwrite the input payload JSON instead of writing a copy.")
    parser.add_argument(
        "--max-images",
        type=int,
        default=0,
        help="Generate at most this many new images in this run (0 = no limit). Useful for time-boxed runs.",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=int(os.environ.get("OPENROUTER_RETRIES") or 2),
        help="Retry count for transient OpenRouter/network errors (default: env OPENROUTER_RETRIES or 2).",
    )
    parser.add_argument(
        "--retry-sleep-s",
        type=float,
        default=float(os.environ.get("OPENROUTER_RETRY_SLEEP_S") or 3.0),
        help="Base sleep between retries; multiplied by attempt number (default: env OPENROUTER_RETRY_SLEEP_S or 3.0).",
    )
    parser.add_argument("--sleep-s", type=float, default=0.0, help="Optional delay between calls (rate limit friendliness).")
    parser.add_argument("--http-referer", default=os.environ.get("OPENROUTER_HTTP_REFERER"))
    parser.add_argument("--x-title", default=os.environ.get("OPENROUTER_X_TITLE"))
    args = parser.parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("Missing OPENROUTER_API_KEY environment variable.", file=sys.stderr)
        return 2

    payload_path: Path = args.payload_json
    payload = load_payload(payload_path)

    if args.inplace:
        out_payload_path = payload_path
    else:
        out_payload_path = payload_path.with_name(payload_path.stem + "_with_images.json")

    unit = payload.get("current_unit") or {}
    unit_index = unit.get("index", "X")
    unit_title = slugify(str(unit.get("unit_of_competency") or f"Unit_{unit_index}"))
    outdir = args.outdir / f"{unit_index}_{unit_title}"
    outdir.mkdir(parents=True, exist_ok=True)

    modalities = [m.strip() for m in str(args.modalities).split(",") if m.strip()]
    if not modalities:
        modalities = ["image"]

    generated = 0
    skipped = 0

    try:
        for unit_idx, lo_idx, lo_title, content in iter_contents(payload):
            if not isinstance(content, dict):
                continue

            existing = content.get("key_facts_image_path")
            if existing and not args.force:
                skipped += 1
                continue

            if args.max_images and generated >= args.max_images:
                break

            content_index = content.get("index", "Z")
            content_title = str(content.get("title") or f"Content_{content_index}")
            key_facts = str(content.get("key_facts") or "")

            prompt = build_prompt(lo_title=str(lo_title or ""), content_title=content_title, key_facts=key_facts)
            data_url = openrouter_chat_generate_image_data_url_with_retries(
                retries=args.retries,
                retry_sleep_s=args.retry_sleep_s,
                api_key=api_key,
                model=args.model,
                prompt=prompt,
                modalities=modalities,
                aspect_ratio=args.aspect_ratio,
                image_size=args.image_size,
                http_referer=args.http_referer,
                x_title=args.x_title,
            )
            ext, image_bytes = parse_data_url(data_url)
            try:
                image_bytes = normalize_image_bytes_to_png(image_bytes)
                ext = "png"
            except Exception:
                # If Pillow can't decode the bytes, fall back to raw bytes and extension from the data URL.
                pass

            filename = f"UC{unit_idx}_LO{lo_idx}_C{content_index}_{slugify(content_title)}.{ext}"
            image_path = outdir / filename
            image_path.write_bytes(image_bytes)

            content["key_facts_image_path"] = os.path.relpath(image_path, start=payload_path.parent)
            content["key_facts_image_caption"] = f"Figure {unit_idx}.{lo_idx}-{content_index} - {content_title}"
            content["key_facts_image_prompt"] = prompt
            content["key_facts_image_model"] = args.model

            generated += 1
            save_payload(out_payload_path, payload)
            print(f"Wrote: {out_payload_path} (generated {generated}, skipped {skipped})")

            if args.sleep_s > 0:
                time.sleep(args.sleep_s)
    except KeyboardInterrupt:
        save_payload(out_payload_path, payload)
        print(f"Interrupted. Wrote: {out_payload_path}")
        print(f"Images generated: {generated}; skipped: {skipped}")
        return 130
    except Exception as e:
        save_payload(out_payload_path, payload)
        print(f"Error. Wrote partial progress: {out_payload_path}", file=sys.stderr)
        print(str(e), file=sys.stderr)
        return 2

    save_payload(out_payload_path, payload)
    print(f"Wrote: {out_payload_path}")
    print(f"Images generated: {generated}; skipped: {skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
