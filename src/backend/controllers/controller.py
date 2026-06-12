# Main UI controller file
#   1. Start communication between drives. 
#   2. Triger X,Y,Z axis UI controller files to control the motors X,Y,Z positions
#   3. Triger updater to update all the X,Y,Z parameters in the seperate files
# 
# Notes: update main_window_ui.py
# keep MainWindow.resize(1100, 800)
# keep self.cam_dock_widget.setMinimumSize(QSize(1250, 950))

# import 
import os
import numpy as np
import csv
import time
from datetime import datetime
# import backend
from backend.motor_control.acs_python_modules import scan_network, write_parameters
from backend.motor_control.acs_python_modules import enable_communication
from backend.motor_control.acs_python_modules import disconnect_communication
from backend.controllers.axis_x_controller import axis_x_ui_controller
from backend.controllers.axis_y_controller import axis_y_ui_controller
from backend.controllers.axis_z_controller import axis_z_ui_controller

from backend.image_processing.web_camera_feed_in import camera_in  # this is to web cam 
from backend.image_processing.web_camera_feed_in import capture_frame_update # second class frame capture, and release

# from backend.image_processing.dahua_cam_api.iRayple_camera_feed_in import camera_frame_update         # maybe dll does not work with python 3.13  
from backend.image_processing.bfs_cam_api.BFS_camera_feed_in import camera_frame_update_BFS
from backend.image_processing.calculation_using_halcon import in_position_calculation

from backend.controllers.calibration_data_controller import calibration_data_control
from backend.image_processing.scan_and_capture import scan_grid
from backend.motor_control.acs_python_modules import read_parameters, write_parameters

from PySide6.QtGui import QIcon, QImage,QPixmap
from PySide6.QtWidgets import QDockWidget, QTableWidgetItem, QFileDialog

import cv2
from PySide6.QtCore import Qt


