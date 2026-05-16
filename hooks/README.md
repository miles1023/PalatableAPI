# hooks/

All findings about game functions, hook points, and events.

## Subfolders

- **confirmed/** — Hook paths that have been tested and are working. Each entry includes the full UE path, what it fires on, authority (client/server/either), and any argument/return info.
- **candidates/** — Suspected hook paths not yet tested. Found via Ghidra analysis, UHT dump inspection, or community reports. Must be tested before moving to confirmed/.

## What belongs here

- UE4SS RegisterHook paths
- UE4SS NotifyOnNewObject paths
- UE4SS StaticFindObject utility paths
- Detour hook addresses (for non-reflected functions via DLL injection)

## What does NOT go here

- DataTable column data
- Memory offsets (go in memory/)
- Session notes (go in sessions/)

## Pre-migration data

`findings/pre-migration/hooks.yml` contains all confirmed hook paths from the 2026-05-15 session. Process these into `confirmed/` as part of the pipeline.
