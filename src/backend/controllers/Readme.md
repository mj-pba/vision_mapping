## Operations of controller

### 1. AXIS CONTROLLER / MOTION MANEGER

X,Y,Z Axis controller enable many featurea avelable in ACS SpiiPlus software motion maneger. In velocity, accleration, deceleration jurk, line edit block have do double duties. 
1. It has to display the selected axis assiged velocity value in the motor controller. 
2. Get the user input from and set velocity in motor controller

**Functions used** : To create fullfill this requiment we have to use timer function update the values and line edit. When user tring to edit the value the cursor position value to will change that identify wether user start editing the paremeter. When user finish edit when he moves to other block we have to use "edit finish" signel to set the cursor point to back to defalt value. 

**Parameters used:** 
1. Default value of the paremter "self.axis_x_velocity_le_cursor_position" is -1,  when start edit it will autumatically update
2. After edit finsih the we have to manually update the self.axis_x_velocity_le_cursor_position value to -1
3. Defalt value of the self.axis_x_velocity_paremter_updater_activation paremter is 0
4. When user selct the axis we change the paremter self.axis_x_velocity_paremter_updater_activation  value to 1

In this way we can control the input values and display the current value. 

The functional block diagram for the process in illustrated in figure 1

![figure 1](https://github.com/malithjkd/2D_optical_vision_mapping/blob/main/assets/images/axis_velocity_input_and_display_controller_value.png)


### 2. Updating axis parameter 

To display motiron paremters such as command velocity, accleration which are in motor drive **"def update_parameters(self):"** timer is used. That function is triger in main loop (QTimer) and we have no control over it. To activate and deactivate differant sections in the updater code blocks, "updater_start_stop" function is used. 

We start updating paramters after communication establish and selecting the axis. 

### Updater control function

def updater_start_stop(self,value): function is to set "on" and "off" all the avelable updater activation paramet such as axis_x_velocity_parameter_updater_activation. While doing that it has to check the communication status with the controller. If we loose communication or disconnect from botton we have to stop updating all the parameters. 


### Creating grid location 

When we place the glass dot matrix, we dont know the dot location. To get the dot locations we can follow the 3 dot method can or or 4 dot method we are intresed to follow to avoid any damaged dots and trying to get the best possible accuracy while doing the dit locations.

We have two options start the process eather selecting locations manully or selection saved location.

1. If we are selecting location from manual 
   1. We have to check wether we have selected or 4 seperate points to do the calculation 

2. If we are loding from file follwing things need to do 
   1. Check the file is not corrupted. The X axis value locations and Y axis value location and Z
   2. If we are using saved dot locations we have to manually move to the location to conform the locaions are correct.

If we have more than 3 dots location in the matrix, we can try to start next stop of calculating the angles of the bitween the dots. For that we have select which methods to follow. 
(In the case of manual entering the location. Consider user ended 3 location and and 3 location are not perpediculer then we wait for 4th location to start calculating the location to save machine power)

**3_dot_method** 
During the 3 dot method  -- Implimnted 2024.05.24
1. We have to check the row, colum values are perpendiculer. Othersize dot locations can be any location.
2. Then we have to check the dot location (actual x and y values of the matrix) are perpendiculer. To do that we calculate the dot product and check each coder is perpendiculer to each other.  
3. Then we can calculate the rest of the matrix.

**4_dot_method**
During the 4 dot method
1. We have to check the are there 2 dots in same column and two values in same row. Othersize dot locations can be any location.
2. Check the line created using the actual x and y values of the matrix of the same column values and  actual position and line created using actual x and y values of the matrix of the same row values are perpendiculer.
3. Then we can calculate the rest of the matrix.


### Scanning and capturing the images

The implimentation scan and capture images while providing live feedback of the camara is challanging task. The first task is to collect the camara feedback and display to use. To do that we use timer to tiger the collecting frames from the camara and put inside the lable variable to give visurl feedback of the camara. 
During the scan phase we have to save the images. To solve the both issues we separate the frame captureing in the differant class. Capturing frame is done by "capture_frame" funtion in "capture_frame_update" class. The "update_frame" function in "camara_in" class is calls the functiaon and gets the image. Then the function dispays it in its UI. The "save_frame" function in same class also call the "capture_frame" function and get the frame then the fram save with given name. While "save_frame" function do the saving the image the "update_frame" function which triggerd by timer goes to error mode pringing some error massage.
 
The instance created in main controller to display the camera feedback is handerd over to scan and capture functions to use the same resorces without the clash. Also the scan and capture functions and running on different tread to make sure the safty of the equpments. Which enables the capability to user to stop the motors by dissabling them in the middle of the scan process.
 

# Improvements suggetions for main UI controller

**Error Handling and Recovery:** Implement robust error handling mechanisms to gracefully handle communication failures, invalid user inputs, unexpected responses from the ACS library, and other potential issues. Provide informative error messages to the user, including details about the error and potential solutions. Consider incorporating retry logic or recovery mechanisms to attempt reconnection or parameter updates in case of transient errors.

**Input Validation:** Thoroughly validate user inputs to ensure they are within valid ranges and adhere to data type requirements. Display appropriate error messages or warnings when invalid inputs are encountered. Consider using input masks or constraints to guide the user towards valid input formats.

**Parameter Limits:** Implement checks for parameter limits (e.g., velocity, acceleration, deceleration, jerk) to prevent exceeding the capabilities of the motor or controller.
Provide feedback to the user if they attempt to set values outside the allowed range.

**Asynchronous Updates:** Explore using asynchronous techniques (e.g., threading or Qt signals/slots) to avoid blocking the main thread during parameter updates or communication operations. This can improve UI responsiveness and prevent freezing during updates.

**Code Organization and Modularity:** Break down the code into smaller, well-defined functions or classes to improve readability, maintainability, and reusability. Use meaningful variable and function names that reflect their purpose.

**Comments and Documentation:** Add clear and concise comments to explain the logic behind different code sections. Consider creating comprehensive documentation for the code, including usage instructions, assumptions, and limitations.

**Additional Considerations:**

**Data Persistence:**
If necessary, implement mechanisms to store and restore user settings or motor parameters across application sessions.

**Logging:** Consider adding logging capabilities to track events, errors, and parameter changes for debugging and analysis purposes.

**User Interface Enhancements:** Provide visual feedback to the user during communication and parameter updates (e.g., progress bars, loading indicators).