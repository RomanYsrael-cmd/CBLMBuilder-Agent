import argparse
import json
import subprocess
from collections import OrderedDict
from pathlib import Path

from build_tos_and_exam_from_syllabus import (
    STATE_DIR as TOS_STATE_DIR,
    ensure_term_assignments,
    parse_syllabus,
    read_single_syllabus_from_inbox,
    read_syllabus_text,
    safe_filename,
)


STATE_IA_DIR = Path("state") / "ia_payloads"
OUTPUT_IA_DIR = Path("output") / "ia"


def _norm(text: str) -> str:
    return " ".join((text or "").split()).strip()


def _load_term_mcqs(path: Path) -> list[dict]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    mcqs = payload.get("mcqs")
    if not isinstance(mcqs, list) or len(mcqs) != 50:
        raise ValueError(f"Expected 50 MCQs in {path}")
    return mcqs


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
            contents.append(
                {
                    "index": topic_index,
                    "title": _norm(topic.title),
                    "subtopics": subtopics,
                }
            )
        learning_outcomes.append({"index": lo_index, "title": lo_title, "contents": contents})
    return learning_outcomes


def _flatten_pairs(learning_outcomes: list[dict]) -> list[tuple[str, str]]:
    pairs = []
    for lo in learning_outcomes:
        lo_title = _norm(lo.get("title", ""))
        for content in lo.get("contents") or []:
            topic_title = _norm(content.get("title", ""))
            if lo_title and topic_title:
                pairs.append((lo_title, topic_title))
    return pairs


def _flatten_subtopics(learning_outcomes: list[dict]) -> list[tuple[str, str, str]]:
    items = []
    for lo in learning_outcomes:
        lo_title = _norm(lo.get("title", ""))
        for content in lo.get("contents") or []:
            topic_title = _norm(content.get("title", ""))
            for sub in content.get("subtopics") or []:
                sub_title = _norm(sub.get("title", ""))
                if lo_title and topic_title and sub_title:
                    items.append((lo_title, topic_title, sub_title))
    return items


def _lower_first(text: str) -> str:
    text = _norm(text)
    if not text:
        return ""
    return text[:1].lower() + text[1:]


def _title_focus(title: str) -> str:
    title = _norm(title)
    if not title:
        return "the lesson"
    lower = title.lower()
    starters = [
        "apply ",
        "work with ",
        "examine ",
        "explain ",
        "create ",
        "transition ",
        "introduce ",
        "build ",
        "design ",
        "analyze ",
        "use ",
        "develop ",
    ]
    for starter in starters:
        if lower.startswith(starter):
            return title[len(starter) :].strip() or title
    return title


def _model_answer(topic: str, subtopic: str = "", mode: str = "purpose") -> str:
    topic = _norm(topic)
    subtopic = _norm(subtopic)
    focus = _title_focus(subtopic or topic)
    lower_focus = _lower_first(focus)
    lower_topic = _lower_first(_title_focus(topic))

    if mode == "purpose":
        return f"It focuses on {lower_focus} as part of {lower_topic}."
    if mode == "application":
        return f"A correct response should apply {lower_focus} while performing a task related to {lower_topic}."
    if mode == "comparison":
        return f"It is connected to {lower_focus} because that competency belongs to {lower_topic}."
    if mode == "outcome":
        return f"After this lesson, the student should be able to perform work involving {lower_focus}."
    return f"It is related to {lower_focus} in the lesson on {lower_topic}."


