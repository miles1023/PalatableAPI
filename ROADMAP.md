# PALWORLD MODDING FRAMEWORK — COMPLETE PROJECT PLAN

> **Status:** Final consolidated plan. All information verified against live sources as of May 16, 2026.
> **Purpose:** This document is the single source of truth for building a BakkesMod-style modding framework for Palworld. It covers everything from a vanilla game installation through a fully published, update-resilient API covering every moddable system in the game.
> **Audience:** AI coding agent. All coding is AI-generated. The project owner is non-technical.

---

## PROJECT VISION

Build a dedicated modding framework for Palworld — the same relationship BakkesMod has to Rocket League. Modders interact with a clean, Palworld-specific API. The framework handles all complexity underneath. A modder should be able to say "change this Pal's attack damage" and the framework already knows how to do everything else. Modders never touch UE4SS, Cheat Engine, or raw memory. They code against the framework's API.

---

## CURRENT STATE OF PALWORLD (May 2026)

| Fact | Detail | Source | Date |
|------|--------|--------|------|
| Current version | 0.7.3 (balance patch) | game8.co patch notes | Apr 2026 |
| Game status | Still Early Access | palworld.fandom.com | Mar 2026 |
| 1.0 release | Confirmed late 2026 (World Tree endgame, progression rework) | Pocketpair Producer Letters, supercraft.host | May 2026 |
| 1.0 details | Labeled "Top Secret" — no advance patch notes | store.steampowered.com | Sep 2025 |
| Player count | 32M+ across Steam, Xbox, PS5 | Multiple sources | 2026 |
| Steam Workshop | LIVE since v0.7.0 (Dec 17 2025) | steamcommunity.com/app/1623730 | Dec 2025 |
| Official Mod Loader | Shipped with v0.7.0 (Info.json, PackageName, InstallRules format) | github.com/pocketpairjp/PalworldModUploader | Dec 2025 |
| In-game mod toggle | Options → Mod Management (opt-in, required) | pwmodding.wiki | Dec 2025 |
| Okaetsu role | Creator of PalSchema + Palworld UE4SS fork. Personally thanked by Pocketpair | Steam announcement | Dec 2025 |
| PalSchema status | v0.5.2, semi-official. Broke on v0.7.0, required manual fix | github.com/Okaetsu/PalSchema | Jan 2026 |
| Anti-cheat | None on standard PC servers | exitlag.com/blog/palworld-mods | Feb 2026 |
| Patch cadence | Every 3-4 weeks throughout 2026 | supercraft.host roadmap analysis | May 2026 |
| UE4SS on Linux | Inconsistent. Windows servers recommended for UE4SS mods | winternode.com/blog/palworld/best-server-mods | Mar 2026 |
| UE4SS on Steam Deck | Broken (confirmed bug, no fix date) | Steam Workshop item notes | Jan 2026 |
| Four mod types | Lua mods, LogicMods (Blueprint .pak), Patch Paks (.pak), PalSchema (JSON) | pwmodding.wiki, curseforge.com/palworld | 2025-2026 |

---

## AVAILABLE LOCAL TOOLING (D:\Tools)

### Reverse Engineering Stack (MCP-Bridged — AI Can Drive These Directly)

| Tool | Location | MCP Bridge | Tool Count | Key Capabilities |
|------|----------|------------|------------|------------------|
| Ghidra 12.0.4 | D:\Tools\ghidra_12.0.4_PUBLIC | D:\Tools\ghidra-mcp (v5.6.0) | 225 MCP tools | Static binary analysis, decompilation, class/vtable reconstruction, function identification, type analysis, P-code emulation, automated function documentation (fun-doc). HTTP endpoint: http://127.0.0.1:8089 |
| Cheat Engine | D:\Tools\cheatengine | D:\Tools\cheat-engine-mcp (v12.0.0) | ~180 MCP tools | Live memory inspection, pointer chain discovery, AOB pattern scanning, hardware breakpoints (DR0-DR3), DBVM invisible tracing, code injection, cheat table (.CT) creation/management. Named Pipe: CE_MCP_Bridge_v99 |
| x64dbg | System installed | D:\Tools\x64dbgMCP | 40+ SDK tools | Runtime debugging, register inspection, pattern searching, breakpoints, stepping, cross-architecture x64/x32. HTTP bridge |

### Game Engine Tools

| Tool | Location | Purpose |
|------|----------|---------|
| Unreal Engine 5.7 | D:\Tools\UE_5.7 | Full UE5 editor for Palworld Modding Kit projects |
| UModel | D:\Tools\umodel_win32 | Unreal model/asset viewer and exporter |
| SteamCMD | D:\Tools\steamcmd | Automated Steam downloads, dedicated server management, version detection |

### Reference Implementation

| Tool | Location | Purpose |
|------|----------|---------|
| BakkesMod | D:\Tools\bakkesmod | The exact framework architecture this project models. Study plugin system, SDK design, and DLL injection approach |

### Why This Matters

The reverse engineering work that would normally require deep manual expertise is **substantially AI-driven** using the MCP bridges. All three RE tools can be directed by AI to systematically discover game internals, build pointer maps, generate AOB signatures, and validate findings — without waiting for human reverse engineers.

