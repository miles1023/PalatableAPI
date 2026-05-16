# intake/raw/

Unprocessed tool output, exactly as the tool produced it.

## Rules

- Never edit files here. The value of raw/ is that it is untouched source material.
- One file per tool session per topic. Do not combine multiple topics in one file.
- If the tool output is very large (UHT dump, full memory dump), it is fine to have large files here.

## Processing

When you are ready to process a file, move it to `intake/processed/` and parse it there into `findings/`. Do not process in-place.
