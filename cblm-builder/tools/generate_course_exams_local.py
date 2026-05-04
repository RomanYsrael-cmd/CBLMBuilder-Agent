import json
import random
import re
from dataclasses import dataclass
from pathlib import Path


def safe_text(value):
    if value is None:
        return ""
    if isinstance(value, list):
        return "\n".join(str(v) for v in value)
    return str(value)


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip()


@dataclass
class TopicItem:
    uc: str
    topic: str
    subtopic: str


def extract_items_from_payload(payload: dict) -> list[TopicItem]:
    unit = payload.get("current_unit") or {}
    uc = _norm(safe_text(unit.get("unit_of_competency", "")))
    items: list[TopicItem] = []
    for lo in unit.get("learning_outcomes") or []:
        topic = _norm(safe_text(lo.get("title", "")))
        if not topic:
            continue
        for c in lo.get("contents") or []:
            sub = _norm(safe_text(c.get("title", "")))
            if sub:
                items.append(TopicItem(uc=uc, topic=topic, subtopic=sub))
    return items


def _distractors(pool: list[str], correct: str, rng: random.Random) -> list[str]:
    pool = [p for p in pool if p and _norm(p).lower() != _norm(correct).lower()]
    rng.shuffle(pool)
    out = []
    for p in pool:
        if p not in out:
            out.append(p)
        if len(out) == 3:
            break
    while len(out) < 3:
        out.append("None of the above")
    return out


def _choice_pack(correct: str, distractors: list[str], rng: random.Random) -> tuple[list[str], str]:
    choices = [correct] + distractors[:3]
    rng.shuffle(choices)
    answer = ["A", "B", "C", "D"][choices.index(correct)]
    return choices, answer


def _q_variants(item: TopicItem) -> list[tuple[str, str]]:
    """
    Returns list of (question, correct_answer_text) variants.
    These are intentionally not copied from Let’s Exercise items.
    """
    uc = item.uc
    topic = item.topic
    sub = item.subtopic
    return [
        (f"In the context of {topic}, what best describes \"{sub}\"?", sub),
        (f"Which item is MOST directly associated with {topic}?", sub),
        (f"Which of the following would be an appropriate example related to \"{sub}\" under {topic}?", sub),
        (f"A trainee is working on {topic}. Which concept should be applied first when dealing with \"{sub}\"?", sub),
        (f"Which statement BEST matches the purpose of \"{sub}\" in {topic}?", sub),
        (f"In workplace practice, why is \"{sub}\" important when performing tasks in {topic}?", sub),
    ]


def generate_exam_mcqs_from_payloads(
    payloads: list[dict],
    *,
    seed: int = 0,
    questions: int = 50,
) -> list[dict]:
    """
    Deterministic local MCQ generator based on UC/Topic/Subtopic titles.
    Output shape matches IA templates / assemble_ia expectations:
      [{question,a,b,c,d,answer}, ...] length==questions
    """
    rng = random.Random(seed or 0)

    items: list[TopicItem] = []
    for p in payloads:
        items.extend(extract_items_from_payload(p))

    if not items:
        # Fallback: generate placeholder MCQs if no items exist.
        return [
            {"question": f"Question {i}: Select the best answer.", "a": "A", "b": "B", "c": "C", "d": "D", "answer": "A"}
            for i in range(1, questions + 1)
        ]

    # Build distractor pools.
    subtopic_pool = sorted({i.subtopic for i in items if i.subtopic})
    topic_pool = sorted({i.topic for i in items if i.topic})
    uc_pool = sorted({i.uc for i in items if i.uc})
    generic_pool = subtopic_pool + topic_pool + uc_pool

    # Expand items to reach question count with variant rotation.
    mcqs: list[dict] = []
    idx = 0
    while len(mcqs) < questions:
        item = items[idx % len(items)]
        variants = _q_variants(item)
        q_text, correct_text = variants[(idx // len(items)) % len(variants)]

        distractors = _distractors(generic_pool, correct_text, rng)
        choices, ans = _choice_pack(correct_text, distractors, rng)
        mcqs.append(
            {
                "question": q_text,
                "a": choices[0],
                "b": choices[1],
                "c": choices[2],
                "d": choices[3],
                "answer": ans,
            }
        )
        idx += 1

    # Light de-duplication by question text.
    seen = set()
    deduped = []
    for m in mcqs:
        key = _norm(m["question"]).lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(m)

    # If dedup reduced below target, pad deterministically with slightly altered stems.
    pad_i = 1
    while len(deduped) < questions:
        base = mcqs[(len(deduped) + pad_i) % len(mcqs)]
        deduped.append({**base, "question": base["question"] + f" (Form {pad_i})"})
        pad_i += 1

    return deduped[:questions]


def split_midterm_final(payloads: list[dict]) -> tuple[list[dict], list[dict]]:
    if not payloads:
        return [], []
    half = (len(payloads) + 1) // 2
    return payloads[:half], payloads[half:]


def generate_midterm_and_finals_local(
    payloads: list[dict],
    *,
    course_code: str,
    course_title: str,
    seed: int = 0,
) -> dict:
    mid_scope, fin_scope = split_midterm_final(payloads)
    midterm = generate_exam_mcqs_from_payloads(mid_scope or payloads, seed=(seed or 0) + 1, questions=50)
    finals = generate_exam_mcqs_from_payloads(fin_scope or payloads, seed=(seed or 0) + 2, questions=50)
    return {"course_code": course_code, "course_title": course_title, "midterm_mcqs": midterm, "finals_mcqs": finals}


def load_payloads(paths: list[Path]) -> list[dict]:
    return [json.loads(p.read_text(encoding="utf-8")) for p in paths]

