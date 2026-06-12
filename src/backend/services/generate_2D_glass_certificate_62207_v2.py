# /src/backend/services/generate_2d_glass_certificate_62207.py
# Issue:#37
# Generate glass certificate 62207
# files required : location_matrix_file.csv,vision_log_file.csv
# output : glass_certificate.csv

# this method was not correct 2025.01.08 : only laser data is used to generate the glass certificate
# I need to use vision data also to generate the glass certificate

import numpy as np
import pandas as pd
import csv
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import cv2
import halcon as ha



# =================================
# Algorithm Performance Analysis
# =================================

import functools
import time
import tracemalloc

# --- Log output directory (project root / logs/) ---
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
_LOG_DIR = os.path.join(_PROJECT_ROOT, "logs")

# --- Step 1: Create a Decorator for Timing ---
# A decorator is a function that wraps another function to add functionality.
Test_name = "without_pixel_sum_calculation_with_second_dataset"
images_used_for_test = 453

def profile_performance(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"--- Profiling '{func.__name__}' ---")
        tracemalloc.start()
        before_current, before_peak = tracemalloc.get_traced_memory()
        start_time = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            end_time = time.perf_counter()
            after_current, after_peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            duration_ms = (end_time - start_time) * 1000
            memory_increase = (after_current - before_current) / (1024 ** 2)
            peak_usage = after_peak / (1024 ** 2)
            print(f"--- Finished '{func.__name__}' in {duration_ms:.2f} ms ---")
            print(f"Memory before: {before_current / 1024:.2f} KiB")
            print(f"Memory after: {after_current / 1024:.2f} KiB")
            print(f"Memory increase: {memory_increase:.2f} MiB")
            print(f"Peak usage: {peak_usage:.2f} MiB")

            # save to file
            os.makedirs(_LOG_DIR, exist_ok=True)
            with open(os.path.join(_LOG_DIR, "performance_profile_log.csv"), "a+") as f:
                # f.write(f"DateTime,Function,TestName,Images Used for Test,Execution Time (ms),Memory Increase (MiB),Peak Memory Usage (MiB)\n")
                f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')},{func.__name__},{Test_name},{images_used_for_test},{duration_ms:.2f},{memory_increase:.2f},{peak_usage:.2f}\n")

    return wrapper




