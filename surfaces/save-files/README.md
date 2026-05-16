# surfaces/save-files/

Palworld save file parsing — offline editing of game state.

## File locations

**Client:**
`%LOCALAPPDATA%\Pal\Saved\SaveGames\<steam-uid>\`

**Dedicated server:**
`PalServer/Pal/Saved/SaveGames/`

## Save file types

| File | Contents |
|------|----------|
| Level.sav | World state: placed buildings, map objects, guild data |
| LocalData.sav | Local player data (client only) |
| Players/<steam64-uid>.sav | Per-player: inventory, stats, position, tech tree, appearance |
| PalStorage_<uid>.sav | Pal storage per base/player (PalBox contents) |

## Tools

- `palworld-save-tools` (Python) — parse and write save files
- `palworld-pal-editor` (web-based) — GUI editor for Pal data

## What it exposes

- Player inventory (item IDs, counts, durability)
- Player stats (HP, hunger, XP, level, tech points)
- Player equipment and hotbar
- Pal data (species, stats, level, passive skills, active skills, nickname, rank)
- World object placement
- Guild data
- Technology research status
- Player appearance

## Critical constraint

The game must NOT be running when editing save files. The save is locked during gameplay and will be overwritten on next save.

## Version notes

Save file format can change on game updates. palworld-save-tools must be updated after major updates.

## Status: KNOWN
