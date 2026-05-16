# systems/player-progression/

Player character leveling, experience gain, and stat progression.

## What this system covers

- Player level (on APalPlayerState)
- Experience points
- Stat upgrade points
- Technology points

## Known data

- Player level is on APalPlayerState (confirmed via NightFyre SDK)
- REST API `/v1/api/players` returns level per player
- Save file contains level and XP

## Open questions

- Exact field name for XP on APalPlayerState (UHT dump needed)
- Level-up hook path (not yet found — open TODO)
- Stat point allocation system class name
- How to trigger a level-up or grant XP at runtime

## Access surfaces

- UE4SS: APalPlayerState (reflected, field names unconfirmed)
- REST API: level readable (read-only)
- Save file: level + XP (offline)

## Status: KNOWN (save/REST) / PARTIAL (live write path)
