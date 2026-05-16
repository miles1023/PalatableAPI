# systems/

One subfolder per major game system identified in `survey/GAME_SYSTEMS.md`.

## Current system folders

| Folder | Game system |
|--------|-------------|
| player-character/ | Player actor, controller, stats (HP, hunger, stamina, speed) |
| player-inventory/ | Item containers, slots, carry weight |
| pal-character/ | Individual Pal actor, stats, skills, AI state |
| pal-storage/ | PalBox, base Pal containers |
| pal-data-static/ | DT_PalMonsterParameter — base stats per species |
| item-system/ | DA_StaticItemDataAsset, DT_PalDropItem, DT_ItemRecipeDataTable |
| building-system/ | DT_BuildObjectDataTable, placed building state |
| combat-waza/ | DT_WazaDataTable, DT_WazaMasterLevel, damage calculation |
| technology-tree/ | Research unlock state, tech points |
| guild-system/ | Guild membership, ownership, shared resources |
| base-camp/ | Base camp object, Pal assignments, work queues |
| world-state/ | Placed objects, resource nodes, dungeon state |
| time-weather/ | Day/night cycle, weather state |
| ai-behavior/ | Wild Pal and NPC AI, aggro, behavior trees |
| server-session/ | Connected players, server authority, replication |
| crafting-production/ | Crafting queue, production buildings |
| player-progression/ | Level, XP, stat points |
| event-system/ | All observable game events and hook points |
| pal-capture/ | Sphere throwing, capture rate calculation |
| pal-breeding/ | Breeding combinations, egg incubation |
| audio-visual/ | Cosmetics only — PAK-modifiable assets |

## What goes in each subfolder

- An INDEX.md summarizing what is known about this system
- Finding files from `findings/` that are system-specific
- Open questions relevant to this system

## Rules

- If a finding belongs to multiple systems, put it in the most relevant one and reference it from the others.
- If a new system is discovered, add it to `survey/GAME_SYSTEMS.md` first, then create the folder.
- Do not add API design or command syntax here. Systems are internal game structures only.
