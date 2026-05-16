# surfaces/dll-injection/

Custom DLL injection — UE4SS C++ mods or external injection.

## What this surface exposes

- Everything memory-raw/ exposes, but persistent and programmable
- Detour-hook any game function (not just reflected) via byte patching
- Intercept Windows API calls (DirectX, networking, file I/O)
- Add in-process background threads
- Full vtable access for virtual function hooking

## Two injection paths

1. **UE4SS C++ mods** — compile to DLL, drop in `Mods/YourMod/dlls/`. UE4SS loads it at startup. Recommended: cleaner, has UE4SS API available.
2. **External injector** — inject via separate injector tool at runtime. More flexible but more complex.

## Hook libraries

- MinHook — lightweight function detour library
- Microsoft Detours — more comprehensive

## Version notes

Function addresses change on game updates. Always target hooks via AOB signature, not hardcoded address.

## Status

UE4SS C++ mod path: KNOWN (documented, used by community mods)
External injection path: INFERRED (not widely documented specifically for Palworld)
