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

### tools/build_tos_and_exam_from_syllabus.py
Build two TOS workbooks (`MIDTERM`, `FINALS`) from a syllabus and generate matching 50-item exam DOCX files.

Behavior:
- reads the first `.txt`, `.md`, or `.docx` syllabus in `./inbox` by default
- identifies topics and subtopics from the syllabus structure
- resolves topics to `MIDTERM` or `FINALS` using explicit term labels when present; otherwise falls back to the repo’s UC-order split
- reads week labels when present and maps the resulting week count into `No. of Days Taught`
- allocates `No. of Items` proportionally, then adjusts counts so each term totals exactly `50`
- fills `{{topic}}`, `{{objectives}}`, `{{number_of_days}}`, `{{k_array}}`, `{{c_array}}`, and `{{a_array}}` in:
  - `templates/TOS_TEMPLATE_MIDTERMS.xlsx`
  - `templates/TOS_TEMPLATE_FINALS.xlsx`
- generates a matching exam DOCX whose item numbering follows the TOS arrays exactly

Term ratios:
- `MIDTERM`: `K + C = 30%`, `A = 70%`
- `FINALS`: `K + C = 20%`, `A = 80%`

Outputs:
- `output/tos/TOS_<COURSE_CODE>_MIDTERM.xlsx`
- `output/tos/TOS_<COURSE_CODE>_FINALS.xlsx`
- `output/exams/EXAM_<COURSE_CODE>_MIDTERM.docx`
- `output/exams/EXAM_<COURSE_CODE>_FINALS.docx`
- `state/tos/<COURSE_CODE>/MIDTERM.json`
- `state/tos/<COURSE_CODE>/FINALS.json`

Example:
`.\.venv\Scripts\python.exe .\tools\build_tos_and_exam_from_syllabus.py`

### tools/build_tos_plan_from_syllabus.py
Build two TOS workbooks (`MIDTERM`, `FINALS`) from a syllabus and write term state JSON scaffolds without generating MCQs.

Use this when CODEX should author the exam items directly.

State JSON behavior:
- writes `expected_level_counts`
- writes `authoring_requirements`
- preserves `k_array`, `c_array`, and `a_array` so CODEX can align question order to the TOS exactly

Outputs:
- `output/tos/TOS_<COURSE_CODE>_MIDTERM.xlsx`
- `output/tos/TOS_<COURSE_CODE>_FINALS.xlsx`
- `state/tos/<COURSE_CODE>/MIDTERM.json`
- `state/tos/<COURSE_CODE>/FINALS.json`

### tools/scaffold_term_ia_from_syllabus.py
Create term-specific IA payload scaffolds from a syllabus without generating oral questions or acceptable answers.

Use this when CODEX should author the oral questions directly.

Outputs:
- `state/ia_payloads/<COURSE_CODE>/IA_MIDTERM.json`
- `state/ia_payloads/<COURSE_CODE>/IA_FINALS.json`

### tools/render_exam_from_state.py
Render one term exam DOCX from a CODEX-authored term state JSON containing exactly 50 MCQs.

Validation behavior:
- requires each MCQ to include `level=knowledge|comprehension|application`
- enforces that the authored MCQ order matches the TOS numbering arrays exactly
- enforces answer-key variety so the correct option is not overly concentrated on one letter
- rejects long repetitive runs in the answer key pattern
- appends a `MODEL ANSWER KEY` section after the 50-item exam

Example:
`.\.venv\Scripts\python.exe .\tools\render_exam_from_state.py ".\state\tos\<COURSE_CODE>\MIDTERM.json"`

### tools/rebalance_authored_answers.py
Reposition the correct answer across `A/B/C/D` in a CODEX-authored term state JSON without changing the question wording or the correct content.

Use this after CODEX authors the MCQs and before rendering if the answer-key pattern is too concentrated on one letter.

Behavior:
- preserves the existing correct choice text
- redistributes answer letters into a balanced deterministic pattern
- validates the final answer distribution immediately

Example:
`.\.venv\Scripts\python.exe .\tools\rebalance_authored_answers.py ".\state\tos\<COURSE_CODE>\MIDTERM.json"`

### tools/render_term_ia_from_authored_state.py
Render one term-specific IA DOCX from a CODEX-authored IA payload JSON and a CODEX-authored term state JSON.

Validation behavior:
- enforces the same authored MCQ level/order checks used by `render_exam_from_state.py`
- enforces the same answer-key variety checks used by `render_exam_from_state.py`
- renders a TOS snapshot image from `output/tos/TOS_<COURSE_CODE>_<TERM>.xlsx` when available
- inserts that TOS snapshot into the IA before the term exam section
- appends the term exam plus its `MODEL ANSWER KEY` inside the term IA output

Example:
`.\.venv\Scripts\python.exe .\tools\render_term_ia_from_authored_state.py ".\state\ia_payloads\<COURSE_CODE>\IA_MIDTERM.json" ".\state\tos\<COURSE_CODE>\MIDTERM.json"`

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
