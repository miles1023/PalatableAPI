# surfaces/ue4ss/

UE4SS — Unreal Engine Scripting System.

## What this surface exposes

- Read/write any reflected UE property by class name + property name (no offsets needed)
- RegisterHook: pre/post hook any reflected UFunction
- NotifyOnNewObject: callback when any new class instance is created
- FindAllOf: enumerate all live instances of a class
- StaticFindObject: get a Class Default Object (CDO)
- Call UFunctions directly from Lua
- Access TArray, TMap, FString, FName, FVector, nested UObjects
- Generate UHT headers from live game (all reflected classes + properties)

## How to install

Drop compiled UE4SS DLL + config next to `Palworld-Win64-Shipping.exe`.
Lua mods go in `Mods/YourMod/Scripts/main.lua`.

## Version notes

- Requires Okaetsu fork of UE4SS for Palworld UE 5.1 compatibility
- Okaetsu fork updated 2026-01-17 for game version 0.7.1
- Confirm the correct fork version before each RE session

## What it does NOT expose

- Non-reflected (private C++) fields — use memory-raw/ surface for those
- Server-internal state if running on a client instance

## Key utility objects for Palworld

- `/Script/Pal.Default__PalUtility` — GetPlayerCharacter, GetOtomoHolderComponent, GetPlayerState, GetItemIDManager
- `/Script/Pal.Default__PalMasterDataTablesUtility` — DataTable lookup functions at runtime

## Session notes and findings

Drop surface-specific notes here. For findings from UE4SS sessions, add them to the appropriate `systems/` folder.
