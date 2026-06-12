#backend/sercices/plot_laser_vision_encoder_error.py

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt


# Open file as 3D numpy array : for location file
def open_location_file(file_location,number_of_axis):
    array_2d = np.loadtxt(file_location, delimiter=',')
    rows_in_file,column = array_2d.shape
    calibration_data_table_row = rows_in_file//number_of_axis
    calibration_data_table_column = column
    position_np_array = np.zeros((number_of_axis,calibration_data_table_row,calibration_data_table_column))
    position_np_array = array_2d.reshape(number_of_axis,calibration_data_table_row,calibration_data_table_column)
    return position_np_array

# Open file as 2D pandas and convert to numpy array : for log file
def open_file_pandas_convert_numpy(file_location):
    pandas_df = pd.read_csv(file_location)
    #print heder file 
    #print(pandas_df.head())
    # Convert the DataFrame to a numpy array
    numpy_array = pandas_df.to_numpy()
    return numpy_array

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
    pixle_per_um = (actual_radius/mean_radius_pix)*1000
    print("pixel size in um = ",pixle_per_um)
    return pixle_per_um


def calculate_x_axis_error(numpy_array, x_axis_column, pixle_per_um):
    axis_x_position_error_um = (numpy_array[:,x_axis_column] - 1296)*pixle_per_um
    return axis_x_position_error_um


def create_full_file_path(ref_file_location, file_name):
    file_path = os.path.dirname(ref_file_location)
    file_path_name = os.path.join(file_path,file_name)
    return file_path_name



# calculate actual dot seperation using laser feedback value and vision system dot center error. Save to values to file and return the array 
def calculate_actual_dot_seperation_using_laser_and_vision_system(laser_numpy_array,log_file_1d_error_mapping_test_with_x_axis_error,test_cycle_count,file_save_location_path_name):
    # create a new array to store the data
    esitimate_dot_location_array_column = 1+test_cycle_count*4
    esitimate_dot_location_array = np.zeros((laser_numpy_array.shape[0],esitimate_dot_location_array_column))

    #print (esitimate_dot_location_array.shape)
    #print (log_file_1d_error_mapping_test_with_x_axis_error.shape)

    log_file_index = 1

    #print(laser_numpy_array.shape)

    for test_cycle in range(0,test_cycle_count,1):
        column = 2+test_cycle*6
        #print("Cycle",test_cycle,"Column:",column)
       
        for laser_numpy_array_index in range(0,laser_numpy_array.shape[0],1):
            #print(laser_numpy_array[x,0],laser_numpy_array[x,1],laser_numpy_array[x,2])
            laser_row_data_file_index = laser_numpy_array_index + 1
            laser_and_visaion_based_location = laser_numpy_array[laser_numpy_array_index,column] - log_file_1d_error_mapping_test_with_x_axis_error[log_file_index,18]/1000
            '''print(
                "laser_row_data_file_index:",laser_row_data_file_index,
                "   Actual value from laser:", laser_numpy_array[laser_numpy_array_index,column],"mm"
                "   Image index:",log_file_1d_error_mapping_test_with_x_axis_error[log_file_index,3],
                "   Error from vision:",log_file_1d_error_mapping_test_with_x_axis_error[log_file_index,17],"um",
                "   Claculated location :",laser_and_visaion_based_location,"mm"
                )'''

            #esitimate_dot_location_array[log_file_index-1,0] = test_cycle                                                              # test cycle    
            esitimate_dot_location_array[laser_numpy_array_index,0] = laser_row_data_file_index                                         # laser row data file index
            esitimate_dot_location_array[laser_numpy_array_index,1+test_cycle*4] = laser_numpy_array[laser_numpy_array_index,column]    # actual value from laser
            esitimate_dot_location_array[laser_numpy_array_index,2+test_cycle*4] = laser_and_visaion_based_location                     # calculated location
            log_file_index = log_file_index + 1 

        #print("-----------------------------")
        log_file_index = log_file_index + 1 
        for laser_numpy_array_index in range(laser_numpy_array.shape[0]-1,-1,-1):
            laser_row_data_file_index = laser_numpy_array_index + 1
            laser_and_visaion_based_location = laser_numpy_array[laser_numpy_array_index,column+3] - log_file_1d_error_mapping_test_with_x_axis_error[log_file_index,18]/1000
            '''print(
                "laser_row_data_file_index:",laser_row_data_file_index,
                "Actual value from laser:", laser_numpy_array[laser_numpy_array_index,column+3],"mm"
                "Image index:",log_file_1d_error_mapping_test_with_x_axis_error[log_file_index,3],
                "Error from vision:",log_file_1d_error_mapping_test_with_x_axis_error[log_file_index,17],"um",
                "Claculated location :",laser_and_visaion_based_location,"mm"
                )'''

            #esitimate_dot_location_array[log_file_index-1,0] = test_cycle                                                              # test cycle
            esitimate_dot_location_array[laser_numpy_array_index,0] = laser_row_data_file_index                                         # laser row data file index
            esitimate_dot_location_array[laser_numpy_array_index,3+test_cycle*4] = laser_numpy_array[laser_numpy_array_index,column+3]  # actual value from laser
            esitimate_dot_location_array[laser_numpy_array_index,4+test_cycle*4] = laser_and_visaion_based_location                     # calculated location

            log_file_index = log_file_index + 1

        #print("-----------------------------")
        log_file_index = log_file_index + 1 

    # save the data to a file
    esitimate_dot_location_array_df = pd.DataFrame(esitimate_dot_location_array)

    # create for loop to add the header to the data frame using the test_cycle_count
    column_count  = test_cycle_count*4+1
    header = np.zeros((column_count),dtype=object)
    header[0] = ("Index")
    for test_cycle in range(0,test_cycle_count,1):
        header[test_cycle*4+1] = str("Run "+str(test_cycle+1)+" (+) Position")
        header[test_cycle*4+2] = str("Calculated location "+str(test_cycle+1)+" (+)")
        header[test_cycle*4+3] = str("Run "+str(test_cycle+1)+" (-) Position")
        header[test_cycle*4+4] = str("Calculated location "+str(test_cycle+1)+" (-)")
    
    esitimate_dot_location_array_df.columns = header


    esitimate_dot_location_array_df.to_csv(file_save_location_path_name,index=False)
    return esitimate_dot_location_array 


