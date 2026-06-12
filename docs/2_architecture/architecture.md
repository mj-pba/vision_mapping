# Software Architecture Overview

The software for the PBA Vision Mapping system is designed using a layered architecture to ensure separation of concerns, maintainability, and scalability. Below is an overview of the key components and their responsibilities within each layer.

For more detailed architectural documents, including conceptual diagrams, technology stack, system components, and key decisions, please refer to the other documents in this section:
- [Conceptual Architecture](./conceptual_architecture.md)
- [Technology Stack](./technology_stack.md)
- [System Components](./system_components.md)
- [Key Architectural Decisions](./key_architectural_decisions.md)

## Architectural Layers

### 1. Presentation Layer

**Frontend Module**
- **Purpose**: Manages the user interface (UI) and all user interactions.
- **Technologies**: PySide6 for the graphical user interface.
- **Key Files**:
  - `src/frontend/main_window.ui`: Qt Designer file defining the layout of the main window.
  - `src/frontend/main_window_ui.py`: Python file generated from the `.ui` file, containing the UI structure in code.

### 2. Application Layer

**Main Application**
- **Purpose**: Serves as the entry point of the application. Initializes the system, sets up the main window, and starts the application's event loop.
- **Key Files**:
  - `src/main.py`: The main script to run the application.

**UI Controller**
- **Purpose**: Acts as an intermediary between the Presentation Layer (UI) and the Domain Layer (backend logic). It handles UI events and coordinates actions with the appropriate backend services.
- **Key Files**:
  - `src/backend/controllers/controller.py`: The main UI controller that integrates and manages other specific controllers (e.g., for axes, camera operations).

### 3. Domain Layer

This layer contains the core business logic and domain-specific knowledge of the application.

**Motor Control**
- **Purpose**: Encapsulates all logic related to controlling the physical motors of the three-axis system.
- **Key Files**:
  - `src/backend/motor_control/acs_python_modules.py`: Contains Python functions and commands to interface with and control the external ACS motor controller.

**Image Processing**
- **Purpose**: Handles all tasks related to image acquisition, processing, and analysis to determine position errors.
- **Key Files**:
  - `src/backend/image_processing/scan_and_capture.py`: Implements the logic for orchestrating the scanning process and capturing images from the camera.
  - `src/backend/image_processing/calculate_position_error.py`: Contains algorithms and logic for calculating position errors based on the captured images.
  - `src/backend/image_processing/calculation_using_halcon.py`: Specific image processing calculations implemented using the MVTec HALCON library.

### 4. Infrastructure Layer

This layer provides technical capabilities that support the higher layers, such as communication with external hardware or software systems.

**Camera API**
- **Purpose**: Manages low-level communication and interaction with the Dahua camera hardware.
- **Key Files**:
  - `src/backend/image_processing/dahua_cam_api/IMVDefines.py`: Contains definitions for data structures and constants used by the Dahua camera SDK.
  - `src/backend/image_processing/dahua_cam_api/MVSDK/`: Directory containing the Software Development Kit (SDK) files for the Dahua camera.