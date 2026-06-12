# Design Mappings: UI to System Logic

This document maps UI components and user flows to the underlying system features (renumbered), scripts, and data, reflecting the consolidated "Run Actions" button and updated Feature IDs.

## 1. UI Components/Actions to Features/Scripts

| UI Action / Component                                       | Corresponding Feature(s) | Backend Script(s) / Logic                                  | Key Data Input(s)                                                                 | Key Data Output(s)                                                                                     |
| :---------------------------------------------------------- | :----------------------- | :--------------------------------------------------------- | :-------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------- |
| **"Scan" Button** (Testing Tab)                             | `FEAT-001`               | `scan_and_capture.py` (`scan_method_5()`)                  | Scan parameters (targets, runs, images, wait time)                                | `Log_file`                                                                                             |
| **"Run Actions" Button** with "Generate Glass Scale Certificate" selected | `FEAT-002`               | `generate_2D_glass_certificate_62207.py`               | `Log_file`                                                                        | `glass_certificate.csv`                                                                                |
| **"Run Actions" Button** with "Generate Encoder Error Matrix" selected | `FEAT-003`               | `generate_2D_encoder_error_matrix.py`                  | `glass_certificate.csv`                                                           | `x_error_map_2D.csv`, `y_error_map_2D.csv`                                                             |
| **"Run Actions" Button** with "Run Correction Test & Validation" selected | `FEAT-004`               | `generate_2D_error_mapping_test.py`                        | `x_error_map_2D.csv`, `y_error_map_2D.csv`, uploaded map path, row/col removal params | `x_error_map_2D_for_test.csv`, `y_error_map_2D_for_test.csv`, validation results                       |
| **"Run Actions" Button** with "Visualize X-Error Map" selected | `FEAT-005`               | `generate_2D_error_mapping_test_plot.py` (for X)           | X-error data (from relevant CSV)                                                  | Plot image/display                                                                                     |
| **"Run Actions" Button** with "Visualize Y-Error Map" selected | `FEAT-005`, `FEAT-006`   | `generate_2D_error_mapping_test_plot.py` (for Y)           | Y-error data (from relevant CSV, potentially refactored by `FEAT-006`)            | Plot image/display                                                                                     |
| **Log Viewer / Status Display**                             | `FEAT-007 AC6`           | (Receives from all scripts)                                | Status messages, errors from backend                                              | Displayed text                                                                                         |
| **Configuration Panel**                                     | (Implicit, `FEAT-007`)   | (Saves/loads settings)                                     | User-defined paths, parameters                                                    | Configuration file                                                                                     |

## 2. User Stories to UI Flows and Features

| User Story | Primary UI Flow(s) Involved                     | Key Features Utilized                                     | Main UI Elements Interacted With                                                                                                                                                              |
| :--------- | :---------------------------------------------- | :-------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `US-001`   | Full Calibration and Correction Cycle           | `FEAT-001`, `FEAT-002`, `FEAT-003`, `FEAT-004`            | "Scan" button, "Select Action" dropdown ("Generate Glass Scale Certificate", "Generate Encoder Error Matrix", "Run Correction Test & Validation"), "Run Actions" button, File selectors, Log Viewer |
| `US-002`   | Full Calibration and Correction Cycle           | `FEAT-001`, `FEAT-002`, `FEAT-003`                        | "Scan" button, "Select Action" dropdown ("Generate Glass Scale Certificate", "Generate Encoder Error Matrix"), "Run Actions" button, File selectors, Log Viewer                                      |
| `US-003`   | Full Calibration and Correction Cycle           | `FEAT-004`                                                | "Select Action" dropdown ("Run Correction Test & Validation"), "Run Actions" button, Log Viewer                                                                                               |
| `US-004`   | Full Calibration and Correction Cycle (Validation part) | `FEAT-004`                                                | "Select Action" dropdown ("Run Correction Test & Validation"), "Run Actions" button, Input fields for params, File selector for uploaded map, Log Viewer                                          |
| `US-005`   | Error Map Visualization                         | `FEAT-005`, `FEAT-006`                                    | "Select Action" dropdown ("Visualize X-Error Map", "Visualize Y-Error Map"), "Run Actions" button, Plot display area                                                                            |
| `US-006`   | System Monitoring and Feedback (all flows)      | `FEAT-007` (specifically AC6 for logging)                 | Log Viewer, Progress Bars (associated with operations from `FEAT-001` to `FEAT-005`)                                                                                                             |

## 3. Data Flow through UI and System

1.  **Dot Grid Scanning:** User clicks "Scan" -> `scan_and_capture.py` (`FEAT-001`) -> `Log_file`.
    *   *UI:* Button click, parameter inputs, status updates.
2.  **Glass Scale Certificate Generation:** User selects "Log_file", action "Generate Glass Scale Certificate", clicks "Run Actions" -> `generate_2D_glass_certificate_62207.py` (`FEAT-002`) -> `glass_certificate.csv`.
    *   *UI:* File selection, dropdown selection, button click, status updates.
3.  **Encoder Error Matrix Generation:** User selects `glass_certificate.csv`, action "Generate Encoder Error Matrix", clicks "Run Actions" -> `generate_2D_encoder_error_matrix.py` (`FEAT-003`) -> `x_error_map_2D.csv`, `y_error_map_2D.csv`.
    *   *UI:* File selection, dropdown selection, button click, status updates.
4.  **Controller File Generation & Validation:** User selects inputs, action "Run Correction Test & Validation", clicks "Run Actions" -> `generate_2D_error_mapping_test.py` (`FEAT-004`) -> `x_error_map_2D_for_test.csv`, `y_error_map_2D_for_test.csv`, validation output.
    *   *UI:* File/parameter inputs, dropdown selection, button click, status/result display.
5.  **Visualization:** User selects input CSV, action "Visualize X/Y-Error Map", clicks "Run Actions" -> `generate_2D_error_mapping_test_plot.py` (`FEAT-005`, `FEAT-006`) -> Plot.
    *   *UI:* File selection, dropdown selection, button click, plot display.

---

*Related Links:*
*   [UI Components](./ui_components.md)
*   [UI Flows](./ui_flows.md)
*   [Integration Points](./integration_points.md)
*   [Main README](../README.md)
