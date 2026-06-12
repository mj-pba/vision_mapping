# we have to create multiple documents from existing documents to create a test 
import pandas as pd
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import csv

class Generate2DErrorMapPlot:
    def __init__(self):
        self.pixel_to_mm = None
        # self.after_centering_dot_location_file_path = None
        pass 
    
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

    def create_full_file_path(self,ref_file_location, file_name):
        file_path = os.path.dirname(ref_file_location)
        file_path_name = os.path.join(file_path,file_name)
        return file_path_name


    # Open file as 3D numpy array : for location file
    def open_3D_location_file(self,file_location,number_of_axis):
        array_2d = np.loadtxt(file_location, delimiter=',')
        rows_in_file,column = array_2d.shape
        calibration_data_table_row = rows_in_file//number_of_axis
        calibration_data_table_column = column
        position_np_array = np.zeros((number_of_axis,calibration_data_table_row,calibration_data_table_column))
        position_np_array = array_2d.reshape(number_of_axis,calibration_data_table_row,calibration_data_table_column)
        return position_np_array


    # Open file as 2D pandas and convert to numpy array : for log file
    def open_file_pandas_convert_numpy(self,file_location):
        pandas_df = pd.read_csv(file_location)
        numpy_array = pandas_df.to_numpy()
        return numpy_array, numpy_array.shape
    
    def plt_x_error_map_2D(self,x_error_map_2D,x_min_int,x_max_int):
        # Plot x direction error map
        plt.figure(figsize=(10, 6))
        plt.plot(x_error_map_2D[x_min_int:x_max_int,5], (x_error_map_2D[x_min_int:x_max_int,11] - 1500)*self.pixel_to_mm )#, c=x_error_map_2D[:10,5], cmap='viridis', s=50)
        plt.title('2D Error Map - X Direction')
        plt.xlabel('Axis 1 Distance (mm)')
        plt.ylabel('Error Value mm')
        plt.show()
    
    def plt_y_error_map_2D(self,y_value,y_error_value):
        # Plot y direction error map
        plt.figure(figsize=(10, 6))
        plt.plot(y_value, y_error_value, c='blue', marker='o', markersize=5)
        plt.title('2D Error Map - Y Direction')
        plt.xlabel('Axis 2 Distance (mm)')
        plt.ylabel('Error Value mm')
        plt.show()





    def generate_2D_error_map_plot(self,Log_file_2D_error_map_test_file_path):

        # Open file as 2D pandas and convert to numpy array
        x_error_map_2D, x_error_map_2D_shape = self.open_file_pandas_convert_numpy(Log_file_2D_error_map_test_file_path)

        # get the search axis values 
        stop_condition_Y = np.max(x_error_map_2D[:,3])
        stop_condition_X = np.max(x_error_map_2D[:,4])
        print("x_error_map_2D_axis_1:", stop_condition_Y)
        print("x_error_map_2D_axis_0:", stop_condition_X)

        # get setup related values from active recipe file 
        if self.pixel_to_mm == None:
            self.pixel_to_mm = float(self.read_recipe_csv("pixel_to_mm"))
            if self.pixel_to_mm == None:
                #print("Error: circle radius not found in the recipe file.")    
                self.pixel_to_mm = 0.001168674                    # if recipe file not found, assign default value PBA lens with 12MP cam
                print("Assined default value: ",self.pixel_to_mm)
            else:
                print("Assined pixel_to_mm and circle_radius from recipe file: ",self.pixel_to_mm)

        # get the row and column values to plot the 2D error map
        # X direction plot
        print("x_error_map_2D_shape:", x_error_map_2D_shape[0])     # 50

        for j in range(0,stop_condition_Y+1,1):
            # get the minimum value of x and maximum value of x
            x_min = np.min(x_error_map_2D[x_error_map_2D[:,3] == j, 2])
            x_max = np.max(x_error_map_2D[x_error_map_2D[:,3] == j, 2])
            # Extract integer part
            x_min_int = int(x_min.replace('.png', '')) -1
            x_max_int = int(x_max.replace('.png', '')) 
            print("j:",j,"x_min:", x_min_int, "x_max:", x_max_int)
            self.plt_x_error_map_2D(x_error_map_2D,x_min_int,x_max_int)
        
        
        
        # y direction plot
        
        for i in range(0,stop_condition_X+1,1):
            # create new array for Y values and Y error values
            y_error_map_2D = x_error_map_2D[x_error_map_2D[:,4] == i, :]
            # sort the array by the third column (which is the distance)
            y_error_map_2D = y_error_map_2D[y_error_map_2D[:,0].argsort()]
            self.plt_y_error_map_2D(y_error_map_2D[:,6],(y_error_map_2D[:,12]-2048)*self.pixel_to_mm)
            
        

# =========================
# main test function call
# =========================

#after_centering_dot_location_file_path = r"C:\Users\mj.j\OneDrive - PBA Systems Pte. Ltd\GitHub\Github\2025_04_21_11_27_35\Expansion_array_2D_0.csv"
Log_file_2D_error_map_test_file_path = r"C:\Users\malit\OneDrive\Documents\GitHub\2025_05_23_11_30_18\Log_file_2D_error_map.csv"


# folder_path = os.path.dirname(Log_file_2D_error_map_test_file_path)
# print("folder_path:",folder_path)
# error_map_axis_0_file_path = os.path.join(folder_path,"x_error_map_2D.csv")

# call the class and method to generate the plot
generate_map = Generate2DErrorMapPlot()

generate_map.generate_2D_error_map_plot(Log_file_2D_error_map_test_file_path)
