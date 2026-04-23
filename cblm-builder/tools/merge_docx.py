from docx import Document
from docxcompose.composer import Composer
import sys


def merge_docs(files, output):
    if not files:
        raise ValueError("No documents to merge.")

    base_doc = Document(files[0])
    composer = Composer(base_doc)

    for file in files[1:]:
        doc = Document(file)
        composer.append(doc)

    composer.save(output)


def main():
    if len(sys.argv) < 4:
        print("Usage: merge_docx.py <input1.docx> <input2.docx> [...inputN.docx] <output.docx>")
        return 1

    *inputs, output = sys.argv[1:]
    merge_docs(inputs, output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
