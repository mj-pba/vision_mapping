# we have to create multiple documents from existing documents to create a test 
import pandas as pd
import numpy as np
import os
import sys

def remove_columns_and_rows(array):
    #remove columns and rows 
    x_error_map_2D_new = np.delete(array,2, axis=1)
    array_shape_1 = int(array.shape[1]/2)+1
    array_shape_0 = int(array.shape[0]/2)+1

    for i in range(3,array_shape_1,1):
        x_error_map_2D_new = np.delete(x_error_map_2D_new,i, axis=1)

    for j in range(2,array_shape_0,1):
        x_error_map_2D_new = np.delete(x_error_map_2D_new,j, axis=0)
    
    return x_error_map_2D_new




def remve_columns_and_rows_encoder_dot_locations(test_distance_matrix,stop_condition_i,stop_condition_j):
    #remove columns and rows
    print("array shape: ", test_distance_matrix.shape)
    # test_distance_matrix = np.delete(test_distance_matrix, 1, axis=2)  # Remove columns along axis 2
    for i in range(1,stop_condition_i,1):
        test_distance_matrix = np.delete(test_distance_matrix,i, axis=1)

    for j in range(1,stop_condition_j,1):
        test_distance_matrix = np.delete(test_distance_matrix,j, axis=2)

    return test_distance_matrix


def create_full_file_path(ref_file_location, file_name):
    file_path = os.path.dirname(ref_file_location)
    file_path_name = os.path.join(file_path,file_name)
    return file_path_name


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
    numpy_array = pandas_df.to_numpy()
    return numpy_array, numpy_array.shape


def generate_non_calibrated_camera_test(error_map_axis_0_file_path, error_map_axis_1_file_path, after_centering_dot_location_file_path, glass_certificate_file_path, vision_rotation_matrix,vision_log_file_file_path):

    # =========================================
    # Create 2D error map values send to ACS
    # =========================================
    np.set_printoptions(suppress=True, precision=6)

    # Read the error using numpy there is no header in the file;
    x_error_map_2D = np.genfromtxt(error_map_axis_0_file_path, delimiter=';')
    y_error_map_2D = np.genfromtxt(error_map_axis_1_file_path, delimiter=';')

    # Remove addesent columns and rows from the error map to create 2mm pitch matrix
    x_error_map_2D_new = remove_columns_and_rows(x_error_map_2D)
    y_error_map_2D_new = remove_columns_and_rows(y_error_map_2D)
    
    # save the x_error_map_2D_new and y_error_map_2D_new to csv files
    full_path_x_errormap = create_full_file_path(error_map_axis_0_file_path,"x_error_map_2D_for_test.csv")
    full_path_y_errormap = create_full_file_path(error_map_axis_0_file_path,"y_error_map_2D_for_test.csv")
    np.savetxt(full_path_x_errormap, x_error_map_2D_new, delimiter=';', fmt='%.6f')  
    np.savetxt(full_path_y_errormap, y_error_map_2D_new, delimiter=';', fmt='%.6f')  


    # =============================================================================
    # Scan dots location values using glass certificate and encoder start location
    # =============================================================================

    print("=========================")
    print("Scan dots location values using glass certificate")
    print("=========================")
    # Read loation file after centering dot location
    number_of_axis = 3
    original_encoder_location_array = open_3D_location_file(after_centering_dot_location_file_path,number_of_axis)
    print("original_location_array shape: ", original_encoder_location_array.shape)
    scan_start_location_array = original_encoder_location_array[:,1,1]
    print("Scan start location :", scan_start_location_array)

    # Read glass certificate file
    glass_certificate_array = open_3D_location_file(glass_certificate_file_path,number_of_axis)
    print("glass_certificate_array shape: ", glass_certificate_array.shape)

    # Read glass certificate file wit relative distance 
    vision_rotation_matrix = open_3D_location_file(vision_rotation_matrix,number_of_axis)
    print("vision_rotation_matrix shape: ", vision_rotation_matrix.shape)

    numpy_array, numpy_array_shape = open_file_pandas_convert_numpy(vision_log_file_file_path)
    #print(f"vision log file shape: {numpy_array_shape}")
    #print(f"rows max value :    {np.max(numpy_array[:,4])}")
    #print(f"columns max value : {np.max(numpy_array[:,3])}")
    stop_condition_i = np.max(numpy_array[:,4])    # 15
    stop_condition_j = np.max(numpy_array[:,3])    # 15

