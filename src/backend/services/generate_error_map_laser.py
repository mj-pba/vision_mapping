import numpy as np
import pandas as pd
import os
from backend.motor_control.acs_python_modules import error_mappting


def read_laser_row_data_file(laser_row_data_file_part):
    '''Read the laser row data file and return the data as a numpy array'''
    try:
        # Read the data from laser row data file
        print(f"Reading data from: {laser_row_data_file_part}")
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
    #print (mesured_value_columns)
    return mesured_value_columns



def get_mesured_values_mean(data, mesured_value_columns_list):
    '''Get the measured values mean from the data'''
    mesured_values = []
    for i in range(len(mesured_value_columns_list)):
        mesured_values.append(data[:, mesured_value_columns_list[i]])   
    mesured_values = np.array(mesured_values)
    #print(mesured_values[1,:])
    mean_values = mesured_values.mean(axis=0)
    return mean_values




def make_fist_value_zero(mean_values):
    '''Make the first value of the mean values zero'''
    mean_values_shifted = mean_values - mean_values[0]
    #print(mean_values_shifted)
    return mean_values_shifted

### create the full file path for new file
def create_full_file_path(ref_file_location, file_name):
    file_path = os.path.dirname(ref_file_location)
    file_path_name = os.path.join(file_path,file_name)
    return file_path_name
    


def create_buffer_file(error,folder_location,step):
    '''Print the error values to file text file'''

    # open file
    axis = 0
    zone = 0
    base = 0 
    #step = 9.9996
    with open(folder_location, "w") as file:
        file.write("! Error map location \n")
        file.write("local int axis\n")
        file.write("local int zone\n")
        file.write("local real base\n")
        file.write("local real step\n")
        file.write(f"axis = {axis}\n")
        file.write(f"zone = {zone}\n")
        file.write(f"base = {base}\n")
        file.write(f"step = {step}\n")
        for i in range(len(error)):
            file.write(f"CorrectionMap2({i}) = {round(error[i], 6)}\n")
        file.write("ERRORMAP1D axis, zone, base, step, CorrectionMap2 \n")
        file.write("ERRORMAPON axis, zone \n")
        file.write("stop")
    # close file
    file.close()


#def check_status_of_error_map(hc):
#    '''Send the error map to the ACS controller'''
#    # check status of error mapping
#    acs_error_mappting = error_mappting()
#    error_mapping_status = acs_error_mappting.get_current_error_map_status(hc)
#    print(error_mapping_status)
#    
#


def upload_error_map_to_ACS(hc, buffer_number, folder_location):
    acs_error_mappting = error_mappting()
    with open(folder_location, "r") as file:
        buffer_text = file.read()
        file.close()
    #acs_error_mappting.upload_buffer(hc, buffer_number, buffer_text)
    acs_error_mappting.load_buffer(hc, buffer_number, buffer_text)


# generate the error map buffer for the ACS controller
def create_error_map_buffer_from_laser_file_and_send_to_acs(laser_row_data_file_part, hc):
    data = read_laser_row_data_file(laser_row_data_file_part)
    if data is not None:
        runs = get_number_of_cycles(data.shape[1])
        steps = data.shape[0]
        print(f"Number of steps: {steps}, Number of runs: {runs}")
        mesured_value_columns_list = mesured_value_columns(runs)
        mean_values = get_mesured_values_mean(data, mesured_value_columns_list)
        mean_values_shifted = make_fist_value_zero(mean_values)
        #print(mean_values_shifted.shape)
        error = data[:,1] - mean_values_shifted
        step_distance = str(data[1,1])
        folder_location = create_full_file_path(laser_row_data_file_part,"acs_buffer_file.txt")
        create_buffer_file(error,folder_location,step_distance)
        upload_error_map_to_ACS(hc, 15, folder_location)



# Test the function
# Note centerd repetability test with laser 
#laser_row_data_file_part = r"C:\Users\mj.j\OneDrive - PBA Systems Pte. Ltd\GitHub\Github\2024_12_11_14_01_27\laser_row_file.csv"

#create_error_map_buffer_from_laser_file_and_send_to_acs(laser_row_data_file_part,1)
