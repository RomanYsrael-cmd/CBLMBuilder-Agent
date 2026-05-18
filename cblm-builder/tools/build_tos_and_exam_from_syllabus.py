import argparse
import copy
import json
import random
import re
import sys
import zipfile
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree as ET


TOOLS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS_DIR))

import exam_builder  # noqa: E402


INBOX_DIR = Path("inbox")
MIDTERM_TOS_TEMPLATE = Path("templates") / "TOS_TEMPLATE_MIDTERMS.xlsx"
FINALS_TOS_TEMPLATE = Path("templates") / "TOS_TEMPLATE_FINALS.xlsx"
EXAM_TEMPLATE = Path("templates") / "EXAM TEMPLATE.docx"
OUT_TOS_DIR = Path("output") / "tos"
OUT_EXAMS_DIR = Path("output") / "exams"
STATE_DIR = Path("state") / "tos"
SHEET_XML_PATH = "xl/worksheets/sheet1.xml"
MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
MC_NS = "http://schemas.openxmlformats.org/markup-compatibility/2006"
X14AC_NS = "http://schemas.microsoft.com/office/spreadsheetml/2009/9/ac"
XR_NS = "http://schemas.microsoft.com/office/spreadsheetml/2014/revision"
XR2_NS = "http://schemas.microsoft.com/office/spreadsheetml/2015/revision2"
XR3_NS = "http://schemas.microsoft.com/office/spreadsheetml/2016/revision3"
WORKBOOK_RELS_PATH = "xl/_rels/workbook.xml.rels"
CONTENT_TYPES_PATH = "[Content_Types].xml"
CALCCHAIN_PATH = "xl/calcChain.xml"

ET.register_namespace("", MAIN_NS)
ET.register_namespace("r", REL_NS)
ET.register_namespace("mc", MC_NS)
ET.register_namespace("x14ac", X14AC_NS)
ET.register_namespace("xr", XR_NS)
ET.register_namespace("xr2", XR2_NS)
ET.register_namespace("xr3", XR3_NS)


@dataclass
class TopicSpec:
    uc_index: int
    uc_title: str
    topic_index: int
    title: str
    subtopics: list[str] = field(default_factory=list)
    explicit_term: str | None = None
    explicit_weeks: int | None = None


@dataclass
class Syllabus:
    course_title: str
    course_code: str
    topics: list[TopicSpec]
    raw_text: str


@dataclass
class TermTopicPlan:
    uc_index: int
    topic_index: int
    title: str
    subtopics: list[str]
    number_of_days: int
    objective: str
    item_count: int = 0
    knowledge_count: int = 0
    comprehension_count: int = 0
    application_count: int = 0
    k_array: list[int] = field(default_factory=list)
    c_array: list[int] = field(default_factory=list)
    a_array: list[int] = field(default_factory=list)


def safe_text(value: str | None) -> str:
    return (value or "").strip()


def normalize_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", safe_text(text))


def safe_filename(text: str) -> str:
    text = re.sub(r"[^A-Za-z0-9]+", "_", safe_text(text))
    text = re.sub(r"_+", "_", text).strip("_")
    return text or "COURSE"


def read_syllabus_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".txt", ".md"}:
        return path.read_text(encoding="utf-8", errors="replace")
    if suffix == ".docx":
        return extract_text_from_docx(path)
    raise ValueError(f"Unsupported syllabus format: {path.suffix}")


def extract_text_from_docx(path: Path) -> str:
    with zipfile.ZipFile(path, "r") as zf:
        xml_bytes = zf.read("word/document.xml")
    root = ET.fromstring(xml_bytes)
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    lines: list[str] = []
    for para in root.findall(".//w:p", ns):
        parts = []
        for node in para.findall(".//w:t", ns):
            parts.append(node.text or "")
        lines.append("".join(parts))
    return "\n".join(lines)


def read_single_syllabus_from_inbox() -> Path | None:
    if not INBOX_DIR.exists():
        return None
    files = [
        p
        for p in INBOX_DIR.iterdir()
        if p.is_file() and p.suffix.lower() in {".txt", ".md", ".docx"}
    ]
    if not files:
        return None
    files.sort(key=lambda p: p.name.lower())
    return files[0]


def find_labeled_value(lines: list[str], label: str) -> str:
    target = label.lower().rstrip(":")
    for i, line in enumerate(lines):
        norm = normalize_spaces(line).lower().rstrip(":")
        if norm == target:
            for j in range(i + 1, min(i + 6, len(lines))):
                value = normalize_spaces(lines[j])
                if value and value != ":":
                    return value
    for line in lines:
        norm = normalize_spaces(line)
        if norm.lower().startswith(target + ":"):
            return normalize_spaces(norm.split(":", 1)[1])
    return ""


def parse_term_label(line: str) -> str | None:
    norm = normalize_spaces(line).lower().strip(":")
    if norm in {"preliminary", "prelim", "preliminary examination", "preliminary exam", "preliminary period"}:
        return "MIDTERM"
    if norm in {"midterm", "midterm examination", "midterm exam", "midterm period"}:
        return "MIDTERM"
    if norm in {"pre-final", "prefinal", "pre final", "pre-final examination", "pre final examination"}:
        return "FINALS"
    if norm in {"final", "finals", "final examination", "final exam", "final period", "finals examination"}:
        return "FINALS"
    if norm.startswith("term:"):
        return parse_term_label(norm.split(":", 1)[1])
    return None


def parse_week_count(line: str) -> int | None:
    norm = normalize_spaces(line)
    if not re.search(r"\bweek", norm, re.IGNORECASE):
        return None
    nums = [int(x) for x in re.findall(r"\d+", norm)]
    if not nums:
        return None
    if any(sep in norm for sep in ["-", "to", "–", "—"]) and len(nums) >= 2:
        return abs(nums[1] - nums[0]) + 1
    if "," in norm and len(nums) >= 2:
        return len(dict.fromkeys(nums))
    return max(1, len(nums))


def is_session_header(line: str) -> str | None:
    norm = normalize_spaces(line).lower().strip(":")
    if norm == "preliminary session":
        return "MIDTERM"
    if norm == "midterm session":
        return "MIDTERM"
    if norm == "pre-final session":
        return "FINALS"
    if norm == "final session":
        return "FINALS"
    return None


def is_lo_line(line: str) -> re.Match[str] | None:
    norm = normalize_spaces(line)
    return re.match(r"^Learning Outcome\s*(\d+)\s*\(LO\d+\)\s*:\s*$", norm, re.IGNORECASE) or re.match(
        r"^LO\s*(\d+)\.\s*(.+)$",
        norm,
        re.IGNORECASE,
    )