---

## RISK MATRIX

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Palworld 1.0 drops before framework is ready | Medium | Critical | Ship Phase 3 as early beta. Phase 4 ships incrementally (Tier 1 modules first) |
| 1.0 restructures core systems breaking all hooks | High | Critical | AOB scanning (Phase 5) + graceful degradation for every module |
| Okaetsu stops maintaining Palworld UE4SS fork | Low | High | Framework uses UE4SS but AOB scanning reduces fork dependency |
| Pocketpair changes official mod format in 1.0 | Medium | High | Framework packaging layer is isolated — updatable independently |
| PalSchema becomes official, replacing need for framework | Low | Medium | Framework is PalSchema-compatible. If PalSchema goes official, framework wraps it |
| Linux dedicated server support never stabilizes for UE4SS | High | Medium | Document Windows-only for UE4SS mods. .pak mods work cross-platform |
| Community doesn't adopt because PalSchema is "good enough" | Medium | High | Must demonstrate clear value on day one: 24hr patch turnaround, conflict resolution, plugin ecosystem |

---

## PROJECT NAME

Needs a name before public-facing work. Candidates:
- PalAPI
- PalForge
- PalKit
- PalFrame
- OpenPal

Decision: owner picks. Must be available as GitHub org and not conflict with existing Palworld modding projects.

---

## TIMELINE

Starting: May 2026. Palworld 1.0 estimated: Q4 2026 (Oct-Dec).

| Phase | Duration | Calendar Target | Risk if Late |
|-------|----------|-----------------|--------------|
| Phase 1 — Environment & Foundation | 2 weeks | June 1 2026 | Blocks everything |
| Phase 2 — Game Mapping & Recon | 3 weeks | June 22 2026 | Incomplete API surface |
| Phase 3 — Core API Build | 5 weeks | July 27 2026 | No usable framework |
| Phase 4 — Full API Coverage | 7 weeks | Sep 14 2026 | Partial coverage at launch |
| Phase 5 — Resilience & Tooling | 3 weeks | Oct 5 2026 | Framework breaks on 1.0 |
| Phase 6 — Release & Community | 2 weeks | Oct 19 2026 | Miss 1.0 launch window |

**Total: 22 weeks → ~Oct 19 2026**

**Contingency:** Phase 4 can ship incrementally. Core modules (Pals, Player, Items, Base, Combat) ship first as Tier 1. Remaining modules ship as updates. A viable v0.9 can exist by Sep 14 even if 1.0 drops early.

---

## PHASE 1 — ENVIRONMENT & FOUNDATION (Week 1–2)

### Objective
Install every required tool, verify the complete modding pipeline, and confirm all MCP bridges are operational.

### Steps

#### 1.1 Install Palworld v0.7.3 via Steam (PC only)
- Xbox/Game Pass versions cannot use UE4SS due to WinGDK restrictions
- Verify game launches and enters main menu cleanly
- Tags: prerequisite, steam, v0.7.3

#### 1.2 Install the Palworld-specific UE4SS build (Okaetsu fork)
- Since v0.4.1.5 the GENERIC UE4SS build crashes Palworld — the Okaetsu fork is REQUIRED
- Source: github.com/Okaetsu/RE-UE4SS (experimental-palworld tag) OR Steam Workshop subscription
- GitHub version is more current than Workshop version
- Extract to: `Palworld/Pal/Binaries/Win64/`
- New default layout (late 2025): UE4SS files go in `ue4ss` subfolder next to game executable
- Verify: UE4SS console appears on game launch
- Tags: ue4ss, okaetsu, required

#### 1.3 Configure UE4SS and enable in-game mod support
- Set `bUseUObjectArrayCache = false` in UE4SS-settings.ini (Palworld-specific, prevents crashes)
- Set `GuiConsoleVisible = 1` for development
- Launch Palworld → Options → Mod Management → Enable Mods
- WITHOUT this in-game toggle, no mods load even if correctly installed (new in v0.7.0)
- Tags: config, mod management

#### 1.4 Download the official Palworld Mod Uploader
- Available as Steam Library tool AND at github.com/pocketpairjp/PalworldModUploader
- Defines the OFFICIAL mod format: Info.json, PackageName, InstallRules
- Framework MUST use this format for Workshop distribution
- Supports four mod types: Lua, LogicMods, Paks, PalSchema
- Tags: mod uploader, official format

#### 1.5 Install the Palworld Modding Kit (PMK)
- Source: github.com/localcc/PalworldModdingKit
- Requires: Visual Studio 2022 Community (NOT VS2026 — breaks UE5.1), Unreal Engine 5.1
- Enables LogicMods (Blueprint mods) and provides access to Palworld's real class definitions
- Tags: modding kit, unreal 5.1

#### 1.6 Install FModel
- Required for browsing Palworld's pak file contents
- Set UE version to GAME_UE5_1
- Enable Local Mapping File, point to .usmap
- Tags: fmodel, pak browser

