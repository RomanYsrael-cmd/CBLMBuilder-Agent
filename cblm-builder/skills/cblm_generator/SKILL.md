---
name: cblm_generator
description: Generate TESDA-style CBLM DOCX files from modular section templates, one unit at a time.
metadata:
  openclaw:
    requires:
      bins: ["powershell"]
---
## Execution Rule

This is a checkpointed autonomous task.

- Do NOT ask for confirmation
- Do NOT ask how to proceed when the next step is clear
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
- all syllabus learning outcomes
- the topics under each syllabus learning outcome
- the subtopics under each topic

Mapping rule:
- syllabus learning outcome -> CBLM unit of competency
- syllabus topic -> CBLM learning outcome
- syllabus subtopic -> CBLM content item

## Required Output Model

Build one structured payload for the current unit using the schema documented in `BOOTSTRAP.md`.

Interpret that payload as:
- `current_unit` = one syllabus learning outcome
- `current_unit.learning_outcomes[]` = the topics under that syllabus learning outcome
- `current_unit.learning_outcomes[].contents[]` = the subtopics under each topic

Do not build the old flat payload model with:
- `LO_1`
- `Contents_1_1`
- `la_1_1_title`

unless explicitly required for legacy compatibility.

## Generation Requirements

For each content item generate:
1. Key Facts
   - Minimum 600 words
   - Preferably 650-800 words
   - Paragraph-based, not bullet-only
   - Maintain an instructional TESDA-style tone
   - Include:
     1. concept overview
     2. detailed explanation
     3. real-world example
     4. industry/workplace application
     5. summary/reinforcement
   - Keep each Key Facts section materially distinct from the others in the same unit
   - Anchor each section to its exact content title and subtopics
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
   - exactly 5 performance criteria

## Validation

Before assembly, verify:
- required payload fields exist
- `Module_Descriptor` is 80-120 words
- `Laboratory` is not empty
- `training_materials` is not empty
- each Key Facts section has at least 600 words
- each answer key has 10 items
- each Let's Apply block has 5 performance criteria
- Key Facts sections in the same unit are not near-duplicates

Use a draft-first workflow:
- save the payload JSON first
- run validation before assembly
- if the similarity checker flags redundancy, rewrite only the flagged Key Facts sections once
- rerun the checker after the rewrite
- if redundancy still remains, treat the run as failed instead of assembling the DOCX
- if the task cannot be completed reliably in one pass, stop after saving valid intermediate state and wait for `continue`

Authoring rule:
- draft the current unit payload directly from the current syllabus learning outcome, its topics, and their subtopics
- do not use a generic multi-unit generator that mass-produces all payloads with the same rhetorical template
- do not use a batch rewrite script that rewrites every Key Facts field in the same style across units
- do not create local phrase-bank or slot-filling scripts that manufacture Key Facts prose from reusable sentence fragments
- a local helper script may save already-authored JSON, but it must not be the thing that invents the instructional content

## Generation Step

1. Build one structured payload JSON for the current unit
2. Run:
   `.\.venv\Scripts\python.exe .\tools\check_keyfacts_similarity.py "<payload.json>"`
3. If validation passes, run:
   `.\.venv\Scripts\python.exe .\tools\assemble_cblm.py "<payload.json>" "<output.docx>"`

## Finalization

- save outputs in `./output`
- move processed syllabus to `./processed`
- avoid duplicate work on already processed files
- if paused mid-workflow, keep the syllabus in `./inbox` and keep draft payloads in `./state`

## Failure Handling

If extraction or generation fails:
- STOP immediately
- do not attempt regeneration automatically
- mark file as failed

Special case for Key Facts redundancy:
- one rewrite pass is allowed before the unit is considered failed
- do not perform more than one redundancy rewrite cycle
- if the failed draft was produced by a synthetic local prose generator, pause instead of marking the source failed and wait for `continue`

Pause behavior:
- do not claim success for a partial run
- do not silently reduce quality requirements to finish faster
- if the model is about to switch into script-generated prose because the unit is too large, stop before doing that and wait for `continue`
- when paused, report completed work, remaining work, and whether it is safe to continue
- when the user says `continue`, resume from saved state instead of starting over
