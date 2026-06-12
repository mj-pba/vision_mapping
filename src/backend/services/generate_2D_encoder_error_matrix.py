# Description: This script generates a 2D encoder error matrix for a given set of parameters.

import numpy as np
import pandas as pd
import csv
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
#import cv2
#import halcon as ha



class encoder_error_matrix:
    def __init__(self):
        # Initialize the encoder error matrix generator
        pass

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
    def open_file_pandas_convert_numpy(self, file_location):
        pandas_df = pd.read_csv(file_location)
        #print heder file 
        #print(pandas_df.head())
        # Convert the DataFrame to a numpy array
        numpy_array = pandas_df.to_numpy()
        
        return numpy_array, numpy_array.shape
    
    # Create matrix to store location values: for encoder error matrix
    def create_error_matrix(self,array_shape):
        # Define the data
        new_array = np.zeros(array_shape)
        self.glass_certificate_array_shape = array_shape
        return new_array

    def get_index_zero_to_dot_distance(self,glass_certificate_3D_array,column_x_index_1,row_y_index_1):

        #print("---")
        #print("x_index_1:",column_x_index_1)
        #print("y_index_1:",row_y_index_1)

        #print("location 1 value:",relative_distance_x_index_1,relative_distance_y_index_1)
        x_distance_mm = 0.0
        y_distance_mm = 0.0

        # get the cumelative distance for column 0 up to column x_index_1
        i = 0
        for i in range(0,row_y_index_1+1):
            #print(glass_certificate_3D_array[0,i,0])
            x_distance_mm = x_distance_mm + glass_certificate_3D_array[0,i,0]  # x values,
            y_distance_mm = y_distance_mm + glass_certificate_3D_array[1,i,0]  # y values,

        i = 0
        for i in range(0,column_x_index_1):
            #print(glass_certificate_3D_array[0,row_y_index_1,i+1])
            x_distance_mm = x_distance_mm + glass_certificate_3D_array[0,row_y_index_1,i+1]  # x values,
            y_distance_mm = y_distance_mm + glass_certificate_3D_array[1,row_y_index_1,i+1]  # y values,

        #print("x_distance_mm:",x_distance_mm)        
        #print("y_distance_mm:",y_distance_mm)

        return x_distance_mm, y_distance_mm


    # [axis,rows, colums] / [axis, x direction data, y direction]
    # one row contans x axis data  / if we changing row values we are going along the y axis 
    # one column contans y axis data / if we changing column values we are going along the x axis
    def update_matrix(self,numpy_matrix_3d,row_x_index,column_y_index,distance_x,distance_y):
        numpy_matrix_3d[0][row_x_index][column_y_index] = distance_x # x values,
        numpy_matrix_3d[1][row_x_index][column_y_index] = distance_y # y values,

    #def update_matrix(self,numpy_matrix_3d,column_x_index,row_y_index,distance_x,distance_y):
        #numpy_matrix_3d[0,column_x_index,row_y_index] = distance_x # x values,
        #numpy_matrix_3d[1,column_x_index,row_y_index] = distance_y # y values,   
    
    def create_full_file_path(self,ref_file_location, file_name):
        file_path = os.path.dirname(ref_file_location)
        file_path_name = os.path.join(file_path,file_name)
        return file_path_name


    def save_3d_matrix(self,position_np_array,file_path ):
        # cannot save the 3D array have to reshape to 2D
        array_2d = position_np_array.reshape(-1, position_np_array.shape[-1])     
        np.savetxt(file_path, array_2d, delimiter=',', fmt='%.6f')      # save 2D file to .csv format
        print("Save file to:", file_path)



    # study the camera rotation 
    def get_camera_rotation_matrix(self,vision_cumilative_distance_matrix):
        # create best fit line using first line x values and y values    
        coefficients_m_sum = 0

        for j in range (0,self.stop_condition_j):
            x_x = vision_cumilative_distance_matrix[0][j][0:self.stop_condition_i]
            x_y = vision_cumilative_distance_matrix[1][j][0:self.stop_condition_i]
            # get the best fit line using the line x values and y values
            coefficients_x = np.polyfit(x_x, x_y, 1)  # Fit a line (degree 1 polynomial)
            coefficients_m_sum = coefficients_x[0] + coefficients_m_sum
            print(f"coefficients_x_0_{j}:",coefficients_x[0],coefficients_x[1])

        mean_coefficients_m = coefficients_m_sum/self.stop_condition_j
        #print("coefficients_x_0_sum:",mean_coefficients_m)
        # calculate the average angle in radians
        average_angle = np.arctan(mean_coefficients_m)
        print("average_angle:",average_angle)

        #===========================
        # rotation matrix
        #===========================

        # create matrix that has same shape as vision_cumilative_distance_matrix
        rotation_matrix = np.zeros(vision_cumilative_distance_matrix.shape)
        
        # create rotation matrix
        rotation_matrix[0] = np.cos(average_angle) * vision_cumilative_distance_matrix[0] + np.sin(average_angle) * vision_cumilative_distance_matrix[1]
        rotation_matrix[1] = np.sin(average_angle) * vision_cumilative_distance_matrix[0] * -1 + np.cos(average_angle) * vision_cumilative_distance_matrix[1]

        self.error_map_grid_step_i_direction = np.zeros((self.stop_condition_i))
        self.error_map_grid_step_j_direction = np.zeros((self.stop_condition_j))

        x_values_in_y_direction_rotation = np.zeros((self.stop_condition_j))
        
        for i in range (0,self.stop_condition_i): # 15
            for j in range (0,self.stop_condition_j): # 20    
                x_values_in_y_direction_rotation[j] = rotation_matrix[0][j][i]
            self.error_map_grid_step_i_direction[i] = np.mean(x_values_in_y_direction_rotation)
            # print(self.error_map_grid_step_i_direction[i])
        
        for j in range (0,self.stop_condition_j): # 20
            self.error_map_grid_step_j_direction[j] = np.mean(rotation_matrix[1][j][0:self.stop_condition_i])
        
        # generate file path to save coefficent c values
        # full_path_coefficients_c_rows_after_rotation = self.create_full_file_path(location_matrix_file_path,"error_map_grid_step.csv")
        # np.savetxt(full_path_coefficients_c_rows_after_rotation, self.error_map_grid_step_i_direction, delimiter=',', fmt='%.6f')      # save 2D file to .csv format

        # plot the rotation matrix

