# Detailed Component Designs

This document provides detailed designs for the major system components identified in the conceptual architecture and system components documentation.

---

## 1. MainWindow (UI)

*   **Component Name**: `MainWindow`
*   **Location**: Instantiated in `src/main.py`, UI definition likely in `src/frontend/main_window.py` (or a .ui file loaded by it).
*   **Detailed Responsibilities**:
    *   Render the main application window and all its UI elements (tabs, buttons, input fields, display areas, menus, toolbar) as defined in `docs/3_design/ui_components.md`.
    *   Capture user interactions with UI elements (e.g., button clicks, text input, dropdown selections, file selections).
    *   Handle UI interactions for scan parameter inputs:
        *   Test type selection (e.g., "2D error map", "2D expansion").
        *   Axis selection for target definition.
        *   First and last target points for selected axis.
        *   Number of runs.
        *   Number of inspection images.
        *   Wait time between operations.
    *   Validate user inputs to a reasonable extent (e.g., check if required fields are filled, basic data type checks) before passing them to the controller.
    *   Display data received from the `UIController`, including status messages, progress updates, error messages, and visualization outputs (plots).
    *   Manage the visual state of UI elements (e.g., enabling/disabling buttons based on application state, showing/hiding contextual input fields).
    *   Invoke appropriate methods on the `UIController` in response to user actions.
*   **Interfaces/APIs Exposed (Internal Methods called by its own event handlers)**:
    *   `handle_scan_button_click()`: Collects parameters from the "Testing" tab (first target, last target, num_runs, num_images, wait_time, selected test type, selected axis) and calls `UIController.start_scan()`.
    *   `handle_select_test_combo_box_changed()`: Updates internal state and UI based on selected test type.
    *   `handle_select_test_axis_combo_box_changed()`: Updates UI for first/last target based on selected axis.
    *   `handle_first_target_line_edit_finished()`: Validates and stores the first target input.
    *   `handle_last_target_line_edit_finished()`: Validates and stores the last target input.
    *   `handle_number_of_runs_line_edit_finished()`: Validates and stores the number of runs.
    *   `handle_number_of_inspection_images_line_edit_finished()`: Validates and stores the number of inspection images.
    *   `handle_wait_time_line_edit_finished()`: Validates and stores the wait time.
    *   `update_log_display(message: str)`: Appends a message to the log viewer.
    *   `update_status_bar(message: str)`: Updates a status bar or label.
    *   `update_progress_bar(value: int)`: Sets the value of a progress bar.
    *   `display_plot(figure: matplotlib.figure.Figure)`: Renders a Matplotlib figure in an appropriate UI element.
    *   `get_input_file_path()`: Opens a file dialog and returns the selected path.
    *   `get_output_file_path()`: Opens a save file dialog and returns the selected path.
*   **Internal Logic Outline/Pseudocode**:
    *   Initialization: Load UI definition (e.g., from .ui file or code), connect signals from UI elements to slots (handler methods).
    *   Event Handling (Example: "Run Actions" button):
        ```python
        # Pseudocode for handle_run_actions_button_click
        selected_action = self.action_dropdown.currentText()
        input_file = self.file_selector.currentPath()
        # ... gather other relevant parameters based on selected_action ...

        if selected_action == "Generate Glass Scale Certificate":
            if not input_file:
                self.show_error_message("Log file is required.")
                return
            self.ui_controller.generate_glass_scale_certificate(log_file_path=input_file)
        elif selected_action == "Generate Encoder Error Matrix":
            if not input_file:
                self.show_error_message("Glass certificate file is required.")
                return
            self.ui_controller.generate_encoder_error_matrix(certificate_path=input_file)
        # ... other actions ...
        ```
*   **Dependencies**:
    *   `UIController`: To delegate actions and receive data.
    *   PySide6: For all UI rendering and event handling.
    *   Matplotlib: For displaying plots (if embedded).

---

## 2. UIController

*   **Component Name**: `UIController`
*   **Location**: `src/backend/controllers/controller.py`
*   **Detailed Responsibilities**:
    *   Mediate all communication between the `MainWindow` (UI) and the backend processing modules/scripts.
    *   Receive requests from the `MainWindow`, validate parameters if necessary, and invoke the appropriate backend script/function.
    *   Manage the execution of backend scripts, potentially in separate threads to keep the UI responsive (e.g., `ImageAcquisitionModule.start_scan_in_thread()`).
    *   Relay progress, status, errors, and results from backend scripts back to the `MainWindow` for display.
    *   Orchestrate sequences of operations if required by a feature.
    *   Maintain application state relevant to backend operations if necessary.
