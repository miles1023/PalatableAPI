# surfaces/x64dbg/

x64dbg — live debugger for the running Palworld process.

## What it exposes

- Exact function parameter values at call time
- Return values
- Call stack at any point
- Register state at any instruction
- Memory at runtime
- Exact timing of when game systems fire

## MCP bridge

`mcp__x64dbg__*` — available in this project. Tools for breakpoints, stepping, register read/write, memory read/write, disassembly, and more.

## Workflow

1. Launch Palworld
2. Attach x64dbg to the process
3. Set breakpoints on addresses found via Ghidra static analysis
4. Trigger the event in-game
5. Inspect registers and stack when breakpoint hits
6. Log findings to `intake/raw/`

## Key uses for this project

- Confirm FFixedPoint inner field (.Value vs .RawValue) — SET A BREAKPOINT ON HP READ
- Confirm function signatures for candidate hook paths
- Find the call path for events not yet hooked (death, capture, level-up)
- Confirm server binary addresses by attaching to the server process

## Important note

Breakpoints pause the game process. Keep sessions focused: one question per session, then resume.

## Status: KNOWN
