# NEXT_SESSION.md — what to do next (in priority order)
# Read this after `RULES.md` at the start of a session.
# Last updated: 2026-05-29

This project is in the **Reverse Engineering** phase. The goal is to map how the game works
internally (memory, events, hooks, data tables), not to design an API yet.

## How to use this file

1. Pick **one** item below (do not multi-task).
2. Follow the pipeline in `workflow/PIPELINE.md` so results don’t get lost.
3. When you finish, write a short handoff note in `sessions/YYYY-MM-DD.md`.

## Priorities

### 1) Confirm `FFixedPoint` inner field name

Why this matters: lots of stats appear to use fixed-point numbers. If we get the inner field wrong,
every “read/write a stat” attempt will be unreliable.

Use these as starting points:
- `memory/structs/FFixedPoint-layout.md`
- `memory/structs/FFixedPoint64-layout.md`
- `intake/processed/2026-05-18-fixedpoint-probe-hp-scale.md`

Done when:
- We can point to a concrete field name (for example `.Value` vs `.RawValue`) and show proof from a 2026 source/tool run.

### 2) Export `DT_WazaDataTable` via FModel + `Mappings.usmap`

Why this matters: Waza (moves/skills) data is a core gameplay system. A clean export gives us a stable
reference point for later mapping.

Done when:
- The exported table is saved under the correct system folder (not under a tool-named folder), and the source/tool details are recorded.

### 3) Run a UHT dump and cross-check pre-migration entity data

Why this matters: it helps confirm which pre-migration entities are still real and what changed.

Done when:
- The dump output is recorded via the intake pipeline, and any mismatches are captured in `unknowns/` instead of silently “fixing” them.

### 4) Find missing event hook paths (death, capture, level-up, etc.)

Why this matters: these events are required for any meaningful modding surface later. Even if we do
nothing with them yet, we need the map.

Done when:
- Candidate hooks are recorded under `hooks/candidates/` with enough detail to reproduce, and confirmed ones are promoted to `hooks/confirmed/`.

### 5) Process pre-migration data into the canonical schema

Why this matters: the older data is useful, but it must be converted into the standard format or it
will stay hard to use and easy to forget.

Start here:
- `findings/pre-migration/README.md`
- `schemas/FINDING_SCHEMA.md`
- `workflow/PIPELINE.md`

Done when:
- A meaningful chunk is converted and placed into the canonical locations (`findings/` + `systems/`/`memory/`/`hooks/`), with confidence/status fields filled in.

## Reminder: out of scope right now

- Do not add anything to `future-api/` (that phase has not started).
- Do not design “what the modder would type”. Just record findings and proof.

