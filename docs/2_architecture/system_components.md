# List of Major System Components & Interactions

This document outlines the major logical components of the PBA Vision Mapping system and their primary interactions.

1.  **MainWindow (UI)**
    *   **Location:** `src/main.py` (instantiation), `src/frontend/main_window.py` (UI definition)
    *   **Primary Responsibilities:**
        *   Provides the graphical user interface for all system operations.
        *   Displays system status, motor positions, camera feedback (if implemented), and results of processing tasks.
        *   Collects user inputs (e.g., scan parameters, file paths, operational triggers).
    *   **Key Interactions:**
        *   Sends user commands and parameters to the `UIController`.
        *   Receives data and status updates from the `UIController` to refresh UI elements.

2.  **UIController**
    *   **Location:** `src/backend/controllers/controller.py`
    *   **Primary Responsibilities:**
        *   Acts as an intermediary (façade/mediator) between the `MainWindow (UI)` and the backend processing logic/hardware interfaces.
        *   Translates UI events (e.g., button clicks) into calls to appropriate backend modules or hardware interfaces.
        *   Manages the overall state and flow of application operations initiated from the UI.
        *   Orchestrates sequences of operations (e.g., scan, then process).
    *   **Key Interactions:**
        *   Receives commands and data from `MainWindow (UI)`.
        *   Invokes methods in `CameraInterface` (via `ImageAcquisition Module` or directly) and `MotorControllerInterface`.
        *   Initiates and monitors the execution of core processing scripts (`ImageAcquisition`, `GlassScaleCalibration`, `EncoderErrorMatrixGeneration`, etc.).
        *   Returns results, progress, and status updates to `MainWindow (UI)`.

3.  **ImageAcquisition Module**
    *   **Script:** `src/backend/image_processing/scan_and_capture.py`
    *   **Primary Responsibilities:**
        *   Manages the process of capturing images from the camera according to defined scan patterns (e.g., `scan_method_5`).
        *   Controls motor movements via the `MotorControllerInterface` to position the camera/stage for each capture.
        *   Saves captured images to a specified (likely temporary) filesystem location.
    *   **Key Interactions:**
        *   Interfaces with the `CameraInterface` to configure the camera and trigger image captures.
        *   Interfaces with the `MotorControllerInterface` to move the stage/optics.
        *   Receives scan parameters (e.g., start/end locations, step size, grid settings) from the `UIController`.
        *   Outputs image files to the filesystem.

4.  **GlassScaleCalibration Module**
    *   **Script:** `src/backend/image_processing/generate_2D_glass_certificate_62207.py`
    *   **Primary Responsibilities:**
        *   Processes collected images of the glass scale to accurately determine the physical locations of dots.
        *   Utilizes the `HalconInterface` (or direct Halcon library calls) for sub-pixel accurate circle edge detection to find circle centers and radii.
        *   Generates the glass scale calibration certificate (e.g., `glass_scale_certificate.csv`).
    *   **Key Interactions:**
        *   Receives paths to the captured images from the `UIController` (or reads from a predefined directory structure).
        *   Interacts with the Halcon library (via `mvtec-halcon` Python package).
        *   Outputs a glass scale certificate CSV file.

5.  **EncoderErrorMatrixGeneration Module**
    *   **Script:** `src/backend/image_processing/generate_2D_encoder_error_matrix.py`
    *   **Primary Responsibilities:**
        *   Uses the generated glass scale certificate as a reference.
        *   Processes new vision-based data (likely from another scan operation similar to calibration) to identify and quantify errors originating from the encoder.
        *   Generates a 2D error matrix for both X and Y axes.
    *   **Key Interactions:**
        *   Inputs: Glass scale certificate file, paths to new image data (or processed dot locations from new images).
        *   Outputs: `x_error_map_2D.csv` and `y_error_map_2D.csv` files.

