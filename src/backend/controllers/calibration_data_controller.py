# This file controlls the UI and data oparations related to setting up position error calculation test and 
#  other importent operations like
# 1. Collecting and storing the glass jig dot positions
# 2. Calculating the estimated glass dot locations
# 3. Save dot location in .csv format
# 4. Open dot locations from csv
# 5. Create single motion
# 6. Check the selected location and real life motor position is are perpendiculer
# 7. Create  
# 8. Triger image capturing
# 9. Triger image processing 

from PySide6.QtWidgets import QDockWidget, QTableWidgetItem, QFileDialog
#from backend.image_processing.calaulate_position_error import position_error
from backend.image_processing.calculation_using_halcon import position_error_claculation
import numpy as np
from datetime import datetime
import math
import glob
import os
import csv
from backend.controllers.axis_x_controller import axis_x_ui_controller
from backend.controllers.axis_y_controller import axis_y_ui_controller
from backend.controllers.axis_z_controller import axis_z_ui_controller

from backend.services.file_services import open_file
from backend.services.plot_laser_vision_encoder_error import calculate_actual_dot_seperation

from backend.services.generate_error_map_laser import create_error_map_buffer_from_laser_file_and_send_to_acs
from backend.services.generate_error_map_vision import  create_error_map_buffer_from_glass_certificate_and_vision_files_and_send_to_acs
from backend.services.generate_glass_certificate_62207 import generate_glass_certificate
from backend.services.plot_in_position_expantion import plot_in_position_stability
from backend.services.plot_repetability_vision_glass_certificate import calculate_and_plot_repetability_after_error_map

from backend.services.image_shapness_calculation import image_shapness


class calibration_data_control:
    def __init__(self,ui):
        self.ui = ui #pass the ui instance to the controller
        self.hc = -1

        # table to save the values.
        self.calibration_data_table_row = 101
        self.calibration_data_table_column = 101
        self.no_of_axis = 3

        self.ui.calibration_data_table_create.clicked.connect(self.setup_calibration_data_table)
        self.ui.calibration_data_table_row_input.editingFinished.connect(self.calibration_data_table_row_input_edit_finished)
        self.ui.calibration_data_table_column_input.editingFinished.connect(self.calibration_data_table_column_input_edit_finished)

        self.ui.get_x_y_value_push_button.clicked.connect(self.get_x_y_value_push_button_clicked)
        self.ui.get_x_y_value_push_button.setEnabled(False)
        self.calibrate_data_table_selected_axis_bit = 0      # select x(0),y(1),z(2) data to show
        self.ui.display_coodinate_combo_box.currentIndexChanged.connect(self.handle_display_coodinate_combo_box_current_changed)

        self.ui.actionSave_dot_locations.triggered.connect(self.save_dot_locations_matrix)
        self.ui.actionOpen_dot_locations.triggered.connect(self.open_dot_lcoations_matrix)
        
        self.ui.auto_focus_button.clicked.connect(self.auto_focus_button_clicked)
        self.ui.dot_center_estimate_button.clicked.connect(self.estimate_dot_center_button_clicked)
        self.new_folder_path_centering = None
        self.axis_x_ui_controller = axis_x_ui_controller
        self.axis_y_ui_controller = axis_y_ui_controller
        self.axis_z_ui_controller = axis_z_ui_controller
        self.position_error_calculation_halcon = position_error_claculation()
        self.ui.dot_center_estimate_button.setEnabled(False)

        self.ui.move_to_position_push_button.clicked.connect(self.move_to_position_push_button_clicked)

        # Calculating grid locations 
        self.ui.calculate_grid_locations_push_button.clicked.connect(self.calculate_glass_scale_dot_locations)
        self.ui.calculate_grid_locations_push_button.setEnabled(False)

        # start scanning butten dissabling
        self.ui.scan_button.setEnabled(False)
            
        # keep file open and save locations
        self.save_file_path = None
        self.open_file_path = None
        self.new_folder_path = None

        self.ui.pitch_input_column_x.editingFinished.connect(self.pitch_input_column_x_edit_finished)
        self.ui.pitch_input_row_y.editingFinished.connect(self.pitch_input_row_y_edit_finished)
        self.ui.update_varible_pitch_button.clicked.connect(self.updata_variable_pitch_button_clicked)
        #self.test_interval = 1

        # UI for action select
        self.ui.select_action_combo_box.currentIndexChanged.connect(self.select_action_combo_box_current_changed)
        self.action_type = None

        # UI for ACS based error mapping file imports

        self.ui.file_input_1_button.clicked.connect(self.file_input_1_button_clicked)
        self.ui.file_input_1_button.setEnabled(False)
        self.ui.file_input_1_line_edit.setEnabled(False)

        self.ui.file_input_2_button.clicked.connect(self.file_input_2_button_clicked)
        self.ui.file_input_2_button.setEnabled(False)
        self.ui.file_input_2_line_edit.setEnabled(False)

        self.ui.file_input_3_button.clicked.connect(self.file_input_3_button_clicked)
        self.ui.file_input_3_button.setEnabled(False)
        self.ui.file_input_3_line_edit.setEnabled(False)

        self.ui.file_input_4_button.clicked.connect(self.file_input_4_button_clicked)
        self.ui.file_input_4_button.setEnabled(False)
        self.ui.file_input_4_line_edit.setEnabled(False)

        # Actions buttons 
        self.ui.run_action_button.clicked.connect(self.run_action_button_clicked)
        self.ui.run_action_button.setEnabled(False)

        # Image shapness calculation
        self.image_shapness = image_shapness()

        # Dot center calculation
        self.pixel_to_mm = None
        self.image_center_pixel_x = None
        self.image_center_pixel_y = None


        pass

