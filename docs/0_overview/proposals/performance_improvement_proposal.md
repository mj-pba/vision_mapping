# Project Proposal: Achieving a 75% Reduction in 2D Error Mapping Test Time and Sub-Micron Accuracy

### 1. Executive Summary

Our goal is to dramatically improve our 2D measurement process, cutting test time from a lengthy **16 hours down to under 4 hours** while significantly boosting accuracy. To meet our project goals and deliver a certifiably accurate system, we require a one-time investment in key hardware and environmental controls. These foundational components are non-negotiable for achieving the target sub-micron precision.

The required components are:
1.  **A Proper Calibration Setup:** Specialized calibration tools and software to ensure our vision system is precise from the start.
2.  **A Certified Master Reference:** A special, temperature-stable glass scale that acts as a certified "ruler" to guarantee our measurements are consistently accurate.
3.  **A High-Precision Verification Tool:** A nano-precise positioning stage to independently verify that our vision system's measurements meet the required sub-micron accuracy.
4.  **A Stable Environment:** A clean, temperature-controlled room to prevent tiny environmental changes from skewing the results.

Estimated cost for the above requirements will be approximately **SGD 100,000**.

*   IMT glass certificate + certificate: SGD 60,000
*   Lens and calibration glass: SGD 20,000
*   Halcon vision software license: SGD 6,000
*   Nano-precision stage: SGD 10,000

### 2. Introduction & Goal

As discussed, this document outlines a detailed proposal to significantly reduce the time required for the 2D error mapping test. The primary goal is to improve efficiency and accuracy by evolving our current process. This proposal evaluates the existing methodology, identifies bottlenecks, and presents a set of software-driven solutions and process improvements that are dependent on the acquisition of critical hardware.

**Thoritical mesurment values**

|No|Discription|Value|Unit|
|---|---|----|---|
|01|Optical measurment accurasy thioritical |+- 10|nm|
|02|Image capturing frequancy|6|hz|

### 3. Test Time Calculation: A Comparative Analysis

To quantify the impact of the proposed changes, we will compare the time to test for the future arrangement (98 x 98 grid) using both the current and proposed methods.

**Arrangement 490mm x 490mm: 98 x 98 dot grid = 9,604 dots.**

#### Current Method: "Two-Image Capture" (Existing Process)
The current process, as implemented in `scan_method_5` within `scan_and_capture.py`, involves two movements and two image captures for each dot to ensure the encoder position is recorded at the precise center of the dot. Due to concurrently displaying images in the UI, it uses significant time delays and CPU resources.

*   **Time Breakdown per Dot (Estimated):**
    *   Move 1 (to calculated location): ~1550 milliseconds
    *   Wait & Settle: ~50 milliseconds
    *   Capture 1 & Process: ~1500 milliseconds
    *   Move 2 (to actual center): ~950 milliseconds
    *   Wait & Settle: ~50 milliseconds
    *   Capture 2 and calculation: ~1500 milliseconds
    *   **Total Time per Dot: ~6.0 seconds**

*   **Total Estimated Test Time (Current Method):**
    9,604 dots \* 6 sec/dot ≈ 57,624 seconds ≈ **16.0 hours**

This does not include the initial setup time for pixel-to-mm calculation or the post-processing time for generating the glass certificate, which is required for every test due to thermal expansion.

#### Proposed Method: "Single-Image Capture"
The proposed method eliminates the second move and capture by using a calibrated camera to calculate the dot's offset from the image center. It also optimizes UI updates to save resources and time.

*   **Time Breakdown per Dot (Estimated):**
    *   Move 1 (to calculated location): ~480 milliseconds
    *   Wait & Settle: ~20 milliseconds
    *   Capture 1 & calculation: ~1000 milliseconds
    *   **Total Time per Dot: ~1.5 seconds**

*   **Total Estimated Test Time (Proposed Method):**
    (9,604 dots \* 1.5 sec/dot) + (98 rows \* 2 sec/row for long stroke motion) ≈ 14,602 seconds ≈ **4.05 hours**

This represents a **75% reduction** in test execution time. The most significant savings, however, come from eliminating the need to re-generate the glass certificate for every run, which is enabled by the proposed hardware.

### 4. Evaluation of Improvement Initiatives

Here we evaluate the key initiatives that enable the time reduction.

#### Initiative 1: Implement Single-Image Capture via Camera Calibration
*   **Method:**
    1.  Perform a one-time camera calibration for both the 4X and 1X magnification lenses to create a distortion correction map using Halcon software and a certified calibration grid.
    2.  Modify the `scan_method_5` in `scan_and_capture.py`. Instead of moving to the center after the first image, the software will:
        a. Capture a single image at the calculated location.
        b. Use the calibration data to get an accurate pixel coordinate for the dot's center.
        c. Calculate the offset in pixels from the image center.
        d. Convert this pixel offset to a physical distance (mm) using the pre-calibrated `pixel_to_mm` ratio.
        e. Record the initial encoder position and the calculated physical offset as the final result.