# 
class UIController:
    def __init__(self,ui):
        self.ui = ui #pass the ui instance to the controller
        self.hc = -1
        
        
        # netowrk scan
        self.netowrk_scanner = scan_network()               # Create an instance of the scan_network class
        self.ui.network_scan_button.clicked.connect(self.network_scan_button_clicked) 

        # enable and dissable communication with motor controler
        self.communication_enabler = enable_communication()
        self.communication_dissabler = disconnect_communication()
        self.ui.enable_communication_button.clicked.connect(self.enable_communication_button_clicked)

        # start axis X,Y,Z axis controller.py 
        self.axis_x_controller = axis_x_ui_controller(self.ui)
        self.axis_y_controller = axis_y_ui_controller(self.ui)
        self.axis_z_controller = axis_z_ui_controller(self.ui)
        
        # Start calibration data section
        self.calibration_data_handler = calibration_data_control(self.ui)

        ## View camera feedback 
        ## self.ui.cam_dock_widget.show()
        self.camera_frame_update_activation = 0     # activation controller for 
        self.ui.cam_dock_widget.close()
        self.ui.actionCamera_feedback.triggered.connect(self.camera_view_button_clicked)
        
        # user select camera type
        self.ui.cam_type_combo_box.currentIndexChanged.connect(self.camera_type_input)
        
        # user select camere index
        self.ui.cam_id_combo_box.currentIndexChanged.connect(self.camera_index_input)
        self.cam_id_select = -1 # start condition
        self.camera = None 
        self.show_down_counter = 0         # for start condition and switch camera type
        self.ui.cam_id_combo_box.setEnabled(False)

        # user start camera frame update 
        self.ui.start_camera_push_button.clicked.connect(self.camera_start_button)
        self.ui.start_camera_push_button.setEnabled(False)
        self.circle_radius = None
        self.image_filename = None
        
        # Camera input frame
        self.ui.stop_camera_push_button.clicked.connect(self.camera_stop_button)

        # drow cycle 
        self.ui.select_circle_radio_button.toggled.connect(self.update_circle)
        self.draw_circle = True

        # save frame
        self.ui.save_image_push_button.clicked.connect(self.save_frame_button)

        # select_camera_mode_button
        self.ui.select_camera_mode_button.clicked.connect(self.camera_activity_type_button_clicked)
        self.camera_activity_type = 1  # start with teach mode

    ## End of camera functions

    # Temparature reading
        self.read_temparature_activation = 0        # activation controller for reading temparature
        self.ui.start_temperature_sensor_button.clicked.connect(self.start_temperature_sensor_button_clicked)

    ## read temparature
        # self.read_temparature = read_parameters()
        self.read_acs_parameters = read_parameters()
        self.write_acs_parameters = write_parameters()
    
    
    ## POSITION ERROR TEST
        # Scanning grid
        self.selected_axis = [-1,-1,-1] 
        self.ui.scan_button.clicked.connect(self.scan_button_clicked)
        self.scan_gird_locations = scan_grid(self.ui)                      # imported from "scan and capture class" 

    

    ### IN POSITION TEST
    ## In position test 
        self.ui.number_of_image_line_edit.editingFinished.connect(self.number_of_image_line_edit_input)
        self.in_position_test_number_of_images = 33


    ## in positon test start button clicked
        self.ui.in_position_test_start_button.clicked.connect(self.in_position_test_start_button_clicked)

        # end of main class 

    ### communication enabling functions
    def network_scan_button_clicked(self):
        self.ip = self.netowrk_scanner.scan_network_function()
        self.ui.ip_input_lineEdit.setText(self.ip[0])
        # Note: 
        # Error massage: Network not connected

    ### UI "Enable communication" button click 
    def enable_communication_button_clicked(self):
        # self.hc is the communication handler which mentioned in the ACS python libry document
        if self.hc  == -1:
            self.ip_input = self.ui.ip_input_lineEdit.text()
            
            self.hc = self.communication_enabler.enable_communication_function(self.ip_input)  # call enable_communication_function in acs_python_modules.py  
            print("Connecting to IP: ",self.ip_input)
            if self.hc == -1:
                print("Not connected")
                self.ui.info_text_edit.setText("Not connected")
            else:
                self.ui.enable_communication_button.setText("Disconnect")
                self.axis_x_controller.set_communication(self.hc)                       # starting x axis_x_controller.py by sending the self.hc value
                self.axis_y_controller.set_communication(self.hc)                       # starting y axis_y_controller.py by sending the self.hc value
                self.axis_z_controller.set_communication(self.hc)
                self.calibration_data_handler.get_communication_enabler_status(self.hc) # Start "calibration_data_controller.py"
                self.ui.info_text_edit.setText("Communication Enabled")                 # Clear previous text and update new status
        else:
            
            self.communication_dissabler.disconnect_communication_function(self.hc)     # call disconnect_communication_function in acs_python_modules.py
            self.hc = -1
            self.ui.enable_communication_button.setText("Enable communication")
            self.axis_x_controller.set_communication(self.hc)                           # Send hc value axis_x_controller.py after communication dessabling
            self.axis_y_controller.set_communication(self.hc)
            self.axis_z_controller.set_communication(self.hc)
            self.calibration_data_handler.get_communication_enabler_status(self.hc)
            self.ui.info_text_edit.setText("Communication Disabled")
        
        # Note: 
        # Error massage: Disconnection of communication.
        # Error massage: When communication loose communication. Ask to save current parameters. 
        # Start reconnection mechanisam: Ask to scan and reconnec, Ask to do homing, and ask to check the all the positon.  

