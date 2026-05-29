from __future__ import annotations

import pathlib
import sys


def _repo_root() -> pathlib.Path:
    # .github/scripts/repo_check.py -> repo root
    return pathlib.Path(__file__).resolve().parents[2]


def _fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def _load_yaml_all(repo_root: pathlib.Path) -> None:
    try:
        import yaml  # type: ignore
    except Exception as exc:
        _fail(
            "PyYAML is required for YAML validation. "
            "Install it with: python -m pip install pyyaml. "
            f"(import error: {exc})"
        )

    yaml_paths = sorted(
        [p for p in repo_root.rglob("*") if p.is_file() and p.suffix.lower() in {".yml", ".yaml"}]
    )

    errors: list[str] = []
    for path in yaml_paths:
        if ".git" in path.parts:
            continue
        try:
            yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception as exc:
            rel = path.relative_to(repo_root)
            errors.append(f"- {rel}: {exc}")

    if errors:
        _fail("One or more YAML files could not be parsed:\n" + "\n".join(errors))

    print(f"YAML validation OK ({len(yaml_paths)} files).")


def _check_future_api_empty(repo_root: pathlib.Path) -> None:
    future_api = repo_root / "future-api"
    if not future_api.exists():
        _fail("Expected folder future-api/ to exist.")

    allowed_files = {"README.md"}
    unexpected: list[str] = []

    for path in future_api.rglob("*"):
        if path.is_dir():
            continue
        rel = path.relative_to(repo_root).as_posix()
        if rel == "future-api/README.md":
            continue
        if path.name in allowed_files and path.parent == future_api:
            continue
        unexpected.append(rel)

    if unexpected:
        _fail(
            "future-api/ must stay empty (API design phase has not started). "
            "Unexpected files found:\n" + "\n".join(f"- {p}" for p in sorted(unexpected))
        )

    print("future-api/ empty check OK (README.md only).")


def main() -> None:
    repo_root = _repo_root()
    print(f"Repo root: {repo_root}")

    _load_yaml_all(repo_root)
    _check_future_api_empty(repo_root)

    print("Repository checks OK.")


if __name__ == "__main__":
    main()

