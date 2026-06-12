#backend/sercices/plot_laser_vision_encoder_error.py

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

# modified
# Open file as 2D numpy array : for glass certificate file
def open_3D_location_file(glass_certificate_file_location,number_of_axis):
    array_2d = np.loadtxt(glass_certificate_file_location, delimiter=',')
    rows_in_file,column = array_2d.shape
    calibration_data_table_row = rows_in_file//number_of_axis
    calibration_data_table_column = column
    position_np_array = np.zeros((number_of_axis,calibration_data_table_row,calibration_data_table_column))
    position_np_array = array_2d.reshape(number_of_axis,calibration_data_table_row,calibration_data_table_column)
    return position_np_array


# Open file as 2D pandas and convert to numpy array : for log file
def open_file_pandas_convert_numpy(log_file_location):
    pandas_df = pd.read_csv(log_file_location)
    #print heder file 
    #print(pandas_df.head())
    # Convert the DataFrame to a numpy array
    log_file_numpy_array = pandas_df.to_numpy()
    return log_file_numpy_array

# getting the axis, active column, from the log file
def get_axis_serch_column_end_index_runs(log_file_1d_error_mapping_test_numpy_array):
    # Get the working axis
    if log_file_1d_error_mapping_test_numpy_array[1,3] - log_file_1d_error_mapping_test_numpy_array[0,3] :
        axis = 1
    else:
        axis = 0

    # get end value, row or column
    if axis == 0:
        test_end_target_index = np.max(log_file_1d_error_mapping_test_numpy_array[:,4])
        test_row_column = log_file_1d_error_mapping_test_numpy_array[1,3]
    elif axis == 1:
        test_end_target_index = np.max(log_file_1d_error_mapping_test_numpy_array[:,3])
        test_row_column = log_file_1d_error_mapping_test_numpy_array[1,4]

    # get the number of test runs
    test_runs = np.max(log_file_1d_error_mapping_test_numpy_array[:,1])+1

    print("Axis:",axis, ", End value:",test_end_target_index, ", Row or Column:",test_row_column, ", Test runs:",test_runs)
    return axis, test_end_target_index, test_row_column, test_runs




def add_column_to_numpy_array(numpy_array, new_column):
    # Ensure the new column has the same number of rows as the existing array
    if len(new_column) != numpy_array.shape[0]:
        raise ValueError("The new column must have the same number of rows as the existing array.")
    # Reshape the new column to be a 2D array with one column
    new_column = new_column.reshape(-1, 1)
    # Horizontally stack the new column to the existing array
    updated_array = np.hstack((numpy_array, new_column))
    return updated_array

def calculate_one_pixel_size(numpy_array,actual_radius,radius_column):
    mean_radius_pix = np.mean(numpy_array[:,radius_column]) 
    print("Mean radius in pixle = ",mean_radius_pix)
    one_pixel_size_um = (actual_radius/mean_radius_pix)*1000
    print("pixel size in um = ",one_pixel_size_um)
    return one_pixel_size_um

def create_full_file_path(ref_file_location, file_name):
    file_path = os.path.dirname(ref_file_location)
    file_path_name = os.path.join(file_path,file_name)
    return file_path_name

def calculate_step_size(glass_certificate_data_array, axis, test_row_column):

    glass_certificate_data = glass_certificate_data_array[axis][test_row_column][:]
    #step_size = glass_certificate_data_array[1,1] - glass_certificate_data_array[0,1]
    step_size = glass_certificate_data[-2]/14
    print("Step size in mm:",step_size)
    return step_size

def create_actual_dot_location_array(test_end_target_index,test_runs):
    actual_dot_location_array = np.zeros((test_end_target_index-1,(test_runs)*4+2))
    print("new arrary dimention",actual_dot_location_array.shape)
    return actual_dot_location_array

def first_two_column_filled(actual_dot_location_array,test_end_target_index, step_size):
    for i in range(0,test_end_target_index-1,1):
        actual_dot_location_array[i][0] = i+1
        actual_dot_location_array[i][1] = (i)*step_size

    return actual_dot_location_array