# ==================================
# Camera functions 
# ==================================
    ### Draw circle 
    def update_circle(self, state):
        # Assuming you have a variable self.draw_circle that indicates whether to draw the circle or not
        self.draw_circle = state
        print(self.draw_circle)

    # start camera input widget
    def camera_view_button_clicked(self):
        print("camera view from")
        #self.camera_frame_update_activation = 1
        self.ui.cam_dock_widget.show()


    # Select camera type
    def camera_type_input(self):
        self.camera_type_input = self.ui.cam_type_combo_box.currentText()
        
        # Validate the camera type input
        if self.camera_type_input in ["Dahua_A550", "Web_cam", "BFS"]:
            self.camera_type = self.camera_type_input

            #print(f"Selected camera type: {self.camera_type}")
            self.ui.cam_id_combo_box.setEnabled(True)
        else:
            self.camera_stop_button()
            print("Error: Invalid camera type selected. Stop camera")
            self.ui.info_text_edit.setText("Error: Invalid camera type selected. Stop camera")
            self.camera_type = -1                                        # Reset to None if the input is invalid
        print(self.camera_type)


    # camera index select 
    def camera_index_input(self):
        self.cam_id_select = int(self.ui.cam_id_combo_box.currentText()) if self.ui.cam_id_combo_box.currentText() else -1
        if self.cam_id_select == -1 :
            self.camera_stop_button()
        else:
            print("camera_ID_selected:", self.cam_id_select)
            self.ui.info_text_edit.setText("camera_ID_selected:" + str(self.cam_id_select))

            self.ui.start_camera_push_button.setEnabled(True)
        
        # otherwise camera may consume computation. 

    def camera_activity_type_button_clicked(self):
        # start condition is 
        if self.camera_activity_type == 1:
            self.camera_activity_type = 0
            self.camera_frame_update_activation = 0
            self.write_acs_parameters.write_led_status(self.hc, "LED_OUT", 0)
            self.ui.select_camera_mode_button.setText("Select Teach mode")
            print("Scan mode activated.")
            self.ui.info_text_edit.setText("Scan mode activated.")

        else:
            self.camera_activity_type = 1
            self.camera_frame_update_activation = 1
            self.write_acs_parameters.write_led_status(self.hc, "LED_OUT", 1)
            self.ui.select_camera_mode_button.setText("Select Scan mode")
            print("Teach mode activated.")
            self.ui.info_text_edit.setText("Teach mode activated.")
        # read acs LED_OUT parameter
        
        self.read_led_status = self.read_acs_parameters.read_led_status(self.hc, "LED_OUT")
        print("LED status:", self.read_led_status)  


    def create_folder_for_instance(self):
        # Creating location to save the data
        file_execution_location = os.getcwd()                                                       # get the current location
        self.parent_directory = os.path.dirname(file_execution_location)                            # get the current location
        current_datetime_based_folder_name = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")           # Getting data and time
        self.new_folder_path = os.path.join(self.parent_directory, current_datetime_based_folder_name)
        # Create the new folder
        os.makedirs(self.new_folder_path, exist_ok=True)



    # Start camera
    def camera_start_button(self):
        if self.camera_frame_update_activation == 1: # cleanup and stop stream if camera was previously already activated
            self.camera_stop_button() 

        if (self.cam_id_select == 0 and self.camera_type == "Web_cam"):
            # start web camera from 
            self.camera_input_frame = capture_frame_update(self.cam_id_select)          # Instance created to gets the frame opencv 
            self.camera_frame_update_activation = 1                                     # To view the 
            self.circle_radius = 132 # hardcoded for now. different radius for different camera
            self.image_filename = 'image_for_UI.bmp'
            self.create_folder_for_instance()   # create folder to save the image
            self.image_filename = os.path.join(self.new_folder_path, self.image_filename)
            # print("web camera 0 started")
            self.ui.info_text_edit.setText("web camera 0 started")
            
        elif(self.cam_id_select == 1 and self.camera_type == "Dahua_A550"):             # actual, original dahua camera code
            # start industrial camera
            self.camera_input_frame = camera_frame_update(self.cam_id_select)
            if self.camera_input_frame.camera_connect_input():                          # To setup industrial camera iRapi camera 
                self.camera_frame_update_activation = 1                                 # Update from to view the camera feed
                self.calibration_data_handler.get_camera_instance(self.camera_input_frame)      # send camera instance to calibration data controller.py file to help to elignt the dot circlr and target dot
                self.circle_radius = 453 # hardcoded for now. different radius for different camera
                self.selected_camera = "Dahua_A550"
                self.image_filename = 'image_for_UI.bmp'
                self.create_folder_for_instance()   # create folder to save the image
                # combine the file name with the parent directory
                self.image_filename = os.path.join(self.new_folder_path, self.image_filename)
            else:
                print("error connecting to Dahua camera.")

        elif self.cam_id_select == 1 and self.camera_type == "BFS":                     # bfs camera code. replace camera type when UI is setup for it
            self.camera_input_frame = camera_frame_update_BFS(self.cam_id_select)       # Instance for BFS camera
            self.camera_input_frame.connect_camera()
            self.camera_frame_update_activation = 1
            self.calibration_data_handler.get_camera_instance(self.camera_input_frame)  # Pass instance to calibration 
            self.circle_radius = int(self.read_recipe_csv("circle_radius"))
            self.image_filename = 'image_for_UI.bmp'
            self.create_folder_for_instance()   # create folder to save the image
            # combine the file name with the parent directory
            self.image_filename = os.path.join(self.new_folder_path, self.image_filename)
            # print("BFS camera started.")
            self.ui.info_text_edit.setText("BFS camera started.")


        else:
            self.camera_frame_update_activation = 0
            #print("Camera type or camera index is not valid")
            self.ui.info_text_edit.setText("Camera type or camera index is not valid")
    
    # stop camera
    def camera_stop_button(self):
        self.camera_frame_update_activation = 0
        self.camera_input_frame.relese_camera()
        self.selected_camera = None
        # print('CAMERA RELEASED.')
        self.ui.info_text_edit.setText("Camera released.")



    def read_recipe_csv(self,parameter):
        # get current working directory
        file_path = os.getcwd()  # get the current location
        recipe_file_location = os.path.join(file_path, r'src\recipes\active_recipe.csv')      # Create full file parth
        # print("Active recipe file path : ",recepe_file_location)  
        # check the file is exist or not
        if os.path.exists(recipe_file_location):
            with open(recipe_file_location, 'r', newline='') as file:
                reader = csv.reader(file)
                header = next(reader, None)  # Skip header if present
                for row in reader:
                    if len(row) >= 2 and row[0] == parameter:
                        return row[1]
                    
        else:
            print("File does not exist.")
            return None

    # Send camera instance to other objects



    
    # collect the frame and send to UI (recurring function)
    # this function is called from the main loop to update the camera frame in the UI
    def collect_frame_from_camera_send_to_UI(self):


        # read acs LED_OUT parameter
        # self.read_led_status = self.read_acs_parameters.read_led_status(self.hc, "LED_OUT")

        if self.camera_type == "BFS" or self.camera_type == "Web_cam":
            self.show_down_counter = self.show_down_counter + 1
            if self.show_down_counter == 5:
                self.show_down_counter = 0
                image_save_status = self.camera_input_frame.save_frame(self.image_filename)
            else:
                image_save_status = False        

        if image_save_status:
            # display the image in the UI
            frame = cv2.imread(self.image_filename)
            
            if frame is not None:
                height = frame.shape[0]
                width  = frame.shape[1]
                # print(height,width)
                if len(frame.shape) == 3:           # for color image
                    if self.draw_circle:            # drow cicle
                        # cv2.circle(frame, pix_value_center_x, pix_value_center_y, radius, size )
                        cv2.circle(frame, (int(width/2), int(height/2)), self.circle_radius, (255, 255, 255), 2)

                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert image fro m BGR to RGB
                    channel = frame.shape[2]  # Number of channels
                    bytes_per_line = channel * width
                    q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
                    # Convert QImage to QPixmap
                    pixmap = QPixmap.fromImage(q_image)
                    # Get label size
                    label_width = self.ui.cam_input_lable.width()
                    label_height = self.ui.cam_input_lable.height()
                    # Scale the pixmap to fit the label, maintaining aspect ratio
                    scaled_pixmap = pixmap.scaled(label_width, label_height, Qt.KeepAspectRatio)
                    # Set alingment 
                    self.ui.cam_input_lable.setAlignment(Qt.AlignCenter)
                    # Display the scaled pixmap in the QLabel
                    self.ui.cam_input_lable.setPixmap(scaled_pixmap)

                elif len(frame.shape) == 2:         # for gray image
                    if self.draw_circle:            # drow cicle
                        # cv2.circle(frame, pix_value_center_x, pix_value_center_y, radius, size )
                        # cv2.circle(frame, (1296, 1024),580, (255, 255, 255), 2) # large circle
                        cv2.circle(frame, (int(width/2), int(height/2)), self.circle_radius, (255, 255, 255), 2) # small circle

                    bytes_per_line = width  # Since it's grayscale
                    q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
                    # Convert QImage to QPixmap
                    pixmap = QPixmap.fromImage(q_image)
                    # Get label size
                    label_width = self.ui.cam_input_lable.width()
                    label_height = self.ui.cam_input_lable.height()
                    # Scale the pixmap to fit the label, maintaining aspect ratio
                    scaled_pixmap = pixmap.scaled(label_width, label_height, Qt.KeepAspectRatio)
                    # Set alingment
                    self.ui.cam_input_lable.setAlignment(Qt.AlignCenter)
                    # Display the scaled pixmap in the QLabel
                    self.ui.cam_input_lable.setPixmap(scaled_pixmap)





    def save_frame_button(self):
        # have to send to folder outdise the software fordl
        file_path = os.getcwd()                                                       # get the current location
        self.parent_directory = os.path.dirname(file_path)                            # get the current location
        filename = 'test_image.bmp'
        # combine the file name with the parent directory
        filename = os.path.join(self.parent_directory, filename)                     # Create full file parth

        self.camera_input_frame.save_frame(filename)

