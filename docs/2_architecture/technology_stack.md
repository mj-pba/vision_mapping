# Technology Stack Recommendations

*   **Category:** Backend Language
    *   **Technology:** Python (Version 3.12.x as per `updated_environment.yml`)
    *   **Rationale:** Existing codebase is in Python. Rich ecosystem of libraries for scientific computing, image processing, hardware interfacing, and GUI development.

*   **Category:** Frontend Framework
    *   **Technology:** PySide6 (Qt for Python)
    *   **Rationale:** Existing UI is built with PySide6. Provides comprehensive tools for building cross-platform desktop GUIs.

*   **Category:** Key Libraries (Python)
    *   **Technology:** OpenCV (`opencv-python`)
    *   **Rationale:** Used for general image processing tasks.
    *   **Technology:** NumPy
    *   **Rationale:** Fundamental package for numerical computation, essential for handling array data from images, mathematical calculations, and data manipulation.
    *   **Technology:** Pandas
    *   **Rationale:** Used for data manipulation and analysis, particularly for reading and writing CSV files.
    *   **Technology:** Matplotlib
    *   **Rationale:** Used for generating static, animated, and interactive visualizations, such as plots of error maps.
    *   **Technology:** `spinnaker-python` (FLIR Spinnaker SDK)
    *   **Rationale:** Specific SDK for interacting with FLIR (formerly Point Grey, BFS) machine vision cameras.
    *   **Technology:** `SPiiPlusPython` (ACS Motion Control SDK)
    *   **Rationale:** Specific SDK for interacting with ACS motion controllers.
    *   **Technology:** `mvtec-halcon`
    *   **Rationale:** Used for advanced image processing tasks, specifically for sub-pixel accurate circle edge detection in the glass scale calibration process.

*   **Category:** Data Format
    *   **Technology:** CSV (Comma-Separated Values)
    *   **Rationale:** Simple, human-readable, and widely supported format used for storing calibration data, error maps, and test results. Suitable for the current scale and requirements.
    *   **Technology:** Image files (e.g., TIFF, PNG - specific format to be confirmed by `scan_and_capture.py` output)
    *   **Rationale:** Standard formats for storing images captured by the camera.

*   **Category:** Development Environment & Dependency Management
    *   **Technology:** Anaconda / Conda (implied by `updated_environment.yml` and `environment.yml`)
    *   **Rationale:** Manages Python environments and dependencies, simplifying setup, ensuring reproducibility, and handling complex binary dependencies.
    *   **Technology:** Pip (with `requirements.txt`)
    *   **Rationale:** Used alongside Conda for managing Python package dependencies, especially for packages not available in Conda channels or for specific versions.
