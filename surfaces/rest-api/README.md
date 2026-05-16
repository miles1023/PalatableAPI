# surfaces/rest-api/

REST API for Palworld dedicated servers.

## How to enable

In `PalWorldSettings.ini`:
```
RESTAPIEnabled=true
RESTAPIPort=8212
```

## Authentication

HTTP Basic Auth: `admin:<AdminPassword>`

## Base URL

`http://<server-ip>:8212/v1/api/`

## Confirmed endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /info | Server name, version, player count |
| GET | /players | All players: UID, name, coordinates, level, ping |
| POST | /kick | Kick player by UID |
| POST | /ban | Ban player by UID |
| POST | /unban | Unban player |
| POST | /teleport | Teleport player to coordinates |
| POST | /item | Spawn item for player (item ID + count) |
| POST | /broadcast | Broadcast message |
| POST | /shutdown | Graceful shutdown with delay |
| GET | /metrics | Server FPS, player count, memory usage |
| POST | /save | Force world save |
| GET | /guilds | List guilds (added in later update) |

## Limitations

- Server-side only — requires a running dedicated server
- Cannot modify Pal data, player stats, or world state beyond what the endpoints expose
- Item spawn (`/item`) is the most useful endpoint for mods — requires knowing item IDs

## Status: KNOWN — documented by Pocketpair