class generate_glass_certificate:
    def __init__(self):
        #self.get_dot_center = multi_dot_center_calculation()
        self.pixel_to_mm = None
        self.image_center_pixel_x = None
        self.image_center_pixel_y = None
        self.dot_pitch_in_pix = None 
        self.circle_radius_tolerance = None
        self.circle_radius = None
        self.image_brightness_threshold_value = None # 100  # default value, can be changed in recipe file
        self.right_adjacent,self.left_adjacent, self.top_adjacent, self.bottom_adjacent = None, None, None, None
        pass

    def read_recipe_csv(self,parameter):
        # get current working directory
        file_path = os.getcwd()  # get the current location
        #print("Current working directory : ",file_path)
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
        

    # Open file as 2D pandas and convert to numpy array : for log file
    def open_file_pandas_convert_numpy(self, file_location):
        pandas_df = pd.read_csv(file_location)
        #print heder file 
        #print(pandas_df.head())
        # Convert the DataFrame to a numpy array
        numpy_array = pandas_df.to_numpy()
        
        return numpy_array, numpy_array.shape


    def get_start_end_row_column_index(self, data):
        '''Get the start and end row and column index of the data'''
        # get the start and end row index
        self.start_row_index_y = min(data[:, 3])   # Y position
        self.end_row_index_y = max(data[:, 3])     # Y position

        # get the start and end column index
        self.start_column_index_x = min(data[:, 4])   # X position
        self.end_column_index_x = max(data[:, 4])     # X position

        # get number of cycles
        self.number_of_cycles = max(data[:, 1]) +1
        

    def create_glass_certificate_62207_matrix(self,array_shape):
        # Define the data
        new_array = np.zeros(array_shape)
        self.glass_certificate_array_shape = array_shape
        return new_array
    
    # =========================================================
    # Image index based dot prediction by convention
    # =========================================================
    def calculate_adjacent_index(self,row_index_y,column_index_x):
        '''Calculate the adjacent index of the row and column index'''

        self.image_center_pixel_x       # 2048
        self.image_center_pixel_y       # 1500
        self.dot_pitch_in_pix           # 857
        self.circle_radius_tolerance    # 50

        adjacent_dots_expected = {
            "Left":     (self.image_center_pixel_x - self.dot_pitch_in_pix, self.image_center_pixel_y),
            "Right":    (self.image_center_pixel_x + self.dot_pitch_in_pix, self.image_center_pixel_y),
            "Top":      (self.image_center_pixel_x, self.image_center_pixel_y - self.dot_pitch_in_pix),
            "Bottom":   (self.image_center_pixel_x, self.image_center_pixel_y + self.dot_pitch_in_pix)
        }

        # define detected adjacent dots dictionary
        detected_adjacent_dots = {}

        # get the adjacent index
        
        if column_index_x -1 < 0: # matrix array start from 0
            left_adjacent = 0   # dont have left adjacent dot
            detected_adjacent_dots["Left"] = None
        else:
            left_adjacent = 1
            detected_adjacent_dots["Left"] = (adjacent_dots_expected["Left"], 0)
            
        if column_index_x +1 >= self.glass_certificate_array_shape[1]:
            right_adjacent = 0
            detected_adjacent_dots["Right"] = None
        else:
            right_adjacent = 1
            detected_adjacent_dots["Right"] = (adjacent_dots_expected["Right"], 1)

        if row_index_y -1 < 0:  # matrix array start from 0
            top_adjacent = 0
            detected_adjacent_dots["Top"] = None
        else:
            top_adjacent = 1
            detected_adjacent_dots["Top"] = (adjacent_dots_expected["Top"], 3)
        
        if row_index_y +1 >= self.glass_certificate_array_shape[2]:
            bottom_adjacent = 0
            detected_adjacent_dots["Bottom"] = None
        else:   
            bottom_adjacent = 1
            detected_adjacent_dots["Bottom"] = (adjacent_dots_expected["Bottom"], 4)

        # print(row_index_y,column_index_x)
        # print(right_adjacent,left_adjacent, top_adjacent, bottom_adjacent)
        # print(detected_adjacent_dots)
        return left_adjacent, right_adjacent, top_adjacent, bottom_adjacent, detected_adjacent_dots
    


    
    def create_full_file_path(self,ref_file_location, file_name):
        file_path = os.path.dirname(ref_file_location)
        file_path_name = os.path.join(file_path,file_name)
        return file_path_name


    # =========================
    # image processing function
    # =========================

    def open_calibration_data(self,calibration_file):

        try:
            with np.load(calibration_file) as data:
                mtx = data['mtx']
                dist = data['dist']
                rvecs = data['rvecs']
                tvecs = data['tvecs']
            # print(f"Calibration data loaded from '{calibration_file}'")
            # print(f"Camera matrix : {mtx}\ndist : {dist}\nrvecs : {rvecs}\ntvecs : {tvecs}")
            return mtx, dist, rvecs, tvecs
        except Exception as e:
            print(f"Error loading calibration data from '{calibration_file}': {e}")
            return None, None, None, None


    def create_undistort_image(self,image_files_path, mtx, dist, mtx0):

        base_path = os.path.dirname(image_files_path)

        try:
            # read image
            img = cv2.imread(image_files_path)

            # Check if the image was successfully loaded
            if img is None:
                raise ValueError(f"Could not read image from {image_files_path}")

            # undistort image
            undistort_image = cv2.undistort(img, mtx, dist, None, mtx0)

            # save undistorted image with corresponding index
            undistorted_file_name = os.path.join(base_path, "undist.png")
            cv2.imwrite(undistorted_file_name, undistort_image)
            #print(f"Saved undistorted image: {undistorted_file_name}")
            return undistorted_file_name

        except Exception as e:
            print(f"Error processing file {image_files_path}: {e}")


    def get_peak_values_ranges(self, value_sum, threshold=5):
        peak_start = []
        peak_end = []
        in_peak = False

        for i in range(len(value_sum)):
            if value_sum[i] > threshold and not in_peak:
                peak_start.append(i)
                in_peak = True
            elif value_sum[i] <= threshold and in_peak:
                peak_end.append(i)
                in_peak = False

        # Handle case where a peak is at the end of the value_sum
        if in_peak:
            peak_end.append(len(value_sum))

        if len(peak_start) != len(peak_end):
            # This should not happen in ideal cases, but handle it for robustness
            min_len = min(len(peak_start), len(peak_end))
            peak_start = peak_start[:min_len]
            peak_end = peak_end[:min_len]

        peak_ranges = []
        for i in range(len(peak_start)):
            if peak_end[i] - peak_start[i] > 210:  # Ensure it's a valid range and removing half dot
                peak_ranges.append((peak_start[i], peak_end[i]))

        #print(f"peaks ranges: {peak_ranges}")
        return peak_ranges


    def get_dot_center_location(self, row_peak_ranges, column_peak_ranges):
        dot_center_location = []
        for row_start, row_end in row_peak_ranges:
            row_center = (row_start + row_end) // 2
            for col_start, col_end in column_peak_ranges:
                col_center = (col_start + col_end) // 2
                dot_center_location.append((col_center, row_center)) # (x, y) format

        return dot_center_location


