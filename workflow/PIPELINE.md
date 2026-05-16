# PIPELINE.md — RE Finding Ingestion Workflow
# This file defines the exact process a finding travels from raw tool output
# to fully stored canonical knowledge.
# Last updated: 2026-05-15

---

## Overview

```
raw tool output
      ↓
  [STEP 1] INTAKE — save raw output to intake/raw/
      ↓
  [STEP 2] PARSE — read and extract discrete findings
      ↓
  [STEP 3] NORMALIZE — convert to canonical schema format
      ↓
  [STEP 4] DEDUPLICATE — check for existing matching findings
      ↓
  [STEP 5] ASSIGN TO GAME SYSTEM — pick the systems/ folder
      ↓
  [STEP 6] ASSIGN TO SURFACE — record which surface found it
      ↓
  [STEP 7] LINK RELATIONSHIPS — connect to other findings
      ↓
  [STEP 8] MARK CONFIDENCE — set confirmed / inferred / speculated
      ↓
  [STEP 9] REVIEW AND TRIAGE — check completeness, flag open questions
      ↓
  [STEP 10] PROMOTE TO CANONICAL — move to final location, mark complete
```

---

## STEP 1: INTAKE

**What to do:**
Drop raw tool output into `intake/raw/` immediately after a session. Do not edit it.

**File naming:** `YYYY-MM-DD-toolname-brief-description.ext`

**Examples:**
- `2026-05-20-cheatengine-fixedpoint-struct-dissect.txt`
- `2026-05-20-uht-dump-apalpcharacter.hpp`
- `2026-05-20-fmodel-dt-wazadatatable-export.json`
- `2026-05-20-x64dbg-hp-read-breakpoint.md`

**Rules:**
- One file per topic. Do not combine unrelated tool output.
- Raw files are the source of truth. Never modify them after saving.
- If you stopped a session mid-way, note the incomplete state at the top of the file.

---

## STEP 2: PARSE

**What to do:**
Move the raw file to `intake/processed/`. Read it and extract discrete findings.

A discrete finding is one piece of information about one thing:
- "UPalIndividualCharacterParameter.Hp is at offset 0x018 in the struct" → one finding
- "The inner float of FFixedPoint is at offset 0x0" → one finding
- "Hook path /Script/Pal.PalCharacter:OnDeath fires on player death" → one finding

Do not try to extract all findings in one pass if there are many. Extract one group at a time.

**Create a working note at the top of the processed file** recording what you have and have not extracted.

---

## STEP 3: NORMALIZE

**What to do:**
Write each extracted finding as a Markdown file with YAML front matter, using the schema defined in `schemas/FINDING_SCHEMA.md`.

**Start with these required fields:**
- type
- name
- description
- game_system (use "unknown" if not yet sure)
- surface
- source (tool, session, detail)
- confidence
- status (set to "parsed" at this step)

**Place the file in `findings/` for now.**

**Naming:** `YYYY-MM-DD-typename-name.md`

Example: `2026-05-20-memory-offset-fixedpoint-inner-value.md`

---

## STEP 4: DEDUPLICATE

**What to do:**
Before committing a normalized finding, check whether it already exists.

Search for:
- The exact name in existing finding files
- Aliases that match the same thing
- The same offset or address from a different session

**If a duplicate exists:**
- Compare confidence levels. Keep or merge the higher-confidence version.
- If they conflict (different values or addresses), record both in an `unknowns/` file with a note about the discrepancy.
- Do not silently overwrite. Always record the conflict.

**If no duplicate:** proceed.

---

## STEP 5: ASSIGN TO GAME SYSTEM

**What to do:**
Set the `game_system` field to the folder name of the most relevant system from `systems/`.

**Rules:**
- One primary system per finding. If a finding genuinely belongs to two systems equally (rare), put it in the more specific one and add a reference note in the other's README.
- Shared component (e.g., UPalCharacterParameterComponent used by both player and Pal): assign to the system that owns the component, reference from the other.
- If no existing system fits: add the finding to `unknowns/` and create a backlog item in `backlog/` to determine the right system.

---

## STEP 6: ASSIGN TO SURFACE

**What to do:**
Set the `surface` field to the folder name of the surface that revealed this finding.

