import json
from collections import Counter
from pathlib import Path


VALID_LEVELS = {"knowledge", "comprehension", "application"}


def load_state_json(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"State JSON must contain an object payload: {path}")
    return payload


def expected_level_sequence(topics: list[dict]) -> list[str]:
    expected: dict[int, str] = {}
    for topic in topics:
        for level, key in (
            ("knowledge", "k_array"),
            ("comprehension", "c_array"),
            ("application", "a_array"),
        ):
            values = topic.get(key) or []
            if not isinstance(values, list):
                raise ValueError(f"TOS topic field {key} must be a list.")
            for value in values:
                if not isinstance(value, int):
                    raise ValueError(f"TOS topic field {key} must contain integers only.")
                if value in expected:
                    raise ValueError(f"Question number {value} is assigned more than once in the TOS arrays.")
                expected[value] = level

    if not expected:
        raise ValueError("TOS state must contain at least one numbered level assignment.")

    max_number = max(expected)
    missing = [n for n in range(1, max_number + 1) if n not in expected]
    if missing:
        raise ValueError(f"TOS numbering arrays are missing question numbers: {missing[:10]}")
    return [expected[n] for n in range(1, max_number + 1)]


def expected_level_counts(topics: list[dict]) -> Counter:
    return Counter(expected_level_sequence(topics))


def validate_authored_mcq_state(payload: dict) -> dict:
    topics = payload.get("topics")
    mcqs = payload.get("mcqs")
    term = str(payload.get("term", "")).strip().upper()
    course_code = str(payload.get("course_code", "")).strip()
    course_title = str(payload.get("course_title", "")).strip()

    if term not in {"MIDTERM", "FINALS"}:
        raise ValueError("State JSON must contain term=MIDTERM or FINALS.")
    if not course_code or not course_title:
        raise ValueError("State JSON must contain course_code and course_title.")
    if not isinstance(topics, list) or not topics:
        raise ValueError("State JSON must contain a non-empty topics list.")
    if not isinstance(mcqs, list) or len(mcqs) != 50:
        raise ValueError("State JSON must contain exactly 50 MCQs in mcqs.")

    expected_sequence = expected_level_sequence(topics)
    if len(expected_sequence) != 50:
        raise ValueError(f"TOS numbering arrays resolve to {len(expected_sequence)} items instead of 50.")

    actual_levels: list[str] = []
    for idx, item in enumerate(mcqs, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"MCQ #{idx} must be an object.")
        level = str(item.get("level", "")).strip().lower()
        if level not in VALID_LEVELS:
            raise ValueError(
                f"MCQ #{idx} must include level=knowledge|comprehension|application to match the TOS plan."
            )
        actual_levels.append(level)

        for key in ("question", "a", "b", "c", "d", "answer"):
            value = str(item.get(key, "")).strip()
            if not value:
                raise ValueError(f"MCQ #{idx} is missing required field: {key}")
        if str(item.get("answer", "")).strip().upper() not in {"A", "B", "C", "D"}:
            raise ValueError(f"MCQ #{idx} answer must be one of A, B, C, or D.")

        expected = expected_sequence[idx - 1]
        if level != expected:
            raise ValueError(
                f"MCQ #{idx} level mismatch: expected {expected} from the TOS arrays, got {level}."
            )

    return {
        "expected_counts": dict(Counter(expected_sequence)),
        "actual_counts": dict(Counter(actual_levels)),
        "expected_sequence": expected_sequence,
    }