def is_topic_line(line: str) -> tuple[int | None, str] | None:
    norm = normalize_spaces(line)
    m = re.match(r"^Topic\s*(\d+)\s*:\s*(.+)$", norm, re.IGNORECASE)
    if m:
        return int(m.group(1)), normalize_spaces(m.group(2))
    m = re.match(r"^(\d+)\.?\s+(.+)$", norm)
    if m and "learning outcome" not in norm.lower():
        return int(m.group(1)), normalize_spaces(m.group(2))
    return None


def clean_bullet(line: str) -> str:
    text = normalize_spaces(line)
    return re.sub(r"^[-*•]+\s*", "", text)


def extract_parenthetical_subtopics(topic_title: str) -> list[str]:
    title = normalize_spaces(topic_title)
    match = re.search(r"\(([^)]*)\)?$", title)
    if not match:
        return []
    inner = match.group(1).strip(" ,;:")
    if not inner:
        return []
    pieces = [p.strip(" .,:;") for p in re.split(r",|/|;|\band\b", inner, flags=re.IGNORECASE)]
    return [piece for piece in pieces if piece]


def infer_subtopics_from_title(topic_title: str) -> list[str]:
    subtopics = extract_parenthetical_subtopics(topic_title)
    if subtopics:
        return subtopics
    title = normalize_spaces(topic_title)
    return [title] if title else []


def is_noise_subtopic(text: str) -> bool:
    lower = normalize_spaces(text).lower()
    if not lower:
        return True
    noise_values = {
        "subtopics",
        "subtopics:",
        "activity",
        "activity:",
        "interactive",
        "discussion",
        "interactive discussion",
        "self",
        "self-",
        "directed",
        "self directed",
        "self-directed",
        "blended",
        "e-books",
        "writing",
        "materials",
        "writing materials",
        "module",
        "internet",
        "connections",
        "internet connections",
        "let's apply",
        "lets apply",
        "let's exercise",
        "lets exercise",
        "read and",
        "understand key topics and",
        "learning points",
    }
    return lower in noise_values


def clean_subtopic_phrase(text: str) -> str:
    cleaned = normalize_spaces(text)
    cleaned = re.sub(r"^\d+\.\s*", "", cleaned)
    return cleaned


def concise_focus_text(text: str, *, max_words: int = 12) -> str:
    cleaned = clean_subtopic_phrase(text)
    for delimiter in [":", ";", " - ", " — ", ","]:
        if delimiter in cleaned:
            candidate = cleaned.split(delimiter, 1)[0].strip()
            if candidate:
                cleaned = candidate
                break
    words = cleaned.split()
    if len(words) > max_words:
        cleaned = " ".join(words[:max_words]).strip()
    return cleaned.rstrip(".,;:-")


def lower_first(text: str) -> str:
    text = normalize_spaces(text)
    if not text:
        return ""
    return text[:1].lower() + text[1:]


def competency_phrase(text: str) -> str:
    text = normalize_spaces(text)
    if not text:
        return "perform the required task"
    lower = text.lower()
    starters = [
        "apply ",
        "work with ",
        "examine ",
        "explain ",
        "create ",
        "transition ",
        "introduce ",
        "build ",
        "design ",
        "analyze ",
        "use ",
        "develop ",
    ]
    for starter in starters:
        if lower.startswith(starter):
            tail = text[len(starter) :].strip()
            if tail:
                return f"{starter.strip()} {lower_first(tail)}"
    return f"work with {lower_first(text)}"


def option_phrase(text: str, *, mode: str) -> str:
    focus = competency_phrase(text)
    if mode == "knowledge":
        return f"Focuses on how to {focus}."
    if mode == "comprehension":
        return f"Explains when and why to {focus}."
    return f"Uses the correct procedure to {focus} in practice."


def parse_table_style_topics(
    lines: list[str],
    *,
    topic_header_stoppers: set[str],
    topic_body_markers: tuple[str, ...],
) -> list[TopicSpec]:
    topics: list[TopicSpec] = []
    current_uc_index: int | None = None
    current_uc_title = ""
    current_term: str | None = None
    i = 0

    def parse_lo_colon(line: str) -> tuple[int, str] | None:
        match = re.match(r"^LO\s*(\d+)\s*[:.]\s*(.+)$", line, re.IGNORECASE)
        if not match:
            return None
        return int(match.group(1)), normalize_spaces(match.group(2))

    def is_candidate_topic(line: str) -> bool:
        lower = line.lower()
        if not line:
            return False
        if lower in topic_header_stoppers:
            return False
        if lower in {"a. orientation", "orientation"}:
            return False
        if lower.startswith(("lo", "co", "sdg", "week", "let", "read key facts", "answer let", "activity ")):
            return False
        if lower.startswith(("interactive discussion", "self-", "e-books", "writing materials", "lms", "internet connections")):
            return False
        if parse_term_label(line) or is_session_header(line):
            return False
        if re.match(r"^\d+\.\d+-\d+[: ]", line):
            return False
        if line.endswith(":"):
            return False
        return True

    while i < len(lines):
        norm = normalize_spaces(lines[i])
        if not norm:
            i += 1
            continue

        session = is_session_header(norm)
        if session:
            current_term = session
            i += 1
            continue

        lo_colon = parse_lo_colon(norm)
        if lo_colon:
            current_uc_index, current_uc_title = lo_colon
            i += 1
            continue

        if current_uc_index is None or not is_candidate_topic(norm):
            i += 1
            continue

        saw_keyfacts = False
        explicit_weeks: int | None = None
        j = i + 1
        while j < len(lines):
            nxt = normalize_spaces(lines[j])
            if not nxt:
                j += 1
                continue
            if parse_lo_colon(nxt) or is_session_header(nxt):
                break
            week_count = parse_week_count(nxt)
            if week_count is not None:
                explicit_weeks = week_count
                j += 1
                break
            nxt_lower = nxt.lower()
            if nxt_lower == "read key facts" or nxt_lower.startswith("read key facts ") or re.match(r"^\d+\.\d+-\d+[: ]", nxt):
                saw_keyfacts = True
            j += 1

        if saw_keyfacts:
            topic_index = len([t for t in topics if t.uc_index == current_uc_index]) + 1
            topics.append(
                TopicSpec(
                    uc_index=current_uc_index,
                    uc_title=current_uc_title,
                    topic_index=topic_index,
                    title=norm,
                    subtopics=infer_subtopics_from_title(norm),
                    explicit_term=current_term,
                    explicit_weeks=explicit_weeks or 1,
                )
            )
            i = j
            continue

        i += 1

    return topics


