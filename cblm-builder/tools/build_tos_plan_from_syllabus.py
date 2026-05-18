import argparse
import json
from dataclasses import asdict
from pathlib import Path

from authored_exam_utils import expected_level_counts
from build_tos_and_exam_from_syllabus import (
    MIDTERM_TOS_TEMPLATE,
    FINALS_TOS_TEMPLATE,
    OUT_TOS_DIR,
    STATE_DIR,
    build_term_plans,
    parse_syllabus,
    read_single_syllabus_from_inbox,
    read_syllabus_text,
    safe_filename,
    write_tos_workbook,
)


def write_plan_state_json(
    output_path: Path,
    *,
    syllabus_file: str,
    course_code: str,
    course_title: str,
    term_name: str,
    plans: list,
) -> None:
    payload = {
        "syllabus_file": syllabus_file,
        "course_code": course_code,
        "course_title": course_title,
        "term": term_name,
        "topics": [asdict(plan) for plan in plans],
        "expected_level_counts": dict(expected_level_counts([asdict(plan) for plan in plans])),
        "mcqs": [],
        "authoring_mode": "codex_required",
        "authoring_requirements": {
            "mcq_count": 50,
            "level_field_required": True,
            "mcq_order_must_follow_tos_numbering": True,
        },
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build MIDTERM/FINALS TOS workbooks and authored-state scaffolds from a syllabus, without generating MCQs.")
    parser.add_argument("--syllabus", type=Path, default=None)
    parser.add_argument("--midterm-tos-template", type=Path, default=MIDTERM_TOS_TEMPLATE)
    parser.add_argument("--finals-tos-template", type=Path, default=FINALS_TOS_TEMPLATE)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    syllabus_path = args.syllabus or read_single_syllabus_from_inbox()
    if syllabus_path is None:
        return 0
    if not syllabus_path.exists():
        raise FileNotFoundError(f"Syllabus not found: {syllabus_path}")
    if not args.midterm_tos_template.exists():
        raise FileNotFoundError(f"Missing MIDTERM TOS template: {args.midterm_tos_template}")
    if not args.finals_tos_template.exists():
        raise FileNotFoundError(f"Missing FINALS TOS template: {args.finals_tos_template}")

    syllabus = parse_syllabus(read_syllabus_text(syllabus_path))
    term_plans = build_term_plans(syllabus, seed=args.seed)
    course_safe = safe_filename(syllabus.course_code.upper())

    summary: dict[str, object] = {
        "syllabus_file": syllabus_path.name,
        "course_code": syllabus.course_code,
        "course_title": syllabus.course_title,
        "outputs": {},
    }

    for term_name in ["MIDTERM", "FINALS"]:
        plans = term_plans[term_name]
        tos_template = args.midterm_tos_template if term_name == "MIDTERM" else args.finals_tos_template
        tos_out = OUT_TOS_DIR / f"TOS_{course_safe}_{term_name}.xlsx"
        state_out = STATE_DIR / course_safe / f"{term_name}.json"

        write_tos_workbook(
            tos_template,
            tos_out,
            course_code=syllabus.course_code,
            course_title=syllabus.course_title,
            term_name=term_name,
            plans=plans,
        )
        write_plan_state_json(
            state_out,
            syllabus_file=syllabus_path.name,
            course_code=syllabus.course_code,
            course_title=syllabus.course_title,
            term_name=term_name,
            plans=plans,
        )

        summary["outputs"][term_name] = {
            "tos": str(tos_out),
            "state": str(state_out),
            "topic_count": len(plans),
            "mcq_authoring_required": True,
        }

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
