
# Glass Scale Measurement Specification

Company: PBA SYSTEMS

Date: 2026.02.10

Revision number: V4

# **1\. Calibration Item Description**

The calibration item is a chrome-coated precision hard mask with overall dimensions of 520 mm x 520 mm. The probe elements are distributed within an active area of 500 mm x 500 mm. The probe elements consist of two pattern types:

**A. Circular patterns** 

These elements consist of a central solid circle and a concentric ring (annulus). Figure 1 illustrates a circular pattern with measurement. 

* **Annulus:** A chrome-coated ring defined by an outer radius of **1.0 mm** and an inner radius of **0.5 mm**.  
* **Central Circle:** A solid chrome circle with a radius of **0.125 mm**.

**Note:** From here onwards **“center position of the circular pattern”** term will be used to describe the center position of the outer circle of annulus with a 1.0 mm radius.

![][image1]

Figure 1: Circular pattern with expected radius values and tolerance values. The shaded areas should be chrome coated areas.  Chrome coated areas should be reflective and visible as white inspecting from a black & white vision system with coaxial lighting.

**B. Checkerboard Patterns**

These elements consist of an 8 x 8 grid of squares (64 squares total). Figure 2 illustrates the checkerboard pattern with four circular patterns. 

* **Square Dimensions:** 0.4 mm x 0.4 mm.  
* **Composition:** 32 squares are chrome-coated, and the remaining 32 squares are clear (uncoated), forming a checkerboard pattern.

![][image2]

Figure 2: Checkered grid pattern with four adjacent circular patterns.

# **2\. Layout and Grid Structure**

* **Circular Grid:** The circular patterns are applied in a regular grid of **101 x 101 points** with a grid dimension (pitch) of **RX \= RY \= 5 mm**.  
* **Checkerboard Placement:** The 8 x 8 checkerboard elements are located at the geometric center of four adjacent circular patterns.  
* **Index Mark for lower left corner:** In the **lower-left corner**, three (3) checkerboard marks are placed between the first three consecutive circular pattern grids in both the X (rows) and Y(columns) directions \[R0,R1,R2,C0,C1,C2\]. Figure 3 illustrates the circular pattern located in the lower left corner. 


# Figure 3: Index mark location with three checkerboard markers to recognize the lower left corner.

# **3\. Coordinate System and Alignment**

For identification purposes, the horizontal tracks (X-direction/rows) and vertical tracks (Y-direction/columns) corresponding to the center positions of the circular patterns are designated as follows:

* **Rows:** R0 to R100  
* **Columns:** C0 to C100

Naming convention of individual circular pattern follows the (Row number \- Column number) format. Rows are named (Row number) and columns are named (Column number).

**Reference Base:**

* **Origin of grid system:** The circular pattern in the lower-left corner is designated **(R0-C0)** and serves as the origin of the grid naming system.  
* **Measurement reference origin**: The measurement reference origin is defined as the **center position of the circular pattern** at (R50-C50).  
* **Reference Line (Skew):** The line connecting the **center position of circular pattern** point (R50-C0) and point (R50-C100) defines the X-axis reference line..

Figure 4: Creating parallel lines using (R50-C0) and (R50-C100) **center position of the circular pattern.**

The measurement shall begin with making the **“measurement reference origin”** (R50-C50) as zero position and aligning the “**reference line**” to the measurement’s instrument base axis. 

# **4\. Measurement data format specifications**

Measurement values should be specified in micrometers with one decimal place.   
Example 1: 	X direction distance (R50-C50) to (R50-C55) \= 24999.7 μm  
		Y direction distance (R50-C50) to (R50-C55) \= 0.6 μm  
Example 2: 	X direction distance (R50-C50) to (R50-C49) \= \-4999.7 μm  
		Y direction distance (R50-C50) to (R50-C49) \= \-0.1 μm

# 

# **5\. Measurement Scope**

The objective is to measure the **“center position of the circular pattern”** with respect to **“measurement reference origin”**. 

**5.1 Circle position measurement (measurement grid):**

The step size (grid spacing) for the measurement is **25 mm**. 

**Specific tracks to be measured:**   
Measure the **center position of the circular pattern** for the following tracks (21 points per track):

1. **Row Track X1:** Row R50 (measuring from C0 to C100 at 25mm intervals)  
2. **Row Track X2:** Row R55 (measuring from C0 to C100 at 25mm intervals)  
3. **Column Track Y1:** Column C50 (measuring from R0 to R100 at 25mm intervals)

Use the reference line and measurement reference base described in section 3 for the measurement. Measure the relative distance to the **“center position of the circular pattern”** with respect to **“Measurement reference origin”.** Figure 5 illustrates the important locations of the glass scale which are required for measurement. (PDF version will also be provided.)

**5.2 Circle radius measurement:**

Measure the **circle radius of the annulus (1 mm diameter)** for the specific coordinates listed below. 

**Specific circles radius to be measured:**

1. R21-C21  
2. R40-C40  
3. R60-C40  
4. R79-C21  
5. R21-C79  
6. R40-C60  
7. R60-C60  
8. R79-C79  
9. R50-C50  
10. R55-C50

  


