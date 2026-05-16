# NEXT_SESSION.md — RE Tools Session Briefing
# This file tells the next reverse engineering session exactly what to do,
# in what order, and what output to expect.
# Written: 2026-05-15

---

## Before you start

Read `RULES.md` first. Then come back here.

---

## What has been done so far

- Phase 0: Ecosystem survey complete (survey/SURFACES.md, survey/GAME_SYSTEMS.md)
- Phase 1: Old project structure audited and cleaned
- Phase 2: Full folder scaffolding created with README.md in every folder
- Phase 3: Canonical finding schema written (schemas/FINDING_SCHEMA.md)
- Phase 4: Ingestion pipeline written (workflow/PIPELINE.md)
- Phase 5: RULES.md written

Community research from 2026-05-15 is stored in `findings/pre-migration/` (not yet processed to canonical format).

---

## What this session should do

### PRIORITY 1: Confirm FFixedPoint inner field

**Why:** HP modification for both players and Pals is blocked until this is confirmed.
Every stat that uses FFixedPoint (HP, MaxHP) cannot be reliably read or written until
we know whether the inner float is at `.Value` or `.RawValue` (or some other name).

**Tool:** x64dbg or CheatEngine (MCP bridge available)

**How:**
1. Launch Palworld, load into the game with a player
2. Attach x64dbg to `Palworld-Win64-Shipping.exe`
3. Note current HP value on screen (e.g., 100/500)
4. Set a breakpoint on memory reads from the address of the player's HP field
   - Start with CheatEngine: scan for the current HP value as "4-byte float"
   - Narrow down to the single address that changes when you take damage
5. When breakpoint hits, inspect the struct at the base address of UPalIndividualCharacterParameter
6. Look for the FFixedPoint member — it should be at offset ~0x018 or nearby
7. Within that member, the inner float is either the first field (offset 0x0) or second (offset 0x4)
8. Read both; whichever equals the displayed HP value is the confirmed inner field

**Expected output:**
A confirmed finding file for `UPalIndividualCharacterParameter.Hp`:
- The confirmed FFixedPoint inner field name (`.Value` or other)
- The byte offset within FFixedPoint of the inner float
- AOB signature for the HP field

**Save raw output:** `intake/raw/YYYY-MM-DD-x64dbg-fixedpoint-inner-field.md`
**Resulting finding:** `systems/player-character/fixedpoint-inner-field.md`

---

### PRIORITY 2: Export DT_WazaDataTable via FModel

**Why:** The Waza/skill DataTable has 0 confirmed columns beyond 3 basic ones. This is the
largest gap in the static data map.

**Tool:** FModel + Mappings.usmap

**How:**
1. Ensure Mappings.usmap is current for game version 0.7.1
   (Source: github.com/PalworldModding/UsefulFiles)
2. Open FModel, point at Palworld game directory
3. Navigate to: `Pal/Content/Pal/DataTable/`
4. Export DT_WazaDataTable as JSON or CSV
5. Also export DT_WazaMasterLevel while here

**Expected output:**
- Full column list for DT_WazaDataTable (expect 15–30 columns based on comparable game DataTables)
- Full column list for DT_WazaMasterLevel
- Several sample rows showing actual values

**Save raw output:** `intake/raw/YYYY-MM-DD-fmodel-dt-wazadatatable.json`
**Resulting findings:** `systems/combat-waza/` (new finding files for each confirmed column)

---

### PRIORITY 3: Run UHT dump and cross-reference with pre-migration entities

**Why:** The pre-migration entity YAMLs were populated from community SDK data, not from
a live UHT dump of the current game version (0.7.1). We need to confirm that property
names are still correct and check for new properties added since that data was gathered.

**Tool:** UE4SS (run inside Palworld)

**How:**
1. Launch Palworld with UE4SS loaded
2. Open UE4SS console
3. Run: `GenerateUHTCompatibleHeaders()`
4. Output appears in `CXXHeaders/` folder next to game executable
5. Find these specific header files:
   - `APalPlayerCharacter.hpp`
   - `APalCharacter.hpp`
   - `UPalIndividualCharacterParameter.hpp`
   - `UPalCharacterParameterComponent.hpp`
   - `UPalPlayerInventoryData.hpp`

**Cross-reference with pre-migration data:**
For each property in the pre-migration YAMLs (`findings/pre-migration/entities/`):
- Does the property name appear in the UHT dump?
- Are there new properties in the dump that are not in the YAML?
- Are there properties in the YAML that are NOT in the dump (may have been removed)?