def calculate_actual_dot_seperation(log_file_1d_error_mapping_test_numpy_array,glass_certificate_data_array,axis,test_row_column,actual_dot_location_array_half_filled,one_pixel_size_um):
    # Open glass certificate
    # ==========================
    # axis 0
    # ==========================
    if axis == 0:
        glass_certificate_data = glass_certificate_data_array[axis][test_row_column][:]
        #print("Certificate shape:",glass_certificate_data)

        for i in range(0,log_file_1d_error_mapping_test_numpy_array.shape[0],1):
            index = log_file_1d_error_mapping_test_numpy_array[i][4]
            
            if index > 0 and index <= actual_dot_location_array_half_filled.shape[0]:
                cycle_number = log_file_1d_error_mapping_test_numpy_array[i][1]
                positive_or_negative = log_file_1d_error_mapping_test_numpy_array[i][4] - log_file_1d_error_mapping_test_numpy_array[i-1][4]

                if positive_or_negative == 1:
                    column_actual_positive = cycle_number*4+2
                    column_error_positive = cycle_number*4+3
                    actual_value = glass_certificate_data[index] - (log_file_1d_error_mapping_test_numpy_array[i,12]-1296)*one_pixel_size_um*0.001 #2592 1296
                    error = actual_value - actual_dot_location_array_half_filled[index-1,1] # actual value - calculated step distance 
                    #print("i:",i,", Index:",index, column_actual_positive, column_error_positive,",Actual value:",actual_value, ", Error:", error*1000, "um")
                    actual_dot_location_array_half_filled[index-1,column_actual_positive] = actual_value
                    actual_dot_location_array_half_filled[index-1,column_error_positive] = error

                elif positive_or_negative == -1:
                    column_actual_negative = cycle_number*4+4
                    column_error_negative = cycle_number*4+5
                    actual_value = glass_certificate_data[index] - (log_file_1d_error_mapping_test_numpy_array[i,12]-1296)*one_pixel_size_um*0.001
                    error = actual_value - actual_dot_location_array_half_filled[index-1,1] # actual value - calculated step distance 
                    #print("i:",i,", Index:",index, column_actual_positive, column_error_positive,",Actual value:",actual_value, ", Error:", error*1000, "um")
                    actual_dot_location_array_half_filled[index-1,column_actual_negative] = actual_value
                    actual_dot_location_array_half_filled[index-1,column_error_negative] = error


    #==========================
    # axis 1
    #==========================
    elif axis == 1:
        glass_certificate_data = glass_certificate_data_array[axis][test_row_column][:]
        #certificate_shape = glass_certificate_data.shape
        #print("Certificate shape:",certificate_shape)
        #print("actual dot matrix shape:",actual_dot_location_array_half_filled.shape)
        #print("Certificate shape:",glass_certificate_data)
        
        
        for i in range(0,log_file_1d_error_mapping_test_numpy_array.shape[0],1):
            index = log_file_1d_error_mapping_test_numpy_array[i][3]
            
            if index > 0 and index <= actual_dot_location_array_half_filled.shape[0]:
                cycle_number = log_file_1d_error_mapping_test_numpy_array[i][1]
                positive_or_negative = log_file_1d_error_mapping_test_numpy_array[i][3] - log_file_1d_error_mapping_test_numpy_array[i-1][3]

                if positive_or_negative == 1:
                    column_actual_positive = cycle_number*4+2
                    column_error_positive = cycle_number*4+3
                    actual_value = glass_certificate_data[index] - (log_file_1d_error_mapping_test_numpy_array[i,11]-1022)*one_pixel_size_um*0.001
                    error = actual_value - actual_dot_location_array_half_filled[index-1,1] # actual value - calculated step distance 
                    #print("i:",i,", Index:",index, column_actual_positive, column_error_positive,",Actual value:",actual_value, ", Error:", error*1000, "um")
                    actual_dot_location_array_half_filled[index-1,column_actual_positive] = actual_value
                    actual_dot_location_array_half_filled[index-1,column_error_positive] = error

                elif positive_or_negative == -1:
                    column_actual_negative = cycle_number*4+4
                    column_error_negative = cycle_number*4+5
                    actual_value = glass_certificate_data[index] - (log_file_1d_error_mapping_test_numpy_array[i,11]-1022)*one_pixel_size_um*0.001
                    error = actual_value - actual_dot_location_array_half_filled[index-1,1] # actual value - calculated step distance 
                    #print("i:",i,", Index:",index, column_actual_positive, column_error_positive,",Actual value:",actual_value, ", Error:", error*1000, "um")
                    actual_dot_location_array_half_filled[index-1,column_actual_negative] = actual_value
                    actual_dot_location_array_half_filled[index-1,column_error_negative] = error


    return actual_dot_location_array_half_filled


