
### **Project Document: Gantry Thermal Compensation Model**

#### **1. Introduction & Executive Summary**

This project aims to enhance the positional accuracy of a high-precision XYZ gantry system by developing a machine learning model to predict and correct for thermal expansion errors. Gantry systems used for micro-scale imaging or manipulation are highly susceptible to dimensional inaccuracies caused by ambient temperature fluctuations. Even minor changes in temperature can cause the system's structural frame to expand or contract, leading to a significant—and undesirable—offset between a commanded position and the true physical position. By leveraging real-world data from on-board temperature and positional sensors, this project will create an intelligent, data-driven compensation model. The final solution will function as a "smart layer" in the system's control software, adjusting coordinates in real-time to maintain exceptional accuracy across varying thermal conditions, without costly hardware modifications or complex environmental controls.

#### **2. Problem Statement**

The core challenge addressed by this project is the inherent physical limitation of thermal expansion in mechanical systems. For our specific application, the gantry's purpose relies on absolute positional accuracy, yet its metallic structure is directly influenced by operating temperatures. This creates a non-linear, multi-dimensional effect where different parts of the system may expand at different rates, leading to a complex distortion field across the operational area. This positional drift, which has been experimentally confirmed by observing known reference targets, directly compromises measurement integrity, diminishes operational repeatability, and ultimately limits the system's overall performance and reliability. Addressing this problem with a physics-based analytical model would be exceedingly complex and fail to capture real-world material imperfections and environmental nuances.

#### **3. Proposed Solution**

The proposed solution is to develop and apply a supervised machine learning model that learns the specific thermal behavior of this gantry. The system has been instrumented to collect the necessary data:

*   **Four PT1000 temperature sensors** are placed at strategic locations across the gantry frame to capture a thermal gradient.
*   **A high-resolution camera** is mounted on the Z-axis to precisely image a grid of 151x151 known circular targets on the system's base.
*   **High-precision encoders** provide the "commanded" or "measured" X and Y positions in millimeters.

Two separate machine learning regressor models will be trained on this dataset—one for the X-axis and one for the Y-axis.

**Model Inputs and Outputs**

The models will be trained to predict the positional *offset* based on the target position and the current thermal state of the system.

*   **Input Features:** The primary inputs for the models will be:
    *   `CP_X` (Calculated/Commanded X-axis position in mm)
    *   `CP_Y` (Calculated/Commanded Y-axis position in mm)
    *   `NT_1`, `NT_2`, `NT_3`, `NT_4` (The four current temperature sensor readings)
    *   `NT_D` (Time difference since last measurement, to be evaluated for importance)

*   **Output Targets (Predicted Variables):** The models will be trained to predict:
    *   `NPD_X` (The predicted difference or offset in the X-axis)
    *   `NPD_Y` (The predicted difference or offset in the Y-axis)

This model will then be integrated into the control system to dynamically apply calculated adjustments to every commanded move, effectively nullifying the error introduced by thermal drift by calculating `Corrected_Position = Commanded_Position - Predicted_Offset`.

#### **4. Key Objectives**

1.  **Quantify Thermal Deviation:** Perform Exploratory Data Analysis (EDA) on the existing dataset to statistically characterize the relationship between temperature changes and positional drift.
2.  **Develop a Predictive Model:** Train, test, and validate multiple machine learning regression models (including Linear Regression, Random Forest, and Gradient Boosting approaches) to accurately predict the positional offset based on the defined thermal and positional inputs.
3.  **Achieve Performance Targets:** The final model must demonstrate high precision, exceeding the system's inherent mechanical repeatability. The success criterion is a **Mean Absolute Error (MAE) of less than 1 micrometer (0.001 mm) for each axis.** This target is considered achievable given the system's hardware repeatability of 500 nanometers (0.5µm).
4.  **Architect a Deployment Path:** Define a clear technical architecture for integrating the saved, trained model into the gantry's real-time control software for live operational use.

#### **5. Technology & Methodology**

*   **Data Foundation:** The training dataset is highly robust, containing thousands of data points collected during heating, cooling, and steady-state thermal conditions. This ensures the model will be generalized for all operational scenarios.
*   **Data Analysis & Modeling:** Python (via Jupyter Notebooks).
*   **Core Libraries:** Pandas for data manipulation, Scikit-learn for model training/evaluation, and Matplotlib/Seaborn for data visualization. Libraries such as XGBoost will be evaluated for superior performance.
*   **Deployment:** The final models will be serialized (using `joblib` or `pickle`) to create lightweight, portable files that can be readily loaded and consumed by the gentry's control logic.