def parse_syllabus(text: str) -> Syllabus:
    lines = [ln.rstrip() for ln in (text or "").splitlines()]
    course_title = find_labeled_value(lines, "Course Title")
    course_code = find_labeled_value(lines, "Course Code")
    lo_title_lookup: dict[int, str] = {}
    for raw_line in lines:
        norm_line = normalize_spaces(raw_line)
        match = re.match(r"^LO\s*(\d+)\.\s+(.+)$", norm_line, re.IGNORECASE)
        if match:
            lo_title_lookup[int(match.group(1))] = normalize_spaces(match.group(2))

    topic_header_stoppers = {
        "interactive discussion",
        "self-directed",
        "self- directed",
        "blended",
        "e-books",
        "writing materials",
        "lms",
        "internet connections",
        "learning content",
        "methods",
        "presentation",
        "practice",
        "feedback",
        "resources",
        "time/week",
        "orientation",
        "course requirements:",
        "course assessment plan:",
        "grading system:",
        "midterm examination",
        "final examination",
        "teacher’s self reflection of the session:",
        "teacher's self reflection of the session:",
    }
    topic_body_markers = (
        "read key facts",
        "key fact",
        "key facts",
        "let's apply",
        "lets apply",
        "let's exercise",
        "lets exercise",
        "activity ",
    )

    def is_lo_inline(line: str) -> tuple[int, str] | None:
        norm = normalize_spaces(line)
        m = re.match(r"^LO\s*(\d+)\.\s*(.+)$", norm, re.IGNORECASE)
        if not m:
            return None
        return int(m.group(1)), normalize_spaces(m.group(2))

    def is_lo_marker(line: str) -> int | None:
        norm = normalize_spaces(line)
        m = re.match(r"^LO\s*(\d+)\.$", norm, re.IGNORECASE)
        if not m:
            return None
        return int(m.group(1))

    def is_week_line(line: str) -> int | None:
        norm = normalize_spaces(line)
        if not re.match(r"^Week\s+", norm, re.IGNORECASE):
            return None
        return parse_week_count(norm)

    method_markers = {
        "interactive discussion",
        "self-directed",
        "self- directed",
        "blended",
        "read key facts",
        "key fact",
        "key facts",
        "read and understand key topics and learning points",
    }

    def looks_like_topic_title(index: int, current_uc_index: int | None) -> bool:
        if current_uc_index is None:
            return False
        norm = normalize_spaces(lines[index])
        if not norm:
            return False
        lower = norm.lower()
        if lower in topic_header_stoppers:
            return False
        if lower.startswith("course ") or lower.startswith("general ") or lower.startswith("program "):
            return False
        if lower in {"a. orientation", "orientation"}:
            return False
        if lower.startswith("co") or lower.startswith("lo") or lower.startswith("sdg"):
            return False
        if parse_term_label(norm) or is_session_header(norm):
            return False
        if is_week_line(norm) is not None:
            return False
        if re.match(r"^Activity\s+\d+", norm, re.IGNORECASE):
            return False
        if norm.endswith(":"):
            return False

        prev_nonempty = ""
        k = index - 1
        while k >= 0:
            prev_nonempty = normalize_spaces(lines[k])
            if prev_nonempty:
                break
            k -= 1
        prev_lower = prev_nonempty.lower()
        allowed_prev = {
            "time/week",
            "midterm session",
            "final session",
            "midterm examination",
            "final examination",
        }
        if not (
            prev_lower in allowed_prev
            or is_week_line(prev_nonempty) is not None
            or is_lo_inline(prev_nonempty)
            or is_lo_line(prev_nonempty)
        ):
            if prev_lower not in {"resources", "internet connections"}:
                return False

        j = index + 1
        saw_subtopic = False
        saw_table_pattern = False
        saw_plain_subtopics = False
        while j < len(lines):
            nxt = normalize_spaces(lines[j])
            if not nxt:
                j += 1
                continue
            nxt_lower = nxt.lower()
            if is_lo_inline(nxt) or is_lo_line(nxt) or is_session_header(nxt):
                break
            if is_week_line(nxt) is not None:
                break
            if nxt_lower in topic_header_stoppers or nxt_lower.startswith(topic_body_markers):
                break
            if nxt_lower in method_markers or re.match(r"^\d+\.\d+-\d+[:]?", nxt):
                saw_table_pattern = True
                j += 1
                continue
            if clean_bullet(nxt) != nxt:
                saw_subtopic = True
                j += 1
                continue
            saw_plain_subtopics = True
            j += 1
        return saw_subtopic or saw_plain_subtopics or (saw_table_pattern and bool(infer_subtopics_from_title(norm)))

    topics: list[TopicSpec] = []
    current_uc_index: int | None = None
    current_uc_title = ""
    pending_term: str | None = None
    pending_weeks: int | None = None
    i = 0

    while i < len(lines):
        norm = normalize_spaces(lines[i])
        if not norm:
            i += 1
            continue

        session = is_session_header(norm)
        if session:
            pending_term = session
            i += 1
            continue

        term = parse_term_label(norm)
        if term:
            pending_term = term
            i += 1
            continue

        weeks = is_week_line(norm)
        if weeks is not None:
            pending_weeks = weeks
            i += 1
            continue

        lo_inline = is_lo_inline(norm)
        if lo_inline:
            current_uc_index, current_uc_title = lo_inline
            i += 1
            continue

        lo_marker = is_lo_marker(norm)
        if lo_marker is not None:
            current_uc_index = lo_marker
            current_uc_title = lo_title_lookup.get(lo_marker, f"LO {lo_marker}")
            i += 1
            continue

        lo_match = is_lo_line(norm)
        if lo_match:
            if lo_match.lastindex and lo_match.lastindex >= 2 and lo_match.group(2):
                current_uc_index = int(lo_match.group(1))
                current_uc_title = normalize_spaces(lo_match.group(2))
                i += 1
                continue
            current_uc_index = int(lo_match.group(1))
            j = i + 1
            while j < len(lines) and not normalize_spaces(lines[j]):
                j += 1
            current_uc_title = normalize_spaces(lines[j]) if j < len(lines) else f"LO {current_uc_index}"
            i = j + 1
            continue

        parsed_topic = is_topic_line(norm)
        if current_uc_index is not None and parsed_topic:
            topic_title = parsed_topic[1]
            topic_index = len([t for t in topics if t.uc_index == current_uc_index]) + 1
            active_term = pending_term
            active_weeks = pending_weeks
            pending_weeks = None

            subtopics: list[str] = []
            j = i + 1
            while j < len(lines):
                nxt = normalize_spaces(lines[j])
                if not nxt:
                    j += 1
                    continue
                nxt_lower = nxt.lower()
                if is_lo_inline(nxt) or is_lo_line(nxt) or is_session_header(nxt) or is_topic_line(nxt):
                    break
                if is_week_line(nxt) is not None:
                    break
                if nxt_lower in {"subtopics", "subtopics:"}:
                    j += 1
                    continue
                if nxt_lower.startswith("activity") or nxt_lower.startswith("let") or nxt_lower in method_markers:
                    break
                cleaned = clean_bullet(nxt)
                if cleaned and not is_noise_subtopic(cleaned):
                    subtopics.append(cleaned)
                j += 1

            if not subtopics:
                subtopics = infer_subtopics_from_title(topic_title)
                if not subtopics:
                    i += 1
                    continue

            topics.append(
                TopicSpec(
                    uc_index=current_uc_index,
                    uc_title=current_uc_title,
                    topic_index=topic_index,
                    title=topic_title,
                    subtopics=subtopics,
                    explicit_term=active_term,
                    explicit_weeks=active_weeks,
                )
            )
            i = j
            continue

        if looks_like_topic_title(i, current_uc_index):
            topic_title = norm
            topic_index = len([t for t in topics if t.uc_index == current_uc_index]) + 1
            active_term = pending_term
            active_weeks = pending_weeks
            pending_weeks = None

            subtopics: list[str] = []
            j = i + 1
            while j < len(lines):
                nxt = normalize_spaces(lines[j])
                if not nxt:
                    j += 1
                    continue
                nxt_lower = nxt.lower()
                if is_lo_inline(nxt) or is_lo_line(nxt) or is_session_header(nxt):
                    break
                if is_topic_line(nxt):
                    break
                if is_week_line(nxt) is not None:
                    break
                if nxt_lower in topic_header_stoppers or nxt_lower.startswith(topic_body_markers):
                    break
                if nxt_lower in method_markers or re.match(r"^\d+\.\d+-\d+[:]?", nxt):
                    j += 1
                    continue
                if clean_bullet(nxt) != nxt:
                    cleaned = clean_bullet(nxt)
                    if cleaned and not is_noise_subtopic(cleaned):
                        subtopics.append(cleaned)
                    j += 1
                    continue
                if not is_noise_subtopic(nxt):
                    subtopics.append(nxt)
                j += 1
                continue

            if not subtopics:
                subtopics = infer_subtopics_from_title(topic_title)
                if not subtopics:
                    i += 1
                    continue

            topics.append(
                TopicSpec(
                    uc_index=current_uc_index,
                    uc_title=current_uc_title,
                    topic_index=topic_index,
                    title=topic_title,
                    subtopics=subtopics,
                    explicit_term=active_term,
                    explicit_weeks=active_weeks,
                )
            )
            i = j
            continue

        i += 1

    if not course_title:
        course_title = "Unknown Course"
    if not course_code:
        course_code = safe_filename(course_title).upper()
    merged_topics: list[TopicSpec] = []
    for topic in topics:
        if merged_topics:
            prev = merged_topics[-1]
            if (
                prev.uc_index == topic.uc_index
                and prev.title == topic.title
                and prev.subtopics == topic.subtopics
                and prev.explicit_term == topic.explicit_term
            ):
                if prev.explicit_weeks is None:
                    prev.explicit_weeks = topic.explicit_weeks
                elif topic.explicit_weeks is not None:
                    prev.explicit_weeks += topic.explicit_weeks
                continue
        merged_topics.append(topic)
    topics = merged_topics
    table_topics = parse_table_style_topics(lines, topic_header_stoppers=topic_header_stoppers, topic_body_markers=topic_body_markers)
    if table_topics and (
        not topics
        or len(table_topics) > len(topics)
        or len({t.uc_index for t in table_topics}) > len({t.uc_index for t in topics})
    ):
        topics = table_topics
    if not topics:
        raise ValueError("No topics were parsed from the syllabus.")
    return Syllabus(course_title=course_title, course_code=course_code, topics=topics, raw_text=text)


