# Scan the grid and capture images

from backend.motor_control.acs_python_modules import motor_activation
from backend.motor_control.acs_python_modules import get_axis_parameters
from backend.image_processing.calculation_using_halcon import position_error_claculation
from backend.motor_control.acs_python_modules import read_parameters
from backend.services.plot_in_position_expantion import plot_in_position_stability
from backend.services.generate_2D_glass_certificate_62207_v1 import generate_glass_certificate
# from src.backend.services.generate_2D_glass_certificate_62207 import generate_glass_certificate
from backend.services.generate_2D_encoder_error_matrix import encoder_error_matrix

import time
import threading
import numpy as np
import os
import datetime
import numpy as np
import math
import cv2
import csv


class scan_grid():
    def __init__(self,ui):
        self.ui = ui
        self.cheack_motor_activation = motor_activation()       # to check motor enabled or not
        self.motor_motion_state = get_axis_parameters()         # to check motor in motion or not
        self.axis_x_position_error = 0
        self.axis_y_position_error = 0
        self.axis_z_position_error = 0

        self.ui.select_test_combo_box.currentIndexChanged.connect(self.select_test_combo_box)
        self.test_type ="1D error map X axis"
        self.first_target_X = 1
        self.last_target_X = 1
        self.first_target_Y = 1
        self.last_target_Y = 1
        self.test_type_X = 1
        self.test_type_Y = 0

        self.ui.select_test_axis_combo_box.currentIndexChanged.connect(self.select_test_axis_combo_box)
        self.test_axis = 'X axis'
        self.ui.first_target_line_edit.editingFinished.connect(self.first_target_line_edit_finished)
        self.ui.last_target_line_edit.editingFinished.connect(self.last_target_line_edit_finished)
        
        self.ui.number_of_runs_line_edit.editingFinished.connect(self.number_of_runs_line_edit_finished)
        self.ui.number_of_inspection_images_line_edit.editingFinished.connect(self.number_of_inspection_images_line_edit_finished)
        
        self.ui.wait_time_line_edit.editingFinished.connect(self.wait_time_line_edit_finshed)

        # PE calculation
        self.pe_calculation = position_error_claculation()
        self.read_temparature = read_parameters()
        self.pixel_to_mm = None
        self.image_center_pixel_x = None
        self.image_center_pixel_y = None
        
        pass

    

    def select_test_combo_box(self):
        self.test_type = self.ui.select_test_combo_box.currentText()

        if self.test_type == "1D error map X axis" or self.test_type == "1D expantion X axis" or self.test_type == "Auto focus X axis":
            self.first_target_X = 0
            self.last_target_X = 10
            self.first_target_Y = 0
            self.last_target_Y = 0
            self.test_type_X = 1
            self.test_type_Y = 0
        elif self.test_type == "1D error map Y axis" or self.test_type == "1D expantion Y axis":
            self.first_target_X = 0
            self.first_target_Y = 0
            self.last_target_X = 0
            self.last_target_Y = 10
            self.test_type_X = 0
            self.test_type_Y = 1
        elif self.test_type == "2D error map" or self.test_type == "2D expantion":
            self.first_target_X = 1
            self.first_target_Y = 1
            self.last_target_X = 10
            self.last_target_Y = 10
            self.test_type_X = 1
            self.test_type_Y = 1
        elif self.test_type == "Expantion inposition static" or self.test_type == "Expantion in position dynamic":
            self.first_target_X = 1
            self.last_target_X = 1
            self.first_target_Y = 1
            self.last_target_Y = 1
        elif self.test_type == "Motion Distance Calculation #54": # remove this after testing
            self.first_target_X = 1
            self.last_target_X = 1
            self.first_target_Y = 1
            self.last_target_Y = 1
            self.test_type_X = 0
            self.test_type_Y = 0
    

        self.select_test_axis_combo_box()


    def select_test_axis_combo_box(self):
        self.test_axis = self.ui.select_test_axis_combo_box.currentText()
        if self.test_axis == 'X axis':
            self.ui.first_target_line_edit.setText(str(self.first_target_X))
            self.ui.last_target_line_edit.setText(str(self.last_target_X))
        elif self.test_axis == 'Y axis':
            self.ui.first_target_line_edit.setText(str(self.first_target_Y))
            self.ui.last_target_line_edit.setText(str(self.last_target_Y))


    def first_target_line_edit_finished(self):
        if self.test_axis == 'X axis':
            self.first_target_X= int(self.ui.first_target_line_edit.text())

            #if self.first_target_X < 1:
            #    self.first_target_X = 1
            #    self.ui.first_target_line_edit.setText(str(self.first_target_X))

            if self.first_target_X < 0:
                self.first_target_X = 0
                self.ui.first_target_line_edit.setText(str(self.first_target_X))
            
            if self.test_type == "1D error map Y axis" or self.test_type == "1D expantion Y axis":
                self.last_target_X = self.first_target_X
                self.ui.last_target_line_edit.setText(str(self.last_target_X))
            elif self.test_type == "Expantion in position static":
                self.last_target_X = self.first_target_X
                self.ui.last_target_line_edit.setText(str(self.last_target_X))

        elif self.test_axis == 'Y axis':
            self.first_target_Y = int(self.ui.first_target_line_edit.text())
            
            #if self.first_target_Y < 1:
            #    self.first_target_Y = 1
            #    self.ui.first_target_line_edit.setText(str(self.first_target_Y))

            if self.first_target_Y < 0:
                self.first_target_Y = 0
                self.ui.first_target_line_edit.setText(str(self.first_target_Y))

            if self.test_type == "1D error map X axis" or self.test_type == "1D expantion X axis" or self.test_type == "Auto focus X axis" :
                self.last_target_Y = self.first_target_Y
                self.ui.last_target_line_edit.setText(str(self.last_target_Y))
            elif self.test_type == "Expantion in position static":
                self.last_target_Y = self.first_target_Y
                self.ui.last_target_line_edit.setText(str(self.last_target_Y))

    def last_target_line_edit_finished(self):

        if self.test_axis == 'X axis':
            self.last_target_X = int(self.ui.last_target_line_edit.text())

            if self.last_target_X < 0:
                self.last_target_X = 0
                self.ui.last_target_line_edit.setText(str(self.last_target_X))
            
            if self.test_type == "1D error map Y axis" or self.test_type == "1D expantion Y axis":
                self.first_target_X = self.last_target_X
                self.ui.first_target_line_edit.setText(str(self.first_target_X))
            elif self.test_type == "Expantion in position static":
                self.first_target_X = self.last_target_X
                self.ui.first_target_line_edit.setText(str(self.first_target_X))

        elif self.test_axis == 'Y axis':
            self.last_target_Y = int(self.ui.last_target_line_edit.text())
            if self.last_target_Y < 0:
                self.last_target_Y = 0
                self.ui.last_target_line_edit.setText(str(self.last_target_Y))

            if self.test_type == "1D error map X axis" or self.test_type == "1D expantion X axis" or self.test_type == "Auto focus X axis":
                self.first_target_Y = self.last_target_Y
                self.ui.first_target_line_edit.setText(str(self.first_target_Y))
            elif self.test_type == "Expantion in position static":
                self.first_target_Y = self.last_target_Y
                self.ui.first_target_line_edit.setText(str(self.first_target_Y))


    
    def number_of_runs_line_edit_finished(self):
        self.number_of_runs = int(self.ui.number_of_runs_line_edit.text())
        print(self.number_of_runs)
    
    def number_of_inspection_images_line_edit_finished(self):
        self.number_of_inspection_images = int(self.ui.number_of_inspection_images_line_edit.text())
        print(self.number_of_inspection_images)

    def wait_time_line_edit_finshed(self):
        self.wait_time= int(self.ui.wait_time_line_edit.text())
        print(self.wait_time)


    # Start thread to prevent hagging the software UI and camara feedback 
    def start_scan_in_thread(self, ui, hc, array, axis_array,camera_input,parent_directory):
        scan_thread = threading.Thread(target=self.scan_start, args=(ui, hc, array, axis_array,camera_input,parent_directory))
        scan_thread.start()


    # scanning function
    def scan_start(self,ui,hc,location_array, axis_select,camera_input,parent_directory):
        self.ui = ui
        self.hc = hc                        # Get communication handler from scan function

        self.wait_time_line_edit_finshed()
        self.number_of_runs_line_edit_finished()
        self.number_of_inspection_images_line_edit_finished()

        self.axis_select = axis_select      # axis index array from x, y, z axis control
        self.capture_image = camera_input   # sending same instance created on main controller to hear
        self.parent_directory = parent_directory
        self.location_array = location_array
        # print(axis_select[0], axis_select[1], axis_select[2])
        if axis_select[0] == -1 or axis_select[1] == -1 or axis_select[2] == -1:
            print("Error: Select X, Y and Z axis index from axis control")
        else: 
            axis_x_status = self.cheack_motor_activation.state(self.hc, str(axis_select[0]))    # cheack motor enablled or not
            axis_y_status = self.cheack_motor_activation.state(self.hc, str(axis_select[1]))
            axis_z_status = self.cheack_motor_activation.state(self.hc, str(axis_select[2]))
            
            if axis_x_status == 1 and axis_y_status == 1 :  # only cheking for X and Y axis are enabled or not
                axis,rows,column = self.location_array.shape

                #print(axis,rows,column)
                if self.test_type == "1D error map X axis" or self.test_type == "1D error map Y axis":
                    self.scan_method_2()                        # Scan method of 1D
                elif self.test_type == "2D error map":
                    self.scan_method_3()
                elif self.test_type == "1D expantion X axis" or self.test_type == "1D expantion Y axis":
                    self.scan_method_4()
                elif self.test_type == "2D expantion":
                    self.scan_method_5()
                elif self.test_type == "Expantion in position static":
                    self.scan_method_6()
                elif self.test_type == "Expantion in position dynamic":
                    self.scan_method_7(self.first_target_X,self.first_target_Y)
                elif self.test_type == "Auto focus X axis":
                    self.scan_method_8()
                elif self.test_type == "Motion Distance Calculation #54": # remove this after testing
                    self.scan_method_9()

            else:
                print("The axis X or axis Y in not enabled state")
        return 0
    
    def get_PE(self):
        self.axis_x_position_error = self.motor_motion_state.axis_pe(self.hc,self.axis_select[0])
        self.axis_y_position_error = self.motor_motion_state.axis_pe(self.hc,self.axis_select[1])
        self.axis_z_position_error = self.motor_motion_state.axis_pe(self.hc,self.axis_select[2])
        return 1

    def feedback_position(self):
        x_pos = self.ui.axis_x_fpos_lable.text()
        y_pos = self.ui.axis_y_fpos_lable.text()
        z_pos = self.ui.axis_z_fpos_lable.text()
        return (x_pos, y_pos, z_pos)


    # get the values from the scan grid function and create the motion accordingly
    def move_to_location(self,rows,column,location_array):  
        #print(location_array[0,rows,column], location_array[1,rows,column])
        tc1 = self.cheack_motor_activation.absolute_motion(self.hc,self.axis_select[0],location_array[0,rows,column])
        tc2 = self.cheack_motor_activation.absolute_motion(self.hc,self.axis_select[1],location_array[1,rows,column])
        tc3 = self.cheack_motor_activation.absolute_motion(self.hc,self.axis_select[2],location_array[2,rows,column])
        time.sleep(0.1)
        self.motion_state = 1

        while self.motion_state == 1:
            # This function is highly dependent on the MST.5 state of the motion !!!!!!
            # if not stup properly need to seup using ACS the MST target value and 
            #self.motion_state = np.amax([self.motor_motion_state.axis_motion_state(self.hc,self.axis_select[0]),self.motor_motion_state.axis_motion_state(self.hc,self.axis_select[1])])
            self.motion_state = np.amax([self.motor_motion_state.axis_motion_state(self.hc,self.axis_select[0]),self.motor_motion_state.axis_motion_state(self.hc,self.axis_select[1]),self.motor_motion_state.axis_motion_state(self.hc,self.axis_select[2])])
            if self.motion_state == 0:
                time.sleep(0.3)    
                self.motion_state = np.amax([self.motor_motion_state.axis_motion_state(self.hc,self.axis_select[0]),self.motor_motion_state.axis_motion_state(self.hc,self.axis_select[1]),self.motor_motion_state.axis_motion_state(self.hc,self.axis_select[2])])
            else:
                time.sleep(0.1)
        
        self.axis_x_position_error = self.motor_motion_state.axis_pe(self.hc,self.axis_select[0])
        self.axis_y_position_error = self.motor_motion_state.axis_pe(self.hc,self.axis_select[1])
        self.axis_z_position_error = self.motor_motion_state.axis_pe(self.hc,self.axis_select[2])
        #print(self.axis_x_position_error)
        time.sleep(1)
        return 1


    def scan_method_1(self):        # Just capture images
        # manual image capture
        now = datetime.datetime.now()
        timestamp_str = now.strftime('%Y-%m-%d-%H-%M-%S')
        name = f"{timestamp_str}.png"
        full_file_path = os.path.join(self.parent_directory,name) # create full file parth
        self.capture_image.save_frame(full_file_path)
        print(full_file_path)


    def create_log_file(self,filename):
        log_file_path = os.path.join(self.parent_directory,filename)
        log_file = open(log_file_path, 'a+')
        log_file.write("Time,Run,image name,Y position,X position,Y comand position,X comand position,Z comand position,axis_x_position_error,axis_y_position_error,axis_z_position_error, pix_Y,pix_X, pix_R, temp0, temp1, temp2,temp3")
        log_file.write(f"\n")
        log_file.close()
        return log_file_path
    
    def get_time_string(self):
        now = datetime.datetime.now()
        timestamp_str = now.strftime('%Y-%m-%d-%H-%M-%S')
        return timestamp_str


    def log_write_in_position_test(self,log_file_path,A,B):
        log_file = open(log_file_path, 'a+')
        self.get_PE()
        x_pos, y_pos, z_pos = self.feedback_position()
        log_file.write(f"{self.get_time_string()},{self.run},{self.image_name},{A},{B},{x_pos},{y_pos},{z_pos},{self.axis_x_position_error},{self.axis_y_position_error},{self.axis_z_position_error},{self.calculated_values[0]},{self.calculated_values[1]},{self.calculated_values[2]},{self.read_temparature.read_temparature(self.hc, 0)},{self.read_temparature.read_temparature(self.hc, 1)},{self.read_temparature.read_temparature(self.hc, 2)},{self.read_temparature.read_temparature(self.hc, 3)} \n")
        log_file.close()

    def log_write(self,log_file_path,A,B):
        log_file = open(log_file_path, 'a+')
        log_file.write(f"{self.get_time_string()},{self.run},{self.image_name},{A},{B},{self.location_array[0,A,B]},{self.location_array[1,A,B]},{self.location_array[2,A,B]},{self.axis_x_position_error},{self.axis_y_position_error},{self.axis_z_position_error},{self.calculated_values[0]},{self.calculated_values[1]},{self.calculated_values[2]},{self.read_temparature.read_temparature(self.hc, 0)},{self.read_temparature.read_temparature(self.hc, 1)},{self.read_temparature.read_temparature(self.hc, 2)},{self.read_temparature.read_temparature(self.hc, 3)} \n")
        log_file.close()
    
    def expantion_log_write(self,log_file_path,A,B):
        log_file = open(log_file_path, 'a+')
                          #"Time,                 Run,        image name,Y position,X position,Y comand position,             X comand position,                     Z comand position,                      axis_x_position_error,       axis_y_position_error,       axis_z_position_error,       pix_Y,                      pix_X,                      pix_R,                      temp0, temp1, temp2,temp3"
        log_file.write(f"{self.get_time_string()},{self.run},{self.image_name},{A},{B},{self.expantion_location_array[0,A,B]},{self.expantion_location_array[1,A,B]},{self.expantion_location_array[2,A,B]},{self.axis_x_position_error},{self.axis_y_position_error},{self.axis_z_position_error},{self.calculated_values[0]},{self.calculated_values[1]},{self.calculated_values[2]},{self.read_temparature.read_temparature(self.hc, 0)},{self.read_temparature.read_temparature(self.hc, 1)},{self.read_temparature.read_temparature(self.hc, 2)},{self.read_temparature.read_temparature(self.hc, 3)} \n")
        log_file.close()
    

    def image_capture(self,count):
        self.image_name = str(count) + '.png'
        full_file_path = os.path.join(self.parent_directory,self.image_name)   # create full file parth
        self.capture_image.save_frame(full_file_path)               # Send full file parth to
        self.calculated_values=self.pe_calculation.calculate_center(full_file_path)

    def save_expansion_array(self,name):
        full_file_path = os.path.join(self.parent_directory,name)   # create full file parth
        array_2d = self.expantion_location_array.reshape(-1, self.expantion_location_array.shape[-1])     
        np.savetxt(full_file_path, array_2d, delimiter=',', fmt='%.6f')      # save 2D file to .csv format
        print("Save file to:", full_file_path)

    # 1D error map X axis, 1D error map Y axis: scanning ether X direction or Y axis without self sentirng just move to location and capture image
    def scan_method_2(self):
        log_file_path = self.create_log_file("Log_file_1D.csv")
        count = 0
        for self.run in range(0,self.number_of_runs,1): 
            for A in range (self.first_target_Y - self.test_type_Y, self.last_target_Y + 1, 1):         # (0,rows,1)
                for B in range (self.first_target_X - self.test_type_X,self.last_target_X + 1, 1):      # (0,column,1)                 
                    self.move_to_location(A,B,self.location_array)
                    count = count + 1
                    self.image_capture(count)
                    self.log_write(log_file_path,A,B)
                    time.sleep(self.wait_time)

            for A in range (self.last_target_Y + self.test_type_Y, self.first_target_Y - 1, -1):
                for B in range (self.last_target_X + self.test_type_X, self.first_target_X -1,-1):                 
                    self.move_to_location(A,B,self.location_array)
                    count = count + 1
                    self.image_capture(count)
                    self.log_write(log_file_path,A,B)
                    time.sleep(self.wait_time)



            # for A in range (self.first_target_Y, self.last_target_Y + 1, 1):
            #     for B in range (self.first_target_X ,self.last_target_X + 1, 1):

    # 2D error map:  scanning X axis and Y axis without self centering just move to location and capture image 
    def scan_method_3(self):
        log_file_path = self.create_log_file("Log_file_2D_error_map.csv")
        count = 0
        # move to start location
        self.move_to_location(self.first_target_Y,self.first_target_X,self.location_array)

        # number of runs 
        for self.run in range(0,self.number_of_runs,1): 
            # move x direction 
            for A in range (self.first_target_Y, self.last_target_Y + 1, 1):

                for B in range (self.first_target_X,self.last_target_X + 1, 1):
                    self.move_to_location(A,B,self.location_array)
                    time.sleep(1)
                    count = count + 1
                    self.image_capture(count)
                    self.log_write(log_file_path,A,B)
                    time.sleep(self.wait_time)

                for B in range (self.last_target_X, self.first_target_X -1 ,-1):
                    self.move_to_location(A,B,self.location_array)
                    time.sleep(1)
                    count = count + 1
                    self.image_capture(count)
                    self.log_write(log_file_path,A,B)
                    time.sleep(self.wait_time)

        # #log_file_path = self.create_log_file("Log_file_2D_Y.csv")
        # self.move_to_location(self.first_target_Y,self.first_target_X,self.location_array)
        # # number of runs 
        # for self.run in range(0,self.number_of_runs,1): 
        #     # move Y direction 
        #     for B in range (self.first_target_X,self.last_target_X + 1, 1):
        #         for A in range (self.first_target_Y - self.test_type_Y, self.last_target_Y + 1, 1):
        #             self.move_to_location(A,B,self.location_array)
        #             time.sleep(1)
        #             count = count + 1
        #             self.image_capture(count)
        #             self.log_write(log_file_path,A,B)
        #             time.sleep(self.wait_time)

        #         for A in range (self.last_target_Y + self.test_type_Y, self.first_target_Y - 1, -1):
        #             self.move_to_location(A,B,self.location_array)
        #             time.sleep(1)
        #             count = count + 1
        #             self.image_capture(count)
        #             self.log_write(log_file_path,A,B)
        #             time.sleep(self.wait_time)


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
    

    def estimate_dot_center_button_clicked(self,A,B,image_name):

        if self.pixel_to_mm == None or self.image_center_pixel_x == None or self.image_center_pixel_y == None:
            self.image_center_pixel_x = int(self.read_recipe_csv('image_center_pixel_x'))
            self.image_center_pixel_y = int(self.read_recipe_csv('image_center_pixel_y'))
            self.pixel_to_mm = float(self.read_recipe_csv('pixel_to_mm'))

        # get axis positions

        x_pos = self.ui.axis_x_fpos_lable.text()
        y_pos = self.ui.axis_y_fpos_lable.text()
        z_pos = self.ui.axis_z_fpos_lable.text()

        # capture image
        # imagename = f"centerring_image_{image_name}.png"
        imagename = "centerring_image.png"
        full_file_path_centering_image =  os.path.join(self.parent_directory,imagename)
        self.capture_image.save_frame(full_file_path_centering_image)   # send full file parth to

        # Clculating PE using halcon 
        image_parameters = self.pe_calculation.calculate_center(full_file_path_centering_image) # output values are in pix_x, pixel_y
        y_position_error = (image_parameters[0] - self.image_center_pixel_y)*self.pixel_to_mm
        x_position_error = (image_parameters[1] - self.image_center_pixel_x)*self.pixel_to_mm
        #radius_of_target = image_parameters[2]*.4403
        correction_value_y = float(y_pos) + y_position_error 
        correction_value_x = float(x_pos) + x_position_error 

        self.expantion_location_array[0,A,B] = round(correction_value_x,6)
        self.expantion_location_array[1,A,B] = round(correction_value_y,6)

        print(correction_value_x ,correction_value_y)
        print(y_position_error, x_position_error)
        return (y_position_error, x_position_error)


    #### 1D expantion X axis, 1D expantion Y axis: scanning ether X direction or Y axis with self centering
    def scan_method_4(self):
        count = 0
        self.expantion_location_array= self.location_array
        log_file_name = f"Log_file_1D_expansion.csv"
        log_file_path = self.create_log_file(log_file_name)

        for self.run in range(0,self.number_of_runs,1): 
            #log_file_name = f"Log_file_1D_expansion_{self.run}.csv"
            #log_file_path = self.create_log_file(log_file_name)

            for A in range (self.first_target_Y, self.last_target_Y+1, 1):         # (0,rows,1)
                for B in range (self.first_target_X,self.last_target_X+1, 1):      # (0,column,1)                 
                    self.move_to_location(A,B,self.location_array)
                    time.sleep(1)
                    error_value = self.estimate_dot_center_button_clicked(A,B,count)
                    # if there is error then center of the dot
                    if -0.0001 < error_value[0] < 0.0001 and -0.0001 < error_value[1] < 0.0001:
                        print("No correction")
                    else:
                        print("correction")
                        self.move_to_location(A,B,self.expantion_location_array)

                    #self.move_to_location(A,B,self.expantion_location_array)
                    self.image_capture(count)
                    count = count +1
                    self.expantion_log_write(log_file_path,A,B)
                    time.sleep(self.wait_time)
            array_file_name = f"Expansion_array_positive{self.run}.csv"
            self.save_expansion_array(array_file_name)

            for A in range (self.last_target_Y, self.first_target_Y-1, -1):
                for B in range (self.last_target_X, self.first_target_X-1,-1):                 
                    self.move_to_location(A,B,self.location_array)
                    time.sleep(1)
                    error_value = self.estimate_dot_center_button_clicked(A,B,count)
                    if -0.0001 < error_value[0] < 0.0001 and -0.0001 < error_value[1] < 0.0001:
                        print("No correction")
                    else:
                        print("correction")
                        self.move_to_location(A,B,self.expantion_location_array)

                    #self.move_to_location(A,B,self.expantion_location_array)
                    self.image_capture(count)
                    count = count +1
                    self.expantion_log_write(log_file_path,A,B)
                    time.sleep(self.wait_time)
            array_file_name = f"Expansion_array_negative{self.run}.csv"
            self.save_expansion_array(array_file_name)


    #### 2D expantion: scanning X axis and Y axis with self centering
    def scan_method_5(self):
        count = 0
        self.expantion_location_array= self.location_array
        # move to start location
        self.move_to_location(self.first_target_Y,self.first_target_X,self.location_array)
        log_file_name = f"Log_file_2D_expansion_X_axis.csv"
        log_file_path = self.create_log_file(log_file_name)
        # number of runs 
        for self.run in range(0,self.number_of_runs,1): 
            # move X direction 
            
            for A in range (self.first_target_Y, self.last_target_Y + 1, 1):
                for B in range (self.first_target_X ,self.last_target_X + 1, 1):
                    self.move_to_location(A,B,self.expantion_location_array)
                    time.sleep(0.2)
                    self.estimate_dot_center_button_clicked(A,B,count)
                    self.move_to_location(A,B,self.expantion_location_array)
                    self.image_capture(count)
                    self.log_write(log_file_path,A,B)
                    time.sleep(self.wait_time) # manual wait time based on user input sometimes it can be 0.5
                    count = count + 1

                # for B in range (self.last_target_X, self.first_target_X -1,-1):
                #     self.move_to_location(A,B,self.expantion_location_array)
                #     time.sleep(1)
                #     self.estimate_dot_center_button_clicked(A,B,count)
                #     self.move_to_location(A,B,self.expantion_location_array)
                #     self.image_capture(count)
                #     self.log_write(log_file_path,A,B)
                #     time.sleep(self.wait_time)
                #     count = count + 1
            
            array_file_name = f"Expansion_array_2D_{self.run}.csv"
            self.save_expansion_array(array_file_name)
            print("Scan finished")

            # ======================================
            # Combining 2D error mapping calculation with 2D expantion
            # Temporary solution 2025_07_30
            # ======================================
            # 2D error mapping calculations
            # ======================================
            vision_log_file_file_path = log_file_path
            location_matrix_file_path = os.path.join(self.parent_directory,"calculated_all_referance_locations.csv")
            dot_center_encoder_location_matrix_file_path = os.path.join(self.parent_directory,"Expansion_array_2D_0.csv")
            # update this relative path for different computers
            camera_calibration_file_path = os.path.join(os.getcwd(), r"src\recipes\camera_calibration_data_2X_lens.npz")
            #camera_calibration_file_path = r"C:\Users\malit\Documents\GitHub\2D_optical_vision_mapping\src\recipes\camera_calibration_data_2X_lens.npz"
            print(vision_log_file_file_path)
            print(location_matrix_file_path)
            print(camera_calibration_file_path)
            generate_glass_certificate_test = generate_glass_certificate()
            glass_certificate_full_file_path = generate_glass_certificate_test.generate_2d_glass_certificate(location_matrix_file_path,vision_log_file_file_path,camera_calibration_file_path)
            print("2D error mapping calculations finished")
            # ======================================

            # Create an instance of the encoder_error_matrix class and call the generate_2D_encoder_error_matrix method
            generate_encoder_error_matrix = encoder_error_matrix()
            encoder_error_matrix_new = generate_encoder_error_matrix.generate_2D_encoder_error_matrix(vision_log_file_file_path, location_matrix_file_path, glass_certificate_full_file_path, dot_center_encoder_location_matrix_file_path)
            full_path_x_errormap,full_path_y_errormap = generate_encoder_error_matrix.generate_ACS_errormaps(encoder_error_matrix_new, vision_log_file_file_path)
            
            print("full 2D encoder error mapping calculations finished")
            print("Full path X error map:", full_path_x_errormap)
            print("Full path Y error map:", full_path_y_errormap)
            # ======================================




    # no motion just capture image and calculate the error to see the expantion of the system
    def scan_method_6(self):
        '''go to the first target location and capture the image calculate error and recode the error, repeta multiple times'''
        log_file_path = self.create_log_file("Log_file_in_position_stability_static.csv")
        count = 0
        self.move_to_location(self.first_target_Y,self.first_target_X,self.location_array)
        time.sleep(self.wait_time)

        for self.run in range(0,self.number_of_runs,1):
            self.image_capture(count)
            self.log_write_in_position_test(log_file_path,self.first_target_Y,self.first_target_X)
            time.sleep(self.wait_time)
            count = count + 1
        
        print("Scan finished")
        print(log_file_path)


    # capture image and calculate the error and move to 
    def scan_method_7(self,A,B):
        '''go to the first target location and capture the image calculate error and recode the error, repeta multiple times'''
        log_file_path = self.create_log_file("Log_file_in_position_stability_dynamic.csv")
        count = 0
        self.expantion_location_array= self.location_array
        self.move_to_location(A,B,self.location_array)
        time.sleep(self.wait_time)

        for self.run in range(0,self.number_of_runs,1):
            self.image_capture(count)
            error_value = self.estimate_dot_center_button_clicked(A,B,count)
            print(error_value)
            time.sleep(0.5)
            self.move_to_location(A,B,self.expantion_location_array)
            time.sleep(0.5)
            self.image_capture(count)
            self.log_write_in_position_test(log_file_path,self.first_target_Y,self.first_target_X)
            time.sleep(self.wait_time)
            count = count + 1
        
        print("Scan finished")
        print(log_file_path)


