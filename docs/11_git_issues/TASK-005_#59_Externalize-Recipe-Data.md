---
GitHub Issue: #NN
Type: Task
Priority: High
Status: Open
Assignee: Malith
Sprint: Backlog
Labels: type: tech-debt, priority: high
Created: 2026-06-19
Requirement Refs: —
---

# [TASK-005] Externalize Recipe Data — Move `src/recipes/` Outside Source Tree

## Description

Currently, application recipe/configuration data files (`active_recipe.csv`, `camera_calibration_data_2X_lens.npz`) are stored inside the source tree at `src/recipes/`. This is incorrect for a compiled executable (PyInstaller `.exe`) because:

1. **Bundled files are read-only** — PyInstaller packages `src/` into a frozen archive. Files inside it cannot be modified at runtime.
2. **Parameters need updating** — The recipe file contains operational parameters (pixel-to-mm ratio, circle radius, brightness threshold, etc.) that operators need to adjust per machine/lens configuration.
3. **Camera calibration data** — Calibration `.npz` files may be regenerated after hardware changes (lens swap, camera replacement).

### Solution

Move the recipe data to an **external folder** relative to the executable location:

```
<exe_parent_directory>/
├── PBA_vision_mapping.exe
└── PBA_vision_mapping_recepy_data/
    ├── active_recipe.csv
    └── camera_calibration_data_2X_lens.npz
```

The application should resolve the data path at runtime relative to the executable location (or `os.getcwd()` during development), **not** relative to the source tree.

> ⚠️ **BREAKING CHANGE:** This changes how every module resolves the recipe file path. All 15+ references to `src/recipes/` across the codebase must be updated simultaneously. Partial migration will break the application.

## Current Recipe Files

| File | Purpose | Mutable at Runtime? |
|------|---------|-------------------|
| `active_recipe.csv` | Operational parameters (image size, pixel-to-mm, circle radius, thresholds) | ✅ Yes — operators tune these |
| `camera_calibration_data_2X_lens.npz` | Camera lens distortion calibration data | ✅ Yes — regenerated after hardware changes |

## Affected Files (15 references across 9 files)

### Image Processing
- [ ] `src/backend/image_processing/calculation_using_halcon.py` — **2 references** (lines ~30, ~248)
- [ ] `src/backend/image_processing/scan_and_capture.py` — **3 references** (lines ~422, ~571, ~572)

### Controllers
- [ ] `src/backend/controllers/calibration_data_controller.py` — **1 reference** (line ~551)
- [ ] `src/backend/controllers/controller.py` — **1 reference** (line ~318)

### Services
- [ ] `src/backend/services/generate_2D_glass_certificate_62207.py` — **2 references** (lines ~93, ~575)
- [ ] `src/backend/services/generate_2D_glass_certificate_62207_v1.py` — **2 references** (lines ~89, ~706)
- [ ] `src/backend/services/generate_2D_glass_certificate_62207_v2.py` — **2 references** (lines ~89, ~704)
- [ ] `src/backend/services/backup_2D_plot_test.py` — **1 reference** (line ~18)
- [ ] `src/backend/services/generate_2D_error_mapping_test_plot.py` — **1 reference** (line ~21)

### Other
- [ ] `src/recipes/` directory — **remove from source tree** after migration

## Technical Tasks

- [ ] Create a path resolution utility function (e.g., `get_recipe_data_dir()`) that returns the correct path for both:
  - **Development mode:** `<project_root>/PBA_vision_mapping_recepy_data/`
  - **Compiled mode:** `<exe_dir>/PBA_vision_mapping_recepy_data/`
- [ ] Create `PBA_vision_mapping_recepy_data/` folder at the project root level
- [ ] Move `active_recipe.csv` from `src/recipes/` to `PBA_vision_mapping_recepy_data/`
- [ ] Move `camera_calibration_data_2X_lens.npz` from `src/recipes/` to `PBA_vision_mapping_recepy_data/`
- [ ] Update all 9 affected source files to use the new path resolution utility
- [ ] Remove hardcoded `r'src\\recipes\\...'` path strings from all modules
- [ ] Remove legacy commented-out absolute paths (e.g., `C:\\Users\\malit\\Documents\\...`)
- [ ] Add `.gitkeep` or a README to `PBA_vision_mapping_recepy_data/` so the folder is tracked
- [ ] Update `.gitignore` if needed (ensure data files are tracked or templated)
- [ ] Delete `src/recipes/` directory after all references are migrated
- [ ] Update `AGENTS.md` project structure diagram
- [ ] Update PyInstaller spec/build script (if exists) to exclude `PBA_vision_mapping_recepy_data/` from the bundle

## Acceptance Criteria

- [ ] No source file references `src/recipes/` or `src\\recipes\\`
- [ ] Application runs correctly in development mode with `python src/main.py`
- [ ] Recipe parameters can be read and written at runtime
- [ ] Camera calibration data loads correctly from the new location
- [ ] All existing scan methods (`scan_method_4()`, `scan_method_5()`, etc.) work with the new path
- [ ] Path resolution works for both Windows (`\\`) and macOS/Linux (`/`) paths

## Definition of Done

- [ ] Code reviewed and approved
- [ ] All 9 affected files updated and tested
- [ ] Tests written and passing
- [ ] Old `src/recipes/` directory deleted
- [ ] Documentation updated (AGENTS.md, as-built updates)
- [ ] No regression in scanning, certificate generation, or error mapping workflows

## Risk Assessment

| Risk | Mitigation |
|------|-----------|
| Missed file reference → runtime crash | Grep for `recipes` across entire codebase before marking complete |
| Windows path separators (`\\`) vs POSIX (`/`) | Use `os.path.join()` or `pathlib.Path` exclusively |
| PyInstaller frozen path differs from dev path | Use `sys._MEIPASS` detection for frozen mode |
| Operators don't have the external folder | Add first-run check that creates default recipe files if missing |

## Implementation Notes

### Recommended Path Resolution Pattern

```python
import os
import sys

def get_recipe_data_dir() -> str:
    """Return the path to the external recipe data directory.
    
    Works in both development and PyInstaller-compiled modes.
    """
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        base_dir = os.path.dirname(sys.executable)
    else:
        # Running in development
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__)
        )))  # Navigate up to project root
    
    return os.path.join(base_dir, 'PBA_vision_mapping_recepy_data')
```

### Git Branch

```
feature/#59-externalize-recipe-data
```

## Notes

- This is a **breaking change** — all 15 references must be migrated in one atomic PR
- Consider adding a `default_active_recipe.csv` as a template that gets copied on first run
- Future recipe files (e.g., for different lens configurations) should also go into this folder
- The `config` scope in TS-002 is appropriate for commits in this task
