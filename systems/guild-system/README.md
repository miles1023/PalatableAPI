# systems/guild-system/

Player organizations. Guilds share a base, storage, and Pal assignments.

## What this system covers

- Guild creation and membership
- Guild ID and name
- Member list (player UIDs)
- Guild base assignment
- Shared item storage (via base chest)

## Known data

- Save file (Level.sav) contains guild data
- REST API `/v1/api/guilds` lists guilds
- UE4SS: PalBaseCampModel (NotifyOnNewObject hook exists — base camp ties to guild)

## Open questions

- UE class name for the guild manager or guild state object
- Live UE4SS access path to guild member list
- How guild base ownership is tracked vs. individual base ownership
- Are there hooks for guild join/leave events?

## Access surfaces

- Save file: Level.sav (offline)
- REST API: /v1/api/guilds (limited, server-only)
- UE4SS: partial (PalBaseCampModel hook exists)

## Status: PARTIAL