def split_midterm_final_uc_indices(topics: list[TopicSpec]) -> tuple[set[int], set[int]]:
    uc_indices = sorted({t.uc_index for t in topics})
    mid_count = (len(uc_indices) + 1) // 2
    return set(uc_indices[:mid_count]), set(uc_indices[mid_count:])


def ensure_term_assignments(syllabus: Syllabus) -> dict[str, list[TopicSpec]]:
    mid_ucs, fin_ucs = split_midterm_final_uc_indices(syllabus.topics)
    terms = {"MIDTERM": [], "FINALS": []}
    for topic in syllabus.topics:
        if topic.explicit_term in {"MIDTERM", "FINALS"}:
            terms[topic.explicit_term].append(topic)
            continue
        fallback = "MIDTERM" if topic.uc_index in mid_ucs else "FINALS"
        terms[fallback].append(topic)
    if not terms["MIDTERM"]:
        raise ValueError("No topics resolved to MIDTERM.")
    if not terms["FINALS"]:
        raise ValueError("No topics resolved to FINALS.")
    return terms


def pick_objective_verb(topic_title: str) -> str:
    lower = normalize_spaces(topic_title).lower()
    keyword_map = [
        ("introduction", "Explain"),
        ("fundamentals", "Explain"),
        ("principles", "Explain"),
        ("basics", "Explain"),
        ("architecture", "Describe"),
        ("framework", "Describe"),
        ("planning", "Plan"),
        ("plan", "Plan"),
        ("design", "Design"),
        ("model", "Model"),
        ("analysis", "Analyze"),
        ("analytics", "Analyze"),
        ("evaluation", "Evaluate"),
        ("testing", "Test"),
        ("troubleshooting", "Troubleshoot"),
        ("repair", "Troubleshoot"),
        ("configuration", "Configure"),
        ("setup", "Configure"),
        ("deployment", "Deploy"),
        ("implementation", "Implement"),
        ("integration", "Integrate"),
        ("security", "Apply"),
        ("governance", "Apply"),
        ("management", "Manage"),
        ("service", "Manage"),
        ("documentation", "Document"),
        ("reporting", "Present"),
        ("presentation", "Present"),
    ]
    for keyword, verb in keyword_map:
        if keyword in lower:
            return verb
    return "Apply"


def normalize_objective_length(text: str) -> str:
    words = normalize_spaces(text).split()
    fillers = ["effectively", "in", "practical", "workplace", "tasks"]
    fill_index = 0
    while len(words) < 10:
        words.append(fillers[fill_index % len(fillers)])
        fill_index += 1
    if len(words) > 20:
        words = words[:20]
    return " ".join(words)


def build_objective(topic_title: str, subtopics: list[str]) -> str:
    title = normalize_spaces(topic_title)
    clean_subtopics = [clean_subtopic_phrase(s) for s in subtopics if clean_subtopic_phrase(s)]
    verb = pick_objective_verb(title)

    if len(clean_subtopics) >= 2:
        candidate = f"{verb} {title} through {clean_subtopics[0]} and {clean_subtopics[1]} in practical information systems work"
    elif len(clean_subtopics) == 1:
        candidate = f"{verb} {title} through {clean_subtopics[0]} in practical information systems work"
    else:
        candidate = f"{verb} {title} in practical information systems work using course-relevant methods"

    return normalize_objective_length(candidate)