#    def identify_index_dot_center_location(self, dot_center_location):
#        predicted_center_x_expected = 1297
#        predicted_center_y_expected = 1024
#        index_dot_center_x = None
#        index_dot_center_y = None
#
#        for i, (detected_x, detected_y) in enumerate(dot_center_location):
#            distance = np.sqrt((predicted_center_x_expected - detected_x)**2 + (predicted_center_y_expected - detected_y)**2)
#            if distance < 50:
#                #print(f"Dot {i + 1}: ({detected_x}, {detected_y})")
#                index_dot_center_x = detected_x
#                index_dot_center_y = detected_y
#
#        if index_dot_center_x is not None and index_dot_center_y is not None:
#            return index_dot_center_x, index_dot_center_y
#        else:
#            return predicted_center_x_expected, predicted_center_y_expected
#

    def get_adgent_dot_location(self, dot_center_location):
        # get center dot location and 4 adjacent dot locations
        # center dot location is the (1297, 1024) and 4 adjacent dot locations are (1296, 1024), (1298, 1024), (1297, 1023), (1297, 1025)
        self.image_center_pixel_x       # 2048
        self.image_center_pixel_y       # 1500
        self.dot_pitch_in_pix           # 857
        self.circle_radius_tolerance    # 50
        # Calculate expected adjacent dot locations based on the center dot location
        # Assuming the dot pitch is the same in both directions
        # Adjust the expected locations based on the dot pitch
        adjacent_dots_expected = {
            "Left":     (self.image_center_pixel_x - self.dot_pitch_in_pix, self.image_center_pixel_y),
            "Right":    (self.image_center_pixel_x + self.dot_pitch_in_pix, self.image_center_pixel_y),
            "Top":      (self.image_center_pixel_x, self.image_center_pixel_y - self.dot_pitch_in_pix),
            "Bottom":   (self.image_center_pixel_x, self.image_center_pixel_y + self.dot_pitch_in_pix)
        }

        detected_adjacent_dots = {}


        for adj_name, expected_loc in adjacent_dots_expected.items():
            best_match_dot_index = None
            min_distance = float('inf')

            for i, (detected_x, detected_y) in enumerate(dot_center_location):
                distance = np.sqrt((expected_loc[0] - detected_x)**2 + (expected_loc[1] - detected_y)**2)
                if distance < min_distance and distance < self.circle_radius_tolerance:
                    min_distance = distance
                    best_match_dot_index = i

            if best_match_dot_index is not None:
                detected_adjacent_dots[adj_name] = (dot_center_location[best_match_dot_index], best_match_dot_index + 1) # Store location and original index


        # return the detected adjacent dots
        return detected_adjacent_dots





    def pre_processing(self,image_path):

        # 1. read the image and convert to binary
        self.image_path = image_path
        cv_image  = cv2.imread(self.image_path)

        if cv_image is None:
            print(f"Error: Could not read image at {self.image_path}")
            return []

        # Convert to grayscale
        gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        # thresholding to create a binary image values less than 100 set to 0 and greater than 100 set to 255
        thresh_value = self.image_brightness_threshold_value    # 70, 100
        _, binary_image = cv2.threshold(gray_image, thresh_value, 255, cv2.THRESH_BINARY_INV)

        inverted_binary_image_bitwise_cv = cv2.bitwise_not(binary_image)

       # Visualize the binary image
        # plt.figure(figsize=(8, 6))
        # plt.title("Binary Image")
        # plt.imshow(inverted_binary_image_bitwise_cv, cmap='gray')
        # plt.axis('off')  # Turn off axis labels
        # plt.show()

        # 2. calculate the row values and column values
        row_sum = np.sum(inverted_binary_image_bitwise_cv, axis=1)
        col_sum = np.sum(inverted_binary_image_bitwise_cv, axis=0)
        

        # 3. output range of values higher than threshold and remove half dot
        row_peak_ranges = self.get_peak_values_ranges(row_sum, threshold=5000) # Adjusted threshold for row_sum
        column_peak_ranges = self.get_peak_values_ranges(col_sum, threshold=5000) # Adjusted threshold for col_sum
        # print(f"Row Peak Ranges: {row_peak_ranges}")
        # print(f"Column Peak Ranges: {column_peak_ranges}")

        # 4. get the center of the image
        dot_center_location = self.get_dot_center_location(row_peak_ranges, column_peak_ranges)

        # print the dot center locations one by one
