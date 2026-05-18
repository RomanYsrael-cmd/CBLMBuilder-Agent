import argparse
import json
import subprocess
from pathlib import Path

from authored_exam_utils import validate_authored_mcq_state
from tos_snapshot import render_tos_snapshot


def main() -> int:
    parser = argparse.ArgumentParser(description="Render one term-specific IA DOCX from a Codex-authored IA payload and a Codex-authored term state JSON.")
    parser.add_argument("ia_payload_json", type=Path)
    parser.add_argument("term_state_json", type=Path)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    if not args.ia_payload_json.exists():
        raise FileNotFoundError(f"IA payload JSON not found: {args.ia_payload_json}")
    if not args.term_state_json.exists():
        raise FileNotFoundError(f"Term state JSON not found: {args.term_state_json}")

    ia_payload = json.loads(args.ia_payload_json.read_text(encoding="utf-8"))
    term_state = json.loads(args.term_state_json.read_text(encoding="utf-8"))

    term = str(ia_payload.get("term", "")).strip().upper()
    if term not in {"MIDTERM", "FINALS"}:
        raise ValueError("IA payload must contain term=MIDTERM or FINALS")
    if str(term_state.get("term", "")).strip().upper() != term:
        raise ValueError("IA payload term and term state term must match")

    mcqs = term_state.get("mcqs")
    validate_authored_mcq_state(term_state)

    ia_payload["exams"] = {
        "course_code": term_state.get("course_code", ""),
        "course_title": term_state.get("course_title", ""),
        "midterm_mcqs": mcqs if term == "MIDTERM" else [],
        "finals_mcqs": mcqs if term == "FINALS" else [],
    }
    course_code_safe = str(term_state.get("course_code", "")).replace(" ", "_")
    tos_workbook = Path("output") / "tos" / f"TOS_{course_code_safe}_{term}.xlsx"
    if tos_workbook.exists():
        tos_snapshot_path = Path("state") / "artifacts" / "tos_snapshots" / course_code_safe / f"TOS_{term}.png"
        render_tos_snapshot(tos_workbook, tos_snapshot_path)
        ia_payload["tos_snapshot_path"] = str(tos_snapshot_path)
    args.ia_payload_json.write_text(json.dumps(ia_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    output_path = args.output or (Path("output") / "ia" / str(term_state.get("course_code", "")).replace(" ", "_") / f"IA_{term}.docx")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    result = subprocess.run(
        [str(Path(".venv") / "Scripts" / "python.exe"), str(Path("tools") / "assemble_ia_term.py"), str(args.ia_payload_json), str(output_path)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
        raise SystemExit(result.returncode)

    print(json.dumps({"ia_payload": str(args.ia_payload_json), "term_state": str(args.term_state_json), "ia_output": str(output_path)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
