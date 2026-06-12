# /src/backend/services/plot_in_position_expantion.py

# this code block was deverloped to plot the thermal expantion and thermal expantion correction capability of the system
# Technoproble is the companty requested the solution for thermal expantion
# The code was developed by Malith Jayasinghe on 2024-11-27

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

import os


# Open file as 2D pandas and convert to numpy array : for log file
def open_file_pandas_convert_numpy(file_location):
    pandas_df = pd.read_csv(file_location)
    #print heder file 
    print(pandas_df.head())
    # Convert the DataFrame to a numpy array
    numpy_array = pandas_df.to_numpy()
    return numpy_array, numpy_array.shape[0]


def get_time(time):
    """
    Get the time column from the log file
    """
    time = datetime.strptime(time, "%Y-%m-%d-%H-%M-%S")
    time_lable = f"{time.hour}:{time.minute}"
    
    return time_lable

def get_ticks(array,size):
    """
    Get the ticks for the x-axis
    """
    ticks = []
    for i in range(0, size,15):
        ticks.append(array[i])
    return ticks

def get_time_ticks(array,size):
    """
    Get the time ticks for the x-axis
    """
    ticks = []
    for i in range(0, size,15):
        ticks.append(get_time(array[i]))
    return ticks
    
def calculate_one_pixel_size(numpy_array,actual_radius,radius_column):
    mean_radius_pix = np.mean(numpy_array[:,radius_column]) 
    print("Mean radius in pixle = ",mean_radius_pix)
    pixle_per_um = (actual_radius/mean_radius_pix)*1000
    print("pixel size in um = ",pixle_per_um)
    return pixle_per_um


def create_full_file_path(ref_file_location, file_name):
    file_path = os.path.dirname(ref_file_location)
    file_path_name = os.path.join(file_path,file_name)
    return file_path_name

def plot_in_position_stability(file_path):
    """
    Plot the stability of the system in position
    """
    log_file_np_array,number_of_rows = open_file_pandas_convert_numpy(file_path)

    # Get the position column
    pixle_per_um = calculate_one_pixel_size(log_file_np_array, 0.25, 13)
    position_x_start = (log_file_np_array[0, 12] - 1296)* pixle_per_um
    position_y_start = (log_file_np_array[0, 11] - 1024)* pixle_per_um

    position_x = (log_file_np_array[:, 12] - 1296)* pixle_per_um - position_x_start
    position_y = (log_file_np_array[:, 11] - 1024)* pixle_per_um - position_y_start
    # Get the time column
    image_index = log_file_np_array[:, 1]
    time = log_file_np_array[:, 0]
    
    image_tics = get_ticks(image_index,number_of_rows)
    time_tics = get_time_ticks(time,number_of_rows)

    temparature1 = log_file_np_array[:, 14]
    temparature2 = log_file_np_array[:, 15]
    temparature3 = log_file_np_array[:, 16]
    temparature4 = log_file_np_array[:, 17]

    X_axis_pe = log_file_np_array[:, 8]
    Y_axis_pe = log_file_np_array[:, 9]
    Z_axis_pe = log_file_np_array[:, 10]

    X_axis_fpos = log_file_np_array[:, 5] - log_file_np_array[0, 5]
    Y_axis_fpos = log_file_np_array[:, 6] - log_file_np_array[0, 6]
    Z_axis_fpos = log_file_np_array[:, 7]

    fig, axs = plt.subplots(5, 1, figsize=(20, 15))

    # Plot X axis position
    axs[0].plot(image_index, position_x, 'k', label='X axis position')
    axs[0].set_xlabel('Time')
    axs[0].set_ylabel('X axis position in μm')
    axs[0].set_title('X axis position estimation using camera')
    axs[0].set_xticks(image_tics)
    axs[0].set_xticklabels(time_tics, rotation=45)
    axs[0].grid(True)
    axs[0].legend()

    # Plot Y axis position
    axs[1].plot(image_index, position_y, 'r', label='Y axis position')
    axs[1].set_xlabel('Time')
    axs[1].set_ylabel('Y axis position in μm')
    axs[1].set_title('Y axis position estimation using camera')
    axs[1].set_xticks(image_tics)
    axs[1].set_xticklabels(time_tics, rotation=45)
    axs[1].legend()
    axs[1].grid(True)

    # temparature column 14,15,16,17
    axs[2].plot(image_index, temparature1, 'green', label='temparature sensor 1')
    axs[2].plot(image_index, temparature2, 'cyan', label='temparature sensor 2')
    axs[2].plot(image_index, temparature3, 'pink', label='temparature sensor 3')
    axs[2].plot(image_index, temparature4, 'gray', label='temparature sensor 4')
    axs[2].set_xlabel('Time')
    axs[2].set_ylabel('Temparature C')
    axs[2].set_title('Temparature sensor reading')
    axs[2].set_xticks(image_tics)
    axs[2].set_xticklabels(time_tics, rotation=45)
    axs[2].legend()
    axs[2].grid(True)

    # Position error column 5,6,7
    axs[3].plot(image_index, X_axis_pe, 'green', label='X axis position error')
    axs[3].plot(image_index, Y_axis_pe, 'cyan', label='Y axis position error')
    #axs[3].plot(image_index, Z_axis_pe, 'pink', label='Z axis position error')
    axs[3].set_xlabel('Time')
    axs[3].set_ylabel('Position error in mm')
    axs[3].set_title('Position error estimation using encoders')
    axs[3].set_xticks(image_tics)
    axs[3].set_xticklabels(time_tics, rotation=45)
    axs[3].legend()
    axs[3].grid(True)

    # feedback position colum
    axs[4].plot(image_index, X_axis_fpos, 'green', label='X axis position')
    axs[4].plot(image_index, Y_axis_fpos, 'cyan', label='Y axis position')
    axs[4].set_xlabel('Time')
    axs[4].set_ylabel('Position error in mm')
    axs[4].set_title('X and Y encoder position feedback')
    axs[4].set_xticks(image_tics)
    axs[4].set_xticklabels(time_tics, rotation=45)
    axs[4].legend()
    axs[4].grid(True)


    plt.tight_layout()
    full_path = create_full_file_path(file_path,"In_position_stability.png")
    plt.savefig(full_path, dpi=300)
    plt.show()



#file_path = f"C:/Users/mj.j/OneDrive - PBA Systems Pte. Ltd/GitHub/Github/2024_11_27_17_28_40/Log_file_in_position_stability_static.csv"
#file_path = f"C:/Users/mj.j/OneDrive - PBA Systems Pte. Ltd/GitHub/Github/2024_11_27_17_28_40/Log_file_in_position_stability_dynamic.csv"
#file_path = f"C:/Users/mj.j/OneDrive - PBA Systems Pte. Ltd/GitHub/Github/2024_11_28_16_34_52/Log_file_in_position_stability_dynamic.csv"

#file_path = f"C:/Users/mj.j/OneDrive - PBA Systems Pte. Ltd/GitHub/Github/2024_11_28_17_06_25/Log_file_in_position_stability_dynamic.csv"
#file_path = f"C:/Users/mj.j/OneDrive - PBA Systems Pte. Ltd/GitHub/Github/2024_11_29_08_36_20/Log_file_in_position_stability_dynamic.csv"

#file_path = r"C:\Users\mj.j\OneDrive - PBA Systems Pte. Ltd\GitHub\Github\2025_01_07_13_10_21\Log_file_in_position_stability_dynamic.csv"
#
#plot_in_position_stability(file_path)
#