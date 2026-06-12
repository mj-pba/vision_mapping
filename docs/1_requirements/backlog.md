# Project Backlog: PBA Vision Mapping

This document lists the formal requirements for the PBA Vision Mapping project, derived from the TIA Summary and subsequent clarifications, and aligned with the `features.md` document.

## Functional and System Requirements

*   **REQ-002:** (Corresponds to `FEAT-002`) The system shall generate a glass scale certificate from the scan log file.
    *   **REQ-002.1:** The system shall allow the user to select the "Log_file" via the UI.
    *   **REQ-002.2:** The system shall process the selected "Log_file" using `generate_2D_glass_certificate_62207.py` upon user initiation from the UI.
    *   **REQ-002.3:** The system shall output a `glass_certificate.csv` file.
    *   **REQ-002.4:** The glass scale certificate generation process shall achieve a target accuracy of 100 nanometers for determining the distance between dots.

*   **REQ-003:** (Corresponds to `FEAT-003`) The system shall generate a 2D encoder error matrix using the glass scale certificate.
    *   **REQ-003.1:** The system shall allow the user to select the `glass_certificate.csv` via the UI.
    *   **REQ-003.2:** The system shall process the `glass_certificate.csv` using `generate_2D_encoder_error_matrix.py` upon user initiation from the UI.
    *   **REQ-003.3:** The system shall output `x_error_map_2D.csv` for X-axis errors.
    *   **REQ-003.4:** The system shall output `y_error_map_2D.csv` for Y-axis errors.

*   **REQ-004:** (Corresponds to `FEAT-005`) The system shall provide error correction system testing, validation, and controller file generation capabilities.
    *   **REQ-004.1:** The system shall process `x_error_map_2D.csv` and `y_error_map_2D.csv` using `generate_2D_error_mapping_test.py` upon user initiation from the UI.
    *   **REQ-004.2:** The script shall be capable of removing specified rows and columns from the input error maps to generate `x_error_map_2D_for_test.csv` (for controller).
    *   **REQ-004.3:** The script shall be capable of removing specified rows and columns from the input error maps to generate `y_error_map_2D_for_test.csv` (for controller).
    *   **REQ-004.4:** The system shall allow designation of a test CSV file as an "uploaded" map for simulated controller input via the UI.
    *   **REQ-004.5:** The system shall use the remaining (non-uploaded) part of the original error map to validate the effectiveness of applied corrections.

*   **REQ-005:** (Corresponds to `FEAT-006`) The system shall be capable of generating test plots for visualizing X-directional and Y-directional error maps.
    *   **REQ-005.1:** The system shall use `generate_2D_error_mapping_test_plot.py` for visualization.

*   **REQ-006:** (Corresponds to `FEAT-007`) The system's data saving and processing procedures for Y-directional repeatability plotting shall be refactored to ensure the data is directly usable and suitable for plotting tools.

*   **REQ-007:** (Corresponds to `FEAT-008`) The system shall integrate core operations into a PySide6 graphical user interface.
    *   **REQ-007.1:** User can initiate Dot Grid Scanning (`REQ-001`/`FEAT-001`) from the UI.
    *   **REQ-007.2:** User can initiate Glass Scale Certificate Generation (`REQ-002`/`FEAT-002`) from the UI.
    *   **REQ-007.3:** User can initiate Encoder Error Matrix Generation (`REQ-003`/`FEAT-003`) from the UI.
    *   **REQ-007.4:** User can initiate Error Correction System Testing, Validation & Controller File Generation (`REQ-004`/`FEAT-005`) from the UI.
    *   **REQ-007.5:** User can initiate Error Map Visualization (`REQ-005`/`FEAT-006`) from the UI.
    *   **REQ-007.6:** UI shall provide feedback on the status and completion of these operations.

*   **REQ-008:** The system shall have clear and comprehensive documentation detailing the entire process flow, including illustrative diagrams. (Related to `NFR-USAB-002`)

*   **REQ-009:** The system shall capture encoder errors and correct them using a vision-based system with a camera overlooking a glass scale (1mm x 1mm dot grid) as reference. (General system scope)

---

## Completed Requirements

*   **REQ-001:** (Corresponds to `FEAT-001`) The system shall enable dot grid scanning for glass scale calibration.
    *   **REQ-001.1:** The system shall allow the user to select a "2D expansion" test procedure via the UI.
    *   **REQ-001.2:** The system shall allow the user to input parameters: `First target`, `Last target`, `Number of runs`, `Number of Images`, and `wait time` via the UI.
    *   **REQ-001.3:** The system shall execute `scan_method_5()` (from `scan_and_capture.py`) upon user initiation from the UI.
    *   **REQ-001.4:** The system shall generate a "Log_file" containing raw scan data as an output of the scan.

---
*Initial REQ-001 to REQ-003, REQ-009, REQ-010, REQ-013 from the previous version have been refactored and integrated into the new structure above to align with the feature list and reduce redundancy.*
