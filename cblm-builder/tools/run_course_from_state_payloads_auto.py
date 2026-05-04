import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


STATE_PAYLOADS_DIR = Path("state") / "payloads"
OUTPUT_DIR = Path("output")


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip()


def _safe_filename(text: str) -> str:
    text = re.sub(r"[^A-Za-z0-9]+", "_", (text or "").strip())
    text = re.sub(r"_+", "_", text).strip("_")
    return text or "Course"


def load_payload(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def infer_course_code_from_filename(path: Path) -> str:
    # Convention: <COURSECODE>_..._UC<n>.json (or similar)
    stem = path.stem
    m = re.match(r"^([A-Za-z0-9]+)_", stem)
    if m:
        return m.group(1).upper()
    return "COURSE"


def infer_uc_index(payload: dict, fallback: int) -> int:
    unit = payload.get("current_unit") or {}
    idx = unit.get("index")
    if isinstance(idx, int) and idx > 0:
        return idx
    return fallback


def choose_course_payloads(payload_dir: Path) -> tuple[str, list[Path]]:
    candidates = sorted(payload_dir.glob("*.json"), key=lambda p: p.name.lower())
    if not candidates:
        return "", []
    # deterministically pick first course code
    course = infer_course_code_from_filename(candidates[0])
    chosen = [p for p in candidates if infer_course_code_from_filename(p) == course]
    return course, chosen


def assemble_unit(payload_path: Path, *, course_code: str, generate_images: bool) -> Path:
    payload = load_payload(payload_path)
    uc_index = infer_uc_index(payload, fallback=1)
    unit = payload.get("current_unit") or {}
    safe_title = _safe_filename(_norm(unit.get("unit_of_competency", "")) or f"UC{uc_index}")
    out_path = OUTPUT_DIR / f"CBLM_Unit_{uc_index}_{course_code}_{safe_title}.docx"

    # Similarity check
    sim = subprocess.run(
        [str(Path(".venv") / "Scripts" / "python.exe"), str(Path("tools") / "check_keyfacts_similarity.py"), str(payload_path)],
        capture_output=True,
        text=True,
    )
    if sim.returncode != 0:
        sys.stderr.write(sim.stdout)
        sys.stderr.write(sim.stderr)
        raise RuntimeError(f"Key Facts similarity check failed for {payload_path.name}")

    # Optional images
    if generate_images:
        img = subprocess.run(
            [str(Path(".venv") / "Scripts" / "python.exe"), str(Path("tools") / "generate_keyfacts_images_openrouter.py"), str(payload_path), "--inplace"],
            capture_output=True,
            text=True,
        )
        if img.returncode != 0:
            sys.stderr.write(img.stdout)
            sys.stderr.write(img.stderr)
            raise RuntimeError(f"Image generation failed for {payload_path.name}")

    # Assemble
    asm = subprocess.run(
        [str(Path(".venv") / "Scripts" / "python.exe"), str(Path("tools") / "assemble_cblm.py"), str(payload_path), str(out_path)],
        capture_output=True,
        text=True,
    )
    if asm.returncode != 0:
        sys.stderr.write(asm.stdout)
        sys.stderr.write(asm.stderr)
        raise RuntimeError(f"CBLM assembly failed for {payload_path.name}")

    return out_path


def merge_units(unit_paths: list[Path], out_path: Path) -> None:
    if not unit_paths:
        return
    tmp = out_path.with_name(out_path.stem + "__tmp.docx")
    cmd = [str(Path(".venv") / "Scripts" / "python.exe"), str(Path("tools") / "merge_docx.py")]
    cmd.extend(str(p) for p in unit_paths)
    cmd.append(str(tmp))
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        sys.stderr.write(result.stdout)
        sys.stderr.write(result.stderr)
        raise RuntimeError("CBLM_FULL merge failed")
    try:
        if out_path.exists():
            out_path.unlink()
        shutil.move(str(tmp), str(out_path))
    finally:
        try:
            if tmp.exists():
                tmp.unlink()
        except Exception:
            pass


def main() -> int:
    if not STATE_PAYLOADS_DIR.exists():
        return 0

    course_code, payload_paths = choose_course_payloads(STATE_PAYLOADS_DIR)
    if not payload_paths:
        return 0

    payload_objs = [(p, load_payload(p)) for p in payload_paths]
    payload_objs.sort(key=lambda t: infer_uc_index(t[1], fallback=9999))
    payload_paths = [p for p, _ in payload_objs]

    generate_images = str(os.environ.get("CBLM_GENERATE_IMAGES") or "0").strip() == "1"

    unit_outs: list[Path] = []
    for p in payload_paths:
        unit_outs.append(assemble_unit(p, course_code=course_code, generate_images=generate_images))

    full_out = OUTPUT_DIR / "CBLM_FULL.docx"
    merge_units(unit_outs, full_out)

    # Generate course-level IA (includes exams locally + assembles IA_FULL)
    ia = subprocess.run(
        [str(Path(".venv") / "Scripts" / "python.exe"), str(Path("tools") / "run_ia_course_from_state_payloads.py"), "--course-code", course_code],
        capture_output=True,
        text=True,
    )
    if ia.returncode != 0:
        sys.stderr.write(ia.stdout)
        sys.stderr.write(ia.stderr)
        raise RuntimeError("IA generation failed")

    print(
        json.dumps(
            {
                "course_code": course_code,
                "payloads_processed": [p.name for p in payload_paths],
                "unit_outputs": [str(p) for p in unit_outs],
                "cblm_full": str(full_out),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
