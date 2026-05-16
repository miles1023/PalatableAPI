# survey/

Contains the Phase 0 ecosystem survey outputs.

## Files here

- **SURFACES.md** — Every external access point into Palworld the modding community has found. One entry per surface. Each entry covers what it exposes, how it is accessed, and confidence level.
- **GAME_SYSTEMS.md** — Every internal game system identified through community research. One entry per system.

## Purpose

These two files are the seed documents for the entire reverse engineering project. They define the complete scope of what needs to be mapped. Every folder in `systems/` and `surfaces/` traces back to an entry here.

## Rules

- Do not edit these files lightly. A change here changes the scope of the entire project.
- If a new surface or system is discovered during RE work, add it here first, then create the corresponding folder.
- Do not add tool output or findings here. This folder is survey-only.
