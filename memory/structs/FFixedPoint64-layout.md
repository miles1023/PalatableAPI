---
type: struct
name: FFixedPoint64
description: Live UE4SS CXX headers show that FFixedPoint64 has a single inner field named Value at offset 0x0, and UPalIndividualCharacterParameter uses FFixedPoint64 for Hp, MaxHP, MP, MaxMP, ShieldHP, ShieldMaxHP, and MaxSP.
game_system: player-character
surface: ue4ss
source:
  tool: UE4SS
  session: 2026-05-18
  detail: C:\Program Files (x86)\Steam\steamapps\common\Palworld\Pal\Binaries\Win64\ue4ss\CXXHeaderDump\Pal.hpp:120-124 and 3477-3502
confidence: confirmed
status: complete
game_version: "0.7.3"
technical:
  total_size: 8
  fields:
    - offset: "0x0000"
      size: 8
      type: int64
      name: Value
---

## Description

The active 0.7.3 UE4SS CXX dump defines `FFixedPoint64` as an 8-byte struct with one member: `Value`.
In the same live dump, `UPalIndividualCharacterParameter` uses `FFixedPoint64` for `Hp`, `MP`, `MaxHP`, `ShieldHP`, `ShieldMaxHP`, `MaxMP`, and `MaxSP`.

Live probe evidence captured on 2026-05-18 also strongly supports a runtime scale of `1000` raw units per `1` whole-number HP unit for player HP-family values: in the same live player session, the probe repeatedly read `hp_raw=900000` while `UPalIndividualCharacterParameter::GetMaxHP()` returned `900`.

## Technical Details

- Struct declaration in `Pal.hpp`:

```cpp
struct FFixedPoint64
{
    int64 Value;                                                                      // 0x0000 (size: 0x8)

}; // Size: 0x8
```

- Relevant `UPalIndividualCharacterParameter` fields in the same dump:

```cpp
FFixedPoint64 Hp;                                                                     // 0x0078 (size: 0x8)
FFixedPoint64 MP;                                                                     // 0x00A8 (size: 0x8)
FFixedPoint64 MaxHP;                                                                  // 0x00E0 (size: 0x8)
FFixedPoint64 ShieldHP;                                                               // 0x0100 (size: 0x8)
FFixedPoint64 ShieldMaxHP;                                                            // 0x0108 (size: 0x8)
FFixedPoint64 MaxMP;                                                                  // 0x0118 (size: 0x8)
FFixedPoint64 MaxSP;                                                                  // 0x0120 (size: 0x8)
```

- No `RawValue` member appears in the live dumped declaration.

## Runtime Scaling Evidence

- Raw capture: `intake/raw/2026-05-18-fixedpoint-probe-hp-scale.txt`
- Processed note: `intake/processed/2026-05-18-fixedpoint-probe-hp-scale.md`
- Repeated live player probe result:

```text
hp_raw=900000
max_hp_display=900
hp_rate=0.99900007247925
```

- `900000 / 1000 = 900` exactly, matching the live `GetMaxHP()` result.
- In the same probe, `PalDatabaseCharacterParameter::GetHP(individual)` returned `-1`, so that helper should not be treated as a valid current-player display getter in this context.

## Relationships

- `FFixedPoint` — same family
- `UPalIndividualCharacterParameter` — part of