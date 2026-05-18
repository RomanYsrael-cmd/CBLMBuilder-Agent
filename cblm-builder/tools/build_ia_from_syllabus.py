import argparse
import json
import subprocess
from pathlib import Path

from build_tos_and_exam_from_syllabus import parse_syllabus, read_single_syllabus_from_inbox, read_syllabus_text, safe_filename
from ia_oral_questions import build_oral_questions_from_payload


STATE_IA_DIR = Path("state") / "ia_payloads"
OUTPUT_IA_DIR = Path("output") / "ia"


def build_ia_payload(*, course_title: str, topics: list[dict], exams: dict) -> dict:
    learning_outcomes: list[dict] = []
    for idx, topic in enumerate(topics, start=1):
        lo_title = f"{topic['uc_title']} - {topic['title']}" if topic["uc_title"] else topic["title"]
        contents = [{"index": cidx, "title": subtopic} for cidx, subtopic in enumerate(topic["subtopics"], start=1)]
        learning_outcomes.append({"index": idx, "title": lo_title, "contents": contents})

    payload = {
        "qualification_title": course_title,
        "current_unit": {
            "unit_of_competency": "",
            "module_title": "",
            "next_unit_of_competency": "",
            "learning_outcomes": learning_outcomes,
            "ia": {},
        },
        "exams": exams,
    }
    payload["current_unit"]["ia"]["oral_questions"] = build_oral_questions_from_payload(payload)
    return payload


def load_exam_state(path: Path) -> list[dict]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    mcqs = payload.get("mcqs")
    if not isinstance(mcqs, list) or len(mcqs) != 50:
        raise ValueError(f"Expected 50 MCQs in {path}")
    return mcqs


def main() -> int:
    parser = argparse.ArgumentParser(description="Build IA_FULL directly from one syllabus and generated term state JSON files.")
    parser.add_argument("--syllabus", type=Path, default=None)
    parser.add_argument("--midterm-state", type=Path, required=True)
    parser.add_argument("--finals-state", type=Path, required=True)
    args = parser.parse_args()

    syllabus_path = args.syllabus or read_single_syllabus_from_inbox()
    if syllabus_path is None or not syllabus_path.exists():
        return 0

    syllabus = parse_syllabus(read_syllabus_text(syllabus_path))
    course_safe = safe_filename(syllabus.course_code.upper())

    exams = {
        "course_code": syllabus.course_code,
        "course_title": syllabus.course_title,
        "midterm_mcqs": load_exam_state(args.midterm_state),
        "finals_mcqs": load_exam_state(args.finals_state),
    }
    payload = build_ia_payload(
        course_title=syllabus.course_title,
        topics=[
            {
                "uc_index": topic.uc_index,
                "uc_title": topic.uc_title,
                "topic_index": topic.topic_index,
                "title": topic.title,
                "subtopics": topic.subtopics,
            }
            for topic in syllabus.topics
        ],
        exams=exams,
    )

    state_dir = STATE_IA_DIR / course_safe
    out_dir = OUTPUT_IA_DIR / course_safe
    state_dir.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)

    payload_path = state_dir / "IA_FULL.json"
    output_path = out_dir / "IA_FULL.docx"
    payload_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    result = subprocess.run(
        [str(Path(".venv") / "Scripts" / "python.exe"), str(Path("tools") / "assemble_ia.py"), str(payload_path), str(output_path)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
        raise SystemExit(result.returncode)

    print(
        json.dumps(
            {
                "syllabus_file": syllabus_path.name,
                "course_code": syllabus.course_code,
                "course_title": syllabus.course_title,
                "ia_payload": str(payload_path),
                "ia_output": str(output_path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
