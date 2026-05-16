# systems/time-weather/

In-game day/night cycle and weather state.

## What this system covers

- Current time of day
- Day/night cycle speed
- Weather state and transitions

## Known data

- Day/night cycle speed is a config file setting (DayTimeSpeedRate, NightTimeSpeedRate in PalWorldSettings.ini)

## Open questions

- UE class name for the time/weather manager
- How to read current in-game time at runtime via UE4SS
- How to modify time of day live (not just speed via config)
- Weather state class and properties
- Are there hooks for time-of-day transition events?

## Access surfaces

- Config file: DayTimeSpeedRate, NightTimeSpeedRate (static, requires restart)
- UE4SS: class name unknown, no confirmed access path

## Status: INFERRED — exists but no confirmed live access path