#    for i in range(1,vision_cumilative_distance_matrix.shape[0],1):
#        for j in range(1,vision_cumilative_distance_matrix.shape[0],1):
    
    # zero matrix 
    test_distance_matrix_shape = glass_certificate_array.shape
    test_distance_matrix = np.zeros(test_distance_matrix_shape)
    print("test_distance_matrix shape: ", test_distance_matrix.shape)

    for j in range(1,stop_condition_j,1):
        print('================',j)
        for i in range(1,stop_condition_i,1):
            test_distance_matrix[0,j,i] = scan_start_location_array[0] + vision_rotation_matrix[0,j,i] - vision_rotation_matrix[0,1,1]
            test_distance_matrix[1,j,i] = scan_start_location_array[1] + vision_rotation_matrix[1,j,i] - vision_rotation_matrix[1,1,1]
            test_distance_matrix[2,j,i] = original_encoder_location_array[2,j,i]
            print(test_distance_matrix[0,j,i],test_distance_matrix[1,j,i])

    # remove first row and first column
    test_distance_matrix = test_distance_matrix[:,1:,1:]
    
    test_distance_matrix = remve_columns_and_rows_encoder_dot_locations(test_distance_matrix,stop_condition_i,stop_condition_j)
    


    # remove the first row and first column


    # save the test_distance_matrix to csv file
    full_path_test_distance_matrix = create_full_file_path(error_map_axis_0_file_path,"test_distance_matrix.csv")
    array_2d = test_distance_matrix.reshape(-1, test_distance_matrix.shape[-1])     # convert to 2D
    np.savetxt(full_path_test_distance_matrix, array_2d, delimiter=',', fmt='%.6f') # save to csv file




# =========================
# main test function call
# =========================

#after_centering_dot_location_file_path =    r"C:\Users\mj.j\OneDrive - PBA Systems Pte. Ltd\GitHub\Github\2025_04_21_11_27_35\Expansion_array_2D_0.csv"

# after_centering_dot_location_file_path =    r"C:\Users\malit\Documents\GitHub\2025_07_31_08_56_23\Expansion_array_2D_0.csv"


# folder_path = os.path.dirname(after_centering_dot_location_file_path)
# print("folder_path:",folder_path)
# error_map_axis_0_file_path = os.path.join(folder_path,"x_error_map_2D.csv")
# error_map_axis_1_file_path = os.path.join(folder_path,"y_error_map_2D.csv")
# glass_certificate_file_path = os.path.join(folder_path,"glass_certificate_2D_relative.csv")
# vision_rotation_matrix = os.path.join(folder_path,"vision_rotation_matrix.csv")
# vision_log_file_file_path = os.path.join(folder_path,"Log_file_2D_expansion_X_axis.csv")

# # check if the files are available
# if not os.path.exists(error_map_axis_0_file_path):
#     print("location_matrix_file_path not found")
#     sys.exit(1)
# if not os.path.exists(error_map_axis_1_file_path):
#     print("glass_certificate_matrix_file_path not found")
#     sys.exit(1)
# if not os.path.exists(glass_certificate_file_path):
#     print("dot_center_encoder_location_matrix_file_path not found")
#     sys.exit(1)
# if not os.path.exists(vision_rotation_matrix):
#     print("vision_cumilative_distance_matrix not found")
#     sys.exit(1)
# if not os.path.exists(vision_log_file_file_path):
#     print("vision_log_file_path not found")
#     sys.exit(1)


# generate_non_calibrated_camera_test(error_map_axis_0_file_path, error_map_axis_1_file_path, after_centering_dot_location_file_path, glass_certificate_file_path,vision_rotation_matrix,vision_log_file_file_path)
