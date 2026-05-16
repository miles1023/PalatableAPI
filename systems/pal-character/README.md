# systems/pal-character/

An individual Pal in the running game — following the player, in combat, or working at a base.

## What this system covers

- APalCharacter — the Pal actor (position, model, combat state)
- UPalCharacterParameterComponent — shared with player, holds runtime stats
- UPalIndividualCharacterParameter — Pal-specific permanent data
- AI / behavior component (class name unconfirmed)

## Key fields known

- HP (FFixedPoint — same unconfirmed inner field issue as player)
- FullStomach (hunger)
- SanityValue (float, 0.0–100.0)
- Level / experience
- Passive skills (list of EPalPassiveSkillList values)
- Active skills / Waza list
- Partner skill
- Species (EPalTribeID)
- Gender (EPalGenderType)
- Nickname (FString, nullable)
- Rank (condensed star rating)
- Pal UUID (unique instance identifier)

## Access chains confirmed

- HP: APalCharacter → CharacterParameterComponent → IndividualParameter → Hp
- FullStomach: same chain → FullStomach
- SanityValue: same chain → SanityValue

## Open questions

- AI component class name
- Behavior tree access path
- Hook path for Pal capture event
- Hook path for Pal death event
- Hook path for Pal level-up event
- How to enumerate all Pals belonging to a player (active party + PalBox)

## Pre-migration data

See `findings/pre-migration/entities/APalCharacter.yml`,
`UPalIndividualCharacterParameter.yml`
