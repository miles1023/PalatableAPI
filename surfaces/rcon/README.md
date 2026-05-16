# surfaces/rcon/

RCON server interface for Palworld dedicated servers.

## How to enable

In `PalWorldSettings.ini`:
```
RCONEnabled=true
RCONPort=25575
AdminPassword=YourPassword
```

## Protocol

Palworld uses a Minecraft-compatible RCON format over TCP.

## Confirmed commands

| Command | Description |
|---------|-------------|
| Info | Server name and version |
| ShowPlayers | List connected players with UID and Steam ID |
| KickPlayer <uid> | Kick a player |
| BanPlayer <uid> | Ban a player |
| TeleportToPlayer <uid> | Admin teleports to a player |
| TeleportToMe <uid> | Teleports a player to admin |
| Broadcast <message> | Server-wide chat message |
| DoExit | Stop server immediately |
| Shutdown [seconds] [message] | Graceful shutdown with delay |
| Save | Force world save |

## Limitations

- Server management only — cannot modify player stats, inventory, or Pal data
- No query commands (cannot read game state, only act)
- Requires dedicated server with RCON enabled

## Status: KNOWN — documented by Pocketpair
