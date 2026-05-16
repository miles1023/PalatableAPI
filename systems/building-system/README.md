# systems/building-system/

Static DataTable for placeable buildings, plus live building object state.

## DataTable

**DT_BuildObjectDataTable** (18 columns, all confirmed from PalSchema)

Key columns: BuildObjectID, Hp, Defense, BelongTo, RequiredBuildWorkAmount, WorkSuitability, IsExternal, IsTechnology

## Live state

Placed buildings in the world are map objects (`PalMapObjectConcreteModelBase`). Each has:
- An interaction trigger (hooked: OnTriggerInteract)
- A UI close event (hooked: OnCloseParameter)
- A server-side state object

## Access surfaces

- DT_BuildObjectDataTable: FModel + Mappings.usmap, PalSchema, PAK mod
- Live building objects: UE4SS hooks (OnTriggerInteract, OnCloseParameter)

## Pre-migration data

See `findings/pre-migration/datatables/DT_BuildObjectDataTable.yml`