#### 1.7 Set up and verify MCP tool bridges
- **Ghidra MCP:** Build and deploy plugin:
  ```
  python -m tools.setup deploy --ghidra-path D:\Tools\ghidra_12.0.4_PUBLIC
  ```
  Launch Ghidra, verify HTTP endpoint at http://127.0.0.1:8089. Start bridge: `python bridge_mcp_ghidra.py`
- **Cheat Engine MCP:** Launch CE from D:\Tools\cheatengine. Load bridge:
  File → Execute Script → D:\Tools\cheat-engine-mcp\MCP_Server\ce_mcp_bridge.lua
  Verify log: `[MCP v12.0.0] MCP Server Listening on: CE_MCP_Bridge_v99`
  **CRITICAL:** CE Settings → Extra → DISABLE "Query memory region routines" (prevents BSODs during DBVM scans)
- **x64dbg MCP:** Copy .dp64 from D:\Tools\x64dbgMCP\release to x64dbg plugins directory. Launch x64dbg, verify plugin loaded (ALT+L). Start bridge: `python src/x64dbgmcp.py`
- All three MCP bridges MUST be operational before Phase 2
- Tags: ghidra mcp, cheat engine mcp, x64dbg mcp

#### 1.8 Set up the project repository
- GitHub repository structure:
  ```
  /core        — loader, injection layer, namespace
  /api         — Palworld-specific API modules (one folder per module)
  /schema      — Info.json templates, mod packaging scripts, InstallRules
  /logicmods   — any Blueprint-based components
  /docs        — auto-generated API documentation
  /tests       — in-game validation scripts
  /examples    — starter plugins
  /signatures  — AOB signature database (versioned per Palworld version)
  ```
- MIT license (non-negotiable for trust)
- Tags: github, structure, MIT

#### 1.9 Verify all four mod types end-to-end
- Subscribe to and test ONE of each from Workshop/Nexus:
  - Lua mod (e.g. Map Unlocker)
  - LogicMod/Blueprint mod (e.g. Pal Analyzer)
  - Patch Pak mod (e.g. skin replacement)
  - PalSchema mod (e.g. Tool Expansion)
- All four must work on v0.7.3 with Okaetsu UE4SS
- If any fail, do NOT proceed — fix the setup first
- Tags: validation, all mod types

### PHASE 1 GATE
- [ ] Palworld v0.7.3 launches with UE4SS active
- [ ] Mod Management enabled in Options
- [ ] All four mod types verified working in-game
- [ ] Modding Kit compiles successfully
- [ ] Mod Uploader tool opens and functions
- [ ] FModel browses pak contents
- [ ] Ghidra MCP bridge responds to commands
- [ ] Cheat Engine MCP bridge responds to commands
- [ ] x64dbg MCP bridge responds to commands
- [ ] GitHub repository created with correct structure

---

## PHASE 2 — GAME MAPPING & RECON (Week 2–5)

### Objective
Extract Palworld v0.7.3's complete internal structure using AI-driven reverse engineering. Define the exact scope of every system the API will cover.

### AI-Driven Reverse Engineering Pipeline

```
1. STATIC ANALYSIS (Ghidra MCP)
   Load Palworld binary → auto-analyze → extract classes/functions/vtables

2. LIVE MEMORY ANALYSIS (Cheat Engine MCP)
   Attach to running game → scan values → discover pointer chains → generate AOB signatures

3. RUNTIME VALIDATION (x64dbg MCP)
   Set breakpoints → verify function behavior → trace execution paths

4. CROSS-REFERENCE (UE4SS Dumps)
   Compare all findings → identify gaps → generate definitive API surface map
```

### Steps

#### 2.1 Static analysis via Ghidra MCP (AI-driven)
- Load Palworld-Win64-Shipping.exe into Ghidra
- Use Ghidra MCP's 225 tools to:
  - Auto-analyze the binary (let Ghidra complete initial analysis pass)
  - Search for all UE5 reflected class structures (UObject, AActor, APawn, ACharacter, etc.)
  - Identify all Pal-related classes (PalCharacter, PalParameter, PalStatComponent, etc.)
  - Identify all Player-related classes (PalPlayerCharacter, PalPlayerState, etc.)
  - Identify all Base/Building classes (PalBaseCampManager, PalBuildObject, etc.)
  - Extract vtable layouts for key game classes
  - Use fun-doc to auto-document discovered functions at scale
  - Export complete class hierarchy as structured data
- This replaces manual reverse engineering — AI directs Ghidra systematically
- Tags: ghidra, static analysis, class discovery

#### 2.2 Live memory analysis via Cheat Engine MCP (AI-driven)
- Launch Palworld, attach Cheat Engine via CE MCP bridge
- Use CE MCP's ~180 tools to:
  - Scan for known game values (player HP, Pal level, item counts, base camp stats, carry weight)
  - Use "find what writes" / "find what accesses" to discover which functions modify each value
  - Follow pointer chains from base addresses to game object structures
  - Build complete pointer maps for:
    - Player object → stats, inventory, equipment, party
    - Active Pal party → individual Pal objects → stats, skills
    - Palbox → all stored Pals
    - Base camp → workers, buildings, production state
    - World state → time, weather, spawn tables
  - Generate AOB signatures for EVERY function the framework will hook
  - Export all findings as structured cheat table (.CT)
  - Test AOB signatures by verifying they resolve correctly after game restart
