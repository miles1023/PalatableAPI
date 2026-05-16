# Extracted from commands.yml — 2026-05-15
# Source: previous session's command mapping file (now deleted)
# Status: needs processing through pipeline into findings/
# These are confirmed access chains and column names from community research

---

## Confirmed Entity Access Chains

The following paths were mapped in the previous session. They describe how to traverse
from a player or Pal actor to a specific property. All confirmed against NightFyre SDK
and community UE4SS mods. Game version: 0.7.1.

| Property | Entity | Field | Access Chain | Value Type | Notes |
|----------|--------|-------|--------------|------------|-------|
| HP (player) | UPalIndividualCharacterParameter | Hp | CharacterParameterComponent → IndividualParameter | FFixedPoint | inner field unconfirmed |
| MaxHP (player) | UPalIndividualCharacterParameter | MaxHP | CharacterParameterComponent → IndividualParameter | FFixedPoint | inner field unconfirmed |
| Hunger/FullStomach | UPalIndividualCharacterParameter | FullStomach | CharacterParameterComponent → IndividualParameter | float | |
| Sanity | UPalIndividualCharacterParameter | SanityValue | CharacterParameterComponent → IndividualParameter | float | range: 0.0–100.0 |
| Invincible | UPalCharacterParameterComponent | bIsEnableMuteki | CharacterParameterComponent | bool | |
| Walk Speed | UPalCharacterMovementComponent | MaxWalkSpeed | CharacterMovement | float | default: 600.0 |
| Max Carry Weight | UPalPlayerInventoryData | MaxInventoryWeight | Controller → PlayerState → InventoryData | float | |
| HP (pal) | UPalIndividualCharacterParameter | Hp | CharacterParameterComponent → IndividualParameter | FFixedPoint | same as player |
| MaxHP (pal) | UPalIndividualCharacterParameter | MaxHP | CharacterParameterComponent → IndividualParameter | FFixedPoint | same as player |
| Hunger (pal) | UPalIndividualCharacterParameter | FullStomach | CharacterParameterComponent → IndividualParameter | float | |
| Sanity (pal) | UPalIndividualCharacterParameter | SanityValue | CharacterParameterComponent → IndividualParameter | float | range: 0.0–100.0 |

---

## Confirmed DataTable Columns

### DA_StaticItemDataAsset (items)

| Column | Type | Notes |
|--------|------|-------|
| Price | int | Gold value |
| MaxStackCount | int | Max stack size |
| Weight | float | Item weight |
| bLegalInGame | bool | Whether item is obtainable |
| AttackValue | int | Weapon damage |
| MagazineSize | int | Gun magazine size |
| RestoreSatiety | int | Food hunger restoration |
| RestoreHP | int | Food/medicine HP restoration |

### DT_PalMonsterParameter (Pal species base stats)

Additional confirmed columns not in pre-migration YAML:

| Column | Type | Notes |
|--------|------|-------|
| CaptureRateCorrect | float | Base capture rate modifier |
| Hp | int | Base HP stat |
| MeleeAttack | int | |
| ShotAttack | int | |
| Defense | int | |
| RunSpeed | int | |
| RideSprintSpeed | int | Mount sprint speed |
| Nocturnal | bool | Activity timing |
| AIResponse | FName | EPalAIResponseType enum |

### DT_PalMonsterParameter — WorkSuitability columns (all 13 confirmed)

Format: `WorkSuitability_<EnumValue>` — integer level 0–4

| Column | Plain name |
|--------|-----------|
| WorkSuitability_EmitFlame | Fire / Kindling |
| WorkSuitability_Watering | Watering |
| WorkSuitability_Seeding | Planting |
| WorkSuitability_GenerateElectricity | Electricity |
| WorkSuitability_Handcraft | Crafting / Handiwork |
| WorkSuitability_Collection | Gathering |
| WorkSuitability_Deforest | Lumbering |
| WorkSuitability_Mining | Mining |
| WorkSuitability_OilExtraction | Oil Extraction |
| WorkSuitability_ProductMedicine | Medicine Production |
| WorkSuitability_Cool | Cooling |
| WorkSuitability_Transport | Transporting |
| WorkSuitability_MonsterFarm | Farming / Ranch |

### DT_ItemRecipeDataTable (crafting)

| Column | Type | Notes |
|--------|------|-------|
| WorkAmount | float | Crafting effort/time |

### DT_BuildObjectDataTable (buildings)

| Column | Type | Notes |
|--------|------|-------|
| Hp | int | Building HP |

---

## Special Values (from command grammar)

| Token | Resolution |
|-------|-----------|
| infinite | 99999999.0 |
| max | read the corresponding _max field at runtime |
| min | 0.0 |
| default | read the default from the column definition |
| free | 0 |
| full | read the corresponding _max field at runtime |
| empty | 0.0 |

---

## Processing status

These findings have been read and recorded here. Next step: process each row through
the ingestion pipeline (workflow/PIPELINE.md) and write canonical finding files.
The access chain rows go into systems/player-character/ and systems/pal-character/.
The DataTable columns go into the relevant systems/ folder per table.
