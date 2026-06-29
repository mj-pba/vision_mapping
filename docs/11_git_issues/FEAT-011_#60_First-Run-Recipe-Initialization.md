---
GitHub Issue: #60
Type: Feature
Priority: High
Status: Open
Assignee: Malith
Sprint: Backlog
Labels: type: feature, priority: high
Created: 2026-06-19
Requirement Refs: TASK-005
---

# [FEAT-011] First-Run Recipe Data Initialization

## Description / User Story

**As a** machine operator deploying PBA Vision Mapping for the first time,
**I want** the application to automatically create default recipe files if they don't exist,
**so that** the software starts up correctly without manual file setup.

## Context and Motivation

After TASK-005 (#59) externalizes recipe data to `PBA_vision_mapping_recepy_data/`, the recipe folder and files will live **outside** the compiled executable. This means:

1. **First deployment** — The folder won't exist yet when the `.exe` is first extracted/installed
2. **Accidental deletion** — An operator could delete or corrupt recipe files
3. **New machine setup** — Each new gantry installation needs a clean starting point

Without this feature, the application will crash on startup with `FileNotFoundError` if the recipe folder is missing.

## Dependency

> [!IMPORTANT]
> This feature **depends on** [TASK-005 (#59)](TASK-005_%2359_Externalize-Recipe-Data.md) being completed first. The recipe path resolution utility (`get_recipe_data_dir()`) must exist before this feature can be implemented.

## Expected Behavior

```
Application starts
  → Check: Does PBA_vision_mapping_recepy_data/ folder exist?
    → NO:  Create folder + write default recipe files → Log "First-run: created default recipe data" → Continue startup
    → YES: Check: Do required files exist inside it?
      → All present:  Continue startup (no action needed)
      → Some missing: Create only the missing files with defaults → Log warning → Continue startup
      → Files corrupt: Log error → Show UI warning → Use defaults in memory → Continue startup
```

## Default Recipe Files

### `active_recipe.csv` — Default Values

```csv
parameter,value
image_width,4096
image_height,3000
image_center_pixel_x,2048
image_center_pixel_y,1500
circle_radius,87
circle_radius_tolerance,30
pixel_to_mm,0.01146499
dot_pitch_in_pix,1160
image_brightness_threshold_value,170
pixel_to_mm_original,0.0011526
```

### `camera_calibration_data_2X_lens.npz`

> [!WARNING]
> Camera calibration data is machine-specific and cannot have meaningful defaults. The first-run initialization should either:
> - **Option A:** Skip creating this file and show a UI prompt: "Camera calibration required — please run calibration before first scan"
> - **Option B:** Create a placeholder identity calibration (no distortion correction) that allows the app to start but produces uncalibrated results

**Recommendation:** Option A — it's safer to force calibration than to silently produce incorrect measurements in a precision metrology application.

## Technical Tasks

- [ ] Create `default_recipes/` resource folder containing template recipe files
- [ ] Implement `ensure_recipe_data_exists()` function in the path utility module
- [ ] Call `ensure_recipe_data_exists()` early in `main.py` startup sequence
- [ ] Handle folder creation (`os.makedirs(..., exist_ok=True)`)
- [ ] Handle individual file creation (only create missing files, don't overwrite existing)
- [ ] Add validation for `active_recipe.csv` format (correct headers, numeric values)
- [ ] Add logging for all first-run actions (created folder, created files, skipped existing)
- [ ] Show UI notification if calibration data is missing
- [ ] Add unit tests for:
  - [ ] Folder missing → creates folder + files
  - [ ] Folder exists, files missing → creates only missing files
  - [ ] Folder exists, all files present → no action
  - [ ] Recipe file has invalid format → log warning, use defaults

## Acceptance Criteria

- [ ] **GIVEN** a fresh deployment with no `PBA_vision_mapping_recepy_data/` folder, **WHEN** the application starts, **THEN** the folder and default `active_recipe.csv` are created automatically
- [ ] **GIVEN** the recipe folder exists with all files, **WHEN** the application starts, **THEN** no files are modified or overwritten
- [ ] **GIVEN** the recipe folder exists but `active_recipe.csv` is missing, **WHEN** the application starts, **THEN** only the missing file is created with defaults
- [ ] **GIVEN** camera calibration data is missing, **WHEN** the application starts, **THEN** a clear UI message informs the operator that calibration is required
- [ ] **GIVEN** `active_recipe.csv` exists but has invalid content, **WHEN** the application starts, **THEN** a warning is logged and sensible defaults are used in memory

## Definition of Done

- [ ] Code reviewed and approved
- [ ] Unit tests written and passing
- [ ] Tested on fresh deployment (no recipe folder)
- [ ] Tested on existing deployment (recipe folder already present)
- [ ] Tested with corrupted/partial recipe data
- [ ] Documentation updated
- [ ] No regression in existing scan/certificate/error-map workflows

## Notes

- Default values in `active_recipe.csv` are based on the current 0.35X telecentric lens configuration
- When new lens configurations are added (e.g., 4X telecentric), consider supporting multiple recipe profiles
- The initialization check should run **before** any module tries to read recipe data
- Consider adding a "Reset to Defaults" button in the UI for operators to restore factory settings
