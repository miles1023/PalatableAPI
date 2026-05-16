# surfaces/

One subfolder per modding surface identified in `survey/SURFACES.md`.

## Current surface folders

| Folder | Surface |
|--------|---------|
| ue4ss/ | UE4SS — Unreal Engine Scripting System (Lua/C++ in-process) |
| pak-mods/ | PAK asset replacement system |
| palschema/ | PalSchema DataTable JSON patching |
| memory-raw/ | Raw memory access via CheatEngine |
| dll-injection/ | Custom DLL injection (UE4SS C++ or external) |
| rcon/ | RCON server interface |
| rest-api/ | REST API server interface |
| save-files/ | Save file parsing (offline) |
| config-ini/ | PalWorldSettings.ini and other config files |
| uht-dump/ | UHT dump generator via UE4SS |
| fmodel/ | FModel + Mappings.usmap asset reader |
| ghidra/ | Ghidra static binary analysis |
| x64dbg/ | x64dbg live debugger |
| steam-workshop/ | Steam Workshop (upcoming — details unknown) |

## What goes in each subfolder

- A README.md explaining the surface (already written)
- Tool-specific session notes
- Tool output summaries
- Known limitations, gotchas, version dependencies

## Rules

- Surface folders document HOW to access the game through that surface
- Findings discovered via a surface go in `findings/` and `systems/`, not here
- If a new surface is found, add it to `survey/SURFACES.md` first, then create the folder
