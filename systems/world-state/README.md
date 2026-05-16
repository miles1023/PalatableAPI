# systems/world-state/

The persistent world: terrain objects, resource nodes, dungeon state, placed items.

## What this system covers

- Object placement in the world (buildings, chests, resource nodes)
- Resource node regeneration timing
- Dungeon instance state
- Fast travel point unlock state

## Known data

- Level.sav contains world object placement and state
- Map object interaction: UE4SS hook `PalMapObjectConcreteModelBase:OnTriggerInteract`
- Map object UI close: UE4SS hook `PalMapObject:OnCloseParameter`

## Open questions

- How to enumerate all placed objects in the world at runtime
- How resource node respawn timers are stored
- Dungeon instance class name
- Fast travel point UE class name

## Access surfaces

- Save file: Level.sav (authoritative for offline state)
- UE4SS: map object interaction hooks confirmed

## Status: PARTIAL