**Expected output:**
- Confirmation or correction of all property names in the five priority classes
- List of new properties not currently recorded
- List of properties that may have been removed (mark as broken_since: "0.7.1")

**Save raw output:** `intake/raw/YYYY-MM-DD-uht-dump/` (one .hpp file per class)
**Resulting finding updates:** Update or create finding files in `systems/player-character/` and `systems/pal-character/`

---

### PRIORITY 4: Find missing event hook paths

**Why:** Seven game events have no known hook path (death, capture, level-up, raid,
item pickup, craft complete, fast travel). These block event-driven functionality.

**Tool:** Ghidra (MCP bridge available) + cross-reference with UHT dump

**How:**
For each missing event, search Ghidra for function names containing:
- Death: "OnDeath", "OnDie", "OnKilled", "Death" in class name Pal*
- Capture: "OnCapture", "OnCatch", "Capture", "PalSphere"
- Level-up: "OnLevelUp", "LevelUp", "GainLevel"
- Raid: "OnRaid", "OnAttack", "BaseCampAttack"
- Item pickup: "OnPickup", "OnCollect", "AddItem", "PickItem"
- Craft complete: "OnCraftComplete", "OnProductComplete"
- Fast travel: "OnFastTravel", "OnTeleport", "OnWarp"

**For each candidate found:**
1. Look at the function signature in Ghidra
2. Check if it is a UFunction (reflected) — if yes, it can be hooked via RegisterHook
3. Get the full UE path format: "/Script/Pal.ClassName:FunctionName"
4. Add to `hooks/candidates/` with the source and confidence level

Testing candidates requires UE4SS to RegisterHook and trigger the event in-game.
Save candidates now; test them in a follow-up session.

**Save raw output:** `intake/raw/YYYY-MM-DD-ghidra-event-hook-candidates.md`
**Resulting files:** `hooks/candidates/YYYY-MM-DD-<event>-candidate.md` for each

---

### PRIORITY 5: Process pre-migration data into canonical format

**Why:** The pre-migration data contains real findings that are not yet in the canonical
schema. Processing them makes the map more searchable and usable.

**Start with (in order):**
1. `findings/pre-migration/hooks.yml` → promote confirmed hooks to `hooks/confirmed/`
2. `intake/processed/2026-05-15-commands-yml-access-chains.md` → create finding files for each access chain
3. `findings/pre-migration/datatables/DT_PalMonsterParameter.yml` → create finding files for the 55 columns
4. `findings/pre-migration/enums.yml` → create finding files for confirmed enum values

Follow the pipeline in `workflow/PIPELINE.md` for each.

---

## What NOT to do in this session

- Do not design any API layer, command syntax, or modder-facing interface
- Do not write any Python, Lua, or framework code
- Do not add files to `future-api/`
- Do not process all pre-migration data in one pass — do it in batches, one system at a time
- Do not skip writing intake files — raw tool output must be saved before anything else

---

## Session handoff

At the end of this session, write `sessions/YYYY-MM-DD.md` with:
1. Which of the 5 priorities were completed
2. Any findings confirmed or discovered
3. Any failures or dead ends (prevents re-trying)
4. Updated next session priorities
5. Any new open questions

---

## Quick reference: MCP bridge commands

**CheatEngine (value scan):**
```
mcp__cheatengine__open_process — attach to game process
mcp__cheatengine__scan_all — initial value scan
mcp__cheatengine__next_scan — narrow scan
mcp__cheatengine__read_memory — read bytes at address
mcp__cheatengine__dissect_structure — struct layout analysis
mcp__cheatengine__aob_scan — scan for byte signature
```

**x64dbg (live debugging):**
```
mcp__x64dbg__DebugSetBreakpoint — set breakpoint at address
mcp__x64dbg__DebugRun — resume execution
mcp__x64dbg__GetRegisterDump — read all registers
mcp__x64dbg__MemoryRead — read memory at address
mcp__x64dbg__GetCallStack — current call stack
```

**Ghidra (static analysis):**
```
mcp__ghidra__connect_instance — connect to running Ghidra
mcp__ghidra__analyze_function — analyze a function
mcp__ghidra__find_references — find all references to a symbol
mcp__ghidra__find_function_boundaries — get function start/end
mcp__ghidra__disassemble — disassemble at address
```

CE REQUIRED SETTING: Settings > Extra > uncheck "Query memory region routines" before any CE session.
