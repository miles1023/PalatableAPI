# SURFACES.md — Palworld Modding Surfaces Survey
# Phase 0 output.
# Last updated: 2026-05-15

---

> ## WARNING
> **This file was seeded from AI training data. All entries are unverified
> until confirmed against current 2026 sources provided by the user.**
>
> Training data cutoff is approximately mid-2024. Palworld has been in active
> development since then. Tool names, installation paths, API endpoints, hook
> paths, and community projects may have changed, moved, or been discontinued.
> Do not treat any entry here as accurate without verifying against a current source.

---

## What this file is

Every external access point into Palworld that the modding community has found,
used, or documented. Each entry describes what it exposes, how it is accessed,
and what game systems it touches.

Confidence levels:
- KNOWN — used by real mods or documented in verified community sources
- INFERRED — exists in the codebase but not widely used by mods yet
- UNKNOWN — suspected to exist but not confirmed

---

## SURFACE 1: UE4SS — Unreal Engine Scripting System
**[UNVERIFIED — training data, may be outdated]**

**What it is:** A DLL injected into the game process that hooks into Unreal Engine's
reflection system. The Okaetsu fork is Palworld-specific with additional UE 5.1 fixes.

**How it is accessed:**
- Drop a compiled UE4SS DLL + `ue4ss.dll` + `Mods/` folder next to the game executable
- Lua mod scripts go in `Mods/YourMod/Scripts/main.lua`
- C++ mods compile to DLL and are placed in `Mods/YourMod/dlls/`
- Blueprint mods go in `Mods/YourMod/` as `.pak` files

**What it exposes:**
- Full UE reflection API: read/write any reflected property by name (no offsets needed)
- `RegisterHook("/Script/Pal.ClassName:FunctionName")` — pre/post-hook any reflected function
- `NotifyOnNewObject("/Script/Pal.ClassName")` — callback when any new instance is created
- `FindAllOf("ClassName")` — enumerate all live instances of a class
- `StaticFindObject("/Script/Pal.Default__ClassName")` — get Class Default Object (CDO)
- `GetKismetSystemLibrary()`, `GetKismetMathLibrary()` — engine utility functions
- Lua standard library + file I/O
- Can call reflected UFunctions directly from Lua
- Can spawn objects, call static helpers, read/write TArray, TMap, FString, FName
- UHT (Unreal Header Tool) dump generator — exports all classes, properties, functions as .hpp files

**Game systems touched:** All reflected systems. Player, Pal, inventory, world, events,
DataTable access, building, AI (via hooks), server functions.

**Limitations:**
- Only exposes what Unreal's reflection system exposes (UPROPERTY/UFUNCTION marked)
- Non-reflected (private, bare C++) fields require the Direct tier (raw offsets)
- Lua-only or C++ DLL — no Python or other language access
- Hooks fire in-process; errors in hook code can crash the game

**Sources:** pwmodding.wiki, Okaetsu/UE4SS fork, mczubaj/Palworld-Mods, Elliesaur/Palworld-Mods
**Confidence:** KNOWN — in active use by all major Palworld script mods

---

## SURFACE 2: PAK Mod System — Unreal Asset Replacement
**[UNVERIFIED — training data, may be outdated]**

**What it is:** Unreal Engine's pak file system allows additional .pak files to be loaded
alongside the base game assets. Content in a mod pak overrides or supplements base content.

**How it is accessed:**
- Drop a `.pak` file into `Palworld/Content/Paks/` (path changed in 0.7.0, reverted in 0.7.1)
- Pak file is created with UnrealPak or repak tools
- To extract/read existing assets: FModel + Mappings.usmap
- To create replacement assets: need the original asset plus the UE editor (or compatible tools)

**What it exposes:**
- DataTable replacement — replace any game data spreadsheet (stat tables, item data, etc.)
- Blueprint replacement — replace or add Blueprint compiled logic
- Asset replacement — textures, models, audio, UI widgets
- New content injection — can add new assets (items, Pals, buildings) via pak