- **CRITICAL:** Disable "Query memory region routines" in CE Settings → Extra before DBVM work
- Tags: cheat engine, pointer chains, aob signatures

#### 2.3 Runtime validation via x64dbg MCP
- Attach x64dbg to Palworld process
- Use x64dbg MCP's 40+ tools to:
  - Set breakpoints on Ghidra-discovered functions
  - Verify function parameters and return values match static analysis
  - Trace execution paths for event candidates (Pal caught, damage dealt, base built, etc.)
  - Validate AOB signatures from CE resolve to correct functions
  - Identify additional hookable functions missed by static analysis
- Tags: x64dbg, runtime validation, tracing

#### 2.4 Run UE4SS dumps and cross-reference
- CTRL+J in UE4SS console → UE4SS_ObjectDump.txt (all loaded objects)
- CTRL+H in UE4SS console → C++ headers for all reflected classes
- Cross-reference against Ghidra and CE findings:
  - Every Ghidra-discovered class should appear in UE4SS headers
  - Every CE pointer chain should be reachable via UE4SS object traversal
  - Identify functions Ghidra found that UE4SS CANNOT hook (need direct memory hooks)
  - Identify UE4SS-visible objects Ghidra MISSED (dynamically created, runtime-only)
- Tags: ue4ss, cross-reference

#### 2.5 Generate .usmap mappings and browse pak data
- Generate .usmap files for unversioned property mapping
- Browse pak files with FModel (UE version: GAME_UE5_1)
- Catalog ALL data tables: Pal stats, item definitions, building definitions, passive skills, technology trees, breeding tables, dungeon loot, tower boss definitions, oil rig configs
- Cross-reference with PalSchema's existing coverage — catalog what it covers AND what it doesn't
- Tags: usmap, fmodel, data tables

#### 2.6 Catalog ALL moddable game systems

Every system must be located in CXX headers, CE pointer maps, and/or data tables:

**Core Systems:**
- Pals (stats, skills, work suitabilities, partner skills, food debuffs)
- Player (stats, inventory, equipment, party, position, Lifmunk Effigies)
- Items (definitions, properties, crafting recipes, schematics, blueprints)
- Technology tree (regular + ancient technology points)

**Base & Building:**
- Base camps (level, upgrade, area range, workers, production speed)
- Buildings (all types incl. v0.7.0 triangular pieces, color customization)
- Palbox management
- Guild Chest (shared resources between bases)
- Pal work assignments and work location indicators (Cattiva icon system v0.7.0)
- Summoning Altar (no longer destroyed at raid end per v0.7.1 fix)

**Combat & PvP:**
- Weapons (all types, ammo, durability, damage modifiers)
- Melee combo system (v0.7.0 improved swords/katanas, special attacks)
- Ricoshot mechanic (Marksman Revolver + coin throw, v0.7.0)
- Status effects
- PvP system (experimental, private servers only, v0.7.0)
- PvP raid log (on-screen display during base attacks, v0.7.1)

**World & Environment:**
- Time of day, weather
- Map fog of war, fast travel points, map pins
- Resource nodes and regeneration
- Supply crates (locations, collection tracking)
- NPC merchant inventories
- Wild Pal spawn rates per area/per species

**Dungeons & Encounters:**
- Dungeon system (randomly generated, loot tables, discovery tracking)
- Tower Bosses (5 towers with unique boss fights)
- Oil Rigs (Rayne Syndicate strongholds, loot, blueprint drop rates)
- Raid Bosses (Bellanoir, Predator bosses)
- Raid Battlefield (separate from base, v0.7.0)
- Alpha Pals and Lucky Pals (spawn behavior, stat bonuses)

**Breeding & Genetics:**
- Breeding pair compatibility tables
- Egg production, incubation (Electric Egg Incubator)
- Passive skill inheritance and probability
- Breeding ranch automation state

**Mounts & Movement:**
- Pal saddles (crafting, equipping)
- Mount types: ground, flying, swimming
- Mount stats and speed modifiers
- Glider system (including Hyper Glider)

**Multiplayer & Server:**
- Connected players, server configuration (runtime read/write)
- Guild system
- Global Palbox (cross-platform sharing, v0.5)
- Server cluster support (IN DEVELOPMENT for 2026 — placeholder hooks needed)
- PvP configuration for private servers

**Progression & Tracking:**
- Palpedia completion tracking
- Expeditions system, Missions system
- Pal Labour Research Laboratory
- Bounty tokens
- Steam Achievements (read-only detection)

**Crossover Content:**
- ULTRAKILL collaboration content (v0.7.0)
- Terraria "Tides of Terraria" content
- Framework must detect and handle crossover-specific classes

**UI Systems:**
- HUD elements
- Building menu (v0.7.0 list-based overhaul)
- Pal work location indicators
- In-game notifications, mod management UI integration

