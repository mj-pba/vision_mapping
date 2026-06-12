# TIA Summary: 2025_05_27 Meeting - PBA Vision Mapping Project

## A. Structured Meeting Notes/Summary:

*   **Key discussion points and topics:**
    *   The meeting focused on the "PBA Vision Mapping Project."
    *   The core requirement is to capture errors from an encoder and correct them using a vision-based system.
    *   Errors are expected due to manufacturing defects in the encoder.
    *   The correction method involves a camera overlooking a glass scale with a 1mm x 1mm dot grid.
    *   A glass scale certificate generation mechanism is used to determine dot locations accurately (target accuracy 100nm).
    *   Scanning of the grid for image collection (specifically the "Expansion, 2D expansion" scan procedure, referring to `scan_method_5()`) is performed by `C:\\Users\\malit\\OneDrive\\Documents\\GitHub\\pba_vision_mapping\\src\\backend\\image_processing\\scan_and_capture.py`.
    *   A service named `C:\\Users\\malit\\OneDrive\\Documents\\GitHub\\pba_vision_mapping\\src\\backend\\services\\generate_2D_glass_certificate_62207.py` processes captured images to generate the certificate.
    *   The generated glass certificate is then used by `C:\\Users\\malit\\OneDrive\\Documents\\GitHub\\pba_vision_mapping\\src\\backend\\services\\generate_2D_encoder_error_matrix.py` to create an error matrix based on vision values.
    *   The system testing involves feeding back error values to the controller, using data from CSV files (`x_error_map_2D_for_test.csv`, `y_error_map_2D_for_test.csv`) to derive the necessary input format (direct buffer creation by the software is not currently required).
    *   `C:\\Users\\malit\\OneDrive\\Documents\\GitHub\\pba_vision_mapping\\src\\backend\\services\\generate_2D_encoder_error_matrix.py` produces `x_error_map_2D.csv` and `y_error_map_2D.csv` for updating the ACS controller.
    *   Due to limitations in testing (related to hardware calibration like camera calibration, which is not yet implemented and considered out of scope for the current software focus), another set of files is created by `C:\\Users\\malit\\OneDrive\\Documents\\GitHub\\pba_vision_mapping\\src\\backend\\services\\generate_2D_error_mapping_test.py`. This script takes existing error maps .csv files ,`x_error_map_2D.csv` and `y_error_map_2D.csv` removes some rows/columns to create test versions (`x_error_map_2D_for_test.csv`, `y_error_map_2D_for_test.csv`), uploads a partial map to the controller, and uses the remaining part for testing.
    *   Currently, the focus is on generating a test plot using `C:\\Users\\malit\\OneDrive\\Documents\\GitHub\\pba_vision_mapping\\src\\backend\\services\\generate_2D_error_mapping_test_plot.py`.
    *   A challenge exists in plotting the Y-directional error map due to the data saving format, requiring refactoring.
*   **Decisions made:** None explicitly stated as decisions, but processes and file generation paths were described as established.
*   **Action items identified:**
    *   Refactor the data saving/processing for Y-directional repeatability plotting.
    *   Generate a process flow and diagrams based on the transcript.
*   **Main outcomes or conclusions of the meeting:** The meeting served to outline the current process flow for 2D error mapping, certificate generation, error matrix creation, testing methodology, and current challenges, particularly with Y-directional plotting.

## B. Initial Project Overview:

The project, "PBA Vision Mapping," aims to develop a system that identifies and corrects errors originating from encoders, likely due to manufacturing defects. This is achieved by using a vision system with a camera that observes a glass scale marked with a precise dot grid. The system involves processes for calibrating this glass scale (certificate generation), capturing images, processing these images to determine errors, and then feeding these error corrections back to a controller. A significant part of the current work involves testing the accuracy of this error correction mechanism and generating visual plots of the error maps, with a specific challenge in handling Y-directional data for plotting.

## C. Preliminary Problem Statement:

The primary problem is the presence of inaccuracies in encoders due to manufacturing defects. These inaccuracies need to be measured and corrected to ensure precise system operation. A secondary problem is the current difficulty in plotting Y-directional error data due to the way it's saved, which hinders testing and validation.

