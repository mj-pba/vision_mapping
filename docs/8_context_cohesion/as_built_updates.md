<!-- filepath: docs/8_context_cohesion/as_built_updates.md -->
# As-Built Updates

> Add updates to DTD, ITB, and other SPCR documents to accurately reflect the implemented reality here as the project evolves.

## 2025-05-15: Initial Feature Implementation & Documentation Update

**Completed Tasks (from `task_backlog.md`):**

*   **ITB-TASK-001: Implement dot grid scanning logic and logging**
    *   **Status:** Done
    *   **As-Built Notes:** The core logic for dot grid scanning and image capture is implemented in `src/backend/image_processing/scan_and_capture.py`.
        *   The `scan_grid` class handles various scanning methods.
        *   `scan_method_5()` specifically implements 2D expansion scanning, which involves moving to target locations, performing self-centering using `estimate_dot_center_button_clicked()`, capturing images with `image_capture()`, and logging data with `log_write()`.
        *   It creates a log file (e.g., `Log_file_2D_expansion_X_axis.csv`) and saves an expansion array (e.g., `Expansion_array_2D_{run}.csv`).
        *   Dependencies: `motor_control` modules, `position_error_claculation` from `calculation_using_halcon.py`.
    *   **DTD/ITB Document Impact:**
        *   `component_designs.md`: The `ImageAcquisitionModule` section should be reviewed to ensure it accurately reflects the capabilities of `scan_and_capture.py`, particularly `scan_method_5()` and its interaction with motor control and Halcon for centering.
        *   `key_algorithms.md`: The self-centering algorithm (`estimate_dot_center_button_clicked`) and the overall 2D expansion scan pattern (`scan_method_5`) should be detailed.
        *   `data_flows.md`: Data flow for 2D expansion scanning, including input parameters, image capture, Halcon processing, and output log/array files, should be documented.
        *   `data_models.md`: The structure of the log files and the expansion array CSV should be defined.

*   **ITB-TASK-002: Develop UI for scan parameter input and scan initiation**
    *   **Status:** Done
    *   **As-Built Notes:** The `scan_and_capture.py` file includes UI connections for selecting test types, axes, target ranges, number of runs, inspection images, and wait times.
        *   Methods like `select_test_combo_box()`, `select_test_axis_combo_box()`, `first_target_line_edit_finished()`, `last_target_line_edit_finished()`, `number_of_runs_line_edit_finished()`, `number_of_inspection_images_line_edit_finished()`, and `wait_time_line_edit_finshed()` handle UI interactions and update internal parameters.
        *   The `start_scan_in_thread()` method initiates the scanning process in a separate thread to prevent UI freezing.
    *   **DTD/ITB Document Impact:**
        *   `component_designs.md`: The `MainWindow` and `UIController` (or equivalent UI handling components) sections should reflect the implemented UI elements for scan control as seen in `scan_and_capture.py`.
        *   `user_stories.md` (US-001): Acceptance criteria related to UI input for scan parameters are met by these functionalities.

**Potential DTD Updates Required:**

*   Review and update `component_designs.md` to accurately reflect the implemented `ImageAcquisitionModule` (specifically `scan_and_capture.py` and its methods like `scan_method_5`, `estimate_dot_center_button_clicked`).
*   Review and update `key_algorithms.md` with details of the self-centering and 2D expansion scan algorithms.
*   Review and update `data_flows.md` for the 2D expansion scan process.
*   Review and update `data_models.md` for the log file and expansion array structures.

---

## 2025-05-20: Glass Certificate Generation Implemented

**Completed Tasks (from `task_backlog.md`):**

