# systems/crafting-production/

Player and Pal-assisted crafting and production.

## What this system covers

- Manual player crafting
- Production buildings (furnace, cooler, etc.)
- Pal work assignments to production buildings
- Production queue state

## Known data

- DT_ItemRecipeDataTable: WorkAmount (crafting effort/time), ingredients, outputs — 13 columns total
- Building interaction hook: `PalMapObjectConcreteModelBase:OnTriggerInteract`
- Building UI close hook: `PalMapObject:OnCloseParameter`

## Open questions

- Class name for the production queue on a building
- How to read the current queue state at runtime
- Hook path for crafting-complete event
- Pal work assignment class and properties

## Access surfaces

- DT_ItemRecipeDataTable: FModel, PalSchema (static recipe data)
- UE4SS: building interaction hooks (entry/exit events only, not queue state)

## Pre-migration data

See `findings/pre-migration/datatables/DT_ItemRecipeDataTable.yml`

## Status: PARTIAL — recipe data known, live queue access unknown
