import numpy as np
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt
#from backend.motor_control.acs_python_modules import error_mappting

#from backend.motor_control.acs_python_modules import error_mappting

# create vision test mesument row data file
# step 1: created array  - done
# step 2: claculate step sizes - done
# step 3: calculate distance and error values - done
# step 4: save file - done
# step 5: plot the data  - not done !!!
# step 6: create buffer file from vision data - not done !!!
# step 7: upload buffer file to ACS controller - not done !!!

# Open file as 3D numpy array : for location file
def open_3D_location_file(file_location,number_of_axis):
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
    return numpy_array, numpy_array.shape



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




def calculate_one_pixel_size(numpy_array,actual_radius,radius_column):
    mean_radius_pix = np.mean(numpy_array[:,radius_column]) 
    print("Mean radius in pixle = ",mean_radius_pix)
    pixle_per_um = (actual_radius/mean_radius_pix)*1000
    print("pixel size in um = ",pixle_per_um)
    return pixle_per_um



def check_row_ctf_and_log_file(numpy_array, certificate_data_row):
    mesure_row = 0
    numpy_array_shape = numpy_array.shape
    axis = 0
    axis = 1
    if axis == 0:    
        for i in range (0,numpy_array_shape[0],1):
            # check certificate data row equace to certificate_data_row
            mesure_row = 0
            if numpy_array[i][3] != certificate_data_row:
                mesure_row += 1
                print("Mesurment error:",mesure_row, i,numpy_array[i][3])

        if mesure_row == 0:
            print("certificate_data_row equace to log file data row")
            value= 1
        else:
            print("Two rows in log file")
            value = 0
    elif axis == 1:
        for i in range (0,numpy_array_shape[0],1):
            # check certificate data row equace to certificate_data_row
            mesure_row = 0
            if numpy_array[i][4] != certificate_data_row:
                mesure_row += 1
                print("Mesurment error:",mesure_row, i,numpy_array[i][4])

        if mesure_row == 0:
            print("certificate_data_row equace to log file data row")
            value= 1
        else:
            print("Two rows in log file")
            value = 0

    return value


def calculate_step_size_and_add_to_array(step_size,steps_count,row_data):
    '''Calculate the step size and add to the array'''
    print(row_data.shape)
    for i in range(0,steps_count-1,1):
        row_data[i][0] = int(i+1)
        row_data[i][1] = step_size*(i)    
    return row_data






def calculate_error_map(certificate_date, numpy_array,pixle_size_in_um,runs,row_data, axis):
    '''Calculate the error map'''
    steps_count = certificate_date.shape[0]-1
    if axis == 0:
        for j in range(0,runs+1,1):
            for i in range(1+32*j,steps_count+32*j,1):
                error_value = ((numpy_array[i][12]-1296)*pixle_size_in_um)
                index = numpy_array[i][4]
                row_data[index-1][2+4*j] = certificate_date[index] + error_value/1000   # actual distance
                #row_data[index-1][3+4*j] = row_data[index-1][2] - row_data[index-1][1]
                row_data[index-1][3+4*j] =  row_data[index-1][1] - row_data[index-1][2+4*j] # step error
                #print("sample:",i,"run",j,", index: ",index, ", image error:",error_value,", index:",row_data[index-1][0], ", distance: ",row_data[index-1][1], ", actual distance:",row_data[index-1][2+4*j], ", step error:",row_data[index-1][3+4*j])

            for i in range(17+32*j,steps_count*2 + 32*j,1):
                error_value = ((numpy_array[i][12]-1296)*pixle_size_in_um)
                index = numpy_array[i][4]
                row_data[index-1][4+4*j] = certificate_date[index] + error_value/1000
                #row_data[index-1][5+4*j] = row_data[index-1][2] - row_data[index-1][1]
                row_data[index-1][5+4*j] =  row_data[index-1][1] - row_data[index-1][4+4*j]
                #print("sample:",i,"run",j,", index: ",index, ", image error:",error_value,", index:",row_data[index-1][0], ", distance: ",row_data[index-1][1], ", actual distance:",row_data[index-1][4+4*j], ", step error:",row_data[index-1][5+4*j])
    elif axis == 1:
        for j in range(0,runs+1,1):
            for i in range(1+32*j,steps_count+32*j,1):
                error_value = ((numpy_array[i][11]-1024)*pixle_size_in_um)
                index = numpy_array[i][3]
                row_data[index-1][2+4*j] = certificate_date[index] + error_value/1000   # actual distance
                #row_data[index-1][3+4*j] = row_data[index-1][2] - row_data[index-1][1]
                row_data[index-1][3+4*j] =  row_data[index-1][1] - row_data[index-1][2+4*j] # step error
                print("sample:",i,"run",j,", index: ",index, ", image error:",error_value,", index:",row_data[index-1][0], ", distance: ",row_data[index-1][1], ", actual distance:",row_data[index-1][2+4*j], ", step error:",row_data[index-1][3+4*j])

            for i in range(17+32*j,steps_count*2 + 32*j,1):
                error_value = ((numpy_array[i][11]-1024)*pixle_size_in_um)
                index = numpy_array[i][3]
                row_data[index-1][4+4*j] = certificate_date[index] + error_value/1000
                #row_data[index-1][5+4*j] = row_data[index-1][2] - row_data[index-1][1]
                row_data[index-1][5+4*j] =  row_data[index-1][1] - row_data[index-1][4+4*j]
                print("sample:",i,"run",j,", index: ",index, ", image error:",error_value,", index:",row_data[index-1][0], ", distance: ",row_data[index-1][1], ", actual distance:",row_data[index-1][4+4*j], ", step error:",row_data[index-1][5+4*j])


    return row_data


