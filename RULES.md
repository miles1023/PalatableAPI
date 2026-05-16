# RULES.md — Session Continuation Rules
# Read this at the start of every session before doing anything else.
# Last updated: 2026-05-15

---

## What this project is

We are reverse engineering Palworld to build a complete, accurate map of its internal
systems: memory, functions, entities, events, hooks, server interfaces, and any other
surface that can be observed or controlled externally.

That map will be used later, in a separate phase, to design a plain-English API. That
phase has not started. Do not think about it. Do not shape findings around it.

Your job is to discover and record how the game works internally, organized so nothing
is ever lost or missed.

---

## How to start a session

1. Read `sessions/<most-recent-date>.md` — this tells you what was done last and what to do next
2. Read `backlog/` for any items that need attention
3. Read `unknowns/` for unresolved questions that may be answerable today
4. Pick one focus area — do not hop between topics
5. Work one step at a time through the pipeline (`workflow/PIPELINE.md`)

---

## Project structure

```
survey/         Phase 0 outputs — SURFACES.md and GAME_SYSTEMS.md (the scope)
intake/         Raw tool output landing area
  raw/          Unprocessed. Never edit these files.
  processed/    Files being actively parsed into findings.
findings/       Normalized findings in canonical schema format
  pre-migration/ Old data from 2026-05-15, not yet in canonical format
systems/        One folder per game system (21 total)
surfaces/       One folder per modding surface (14 total)
memory/         Memory struct layouts and confirmed offsets
  structs/      Class and struct memory layouts
  offsets/      Specific confirmed offset records
hooks/          Function hooks and events
  confirmed/    Tested and working hook paths
  candidates/   Suspected but untested hook paths
relationships/  Cross-system dependency maps
unknowns/       Unresolved questions and unclassified findings
evidence/       Source tracking and confidence records
sessions/       Session handoff notes (one per session)
schemas/        Data model definitions (FINDING_SCHEMA.md is the contract)
workflow/       Ingestion pipeline (PIPELINE.md)
backlog/        Prioritized items for future sessions
future-api/     EMPTY — placeholder for the API design phase, not started
```

---

## Where new findings go

Follow the pipeline in `workflow/PIPELINE.md`. Short version:

1. Raw tool output → `intake/raw/`
2. Extract findings → `intake/processed/`
3. Write normalized finding files → `findings/` (using schema from `schemas/FINDING_SCHEMA.md`)
4. Assign to game system and surface
5. Promote to permanent location: `systems/<name>/`, `memory/`, `hooks/confirmed/`, etc.

**Never skip the pipeline.** A finding that is not recorded is a finding that will be re-done.

---

## The canonical schema

Every finding is stored as a Markdown file with YAML front matter. The schema is defined
in `schemas/FINDING_SCHEMA.md`. Required fields:

- type, name, description
- game_system (which system/ subfolder)
- surface (which surface/ subfolder)
- source (tool, session date, detail)
- confidence (confirmed / inferred / speculated)
- status (raw / parsed / mapped / reviewed / complete)

Do not add API-layer fields (command syntax, error codes, backend routing). Those go in
`future-api/` when that phase begins.

---

## Confidence rules

| Level | Evidence required |
|-------|------------------|
| confirmed | Direct verification: CE read returned expected value; hook fired on event; FModel showed column |
| inferred | Deduced from community docs, SDK data, class names, adjacent confirmed fields |
| speculated | Reasonable guess, no direct evidence — mark clearly, do not act on it |

When in doubt, use the lower level. Confirming an inferred finding is straightforward.
Correcting a wrongly-confirmed finding wastes time.

---

## Deduplication

Before writing a new finding, search for existing ones by name and by aliases.

If a conflict exists (two findings describe the same thing differently): record both in
`unknowns/` with a note about the discrepancy. Do not silently overwrite.

---

## How to handle uncertainty

- If you cannot assign a finding to a game system: assign `"unknown"`, add to `unknowns/`
- If you cannot confirm confidence: use `speculated`, add an open question to the finding
- If tool output is ambiguous: record it as-is in `intake/raw/`, add a note in `unknowns/`
- If a finding conflicts with another: document both, do not guess which is right

Unknown things are valid findings. Record them as unknown rather than guessing.

---

## The pre-migration data

`findings/pre-migration/` contains data from 2026-05-15. This data is real but not yet
in canonical schema format. When processing it:
- Treat it as raw input (START at STEP 2 of the pipeline)
- Do not assume it is correct without verifying
- Confidence on these findings was set from community research, not live tool verification
- The highest-priority pre-migration files to process are listed in `workflow/PIPELINE.md`

---

## What is out of scope until the map is complete

Do not do any of the following until the RE map is complete and explicitly signed off:

1. **API design** — no command syntax, no verbs, no grammar files
2. **Backend implementation** — no Python, no Lua, no framework code
3. **SDK or tooling** — no language bindings, no distribution format
4. **Anything in future-api/** — leave that folder empty

If you find yourself thinking about "what the modder would type" or "how to expose this
to users" — stop. Record the raw finding and move on. The API phase comes later.

---

## How to write a good session handoff note

At the end of every session, write `sessions/YYYY-MM-DD.md` with:

1. **Focus** — what this session was trying to accomplish
2. **Tools used** — which MCP bridges or manual tools
3. **Findings** — what was confirmed or discovered (brief summary; full data in findings/)
4. **Failures** — what was tried and did not work (prevents re-trying failed approaches)
5. **Open questions** — what remains unresolved
6. **Next session priorities** — ordered list, most important first

The handoff note is the contract between this session and the next one.

---

## MCP tools available in this project

| Bridge | Purpose |
|--------|---------|
| `mcp__cheatengine__*` | Memory R/W, AOB scanning, struct dissection, pointer chains |
| `mcp__ghidra__*` | Static binary analysis, function addresses, struct layouts |
| `mcp__x64dbg__*` | Live debugging, breakpoints, register inspection, call stacks |

See the relevant `surfaces/<name>/README.md` for setup instructions and known gotchas for each tool.

CE REQUIRED SETTING: Settings > Extra > uncheck "Query memory region routines" (prevents BSOD).

---

## Game version

Current game version as of 2026-05-15: **0.7.1** (released 2025-12-19, UE 5.1.1)

Version 1.0 is upcoming (2026-TBD) and expected to break all hardcoded addresses. When it ships:
- Re-validate all addresses in `memory/offsets/`
- Re-run AOB scans to update signatures
- Re-run UHT dump to check for new/changed reflected properties
- Update Mappings.usmap before running FModel

Version history and binary hashes: `evidence/game-versions.yml`
