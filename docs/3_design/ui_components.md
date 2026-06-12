# UI Components for PBA Vision Mapping

This document outlines the key UI components of the PBA Vision Mapping system, derived from `main_window.ui` and system features.

## 1. Main Application Window

The primary container for all UI elements.

*   **Menu Bar:**
    *   `File`: Options like Open, Save, Exit.
    *   `View`: Addtional UI area for Camera image feedback rendering.
    *   `Settings`: Configuration options for calibration, processing, etc. (Yet to deverlop)
    *   `Help`: Access to documentation or about information.(Yet to deverlop)
*   **Toolbar:** Quick access buttons for common operations.

## 2. Control Panel / Operations Tab

A dedicated area, possibly a tabbed interface or a distinct panel, for initiating core system operations.

*   **Dot Grid Scanning Section (`FEAT-001`, `FEAT-007 AC1`):**
    *   `Tab`: "Testing"
    *   `Dropdown`: "Select test" (with "2D expansion" option)
    *   `Input Fields`: `First target`, `Last target`, `Number of runs`, `Number of Images`, `wait time`.
    *   `Button`: "Scan"
        *   *Purpose:* Initiates `scan_method_5()`.
    *   `Label/Status Display`: Shows scan progress.

*   **Error Mapping Tab (Shared Components):**
    *   `Tab`: "Error mapping"
    *   `Section`: "Import file"
        *   `Input Field/File Selector`: For selecting input files like "Log_file" or "glass_certificate.csv".
    *   `Dropdown`: "Select Action" (listing actions like "Generate Glass Scale Certificate", "Generate Encoder Error Matrix", "Run Correction Test & Validation", "Visualize X-Error Map", "Visualize Y-Error Map")
    *   `Button`: "Run Actions"
        *   *Purpose:* Initiates the script corresponding to the selected action in the dropdown.
    *   `Label/Status Display`: Shows progress and results of the selected action.

*   **Glass Scale Certificate Generation (`FEAT-002`, `FEAT-007 AC2`):**
    *   *UI Interaction:* User selects "Log_file" in "Import file" section, selects "Generate Glass Scale Certificate" from "Select Action" dropdown, and clicks "Run Actions".
    *   *Associated Feature ID:* `FEAT-002`

*   **Encoder Error Matrix Generation (`FEAT-003`, `FEAT-007 AC3`):**
    *   *UI Interaction:* User selects "glass_certificate.csv" in "Import file" section, selects "Generate Encoder Error Matrix" from "Select Action" dropdown, and clicks "Run Actions".
    *   *Associated Feature ID:* `FEAT-003`

*   **Error Correction System Testing, Validation & Controller File Generation (`FEAT-004`, `FEAT-007 AC4`):**
    *   *UI Interaction:* User selects relevant input files (e.g., `x_error_map_2D.csv`, `y_error_map_2D.csv`), selects "Run Correction Test & Validation" from "Select Action" dropdown, and clicks "Run Actions".
    *   `Input Fields`: For specifying parameters for removing rows/columns (contextually visible or enabled when this action is selected).
    *   `Input Field/File Selector`: For designating the "uploaded" map (contextually visible or enabled).
    *   *Associated Feature ID:* `FEAT-004`

*   **Error Map Visualization (`FEAT-005`, `FEAT-006`, `FEAT-007 AC5`):**
    *   *UI Interaction (X-Map):* User selects relevant X-error map CSV, selects "Visualize X-Error Map" from "Select Action" dropdown, and clicks "Run Actions".
    *   *UI Interaction (Y-Map):* User selects relevant Y-error map CSV, selects "Visualize Y-Error Map" from "Select Action" dropdown, and clicks "Run Actions".
    *   `Display Area`: An embedded plot area or a separate window to show the generated graphs.
    *   *Associated Feature IDs:* `FEAT-005` (visualization), `FEAT-006` (Y-data refactoring for plotting)

## 3. Status and Log Display

*   **Text Area/Log Viewer (`FEAT-007 AC6`):**
    *   *Purpose:* Displays real-time status messages, progress updates, errors, and completion notifications from the backend scripts.
*   **Progress Bar:**
    *   *Purpose:* Provides visual feedback for long-running operations.

## 4. Configuration/Settings Panel

*   **Input Fields/Selectors:**
    *   *Purpose:* Allow users to set parameters for various processes, such as file paths for scripts, default save locations, precision targets, etc.

## 5. File/Directory Selection Dialogs

*   Standard OS dialogs invoked by UI buttons/actions to select input files or specify output directories.

---

*Related Links:*
*   [UI Flows](./ui_flows.md)
*   [Design Mappings](./design_mappings.md)
*   [Integration Points](./integration_points.md)
*   [Main README](../README.md)