**Rules:**
- Surface = how you found it, not where it lives. A memory offset found via CheatEngine → `memory-raw`. The same offset found via Ghidra → `ghidra`.
- If the same finding is confirmed via multiple surfaces, list the primary (most authoritative) in the `surface` field and note the others in `relationships` or the description.

---

## STEP 7: LINK RELATIONSHIPS

**What to do:**
Populate the `relationships` field with connections to other findings you know about.

Common relationship types:
- `part of` — this field is part of this struct
- `references` — this DataTable column references this enum
- `depends on` — this offset is only valid if this other condition is true
- `conflicts with` — this contradicts another finding (investigate)
- `same as` — this is the same thing under a different name
- `parent of / child of` — class hierarchy

You do not need to find every relationship at this step. Add what you know.

---

## STEP 8: MARK CONFIDENCE

**What to do:**
Set the `confidence` field based on how this finding was established.

| Evidence | Confidence |
|----------|------------|
| You read a known HP value from memory and CE showed the correct address | confirmed |
| Hook fired when you triggered the expected event | confirmed |
| FModel showed the column and value matches game behavior | confirmed |
| Class name strongly implies purpose; community documentation agrees | inferred |
| Adjacent confirmed field; SDK data without live verification | inferred |
| You think this is probably right but have not verified | speculated |

**Rule:** When in doubt, use the lower confidence level. It is better to verify and upgrade than to mark something confirmed that is wrong.

---

## STEP 9: REVIEW AND TRIAGE

**What to do:**
Read through the finding as if you are seeing it for the first time. Ask:

1. Is everything required filled in?
2. Does the description make sense without context?
3. Are there open questions that should be recorded?
4. Does anything conflict with what you know from other findings?
5. Is the confidence level honest?

**Add `open_questions` entries** for anything that needs follow-up.

**If the finding is incomplete** — missing a required field, confidence is too low to be useful, or there is an unresolved conflict — set status to `raw` or `parsed` and add it to `unknowns/` or `backlog/`.

**Update status:**
- All required fields present, no blocking open questions → `mapped`
- Cross-referenced and verified internally consistent → `reviewed`

---

## STEP 10: PROMOTE TO CANONICAL

**What to do:**
Move the finding file from `findings/` to its permanent location and set status to `complete`.

**Permanent locations:**
- Memory offsets and struct layouts: `memory/offsets/` or `memory/structs/`
- Hook paths and functions: `hooks/confirmed/` (if confirmed) or `hooks/candidates/` (if inferred)
- System-specific findings: `systems/<name>/`
- DataTable columns: `systems/<system-name>/`
- Cross-system findings: `relationships/`

**Update the relevant `systems/<name>/README.md`** to reference the new finding if it fills an open question or adds significant new knowledge.

**Mark status `complete`** only when:
- Confidence is `confirmed` or `inferred` (not `speculated`)
- No blocking open questions
- All required fields populated
- Cross-references checked

---

## Processing Pre-Migration Data

The `findings/pre-migration/` folder contains data from the 2026-05-15 session.
These files are in the old YAML format, not the canonical schema. Process them as follows:

1. Open each file as if it were raw tool output (treat as STEP 2)
2. Extract discrete findings
3. Follow STEPS 3–10 for each

Start with the highest-priority data:
1. `findings/pre-migration/hooks.yml` — confirmed hook paths
2. `findings/pre-migration/entities/UPalIndividualCharacterParameter.yml` — stat fields
3. `intake/processed/2026-05-15-commands-yml-access-chains.md` — confirmed access chains and column names
4. `findings/pre-migration/datatables/DT_PalMonsterParameter.yml` — all 55 columns

---

## Handling Unknowns

If at any step you cannot determine the right value for a required field:

- `game_system`: use `"unknown"` and add to `unknowns/`
- `surface`: use the tool that produced the raw data
- `confidence`: use `speculated` and note why it is uncertain
- `type`: use `"unknown"` — it is better to admit uncertainty than to misclassify

**Never guess at a required field to make a finding look more complete.**
Move incomplete findings to `unknowns/` or `backlog/` rather than force them through.

---

## Batch Processing Rules

When a single tool session produces many findings of the same type (e.g., a full UHT dump):

1. Save the full dump in `intake/raw/`
2. Process in focused batches — one system at a time
3. Record progress in the processed file so interrupted sessions can resume
4. Do not try to process everything in one pass

A partial but accurate finding is better than a rushed but wrong one.