#         plt.plot(rotation_matrix[0], rotation_matrix[1], 'go')
#         plt.xlabel('X Axis (mm)')
#         plt.ylabel('Y Axis (mm)')
#         plt.title('Vision based glass certificate')
#         plt.grid()
#         plt.show()

# #
#        plt.plot(vision_cumilative_distance_matrix[0], vision_cumilative_distance_matrix[1], 'go')
#        plt.xlabel('X Axis')
#        plt.ylabel('Y Axis')
#        plt.title('Vision based dot location before rotation') 
#        plt.grid()
#        plt.show()
        return rotation_matrix


    # # Plot relative encoder position in 2D space
    # def plot_relative_encoder_position_2D(self, position_np_array,title):     
    #     # Create a 2D scatter plot of the encoder positions
    #     fig, ax = plt.subplots()

    #     # Scatter plot for X and Y error values
    #     ax.scatter(position_np_array[0], position_np_array[1], c='r', marker='o')

    #     ax.set_xlabel('X Axis error (mm)')
    #     ax.set_ylabel('Y Axis error (mm)')
    #     ax.set_title(title)  
    #     ax.grid(True)

    #     # Save the plot as a PNG file
    #     save_path = self.create_full_file_path(location_matrix_file_path, f"{title}.png")
    #     plt.savefig(save_path)
    #     print(f"2D error plot saved to: {save_path}")

    #     plt.show()



