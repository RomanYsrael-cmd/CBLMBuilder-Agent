import hashlib
import json
import random
from collections import Counter
from pathlib import Path


VALID_LEVELS = {"knowledge", "comprehension", "application"}
VALID_ANSWER_CHOICES = {"A", "B", "C", "D"}
MIN_OPTION_COUNT = 8
MAX_OPTION_COUNT = 17
MAX_CONSECUTIVE_SAME_ANSWER = 3


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
    answer_sequence: list[str] = []
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
        answer = str(item.get("answer", "")).strip().upper()
        if answer not in VALID_ANSWER_CHOICES:
            raise ValueError(f"MCQ #{idx} answer must be one of A, B, C, or D.")
        answer_sequence.append(answer)

        expected = expected_sequence[idx - 1]
        if level != expected:
            raise ValueError(
                f"MCQ #{idx} level mismatch: expected {expected} from the TOS arrays, got {level}."
            )

    answer_counts = Counter(answer_sequence)
    for option in sorted(VALID_ANSWER_CHOICES):
        count = answer_counts.get(option, 0)
        if count < MIN_OPTION_COUNT or count > MAX_OPTION_COUNT:
            raise ValueError(
                f"Answer key distribution is too lopsided: option {option} appears {count} times. "
                f"Each option must appear between {MIN_OPTION_COUNT} and {MAX_OPTION_COUNT} times."
            )

    run_answer = None
    run_length = 0
    for idx, answer in enumerate(answer_sequence, start=1):
        if answer == run_answer:
            run_length += 1
        else:
            run_answer = answer
            run_length = 1
        if run_length > MAX_CONSECUTIVE_SAME_ANSWER:
            raise ValueError(
                f"Answer key pattern is too repetitive: option {answer} repeats more than "
                f"{MAX_CONSECUTIVE_SAME_ANSWER} times in a row ending at MCQ #{idx}."
            )

    return {
        "expected_counts": dict(Counter(expected_sequence)),
        "actual_counts": dict(Counter(actual_levels)),
        "expected_sequence": expected_sequence,
        "answer_counts": dict(answer_counts),
    }


def build_balanced_answer_pattern(course_code: str, term: str, count: int = 50) -> list[str]:
    base_counts = {"A": 13, "B": 13, "C": 12, "D": 12}
    answers: list[str] = []
    for option, qty in base_counts.items():
        answers.extend([option] * qty)
    if len(answers) != count:
        raise ValueError(f"Balanced answer pattern is configured for {count} items.")

    seed_bytes = hashlib.sha256(f"{course_code}|{term}|answer-pattern".encode("utf-8")).digest()
    rng = random.Random(int.from_bytes(seed_bytes[:8], "big"))

    for _ in range(5000):
        rng.shuffle(answers)
        run_option = None
        run_length = 0
        ok = True
        for answer in answers:
            if answer == run_option:
                run_length += 1
            else:
                run_option = answer
                run_length = 1
            if run_length > MAX_CONSECUTIVE_SAME_ANSWER:
                ok = False
                break
        if ok:
            return list(answers)

    raise ValueError("Could not construct a balanced answer pattern without repetitive streaks.")


def rebalance_mcq_answers(payload: dict) -> dict:
    mcqs = payload.get("mcqs")
    course_code = str(payload.get("course_code", "")).strip()
    term = str(payload.get("term", "")).strip().upper()
    if not isinstance(mcqs, list) or len(mcqs) != 50:
        raise ValueError("State JSON must contain exactly 50 MCQs in mcqs before rebalancing answers.")

    target_pattern = build_balanced_answer_pattern(course_code, term, len(mcqs))
    option_keys = ["A", "B", "C", "D"]
    field_map = {"A": "a", "B": "b", "C": "c", "D": "d"}

    for idx, (item, target_answer) in enumerate(zip(mcqs, target_pattern, strict=True), start=1):
        current_answer = str(item.get("answer", "")).strip().upper()
        if current_answer not in VALID_ANSWER_CHOICES:
            raise ValueError(f"MCQ #{idx} answer must be one of A, B, C, or D before rebalancing.")

        correct_text = item[field_map[current_answer]]
        distractors = [item[field_map[key]] for key in option_keys if key != current_answer]
        ordered_texts: list[str] = []
        distractor_iter = iter(distractors)
        for key in option_keys:
            if key == target_answer:
                ordered_texts.append(correct_text)
            else:
                ordered_texts.append(next(distractor_iter))
        for key, text in zip(option_keys, ordered_texts, strict=True):
            item[field_map[key]] = text
        item["answer"] = target_answer

    return payload
