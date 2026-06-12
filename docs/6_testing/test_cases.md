# Test Cases: PBA Vision Mapping

This document provides detailed test cases for validating both software and hardware-integrated functionality.

---

## Software Test Cases

### TC-SW-001: Dot Center Detection Accuracy
**Scenario:** SCN-SW-001 | **Priority:** Critical

| Step | Action | Expected Result |
|:---:|:---|:---|
| 1 | Load a test image with known dot positions | Image loads without errors |
| 2 | Run `position_error_claculation()` from `calculation_using_halcon.py` | Returns dot center coordinates |
| 3 | Compare returned coordinates to known ground truth | Deviation < 0.1 pixels for center position |
| 4 | Repeat for 10 different test images | Results are consistent across all images |

**Pass Criteria:** All dot center positions within 0.1 pixel of expected values.

---

### TC-SW-002: Dot Detection Repeatability
**Scenario:** SCN-SW-001 | **Priority:** Critical

| Step | Action | Expected Result |
|:---:|:---|:---|
| 1 | Load a single test image | Image loads without errors |
| 2 | Run dot detection 50 times on the same image | Returns center coordinates each time |
| 3 | Calculate standard deviation of X and Y center | Std deviation = 0 (deterministic for same image) |

**Pass Criteria:** Zero variation for identical inputs confirms determinism (NFR-RELI-001).

---

### TC-SW-003: Glass Certificate Calculation
**Scenario:** SCN-SW-002 | **Priority:** Critical

| Step | Action | Expected Result |
|:---:|:---|:---|
| 1 | Prepare a known log file (from scan with verified data) | File readable by `generate_glass_certificate` |
| 2 | Prepare a known location matrix CSV | Contains nominal dot positions |
| 3 | Run `generate_2D_glass_certificate_62207.py` | Outputs `glass_certificate.csv` |
| 4 | Verify CSV header: Nominal_X, Nominal_Y, Measured_X, Measured_Y, Delta_X, Delta_Y | All columns present |
| 5 | Verify Delta values match manual calculation for at least 5 known dots | Deltas within ±1nm of manual calculation |

**Pass Criteria:** Output CSV is correctly formatted and Delta values match expected.

---

### TC-SW-004: Encoder Error Matrix Generation
**Scenario:** SCN-SW-002 | **Priority:** Critical

| Step | Action | Expected Result |
|:---:|:---|:---|
| 1 | Provide a known `glass_certificate.csv` | File accepted as valid input |
| 2 | Run `generate_2D_encoder_error_matrix.py` | Outputs `x_error_map_2D.csv` and `y_error_map_2D.csv` |
| 3 | Verify matrix dimensions match expected grid size | Rows × columns match expected dot grid |
| 4 | Spot-check 5 error values against manual calculation | Values match within precision |

**Pass Criteria:** Error matrices have correct dimensions and accurate values.

---

### TC-SW-005: Controller File Format Compatibility
**Scenario:** SCN-SW-002 | **Priority:** High

| Step | Action | Expected Result |
|:---:|:---|:---|
| 1 | Generate `x_error_map_2D_for_test.csv` and `y_error_map_2D_for_test.csv` | Files generated successfully |
| 2 | Verify CSV format matches ACS controller expected format | Column count, delimiter, and header match spec |
| 3 | Load files into ACS SPiiPlus (simulated or real) | No format errors |

**Pass Criteria:** Generated files are accepted by ACS controller without format errors.

---

### TC-SW-006: Error Map Plot Generation
**Scenario:** SCN-SW-003 | **Priority:** Medium

| Step | Action | Expected Result |
|:---:|:---|:---|
| 1 | Provide valid `x_error_map_2D.csv` | File accepted |
| 2 | Run `generate_2D_error_mapping_test_plot.py` for X-directional plot | Plot generated and displayed/saved |
| 3 | Verify plot axes labels and data ranges are correct | Axes match physical dimensions |
| 4 | Repeat for Y-directional error map | Y plot generated correctly |

**Pass Criteria:** Both X and Y plots render correctly with accurate data representation.

---

### TC-SW-007: UI Scan Parameter Input
**Scenario:** SCN-SW-004 | **Priority:** High