def plot_laser_row_data(laser_numpy_array,image_save_location_path_name,test_runs):
    plt.figure(figsize=(20, 10))
    plt.grid()
    plt.minorticks_on()
    plt.grid(which='both', axis='both', linestyle='-', linewidth=0.5)
    for test_cycle in range(0,test_runs,1):

        plt.plot(laser_numpy_array[:,1],(laser_numpy_array[:,3+test_cycle*6]) ,'red', label = "Run"+str(test_cycle+1)+"(+)",marker= '.') 
        plt.plot(laser_numpy_array[:,1],(laser_numpy_array[:,6+test_cycle*6]),'orange', label = "Calculated location"+str(test_cycle+1)+"(+)",marker = '.')

    plt.title("Estimating dot location using laser")
    plt.xlabel("Axis Position(mm)")
    plt.ylabel("Error (µm)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(image_save_location_path_name, dpi=300)
    plt.show()


def plot_vision_based_esitimate_dot_location(filled_actual_dot_location_array,test_runs,image_save_location_path_name):
     #plot the data
    plt.figure(figsize=(20, 10))
    plt.grid()
    plt.title("Estimating dot location using glass certificate & vision system")
    plt.xlabel("Laser location (mm)")
    plt.ylabel("Error (mm)")
    plt.minorticks_on()
    plt.grid(which='both', axis='both', linestyle='-', linewidth=0.5)
    
    for test_cycle in range(0,test_runs,1):

        plt.plot(filled_actual_dot_location_array[:,1],(filled_actual_dot_location_array[:,3+test_cycle*4]) ,'red', label = "Run"+str(test_cycle+1)+"(+)",marker= '.') 
        plt.plot(filled_actual_dot_location_array[:,1],(filled_actual_dot_location_array[:,5+test_cycle*4]),'orange', label = "Calculated location"+str(test_cycle+1)+"(+)",marker = '.')
        #plt.plot(esitimate_dot_location_array[:,1],(esitimate_dot_location_array[:,3+test_cycle*4] - laser_numpy_array[:,1]),'b', label = "Run"+str(test_cycle+1)+"(-)",marker = '.')
        #plt.plot(esitimate_dot_location_array[:,1],(esitimate_dot_location_array[:,4+test_cycle*4] - laser_numpy_array[:,1]),'c', label = "Calculated location"+str(test_cycle+1)+"(-)", marker = '.') 

    plt.xlabel("Axis Position(mm)")
    plt.ylabel("Error (µm)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(image_save_location_path_name, dpi=300)
    plt.show()


##### main function #####

def calculate_and_plot_repetability_after_error_map(glass_certificate_file_location,log_file_1d_error_mapping_test):
#def calculate_and_plot_repetability_after_error_map(laser_row_data_file_part,glass_certificate_file_location,log_file_1d_error_mapping_test):
    number_of_axis = 3

    # Open log file
    #print(log_file_1d_error_mapping_test)
    log_file_1d_error_mapping_test_numpy_array = open_file_pandas_convert_numpy(log_file_1d_error_mapping_test)
    axis, test_end_target_index, test_row_column, test_runs = get_axis_serch_column_end_index_runs(log_file_1d_error_mapping_test_numpy_array)
    # calculate the pixel size in um
    actual_radius_mm = 0.25 #mm
    radius_column = 13
    one_pixel_in_um = calculate_one_pixel_size(log_file_1d_error_mapping_test_numpy_array,actual_radius_mm,radius_column)
    #print(one_pixel_in_um)
    

    # Open glass certificate
    glass_certificate_data_array = open_3D_location_file(glass_certificate_file_location,number_of_axis)
    print(glass_certificate_data_array.shape)
    # get step size in mm
    step_size = calculate_step_size(glass_certificate_data_array, axis, test_row_column)
    print(step_size)


    # Open laser row data file
    #laser_numpy_array = open_file_pandas_convert_numpy(laser_row_data_file_part)
    #print(laser_numpy_array.shape)
    #print(laser_numpy_array[:,2])
    #step_size = calculate_step_size(laser_numpy_array)
    #print(laser_numpy_array)

    # plot the laser row data and save image
    #image_save_location_path_name = create_full_file_path(laser_row_data_file_part,"laser_row_data_plot.png")
    #plot_laser_row_data(laser_numpy_array,image_save_location_path_name,test_runs)


    # create empty array to store the actual dot location and error date
    actual_dot_location_array = create_actual_dot_location_array(test_end_target_index,test_runs)

    actual_dot_location_array_half_filled = first_two_column_filled(actual_dot_location_array,test_end_target_index, step_size)
    #print(fill_first_2_columns_actual_dot_location_array)
    
    file_save_location_path_name = create_full_file_path(log_file_1d_error_mapping_test,"vision_based_esitimate_dot_location_array.csv")
    filled_actual_dot_location_array = calculate_actual_dot_seperation(log_file_1d_error_mapping_test_numpy_array,glass_certificate_data_array,axis,test_row_column,actual_dot_location_array_half_filled,one_pixel_in_um)

    # save the filled array
    np.savetxt(file_save_location_path_name, filled_actual_dot_location_array, delimiter=",", fmt='%.6f')

     
    # plot laser and image based repetability image and save
    image_save_location_path_name = create_full_file_path(log_file_1d_error_mapping_test,"vision_based_error_map_plot.png")
    plot_vision_based_esitimate_dot_location(filled_actual_dot_location_array,test_runs,image_save_location_path_name)

#    
#    # plot variable pitch encoder values vs encoder values after centering
#    image_save_location_path_name = create_full_file_path(laser_file_location,"encoder_values_vs_calculated_encoder_values.png")
#    if test_cycle_count >= 5:
#        plot_encoder_values_vs_calculated_encoder_values(varible_pitch_array,log_file_1d_error_mapping_test_with_x_axis_error,test_cycle_count,image_save_location_path_name)  
#
#    # plot vision baseed error vs location
#    image_save_location_path_name = create_full_file_path(laser_file_location,"vision_based_error_vs_location.png")
#    plot_vision_based_error_vs_location(log_file_1d_error_mapping_test_with_x_axis_error,image_save_location_path_name)
#


# self centerd with laser data - 2024_12_02_13_45_59
#varible_pitch_file_location = r"C:/Users/mj.j/OneDrive - PBA Systems Pte. Ltd/GitHub/Github/2024_12_02_16_19_27_plot/variable_pitch.csv"
#expantion_file_location = r"C:/Users/mj.j/OneDrive - PBA Systems Pte. Ltd/GitHub/Github/2024_12_02_16_19_27_plot/Expansion_array_positive0.csv"
#laser_file_location = r"C:/Users/mj.j/OneDrive - PBA Systems Pte. Ltd/GitHub/Github/2024_12_02_16_19_27_plot/laser_row_data.csv"
#log_file_1d_error_mapping_test = r"C:/Users/mj.j/OneDrive - PBA Systems Pte. Ltd/GitHub/Github/2024_12_02_16_19_27_plot/Log_file_full.csv"

#calculate_actual_dot_seperation(varible_pitch_file_location,expantion_file_location,laser_file_location,log_file)
#calculate_actual_dot_seperation(varible_pitch_file_location,laser_file_location,log_file_1d_error_mapping_test)



# Repetability After error map  
# glass certificate provides distance bitween two dots
#laser_row_data_file_part = r"C:\Users\mj.j\OneDrive - PBA Systems Pte. Ltd\GitHub\Github\2025_02_13_16_48_52_GC\laser_row_date.csv"
#glass_certificate_file_location = r"C:\Users\mj.j\OneDrive - PBA Systems Pte. Ltd\GitHub\Github\2025_02_13_16_48_52_GC\glass_certificate.csv"
#log_file_1d_error_mapping_test = r"C:\Users\mj.j\OneDrive - PBA Systems Pte. Ltd\GitHub\Github\2025_02_14_11_12_45\Log_file_1D.csv"
#calculate_and_plot_repetability_after_error_map(laser_row_data_file_part,glass_certificate_file_location,log_file_1d_error_mapping_test)
#calculate_and_plot_repetability_after_error_map(glass_certificate_file_location,log_file_1d_error_mapping_test)

