import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
import csv

# folder_path = r"C:\Users\malit\Documents\GitHub\2025_07_18_14_55_15"
# files = os.listdir(folder_path)
# other_files = [f for f in files if not f.lower().endswith('.png')]
# print(other_files)
 

class thermal_expansion_demo_room_gantry:
    def __init__(self):
        self.start_time_previous = None
        self.end_time_previous = None
        pass

    def plot_temparature_vs_time(self, data):
        # Extract the temperature data from the DataFrame
        time = data[20:, 1]  # Assuming the second column is time
        temperatures = data[20:, 2:6] / 10
        
        plt.figure(figsize=(12, 6))
        
        # Plot each temperature sensor
        for i in range(temperatures.shape[1]):
            plt.plot(time, temperatures[:, i], label=f'Sensor {i+1}')

        # To avoid overcrowding the x-axis, we select a subset of ticks to display.
        # This will show approximately 15 time labels.``
        tick_spacing = max(1, len(time) // 15)
        plt.xticks(ticks=np.arange(0, len(time), tick_spacing), rotation=45, ha='right')

        plt.xlabel('Time (s)')
        plt.ylabel('Temperature (°C)')
        plt.title('Temperature vs Time')

        plt.legend()
        plt.grid()
        plt.savefig('Temperature_variation_in_R&D_room_2025_09_31.png', dpi=300, bbox_inches='tight')
        plt.show()


    # plot multiple positions vs time
    def plot_positions_vs_time_2(self,time_stamp, temparature_1,temparature_2, temparature_3, temparature_4, X_position_values,file_name):
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(20, 8), sharex=True)

        # Plot Temperature 4 on the first subplot
        ax1.plot(time_stamp, temparature_1, label='Temperature 1')
        ax1.plot(time_stamp, temparature_2, label='Temperature 2')
        ax1.plot(time_stamp, temparature_3, label='Temperature 3')
        ax1.plot(time_stamp, temparature_4, label='Temperature 4')
        ax1.set_title('Temperature vs. Time')
        ax1.set_ylabel('Temperature (°C)')
        ax1.legend()
        ax1.grid(True)

        # Plot Expansion Position on the second subplot
        ax2.plot(time_stamp, X_position_values[0], label='Expansion Position 1', color='r')
        ax2.plot(time_stamp, X_position_values[1], label='Expansion Position 2', color='g')
        ax2.plot(time_stamp, X_position_values[2], label='Expansion Position 3', color='b')
        ax2.plot(time_stamp, X_position_values[3], label='Expansion Position 4', color='c')
        ax2.plot(time_stamp, X_position_values[4], label='Expansion Position 5', color='m')
        ax2.plot(time_stamp, X_position_values[5], label='Expansion Position 6', color='y')
        ax2.plot(time_stamp, X_position_values[6], label='Expansion Position 7', color='k')
        ax2.plot(time_stamp, X_position_values[7], label='Expansion Position 8', color='orange')
        
        ax2.set_title('Expansion Position vs. Time')
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('Position (mm)')
        #ax2.set_ylim(-0.025,0.010 ) 
        ax2.legend()
        ax2.grid(True)

        # Rotate x-axis tick labels
        plt.xticks(rotation=45)

        # Adjust layout to prevent labels from overlapping
        plt.tight_layout()
        plt.savefig(file_name, dpi=300, bbox_inches='tight')
        plt.show()




    def plot_positions_vs_time(self,time_stamp, temparature_1,temparature_2, temparature_3, temparature_4, single_expansion_position,file_name):
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(20, 8), sharex=True)

        # Plot Temperature 4 on the first subplot
        ax1.plot(time_stamp, temparature_1, label='Temperature 1')
        ax1.plot(time_stamp, temparature_2, label='Temperature 2')
        ax1.plot(time_stamp, temparature_3, label='Temperature 3')
        ax1.plot(time_stamp, temparature_4, label='Temperature 4')
        ax1.set_title('Temperature vs. Time')
        ax1.set_ylabel('Temperature (°C)')
        ax1.legend()
        ax1.grid(True)

        # Plot Expansion Position on the second subplot
        ax2.plot(time_stamp, single_expansion_position, label='Expansion Position', color='r')
        ax2.set_title('Expansion Position vs. Time')
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('Position (mm)')
        ax2.legend()
        ax2.grid(True)

        # Rotate x-axis tick labels
        plt.xticks(rotation=45)

        # Adjust layout to prevent labels from overlapping
        plt.tight_layout()
        plt.savefig(file_name, dpi=300, bbox_inches='tight')
        plt.show()



    def plot_location_expantion_vs_time(self, folder_path, expantion_array):
        # thermal_expansion_demo_room_gantry().plot_temparature_vs_time(data_np)

        all_expantion_positions = []

        for x in range (len(expantion_array)):
            file_path = os.path.join(folder_path, expantion_array[x])
            # print(file_path)

            no_of_axis = 3
            calculated_array_2d = np.loadtxt(file_path, delimiter=',')
            rows_in_file,column = calculated_array_2d.shape
            calculated_calibration_data_table_row = rows_in_file//no_of_axis
            calibration_data_table_column = column
            calculated_position_np_array = calculated_array_2d.reshape(no_of_axis,calculated_calibration_data_table_row,calibration_data_table_column)
            all_expantion_positions.append(calculated_position_np_array)
            # X axis 
            # print(calculated_position_np_array[0][:][0])


        time_stamp = []
        temparature_1 = []
        temparature_2 = []
        temparature_3 = []
        temparature_4 = []
        single_expansion_position = []
        
        for x in range (len(expantion_array)):
            time_stamp.append(data[(81*x),0])  # Print the first column of the first axis
            temparature_1.append(data[(81*x),14])
            temparature_2.append(data[(81*x),15])
            temparature_3.append(data[(81*x),16])
            temparature_4.append(data[(81*x),17])


        self.axis = 0   # 0 for X, 1 for Y, 2 for Z
        self.row = 1    # 
        self.column = 2 # 

        for row in range (0,9,1):
            self.row = row
            X_position_values = []
            for X_position in range (1,9,1):
                print("Number of expansion positions: Test")
                single_expansion_position = []
                single_expansion_position_all = []
                for x in range (len(expantion_array)):
                    calculated_position_np_array = all_expantion_positions[x]   
                                                                            #    [axis]      []        [row] 
                    single_expansion_position.append(calculated_position_np_array[self.axis, self.row, X_position])  # Print the second column of the first axis
                    single_expansion_position_all.append(calculated_position_np_array[self.axis, self.row, X_position] - calculated_position_np_array[self.axis, 0, X_position])  # Print the second column of the first axis
                    self.file_name = f"Expantion_at_index_position_relative({X_position},{self.row}).png"

                # self.plot_positions_vs_time_2(file_name)
                X_position_values.append(single_expansion_position_all)
                #self.plot_positions_vs_time(time_stamp, temparature_1,temparature_2, temparature_3, temparature_4, single_expansion_position_all, self.file_name)

            self.file_name = f"test_multiple_expansion_positions_{self.axis},{self.row}.png"
            self.plot_positions_vs_time_2(time_stamp, temparature_1,temparature_2, temparature_3, temparature_4, X_position_values,self.file_name)