def plot_laser_and_vision_based_esitimate_dot_location(laser_numpy_array,esitimate_dot_location_array,test_cycle_count,image_save_location_path_name):
     #plot the data
    plt.figure(figsize=(20, 10))
    plt.grid()
    plt.title("Estimating dot location using laser and vision system")
    plt.xlabel("Laser location (mm)")
    plt.ylabel("Error (mm)")
    plt.minorticks_on()
    plt.grid(which='both', axis='both', linestyle='-', linewidth=0.5)
    
    for test_cycle in range(0,test_cycle_count,1):

        plt.plot(esitimate_dot_location_array[:,1],(esitimate_dot_location_array[:,1+test_cycle*4] - laser_numpy_array[:,1]) ,'red', label = "Run"+str(test_cycle+1)+"(+)",marker= '.') 
        plt.plot(esitimate_dot_location_array[:,1],(esitimate_dot_location_array[:,2+test_cycle*4] - laser_numpy_array[:,1]),'orange', label = "Calculated location"+str(test_cycle+1)+"(+)",marker = '.')
        plt.plot(esitimate_dot_location_array[:,1],(esitimate_dot_location_array[:,3+test_cycle*4] - laser_numpy_array[:,1]),'b', label = "Run"+str(test_cycle+1)+"(-)",marker = '.')
        plt.plot(esitimate_dot_location_array[:,1],(esitimate_dot_location_array[:,4+test_cycle*4] - laser_numpy_array[:,1]),'c', label = "Calculated location"+str(test_cycle+1)+"(-)", marker = '.') 

    plt.legend()
    plt.tight_layout()
    plt.savefig(image_save_location_path_name, dpi=300)
    plt.show()

    