#=========================================================
# select actions in with combo box after performaing test
#=========================================================
    def select_action_combo_box_current_changed(self):
        self.action_type = self.ui.select_action_combo_box.currentText()
        if self.action_type == None:
            print("None")
            self.ui.run_action_button.setEnabled(False)

        #1 self centering repeatability plot with laser test
        elif self.action_type == "Self centering repeatability plot":
            print(self.action_type)
            # enable wanted buttons
            self.ui.run_action_button.setEnabled(True)
            # enable file input buttons
            self.ui.file_input_1_button.setEnabled(True)
            self.ui.file_input_2_button.setEnabled(True)
            self.ui.file_input_3_button.setEnabled(True)
            self.ui.file_input_4_button.setEnabled(False)
            # change import file name
            # varible_pitch_file_location,laser_file_location,log_file_1d_error_mapping_test
            self.ui.file_input_1_button.setText("Import variable pitch matrix")
            self.ui.file_input_2_button.setText("Import Laser row data")
            self.ui.file_input_3_button.setText("Import 1D error map log file")
            self.ui.file_input_4_button.setText("")
            # remove unwated file paths
            self.ui.file_input_1_line_edit.setText("")
            self.ui.file_input_2_line_edit.setText("")
            self.ui.file_input_3_line_edit.setText("")
            self.ui.file_input_4_line_edit.setText("")
            # set the info text
            self.ui.info_text_edit.setText("Action: Plot repetability graph.\n" 
                                           "Test: 1D expantion X axis or 1D expantion Y axis with laser test\n"
                                           " 1. Variable pitch matrix file\n"
                                           " 2. Laser row data file\n"
                                           " 3. 1D error map log file")
        
        #2 Create glass scale certificate from laser data 
        elif self.action_type == "Create glass scale certificate":
            print(self.action_type)
            self.ui.run_action_button.setEnabled(True)
            
            self.ui.file_input_1_button.setEnabled(True)
            self.ui.file_input_2_button.setEnabled(True)
            self.ui.file_input_3_button.setEnabled(True)
            self.ui.file_input_4_button.setEnabled(False)
            
            # change import file name
             # varible_pitch_file_location,laser_file_location,log_file_1d_error_mapping_test
            self.ui.file_input_1_button.setText("Import variable pitch matrix")
            self.ui.file_input_2_button.setText("Import Laser row data")
            self.ui.file_input_3_button.setText("Import 1D error map log file")
            self.ui.file_input_4_button.setText("")
            # remove unwated file paths
            self.ui.file_input_1_line_edit.setText("")
            self.ui.file_input_2_line_edit.setText("")
            self.ui.file_input_3_line_edit.setText("")
            self.ui.file_input_4_line_edit.setText("")
            # set the info text
            self.ui.info_text_edit.setText("Action: Calculate glass scale certificate.\n" 
                                           "Test: 1D expantion X axis or 1D expantion Y axis with laser test\n"
                                           " 1. Laser row data file\n")
        
        #3 calculate error map values using vision and glass certificate and send to ACS
        elif self.action_type == "Calculate error map values-Vision":
            print(self.action_type)
            self.ui.run_action_button.setEnabled(True)

            self.ui.file_input_1_button.setEnabled(True)
            self.ui.file_input_2_button.setEnabled(False)
            self.ui.file_input_3_button.setEnabled(True)
            self.ui.file_input_4_button.setEnabled(False)
            # set text for import button
            self.ui.file_input_1_button.setText("Import Glass scale certificate")
            self.ui.file_input_2_button.setText("")
            self.ui.file_input_3_button.setText("Import 1D error map test log file")
            self.ui.file_input_4_button.setText("")
            # remove untanted text 
            self.ui.file_input_1_line_edit.setText("")
            self.ui.file_input_2_line_edit.setText("")
            self.ui.file_input_3_line_edit.setText("")
            self.ui.file_input_4_line_edit.setText("")
            # set the info text
            self.ui.info_text_edit.setText("Action: Calculate error map value using vision.\n" 
                                           "Test: 1D error map X axis\n"
                                           " 1. Glass certificate \n"
                                           " 2. 1D error map log file 1D error mapping test\n")
        
        #4 Generate 1D error map buffer-Laser
        elif self.action_type == "Generate 1D error map buffer-Laser":
            print(self.action_type)
            self.ui.run_action_button.setEnabled(True)

            self.ui.file_input_1_button.setEnabled(False)
            self.ui.file_input_2_button.setEnabled(True)
            self.ui.file_input_3_button.setEnabled(False)
            self.ui.file_input_4_button.setEnabled(False)
            # change import file name
            self.ui.file_input_1_button.setText("")
            self.ui.file_input_2_button.setText("Laser row data file")
            self.ui.file_input_3_button.setText("")
            self.ui.file_input_4_button.setText("")
            # remove unwated file paths
            self.ui.file_input_1_line_edit.setText("")
            self.ui.file_input_2_line_edit.setText("")
            self.ui.file_input_3_line_edit.setText("")
            self.ui.file_input_4_line_edit.setText("")
            # set the info text
            self.ui.info_text_edit.setText("Action: Calculate error correction values & send to ACS.\n" 
                                           "Test: 1D error mapping test X axis or 1D expantion Y axis with laser test\n"
                                           " 1. Laser row data file\n")    
        
        #5 - plotting thermal expantion test data 
        elif self.action_type == "Plot thermal expantion-Vision":
            print(self.action_type)
            self.ui.run_action_button.setEnabled(True)
            # file input buttons
            self.ui.file_input_1_button.setEnabled(False)
            self.ui.file_input_2_button.setEnabled(False)
            self.ui.file_input_3_button.setEnabled(True)
            self.ui.file_input_4_button.setEnabled(False)
            # change import file name
            self.ui.file_input_1_button.setText("")
            self.ui.file_input_2_button.setText("")
            self.ui.file_input_3_button.setText("Import log file expantion in position")
            self.ui.file_input_4_button.setText("")
            # remove unwated file paths
            self.ui.file_input_1_line_edit.setText("")
            self.ui.file_input_2_line_edit.setText("")
            self.ui.file_input_3_line_edit.setText("")
            self.ui.file_input_4_line_edit.setText("")
            # set the info text
            self.ui.info_text_edit.setText("Action: Plot variation in position due to temparature Expantion.\n" 
                                           "Test: Expantion in position static, or Expantion in position dynamic\n"
                                           " 1. Log_file_in_position_stability_dynamic\n")

        #6 - plotting repetability graph vision
        elif self.action_type == "Plot repetabilety graph vision":
            print(self.action_type)
            self.ui.run_action_button.setEnabled(True)
            # file input buttons
            self.ui.file_input_1_button.setEnabled(True)
            self.ui.file_input_2_button.setEnabled(False)
            self.ui.file_input_3_button.setEnabled(True)
            self.ui.file_input_4_button.setEnabled(False)
            # change import file name
            self.ui.file_input_1_button.setText("Import Glass scale certificate")
            self.ui.file_input_2_button.setText("")
            self.ui.file_input_3_button.setText("Import 1D error map test log file")
            self.ui.file_input_4_button.setText("")
            # remove unwated file paths
            self.ui.file_input_1_line_edit.setText("")
            self.ui.file_input_2_line_edit.setText("")
            self.ui.file_input_3_line_edit.setText("")
            self.ui.file_input_4_line_edit.setText("")
            # set the info text
            self.ui.info_text_edit.setText("Action: Plot repetability graph with vision values.\n" 
                                           "Test: 1D error map X or Y axis\n"
                                           " 1. Glass certificate\n")

    def run_action_button_clicked(self):
        if self.action_type == None:
            print("None")

        #1 self centering repeatability plot with laser test
        # input files : Variable pitch matrix file, Laser row data file, 1D error map log file
        elif self.action_type == "Self centering repeatability plot":
            if self.file_path_input_1 and self.file_path_input_2 and self.file_path_input_3:
                # plot the graph for self centering repeatability test and save the graph
                # input files: Variable pitch matrix file, Laser row data file, 1D error map log file
                calculate_actual_dot_seperation(self.file_path_input_1,self.file_path_input_2,self.file_path_input_3)
            elif self.file_input_1_line_edit == None or self.file_parth_laser_row_data == None or self.file_parth_log_file_1D_error_map == None:
                print("Error: Missing file paths")

        #2 Create glass scale certificate
        # input files : Laser row data file, variable pitch matrix file
        elif self.action_type == "Create glass scale certificate":
            
            print("Create glass scale certificate")
            if self.file_path_input_2 == None or self.file_path_input_1 == None:
                print("Error: Missing file paths")
            else:
                # generate certificat file to glass using laser data (need to intergrage vision data)
                # input files : Laser row data file, variable pitch matrix file, 1D error map log file
                generate_glass_certificate(self.file_path_input_2,self.file_path_input_1,self.file_path_input_3)  

        #3 Calculate error map values-Vision
        # input files : Glass certificate, 1D error map log file
        elif self.action_type == "Calculate error map values-Vision":
            
            print("Calculate error map values - Vision")
            if(self.file_path_input_1 == None or self.file_path_input_3 == None):
                print("Error: Missing file paths")
            elif  self.file_path_input_1 and self.file_path_input_3:
                #create_error_map_vision( glass_certificate_matrix,file_parth_log_file_1D_error_map,hc)
                create_error_map_buffer_from_glass_certificate_and_vision_files_and_send_to_acs(self.file_path_input_1,self.file_path_input_3,self.hc)  

        #4 Generate 1D error map buffer-Laser
        # input files : Laser row data file
        elif self.action_type == "Generate 1D error map buffer-Laser":
            
            print("Generate 1D error map buffer-Laser")
            if self.file_parth_laser_row_data == None or self.hc == -1:
                print("Error: Missing file paths")
            else:
                # generate certificat file to glass certificate folder
                create_error_map_buffer_from_laser_file_and_send_to_acs(self.file_parth_laser_row_data,self.hc) 
        
        #5 Plot thermal expantion-Vision 
        # input file: Log_file_in_position_stability_dynamic.csv
        elif self.action_type == "Plot thermal expantion-Vision":
            
            print("Plot thermal expantion-Vision")
            if self.file_path_input_3 == None:
                print("Error: Missing file paths")
            else:
                plot_in_position_stability(self.file_path_input_3)


        # 6 Generate error map plot and save it 
        # input files : Glass certificate, 1D error map log file
        elif self.action_type == "Plot repetabilety graph vision":
            
            print("Plot repetabilety graph vision")
            if(self.file_path_input_1 == None or self.file_path_input_3 == None):
                print("Error: Missing file paths")
            elif  self.file_path_input_1 and self.file_path_input_3:
                #create_error_map_vision( glass_certificate_matrix,file_parth_log_file_1D_error_map,hc)
                calculate_and_plot_repetability_after_error_map(self.file_path_input_1,self.file_path_input_3)



    def file_input_1_button_clicked(self):
        self.file_path_input_1 = open_file(self.ui)
        self.ui.file_input_1_line_edit.setText(self.file_path_input_1)
        
    def file_input_2_button_clicked(self):
        self.file_path_input_2 = open_file(self.ui)
        self.ui.file_input_2_line_edit.setText(self.file_path_input_2)

    def file_input_3_button_clicked(self):
        self.file_path_input_3 = open_file(self.ui)
        #print(self.file_parth_laser_row_data)
        self.ui.file_input_3_line_edit.setText(self.file_path_input_3)
    
    def file_input_4_button_clicked(self):
        self.file_path_input_4 = open_file(self.ui)
        #print(self.file_parth_log_file_1D_error_map)
        self.ui.file_input_4_line_edit.setText(self.file_path_input_4)



    def get_communication_enabler_status(self, hc):
        self.hc = hc
        #print(self.hc)
        self.ui.dot_center_estimate_button.setEnabled(True)
        
    # 1. Collecting and storing the glass jig dot positions
    ### Calibration table (glass calibration jig)
 
    def calibration_data_table_row_input_edit_finished(self):
        self.calibration_data_table_row = int(self.ui.calibration_data_table_row_input.text())
        if self.calibration_data_table_row < 3:
                self.calibration_data_table_row = 3
                self.ui.calibration_data_table_row_input.setText(str(self.calibration_data_table_row))
    # Note:
    # Need error massages for non intiger values, minus values and values bellow 3 

    def calibration_data_table_column_input_edit_finished(self):
        self.calibration_data_table_column = int(self.ui.calibration_data_table_column_input.text())
        if self.calibration_data_table_column < 3:
                self.calibration_data_table_column = 3
                self.ui.calibration_data_table_column_input.setText(str(self.calibration_data_table_column))

    def setup_calibration_data_table(self):
        # UI part
        self.ui.table_widget.setRowCount(self.calibration_data_table_row)
        self.ui.table_widget.setColumnCount(self.calibration_data_table_column)
        self.ui.table_widget.setHorizontalHeaderLabels([str(x) for x in range(self.calibration_data_table_row)])
        self.ui.table_widget.setVerticalHeaderLabels([str(x) for x in range(self.calibration_data_table_column)])
        for row in range (self.calibration_data_table_row):
            self.ui.table_widget.setRowHeight(row,20)
        for column in range (self.calibration_data_table_column):
            self.ui.table_widget.setColumnWidth(column,65)
        
        # makes all elements zero
        for row in range (self.calibration_data_table_row):
            for column in range (self.calibration_data_table_column):
                item = QTableWidgetItem(0)
                self.ui.table_widget.setItem(row,column,item)

        # create np array and mekes all elements zero
        self.create_position_map_np_array()

    # Dot location map
    def create_position_map_np_array(self):
        self.position_np_array = np.zeros((self.no_of_axis,self.calibration_data_table_row,self.calibration_data_table_column))
        self.ui.get_x_y_value_push_button.setEnabled(True)
        

    def get_x_y_value_push_button_clicked(self):

        self.selected_items = self.ui.table_widget.selectedItems()
        if len(self.selected_items) == 1 and self.hc >= 0 :
            # print(self.selected_items[0].row())
            # print(self.selected_items[0].column())
            x_pos = self.ui.axis_x_fpos_lable.text()
            y_pos = self.ui.axis_y_fpos_lable.text()
            z_pos = self.ui.axis_z_fpos_lable.text()
            
            # recode all the values in matrix
            self.position_np_array[0,self.selected_items[0].row(),self.selected_items[0].column()] = x_pos 
            self.position_np_array[1,self.selected_items[0].row(),self.selected_items[0].column()] = y_pos
            self.position_np_array[2,self.selected_items[0].row(),self.selected_items[0].column()] = z_pos

            # update the table based on radio button
            self.update_the_table()
            self.check_ability_to_estimate_locations()

        else:
            print("Error massage: More than one item selected")
            print("Error massage: controller not connected")

    def handle_display_coodinate_combo_box_current_changed(self):
        value = self.ui.display_coodinate_combo_box.currentText()
        if value == 'X axis':
            self.calibrate_data_table_selected_axis_bit = 0
        if value == 'Y axis':
            self.calibrate_data_table_selected_axis_bit = 1
        if value == 'Z axis':
            self.calibrate_data_table_selected_axis_bit = 2
        self.update_the_table()


    def update_the_table(self):
        for row in range (self.calibration_data_table_row):
            for column in range (self.calibration_data_table_column):
                item = QTableWidgetItem(str(self.position_np_array[self.calibrate_data_table_selected_axis_bit,row,column]))
                self.ui.table_widget.setItem(row,column,item)




    ## Save dot locations
    def save_dot_locations_matrix(self):
        file_dialog = QFileDialog(self.ui.centralwidget)
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setNameFilter("CSV files (*.csv)")  # can create only csv 
        if file_dialog.exec():
            file_paths = file_dialog.selectedFiles()
            for file_path in file_paths:
                # cannot save the 3D array have to reshape to 2D
                array_2d = self.position_np_array.reshape(-1, self.position_np_array.shape[-1])     
                np.savetxt(file_path, array_2d, delimiter=',', fmt='%.6f')      # save 2D file to .csv format
                print("Save file to:", file_path)

        if file_path:
            self.save_file_path = file_path  


           

    def open_dot_lcoations_matrix(self):
        file_dialog = QFileDialog(self.ui.centralwidget)
        file_dialog.setFileMode(QFileDialog.ExistingFile) 
        file_dialog.setNameFilter("CSV files (*.csv)")
        if file_dialog.exec():
            file_paths = file_dialog.selectedFiles()
            for file_path in file_paths:
                print("Selected file:", file_path)          # get the file locations

        if file_path:
            self.open_file_path = file_path
            print(file_path)
            array_2d = np.loadtxt(file_path, delimiter=',')
            rows_in_file,column = array_2d.shape
            self.calibration_data_table_row = rows_in_file//self.no_of_axis
            self.calibration_data_table_column = column
            self.create_position_map_np_array()     # create array
            self.setup_calibration_data_table()     # create grid ui
            # put the data to the matrix
            self.position_np_array = array_2d.reshape(self.no_of_axis,self.calibration_data_table_row,self.calibration_data_table_column)
            self.update_the_table()                 # update the table
            self.check_ability_to_estimate_locations()
            #print(self.position_np_array)


    def get_camera_instance(self, camera_instance):
        self.capture_image = camera_instance

    def create_new_folder(self):
        file_exicution_location_centering = os.getcwd()                                                       # get the current location
        self.parent_directory_centering = os.path.dirname(file_exicution_location_centering)                  # get the current location
        current_datetime_based_folder_name_centering = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")           # Getting data and time
        self.new_folder_path = os.path.join(self.parent_directory_centering, current_datetime_based_folder_name_centering)
        # Create the new folder
        os.makedirs(self.new_folder_path, exist_ok=True)
        print(self.new_folder_path)
        return self.new_folder_path

