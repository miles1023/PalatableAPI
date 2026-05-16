# workflow/

Ingestion pipeline and processing workflow definitions.

## Files

- **PIPELINE.md** — The step-by-step process a finding travels from raw tool output to fully stored canonical knowledge.

## Rules

- Follow the pipeline for every finding. Do not skip steps.
- If a step cannot be completed (e.g., cannot assign to a game system yet), move the finding to `unknowns/` rather than forcing an assignment.
