import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import importlib.util

from ia_oral_questions import build_oral_questions_from_payload


STATE_PAYLOADS_DIR = Path("state") / "payloads"
STATE_IA_DIR = Path("state") / "ia_payloads"
OUTPUT_IA_DIR = Path("output") / "ia"


def safe_text(value):
    if value is None:
        return ""
    if isinstance(value, list):
        return "\n".join(str(v) for v in value)
    return str(value)


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip()


def _safe_filename(text: str) -> str:
    text = re.sub(r"[^A-Za-z0-9]+", "_", (text or "").strip())
    text = re.sub(r"_+", "_", text).strip("_")
    return text or "Course"


def load_payload(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))




def iter_topic_los(payload: dict) -> list[dict]:
    """
    Return a list of LO dicts in the topic-level schema shape:
      {index,title,contents:[{index,title}...], key_facts?, exercise_questions?, answer_key?, apply_*?}
    For IA, we only need index/title/contents.
    """
    unit = payload.get("current_unit") or {}
    out = []
    for lo in unit.get("learning_outcomes") or []:
        title = _norm(safe_text(lo.get("title", "")))
        if not title:
            continue
        contents = []
        for c in lo.get("contents") or []:
            ct = _norm(safe_text(c.get("title", "")))
            if ct:
                contents.append({"index": int(c.get("index") or (len(contents) + 1)), "title": ct})
        out.append({"index": int(lo.get("index") or (len(out) + 1)), "title": title, "contents": contents})
    return out


def build_course_ia_payload(payloads: list[dict], *, qualification_title: str) -> dict:
    """
    Build a single IA payload (one per syllabus/course) that lists all contents
    across all unit payloads (in UC order) inside current_unit.learning_outcomes[].
    """
    learning_outcomes: list[dict] = []
    y = 1
    for unit_idx, p in enumerate(payloads, start=1):
        unit = p.get("current_unit") or {}
        uc_title = _norm(safe_text(unit.get("unit_of_competency", "")))
        for lo in iter_topic_los(p):
            lo_title = lo["title"]
            # Preserve UC context in the LO title (no unit placeholders exist in the template).
            merged_title = f"{uc_title} — {lo_title}" if uc_title else lo_title
            contents = lo.get("contents") or []
            learning_outcomes.append({"index": y, "title": merged_title, "contents": contents})
            y += 1

    payload = {
        "qualification_title": qualification_title,
        "current_unit": {
            # assemble_ia requires current_unit with learning_outcomes.
            "unit_of_competency": "",
            "module_title": "",
            "next_unit_of_competency": "",
            "learning_outcomes": learning_outcomes,
            "ia": {},
        },
    }
    payload["current_unit"]["ia"]["oral_questions"] = build_oral_questions_from_payload(payload)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate one IA_FULL.docx per syllabus/course from unit payload JSONs in state/payloads.")
    parser.add_argument("--course-code", required=True, help="Course code used to select payloads by filename prefix.")
    parser.add_argument("--payloads-dir", type=Path, default=STATE_PAYLOADS_DIR)
    parser.add_argument("--outdir", type=Path, default=OUTPUT_IA_DIR)
    parser.add_argument("--state-dir", type=Path, default=STATE_IA_DIR)
    parser.add_argument("--qualification-title", default="", help="Override qualification title; default is from first payload.")
    parser.add_argument("--continue", dest="cont", action="store_true", help="Allow proceeding when multiple syllabi are present; deterministic selection still applies.")
    args = parser.parse_args()

    course_code = _safe_filename(args.course_code).upper()
    payloads_dir: Path = args.payloads_dir
    if not payloads_dir.exists():
        return 0

    # Match common payload naming: <COURSECODE>_..._UC<n>.json
    candidates = sorted(payloads_dir.glob(f"{course_code}*.json"), key=lambda p: p.name.lower())
    if not candidates:
        # Fallback: accept files starting with course code without underscores normalization.
        candidates = sorted(payloads_dir.glob(f"{args.course_code}*.json"), key=lambda p: p.name.lower())
    if not candidates:
        return 0

    payload_objs = [load_payload(p) for p in candidates]
    payload_objs.sort(key=lambda p: int((p.get("current_unit") or {}).get("index") or 0) or 9999)

    qualification_title = args.qualification_title.strip()
    if not qualification_title:
        qualification_title = _norm(safe_text(payload_objs[0].get("qualification_title", ""))) or course_code

    ia_payload = build_course_ia_payload(payload_objs, qualification_title=qualification_title)

    # Exams are required for IA assembly; generate MIDTERM + FINAL locally (no external API).
    tool_path = Path(__file__).resolve().parent / "generate_course_exams_local.py"
    spec = importlib.util.spec_from_file_location("generate_course_exams_local", tool_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load local exam generator module from: {tool_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    fn = getattr(mod, "generate_midterm_and_finals_local", None)
    if not callable(fn):
        raise RuntimeError("generate_midterm_and_finals_local not found in generate_course_exams_local.py")

    ia_payload["exams"] = fn(
        payload_objs,
        course_code=course_code,
        course_title=qualification_title,
        seed=0,
    )

    course_state = args.state_dir / course_code
    course_out = args.outdir / course_code
    course_state.mkdir(parents=True, exist_ok=True)
    course_out.mkdir(parents=True, exist_ok=True)

    ia_payload_path = course_state / "IA_FULL.json"
    ia_out_path = course_out / "IA_FULL.docx"
    ia_payload_path.write_text(json.dumps(ia_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    result = subprocess.run(
        [str(Path(".venv") / "Scripts" / "python.exe"), str(Path("tools") / "assemble_ia.py"), str(ia_payload_path), str(ia_out_path)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        sys.stderr.write(result.stdout)
        sys.stderr.write(result.stderr)
        return result.returncode

    print(json.dumps({"course_code": course_code, "payloads_used": [p.name for p in candidates], "ia_payload": str(ia_payload_path), "ia_output": str(ia_out_path)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
