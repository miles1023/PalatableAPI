# GAME_SYSTEMS.md — Palworld Internal Game Systems Survey
# Phase 0 output.
# Last updated: 2026-05-15

---

> ## WARNING
> **This file was seeded from AI training data. All entries are unverified
> until confirmed against current 2026 sources provided by the user.**
>
> Training data cutoff is approximately mid-2024. Palworld has been in active
> development since then. Class names, component structures, DataTable schemas,
> field names, and system descriptions may be wrong or out of date.
> Do not treat any entry here as accurate without verifying against a current source.

---

## What this file is

Every internal system inside Palworld that has been observed, documented, or inferred
from community mod research, source analysis, and reverse engineering. Each entry
describes what the system does, what data it contains, and how external tools have
interacted with it.

Confidence levels:
- KNOWN — directly observed via mods, CheatEngine, UHT dump, or DataTable export
- INFERRED — deduced from class names, hook paths, enum values, or related confirmed systems
- UNKNOWN — suspected to exist but no data found yet

---

## SYSTEM 1: Player Character
**[UNVERIFIED — training data, may be outdated]**

**What it is:** The live in-game player actor. In UE5 terms, an APawn derived from APalPlayerCharacter.

**Subcomponents:**
- `APalPlayerCharacter` — the actor itself (position, rotation, visual)
- `APalPlayerController` — processes input, manages possession
- `APalPlayerState` — persisted server-side state (name, level, etc.)
- `UPalCharacterParameterComponent` — current runtime stats (HP, hunger, stamina)
- `UPalIndividualCharacterParameter` — permanent character data
- `UPalCharacterMovementComponent` — movement speed, jump, fall, swim, fly

**Known data fields (from UHT + NightFyre SDK):**
- HP (current, max) — stored as FFixedPoint
- Hunger — float
- Stamina — current
- Shield / defense
- Movement speed
- Player name (FString)
- Player UID / Steam ID
- Level / experience (on PlayerState)
- Player coordinates (FVector on Actor)
- Rotation

**Known writable state (from community mods):**
- HP: writable but authority is server-side in multiplayer
- Movement speed: client-side write works cosmetically; may desync on server
- Position: teleport works if done server-side

**Access surfaces:** UE4SS reflection (most fields), CheatEngine (FFixedPoint inner), REST API (coordinates, level read-only)

**Confidence:** KNOWN

---

## SYSTEM 2: Player Inventory
**[UNVERIFIED — training data, may be outdated]**

**What it is:** The container holding a player's items. Separate containers exist for
main inventory, equipment slots, key items, and hotbar.

**Subcomponents:**
- `UPalPlayerInventoryData` — top-level player inventory manager
- `UPalItemContainer` — a generic container (used for main bag, equipment, etc.)
- `UPalItemSlot` — a single slot within a container (item ID + stack count + durability)

**Known data fields:**
- Item ID (FName) — references `DA_StaticItemDataAsset`
- Stack count (int32)
- Durability (float, 0.0–1.0)
- Slot index

**Known writable state:**
- Items can be added via `RequestAddItem` UFunction (UE4SS reflected)
- Item removal: not yet confirmed via reflection
- Inventory slot count: `InventorySlotNum` on player stats component

**Access surfaces:** UE4SS reflection, Save file parsing, REST API (item spawn endpoint)

**Confidence:** KNOWN (structure) / PARTIAL (write paths)

---

## SYSTEM 3: Pal Character (Individual)
**[UNVERIFIED — training data, may be outdated]**

**What it is:** A live Pal actor in the world — either following the player, in combat,
or placed in a base. Uses `APalCharacter` class hierarchy.

**Subcomponents:**
- `APalCharacter` — the actor (position, model, combat state)
- `UPalCharacterParameterComponent` — same component as player, holds runtime stats
- `UPalIndividualCharacterParameter` — Pal-specific permanent data (level, passive skills, etc.)
- `UPalAIComponent` or similar — AI behavior state (unconfirmed name)

**Known data fields:**
- HP (current, max)
- Attack, defense, work speed — base stats
- Level / experience
- Passive skills (list of EPalPassiveSkillList values)
- Active skills / learned attacks (Waza list)
- Partner skill
- Pal species (EPalTribeID)
- Gender (EPalGenderType)
- Nickname (FString, nullable)
- Pal rank (condensed — 0–5 stars equivalent)
- Hunger
- Sanity / mood (inferred from work system)
- Pal UUID (unique instance identifier)

**Access surfaces:** UE4SS reflection, Save file parsing (PalStorage_.sav), CheatEngine

