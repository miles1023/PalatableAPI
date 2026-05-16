# systems/server-session/

Dedicated server session management.

## What this system covers

- Connected player list
- Player UIDs / Steam IDs
- Server authority and replication state
- Join / disconnect events

## Known data

- ServerAcknowledgePossession hook: `/Script/Engine.PlayerController:ServerAcknowledgePossession` — fires server-side when a player is possessed. Use for server-side init.
- ClientRestart hook: `/Script/Engine.PlayerController:ClientRestart` — fires client-side on possession.
- REST API: `/v1/api/players` returns player list with UID, name, coords, level, ping
- RCON: ShowPlayers, KickPlayer, BanPlayer

## Open questions

- Player disconnect event hook path
- How to enumerate all connected players via UE4SS (not REST API)
- GameState class name for the Palworld-specific game state

## Access surfaces

- UE4SS: hooks confirmed (ServerAcknowledgePossession, ClientRestart)
- REST API: full player list with coordinates
- RCON: limited (kick, ban, list)

## Status: KNOWN (interfaces) / PARTIAL (internal access)
