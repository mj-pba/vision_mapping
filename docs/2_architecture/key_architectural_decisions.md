# Key Architectural Decisions & Trade-offs

This document outlines the significant architectural decisions made during the development of the PBA Vision Mapping system, the rationale behind them, and any trade-offs considered.

*   **Decision:** Adopted a monolithic desktop application architecture with a Python backend and PySide6 frontend.
    *   **Rationale:**
        *   Suitable for a specialized engineering tool where all components are tightly integrated and typically run on a single machine.
        *   Leverages Python's strengths in scientific computing, data analysis, and the availability of libraries for hardware control and GUI development.
        *   Aligns with the existing codebase and likely team familiarity.
        *   Simplifies development, deployment, and management for this type of application compared to distributed architectures.
    *   **Trade-offs Considered:**
        *   *vs. Web Application:* A web application could offer broader accessibility but would introduce significant complexity (web server, client-server communication, browser compatibility, potential security concerns for hardware control). It might also be less performant for direct, real-time hardware interaction and intensive local image processing.
        *   *vs. Microservices Architecture:* Considered overkill for the current scope and scale of the project. A monolithic approach is simpler to manage and debug for a single-purpose, expert-user tool.

*   **Decision:** Use of Python for the entire stack (backend logic, hardware interaction, UI event handling via PySide6).
    *   **Rationale:**
        *   **Future-proofing for Machine Learning:** A key driver for selecting Python is its strong ecosystem for machine learning (e.g., TensorFlow, PyTorch, scikit-learn). This decision facilitates the planned integration of ML modules for advanced data analysis, pattern recognition, or predictive capabilities without requiring a shift in the primary development language.
        *   **Rich Library Ecosystem:** Access to a vast collection of mature libraries for scientific computing (NumPy, SciPy), image processing (OpenCV, scikit-image), data manipulation (Pandas), plotting (Matplotlib), and direct hardware control (specific SDKs like `spinnaker-python`, `SPiiPlusPython`).
        *   **Development Speed & Simplicity:** Python's syntax and dynamic typing can lead to faster development cycles for certain types of applications. Using a single language across the stack reduces context switching and simplifies the development toolchain.
    *   **Trade-offs Considered:**
        *   *vs. Higher Performance Languages (e.g., C++, C#):* Languages like C++ or C# might offer better raw execution speed for computationally intensive tasks. However, the development complexity would increase. Python's performance is often sufficient, especially when critical sections leverage optimized C/C++ libraries (like NumPy or OpenCV internals). The ease of ML integration and library availability in Python was deemed to outweigh potential raw performance differences for non-real-time critical parts.
        *   *vs. Different Language for Frontend (e.g., JavaScript with Electron, or C++ with Qt directly):* While options like Electron could offer more web-centric UI possibilities, and direct C++/Qt could offer maximum performance, PySide6 provides a good balance, allowing Python to control the UI logic seamlessly and reducing multi-language project complexity.

*   **Decision:** Employing CSV files for primary data storage (calibration certificates, error maps).
    *   **Rationale:**
        *   **Simplicity & Human Readability:** CSV is a straightforward, text-based format that is easy for humans to inspect, understand, and debug.
        *   **Ease of Use with Python:** Excellent support in Python via the `csv` module and especially the Pandas library for parsing and manipulation.
        *   **Sufficiency for Current Needs:** Adequate for the current data complexity, volume, and relational structure. Data is typically processed in batches by scripts.
    *   **Trade-offs Considered:**
        *   *vs. Relational Databases (e.g., SQLite, PostgreSQL):* Would introduce overhead (database setup, schema management, ORM or SQL query language). Not deemed necessary given that data relationships are relatively simple and transactional integrity requirements are managed within the scope of individual script executions.
        *   *vs. NoSQL Databases (e.g., MongoDB):* Could offer flexibility but also adds complexity. The structured nature of the data (grids, tables) fits well with CSV.
        *   *vs. Binary Formats (e.g., HDF5, Apache Parquet, Feather):* These could offer better performance and storage efficiency for very large datasets or complex data types. However, they reduce human readability and add dependencies. CSV is considered a good baseline, and these could be adopted later if performance with CSV becomes a bottleneck.

*   **Decision:** Direct hardware control via Python SDKs (`spinnaker-python` for BFS cameras, `SPiiPlusPython` for ACS motor controllers).
    *   **Rationale:**
        *   **Tight Integration:** Allows for close coupling of hardware control logic with the application's core processing tasks.
        *   **Convenience:** Python wrappers provided by hardware vendors offer a convenient and Pythonic way to access native SDK functionalities without needing to write C/C++ bindings from scratch.
        *   **Simplified Architecture:** Avoids the need for an intermediate control layer or server, which would add complexity to a dedicated desktop application.
    *   **Trade-offs Considered:**
        *   *vs. Intermediate Control Layer/Server (e.g., OPC-UA, custom RPC):* Could decouple the main application from direct hardware dependencies, potentially improving modularity or allowing remote control. However, this adds significant development and deployment complexity not justified for the current application type.

*   **Decision:** Use of MVTEC Halcon for sub-pixel accurate circle detection in glass scale calibration.
    *   **Rationale:**
        *   **High Precision Requirement:** The task of accurately locating dot centers on the glass scale, especially when edges might be blurry or imperfectly defined, requires specialized and robust image processing algorithms to achieve sub-pixel accuracy.
        *   **Proven Industrial Solution:** Halcon is a well-established commercial library known for its powerful and precise algorithms in industrial machine vision, including metrology.
        *   **Specific Algorithm Suitability:** Halcon's circle detection algorithms are likely more optimized and robust for this specific challenge than general-purpose algorithms in some open-source libraries.
    *   **Trade-offs Considered:**
        *   *vs. OpenCV or other open-source alternatives:* While OpenCV and other libraries offer circle detection, Halcon's specialized algorithms were chosen for their superior accuracy and robustness in the context of potentially challenging image conditions (e.g., non-ideal illumination, edge blur). The potential gain in measurement precision was deemed to justify the use of a commercial library (including licensing costs and an additional dependency).

*   **Decision:** Primarily sequential execution flow for core processing tasks (e.g., scan, then calibrate, then generate error map).
    *   **Rationale:**
        *   **Data Dependencies:** The workflow is inherently sequential due to strong data dependencies between steps (e.g., calibration requires scanned images; error map generation requires a calibration certificate).
        *   **User-Driven Process:** The system is an engineering tool where users often initiate these steps distinctly and review intermediate results.
        *   **Simplified Initial Development:** Focusing on a clear, step-by-step process simplifies the logic and debugging during initial development.
    *   **Trade-offs Considered (and future evolution):**
        *   *vs. More Automated/Pipelined Processing with Parallelism:* While the high-level sequence is fixed, future enhancements (especially as part of `FEAT-007` - UI Integration) could introduce more automation in transitioning between steps and potentially parallelize sub-tasks within a step if feasible (e.g., processing multiple images in parallel if hardware/algorithm allows). However, the core inter-step dependency remains sequential.

*   **Constraint:** Requirement to interface with existing ACS motor controllers and BFS cameras.
    *   **Impact:** This directly led to the selection of `SPiiPlusPython` and `spinnaker-python` SDKs, respectively, as they are the vendor-provided or standard libraries for controlling this specific hardware from Python.
