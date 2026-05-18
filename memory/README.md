# memory/

All findings about Palworld's memory layout.

## Subfolders

- **structs/** — Struct and class memory layouts. How fields are arranged inside a class, their sizes and offsets relative to the object base address.
- **offsets/** — Specific confirmed offset records. Each file is one confirmed finding: this address, this field, this version, this AOB signature.

## What belongs here

- Struct dissection output from CheatEngine
- Field offsets confirmed via CheatEngine + x64dbg
- AOB signatures for confirmed fields
- Pointer chains from a base object to a target field
- Non-reflected fields (if a field IS reflected, the primary record goes in the relevant `systems/` folder)

## What does NOT go here

- DataTable column data (goes in `systems/<name>/`)
- Reflected property names (go in `systems/<name>/`)
- Session notes (go in `sessions/`)

## File naming — structs/

`ClassName-layout.md` — e.g., `FFixedPoint-layout.md`, `UPalCharacterParameterComponent-layout.md`

## File naming — offsets/

`YYYY-MM-DD-ClassName-fieldname.md`

## Critical open finding

Resolved on 2026-05-18 via the live UE4SS CXX dump in `Pal.hpp`: `FFixedPoint` has a single `int32 Value` field and `FFixedPoint64` has a single `int64 Value` field. `UPalIndividualCharacterParameter` uses `FFixedPoint64` for HP-family fields, so the old `.RawValue` and float assumptions should be treated as stale.

Additional live runtime evidence from 2026-05-18: the in-game UE4SS probe repeatedly measured `hp_raw=900000` while `UPalIndividualCharacterParameter::GetMaxHP()` returned `900`, which strongly supports a `1000:1` raw-to-whole-number scale for player HP-family `FFixedPoint64.Value` data.
