# surfaces/config-ini/

PalWorldSettings.ini and standard UE config files.

## File location

**Server:** `PalServer/Pal/Saved/Config/WindowsServer/PalWorldSettings.ini`
**Client:** `%LOCALAPPDATA%\Pal\Saved\Config\WindowsNoEditor\PalWorldSettings.ini`

## What it exposes

- Gameplay rate multipliers (XP rate, drop rate, damage rate, etc.)
- Player and Pal inventory slot counts
- Server tick rate and player count limits
- PvP enable/disable
- Building damage and decay settings
- Day/night cycle speed (DayTimeSpeedRate, NightTimeSpeedRate)
- Guild base limits
- RCON and REST API enable/config
- Admin password

## How to use

Edit the .ini file directly in a text editor before launching the game or server. Changes take effect on next start.

## Limitations

- Static — changes require restart
- Limited to options Pocketpair exposes as settings
- Does not modify individual player or Pal state

## Status: KNOWN — documented by Pocketpair
