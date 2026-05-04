import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


INBOX_DIR = Path("inbox")
OUT_DIR = Path("state") / "chatgpt_prompts"
TEMPLATE_PATH = Path("PromptPayload_parts") / "06_FOR_CHATGPT_UNIT_PAYLOAD.txt"


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip()


def _safe_filename(text: str) -> str:
    text = re.sub(r"[^A-Za-z0-9]+", "_", (text or "").strip())
    text = re.sub(r"_+", "_", text).strip("_")
    return text or "Course"


@dataclass
class Topic:
    index: int
    title: str
    subtopics: list[str]
    activity: str


@dataclass
class UC:
    index: int
    title: str
    topics: list[Topic]


@dataclass
class Syllabus:
    course_title: str
    course_code: str
    ucs: list[UC]
    raw_text: str


def _read_single_syllabus_from_inbox() -> Path | None:
    if not INBOX_DIR.exists():
        return None
    files = [p for p in INBOX_DIR.iterdir() if p.is_file() and p.suffix.lower() in {".txt", ".md"}]
    if not files:
        return None
    files.sort(key=lambda p: p.name.lower())
    return files[0]


def parse_extracted_syllabus(text: str) -> Syllabus:
    """
    Parser for the extracted text format used in this workspace, e.g.:
      Course Title
      ...
      Course Code
      ...
      LO1. ...
      Topic 1: ...
      Subtopics:
      ...
      Activity:
      ...
    """
    raw = text
    lines = [ln.rstrip() for ln in (text or "").splitlines()]

    def find_value_after(label: str) -> str:
        for i, ln in enumerate(lines):
            if _norm(ln).lower() == _norm(label).lower():
                for j in range(i + 1, min(i + 6, len(lines))):
                    v = _norm(lines[j])
                    if v:
                        return v
        return ""

    course_title = find_value_after("Course Title")
    course_code = find_value_after("Course Code")

    # LO blocks
    ucs: list[UC] = []
    i = 0
    lo_re = re.compile(r"^LO\s*(\d+)\.\s*(.+)$", re.I)
    topic_re = re.compile(r"^Topic\s*(\d+)\s*:\s*(.+)$", re.I)

    # Precompute LO start indices.
    # The extracted syllabus often lists LOs twice:
    #   1) in a summary list, then
    #   2) again as detailed sections with Topics/Subtopics/Activity.
    # We want the detailed sections, so for duplicate LO numbers we keep the LAST occurrence.
    lo_by_num: dict[int, tuple[int, str]] = {}
    for idx, ln in enumerate(lines):
        m = lo_re.match(_norm(ln))
        if m:
            lo_num = int(m.group(1))
            lo_title = _norm(m.group(2))
            lo_by_num[lo_num] = (idx, lo_title)

    lo_starts: list[tuple[int, int, str]] = [(idx, num, title) for num, (idx, title) in lo_by_num.items()]
    lo_starts.sort(key=lambda t: t[0])

    for lo_idx, (start_line, lo_num, lo_title) in enumerate(lo_starts):
        end_line = lo_starts[lo_idx + 1][0] if lo_idx + 1 < len(lo_starts) else len(lines)
        block = lines[start_line:end_line]

        topics: list[Topic] = []
        k = 0
        while k < len(block):
            m = topic_re.match(_norm(block[k]))
            if not m:
                k += 1
                continue
            topic_num = int(m.group(1))
            topic_title = _norm(m.group(2))

            # Seek "Subtopics:" then capture until "Activity:"
            subtopics: list[str] = []
            activity_lines: list[str] = []

            s = k + 1
            while s < len(block) and _norm(block[s]).lower() != "subtopics:":
                # Stop if another topic begins unexpectedly
                if topic_re.match(_norm(block[s])):
                    break
                s += 1

            if s < len(block) and _norm(block[s]).lower() == "subtopics:":
                s += 1
                while s < len(block):
                    ln = _norm(block[s])
                    if not ln:
                        s += 1
                        continue
                    if _norm(block[s]).lower() == "activity:":
                        break
                    if topic_re.match(_norm(block[s])):
                        break
                    subtopics.append(ln)
                    s += 1

            # Activity:
            while s < len(block) and _norm(block[s]).lower() != "activity:":
                if topic_re.match(_norm(block[s])):
                    break
                s += 1
            if s < len(block) and _norm(block[s]).lower() == "activity:":
                s += 1
                while s < len(block):
                    ln = block[s].rstrip()
                    if topic_re.match(_norm(ln)) or lo_re.match(_norm(ln)):
                        break
                    if ln.strip():
                        activity_lines.append(ln.strip())
                    s += 1

            activity = "\n".join(activity_lines).strip()
            topics.append(Topic(index=topic_num, title=topic_title, subtopics=subtopics, activity=activity))
            k = s

        ucs.append(UC(index=lo_num, title=lo_title, topics=topics))

    return Syllabus(course_title=course_title, course_code=course_code, ucs=ucs, raw_text=raw)


