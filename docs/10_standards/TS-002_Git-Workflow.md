# Git Workflow & GitHub Standards

---
**Document ID:** TS-002
**Title:** Git Workflow, GitHub Issues & Projects Standard — PBA Vision Mapping
**Version:** 1.1
**Status:** Active
**Owner:** Project Lead
**Last Updated:** 2026-04-20
**Review Due:** 2026-07-20
**Approved By:** Project Lead
---

# TS-002 — Git Workflow & GitHub Standards

> This document is the single authoritative reference for Git workflow, commit conventions, branching, GitHub Issues, and release process. It is designed to be used daily.

---

## 1. Branch Strategy at a Glance

```
main          ← Production-ready. Protected. Every commit is deployable.
│
develop       ← Integration branch. All features merge here first.
│
├── feature/#NNN-description     ← New feature
├── fix/#NNN-description         ← Bug fix
├── research/#NNN-description    ← Research / experiment
├── hotfix/#NNN-description      ← Emergency production fix
└── docs/#NNN-description        ← Documentation update
```

### Branch Rules

| Branch | Created From | Merges Into | Who Merges | Push Allowed? |
|--------|-------------|------------|-----------|---------------|
| `main` | — | — | Team Lead | ❌ Never (direct push) |
| `develop` | — | — | Team Lead | ❌ Never (direct push) |
| `feature/*` | `develop` | `develop` | Developer (after review) | ✅ Own branch |
| `fix/*` | `develop` | `develop` | Developer (after review) | ✅ Own branch |
| `research/*` | `develop` | `develop` | Developer (after TL review) | ✅ Own branch |
| `hotfix/*` | `main` | `main` AND `develop` | Team Lead | ✅ Own branch |
| `docs/*` | `develop` | `develop` | Any (after review) | ✅ Own branch |

### Branch Naming

```
Pattern: <type>/#<issue-number>-<short-description>

✅ feature/#12-glass-certificate-1d
✅ fix/#15-scan-log-path-error
✅ research/#10-pixel-to-mm-calibration
✅ hotfix/#INC-001-motor-timeout
✅ docs/#20-update-agents-md

❌ Feature_12_Glass_Certificate      (capitals, underscores)
❌ feature/glass-certificate          (missing issue number)
❌ my-branch                          (no type, no issue)
```

---

## 2. Commit Message Format (Conventional Commits)

```
<type>[optional scope]: <description in imperative mood>

[optional body]

[optional footer: Closes #NNN]
```

### Types

