# systems/pal-data-static/

Static DataTable defining every Pal species' base values.

## What this system covers

DataTable: DT_PalMonsterParameter (55 columns, all confirmed from PalSchema)

This is read-only data loaded at game startup. It defines the template every live Pal instance is built from.

## Key columns (selected)

- BPClass — Blueprint class reference
- ElementType1, ElementType2 — element types (EPalElementType)
- Hp, MeleeAttack, ShotAttack, Defense, Support, CraftSpeed — base stats
- CaptureRateCorrect — base capture rate modifier
- RunSpeed, RideSprintSpeed — movement speeds
- AIResponse — default AI behavior (EPalAIResponseType)
- Nocturnal — activity timing
- WorkSuitability_EmitFlame through WorkSuitability_MonsterFarm — 13 work suitability levels
- PalTribe — maps to EPalTribeID

## Access surfaces

- FModel + Mappings.usmap (read all rows)
- PalSchema / PAK mod (modify rows)
- UE4SS at runtime (read via StaticFindObject → PalMasterDataTablesUtility)

## Pre-migration data

See `findings/pre-migration/datatables/DT_PalMonsterParameter.yml`