*   **Interfaces/APIs Exposed (Methods called by `MainWindow`)**:
    *   `start_scan(params: dict)`: Initiates `FEAT-001`. Collects scan parameters from UI (test type, targets, runs, images, wait time) and calls `ImageAcquisitionModule.start_scan_in_thread()` with these parameters, along with `hc` (Halcon communication handle), `array` (location_array), `axis_array` (axis selection), `camera_input`, and `parent_directory`.
    *   `generate_glass_scale_certificate(log_file_path: str, location_matrix_file_path: str, camera_calibration_file_path: str)`: Initiates `FEAT-002`. Calls `generate_glass_certificate.generate_2d_glass_certificate()` in `src/backend/services/generate_2D_glass_certificate_62207.py`.
    *   `generate_encoder_error_matrix(vision_log_file_file_path: str)`: Initiates `FEAT-003`. Calls `encoder_error_matrix.generate_2D_encoder_error_matrix()` in `src/backend/services/generate_2D_encoder_error_matrix.py`.
    *   (Other methods for interacting with different backend services and controllers)
*   **Dependencies**:
    *   `MainWindow`: For receiving UI events.
    *   Backend Modules/Services (see components below).
    *   PySide6.

---

## 3. CalibrationDataController

*   **Component Name**: `CalibrationDataController` (maps to `calibration_data_control` class)
*   **Location**: `src/backend/controllers/calibration_data_controller.py`
*   **Detailed Responsibilities**:
    *   Manages UI interactions and data operations related to calibration setup, particularly for glass jig dot positions.
    *   Handles input for calibration table (rows, columns).
    *   Creates and manages the position map (NumPy array) for dot locations.
    *   Triggers actions based on user selections in its specific UI section (e.g., saving/loading dot locations, image capture/processing triggers related to calibration).
    *   Interfaces with axis controllers (`axis_x_ui_controller`, `axis_y_ui_controller`, `axis_z_ui_controller`).
    *   Uses file services for loading/saving data.
*   **Key Methods (Interfaces)**:
    *   `__init__(self, ui)`: Initializes with the UI elements it controls.
    *   `select_action_combo_box_current_changed(self)`: Handles changes in the action selection dropdown.
    *   `run_action_button_clicked(self)`: Executes the selected action.
    *   `file_input_1_button_clicked(self)` (and similar for other file inputs): Handles file selection.
    *   `calibration_data_table_row_input_edit_finished(self)`: Handles edits to table rows.
    *   `calibration_data_table_column_input_edit_finished(self)`: Handles edits to table columns.
    *   `setup_calibration_data_table(self)`: Initializes the calibration data table in the UI.
    *   `create_position_map_np_array(self)`: Generates the NumPy array for dot positions.
    *   `get_x_y_value_push_button_clicked(self)`: Handles UI event to get X,Y values.
