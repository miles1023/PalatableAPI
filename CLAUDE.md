# CLAUDE.md
# Read this before doing anything else in this repository.
# Last updated: 2026-05-16

---

## CRITICAL — Communication Style

**The user is non-technical. All explanations must be in plain, non-technical language.**

- Never use jargon without immediately explaining what it means in plain terms.
- Never explain what something IS without also explaining what the user experiences or gains from it.

---

## What This Project Is RIGHT NOW

We are in **Phase: Reverse Engineering**. The goal is to build a complete, accurate map of
Palworld's internal systems — memory, functions, entities, events, hooks, server interfaces,
and every modding surface — before touching any API design.

**The plain-English API comes LAST.** The folder `future-api/` is intentionally empty.
Do not put anything in it. Do not design commands, verbs, or API syntax. That phase has not started.

The old framework code (Python parser, Lua mod, grammar files, knowledge/ YAMLs) was the
pre-RE prototype. It has been superseded by this structured RE capture system. Do not reference
or rebuild it. The pre-migration data from that effort is in `findings/pre-migration/`.

---

## CRITICAL — Training Data Warning

**Palworld training data is approximately 2 years out of date.**
The game was in active beta development and changed constantly. Do not use training data
about Palworld as a reliable source for anything — class names, offsets, hook paths, DataTable
schemas, tool instructions.

Any entry you add from training data must be tagged: `[UNVERIFIED - training data, may be outdated]`

All verified knowledge must come from current 2026 sources in `evidence/sources-2026.md`.

---

## Project Structure

```
survey/           Phase 0 outputs — SURFACES.md and GAME_SYSTEMS.md (the scope)
intake/           Raw tool output landing area
  raw/            Unprocessed. Never edit these files.
  processed/      Files being actively parsed into findings.
findings/         Normalized findings in canonical schema format
  pre-migration/  Old data from 2026-05-15, not yet in canonical format
systems/          One folder per game system (21 total) — organized by GAME SYSTEM, not by tool
surfaces/         One folder per modding surface (14 total)
memory/           Memory struct layouts and confirmed offsets
  structs/        Class and struct memory layouts
  offsets/        Specific confirmed offset records
hooks/            Function hooks and events
  confirmed/      Tested and working hook paths
  candidates/     Suspected but untested hook paths
relationships/    Cross-system dependency maps
unknowns/         Unresolved questions and unclassified findings
evidence/         Source tracking and confidence records (sources-2026.md has verified 2026 sources)
sessions/         Session handoff notes (one per session)
schemas/          Data model definitions (FINDING_SCHEMA.md is the contract)
workflow/         Ingestion pipeline (PIPELINE.md)
backlog/          Prioritized items for future sessions
future-api/       EMPTY — placeholder for the API design phase, not started
```

**Organizing rule:** Findings go in `systems/<game-system>/`. Never create a folder named after
a tool (CheatEngine, Ghidra, x64dbg). The tool is recorded in the `source.tool` field of each finding.

---

## How to Start a Session

1. Read `RULES.md` — session continuation rules
2. Read `NEXT_SESSION.md` — exactly what to do next, in priority order
3. Read `sessions/<most-recent-date>.md` — what was done last
4. Pick ONE priority from NEXT_SESSION.md. Do not hop between topics.
5. Follow the pipeline in `workflow/PIPELINE.md`

---

## Where Findings Go

Every discovery follows this pipeline (defined in `workflow/PIPELINE.md`):

```
raw tool output → intake/raw/ → intake/processed/ → findings/ →
systems/<name>/ or memory/ or hooks/confirmed/ or hooks/candidates/
```

The schema every finding must conform to: `schemas/FINDING_SCHEMA.md`

---

## Current Status (as of 2026-05-16)

- RE scaffolding: COMPLETE (phases 0–5 done)
- survey/SURFACES.md: 14 surfaces documented; RCON confirmed deprecated, Steam Workshop confirmed live
- survey/GAME_SYSTEMS.md: 21 systems documented; all tagged [UNVERIFIED] pending live tool confirmation
- evidence/sources-2026.md: 13 verified 2026 sources recorded
- findings/pre-migration/: pre-RE data (hooks.yml, entity YAMLs, datatable YAMLs, enums.yml) — not yet in canonical format
- Next step: begin RE tool sessions per NEXT_SESSION.md priorities

---

## RE Priorities (see NEXT_SESSION.md for full detail)

1. Confirm FFixedPoint inner field (.Value or .RawValue?) — blocks all stat modification
2. Export DT_WazaDataTable via FModel + Mappings.usmap
3. Run UHT dump, cross-reference pre-migration entity data
4. Find missing event hook paths (death, capture, level-up, etc.)
5. Process pre-migration data into canonical format

---

## MCP Tools Available

| Bridge | Purpose |
|--------|---------|
| `mcp__cheatengine__*` | Memory R/W, AOB scanning, struct dissection, pointer chains |
| `mcp__ghidra__*` | Static binary analysis, function addresses, struct layouts |
| `mcp__x64dbg__*` | Live debugging, breakpoints, register inspection, call stacks |

**CE required setting:** Settings > Extra > uncheck "Query memory region routines" (prevents BSOD).

---

## What Is Out of Scope Until the RE Map Is Complete

Do not do any of the following:

- API design — no command syntax, no verbs, no grammar files
- Backend implementation — no Python, no Lua, no framework code
- SDK or tooling — no language bindings
- Anything in `future-api/` — leave it empty

If you find yourself thinking about "what the modder would type" — stop.
Record the raw finding and move on. The API phase comes later.

---

## Game Version

Current: **0.7.1** (released 2025-12-19, UE 5.1.1)
Palworld 1.0 "World Tree update" is upcoming (2026, no confirmed date). All hardcoded addresses
will change at 1.0. Byte signatures and reflected property names are more likely to survive.

**Python:** C:\Python314\python.exe (3.14.4)
**uv:** C:\Users\bmile\AppData\Roaming\Python\Python314\Scripts\uv.exe