**Game systems touched:** Any system backed by static data assets:
- Pal stats (DT_PalMonsterParameter)
- Item data (DA_StaticItemDataAsset, DT_PalDropItem)
- Crafting recipes (DT_ItemRecipeDataTable)
- Building data (DT_BuildObjectDataTable)
- Skill/attack data (DT_WazaDataTable, DT_WazaMasterLevel)
- Cosmetics, UI, audio

**Limitations:**
- Does not touch live runtime state — only static data loaded at startup
- Mappings.usmap required to read Palworld's asset format (game-specific type mappings)
- Pak conflicts: only one pak wins per asset — no merging of DataTable rows
- PalSchema solves the merge problem for DataTables

**Sources:** pwmodding.wiki, FModel tool, PalSchema documentation, Nexus Mods Palworld section
**Confidence:** KNOWN — the most widely used Palworld mod delivery mechanism

---

## SURFACE 3: PalSchema — DataTable JSON Patch System
**[UNVERIFIED — training data, may be outdated]**

**What it is:** A pak-delivered C++ DLL loader (by Okaetsu) that applies JSON patches to
DataTables instead of replacing the whole asset. Solves the pak conflict problem for data mods.

**How it is accessed:**
- Install PalSchema pak + DLL into the game
- Create `.schema.json` files describing row-level patches to specific DataTables
- PalSchema applies the patches at game startup before data is used

**What it exposes:**
- Row-level add, modify, or delete for any DataTable the game loads
- Can change individual column values without touching other columns
- Multiple mods can patch the same DataTable without conflict

**Game systems touched:** Same as PAK — only static data DataTables. Examples:
- `DT_PalMonsterParameter` — all Pal base stats
- `DT_PalDropItem` — Pal drop tables
- `DT_ItemRecipeDataTable` — crafting recipes
- `DA_StaticItemDataAsset` — item properties
- `DT_BuildObjectDataTable` — building stats
- `DT_WazaDataTable` — attack/skill data

**Limitations:**
- Static data only — cannot modify live game state
- The pak redirector broke on game version 0.7.0; workaround is manual pak placement in 0.7.1
- Depends on PalSchema being maintained; one-developer project

**Sources:** github.com/Okaetsu/PalSchema, PalSchema schema files in existing knowledge base
**Confidence:** KNOWN — actively used by the data mod community

---

## SURFACE 4: Raw Memory Access (CheatEngine / Direct)
**[UNVERIFIED — training data, may be outdated]**

**What it is:** Direct read/write of the game process's memory. No injection required —
CheatEngine attaches as an external debugger with elevated privileges.

**How it is accessed:**
- CheatEngine attaches to the running game process (Palworld-Win64-Shipping.exe)
- AOB (Array of Bytes) scan to find code patterns and data structures
- Pointer chain resolution to follow UObject pointers to nested fields
- Value scan to find specific memory addresses by current value
- CheatEngine table (.CT files) to save found addresses for reuse

**What it exposes:**
- Any value in the game's memory, reflected or not
- Struct layouts for non-reflected types (via dissect structure)
- Function addresses (via code scanning)
- FFixedPoint inner fields, private member variables, etc.
- Can discover things UE4SS reflection does not expose

**Game systems touched:** Everything in memory — player stats, Pal stats, inventory,
entity pointers, server state, AI state, physics, anything.

**Limitations:**
- Addresses change on every game update and at every process restart for ASLR-affected regions
- AOB signatures are more stable than addresses but can still break on game updates
- Writing arbitrary memory can corrupt game state or crash
- Does not work on VAC-protected servers
- Palworld uses some kernel-level protections on certain memory pages (DBVM pages — see CE setting workaround)

**Sources:** CheatEngine MCP bridge (available in tools setup), community CheatEngine tables
**Confidence:** KNOWN — used for all discovered raw offsets in existing knowledge base

---

