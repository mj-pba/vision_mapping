# /src/backend/services/generate_glass_certificate_62207.py
# Issue:#28 
# Generate glass certificate 62207
# files required : laser_row_data.csv, variable_pitch.csv
# output : glass_certificate.csv

# this method was not correct 2025.01.08 : only laser data is used to generate the glass certificate
# I need to use vision data also to generate the glass certificate


import numpy as np
import pandas as pd
import csv
import os


# Open file as 2D pandas and convert to numpy array : for log file
def open_file_pandas_convert_numpy(file_location):
    pandas_df = pd.read_csv(file_location)
    #print heder file 
    #print(pandas_df.head())
    # Convert the DataFrame to a numpy array
    numpy_array = pandas_df.to_numpy()
    return numpy_array, numpy_array.shape


def read_laser_row_data_file(laser_row_data_file_part):
    '''Read the laser row data file and return the data as a numpy array'''
    try:
        # Read the data from laser row data file
        #print(f"Reading data from: {laser_row_data_file_part}")
        data = pd.read_csv(laser_row_data_file_part)
        # convert to numpy array
        data = data.to_numpy()
        return data
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_number_of_cycles(shape):
    '''Get the number of cycles from the shape of the data'''
    columns = 0
    while columns < shape:
        if columns == 0:
            columns = 5
            runs = 1
        else:
            columns += 6
            runs += 1
    return runs-1


def mesured_value_columns(runs):
    '''Get the column number of the mesured value columns'''
    P = 0
    mesured_value_columns = []
    for i in range(runs):
        if P == 0:
            P = 2 + 3 * i
            N = P + 3
            mesured_value_columns.append(P)
            mesured_value_columns.append(N)
            P = N
        else:
            P = P + 3
            N = P + 3
            mesured_value_columns.append(P)
            mesured_value_columns.append(N)
            P = N
    return mesured_value_columns


def get_mesured_values_mean(data, mesured_value_columns_list):
    '''Get the measured values mean from the data'''
    mesured_values = []
    for i in range(len(mesured_value_columns_list)):
        mesured_values.append(data[:, mesured_value_columns_list[i]])   
    mesured_values = np.array(mesured_values)
    #print(f"measured values :{mesured_values[1,:]}")
    mean_values = mesured_values.mean(axis=0)
    return mean_values

#def get_mesured_values_mean(data, mesured_value_columns_list):
#    '''get mesured vlaue mean value after removed abnormal values'''
#    mesured_values = []
#    for i in range(len(mesured_value_columns_list)):    
#        mesured_values.append(data[:, mesured_value_columns_list[i]])
#    
#    print (mesured_values)
#    # remove the abnormal values
#    for i in range(len(mesured_values)):
#        mean = np.mean(mesured_values[i])
#        std = np.std(mesured_values[i])
#        #print(f"mean:{mean}, std:{std}")
#        for j in range(len(mesured_values[i])):
#            if mesured_values[i][j] > mean + 3*std or mesured_values[i][j] < mean - 3*std:
#                mesured_values[i][j] = mean
#
#
#    mesured_values = np.array(mesured_values)
#    #print(f"measured values :{mesured_values[1,:]}")
#    mean_values = mesured_values.mean(axis=0)
#    return mean_values


def make_fist_value_zero(mean_values):
    '''Make the first value of the mean values zero'''
    mean_values_shifted = mean_values - mean_values[0]
    return mean_values_shifted


# Open file as 3D numpy array : for location file
def open_3D_location_file(file_location,number_of_axis):
    array_2d = np.loadtxt(file_location, delimiter=',')
    rows_in_file,column = array_2d.shape
    calibration_data_table_row = rows_in_file//number_of_axis
    calibration_data_table_column = column
    position_np_array = np.zeros((number_of_axis,calibration_data_table_row,calibration_data_table_column))
    position_np_array = array_2d.reshape(number_of_axis,calibration_data_table_row,calibration_data_table_column)
    return position_np_array

def create_glass_certificate_62207_matrix(array_shape):
    # Define the data
    new_array = np.zeros(array_shape)
    return new_array

