# sources-2026.md — Verified 2026 Research Sources
# All sources confirmed current as of 2026-05-16.
# This file is the primary reference for verifying and updating
# SURFACES.md and GAME_SYSTEMS.md entries tagged [UNVERIFIED].
#
# FORMAT: URL | What it covers | Key finding | Accessed
# ─────────────────────────────────────────────────────────────────

---

## IMPORTANT CORRECTIONS TO SURVEY DATA

The following entries in SURFACES.md were inaccurate due to training data cutoff.
These must be updated before Phase 0 is considered complete.

| Surface | Old Status | Confirmed Status | Source |
|---------|-----------|------------------|--------|
| Steam Workshop | INFERRED — upcoming | **CONFIRMED LIVE** (since 0.7.0) | steamcommunity.com/app/1623730/workshop/ |
| RCON | CONFIRMED — active | **DEPRECATED** — scheduled removal, use REST API | docs.palworldgame.com/api/rcon/ |

---

## SOURCE RECORDS

### 1. UE4SS — Okaetsu Experimental-Palworld Fork

| Field | Value |
|-------|-------|
| URL (GitHub) | https://github.com/Okaetsu/RE-UE4SS/releases/tag/experimental-palworld |
| URL (Nexus) | https://www.nexusmods.com/palworld/mods/2237 |
| URL (Steam Workshop) | https://steamcommunity.com/sharedfiles/filedetails/?id=3625223587 |
| Last updated | January 17, 2026 |
| Commit | 486806ab2bedf542d4df4640dd7854194886ada6 |
| Maintained by | Okaetsu |
| Covers | Palworld-specific UE4SS fork; DLL injection, Lua scripting, UE reflection |
| Key finding | Workshop version and Nexus version CANNOT both be installed — will crash. Disable one by renaming dwmapi.dll. |
| Accessed | 2026-05-16 |

---

### 2. UE4SS — Installation Guide (Nexus)

| Field | Value |
|-------|-------|
| URL | https://www.nexusmods.com/palworld/articles/69 |
| URL (alternate Nexus) | https://www.nexusmods.com/palworld/mods/3035 |
| Covers | Step-by-step UE4SS installation; dwmapi.dll placement |
| Accessed | 2026-05-16 |

---

### 3. UE4SS — Community Docs (pwmodding.wiki)

| Field | Value |
|-------|-------|
| URL | https://pwmodding.wiki/docs/category/ue4ss |
| Covers | UE4SS setup, scripting patterns, hook registration |
| Accessed | 2026-05-16 |

---

### 4. PalSchema — Official GitHub

| Field | Value |
|-------|-------|
| URL (releases) | https://github.com/Okaetsu/PalSchema/releases |
| URL (docs) | https://okaetsu.github.io/PalSchema/docs/installation |
| URL (Steam Workshop) | https://steamcommunity.com/sharedfiles/filedetails/?id=3625280368 |
| URL (Nexus) | https://www.nexusmods.com/palworld/mods/2361 |
| Last known version | 0.5.0 (January 24, 2026) |
| Maintained by | Okaetsu |
| Covers | DataTable JSON patch system; .schema.json format; static data modification |
| Key finding | Pak redirector STILL BROKEN as of 0.7.0. Workaround: place pak files directly in Palworld/Pal/Content/Paks/ instead of PalSchema's own paks folder. |
| Accessed | 2026-05-16 |

---

### 5. Steam Workshop — Live Palworld Page

| Field | Value |
|-------|-------|
| URL (browse) | https://steamcommunity.com/app/1623730/workshop/ |
| URL (about) | https://steamcommunity.com/workshop/about/?appid=1623730 |
| Status | **CONFIRMED LIVE** — went live with the Home Sweet Home update (0.7.0) |
| Covers | Official Steam mod distribution for Palworld |
| Key findings | (1) Workshop mod support is described as "highly experimental." (2) Workshop UE4SS does NOT work on Steam Deck / Proton / Wine — known bug, no fix date confirmed. (3) Workshop mods only work on private servers, NOT official Pocketpair servers. |
| Source for update news | https://www.mmorpg.com/news/palworld-adds-ultrakill-collab-steam-workshop-compatibility-experimental-pvp-and-more-in-new-update-2000136878 |
| Accessed | 2026-05-16 |

