# surfaces/memory-raw/

Raw memory access via CheatEngine (external process).

## What this surface exposes

- Any in-memory value, reflected or not
- Struct layouts for non-reflected types (via Dissect Structure)
- Function addresses (via code scanning)
- Pointer chain resolution
- FFixedPoint inner fields and other non-reflected types

## MCP bridge

`mcp__cheatengine__*` — available in this project. 180+ tools covering memory read/write, AOB scanning, pointer chains, struct dissection, breakpoints.

## REQUIRED CE setting

Settings > Extra > uncheck "Query memory region routines"
This prevents a BSOD on DBVM-protected memory pages in Palworld.

## How to use

1. Launch Palworld
2. Open CheatEngine (or use the CE MCP bridge)
3. Attach to `Palworld-Win64-Shipping.exe`
4. Use AOB scan to find addresses, pointer scans to follow chains
5. Dissect Structure to understand struct layouts

## Address stability

- Absolute addresses change on every game update and (for ASLR regions) on every process restart
- Always use AOB signatures alongside addresses
- Validate addresses at startup via the AOB signature

## Key open question

FFixedPoint inner field: is the value at `.Value` or `.RawValue`? CheatEngine is the tool to confirm this. See `systems/player-character/README.md`.