#        for i, (center_x, center_y) in enumerate(dot_center_location):
#            print(f"Dot {i + 1}: ({center_x}, = {center_y})")

        # identify the index dot center location
        #index_dot_center_x, index_dot_center_y = self.identify_index_dot_center_location(dot_center_location)


        # 5. get center dot location and 4 adjacent dot locations
        detected_adjacent_dots = self.get_adgent_dot_location(dot_center_location)

        return detected_adjacent_dots

        # calcuate dot cneter location using Halcon



    def calculate_dot_center_location_using_halcon(self,image_path, dot_center_x_expected, dot_center_y_expected):
         
        
        # halcon xld based image center calculation
        self.image = ha.read_image(image_path)
        self.width,self.height=ha.get_image_size_s(self.image)
        #print(self.width,self.height)

        # define the dot location
        Define_Circle_Row = dot_center_y_expected   #1024  
        Define_Circle_Column = dot_center_x_expected    #1298
        ha.gen_cross_contour_xld ( Define_Circle_Row, Define_Circle_Column, 30, 0.785398)
        

        MetrologyHandle = ha.create_metrology_model()
        ha.set_metrology_model_image_size (MetrologyHandle, self.width, self.height)
        # MetrologyCircleIndices = ha.add_metrology_object_circle_measure (MetrologyHandle, Define_Circle_Row , Define_Circle_Column, CircleInitRadius, CircleRadiusTolerance, Thichness_of_the_box, sigma, measure_threshold, ['measure_distance'], [50] )
        MetrologyCircleIndices = ha.add_metrology_object_circle_measure (MetrologyHandle, Define_Circle_Row , Define_Circle_Column, self.circle_radius, self.circle_radius_tolerance, 20, 0.4, 1.8, ['measure_distance'], [40] ) # 20,1.5,1.8
        ha.set_metrology_object_param (MetrologyHandle, MetrologyCircleIndices, 'measure_transition', 'uniform')
        ha.apply_metrology_model (self.image, MetrologyHandle)
        CircleParameter = ha.get_metrology_object_result(MetrologyHandle, MetrologyCircleIndices, 'all', 'result_type', 'all_param')
        # print(CircleParameter)
        return CircleParameter        
        
    def update_glass_certificate_matrix_relative(self,numpy_matrix_3d,row_x_index,column_y_index,distance_x,distance_y):
        numpy_matrix_3d[0][row_x_index][column_y_index] = distance_x # x values,
        numpy_matrix_3d[1][row_x_index][column_y_index] = distance_y # y values,    

    #def update_glass_certificate_matrix_relative(self,column_x_index,row_y_index,relative_distance_x,relative_distance_y):
    #    self.glass_certificate_matrix_relative[0][column_x_index][row_y_index] = relative_distance_x # x values,
    #    self.glass_certificate_matrix_relative[1][column_x_index][row_y_index] = relative_distance_y # y values,

    # Open file as 3D numpy array : for location file
    def open_3D_location_file(self,file_location,number_of_axis):
        array_2d = np.loadtxt(file_location, delimiter=',')
        rows_in_file,column = array_2d.shape
        calibration_data_table_row = rows_in_file//number_of_axis
        calibration_data_table_column = column
        position_np_array = np.zeros((number_of_axis,calibration_data_table_row,calibration_data_table_column))
        position_np_array = array_2d.reshape(number_of_axis,calibration_data_table_row,calibration_data_table_column)
        return position_np_array


    def save_dot_locations_matrix(self,position_np_array,file_path ):
        # cannot save the 3D array have to reshape to 2D
        array_2d = position_np_array.reshape(-1, position_np_array.shape[-1])     
        np.savetxt(file_path, array_2d, delimiter=',', fmt='%.6f')      # save 2D file to .csv format
        print("Save file to:", file_path)
        


