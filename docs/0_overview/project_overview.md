# Project Overview

This document provides a comprehensive overview of the **PBA Vision Mapping** project, detailing its purpose, historical context, current state, roadmap, and scope. 

**Target Audience:** This documentation is primarily intended for **developers** working on the project to deeply understand requirements, objectives, and technical directions.

---

## 1. Project Purpose

This software, originally developed by PBA Vision Systems, is designed for a three-axis system equipped with an onboard camera. It addresses the need for constant error mapping, often due to thermal expansion or other environmental factors in production environments.

The core objective is to perform high-precision PBA Vision Mapping by leveraging advanced image processing and motor control techniques to identify and quantify geometric and thermal positional errors within the system.

## 2. Core Technology Stack

- **Vision:** Integration via specialized Camera APIs (Dahua/FLIR) combined with **Halcon** for highly accurate, sub-pixel feature detection.
- **Motion:** **ACS Motion Control** (SPiiPlus) integration allowing for synchronized, automated "Scan & Capture" workflows.
- **Reference Standard:** Utilizing zero-expansion certified master glass targets to guarantee absolute traceability and reliable reference points.

---

## 3. Historical Context & Original Specifications (Started April 2024)

Prior to vision-based solutions, accurately measuring position errors across a 3-axis system required implementing very expensive miniature 3-axis distance measurement systems (e.g., Atticube, Keyence). Additionally, to cope with thermal expansion, measuring the position error repetitively to recreate thermal compensation maps was necessary but challenging.

**The Solution Approach:**
Moving to an optical vision mapping technology with an onboard camera feed addresses these challenges. It allows the use of 0 ppm expansion glass scales for thermal error estimation. Multiple customers have built their own optical vision mapping technology; replicating and improving this capability drastically improves the capabilities of our PAB machines.

**Original Process Overview:**
The system uses a calibration master glass dot matrix grid. The software allows manual operation of X, Y, and Z axes to select three dot locations forming a perpendicular angle to establish a coordinate system. Once established, the software calculates the remaining dot locations, automating the scan function. Capturing images at each location calculates position error values used to reduce physical motion error.

---

## 4. Current Status: Phase 1 Execution & Alpha Testing

The project is currently focused on Phase 1 Execution, heavily involving the establishment of foundational scanning and calculating mechanisms.

- **Current Hardware:** We have acquired a precise **500 mm x 500 mm certified master glass scale** (upgraded from a previous 150x150 mm scale), paired with its certificate. The glass scale has a 5 mm spacing pitch with solid and annulus circular markings.
- **Current Objective:** We are currently generating a full scanning certificate map and attempting to accurately implement a 1 camera pixel to mm distance calculation (a major historical challenge). The certificate contains 2 rows and 1 column measurement with 25 mm spacing to guide this calibration.
- **Development Context:** The project is being driven full-time by a single developer. While the current environment is not thermally controlled, sub-micron accuracy is expected under certain temperature variation tolerances.

---

## 5. Phased Roadmap & Future Directions

### Phase 1: Static Mapping (Current Focus)
- **Goal:** Achieve precise 2D geometric error mapping of the system across the XY plane.
- **Activities:** Automate scanning over the 500x500mm master glass target, perform sub-pixel dot detection, calculate absolute positional errors, determine pixel-to-mm conversions accurately, and generate static compensation maps to prove the technology.

### Phase 2: Dynamic Mapping (Future Direction)
- **Goal:** Integrate thermal sensors to map positional error as a mathematical function of temperature ($E = f(x, y, T)$).
- **Status:** Hardware is ready (four PT100 and four PT1000 temperature sensors). Development begins once Phase 1 is fully validated.
- **Activities:** Correlate specific temperature gradients with spatial drift data captured via vision to establish predictive thermal models.

### Phase 3: Active Compensation (Future Direction)
- **Goal:** Shift from post-process mapping to real-time, closed-loop error correction.
- **Activities:** Inject compensation offsets dynamically into the ACS controller's servo loop during active machine operation.

---

## 6. Scope & Key Deliverables

### Included:
- Development of a software application for PBA Vision Mapping.
- Implementation of image acquisition and processing algorithms (OpenCV/Halcon).
- Integration with a three-axis motor control system (ACS SPiiPlus).
- A graphical user interface (GUI) via PySide6.
- Mechanisms for calculating position errors and enabling eventual thermal compensation.
- Python environment management (`requirements.txt`, `environment.yml`).

### Not Included:
- Design and manufacturing of the physical 3-axis motion system or camera hardware.
- Development of the motor controller firmware.
- Operating system customization beyond application-level configuration.

### Key Deliverables:
1. **PBA Vision Mapping Software:** Functional desktop app for automated mapping.
2. **Image Processing Module:** Robust capturing, processing, and error detection.
3. **Motor Control Integration:** Seamless integration with ACS SPiiPlus.
4. **User Interface (UI):** Intuitive GUI for configuring parameters and viewing results.
5. **Error Reporting and Visualization:** Tools to aid system calibration.
6. **Documentation:** Developer-focused setup guides, architecture, and references.
7. **Source Code:** Full source and configurations for reproducibility.

---

## 7. Key Architectural Layers

The software follows a layered architecture for separation of concerns:

1. **Presentation Layer** — PySide6 GUI (`src/frontend/main_window.ui`, `main_window_ui.py`)
2. **Application Layer** — Entry point (`src/main.py`) and UI controller (`src/backend/controllers/controller.py`)
3. **Domain Layer** — Motor control (`src/backend/motor_control/acs_python_modules.py`), image processing (`src/backend/image_processing/scan_and_capture.py`, `calculate_position_error.py`, `calculation_using_halcon.py`)
4. **Infrastructure Layer** — Camera API communication (`src/backend/image_processing/dahua_cam_api/`)

Full architecture details: [Architecture](../2_architecture/architecture.md)

---

## 8. Main Workflows

1. **Image Capture:** Move the stage to target positions, capture images, and save them for analysis.
2. **Error Calculation:** Process captured images to calculate position errors using Halcon and OpenCV algorithms.
3. **Compensation Map Generation:** Generate 2D error maps and controller-compatible correction files.
4. **User Interaction:** Engineers operate the system via the PySide6 GUI with real-time feedback and controls.
5. **Testing & Validation:** Pytest-based tests and hardware-integrated validation for measurement accuracy.

---

## Related Links

- [Back to Main Links](links.md)
