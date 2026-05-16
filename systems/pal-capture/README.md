# systems/pal-capture/

The system for throwing Pal Spheres and capturing wild Pals.

## What this system covers

- Sphere throw mechanics
- Capture rate calculation
- Capture success/failure resolution
- Newly captured Pal initialization

## Known data

- Base capture rate per species: DT_PalMonsterParameter.CaptureRateCorrect (float)
- Sphere tier multiplier: unknown (not yet mapped to DataTable column)
- Pal HP at throw time affects success rate: mechanism unknown

## Open questions

- Sphere type multiplier — is it in DT_PalMonsterParameter, a separate table, or hardcoded?
- Hook path for capture event (not yet found — open TODO)
- Class name for the capture calculation function
- How newly captured Pals are initialized (stats, skills)

## Access surfaces

- DT_PalMonsterParameter: CaptureRateCorrect column (static base rate)
- UE4SS: no confirmed hook path yet

## Status: PARTIAL