#### 2.7 Map the official mod loader integration points
- How PalModSettings.ini initializes mods
- How Info.json PackageName and InstallRules work
- How the official loader handles dependencies (Workshop "Required Items")
- How all four mod types coexist and their install paths:
  - Lua mods: `ue4ss/Mods/<ModName>/`
  - LogicMods: `Pal/Content/Paks/LogicMods/<ModName>.pak`
  - Patch Paks: `Pal/Content/Paks/~mods/<ModName>.pak`
  - PalSchema: `NativeMods/UE4SS/Mods/PalSchema/mods/<ModName>/`
- Goal: framework sits INSIDE the official system as a valid Lua mod

#### 2.8 Map function hooks for runtime behavior
Key functions to hook via RegisterHook (validated by x64dbg MCP in step 2.3):
- Pal caught, summoned, returned to box, died
- Player takes damage, dies, respawns
- Base building placed, destroyed, level up
- Raid starts/ends, raid battlefield entered
- PvP kill, PvP state change
- Dungeon entered/completed, tower boss started/defeated
- Item picked up, crafted, used
- Egg laid, hatched
- Mount summoned, dismissed
- Server tick, player join, player leave
- Reference: pwmodding.wiki/docs/developers/ue4ss-modding/lua-mods/ue4ss-functions

#### 2.9 Define the complete API surface in plain language
- Every method the finished API will expose
- Written BEFORE any code
- This is the contract everything is measured against
- Must include ALL systems from 2.6
- 1.0 systems flagged as "planned" where known

### PHASE 2 GATE
- [ ] Ghidra class analysis complete for all major game systems
- [ ] CE pointer chains discovered for player, pals, base, items, world state
- [ ] AOB signatures generated and validated for all hookable functions
- [ ] UE4SS dumps cross-referenced against Ghidra/CE findings
- [ ] All data tables cataloged via FModel
- [ ] Official mod loader integration points mapped
- [ ] Plain-language API surface defined and agreed
- [ ] All findings stored in /signatures directory (versioned for v0.7.3)

---

## PHASE 3 — CORE API BUILD (Week 5–10)

### Objective
Build the foundational framework layer fully integrated with the official v0.7 mod system.

### Steps

#### 3.1 Build the framework as a valid official mod
- Package using Info.json, PackageName, InstallRules format
- Type: Lua mod in the official system
- When other mods list framework as Workshop dependency, Steam auto-downloads it
- **This is the install experience: subscribe to framework → subscribe to plugin → done**

#### 3.2 Build the framework loader and namespace
- UE4SS Lua mod that initializes on game start
- Checks Palworld version against known-good version map
- Loads all API modules in dependency order
- Exposes clean global namespace: `PalAPI`
- Reads PalModSettings.ini to detect active plugins
- Logs all initialization status to UE4SS console
- Detects presence of PalSchema and registers interop layer if found

#### 3.3 Build the plugin system
- Plugins are official mods that declare framework as dependency
- Manifest: mod name, version, author, dependencies, priority (for conflict resolution)
- Framework reads active mods from PalModSettings.ini
- Plugins register with PalAPI and NEVER interact with UE4SS directly
- Installable from Workshop in one click — no manual file placement

#### 3.4 Build the event system
- Wraps UE4SS RegisterHook calls behind named events
- Clean subscription API: `PalAPI.Events.On("PalCaught", function(data) end)`
- Framework handles all raw hook registration
- Delivers structured data to subscribers (not raw UE4SS objects)
- Includes all v0.7.x events

#### 3.5 Build PalAPI.Pals module
```
GetByName(name), GetById(id)
GetAllInBox(), GetAllInWorld(), GetAllInBase(baseId)
GetStat(pal, statName), SetStat(pal, statName, value)
GetPassiveSkills(pal), AddPassiveSkill(pal, skillId), RemovePassiveSkill(pal, skillId)
GetPartnerSkill(pal)
GetWorkSuitabilities(pal), SetWorkSuitability(pal, type, level)
Spawn(palName, position), Despawn(pal)
GetMountData(pal)
```

#### 3.6 Build PalAPI.Player module
```
GetLocal(), GetAll()
GetStat(statName), SetStat(statName, value)
  — HP, stamina, hunger, temperature tolerance, level, XP, tech points, ancient tech points
GetInventory(), AddItem(itemId, count), RemoveItem(itemId, count)
GetEquipped(), GetParty()
GetPosition(), Teleport(position)
GetEffigyBonus()
```

#### 3.7 Test all Phase 3 modules
- Every method has a test script
- Tests run from UE4SS console as single command
- Read methods return correct values
- Write methods produce expected in-game changes
- **GATE: No Phase 4 work until ALL Phase 3 tests pass on v0.7.3**

### PHASE 3 GATE
- [ ] Framework is a valid Workshop mod (Info.json, PackageName)
- [ ] Plugins install via Steam Workshop subscription
- [ ] Plugin dependency resolution works
- [ ] Events fire with structured data
- [ ] PalAPI.Pals fully tested
- [ ] PalAPI.Player fully tested
- [ ] PalAPI.Events fully tested

---

## PHASE 4 — FULL API COVERAGE (Week 10–18)

### Objective
Expand to every moddable system. Ship in priority tiers.

### Priority Tiers
- **Tier 1 (ship first):** Items, Base, Combat, World, Breeding — covers 90% of existing mod use cases
- **Tier 2 (fast follow):** Server, UI, Data, Dungeons
- **Tier 3 (post-launch):** Content, Mounts, Crossover

