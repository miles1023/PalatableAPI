# CI/CD Infrastructure Documentation

## Overview

This document describes the Continuous Integration and Continuous Deployment (CI/CD) infrastructure set up for the PalatableAPI project, including runner choices, workflow design rationale, and maintenance procedures.

## Project Context

PalatableAPI is a **reverse engineering documentation project** for Palworld modding. Unlike traditional software projects, this repository contains:
- Structured documentation of game internals (memory layouts, function signatures, hooks)
- YAML-based findings following a defined schema
- Research notes and session handoffs
- Roadmap and planning documentation

The CI/CD workflows are designed specifically for this documentation-centric workflow, not traditional code testing.

## Runner Selection

### Primary Runner: `ubuntu-latest` (GitHub-hosted)

**Rationale:**
- **Cost-effective**: GitHub provides 2,000 free minutes/month for public repositories
- **Sufficient for documentation validation**: All workflows perform lightweight tasks (linting, link checking, schema validation)
- **Minimal dependencies**: Python 3.11 and Node.js 20 are all that's required
- **Fast startup**: Ubuntu runners boot in ~3-5 seconds
- **Standard environment**: Ensures consistent validation across all contributors

### Why NOT Windows or macOS runners:
- **Not needed**: The project documents Windows game internals, but CI validation is platform-agnostic
- **Cost**: Windows/macOS minutes consume GitHub Actions quota 2-10x faster
- **Performance**: Ubuntu is faster for script-based validation tasks
- **Overkill**: No platform-specific tooling required for documentation validation

### When to Consider Self-Hosted Runners:
- **IF** the project grows to include binary analysis automation (Ghidra, Cheat Engine)
- **IF** GitHub Actions quota becomes a constraint
- **IF** live game testing integration is added (would require Windows + actual game installation)

**Current recommendation**: Stick with GitHub-hosted Ubuntu runners. The project is well within free tier limits.

## Workflow Descriptions

### 1. Documentation Validation (`documentation-validation.yml`)

**Triggers:** Push to `main` or `claude/*` branches, PRs to `main`, manual dispatch

**Purpose:** Ensures all documentation files are syntactically correct and structurally sound.

**Jobs:**

#### `validate-markdown`
- **Tool**: `markdownlint-cli` (Node.js-based linter)
- **What it checks**:
  - Markdown syntax correctness
  - Heading structure
  - Consistent formatting
- **Lenient rules**: Disables line length limits (MD013), raw HTML (MD033), and strict indentation rules unsuitable for technical docs
- **Internal link checking**: Python script validates that all relative markdown links point to existing files
- **Non-blocking**: Style warnings don't fail the build

#### `validate-yaml`
- **Tool**: PyYAML (Python library)
- **What it checks**:
  - YAML syntax correctness across all `.yml` files
  - Excludes third-party code (`UE4SSforCONTEXTonly/`)
  - Validates GitHub Actions workflow YAML separately
- **Blocking**: Syntax errors fail the build

#### `validate-finding-schema`
- **Purpose**: Enforces the canonical schema defined in `schemas/FINDING_SCHEMA.md`
- **What it checks**:
  - All finding files have required YAML frontmatter
  - Required fields: `type`, `name`, `description`, `game_system`, `surface`, `source`, `confidence`, `status`
  - Valid field values against enumerated types
  - Warns on schema deviations without blocking
- **Schema-aware**: Understands 14 valid finding types, 3 confidence levels, 5 status values
- **Excludes**: Pre-migration files (old format, intentionally not migrated yet)

#### `check-structure`
- **Purpose**: Verifies the repository directory structure matches project requirements
- **What it checks**:
  - All required directories exist (18 directories per RULES.md)
  - All required root documentation files exist (7 files)
  - Fails if critical structure is missing
- **Why this matters**: The project organizes findings by game system and modding surface; missing directories indicate structural corruption

### 2. External Link Validation (`link-checker.yml`)

**Triggers:** Weekly (Mondays 9am UTC), PRs touching markdown files, manual dispatch

**Purpose:** Detects broken external URLs that may have moved or been deleted.

**Jobs:**

#### `check-external-links`
- **Tool**: Python `requests` library with retry logic
- **What it checks**:
  - All `http://` and `https://` URLs in markdown files
  - HTTP status codes (400+ = broken, 300+ = warning)
  - Handles sites that reject HEAD requests (falls back to GET)
  - Rate-limited to avoid triggering rate limiters (2s pause every 10 requests)
- **Non-blocking**: Reports broken links as warnings, doesn't fail builds
- **Why weekly**: External sites change slowly; daily checks would waste quota
- **Why non-blocking**: External link rot shouldn't block internal work

**Special handling:**
- User-Agent spoofing to avoid bot blocks
- 10-second timeout per URL
- Tracks which files reference each URL for debugging

### 3. Consistency and Logic Validation (`consistency-check.yml`)

**Triggers:** Push to `main` or `claude/*` branches, PRs to `main`, manual dispatch

**Purpose:** Validates logical coherence across the entire knowledge base.

**Jobs:**

#### `check-consistency`
- **Cross-reference validation**:
  - Every finding's `game_system` field must match an actual directory in `systems/`
  - Every finding's `surface` field must match an actual directory in `surfaces/`
  - Detects orphaned findings pointing to non-existent systems
  - **Blocking**: Invalid references fail the build

- **Duplicate detection**:
  - Identifies findings with identical `name` fields
  - Reports top 10 duplicates as warnings
  - **Non-blocking**: Legitimate duplicates may exist (same finding from multiple sources)
  - **Deduplication process**: Documented in PIPELINE.md, not enforced by CI