def compute_item_counts(days: list[int], total_items: int, rng: random.Random) -> list[int]:
    total_days = sum(days)
    if total_days <= 0:
        raise ValueError("Total number of days must be positive.")
    counts = [round(total_items * d / total_days) for d in days]
    while sum(counts) > total_items:
        candidates = [i for i, count in enumerate(counts) if count > 0]
        counts[rng.choice(candidates)] -= 1
    while sum(counts) < total_items:
        counts[rng.randrange(len(counts))] += 1
    return counts


def allocate_counts_with_caps(target: int, caps: list[int], rng: random.Random) -> list[int]:
    if target < 0:
        raise ValueError("Allocation target cannot be negative.")
    if target == 0:
        return [0 for _ in caps]
    if sum(caps) < target:
        raise ValueError("Allocation target exceeds available capacity.")

    total_cap = sum(caps)
    provisional: list[int] = []
    fractions: list[tuple[float, int]] = []
    assigned = 0
    for index, cap in enumerate(caps):
        if cap <= 0:
            provisional.append(0)
            fractions.append((0.0, index))
            continue
        raw = target * cap / total_cap
        base = min(cap, int(raw))
        provisional.append(base)
        fractions.append((raw - base, index))
        assigned += base

    remaining = target - assigned
    if remaining > 0:
        for _, index in sorted(fractions, key=lambda item: (item[0], rng.random()), reverse=True):
            if remaining <= 0:
                break
            if provisional[index] >= caps[index]:
                continue
            provisional[index] += 1
            remaining -= 1

    while remaining > 0:
        candidates = [i for i, cap in enumerate(caps) if provisional[i] < cap]
        if not candidates:
            raise ValueError("Could not complete capped allocation.")
        chosen = rng.choice(candidates)
        provisional[chosen] += 1
        remaining -= 1

    return provisional


def distribute_level_counts(topic_item_counts: list[int], term_name: str, rng: random.Random) -> list[tuple[int, int, int]]:
    combined_ratio = 0.30 if term_name == "MIDTERM" else 0.20
    total_items = sum(topic_item_counts)
    kc_target = round(total_items * combined_ratio)
    knowledge_target = (kc_target + 1) // 2
    comprehension_target = kc_target // 2

    knowledge_counts = allocate_counts_with_caps(knowledge_target, topic_item_counts, rng)
    remaining_caps = [total - knowledge for total, knowledge in zip(topic_item_counts, knowledge_counts, strict=True)]
    comprehension_counts = allocate_counts_with_caps(comprehension_target, remaining_caps, rng)

    out: list[tuple[int, int, int]] = []
    for total, knowledge, comprehension in zip(topic_item_counts, knowledge_counts, comprehension_counts, strict=True):
        application = total - knowledge - comprehension
        out.append((knowledge, comprehension, application))
    return out


def build_term_plans(syllabus: Syllabus, seed: int) -> dict[str, list[TermTopicPlan]]:
    resolved_terms = ensure_term_assignments(syllabus)
    term_plans: dict[str, list[TermTopicPlan]] = {}
    for offset, term_name in enumerate(["MIDTERM", "FINALS"], start=1):
        topics = resolved_terms[term_name]
        plans = [
            TermTopicPlan(
                uc_index=topic.uc_index,
                topic_index=topic.topic_index,
                title=topic.title,
                subtopics=topic.subtopics,
                number_of_days=topic.explicit_weeks or 1,
                objective=build_objective(topic.title, topic.subtopics),
            )
            for topic in topics
        ]
        rng = random.Random(seed + offset)
        item_counts = compute_item_counts([p.number_of_days for p in plans], total_items=50, rng=rng)
        level_counts = distribute_level_counts(item_counts, term_name=term_name, rng=rng)
        counter = 1
        for plan, item_count, (knowledge, comprehension, application) in zip(plans, item_counts, level_counts, strict=True):
            plan.item_count = item_count
            plan.knowledge_count = knowledge
            plan.comprehension_count = comprehension
            plan.application_count = application
            plan.k_array = list(range(counter, counter + knowledge))
            counter += knowledge
            plan.c_array = list(range(counter, counter + comprehension))
            counter += comprehension
            plan.a_array = list(range(counter, counter + application))
            counter += application
        term_plans[term_name] = plans
    return term_plans


def array_text(values: Iterable[int]) -> str:
    return ", ".join(str(v) for v in values)


def sanitize_xml_text(text: str) -> str:
    # Excel worksheet XML rejects control chars even when the rest of the package is valid.
    cleaned = []
    for ch in text:
        code = ord(ch)
        if code in (0x9, 0xA, 0xD) or code >= 0x20:
            cleaned.append(ch)
    return "".join(cleaned)


def split_cell_ref(cell_ref: str) -> tuple[str, int]:
    match = re.fullmatch(r"([A-Z]+)(\d+)", cell_ref)
    if not match:
        raise ValueError(f"Unsupported cell reference: {cell_ref}")
    return match.group(1), int(match.group(2))


def shift_row_refs(text: str, start_row: int, offset: int) -> str:
    def repl(match: re.Match[str]) -> str:
        col = match.group(1)
        row = int(match.group(2))
        if row >= start_row:
            row += offset
        return f"{col}{row}"

    return re.sub(r"([A-Z]+)(\d+)", repl, text)