*   **Dependencies**:
    *   PySide6 (for UI elements it directly manages).
    *   `UIController` (potentially, for broader coordination or if it's a sub-controller).
    *   `axis_x_ui_controller`, `axis_y_ui_controller`, `axis_z_ui_controller`.
    *   `backend.services.file_services`.
    *   `backend.image_processing.calculation_using_halcon` (indirectly via actions).
    *   NumPy.

---

## 4. ImageAcquisitionModule

*   **Component Name**: `ImageAcquisitionModule` (maps to `scan_grid` class)
*   **Location**: `src/backend/image_processing/scan_and_capture.py`
*   **Detailed Responsibilities**:
    *   Manages various grid scanning methodologies based on UI selections (e.g., "1D error map", "2D error map", "1D expansion", "2D expansion" (`scan_method_5`), "Auto focus").
    *   Handles UI inputs for scan parameters (test type, axis, targets, runs, images, wait time) via methods like `select_test_combo_box()`, `first_target_line_edit_finished()`, etc.
    *   Controls motor movements to target locations using `move_to_location()`, which interfaces with `backend.motor_control.acs_python_modules.motor_activation`.
    *   Triggers image capture using `image_capture()`, which saves images and calls `position_error_claculation.calculate_center()` for dot detection.
    *   Implements self-centering logic in methods like `scan_method_4()` and `scan_method_5()` using `estimate_dot_center_button_clicked()`. This method:
        *   Captures a centering image.
        *   Calls `position_error_claculation.calculate_center()` to get pixel offsets.
        *   Converts pixel offsets to mm.
        *   Updates an internal `expantion_location_array` with the corrected target coordinates.
        *   Commands a move to the corrected coordinates if the error exceeds a threshold.
    *   Logs scan data (timestamps, target/actual positions, vision data, image names, temperatures) to CSV files (e.g., `Log_file_2D_expansion_X_axis.csv`) using `log_write()` or `expantion_log_write()`.
    *   Saves the final centered encoder positions to an "expansion array" CSV file (e.g., `Expansion_array_2D_{run}.csv`) using `save_expansion_array()`.
    *   Handles multi-run scans and image acquisition sequences as per user-defined parameters.
    *   Implements autofocus logic (`auto_focus()`, `fit_quadratic()`, `detect_sharpness_sobel()`) for `scan_method_8()`.
*   **Key Methods (Interfaces)**:
    *   `__init__(self, ui)`: Initializes with UI references and connects UI signals for scan parameter input.
    *   `select_test_combo_box(self)`: Handles test type selection from UI.
    *   `select_test_axis_combo_box(self)`: Handles test axis selection from UI.
    *   `first_target_line_edit_finished(self)` & `last_target_line_edit_finished(self)`: Handle target range input.
    *   `number_of_runs_line_edit_finished(self)`, `number_of_inspection_images_line_edit_finished(self)`, `wait_time_line_edit_finshed(self)`: Handle other scan parameters.
    *   `start_scan_in_thread(self, ui, hc, array, axis_array, camera_input, parent_directory)`: Starts the main `scan_start` method in a new thread.
    *   `scan_start(self, ui, hc, location_array, axis_select, camera_input, parent_directory)`: Orchestrates the selected scan method based on `self.test_type`.
    *   `scan_method_5(self)`: Implements 2D expansion scanning. Iterates through target points, performs self-centering using `estimate_dot_center_button_clicked()`, moves to corrected location, captures images with `image_capture()`, logs data with `log_write()`, and saves the `expantion_location_array` via `save_expansion_array()`.
    *   `move_to_location(self, rows, column, location_array)`: Moves motors to a specified grid location using `motor_activation.absolute_motion()` and waits for motion completion.
    *   `image_capture(self, count)`: Saves a frame from `self.capture_image` and calls `self.pe_calculation.calculate_center()` (instance of `position_error_claculation`).
    *   `estimate_dot_center_button_clicked(self, A, B, image_name)`: Captures an image, calls `pe_calculation.calculate_center()`, calculates position error in mm, updates `self.expantion_location_array` with corrected X, Y coordinates. Returns (y_position_error_mm, x_position_error_mm).
    *   `log_write(self, log_file_path, A, B)` & `expantion_log_write(self, log_file_path, A, B)`: Writes detailed scan event data to the specified log file.
    *   `save_expansion_array(self, name)`: Saves the `self.expantion_location_array` to a CSV file.
    *   `create_log_file(self, filename)`: Creates and initializes a log file with headers.
    *   `auto_focus(self, threshold, count, A, B)`: Implements the autofocus sequence.
    *   `fit_quadratic(self, x, y)`: Fits a quadratic curve for autofocus.
    *   `detect_sharpness_sobel(self, threshold, count)`: Calculates image sharpness using Sobel operator.
*   **Dependencies**:
    *   UI elements (passed in `__init__` and `start_scan_in_thread`) for parameter retrieval and feedback (though direct UI manipulation from here is minimal, mostly reading initial values).
    *   `backend.motor_control.acs_python_modules` (for `motor_activation`, `get_axis_parameters`, `read_parameters`).
    *   `backend.image_processing.calculation_using_halcon.position_error_claculation` (for dot center calculation).
    *   `backend.services.plot_in_position_expantion` (for `plot_in_position_stability`).
    *   Camera input object (`self.capture_image`).
    *   NumPy.
    *   OS, datetime, time, threading, csv modules.

---

## 5. GlassCertificateGenerationModule

*   **Component Name**: `GlassCertificateGenerationModule` (maps to `generate_glass_certificate` class)
*   **Location**: `src/backend/services/generate_2D_glass_certificate_62207.py`
*   **Detailed Responsibilities**:
    *   Generates a glass certificate CSV file (e.g., `glass_certificate.csv`).
    *   Reads nominal dot locations from a `location_matrix_file.csv` (specified by `location_matrix_file_path`).
    *   Reads measured dot locations from a `vision_log_file.csv` (specified by `vision_log_file_file_path`). These are typically the encoder coordinates the system moved to after performing vision-based self-centering on each dot.
    *   Reads camera calibration data from an `.npz` file (specified by `camara_calibration_file_path`). The current implementation loads this data, but its application to refine measured positions based on vision data appears to be a future enhancement or under review, as indicated by comments in the source code.
    *   Determines grid dimensions (start/end row/column indices, number of cycles) from the vision log data using `get_start_end_row_column_index()`.
    *   Calculates the difference (delta) between the nominal (design) positions and the measured (actual commanded encoder) positions for each dot.
    *   Saves the results, including Nominal_X, Nominal_Y, Measured_X, Measured_Y, Delta_X, and Delta_Y, to the output CSV file.
    *   Includes image processing utilities (`pre_processing`, `calculate_dot_center_location_using_halcon`, etc.) which can be used for detailed dot analysis, though the primary certificate generation relies on the already processed `vision_log_file.csv`.
*   **Key Methods (Interfaces)**:
    *   `__init__(self)`: Initializes instance variables, including those for recipe parameters.
    *   `generate_2d_glass_certificate(self, location_matrix_file_path: str, vision_log_file_file_path: str, camara_calibration_file_path: str)`: The main method that orchestrates certificate generation. This involves:
        *   Reading recipe parameters using `read_recipe_csv()`.
        *   Loading nominal locations using `open_3D_location_file()`.
        *   Loading vision log data using `open_file_pandas_convert_numpy()`.
        *   Loading camera calibration data using `open_calibration_data()`.
        *   Extracting grid dimensions using `get_start_end_row_column_index()`.
        *   Iterating through the grid points, comparing nominal X, Y with measured X, Y (from vision log's commanded positions).
        *   Calculating deltas.
        *   Preparing and saving the data to `glass_certificate.csv` (specific saving mechanism to be fully implemented within this method, potentially using a helper like `save_dot_locations_matrix` or a pandas DataFrame).
    *   `read_recipe_csv(self, parameter: str)`: Reads a specific parameter value from `active_recipe.csv`.
    *   `open_file_pandas_convert_numpy(self, file_location: str) -> np.ndarray`: Opens a CSV and converts to a NumPy array.
    *   `open_3D_location_file(self, file_location: str, number_of_axis: int) -> np.ndarray`: Opens a CSV and reshapes to a 3D NumPy array.
    *   `get_start_end_row_column_index(self, data: np.ndarray)`: Extracts grid boundary indices and cycle count from log data.
    *   `create_glass_certificate_62207_matrix(self, array_shape: tuple) -> np.ndarray`: Creates an empty NumPy array.
    *   `calculate_dot_center_location_using_halcon(self, image_path: str, dot_center_x_expected: float, dot_center_y_expected: float) -> list`: Uses Halcon to find dot center in an image.
    *   `pre_processing(self, image_path: str) -> dict`: Performs a sequence of image processing steps to find dot locations.
    *   `open_calibration_data(self, calibration_file: str)`: Loads camera calibration data.
*   **Dependencies**:
    *   NumPy, Pandas.
    *   OpenCV (`cv2`) (for image processing utilities).
    *   Halcon (`halconpy` as `ha`) (for `calculate_dot_center_location_using_halcon`).
    *   OS (for file paths).

---

## 6. EncoderErrorMatrixModule

*   **Component Name**: `EncoderErrorMatrixModule` (maps to `encoder_error_matrix` class)
*   **Location**: `src/backend/services/generate_2D_encoder_error_matrix.py`
*   **Detailed Responsibilities**:
    *   Generates a 2D encoder error matrix.
    *   Reads vision log files (e.g., `Log_file_2D_expansion_X_axis.csv`), location matrix files (e.g., `calculated_all_referance_locations.csv`), glass certificate files (e.g., `glass_certificate_2D_relative.csv`), and dot center encoder location files (e.g., `Expansion_array_2D_0.csv`). These paths are typically derived based on the directory of the main input file (vision log file).
    *   Calculates encoder errors by comparing ideal/calibrated dot positions with actual encoder positions recorded during centering.
    *   Provides functionality to save the generated error matrix as 2D CSV files (`x_error_map_2D.csv`, `y_error_map_2D.csv`).
    *   Can convert and save the error matrix into a format suitable for ACS motion controllers (`generate_ACS_errormaps`).
    *   Includes utility methods for opening 3D location files (reshaping to 3D NumPy arrays) and generic CSV/pandas DataFrame to NumPy array conversion.
    *   Contains logic to calculate camera rotation based on vision cumulative distance matrix and apply corrections.
*   **Key Methods (Interfaces)**:
    *   `__init__(self)`: Initializes the class.
    *   `generate_2D_encoder_error_matrix(self)`: Main orchestrator method. It likely calls other internal methods to:
        *   Load necessary input files (vision log, glass certificate, expansion array).
        *   Create an empty error matrix.
        *   Populate the error matrix by calculating differences between ideal and actual positions.
        *   Save the resulting X and Y error maps.
        *   (The provided script shows this method as largely a placeholder, with main logic in the script's global scope test code. In a refactored system, this method would encapsulate that logic.)
    *   `generate_ACS_errormaps(self, encoder_error_matrix)`: Converts the internal error matrix to the ACS controller format and saves it.
    *   `open_3D_location_file(self, file_location, number_of_axis)`: Loads a 2D CSV and reshapes it into a 3D NumPy array.
    *   `open_file_pandas_convert_numpy(self, file_location)`: Reads a CSV into a pandas DataFrame and converts it to a NumPy array.
    *   `create_error_matrix(self, array_shape)`: Initializes a NumPy array of zeros with the given shape.
    *   `update_matrix(self, numpy_matrix_3d, row_x_index, column_y_index, distance_x, distance_y)`: Updates specific elements in the 3D error matrix.
    *   `save_3d_matrix(self, position_np_array, file_path)`: Reshapes a 3D array to 2D and saves it as a CSV.
    *   `get_camera_rotation_matrix(self, vision_cumilative_distance_matrix)`: Calculates a rotation matrix to correct for camera angle based on vision data.
    *   `plot_relative_encoder_position_2D(self, position_np_array, title)`: (Commented out in source) Intended for plotting encoder positions.
*   **Dependencies**:
    *   NumPy, Pandas.
    *   OS, sys (for file path manipulation and system exit).
    *   Matplotlib (for plotting, though currently commented out).

---

## 7. ErrorMappingTestUtilsModule

*   **Component Name**: `ErrorMappingTestUtilsModule` (collection of functions)
*   **Location**: `src/backend/services/generate_2D_error_mapping_test.py`
*   **Detailed Responsibilities**:
    *   Provides utility functions for creating test datasets for 2D error mapping.
    *   Includes functions to remove columns/rows from arrays.
    *   Generates test data for non-calibrated camera scenarios.
*   **Key Functions (Interfaces)**:
    *   `remove_columns_and_rows(array)`
    *   `remve_columns_and_rows_encoder_dot_locations(test_distance_matrix, stop_condition_i, stop_condition_j)`
    *   `create_full_file_path(ref_file_location, file_name)`
    *   `open_3D_location_file(file_location, number_of_axis)`
    *   `open_file_pandas_convert_numpy(file_location)`
    *   `generate_non_calibrated_camera_test(error_map_axis_0_file_path, ...)`
*   **Dependencies**:
    *   NumPy, Pandas.
    *   OS (for file paths).

---

## 8. ErrorMapPlottingModule

*   **Component Name**: `ErrorMapPlottingModule` (maps to `Generate2DErrorMapPlot` class)
*   **Location**: `src/backend/services/generate_2D_error_mapping_test_plot.py`
*   **Detailed Responsibilities**:
    *   Generates plots related to 2D error maps.
    *   Reads log files containing error map test data.
    *   Uses Matplotlib for plotting.
*   **Key Methods (Interfaces)**:
    *   `__init__(self)`
    *   `generate_2D_error_map_plot(self, Log_file_2D_error_map_test_file_path)`: Main method to generate and display/save plots.
    *   `read_recipe_csv(self, parameter)`: Reads configuration.
    *   `open_3D_location_file(self, file_location, number_of_axis)`
    *   `open_file_pandas_convert_numpy(self, file_location)`
    *   `plt_x_error_map_2D(self, x_error_map_2D, x_min_int, x_max_int)`
    *   `plt_y_error_map_2D(self, y_value, y_error_value)`
*   **Dependencies**:
    *   NumPy, Pandas.
    *   Matplotlib.
    *   OS (for file paths).

---

*Related Links:*
*   [API Specifications](./api_specifications.md)
*   [Data Models](./data_models.md)
*   [Data Flows](./data_flows.md)
*   [Key Algorithms](./key_algorithms.md)
*   [Main README](../../README.md)
