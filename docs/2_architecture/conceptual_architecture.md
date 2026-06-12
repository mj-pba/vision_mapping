# Proposed Conceptual Architecture Description

## Architectural Style/Pattern
The system is a desktop application with a monolithic architecture. It comprises a Python backend for core logic and hardware interaction, and a PySide6 frontend for the user interface. The backend consists of several distinct processing scripts that are currently loosely coupled but are planned to be integrated more tightly with the UI (as per `FEAT-007`).

## High-Level Structure
The system is broadly divided into a Frontend (UI Layer) and a Backend (Application Logic & Hardware Interface Layer).

*   **Frontend (UI Layer):**
    *   Built with PySide6 (primarily `src/frontend/main_window.py` for UI definitions and `src/main.py` for application instantiation and main loop).
    *   Provides the graphical user interface for initiating operations (e.g., calibration, scanning, testing), displaying data (e.g., motor positions, error maps), and controlling the system.

*   **Backend (Application Logic & Hardware Interface Layer):**
    *   **UIController (`src/backend/controllers/controller.py`):** Mediates between the UI and the backend processing scripts/hardware interfaces. It translates UI actions into backend calls and relays data/status back to the UI.
    *   **Core Processing Scripts (located in `src/backend/image_processing/`):**
        *   `scan_and_capture.py`: Handles the image acquisition process, including implementing scanning routines like `scan_method_5()`.
        *   `generate_2D_glass_certificate_62207.py`: Performs glass scale calibration. It processes collected images, using the MVTEC Halcon library for sub-pixel accurate circle edge detection (identifying circle center and radius) to determine precise dot locations and generates the calibration certificate.
        *   `generate_2D_encoder_error_matrix.py`: Generates the 2D encoder error matrix using the glass scale certificate and encoder data from `Expansion_array_2D_0.csv` .
        *   `generate_2D_error_mapping_test.py`: Facilitates testing and validation of the error correction system by generating partial error maps.
        *   `generate_2D_error_mapping_test_plot.py`: Visualizes the error maps.
    *   **Hardware Interface Modules:**
        *   **Camera API Wrapper (`src/backend/bfs_cam_api/`):** Manages communication with the BFS camera using the `spinnaker-python` SDK.
        *   **Motor Controller API Wrapper (`src/backend/motor_controller/`):** Manages communication with the ACS motor controller using the `SPiiPlusPython` SDK.
    *   **Data Storage:**
        *   Primarily uses CSV files for storing calibration certificates, error maps, and test data.
        *   Images captured during scanning are temporarily stored on the filesystem.
