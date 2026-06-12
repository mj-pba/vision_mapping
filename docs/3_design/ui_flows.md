# UI Flows for PBA Vision Mapping

This document describes the user interaction flows within the PBA Vision Mapping system, based on the defined features (renumbered) and user stories, incorporating the single "Run Actions" button concept.

## 1. Full Calibration and Correction Cycle (Corresponds to `US-001`, `US-002`, `US-003`)

This flow represents the primary use case of the system: generating and applying error corrections.

1.  **User Action:** Navigates to the "Testing" tab.
2.  **User Action:** Selects "2D expansion" from the "Select test" dropdown.
3.  **User Action:** Enters parameters: `First target`, `Last target`, `Number of runs`, `Number of Images`, `wait time`.
4.  **User Action:** Clicks the "Scan" button.
    *   **System Action:** Executes `scan_method_5()` (from `scan_and_capture.py`) (`FEAT-001`).
    *   **UI Feedback:** Displays progress (e.g., "Scanning...").
    *   **UI Feedback:** Upon completion, indicates "Log_file generated" and logs the event.

5.  **User Action:** Navigates to the "Error mapping" tab.
6.  **User Action:** In the "Import file" section, selects the "Log_file" generated in the previous step.
7.  **User Action:** From the "Select Action" dropdown, chooses "Generate Glass Scale Certificate".
8.  **User Action:** Clicks the "Run Actions" button.
    *   **System Action:** Executes `generate_2D_glass_certificate_62207.py` (`FEAT-002`).
    *   **UI Feedback:** Displays progress (e.g., "Generating certificate...").
    *   **UI Feedback:** Upon completion, displays "Glass Scale Certificate Generated: [path_to_certificate.csv]" and logs the event.

9.  **User Action:** In the "Import file" section, selects the `glass_certificate.csv` generated.
10. **User Action:** From the "Select Action" dropdown, chooses "Generate Encoder Error Matrix".
11. **User Action:** Clicks the "Run Actions" button.
    *   **System Action:** Executes `generate_2D_encoder_error_matrix.py` (`FEAT-003`).
    *   **UI Feedback:** Displays progress (e.g., "Generating X-error map...", "Generating Y-error map...").
    *   **UI Feedback:** Upon completion, displays "Encoder Error Matrices Generated: [path_to_x_error_map_2D.csv], [path_to_y_error_map_2D.csv]" and logs the event.

12. **User Action:** (Assuming `x_error_map_2D.csv` and `y_error_map_2D.csv` are implicitly used or selected if needed) From the "Select Action" dropdown, chooses "Run Correction Test & Validation".
13. **User Action (Optional):** Enters parameters for row/column removal.
14. **User Action (Optional):** Selects an "uploaded" map file.
15. **User Action:** Clicks the "Run Actions" button.
    *   **System Action:** Executes `generate_2D_error_mapping_test.py` (`FEAT-004`). This generates controller files and performs validation.
    *   **UI Feedback:** Displays progress (e.g., "Generating controller files...", "Validating corrections...").
    *   **UI Feedback:** Upon completion, displays "Controller Correction Files Generated: [paths]" and validation results. Logs the event.

## 2. Error Map Visualization (Corresponds to `US-005`)

This flow enables users to visually inspect the error maps.

1.  **User Action:** Navigates to the "Error mapping" tab.
2.  **User Action:** In the "Import file" section, selects the relevant error map CSV (e.g., `x_error_map_2D.csv`).
3.  **User Action:** From the "Select Action" dropdown, chooses "Visualize X-Error Map".
4.  **User Action:** Clicks the "Run Actions" button.
    *   **System Action:** Executes `generate_2D_error_mapping_test_plot.py` for X-error data (`FEAT-005`).
    *   **UI Feedback:** Displays the X-error map plot. Logs the event.

5.  **User Action:** In the "Import file" section, selects the relevant error map CSV (e.g., `y_error_map_2D.csv`, potentially refactored as per `FEAT-006`).
6.  **User Action:** From the "Select Action" dropdown, chooses "Visualize Y-Error Map".
7.  **User Action:** Clicks the "Run Actions" button.
    *   **System Action:** Executes `generate_2D_error_mapping_test_plot.py` for Y-error data (`FEAT-005`, `FEAT-006`).
    *   **UI Feedback:** Displays the Y-error map plot. Logs the event.

## 3. System Monitoring and Feedback (Corresponds to `US-006`, `FEAT-007 AC6`)

This is an ongoing flow, active during all other operations.

1.  **System Action:** As backend scripts execute (triggered by user actions in Flows 1 & 2):
    *   Sends status updates, progress messages, errors, and completion notifications to the UI.
2.  **UI Action:** Displays these messages in the Log Viewer/Status Area.
3.  **UI Action:** Updates progress bars accordingly.

## 4. Configuration Management (Implicit)

1.  **User Action:** Navigates to a "Settings" or "Configuration" panel (details TBD).
2.  **User Action:** Modifies parameters.
3.  **System Action:** Saves these settings.
    *   **UI Feedback:** Confirmation of settings saved.

---

*Related Links:*
*   [UI Components](./ui_components.md)
*   [Design Mappings](./design_mappings.md)
*   [Integration Points](./integration_points.md)
*   [Main README](../README.md)