def plot_encoder_values_vs_calculated_encoder_values(varible_pitch_array, log_file_1d_error_mapping_test_with_x_axis_error, test_cycle_count,image_save_location_path_name):
    calculated_location =  varible_pitch_array[0,7,:]
    print(calculated_location)
    actual_location_run_1_positive = log_file_1d_error_mapping_test_with_x_axis_error[:17,5]
    actual_location_run_1_negative = np.sort(log_file_1d_error_mapping_test_with_x_axis_error[16:33,5])
    actual_location_run_2_positive = log_file_1d_error_mapping_test_with_x_axis_error[32:49,5]
    actual_location_run_2_negative = np.sort(log_file_1d_error_mapping_test_with_x_axis_error[48:65,5])
    actual_location_run_3_positive = log_file_1d_error_mapping_test_with_x_axis_error[64:81,5]
    actual_location_run_3_negative = np.sort(log_file_1d_error_mapping_test_with_x_axis_error[80:97,5])
    actual_location_run_4_positive = log_file_1d_error_mapping_test_with_x_axis_error[96:113,5]
    actual_location_run_4_negative = np.sort(log_file_1d_error_mapping_test_with_x_axis_error[112:129,5])
    actual_location_run_5_positive = log_file_1d_error_mapping_test_with_x_axis_error[128:145,5]
    actual_location_run_5_negative = np.sort(log_file_1d_error_mapping_test_with_x_axis_error[144:160,5])

    plt.figure(figsize=(20, 10))
    plt.grid()
    plt.title("Encoder values vs calculated encoder values")
    plt.xlabel("Encoder values")
    plt.ylabel("Error (mm)")
    
    #for test_cycle in range(0,test_cycle_count,1):
    plt.plot(calculated_location,((actual_location_run_1_positive-calculated_location)*-1),'red', label = "1 run positive",marker= '.') 
    plt.plot(calculated_location,((actual_location_run_1_negative-calculated_location)*-1),'orange', label = "1 run negative",marker = '.')
    plt.plot(calculated_location,((actual_location_run_2_positive-calculated_location)*-1),'b', label = "2 run positive",marker = '.')
    plt.plot(calculated_location,((actual_location_run_2_negative-calculated_location)*-1),'c', label = "2 run negative", marker = '.')
    plt.plot(calculated_location,((actual_location_run_3_positive-calculated_location)*-1),'m', label = "3 run positive", marker = '.')
    plt.plot(calculated_location,((actual_location_run_3_negative-calculated_location)*-1),'y', label = "3 run negative", marker = '.')
    plt.plot(calculated_location,((actual_location_run_4_positive-calculated_location)*-1),'k', label = "4 run positive", marker = '.')
    plt.plot(calculated_location,((actual_location_run_4_negative-calculated_location)*-1),'g', label = "4 run negative", marker = '.')
    plt.plot(calculated_location,((actual_location_run_5_positive-calculated_location)*-1),'purple', label = "5 run positive", marker = '.')
    #plt.plot(calculated_location,((actual_location_run_5_negative-calculated_location)*-1),'brown', label = "5 run negative", marker = '.')

    plt.tight_layout()
    plt.legend()
    plt.savefig(image_save_location_path_name, dpi=300)
    plt.show()
    

def plot_vision_based_error_vs_location(log_file_1d_error_mapping_test_with_x_axis_error,image_save_location_path_name):
    plt.figure(figsize=(20, 10))
    plt.grid()
    plt.title("Vision based error vs location")
    plt.xlabel("Location")
    plt.ylabel("Error (um)")
    plt.minorticks_on()
    plt.grid(which='both', axis='both', linestyle='-', linewidth=0.5)
    
    plt.plot(log_file_1d_error_mapping_test_with_x_axis_error[:,5],log_file_1d_error_mapping_test_with_x_axis_error[:,18],'red', label = "Vision based error",marker= '.') 

    plt.legend()
    plt.tight_layout()
    plt.savefig(image_save_location_path_name, dpi=300)
    plt.show()


### get number of cyles from the shape of the data
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



