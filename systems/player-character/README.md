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

- HP (FFixedPoint — inner field unconfirmed: .Value or .RawValue?)
- Hunger / FullStomach (float)
- Sanity / SanityValue (float, range 0.0–100.0)
- Invincibility / bIsEnableMuteki (bool)
- MaxWalkSpeed (float, default 600.0)
- MaxInventoryWeight (float, on UPalPlayerInventoryData)

## Access chains confirmed

- HP: APalPlayerCharacter → CharacterParameterComponent → IndividualParameter → Hp
- FullStomach: same chain → FullStomach
- bIsEnableMuteki: APalPlayerCharacter → CharacterParameterComponent → bIsEnableMuteki
- MaxWalkSpeed: APalPlayerCharacter → CharacterMovement → MaxWalkSpeed
- MaxInventoryWeight: APalPlayerCharacter → Controller → PlayerState → InventoryData → MaxInventoryWeight

## Open questions

- FFixedPoint inner field: .Value or .RawValue? (highest priority — blocks all stat modification)
- Server hook path for player death event (not yet found)
- Player level-up hook path (not yet found)
- Full list of properties on APalPlayerState

## Pre-migration data

See `findings/pre-migration/entities/APalPlayerCharacter.yml`, `APalPlayerController.yml`,
`APalPlayerState.yml`, `UPalCharacterParameterComponent.yml`,
`UPalIndividualCharacterParameter.yml`, `UPalCharacterMovementComponent.yml`
