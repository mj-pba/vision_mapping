# Contributing Guide

Thank you for your interest in contributing to the PBA Vision Mapping project! This guide provides information on how to set up your development environment and contribute to the project.

For a general overview of the project, please see the [main README.md](../../README.md).

## Setting Up Developer Environment

### Challenges and Limitations
ACS SPiiplus has multiple active versions (3.14.01 and 4.0) with differing Python package support.
- SPiiplus 3.14.01 supports Python 3.12.
- SPiiplus 4.0.0.0 supports Python 3.11, 3.12, and 3.13.

The FLIR camera initially had Python .whl files for Python 3.10. However, a Python 3.13 compatible .whl file has been obtained from customer support. Therefore, the project will use Python 3.13.

### Environment Creation (Windows)

1.  **Setup PowerShell Execution Policy**
    Open PowerShell as an administrator. To allow scripts for the current user, run:
    ```powershell
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
    ```
    Alternatively, for the current session only:
    ```powershell
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
    ```

2.  **Install Python 3.13**
    Download [Python 3.13.3](https://www.python.org/downloads/release/python-3133/) and install it.
    **Important:** During installation, check the box "Add Python 3.13 to PATH".
    To verify Python versions available:
    ```powershell
    py --list
    ```

3.  **Create Python Virtual Environment**
    From the **project root directory**, create the virtual environment:
    ```powershell
    py -3.13 -m venv .venv
    .\.venv\Scripts\activate
    ```
    > The `.venv` folder will be created inside the project root and is already excluded by `.gitignore`.

### Dependency Installation

(Ensure your `.venv` virtual environment is activated for the following steps)

4.  **Install ACS SPiiPlus Software & Python Package**
    Install the [SPiiPlus MMI Application Studio v4.10.1](https://www.acsmotioncontrol.com/products/spiiplus-mmi-application-studio/).
    The Python package may not be compatible with the installed software version. The correct `.whl` file is in the repository `assets/` folder.
    Then, install the Python package:
    ```powershell
    pip install assets\spiipluspython-4.10.1.0-cp313-cp313-win_amd64.whl
    ```

5.  **Install FLIR Camera (PySpin) Python Package**
    First, install dependencies for PySpin:
    ```powershell
    python.exe -m pip install --upgrade pip
    python -m ensurepip
    python -m pip install --upgrade pip numpy matplotlib Pillow
    ```
    Then, install the PySpin .whl file (replace `path\to\your\...` with the actual path to your `spinnaker_python_3.13_compatible.whl`):
    ```powershell
    python -m pip install path\to\your\spinnaker_python_3.13_compatible.whl
    
    ```
    Example:
    ```powershell
    python -m pip install assets\spinnaker_python\spinnaker_python-4.2.0.83-cp313-cp313-win_amd64.whl
    ```

6.  **Install OpenCV, SciPy, Pandas**
    ```powershell
    python -m pip install opencv-python scipy pandas
    ```

7.  **Install MVTec HALCON**
    a. Open readme file at ``https://pbasystems-my.sharepoint.com/:f:/r/personal/mj_j_pba_com_sg/Documents/Malith%20-%20R%26D/2D%20error%20mapping/halcon_documents?csf=1&web=1&e=2AvRGC`

    a. Download the "MVTec Software Manager Download" SOM, Ensure HALCON software is installed first.
    
    b. Copy licence file to SOM or 
    
    c. Install follwoing pacakages. 
        ```powershell
        python -m pip install mvtec-halcon==24050 pillow numpy
        ```

        or (in case if 24050 did not worked)

        ```powershell
        python -m pip install mvtec-halcon==24111 pillow numpy
        ```
        (Note: The README also mentioned `mvtec-halcon==24111`. Use the version appropriate for your HALCON installation.)


8.  **Install Graphviz**
    ```powershell
    python -m pip install graphviz
    ```
    Alternative:
    1.  Download and install [Graphviz](https://graphviz.gitlab.io/_pages/Download/Download_windows.html).
    2.  Add the Graphviz `bin` directory (e.g., `C:\Program Files\Graphviz\bin`) to your system PATH.


9. **Install PySide6**
    ```powershell
    pip install PySide6
    ```
10. **Compile Qt `.ui` Files to Python**
     After modifying `main_window.ui` (or any other `.ui` file) in Qt Designer, recompile it to Python using `pyside6-uic` (available once PySide6 is installed):
     ```powershell
     pyside6-uic src/frontend/main_window.ui -o src/frontend/main_window_ui.py
     ```
     Run this command from the **project root** with your virtual environment activated.

11. **Potential Qt Plugin Error Fix**
     If you encounter a "Could not load the Qt platform plugin 'windows'" error:
     This typically involves copying Qt platform plugin files (e.g., `qwindows.dll`) from a PySide6 installation path like:
     `...\Lib\site-packages\PySide6\plugins\platforms`
     to a path like:
     `...\Library\plugins\platforms` (often within an Anaconda environment if used).
     The exact paths depend on your Python distribution (e.g., standard Python install vs. Anaconda). For a standard `venv` as created above, this specific Anaconda-style path fix might not be directly applicable, but the principle is to ensure the Qt runtime can find its platform plugins. If using PySide6 installed via pip into the `py313` venv, ensure the environment is correctly activated and that PySide6 installed properly.

### Hardware-Specific Setup

**Dahua Camera (A5501M)**
1.  Install MV viewer software (link was provided in the original README).
2.  Refer to the iRAYPLE USB Area Scan Camera User Manual.
3.  Python SDK documentation is typically found in the MV viewer installation directory (e.g., `C:\Program Files\HuarayTech\MV Viewer\Documentations`).

**HALCON Library**
Refer to the specific setup documentation for the HALCON library, which might involve setting environment variables like `HALCONROOT` and `HALCONARCH`.
See also: [HALCON setup for testing](https://github.com/malithjkd/pba_vision_mapping/tree/main/src/backend/image_processing).

### Project Structure and Running the Application
For details on the project structure and how to run the main application, please refer to the [main README.md](../../README.md).

### Testing
- **Jupyter Notebook for testing:** [ACS/funtions_test.ipynb](https://github.com/malithjkd/pba_vision_mapping/blob/main/ACS/funtions_test.ipynb) (Note: This path seems to be outside the current project structure, ensure it's correct or update as needed).
- **Python Environment for Qt and OpenCV:** The same `py313` environment is used. See `requirements.txt` in the main project directory for a list of dependencies.

### Tutorials and Reference Work
1. [Tutorial Video 1](https://www.youtube.com/watch?v=Z1N9JzNax2k) - [Repo for Video](https://github.com/rutura/Qt-For-Python-PySide6-GUI-For-Beginners-The-Fundamentals-/tree/main/3.ATourOfQtWidgets)
2. [Reference Project Video](https://www.youtube.com/watch?v=Mtlr12cGc9Y)
3. [Servo Control Python App GitHub Link](https://github.com/snow-flakes1215/Servo-Control/blob/main/ACS/Python%20Demo/app.py)
4. [Qt Documentation](https://doc.qt.io/)
5. [SPiiPlus Python Library](https://www.acsmotioncontrol.com/products/host-application-libraries/)

## How to Contribute

1. Fork the repository and clone your fork.
2. Create a new branch with a descriptive name.
3. Make your changes and ensure tests pass.
4. Update documentation/context artifacts as needed (e.g., `PROJECT_CONTEXT.md`, architecture diagram).
5. Submit a pull request with a clear description.

## Coding Standards

- Follow PEP8 for Python code.
- Use clear, descriptive commit messages.
- Document new modules with docstrings and comments.

## Keeping Context Up to Date

- If you add major features or refactor architecture, please update:
  - `PROJECT_CONTEXT.md`
  - `docs/architecture.md`
  - This file (`CONTRIBUTING.md`)

## Communication

Open an issue for questions, feature requests, or reporting bugs.

---

## Related Links

- [Back to Main Links](links.md)