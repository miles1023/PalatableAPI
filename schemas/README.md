# schemas/

Data model definitions.

## Files

- **FINDING_SCHEMA.md** — The canonical schema every finding must conform to. This is the contract. All findings in `findings/`, `systems/`, and `memory/` follow this format.

## Rules

- The schema is the contract. Do not add fields that don't belong to it without updating the schema.
- The schema does NOT contain API-layer fields. Those belong to the future-api/ phase.
- If a finding cannot be expressed in the schema, update the schema first, then add the finding.
