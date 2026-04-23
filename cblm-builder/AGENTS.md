## Pre-Check

Before generating content:

- If `./inbox` is empty -> EXIT immediately
- If files exist but are invalid -> move the file to `./failed` and EXIT
- Do not generate anything unless a valid syllabus is detected

## Retry Protection

- NEVER retry a failed file automatically
- If processing fails:
  - move the file to `./failed`
  - do not attempt again automatically
- Do not reprocess files already in `./processed` or `./failed`
- A user-approved `continue` is not an automatic retry; it is a continuation of the same in-progress workflow from saved state

## Controlled Interaction Mode

Do NOT ask unnecessary questions.
Do NOT ask for confirmation when the next step is clear.

Always:
- scan `./inbox`
- process files when the workflow can be completed without cutting corners
- save valid intermediate state before any pause

If no files exist:
- do nothing silently

If the task cannot be completed reliably in one pass without violating the repository rules:
- stop cleanly after saving valid intermediate state
- report what was completed
- report what remains
- report whether it is safe to continue
- wait for the user to reply with `continue`

If the user replies with `continue`:
- resume from the last valid intermediate state
- do not restart from scratch unless the saved state is invalid

# CBLM Builder Standing Orders

You are an autonomous CBLM generation agent.

## Mission
Monitor the workspace for new syllabus files and generate TESDA-style CBLM documents automatically using the modular section templates in `./templates`.

## Workspace Locations
- Input syllabus files: `./inbox`
- Output generated files: `./output`
- Processed syllabus files: `./processed`
- Failed syllabus files: `./failed`
- Section templates:
  - `./templates/00_front_matter.docx`
  - `./templates/10_lo_intro.docx`
  - `./templates/20_learning_experience.docx`
  - `./templates/30_key_facts.docx`
  - `./templates/40_lets_exercise.docx`
  - `./templates/50_lets_apply.docx`

## Supported Inputs
- `.docx`
- `.txt`
- `.md`

## Core Output Rule
- Generate ONE DOCX FILE PER UNIT OF COMPETENCY
- Generate ONE CBLM DOCUMENT by assembling section templates, not by filling one monolithic template

## Unit Sequencing Rule
- Work on one unit at a time
- Do NOT generate all unit payloads in one batch before review
- Complete the current unit's payload, validation, and DOCX generation first
- After one unit is completed successfully, pause and report status unless the user explicitly instructed fully automatic continuation
- When the user says `continue`, proceed to the next unit from the same syllabus
- Move the source syllabus into `./processed` only after all required units for that syllabus are fully completed

## Template Assembly Model

Each CBLM document is assembled in this order:

1. `00_front_matter.docx`
2. For each LO in the current unit:
   - `10_lo_intro.docx`
   - `20_learning_experience.docx`
   - For each content item in that LO:
     - `30_key_facts.docx`
     - `40_lets_exercise.docx`
     - `50_lets_apply.docx`

## Indexing Rules

- `X` = UC index
- `Y` = LO index within the current unit
- `Z` = content index within the current LO
- `{{LO}}` = current LO title
- `{{Contents_Z}}` = current content title
- `{{la_title_z}}` and `{{la_z_*}}` = current Let's Apply content block

Visible numbering such as `Key Facts {{X}}.{{Y}}-{{Z}}` should render like `Key Facts 2.1-2`.

## List Behavior

- List sections in templates may have a fixed maximum number of rows or paragraphs
- Populate only the used rows or paragraphs
- Delete unused rows or paragraphs during generation
- Do not leave unresolved placeholders or blank repeated rows behind

## Payload Model

The production payload is now a structured JSON document for one current unit, not the old fixed `LO_1` / `Contents_1_1` style flat payload.

Required top-level fields:
- `sector`
- `qualification_title`
- `qualification_units`
- `current_unit`

`qualification_units` must list all UCs in the qualification, each with:
- `index`
- `unit_of_competency`
- `module_title`
- `unit_of_competency_code`

`current_unit` must contain:
- `index`
- `unit_of_competency`
- `module_title`
- `next_unit_of_competency`
- `Module_Descriptor`
- `Laboratory`
- `training_materials`
- `learning_outcomes`

Each `learning_outcomes` item must contain:
- `index`
- `title`
- `contents`

Each `contents` item must contain:
- `index`
- `title`
- `key_facts`
- `exercise_questions`
- `answer_key`
- `apply_title`
- `apply_objective`
- `apply_sup_mat`
- `apply_equipment_list`
- `apply_steps_list`
- `apply_assessmentmethod`
- `apply_pc1`
- `apply_pc2`
- `apply_pc3`
- `apply_pc4`
- `apply_pc5`

## Content Rules

For each content item:

### Key Facts
- Minimum 600 words
- Prefer 650-800 words
- Paragraph-based, not bullet-only
- Maintain TESDA instructional tone
- Include:
  1. concept overview
  2. detailed explanation
  3. real-world example
  4. industry/workplace application
  5. summary/reinforcement
- Keep each Key Facts section materially distinct from the others in the same unit
- Anchor each section to its exact content title and subtopics, not just the parent topic
- Vary the explanation angle, examples, workplace context, and summary language across contents
- Avoid generic filler that could fit any content title

### Let's Exercise
- exactly 10 multiple choice questions
- include answer key

### Let's Apply
- one activity block per content item
- exactly 5 performance criteria

## Validation Rules

Before assembling the DOCX:
- validate payload completeness
- validate `Module_Descriptor` is 80-120 words
- validate `Laboratory` is not empty
- validate `training_materials` is not empty
- validate each Key Facts section has at least 600 words
- validate each answer key has 10 items
- validate each Let's Apply section has 5 performance criteria

Run:

`.\.venv\Scripts\python.exe .\tools\check_keyfacts_similarity.py "<payload.json>"`

If redundant Key Facts sections are detected:
- regenerate only the flagged Key Facts sections once
- overwrite the draft payload JSON
- rerun validation

If redundancy still remains after one rewrite:
- treat the unit as failed
- do not assemble the DOCX for that unit

## Tooling Rules

- Use `tools/assemble_cblm.py` as the production assembler for the modular templates
- `tools/fill_cblm.py` is legacy support for the old monolithic template and must not be preferred for the new workflow
- `tools/docx_filler.py` is helper code only

## Processing Rules

For each new syllabus in `./inbox`:
1. Read and extract the course title, all learning outcomes, topics, and subtopics
2. Build structured qualification data
3. For the current unit only, create one draft structured payload JSON
4. Save the draft payload JSON in `./state`
5. Validate the payload and similarity constraints
6. If valid, assemble one DOCX for the current unit only
7. Save generated files in `./output`
8. Pause and report status after each completed unit unless explicit instructions say to continue automatically
9. Move the source syllabus into `./processed` only after all required units are fully completed

If the agent must pause mid-workflow:
- keep the source syllabus in `./inbox`
- keep draft payloads and progress artifacts in `./state`
- do not move the source syllabus to `./processed`
- do not mark the run as successful

## File Naming

Use:

- Unit output: `CBLM_Unit_<n>_<safe_short_title>.docx`
- Full merged output: `CBLM_FULL.docx`

## Runtime Rule

- For long-running terminal commands, use a timeout of up to 600000 ms (10 minutes) when needed

## Throughput Control

- Process ONLY ONE syllabus file per run
- Do not batch process multiple files in a single cycle

## Finalization

After generating all unit-level DOCX files for a syllabus:
- combine them into `./output/CBLM_FULL.docx`
- maintain original unit order
