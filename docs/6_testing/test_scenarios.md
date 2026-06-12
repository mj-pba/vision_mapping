# Test Scenarios: PBA Vision Mapping

This document defines high-level test scenarios derived from features and user stories. Each scenario groups related test cases that validate a specific capability.

---

## Software Test Scenarios

### SCN-SW-001: Dot Detection Accuracy
**Related:** FEAT-001, FEAT-002
**Description:** Verify that the image processing pipeline correctly detects dot centers from captured images with sub-pixel accuracy.
- Dot center calculation matches expected values for known test images
- Halcon XLD contour detection produces consistent results across repeated runs
- Edge cases: partially visible dots, dust/debris on glass, varying lighting conditions

### SCN-SW-002: CSV File Processing Pipeline
**Related:** FEAT-002, FEAT-003, FEAT-004
**Description:** Verify that the chain of CSV file processing (log file → glass certificate → error matrix → controller file) produces correct outputs.
- Log file parser correctly extracts encoder positions and dot measurements
- Glass certificate calculations match expected delta values for known inputs
- Error matrix generation produces correct X and Y error maps
- Controller file format is ACS-compatible

### SCN-SW-003: Error Map Visualization
**Related:** FEAT-005, FEAT-006
**Description:** Verify that error map plots are generated correctly and accurately represent the underlying data.
- X-directional plots render without errors
- Y-directional plots render correctly after data refactoring
- Plot axes, labels, and scales are correct

### SCN-SW-004: UI Parameter Binding
**Related:** FEAT-001, FEAT-007, US-001, US-007
**Description:** Verify that UI input fields correctly bind to backend processing parameters.
- Test dropdown selections propagate to scan method selection
- Numeric input fields correctly parse and validate user input
- "Scan" button triggers the correct backend method with correct parameters
- Progress feedback updates during long operations

### SCN-SW-005: Error Handling & Edge Cases
**Related:** NFR-RELI-001
**Description:** Verify the system handles error conditions gracefully.
- Missing or corrupted input files produce clear error messages
- Camera disconnection during scan is handled (no crash)
- Motor controller communication timeout is handled
- Invalid user inputs (negative numbers, non-numeric text) are rejected

---

## Hardware-Integrated Test Scenarios

### SCN-HW-001: Vision System Repeatability
**Related:** TST-001, TST-002
**Description:** Verify that the vision system produces repeatable measurements when the gantry is stationary.
- Dot radius measurements are consistent across 100+ captures at a single location
- Dot center position (X, Y) measurements are stable (low jitter)
- Results are consistent across at least 5 different grid locations

### SCN-HW-002: Pixel-to-mm Calibration Accuracy
**Related:** TST-003
**Description:** Verify that the pixel-to-mm conversion is accurate and stable.
- Vision-measured distances match laser interferometer measurements
- Calibration is repeatable with <0.1% variation across multiple tests
- Calibration holds across the full 500×500 mm scan area

### SCN-HW-003: Glass Certificate Generation Consistency
**Related:** TST-004
**Description:** Verify that the glass certificate generation process is repeatable in a controlled environment.
- Multiple certificate generations produce consistent results
- Variation between certificates is within acceptable limits
- Results are documented and traceable

### SCN-HW-004: Full 2D Error Mapping Pipeline
**Related:** FEAT-001 through FEAT-005
**Description:** Verify the complete pipeline from scan to controller correction file.
- Complete a full scan of the glass scale
- Generate glass certificate from scan data
- Generate encoder error matrices (X and Y)
- Generate controller correction files
- Validate corrections reduce error in subsequent test scans

---

## Related Links
- [Test Strategy](./test_strategy.md)
- [Test Plan (Hardware)](./test_plan.md)
- [Test Cases](./test_cases.md)
- [Requirements](../1_requirements/requirements.md)