### All Modules

#### 4.1 PalAPI.Items
```
GetDefinition(itemId), GetAllDefinitions()
ModifyStat(itemId, statName, value)
GetRecipe(itemId), GetAllRecipes()
UnlockTech(techId), UnlockAncientTech(techId), GetTechTree()
GetSchematics(), GetChestBlueprints(baseId)
SpawnItem(itemId, position, count)
```

#### 4.2 PalAPI.Base
```
GetAll(), GetById(baseId)
GetWorkers(baseId), GetLevel(baseId)
SetProductionSpeed(baseId, multiplier)
GetBuildings(baseId), PlaceBuilding(baseId, buildingType, position)
SetBuildingColor(building, colorData)
GetRaidBattlefield(baseId)
GetSummoningAltar(baseId)
GetGuildChest(baseId)
GetAreaRange(baseId), SetAreaRange(baseId, multiplier)
GetPalbox(baseId)
```

#### 4.3 PalAPI.Combat
```
GetWeaponDefinition(weaponId), GetAllWeaponDefs()
ModifyDamage(source, target, multiplier)
ApplyStatusEffect(target, effectId), RemoveStatusEffect(target, effectId), GetActiveEffects(target)
GetPvPState(), SetPvPConfig(config)
GetRaidLog()
GetMeleeComboState(player)
GetRicoshotState(player)
ModifyDefense(target, multiplier)
```

#### 4.4 PalAPI.World
```
GetTime(), SetTime(timeOfDay)
GetWeather(), SetWeather(weatherType)
GetSpawnRate(area), SetSpawnRate(area, multiplier)
GetBossStatus(bossId)
GetOilRigStatus(rigId)
GetDungeonStatus(dungeonId)
GetSupplyCrates()
UnlockMap(), GetFastTravelPoints()
GetMerchantInventory(npcId)
GetAlphaStatus(palId), GetLuckyPalSpawns()
```

#### 4.5 PalAPI.Breeding
```
GetEggStatus(eggId)
GetCompatibility(pal1, pal2)
GetOffspring(pal1, pal2)
SetHatchTime(eggId, seconds)
GetSkillProbability(pal1, pal2, skillId)
GetRanchState(baseId)
```

#### 4.6 PalAPI.Server
```
GetAllPlayers(), GetPlayerById(playerId)
Broadcast(message), KickPlayer(playerId), BanPlayer(playerId)
GetConfig(key), SetConfig(key, value)
GetGuilds(), GetGuildMembers(guildId)
GetGlobalPalbox()
GetClusterState()
GetPvPConfig()
```

#### 4.7 PalAPI.UI
```
ShowNotification(message, duration)
DrawHUD(elementDef)
CreateMenu(menuDef)
AddBuildingMenuEntry(entry)
ShowDialog(dialogDef)
RegisterKeybind(key, callback)
GetPalWorkIndicators()
```

#### 4.8 PalAPI.Data
```
Save(pluginId, key, value)
Load(pluginId, key)
Delete(pluginId, key)
GetConfig(pluginId, key), SetConfig(pluginId, key, value)
Exists(pluginId, key)
— All operations use safe file I/O that NEVER touches game save files
```

#### 4.9 PalAPI.Dungeons
```
GetAllDungeons(), GetDungeonById(dungeonId)
GetDungeonLootTable(dungeonId), ModifyLootTable(dungeonId, lootDef)
GetTowerBoss(towerId), GetTowerBossStatus(towerId)
ModifyTowerBossStats(towerId, statDef)
GetOilRig(rigId), ModifyOilRigLoot(rigId, lootDef)
GetRaidBoss(bossId), ModifyRaidBossStats(bossId, statDef)
GetExpeditionStatus(), GetMissions()
```

#### 4.10 PalAPI.Mounts
```
GetMountData(pal)
GetMountSpeed(pal), SetMountSpeed(pal, multiplier)
GetSaddleDefinition(saddleId), ModifySaddleStat(saddleId, statName, value)
GetGliderData(playerId)
ModifyGliderStat(gliderId, statName, value)
```

#### 4.11 PalAPI.Content (PalSchema-compatible)
```
RegisterPal(palDef), RegisterItem(itemDef), RegisterBuilding(buildingDef), RegisterSkill(skillDef)
ValidateSchema(schemaDef)
LoadPalSchema(modPath)
— Compatible with PalSchema v0.5.2 format. Existing PalSchema mods work without modification
— Install path: NativeMods/UE4SS/Mods/PalSchema/mods/<ModName>/
```

#### 4.12 PalAPI.Events (complete event list)
```
On(eventName, callback), Off(eventName, callback), Emit(eventName, data)

Events:
  OnPalCaught, OnPalSummoned, OnPalReturned, OnPalDied
  OnPlayerDamaged, OnPlayerDied, OnPlayerRespawned, OnPlayerJoined, OnPlayerLeft
  OnBaseBuildingPlaced, OnBaseBuildingDestroyed, OnBaseLevelUp, OnBaseBuildingColorChanged
  OnRaidStart, OnRaidEnd, OnRaidBattlefieldEnter
  OnPvPKill, OnPvPStateChange
  OnDungeonEntered, OnDungeonCompleted
  OnTowerBossStarted, OnTowerBossDefeated
  OnItemCrafted, OnItemPickedUp, OnItemUsed
  OnEggLaid, OnEggHatched
  OnMountSummoned, OnMountDismissed
  OnServerTick
```

