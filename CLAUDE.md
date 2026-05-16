# PalatableAPI — Claude Code Project Context

This file is auto-read by Claude Code at session start. It is the authoritative reference for
project vision, architecture decisions, open questions, and working philosophy. Keep it current.

---

## What This Project Is

**PalatableAPI** (formerly PALlainEnglish -- "PAL" + "plain English") is a Palworld modding
framework analogous to BakkesMod for Rocket League. Modders type plain-English commands; the
framework handles all Unreal Engine internals, DLL injection, and memory management underneath.

**Core vision (user's own words):** "A framework solves all of that once, centrally. The modder
just says 'I want to change this Pal's attack damage' and the framework already knows how to do
everything else."

**API style examples:**
```
give 10 "Stones" to "PlayerName"
change global carryweight infinite
add global playerinventoryslots 50
set pal "Lamball" health max
```

**Scope:** Full runtime framework -- BOTH in-memory modification AND DLL injection. Not limited
to config/data mods.

---

## This Is a Real API, Not a Mod Bundle

This distinction was made explicitly and must be maintained in all future work.

**What makes it a real API vs a mod bundle:**

A real API defines its contract first -- the stable surface modders code against -- and then
backends implement it underneath. The caller never knows or cares which backend ran. A mod bundle
is the opposite: "call UE4SS this way, call PalSchema that way," and when either changes,
everything breaks.

**The real test:** Can a modder write `give 10 "Stones" to "PlayerName"` and have it work without
knowing whether UE4SS is running, whether there's a DataTable for items, or what
`RequestAddItem`'s signature is? If yes, it's an API. If the answer is "only works if UE4SS is
installed and attached and the game version matches the YAMLs," it's a wrapper.

**Where the design IS genuinely an API:**
- The grammar (`palworld.lark` + `commands.yml`) is defined independent of any backend. The
  same command means the same thing whether it runs through UE4SS reflection, raw memory write,
  or a DataTable patch. The caller does not choose.
- The resolver picks Tier 1 vs Tier 2 automatically based on what is confirmed available for
  that property. Modders never touch offsets.
- Game updates break the knowledge YAMLs (internal mapping), NOT the API surface. The API
  contract is version-stable even when internals change.

**Where it risks becoming a wrapper (watch for these):**
- If every command is a 1:1 thin wrap around a specific UE4SS function (`RequestAddItem` ->
  `give item`), we are just PalSchema with nicer syntax.
- If the DataTable backend literally calls PalSchema, we depend on PalSchema being alive.
- If the grammar is too tied to current Palworld concepts (specific Pal names, current item IDs
  hardcoded), it cannot evolve.
- If the resolver has only one known path per command rather than genuine backend selection.

**The real API work still to do:** The resolver must be truly backend-agnostic. Currently most
commands are mapped to a single known implementation path. The resolver should select among
available backends based on what is confirmed working for the current game version and context.

---

## Palworld Landscape (May 2026)

- 32M+ players across Steam, Xbox, PS5
- Palworld 1.0 confirmed for 2026, labeled "Top Secret" -- major update incoming, expect all
  hardcoded addresses to change; byte signatures more likely to survive than addresses; DataTable
  column names most likely to survive
- Official Steam Workshop mod support in active development but NOT yet shipped
- Current mods: .pak asset replacement or UE4SS scripting mods

**Game version history:**
- 0.7.1 (2025-12-19, UE 5.1.1) -- last verified; broke PalSchema pak redirector
- 1.0 (2026-TBD) -- upcoming, labeled Top Secret by Pocketpair

---

## Competition: PalSchema (Okaetsu)

- Config/data mods only via JSON patches to DataTables
- Breaks on every major game update (broke on 0.7.0)
- One developer, no official backing
- Community asking Pocketpair to adopt it officially
- GitHub: github.com/Okaetsu/PalSchema
- Data format: .schema.json files per DataTable

**How PalatableAPI differs:**
1. Full runtime scope -- live game state, not just data tables
2. Both DLL injection AND in-memory modification
3. Plain-English API surface -- modders never touch raw addresses
4. Systematically discovered -- enumerate every possible mod capability
5. Two-tier access (reflected + direct) -- resilient to updates

---

## Architecture

**Foundation:** UE4SS (Okaetsu fork) handles DLL injection and UE reflection. We build on top
of it. UE4SS is a backend, not a dependency the modder knows about.

**Two-tier property access:**
- Tier 1: Reflected -- UE4SS accesses properties by name (no addresses needed, update-resilient)
- Tier 2: Direct -- raw memory offsets + byte AOB signatures (fallback for non-reflected fields)

**Two execution backends:**
- Runtime backend -- UE4SS Lua mod runs inside the game, receives commands via named pipe IPC
- DataTable backend -- generates PalSchema-compatible JSON patches for static game data

**Project structure:**
```
knowledge/
  entities/         -- runtime objects (APalPlayerCharacter, etc.) -- 11 files
  datatables/       -- static data (DT_PalMonsterParameter, etc.) -- 7 files
  hooks/            -- UE4SS RegisterHook paths
  enums/            -- all game enum values
  sessions/         -- RE session notes
  discovery_index.yml -- auto-generated status dashboard (run reindex.py to refresh)
  versions.yml      -- game version history and breaking changes

grammar/
  palworld.lark     -- formal Lark parse grammar (authoritative -- defines what parses)
  commands.yml      -- verb/property/error definitions (lookup only, not grammar)

framework/
  ue4ss_mod/        -- Lua mod (runs inside game process)
  host/             -- Python CLI (parser, resolver, router, bridge, repl)
  tools/            -- reindex.py, validate.py

docs/api.md         -- what modders read
```

---

## Architecture Decisions -- the WHY

These decisions came out of a formal gap analysis before scaffolding. Do not reverse them
without re-reading the rationale.

### Lark grammar file, not YAML tokens
YAML token lists (verbs.yml, targets.yml, properties.yml) cannot express precedence, optionality,
or grouping. `give 10 "Stones" to "PlayerName"` requires knowing that `10` is a quantity,
`"Stones"` is an item name, and `to "PlayerName"` is a target phrase. None of that structure is
expressible in YAML. Edit `palworld.lark` to add syntax; `commands.yml` is lookup only.

### Single commands.yml (not split verbs/targets/properties)
The three-file split required joining across files to validate one command. `give global` and
`set item health` would both parse successfully and fail silently at runtime because no file
defined verb+target compatibility. One entry in commands.yml per command, all fields populated.

### Property path key for component traversal
A Pal's health is NOT a flat field on APal. It lives in a UHealthComponent attached to the Pal
actor. Flat offset access reads wrong memory silently. Properties use a `path:` key (e.g.
`path: HealthComponent -> CurrentHealth`) alongside the raw offset. If path is unknown, mark
the property `unverified`.

### Per-offset authority field (not class-level context flag)
Palworld dedicated servers are server-authoritative. Writing a player's carry weight client-side
is overwritten by the next server tick. Some fields are safe client-side (cosmetic), others are
not (inventory counts, stats). A coarse `context: multiplayer_safe` flag cannot express this.
Each property has `authority: client | server | either`.

### AOB signature validation + broken_since field
`game_version_confirmed: 0.7.1` records when an offset was last verified, not whether it still
works. Without active validation, users on 0.8.x silently get wrong values. Always include an
AOB signature when adding a raw offset. Framework validates at startup.

### discovery_index.yml as aggregated status dashboard
With 20+ entity files, there is no way to answer "which offsets are unverified?" without
grepping every YAML. `discovery_index.yml` is auto-generated by `reindex.py`. Run it after
editing any entity or datatable YAML. Never edit it manually.

### Inheritance resolution at load time
If APal extends APawn extends AActor, and every child entity duplicates inherited properties,
they drift out of sync. The `parent:` key lets the resolver walk the chain. Add properties
to the base class only -- do not copy to child YAMLs.

### Named pipe IPC between Python host and Lua mod
The Lua mod runs inside the game process. Named pipes are the simplest reliable out-of-process
communication without a custom C++ DLL. **Status: NOT yet implemented in main.lua as of
2026-05-15. This is the next major implementation task.**

---

## Ecosystem Research -- What Was Used to Bootstrap

Sources investigated 2026-05-15 and used to populate the knowledge base:

| Source | What was taken from it |
|--------|----------------------|
| NightFyre/Palworld-Internal | C++ SDK class hierarchy, property names for all entity YAMLs |
| mczubaj/Palworld-Mods | UE4SS Lua hook paths -> hooks.yml |
| DRayX CXX Header Gist | Full enum dump (300+ enums) -> enums.yml |
| PalworldDataTools/PalworldDataExtractor | Additional struct property names |
| Elliesaur/Palworld-Mods | FindAllOf patterns, dynamic item data, hook paths |
| pwmodding.wiki | Tool workflows and UE4SS documentation |
| PalSchema schemas | DT_PalMonsterParameter (55 cols), DT_PalDropItem (41 cols), DT_ItemRecipeDataTable (13 cols), DA_StaticItemDataAsset (20 cols), DT_BuildObjectDataTable (18 cols) |

---

## Current Status (as of 2026-05-15)

- 37 plain-English API commands defined
- 11 entity YAML files with real SDK data
- 7 DataTable YAML files
- Full hooks.yml, enums.yml, grammar files
- Python host: parser, resolver, router, bridge, repl -- all scaffolded
- Lua UE4SS mod: skeleton with player stat handlers, named pipe IPC not yet implemented

**Discovery index summary:**
- Entities: 11 total (4 confirmed, 6 partial, 1 unverified), 71 total TODO items
- DataTables: 7 total (5 confirmed, 1 partial, 1 unverified)
- Total API commands ready: 37

---

## Open Questions / Blockers

1. **DT_WazaDataTable columns** -- 0 confirmed, ~4 estimated; needs FModel export with
   Mappings.usmap. Currently marked `unverified` with 6 TODO items.

2. **EPalTribeID name map** -- ~60% complete; ~60+ entries still need plain-English names.
   Source: PalSchema example mods.

3. **FFixedPoint inner field** -- is it `.Value` or `.RawValue`? Needs CheatEngine live session
   to confirm before any stat modification commands will work reliably.

4. **Server binary hook paths** -- all function addresses are null for server. Server uses
   Palworld-Win64-Shipping-Server.exe with different section layout than client binary.

5. **Level-up, death, capture hook paths** -- not yet found or documented. Needed for event
   hooks in the API.

6. **Named pipe IPC** -- the core IPC mechanism between the Python CLI and the in-game Lua mod
   is not yet implemented. framework/ue4ss_mod/PalatableAPI/Scripts/main.lua has the TODO.

---

## Next Session Priorities (in order)

1. Run FModel with Mappings.usmap to export DT_WazaDataTable column names
2. Run UE4SS UHT generator in-game to confirm all property names against current YAMLs
3. CheatEngine live session -- confirm FFixedPoint field (.Value vs .RawValue)
4. Complete EPalTribeID plain-English name map from PalSchema example mods
5. Implement named pipe IPC in framework/ue4ss_mod/PalatableAPI/Scripts/main.lua
6. Test give_item end-to-end via RequestAddItem

---

## Tools Setup

**MCP Bridges (registered user-scope, available in all Claude Code sessions):**
- `mcp__ghidra__*` -- 225 tools, static analysis (binary not running)
- `mcp__x64dbg__*` -- 40+ tools, live debugger (step through running code)
- `mcp__cheatengine__*` -- 180 tools, memory R/W and AOB scanning

**CE required setting:** Settings > Extra > uncheck "Query memory region routines" (prevents
BSOD on DBVM-protected pages). User must set this manually.

**RE workflow:**
- Ghidra: static analysis, find function addresses, disassemble without running game
- x64dbg: live debugging, breakpoints, step through game code
- CheatEngine: scan for values, read/write memory, find structs while game runs

**Python:** C:\Python314\python.exe (3.14.4)
**uv:** C:\Users\bmile\AppData\Roaming\Python\Python314\Scripts\uv.exe
**All D:\Tools entries are full directory copies, not symlinks.**

---

## Working Rules for This Project

1. The API surface (grammar, commands.yml) is defined before any backend implementation.
   Never let backend capabilities dictate what commands exist.

2. When adding a new property to a knowledge YAML, always fill in: `path:` (component chain),
   `authority:` (client/server/either), an AOB signature, and `discovery_status:`.

3. Run `python framework/tools/reindex.py` after editing any entity or datatable YAML.
   Never edit discovery_index.yml manually.

4. Add properties to base class YAMLs (AActor, APawn) only. The resolver walks parent chains.
   Do not duplicate inherited properties in child YAMLs.

5. Modders read docs/api.md only. Knowledge YAMLs, grammar files, and framework internals are
   not part of the public API and can change freely.

6. ASCII only in AGENTS.md at D:\. discovery_engine.ps1 may read it under Windows-1252.
