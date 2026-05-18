---
type: struct
name: FFixedPoint
description: Live UE4SS CXX headers show that FFixedPoint has a single inner field named Value at offset 0x0; there is no RawValue member in the dumped layout.
game_system: player-character
surface: ue4ss
source:
  tool: UE4SS
  session: 2026-05-18
  detail: C:\Program Files (x86)\Steam\steamapps\common\Palworld\Pal\Binaries\Win64\ue4ss\CXXHeaderDump\Pal.hpp:114-118
confidence: confirmed
status: complete
game_version: "0.7.3"
technical:
  total_size: 4
  fields:
    - offset: "0x0000"
      size: 4
      type: int32
      name: Value
---

## Description

The active 0.7.3 UE4SS CXX dump defines `FFixedPoint` as a 4-byte struct with one member: `Value`.
This resolves the `.Value` vs `.RawValue` question for the 32-bit fixed-point struct name itself.

## Technical Details

- Struct declaration in `Pal.hpp`:

```cpp
struct FFixedPoint
{
    int32 Value;                                                                      // 0x0000 (size: 0x4)

}; // Size: 0x4
```

- No `RawValue` member appears in the live dumped declaration.

## Relationships

- `FFixedPoint64` — same family