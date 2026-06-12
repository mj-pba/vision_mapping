# Test Strategy: PBA Vision Mapping

## 1. Overview

This document defines the testing approach for the PBA Vision Mapping system. The system has two distinct testing domains:

1. **Software Testing** — Verifying code correctness, data processing logic, and UI behavior
2. **Hardware-Integrated Testing** — Validating the complete measurement pipeline using the physical gantry, cameras, and master glass scale

---

## 2. Testing Levels

### 2.1 Unit Testing
- **Scope:** Individual functions and classes in isolation
- **Tools:** `pytest`, unittest mocks for hardware dependencies
- **Location:** `tests/backend_tests/`, `tests/frontend_tests/`
- **Key areas:**
  - Image processing algorithms (dot detection, center calculation, error computation)
  - CSV file parsing and output formatting
  - Motor control command generation
  - Glass certificate calculation logic
  - Encoder error matrix computation

### 2.2 Integration Testing
- **Scope:** Component interactions (e.g., controller → service → file I/O)
- **Tools:** `pytest` with test fixtures, mock camera/motor interfaces
- **Key areas:**
  - Scan workflow: controller triggers scan → image capture → log file generation
  - Certificate pipeline: log file → glass certificate → error matrix → controller file
  - UI-backend integration: PySide6 signals → controller methods → data processing

### 2.3 System Testing (Hardware-Integrated)
- **Scope:** Full end-to-end measurement pipeline with real hardware
- **Tools:** Physical gantry, cameras, master glass scale, laser interferometer
- **Environment:** Temperature-controlled cleanroom (when available)
- **Key areas:**
  - Vision measurement accuracy and repeatability (TST-001, TST-002)
  - Pixel-to-mm calibration accuracy (TST-003)
  - Glass certificate generation consistency (TST-004)
  - Full 2D error mapping pipeline validation

### 2.4 Manual / Exploratory Testing
- **Scope:** UI usability, visual inspection of plots, edge cases in hardware interaction
- **Tools:** Manual testing checklists, Jupyter notebooks for data exploration
- **Key areas:**
  - GUI layout and responsiveness
  - Plot correctness and readability
  - Error handling for hardware disconnection or camera failure

---

## 3. Testing Tools & Infrastructure

| Tool | Purpose |
|:---|:---|
| `pytest` | Unit and integration test execution |
| `pytest-qt` | PySide6 GUI testing (if needed) |
| Mock objects | Simulate camera APIs, motor controllers |
| Jupyter Notebooks | Interactive data validation and visualization |
| Laser interferometer | Independent distance verification for pixel-to-mm calibration |
| Master glass scale (500×500mm) | Reference standard for dot position accuracy |

---

## 4. Test Environments

| Environment | Description | Use |
|:---|:---|:---|
| **Development** | Developer workstation with virtual environment | Unit tests, integration tests, UI testing |
| **Lab (R&D room)** | Gantry with cameras, uncontrolled temperature | Hardware integration tests, preliminary accuracy tests |
| **Cleanroom** | Temperature-controlled environment | Precision testing: pixel-to-mm calibration, glass certificate verification |

---

## 5. Test Execution

### Running Software Tests
```bash
# All tests
pytest tests/

# Backend tests only
pytest tests/backend_tests/

# Frontend tests only
pytest tests/frontend_tests/

# With verbose output
pytest tests/ -v
```

### Hardware-Integrated Tests
Hardware tests are executed manually following the procedures in [test_plan.md](./test_plan.md). Results are documented in the `logs/` directory and referenced in test reports.

---

## 6. Coverage & Known Gaps

### Current Coverage
- Backend data processing logic has unit test coverage
- Frontend UI structure has basic tests

### Known Gaps
- Edge cases in hardware error recovery (camera disconnection mid-scan)
- Full regression testing across all supported hardware configurations
- Automated GUI testing with `pytest-qt`

---

## Related Links
- [Test Plan (Hardware Tests)](./test_plan.md)
- [Test Scenarios](./test_scenarios.md)
- [Test Cases](./test_cases.md)
- [Main README](../../README.md)
