import argparse
import json
from collections import OrderedDict
from pathlib import Path

from build_tos_and_exam_from_syllabus import (
    ensure_term_assignments,
    parse_syllabus,
    read_single_syllabus_from_inbox,
    read_syllabus_text,
    safe_filename,
)


STATE_IA_DIR = Path("state") / "ia_payloads"


def _norm(text: str) -> str:
    return " ".join((text or "").split()).strip()


def _group_topics_by_lo(term_topics: list) -> list[dict]:
    grouped: "OrderedDict[tuple[int, str], list]" = OrderedDict()
    for topic in term_topics:
        key = (int(topic.uc_index), _norm(topic.uc_title))
        grouped.setdefault(key, []).append(topic)

    learning_outcomes = []
    for lo_index, ((_, lo_title), topics) in enumerate(grouped.items(), start=1):
        contents = []
        for topic_index, topic in enumerate(topics, start=1):
            subtopics = []
            for sub_index, sub in enumerate(topic.subtopics or [], start=1):
                title = _norm(sub)
                if title:
                    subtopics.append({"index": sub_index, "title": title})
            contents.append({"index": topic_index, "title": _norm(topic.title), "subtopics": subtopics})
        learning_outcomes.append({"index": lo_index, "title": lo_title, "contents": contents})
    return learning_outcomes


def build_term_payload(*, syllabus, term: str, term_topics: list) -> dict:
    return {
        "qualification_title": syllabus.course_title,
        "term": term,
        "current_unit": {
            "unit_of_competency": "",
            "module_title": "",
            "next_unit_of_competency": "",
            "learning_outcomes": _group_topics_by_lo(term_topics),
            "ia": {
                "oral_questions": [],
            },
        },
        "authoring_mode": "codex_required",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold separate MIDTERM and FINALS IA payloads directly from a syllabus, without authoring oral questions or exams.")
    parser.add_argument("--syllabus", type=Path, default=None)
    args = parser.parse_args()

    syllabus_path = args.syllabus or read_single_syllabus_from_inbox()
    if syllabus_path is None or not syllabus_path.exists():
        return 0

    syllabus = parse_syllabus(read_syllabus_text(syllabus_path))
    course_safe = safe_filename(syllabus.course_code.upper())
    resolved_terms = ensure_term_assignments(syllabus)

    state_dir = STATE_IA_DIR / course_safe
    state_dir.mkdir(parents=True, exist_ok=True)

    summary = {
        "syllabus_file": syllabus_path.name,
        "course_code": syllabus.course_code,
        "course_title": syllabus.course_title,
        "outputs": {},
    }

    for term in ["MIDTERM", "FINALS"]:
        payload = build_term_payload(syllabus=syllabus, term=term, term_topics=resolved_terms[term])
        payload_path = state_dir / f"IA_{term}.json"
        payload_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        summary["outputs"][term] = {
            "ia_payload": str(payload_path),
            "learning_outcome_count": len(payload["current_unit"]["learning_outcomes"]),
            "oral_authoring_required": True,
        }

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
