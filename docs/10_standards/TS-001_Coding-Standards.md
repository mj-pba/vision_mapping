# Coding Standards

---
**Document ID:** TS-001
**Title:** Coding Standards — PBA Vision Mapping
**Version:** 1.0
**Status:** Active
**Owner:** Project Lead
**Last Updated:** 2026-04-14
**Review Due:** 2026-07-14
**Approved By:** Project Lead
---

# TS-001 — Coding Standards

---

## 1. Purpose

This document is the project-wide coding standards reference for PBA Vision Mapping. It defines how code is written, formatted, documented, and tested. Every developer — including new team members during handover — must follow these standards.

This is the **single authoritative source** for coding conventions. If you are unsure about a convention, check here first.

---

## 2. General Principles

These apply to every line of code in the project.

### 2.1 Readability Over Cleverness

```python
# Bad — clever but unreadable
result = [x for x in (y.strip() for y in f.readlines()) if x and not x.startswith('#')]

# Good — clear and maintainable
lines = f.readlines()
stripped_lines = [line.strip() for line in lines]
result = [line for line in stripped_lines if line and not line.startswith('#')]
```

Write code that someone unfamiliar with the project can understand without asking you. This project will be handed over to a team.

### 2.2 Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Variables | `snake_case` | `dot_center_x`, `error_matrix` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_DOT_PITCH = 5.0`, `GLASS_SCALE_SIZE = 500` |
| Functions / Methods | `snake_case` | `calculate_position_error()`, `generate_glass_certificate()` |
| Classes | `PascalCase` | `ScanGrid`, `GlassCertificate`, `ErrorMapping` |
| Files | `snake_case.py` | `scan_and_capture.py`, `calculate_position_error.py` |
| Directories | `snake_case` | `image_processing/`, `motor_control/` |
| Boolean variables | Phrased as questions | `is_scanning`, `has_calibration_data`, `should_save_log` |

**Naming quality test:** Can a new team member understand what this variable does without reading the surrounding code?

### 2.3 Function Design

| Rule | Standard | Enforcement |
|------|----------|-------------|
| Maximum function length | 50 lines (hard limit) | Code review blocks PR |
| Maximum parameters | 4 (use a config object / data class for more) | Code review |
| Single responsibility | One function does one thing | Code review |
| Command-Query Separation | A function either does something OR returns something — not both | Code review |

```python
# Bad — does too much
def process_scan_data(log_file, certificate_path, generate_plots=True, save_to_acs=True):
    # 80 lines of mixed logic...
    pass

# Good — separated concerns
def load_scan_log(log_file_path: Path) -> pd.DataFrame:
    """Load and validate the raw scan log data."""
    ...

def calculate_dot_errors(scan_data: pd.DataFrame, nominal_locations: pd.DataFrame) -> pd.DataFrame:
    """Calculate positional errors for each measured dot."""
    ...

def save_glass_certificate(errors: pd.DataFrame, output_path: Path) -> None:
    """Write the glass certificate CSV file."""
    ...
```

### 2.4 Error Handling

| Rule | Standard |
|------|----------|
| Catch specific exceptions | `except ValueError` not `except Exception` and never bare `except:` |
| Error messages describe the problem | Include what happened, where, and what the user/developer should do |
| Fail fast | Validate inputs at function boundaries, not deep inside logic |
| Log before raising | Log the error with context before raising (for debugging later) |

```python
# Bad
try:
    result = process(data)
except:
    print("Error")

# Good
try:
    scan_data = load_scan_log(log_file_path)
except FileNotFoundError as e:
    logger.error(
        "Scan log file not found: %s. Expected at path: %s. "
        "Verify the scan was completed and the log file was generated.",
        e.filename, log_file_path
    )
    raise
except pd.errors.EmptyDataError as e:
    logger.error(
        "Scan log file %s is empty — scan may not have completed successfully.",
        log_file_path
    )
    raise
```

### 2.5 Comments

| Type | Rule | Example |
|------|------|---------|
| **Why comments** | Always explain *why*, never *what* | `# Overlap of 50 pixels ensures no dots are missed at image boundaries` |
| **Domain comments** | Explain domain-specific constants | `# 5mm pitch = nominal distance between dot centers on glass scale` |
| **TODO comments** | Must include GitHub Issue reference | `# TODO: GH-#NN add retry logic for camera connection timeout` |
| **Commented-out code** | **Forbidden** — use git history instead | Code review blocks PR |
| **Docstrings** | Required on all public functions/classes | See §3.3 |