### create the full file path for new file
def create_full_file_path(ref_file_location, file_name):
    file_path = os.path.dirname(ref_file_location)
    file_path_name = os.path.join(file_path,file_name)
    return file_path_name


def plot_vision_row_values(row_date_filled,numpy_array,runs,pixle_size_in_um):
    '''Plot the error values'''
    for j in range (0,5,1):
        x_position = row_date_filled[:, 1]
        error_x = -1*row_date_filled[:, 3+j*2]
        plt.plot(x_position, error_x, marker='o')
        x_position = row_date_filled[:, 1]
        error_x = -1*row_date_filled[:, 5+j*2]
        plt.plot(x_position, error_x, marker='o')
    
    plt.xlabel('X Position')
    plt.ylabel('pix_R')
    plt.title('Column 13 (pix_R) vs Column 5 (X Position)')
    plt.grid(True)
    plt.show()



#def plot_vision_row_values(row_date_filled,numpy_array,runs,pixle_size_in_um):
#    '''Plot the error values'''    
#    x_position = numpy_array[:, 5]
#    error_x = (numpy_array[:, 12]-1296)*pixle_size_in_um
#    # Plot the data
#    plt.plot(x_position, error_x, marker='o')
#    plt.xlabel('X Position')
#    plt.ylabel('pix_R')
#    plt.title('Column 13 (pix_R) vs Column 5 (X Position)')
#    plt.grid(True)
#    plt.show()



def get_mesured_values_mean(row_date_filled):
    '''Get the mean values of the mesured values'''
    #print(row_date_filled.shape[0],row_date_filled.shape[1])
    mean_values_array = np.zeros((row_date_filled.shape[0]))
    for i in range(0,row_date_filled.shape[0],1):
        #i = 1
        values = row_date_filled[i][2:]
        selected_values = [values[j] for j in [1,3,5,7,9,11,13,15,17,19]]
        sorted_values = np.sort(selected_values)
        #print(sorted_values)
        meadian_value = np.median(sorted_values)
        first_quartile = np.percentile(sorted_values, 25)
        third_quartile = np.percentile(sorted_values, 75)
        IQR = third_quartile - first_quartile
        lower_outlier = first_quartile - 1.5*IQR
        upper_outlier = third_quartile + 1.5*IQR
        # Filter values to remove outliers
        filtered_values = [x for x in sorted_values if lower_outlier <= x <= upper_outlier]
        # Calculate the mean of the filtered values
        mean_value_after_outliers = np.mean(filtered_values)
        mean_values_array[i] = mean_value_after_outliers
        #print(row_date_filled[i][1],meadian_value,mean_value_after_outliers)

    return mean_values_array

def plot_vision_mean_values(mean_values_array):
    '''Plot the mean values of the mesured values'''
    # Plot the data

    plt.plot(mean_values_array*-1, marker='o')
    plt.xlabel('X Position')
    plt.ylabel('Mean Error Value (μm)')
    plt.title('Vision Based Shifted Mean Error Value vs X Position')
    plt.grid(True)
    plt.show()


def make_fist_value_zero(mean_values):
    '''Make the first value of the mean values zero'''
    mean_values_shifted = mean_values - mean_values[0]
    #print("mean_values_shifted",mean_values_shifted)
    return mean_values_shifted