# ==================================
# End of camera functions
# ==================================

# ==================================
# Start: Temparature sensor setup
# ==================================

    def start_temperature_sensor_button_clicked(self):
        if self.read_temparature_activation == 0:
            self.read_temparature_activation = 1
            self.ui.start_temperature_sensor_button.setText("Stop temparature sensor")
            print("temparature sensor started")
        else:
            self.read_temparature_activation = 0
            self.ui.start_temperature_sensor_button.setText("Start temparature sensor")
            print("temparature sensor stoped")

# ==================================
# End: Temparature sensor setup
# ==================================
### Each scan have to consider like a one instance. We have to save all the data in the instance in one folder.  
#   When each scan starts we have to save the initial data such as 3 ref points, full grid location, 
#   and all the image captured, and Position error matrix calculated from images. 


    def save_user_input_ref_location(self):

        # Save user input ref locations 
        user_ref_input_file_name = "user_input_referance_locations.csv"                               # Define the file name
        ref_file_path = os.path.join(self.new_folder_path, user_ref_input_file_name)                  # Create full file parth
        # cannot save the 3D array, so we have to reshape it to 2D
        ref_array_2d = self.position_np_array_ref.reshape(-1, self.position_np_array_ref.shape[-1])     
        np.savetxt(ref_file_path, ref_array_2d, delimiter=',', fmt='%.6f')                            # save 2D file to .csv format

        # Save user input ref locations 
        calculated_full_dot_location_file_name = "calculated_all_referance_locations.csv"             # Define the file name
        full_file_path = os.path.join(self.new_folder_path, calculated_full_dot_location_file_name)   # Create full file parth
        full_array_2d = self.position_np_array.reshape(-1, self.position_np_array.shape[-1])          # convert 3D to 2D matrix
        np.savetxt(full_file_path, full_array_2d, delimiter=',', fmt='%.6f')                          # save 2D file to .csv format

        # send file location to calibration data control to start calculating the PE values
        self.calibration_data_handler.get_new_instance_folder_location(self.new_folder_path)

