# Tool Usage Notes

## tools/fill_cblm.py
Use this script to fill the CBLM DOCX template with a prepared JSON payload.

Expected arguments:
`powershell -ExecutionPolicy Bypass -File .\tools\run_fill_cblm.ps1 "<template.docx>" "<payload.json>" "<output.docx>"`

This launcher prefers `.\.venv\Scripts\python.exe` and falls back to `python` on `PATH`, so it avoids the Windows Store alias problem.

## tools/check_keyfacts_similarity.py
Use this script to flag repeated or overly similar `Contents_X_Y_Key_Facts` sections inside a generated payload before filling the DOCX.

Expected arguments:
`.\.venv\Scripts\python.exe .\tools\check_keyfacts_similarity.py "<payload.json>"`

Behavior:
- exit code `0`: no strong repetition detected
- exit code `2`: redundancy detected and the payload should be revised before filling the template

## tools/docx_filler.py
Helper script for lower-level placeholder replacement.

## Expected Flow
1. Read syllabus from ./inbox
2. Extract structure into JSON
3. Build one draft payload per unit of competency
4. Ensure payload uses hierarchical fields:
   - Contents_X_Y
   - Contents_X_Y_Key_Facts
   - Contents_X_Y_LE_MC
   - Contents_X_Y_LE_MC_Answer
   - la_X_Y_*
5. Save the draft payload JSON
6. Run `check_keyfacts_similarity.py`
7. If flagged, rewrite only the overlapping Key Facts sections once and rerun the checker
8. Fill ./templates/CBLM Template.docx using fill_cblm.py only after validation passes
9. Save results into ./output
10. Move processed inputs into ./processed
