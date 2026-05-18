import json
import re
import subprocess
import sys
from pathlib import Path
import shutil

from ia_oral_questions import build_oral_questions_from_payload


STATE_DIR = Path("state") / "ia_payloads"
OUTPUT_DIR = Path("output") / "ia"


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip()

def _tokens(text: str) -> list[str]:
    return [t for t in re.split(r"[^A-Za-z0-9]+", (text or "").lower()) if t]


def _norm_q(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (text or "").lower()).strip()


def _build_ia_block(payload: dict, *, unit_index: int, prior_question_texts: list[str], used_project_anchors: set[str]) -> dict:
    unit = payload["current_unit"]
    qualification_title = payload.get("qualification_title", "")
    module_title = unit.get("module_title", "") or qualification_title
    unit_of_competency = (unit.get("unit_of_competency", "") or "").strip()

    def iter_contents():
        for lo in unit.get("learning_outcomes", []) or []:
            for content in lo.get("contents", []) or []:
                title = _norm(content.get("title", ""))
                if title:
                    yield title

    contents = list(iter_contents())
    lo_titles = [_norm(lo.get("title", "")) for lo in unit.get("learning_outcomes", []) or [] if _norm(lo.get("title", ""))]

    def pick_titles(count: int, offset: int = 0) -> list[str]:
        seen: set[str] = set()
        picked: list[str] = []
        ordered = list(contents)
        if ordered and offset:
            offset = offset % len(ordered)
            ordered = ordered[offset:] + ordered[:offset]
        for title in ordered:
            key = title.lower()
            if key in seen:
                continue
            seen.add(key)
            picked.append(title)
            if len(picked) >= count:
                break
        while len(picked) < count and lo_titles:
            picked.append(lo_titles[len(picked) % len(lo_titles)])
        while len(picked) < count:
            picked.append(unit_of_competency or module_title or qualification_title or "this unit")
        return picked

    base_offset = unit_index * 3
    picks = pick_titles(5, offset=base_offset)
    project_core = _norm(unit_of_competency or module_title or qualification_title or "Institutional Assessment")
    project_name = f"{project_core} Evidence Portfolio: {picks[0]}"

    instructions = [
        "1. Review the IA plan and identify the required evidence for each Learning Outcome and content item.",
        f"2. Create a one-page overview for the unit of competency: {project_core}.",
        f"3. Prepare evidence artifacts for at least three contents (e.g., short notes, diagrams, examples, or outputs), prioritizing: {picks[0]}, {picks[1]}, and {picks[2]}.",
        "4. Organize your evidence by LO number and content index, and label each artifact clearly.",
        "5. Perform the demonstration as directed by the assessor and explain the purpose of each artifact.",
        "6. Answer the oral questions by referencing your evidence and using correct technical terms from the unit.",
        "7. Participate in the interview and justify the steps/decisions you made, including any checks you performed to ensure correctness.",
        "8. Submit your final evidence package in the required format (printed or digital) for recording and evaluation.",
    ]

    materials = [
        "Pen and paper / notebook",
        "Laptop/desktop computer",
        "Printed or digital copy of the CBLM unit and IA plan",
        "Basic office supplies (highlighters, sticky notes) for organizing evidence",
    ]
    if any("diagram" in t.lower() or "model" in t.lower() or "flow" in t.lower() for t in picks):
        materials.append("Diagramming tool (e.g., draw.io, Visio, or equivalent)")

    payload["current_unit"]["ia"] = payload["current_unit"].get("ia") or {}
    oral_questions = build_oral_questions_from_payload(payload)
    def questions_ok(qs: list[dict]) -> bool:
        texts = [q.get("question", "") for q in qs]
        texts_strict = texts[:4]
        for i in range(len(texts_strict)):
            for j in range(i + 1, len(texts_strict)):
                if _norm_q(texts_strict[i]) == _norm_q(texts_strict[j]):
                    return False
        for t in texts_strict:
            for prev in prior_question_texts:
                if _norm_q(t) == _norm_q(prev):
                    return False
        return True

    attempt = 0
    while attempt < 3 and (picks[0].lower() in used_project_anchors or not questions_ok(oral_questions)):
        attempt += 1
        picks = pick_titles(5, offset=base_offset + (attempt * 7))
        project_name = f"{project_core} Evidence Portfolio: {picks[0]}"
        oral_questions = build_oral_questions_from_payload(payload)
    if picks[0].lower() in used_project_anchors or not questions_ok(oral_questions):
        raise RuntimeError("IA guardrails failed: could not produce unique oral questions/project for this unit.")
    used_project_anchors.add(picks[0].lower())

    interview_questions = [
        f"Walk through your evidence portfolio for {project_core} and explain how it demonstrates competence.",
        f"Which content did you find most challenging ({picks[0]} / {picks[1]} / {picks[2]}) and how did you address it?",
        "What checks did you perform to ensure accuracy and consistency of your outputs/evidence?",
        "If you had more time, how would you improve the quality or clarity of your evidence package?",
        "Describe one professional or ethical consideration relevant to this unit and how you applied it during the activity.",
    ]

    return {
        "name_of_project": project_name,
        "Specific_Instructions": "\n".join(instructions),
        "instructions_for_demo": (
            f"Demonstrate the required tasks for {project_core} using your prepared evidence artifacts. "
            "Explain each step clearly and answer follow-up questions from the assessor."
        ),
        "list_of_materials_and_equipment": "\n".join(materials),
        "oral_questions": oral_questions,
        "interview_questions": interview_questions,
    }