| Type | Use For | Bumps Version? |
|------|---------|---------------|
| `feat` | New feature | Minor (1.x.0) |
| `fix` | Bug fix | Patch (1.0.x) |
| `docs` | Documentation only | No |
| `test` | Adding/updating tests | No |
| `refactor` | Code restructuring, no behaviour change | No |
| `perf` | Performance improvement | Patch |
| `build` | Build system / dependencies | No |
| `ci` | CI/CD pipeline changes | No |
| `chore` | Maintenance, tooling, config | No |
| `research` | Experimental (research/* branches only) | No |

### Scopes

Scopes identify **which domain or module** the change belongs to. Each scope maps directly to a functional area of the PBA Vision Mapping system.

| Scope | Domain | What it covers | Key files |
|-------|--------|---------------|-----------|
| `scan` | Test execution | All test cases orchestrated by the scanner: position stability, 1D/2D expansion tests (X/Y), 2D error mapping scan, auto-focus, laser test, motion distance estimation, pixel distance, glass thermal expansion | `scan_and_capture.py` |
| `calc` | Calculation | Mathematical processing: positional error calculation, encoder error matrix generation, pixel-to-mm conversion, image-based distance calculation, image rotation, image correction algorithms | `calculate_position_error.py`, `generate_2D_encoder_error_matrix.py` |
| `vision` | Computer vision | Vision algorithms: sub-pixel circle edge detection (gradient-based), image distortion correction, HALCON XLD contour detection, pixel distance computation from images. Use this scope when HALCON is later replaced by CUDA-based detection | `calculation_using_halcon.py`, OpenCV processing modules |
| `camera` | Camera hardware | Camera SDK bindings, camera API integration, camera calibration, image distortion profiling, optics characterisation | `dahua_cam_api/`, FLIR PySpin bindings |
| `motor` | Motion control | ACS motor controller, axis movement commands, trajectory parameters | `acs_python_modules.py` |
| `certificate` | Output — certificate | Glass scale certificate generation (1D column extract and 2D full grid) | `generate_2D_glass_certificate_62207.py` |
| `error-map-1d` | Output — 1D error map | 1D error map generation, verification against certified values, 1D plot output | Services and tests targeting single-axis error maps |
| `error-map-2d` | Output — 2D error map | 2D error map generation, full XY grid visualisation, ACS controller compensation file generation | `generate_2D_error_mapping_test.py`, `generate_2D_error_mapping_test_plot.py` |
| `ui` | Frontend | PySide6 GUI components, tab layout, signal-slot wiring, UI controller logic | `src/frontend/` |
| `docs` | Documentation | Documentation-only changes (standards, guides, issue files, as-built updates) | `docs/` |
| `config` | Configuration | Constants, environment config files, machine-specific parameters | `config.ini`, constants modules |
| `ci` | CI/CD | GitHub Actions workflows, linting pipelines, test automation | `.github/` |

#### How to Select a Scope — Decision Guide

Work through these questions in order and use the **first match**:

```
1. Does this change affect a TEST CASE run by the scanner
   (stability, expansion, error-map scan, auto-focus, laser, motion distance)?
   → scan

2. Does this change affect a MATHEMATICAL CALCULATION
   (error computation, matrix generation, pixel-to-mm, distance from images)?
   → calc

3. Does this change affect a VISION ALGORITHM
   (edge detection, image correction, rotation, distortion, sub-pixel fitting,
    HALCON detection, or future CUDA replacement)?
   → vision

4. Does this change affect CAMERA HARDWARE
   (SDK bindings, camera API, calibration, optics characterisation)?
   → camera

5. Does this change affect MOTOR CONTROL or AXIS MOVEMENT?
   → motor

6. Does this change affect GLASS CERTIFICATE generation or output?
   → certificate

7. Does this change affect the 1D ERROR MAP specifically?
   → error-map-1d

8. Does this change affect the 2D ERROR MAP or ACS compensation file?
   → error-map-2d

9. Does this change affect the UI / PySide6 frontend?
   → ui

10. Is this a DOCUMENTATION-ONLY change?
    → docs

11. Is this a CONFIG FILE or constants change?
    → config

12. Is this a CI/CD PIPELINE change?
    → ci
```

> **When scope is ambiguous:** If a single commit touches two scopes equally, split it into two atomic commits. If you cannot split, choose the scope that describes the *primary output or user-visible effect* of the change.

> **Scope is optional** for trivial `chore` or `ci` commits where the scope adds no clarity (e.g., `chore: update .gitignore`).

### Examples

```bash
# Test case — new scan type added to scan_and_capture.py
feat(scan): add 2D expansion test case to scanner workflow

# Calculation — error matrix logic changed
feat(calc): implement bilinear interpolation for encoder error matrix

# Vision algorithm — sub-pixel detection improved
perf(vision): replace centroid with gradient-based edge detection for sub-pixel accuracy

# Vision algorithm — HALCON → CUDA migration (future)
refactor(vision): replace halcon XLD detection with cuda-based circle fit

# Camera — SDK change
fix(camera): correct FLIR exposure time units from microseconds to milliseconds

# Certificate output
feat(certificate): add 1D glass certificate generation for single column

# 1D error map
feat(error-map-1d): add X-axis 1D error map generation from scan log

# 2D error map
feat(error-map-2d): generate ACS controller compensation file from 2D error grid

# Bug fix in scan path
fix(scan): correct log file path to use logs/ directory

# UI change
feat(ui)!: redesign error mapping tab layout  # Breaking change

# Documentation only
docs(docs): update agents.md with phase 1 completed features

# Ambiguous — calc touches vision: split into two commits
feat(vision): add gradient-based circle edge detection
feat(calc): integrate detected edge positions into pixel-to-mm calibration
```

### Rules
- ✅ Imperative mood: "add", "fix", "update"
- ✅ Under 72 characters total
- ✅ Include issue reference in footer: `Closes #NN`
- ❌ No "WIP", "temp", "fix fix", "FINAL"
- ❌ No period at end
- ❌ No capital first letter

### Breaking Changes

Mark with `!` after the type/scope:

```
feat(certificate)!: change glass certificate CSV output format

All columns now use ISO 80000-1 standard units (mm).
Existing scripts that parse the old format will need updating.

BREAKING CHANGE: CSV columns renamed from X_Error to Delta_X.
See docs/8_context_cohesion/as_built_updates.md for migration details.

Closes #NN
```

---

## 3. Daily Workflow Cheat Sheet

### Starting a New Feature

```bash
# 1. Switch to develop and pull latest
git checkout develop
git pull origin develop

# 2. Create feature branch
git checkout -b feature/#12-glass-certificate-1d

# 3. Develop with small, frequent commits
git add src/backend/services/generate_glass_certificate_1d.py
git commit -m "feat(certificate): add 1D glass certificate generation for column C50

Generates a 1D certificate by extracting a single column from the 2D scan
data and comparing with the original certified values.

Refs #12"

# 4. Push branch and open PR
git push -u origin feature/#12-glass-certificate-1d
# → Open PR on GitHub against develop
```

### Keeping Your Branch Up to Date

```bash
# Rebase your feature branch on latest develop
git checkout develop
git pull origin develop
git checkout feature/#12-glass-certificate-1d
git rebase develop

# If conflicts: resolve, then
git add .
git rebase --continue
```

### After PR Approval

```bash
# Reviewer merges the PR on GitHub (not you)
# Delete your local branch
git checkout develop
git pull origin develop
git branch -d feature/#12-glass-certificate-1d
```

---

## 4. PR Checklist (Copy Before Every PR)

```
Before opening this PR:
  [ ] Branch is up to date with develop
  [ ] Linter passes locally (ruff check .)
  [ ] Formatter passes locally (black .)
  [ ] All tests pass locally (pytest tests/)
  [ ] Coverage has not dropped
  [ ] No secrets or credentials in any file
  [ ] PR template is fully filled in
  [ ] PR is under 400 lines changed
  [ ] Assigned a reviewer (or self-reviewed if solo)
```

### PR Template

Every PR must use this template (saved as `.github/PULL_REQUEST_TEMPLATE.md`):

```markdown
## Summary
[1–3 sentences describing what this PR does and why]

## Related Story / Issue
Closes: #[issue-number]

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Refactor
- [ ] Documentation
- [ ] Test
- [ ] Research / experimental

## Changes Made
- [Specific change 1]
- [Specific change 2]

## How to Test
1. [Step to verify the change works]
2. [Expected result]

## Definition of Done Checklist
- [ ] Code follows the project style guide (linting passes)
- [ ] Unit tests written and passing
- [ ] Test coverage maintained or improved
- [ ] No new warnings
- [ ] README or docs updated if applicable
- [ ] Acceptance criteria verified
- [ ] Hardware test documented (if applicable)

## Screenshots / Results (if applicable)
[Add screenshots for UI changes; add CSV output samples for data changes]

## Notes for Reviewer
[Anything the reviewer should know: design trade-offs, open questions]
```

---

## 5. GitHub Issues — Templates

GitHub Issues are the single source of truth for all work items.

### 5.1 Issue Types and Labels

| Label | Colour | When to Use |
|-------|--------|------------|
| `type: epic` | `#3E4B9E` (indigo) | Large body of work grouping multiple issues |
| `type: feature` | `#0075CA` (blue) | New feature or capability |
| `type: user-story` | `#0075CA` (blue) | Feature from user perspective |
| `type: bug` | `#D73A4A` (red) | Something broken |
| `type: research` | `#7057FF` (purple) | Exploratory / calibration research |
| `type: tech-debt` | `#E4E669` (yellow) | Refactor, cleanup |
| `type: docs` | `#0052CC` (dark blue) | Documentation only |
| `type: hardware` | `#006B75` (teal) | Physical equipment tasks |
| `priority: critical` | `#B60205` | Blocking production |
| `priority: high` | `#E4430F` | Current sprint |
| `priority: medium` | `#F9A825` | Near future |
| `priority: low` | `#A2EEEF` (teal) | Parking lot |
| `status: blocked` | `#D93F0B` (orange) | Needs external input |
| `status: needs-info` | `#FBCA04` (yellow) | Awaiting clarification |

### 5.2 Issue Template — Feature / User Story

```markdown
## Description / User Story
**As a** [persona],
**I want to** [action],
**so that** [benefit].

## Acceptance Criteria
- [ ] **GIVEN** [context], **WHEN** [action], **THEN** [expected result]

## Technical Tasks
- [ ] Task 1
- [ ] Task 2

## Definition of Done
- [ ] Code reviewed and approved
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] Hardware test documented (if applicable)
```

### 5.3 Issue Template — Research Task

```markdown
## Research Question
[State the specific question — not a task]

## Context and Motivation
[Why are we investigating this?]

## Approach
**Equipment:** [Camera, lens, glass scale, cleanroom?]
**Method:** [What you will try]
**Baseline:** [What "good" means]

## Success Criteria
- [ ] [Metric] exceeds [threshold]
- [ ] Results are reproducible
- [ ] Findings documented

## Time Box
**Maximum time:** [e.g. 2 weeks]
```

### 5.4 Issue Template — Hardware Task

```markdown
## Description
[What hardware task needs to be done]

## Equipment Required
- [Equipment 1]
- [Equipment 2]

## Procedure
1. [Step 1]
2. [Step 2]

## Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]

## Safety Notes
[Any safety precautions]

## Definition of Done
- [ ] Hardware task completed
- [ ] Test results documented
- [ ] Photos / measurements captured
- [ ] As-built updates logged
```

---

## 6. Sprint Board Columns

| Column | Meaning | Rule |
|--------|---------|------|
| **Backlog** | Prioritised but not in a sprint | |
| **Sprint — To Do** | Committed to current sprint | |
| **In Progress** | Being worked on | Max 2 per person |
| **In Review** | PR open, waiting for review | |
| **Done** | Merged, DoD complete | |
| **Blocked** | Cannot proceed | Must annotate with blocker |

---

## 7. Release Process

```
Sprint ends
  → Sprint Review passed
    → Team Lead reviews develop
      → Tag version on develop (e.g., v1.2.0)
        → Merge develop → main
          → Deploy / release
            → Announce release
```

### Semantic Versioning

```
MAJOR.MINOR.PATCH

MAJOR → Breaking changes (feat!: ...)
MINOR → New features (feat: ...)
PATCH → Bug fixes (fix: ...)

Example progression:
  0.1.0 → 0.2.0 → 0.2.1 → 0.3.0 → 1.0.0
```

---

## 8. Code Review Standards

### 8.1 Conventional Comments

All review comments must use the **Conventional Comments** format:

| Label | Meaning | Author Action Required? |
|-------|---------|------------------------|
| `**praise:**` | Something done well | No |
| `**nit:**` | Tiny style or preference issue | Optional |
| `**suggestion:**` | An improvement, not required to merge | Optional |
| `**issue:**` | A correctness or design problem that must be fixed | **Yes — must fix** |
| `**question:**` | Reviewer does not understand something | **Yes — must respond** |
| `**thought:**` | Future idea, no action now | No |
| `**todo:**` | Must be done in a follow-up issue | **Yes — create issue** |

### 8.2 Review Checklist

#### Tier 1 — Always Check (Blocks Merge)

- [ ] Does the code do what the issue describes?
- [ ] Are error paths handled? (file not found, empty data, hardware timeout)
- [ ] No hardcoded credentials or local machine paths
- [ ] Tests written for new behaviour

#### Tier 2 — Check for PRs > 50 Lines

- [ ] Variable names express intent
- [ ] Functions under 50 lines
- [ ] No commented-out code
- [ ] Type hints on all function signatures

---

## 9. Related Documents

| Document | Purpose |
|----------|---------|
| [TS-001 — Coding Standards](TS-001_Coding-Standards.md) | Code quality, formatting, language standards |
| [TS-003 — Definition of Done](TS-003_Definition-of-Done.md) | DoD checklist |
| [Git Issues README](../11_git_issues/README.md) | Local issue mirror conventions |

---

## Change Log

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-04-14 | Malith | Initial version — adapted from docs_SOP/TS-002; updated scopes and examples to PBA Vision Mapping domain |
| 1.1 | 2026-04-20 | Malith | Rewrote Scopes section: expanded scope table to map all project modules; added decision guide for scope selection; updated commit examples to reflect test cases, calc, vision, error-map-1d/2d scopes |