### Grid Scan starting - 
    def scan_button_clicked(self):
        self.selected_axis[0] = self.axis_x_controller.send_axis_select()   # get axis x selected index
        self.selected_axis[1] = self.axis_y_controller.send_axis_select()   # get axis y selected index
        self.selected_axis[2] = self.axis_z_controller.send_axis_select()   # get axis z selected index
        self.position_np_array = self.calibration_data_handler.send_array_data()    # get position array from calibration data
        self.position_np_array_ref = self.calibration_data_handler.send_array_data_ref()
        self.create_folder_for_instance()
        self.save_user_input_ref_location()
        time.sleep(0.1)
        #self.scan_gird_locations.scan_start(self.hc,self.position_np_array)
        self.scan_gird_locations.start_scan_in_thread(self.ui, self.hc, self.position_np_array,self.selected_axis,self.camera_input_frame,self.new_folder_path)
        time.sleep(0.1)






### Test 1 - In poisition test 
    def number_of_image_line_edit_input(self):
        self.in_position_test_number_of_images = int(self.ui.number_of_image_line_edit.text())


    def in_position_test_start_button_clicked(self):
    # Creating location to save the data
        self.create_folder_for_instance()

        x_pos = self.ui.axis_x_fpos_lable.text()
        y_pos = self.ui.axis_y_fpos_lable.text()
        z_pos = self.ui.axis_z_fpos_lable.text()
        
        count = 0
        for count in range (0,self.in_position_test_number_of_images,1):
            # led out on
            self.write_acs_parameters.write_led_status(self.hc, "LED_OUT", 1)
            time.sleep(0.2) # wait for led to turn on
            name = str(count) + '.png'
            full_file_path = os.path.join(self.new_folder_path,name) # create full file parth
            self.camera_input_frame.save_frame(full_file_path)
            # led out off
            self.write_acs_parameters.write_led_status(self.hc, "LED_OUT", 0)
            time.sleep(0.1) # wait for led to turn off

        # hard code location 
        # dir = r'C:\Users\mj.j\OneDrive - PBA Systems Pte. Ltd\GitHub\Github\2024_09_19_08_36_20'
        # self.calculation = in_position_calculation(dir)


        # Calculating PE and plotting variation graphs. 
        self.calculation = in_position_calculation(self.new_folder_path)
        self.std_deviation_nm = self.calculation.calculate_and_print(float(x_pos),float(y_pos),float(z_pos))
        self.ui.label_sigma_X.setText(str(round(self.std_deviation_nm[0],3))+' nm')
        self.ui.label_sigma_Y.setText(str(round(self.std_deviation_nm[1],3))+' nm')
        self.ui.label_sigma_R.setText(str(round(self.std_deviation_nm[2],3))+' nm')



