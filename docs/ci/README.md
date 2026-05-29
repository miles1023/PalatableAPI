# CI runners and workflows

This project is mainly a structured research notebook (it is not a compiled app yet), so the goal
of CI is to catch “oops” mistakes early (broken YAML, accidental files in `future-api/`, etc.).

## Recommended runners

- **Default runner:** `ubuntu-latest`
  - Fast and cheap for simple validation checks.
  - Matches the most common GitHub Actions setup, so it is easy for contributors to understand.
- **Secondary runner:** `windows-latest`
  - This project is Windows-heavy in the real world (Palworld is Windows-first and many RE tools are
    Windows-only), so we also run the same checks on Windows to avoid accidental Linux-only assumptions.
- **Not used right now:** `macos-latest`
  - There is nothing Mac-specific to validate today, so we avoid the extra time/cost for now.

## Workflows

- `CI` (`.github/workflows/ci.yml`)
  - Runs on every pull request and push.
  - Checks that all YAML files are readable and that `future-api/` stays empty (except its README).
- `Snapshot Artifact` (`.github/workflows/snapshot.yml`)
  - Manual run (“Run workflow” button).
  - Produces a downloadable snapshot archive as a build artifact.
  - This is the closest thing to “deployment” right now, because there is no app to deploy yet.

## Security notes (plain language)

- The workflows only need read-only access to the repository.
- They do not use secrets.
- They only run a small local checker script that lives in this repository.