---

### 6. Steam Workshop — Mod Installation Guide (pwmodding.wiki)

| Field | Value |
|-------|-------|
| URL | https://pwmodding.wiki/docs/category/steam-workshop |
| URL (users install guide) | https://pwmodding.wiki/docs/users/workshop/installing-mods |
| URL (mod publishing) | https://pwmodding.wiki/docs/developers/mod-publishing/workshop/uploading |
| Covers | End-user mod installation; developer upload workflow for Steam Workshop |
| Accessed | 2026-05-16 |

---

### 7. Palworld Official Server REST API

| Field | Value |
|-------|-------|
| URL (REST API docs) | https://docs.palworldgame.com/api/rest-api/palwold-rest-api/ |
| URL (API category) | https://docs.palworldgame.com/category/api/ |
| URL (mod install on server) | https://docs.palworldgame.com/settings-and-operation/mod/ |
| Maintained by | Pocketpair (official) |
| Covers | Official server REST API; endpoint list; server-side configuration |
| Key finding | REST API requires `RESTAPIEnabled=True` in server config. Port default: 8212. **NOT designed for direct Internet exposure.** |
| Accessed | 2026-05-16 |

---

### 8. Palworld RCON — DEPRECATED

| Field | Value |
|-------|-------|
| URL | https://docs.palworldgame.com/api/rcon/ |
| Status | **DEPRECATED** — Pocketpair has announced RCON will stop functioning in an upcoming update |
| Covers | Legacy RCON command interface for server management |
| Key finding | RCON is being replaced entirely by the REST API. Do not build any new tooling against RCON. Mark all RCON surface entries with `deprecated: true`. |
| Accessed | 2026-05-16 |

---

### 9. pwmodding.wiki — Primary Community Modding Hub

| Field | Value |
|-------|-------|
| URL (main) | https://pwmodding.wiki/ |
| URL (FModel guide) | https://pwmodding.wiki/docs/developers/useful-tools/fmodel |
| URL (useful tools) | https://pwmodding.wiki/docs/category/useful-tools |
| URL (Palworld Modding Kit) | https://pwmodding.wiki/docs/category/palworld-modding-kit |
| URL (DataTable modding) | https://pwmodding.wiki/docs/developers/uassetgui-modding/datatable-modding/UAssetGuide1 |
| Covers | Comprehensive community documentation: FModel setup, UHT, PMK, asset swapping, workshop publishing |
| Key finding (Jan 7, 2026 update) | **VS 2026 (Visual Studio 2026) does NOT work with Unreal Engine 5.1.** Must use VS 2022. The wiki corrected a broken link pointing to VS 2026 and replaced it with a direct link to VS 2022 from Microsoft. |
| Accessed | 2026-05-16 |

---

### 10. PalworldModding/UsefulFiles — Mappings.usmap

| Field | Value |
|-------|-------|
| URL | https://github.com/PalworldModding/UsefulFiles/blob/master/Mappings.usmap |
| URL (org) | https://github.com/PalworldModding |
| Last updated | December 22, 2025 |
| Covers | Current Mappings.usmap for use with FModel; required to read DataTable column names |
| Key finding | Last update was December 22, 2025 — predates 0.7.1 (released 2025-12-19). Likely current for 0.7.1 but should be verified before FModel session. If game updates past 0.7.1, this file must be updated first. |
| Alternate source | https://github.com/elliotks/Palworld-FModel (AES keys + usmap) |
| Accessed | 2026-05-16 |

---

### 11. NightFyre/Palworld-Internal — C++ SDK / Struct Reference