### Updater function
    def update_parameters(self):

        if self.read_temparature_activation == 1:
            sensor_value_1 = self.read_acs_parameters.read_temparature(self.hc, 0)
            sensor_value_2 = self.read_acs_parameters.read_temparature(self.hc, 1)
            sensor_value_3 = self.read_acs_parameters.read_temparature(self.hc, 2)
            sensor_value_4 = self.read_acs_parameters.read_temparature(self.hc, 3)
            # sensor_value_1 = self.read_temparature.read_temparature(self.hc, 0)
            # sensor_value_2 = self.read_temparature.read_temparature(self.hc, 1)
            # sensor_value_3 = self.read_temparature.read_temparature(self.hc, 2)
            # sensor_value_4 = self.read_temparature.read_temparature(self.hc, 3)

            self.ui.label_15.setText("Temperature sensor 1 : " + str(sensor_value_1) + " °C" )
            self.ui.label_16.setText("Temperature sensor 2 : " + str(sensor_value_2) + " °C" )
            self.ui.label_17.setText("Temperature sensor 3 : " + str(sensor_value_3) + " °C" )
            self.ui.label_31.setText("Temperature sensor 4 : " + str(sensor_value_4) + " °C" )

        if self.camera_frame_update_activation == 1:
            self.collect_frame_from_camera_send_to_UI()

        if self.hc != -1:
            self.axis_x_controller.axis_x_update_parameters()
            self.axis_y_controller.axis_y_update_parameters()
            self.axis_z_controller.axis_z_update_parameters()


