# findings/pre-migration/

Data from the project's previous structure. Preserved before the project was restructured around the canonical schema.

## Contents

- **entities/** — YAML files describing UE classes (APalPlayerCharacter, APalCharacter, etc.). Source: NightFyre/Palworld-Internal SDK, UHT dumps. Game version: 0.7.1.
- **datatables/** — YAML files describing DataTable schemas (DT_PalMonsterParameter, DA_StaticItemDataAsset, etc.). Source: PalSchema, FModel exports. Game version: 0.7.1.
- **hooks.yml** — Confirmed UE4SS RegisterHook and NotifyOnNewObject paths.
- **enums.yml** — Enum values: EPalElementType, EPalWorkSuitability, EPalTribeID (partial), etc.
- **access-chains.md** — Confirmed component access chains extracted from the previous session's command mapping work.

## Status

These files contain real, useful data but do not conform to the canonical schema in `schemas/FINDING_SCHEMA.md`. A future RE session should process these through the ingestion pipeline (see `workflow/PIPELINE.md`) to normalize them.

Until that is done, treat these as reference material — look here when you need a starting point for a system, but do not treat them as complete or verified.

## Do not edit

Do not add new data here. All new findings go through the pipeline and land in `findings/` or the appropriate `systems/` subfolder.