def expand_topic_rows(root: ET.Element, topic_count: int) -> tuple[int, int]:
    topic_row_start = 13
    topic_row_capacity = 7
    topic_row_end = topic_row_start + topic_row_capacity - 1
    totals_row = topic_row_end + 1
    items_total_row = totals_row + 1
    extra_rows = max(0, topic_count - topic_row_capacity)
    if extra_rows == 0:
        return totals_row, items_total_row

    sheet_data = root.find(f"{{{MAIN_NS}}}sheetData")
    if sheet_data is None:
        raise ValueError("Worksheet is missing sheetData.")

    rows = sheet_data.findall(f"{{{MAIN_NS}}}row")
    row_nodes = {int(row.get("r", "0")): row for row in rows}
    template_row = row_nodes.get(topic_row_end)
    if template_row is None:
        raise ValueError("Could not locate the last topic row in the TOS template.")

    for row in sorted(rows, key=lambda node: int(node.get("r", "0")), reverse=True):
        current_row = int(row.get("r", "0"))
        if current_row < totals_row:
            continue
        new_row = current_row + extra_rows
        row.set("r", str(new_row))
        for cell in row.findall(f"{{{MAIN_NS}}}c"):
            col, _ = split_cell_ref(cell.get("r", ""))
            cell.set("r", f"{col}{new_row}")
            formula = cell.find(f"{{{MAIN_NS}}}f")
            if formula is not None:
                if formula.get("ref"):
                    formula.set("ref", shift_row_refs(formula.get("ref", ""), totals_row, extra_rows))
                if formula.text:
                    formula.text = shift_row_refs(formula.text, totals_row, extra_rows)

    insert_after = row_nodes[topic_row_end]
    insert_index = list(sheet_data).index(insert_after) + 1
    for extra_index in range(1, extra_rows + 1):
        new_row_num = topic_row_end + extra_index
        new_row = copy.deepcopy(template_row)
        new_row.set("r", str(new_row_num))
        for cell in new_row.findall(f"{{{MAIN_NS}}}c"):
            col, _ = split_cell_ref(cell.get("r", ""))
            cell.set("r", f"{col}{new_row_num}")
        sheet_data.insert(insert_index, new_row)
        insert_index += 1

    merge_cells = root.find(f"{{{MAIN_NS}}}mergeCells")
    if merge_cells is not None:
        existing_refs = {merge.get("ref", "") for merge in merge_cells.findall(f"{{{MAIN_NS}}}mergeCell")}
        for merge in merge_cells.findall(f"{{{MAIN_NS}}}mergeCell"):
            ref = merge.get("ref", "")
            if ref:
                merge.set("ref", shift_row_refs(ref, totals_row, extra_rows))
        for extra_index in range(1, extra_rows + 1):
            row_num = topic_row_end + extra_index
            for ref in [f"C{row_num}:E{row_num}", f"F{row_num}:I{row_num}"]:
                if ref in existing_refs:
                    continue
                merge_node = ET.SubElement(merge_cells, f"{{{MAIN_NS}}}mergeCell")
                merge_node.set("ref", ref)
                existing_refs.add(ref)
        merge_cells.set("count", str(len(merge_cells.findall(f"{{{MAIN_NS}}}mergeCell"))))

    dimension = root.find(f"{{{MAIN_NS}}}dimension")
    if dimension is not None and dimension.get("ref"):
        start_ref, end_ref = dimension.get("ref", "").split(":")
        end_col, end_row = split_cell_ref(end_ref)
        dimension.set("ref", f"{start_ref}:{end_col}{end_row + extra_rows}")

    return totals_row + extra_rows, items_total_row + extra_rows


def find_cell(root: ET.Element, cell_ref: str) -> ET.Element:
    for cell in root.findall(f".//{{{MAIN_NS}}}c"):
        if cell.get("r") == cell_ref:
            return cell
    raise KeyError(f"Cell not found in template: {cell_ref}")


def clear_cell_value(cell: ET.Element) -> None:
    for child in list(cell):
        if child.tag in {f"{{{MAIN_NS}}}f", f"{{{MAIN_NS}}}v", f"{{{MAIN_NS}}}is"}:
            cell.remove(child)


def set_cell_string(root: ET.Element, cell_ref: str, text: str) -> None:
    cell = find_cell(root, cell_ref)
    clear_cell_value(cell)
    cell.set("t", "inlineStr")
    is_node = ET.SubElement(cell, f"{{{MAIN_NS}}}is")
    t_node = ET.SubElement(is_node, f"{{{MAIN_NS}}}t")
    t_node.text = sanitize_xml_text(text)


def set_cell_number(root: ET.Element, cell_ref: str, value: int | float) -> None:
    cell = find_cell(root, cell_ref)
    clear_cell_value(cell)
    cell.attrib.pop("t", None)
    v_node = ET.SubElement(cell, f"{{{MAIN_NS}}}v")
    v_node.text = str(value)


def ensure_sheet_namespace_declarations(xml_bytes: bytes) -> bytes:
    text = xml_bytes.decode("utf-8")
    if 'mc:Ignorable="x14ac xr xr2 xr3"' in text:
        if 'xmlns:xr2="' not in text:
            text = text.replace(
                f'xmlns:xr="{XR_NS}"',
                f'xmlns:xr="{XR_NS}" xmlns:xr2="{XR2_NS}"',
                1,
            )
        if 'xmlns:xr3="' not in text:
            text = text.replace(
                f'xmlns:xr2="{XR2_NS}"',
                f'xmlns:xr2="{XR2_NS}" xmlns:xr3="{XR3_NS}"',
                1,
            )
    return text.encode("utf-8")


def write_tos_workbook(
    template_path: Path,
    output_path: Path,
    *,
    course_code: str,
    course_title: str,
    term_name: str,
    plans: list[TermTopicPlan],
) -> None:
    total_days = sum(plan.number_of_days for plan in plans)
    with zipfile.ZipFile(template_path, "r") as zin:
        root = ET.fromstring(zin.read(SHEET_XML_PATH))
        totals_row, items_total_row = expand_topic_rows(root, len(plans))

        set_cell_string(root, "B8", f"{course_code} - {course_title}")
        set_cell_string(root, "B9", "Midterm Examination" if term_name == "MIDTERM" else "Finals Examination")

        for row_num, plan in enumerate(plans, start=13):
            set_cell_string(root, f"B{row_num}", str(row_num - 12))
            set_cell_string(root, f"C{row_num}", plan.title)
            set_cell_string(root, f"F{row_num}", plan.objective)
            set_cell_string(root, f"J{row_num}", array_text(plan.k_array))
            set_cell_string(root, f"K{row_num}", array_text(plan.c_array))
            set_cell_string(root, f"L{row_num}", array_text(plan.a_array))
            set_cell_number(root, f"M{row_num}", plan.number_of_days)
            set_cell_number(root, f"N{row_num}", round((plan.number_of_days / total_days) * 100, 2))
            set_cell_number(root, f"O{row_num}", round(plan.number_of_days / total_days, 4))
            set_cell_number(root, f"P{row_num}", plan.item_count)

        for row_num in range(13 + len(plans), 20):
            for col in ["C", "F", "J", "K", "L"]:
                set_cell_string(root, f"{col}{row_num}", "")
            for col in ["M", "N", "O", "P"]:
                set_cell_number(root, f"{col}{row_num}", 0)

        set_cell_number(root, f"M{totals_row}", total_days)
        set_cell_number(root, f"N{totals_row}", 100)
        set_cell_number(root, f"O{totals_row}", 1)
        set_cell_number(root, f"P{totals_row}", 50)
        set_cell_number(root, f"P{items_total_row}", 50)

        updated_sheet = ensure_sheet_namespace_declarations(
            ET.tostring(root, encoding="utf-8", xml_declaration=True)
        )
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(output_path, "w") as zout:
            for info in zin.infolist():
                if info.filename == SHEET_XML_PATH:
                    data = updated_sheet
                elif info.filename in {CALCCHAIN_PATH, WORKBOOK_RELS_PATH, CONTENT_TYPES_PATH}:
                    # These are regenerated/filtered below so Excel does not repair stale calc-chain records.
                    continue
                else:
                    data = zin.read(info.filename)
                zout.writestr(info, data)

            # Rewrite workbook rels without calcChain relationship.
            if any(info.filename == WORKBOOK_RELS_PATH for info in zin.infolist()):
                rels_root = ET.fromstring(zin.read(WORKBOOK_RELS_PATH))
                rel_tag = "{http://schemas.openxmlformats.org/package/2006/relationships}Relationship"
                for rel in list(rels_root):
                    if rel.tag == rel_tag and rel.get("Target") == "calcChain.xml":
                        rels_root.remove(rel)
                zout.writestr(WORKBOOK_RELS_PATH, ET.tostring(rels_root, encoding="utf-8", xml_declaration=True))

            # Rewrite content types without calcChain override.
            if any(info.filename == CONTENT_TYPES_PATH for info in zin.infolist()):
                types_root = ET.fromstring(zin.read(CONTENT_TYPES_PATH))
                override_tag = "{http://schemas.openxmlformats.org/package/2006/content-types}Override"
                for node in list(types_root):
                    if node.tag == override_tag and node.get("PartName") == "/xl/calcChain.xml":
                        types_root.remove(node)
                zout.writestr(CONTENT_TYPES_PATH, ET.tostring(types_root, encoding="utf-8", xml_declaration=True))