#### 4.13 Test all modules
- Every method tested on v0.7.3 in BOTH single-player AND private dedicated server
- Server tests run on Windows (Linux UE4SS inconsistent May 2026)
- PvP APIs tested with PvP enabled
- Full test suite runs as single command

### PHASE 4 GATE
- [ ] All 14 modules implemented
- [ ] All tests passing on v0.7.3
- [ ] Tested in both single-player and dedicated server
- [ ] Workshop-packaged via official uploader
- [ ] Tier 1 modules fully stable

---

## PHASE 5 — RESILIENCE & DEVELOPER TOOLING (Week 18–22)

### Objective
Make the framework survive Palworld 1.0 and give modders professional development tools.

### Steps

#### 5.1 Version detection and 1.0 readiness
- On startup: check game version against known-good version map
- Unknown version → enter compatibility mode, log affected modules
- 1.0 is a PLANNED BREAKING CHANGE — architecture treats it as expected
- Every module has fallback behavior:
  - **Graceful degradation:** missing hook → module disables itself with clear error, no crash
  - **Partial operation:** modules that can partially function (e.g. read-only when write hooks missing) do so

#### 5.2 AOB-based address resolution (built on CE MCP)
- Array of Bytes scanning finds game functions by code pattern, not fixed address
- **Implementation leverages Cheat Engine MCP's existing AOB scanning infrastructure**
- Phase 2 AOB signatures stored in versioned `/signatures` directory
- On each Palworld update, the update pipeline:
  1. Launches Palworld + attaches CE via MCP bridge
  2. Re-scans all stored AOB signatures
  3. Reports which resolve and which need update
  4. For failures, Ghidra MCP re-analyzes updated binary to find relocated functions
- AOB signature config updatable independently of framework code
- **This is the single most important technical differentiator vs PalSchema**

#### 5.3 Mod conflict resolution
- Two plugins modifying same property → framework detects conflict
- Resolves using priority system in plugin manifest
- Neither plugin crashes
- Conflicts logged to framework console
- Directly addresses core PalSchema problem: mods modifying same data table cancel each other silently

#### 5.4 Hot-reload for development
- File change detection in plugin folders
- Reloads only changed plugin without restarting game
- Preserves all other framework state
- Critical for rapid iteration during 2026 patch cycle

#### 5.5 Framework console
- In-game console (integrated with UE4SS console):
  - Framework version, Palworld version
  - All loaded plugins and status (loaded, error, disabled)
  - All active event subscriptions
  - Live error logging with stack traces
  - Command line for calling API methods directly
  - Conflict log

#### 5.6 Auto-generate documentation
- Generated from API source code
- Every method, parameters, return types, inline examples
- Static HTML site hosted on GitHub Pages
- Never manually maintained, never out of date
- Regenerated on every build

#### 5.7 Performance monitoring
- Track framework initialization time
- Track per-module load time
- Track event handler execution time
- Warn when any handler exceeds 16ms (one frame at 60fps)
- **Performance budget: < 5ms startup overhead, < 1ms per frame steady state**

### PHASE 5 GATE
- [ ] AOB scanning re-finds functions after simulated version bump
- [ ] Graceful degradation works for every module
- [ ] Conflict resolution works correctly
- [ ] Hot-reload works during development
- [ ] Documentation generates on build
- [ ] Performance within budget
- [ ] ALL above operational before Palworld 1.0 drops

---

## PHASE 6 — RELEASE & COMMUNITY (Week 22+)

### Steps

#### 6.1 Publish to Steam Workshop (primary distribution)
- Use official Palworld Mod Uploader
- Subscribing = the only install step users need
- All plugins declare framework as Required Item
- Steam auto-updates subscribers when framework updates

#### 6.2 Publish source to GitHub (Nexus as secondary)
- MIT license, open source, non-negotiable
- Nexus Mods as secondary distribution
- Detailed README: API overview, plugin quickstart, Workshop publishing guide, contribution guide

#### 6.3 Publish five starter plugins
Each is a Workshop item declaring framework as dependency:
1. **Pal Stat Editor** — demonstrates PalAPI.Pals
2. **Server Command System** — demonstrates PalAPI.Server
3. **Auto-Breeding Optimizer** — demonstrates PalAPI.Breeding
4. **Base Camp Manager** — demonstrates PalAPI.Base
5. **PvP Scoreboard** — demonstrates PalAPI.Combat (v0.7.0 PvP)

#### 6.4 Community strategy
- Join Palworld Modding Community Discord server
- Create dedicated framework support channel
- Documentation site with tutorials, not just API reference
- Contribution guide with clear standards