6.  **ErrorCorrectionDataOutput Module**
    *   **Script(s):** Potentially part of `generate_2D_encoder_error_matrix.py` or a dedicated script/utility function.
    *   **Primary Responsibilities:**
        *   Prepares and formats the generated error correction data (`x_error_map_2D.csv`, `y_error_map_2D.csv`) into a structure suitable for ingestion by the ACS controller (e.g., `x_error_map_2D_for_test.csv`, `y_error_map_2D_for_test.csv`).
    *   **Key Interactions:**
        *   Inputs: `x_error_map_2D.csv`, `y_error_map_2D.csv`.
        *   Outputs: Formatted CSV files for the ACS controller.

7.  **ErrorCorrectionSystemTest Module**
    *   **Script:** `src/backend/image_processing/generate_2D_error_mapping_test.py`
    *   **Primary Responsibilities:**
        *   Provides methods to test and validate the error correction capabilities.
        *   Generates partial error maps from the full error maps (e.g., by removing rows/columns).
        *   Simulates the upload of these partial maps to the controller and uses remaining data for validation.
    *   **Key Interactions:**
        *   Inputs: Full error map CSV files (`x_error_map_2D.csv`, `y_error_map_2D.csv`).
        *   Outputs: Partial test maps (e.g., `x_error_map_2D_for_test.csv`), and potentially validation reports or metrics.

8.  **ErrorMapVisualization Module**
    *   **Script:** `src/backend/image_processing/generate_2D_error_mapping_test_plot.py`
    *   **Primary Responsibilities:**
        *   Generates visual plots (e.g., heatmaps, contour plots) of the X-directional and Y-directional error maps.
        *   Aids in understanding error patterns and verifying data integrity.
    *   **Key Interactions:**
        *   Inputs: Error map CSV files.
        *   Utilizes the Matplotlib library.
        *   Outputs: Plots that can be displayed in the `MainWindow (UI)` or saved as image files.

9.  **CameraInterface (BFS Camera API Wrapper)**
    *   **Location:** `src/backend/bfs_cam_api/` (contains wrapper code)
    *   **Primary Responsibilities:**
        *   Provides a high-level, simplified interface to the `spinnaker-python` SDK for the BFS camera.
        *   Handles camera discovery, initialization, configuration (e.g., exposure, gain, resolution).
        *   Manages image acquisition triggers and retrieval of image data buffers.
        *   Handles camera de-initialization and error management.
    *   **Key Interactions:**
        *   Called by the `ImageAcquisition Module` (and potentially `UIController` for features like live camera view).
        *   Directly interacts with the `spinnaker-python` library functions.

10. **MotorControllerInterface (ACS Motor API Wrapper)**
    *   **Location:** `src/backend/motor_controller/` (contains wrapper code)
    *   **Primary Responsibilities:**
        *   Provides a high-level, simplified interface to the `SPiiPlusPython` SDK for the ACS motor controller.
        *   Handles controller connection, communication setup.
        *   Manages axis enabling/disabling, homing procedures.
        *   Executes motion commands (e.g., point-to-point moves, velocity control).
        *   Queries controller status (e.g., current position, motor state, errors).
        *   Handles controller disconnection and error management.
    *   **Key Interactions:**
        *   Called by the `UIController` and `ImageAcquisition Module` to control stage/gantry movements.
        *   Directly interacts with the `SPiiPlusPython` library functions.

11. **HalconInterface (MVTEC Halcon Wrapper/Usage)**
    *   **Location:** Integrated within `src/backend/image_processing/generate_2D_glass_certificate_62207.py` or potentially a dedicated wrapper if interactions become complex.
    *   **Primary Responsibilities:**
        *   Provides access to MVTEC Halcon's image processing functionalities.
        *   Specifically used for sub-pixel accurate circle detection (finding center coordinates and radius of dots on the glass scale).
    *   **Key Interactions:**
        *   Called by the `GlassScaleCalibration Module`.
        *   Utilizes the `mvtec-halcon` Python library.
        *   Processes image data and returns results (e.g., dot coordinates, radii).
