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

FFixedPoint is used for HP on both player and Pal characters. The inner field that holds the actual float value is not yet confirmed: `.Value` or `.RawValue`? This blocks all stat modification. Use x64dbg to set a breakpoint on an HP read and inspect the struct layout.
