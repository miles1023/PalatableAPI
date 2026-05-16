# systems/technology-tree/

The research system tracking which technologies a player has unlocked.

## What this system covers

- Per-player list of unlocked technology IDs
- Technology points (currency for unlocking)
- Technology tier gating (what is available at what level)
- Technology DataTable (if one exists — not yet confirmed)

## Known data

- Technology state is in the player save file (`Players/<uid>.sav`)
- Each tech has an ID (FName or similar)
- Tech points are a player resource

## Open questions

- Is there a DataTable for technology definitions? Name unknown.
- Live UE class name for the technology component or manager
- How to read/write tech unlock state at runtime (live game)
- Are there hooks for when a player unlocks a technology?

## Access surfaces

- Save file: confirmed (per-player save contains tech state)
- UE4SS reflection: class name unknown, not yet mapped

## Status: INFERRED — save file structure known, live access path unknown