## SURFACE 5: DLL Injection (Custom C++ / D3D Hook)
**[UNVERIFIED — training data, may be outdated]**

**What it is:** A custom compiled DLL injected into the game process, either via UE4SS
C++ mod system or via external injection. The DLL runs inside the game process with full
access to game memory and functions.

**How it is accessed:**
- Via UE4SS: compile C++ mod to `.dll`, place in `Mods/YourMod/dlls/`
- Via external injector: use a DLL injector tool to load the DLL at game startup
- Via MinHook, Detours, or similar: patch function jump tables to redirect calls

**What it exposes:**
- Everything CheatEngine can access, but programmatically and persistently
- Can detour-hook any game function (not just reflected ones) via byte patching
- Can intercept Windows API calls (DirectX, networking, file I/O, etc.)
- Can add new in-process threads for background work
- Full access to game's vtables for virtual function hooking

**Game systems touched:** Everything. No reflection required.

**Limitations:**
- Requires C++ expertise and recompilation on game updates
- Function addresses change on updates (use AOB signatures for hook targets)
- More crash risk than Lua scripting

**Sources:** NightFyre/Palworld-Internal (C++ SDK), UE4SS C++ mod documentation
**Confidence:** KNOWN (UE4SS C++ path) / INFERRED (external injection path — not widely documented in Palworld-specific mods)

---

## SURFACE 6: RCON Interface (Dedicated Server)
**[DEPRECATED — confirmed 2026-05-16 via docs.palworldgame.com/api/rcon/]**

> **DEPRECATED:** Pocketpair has announced RCON is scheduled to stop functioning in an
> upcoming update. Do not build new tooling against RCON. Use the REST API (Surface 7) instead.
> Source: docs.palworldgame.com/api/rcon/ — accessed 2026-05-16.

**What it is:** A remote console interface on Palworld dedicated servers. Allows external
tools to send admin commands to the running server over the network.

**How it is accessed:**
- Enable in `PalWorldSettings.ini`: `RCONEnabled=true`, `RCONPort=25575`, `AdminPassword=...`
- Client connects via the RCON protocol (Palworld uses a Minecraft-compatible RCON format)
- Send commands as plaintext strings over TCP

**What it exposes (confirmed commands):**
- `Info` — server version and name
- `ShowPlayers` — list connected players with UID and Steam ID
- `KickPlayer <uid>` — kick a player
- `BanPlayer <uid>` — ban a player
- `TeleportToPlayer <uid>` — admin teleport
- `TeleportToMe <uid>` — teleport player to admin
- `Broadcast <message>` — send server-wide message
- `DoExit` / `Shutdown [seconds] [message]` — stop the server
- `Save` — force a world save

**What it does NOT expose:**
- Inventory modification
- Pal data
- Per-player stats
- Game world state queries

**Game systems touched:** Server management only. Player list, basic admin actions.

**Sources:** docs.palworldgame.com/api/rcon/ (confirmed deprecated 2026-05-16)
**Confidence:** KNOWN but DEPRECATED — will be removed in an upcoming game update

---

## SURFACE 7: REST API (Dedicated Server)
**[UNVERIFIED — training data, may be outdated]**

**What it is:** An HTTP REST API on Palworld dedicated servers. Richer than RCON.
Added in a game update (around 0.3.x).

**How it is accessed:**
- Enable in `PalWorldSettings.ini`: `RESTAPIEnabled=true`, `RESTAPIPort=8212`
- HTTP requests with Basic Auth (`admin:<password>`)
- Default base URL: `http://<server-ip>:8212/v1/api/`

**What it exposes (confirmed endpoints):**
- `GET /info` — server name, version, player count
- `GET /players` — list all connected players with UID, name, coordinates, level, ping
- `POST /kick` — kick player by UID
- `POST /ban` — ban player by UID
- `POST /unban` — unban player
- `POST /teleport` — teleport player to coordinates
- `POST /item` — spawn item for player (item ID + count)
- `POST /broadcast` — broadcast message
- `POST /shutdown` — graceful shutdown with delay
- `GET /metrics` — server metrics (FPS, player count, memory, etc.)
- `POST /save` — force world save
- `GET /guilds` — list guilds (added in later update)