#===========================
# Auto focus button clicked 
#===========================
    def auto_focus_button_clicked(self):
        threasold = 1800

        # get image save folder location if None create new one
        if self.new_folder_path_centering == None:
            self.new_folder_path_centering = self.create_new_folder()
        
        #capture image
        imagename = "auto_focus.png"
        full_file_path_auto_focus_image =  os.path.join(self.new_folder_path_centering,imagename)
        self.capture_image.save_frame(full_file_path_auto_focus_image)   # send full file parth to

        variance, status = self.image_shapness.detect_sharpness_sobel(full_file_path_auto_focus_image,threasold)
        print("variance:",variance, "status:",status)

#===========================
# Calculate dot 
#===========================

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


    def estimate_dot_center_button_clicked(self):



        if self.pixel_to_mm == None:
                self.pixel_to_mm = float(self.read_recipe_csv("pixel_to_mm"))
                if self.pixel_to_mm == None:
                    #print("Error: circle radius not found in the recipe file.")    
                    self.pixel_to_mm = 0.001168674                    # if recipe file not found, assign default value PBA lens with 12MP cam
                    #print("Assined default value: ",self.pixel_to_mm)
                else:
                    print("Assined pixel_to_mm from recipe file: ",self.pixel_to_mm)
        

        # obtaining image center pixel values from recipe file
        if self.image_center_pixel_x == None or self.image_center_pixel_y == None:
            self.image_center_pixel_x = int(self.read_recipe_csv("image_center_pixel_x"))
            self.image_center_pixel_y = int(self.read_recipe_csv("image_center_pixel_y"))
            if self.image_center_pixel_x == None or self.image_center_pixel_y == None:
                #print("Error: image center pixel not found in the recipe file.")    
                self.image_center_pixel_x = 2048
                self.image_center_pixel_y = 1500
                #print("Assined default value: ",self.image_center_pixel_x,self.image_center_pixel_y)
            else:
                print("Assined image center pixel from recipe file: ",self.image_center_pixel_x,self.image_center_pixel_y)
        
    
        # get image save folder location if None create new one
        if self.new_folder_path_centering == None:
            self.new_folder_path_centering = self.create_new_folder()

        # get axis positions

        x_pos = self.ui.axis_x_fpos_lable.text()
        y_pos = self.ui.axis_y_fpos_lable.text()
        z_pos = self.ui.axis_z_fpos_lable.text()

        #capture image
        imagename = f"{x_pos}_{y_pos}_{z_pos}.png"
        full_file_path_centering_image =  os.path.join(self.new_folder_path_centering,imagename)
        self.capture_image.save_frame(full_file_path_centering_image)   # send full file parth to

        # Clculating PE using halcon 
        image_parameters = self.position_error_calculation_halcon.calculate_center(full_file_path_centering_image)
        print("Image parameters:", image_parameters)
        y_position_error = (image_parameters[0] - self.image_center_pixel_y)*self.pixel_to_mm     # 1024 # for 5mp camera
        x_position_error = (image_parameters[1] - self.image_center_pixel_x)*self.pixel_to_mm     # 1296
        # radius_of_target = image_parameters[2]*pixel_to_mm*1000  # unwanterd radius value in um
        correction_value_y = float(y_pos) + y_position_error # correction value in mm axis Y and image Y in same direction
        correction_value_x = float(x_pos) + x_position_error # correction value in mm axis X and image X in same direction
        print(correction_value_x ,correction_value_y)
        self.ui.axis_x_set_position_line_edit.setText(str(round(correction_value_x,6)))
        self.ui.axis_y_set_position_line_edit.setText(str(round(correction_value_y,6)))
        


    # More to location button click 
    # Get the seleted position
    # update the actual value in UI X,Y,Z coordinate next positon set value
    def move_to_position_push_button_clicked(self):
        #print("Note: error")
        self.selected_items = self.ui.table_widget.selectedItems()
        if self.selected_items:
            self.ui.axis_x_set_position_line_edit.setText(str(self.position_np_array[0,self.selected_items[0].row(),self.selected_items[0].column()]))
            self.ui.axis_y_set_position_line_edit.setText(str(self.position_np_array[1,self.selected_items[0].row(),self.selected_items[0].column()]))
            self.ui.axis_z_set_position_line_edit.setText(str(self.position_np_array[2,self.selected_items[0].row(),self.selected_items[0].column()]))

        else:
            print("item not selected")

        #print(self.position_np_array[0,self.selected_items[0].row(),self.selected_items[0].column()])
        #print(self.position_np_array[1,self.selected_items[0].row(),self.selected_items[0].column()])


    # Dot matrix calculation stage #(Docs @ "Creating grid location" in readme)
    # Check the posibility to calculate the positions 



    def check_ability_to_estimate_locations(self):
        print("cheacking started")
        # start cheking how many non zero points are in the array in x,y
        non_zero_x = np.nonzero(self.position_np_array[0,:,:])
        non_zero_y = np.nonzero(self.position_np_array[1,:,:])
        # check the data is not corrupted
        nonzero_points_x = list(zip(non_zero_x[0], non_zero_x[1]))
        nonzero_points_y = list(zip(non_zero_y[0], non_zero_y[1]))
        if nonzero_points_x == nonzero_points_y:
            print(nonzero_points_x)
            if len(nonzero_points_x) == 3:
                print("Possible to calculate with",len(nonzero_points_x),"points")
                x_points = [(i, j) for i, j in zip(non_zero_x[0], non_zero_x[1])]
                self.nonzero_points = np.array(x_points)
                self.matrix_calculation_method_select_check()
            else:
                print("In sufficent locations.") 
                self.ui.calculate_grid_locations_push_button.setEnabled(False)
        else: 
            print("Location matrix is has mis allinged X and Y values")
            self.ui.calculate_grid_locations_push_button.setEnabled(False)

