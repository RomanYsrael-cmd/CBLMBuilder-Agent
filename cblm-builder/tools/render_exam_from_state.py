import argparse
import json
from pathlib import Path

import exam_builder
from authored_exam_utils import validate_authored_mcq_state
from build_tos_and_exam_from_syllabus import EXAM_TEMPLATE, OUT_EXAMS_DIR


def main() -> int:
    parser = argparse.ArgumentParser(description="Render one exam DOCX from a term state JSON authored by Codex.")
    parser.add_argument("state_json", type=Path)
    parser.add_argument("--exam-template", type=Path, default=EXAM_TEMPLATE)
    parser.add_argument("--outdir", type=Path, default=OUT_EXAMS_DIR)
    args = parser.parse_args()

    if not args.state_json.exists():
        raise FileNotFoundError(f"State JSON not found: {args.state_json}")
    if not args.exam_template.exists():
        raise FileNotFoundError(f"Missing exam template: {args.exam_template}")

    payload = json.loads(args.state_json.read_text(encoding="utf-8"))
    course_code = str(payload.get("course_code", "")).strip()
    course_title = str(payload.get("course_title", "")).strip()
    term_name = str(payload.get("term", "")).strip().upper()
    mcqs = payload.get("mcqs")
    validation = validate_authored_mcq_state(payload)

    output_path = args.outdir / f"EXAM_{course_code.replace(' ', '_')}_{term_name}.docx"
    exam_builder.fill_exam_template(
        args.exam_template,
        output_path,
        course_code=course_code,
        course_title=course_title,
        term="MIDTERM" if term_name == "MIDTERM" else "FINAL",
        mcqs=[
            exam_builder.MCQ(
                question=item["question"],
                a=item["a"],
                b=item["b"],
                c=item["c"],
                d=item["d"],
                answer=item["answer"],
                level=item.get("level"),
            )
            for item in mcqs
        ],
        include_answer_key=True,
    )
    print(
        json.dumps(
            {
                "state_json": str(args.state_json),
                "exam_output": str(output_path),
                "level_counts": validation["actual_counts"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
