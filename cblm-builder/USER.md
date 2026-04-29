# User Task Contract

When a syllabus file is available in `./inbox`:

- extract course title
- map the syllabus exactly as:
  - syllabus LO -> CBLM UC
  - syllabus Topic -> CBLM LO
  - syllabus Subtopic -> CBLM Content
- extract all learning outcomes, topics, and subtopics needed for the current unit
- generate one CBLM document per unit of competency
- save and validate one structured unit payload before DOCX assembly
- if Key Facts redundancy is detected, regenerate the flagged Key Facts sections once before continuing
- work on one unit at a time instead of generating all unit payloads in one batch
- after finishing one unit, pause for user continuation unless fully automatic continuation was explicitly requested
- assemble the official CBLM from the modular section templates
- save outputs in `./output`
- move processed syllabus files into `./processed` only after all required units are completed