#### 6.5 Establish the 24-hour update pipeline (MCP-accelerated)
When Palworld patches (confirmed 3–4 week cadence):
1. Detect update (SteamCMD from D:\Tools\steamcmd automates version checking)
2. Launch updated Palworld + attach CE MCP → re-scan all stored AOB signatures
3. For failed signatures, load updated binary in Ghidra MCP → re-analyze relocated functions
4. Validate fixes via x64dbg MCP → breakpoints, confirm behavior matches
5. Update AOB signature config, test framework, push updated Workshop item
- Steam auto-updates all subscribers on Workshop push
- **Target: framework updated within 24 hours of any Palworld patch**
- Current ecosystem: days to weeks. MCP pipeline makes 24hr achievable

#### 6.6 Prepare for Palworld 1.0
- 1.0 internals "Top Secret" — no advance warning
- Readiness checklist:
  - All AOB signatures documented and tested
  - All modules have graceful degradation fallbacks
  - 1.0 compatibility beta published within 48 hours of update
  - Pre-built test suite validates all modules against new version in < 30 minutes

#### 6.7 Backward compatibility policy
- Framework API versioned semantically (major.minor.patch)
- Minor versions: new methods added, no existing methods changed
- Major versions: breaking changes allowed, documented in migration guide
- Plugin manifests declare minimum framework version
- Framework supports loading plugins built for previous minor versions

### PHASE 6 GATE
- [ ] Workshop item live and subscribable
- [ ] Five example plugins published and working
- [ ] GitHub public with MIT license
- [ ] Documentation site live
- [ ] Update pipeline tested against at least one real Palworld patch
- [ ] Backward compatibility policy documented

---

## NON-NEGOTIABLE PRINCIPLES

1. **Steam Workshop is the install experience.** Users subscribe. Steam downloads everything. If it requires more than two clicks it's not good enough.

2. **1.0 is the hard deadline.** Framework must be stable with working update pipeline before 1.0 drops. Not after.

3. **AOB scanning is mandatory.** PalSchema proved what happens without it. Every major patch breaks every mod. This is the reason the framework exists.

4. **Modders never touch UE4SS.** If using the framework requires interacting with UE4SS directly, the API has a gap.

5. **Graceful degradation over hard crashes.** A missing hook disables one module, not the entire framework.

6. **All four mod types interoperate.** Framework handles Lua natively, loads PalSchema via compatibility layer, coexists with LogicMods and Patch Paks.

7. **Performance is a constraint.** < 5ms startup overhead, < 1ms per frame. Laggy frameworks don't get adopted.

---

## COMPLETE API SURFACE SUMMARY

```
PalAPI.Pals          — 12 methods
PalAPI.Player        — 11 methods
PalAPI.Items         —  8 methods
PalAPI.Base          — 12 methods
PalAPI.Combat        — 10 methods
PalAPI.World         — 14 methods
PalAPI.Breeding      —  6 methods
PalAPI.Server        —  8 methods
PalAPI.UI            —  7 methods
PalAPI.Data          —  5 methods
PalAPI.Dungeons      — 10 methods
PalAPI.Mounts        —  5 methods
PalAPI.Content       —  6 methods
PalAPI.Events        — 25+ events

Total: 14 modules, ~139 methods, 25+ events
```

---

## ALL SOURCES (Verified May 16, 2026)

| Source | URL | Verified |
|--------|-----|----------|
| Palworld v0.7.0 patch notes | steamcommunity.com/app/1623730/allnews | Dec 17 2025 |
| Palworld v0.7.1 patch notes | game8.co/games/Palworld/archives/575468 | Jan 22 2026 |
| Palworld v0.7.2-v0.7.3 patches | paldb.cc | Apr 6 2026 |
| Official Mod Uploader | github.com/pocketpairjp/PalworldModUploader | Dec 2025 |
| UE4SS Palworld fork | github.com/Okaetsu/RE-UE4SS | Jan 17 2026 |
| PalSchema | github.com/Okaetsu/PalSchema | Jan 17 2026 |
| UE4SS Lua API docs | docs.ue4ss.com/lua-api | 2025 |
| Palworld modding wiki | pwmodding.wiki | 2025-2026 |
| Palworld Modding Kit | github.com/localcc/PalworldModdingKit | 2025 |
| Workshop install guide | pwmodding.wiki/docs/users/workshop/installing-mods | Dec 2025 |
| Logic Mods documentation | pwmodding.wiki/docs/developers/ue4ss-modding/logic-mods/introduction | 2025 |
| Official server mod docs | docs.palworldgame.com/settings-and-operation/mod | 2025-2026 |
| Server mod guide | winternode.com/blog/palworld/best-server-mods | Mar 20 2026 |
| 2026 roadmap analysis | supercraft.host/article/palworld-roadmap-2026 | May 2026 |
| CurseForge mod types | curseforge.com/palworld | Mar 2026 |
| Modding safety | exitlag.com/blog/palworld-mods | Feb 16 2026 |
| Ghidra MCP | D:\Tools\ghidra-mcp\CLAUDE.md | Local, v5.6.0 |
| Cheat Engine MCP | D:\Tools\cheat-engine-mcp\CLAUDE.md | Local, v12.0.0 |
| x64dbg MCP | D:\Tools\x64dbgMCP\README.md | Local |
