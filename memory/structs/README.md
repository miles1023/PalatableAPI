# memory/structs/

Struct and class memory layouts.

Each file documents how a specific struct or class is laid out in memory: which fields are at which offsets, their sizes, and their types.

## File format

```markdown
# StructName — Memory Layout
Game version: 0.x.x
Verified via: CheatEngine struct dissect / x64dbg + Ghidra
Session: YYYY-MM-DD

| Offset | Size | Type | Field | Notes |
|--------|------|------|-------|-------|
| 0x000  | 4    | float| FieldA | ... |
...
```

## Priority targets

1. FFixedPoint — inner field layout (float at 0x0 or 0x4?)
2. UPalIndividualCharacterParameter — full field list
3. UPalCharacterParameterComponent — full field list