**What it does NOT expose:**
- Live Pal data modification
- Player stat modification
- World state queries beyond player positions

**Game systems touched:** Server management, limited player management, item spawning,
some world events.

**Sources:** Palworld official REST API documentation, community reverse engineering of endpoints
**Confidence:** KNOWN — documented by Pocketpair, endpoints verified by community tools

---

## SURFACE 8: Save File Parsing (Offline)
**[UNVERIFIED — training data, may be outdated]**

**What it is:** Palworld's save files (`.sav`) use Unreal Engine's save format with
Palworld-specific serialization. Community tools can parse, read, and write them.

**How it is accessed:**
- Game must not be running (save file is locked while game runs)
- Tools: `palworld-save-tools` (Python library), `palworld-pal-editor` (web-based editor)
- Files located in `%LOCALAPPDATA%\Pal\Saved\SaveGames\<steam-uid>\` (client)
  or `PalServer/Pal/Saved/SaveGames/` (server)

**Save file structure:**
- `Level.sav` — world state: buildings, objects placed in the world
- `LocalData.sav` — local player data
- `Players/<steam64-uid>.sav` — per-player data: inventory, stats, position, tech tree
- `PalStorage_<uid>.sav` — Pal storage (PalBox contents) per base/player

**What it exposes:**
- Player inventory (item IDs, counts, durability)
- Player stats (HP, hunger, XP, level, tech points)
- Player equipment and hotbar
- Pal data (species, stats, level, passive skills, active skills, nickname)
- World object placement
- Guild data
- Technology research status
- Player appearance / customization

**Limitations:**
- Offline only — cannot modify a running game's save
- Format changes with game updates (tools must be updated)
- Corrupted edits can make saves unloadable

**Sources:** github.com/cheahjs/palworld-save-tools, palworld-pal-editor project
**Confidence:** KNOWN — save tool is widely used in the community

---

## SURFACE 9: Config / INI Files (Server and Client)
**[UNVERIFIED — training data, may be outdated]**

**What it is:** Standard Unreal Engine configuration files that control game settings.

**How it is accessed:**
- Direct file editing before game launch
- Server: `PalServer/Pal/Saved/Config/WindowsServer/PalWorldSettings.ini`
- Client: `%LOCALAPPDATA%\Pal\Saved\Config\WindowsNoEditor\PalWorldSettings.ini`

**What it exposes:**
- Gameplay rate multipliers (experience, drop rates, damage, etc.)
- Player and Pal inventory slot counts
- Server tick rate, player count limits
- PvP enable/disable
- Building damage, decay settings
- Day/night cycle speed
- Guild base limits
- RCON and REST API enable/config
- Admin password

**Limitations:**
- Static — changes take effect on next server restart
- Limited to the options Pocketpair exposes as settings
- Does not touch individual player/Pal state

**Sources:** Official Palworld dedicated server documentation, PalWorldSettings.ini reference
**Confidence:** KNOWN — directly documented by Pocketpair

---

## SURFACE 10: UHT (Unreal Header Tool) Dump via UE4SS
**[UNVERIFIED — training data, may be outdated]**

**What it is:** UE4SS can generate C++ header files from Unreal's live reflection data.
This is a research tool, not a modding surface per se, but it is the primary source of
truth for what UE reflection exposes.

**How it is accessed:**
- Load UE4SS with Palworld running
- Run `GenerateUHTCompatibleHeaders()` in the UE4SS console
- Outputs `.hpp` files to a `CXXHeaders/` folder next to the game executable

**What it exposes:**
- All UPROPERTY-marked fields for all Unreal classes in the game
- All UFUNCTION-marked methods (and their signatures)
- All UEnum values
- Class hierarchy (inheritance chains)
- Component relationships

**Why it matters for this project:**
- It is the definitive list of what Surface 1 (UE4SS reflection) can access
- Cross-referencing UHT output with CheatEngine findings shows which fields are
  reflected vs. which require raw memory access

**Sources:** UE4SS documentation, NightFyre/Palworld-Internal (contains older UHT dump data)
**Confidence:** KNOWN — standard UE4SS feature

---

## SURFACE 11: FModel + Mappings.usmap (Asset Research Tool)
**[UNVERIFIED — training data, may be outdated]**

**What it is:** FModel is an Unreal Engine asset browser. Mappings.usmap is a
Palworld-specific file that maps the game's compressed/obfuscated type names to
human-readable names. Together they allow reading all game DataTables and assets.

**How it is accessed:**
- Download FModel, configure with Palworld game path and Mappings.usmap
- Browse or export any asset in the game's pak files
- Mappings.usmap maintained by community: github.com/PalworldModding/UsefulFiles

**What it exposes:**
- Complete DataTable contents (all rows and columns) for every game DataTable
- Blueprint class contents
- All enum values
- Asset paths and UObject structure

**Why it matters for this project:**
- This is the source for all DataTable schema knowledge (columns, types, row names)
- Without Mappings.usmap, DataTable data appears as raw byte blobs

**Limitations:**
- Read-only — this is a research/discovery tool only
- Mappings.usmap must be updated when Pocketpair updates the game

**Sources:** FModel GitHub, github.com/PalworldModding/UsefulFiles, Okaetsu/PalSchema
**Confidence:** KNOWN — used by all DataTable mod developers

---

## SURFACE 12: Ghidra / IDA Pro (Static Binary Analysis)
**[UNVERIFIED — training data, may be outdated]**

**What it is:** Disassemblers that can analyze the Palworld shipping binary without
running the game. Used to find function addresses, understand logic, and discover
structures not visible through UE reflection.

**How it is accessed:**
- Import `Palworld-Win64-Shipping.exe` into Ghidra or IDA Pro
- Use a Palworld-specific Ghidra script or PDBEX if PDB symbols exist (they do not for Palworld)
- Community-maintained function name databases (Ghidra project files shared on Discord)
- Palworld-specific Ghidra extensions exist in the modding community

**What it exposes:**
- All game functions and their addresses (requires analysis to name them)
- Non-reflected structs and their memory layouts
- Virtual function tables (vtables)
- String references that reveal function purpose
- RTTI (Run-Time Type Information) class names

**Why it matters for this project:**
- Needed to find function addresses for hooking non-reflected functions
- Needed to understand FFixedPoint and other custom types
- Cross-reference with CheatEngine AOB findings to validate signatures

**Tools available:** Ghidra MCP bridge (`mcp__ghidra__*`) available in this project
**Sources:** Ghidra project, community Palworld Ghidra databases
**Confidence:** KNOWN (tool) / INFERRED (Palworld-specific Ghidra databases — community shared but not publicly hosted)

---

## SURFACE 13: x64dbg (Live Dynamic Debugging)
**[UNVERIFIED — training data, may be outdated]**

**What it is:** A debugger that attaches to the running Palworld process and allows
stepping through code, setting breakpoints, and inspecting registers and memory at
exact execution points.

**How it is accessed:**
- Launch Palworld, then attach x64dbg to the process
- Set breakpoints on addresses found via Ghidra static analysis
- Step through code to understand call chains and parameter passing

**What it exposes:**
- Exact function parameter values at call time
- Return values
- Exact timing of when game systems fire
- Stack traces showing what called a function
- Register state at any instruction

**Why it matters for this project:**
- Confirms function signatures found in Ghidra
- Reveals parameter order and types for C++ functions
- Essential for confirming FFixedPoint inner field (.Value vs .RawValue)
- Discovers the call path for events UE4SS does not expose (death, capture, level-up)

**Tools available:** x64dbg MCP bridge (`mcp__x64dbg__*`) available in this project
**Sources:** x64dbg project, standard RE practice
**Confidence:** KNOWN

---

## SURFACE 14: Steam Workshop
**[CONFIRMED LIVE — verified 2026-05-16 via steamcommunity.com/app/1623730/workshop/]**

> **Correction from training data:** Training data listed this as INFERRED / upcoming.
> Steam Workshop went live with the Home Sweet Home update (0.7.0).
> Sources: steamcommunity.com/app/1623730/workshop/, pwmodding.wiki/docs/category/steam-workshop — accessed 2026-05-16.

**What it is:** Official Pocketpair-supported mod distribution via Steam Workshop.
Launched with the 0.7.0 "Home Sweet Home" update.

**How it is accessed:**
- Browse and subscribe to mods directly through Steam or within Palworld
- Mod installation guide: pwmodding.wiki/docs/users/workshop/installing-mods
- Server-side: docs.palworldgame.com/settings-and-operation/mod/
- For mod developers publishing: pwmodding.wiki/docs/developers/mod-publishing/workshop/uploading

**What it exposes:**
- Officially distributed .pak mods and UE4SS script mods via Steam subscription
- Same capabilities as Surface 1 (UE4SS) and Surface 2 (PAK) — Workshop is a delivery
  mechanism, not a new capability layer

**Current limitations and known bugs:**
- Described by Pocketpair as "highly experimental" — may be unstable
- Workshop UE4SS does NOT work on Steam Deck / Proton / Wine (known bug, no fix date)
- Workshop mods only work on private servers; NOT on official Pocketpair servers
- Workshop UE4SS and separately-installed Nexus UE4SS CANNOT both be active at once — will crash

**Why it matters for this project:**
- This is the distribution surface that modders using PalatableAPI will likely use
- Any mod we produce for testing or distribution will be published here
- All UE4SS limitations apply — Steam Workshop does not add new reflection capabilities

**Sources:** steamcommunity.com/app/1623730/workshop/, pwmodding.wiki/docs/category/steam-workshop,
mmorpg.com/news/palworld-adds-ultrakill-collab-steam-workshop-compatibility... (confirmed 2026-05-16)
**Confidence:** KNOWN — live and in active use

---

## Surface Completeness Assessment
Last updated: 2026-05-16 (RCON and Steam Workshop entries corrected from web research)

| Surface | Confidence | RE Tools Cover It? | Notes |
|---------|------------|-------------------|----|
| UE4SS Reflection + Hooks | KNOWN | Yes (via MCP bridges) | Confirmed active Jan 2026 |
| PAK Asset Replacement | KNOWN | Partial (FModel reads; writing not needed for RE) | |
| PalSchema DataTable Patching | KNOWN | Partial (DataTable schema from FModel) | Pak redirector broken in 0.7.0; manual workaround |
| Raw Memory (CheatEngine) | KNOWN | Yes (CE MCP bridge) | EAC/anticheat status for 0.7.1 still unverified |
| DLL Injection / Custom Hooks | KNOWN | Yes (via x64dbg + Ghidra) | |
| RCON Interface | DEPRECATED | Not needed for RE | Will be removed in upcoming update |
| REST API | KNOWN | Not needed for RE | Official docs at docs.palworldgame.com |
| Save File Parsing | KNOWN | No (separate tool; offline) | |
| Config / INI Files | KNOWN | Not needed for RE | |
| UHT Dump (UE4SS) | KNOWN | Yes (drives Surface 1) | |
| FModel + Mappings | KNOWN | Yes (DataTable research) | Mappings.usmap last updated Dec 22, 2025 |
| Ghidra Static Analysis | KNOWN | Yes (Ghidra MCP bridge) | |
| x64dbg Live Debugging | KNOWN | Yes (x64dbg MCP bridge) | |
| Steam Workshop | KNOWN | N/A (distribution only) | LIVE since 0.7.0; no new RE capabilities |