**Confidence:** KNOWN (structure from NightFyre SDK) / PARTIAL (write paths)

---

## SYSTEM 4: Pal Storage / Container (PalBox)
**[UNVERIFIED — training data, may be outdated]**

**What it is:** The Pal storage system — the "PalBox" that holds captured Pals not in
the active party. Players have one PalBox, bases have base-specific storage.

**Subcomponents:**
- `UPalItemContainer` (also used for item containers — generic container class)
- Per-Pal slots containing `UPalIndividualCharacterParameter` references

**Known data:**
- Max Pal slots per container
- Pal assignment to slots
- Base ID or player UID owning the container

**Access surfaces:** Save file parsing (PalStorage_.sav files), UE4SS reflection (via container class), REST API (limited)

**Confidence:** KNOWN (structure) / PARTIAL (live access paths)

---

## SYSTEM 5: Static Pal Data (DataTable)
**[UNVERIFIED — training data, may be outdated]**

**What it is:** The read-only spreadsheet defining every Pal species' base values.
This is not live state — it is the template that live Pal instances are built from.

**DataTable:** `DT_PalMonsterParameter`

**Known columns (55 total, all confirmed from PalSchema):**
- BPClass, OverrideNameTextID — species identity
- ElementType1, ElementType2 — element types
- AIResponse — combat behavior (EPalAIResponseType)
- Size — body size (EPalSizeType)
- GenusCategory — movement type category
- Organization — faction affiliation
- Rarity — capture/drop rarity
- HP, MeleeAttack, ShotAttack, Defense, Support, CraftSpeed — base stats
- MaxFullStomach, FullStomachDecreaseRate, FoodAmount — hunger parameters
- CaptureRateCorrect — base capture rate modifier
- ExpRate — experience given when defeated
- PalTribe — maps to EPalTribeID
- NocturnalType — activity timing
- BattleBGM — combat music type
- Work suitability columns (EmitFlame, Watering, Seeding, etc. — 14 types)
- Many more (passive skill slots, partner skill data, etc.)

**Access surfaces:** FModel export, PalSchema JSON patches, PAK mod replacement

**Confidence:** KNOWN — all 55 columns documented in existing knowledge base

---

## SYSTEM 6: Item System (Static Data)
**[UNVERIFIED — training data, may be outdated]**

**What it is:** The static definitions for every item in the game.

**DataTables:**
- `DA_StaticItemDataAsset` — item properties (weight, stack size, rarity, item type)
- `DT_PalDropItem` — Pal drop tables (what each Pal drops when defeated, and at what rate)
- `DT_ItemRecipeDataTable` — crafting recipes (ingredients + quantities + output)

**Known data (DA_StaticItemDataAsset — 20 columns):**
- ItemID (FName) — unique identifier
- DisplayName, Description
- Type (weapon, armor, consumable, material, etc.)
- MaxStackCount
- Weight
- SortID
- IsConsumable, IsTechnology, IsQuestItem flags
- Gold value

**Access surfaces:** FModel, PalSchema, PAK mods

**Confidence:** KNOWN

---

## SYSTEM 7: Building System (Static Data)
**[UNVERIFIED — training data, may be outdated]**

**What it is:** The static definitions for all placeable building objects.

**DataTable:** `DT_BuildObjectDataTable`

**Known data (18 columns):**
- BuildObjectID
- DisplayName, Description
- HP, Defense
- BelongTo (ownership type)
- RequiredBuildWorkAmount
- WorkSuitability (what Pal work type can interact with it)
- ReplicateType
- IsExternal, IsTechnology flags
- Many more (build cost, category, etc.)

**Access surfaces:** FModel, PalSchema, PAK mods

**Confidence:** KNOWN

---

## SYSTEM 8: Combat / Skill System (Waza)
**[UNVERIFIED — training data, may be outdated]**

**What it is:** The system governing Pal attacks and skills. "Waza" is the internal term
for attack/skill moves.

**DataTables:**
- `DT_WazaDataTable` — individual skill definitions (damage, type, cooldown, etc.)
- `DT_WazaMasterLevel` — level-up skill learning table (which Pal learns which Waza at which level)

**Known data (DT_WazaDataTable — ~4 columns confirmed, more unknown):**
- WazaID — unique skill identifier
- WazaType — element type (EPalElementType)
- Power — base damage
- (Other columns: NOT YET CONFIRMED — needs FModel with current Mappings.usmap)

**Known data (DT_WazaMasterLevel):**
- Maps Pal species + level → Waza learned at that level

