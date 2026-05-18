from __future__ import annotations

import subprocess
import textwrap
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import ZipFile

from PIL import Image, ImageChops, ImageDraw, ImageFont


NS = {
    "main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "rel": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "pkgrel": "http://schemas.openxmlformats.org/package/2006/relationships",
}


def _parse_ref(ref: str) -> tuple[str, int]:
    letters = []
    digits = []
    for ch in ref:
        if ch.isalpha():
            letters.append(ch)
        elif ch.isdigit():
            digits.append(ch)
    return "".join(letters), int("".join(digits))


def _col_to_num(col: str) -> int:
    value = 0
    for ch in col:
        value = value * 26 + (ord(ch.upper()) - 64)
    return value


def _num_to_col(num: int) -> str:
    out = []
    while num > 0:
        num, rem = divmod(num - 1, 26)
        out.append(chr(65 + rem))
    return "".join(reversed(out))


def _read_shared_strings(zf: ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in zf.namelist():
        return []
    root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
    out = []
    for si in root.findall("main:si", NS):
        text = "".join((node.text or "") for node in si.iterfind(".//main:t", NS))
        out.append(text)
    return out


def _first_sheet_xml(zf: ZipFile) -> ET.Element:
    workbook = ET.fromstring(zf.read("xl/workbook.xml"))
    rels = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
    rid_to_target = {
        rel.attrib["Id"]: rel.attrib["Target"]
        for rel in rels.findall("pkgrel:Relationship", NS)
    }
    first_sheet = workbook.find("main:sheets/main:sheet", NS)
    if first_sheet is None:
        raise ValueError("Workbook does not contain a visible sheet.")
    rid = first_sheet.attrib["{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"]
    target = rid_to_target[rid]
    return ET.fromstring(zf.read("xl/" + target))


def _cell_value(cell: ET.Element, shared: list[str]) -> str:
    cell_type = cell.attrib.get("t")
    if cell_type == "inlineStr":
        node = cell.find("main:is/main:t", NS)
        return (node.text or "") if node is not None else ""
    value = cell.find("main:v", NS)
    if value is None:
        return ""
    raw = value.text or ""
    if cell_type == "s":
        return shared[int(raw)]
    return raw


def _extract_sheet_matrix(xlsx_path: Path) -> tuple[dict[tuple[int, int], str], dict[int, float]]:
    with ZipFile(xlsx_path) as zf:
        shared = _read_shared_strings(zf)
        sheet = _first_sheet_xml(zf)

        widths: dict[int, float] = {}
        cols = sheet.find("main:cols", NS)
        if cols is not None:
            for col in cols.findall("main:col", NS):
                min_col = int(col.attrib["min"])
                max_col = int(col.attrib["max"])
                width = float(col.attrib.get("width", "10"))
                for index in range(min_col, max_col + 1):
                    widths[index] = width

        matrix: dict[tuple[int, int], str] = {}
        sheet_data = sheet.find("main:sheetData", NS)
        if sheet_data is None:
            raise ValueError("Worksheet is missing sheetData.")
        for row in sheet_data.findall("main:row", NS):
            row_num = int(row.attrib["r"])
            for cell in row.findall("main:c", NS):
                col_letters, _ = _parse_ref(cell.attrib["r"])
                col_num = _col_to_num(col_letters)
                matrix[(row_num, col_num)] = _cell_value(cell, shared)
        return matrix, widths


def _extract_workbook_banner(xlsx_path: Path) -> Image.Image | None:
    with ZipFile(xlsx_path) as zf:
        media = sorted(name for name in zf.namelist() if name.startswith("xl/media/"))
        if not media:
            return None
        with zf.open(media[0]) as handle:
            image = Image.open(handle).convert("RGBA")
            image.load()
            return image


def _load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = ["arialbd.ttf", "Arial Bold.ttf"] if bold else ["arial.ttf", "Arial.ttf"]
    for name in candidates:
        try:
            return ImageFont.truetype(name, size=size)
        except Exception:
            continue
    return ImageFont.load_default()


def _find_total_row(matrix: dict[tuple[int, int], str], start_row: int, label_col: int) -> int:
    row = start_row
    while row < start_row + 200:
        value = str(matrix.get((row, label_col), "")).strip().upper()
        if value == "TOTAL":
            return row
        row += 1
    raise ValueError("Could not locate TOTAL row in the TOS workbook.")


def _crop_outer_whitespace(image_path: Path) -> None:
    image = Image.open(image_path).convert("RGB")
    bg = Image.new("RGB", image.size, "white")
    diff = Image.eval(ImageChops.difference(image, bg), lambda px: 255 if px > 10 else 0)
    bbox = diff.getbbox()
    if bbox is None:
        return
    left, top, right, bottom = bbox
    pad = 8
    cropped = image.crop(
        (
            max(0, left - pad),
            max(0, top - pad),
            min(image.width, right + pad),
            min(image.height, bottom + pad),
        )
    )
    cropped.save(image_path)


def _crop_outer_whitespace_image(image: Image.Image) -> Image.Image:
    rgb = image.convert("RGB")
    bg = Image.new("RGB", rgb.size, "white")
    diff = Image.eval(ImageChops.difference(rgb, bg), lambda px: 255 if px > 10 else 0)
    bbox = diff.getbbox()
    if bbox is None:
        return image
    left, top, right, bottom = bbox
    pad = 8
    return image.crop(
        (
            max(0, left - pad),
            max(0, top - pad),
            min(image.width, right + pad),
            min(image.height, bottom + pad),
        )
    )


def _try_export_exact_excel_range(
    xlsx_path: Path,
    output_png: Path,
    *,
    start_row: int,
    end_row: int,
    start_col: str,
    end_col: str,
) -> bool:
    script_path = Path(__file__).with_name("export_excel_range_image.ps1")
    if not script_path.exists():
        return False
    range_address = f"{start_col}{start_row}:{end_col}{end_row}"
    command = [
        "powershell",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        str(script_path),
        "-WorkbookPath",
        str(xlsx_path),
        "-RangeAddress",
        range_address,
        "-OutputPng",
        str(output_png),
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    ok = result.returncode == 0 and output_png.exists() and output_png.stat().st_size > 0
    if ok:
        _crop_outer_whitespace(output_png)
    return ok


def _render_fallback_table(
    matrix: dict[tuple[int, int], str],
    widths: dict[int, float],
    *,
    header_row: int,
    total_row: int,
    start_col: str,
    end_col: str,
) -> Image.Image:
    start_col_num = _col_to_num(start_col)
    end_col_num = _col_to_num(end_col)
    draw_probe = ImageDraw.Draw(Image.new("RGB", (10, 10), "white"))
    header_font = _load_font(22, bold=True)
    body_font = _load_font(18, bold=False)
    total_font = _load_font(20, bold=True)

    logical_cols = [
        ("no", [_col_to_num("B")], "No."),
        ("content", [_col_to_num("C"), _col_to_num("D"), _col_to_num("E")], "Content/Topics"),
        ("objectives", [_col_to_num("F"), _col_to_num("G"), _col_to_num("H"), _col_to_num("I")], "Objectives"),
        ("knowledge", [_col_to_num("J")], "Knowledge"),
        ("comprehension", [_col_to_num("K")], "Comprehension"),
        ("application", [_col_to_num("L")], "Application"),
        ("days", [_col_to_num("M")], "No. of Days Taught"),
        ("pct1", [_col_to_num("N")], "%"),
        ("pct2", [_col_to_num("O")], "%"),
        ("items", [_col_to_num("P")], "No. of Items"),
    ]
    logical_cols = [
        item for item in logical_cols
        if item[1][0] >= start_col_num and item[1][-1] <= end_col_num
    ]

    col_widths: list[int] = []
    for _, cols, _ in logical_cols:
        width = 0
        for col in cols:
            excel_width = widths.get(col, 10.0)
            width += max(55, int(excel_width * 9))
        col_widths.append(width)

    data_rows = list(range(header_row, total_row + 1))
    row_heights: dict[int, int] = {}
    for row_num in data_rows:
        max_lines = 1
        for idx, (_, cols, heading) in enumerate(logical_cols):
            text = heading if row_num == header_row else str(matrix.get((row_num, cols[0]), "") or "").strip()
            wrap_width = max(8, int(col_widths[idx] / 12))
            wrapped = textwrap.wrap(text, width=wrap_width) or [text]
            max_lines = max(max_lines, len(wrapped))
        if row_num == header_row:
            row_heights[row_num] = max(56, max_lines * 26 + 16)
        elif row_num == total_row:
            row_heights[row_num] = max(42, max_lines * 22 + 12)
        else:
            row_heights[row_num] = max(70, max_lines * 22 + 18)

    total_width = 40 + sum(col_widths) + 40
    total_height = 20 + sum(row_heights.values()) + 20
    image = Image.new("RGB", (total_width, total_height), "white")
    draw = ImageDraw.Draw(image)

    x0 = 20
    y = 20
    for row_num in data_rows:
        x = x0
        for idx, (_, cols, heading) in enumerate(logical_cols):
            width = col_widths[idx]
            height = row_heights[row_num]
            fill = "white"
            font = body_font
            if row_num == header_row:
                fill = "#d9e2f3"
                font = header_font
            elif row_num == total_row:
                fill = "#fce4d6"
                font = total_font
            draw.rectangle([x, y, x + width, y + height], outline="#5f5f5f", fill=fill, width=1)

            if row_num == header_row:
                text = heading
            else:
                col = cols[0]
                text = str(matrix.get((row_num, col), "") or "").strip()
                if heading in {"Content/Topics", "Objectives"} and not text:
                    merged_text = [str(matrix.get((row_num, c), "") or "").strip() for c in cols]
                    text = " ".join(part for part in merged_text if part)
            wrapped = "\n".join(textwrap.wrap(text, width=max(8, int(width / 12))) or [text])
            if wrapped.strip():
                bbox = draw_probe.multiline_textbbox((0, 0), wrapped, font=font, spacing=4)
                tw = bbox[2] - bbox[0]
                th = bbox[3] - bbox[1]
                tx = x + 6
                if heading in {"No.", "Knowledge", "Comprehension", "Application", "No. of Days Taught", "%", "No. of Items"}:
                    tx = x + max(6, (width - tw) // 2)
                ty = y + max(6, (height - th) // 2)
                draw.multiline_text((tx, ty), wrapped, fill="black", font=font, spacing=4, align="center")
            x += width
        y += row_heights[row_num]
    return image


def _compose_snapshot(
    *,
    banner: Image.Image | None,
    course_title: str,
    exam_title: str,
    table_image: Image.Image,
    output_png: Path,
) -> Path:
    title_font = _load_font(28, bold=True)
    subtitle_font = _load_font(26, bold=True)
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10), "white"))

    body = _crop_outer_whitespace_image(table_image.convert("RGBA"))
    body_width = body.width
    banner_image = None
    if banner is not None:
        banner_image = _crop_outer_whitespace_image(banner)
        target_width = min(body_width, 900)
        if banner_image.width > target_width:
            target_height = int(banner_image.height * target_width / banner_image.width)
            banner_image = banner_image.resize((target_width, target_height))

    title_bbox = probe.textbbox((0, 0), course_title, font=title_font)
    subtitle_bbox = probe.textbbox((0, 0), exam_title, font=subtitle_font)
    title_height = title_bbox[3] - title_bbox[1]
    subtitle_height = subtitle_bbox[3] - subtitle_bbox[1]

    canvas_width = max(body_width, (banner_image.width if banner_image else 0), title_bbox[2], subtitle_bbox[2]) + 80
    canvas_height = 40 + (banner_image.height if banner_image else 0) + 18 + title_height + 8 + subtitle_height + 20 + body.height + 30
    canvas = Image.new("RGB", (canvas_width, canvas_height), "white")
    draw = ImageDraw.Draw(canvas)

    y = 20
    if banner_image is not None:
        bx = (canvas_width - banner_image.width) // 2
        canvas.paste(banner_image.convert("RGB"), (bx, y))
        y += banner_image.height + 18

    draw.text(((canvas_width - (title_bbox[2] - title_bbox[0])) // 2, y), course_title, fill="black", font=title_font)
    y += title_height + 8
    draw.text(((canvas_width - (subtitle_bbox[2] - subtitle_bbox[0])) // 2, y), exam_title, fill="black", font=subtitle_font)
    y += subtitle_height + 20

    bx = (canvas_width - body.width) // 2
    canvas.paste(body.convert("RGB"), (bx, y))
    output_png.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output_png)
    return output_png


def render_tos_snapshot(
    xlsx_path: Path,
    output_png: Path,
    *,
    start_row: int = 1,
    header_row: int = 12,
    label_col: str = "B",
    start_col: str = "B",
    end_col: str = "P",
) -> Path:
    matrix, widths = _extract_sheet_matrix(xlsx_path)
    label_col_num = _col_to_num(label_col)
    total_row = _find_total_row(matrix, header_row, label_col_num)
    banner = _extract_workbook_banner(xlsx_path)
    course_title = str(matrix.get((8, _col_to_num("B")), "") or "").strip()
    exam_title = str(matrix.get((9, _col_to_num("B")), "") or "").strip()

    output_png.parent.mkdir(parents=True, exist_ok=True)
    temp_body = output_png.with_name(output_png.stem + "__body.png")
    if _try_export_exact_excel_range(
        xlsx_path,
        temp_body,
        start_row=header_row,
        end_row=total_row,
        start_col=start_col,
        end_col=end_col,
    ):
        body_image = Image.open(temp_body).convert("RGBA")
    else:
        body_image = _render_fallback_table(
            matrix,
            widths,
            header_row=header_row,
            total_row=total_row,
            start_col=start_col,
            end_col=end_col,
        ).convert("RGBA")

    try:
        result = _compose_snapshot(
            banner=banner,
            course_title=course_title,
            exam_title=exam_title,
            table_image=body_image,
            output_png=output_png,
        )
    finally:
        if temp_body.exists():
            temp_body.unlink(missing_ok=True)
    return result
