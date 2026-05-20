import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_IA_STATE = ROOT / "state" / "ia_payloads"
DEFAULT_TOS_STATE = ROOT / "state" / "tos"
DEFAULT_OUTPUT_IA = ROOT / "output" / "ia"
DEFAULT_OUTPUT_TOS = ROOT / "output" / "tos"
DEFAULT_OUTPUT_EXAMS = ROOT / "output" / "exams"
DEFAULT_PACKAGE_ROOT = ROOT / "output" / "regenerated_ia_packages"
PYTHON = ROOT / ".venv" / "Scripts" / "python.exe"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def copy_if_exists(src: Path, dest: Path) -> bool:
    if not src.exists():
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    return True


def term_output_name(term: str) -> str:
    term = term.strip().upper()
    if term not in {"MIDTERM", "FINALS"}:
        raise ValueError(f"Unsupported term: {term}")
    return term


def render_exam(term_state_json: Path, outdir: Path) -> Path:
    payload = load_json(term_state_json)
    term = term_output_name(str(payload.get("term", "")))
    course_code = str(payload.get("course_code", "")).replace(" ", "_")
    outdir.mkdir(parents=True, exist_ok=True)

    cmd = [
        str(PYTHON),
        str(ROOT / "tools" / "render_exam_from_state.py"),
        str(term_state_json),
        "--outdir",
        str(outdir),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    if result.returncode != 0:
        sys.stderr.write(result.stdout)
        sys.stderr.write(result.stderr)
        raise RuntimeError(f"Exam render failed for {term_state_json}")
    return outdir / f"EXAM_{course_code}_{term}.docx"


def render_ia(ia_payload_json: Path, term_state_json: Path, outdir: Path) -> Path:
    payload = load_json(ia_payload_json)
    term = term_output_name(str(payload.get("term", "")))
    course_code = str(load_json(term_state_json).get("course_code", "")).replace(" ", "_")
    outdir.mkdir(parents=True, exist_ok=True)
    output_path = outdir / f"IA_{term}.docx"

    cmd = [
        str(PYTHON),
        str(ROOT / "tools" / "render_term_ia_from_authored_state.py"),
        str(ia_payload_json),
        str(term_state_json),
        "--output",
        str(output_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    if result.returncode != 0:
        sys.stderr.write(result.stdout)
        sys.stderr.write(result.stderr)
        raise RuntimeError(f"IA render failed for {ia_payload_json}")
    return outdir / f"IA_{term}.docx"


def rebalance_term_state(term_state_json: Path) -> None:
    cmd = [
        str(PYTHON),
        str(ROOT / "tools" / "rebalance_authored_answers.py"),
        str(term_state_json),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    if result.returncode != 0:
        sys.stderr.write(result.stdout)
        sys.stderr.write(result.stderr)
        raise RuntimeError(f"Answer rebalance failed for {term_state_json}")


def iter_course_codes(ia_state_root: Path) -> list[str]:
    codes = []
    for course_dir in sorted(p for p in ia_state_root.iterdir() if p.is_dir()):
        if (course_dir / "IA_MIDTERM.json").exists() and (course_dir / "IA_FINALS.json").exists():
            codes.append(course_dir.name)
    return codes


def has_full_mcqs(term_state_json: Path) -> bool:
    payload = load_json(term_state_json)
    mcqs = payload.get("mcqs")
    return isinstance(mcqs, list) and len(mcqs) == 50


def copy_term_artifacts(
    course_code: str,
    term: str,
    *,
    ia_state_root: Path,
    tos_state_root: Path,
    output_tos_root: Path,
    package_root: Path,
) -> tuple[Path, Path]:
    package_course_root = package_root / course_code
    ia_state_dest = package_course_root / "state" / "ia_payloads" / course_code
    tos_state_dest = package_course_root / "state" / "tos" / course_code
    tos_out_dest = package_course_root / "output" / "tos"

    ia_src = ia_state_root / course_code / f"IA_{term}.json"
    tos_src = tos_state_root / course_code / f"{term}.json"
    workbook_src = output_tos_root / f"TOS_{course_code}_{term}.xlsx"

    ia_dest = ia_state_dest / ia_src.name
    tos_dest = tos_state_dest / tos_src.name
    workbook_dest = tos_out_dest / workbook_src.name

    if not ia_src.exists():
        raise FileNotFoundError(f"Missing IA payload: {ia_src}")
    if not tos_src.exists():
        raise FileNotFoundError(f"Missing term state: {tos_src}")
    if not workbook_src.exists():
        raise FileNotFoundError(f"Missing TOS workbook: {workbook_src}")

    copy_if_exists(ia_src, ia_dest)
    copy_if_exists(tos_src, tos_dest)
    copy_if_exists(workbook_src, workbook_dest)
    return ia_dest, tos_dest


def regenerate_course(
    course_code: str,
    *,
    ia_state_root: Path,
    tos_state_root: Path,
    output_tos_root: Path,
    output_ia_root: Path,
    output_exams_root: Path,
    package_root: Path,
) -> dict:
    package_course_root = package_root / course_code
    ia_outputs = package_course_root / "output" / "ia" / course_code
    exam_outputs = package_course_root / "output" / "exams"

    course_result = {
        "course_code": course_code,
        "midterm": {},
        "finals": {},
    }

    for term in ("MIDTERM", "FINALS"):
        ia_payload_copy, tos_state_copy = copy_term_artifacts(
            course_code,
            term,
            ia_state_root=ia_state_root,
            tos_state_root=tos_state_root,
            output_tos_root=output_tos_root,
            package_root=package_root,
        )
        if has_full_mcqs(tos_state_copy):
            rebalance_term_state(tos_state_copy)
            exam_path = render_exam(tos_state_copy, exam_outputs)
            ia_path = render_ia(ia_payload_copy, tos_state_copy, ia_outputs)
            mode = "regenerated"
        else:
            exam_src = output_exams_root / f"EXAM_{course_code}_{term}.docx"
            ia_src = output_ia_root / course_code / f"IA_{term}.docx"
            if not exam_src.exists():
                raise FileNotFoundError(f"Cannot regenerate or copy missing exam output: {exam_src}")
            if not ia_src.exists():
                raise FileNotFoundError(f"Cannot regenerate or copy missing IA output: {ia_src}")
            exam_path = exam_outputs / exam_src.name
            ia_path = ia_outputs / ia_src.name
            copy_if_exists(exam_src, exam_path)
            copy_if_exists(ia_src, ia_path)
            mode = "copied_existing_output"

        course_result[term.lower()] = {
            "mode": mode,
            "ia_payload_copy": str(ia_payload_copy),
            "term_state_copy": str(tos_state_copy),
            "ia_docx": str(ia_path),
            "exam_docx": str(exam_path),
            "tos_xlsx": str(package_course_root / "output" / "tos" / f"TOS_{course_code}_{term}.xlsx"),
        }

    return course_result


def main() -> int:
    parser = argparse.ArgumentParser(description="Regenerate IA packages from existing authored IA payloads and TOS state without modifying the original files.")
    parser.add_argument("--package-root", type=Path, default=DEFAULT_PACKAGE_ROOT)
    parser.add_argument("--ia-state-root", type=Path, default=DEFAULT_IA_STATE)
    parser.add_argument("--tos-state-root", type=Path, default=DEFAULT_TOS_STATE)
    parser.add_argument("--output-tos-root", type=Path, default=DEFAULT_OUTPUT_TOS)
    parser.add_argument("--output-ia-root", type=Path, default=DEFAULT_OUTPUT_IA)
    parser.add_argument("--output-exams-root", type=Path, default=DEFAULT_OUTPUT_EXAMS)
    parser.add_argument("--course-code", action="append", default=[])
    parser.add_argument("--force", action="store_true", help="Delete the destination package root before regenerating.")
    args = parser.parse_args()

    package_root = args.package_root
    if args.force and package_root.exists():
        shutil.rmtree(package_root)
    package_root.mkdir(parents=True, exist_ok=True)

    course_codes = args.course_code or iter_course_codes(args.ia_state_root)
    results = []
    for course_code in course_codes:
        results.append(
            regenerate_course(
                course_code,
                ia_state_root=args.ia_state_root,
                tos_state_root=args.tos_state_root,
                output_tos_root=args.output_tos_root,
                output_ia_root=args.output_ia_root,
                output_exams_root=args.output_exams_root,
                package_root=package_root,
            )
        )

    summary_path = package_root / "regeneration_summary.json"
    summary_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"package_root": str(package_root), "courses": len(results), "summary": str(summary_path)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
