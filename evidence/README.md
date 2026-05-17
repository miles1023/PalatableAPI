# evidence/

Source tracking and confidence records.

## Purpose

Every finding's confidence level must be justifiable. This folder stores:
- The source of a finding (which tool, which session, which file, which address)
- When confidence was upgraded (inferred → confirmed)
- Game version records (which binary, which hash)
- Contradictory evidence (when two sources disagree)

## Files

- **game-versions.yml** — Version history, local installation mappings, binary hashes, known breaking changes, Mappings.usmap hashes per version
- **source-log.md** — Running log of sources consulted per session

## Confidence levels

| Level | Meaning |
|-------|---------|
| confirmed | Verified directly via tool output (CE read returned expected value, hook fired, etc.) |
| inferred | Deduced from surrounding evidence (class name suggests purpose, adjacent field confirmed) |
| speculated | Reasonable guess with no direct verification |

## Pre-migration data

`findings/pre-migration/` contains data at various confidence levels from the 2026-05-15 session. Confidence was assigned but not all findings were verified via live tools.