#def add_mesured_values_to_matrix(glass_certificate_matrix,mesured_values_index,mean_values_shifted,axis,row):
#    # Add the mesured values to the matrix
#    print(int(axis),int(row))
#    for i in range(len(mesured_values_index)):
#        index = mesured_values_index[i]
#        #glass_certificate_matrix[axis,row,column]
#        # axis : x,y,z
#        # row : 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16    for variable pitch matrix
#        # column : 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16   for variable pitch matrix    
#        glass_certificate_matrix[0,8,index] = mean_values_shifted[i]
#        #print (i,index,glass_certificate_matrix[0,index,8])
#    return glass_certificate_matrix
#

# Y axis glass certificate creation 
def add_mesured_values_to_matrix(glass_certificate_matrix,mesured_values_index,mean_values_shifted,select_axis,row_or_column):
    # Add the mesured values to the matrix
    axis = int(select_axis)
    print("add mesured values:",axis,row_or_column)

    if axis == 0:
        row = int(row_or_column)
        for i in range(len(mesured_values_index)):
            index = mesured_values_index[i]
            #glass_certificate_matrix[axis,row,column]
            # axis : x,y,z
            # row : 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16    for variable pitch matrix
            # column : 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16   for variable pitch matrix    
            #glass_certificate_matrix[0,8,index] = mean_values_shifted[i]
            glass_certificate_matrix[axis,row,index] = mean_values_shifted[i]
        return glass_certificate_matrix

    elif axis == 1:
        column = int(row_or_column)
        for i in range(len(mesured_values_index)):
            index = mesured_values_index[i]
            glass_certificate_matrix[axis,column,index] = mean_values_shifted[i]
        return glass_certificate_matrix


def create_full_file_path(ref_file_location, file_name):
    file_path = os.path.dirname(ref_file_location)
    file_path_name = os.path.join(file_path,file_name)
    return file_path_name

def save_dot_locations_matrix(position_np_array,file_path ):
    # cannot save the 3D array have to reshape to 2D
    array_2d = position_np_array.reshape(-1, position_np_array.shape[-1])     
    np.savetxt(file_path, array_2d, delimiter=',', fmt='%.6f')      # save 2D file to .csv format
    print("Save file to:", file_path)


# plot the glass certificate matrix as linear graph
def plot_3D_matrix(glass_certificate_matrix_with_data,full_file_path):
    import matplotlib.pyplot as plt
    import numpy as np
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
    


# main function to generate glass certificate
# Pourpose of each input file is as follows
# laser_row_data.csv: to get the measured values
# variable_pitch.csv: Obtain the shape of the matrix, and create same shape matrix to store the measured values.

# Process flow 1
# 1. Read the laser row data file get numpy array
# 2. Get the number of cycles from the shape of the data
# 3. Get the column number of the mesured value columns
# 4. Get the measured values mean from the data
# 5. Make the first value of the mean values zero
# 6. Read the variable pitch matrix
# 7. Create a glass certificate matrix with the same shape as the variable pitch matrix
# 8. Add the mesured values to the glass certificate matrix
# 9. Save the glass certificate matrix
# 10. Plot the glass certificate matrix

# Process flow 2 : 
#       Previus glass certificate only work for x axis now I need to make it work for y axis also.
#       So there are two axis x and y and it will be a full 3D matrix
#       Propsed pocess flow need to modifiy to undestand the rows and columns of log file
# 1. Read the log file and identify rows or columns which to generate the glass certificate 
# 2. Read the laser row data file get numpy array
# 3. Get the number of cycles from the shape of the data
# 4. Get the column number of the mesured value columns
# 5. Get the measured values mean from the data
# 6. Make the first value of the mean values zero
# 7. Read the variable pitch matrix
# 8. Create a glass certificate matrix with the same shape as the variable pitch matrix
# 9. Add the mesured values to the glass certificate matrix



