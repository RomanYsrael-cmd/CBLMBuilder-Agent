import re


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip()


def _safe_text(value) -> str:
    if value is None:
        return ""
    return str(value)


def _collect_learning_outcomes(payload: dict) -> list[dict]:
    unit = payload.get("current_unit") or {}
    out: list[dict] = []
    for lo_index, lo in enumerate(unit.get("learning_outcomes") or [], start=1):
        title = _norm(_safe_text(lo.get("title", "")))
        if not title:
            continue
        contents = []
        for content_index, content in enumerate(lo.get("contents") or [], start=1):
            content_title = _norm(_safe_text(content.get("title", "")))
            if content_title:
                contents.append(
                    {
                        "index": int(content.get("index") or content_index),
                        "title": content_title,
                    }
                )
        out.append(
            {
                "index": int(lo.get("index") or lo_index),
                "title": title,
                "contents": contents,
            }
        )
    return out


def _topic_title(lo: dict) -> str:
    title = _norm(_safe_text(lo.get("title", "")))
    if " - " in title:
        return title.split(" - ", 1)[1].strip()
    return title


def _content_title(lo: dict, position: int = 0) -> str:
    contents = lo.get("contents") or []
    if not contents:
        return _topic_title(lo)
    index = min(max(position, 0), len(contents) - 1)
    return contents[index]["title"]


def _unique_questions(items: list[dict]) -> list[dict]:
    seen: set[tuple[str, str]] = set()
    out: list[dict] = []
    for item in items:
        key = (_norm(item.get("question", "")).lower(), _norm(item.get("acceptable_answer", "")).lower())
        if not key[0] or not key[1] or key in seen:
            continue
        seen.add(key)
        out.append(
            {
                "question": _norm(item["question"]),
                "acceptable_answer": _norm(item["acceptable_answer"]),
            }
        )
    return out


def build_oral_questions_from_payload(payload: dict) -> list[dict]:
    unit = payload.get("current_unit") or {}
    qualification_title = _norm(_safe_text(payload.get("qualification_title", ""))) or "this course"
    unit_title = _norm(_safe_text(unit.get("unit_of_competency", "")))
    module_title = _norm(_safe_text(unit.get("module_title", "")))
    next_unit = _norm(_safe_text(unit.get("next_unit_of_competency", "")))
    los = _collect_learning_outcomes(payload)

    if not los:
        fallback_title = module_title or unit_title or qualification_title
        return [
            {
                "question": f"What is the title of the course or module for this assessment package?",
                "acceptable_answer": fallback_title,
            }
        ] * 5

    first_lo = los[0]
    second_lo = los[1] if len(los) > 1 else first_lo
    middle_lo = los[len(los) // 2]
    penultimate_lo = los[-2] if len(los) > 1 else los[-1]
    last_lo = los[-1]

    questions = [
        {
            "question": f"Which topic in {qualification_title} includes the content item '{_content_title(first_lo, 0)}'?",
            "acceptable_answer": first_lo["title"],
        },
        {
            "question": f"What topic comes immediately after '{first_lo['title']}' in the assessment sequence?",
            "acceptable_answer": second_lo["title"],
        },
        {
            "question": f"Under the topic '{middle_lo['title']}', what is the second content item listed?",
            "acceptable_answer": _content_title(middle_lo, 1),
        },
        {
            "question": f"Which topic covers the content '{_content_title(penultimate_lo, 0)}'?",
            "acceptable_answer": penultimate_lo["title"],
        },
    ]

    if next_unit:
        questions.append(
            {
                "question": f"After the current module '{module_title or unit_title or qualification_title}', what is the next unit of competency?",
                "acceptable_answer": next_unit,
            }
        )
    else:
        questions.append(
            {
                "question": f"What is the final topic listed in the assessment package for {qualification_title}?",
                "acceptable_answer": last_lo["title"],
            }
        )

    unique = _unique_questions(questions)
    fallback_questions = [
        {
            "question": f"In {qualification_title}, what is the first content item listed under '{last_lo['title']}'?",
            "acceptable_answer": _content_title(last_lo, 0),
        },
        {
            "question": f"Which topic in {qualification_title} includes the content item '{_content_title(last_lo, 0)}'?",
            "acceptable_answer": last_lo["title"],
        },
        {
            "question": f"What is the first topic listed in the assessment package for {qualification_title}?",
            "acceptable_answer": first_lo["title"],
        },
    ]
    for fallback in fallback_questions:
        if len(unique) >= 5:
            break
        unique = _unique_questions(unique + [fallback])
    return unique[:5]
