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

# 
class temperature_plotter():
    def __init__(self):
        self.start_time_previous = None
        self.end_time_previous = None
        pass

    def plot_temperature_vs_time(self, data, fig_name, fig_title):
        # Extract the temperature data from the DataFrame
        time = data[:, 1]  # Assuming the first column is time
        plt.figure(figsize=(15, 8))
        #plt.plot(time, temperature, label='Temperature over Time')
        plt.plot(time, data[:, 2], label='Temperature sensor 0')
        plt.plot(time, data[:, 3], label='Temperature sensor 1')
        plt.plot(time, data[:, 4], label='Temperature sensor 2')
        plt.plot(time, data[:, 5], label='Temperature sensor 3')
        plt.xlabel('Time (hh:mm:ss)')
        plt.ylabel('Temperature (°C)')
        plt.ylim([18, 28])  # Set y-axis limits
        plt.title(fig_title)
        plt.legend()

        # Show only every 30th tick
        ax = plt.gca()
        ticks = ax.get_xticks()
        ax.set_xticks(ticks[::30])  # Show every 30th tick

        # Rotate x-axis tick labels
        plt.xticks(rotation=75)
        plt.grid()
        # Adjust layout to prevent labels from overlapping
        plt.tight_layout()

        plt.savefig(fig_name, dpi=100, bbox_inches='tight')
        plt.show()


    def plot_positions_vs_time(self):
        folder_path = r"C:\Users\mj.j\Documents\temparature_log_R&D_room"
        # List of dates for your log files
        dates = ["20250819","20250821","20250822","20250823","20250824"]

        fig, axs = plt.subplots(len(dates), 1, figsize=(30,  6 * len(dates)), sharex=False)


        # Loop through each date and process the corresponding log file
        for i, date in enumerate(dates):
            file_path = os.path.join(folder_path, f"temperature_log_{date}.csv")
            if not os.path.exists(file_path):
                print(f"File not found: {file_path}")
                continue
            data = pd.read_csv(file_path, skiprows=1).to_numpy()
            time = data[:, 1]
            axs[i].plot(time, data[:, 2]/10, label='Sensor 0')
            axs[i].plot(time, data[:, 3]/10, label='Sensor 1')
            axs[i].plot(time, data[:, 4]/10, label='Sensor 2')
            axs[i].plot(time, data[:, 5]/10, label='Sensor 3')
            axs[i].set_ylabel('Temp (°C)')
            axs[i].set_title(f'Temperature {date[:4]}.{date[4:6]}.{date[6:]}')
            axs[i].set_xticks(time[::30])  # Show every 30th tick
            axs[i].legend()
            axs[i].set_ylim([18, 28])  # Set y-axis limits
            axs[i].grid(True)
            axs[i].tick_params(axis='x', rotation=75)

        plt.xlabel('Time (hh:mm:ss)')
        plt.tight_layout()
        plt.savefig(os.path.join(folder_path, "all_temperatures.png"), dpi=100, bbox_inches='tight')
        plt.show()



# ===================================================
# main function to run the demo
# ===================================================

calculated_locations = r"C:\Users\mj.j\Documents\temparature_log_demo_room\temperature_log_20250831.csv"
data = pd.read_csv(calculated_locations, skiprows=1).to_numpy()
print(data.shape)
print(f"Data type: {data.dtype}")
print("First 3 rows:")
print(data[:3])

# Create file_name by replacing .csv with .png
fig_name = os.path.splitext(calculated_locations)[0] + ".png"

fig_title = 'L1 Dimo room 2025.08.31 Temperature vs Time'

# plot single day
temperature_plotter().plot_temperature_vs_time(data, fig_name, fig_title) #, folder_path_2,folder_path_3, folder_path_4, folder_path_5])

# plot multiple days 
# temperature_plotter().plot_positions_vs_time()


