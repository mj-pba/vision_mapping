# Integration Points for PBA Vision Mapping

This document outlines the key integration points between the UI, backend Python scripts, and data files within the PBA Vision Mapping system. It references the updated Feature IDs from `features.md`.

## 1. UI to Backend Script Integration

| UI Action / Component                                  | Backend Script Called                                  | Feature(s) Involved | Data Passed to Script                                     | Data Returned/Updated by Script                                                                                                |
| :----------------------------------------------------- | :----------------------------------------------------- | :------------------ | :-------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------- |
| **"Scan" Button** (Testing Tab)                        | `scan_and_capture.py` (`scan_method_5()`)              | `FEAT-001`          | Scan parameters (targets, runs, images, wait time)        | `Log_file` (raw scan data)                                                                                                     |
| **"Run Actions" Button** (Error Mapping Tab - Action: "Generate Glass Scale Certificate") | `generate_2D_glass_certificate_62207.py`               | `FEAT-002`          | Path to `Log_file`                                        | `glass_certificate.csv`                                                                                                        |
| **"Run Actions" Button** (Error Mapping Tab - Action: "Generate Encoder Error Matrix") | `generate_2D_encoder_error_matrix.py`                  | `FEAT-003`          | Path to `glass_certificate.csv`                           | `x_error_map_2D.csv`, `y_error_map_2D.csv`                                                                                     |
| **"Run Actions" Button** (Error Mapping Tab - Action: "Run Correction Test & Validation") | `generate_2D_error_mapping_test.py`                    | `FEAT-005`          | Paths to `x_error_map_2D.csv`, `y_error_map_2D.csv`, uploaded map path, row/col removal params | `x_error_map_2D_for_test.csv`, `y_error_map_2D_for_test.csv`, validation results                                               |
| **"Run Actions" Button** (Error Mapping Tab - Action: "Visualize X/Y-Error Map") | `generate_2D_error_mapping_test_plot.py`               | `FEAT-006`          | Path to relevant error map CSV (X or Y), selected action (X or Y plot) | Visual plot (displayed in UI or saved)                                                                                         |
| **Log Viewer / Status Display**                        | (Receives from all backend scripts)                    | `FEAT-008` (AC6)    | Stdout/stderr streams, custom status messages             | Text displayed in the UI log area                                                                                              |

## 2. Backend Script to Backend Script Integration (Data Handoff)

| Producing Script                             | Data File(s) Produced                                  | Consuming Script                               | Feature Chain                                |
| :------------------------------------------- | :----------------------------------------------------- | :--------------------------------------------- | :------------------------------------------- |
| `scan_and_capture.py` (`scan_method_5()`)    | `Log_file`                                             | `generate_2D_glass_certificate_62207.py`       | `FEAT-001` -> `FEAT-002`                     |
| `generate_2D_glass_certificate_62207.py`   | `glass_certificate.csv`                                | `generate_2D_encoder_error_matrix.py`          | `FEAT-002` -> `FEAT-003`                     |
| `generate_2D_encoder_error_matrix.py`      | `x_error_map_2D.csv`, `y_error_map_2D.csv`             | `generate_2D_error_mapping_test.py`            | `FEAT-003` -> `FEAT-005`                     |
| `generate_2D_encoder_error_matrix.py`      | `x_error_map_2D.csv`                                   | `generate_2D_error_mapping_test_plot.py` (X)   | `FEAT-003` -> `FEAT-006`                     |
| `generate_2D_encoder_error_matrix.py`      | `y_error_map_2D.csv` (potentially refactored by `FEAT-007`) | `generate_2D_error_mapping_test_plot.py` (Y)   | `FEAT-003` -> `FEAT-006` (via `FEAT-007`)    |
| `generate_2D_error_mapping_test.py`        | `x_error_map_2D_for_test.csv`, `y_error_map_2D_for_test.csv` | (ACS Controller - external system)             | `FEAT-005` -> External                       |

## 3. Data File Integration Points

*   **`Log_file`**: Output of `FEAT-001`, input to `FEAT-002`.
*   **`glass_certificate.csv`**: Output of `FEAT-002`, input to `FEAT-003`.
*   **`x_error_map_2D.csv` / `y_error_map_2D.csv`**: Outputs of `FEAT-003`, inputs to `FEAT-005` and `FEAT-006`.
*   **`x_error_map_2D_for_test.csv` / `y_error_map_2D_for_test.csv`**: Outputs of `FEAT-005`, intended for the ACS controller.

## 4. External System Integration

*   **ACS Controller**: Consumes `x_error_map_2D_for_test.csv` and `y_error_map_2D_for_test.csv` generated by `FEAT-005`.
    *   *Integration Mechanism:* File-based transfer (details of controller ingestion TBD).

---

*Related Links:*
*   [UI Components](./ui_components.md)
*   [UI Flows](./ui_flows.md)
*   [Design Mappings](./design_mappings.md)
*   [Main README](../README.md)
