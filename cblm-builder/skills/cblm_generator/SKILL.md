---
name: cblm_generator
description: Generate one TESDA-style CBLM DOCX per syllabus learning outcome and fill the CBLM template automatically.
metadata:
  openclaw:
    requires:
      bins: ["powershell"]
---
## Execution Rule

This is a checkpointed autonomous task.

- Do NOT ask for confirmation
- Do NOT ask how to proceed
- Do NOT send unnecessary messages

Immediately execute the workflow when triggered if it can be completed reliably.
If not, pause cleanly after saving valid intermediate state and wait for `continue`.

Unit progression rule:
- work on one unit payload at a time
- do not draft all units in one batch before review
- after one unit is fully validated and its DOCX is generated, pause unless the user explicitly asked for full automatic continuation
- when the user says `continue`, resume with the next unit

# CBLM Generator Skill

Use this skill when a syllabus file exists in `./inbox` and the goal is to generate completed CBLM DOCX files.

## Required Extraction
Read the syllabus and extract:
- course title
- all learning outcomes
- topics under each learning outcome
- subtopics under each topic

## Required Mapping
Map the syllabus to the template as follows:
- Course Title -> `qualification_title`
- One syllabus learning outcome -> one `unit_of_competency` -> one output DOCX
- Topics -> `LO_1`, `LO_2`, `LO_3`
- Subtopics -> `Contents_1_1..Contents_3_3`

## Generation Requirements
For each content generate:
1. Key Facts:
   - Minimum 600 words
   - Preferably 650-800 words
   - Must include explanation, examples, and application context
   - Must be paragraph-based, not bullet-only
   - Maintain an instructional TESDA-style tone
   - Include:
     1. concept overview
     2. detailed explanation
     3. real-world example
     4. industry/workplace application
     5. summary/reinforcement
   - Each Key Facts section must be materially distinct from the others in the same payload
   - Anchor each section to its exact content title and subtopics, not just the parent topic
   - Vary the opening, example, workflow context, and summary language across contents
   - Do not reuse the same sentence pattern with only term substitutions
   - Avoid generic filler that could fit any content title
2. Let's Exercise
   - exactly 10 multiple choice questions
   - answer key
3. Let's Apply
   - Title
   - Performance Objective
   - Supplies/Materials
   - Equipment
   - Steps/Procedure
   - Assessment Method
4. Performance Criteria Checklist
   - exactly 5 criteria

## Template Fit Rules
The template is fixed-width.
- Use up to 3 learning outcomes
- Use up to 3 contents
- Merge closely related items when necessary

## Validation
Before calling the filler script, verify:
- required payload fields exist
- 10 MCQs per exercise
- 5 performance criteria per checklist
- no critical placeholder is missing without a reasonable generated substitute
- Module_Descriptor is 80-120 words
- unit_of_competency_code_X follows `[A-Z]{3}-[A-Z]{3}-[0-9]{3}`
- Laboratory is not empty
- uc_no is an integer from 1 to 4
- Key Facts sections in the same payload are not near-duplicates

Use a draft-first workflow:
- save the payload JSON first
- run validation before filling the template
- if the similarity checker flags redundancy, rewrite only the flagged Key Facts sections once
- rerun the checker after the rewrite
- if redundancy still remains, treat the run as failed instead of filling the DOCX
- if the task cannot be completed reliably in one pass, stop after saving valid intermediate state and wait for `continue`

Authoring rule:
- draft the current unit payload directly from the current learning outcome, topics, and subtopics
- do not use a generic multi-unit generator that mass-produces all payloads with the same rhetorical template
- do not use a batch rewrite script that rewrites every Key Facts field in the same style across units
- ensure the current unit remains materially different in content, examples, and explanation from other units in the syllabus

## Generation Step
Create one JSON payload per unit of competency, then run:

`powershell -ExecutionPolicy Bypass -File .\tools\run_fill_cblm.ps1 "./templates/CBLM Template.docx" "<payload.json>" "<output.docx>"`

This still uses `tools/fill_cblm.py` as the production filler, but routes through the project venv when available.

Before filling the template, run:

`.\.venv\Scripts\python.exe .\tools\check_keyfacts_similarity.py "<payload.json>"`

If the checker flags repetition, rewrite the overlapping Key Facts sections once, save the updated payload, and rerun the checker before filling the DOCX.

## Finalization
- save outputs in `./output`
- move processed syllabus to `./processed`
- avoid duplicate work on already processed files
- if paused mid-workflow, keep the syllabus in `./inbox` and keep draft payloads in `./state`

## Failure Handling

If extraction or generation fails:

- STOP immediately
- do not attempt regeneration
- mark file as failed
- do not loop or retry

Special case for Key Facts redundancy:
- one rewrite pass is allowed before the file is considered failed
- do not perform more than one redundancy rewrite cycle

Pause behavior:
- do not claim success for a partial run
- do not silently reduce quality requirements to finish faster
- when paused, report completed work, remaining work, and whether it is safe to continue
- when the user says `continue`, resume from saved state instead of starting over