| Step | Action | Expected Result |
|:---:|:---|:---|
| 1 | Open the application | Main window displays "Testing" tab |
| 2 | Select "2D expansion" from the test dropdown | Selection registered |
| 3 | Enter First target = 0, Last target = 100 | Values accepted |
| 4 | Enter Number of runs = 1, Number of Images = 1, Wait time = 50 | Values accepted |
| 5 | Click "Scan" button | `scan_method_5()` is invoked with correct parameters |

**Pass Criteria:** All UI inputs correctly propagate to backend method call.

---

### TC-SW-008: Invalid Input Handling
**Scenario:** SCN-SW-005 | **Priority:** Medium

| Step | Action | Expected Result |
|:---:|:---|:---|
| 1 | Select a non-existent file path for log file import | Error message displayed, no crash |
| 2 | Provide a corrupted CSV file to certificate generation | Error message displayed, no crash |
| 3 | Enter negative number for First target | Input rejected or error shown |
| 4 | Enter non-numeric text in numeric field | Input rejected or error shown |

**Pass Criteria:** All invalid inputs produce user-friendly error messages without crashing.

---

## Hardware-Integrated Test Cases

### TC-HW-001: In-Position Vision Capability (TST-001)
**Scenario:** SCN-HW-001 | **Priority:** Critical

| Step | Action | Expected Result |
|:---:|:---|:---|
| 1 | Position gantry at a known dot location | Gantry is stationary |
| 2 | Capture 33 images at this location | Images saved successfully |
| 3 | Run dot detection on each image, calculate radius | 33 radius values obtained |
| 4 | Calculate 3-sigma of radius values | 3σ documented |
| 5 | Repeat at 5 different grid locations | Results consistent across locations |

**Pass Criteria:** 3-sigma of radius measurement meets precision threshold (documented).

---

### TC-HW-002: Mechanical Jitter Analysis (TST-002)
**Scenario:** SCN-HW-001 | **Priority:** Critical

| Step | Action | Expected Result |
|:---:|:---|:---|
| 1 | Position gantry at a known dot location | Gantry is stationary |
| 2 | Capture 33 images at this location | Images saved successfully |
| 3 | Run dot detection on each image, calculate center X, Y | 33 center positions obtained |
| 4 | Calculate 3-sigma of X and Y center values | 3σ documented |
| 5 | Verify within acceptable machine stability limits | Jitter within spec |

**Pass Criteria:** 3-sigma of X and Y position variation within machine stability limits.

---

### TC-HW-003: Pixel-to-mm Calibration (TST-003)
**Scenario:** SCN-HW-002 | **Priority:** Critical

| Step | Action | Expected Result |
|:---:|:---|:---|
| 1 | In cleanroom, scan a line of 150 dots using `scan_method_5()` | Scan completes with log file |
| 2 | Measure physical distance between first and last dot using laser interferometer | Physical distance recorded |
| 3 | Calculate pixel-to-mm ratio from vision vs laser data | Ratio calculated |
| 4 | Repeat 3 times | 3 ratio values obtained |
| 5 | Calculate variation between the 3 ratios | Variation < 0.1% |

**Pass Criteria:** Pixel-to-mm value stable with <0.1% variation across multiple tests.

---

### TC-HW-004: Glass Certificate Verification (TST-004)
**Scenario:** SCN-HW-003 | **Priority:** Critical

| Step | Action | Expected Result |
|:---:|:---|:---|
| 1 | Using calibrated pixel-to-mm ratio in cleanroom | Calibration data loaded |
| 2 | Run full glass certificate generation process | `glass_certificate.csv` generated |
| 3 | Repeat the process at least 3 times | 3 certificates generated |
| 4 | Compare the 3 certificates | Variation analyzed |
| 5 | Document results and consistency assessment | Report generated |

**Pass Criteria:** Variation between certificates is minimal, proving end-to-end reliability.

---

## Related Links
- [Test Strategy](./test_strategy.md)
- [Test Plan (Hardware)](./test_plan.md)
- [Test Scenarios](./test_scenarios.md)
- [Requirements](../1_requirements/requirements.md)
