import json
import re
import subprocess
import sys
from pathlib import Path

from ia_oral_questions import build_oral_questions_from_payload


STATE_DIR = Path("state") / "ia_payloads"
OUTPUT_DIR = Path("output") / "ia"


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip()


def _safe_filename(text: str) -> str:
    text = re.sub(r"[^A-Za-z0-9]+", "_", (text or "").strip())
    text = re.sub(r"_+", "_", text).strip("_")
    return text or "Unit"


def _infer_course_code(payload_path: Path) -> str:
    # Convention: <COURSECODE>_<...>_UC<n>.json
    name = payload_path.stem
    m = re.match(r"^([A-Za-z0-9]+)_", name)
    if m:
        return m.group(1).upper()
    return "COURSE"


def _infer_unit_index(payload: dict, payload_path: Path) -> int:
    unit = payload.get("current_unit", {}) or {}
    idx = unit.get("index")
    if isinstance(idx, int) and idx > 0:
        return idx
    m = re.search(r"_UC(\d+)$", payload_path.stem, re.I)
    if m:
        return int(m.group(1))
    return 1


def _ability_phrase(title: str) -> str:
    # Keep aligned with tools/assemble_ia.py wording intent.
    t = _norm(title)
    if not t:
        return ""
    lower = t.lower()
    if lower.startswith("to "):
        t = t[3:].lstrip()
        lower = t.lower()
    first = lower.split()[0] if lower.split() else ""
    common_verbs = {
        "apply",
        "analyze",
        "assess",
        "calculate",
        "communicate",
        "conduct",
        "configure",
        "coordinate",
        "create",
        "demonstrate",
        "describe",
        "design",
        "develop",
        "evaluate",
        "explain",
        "identify",
        "implement",
        "inspect",
        "install",
        "interpret",
        "maintain",
        "manage",
        "monitor",
        "operate",
        "perform",
        "plan",
        "prepare",
        "present",
        "record",
        "report",
        "test",
        "troubleshoot",
        "use",
    }
    if first in common_verbs:
        return t[:1].lower() + t[1:]
    return f"demonstrate competence in {t}"


def _pick_content_anchor_titles(payload: dict, limit: int = 3) -> list[str]:
    unit = payload.get("current_unit", {}) or {}
    anchors: list[str] = []
    for lo in unit.get("learning_outcomes", []) or []:
        for content in lo.get("contents", []) or []:
            title = _norm(content.get("title", ""))
            if title:
                anchors.append(title)
            if len(anchors) >= limit:
                return anchors
    return anchors


def _build_ia_block(payload: dict) -> dict:
    unit = payload["current_unit"]
    qualification_title = _norm(payload.get("qualification_title", ""))
    module_title = _norm(unit.get("module_title", "")) or qualification_title

    anchors = _pick_content_anchor_titles(payload, limit=3)
    anchors_text = ", ".join(anchors) if anchors else "the required unit tasks"

    return {
        "name_of_project": f"Institutional Assessment Activity ({module_title})",
        "Specific_Instructions": "\n".join(
            [
                "1. Read the assessment brief and confirm the allotted time with the trainer/assessor.",
                "2. Review the learning outcomes and contents listed in the IA plan for this unit.",
                f"3. Prepare evidence and outputs related to {anchors_text} based on your trainer’s instructions.",
                "4. Perform the demonstration/work activity as directed and observe workplace-safe practices.",
                "5. Present your outputs/evidence to the assessor and answer the oral questions.",
                "6. Participate in the interview and clarify any steps or decisions you made during the activity.",
                "7. Submit final outputs in the required format (printed or digital) for recording and evaluation.",
            ]
        ),
        "instructions_for_demo": (
            "Demonstrate the required tasks for the unit based on the IA plan, explain your steps clearly, "
            "and answer follow-up questions from the assessor."
        ),
        "list_of_materials_and_equipment": "\n".join(
            [
                "Pen and paper / notebook",
                "Laptop/desktop computer (if required by the activity)",
                "Access to references or handouts provided by the trainer",
            ]
        ),
        "oral_questions": build_oral_questions_from_payload(payload),
        "interview_questions": [
            "Explain the reasoning behind the steps you followed during the activity.",
            "What assumptions did you make, and how would you verify them in an actual workplace?",
            "How would you improve your process to reduce time and errors while maintaining quality?",
            "What documentation would you keep as evidence of correct performance?",
            "Describe one ethical or professional consideration relevant to this unit.",
        ],
    }