#        # Plot relative encoder position in 2D space
#    def plot_relative_encoder_position_2D(self, position_np_array,title):     
#        # Create a 2D scatter plot of the encoder positions
#        fig, ax = plt.subplots()
#        
#        # 15 color array 
#        color_array = ['r','g','b','c','m','y','k','orange','purple','pink','brown','gray','olive','teal','navy']
#        # markers
#        markers = ['o','s','^','D','v','<','>','p','*','h','+','x','|','_','1','2']
#
#        # Scatter plot for X and Y error values
#        for i in range(0,15):
#           for j in range(0,15):
#            ax.scatter(i, position_np_array[0][i][j],c = color_array[j], marker= markers[j])
#
#        ax.set_xlabel('X Axis Error (mm)')
#        ax.set_ylabel('Y Axis Error (mm)')
#        ax.set_title(title)  
#        ax.grid(True)
#
#        # Save the plot as a PNG file
#        save_path = self.create_full_file_path(location_matrix_file_path, "encoder_error_matrix_2D.png")
#        plt.savefig(save_path)
#        print(f"2D error plot saved to: {save_path}")
#
#        plt.show()





    #==============
    # Main function 
    #==============
    def generate_2D_encoder_error_matrix(self,vision_log_file_file_path, location_matrix_file_path, glass_certificate_full_file_path, dot_center_encoder_location_matrix_file_path):
        # 0. Read log file and identify stop condition
        numpy_array, numpy_array_shape = self.open_file_pandas_convert_numpy(vision_log_file_file_path)
        print(f"vision log file shape: {numpy_array_shape}")
        print(f"rows max value :    {np.max(numpy_array[:,4])}")
        print(f"columns max value : {np.max(numpy_array[:,3])}")

        self.stop_condition_i = np.max(numpy_array[:,4])    # 15
        self.stop_condition_j = np.max(numpy_array[:,3])    # 15

        print(f"stop_condition_i: {self.stop_condition_i}")
        print(f"stop_condition_j: {self.stop_condition_j}")

        # 1. Read the variable pitch matrix or location matrix and create a glass certificate matrix
        number_of_axis = 3
        location_matrix = self.open_3D_location_file(location_matrix_file_path,number_of_axis)
        
        self.encoder_error_matrix = self.create_error_matrix(location_matrix.shape)
        self.vision_cumilative_distance_matrix = self.create_error_matrix(location_matrix.shape)
        self.encoder_distance_matrix = self.create_error_matrix(location_matrix.shape)
        print(self.encoder_error_matrix.shape)

        # 3. Open glass cerificate matrix
        glass_certificate_3D_array = self.open_3D_location_file(glass_certificate_full_file_path,number_of_axis)
        print(glass_certificate_3D_array.shape)


        # 3. get distance of dot to dot from glass certificate matrix
        #for i in range(0,glass_certificate_3D_array.shape[1]):
        for i in range(0,self.stop_condition_i):
            #for j in range(0,glass_certificate_3D_array.shape[2]):
            for j in range(0,self.stop_condition_j):
                x_distance_mm, y_distance_mm = self.get_index_zero_to_dot_distance(glass_certificate_3D_array,i,j)
                # [axis,rows, colums] going along the row is increasing x axis values 
                self.update_matrix(self.vision_cumilative_distance_matrix,j,i,x_distance_mm,y_distance_mm)     
                


        # 4. generate file path and save cumalative distance matrix from vision
        full_path_vision_cumilative_distance_matrix = self.create_full_file_path(location_matrix_file_path,"vision_cumilative_distance_matrix.csv")
        self.save_3d_matrix(self.vision_cumilative_distance_matrix,full_path_vision_cumilative_distance_matrix)


        # 5. Correct the camera rotation and get corrected vision based cumalative distance matrix
        # ge the the step distance of the rows and columns
        self.vision_rotational_matrix = self.get_camera_rotation_matrix(self.vision_cumilative_distance_matrix)


        # 6. save the rotation matrix
        full_path_rotation_matrix = self.create_full_file_path(location_matrix_file_path,"vision_rotation_matrix.csv")          # matrix after rotation
        self.save_3d_matrix(self.vision_rotational_matrix,full_path_rotation_matrix)


        # 7. get the encoder index dot to other dot distance from expantion array 
        dot_center_encoder_values = self.open_3D_location_file(dot_center_encoder_location_matrix_file_path,number_of_axis)
        #print(f"0,1,0:{dot_center_encoder_values[0,1,0]}")
        #print(f"1,1,0:{dot_center_encoder_values[1,1,0]}")
        #for i in range(0,dot_center_encoder_values.shape[1]):
        for i in range(0,self.stop_condition_i): # 15
            #for j in range(0,dot_center_encoder_values.shape[2]):
            for j in range(0,self.stop_condition_j): # 20
                #print(f"{i}:{j}:{dot_center_encoder_values[0,i,j]}")
                x_distance_mm = dot_center_encoder_values[0,j,i] - dot_center_encoder_values[0,0,0]     # dot center x values - index 0,0 x values
                y_distance_mm = dot_center_encoder_values[1,j,i] - dot_center_encoder_values[1,0,0]     # dot center y values - index 0,0 y values
                self.update_matrix(self.encoder_distance_matrix,j,i,x_distance_mm,y_distance_mm)

        # 8. Save encoder distance matrix
        full_path_encoder_distance_matrix = self.create_full_file_path(location_matrix_file_path,"encoder_distance_matrix.csv")
        self.save_3d_matrix(self.encoder_distance_matrix,full_path_encoder_distance_matrix)


        # 9. Generate 2D error correction matrix encoder grid values
        self.axis_y_grid_encoder_values = np.zeros((dot_center_encoder_values.shape[2]))      # number of rows  Y steop 
        self.axis_x_grid_encoder_values = np.zeros((dot_center_encoder_values.shape[1]))      # number of columns X step
        
        self.axis_x_grid_encoder_values = dot_center_encoder_values[0][0][:]             # x values
        for i in range(0,dot_center_encoder_values.shape[2]):
            self.axis_y_grid_encoder_values[i] = dot_center_encoder_values[1][i][0]     # y values
        

        # generate the x axis grid encoder values
        self.axis_x_grid_encoder_values[0] = self.error_map_grid_step_i_direction[0]+self.axis_x_grid_encoder_values[0]
        for i in range(1,len(self.error_map_grid_step_i_direction)):
            self.axis_x_grid_encoder_values[i] = self.axis_x_grid_encoder_values[i-1] + self.error_map_grid_step_i_direction[i] - self.error_map_grid_step_i_direction[i-1]
        # print(self.axis_x_grid_encoder_values)
        # generate the y axis grid encoder values
        self.axis_y_grid_encoder_values[0] = self.axis_y_grid_encoder_values[0]+self.error_map_grid_step_j_direction[0]
        # print(self.axis_y_grid_encoder_values[0])
        for j in range(1,len(self.error_map_grid_step_j_direction)):
            self.axis_y_grid_encoder_values[j] = self.axis_y_grid_encoder_values[j-1] + self.error_map_grid_step_j_direction[j] - self.error_map_grid_step_j_direction[j-1]
        # print(self.axis_y_grid_encoder_values)

        # print(self.axis_x_grid_encoder_values)       # final values for X axis grid encoder values
        # print(self.axis_y_grid_encoder_values)




        # 10. get the encoder error matrix
        for i in range(0,self.stop_condition_i):
            for j in range(0,self.stop_condition_j):
                #error_x_distance_mm = self.encoder_distance_matrix[0,i,j] - self.vision_cumilative_distance_matrix[0,i,j]
                #error_y_distance_mm = self.encoder_distance_matrix[1,i,j] - self.vision_cumilative_distance_matrix[1,i,j]
                error_x_distance_mm = self.encoder_distance_matrix[0,j,i] - self.vision_rotational_matrix[0,j,i]
                error_y_distance_mm = self.encoder_distance_matrix[1,j,i] - self.vision_rotational_matrix[1,j,i]
                self.update_matrix(self.encoder_error_matrix ,j,i,error_x_distance_mm,error_y_distance_mm)
        
        # 8. save encoder error matrix
        full_path_encoder_error_matrix = self.create_full_file_path(location_matrix_file_path,"encoder_error_matrix.csv")
        self.save_3d_matrix(self.encoder_error_matrix,full_path_encoder_error_matrix)

        # 9. plot encoder error matrix
        #self.plot_relative_encoder_position(self.encoder_error_matrix)
        #self.plot_relative_encoder_position_2D(self.encoder_distance_matrix,"Dot center encoder position with respect to 0,0 position")
        #self.plot_relative_encoder_position_2D(self.encoder_error_matrix[:][0][:],"Variation of 2D error correction values")
        #print("encoder error matrix shape:",self.encoder_error_matrix[1])
        #self.plot_relative_encoder_position_2D(self.cumilative_distance_matrix)
        #self.plot_relative_encoder_position(glass_certificate_3D_array)

        return self.encoder_error_matrix


    #===============================
    # generate 2D error map for ACS
    #===============================
    def convert_to_acs_format(self,axis_encoder_values_x, axis_encoder_values_y,error_2D_matrix):
        try:
            num_rows = len(error_2D_matrix[:,1])
            num_cols = len(error_2D_matrix[1,:])

            if num_cols is not len(axis_encoder_values_x): # FIX
                print(f"Error: Mismatch of no. of columns in error_2D matrix({num_cols}) vs axis_encoder_values({len(axis_encoder_values_x)})")
                return []
            else:
                #print(f'numrows: {num_cols}, lenof axis_encoder_values: {len(axis_encoder_values_x)}')
                #print(f'===\nerror_2D_matrix: {error_2D_matrix.shape} num_rows: {num_rows} num_cols: {num_cols}')
                #zeros_row = np.zeros((1, num_cols)) # one row of zeros, num_cols wide
                #zeros_col = np.zeros((num_rows+1, 1)) # one column of zeros, num_rows high. +1 as it's appended after column was appended.
                #add_row = np.vstack([zeros_row, error_2D_matrix])
                #add_col = np.concatenate((zeros_col,add_row), axis=1)
                #print(f'=>addRow: {add_row.shape}, addCol: {add_col.shape}\n{add_col}')

                coords_x = axis_encoder_values_x.reshape(1,-1)   # np.arange(0, num_cols_paddedzero, 1, dtype=np.float64).reshape(1,-1)
                coords_y = axis_encoder_values_y.reshape(-1,1)   # np.arange(0, num_rows_paddedzero, 1, dtype=np.float64).reshape(-1,1) 
                #print(f'shapex: {coords_x.shape}')
                #print(f'shapey: {coords_y.shape}')
                #print(coords_y)
                #print(f'shapey: {coords_y.shape}')
                #coords_x = np.insert(coords_x, 0, 0, axis=1) # pad w 1 zero
                #print(f'shapex_: {coords_x.shape}')
                zeros = np.zeros((1, 1))  # 1 rows, 1 column
                coords_y = np.vstack((zeros, coords_y)) # add 0 at the top to adhere to ACS format, plus an additional zero for padding
                #print(f'coords_y.shape: {coords_y.shape}')
                #add_coords_x = np.vstack([coords_x, add_col])

                add_coords_x = np.vstack([coords_x, error_2D_matrix])
                add_coords_y = np.concatenate((coords_y,add_coords_x), axis=1)
                # print(f'added x row: {add_coords_x.shape}, added y col: {add_coords_y.shape}\n{add_coords_y}')
                return add_coords_y
        except Exception as e:
            print(f'Error converting matrix to ACS format, {e}')
        return []


