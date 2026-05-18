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
3. Prefer a live UE4SS DumpUSMAP output for the current game build when available
4. If no live dump exists yet, download a current community Mappings.usmap from: github.com/PalworldModding/UsefulFiles
5. Load the verified mapping file in FModel settings

## Version dependency

Mappings.usmap must match the current game version. When the game updates, wait for the community to update Mappings.usmap before running FModel.

For the current local 0.7.3 research setup, UE4SS generated
`Pal-5.1.1-0+++UE5+Release-5.1-486806a.usmap` with SHA256
`8F85BD27CDF9CEA8525EF01F0E0B567E958DAF576F26263185F5444D459A2AE7`.
The older local FModel copy at `D:\Tools\FModel\Mappings.usmap` hashed differently and should be treated as stale until replaced.

## What it does NOT do

FModel is read-only. To create modifications, use PAK mods or PalSchema.

## Top priority use for this project

Export DT_WazaDataTable — column names are currently unconfirmed.
This is the highest-priority FModel task. See `systems/combat-waza/README.md`.

## Where to put FModel output

Drop exported JSON/CSV files into `intake/raw/YYYY-MM-DD-fmodel-<tablename>/`

## Status: KNOWN