*   **ITB-TASK-003: Implement glass certificate generation logic**
    *   **Status:** Done
    *   **As-Built Notes:** The logic for generating the 2D glass certificate is implemented in `src\backend\services\generate_2D_glass_certificate_62207.py`.
        *   The `generate_glass_certificate` class orchestrates the process.
        *   **Inputs**:
            *   `location_matrix_file_path`: Path to a CSV file with nominal/design dot locations (e.g., `calculated_all_referance_locations.csv`).
            *   `vision_log_file_file_path`: Path to a CSV log file from a scan (e.g., `Log_file_2D_expansion_X_axis.csv`), which contains the actual commanded encoder positions after vision-based self-centering. These are used as the measured dot positions.
            *   `camara_calibration_file_path`: Path to an `.npz` file with camera calibration data (e.g., `camera_calibration_data.npz`). This is loaded but its application for refining measurements in the certificate is currently under review/placeholder.
            *   `active_recipe.csv`: Contains various parameters like pixel-to-mm conversion, image center coordinates, dot pitch, and circle tolerances, read via `read_recipe_csv()`.
        *   **Processing Steps**:
            1.  Loads nominal dot locations, vision log data (measured/commanded positions), and camera calibration data.
            2.  Reads recipe parameters.
            3.  Determines grid dimensions (start/end row/column indices) from the vision log using `get_start_end_row_column_index()`.
            4.  For each dot, it compares the nominal (X_nom, Y_nom) with the measured (X_meas, Y_meas from vision log's commanded positions).
            5.  Calculates the deltas: Delta_X = X_meas - X_nom, Delta_Y = Y_meas - Y_nom.
        *   **Output**: A CSV file (e.g., `glass_certificate.csv` or `glass_certificate_2D_relative.csv`) containing columns for Nominal_X, Nominal_Y, Measured_X, Measured_Y, Delta_X, Delta_Y.
        *   The script also includes extensive image processing utilities (e.g., `pre_processing`, `calculate_dot_center_location_using_halcon`) for dot detection from raw images, but the main certificate generation path appears to use the pre-processed data from the vision log.
    *   **DTD/ITB Document Impact:**
        *   `component_designs.md`: The `GlassCertificateGenerationModule` section updated to reflect these implementation details.
        *   `key_algorithms.md`: The "Glass Certificate Generation" algorithm section updated with detailed steps, inputs, and outputs.
        *   `data_flows.md`: The data flow for certificate generation (FEAT-002) should align with these inputs and outputs. The output filename in the diagram (`glass_certificate_2D_relative.csv`) is consistent with one of the potential output names.
        *   `data_models.md`: The structure of `location_matrix_file.csv`, `vision_log_file.csv`, and the output `glass_certificate.csv` should be defined or reviewed for accuracy.
        *   `user_stories.md` (US-002): Acceptance criteria related to certificate generation are met.

---

## 2025-05-23: Encoder Error Matrix Generation Implemented

**Completed Tasks (from `task_backlog.md`):**

*   **ITB-TASK-004: Implement encoder error matrix generation**
    *   **Status:** Done
    *   **As-Built Notes:** The logic for generating the 2D encoder error matrix is implemented in `src\\backend\\services\\generate_2D_encoder_error_matrix.py`. This script processes [Specify Inputs, e.g., 'raw encoder data and vision system measurements'] to produce an error matrix. The output is [Specify Output format, e.g., 'a CSV file representing the error matrix and potentially an ACS format file']. Key functionalities include opening location and log files, creating and updating the error matrix, calculating camera rotation, and converting the matrix to ACS format.
    *   **DTD/ITB Document Impact:**
        *   `component_designs.md`: The `EncoderErrorMatrixModule` section needs to be updated to reflect the implementation details of `generate_2D_encoder_error_matrix.py`.
        *   `key_algorithms.md`: Algorithms for camera rotation correction and ACS format conversion should be documented.
        *   `data_flows.md`: The data flow for error matrix generation, including input data sources and output formats, needs to be detailed.
        *   `data_models.md`: The structure of the input files and the output error matrix (CSV and ACS format) should be defined.
        *   `user_stories.md` (US-003): Acceptance criteria related to encoder error matrix generation are met.

---

## 2026-04-14: SOP Adoption & Git Issue Tracking

**Completed Tasks:**

*   **DOCS-001: Adopt SOP Standards & Git Issue Tracking**
    *   **Status:** Done
    *   **As-Built Notes:**
        *   Adapted industry-standard SOPs from `docs/docs_SOP/` reference templates into project-specific documents.
        *   Created `docs/10_standards/` directory with 4 files:
            *   `README.md` — Standards index and reading order for new team members
            *   `TS-001_Coding-Standards.md` — Python 3.13 / PySide6 coding standards (adapted from docs_SOP/TS-001)
            *   `TS-002_Git-Workflow.md` — Git workflow, conventional commits, PR process (adapted from docs_SOP/TS-002)
            *   `TS-003_Definition-of-Done.md` — DoD for code, research, hardware, and docs tasks
        *   Created `docs/11_git_issues/` directory with 17 files:
            *   `README.md` — Issue naming convention, templates, and master index
            *   1 Epic issue (Phase 1 tracking)
            *   6 completed feature issues (FEAT-001 through FEAT-006) — historical records for traceability
            *   9 active/new work item issues (FEAT-007, TASK-001–003, RESEARCH-001–002, HW-001–002, DOCS-001)
        *   Added custom `HW` (Hardware) issue type prefix for physical equipment tasks
        *   Updated `AGENTS.md`:
            *   Section 3: Added `docs/10_standards/` and `docs/11_git_issues/` to project structure tree
            *   Section 7: Added Standards and Git Issues rows to documentation map
            *   Section 8: Replaced basic conventions with references to TS-001, TS-002, TS-003
            *   Section 9: Added new "SOP & Issue Tracking" section
        *   Deleted `docs/docs_SOP/` example template files after adaptation was complete
    *   **Key Decisions:**
        *   Standards designed for 2–3 person team (not simplified for solo developer)
        *   Git issues created as local `.md` files with placeholder `#NN` numbers; user will create GitHub issues manually
        *   Issue scopes: `scan`, `vision`, `motor`, `certificate`, `error-map`, `ui`, `docs`, `ci`, `halcon`, `camera`
    *   **DTD/ITB Document Impact:**
        *   `AGENTS.md`: Updated with new sections 8 and 9
        *   All future work should follow the adopted standards (TS-001, TS-002, TS-003)
        *   All future work items should have corresponding issue files in `docs/11_git_issues/`

---

## Related Links

*   [Implementation Plan](../5_implementation_plan/implementation_plan.md)
*   [Task Backlog](../5_implementation_plan/task_backlog.md)
*   [Technical Standards](../10_standards/README.md)
*   [Git Issues](../11_git_issues/README.md)
