# systems/ai-behavior/

Wild Pal and NPC AI behavior.

## What this system covers

- Wild Pal AI: patrol, aggro, escape, attack, special behaviors
- NPC enemy AI (human faction enemies)
- Boss AI

## Known data

- AIResponse enum (EPalAIResponseType): Ignore, Escape, Battle, Special
- DT_PalMonsterParameter.AIResponse — default AI response per species
- EPalOrganizationType — faction the Pal/NPC belongs to

## Open questions

- Behavior tree class names
- How to read current AI state at runtime (aggro target, current behavior)
- How to override AI behavior live
- Class name for the AI controller/component on APalCharacter
- Hooks for AI state transitions (e.g., Pal begins attacking)

## Access surfaces

- DT_PalMonsterParameter: default AIResponse per species (static, via FModel/PalSchema)
- UE4SS: no confirmed live AI access path yet

## Status: PARTIAL — static data known, live access unknown