![][image3]

Figure 5: Measurement specification drawing.

# **6\. Environmental condition**

To ensure measurement accuracy, the laboratory environment must conform to the following conditions:

Lab ambient Temperature:  
	Example:  20°C (Standard Reference Temperature)

**Temperature Stability:** 

Example:  The ambient temperature of the lab must be maintained at 20°C ± 0.5°C

**Acclimatization time:** 

The scale must undergo a thermal soak period within the measurement environment prior to calibration to minimize thermal expansion errors. Ex: 5 hours.

# **7\. Format for measurement results**

Use the reference defined in Section 3\. Measure the distance relative to **“center position of the circular pattern”** of **“measurement reference origin”** to positions specified in “section 5.1”. Table 1 and Table 2 and Table 3 specify the measurement results output format and “section 4” specifies the measurement data output format.   Table 4 specifies the measurement results output format for radius measurement.

Table 1: Column “C50” measurement reporting format.  

| No | Row ID | Column ID | X value µm | Y value µm |
| :- | :----- | :-------- | :--------- | :--------- |
| 1  | R0     | C50       |            |            |
| 2  | R5     | C50       |            |            |
| 3  | R10    | C50       |            |            |
| 4  | R15    | C50       |            |            |
| 5  | R20    | C50       |            |            |
| 6  | R25    | C50       |            |            |
| 7  | R30    | C50       |            |            |
| 8  | R35    | C50       |            |            |
| 9  | R40    | C50       |            |            |
| 10 | R45    | C50       |            |            |
| 11 | R50    | C50       |            |            |
| 12 | R55    | C50       |            |            |
| 13 | R60    | C50       |            |            |
| 14 | R65    | C50       |            |            |
| 15 | R70    | C50       |            |            |
| 16 | R75    | C50       |            |            |
| 17 | R80    | C50       |            |            |
| 18 | R85    | C50       |            |            |
| 19 | R90    | C50       |            |            |
| 20 | R95    | C50       |            |            |
| 21 | R100   | C50       |            |            |



Table 2: Row “R50” measurement reporting format.

| No | Row ID | Column ID | X value µm | Y value µm |
| :- | :----- | :-------- | :--------- | :--------- |
| 1  | R50    | C0        |            |            |
| 2  | R50    | C5        |            |            |
| 3  | R50    | C10       |            |            |
| 4  | R50    | C15       |            |            |
| 5  | R50    | C20       |            |            |
| 6  | R50    | C25       |            |            |
| 7  | R50    | C30       |            |            |
| 8  | R50    | C35       |            |            |
| 9  | R50    | C40       |            |            |
| 10 | R50    | C45       |            |            |
| 11 | R50    | C50       |            |            |
| 12 | R50    | C55       |            |            |
| 13 | R50    | C60       |            |            |
| 14 | R50    | C65       |            |            |
| 15 | R50    | C70       |            |            |
| 16 | R50    | C75       |            |            |
| 17 | R50    | C80       |            |            |
| 18 | R50    | C85       |            |            |
| 19 | R50    | C90       |            |            |
| 20 | R50    | C95       |            |            |
| 21 | R50    | C100      |            |            |


Table 2: Row “R55” measurement reporting format.

| No | Row ID | Column ID | X value µm | Y value µm |
| :- | :----- | :-------- | :--------- | :--------- |
| 1  | R55    | C0        |            |            |
| 2  | R55    | C5        |            |            |
| 3  | R55    | C10       |            |            |
| 4  | R55    | C15       |            |            |
| 5  | R55    | C20       |            |            |
| 6  | R55    | C25       |            |            |
| 7  | R55    | C30       |            |            |
| 8  | R55    | C35       |            |            |
| 9  | R55    | C40       |            |            |
| 10 | R55    | C45       |            |            |
| 11 | R55    | C50       |            |            |
| 12 | R55    | C55       |            |            |
| 13 | R55    | C60       |            |            |
| 14 | R55    | C65       |            |            |
| 15 | R55    | C70       |            |            |
| 16 | R55    | C75       |            |            |
| 17 | R55    | C80       |            |            |
| 18 | R55    | C85       |            |            |
| 19 | R55    | C90       |            |            |
| 20 | R55    | C95       |            |            |
| 21 | R55    | C100      |            |            |





For the radius measurements specifics of the measurements are described in “section 5.2”.  Table 3 specifies the measurement results output format and “section 4” specifies the measurement data output format.   

Table 4: Circle radius measurement reporting format.

The following table is sourced entirely from your selection in Sheet1.

| No | Row ID | Column ID | Radius value in µm |
| :- | :----- | :-------- | :----------------- |
| 1  | R21    | C21       |                    |
| 2  | R40    | C40       |                    |
| 3  | R60    | C40       |                    |
| 4  | R79    | C21       |                    |
| 5  | R21    | C79       |                    |
| 6  | R40    | C60       |                    |
| 7  | R60    | C60       |                    |
| 8  | R79    | C79       |                    |
| 9  | R50    | C50       |                    |
| 10 | R55    | C50       |                    |