**Access surfaces:** FModel (Mappings.usmap required for full export), PAK mods, PalSchema

**Confidence:** PARTIAL — column names not yet confirmed for DT_WazaDataTable (open TODO)

---

## SYSTEM 9: Technology Tree / Research System
**[UNVERIFIED — training data, may be outdated]**

**What it is:** The system tracking which technologies a player has researched.
Determines what items and buildings can be crafted.

**Known data:**
- Per-player list of unlocked tech IDs
- Technology points (currency for unlocking)
- Tech tier gating

**Access surfaces:** Save file (Players/<uid>.sav contains tech tree state), UE4SS reflection (inferred — not yet confirmed)

**Confidence:** KNOWN (save file) / INFERRED (live access path)

---

## SYSTEM 10: Guild System
**[UNVERIFIED — training data, may be outdated]**

**What it is:** Player organizations. Guilds share a base and resources.

**Known data:**
- Guild ID
- Guild name
- Member list (player UIDs)
- Guild base assignment
- Shared item storage (via base chest)

**Access surfaces:** Save file (Level.sav), REST API (`/v1/api/guilds`), UE4SS (PalBaseCampModel hook exists in hooks.yml)

**Confidence:** KNOWN (structure) / PARTIAL (live write paths)

---

## SYSTEM 11: Base Camp System
**[UNVERIFIED — training data, may be outdated]**

**What it is:** Player-owned bases where Pals work. Each base has assigned Pals,
buildings, storage, and work queues.

**Known classes:**
- `PalBaseCampModel` — the base camp object (NotifyOnNewObject hook exists)
- Base camp has attached storage, Pal assignments, building list

**Known data:**
- Base ID / owner guild
- Base level
- Assigned Pal list
- Building object list
- Base location coordinates

**Access surfaces:** UE4SS (PalBaseCampModel hook), Save file (Level.sav), REST API (limited)

**Confidence:** KNOWN (hook path) / PARTIAL (field-level details)

---

## SYSTEM 12: World State / Map
**[UNVERIFIED — training data, may be outdated]**

**What it is:** The persistent world — terrain, placed objects, resource nodes,
dungeon state, and world events.

**Known data:**
- Object placement (from Level.sav)
- Resource node regeneration state
- Dungeon instances
- Fast travel point unlock state

**Access surfaces:** Save file (Level.sav), UE4SS (map object interaction hooks exist)

**Confidence:** KNOWN (save file) / INFERRED (live world query paths)

---

## SYSTEM 13: Time / Weather System
**[UNVERIFIED — training data, may be outdated]**

**What it is:** In-game day/night cycle and weather state.

**Known data:**
- Current time of day
- Weather state
- Day/night cycle speed (config setting)

**Access surfaces:** Config file (day cycle speed), UE4SS reflection (inferred — no confirmed hook path yet)

**Confidence:** INFERRED — no confirmed hook paths or direct access methods documented yet

---

## SYSTEM 14: AI / Behavior System
**[UNVERIFIED — training data, may be outdated]**

**What it is:** The AI governing wild Pal and enemy NPC behavior. Separate from the
player-controlled Pal behavior system.

**Known data:**
- AI response type (EPalAIResponseType: Ignore, Escape, Battle, Special)
- Behavior tree state
- Aggro target
- Patrol/wander state

**Access surfaces:** DT_PalMonsterParameter (AIResponse column), UE4SS (behavior hooks not yet found)

**Confidence:** PARTIAL — static data known; live AI state access not yet mapped

---

## SYSTEM 15: Server / Multiplayer Session
**[UNVERIFIED — training data, may be outdated]**

**What it is:** The dedicated server session management: who is connected, server authority,
tick rate, and replication state.

**Known data:**
- Connected player list
- Player UIDs / Steam IDs
- Server tick rate
- Server world authority

**Known functions:**
- Player join event (ServerAcknowledgePossession hook — confirmed)
- Player kick/ban (RCON + REST API)
- World save trigger

**Access surfaces:** RCON, REST API, UE4SS (ServerAcknowledgePossession hook)

**Confidence:** KNOWN (interfaces) / PARTIAL (internal session object access)

---

## SYSTEM 16: Crafting / Production System
**[UNVERIFIED — training data, may be outdated]**

**What it is:** Player and Pal-assisted crafting. Includes manual crafting, production
buildings (furnace, etc.), and automatic Pal work.

**Known data:**
- Recipe definitions (DT_ItemRecipeDataTable)
- Production queue state (inferred — no confirmed class name yet)
- Work assignment to Pals

