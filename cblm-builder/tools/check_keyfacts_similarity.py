import json
import re
import sys
from itertools import combinations
from pathlib import Path


def normalize(text: str) -> list[str]:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return [token for token in text.split() if token]


def shingles(tokens: list[str], size: int = 5) -> set[str]:
    if not tokens:
        return set()
    if len(tokens) < size:
        return {" ".join(tokens)}
    return {" ".join(tokens[i : i + size]) for i in range(len(tokens) - size + 1)}


def jaccard(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def extract_structured_sections(payload: dict) -> dict[str, str]:
    sections: dict[str, str] = {}
    current_unit = payload.get("current_unit")
    if not isinstance(current_unit, dict):
        return sections

    learning_outcomes = current_unit.get("learning_outcomes")
    if not isinstance(learning_outcomes, list):
        return sections

    unit_index = current_unit.get("index", "X")
    for lo_position, lo in enumerate(learning_outcomes, start=1):
        if not isinstance(lo, dict):
            continue
        lo_index = lo.get("index", lo_position)
        contents = lo.get("contents")
        if not isinstance(contents, list):
            continue
        for content_position, content in enumerate(contents, start=1):
            if not isinstance(content, dict):
                continue
            content_index = content.get("index", content_position)
            key_facts = content.get("key_facts")
            if isinstance(key_facts, str) and key_facts.strip():
                field_name = f"Contents_{unit_index}_{lo_index}_{content_index}_Key_Facts"
                sections[field_name] = key_facts
    return sections


def extract_legacy_sections(payload: dict) -> dict[str, str]:
    return {
        key: value
        for key, value in payload.items()
        if key.endswith("_Key_Facts") and isinstance(value, str) and value.strip()
    }


def extract_sections(payload: dict) -> dict[str, str]:
    sections = extract_structured_sections(payload)
    if sections:
        return sections
    return extract_legacy_sections(payload)


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: check_keyfacts_similarity.py <payload.json>")
        return 1

    payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    sections = extract_sections(payload)

    if len(sections) < 2:
        print("OK: fewer than two Key Facts sections found.")
        return 0

    prepared = {key: shingles(normalize(value)) for key, value in sections.items()}
    flagged = []

    for left_key, right_key in combinations(sorted(prepared), 2):
        score = jaccard(prepared[left_key], prepared[right_key])
        if score >= 0.35:
            flagged.append((left_key, right_key, score))

    if flagged:
        print("Potential repetition detected:")
        for left_key, right_key, score in flagged:
            print(f"- {left_key} vs {right_key}: similarity={score:.2f}")
        return 2

    print("OK: Key Facts sections look sufficiently distinct.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
