# Live FixedPoint64 HP probe - 2026-05-18

## Source

- Raw capture: `intake/raw/2026-05-18-fixedpoint-probe-hp-scale.txt`
- Tool: UE4SS Lua probe in the live 0.7.3 player session
- Trigger: `F6`

## Repeated observations

- `hp_raw=900000`
- `max_hp_display=900` from `UPalIndividualCharacterParameter::GetMaxHP()`
- `hp_rate=0.99900007247925` from `UPalCharacterParameterComponent::GetHPRate()`
- `PalDatabaseCharacterParameter::GetHP(individual)` returned `-1` for the live player object in both reads
- The same values repeated twice in the same loaded game session

## Interpretation

- `900000 / 1000 = 900` exactly, which matches the live `GetMaxHP()` result
- This is strong live evidence that player HP-family `FFixedPoint64.Value` uses `1000` raw units per `1` whole-number HP unit
- The attempted database helper is not a valid proof source for current displayed player HP in this context because it returned `-1`

## Remaining caution

- The live session cleanly confirms the `1000:1` mapping against `GetMaxHP()`
- A clean plain-number getter for current player HP is still desirable if we want the current-HP side confirmed without inference from the same session