### 2.6 File Organisation

| Rule | Standard |
|------|----------|
| Maximum file length | 500 lines (split into modules if exceeded) |
| Import ordering | Standard library → third-party → local (enforced by isort) |
| One class per file | For non-trivial classes (small data classes can share a file) |
| No circular imports | If A imports B and B imports A, restructure |

### 2.7 Forbidden Practices (PR Blockers)

These will block any PR from being merged — no exceptions:

- ❌ Hardcoded credentials, API keys, passwords, or secrets
- ❌ Commented-out code blocks
- ❌ `TODO` without a GitHub Issue reference
- ❌ `print()` debugging left in production code
- ❌ Functions exceeding 50 lines
- ❌ Files exceeding 500 lines
- ❌ Mutable default arguments in Python (`def fn(items=[])`)
- ❌ Bare `except:` clauses
- ❌ Hardcoded file paths to local machines (`C:\Users\specific-user\...`)

---

## 3. Python Standards

> Python 3.13 is the project language for all application code.

### 3.1 Tooling

| Tool | Purpose | Configuration |
|------|---------|---------------|
| **Formatter:** `black` | Code formatting | Line length 88, default settings |
| **Linter:** `ruff` | Static analysis | See `pyproject.toml` for rule set |
| **Import sorter:** `isort` | Import ordering | Compatible with black (`profile = "black"`) |
| **Type checker:** `mypy` | Static type checking | `--strict` mode for production code |

### 3.2 Type Hints

Type hints are **required** on all function signatures for production code. Research scripts on `research/*` branches may defer type hints until promoted.

```python
# Required for all public functions
def calculate_dot_center(
    image: np.ndarray,
    roi: tuple[int, int, int, int],
    threshold: float = 0.5,
) -> tuple[float, float]:
    """Calculate the sub-pixel center of a dot in the given ROI."""
    ...

# For complex types, use typing module
from typing import Optional
from pathlib import Path

def generate_glass_certificate(
    log_file_path: Path,
    reference_locations_path: Path,
    output_path: Optional[Path] = None,
) -> pd.DataFrame:
    ...
```

### 3.3 Docstrings (Google Style)

```python
def calculate_position_error(
    measured_x: float,
    measured_y: float,
    nominal_x: float,
    nominal_y: float,
) -> tuple[float, float]:
    """Calculate the positional error between measured and nominal dot locations.

    Computes the difference (delta) between the vision-measured position
    and the nominal (design) position for a single dot on the glass scale.
    Results are in millimeters.

    Args:
        measured_x: The X coordinate measured by the vision system (mm).
        measured_y: The Y coordinate measured by the vision system (mm).
        nominal_x: The nominal X coordinate from the reference grid (mm).
        nominal_y: The nominal Y coordinate from the reference grid (mm).

    Returns:
        A tuple (delta_x, delta_y) representing the positional errors
        in the X and Y directions respectively, in millimeters.

    Raises:
        ValueError: If any coordinate value is outside the expected
            glass scale range (0 to 500mm).

    Example:
        >>> dx, dy = calculate_position_error(
        ...     measured_x=250.0012, measured_y=250.0005,
        ...     nominal_x=250.0000, nominal_y=250.0000,
        ... )
        >>> print(f"Error: ({dx:.4f}, {dy:.4f}) mm")
        Error: (0.0012, 0.0005) mm
    """
```

### 3.4 Python-Specific Rules

| Rule | Standard |
|------|----------|
| String formatting | f-strings only — not `%` or `.format()` |
| File handling | Context managers (`with` statement) |
| File paths | `pathlib.Path` — not `os.path` string concatenation |
| Exceptions | Specific types: `except ValueError` not `except Exception` |
| Mutable defaults | `def fn(items=None):` then `items = items or []` inside |
| Data containers | `@dataclass` for data-only classes |
| Enums | `enum.Enum` for fixed sets of values (scan types, axis names, etc.) |
| Logging | `logging` module — not `print()` |
| CSV output | All CSV files go to `logs/` directory |

