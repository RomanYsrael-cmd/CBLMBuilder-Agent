import json
import shutil
import subprocess
from pathlib import Path

from build_tos_and_exam_from_syllabus import read_single_syllabus_from_inbox


PROCESSED_DIR = Path("processed")


def main() -> int:
    syllabus_path = read_single_syllabus_from_inbox()
    if syllabus_path is None:
        return 0

    python_exe = Path(".venv") / "Scripts" / "python.exe"

    tos_result = subprocess.run(
        [str(python_exe), str(Path("tools") / "build_tos_and_exam_from_syllabus.py"), "--syllabus", str(syllabus_path)],
        capture_output=True,
        text=True,
    )
    if tos_result.returncode != 0:
        if tos_result.stdout:
            print(tos_result.stdout)
        if tos_result.stderr:
            print(tos_result.stderr)
        return tos_result.returncode
    tos_summary = json.loads(tos_result.stdout or "{}")

    ia_result = subprocess.run(
        [str(python_exe), str(Path("tools") / "build_term_ia_from_syllabus.py"), "--syllabus", str(syllabus_path)],
        capture_output=True,
        text=True,
    )
    if ia_result.returncode != 0:
        if ia_result.stdout:
            print(ia_result.stdout)
        if ia_result.stderr:
            print(ia_result.stderr)
        return ia_result.returncode
    ia_summary = json.loads(ia_result.stdout or "{}")

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    moved_path = PROCESSED_DIR / syllabus_path.name
    if moved_path.exists():
        moved_path = PROCESSED_DIR / f"{syllabus_path.stem}__DUPLICATE{syllabus_path.suffix}"
    shutil.move(str(syllabus_path), str(moved_path))

    summary = {
        "syllabus_file_processed": syllabus_path.name,
        "course_code": ia_summary.get("course_code") or tos_summary.get("course_code"),
        "course_title": ia_summary.get("course_title") or tos_summary.get("course_title"),
        "packages_written": {
            "MIDTERM_IA": (ia_summary.get("outputs") or {}).get("MIDTERM"),
            "FINALS_IA": (ia_summary.get("outputs") or {}).get("FINALS"),
            "MIDTERM_TOS": (tos_summary.get("outputs") or {}).get("MIDTERM"),
            "FINALS_TOS": (tos_summary.get("outputs") or {}).get("FINALS"),
        },
        "syllabus_moved_to": str(moved_path),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
