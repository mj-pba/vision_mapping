# Key Algorithms

This document describes some of the core algorithms and complex logic used within the PBA Vision Mapping system.

## 1. Dot Center Estimation (Vision Processing)

*   **Location**: `backend.image_processing.calculation_using_halcon.position_error_claculation` (and related Halcon functions).
*   **Input**: Captured image (NumPy array or Halcon image object), camera parameters (optional, for calibrated measurements).
*   **Output**: X, Y coordinates of the dot center in the image (in pixels), or offset (dX, dY) from image center.
*   **Description**:
    1.  **Preprocessing**: Image enhancement, noise reduction (e.g., Gaussian blur, median filter).
    2.  **Segmentation**: Isolate the dot from the background. This might involve:
        *   Thresholding (e.g., Otsu's method, binary threshold).
        *   Blob detection/analysis.
        *   Edge detection (e.g., Canny, Sobel) followed by contour finding.
    3.  **Feature Extraction**: Once the dot region is identified.
        *   **Centroid Calculation**: Calculate the geometric center of the detected blob.
        *   **Circle Fitting**: If the dot is circular, fit a circle to the detected contour/points and use its center. Halcon provides robust circle fitting operators.
        *   **Gaussian Peak Fitting**: If the dot has a Gaussian-like intensity profile, a 2D Gaussian function can be fitted to the intensity values to find the peak, which corresponds to the center.
    4.  **Coordinate Transformation (Optional)**: If camera calibration data is available, transform pixel coordinates to real-world units (mm) or correct for lens distortion.
*   **Notes**: The exact Halcon operators used would depend on the specifics of `position_error_claculation`. Common Halcon operators could include `threshold`, `connection`, `select_shape`, `fit_circle_contour_xld`, `smallest_circle_xld`, `area_center_xld`.

## 2. Automated Scanning Patterns

*   **Location**: `ImageAcquisitionModule` (`src/backend/image_processing/scan_and_capture.py`), specifically methods like `scan_method_1` through `scan_method_7`.
*   **Input**: Grid definition (start/end points, step size or number of points), scan parameters (number of images, wait times, axis selection).
*   **Output**: Series of motor movements, captured images, and log data.

### 2.1. Simple Grid Scan (e.g., `scan_method_2`, `scan_method_3`)
    1.  Define a 1D or 2D array of target X,Y (and Z) coordinates based on user input.
    2.  Iterate through each coordinate in the array.
    3.  For each coordinate:
        a.  Call `move_to_location()` to command motors to the target.
        b.  Wait for motion to complete (optional: check `IN_POSITION` status).
        c.  Call `image_capture()` to acquire and save one or more images.
        d.  Call `log_write()` to record target, actual encoder position, image name, etc.

### 2.2. Grid Scan with Self-Centering (e.g., `scan_method_4`, `scan_method_5`)
    1.  Define a 1D or 2D array of nominal target X,Y coordinates (`location_array`).
    2.  Initialize `expantion_location_array` (e.g., as a copy of `location_array`). This array will store the corrected, centered positions.
    3.  Iterate through each nominal coordinate (A, B for row, column index) from user-defined `first_target_X/Y` to `last_target_X/Y`.
    4.  For each nominal coordinate:
        a.  Move to the current target position in `expantion_location_array[0,A,B]` (X) and `expantion_location_array[1,A,B]` (Y) using `move_to_location()`.
        b.  **Self-Centering (`estimate_dot_center_button_clicked(A,B,image_name)`)**:
            i.  Capture a centering image (`self.capture_image.save_frame()`).
            ii. Estimate dot center using `self.pe_calculation.calculate_center(image_path)`. This returns (pix_Y, pix_X, pix_R) from Halcon.
            iii. Retrieve `image_center_pixel_x`, `image_center_pixel_y`, and `pixel_to_mm` from recipe/config.
            iv. Calculate position error in mm:
                *   `y_position_error_mm = (pix_Y - image_center_pixel_y) * pixel_to_mm`
                *   `x_position_error_mm = (pix_X - image_center_pixel_x) * pixel_to_mm`
            v.  Get current feedback positions: `x_pos_feedback`, `y_pos_feedback` from UI/motor controller.
            vi. Calculate corrected target coordinates:
                *   `correction_value_y = float(y_pos_feedback) + y_position_error_mm`
                *   `correction_value_x = float(x_pos_feedback) - x_position_error_mm` (Note: subtraction for X based on implementation)
            vii.Update `self.expantion_location_array[0,A,B]` with `correction_value_x` and `self.expantion_location_array[1,A,B]` with `correction_value_y`.
        c.  Move to the newly corrected target position in `expantion_location_array` using `move_to_location(A,B,self.expantion_location_array)`.
        d.  Capture final image(s) at the centered position using `image_capture(count)`. This also calls `pe_calculation.calculate_center()` on the new image, storing results in `self.calculated_values`.
        e.  Log data using `log_write(log_file_path,A,B)` (or `expantion_log_write`). This logs:
            *   Timestamp, run number, image name.
            *   Original target indices (A,B).
            *   Commanded positions from `expantion_location_array` (X, Y, Z).
            *   Axis position errors (PE_X, PE_Y, PE_Z) from motor controller.
            *   Pixel values (pix_Y, pix_X, pix_R) from the `image_capture` step's `calculated_values`.
            *   Temperature readings.
        f.  Increment image counter (`count`).
        g.  Wait for `self.wait_time`.
    5.  After each run (or at the end), save the `expantion_location_array` to a CSV file (e.g., `Expansion_array_2D_{run}.csv`) using `save_expansion_array()`.

## 3. Autofocus Algorithm (Quadratic Fit & Sobel Sharpness)

*   **Location**: `ImageAcquisitionModule.auto_focus()`, `fit_quadratic()`, `detect_sharpness_sobel()` (used in `scan_method_8`).
*   **Input**: Current Z position, a sharpness threshold, image counter, target indices (A,B).
*   **Output**: Adjusted Z position in `expantion_location_array[2,A,B]`.
*   **Description**:
    1.  **Initial Sharpness Check (`detect_sharpness_sobel`)**:
        a.  Capture an image at the current Z position (`expantion_location_array[2,A,B]`).
        b.  Read the image with OpenCV, convert to grayscale.
        c.  Compute Sobel gradients in X and Y directions (`cv2.Sobel`).
        d.  Compute magnitude of gradient (`np.sqrt(sobel_x**2 + sobel_y**2)`).
        e.  Calculate variance of the Sobel magnitude (`sobel_magnitude.var()`). This is the sharpness score.
        f.  If sharpness > threshold, current Z is considered in focus, return.
    2.  **Three-Point Scan for Quadratic Fit (if initial check fails)**:
        a.  Store current Z (`z_axis_position[0]`) and its sharpness (`variance[0]`).
        b.  Move Z down by a fixed step (e.g., 0.03mm): `expantion_location_array[2,A,B] -= 0.03`. Call `move_to_location()`.
        c.  Get new Z (`z_axis_position[1]`) and its sharpness (`variance[1]`) using `detect_sharpness_sobel()`.
        d.  Move Z up by a larger step (e.g., 0.06mm from the new position, so +0.03mm from original): `expantion_location_array[2,A,B] += 0.06`. Call `move_to_location()`.
        e.  Get new Z (`z_axis_position[2]`) and its sharpness (`variance[2]`) using `detect_sharpness_sobel()`.
    3.  **Fit Quadratic Curve (`fit_quadratic(self.z_axis_position, self.variance)`)**:
        a.  Construct Vandermonde matrix `A = np.vstack([z**2, z, np.ones(len(z))]).T`.
        b.  Solve for coefficients (a, b, c) of `S = aZ^2 + bZ + c` using `np.linalg.lstsq(A, variance_scores)`.
    4.  **Find Maximum and Update Z**:
        a.  Calculate optimal Z: `predicted_max_z_position = -b / (2*a)`.
        b.  If `predicted_max_z_position` is within a plausible range of the current Z, update `expantion_location_array[2,A,B] = predicted_max_z_position`.
        c.  Move to the new optimal Z position using `move_to_location()`.
        d.  Optionally, re-calculate sharpness at the new Z.

## 4. Error Matrix Generation

*   **Location**: `EncoderErrorMatrixModule` (`src/backend/services/generate_2D_encoder_error_matrix.py`).
*   **Input**:
    *   `glass_certificate_matrix_file_path`: Ideal/calibrated dot locations (X_ideal, Y_ideal).
    *   `dot_center_encoder_location_matrix_file_path` (`Expansion_array`): Actual encoder positions (X_encoder, Y_encoder) when the system was centered on each dot.
*   **Output**: `x_error_map_2D.csv`, `y_error_map_2D.csv`.
*   **Description**:
    1.  Load the ideal dot locations from the glass certificate. This forms a grid of (X_ideal_ij, Y_ideal_ij).
    2.  Load the actual encoder readings from the expansion array. This forms a grid of (X_encoder_ij, Y_encoder_ij).
    3.  Ensure both grids are aligned (i.e., entry (i,j) in both arrays corresponds to the same physical dot).
    4.  For each dot (i,j) in the grid:
        *   `Error_X_ij = X_encoder_ij - X_ideal_ij`
        *   `Error_Y_ij = Y_encoder_ij - Y_ideal_ij`
    5.  Store these `Error_X_ij` values in the `x_error_map_2D` matrix and `Error_Y_ij` values in the `y_error_map_2D` matrix.
    6.  Save these matrices as CSV files.

## 5. Camera Rotation Correction (for Encoder Error Matrix)

*   **Location**: `EncoderErrorMatrixModule` (`src/backend/services/generate_2D_encoder_error_matrix.py`), specifically `get_camera_rotation_matrix()`.
*   **Input**: `vision_cumilative_distance_matrix` (a 3D NumPy array [axis, rows, columns] representing X and Y cumulative distances measured by the vision system). Stop conditions `self.stop_condition_i` (max rows) and `self.stop_condition_j` (max columns) are also used.
*   **Output**: `rotation_matrix` (a 3D NumPy array of the same shape as input, with X and Y coordinates corrected for camera rotation).
*   **Description**:
    1.  **Calculate Average Angle**:
        *   The current script has placeholder loops for calculating `mean_coefficients_m`. This part of the algorithm appears incomplete in the provided `generate_2D_encoder_error_matrix.py` script.
        *   Conceptually, it would iterate through data points (likely from the first row or column of the `vision_cumilative_distance_matrix`) to determine the overall rotation.
        *   An average slope (`mean_coefficients_m`) is determined.
        *   The average angle of rotation is calculated using `average_angle = np.arctan(mean_coefficients_m)`.
    2.  **Apply Rotation Matrix**:
        *   A new matrix (`rotation_matrix`) is initialized with the same shape as `vision_cumilative_distance_matrix`.
        *   The standard 2D rotation formulas are applied to each (X, Y) pair in the `vision_cumilative_distance_matrix`:
            *   `X_rotated = cos(average_angle) * X_original + sin(average_angle) * Y_original`
            *   `Y_rotated = -sin(average_angle) * X_original + cos(average_angle) * Y_original`
        *   The `rotation_matrix` is populated with these corrected X and Y coordinates.
    3.  **Grid Step Calculation (Placeholder)**:
        *   The script initializes `self.error_map_grid_step_i_direction` and `self.error_map_grid_step_j_direction` and has placeholder loops, suggesting an intent to calculate grid steps after rotation, but this logic is also incomplete.
*   **Notes**: The effectiveness of this algorithm depends on the correct implementation of the `mean_coefficients_m` calculation. The script also includes commented-out Matplotlib code to visualize the original and rotated data.

## 6. ACS Error Map Format Conversion

*   **Location**: `EncoderErrorMatrixModule` (`src/backend/services/generate_2D_encoder_error_matrix.py`), specifically `generate_ACS_errormaps()` and the conceptual `convert_to_acs_format()`.
*   **Input**:
    *   `encoder_error_matrix`: A NumPy array containing the calculated X and Y errors.
    *   (Potentially) `axis_encoder_values_x`, `axis_encoder_values_y`: Arrays representing the encoder positions at which the errors are defined.
*   **Output**: Files formatted for the ACS motion controller. The exact format is controller-specific.
*   **Description**:
    1.  The `generate_ACS_errormaps()` method in the script is largely a placeholder.
    2.  The conceptual `convert_to_acs_format()` method would take the 2D error matrix (e.g., separate X and Y error maps) and the corresponding encoder positions.
    3.  It would then reformat this data into the specific structure required by the ACS controller for its error compensation tables. This might involve:
        *   Specific header information.
        *   Defined start and end points or grid parameters.
        *   Error values arranged in a particular sequence or table format.
        *   Scaling or unit conversions if necessary.
    4.  The formatted data would be saved to one or more files.
*   **Notes**: The actual implementation details for `convert_to_acs_format` are missing in the provided script and would depend on the ACS controller's documentation for error map compensation.

## 7. Glass Certificate Generation

*   **Location**: `GlassCertificateGenerationModule` (`src/backend/services/generate_2D_glass_certificate_62207.py`).
*   **Input**:
    *   `location_matrix_file_path`: CSV file containing nominal/design dot locations (X_nom, Y_nom for each grid point). Typically `calculated_all_referance_locations.csv`.
    *   `vision_log_file_file_path`: CSV log file from a scan (e.g., `Log_file_2D_expansion_X_axis.csv`). This file contains the actual commanded encoder positions (e.g., 'Y comand position', 'X comand position') after vision-based self-centering for each dot. These are treated as the measured positions (X_meas, Y_meas).
    *   `camara_calibration_file_path`: `.npz` file containing camera calibration parameters (e.g., `camera_calibration_data.npz`). While loaded, its direct application to refine `vision_log_file` data for certificate generation is noted as a potential future step or under review in the source.
    *   `active_recipe.csv`: Contains recipe parameters like `pixel_to_mm`, `image_center_pixel_x`, `image_center_pixel_y`, `dot_pitch_in_pix`, `circle_radius`, `circle_radius_tolerance`, read by `read_recipe_csv()`.
*   **Output**: `glass_certificate.csv` (or a similarly named file, e.g., `glass_certificate_2D_relative.csv` as seen in `data_flows.md`). This CSV contains columns such as: Nominal_X, Nominal_Y, Measured_X, Measured_Y, Delta_X, Delta_Y.
*   **Description**:
    1.  **Initialization**:
        *   The `generate_glass_certificate` class is instantiated.
        *   Recipe parameters are loaded from `active_recipe.csv` via `read_recipe_csv()` and stored as instance variables.
    2.  **Load Input Data**:
        *   Nominal dot locations (X_nom, Y_nom) are loaded from `location_matrix_file_path` (e.g., using `open_3D_location_file` and then selecting relevant X, Y data).
        *   Measured dot data is loaded from `vision_log_file_file_path` (e.g., using `open_file_pandas_convert_numpy`).
        *   Camera calibration data is loaded from `camara_calibration_file_path` using `open_calibration_data()`.
    3.  **Determine Grid Dimensions**:
        *   The `get_start_end_row_column_index()` method is called with the vision log data to determine the grid's start/end row indices (Y-axis), start/end column indices (X-axis), and the number of scan cycles.
    4.  **Data Alignment and Processing Loop (Conceptual)**:
        *   The core logic iterates through each dot position defined by the grid dimensions.
        *   For each dot (identified by its row and column index):
            *   Retrieve the nominal X (`X_nom`) and Y (`Y_nom`) coordinates from the loaded location matrix.
            *   Retrieve the corresponding measured X (`X_meas`) and Y (`Y_meas`) coordinates from the vision log data. These are typically the 'X comand position' and 'Y comand position' columns for the specific dot index and run. Care must be taken to correctly map log entries to nominal grid points.
            *   **Camera Calibration Application (Placeholder/Future)**: The loaded camera calibration data (`mtx`, `dist`) could be used here if the vision log contained raw pixel offsets that needed correction before being converted to mm and applied to stage positions. The current script structure suggests this is not yet fully integrated into the main certificate flow if the log file already contains final commanded/encoder positions.
            *   Calculate deviations:
                *   `Delta_X = X_meas - X_nom`
                *   `Delta_Y = Y_meas - Y_nom`
    5.  **Output Generation**:
        *   An output data structure (e.g., a list of lists or a Pandas DataFrame) is populated with `X_nom`, `Y_nom`, `X_meas`, `Y_meas`, `Delta_X`, `Delta_Y` for all processed dots.
        *   This data structure is then saved as a CSV file (e.g., `glass_certificate.csv`). The exact method for saving (e.g., `np.savetxt`, `pandas.DataFrame.to_csv`) would be within `generate_2d_glass_certificate`.
    *   **Image Processing Sub-algorithms (available but not central to the main flow if using pre-processed logs)**:
        *   `pre_processing(image_path)`: Takes an image, binarizes it, sums rows/columns, finds peak intensity ranges (`get_peak_values_ranges`), and calculates dot centers (`get_dot_center_location`). Can also find adjacent dots (`get_adgent_dot_location`).
        *   `calculate_dot_center_location_using_halcon(image_path, ...)`: Uses Halcon metrology to find a circle's center and radius in an image, providing a precise dot location.
    *   **Note**: The comment "# this method was not correct 2025.01.08 : only laser data is used to generate the glass certificate # I need to use vision data also to generate the glass certificate" indicates an ongoing refinement of the input data source and processing logic. The description above assumes the use of vision log data as per the current script structure and file inputs.


## 8. Y-Axis Repeatability Plotting from 2D Scan Data

*   **Location**: `Generate2DErrorMapPlot.plot_y_repeatability_at_x_index` (in `src/backend/services/generate_2D_error_mapping_test_plot.py`).
*   **Input**:
    *   `pandas_df_original`: Pandas DataFrame containing the full log data, sorted by image acquisition order (e.g., by a numeric version of 'image name').
    *   `x_index_val`: The specific 'X position' index (e.g., 0, 1, 2...) for which to analyze Y-axis repeatability.
    *   `self.pixel_to_mm`: Conversion factor from pixels to millimeters.
*   **Output**: A Matplotlib plot showing Y-axis command position vs. Y-axis error (derived from 'pix_X') for the specified 'X position' index.
*   **Description**:
    1.  **Data Preparation**:
        a.  The input DataFrame is filtered to include only rows matching the specified `x_index_val`.
        b.  A 'pass_num' column is added by grouping the filtered data by 'Y position' and using `cumcount()`. This identifies the first (pass 0) and second (pass 1) time the scanner visited each (X, Y) coordinate pair during the scan sequence (assuming X scans back and forth at fixed Y levels).
    2.  **Reference Point Identification**:
        a.  Data for 'pass 0' is isolated.
        b.  This 'pass 0' data is sorted by 'Y comand position' in ascending order.
        c.  The 'pix_X' value from the first entry in this sorted 'pass 0' data (i.e., the measurement taken at the lowest 'Y comand position' for the given `x_index_val` during the initial pass) is taken as the `reference_pix_X`.
    3.  **Error Calculation**:
        a.  For 'pass 0' data:
            i.  `error_pass_0_mm = (pass_0_data['pix_X'] - reference_pix_X) * self.pixel_to_mm`.
        b.  For 'pass 1' data (if it exists):
            i.  The 'pass 1' data is sorted by 'Y comand position' in *descending* order to match the desired plotting sequence for the return scan.
            ii. `error_pass_1_mm = (pass_1_data['pix_X'] - reference_pix_X) * self.pixel_to_mm`.
    4.  **Plotting**:
        a.  A Matplotlib figure is created.
        b.  'Pass 0' data is plotted: 'Y comand position' vs. `error_pass_0_mm`.
        c.  'Pass 1' data is plotted (if available): 'Y comand position' vs. `error_pass_1_mm`.
        d.  The plot is titled and labeled appropriately. The X-axis of the plot (representing 'Y comand position') may be inverted for visualization.
*   **Purpose**: This algorithm visualizes the consistency of Y-axis measurements (derived from X-pixel values) at a fixed X-axis station as the Y-axis moves. It helps assess repeatability by comparing measurements taken during an initial scan pass with those from a return scan pass over the same Y-positions.


---

*Related Links:*
*   [Detailed Component Designs](./component_designs.md)
*   [API Specifications](./api_specifications.md)
*   [Data Models](./data_models.md)
*   [Data Flows](./data_flows.md)
*   [Main README](../../README.md)
*   [Implementation Plan](../5_implementation_plan/implementation_plan.md)
*   [User Stories](../8_context_cohesion/user_stories.md)