*   **Pros:**
    *   Drastically reduces on-the-fly calculations and stage movements.
    *   Halves the number of image captures per dot.
*   **Cons:**
    *   Requires an initial time investment to perform the camera calibration procedure.
*   **Expected Time Reduction:**
    *   Saves ~4.5 seconds per dot, totaling ~12 hours for a 98x98 grid scan.
*   **Resource Requirements:**
    *   **Hardware:**
        *   Halcon-accepted camera calibration glass scales (2 nos).
        *   1x telecentric lens (1 pixel ≈ 3.45 µm).
        *   4x telecentric lens (1 pixel ≈ 0.8625 µm).
        *   Halcon development license.
        *   IMT Master glass scale.
        *   **Nano-precision stage:** A high-resolution stage (e.g., piezo) capable of sub-micron movements is required to independently verify the accuracy of the vision-based offset measurements.
    *   **Software:** Requires implementing a camera calibration routine and modifying the image processing logic in `scan_and_capture.py`.
*   **Industry Standard:** This is standard practice. High-precision vision systems rely on calibrated optics to make accurate measurements from a single frame without corrective movements.

#### Initiative 2: Leverage Certified Glass Scale & Stable Environment
*   **Method:**
    1.  Utilize the new non-thermally expanding glass scale with its manufacturer's certificate.
    2.  Perform all tests in the clean room environment to ensure thermal stability.
    3.  The software no longer needs to run the `generate_2d_glass_certificate` process for every test. The `pixel_to_mm` calculation also becomes a one-time setup step.
*   **Pros:**
    *   Eliminates the lengthy, vision-based certificate generation process for every test.
    *   Improves overall accuracy and repeatability by using a stable, certified measurement baseline.
*   **Cons:**
    *   The provided certificate is partial. Software logic may be needed to interpolate or work with the given data.
*   **Expected Time Reduction:**
    *   This is a major time saving. The current process of generating a glass certificate can take 4-8 hours. By eliminating this, we remove a primary bottleneck.
*   **Resource Requirements:**
    *   **Hardware:** Requires the non-thermally expanding glass scale and access to the thermally stable clean room.
    *   **Software:** The data processing pipeline must be re-architected to use the pre-existing certificate data as the "ground truth."
*   **Industry Standard:** Using a certified and thermally stable artifact in a controlled environment is the gold standard for metrology and calibration.

### 5. Consequences of Insufficient Hardware

It is critical to highlight the direct impact of failing to invest in the required hardware. These are not "nice-to-haves"; they are fundamental requirements for meeting the project's goals.

*   **Without a Thermally Stable Glass Scale:** We are forced to treat the glass as a variable in every measurement. This necessitates the time-consuming process of re-generating a glass certificate for every test run. The system measures errors in both the stage *and* the glass, confounding the results and adding hours to the process.

*   **Without a Thermally Stable Environment:** Similar to the glass scale, environmental temperature changes introduce thermal expansion in the machine frame itself. This forces frequent re-calibration of `pixel_to_mm` and other parameters, adding time and profound uncertainty to the measurements.

*   **Without Calibrated Cameras:** We cannot trust a single image to provide an accurate offset measurement. This forces the "two-image" method, which is merely a slow and inefficient workaround for a hardware/software deficiency. It adds hours of mechanical movement and settling time to the overall test.

*   **Without a Nano-Precision Verification Stage:** We have **no objective way to prove our system's accuracy**. The software will *calculate* a sub-micron offset, but we cannot be certain this calculated value corresponds to a real-world physical displacement. This stage provides the independent "ground truth" needed to validate our vision measurements. Without it, we are making an unverified claim of accuracy, undermining the project's credibility and exposing us to the significant risk of delivering a system that fails to meet its core specification.

### 6. Conclusion & Recommendation

To achieve the target accuracy of **±0.5µm** and reduce test time from **16 hours to under 4 hours**, this proposal outlines critical hardware and environmental upgrades. The current "two-image" method is an unsustainable workaround. Transitioning to a "single-image" capture process is essential, but it is entirely dependent on a high-precision, one-time camera calibration.

This calibration and the overall system's validity hinge on the following investments:
*   **Halcon-accepted calibration glass and telecentric lenses** to correctly map and remove optical distortion.
*   **A certified, non-thermally expanding master glass scale** to provide a reliable measurement baseline.
*   **A nano-precision stage** to independently verify that our vision measurements meet the demanding nanometer-level accuracy requirement.
*   **A thermally stable clean room** to eliminate environmental variables that corrupt results.

Without this foundational investment in a controlled setup and certified hardware, we cannot escape the current slow, inaccurate process. We will fail to meet the project's core accuracy and efficiency requirements, and we will be unable to certify the performance of our system with confidence. I strongly recommend the approval of the SGD 100,000 budget to procure these essential components.