# API Specifications

This document outlines the key API contracts within the PBA Vision Mapping system.

## 1. UIController to Backend Modules

The `UIController` acts as the primary mediator between the `MainWindow` (UI) and the backend processing modules. The methods exposed by `UIController` effectively form an internal API layer.

Refer to `component_designs.md` for detailed method signatures of the `UIController` and the backend modules it interacts with.

## 2. Inter-Component APIs (Backend)

Internal APIs exist between various backend components. These are typically direct Python method calls. Examples include:

*   `ImageAcquisitionModule` (`scan_and_capture.py`) calling functions from `backend.motor_control.acs_python_modules`.
*   `CalibrationDataController` calling methods on `axis_x_ui_controller`, `axis_y_ui_controller`, `axis_z_ui_controller`.

These are detailed within the "Key Methods (Interfaces)" and "Dependencies" sections of each component in `component_designs.md`.

## 3. External APIs (if any)

Currently, the system does not expose external APIs for third-party consumption.

---

*Related Links:*
*   [Detailed Component Designs](./component_designs.md)
*   [Data Models](./data_models.md)
*   [Data Flows](./data_flows.md)
*   [Key Algorithms](./key_algorithms.md)
*   [Main README](../../README.md)