# ==========================
# unused functions
# ==========================


    # plot the glass certificate matrix as linear graph
    def plot_3D_matrix(glass_certificate_matrix_with_data,full_file_path):
        
        x_array = np.zeros(15)
        y_array = np.zeros(15)
        for i in range(1, 16,1):
            value = (i-1)*10 - glass_certificate_matrix_with_data[0, 8, i]
            print(value)

            # append vlaues to the array
            x_array[i-1] = i
            y_array[i-1] = round(value,6)
            #print(i,glass_certificate_matrix_with_data[0, 8, i],value)

        plt.plot(x_array, y_array, 'ro-')  # 'ro-' means red color, round points, solid lines
        plt.xlabel('Index')
        #plt.ylim(-0.01, 0.05)
        plt.ylabel('Glass scall accumilated error in X direaction (mm)')
        plt.title('Glass scall expantion error in X direaction vs Index')
        plt.savefig(full_file_path)
        plt.show()



#==========================
# Main function
#==========================
    @profile_performance
    def generate_2d_glass_certificate(self,location_matrix_file_path,vision_log_file_file_path,camera_calibration_file_path,images_used_for_test):

        # 1. Read the recipe file and get the setup related values
        
        # get setup related values from active recipe file 
        if self.pixel_to_mm == None or self.circle_radius == None:
            self.pixel_to_mm = float(self.read_recipe_csv("pixel_to_mm"))
            self.circle_radius = int(self.read_recipe_csv("circle_radius"))
            if self.pixel_to_mm == None or self.circle_radius == None:
                #print("Error: circle radius not found in the recipe file.")    
                self.pixel_to_mm = 0.001158878794                   # if recipe file not found, assign default value PBA lens with 12MP cam
                self.circle_radius = 294
                print("Assined default value: ",self.pixel_to_mm)
            else:
                print("Assined pixel_to_mm and circle_radius from recipe file: ",self.pixel_to_mm, self.circle_radius)
        
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

        if self.dot_pitch_in_pix == None or self.circle_radius_tolerance == None:
            self.circle_radius_tolerance    = int(self.read_recipe_csv("circle_radius_tolerance"))
            self.dot_pitch_in_pix           = int(self.read_recipe_csv("dot_pitch_in_pix"))
            if self.dot_pitch_in_pix == None or self.circle_radius_tolerance == None :
                #print("Error: circle radius not found in the recipe file.")    
                self.dot_pitch_in_pix        = 1160                    # if recipe file not found, assign default value PBA lens with 12MP cam
                self.circle_radius_tolerance = 50
                #print("Assined default value: ",self.pixel_to_mm)
            else:
                print("Assined dot_pitch_in_pix and circle_radius_tolerance from recipe file: ",self.dot_pitch_in_pix, self.circle_radius_tolerance)

        if self.image_brightness_threshold_value == None:
            self.image_brightness_threshold_value = int(self.read_recipe_csv("image_brightness_threshold_value"))
            if self.image_brightness_threshold_value == None:
                #print("Error: image brightness threshold value not found in the recipe file.")    
                self.image_brightness_threshold_value = 150                    # if recipe file not found, assign default value PBA lens with 12MP cam
                #print("Assined default value: ",self.image_brightness_threshold_value)
            else:
                print("Assined image_brightness_threshold_value from recipe file: ",self.image_brightness_threshold_value)

        # 1. Define home position index for the glass certificate matrix
        #home_position_index_row = 0
        #home_position_index_column = 0
        #print(f"home position index: {home_position_index_row},{home_position_index_column}")

        
        # 2. Read the variable pitch matrix or location matrix and create a glass certificate matrix
        number_of_axis = 3
        location_matrix = self.open_3D_location_file(location_matrix_file_path,number_of_axis)
        print(f"location_matrix.shape : {location_matrix.shape}")
        self.glass_certificate_matrix_relative = self.create_glass_certificate_62207_matrix(location_matrix.shape)

        # print the shape of the glass certificate matrix
        print(f"glass_certificate_matrix.shape : {self.glass_certificate_matrix_relative.shape}")
        
        
        # 3. read the vision log file 
        numpy_array, numpy_array_shape = self.open_file_pandas_convert_numpy(vision_log_file_file_path)
        print(f"vision log file shape: {numpy_array_shape}")
        
        # 4. get the start and end row and column index and number of cycles and put those in 
        # self.start_row_index_y, self.end_row_index_y, self.start_column_index_x, self.end_column_index_x , self.number_of_cycles
        self.get_start_end_row_column_index(numpy_array)

        print(f"start_row_index: {self.start_row_index_y}, end_row_index: {self.end_row_index_y}")
        print(f"start_column_index: {self.start_column_index_x}, end_column_index: {self.end_column_index_x}")
        print(f"number_of_cycles: {self.number_of_cycles}")


        # 5. get the camera calibration data
        mtx, dist, rvecs, tvecs = self.open_calibration_data(camera_calibration_file_path)
        if mtx is None or dist is None:
            print("Error loading camera calibration data. Exiting.")
            return
        

        # 5. Going through the vision log file and get the dot center location and 4 adjacent dot locations and put those in the glass certificate matrix 
        # for i in range(numpy_array.shape[0]-1):        # # going through the full vision log file rows
        for i in range(0, images_used_for_test, 1):                       # going through the vision log file first 10 rows
            # numpy_array[i][3]  # Y position
            # numpy_array[i][4]  # X position
            # print("---pricessing vision log file row: ",i)           
            # 1. Identify available adjacent index
            left_adjacent, right_adjacent, top_adjacent, bottom_adjacent, detected_adjacent_dots = self.calculate_adjacent_index(numpy_array[i][3],numpy_array[i][4])    # get the adjacent index
            # print(left_adjacent, right_adjacent, top_adjacent, bottom_adjacent)

            # 2. Create image file path
            image_full_file_path = self.create_full_file_path(vision_log_file_file_path, str(numpy_array[i][2]))
            #print(f"image_full_file_path: {image_full_file_path}")

            # 3. create undistroted image
            undistorted_image_file_path = self.create_undistort_image(image_full_file_path,mtx,dist,mtx)
            image_full_file_path = undistorted_image_file_path

            # 3. Pre process image and get 4 adjacent dot locations (and center dot location freatures deverloped but not used) 
            # detected_adjacent_dots = self.pre_processing(image_full_file_path)

            # print(f"image center dot index: {numpy_array[i][4]}, {numpy_array[i][3]}")                      # index value not pixel value
            # print(f"index_dot_center_x: {numpy_array[i][12]}, index_dot_center_y: {numpy_array[i][11]}")    # halcon calculate this for us in the vision log file

            # 4. Calculate the distance differance bitween center location and 4 adjacent dot locations and put those in the glass certificate matrix
            for adj_name, adj_data  in detected_adjacent_dots.items():
                if adj_data is not None:  # Check if adjacent dot exists
                    detected_loc, detected_index = adj_data
                #     print(f"Adjacent Dot ({adj_name}): Detected Dot {detected_index} at {detected_loc}")
                # else:
                #     print(f"Adjacent Dot ({adj_name}): Not Detected")

                #print(f"Adjacent Dot ({adj_name}): Detected Dot {detected_index} at {detected_loc}, Expected Location: {adjacent_dots_expected[adj_name]}")
                #print(f"Adjacent Dot ({adj_name}): Detected Dot {detected_index} at {detected_loc}")

                ## if adj_name == "Left" and left_adjacent == 1:
                    ## give image location, and estimated dot center values to halcon and get correctd pixel values
                    # circle_parameter = self.calculate_dot_center_location_using_halcon(image_full_file_path, detected_loc[0], detected_loc[1])
                    # print(f"Left dot location: {detected_loc[0]},{detected_loc[1]}")
                    # print(circle_parameter[1],circle_parameter[0])
                    # relative_distance_x = (numpy_array[i][12] - circle_parameter[1])*self.pixel_to_mm
                    # relative_distance_y = (circle_parameter[0] - numpy_array[i][11])*self.pixel_to_mm
                    # row_x_index = numpy_array[i][3]
                    # column_y_index = numpy_array[i][4]+1
                    ## print(f"Left dot index: {row_x_index},{column_y_index}")
                    ## print(f"Relative distance from ceter dot to Left dot : {relative_distance_x},{relative_distance_y} ")
                    # self.update_glass_certificate_matrix_relative(self.glass_certificate_matrix_relative,row_x_index,column_y_index,relative_distance_x,relative_distance_y)
                    ## self.update_glass_certificate_matrix_relative(column_x_index,row_y_index,relative_distance_x,relative_distance_y)
                    ## print("---")

                if adj_name == "Right" and right_adjacent == 1:
                    # give image location, and estimated dot center values to halcon and get correctd pixel values
                    circle_parameter = self.calculate_dot_center_location_using_halcon(image_full_file_path, detected_loc[0], detected_loc[1])
                    # print(circle_parameter[1],circle_parameter[0], numpy_array[i][12],numpy_array[i][11])
                    # print(f"Right dot location: {detected_loc[0]},{detected_loc[1]}")
                    relative_distance_x = (circle_parameter[1] - numpy_array[i][12])*self.pixel_to_mm
                    relative_distance_y = (circle_parameter[0] - numpy_array[i][11])*self.pixel_to_mm
                    row_x_index = numpy_array[i][3]
                    column_y_index = numpy_array[i][4]+1
                    # print("Right dot index: ",row_x_index},{column_y_index})
                    # print(f"Relative distance from ceter dot to Right dot : {relative_distance_x},{relative_distance_y} ")
                    self.update_glass_certificate_matrix_relative(self.glass_certificate_matrix_relative,row_x_index,column_y_index,relative_distance_x,relative_distance_y)
                    # print("---")

                #elif adj_name == "Top" and top_adjacent == 1:
                    # print(f"Top dot location: {detected_loc[0]},{detected_loc[1]} ")
                    # relative_distance_x = numpy_array[i][12] - detected_loc[0]
                    # relative_distance_y = detected_loc[1] - numpy_array[i][11]
                    # print("Top dot index: ",{numpy_array[i][4]},{numpy_array[i][3]-1})
                    # print(f"Relative distance from ceter dot to Top dot : {relative_distance_x},{relative_distance_y} ")
                    # print("---")

                elif adj_name == "Bottom" and bottom_adjacent == 1:
                    
                    circle_parameter = self.calculate_dot_center_location_using_halcon(image_full_file_path, detected_loc[0], detected_loc[1])
                    #print(f"Bottom dot location: {detected_loc[0]},{detected_loc[1]} ")
                    #print(circle_parameter[1],circle_parameter[0])
                    relative_distance_x = (circle_parameter[1] - numpy_array[i][12])*self.pixel_to_mm
                    relative_distance_y = (circle_parameter[0] - numpy_array[i][11])*self.pixel_to_mm
                    row_x_index     = numpy_array[i][3]+1   # y direction
                    column_y_index  = numpy_array[i][4]     # x direction
                    #print("Bottom dot index: ",{numpy_array[i][4]},{numpy_array[i][3]+1})
                    #print(f"Relative distance from ceter dot to Bottom dot : {relative_distance_x},{relative_distance_y} ")
                    self.update_glass_certificate_matrix_relative(self.glass_certificate_matrix_relative,row_x_index,column_y_index,relative_distance_x,relative_distance_y)
                    #self.update_glass_certificate_matrix_relative(column_x_index,row_y_index,relative_distance_x,relative_distance_y)
                    #print("---")

        print("glass certiicate generated, saving glass certificate matrix to file")

        glass_certificate_full_file_path = self.create_full_file_path(vision_log_file_file_path,"glass_certificate_2D_relative.csv")

        print(self.glass_certificate_matrix_relative[0,1,1])
        print(self.glass_certificate_matrix_relative[0,2,1])
        print(self.glass_certificate_matrix_relative[0,3,1])
        print(self.glass_certificate_matrix_relative.shape)
        self.save_dot_locations_matrix(self.glass_certificate_matrix_relative,glass_certificate_full_file_path)
        newly_glass_certificate = self.open_3D_location_file(glass_certificate_full_file_path,3) # number_of_axis = 3
        print(newly_glass_certificate[0,1,1])
        print(newly_glass_certificate[0,2,1])
        print(newly_glass_certificate[0,3,1])
        return glass_certificate_full_file_path