def generate_glass_certificate(laser_row_data_file_part,variable_pitch_matrix_file_path,vision_log_file_file_path):

    numpy_array, numpy_array_shape = open_file_pandas_convert_numpy(vision_log_file_file_path)
    #print(f"vision log file shape: {numpy_array_shape}")
    #print(numpy_array[0][3])

    axis=1
    row_or_column=8

    laser_row_data = read_laser_row_data_file(laser_row_data_file_part)
    #print(f"laser row data shape: {laser_row_data.shape}")

    if laser_row_data is not None:
        runs = get_number_of_cycles(laser_row_data.shape[1])
        steps = laser_row_data.shape[0]
        #print(f"Number of steps: {steps}, Number of runs: {runs}")
        mesured_value_columns_list = mesured_value_columns(runs)
        mean_values = get_mesured_values_mean(laser_row_data, mesured_value_columns_list)
        mean_values_shifted = make_fist_value_zero(mean_values)
        #print(f"mean values :{mean_values}")
        #print(f"mean values shifted:{mean_values_shifted}")

        # Read the variable pitch matrix
        number_of_axis = 3
        variable_pitch_matrix = open_3D_location_file(variable_pitch_matrix_file_path,number_of_axis)
        glass_certificate_matrix = create_glass_certificate_62207_matrix(variable_pitch_matrix.shape)

        # Add the mesured values to the matrix
        
        glass_certificate_matrix_with_data = add_mesured_values_to_matrix(glass_certificate_matrix,laser_row_data[:,0],mean_values_shifted,axis,row_or_column)

        # Save the glass certificate
        full_file_path = create_full_file_path(laser_row_data_file_part,"glass_certificate.csv")
        save_dot_locations_matrix(glass_certificate_matrix_with_data,full_file_path)

        # plot the glass certificate
        full_file_path = create_full_file_path(laser_row_data_file_part,"glass_certificate.png")
        plot_3D_matrix(glass_certificate_matrix_with_data,full_file_path)





# Test the function
#laser_row_data_file_part = r"C:\Users\mj.j\OneDrive - PBA Systems Pte. Ltd\GitHub\Github\2024_12_02_16_19_27_plot\laser_row_data.csv"
#variable_pitch_matrix_file_path = r"C:\Users\mj.j\OneDrive - PBA Systems Pte. Ltd\GitHub\Github\2024_12_02_16_19_27_plot\variable_pitch.csv"
## axis = 0 - x axis

##row = 8 - 8th row of the variable pitch matrix
#generate_glass_certificate(laser_row_data_file_part,variable_pitch_matrix_file_path)#

#laser_row_data_file_part =r"C:\Users\mj.j\OneDrive - PBA Systems Pte. Ltd\GitHub\Github\2025_01_14_11_21_37_GC\laser_row_data.csv"
#variable_pitch_matrix_file_path =r"C:\Users\mj.j\OneDrive - PBA Systems Pte. Ltd\GitHub\Github\2025_01_14_11_21_37_GC\variable_pitch.csv"
#generate_glass_certificate(laser_row_data_file_part,variable_pitch_matrix_file_path)

#laser_row_data_file_part =r"C:\Users\mj.j\OneDrive - PBA Systems Pte. Ltd\GitHub\Github\2025_01_17_09_20_47\laser_row_data.csv"
#variable_pitch_matrix_file_path =r"C:\Users\mj.j\OneDrive - PBA Systems Pte. Ltd\GitHub\Github\2025_01_17_08_59_51\variable_pitch_2.csv"
#generate_glass_certificate(laser_row_data_file_part,variable_pitch_matrix_file_path)


#axis = 1 - y axis
#laser_row_data_file_part =r"C:\Users\mj.j\OneDrive - PBA Systems Pte. Ltd\GitHub\Github\2025_01_21_17_07_13\laser_row_data.csv"
#variable_pitch_matrix_file_path =r"C:\Users\mj.j\OneDrive - PBA Systems Pte. Ltd\GitHub\Github\2025_01_20_15_20_58\variable_pitch_8_1_zero.csv"
#vision_log_file_file_path = r"C:\Users\mj.j\OneDrive - PBA Systems Pte. Ltd\GitHub\Github\2025_01_21_17_07_13\Log_file_1D_expansion.csv"
#generate_glass_certificate(laser_row_data_file_part,variable_pitch_matrix_file_path,vision_log_file_file_path)


#axis = 1 - y axis
#laser_row_data_file_part = r"C:\Users\mj.j\OneDrive - PBA Systems Pte. Ltd\GitHub\Github\2025_02_03_13_11_49\laser_row_date.csv"
#variable_pitch_matrix_file_path = r"C:\Users\mj.j\OneDrive - PBA Systems Pte. Ltd\GitHub\Github\2025_02_03_10_21_50\variable_pitch_8_1_zero.csv"
#vision_log_file_file_path = r"C:\Users\mj.j\OneDrive - PBA Systems Pte. Ltd\GitHub\Github\2025_02_03_13_11_49\Log_file_1D_expansion.csv"
#generate_glass_certificate(laser_row_data_file_part,variable_pitch_matrix_file_path,vision_log_file_file_path)
