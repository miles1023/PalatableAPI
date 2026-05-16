# findings/

Normalized findings that have been processed through the ingestion pipeline.

Each file here represents one or more findings in the canonical schema defined in `schemas/FINDING_SCHEMA.md`. Every entry must be traceable to a source in `intake/` or `evidence/`.

## Subfolders

- **pre-migration/** — Data from the project's previous structure. Preserved as-is. Not yet in canonical schema format. Must be processed through the pipeline before being treated as authoritative.

## What belongs here

Findings that are:
- Parsed (not raw tool output)
- Normalized (using the canonical schema fields)
- Assigned to at least one game system and one surface
- Marked with a confidence level

## What does NOT go here

- Raw tool output (goes to `intake/raw/`)
- Session notes (goes to `sessions/`)
- Open questions without evidence (goes to `unknowns/`)
- System-level summary documents (go in `systems/<name>/`)

## File naming

`YYYY-MM-DD-brief-description.md`
One finding per file, or a batch file for related findings from the same session.
