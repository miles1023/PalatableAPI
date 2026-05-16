# systems/base-camp/

Player-owned bases where Pals work.

## What this system covers

- PalBaseCampModel — the base camp object (confirmed hook path via NotifyOnNewObject)
- Assigned Pal list
- Building object list
- Base location, level, and owner
- Work queue state

## Known data

- NotifyOnNewObject path: `/Script/Pal.PalBaseCampModel` — fires when a base camp is created or loaded
- Base data is in Level.sav

## Open questions

- Full property list on PalBaseCampModel (needs UHT dump inspection)
- How to read the list of assigned Pals on a specific base
- Hook path for base camp attack / raid event
- Base camp level and how it affects capacity

## Access surfaces

- UE4SS: NotifyOnNewObject hook confirmed
- Save file: Level.sav (building list, Pal assignments)

## Status: PARTIAL