### 3.5 PySide6 / Qt Conventions

| Rule | Standard |
|------|----------|
| UI files | Edit `.ui` in Qt Designer, compile with `pyside6-uic` |
| Signal-slot | Use `@Slot()` decorator for slot methods |
| Threading | Long operations in `QThread` or `QRunnable` — never block the UI thread |
| Controller separation | Business logic in controllers (`src/backend/controllers/`), not in UI widgets |
| Naming | UI-related methods: `on_<widget>_<signal>()` pattern |

```python
# Good — controller handles logic, UI just connects
class MainController:
    def start_scan(self, parameters: ScanParameters) -> None:
        """Initiate a dot grid scan with the given parameters."""
        self.scan_thread = ScanThread(parameters)
        self.scan_thread.progress_updated.connect(self._on_progress_updated)
        self.scan_thread.start()
```

---

## 4. Testing Standards

### 4.1 Test Categories

| Type | What it Tests | Tool | Required? | Minimum Coverage |
|------|--------------|------|-----------|--------------------|
| Unit | Individual functions and classes | pytest | Yes | 80% line coverage |
| Integration | Module interactions (e.g., scan → certificate) | pytest + fixtures | Yes for pipelines | Key paths covered |
| Hardware | Physical equipment verification | Manual + documented | Yes for HW tasks | Documented results |

### 4.2 Test Placement

```
tests/
├── backend_tests/
│   ├── test_scan_and_capture.py
│   ├── test_calculate_position_error.py
│   ├── test_generate_glass_certificate.py
│   ├── test_generate_encoder_error_matrix.py
│   └── test_generate_error_mapping_test.py
└── frontend_tests/
    └── test_main_window.py
```

### 4.3 Test Writing Standards

- Test file names mirror source file names: `src/.../scan_and_capture.py` → `tests/backend_tests/test_scan_and_capture.py`
- Each test function must have a docstring explaining what it tests
- Use the Arrange-Act-Assert (AAA) pattern

```python
def test_glass_certificate_output_has_correct_columns():
    """Glass certificate CSV must contain Nominal_X, Nominal_Y, Measured_X, Measured_Y, Delta_X, Delta_Y columns."""
    # Arrange
    test_log_path = Path("tests/fixtures/sample_scan_log.csv")
    test_ref_path = Path("tests/fixtures/sample_reference_locations.csv")

    # Act
    certificate = generate_glass_certificate(test_log_path, test_ref_path)

    # Assert
    expected_columns = ["Nominal_X", "Nominal_Y", "Measured_X", "Measured_Y", "Delta_X", "Delta_Y"]
    assert list(certificate.columns) == expected_columns
```

- Tests must be independent — no test depends on state from another
- Use fixtures for shared setup, not global variables

### 4.4 Hardware Test Documentation

For tasks involving physical equipment, document test results using this format:

```markdown
## Hardware Test Report
- **Date:** YYYY-MM-DD
- **Equipment:** [gantry model, camera, lens, glass scale]
- **Environment:** [temperature, cleanroom Y/N]
- **Procedure:** [step-by-step what was done]
- **Results:** [measurements, CSV file references]
- **Pass/Fail:** [against acceptance criteria]
- **Notes:** [observations, anomalies]
```

---

## 5. Secrets Management

**Secrets must never enter the repository.** This is an absolute rule.

| Method | When to Use |
|--------|-------------|
| Environment variables | Local development (`.env` file in `.gitignore`) |
| Configuration files | Machine-specific settings (`config.ini` in `.gitignore`) |

If a secret is accidentally committed:
1. **Immediately** treat the secret as compromised
2. Rotate the credential
3. Notify the team lead

---

## 6. Related Documents

| Document | Purpose |
|----------|---------|
| [TS-002 — Git Workflow](TS-002_Git-Workflow.md) | Commit messages, branch naming, PR process |
| [TS-003 — Definition of Done](TS-003_Definition-of-Done.md) | DoD checklist for code and hardware tasks |
| [Git Issues](../11_git_issues/README.md) | Issue tracking conventions |

---

## Change Log

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-04-14 | Malith | Initial version — adapted from docs_SOP/TS-001; tailored to Python/PySide6; added PBA-specific examples |
