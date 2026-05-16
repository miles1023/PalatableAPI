# systems/player-inventory/

The container system holding a player's items.

## What this system covers

- UPalPlayerInventoryData — top-level inventory manager
- UPalItemContainer — generic container (main bag, equipment, hotbar, etc.)
- UPalItemSlot — a single slot: item ID + stack count + durability

## Key fields known

- Item ID: FName, references DA_StaticItemDataAsset
- Stack count: int32
- Durability: float (0.0–1.0)
- MaxInventoryWeight: float (on UPalPlayerInventoryData)
- Inventory slot count: InventorySlotNum

## Known write paths

- RequestAddItem — UFunction (reflected), callable via UE4SS. Adds items to player inventory.
- Item removal: not yet confirmed via reflection

## Access chains confirmed

- UPalPlayerInventoryData: APalPlayerCharacter → Controller → PlayerState → InventoryData

## Open questions

- Confirmed method signature for RequestAddItem (arg types and order)
- Method for removing items
- How equipment slot items differ from main inventory slots

## Pre-migration data

See `findings/pre-migration/entities/UPalItemContainer.yml`,
`UPalItemSlot.yml`, `UPalPlayerInventoryData.yml`