#    def generate_ACS_errormaps(self,dot_center_encoder_location_matrix_file_path, encoder_error_matrix,NUM_POINTS):
    def generate_ACS_errormaps(self,encoder_error_matrix,vision_log_file_file_path):


        error_map_grid_x_axis_column = self.axis_x_grid_encoder_values    # x values
        error_map_grid_y_axis_row = self.axis_y_grid_encoder_values       # y values
        # print(encoder_error_matrix.shape)
        final_x = self.convert_to_acs_format(error_map_grid_x_axis_column, error_map_grid_y_axis_row, encoder_error_matrix[0]) 
        final_y = self.convert_to_acs_format(error_map_grid_x_axis_column, error_map_grid_y_axis_row, encoder_error_matrix[1])  
        #final_y = self.convert_to_acs_format(encoder_error_matrix[1])  

        if len(final_x) >0 and len(final_y) >0:
            # create full file path and save x and y error map
            full_path_x_errormap = self.create_full_file_path(vision_log_file_file_path,"x_error_map_2D.csv")
            full_path_y_errormap = self.create_full_file_path(vision_log_file_file_path,"y_error_map_2D.csv")
            np.savetxt(full_path_x_errormap, final_x, delimiter=';', fmt='%.6f')  
            np.savetxt(full_path_y_errormap, final_y, delimiter=';', fmt='%.6f')  
            print("x_errmap and y_errmap have been saved to 'x_errmap.csv' and 'y_errmap.csv'.")
            return full_path_x_errormap,full_path_y_errormap
        else:
            print("Error: Failure to convert x and y values into ACS format. Error maps not generated.") 
            return None, None