# **3_dot_method** 
# During the 3 dot method  
# 1. We have to check the row, colum values are perpendiculer. Othersize dot locations can be any location.
# 2. Then we have to check the dot location (actual x and y values of the matrix) are perpendiculer. To do that we create a line(in mathamatics )   
# 3. Then we can calculate the rest of the matrix.

    def matrix_calculation_method_select_check(self):
        #for items in self.nonzero_points:
            #print(items)
            #print(self.nonzero_points)

        (x1, y1), (x2, y2), (x3, y3) = self.nonzero_points
        # Consider middle point(B or X2,Y2) is the 90 digree coner. 
        # Calculate vectors AB and BC (It is more sutable BA and BC)
        AB = (x2 - x1, y2 - y1)
        BC = (x3 - x2, y3 - y2)
        # Calculate dot product
        dot_product = AB[0] * BC[0] + AB[1] * BC[1]
        #print(dot_product)
        
        # Check if the dot product is zero
        if dot_product == 0:
            #print("The selected points are perpendicular.")
            # Calculation actual dot location values are perpendiculertity
            CD = (self.position_np_array[0,x2,y2] - self.position_np_array[0,x1,y1], self.position_np_array[1,x2,y2] - self.position_np_array[1,x1,y1] )
            DE = (self.position_np_array[0,x3,y3] - self.position_np_array[0,x2,y2], self.position_np_array[1,x3,y3] - self.position_np_array[1,x2,y2] )
            magniture_CD = np.sqrt(CD[0]**2 + CD[1]**2) 
            magniture_DE = np.sqrt(DE[0]**2 + DE[1]**2)
            dot_product_actual = CD[0] * DE[0] + CD[1] * DE[1]
            #print(CD,DE)
            cos_theta = dot_product_actual/(magniture_CD * magniture_DE)
            theta = math.degrees(math.acos(cos_theta))
            # The value is get from actual testing we can increase this up to 87 to 92
            # 
            if 89.5<theta<90.5:
                print("Selected glass markers are perpendiculer (Theta =",theta,")")
                self.ui.calculate_grid_locations_push_button.setEnabled(True)
            else:
                print("Selected glass markers are not perpendiculer (theta =",theta,  ")")
                self.ui.calculate_grid_locations_push_button.setEnabled(False)
                self.ui.scan_button.setEnabled(False)
        else:
            print("The points are not perpendicular.")
            self.ui.calculate_grid_locations_push_button.setEnabled(False)
            self.ui.scan_button.setEnabled(False)


    def calculate_glass_scale_dot_locations(self):
        # Get copy of user input ref values
        self.position_np_array_ref = np.copy(self.position_np_array)
        # Calculating only for middle point(B or X2,Y2) is the 90 digree coner.
        (x1, y1), (x2, y2), (x3, y3) = self.nonzero_points
        column_difference = y3 - y2
        row_difference = x2 -x1

        x_direction_distance_bitween_column = (self.position_np_array[0,x3,y3] - self.position_np_array[0,x2,y2])/column_difference
        y_direction_distance_bitween_column = (self.position_np_array[1,x3,y3] - self.position_np_array[1,x2,y2])/column_difference
        z_direction_distance_bitween_column = (self.position_np_array[2,x3,y3] - self.position_np_array[2,x2,y2])/column_difference
        
        x_direction_distance_bitween_row    = (self.position_np_array[0,x2,y2] - self.position_np_array[0,x1,y1])/row_difference
        y_direction_distance_bitween_row    = (self.position_np_array[1,x2,y2] - self.position_np_array[1,x1,y1])/row_difference
        z_direction_distance_bitween_row    = (self.position_np_array[2,x2,y2] - self.position_np_array[2,x1,y1])/row_difference
        
        # only works work if we only selected x1,y1 as 0,0 position ??
        # rows and column values should represent Y and X axis directions. but in hear its row and column are X and Y.  
        for rows in range (0,self.calibration_data_table_row,1):
            for column in range (0,self.calibration_data_table_column,1):
                self.position_np_array[0,rows,column] = round(self.position_np_array[0,x1,y1] + x_direction_distance_bitween_column*column  + x_direction_distance_bitween_row*rows,6)       # X axis
                self.position_np_array[1,rows,column] = round(self.position_np_array[1,x1,y1] + y_direction_distance_bitween_column*column  + y_direction_distance_bitween_row*rows,6)       # Y axis
                self.position_np_array[2,rows,column] = round(self.position_np_array[2,x1,y1] + z_direction_distance_bitween_column*column  + z_direction_distance_bitween_row*rows,6)       # Y axis

        self.update_the_table()
        self.ui.scan_button.setEnabled(True)


    # get the newly created file parth related to 
    def get_new_instance_folder_location(self,new_folder_path):
        self.new_folder_path = new_folder_path


    # Send the data value
    def send_array_data(self):
        return self.position_np_array
    
    def send_array_data_ref(self):
        return self.position_np_array_ref
    
    # Send the data value
    #def send_open_file_parth(self):
    #    return self.open_file_path
    
    # Send the data value
    #def send_save_file_parth(self):
    #    return self.save_file_path


    # ==========================
    # Variable pitch  matrix
    # ==========================

    def pitch_input_column_x_edit_finished(self):
        self.new_pitch_column_x = int(self.ui.pitch_input_column_x.text())
        print(self.new_pitch_column_x)


    def pitch_input_row_y_edit_finished(self):
        self.new_pitch_row_y = int(self.ui.pitch_input_row_y.text())
        print(self.new_pitch_row_y)

            ## Save dot locations
    def save_location_matrix(self,location_array):
        file_dialog = QFileDialog(self.ui.centralwidget)
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setNameFilter("CSV files (*.csv)")  # can create only csv 
        if file_dialog.exec():
            file_paths = file_dialog.selectedFiles()
            for file_path in file_paths:
                # cannot save the 3D array have to reshape to 2D
                array_2d = location_array.reshape(-1, location_array.shape[-1])     
                np.savetxt(file_path, array_2d, delimiter=',', fmt='%.6f')      # save 2D file to .csv format
                print("Save file to:", file_path)

        if file_path:
            self.save_file_path = file_path 


    def updata_variable_pitch_button_clicked(self):
        variable_pitch_np_array = self.create_variable_pitch_matrix(self.position_np_array,self.new_pitch_row_y,self.new_pitch_column_x)
        self.save_location_matrix(variable_pitch_np_array)
        #print(variable_pitch_np_array.shape)


    # ==================================================================
    # Variable pitch matrix for laser with overrun !!! not in use
    # ===================================================================

    def create_variable_pitch_matrix_for_laser(self,calculated_position_np_array,pitch_row,pitch_column):
        number_of_axis = calculated_position_np_array.shape[0]
        number_of_columns = calculated_position_np_array.shape[1]
        number_of_rows = calculated_position_np_array.shape[2]

        # 1. getting intermidate matrix dimentions
        row = 0
        variable_pitch_matrix_row = 0


        for row in range (1,number_of_rows,pitch_row):
            variable_pitch_matrix_row = variable_pitch_matrix_row +1

        row = row +1 
        variable_pitch_matrix_row = variable_pitch_matrix_row + 1 

        # 2. creating intermidate matrix
        variable_pitch_intermediate_matrx_shape = [number_of_axis,number_of_columns,variable_pitch_matrix_row+1]
        variable_pitch_intermediate_matrx = np.zeros(variable_pitch_intermediate_matrx_shape)
        print(variable_pitch_intermediate_matrx.shape)

        # 3. Update position values from calculated_position_np_array to variable_pitch_intermediate_matrx
        row = 0
        variable_pitch_matrix_row = 0
        for x in range (0,number_of_columns,1):
            variable_pitch_intermediate_matrx[0][x][variable_pitch_matrix_row] = calculated_position_np_array[0][x][row]
            variable_pitch_intermediate_matrx[1][x][variable_pitch_matrix_row] = calculated_position_np_array[1][x][row]
            variable_pitch_intermediate_matrx[2][x][variable_pitch_matrix_row] = calculated_position_np_array[2][x][row]

        for row in range (1,number_of_rows,pitch_row):
            variable_pitch_matrix_row = variable_pitch_matrix_row +1
            for x in range (0,number_of_columns,1):
                variable_pitch_intermediate_matrx[0][x][variable_pitch_matrix_row] = calculated_position_np_array[0][x][row]
                variable_pitch_intermediate_matrx[1][x][variable_pitch_matrix_row] = calculated_position_np_array[1][x][row]
                variable_pitch_intermediate_matrx[2][x][variable_pitch_matrix_row] = calculated_position_np_array[2][x][row]

        row = row +1 
        variable_pitch_matrix_row = variable_pitch_matrix_row + 1 
        for x in range (0,number_of_columns,1):
            variable_pitch_intermediate_matrx[0][x][variable_pitch_matrix_row] = calculated_position_np_array[0][x][row]
            variable_pitch_intermediate_matrx[1][x][variable_pitch_matrix_row] = calculated_position_np_array[1][x][row]
            variable_pitch_intermediate_matrx[2][x][variable_pitch_matrix_row] = calculated_position_np_array[2][x][row]

        # 4. getting final matrix dimentions 
        column = 0
        variable_pitch_matrix_column = 0

        for column in range (1,number_of_columns,pitch_column):
            variable_pitch_matrix_column = variable_pitch_matrix_column +1

        column = column +1 
        variable_pitch_matrix_column = variable_pitch_matrix_column + 1 

        # 5. Creating final matrix
        variable_pitch_matrx_shape = [number_of_axis,variable_pitch_matrix_column+1,variable_pitch_matrix_row+1]
        variable_pitch_matrix = np.zeros(variable_pitch_matrx_shape)
        #print(variable_pitch_matrix.shape)


        # 6. update position values from variable variable_pitch_intermediate_matrx to variable_pitch_matrix
        column = 0
        variable_pitch_matrix_column = 0
        #print(column,variable_pitch_matrix_column)
        for x in range (0,variable_pitch_intermediate_matrx_shape[2],1):
            variable_pitch_matrix[0][variable_pitch_matrix_column][x] = variable_pitch_intermediate_matrx[0][column][x]
            variable_pitch_matrix[1][variable_pitch_matrix_column][x] = variable_pitch_intermediate_matrx[1][column][x]
            variable_pitch_matrix[2][variable_pitch_matrix_column][x] = variable_pitch_intermediate_matrx[2][column][x]

        for column in range (1,number_of_columns,pitch_column):
            variable_pitch_matrix_column = variable_pitch_matrix_column +1
            for x in range (0,variable_pitch_intermediate_matrx_shape[2],1):  
                #print(column,variable_pitch_matrix_column,x)  
                variable_pitch_matrix[0][variable_pitch_matrix_column][x] = variable_pitch_intermediate_matrx[0][column][x]
                variable_pitch_matrix[1][variable_pitch_matrix_column][x] = variable_pitch_intermediate_matrx[1][column][x]
                variable_pitch_matrix[2][variable_pitch_matrix_column][x] = variable_pitch_intermediate_matrx[2][column][x]

        column = column +1 
        variable_pitch_matrix_column = variable_pitch_matrix_column + 1
        for x in range (0,variable_pitch_intermediate_matrx_shape[2],1):
            #print(column,variable_pitch_matrix_column,x)
            variable_pitch_matrix[0][variable_pitch_matrix_column][x] = variable_pitch_intermediate_matrx[0][column][x]
            variable_pitch_matrix[1][variable_pitch_matrix_column][x] = variable_pitch_intermediate_matrx[1][column][x]
            variable_pitch_matrix[2][variable_pitch_matrix_column][x] = variable_pitch_intermediate_matrx[2][column][x]

        return variable_pitch_matrix

    # ==================================================================
    # Variable pitch  matrix for laser finishing - not in use
    # ==================================================================

    # ==================================================================
    # Create variable pitch matrix for optics system - without overrun
    # ==================================================================

    def create_variable_pitch_matrix(self,calculated_position_np_array,pitch_row,pitch_column):
        number_of_axis = calculated_position_np_array.shape[0]
        number_of_columns = calculated_position_np_array.shape[1]
        number_of_rows = calculated_position_np_array.shape[2]

        # 1. getting intermidate matrix dimentions
        row = 0
        variable_pitch_matrix_column = (int(number_of_columns) // int(pitch_column)) + 1
        variable_pitch_matrix_row    = (int(number_of_rows) // int(pitch_row)) + 1

        print("variable_pitch_matrix_row:",variable_pitch_matrix_column)


        # 2. Calcualte variable pitch matrix dimentions
        variable_pitch_intermediate_matrx_shape = [number_of_axis,variable_pitch_matrix_row,variable_pitch_matrix_column]
        variable_pitch_matrix = np.zeros(variable_pitch_intermediate_matrx_shape)
        print(variable_pitch_matrix.shape)

        # 3. Update position values from calculated_position_np_array to variable_pitch_intermediate_matrx
        variable_pitch_matrix_column = 0
        variable_pitch_matrix_row = 0

        for row in range (0,number_of_rows,pitch_row):
            variable_pitch_matrix_column = 0
            for column in range (0,number_of_columns,pitch_column):
                variable_pitch_matrix[0][variable_pitch_matrix_row][variable_pitch_matrix_column] = calculated_position_np_array[0][row][column]
                variable_pitch_matrix[1][variable_pitch_matrix_row][variable_pitch_matrix_column] = calculated_position_np_array[1][row][column]
                variable_pitch_matrix[2][variable_pitch_matrix_row][variable_pitch_matrix_column] = calculated_position_np_array[2][row][column]
                variable_pitch_matrix_column = variable_pitch_matrix_column +1

            variable_pitch_matrix_row = variable_pitch_matrix_row +1

        # print ("variable_pitch_matrix:",variable_pitch_matrix)  

        return variable_pitch_matrix

    # =======================
    # Variable pitch matrix
    # =======================

