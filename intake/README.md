# intake/

The landing area for raw reverse engineering tool output.

## Subfolders

- **raw/** — Unprocessed output exactly as the tool produced it. Drop files here immediately after a session. Never edit.
- **processed/** — Files from raw/ that have been read and are being parsed. Once fully processed into findings, remove or archive.

## Workflow

1. Run a tool (Ghidra, CheatEngine, x64dbg, FModel, UHT dump, etc.)
2. Save its output as a file in `raw/`
3. In the next processing pass, read from `raw/`, parse, and write normalized findings to `findings/`
4. Move or delete the raw file when fully processed

## File naming convention

`YYYY-MM-DD-toolname-brief-description.ext`

Examples:
- `2026-05-20-cheatengine-pal-stats-scan.txt`
- `2026-05-20-ghidra-requestadditem-disasm.md`
- `2026-05-20-uht-dump-apalpcharacter-properties.hpp`

## What does NOT go here

- Normalized findings (go to `findings/`)
- Session notes (go to `sessions/`)
- Anything that has already been processed through the pipeline
