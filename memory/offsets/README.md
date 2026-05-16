# memory/offsets/

Confirmed offset records. One file per confirmed finding.

## File format

Each file is a single offset finding in the canonical schema from `schemas/FINDING_SCHEMA.md`.

## Naming

`YYYY-MM-DD-ClassName-fieldname.md`

## What makes an offset "confirmed"

- Address was verified by reading a known value and seeing the correct result
- AOB signature is recorded
- Game version is recorded
- Authority (client or server) is recorded
- Broken_since field is null (still working)

## Unconfirmed offsets

If you found an address but have not verified it yet, put the file in `unknowns/` instead.