##### main function #####

def calculate_actual_dot_seperation(varible_pitch_file_location,laser_file_location,log_file_1d_error_mapping_test):
    number_of_axis = 3
#    print(varible_pitch_file_location)
    varible_pitch_array = open_location_file(varible_pitch_file_location,number_of_axis)
#    print(varible_pitch_array.shape)
#
#    print(expantion_file_location)
#    expantion_array = open_location_file(expantion_file_location,number_of_axis)
#    print(expantion_array.shape)
#

##### processing log file data working code blcok ####
    print(log_file_1d_error_mapping_test)
    log_file_1d_error_mapping_test_numpy_array = open_file_pandas_convert_numpy(log_file_1d_error_mapping_test)

    # calculate the pixel size in um
    actual_radius_mm = 0.25 #mm
    radius_column = 13
    one_pixel_in_um = calculate_one_pixel_size(log_file_1d_error_mapping_test_numpy_array,actual_radius_mm,radius_column)

    # calculate the x axis error in um using vision system
    dot_location_center_vision_x_axis_column = 12
    axis_x_position_error_um = calculate_x_axis_error(log_file_1d_error_mapping_test_numpy_array,dot_location_center_vision_x_axis_column,one_pixel_in_um)
    print(axis_x_position_error_um.shape)

    # add that array to the  log_file_1d_error_mapping_test_numpy_array array
    log_file_1d_error_mapping_test_with_x_axis_error = add_column_to_numpy_array(log_file_1d_error_mapping_test_numpy_array,axis_x_position_error_um)
    print("New combined array dimention",log_file_1d_error_mapping_test_with_x_axis_error.shape)

    # save the data to a file
    file_save_location_path_name = create_full_file_path(log_file_1d_error_mapping_test,"log_file_1d_error_mapping_test_with_x_axis_error.csv")
    log_file_1d_error_mapping_test_with_x_axis_error_df = pd.DataFrame(log_file_1d_error_mapping_test_with_x_axis_error)
    log_file_1d_error_mapping_test_with_x_axis_error_df.to_csv(file_save_location_path_name,index=False)

    #### processing laser data working code block ####
    print(laser_file_location)
    laser_numpy_array = open_file_pandas_convert_numpy(laser_file_location)

    # calculate the dot location using laser and vision system and creat an array
    test_cycle_count = get_number_of_cycles(laser_numpy_array.shape[1])
    file_save_location_path_name = create_full_file_path(laser_file_location,"laser_and_vision_based_esitimate_dot_location_array.csv")
    esitimate_dot_location_array = calculate_actual_dot_seperation_using_laser_and_vision_system(laser_numpy_array,log_file_1d_error_mapping_test_with_x_axis_error,test_cycle_count,file_save_location_path_name)
    
    # plot laser and image based repetability image and save
    image_save_location_path_name = create_full_file_path(laser_file_location,f"laser_and_vision_based_esitimate_dot_location_array_{test_cycle_count}.png")
    plot_laser_and_vision_based_esitimate_dot_location(laser_numpy_array,esitimate_dot_location_array,test_cycle_count,image_save_location_path_name)
    
    # plot variable pitch encoder values vs encoder values after centering
    image_save_location_path_name = create_full_file_path(laser_file_location,"encoder_values_vs_calculated_encoder_values.png")
    if test_cycle_count >= 5:
        plot_encoder_values_vs_calculated_encoder_values(varible_pitch_array,log_file_1d_error_mapping_test_with_x_axis_error,test_cycle_count,image_save_location_path_name)  

    # plot vision baseed error vs location
    image_save_location_path_name = create_full_file_path(laser_file_location,"vision_based_error_vs_location.png")
    plot_vision_based_error_vs_location(log_file_1d_error_mapping_test_with_x_axis_error,image_save_location_path_name)