# ===========================
# Test file
# ===========================
#150 x 150 matrix
#location_matrix_file_path = r"C:\Users\mj.j\OneDrive - PBA Systems Pte. Ltd\GitHub\Github\2025_04_03_18_51_01\calculated_all_referance_locations.csv"
#vision_log_file_file_path = r"C:\Users\mj.j\OneDrive - PBA Systems Pte. Ltd\GitHub\Github\2025_04_03_18_51_01\Log_file_2D_expansion_X_axis.csv"

# 10 x 10 matrix
#location_matrix_file_path = r"C:\Users\mj.j\OneDrive - PBA Systems Pte. Ltd\GitHub\Github\2025_04_07_08_34_26\calculated_all_referance_locations.csv"
#vision_log_file_file_path = r"C:\Users\mj.j\OneDrive - PBA Systems Pte. Ltd\GitHub\Github\2025_04_07_08_34_26\Log_file_2D_expansion_X_axis.csv"

# 4 x 4 matrix
#location_matrix_file_path = r"C:\Users\mj.j\OneDrive - PBA Systems Pte. Ltd\GitHub\Github\2025_04_16_14_15_46\calculated_all_referance_locations.csv"
#vision_log_file_file_path = r"C:\Users\mj.j\OneDrive - PBA Systems Pte. Ltd\GitHub\Github\2025_04_16_14_15_46\Log_file_2D_expansion_X_axis.csv"


# 15 x 15 matrix
#location_matrix_file_path = r"C:\Users\mj.j\OneDrive - PBA Systems Pte. Ltd\GitHub\Github\2025_04_17_08_59_33\calculated_all_referance_locations.csv"
#vision_log_file_file_path = r"C:\Users\mj.j\OneDrive - PBA Systems Pte. Ltd\GitHub\Github\2025_04_17_08_59_33\Log_file_2D_expansion_X_axis.csv"


# ======================
# Test run
# ======================

# location_matrix_file_path = r"C:\Users\malit\Documents\GitHub\2025_10_29_11_32_19\calculated_all_referance_locations.csv"
# vision_log_file_file_path = r"C:\Users\malit\Documents\GitHub\2025_10_29_11_32_19\Log_file_2D_expansion_X_axis.csv"
# camera_calibration_file_path = r"C:\Users\malit\Documents\GitHub\2D_optical_vision_mapping\src\recipes\camera_calibration_data_2X_lens.npz"

# generate_glass_certificate_test = generate_glass_certificate()
# generate_glass_certificate_test.generate_2d_glass_certificate(location_matrix_file_path,vision_log_file_file_path,camera_calibration_file_path,images_used_for_test)