def build_distractor_pool(term_plans: list[TermTopicPlan], current_topic: TermTopicPlan) -> list[str]:
    pool: list[str] = []
    for plan in term_plans:
        if plan.title != current_topic.title:
            pool.append(plan.title)
        for sub in plan.subtopics:
            if sub not in current_topic.subtopics:
                pool.append(sub)
    return [normalize_spaces(item) for item in pool if normalize_spaces(item)]


def distinct_distractors(pool: list[str], correct: str, rng: random.Random) -> list[str]:
    unique: list[str] = []
    seen = {normalize_spaces(correct).lower()}
    for item in pool:
        key = normalize_spaces(item).lower()
        if key in seen:
            continue
        seen.add(key)
        unique.append(item)
    rng.shuffle(unique)
    out = unique[:3]
    while len(out) < 3:
        out.append(f"Alternative {len(out) + 1}")
    return out


def choice_pack(correct: str, distractors: list[str], rng: random.Random) -> tuple[list[str], str]:
    choices = [correct] + distractors[:3]
    rng.shuffle(choices)
    answer = ["A", "B", "C", "D"][choices.index(correct)]
    return choices, answer


def generate_exam_items_for_topic(
    plan: TermTopicPlan,
    *,
    rng: random.Random,
    distractor_pool: list[str],
) -> list[dict]:
    subtopics = plan.subtopics or [plan.title]
    clean_subtopics = [concise_focus_text(s) for s in subtopics]
    items: list[dict] = []
    def focus_phrase(index: int, *, mode: str = "mixed") -> str:
        primary = clean_subtopics[index % len(clean_subtopics)]
        if mode == "single":
            if len(clean_subtopics) == 1:
                singles = [
                    primary,
                    f"the concept of {primary}",
                    f"the use of {primary}",
                    f"the role of {primary}",
                    f"the correct application of {primary}",
                    f"the practical use of {primary}",
                    f"the correct procedure for {primary}",
                    f"the main purpose of {primary}",
                    f"the proper use of {primary}",
                    f"the key idea behind {primary}",
                ]
                return singles[index % len(singles)]
            singles = [
                primary,
                f"the concept of {primary}",
                f"the use of {primary}",
                f"the role of {primary}",
            ]
            return singles[index % len(singles)]
        if len(clean_subtopics) == 1:
            return primary
        secondary = clean_subtopics[(index + 1) % len(clean_subtopics)]
        if normalize_spaces(primary).lower() == normalize_spaces(secondary).lower():
            return primary
        variants = [
            f"{primary} together with {secondary}",
            f"{primary} as it relates to {secondary}",
            f"the relationship between {primary} and {secondary}",
            f"{secondary} in connection with {primary}",
        ]
        return variants[index % len(variants)]

    def add_item(level: str, question: str, correct: str) -> None:
        correct_choice = option_phrase(correct, mode=level)
        distractor_choices = [option_phrase(item, mode=level) for item in distinct_distractors(distractor_pool, correct, rng)]
        choices, answer = choice_pack(correct_choice, distractor_choices, rng)
        items.append(
            {
                "question": question,
                "a": choices[0],
                "b": choices[1],
                "c": choices[2],
                "d": choices[3],
                "answer": answer,
                "level": level,
                "topic": plan.title,
            }
        )

    knowledge_stems = [
        "Which statement best describes the competency covered in {subject} during the lesson on {area}?",
        "A student is reviewing {area}. Which option correctly identifies what {subject} is about?",
        "Which idea best represents the lesson focus of {subject} in {area}?",
        "When studying {area}, which statement best defines {subject}?",
        "Which option best summarizes the skill expected in {subject} under {area}?",
        "During class discussion on {area}, which statement best explains the focus of {subject}?",
    ]
    comprehension_stems = [
        "Why is {subject} important when students are learning {area}?",
        "Which statement best explains why {subject} matters in {area}?",
        "How does understanding {subject} improve a student's grasp of {area}?",
        "Which explanation best shows the value of {subject} in the lesson on {area}?",
        "Why should a student understand {subject} before moving further in {area}?",
        "Which option best explains the purpose of {subject} in {area}?",
    ]
    application_stems = [
        "During {context} in {area}, which action best shows correct use of {subject} for {goal}?",
        "A student is working on {area} during {context}. Which step best applies {subject} to achieve {goal}?",
        "In a practical task about {area} during {context}, which action best demonstrates {subject} while addressing {goal}?",
        "During a classroom exercise in {area} for {goal}, which response most clearly applies {subject} while {context}?",
        "A learner is solving a problem in {area} during {context}. Which action best uses {subject} to support {goal}?",
        "In a hands-on assessment for {area} while {context}, which step best demonstrates {subject} while working toward {goal}?",
        "A student is asked to perform {area} during {context}. Which action best applies {subject} in order to maintain {goal}?",
        "Which classroom action best uses {subject} during {context} in {area} to achieve {goal}?",
        "In a skills check on {area} during {context}, which response shows the strongest practical use of {subject} for {goal}?",
    ]
    contexts = [
        "writing a short program",
        "reviewing sample code",
        "drawing a design solution",
        "debugging a class activity",
        "checking program behavior",
        "planning a software solution",
        "analyzing a case example",
        "preparing a laboratory output",
    ]
    goals = [
        "correct program behavior",
        "clear software structure",
        "better code reuse",
        "safe error handling",
        "accurate system modeling",
        "proper object interaction",
        "efficient execution",
        "clean database access",
        "maintainable design",
        "clear architectural separation",
    ]
    for idx in range(plan.knowledge_count):
        subject = focus_phrase(idx, mode="single")
        stem = knowledge_stems[(idx + plan.topic_index) % len(knowledge_stems)]
        add_item("knowledge", stem.format(subject=subject, area=plan.title), clean_subtopics[idx % len(clean_subtopics)])

    for idx in range(plan.comprehension_count):
        subject = focus_phrase(idx + 1, mode="single")
        stem = comprehension_stems[(idx + plan.uc_index) % len(comprehension_stems)]
        add_item("comprehension", stem.format(subject=subject, area=plan.title), clean_subtopics[idx % len(clean_subtopics)])

    for idx in range(plan.application_count):
        subject = focus_phrase(idx + 2, mode="single" if len(clean_subtopics) <= 4 else "mixed")
        stem = application_stems[(idx + plan.uc_index + plan.topic_index) % len(application_stems)]
        context = contexts[(idx + plan.topic_index + plan.uc_index) % len(contexts)]
        goal = goals[(idx + plan.uc_index + len(clean_subtopics)) % len(goals)]
        question = stem.format(subject=subject, area=plan.title, context=context, goal=goal)
        add_item("application", question, clean_subtopics[idx % len(clean_subtopics)])

    return items


