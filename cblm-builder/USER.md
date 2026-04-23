# User Task Contract

When a syllabus file is available in ./inbox:

- extract course title
- extract all learning outcomes
- extract topics under each learning outcome
- extract subtopics under each topic
- generate one CBLM document per learning outcome
- save and validate each payload before filling the template
- if Key Facts redundancy is detected, regenerate the flagged Key Facts sections once before continuing
- work on one unit at a time instead of generating all unit payloads in one batch
- after finishing one unit, pause for user continuation unless fully automatic continuation was explicitly requested
- fill the official template
- save outputs in ./output
- move processed syllabus files into ./processed
