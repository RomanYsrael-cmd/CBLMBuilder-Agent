When awakened automatically, check `./inbox` for unprocessed syllabus files.

1. Check `./inbox`
2. If empty -> EXIT immediately with no output
3. If a file exists:
- process it according to `AGENTS.md`
- validate draft payloads before filling templates
- if redundant Key Facts are detected, perform one rewrite pass and validate again
- generate one unit at a time
- generate outputs only if the workflow can be completed reliably in the current pass
- if the workflow must pause, keep the source file in `./inbox` and keep drafts in `./state`
- move completed inputs to `./processed` only after the required outputs are fully completed
4. If the file fails -> move it to `./failed` and STOP
5. Do not retry failed files automatically
6. If the user later says `continue`, resume from the last valid saved state
