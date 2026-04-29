# Tool Usage Notes

## tools/assemble_cblm.py
Use this script to assemble one CBLM DOCX from the modular section templates.

Expected arguments:
`.\.venv\Scripts\python.exe .\tools\assemble_cblm.py "<payload.json>" "<output.docx>"`

Optional third argument:
`"<templates_dir>"`

Behavior:
- validates the structured unit payload
- assembles `00_front_matter.docx`
- appends one `10_lo_intro.docx` and one `20_learning_experience.docx` per LO
- appends `30_key_facts.docx`, `40_lets_exercise.docx`, and `50_lets_apply.docx` per content item
- deletes unused fixed-list rows and paragraphs where applicable

## tools/check_keyfacts_similarity.py
Use this script to flag repeated or overly similar Key Facts sections inside a generated payload before DOCX assembly.

Expected arguments:
`.\.venv\Scripts\python.exe .\tools\check_keyfacts_similarity.py "<payload.json>"`

Behavior:
- exit code `0`: no strong repetition detected
- exit code `2`: redundancy detected and the payload should be revised before assembly

## tools/merge_docx.py
Use this script to merge completed unit DOCX files into one `CBLM_FULL.docx`.

Expected arguments:
`.\.venv\Scripts\python.exe .\tools\merge_docx.py "<input1.docx>" "<input2.docx>" ... "<output.docx>"`

## Legacy Tools

### tools/fill_cblm.py
Legacy filler for the old monolithic `CBLM Template.docx`.

Do not prefer this for the new modular workflow.

### tools/docx_filler.py
Lower-level helper code only.

## Exam Generation

### tools/exam_builder.py
Build term exam DOCX files using `templates/EXAM TEMPLATE.docx` and MCQs sourced from unit payloads (`exercise_questions` per content item).

If upstream question items include a hidden `level` field (`knowledge`, `comprehension`, `application`), `tools/exam_builder.py` can enforce the requested taxonomy mix before filling the template.

Example (default terms MIDTERM,FINAL; 50 questions each):
`.\.venv\Scripts\python.exe .\tools\exam_builder.py --course-code "IPE9" --course-title "Enterprise Systems" --payloads ".\state\payloads\IPE9_UC1.json" ".\state\payloads\IPE9_UC2.json" ".\state\payloads\IPE9_UC3.json" ".\state\payloads\IPE9_UC4.json"`

Custom terms:
`.\.venv\Scripts\python.exe .\tools\exam_builder.py --course-code "IPE9" --course-title "Enterprise Systems" --terms "PRELIMINARY,MIDTERM,PRE-FINAL,FINAL" --payloads <payloads...>`

### tools/validate_exam_docx.py
Validate a generated exam DOCX for:
- bracketed provenance tags such as `[UC3-T2-S3-V3]`
- `UC` / `Unit of Competency` mentions in question text
- duplicate or near-duplicate questions
- overused scaffold patterns
- rough 10/10/30 knowledge/comprehension/application balance

Example:
`.\.venv\Scripts\python.exe .\tools\validate_exam_docx.py ".\output\exams\EXAM_IPC7_MIDTERM.docx"`

## Expected Flow

1. Read one syllabus from `./inbox`
2. Extract qualification, units, LOs, and content items
3. Build one structured payload for the current unit
4. Save the draft payload JSON in `./state`
5. Run `check_keyfacts_similarity.py`
6. If flagged, rewrite only the overlapping Key Facts sections once and rerun the checker
7. Assemble the unit DOCX with `assemble_cblm.py` only after validation passes
8. Save results into `./output`
9. Pause after each completed unit unless explicit instructions say to continue automatically
10. Move the source file to `./processed` only after all required units are fully completed