# ===================================================
# main function to run the demo
# ===================================================

calculated_locations = r"C:\Users\mj.j\Documents\2D_optical_vision_mapping\temperature_logs\temperature_log_20250930_1.csv"
data = pd.read_csv(calculated_locations, skiprows=1).to_numpy()
print(data.shape)

# thermal_expansion_demo_room_gantry().plot_temparature_vs_time(data) #, folder_path_2,folder_path_3, folder_path_4, folder_path_5])

# expantion_array = ['Expansion_array_2D_0.csv', 'Expansion_array_2D_1.csv', 'Expansion_array_2D_10.csv', 'Expansion_array_2D_11.csv', 'Expansion_array_2D_12.csv', 'Expansion_array_2D_13.csv', 'Expansion_array_2D_14.csv', 'Expansion_array_2D_15.csv', 'Expansion_array_2D_16.csv', 'Expansion_array_2D_17.csv', 'Expansion_array_2D_18.csv', 'Expansion_array_2D_19.csv', 'Expansion_array_2D_2.csv', 'Expansion_array_2D_3.csv', 'Expansion_array_2D_4.csv', 'Expansion_array_2D_5.csv', 'Expansion_array_2D_6.csv', 'Expansion_array_2D_7.csv', 'Expansion_array_2D_8.csv', 'Expansion_array_2D_9.csv']
# expantion_array = ['Expansion_array_2D_0.csv', 'Expansion_array_2D_1.csv', 'Expansion_array_2D_10.csv', 'Expansion_array_2D_11.csv', 'Expansion_array_2D_12.csv', 'Expansion_array_2D_13.csv', 'Expansion_array_2D_14.csv', 'Expansion_array_2D_15.csv', 'Expansion_array_2D_16.csv', 'Expansion_array_2D_17.csv', 'Expansion_array_2D_18.csv', 'Expansion_array_2D_19.csv', 'Expansion_array_2D_2.csv', 'Expansion_array_2D_20.csv', 'Expansion_array_2D_21.csv', 'Expansion_array_2D_22.csv', 'Expansion_array_2D_23.csv', 'Expansion_array_2D_24.csv', 'Expansion_array_2D_25.csv', 'Expansion_array_2D_26.csv', 'Expansion_array_2D_27.csv', 'Expansion_array_2D_28.csv', 'Expansion_array_2D_29.csv', 'Expansion_array_2D_3.csv', 'Expansion_array_2D_30.csv', 'Expansion_array_2D_31.csv', 'Expansion_array_2D_32.csv', 'Expansion_array_2D_33.csv', 'Expansion_array_2D_34.csv', 'Expansion_array_2D_35.csv', 'Expansion_array_2D_36.csv', 'Expansion_array_2D_37.csv', 'Expansion_array_2D_38.csv', 'Expansion_array_2D_39.csv', 'Expansion_array_2D_4.csv', 'Expansion_array_2D_40.csv', 'Expansion_array_2D_41.csv', 'Expansion_array_2D_42.csv', 'Expansion_array_2D_43.csv', 'Expansion_array_2D_44.csv', 'Expansion_array_2D_45.csv', 'Expansion_array_2D_46.csv', 'Expansion_array_2D_47.csv', 'Expansion_array_2D_48.csv', 'Expansion_array_2D_49.csv', 'Expansion_array_2D_5.csv', 'Expansion_array_2D_50.csv', 'Expansion_array_2D_51.csv', 'Expansion_array_2D_52.csv', 'Expansion_array_2D_53.csv', 'Expansion_array_2D_54.csv', 'Expansion_array_2D_55.csv', 'Expansion_array_2D_56.csv', 'Expansion_array_2D_57.csv', 'Expansion_array_2D_58.csv', 'Expansion_array_2D_59.csv', 'Expansion_array_2D_6.csv', 'Expansion_array_2D_7.csv', 'Expansion_array_2D_8.csv', 'Expansion_array_2D_9.csv']
# expantion_array = ['Expansion_array_2D_0.csv', 'Expansion_array_2D_1.csv', 'Expansion_array_2D_10.csv', 'Expansion_array_2D_11.csv', 'Expansion_array_2D_12.csv', 'Expansion_array_2D_13.csv', 'Expansion_array_2D_14.csv', 'Expansion_array_2D_15.csv', 'Expansion_array_2D_16.csv', 'Expansion_array_2D_17.csv', 'Expansion_array_2D_18.csv', 'Expansion_array_2D_19.csv', 'Expansion_array_2D_2.csv', 'Expansion_array_2D_20.csv', 'Expansion_array_2D_21.csv', 'Expansion_array_2D_22.csv', 'Expansion_array_2D_23.csv', 'Expansion_array_2D_24.csv', 'Expansion_array_2D_25.csv', 'Expansion_array_2D_26.csv', 'Expansion_array_2D_27.csv', 'Expansion_array_2D_28.csv', 'Expansion_array_2D_29.csv', 'Expansion_array_2D_3.csv', 'Expansion_array_2D_30.csv', 'Expansion_array_2D_31.csv', 'Expansion_array_2D_32.csv', 'Expansion_array_2D_33.csv', 'Expansion_array_2D_34.csv', 'Expansion_array_2D_35.csv', 'Expansion_array_2D_36.csv', 'Expansion_array_2D_37.csv', 'Expansion_array_2D_38.csv', 'Expansion_array_2D_39.csv', 'Expansion_array_2D_4.csv', 'Expansion_array_2D_40.csv', 'Expansion_array_2D_41.csv', 'Expansion_array_2D_42.csv', 'Expansion_array_2D_43.csv', 'Expansion_array_2D_44.csv', 'Expansion_array_2D_45.csv', 'Expansion_array_2D_46.csv', 'Expansion_array_2D_47.csv', 'Expansion_array_2D_48.csv', 'Expansion_array_2D_49.csv', 'Expansion_array_2D_5.csv', 'Expansion_array_2D_6.csv', 'Expansion_array_2D_7.csv', 'Expansion_array_2D_8.csv', 'Expansion_array_2D_9.csv']

# Sort the list based on the number in the filename
# expantion_array.sort(key=lambda f: int(f.split('_')[-1].split('.')[0]))


# folder_path = r"C:\Users\malit\Documents\GitHub\2025_07_24_10_12_09"


thermal_expansion_demo_room_gantry().plot_temparature_vs_time(data)

