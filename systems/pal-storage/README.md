# systems/pal-storage/

The PalBox and base-level Pal container systems.

## What this system covers

- PalBox: the main Pal storage accessed by the player
- Base Pal storage: Pals assigned to a base camp
- Container class shared with item containers (UPalItemContainer)

## Key data

- Max slots per container
- Pal assignment to slots
- Base ID or player UID that owns the container
- Pal data per slot: references UPalIndividualCharacterParameter

## Save file location

`PalStorage_<uid>.sav` — one per base/player. Parsed by palworld-save-tools.

## Open questions

- Exact class name for Pal container (separate from UPalItemContainer or the same?)
- Live access path from a player to their PalBox during a session
- How base-assigned Pals differ from party Pals in memory layout

## Related systems

- pal-character/ — individual Pal data that each slot holds
- base-camp/ — base camp that owns a base Pal storage container