# expantion_array = ['Expansion_array_2D_0.csv', 'Expansion_array_2D_1.csv', 'Expansion_array_2D_10.csv', 'Expansion_array_2D_11.csv', 'Expansion_array_2D_12.csv', 'Expansion_array_2D_13.csv', 'Expansion_array_2D_14.csv', 'Expansion_array_2D_15.csv', 'Expansion_array_2D_16.csv', 'Expansion_array_2D_17.csv', 'Expansion_array_2D_18.csv', 'Expansion_array_2D_19.csv', 'Expansion_array_2D_2.csv', 'Expansion_array_2D_3.csv', 'Expansion_array_2D_4.csv', 'Expansion_array_2D_5.csv', 'Expansion_array_2D_6.csv', 'Expansion_array_2D_7.csv', 'Expansion_array_2D_8.csv', 'Expansion_array_2D_9.csv']
# expantion_array = ['Expansion_array_2D_0.csv', 'Expansion_array_2D_1.csv', 'Expansion_array_2D_10.csv', 'Expansion_array_2D_11.csv', 'Expansion_array_2D_12.csv', 'Expansion_array_2D_13.csv', 'Expansion_array_2D_14.csv', 'Expansion_array_2D_15.csv', 'Expansion_array_2D_16.csv', 'Expansion_array_2D_17.csv', 'Expansion_array_2D_18.csv', 'Expansion_array_2D_19.csv', 'Expansion_array_2D_2.csv', 'Expansion_array_2D_20.csv', 'Expansion_array_2D_21.csv', 'Expansion_array_2D_22.csv', 'Expansion_array_2D_23.csv', 'Expansion_array_2D_24.csv', 'Expansion_array_2D_25.csv', 'Expansion_array_2D_26.csv', 'Expansion_array_2D_27.csv', 'Expansion_array_2D_28.csv', 'Expansion_array_2D_29.csv', 'Expansion_array_2D_3.csv', 'Expansion_array_2D_30.csv', 'Expansion_array_2D_31.csv', 'Expansion_array_2D_32.csv', 'Expansion_array_2D_33.csv', 'Expansion_array_2D_34.csv', 'Expansion_array_2D_35.csv', 'Expansion_array_2D_36.csv', 'Expansion_array_2D_37.csv', 'Expansion_array_2D_38.csv', 'Expansion_array_2D_39.csv', 'Expansion_array_2D_4.csv', 'Expansion_array_2D_40.csv', 'Expansion_array_2D_41.csv', 'Expansion_array_2D_42.csv', 'Expansion_array_2D_43.csv', 'Expansion_array_2D_44.csv', 'Expansion_array_2D_45.csv', 'Expansion_array_2D_46.csv', 'Expansion_array_2D_47.csv', 'Expansion_array_2D_48.csv', 'Expansion_array_2D_49.csv', 'Expansion_array_2D_5.csv', 'Expansion_array_2D_50.csv', 'Expansion_array_2D_51.csv', 'Expansion_array_2D_52.csv', 'Expansion_array_2D_53.csv', 'Expansion_array_2D_54.csv', 'Expansion_array_2D_55.csv', 'Expansion_array_2D_56.csv', 'Expansion_array_2D_57.csv', 'Expansion_array_2D_58.csv', 'Expansion_array_2D_59.csv', 'Expansion_array_2D_6.csv', 'Expansion_array_2D_7.csv', 'Expansion_array_2D_8.csv', 'Expansion_array_2D_9.csv']
# expantion_array = ['Expansion_array_2D_0.csv', 'Expansion_array_2D_1.csv', 'Expansion_array_2D_10.csv', 'Expansion_array_2D_11.csv', 'Expansion_array_2D_12.csv', 'Expansion_array_2D_13.csv', 'Expansion_array_2D_14.csv', 'Expansion_array_2D_15.csv', 'Expansion_array_2D_16.csv', 'Expansion_array_2D_17.csv', 'Expansion_array_2D_18.csv', 'Expansion_array_2D_19.csv', 'Expansion_array_2D_2.csv', 'Expansion_array_2D_20.csv', 'Expansion_array_2D_21.csv', 'Expansion_array_2D_22.csv', 'Expansion_array_2D_23.csv', 'Expansion_array_2D_24.csv', 'Expansion_array_2D_25.csv', 'Expansion_array_2D_26.csv', 'Expansion_array_2D_27.csv', 'Expansion_array_2D_28.csv', 'Expansion_array_2D_29.csv', 'Expansion_array_2D_3.csv', 'Expansion_array_2D_30.csv', 'Expansion_array_2D_31.csv', 'Expansion_array_2D_32.csv', 'Expansion_array_2D_33.csv', 'Expansion_array_2D_34.csv', 'Expansion_array_2D_35.csv', 'Expansion_array_2D_36.csv', 'Expansion_array_2D_37.csv', 'Expansion_array_2D_38.csv', 'Expansion_array_2D_39.csv', 'Expansion_array_2D_4.csv', 'Expansion_array_2D_40.csv', 'Expansion_array_2D_41.csv', 'Expansion_array_2D_42.csv', 'Expansion_array_2D_43.csv', 'Expansion_array_2D_44.csv', 'Expansion_array_2D_45.csv', 'Expansion_array_2D_46.csv', 'Expansion_array_2D_47.csv', 'Expansion_array_2D_48.csv', 'Expansion_array_2D_49.csv', 'Expansion_array_2D_5.csv', 'Expansion_array_2D_6.csv', 'Expansion_array_2D_7.csv', 'Expansion_array_2D_8.csv', 'Expansion_array_2D_9.csv']

# Sort the list based on the number in the filename
# expantion_array.sort(key=lambda f: int(f.split('_')[-1].split('.')[0]))


