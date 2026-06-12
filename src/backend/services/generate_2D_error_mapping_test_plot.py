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
        self.image_width = None
        self.image_height = None
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
        plt.ylim(-0.003, 0.003)
        plt.plot(y_value, y_error_value, c='blue', marker='o', markersize=5)
        plt.title('2D Error Map - Y Direction')
        plt.xlabel('Axis 2 Distance (mm)')
        plt.ylabel('Error Value mm')
        plt.show()

    def create_full_file_path(self,ref_file_location, file_name):
        file_path = os.path.dirname(ref_file_location)
        file_path_name = os.path.join(file_path,file_name)
        return file_path_name

    def plt_x_error_map_2D_refactored(self, data_for_y_level, y_position_value):
        # data_for_y_level is a NumPy array containing only the rows for the current Y position,
        # assumed to be sorted by the original image capture sequence.
        
        # Column indices from the CSV when converted to a 0-indexed NumPy array:
        # - CSV 'Y comand position' (index 5) is currently used for the plot's X-axis.
        #   Plot X-axis label is 'Axis 1 Distance (mm)'. If this should be X-related,
        #   CSV 'X comand position' (index 6) might be more appropriate.
        # - CSV 'pix_Y' (index 11) is used to calculate the error for the plot's Y-axis.
        
        plot_x_values = data_for_y_level[:, 5]  # Current: Y comand position
        # If X comand position is intended: plot_x_values = data_for_y_level[:, 6]
        
        pix_y_for_error_calc = data_for_y_level[:, 11]
        
        # Assuming 1500 is the reference pixel for X error calculation from pix_Y
        error_values_mm = (pix_y_for_error_calc - 1500) * self.pixel_to_mm 
        
        plt.figure(figsize=(10, 6))
        plt.ylim(-0.003, 0.003)  # Set Y limits for better visibility of error values
        plt.plot(plot_x_values, error_values_mm)
        plt.title(f'2D Error Map - X Direction (Y = {y_position_value})')
        plt.xlabel('Y Command Position (mm)') # Label reflects current data source (column 5)
        # If using column 6: plt.xlabel('X Command Position (mm)')
        plt.ylabel('X Error Value (mm)') # Error is in X, derived from pix_Y
        plt.grid(True)
        file_name=f'x_repeatability_at_y_index_{y_position_value}.png'
        file_path_name = self.create_full_file_path(self.Log_file_2D_error_map_test_file_path, file_name)
        plt.savefig(file_path_name, dpi=300)  # Save the plot as a PNG file
        plt.show()

        

    def plot_y_repeatability_at_x_index(self, pandas_df_for_run, x_index_val, run_number):
        """
        Plots Y-direction repeatability for a given X position index and Run number.

        This method filters data for a specific 'X position' within a given Run.
        It then identifies two passes for each 'Y position' based on the image
        acquisition sequence within that Run:
        - Pass 0: The first time the scanner is at this (X, Y) coordinate in this Run.
        - Pass 1: The second time (typically on a return scan) in this Run.

        It calculates the Y error based on 'pix_X'.
        Pass 0 data is plotted with 'Y comand position' increasing.
        Pass 1 data is plotted with 'Y comand position' decreasing.

        Args:
            pandas_df_for_run (pd.DataFrame): The input DataFrame, filtered for a specific Run
                                             and sorted by image acquisition.
            x_index_val (int): The 'X position' index to analyze (e.g., 0).
            run_number (int): The Run number being processed.
        """
        if self.pixel_to_mm is None:
            print("Error in plot_y_repeatability_at_x_index: pixel_to_mm not set. Cannot calculate error in mm.")
            return
        if self.image_width is None:
            print("Error in plot_y_repeatability_at_x_index: image_width not set. Cannot calculate error.")
            return

        print(f"Generating Y repeatability plot for Run {run_number}, X position index: {x_index_val}")
        
        # Work on a copy to avoid modifying the original DataFrame
        pandas_df = pandas_df_for_run.copy()

        # Column names (ensure these match exactly after stripping whitespace)
        x_pos_col = 'X position'
        y_pos_col = 'Y position' # This is the Y index (0, 1, 2, ...)
        y_cmd_pos_col = 'Y comand position'
        pix_x_col = 'pix_X'

        # Filter for the specific X position index (already within a specific run)
        df_at_x_index = pandas_df[pandas_df[x_pos_col] == x_index_val].copy()

        if df_at_x_index.empty:
            print(f"No data found for Run {run_number}, X position index: {x_index_val} in plot_y_repeatability_at_x_index.")
            return

        # Identify passes (0 for first visit, 1 for second visit to an (X_index_val, Y_position_value) combination)
        # Assumes pandas_df (df_for_current_run) was sorted by image acquisition order
        df_at_x_index.loc[:, 'pass_num'] = df_at_x_index.groupby(y_pos_col).cumcount()

        pass_0_data = df_at_x_index[df_at_x_index['pass_num'] == 0].copy()
        pass_1_data = df_at_x_index[df_at_x_index['pass_num'] == 1].copy()

        if pass_0_data.empty:
            print(f"No 'pass 0' data found for Run {run_number}, X position {x_index_val}. Cannot establish Y error reference.")
            return

        # Sort pass_0 data by Y command position to get the correct reference for this X-index
        pass_0_data = pass_0_data.sort_values(by=y_cmd_pos_col)
        
        if pass_0_data.empty: # Re-check after sort, though unlikely to become empty if not already
            print(f"No 'pass 0' data after sorting for Run {run_number}, X position {x_index_val}.")
            return

        # Reference pix_X is from the first point in pass_0 (lowest Y command position for this X-index in this run)
        reference_pix_X = pass_0_data[pix_x_col].iloc[0]
        # print(f"Reference pix_X for Run {run_number}, X={x_index_val}: {reference_pix_X}")
        
        image_middle_width_px = self.image_width // 2

        # Calculate error for pass 0
        # Error for pass 0 is calculated relative to the image center
        y_command_pass_0 = pass_0_data[y_cmd_pos_col]
        error_pass_0_mm = (pass_0_data[pix_x_col] - image_middle_width_px) * self.pixel_to_mm

        # Prepare and calculate error for pass 1
        # Error for pass 1 is calculated relative to the reference_pix_X from pass 0 for repeatability
        if not pass_1_data.empty:
            pass_1_data = pass_1_data.sort_values(by=y_cmd_pos_col, ascending=False)
            y_command_pass_1 = pass_1_data[y_cmd_pos_col]
            error_pass_1_mm = (pass_1_data[pix_x_col] - reference_pix_X) * self.pixel_to_mm
        else:
            y_command_pass_1 = pd.Series(dtype=float) 
            error_pass_1_mm = pd.Series(dtype=float)  
            print(f"Warning: No 'pass 1' data found for Run {run_number}, X position {x_index_val} for Y repeatability plot.")

        # Plotting
        plt.figure(figsize=(10, 6))
        
        if not y_command_pass_0.empty:
            plt.plot(y_command_pass_0, error_pass_0_mm, marker='o', linestyle='-', label=f'Pass 0 (Y incr., ref scan) @ X-idx {x_index_val}')
        
        if not y_command_pass_1.empty:
            plt.plot(y_command_pass_1, error_pass_1_mm, marker='x', linestyle='--', label=f'Pass 1 (Y decr., repeat scan) @ X-idx {x_index_val}')
        
        plt.title(f'Y-Direction Repeatability (Run {run_number}) at X Position Index: {x_index_val}')
        plt.xlabel('Y Command Position (mm)')
        plt.ylabel(f'Y Error (derived from {pix_x_col}) (mm)')
        plt.legend()
        plt.grid(True)
        # Invert X axis (Y command position) to match typical Y-axis representation if needed
        # plt.gca().invert_xaxis() 
        # print(f"Plotting Y repeatability for Run {run_number}, X={x_index_val}. Ref pix_X: {reference_pix_X}")
        
        plot_filename = f"y_repeatability_run_{run_number}_x_index_{x_index_val}.png"
        try:
            plt.savefig(plot_filename, dpi=300) # Added dpi here as well
            print(f"Plot saved to {plot_filename}")
        except Exception as e:
            print(f"Error saving Y repeatability plot: {e}")
        plt.show()


    # main function 
    def generate_2D_error_map_plot(self,Log_file_2D_error_map_test_file_path):
        """
        Generates 2D error map plots for X and Y directions from a log file.

        The method reads a CSV log file containing scan data. For the X-direction plot,
        it iterates through each unique Y position. For each Y position, it identifies
        the sequence of data points corresponding to the X-axis scan (both forward and
        backward movements) based on the 'image name' column. It then plots the
        'X comand position' against the calculated X-axis error (derived from 'pix_Y').

        Args:
            Log_file_2D_error_map_test_file_path (str): The file path to the CSV log file.
        """
        self.Log_file_2D_error_map_test_file_path = Log_file_2D_error_map_test_file_path

        # Open file as pandas DataFrame for easier grouping and robust processing
        try:
            pandas_df = pd.read_csv(Log_file_2D_error_map_test_file_path)
        except FileNotFoundError:
            print(f"Error: Log file not found at {Log_file_2D_error_map_test_file_path}")
            return
        except Exception as e:
            print(f"Error reading log file: {e}")
            return


        # get setup related values from active recipe file 
        if self.pixel_to_mm is None: # Corrected condition to check for None
            pixel_to_mm_str = self.read_recipe_csv("pixel_to_mm")
            if pixel_to_mm_str is not None:
                try:
                    self.pixel_to_mm = float(pixel_to_mm_str)
                    print("Assigned pixel_to_mm from recipe file: ",self.pixel_to_mm)
                except ValueError:
                    print(f"Error: Could not convert pixel_to_mm value '{pixel_to_mm_str}' to float.")
                    self.pixel_to_mm = 0.001168674 # Default value
                    print("Assigned default pixel_to_mm: ",self.pixel_to_mm)
            else:
                self.pixel_to_mm = 0.001168674 # Default value
                print("pixel_to_mm not found in recipe. Assigned default value: ",self.pixel_to_mm)
        
        # get the image dimensions from the recipe file
        if self.image_height is None or self.image_width is None:
            # Read image dimensions from the recipe file
            self.image_height = int(self.read_recipe_csv("image_height"))
            self.image_width = int(self.read_recipe_csv("image_width"))
            print(f"Image dimensions set to: {self.image_width}x{self.image_height} pixels.")


        # X direction plot
        print(f"Log file shape: {pandas_df.shape}")

        # Group data by 'Y position'
        # Column names are case-sensitive and include spaces as per your CSV.
        y_position_col_name = 'Y position' 
        if y_position_col_name not in pandas_df.columns:
            print(f"Error: Column '{y_position_col_name}' not found in the log file.")
            # Attempt to use column index 3 if name matching fails, with a warning
            if len(pandas_df.columns) > 3:
                y_position_col_name = pandas_df.columns[3]
                print(f"Warning: Using column '{y_position_col_name}' (index 3) as Y position.")
            else:
                print("Cannot determine Y position column.")
                return

        for y_val, group_df in pandas_df.groupby(y_position_col_name):
            # group_df is a DataFrame containing all rows for the current y_val.
            # It retains the order from the sorted pandas_df.
            
            # Convert the group to a NumPy array for the plotting function
            group_np = group_df.to_numpy()
            
            print(f"Plotting for Y position: {y_val}, using {group_np.shape[0]} data points.")
            
            # Call the refactored plotting function, passing the data subset and the Y value
            self.plt_x_error_map_2D_refactored(group_np, y_val)
        
        # Y direction repeatability plot (newly added)
        # Example: Plot Y repeatability for X position index 0
        print("\\nGenerating Y-direction repeatability plot...")



        self.plot_y_repeatability_at_x_index(pandas_df, x_index_val=0, run_number = 1)  # Assuming run_number is 1 for the first run
        # self.plot_y_repeatability_at_x_index(pandas_df, x_index_val=0)
        # self.plot_y_repeatability_at_x_index(pandas_df, x_index_val=1)
        # self.plot_y_repeatability_at_x_index(pandas_df, x_index_val=2)
        # self.plot_y_repeatability_at_x_index(pandas_df, x_index_val=3)
        # self.plot_y_repeatability_at_x_index(pandas_df, x_index_val=4)

        # You can call this for other x_index_val if needed, e.g.:
        # self.plot_y_repeatability_at_x_index(pandas_df, x_index_val=1)

# =========================
# main test function call
# =========================

#after_centering_dot_location_file_path = r"C:\Users\mj.j\OneDrive - PBA Systems Pte. Ltd\GitHub\Github\2025_04_21_11_27_35\Expansion_array_2D_0.csv"
# BEFORE ERROR MAP
# Log_file_2D_error_map_test_file_path = r"C:\Users\malit\OneDrive\Documents\GitHub\2025_06_06_19_11_27\Log_file_2D_error_map.csv"

# AFTER ERROR MAP
#Log_file_2D_error_map_test_file_path = r"C:\Users\malit\OneDrive\Documents\GitHub\2025_06_06_19_33_36\Log_file_2D_error_map.csv"


# folder_path = os.path.dirname(Log_file_2D_error_map_test_file_path)
# print("folder_path:",folder_path)
# error_map_axis_0_file_path = os.path.join(folder_path,"x_error_map_2D.csv")

# call the class and method to generate the plot
# generate_map = Generate2DErrorMapPlot()

# generate_map.generate_2D_error_map_plot(Log_file_2D_error_map_test_file_path)
