import argparse
from pathlib import Path

from docx2pdf import convert as docx2pdf_convert
from pypdf import PdfWriter


ROOT = Path(__file__).resolve().parents[1]
REGENERATED_ROOT = ROOT / "output" / "regenerated_ia_packages"
DEFAULT_EXPORT_ROOT = REGENERATED_ROOT / "_pdf_exports"
SUBJECT_ORDER = [
    "IPC_1",
    "IPC_2",
    "IPC_3",
    "IPC_4",
    "IPC_5",
    "IPC_6",
    "IPC_7",
    "IPC_8",
    "IPC_9",
    "IPC_10",
    "IPC_11",
    "IPC_12",
    "IPC_13",
    "IPC_14",
    "ICC_1",
    "ICC_2",
    "ICC_3",
    "ICC_4",
    "ICC_5",
    "ICC_6",
]


def convert_docx_to_pdf(docx_path: Path, pdf_path: Path) -> None:
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    docx2pdf_convert(str(docx_path.resolve()), str(pdf_path.resolve()))
    if not pdf_path.exists():
        raise RuntimeError(f"Failed to convert DOCX to PDF: {docx_path}")


def merge_pdfs(pdf_paths: list[Path], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    writer = PdfWriter()
    for pdf_path in pdf_paths:
        writer.append(str(pdf_path))
    with output_path.open("wb") as handle:
        writer.write(handle)
    writer.close()


def subject_docx_paths(subject: str) -> tuple[Path, Path]:
    base = REGENERATED_ROOT / subject / "output" / "ia" / subject
    return base / "IA_MIDTERM.docx", base / "IA_FINALS.docx"


def export_subject(subject: str, export_root: Path) -> tuple[Path, Path, Path]:
    mid_docx, fin_docx = subject_docx_paths(subject)
    if not mid_docx.exists():
        raise FileNotFoundError(f"Missing MIDTERM DOCX for {subject}: {mid_docx}")
    if not fin_docx.exists():
        raise FileNotFoundError(f"Missing FINALS DOCX for {subject}: {fin_docx}")

    subject_root = export_root / subject
    mid_pdf = subject_root / f"{subject}_MIDTERM.pdf"
    fin_pdf = subject_root / f"{subject}_FINALS.pdf"
    combined_pdf = subject_root / f"{subject}_COMBINED_MIDTERM_THEN_FINALS.pdf"

    convert_docx_to_pdf(mid_docx, mid_pdf)
    convert_docx_to_pdf(fin_docx, fin_pdf)
    merge_pdfs([mid_pdf, fin_pdf], combined_pdf)
    return mid_pdf, fin_pdf, combined_pdf


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert regenerated IA DOCX files to PDF, combine per subject, and create a master combined PDF.")
    parser.add_argument("--export-root", type=Path, default=DEFAULT_EXPORT_ROOT)
    parser.add_argument("--subject", action="append", default=[])
    args = parser.parse_args()

    subjects = args.subject or SUBJECT_ORDER
    export_root = args.export_root
    export_root.mkdir(parents=True, exist_ok=True)

    combined_paths: list[Path] = []
    manifest_lines: list[str] = []

    for subject in subjects:
        mid_pdf, fin_pdf, combined_pdf = export_subject(subject, export_root)
        combined_paths.append(combined_pdf)
        manifest_lines.extend(
            [
                f"{subject}\tMIDTERM\t{mid_pdf}",
                f"{subject}\tFINALS\t{fin_pdf}",
                f"{subject}\tCOMBINED\t{combined_pdf}",
            ]
        )

    master_pdf = export_root / "ALL_SUBJECTS_COMBINED_MIDTERM_THEN_FINALS.pdf"
    merge_pdfs(combined_paths, master_pdf)
    manifest_lines.append(f"ALL\tCOMBINED\t{master_pdf}")

    manifest_path = export_root / "manifest.tsv"
    manifest_path.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

    print(f"Export root: {export_root}")
    print(f"Subjects: {len(subjects)}")
    print(f"Master PDF: {master_pdf}")
    print(f"Manifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
