import os
import datetime
import numpy as np



# read file path 
def read_location_file(calculated_location_array):
    no_of_axis = 3
    calculated_array_2d = np.loadtxt(calculated_location_array, delimiter=',')
    rows_in_file,column = calculated_array_2d.shape
    calculated_calibration_data_table_row = rows_in_file//no_of_axis
    calibration_data_table_column = column
    calculated_position_np_array = calculated_array_2d.reshape(no_of_axis,calculated_calibration_data_table_row,calibration_data_table_column)
    # X axis 
    #print(calculated_position_np_array[axis][row][column])
    return calculated_position_np_array
    

def read_distance(calculated_position_np_array):
    print(calculated_position_np_array.shape)
    sum = 0
    for j in range (0,41,1):
        #print(j,calculated_position_np_array[1][j][0])
        sum = sum + calculated_position_np_array[1][j][0]

    print(sum)
    print(calculated_position_np_array[1][j][1])
    total_distance = sum + calculated_position_np_array[1][j][1] - calculated_position_np_array[1][0][1]
    print(total_distance)


glass_certificate_file_path = r"C:\Users\malit\OneDrive\Documents\GitHub\2025_05_13_09_35_46\glass_certificate_2D_relative.csv"
calculated_position_np_array = read_location_file(glass_certificate_file_path)
read_distance(calculated_position_np_array)
