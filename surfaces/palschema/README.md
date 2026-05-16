# surfaces/palschema/

PalSchema — DataTable JSON patch system by Okaetsu.

## What this surface exposes

- Row-level add, modify, or delete for any DataTable
- Multiple mods can patch the same DataTable without conflict
- More surgical than full PAK replacement

## How it works

1. Install PalSchema pak + DLL into the game
2. Create `.schema.json` files with patches
3. PalSchema applies patches at game startup

## Version notes

- PalSchema pak redirector broke on game version 0.7.0
- Workaround as of 0.7.1: manual pak placement (skip pak redirector)
- GitHub: github.com/Okaetsu/PalSchema
- One-developer project; maintenance not guaranteed

## .schema.json format

Each file targets one DataTable. Rows can be: added (new row key), modified (existing row key), or omitted (unchanged). Only changed columns need to be specified.

## What it does NOT expose

- Runtime state
- Events
- Any dynamic data

## Limitations vs. PAK mods

Cannot replace non-DataTable assets (blueprints, textures, etc.).