#===================================================
# Test code for generate_2D_encoder_error_matrix.py generate full error map matrix
#===================================================


# # # 15 x 15 matrix
# vision_log_file_file_path = r"C:\Users\malit\Documents\GitHub\2025_10_29_11_32_19\Log_file_2D_expansion_X_axis.csv"
# location_matrix_file_path = r"C:\Users\malit\Documents\GitHub\2025_10_29_11_32_19\calculated_all_referance_locations.csv"
# glass_certificate_full_file_path = r"C:\Users\malit\Documents\GitHub\2025_10_29_11_32_19\glass_certificate_2D_relative.csv"
# dot_center_encoder_location_matrix_file_path = r"C:\Users\malit\Documents\GitHub\2025_10_29_11_32_19\Expansion_array_2D_0.csv"


# # # # Create an instance of the encoder_error_matrix class and call the generate_2D_encoder_error_matrix method
# generate_encoder_error_matrix = encoder_error_matrix()
# encoder_error_matrix_new = generate_encoder_error_matrix.generate_2D_encoder_error_matrix(vision_log_file_file_path, location_matrix_file_path, glass_certificate_full_file_path, dot_center_encoder_location_matrix_file_path)

# full_path_x_errormap,full_path_y_errormap = generate_encoder_error_matrix.generate_ACS_errormaps(encoder_error_matrix_new, vision_log_file_file_path)