**Access surfaces:** DT_ItemRecipeDataTable (FModel/PalSchema), UE4SS (map object interaction hooks), Save file

**Confidence:** KNOWN (recipe data) / INFERRED (production queue live state)

---

## SYSTEM 17: Player Progression (Level / XP)
**[UNVERIFIED — training data, may be outdated]**

**What it is:** Player character leveling, experience gain, and stat scaling.

**Known data:**
- Player level (on APalPlayerState)
- Experience points
- Stat upgrade points

**Access surfaces:** UE4SS (APalPlayerState via reflection), Save file, REST API (level in player list)

**Confidence:** KNOWN

---

## SYSTEM 18: Event System (Hooks)
**[UNVERIFIED — training data, may be outdated]**

**What it is:** The set of game events that external code can observe or intercept.
These are the "things that happen" in the game — actions, transitions, lifecycle events.

**Confirmed hook paths (from hooks.yml):**
- ClientRestart — player controller init (client)
- ServerAcknowledgePossession — player controller init (server)
- BroadcastChatMessage — chat message broadcast
- PalMapObjectConcreteModelBase:OnTriggerInteract — world object interaction
- PalMapObject:OnCloseParameter — world object UI close
- PalPartnerSkillParameterComponent:GetActiveSkillMainValueByRank — partner skill value read
- WBP_PalPlayerInventoryScrollList:Construct — inventory UI open
- WBP_ItemChest:Destruct — chest UI close
- BP_OtomoPalHolderComponent:ActivateOtomo — companion Pal switch
- PalBaseCampModel (NotifyOnNewObject) — base camp creation

**Known missing hook paths (open TODOs):**
- Player death event
- Pal capture event
- Player level-up event
- Base camp raid/attack event
- Item pickup event
- Crafting complete event
- Fast travel event

**Access surfaces:** UE4SS RegisterHook / NotifyOnNewObject

**Confidence:** KNOWN (confirmed paths) / UNKNOWN (missing paths)

---

## SYSTEM 19: Pal Capture System
**[UNVERIFIED — training data, may be outdated]**

**What it is:** The system for throwing Pal Spheres and capturing wild Pals.

**Known data:**
- Capture rate calculation (base from DT_PalMonsterParameter.CaptureRateCorrect)
- Sphere tier multiplier
- Pal HP at time of throw affects success chance

**Known events:** Capture event hook path — NOT YET FOUND (open TODO)

**Access surfaces:** DT_PalMonsterParameter (static capture rate), CheatEngine (live capture calc — not yet mapped)

**Confidence:** PARTIAL

---

## SYSTEM 20: Pal Breeding System
**[UNVERIFIED — training data, may be outdated]**

**What it is:** The system for breeding two Pals to produce an egg.

**Known data:**
- Breeding combinations (inferred to exist as DataTable or hardcoded logic)
- Egg incubation time
- Inherited stats/skills rules

**Access surfaces:** Not yet mapped to any known hook or DataTable

**Confidence:** INFERRED — system exists in the game but no confirmed access path

---

## SYSTEM 21: Audio / Visual (Cosmetic Layer)
**[UNVERIFIED — training data, may be outdated]**

**What it is:** Sound effects, music, models, textures, animations, UI.

**Why included:** PAK mods routinely modify these. Not a target for RE work on game internals,
but relevant as a known modding surface.

**Access surfaces:** PAK mod asset replacement

**Confidence:** KNOWN

---

## Game Systems Completeness Assessment
**[UNVERIFIED — training data, may be outdated]**

| System | Data Known? | Live Access Path Known? |
|--------|-------------|------------------------|
| Player Character | Yes | Partial |
| Player Inventory | Yes | Partial |
| Pal Character (Individual) | Yes | Partial |
| Pal Storage (PalBox) | Yes | Partial |
| Static Pal Data (DT) | Yes | Yes (DataTable) |
| Item System (Static) | Yes | Yes (DataTable) |
| Building System (Static) | Yes | Yes (DataTable) |
| Combat / Waza | Partial | No (DT columns unknown) |
| Technology Tree | Partial | No |
| Guild System | Partial | Partial |
| Base Camp System | Partial | Partial |
| World State / Map | Partial | No |
| Time / Weather | No | No |
| AI / Behavior | Partial | No |
| Server Session | Yes | Yes |
| Crafting / Production | Partial | No |
| Player Progression | Yes | Yes |
| Event System (Hooks) | Partial | Partial |
| Pal Capture | Partial | No |
| Pal Breeding | No | No |
| Audio / Visual | N/A | Yes (PAK) |
