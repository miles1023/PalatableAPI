# systems/item-system/

Static DataTables defining all game items.

## DataTables in this system

- **DA_StaticItemDataAsset** (20 columns) — item properties
- **DT_PalDropItem** (41 columns) — Pal drop tables
- **DT_ItemRecipeDataTable** (13 columns) — crafting recipes

## Key columns (DA_StaticItemDataAsset, confirmed)

- ItemID — FName unique identifier
- Price — int
- MaxStackCount — int
- Weight — float
- bLegalInGame — bool (whether item is obtainable)
- AttackValue — int (weapons)
- MagazineSize — int (guns)
- RestoreSatiety — int (food)
- RestoreHP — int (food/medicine)

## Key columns (DT_ItemRecipeDataTable, confirmed)

- WorkAmount — float (crafting time/effort)

## Access surfaces

- FModel + Mappings.usmap (read)
- PalSchema / PAK mod (modify)

## Pre-migration data

See `findings/pre-migration/datatables/DA_StaticItemDataAsset.yml`,
`DT_PalDropItem.yml`, `DT_ItemRecipeDataTable.yml`
