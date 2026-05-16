# surfaces/ghidra/

Ghidra — static binary analysis of Palworld-Win64-Shipping.exe.

## What it exposes

- All game functions and their addresses (requires analysis to name them)
- Non-reflected structs and memory layouts
- Virtual function tables (vtables)
- String references that reveal function purpose
- RTTI class names (Run-Time Type Information)
- Cross-references: what calls what

## MCP bridge

`mcp__ghidra__*` — available in this project. Tools for disassembly, function analysis, cross-reference lookup, debugger attach, and more.

## Workflow

1. Import `Palworld-Win64-Shipping.exe` into Ghidra
2. Run auto-analysis (may take 20–30 min for a shipping binary)
3. Find functions by string reference, RTTI name, or cross-reference from known addresses
4. Export disassembly and analysis to `intake/raw/`

## Key uses for this project

- Find function addresses for non-reflected functions (capture event, death event, etc.)
- Confirm field offsets found via CheatEngine
- Understand FFixedPoint layout in the binary
- Find server binary function addresses (which are different from client addresses)

## Community databases

Community members share Ghidra project files with named functions on Discord servers. These save significant analysis time. Look for Palworld modding Discord servers.

## Version notes

All addresses are version-specific to the binary they were found in. Always record the game version and binary hash alongside any address finding.

## Status: KNOWN