def _assemble_ia(payload_path: Path, output_path: Path) -> None:
    python_exe = Path(".venv") / "Scripts" / "python.exe"
    cmd = [str(python_exe), str(Path("tools") / "assemble_ia.py"), str(payload_path), str(output_path)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError((result.stdout or "") + (result.stderr or ""))


def _merge_docx(inputs: list[Path], output_path: Path) -> None:
    python_exe = Path(".venv") / "Scripts" / "python.exe"
    cmd = [str(python_exe), str(Path("tools") / "merge_docx.py"), *[str(p) for p in inputs], str(output_path)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError((result.stdout or "") + (result.stderr or ""))


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: python tools/regen_ia_outputs_from_state.py <COURSE_CODE>", file=sys.stderr)
        return 2
    course_code = argv[1]
    state_dir = STATE_DIR / course_code
    if not state_dir.exists():
        print(f"State dir not found: {state_dir}", file=sys.stderr)
        return 2

    out_dir = OUTPUT_DIR / course_code
    out_dir.mkdir(parents=True, exist_ok=True)

    payload_paths = sorted(state_dir.glob("IA_Unit_*.json"), key=lambda p: p.name.lower())
    if not payload_paths:
        print(f"No IA payloads found in: {state_dir}", file=sys.stderr)
        return 2

    unit_outputs: list[Path] = []
    prior_oral_questions: list[str] = []
    used_project_anchors: set[str] = set()
    for payload_path in payload_paths:
        payload = json.loads(payload_path.read_text(encoding="utf-8"))
        # Guardrail: fix bad/placeholder qualification title if it leaked into state.
        qt = (payload.get("qualification_title") or "").strip()
        if qt.lower() in ("competency-based learning materials", "competency based learning materials"):
            m_title = re.search(r"IA_Unit_\d+_(.+)\.json$", payload_path.name)
            if m_title:
                payload["qualification_title"] = m_title.group(1).replace("_", " ").strip()
        m = re.search(r"IA_Unit_(\d+)_", payload_path.name)
        unit_index = int(m.group(1)) if m else 1
        payload["current_unit"]["ia"] = _build_ia_block(
            payload,
            unit_index=unit_index,
            prior_question_texts=prior_oral_questions,
            used_project_anchors=used_project_anchors,
        )
        prior_oral_questions.extend([q.get("question", "") for q in (payload["current_unit"]["ia"].get("oral_questions") or [])[:4]])
        payload_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

        unit_out = out_dir / payload_path.with_suffix(".docx").name.replace("IA_Unit_", "IA_Unit_")
        _assemble_ia(payload_path, unit_out)
        unit_outputs.append(unit_out)

    full_path = out_dir / "IA_FULL.docx"
    tmp_full = out_dir / "IA_FULL__tmp.docx"
    _merge_docx(unit_outputs, tmp_full)
    try:
        if full_path.exists():
            full_path.unlink()
        shutil.move(str(tmp_full), str(full_path))
    except PermissionError as e:
        raise RuntimeError(
            f"Cannot overwrite {full_path} (file may be open). Close it and rerun. Details: {e}"
        )
    finally:
        try:
            if tmp_full.exists():
                tmp_full.unlink()
        except Exception:
            pass

    print(json.dumps({"course_code": course_code, "units": [p.name for p in unit_outputs], "full": str(full_path)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