def _build_oral_questions(*, qualification_title: str, term: str, learning_outcomes: list[dict]) -> list[dict]:
    lo_topic_pairs = _flatten_pairs(learning_outcomes)
    subtopic_items = _flatten_subtopics(learning_outcomes)
    if not lo_topic_pairs:
        return [
            {
                "question": f"What should a student be prepared to discuss in the {term} assessment for {qualification_title}?",
                "acceptable_answer": term,
            }
        ] * 5

    questions = []
    first_lo, first_topic = lo_topic_pairs[0]
    last_lo, last_topic = lo_topic_pairs[-1]
    questions.append(
        {
            "question": f"What is the main competency being developed when studying {first_topic} in the {term} assessment?",
            "acceptable_answer": _model_answer(first_topic, mode="purpose"),
        }
    )

    if len(lo_topic_pairs) > 1:
        _, second_topic = lo_topic_pairs[1]
        questions.append(
            {
                "question": f"In classroom practice, how would you distinguish {first_topic} from {second_topic}?",
                "acceptable_answer": f"{_model_answer(first_topic, mode='purpose')} {_model_answer(second_topic, mode='purpose')}",
            }
        )
    else:
        questions.append(
            {
                "question": f"What should a student be able to do after completing the lesson on {first_topic}?",
                "acceptable_answer": _model_answer(first_topic, mode="outcome"),
            }
        )

    if subtopic_items:
        lo_title, topic_title, subtopic_title = subtopic_items[0]
        questions.append(
            {
                "question": f"When working on {topic_title}, how would you explain the role of {subtopic_title}?",
                "acceptable_answer": _model_answer(topic_title, subtopic_title, mode="purpose"),
            }
        )
        mid_lo, mid_topic, mid_subtopic = subtopic_items[len(subtopic_items) // 2]
        questions.append(
            {
                "question": f"Give one practical use of {mid_subtopic} in a lesson about {mid_topic}.",
                "acceptable_answer": _model_answer(mid_topic, mid_subtopic, mode="application"),
            }
        )
    else:
        questions.append(
            {
                "question": f"What is one practical classroom use of {first_topic}?",
                "acceptable_answer": _model_answer(first_topic, mode="application"),
            }
        )
        questions.append(
            {
                "question": f"Why is {last_topic} important in the {term} assessment coverage?",
                "acceptable_answer": _model_answer(last_topic, mode="purpose"),
            }
        )

    questions.append(
        {
            "question": f"What kind of student performance is expected by the end of the {term} coverage in {qualification_title}?",
            "acceptable_answer": _model_answer(last_topic, mode="outcome"),
        }
    )

    unique = []
    seen = set()
    for item in questions:
        key = (_norm(item["question"]).lower(), _norm(item["acceptable_answer"]).lower())
        if key in seen:
            continue
        seen.add(key)
        unique.append(item)
        if len(unique) >= 5:
            break

    while len(unique) < 5:
        unique.append(
            {
                "question": f"What should a student be prepared to discuss in the {term} assessment for {qualification_title}?",
                "acceptable_answer": term,
            }
        )
    return unique[:5]


def build_term_payload(*, syllabus, term: str, term_topics: list, midterm_mcqs: list[dict], finals_mcqs: list[dict]) -> dict:
    learning_outcomes = _group_topics_by_lo(term_topics)
    payload = {
        "qualification_title": syllabus.course_title,
        "term": term,
        "current_unit": {
            "unit_of_competency": "",
            "module_title": "",
            "next_unit_of_competency": "",
            "learning_outcomes": learning_outcomes,
            "ia": {},
        },
        "exams": {
            "course_code": syllabus.course_code,
            "course_title": syllabus.course_title,
            "midterm_mcqs": midterm_mcqs,
            "finals_mcqs": finals_mcqs,
        },
    }
    payload["current_unit"]["ia"]["oral_questions"] = _build_oral_questions(
        qualification_title=syllabus.course_title,
        term=term,
        learning_outcomes=learning_outcomes,
    )
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Build separate MIDTERM and FINALS IA payloads/docx directly from a syllabus and TOS state JSON files.")
    parser.add_argument("--syllabus", type=Path, default=None)
    parser.add_argument("--midterm-state", type=Path, default=None)
    parser.add_argument("--finals-state", type=Path, default=None)
    args = parser.parse_args()

    syllabus_path = args.syllabus or read_single_syllabus_from_inbox()
    if syllabus_path is None or not syllabus_path.exists():
        return 0

    syllabus = parse_syllabus(read_syllabus_text(syllabus_path))
    course_safe = safe_filename(syllabus.course_code.upper())

    midterm_state = args.midterm_state or (TOS_STATE_DIR / course_safe / "MIDTERM.json")
    finals_state = args.finals_state or (TOS_STATE_DIR / course_safe / "FINALS.json")
    if not midterm_state.exists():
        raise FileNotFoundError(f"Missing MIDTERM state JSON: {midterm_state}")
    if not finals_state.exists():
        raise FileNotFoundError(f"Missing FINALS state JSON: {finals_state}")

    midterm_mcqs = _load_term_mcqs(midterm_state)
    finals_mcqs = _load_term_mcqs(finals_state)
    resolved_terms = ensure_term_assignments(syllabus)

    state_dir = STATE_IA_DIR / course_safe
    out_dir = OUTPUT_IA_DIR / course_safe
    state_dir.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)

    summary = {
        "syllabus_file": syllabus_path.name,
        "course_code": syllabus.course_code,
        "course_title": syllabus.course_title,
        "outputs": {},
    }

    for term in ["MIDTERM", "FINALS"]:
        payload = build_term_payload(
            syllabus=syllabus,
            term=term,
            term_topics=resolved_terms[term],
            midterm_mcqs=midterm_mcqs,
            finals_mcqs=finals_mcqs,
        )
        payload_path = state_dir / f"IA_{term}.json"
        output_path = out_dir / f"IA_{term}.docx"
        payload_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

        result = subprocess.run(
            [str(Path(".venv") / "Scripts" / "python.exe"), str(Path("tools") / "assemble_ia_term.py"), str(payload_path), str(output_path)],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr)
            raise SystemExit(result.returncode)

        summary["outputs"][term] = {
            "ia_payload": str(payload_path),
            "ia_output": str(output_path),
            "learning_outcome_count": len(payload["current_unit"]["learning_outcomes"]),
        }

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