def create_buffer_file(error,folder_location,step,axis):
    '''Print the error values to file text file'''

    # open file
    zone = 0
    base = 0 
    with open(folder_location, "w") as file:
        file.write("! 1D Error map from vision date\n")
        file.write("! Date: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "\n")
        file.write("! #ERRORMAPREP, ERRORMAPOFF axis,zone \n")
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



#def upload_error_map_to_ACS(hc, buffer_number, folder_location):
#    acs_error_mappting = error_mappting()
#    with open(folder_location, "r") as file:
#        buffer_text = file.read()
#        file.close()
#    #acs_error_mappting.upload_buffer(hc, buffer_number, buffer_text)
#    acs_error_mappting.load_buffer(hc, buffer_number, buffer_text)
#
def create_error_map_buffer_from_glass_certificate_and_vision_files_and_send_to_acs(glass_certificate,file_parth_log_file_1D_error_map, hc):
    number_of_axis = 3
    # open glass certificate file
    data = open_3D_location_file(glass_certificate,number_of_axis)
    
    if data is not None:

        numpy_array, numpy_array_shape = open_file_pandas_convert_numpy(file_parth_log_file_1D_error_map)
        axis, test_end_target_index, test_row_column, test_runs = get_axis_serch_column_end_index_runs(numpy_array)

        certificate_date = data[axis][:][test_row_column]
        #print("max value index:",np.argmax(certificate_date)-1)
        step_size = np.max(certificate_date)/(np.argmax(certificate_date)-1)
        print("step size:",step_size)

        actual_radius = 0.25 #mm
        radius_column = 13
        pixle_size_in_um = calculate_one_pixel_size(numpy_array,actual_radius,radius_column)
        # get number of cycles

        value = check_row_ctf_and_log_file(numpy_array, test_row_column)

        if value == 1:
            # create row data array
            steps_count = certificate_date.shape[0]-1
            row_data = np.zeros((steps_count-1, 4*test_runs+6))

            # fill first two columns
            row_data = calculate_step_size_and_add_to_array(step_size,steps_count,row_data)
            
            # calculate mesured values and errors using step size and certificate data
            row_date_filled = calculate_error_map(certificate_date, numpy_array,pixle_size_in_um,test_runs-1,row_data,axis)
            
            # save file
            full_file_path = create_full_file_path(file_parth_log_file_1D_error_map,"vision_error_row_data.csv")
            #save vision based mesurment row data file
            np.savetxt(full_file_path, row_date_filled, delimiter=',', fmt='%.6f')

            # plot the error values
            plot_vision_row_values(row_date_filled,numpy_array,test_runs,pixle_size_in_um)
            
            # get mean values from each row
            mean_values_array = get_mesured_values_mean(row_date_filled)

            # shift the mean values to make the first value zero
            mean_values_array_shifted = make_fist_value_zero(mean_values_array)
            #plot_vision_mean_values(mean_values_array_shifted)
            plot_vision_mean_values(mean_values_array)

            # create buffer file
            buffer_file_folder_location = create_full_file_path(full_file_path,"acs_buffer_file.txt")
            print("buffer file folder location:", buffer_file_folder_location)
            #mean_step_distance = get_step_distance(numpy_array,axis)

            create_buffer_file(mean_values_array_shifted,buffer_file_folder_location,step_size,axis)
            #create_buffer_file(mean_values_array_shifted,buffer_file_folder_location,mean_step_distance,axis)
            #upload_error_map_to_ACS(hc, 15, buffer_file_folder_location)
        
        else: 
            print("glass certificate column and log file column is not equal")




# Test the function
# create error map with glass certificate and 1D error map test date

#glass_certificate = r"C:\Users\mj.j\OneDrive - PBA Systems Pte. Ltd\GitHub\Github\2024_12_02_16_19_27_plot\glass_certificate.csv"
#log_file_1D_error_map_test = r"C:\Users\mj.j\OneDrive - PBA Systems Pte. Ltd\GitHub\Github\2024_12_11_09_34_52\Log_file_1D.csv"
#create_error_map_buffer_from_glass_certificate_and_vision_files_and_send_to_acs(glass_certificate,log_file_1D_error_map_test,1)

#glass_certificate = r"C:\Users\mj.j\OneDrive - PBA Systems Pte. Ltd\GitHub\Github\2025_01_14_11_21_37_GC\glass_certificate.csv"
#log_file_1D_error_map_test = r"C:\Users\mj.j\OneDrive - PBA Systems Pte. Ltd\GitHub\Github\2025_01_14_15_19_51\Log_file_1D.csv"
#create_error_map_buffer_from_glass_certificate_and_vision_files_and_send_to_acs(glass_certificate,log_file_1D_error_map_test,1)

#glass_certificate = r"C:\Users\mj.j\OneDrive - PBA Systems Pte. Ltd\GitHub\Github\2025_02_21_10_01_34\glass_certificate.csv"
#log_file_1D_error_map_test = r"C:\Users\mj.j\OneDrive - PBA Systems Pte. Ltd\GitHub\Github\2025_02_21_10_52_52\Log_file_1D.csv"
#axis = 1
#hc = 1
#create_error_map_buffer_from_glass_certificate_and_vision_files_and_send_to_acs(glass_certificate,log_file_1D_error_map_test,hc)