#### `check-roadmap-alignment`
- **Purpose**: Sanity check that documented progress matches actual repository state
- **What it checks**:
  - Latest session date vs today (warns if >30 days old)
  - Counts findings and confirmed hooks
  - Infers current project phase from session notes
- **Informational only**: No failures, just status reporting

## Workflow Execution Matrix

| Workflow | Frequency | Duration (est.) | Quota Impact | Fail Build? |
|----------|-----------|-----------------|--------------|-------------|
| Documentation Validation | Every push/PR | ~1-2 min | Low | Yes (YAML errors, structure) |
| Link Checker | Weekly | ~3-5 min | Very low | No |
| Consistency Check | Every push/PR | ~30-60 sec | Very low | Yes (invalid refs) |

**Total monthly quota usage estimate**: ~200 minutes/month (10% of free tier)

## Security Considerations

### Current Posture:
- ✅ All workflows run in isolated containers (GitHub-hosted runners)
- ✅ No secrets required (documentation-only project)
- ✅ No external deployment targets
- ✅ No write access to repository from workflows
- ✅ Third-party actions pinned to major versions (`@v4`, `@v5`)
- ✅ Python scripts run in inline heredocs (auditable, no external scripts)

### Future Considerations:
- **IF** MCP bridge integration is added:
  - Self-hosted runners will be required (Ghidra, Cheat Engine, x64dbg are Windows desktop tools)
  - Implement strict secret management for any API keys
  - Isolate runners from production networks
  - Use separate GitHub tokens with minimal permissions

- **IF** automated Steam Workshop publishing is added:
  - Store Steam credentials in GitHub Secrets
  - Use environment-specific workflows (staging vs production)
  - Implement approval gates for releases

## Maintenance Procedures

### Weekly Tasks:
- Review link checker output for broken external URLs
- Update `evidence/sources-2026.md` if official sources have moved

### Monthly Tasks:
- Review GitHub Actions usage (Settings → Billing)
- Update action versions if security advisories published
- Verify linter rule sets still appropriate as documentation evolves

### After Major Documentation Changes:
- Run workflows manually (`workflow_dispatch`) to validate before merging
- Check consistency warnings for new findings
- Update this document if new validation needs emerge

## Extending the Workflows

### Adding New Validation Rules:

1. **For markdown**:
   - Edit `.markdownlint.json` (create if needed) to customize rules
   - Reference: https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md

2. **For finding schema**:
   - Update validation logic in `validate-finding-schema` job
   - Reference `schemas/FINDING_SCHEMA.md` as source of truth
   - Add new required fields to `required_fields` set
   - Add new valid enum values to validation sets

3. **For cross-references**:
   - Extend `check-consistency` job with new relationship types
   - Add validation for `relationships` field in findings

### Adding New Workflows:

Example use cases:
- **Auto-generate documentation**: Build HTML docs from markdown on release
- **Dependency updates**: Dependabot for action versions
- **Binary analysis integration**: If MCP bridges are integrated into CI (requires self-hosted Windows runners)

## Troubleshooting

### Common Failure Scenarios:

#### "YAML validation errors found"
- **Cause**: Syntax error in `.yml` file (usually missing colon, incorrect indentation)
- **Fix**: Validate YAML locally with `yamllint` or online parser
- **Location**: Check workflow output for specific file and line number

#### "Invalid game_system 'xyz'"
- **Cause**: Finding references non-existent system directory
- **Fix**: Either create `systems/xyz/README.md` or correct the finding's frontmatter
- **Verify**: Run `ls systems/` to see valid system names

#### "Missing required fields"
- **Cause**: Finding file missing required YAML frontmatter fields
- **Fix**: Add missing fields per `schemas/FINDING_SCHEMA.md`
- **Common omissions**: `confidence`, `status`, `source.session`

#### "Missing required directories"
- **Cause**: Repository structure corrupted or incomplete checkout
- **Fix**: Ensure full clone (not shallow), re-clone if necessary
- **Verify**: Run `tree -L 1 -d` in repo root

### Debugging Workflows Locally:

1. **Markdown linting**:
   ```bash
   npm install -g markdownlint-cli
   markdownlint '**/*.md' --ignore 'unknowns/UE4SSforCONTEXTonly/**'
   ```

2. **YAML validation**:
   ```bash
   python3 -c "import yaml; yaml.safe_load(open('file.yml'))"
   ```

3. **Finding schema**:
   ```bash
   # Extract and validate frontmatter
   python3 << 'EOF'
   import yaml, re
   content = open('findings/example.md').read()
   match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
   print(yaml.safe_load(match.group(1)))
   EOF
   ```

## Metrics and Monitoring

### Key Performance Indicators:

- **Build success rate**: Target >95% (failures should be legitimate issues, not flaky tests)
- **Average build duration**: Target <3 minutes
- **Link checker findings**: Trend should decrease over time as sources stabilize
- **Schema validation warnings**: Should decrease as findings are migrated to canonical format

### Where to Find Metrics:

- **GitHub Actions tab**: Real-time workflow status
- **Insights → Actions**: Historical success rates, duration trends
- **Checks API**: Programmatic access to workflow results

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub-hosted runners specifications](https://docs.github.com/en/actions/using-github-hosted-runners/about-github-hosted-runners)
- [markdownlint rules](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md)
- Project-specific:
  - `schemas/FINDING_SCHEMA.md` - Finding data model
  - `workflow/PIPELINE.md` - Finding ingestion workflow
  - `RULES.md` - Session continuation rules

---

**Last Updated**: 2026-05-29
**Maintained By**: Project maintainers
**Review Cadence**: Quarterly or when major project phase changes occur