#### custom file location and function call  - test 1
#varible_pitch_file_location = r"C:/Users/mj.j/OneDrive - PBA Systems Pte. Ltd/GitHub/Github/2024_11_11/variable_pitch_location_matrix.csv"
#expantion_file_location = r"C:/Users/mj.j/OneDrive - PBA Systems Pte. Ltd/GitHub/Github/2024_11_11/Expansion_array_positive0.csv"
#laser_file_location = r"C:/Users/mj.j/OneDrive - PBA Systems Pte. Ltd/GitHub/Github/2024_11_11/laser_row_data_csv.csv"
#log_file_1d_error_mapping_test = r"C:/Users/mj.j/OneDrive - PBA Systems Pte. Ltd/GitHub/Github/2024_11_11/Log_file_1D.csv"

#varible_pitch_file_location = r"C:/Users/mj.j/OneDrive - PBA Systems Pte. Ltd/GitHub/Github/2024_11_18/variable_pitch_10_10.csv"
#expantion_file_location = r"C:/Users/mj.j/OneDrive - PBA Systems Pte. Ltd/GitHub/Github/2024_11_18_13_08_37/Expansion_array_positive0.csv"
#laser_file_location = r"C:/Users/mj.j/OneDrive - PBA Systems Pte. Ltd/GitHub/Github/2024_11_18/laser_row_data.csv"
#log_file_1d_error_mapping_test = r"C:/Users/mj.j/OneDrive - PBA Systems Pte. Ltd/GitHub/Github/2024_11_18_15_25_57/Log_file_1D.csv"

# self centerd with laser data
#varible_pitch_file_location = r"C:/Users/mj.j/OneDrive - PBA Systems Pte. Ltd/GitHub/Github/2024_11_19/variable pitch.csv"
#expantion_file_location = r"C:/Users/mj.j/OneDrive - PBA Systems Pte. Ltd/GitHub/Github/2024_11_19_11_44_56/Expansion_array_positive0.csv"
#laser_file_location = r"C:/Users/mj.j/OneDrive - PBA Systems Pte. Ltd/GitHub/Github/2024_11_19_15_17_33/laser_row_data.csv"
#log_file = r"C:/Users/mj.j/OneDrive - PBA Systems Pte. Ltd/GitHub/Github/2024_11_19_15_17_33/log_file_combined.csv"

# self centerd with laser data - 2024_12_02_13_45_59
#varible_pitch_file_location = r"C:/Users/mj.j/OneDrive - PBA Systems Pte. Ltd/GitHub/Github/2024_12_02_13_45_59/variable pitch.csv"
#expantion_file_location = r"C:/Users/mj.j/OneDrive - PBA Systems Pte. Ltd/GitHub/Github/2024_12_02_13_45_596/Expansion_array_positive0.csv"
#laser_file_location = r"C:/Users/mj.j/OneDrive - PBA Systems Pte. Ltd/GitHub/Github/2024_12_02_13_45_59/laser_row_data.csv"
#log_file = r"C:/Users/mj.j/OneDrive - PBA Systems Pte. Ltd/GitHub/Github/2024_12_02_13_45_59/Log_file_1D_expansion_0.csv"
##not working#calculate_actual_dot_seperation(varible_pitch_file_location,expantion_file_location,laser_file_location,log_file)

# self centerd with laser data - 2024_12_02_13_45_59
#varible_pitch_file_location = r"C:/Users/mj.j/OneDrive - PBA Systems Pte. Ltd/GitHub/Github/2024_12_02_16_19_27_plot/variable_pitch.csv"
#expantion_file_location = r"C:/Users/mj.j/OneDrive - PBA Systems Pte. Ltd/GitHub/Github/2024_12_02_16_19_27_plot/Expansion_array_positive0.csv"
#laser_file_location = r"C:/Users/mj.j/OneDrive - PBA Systems Pte. Ltd/GitHub/Github/2024_12_02_16_19_27_plot/laser_row_data.csv"
#log_file_1d_error_mapping_test = r"C:/Users/mj.j/OneDrive - PBA Systems Pte. Ltd/GitHub/Github/2024_12_02_16_19_27_plot/Log_file_full.csv"
#calculate_actual_dot_seperation(varible_pitch_file_location,laser_file_location,log_file_1d_error_mapping_test)