#================
# Auto focus
#================
    # get equation from fit points
    def fit_quadratic(self,x, y):
        """
        Fits a second-order polynomial (quadratic) to the given x and y data.

        Args:
          x: A list or NumPy array of x-values.
          y: A list or NumPy array of y-values.

        Returns:
          A tuple (a, b, c) representing the coefficients of the quadratic equation
          y = ax^2 + bx + c.
        """

        # Convert lists to NumPy arrays for easier calculations
        x = np.array(x)
        y = np.array(y)

        # Construct the Vandermonde matrix
        A = np.vstack([x**2, x, np.ones(len(x))]).T

        # Solve for the coefficients using least squares
        coefficients, residuals, rank, s = np.linalg.lstsq(A, y, rcond=None)

        return coefficients

    # try to do auto focus 
    def auto_focus(self,threshold,count,A,B):
        '''Move up and down and get maximum sharpness value.'''
        print("Auto focus scan method started")
        self.variance = np.zeros(3)
        self.z_axis_position = np.zeros(3)
        self.z_axis_position[0] = self.ui.axis_z_fpos_lable.text()
        self.variance[0] = self.detect_sharpness_sobel(threshold,count)
        #self.z_axis_position[0] = self.expantion_location_array[2,A,B]
        
        time.sleep(1)
        if self.variance[0]> threshold:
            return 0
        else:
            
            #print("Sharpness is increasing")
            self.expantion_location_array[2,A,B] = self.expantion_location_array[2,A,B] - 0.03
            self.move_to_location(A,B,self.expantion_location_array)
            time.sleep(1)
            self.z_axis_position[1] = self.ui.axis_z_fpos_lable.text()
            self.variance[1] = self.detect_sharpness_sobel(threshold,count)
            

            self.expantion_location_array[2,A,B] = self.expantion_location_array[2,A,B] + 0.06
            self.move_to_location(A,B,self.expantion_location_array)
            time.sleep(1)
            self.z_axis_position[2] = self.ui.axis_z_fpos_lable.text()
            self.variance[2] = self.detect_sharpness_sobel(threshold,count)

            print(self.variance)
            print(self.z_axis_position)
            # Fit a quadratic to the data
            a, b, c = self.fit_quadratic(self.z_axis_position, self.variance)
            #print(-b/2a)
            print(a,b,c)
            predicted_max_z_position = -b/(2*a)
            print(predicted_max_z_position)
            if predicted_max_z_position > self.expantion_location_array[2,A,B]-1 and predicted_max_z_position < self.expantion_location_array[2,A,B]+1:
                self.expantion_location_array[2,A,B] = predicted_max_z_position
                print("new location is:", self.expantion_location_array[2,A,B])
                self.move_to_location(A,B,self.expantion_location_array)
                time.sleep(20)
            else:
                print("No change in location")
            
            
            self.variance = self.detect_sharpness_sobel(threshold,count)
            self.z_axis_position = self.ui.axis_z_fpos_lable.text()
            print(self.variance, self.z_axis_position)
            return 0



    # Self center and shaptness correction axis: scanning ether X direction or Y axis with self centering
    def detect_sharpness_sobel(self,threshold,count):

        self.image_name = str(count) + '.png'
        full_file_path = os.path.join(self.parent_directory,self.image_name)   # create full file parth
        self.capture_image.save_frame(full_file_path)               # Send full file parth to take image and save in that path
        #self.calculated_values=self.pe_calculation.calculate_center(full_file_path) # calculate center of the dot and update the values

        image = cv2.imread(full_file_path, cv2.IMREAD_GRAYSCALE) # convert image to gray scale

        if image is None:
            print("Error: Could not read image.")
            return None, "Error"

        # Compute Sobel gradients in X and Y direction
        sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=5)
        sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=5)

        # Compute magnitude of gradient
        sobel_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)

        # Compute variance of Sobel response
        variance = sobel_magnitude.var()

        # Determine focus status
        status = "In Focus" if variance > threshold else "Blurry"
        print(f"Sharpness: {variance}, Status: {status}")

        return variance


    def scan_method_8(self):
        '''move up and down and get maximum sharpness value'''
        print("Auto focus scan method started")
        count = 0

        self.expantion_location_array= self.location_array
        log_file_name = f"Log_file_auto_focus.csv"
        log_file_path = self.create_log_file(log_file_name)

        for self.run in range(0,self.number_of_runs,1): 
            
            for A in range (self.first_target_Y - self.test_type_Y, self.last_target_Y + 1, 1):         # (0,rows,10)
                for B in range (self.first_target_X - self.test_type_X,self.last_target_X + 1, 1):      # (0,column,10)                 
                    self.move_to_location(A,B,self.expantion_location_array)
                    time.sleep(1)
                    # Calculate errors on position using vision
                    error_value = self.estimate_dot_center_button_clicked(A,B,count)
                    # move to correct location.
                    self.move_to_location(A,B,self.expantion_location_array)
                    self.image_capture(count)

                    # take image, calculate position error, and detect sharpness using Sobel
                    threshold = 2500
                    self.auto_focus(threshold,count,A,B)
                    #self.detect_sharpness_sobel(threshold,count)

                    self.expantion_log_write(log_file_path,A,B)
                    time.sleep(self.wait_time)
                    count = count +1

            for A in range (self.last_target_Y + self.test_type_Y, self.first_target_Y - 1, -1):
                for B in range (self.last_target_X + self.test_type_X, self.first_target_X -1,-1):                 
                    self.move_to_location(A,B,self.expantion_location_array)
                    time.sleep(1)
                    error_value = self.estimate_dot_center_button_clicked(A,B,count)
                    self.move_to_location(A,B,self.expantion_location_array)

                    threshold = 2500
                    self.auto_focus(threshold,count,A,B)
                    #self.detect_sharpness_sobel(threshold,count)

                    count = count +1
                    self.expantion_log_write(log_file_path,A,B)
                    time.sleep(self.wait_time)
                    count = count +1
        
        array_file_name = f"Expansion_array_negative{self.run}.csv"
        self.save_expansion_array(array_file_name)

    # =============================================================
    # test code for Motion distance calculation
    def create_log_file_motion_distance_calculation(self,filename):
        log_file_path = os.path.join(self.parent_directory,filename)
        log_file = open(log_file_path, 'a+')
        log_file.write("Time,Run,image name,Y position,X position,Dot center position X,Dot center position Y,Dot center position Z,axis_x_fpos,axis_y_fpos,axis_z_fpos, pix_Y,pix_X, pix_R, temp0, temp1, temp2,temp3")
        log_file.write(f"\n")
        log_file.close()
        return log_file_path

    def log_write_motion_distance_calculation(self,log_file_path,A,B):
        
        log_file = open(log_file_path, 'a+')
        log_file.write(f"{self.get_time_string()},{self.run},{self.image_name},{A},{B},{self.location_array[0,A,B]},{self.location_array[1,A,B]},{self.location_array[2,A,B]},{self.x_fpos},{self.y_fpos},{self.z_fpos},{self.calculated_values[0]},{self.calculated_values[1]},{self.calculated_values[2]},{self.read_temparature.read_temparature(self.hc, 0)},{self.read_temparature.read_temparature(self.hc, 1)},{self.read_temparature.read_temparature(self.hc, 2)},{self.read_temparature.read_temparature(self.hc, 3)} \n")
        log_file.close()

    def modify_motion_location_array_for_motion_distance_calculation(self):
        print("Modifying motion location array for motion distance calculation")

        center_x = self.location_array[0,self.first_target_Y,self.first_target_X] 
        print("Center X:", center_x)
        center_y = self.location_array[1,self.first_target_Y,self.first_target_X]
        center_z = self.location_array[2,self.first_target_Y,self.first_target_X]
        
        # Halving rule sequence: 1.0, 0.5, 0.25 ... down to ~0.015 um
        distances_um = []
        d = 2.0
        while d >= 0.005:
            distances_um.append(d)
            d /= 4.0
            
        # Convert to mm
        distances_mm = [x / 1000.0 for x in distances_um]
        print("Distances (mm):", distances_mm)
        
        xs = []
        ys = []
        zs = []
        
        step = 1
        for dist in distances_mm:
            
            # 1. Move to Target (Force X axis motion)
            tx = center_x + dist
            print("Moving to X:", tx)
            self.motion_location_array[0, self.first_target_Y + step, self.first_target_X] = tx
            self.motion_location_array[1, self.first_target_Y + step, self.first_target_X] = center_y
            self.motion_location_array[2, self.first_target_Y + step, self.first_target_X] = center_z
            print(self.motion_location_array[0, self.first_target_Y + step, self.first_target_X])
            step += 1

        # Create the array with shape (3, N, 1) to be compatible with move_to_location(row, col)
        # We will use 'row' as the step index and 'col' as 0
        
        
        # Print the modified locations for verification
        print("Modified motion location array:", self.motion_location_array[0,:10,0]) 
        
        return  self.motion_location_array


    # Motion distance calculation scan method #54
    def scan_method_9(self):
        print("Motion distance calculation scan method started")
        
        # Initialize motion location array
        self.motion_location_array= self.location_array.copy()
        self.expantion_location_array= self.location_array.copy()
        
        # Create log file
        log_file_name = f"Log_file_minimum_motion_distance_calculation.csv"
        log_file_path = self.create_log_file_motion_distance_calculation(log_file_name)
        

        # Step 1: Baseline Calibration
        self.move_to_location(self.first_target_Y, self.first_target_X,self.motion_location_array)
        time.sleep(0.2)

        # Step 2: Find and move to the center
        centering_image_number = 0
        self.estimate_dot_center_button_clicked(self.first_target_Y, self.first_target_X,centering_image_number)
        self.move_to_location(self.first_target_Y, self.first_target_X,self.motion_location_array)


        # Step 3: Baseline Measurment at Center
        count = 1
        self.run = 0
        for i in range (0,self.number_of_inspection_images,1):
            self.x_fpos, self.y_fpos, self.z_fpos = self.feedback_position()
            self.image_capture(count)
            self.log_write_motion_distance_calculation(log_file_path,self.first_target_Y, self.first_target_X)
            time.sleep(self.wait_time) # manual wait time based on user input sometimes it can be 0.5
            count = count + 1

        

        # Step 4: Motion Distance Calculation
        self.motion_location_array_new = self.modify_motion_location_array_for_motion_distance_calculation()

        # Step 5: Execute Sequence
        
        print(self.motion_location_array_new[0,:10,0])

        for step_idx in range(1,5,1):
            # Move to the step location
            self.move_to_location(self.first_target_Y + step_idx, self.first_target_X,self.motion_location_array_new)
            time.sleep(0.5) # Settle time
            
            # Capture images for this step
            for i in range(self.number_of_inspection_images):
                self.x_fpos, self.y_fpos, self.z_fpos = self.feedback_position()
                self.image_capture(count)
                self.log_write_motion_distance_calculation(log_file_path,self.first_target_Y, self.first_target_X)
                time.sleep(self.wait_time)
                count += 1

        print("Motion distance calculation scan method finished")
        print("Log file path:", log_file_path)