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


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: check_keyfacts_similarity.py <payload.json>")
        return 1

    payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    sections = {
        key: value
        for key, value in payload.items()
        if key.endswith("_Key_Facts") and isinstance(value, str) and value.strip()
    }

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