## D. List of High-Level Goals and Business Objectives:

*   Accurately capture and quantify errors from encoders.
*   Correct encoder errors using a vision-based system.
*   Achieve high accuracy in error measurement (e.g., 100nm for dot distance on glass scale).
*   Develop a robust testing methodology to validate the error correction system.
*   Improve the process for visualizing and analyzing error data, particularly for Y-directional errors.

## E. Identified Stakeholders:

*   The speaker (likely an engineer or developer working on the system).
*   Users of the system who rely on accurate encoder readings.
*   The team/company developing this 2D error mapping technology.

## F. List of Raw User Needs/Pain Points:

*   "The requirement is. Capture the Eras, occurred occurred. From the encoder and correct it Correct it using. Vision based correction system the errors, we Expecting due to the manufacturing defect from the encoder." (Need to correct manufacturing-induced encoder errors).
*   "The location of the dot also, we also don't know. So so we created class scale certificate generation mechanism." (Need to accurately know the positions on the reference scale).
*   "but we have a certain limitations of doing the doing and testing the era." (Need a better way to test the error correction).
*   "The challenge is X directional. We can simply generate the drama but the y directional plot. We have to select the correct values because The way I save the data in the CSC file when I do the Test again. The way I saved the data is not suitable to not directly can use to plot the y directional. Repeatability. So I need to refactor it." (Pain point: current data format for Y-axis makes plotting difficult and requires refactoring).
*   "So we use this data to use, please use this transcript, the meeting node, to generate the process flow for me. And the few diagrams." (Need for clear documentation of the process flow).

## G. Clarifying Questions & Answers:

1.  **What is "Expansion, 2D expansion" referring to in the context of the scan procedure (`scan_procedure, Related to Expansion, 2D expansion`)?**
    *   **Answer:** This refers to `scan_method_5()` in the `C:\Users\malit\OneDrive\Documents\GitHub\pba_vision_mapping\src\backend\image_processing\scan_and_capture.py` file.

2.  **Could you elaborate on the "certain limitations of doing and testing the era" that led to creating the `2D I generate 2T array map_test_test.py` script and the partial map testing approach?**
    *   **Answer:** The project involves physical components like linear motors and cameras that require calibration for accurate distance measurement. Currently, camera calibration is not performed. The software development, for now, does not need to focus on these hardware calibration aspects.

3.  **What specific format is the "buffer format" used to feed errors back to the controller?**
    *   **Answer:** The system can create the necessary input for the ACS controller from the `x_error_map_2D_for_test.csv` and `y_error_map_2D_for_test.csv` files. Direct creation of a specific "buffer format" by the software is not a current requirement.

4.  **Who is "Sasi" in "Sasi backend Services.Generate 2D array map test plot.p Wi-Fi"? Is this a person, a module, or a typo?**
    *   **Answer:** This was a typo in the transcript. The correct file is `C:\Users\malit\OneDrive\Documents\GitHub\pba_vision_mapping\src\backend\services\generate_2D_error_mapping_test_plot.py`.

5.  **The transcript mentions `X error map 2D CV.CSV` and `Y error map 2D CSV.CSV`. Later it mentions `x axis map, X error, map, 2D 4test.csv5` and `X Y error map. 2d4 test. Dot CSV file`. Is the "CV" in the first set a typo for "CSV"? Is the "X Y" in the second Y-axis file a typo and should it be "Y error map"?**
    *   **Answer:** Yes, these were typos. The correct filenames are `x_error_map_2D.csv`, `y_error_map_2D.csv`, `x_error_map_2D_for_test.csv`, and `y_error_map_2D_for_test.csv` (as reflected in the updated summary).

6.  **What is the "ACS controller" being referred to? (e.g., manufacturer, model if relevant).**
    *   **Answer:** This level of detail about the ACS controller is not necessary for the current software development focus.

7.  **The transcript mentions "SRC back end. Src. Es SRC, backend image processing and scanned, and capture.py5". Is "Es SRC" a typo or a specific module/path?**
    *   **Answer:** This was a typo in the transcript. The correct file path is `C:\Users\malit\OneDrive\Documents\GitHub\pba_vision_mapping\src\backend\image_processing\scan_and_capture.py`.