def generate_exam_for_term(term_name: str, term_plans: list[TermTopicPlan], seed: int) -> list[dict]:
    required_tokens = {
        token
        for plan in term_plans
        for token in exam_builder.tokenize(f"{plan.title} {' '.join(plan.subtopics)}")
        if len(token) >= 4
    }
    last_error: Exception | None = None
    for attempt in range(6):
        rng = random.Random(seed + attempt * 997)
        mcqs: list[dict] = []
        for plan in term_plans:
            pool = build_distractor_pool(term_plans, plan)
            mcqs.extend(generate_exam_items_for_topic(plan, rng=rng, distractor_pool=pool))
        seen_questions: dict[str, int] = {}
        variant_phrases = [
            "Choose the best answer based on the lesson focus.",
            "Select the most appropriate response for the situation.",
            "Base your answer on correct classroom practice.",
            "Pick the response that best matches the required skill.",
            "Consider the most accurate practical response.",
        ]
        for item in mcqs:
            key = exam_builder.normalize(item["question"])
            count = seen_questions.get(key, 0)
            if count:
                phrase = variant_phrases[(count - 1) % len(variant_phrases)]
                item["question"] = f"{item['question']} {phrase}"
                key = exam_builder.normalize(item["question"])
            seen_questions[key] = seen_questions.get(key, 0) + 1
        if len(mcqs) != 50:
            raise ValueError(f"{term_name} exam generation produced {len(mcqs)} items instead of 50.")
        try:
            exam_builder.validate_mcqs(
                [exam_builder.MCQ(question=m["question"], a=m["a"], b=m["b"], c=m["c"], d=m["d"], answer=m["answer"]) for m in mcqs],
                required_tokens,
                strict_relevance=True,
            )
            return mcqs
        except ValueError as exc:
            last_error = exc
    if last_error is not None:
        raise last_error
    raise ValueError(f"{term_name} exam generation failed unexpectedly.")


def write_exam_docx(
    template_path: Path,
    output_path: Path,
    *,
    course_code: str,
    course_title: str,
    term_name: str,
    mcqs: list[dict],
) -> None:
    exam_builder.fill_exam_template(
        template_path,
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
    )


def write_state_json(
    output_path: Path,
    *,
    syllabus_file: str,
    course_code: str,
    course_title: str,
    term_name: str,
    plans: list[TermTopicPlan],
    mcqs: list[dict],
) -> None:
    payload = {
        "syllabus_file": syllabus_file,
        "course_code": course_code,
        "course_title": course_title,
        "term": term_name,
        "topics": [asdict(plan) for plan in plans],
        "mcqs": mcqs,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build MIDTERM/FINALS TOS workbooks and matching 1-50 exams from a syllabus.")
    parser.add_argument("--syllabus", type=Path, default=None, help="Optional syllabus path. Defaults to the first valid file in ./inbox.")
    parser.add_argument("--midterm-tos-template", type=Path, default=MIDTERM_TOS_TEMPLATE)
    parser.add_argument("--finals-tos-template", type=Path, default=FINALS_TOS_TEMPLATE)
    parser.add_argument("--exam-template", type=Path, default=EXAM_TEMPLATE)
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
    if not args.exam_template.exists():
        raise FileNotFoundError(f"Missing exam template: {args.exam_template}")

    syllabus = parse_syllabus(read_syllabus_text(syllabus_path))
    term_plans = build_term_plans(syllabus, seed=args.seed)

    course_safe = safe_filename(syllabus.course_code.upper())
    summary: dict[str, object] = {
        "syllabus_file": syllabus_path.name,
        "course_code": syllabus.course_code,
        "course_title": syllabus.course_title,
        "outputs": {},
    }

    for offset, term_name in enumerate(["MIDTERM", "FINALS"], start=1):
        plans = term_plans[term_name]
        mcqs = generate_exam_for_term(term_name, plans, seed=args.seed + offset * 100)
        tos_template = args.midterm_tos_template if term_name == "MIDTERM" else args.finals_tos_template

        tos_out = OUT_TOS_DIR / f"TOS_{course_safe}_{term_name}.xlsx"
        exam_out = OUT_EXAMS_DIR / f"EXAM_{course_safe}_{term_name}.docx"
        state_out = STATE_DIR / course_safe / f"{term_name}.json"

        write_tos_workbook(
            tos_template,
            tos_out,
            course_code=syllabus.course_code,
            course_title=syllabus.course_title,
            term_name=term_name,
            plans=plans,
        )
        write_exam_docx(
            args.exam_template,
            exam_out,
            course_code=syllabus.course_code,
            course_title=syllabus.course_title,
            term_name=term_name,
            mcqs=mcqs,
        )
        write_state_json(
            state_out,
            syllabus_file=syllabus_path.name,
            course_code=syllabus.course_code,
            course_title=syllabus.course_title,
            term_name=term_name,
            plans=plans,
            mcqs=mcqs,
        )

        summary["outputs"][term_name] = {
            "tos": str(tos_out),
            "exam": str(exam_out),
            "state": str(state_out),
            "topic_count": len(plans),
        }

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