| Field | Value |
|-------|-------|
| URL | https://github.com/NightFyre/Palworld-Internal |
| URL (releases) | https://github.com/NightFyre/Palworld-Internal/releases |
| Covers | C++ SDK class hierarchy, property names, struct layouts, offsets; internal cheat framework |
| Key finding | Contains "Palworld reversals, structs and offsets" including DX11 internal base, MinHook, Dumper7. **Used to bootstrap pre-migration entity YAMLs.** Has Steam, SteamDeck, and Xbox build variants. |
| Warning | This is an active cheat/trainer project. Struct data is useful for RE but addresses will be stale unless the repo is updated for the current game version. Verify all offsets via live tools before treating as confirmed. |
| Accessed | 2026-05-16 |

---

### 12. Palworld 1.0 — World Tree Update (2026)

| Field | Value |
|-------|-------|
| URL (Steam announcement) | https://store.steampowered.com/news/app/1623730/view/689735528964162147 |
| URL (overview article) | https://www.windowscentral.com/gaming/pocketpair-tease-1-0-update-palworld |
| URL (roadmap overview) | https://www.4netplayers.com/en-us/blog/palworld/palworld-2026-getting-started-update-0-7-release-1-0/ |
| Release date | **2026 — no specific date confirmed.** Pocketpair has explicitly declined to give a hard date. |
| Covers | Exit from early access; World Tree endgame content; second island expansion; Genetic Recombination system |
| Key findings for RE | (1) 1.0 will be labeled the "World Tree update." (2) Free update for all existing early access owners. (3) Pocketpair's approach has been to avoid large content updates in 2026 except for 1.0 itself — focus is on polish. (4) All hardcoded addresses expected to change at 1.0 — byte signatures and reflected property names are more likely to survive than raw offsets. |
| Accessed | 2026-05-16 |

---

### 13. Palworld Modding Kit (PMK) — Official UE5 Mod Development

| Field | Value |
|-------|-------|
| URL | https://pwmodding.wiki/docs/category/palworld-modding-kit |
| URL (prerequisites) | https://pwmodding.wiki/docs/developers/palworld-modding-kit/prerequisites |
| Covers | Official Pocketpair-provided UE5 project for creating .pak mods; asset creation workflow |
| Key finding | VS 2022 required (see source 9 above). PMK enables proper .pak mod creation via UE5 Editor. |
| Accessed | 2026-05-16 |

---

## WHAT STILL NEEDS VERIFICATION

The following SURFACES.md entries remain **[UNVERIFIED — training data]** because no
2026-current source was found that directly confirms or denies them:

| Surface | What needs confirmation |
|---------|------------------------|
| Raw Memory (CheatEngine) | Confirm CE still works with current EAC/anticheat configuration in 0.7.1 |
| DLL Injection | Confirm injection vectors still work in 0.7.1; any new protection added? |
| Save Files | Confirm save file format has not changed in 0.7.1 |
| Config/INI | Confirm PalWorldSettings.ini structure and all field names for 0.7.1 |
| UHT Dump (UE4SS) | Confirm GenerateUHTCompatibleHeaders() still works in current UE4SS build |
| Ghidra | Tooling is game-agnostic; no verification needed for the tool itself |
| x64dbg | Tooling is game-agnostic; no verification needed for the tool itself |

The following GAME_SYSTEMS.md entries remain **[UNVERIFIED — training data]**:
All 21 entries — game system names and structures cannot be fully verified from
external sources alone; UHT dump and FModel export are required for direct confirmation.

---

## HOW TO USE THIS FILE

1. When updating SURFACES.md: use Column 3 ("Confirmed Status") from the corrections
   table at the top of this file to update the affected entries.
2. When setting up FModel: use Source 10 (Mappings.usmap) and Source 9 (FModel guide).
3. When setting up UE4SS: use Sources 1–3. If game has updated past 0.7.1, check Source 1
   first to see if a new experimental-palworld release exists.
4. When referencing struct/property data from NightFyre: always cross-verify against
   live tool output before marking confidence as anything other than `inferred`.
5. Before any RE session: check if Palworld 1.0 has shipped (Source 12). If yes,
   all offset-based findings need re-validation before use.
