# systems/player-character/

The live player actor in the running game.

## What this system covers

- APalPlayerCharacter — the player pawn (position, model, combat)
- APalPlayerController — processes input, manages possession
- APalPlayerState — persisted server-side player data
- UPalCharacterParameterComponent — current runtime stats
- UPalIndividualCharacterParameter — permanent character parameters
- UPalCharacterMovementComponent — movement: walk, run, swim, fly

## Key fields known (from pre-migration data)

- HP / MaxHP / MP / MaxMP / ShieldHP use FFixedPoint64 with a single inner field named .Value (int64 in the live 0.7.3 UE4SS CXX dump)
- Live 2026-05-18 player probe evidence strongly supports `1000` raw fixed-point units per `1` whole-number HP unit (`hp_raw=900000` while `GetMaxHP()` returned `900` in the same session)
- Hunger / FullStomach (float)
- Sanity / SanityValue (float, range 0.0–100.0)
- Invincibility / bIsEnableMuteki (bool)
- MaxWalkSpeed (float, default 600.0)
- MaxInventoryWeight (float, on UPalPlayerInventoryData)

## Access chains confirmed

- HP: APalPlayerCharacter → CharacterParameterComponent → IndividualParameter → Hp
- Player MaxHP (whole-number getter): APalPlayerCharacter → CharacterParameterComponent → IndividualParameter → GetMaxHP()
- Player HPRate: APalPlayerCharacter → CharacterParameterComponent → GetHPRate()
- FullStomach: same chain → FullStomach
- bIsEnableMuteki: APalPlayerCharacter → CharacterParameterComponent → bIsEnableMuteki
- MaxWalkSpeed: APalPlayerCharacter → CharacterMovement → MaxWalkSpeed
- MaxInventoryWeight: APalPlayerCharacter → Controller → PlayerState → InventoryData → MaxInventoryWeight

## Open questions

- Live evidence now strongly supports `1000` raw units = `1` whole-number HP unit for player HP-family values, but a clean plain-number current-HP getter is still desirable because `PalDatabaseCharacterParameter::GetHP(individual)` returned `-1` for the live player object
- Server hook path for player death event (not yet found)
- Player level-up hook path (not yet found)
- Full list of properties on APalPlayerState

## Pre-migration data

See `findings/pre-migration/entities/APalPlayerCharacter.yml`, `APalPlayerController.yml`,
`APalPlayerState.yml`, `UPalCharacterParameterComponent.yml`,
`UPalIndividualCharacterParameter.yml`, `UPalCharacterMovementComponent.yml`

Resolved pointer for the old highest-priority stat question:
- See `memory/structs/FFixedPoint-layout.md`
- See `memory/structs/FFixedPoint64-layout.md`
