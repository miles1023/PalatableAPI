# relationships/

Cross-system dependency maps and relationship documentation.

## Purpose

Game systems do not exist in isolation. A finding in one system often depends on or is referenced by another. This folder documents those connections so that:
- When mapping one system, you know what to check in others
- A change to one system's understanding updates all dependent findings
- No system is mapped in isolation without checking its neighbors

## What belongs here

- Dependency maps: "System A reads from System B at runtime"
- Access chain diagrams: "To reach field X, you traverse objects Y and Z"
- Component ownership: "UPalCharacterParameterComponent is owned by both APalPlayerCharacter and APalCharacter"
- DataTable linkages: "DT_WazaMasterLevel references DT_WazaDataTable by WazaID"
- Event chains: "Event A triggers System B which modifies System C"

## File naming

`YYYY-MM-DD-brief-description.md`

## Example: shared component

UPalCharacterParameterComponent and UPalIndividualCharacterParameter are used by BOTH player-character AND pal-character systems. Findings about these components belong in `systems/player-character/` (primary) with a reference note in `systems/pal-character/`.
