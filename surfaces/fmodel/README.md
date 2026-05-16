# surfaces/fmodel/

FModel + Mappings.usmap — Unreal Engine asset browser (read-only research tool).

## What it exposes

- Complete DataTable contents: all rows and all columns
- Blueprint class structure
- All enum values and their names
- Asset paths and UObject hierarchy

## Setup

1. Download FModel
2. Point it at Palworld game directory
3. Download current Mappings.usmap from: github.com/PalworldModding/UsefulFiles
4. Load Mappings.usmap in FModel settings

## Version dependency

Mappings.usmap must match the current game version. When the game updates, wait for the community to update Mappings.usmap before running FModel.

## What it does NOT do

FModel is read-only. To create modifications, use PAK mods or PalSchema.

## Top priority use for this project

Export DT_WazaDataTable — column names are currently unconfirmed.
This is the highest-priority FModel task. See `systems/combat-waza/README.md`.

## Where to put FModel output

Drop exported JSON/CSV files into `intake/raw/YYYY-MM-DD-fmodel-<tablename>/`

## Status: KNOWN