def build_chatgpt_prompt(*, template: str, syllabus: Syllabus, current_uc: UC) -> str:
    # Build a compact LO-only view for the selected UC, but include full LO list for qualification_units.
    lo_list = "\n".join([f"LO{u.index}. {u.title}" for u in syllabus.ucs]) or "(none found)"

    uc_block_lines = [f"LO{current_uc.index}. {current_uc.title}", ""]
    for t in current_uc.topics:
        uc_block_lines.append(f"Topic {t.index}: {t.title}")
        uc_block_lines.append("Subtopics:")
        for st in t.subtopics:
            uc_block_lines.append(f"- {st}")
        uc_block_lines.append("Activity:")
        uc_block_lines.append(t.activity or "(no activity provided)")
        uc_block_lines.append("")
    uc_block = "\n".join(uc_block_lines).strip()

    # Provide explicit "inputs" for the template prompt.
    header = "\n".join(
        [
            "SYLLABUS INPUT (for authoring one UC payload JSON)",
            f"Course Title: {syllabus.course_title or '(unknown)'}",
            f"Course Code: {syllabus.course_code or '(unknown)'}",
            "",
            "All Syllabus Learning Outcomes (for qualification_units):",
            lo_list,
            "",
            f"Selected UC index X: {current_uc.index}",
            "",
            "Selected UC details (Topics/Subtopics/Activity):",
            uc_block,
            "",
        ]
    )

    return (template.rstrip() + "\n\n" + header).strip() + "\n"


def main(argv: list[str]) -> int:
    syllabus_path = _read_single_syllabus_from_inbox()
    if syllabus_path is None:
        return 0

    template = ""
    if TEMPLATE_PATH.exists():
        template = TEMPLATE_PATH.read_text(encoding="utf-8")
    else:
        print(f"Missing template: {TEMPLATE_PATH}", file=sys.stderr)
        return 2

    raw = syllabus_path.read_text(encoding="utf-8", errors="replace")
    syllabus = parse_extracted_syllabus(raw)
    if not syllabus.ucs:
        print(f"No learning outcomes found in syllabus: {syllabus_path.name}", file=sys.stderr)
        return 2

    course_code_safe = _safe_filename(syllabus.course_code or "COURSE")
    out_dir = OUT_DIR / course_code_safe
    out_dir.mkdir(parents=True, exist_ok=True)

    outputs: list[str] = []
    for uc in sorted(syllabus.ucs, key=lambda u: u.index):
        prompt_text = build_chatgpt_prompt(template=template, syllabus=syllabus, current_uc=uc)
        out_path = out_dir / f"{course_code_safe}_UC{uc.index}_CHATGPT_PROMPT.txt"
        out_path.write_text(prompt_text, encoding="utf-8")
        outputs.append(str(out_path))

    meta = {
        "syllabus_file": syllabus_path.name,
        "course_code": syllabus.course_code,
        "course_title": syllabus.course_title,
        "uc_count": len(syllabus.ucs),
        "outputs": outputs,
    }
    (out_dir / "PROMPTS_INDEX.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(meta, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
