# surfaces/pak-mods/

Unreal Engine PAK mod system — asset replacement via .pak files.

## What this surface exposes

- DataTable replacement (replaces entire DataTable asset)
- Blueprint replacement
- New content injection (items, Pals, buildings)
- Texture, model, audio replacement

## How to use

1. Extract target asset with FModel + Mappings.usmap
2. Modify or create replacement asset
3. Package as .pak file with UnrealPak or repak
4. Drop .pak in `Palworld/Content/Paks/`

## Version notes

- Pak install location changed in 0.7.0, reverted in 0.7.1 (back to `/Pal/Content/Paks/`)
- Must re-test pak install location after each major update
- Mappings.usmap must match the current game version

## Conflict behavior

If two mods provide the same asset, one wins and the other is silently ignored. Use PalSchema to avoid this for DataTable patches.

## What it does NOT expose

- Runtime game state (inventory, live stats, etc.)
- Event hooks
- Anything that isn't a static asset loaded at startup