def build_ia_payload_from_cblm_payload(cblm_payload: dict) -> dict:
    if "current_unit" not in cblm_payload:
        raise ValueError("CBLM payload missing required field: current_unit")

    # Reuse the unit LO/content structure directly (source of truth).
    unit = cblm_payload["current_unit"]

    # Minimal shape compatible with tools/assemble_ia.py.
    ia_payload = {
        "qualification_title": _norm(cblm_payload.get("qualification_title", "")),
        "current_unit": {
            "unit_of_competency": _norm(unit.get("unit_of_competency", "")),
            "module_title": _norm(unit.get("module_title", "")),
            "next_unit_of_competency": _norm(unit.get("next_unit_of_competency", "")),
            "learning_outcomes": [],
            "ia": {},
        },
    }

    for lo in unit.get("learning_outcomes", []) or []:
        ia_lo = {"index": int(lo.get("index") or 0) or (len(ia_payload["current_unit"]["learning_outcomes"]) + 1), "title": _norm(lo.get("title", "")), "contents": []}
        for content in lo.get("contents", []) or []:
            raw_title = _norm(content.get("title", ""))
            ia_lo["contents"].append(
                {
                    "index": int(content.get("index") or 0) or (len(ia_lo["contents"]) + 1),
                    "title": raw_title,
                    # Helpful derived text for humans (not used by assemble_ia templates directly).
                    "ability_phrase": _ability_phrase(raw_title),
                }
            )
        ia_payload["current_unit"]["learning_outcomes"].append(ia_lo)

    ia_payload["current_unit"]["ia"] = _build_ia_block({"qualification_title": ia_payload["qualification_title"], "current_unit": ia_payload["current_unit"]})
    return ia_payload


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: python tools/run_ia_from_cblm_payload.py <cblm_payload.json> [ia_output.docx]", file=sys.stderr)
        return 2

    cblm_payload_path = Path(argv[1])
    if not cblm_payload_path.exists():
        print(f"CBLM payload not found: {cblm_payload_path}", file=sys.stderr)
        return 2

    cblm_payload = json.loads(cblm_payload_path.read_text(encoding="utf-8"))
    ia_payload = build_ia_payload_from_cblm_payload(cblm_payload)

    course_code = _infer_course_code(cblm_payload_path)
    unit_index = _infer_unit_index(cblm_payload, cblm_payload_path)
    short_title = _safe_filename(ia_payload["current_unit"].get("module_title", "")) or "Unit"

    state_dir = STATE_DIR / course_code
    out_dir = OUTPUT_DIR / course_code
    state_dir.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)

    ia_payload_path = state_dir / f"IA_Unit_{unit_index}_{short_title}.json"
    ia_payload_path.write_text(json.dumps(ia_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    if len(argv) >= 3:
        ia_output_path = Path(argv[2])
    else:
        ia_output_path = out_dir / f"IA_Unit_{unit_index}_{short_title}.docx"

    result = subprocess.run(
        [str(Path(".venv") / "Scripts" / "python.exe"), str(Path("tools") / "assemble_ia.py"), str(ia_payload_path), str(ia_output_path)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        sys.stderr.write(result.stdout)
        sys.stderr.write(result.stderr)
        return result.returncode

    print(f"cblm_payload: {cblm_payload_path}")
    print(f"ia_payload: {ia_payload_path}")
    print(f"ia_output: {ia_output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
