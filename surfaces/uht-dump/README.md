# surfaces/uht-dump/

UHT (Unreal Header Tool) dump generator via UE4SS.

## What it produces

C++ header files (.hpp) listing every reflected class in the game:
- All UPROPERTY-marked fields: name, type, offset
- All UFUNCTION-marked methods: signature, parameters, return type
- All UEnum values
- Complete class inheritance hierarchy

## How to generate

1. Launch Palworld
2. Load UE4SS
3. Run `GenerateUHTCompatibleHeaders()` in the UE4SS console
4. Output appears in `CXXHeaders/` folder next to the game executable

## Why this is critical for RE work

This dump is the definitive list of what UE4SS reflection can access. Cross-reference it with:
- CheatEngine struct dissection (shows which fields ARE in reflection vs. which need raw access)
- Ghidra binary analysis (confirms field names and types at the binary level)

## Version dependency

The dump changes with the game version. Always note which game version produced a dump. Do not mix findings from dumps of different versions.

## Where to put dump output

Drop .hpp files into `intake/raw/YYYY-MM-DD-uht-dump/`

## Status: KNOWN — standard UE4SS feature
