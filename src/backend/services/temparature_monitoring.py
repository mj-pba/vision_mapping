# 2D_OPTICAL_VISION_MAPPING/src/backend/services/temparature_monitoring.py

# in this program I am trying to meaure and recode the temperature variation for long prediod of time
# sensors are connected to ethecat network
# We have to connect to the ethercat network via ACS control modules and read the sensor parameters



from fileinput import filename
import sys
import os
import time
import numpy as np
import datetime

# Add the project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..','..'))
sys.path.insert(0, project_root)

# Direct import from the module path - this avoids loading src/__init__.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from motor_control.acs_python_modules import scan_network, enable_communication, read_parameters, error_mappting,disconnect_communication



class TemperatureMonitoring:
    def __init__(self):
        self.ACS_read_parameters = read_parameters()
        self.hc = None
        self.temperature = np.zeros(4)
        self.current_filename = None
        self.current_date = None

        # Set end date to August 31, 2025 (YYYY, MM, DD)
        self.end_date = datetime.datetime(2025, 9, 30, 16, 59, 59)
    
        # Create a logs directory if it doesn't exist
        self.log_dir = os.path.join(project_root, "temperature_logs")
        os.makedirs(self.log_dir, exist_ok=True)
    # Search the network and connect to ACS controller
    def connect_to_acs_controller(self):
        print("Connecting to ACS controller...")
        ACS_network_scan = scan_network()
        ips = ACS_network_scan.scan_network_function()
        if ips:
            print(f"Found ACS controller at IP: {ips[0]}")
            self.ip_address = ips[0]
            comm = enable_communication()
            self.hc = comm.enable_communication_function(self.ip_address)
            print("Communication enabled.")
            print(self.hc)
        else:
            print("No ACS controller found.")

    # disconnect from ACS controller
    def disconnect_from_acs_controller(self):
        if self.hc is not None:
            ACS_disconnect = disconnect_communication()
            ACS_disconnect.disconnect_communication_function(self.hc)
            print("Disconnected from ACS controller.")
        else:
            print("No connection to ACS controller.")

    def read_temperature_sensor(self, sensor_index):
        """Read temperature from specified sensor (0-3)"""
        if self.hc is not None:
            return self.ACS_read_parameters.read_temparature(self.hc, sensor_index)
        else:
            print("No connection to ACS controller")
            return None

    def check_and_create_daily_file(self):
        """Check if we need to create a new daily file"""
        today = datetime.datetime.now().date()
        
        # Create a new file if it's a new day or if we don't have a file yet
        if self.current_date != today or self.current_filename is None:
            # Update the current date
            self.current_date = today
            # Create a new filename with just the date (no time)
            date_str = today.strftime("%Y%m%d")
            filename = os.path.join(self.log_dir, f"temperature_log_{date_str}.csv")
            
            # Create the file if it doesn't exist
            file_exists = os.path.exists(filename)
            with open(filename, 'a') as file:
                if not file_exists:
                    file.write("Count,Time,Sensor1,Sensor2,Sensor3,Sensor4\n")
            
            self.current_filename = filename
            print(f"Created new log file: {filename}")
            return True
        
        return False

    def write_temperature_to_file(self, count):
        """Write the temperature data to the current file."""
        with open(self.current_filename, 'a') as file:
            current_time = time.strftime("%H:%M:%S")
            file.write(f"{count},{current_time},{self.temperature[0]},{self.temperature[1]},{self.temperature[2]},{self.temperature[3]}\n")

    def main_module(self):
        # Connect to the ACS controller
        self.connect_to_acs_controller()
        
        # Initialize counter
        count = 0
        
        try:
            # Run until the end date is reached
            while datetime.datetime.now() < self.end_date:
                # Check if we need to create a new daily file
                self.check_and_create_daily_file()
                
                # Read temperatures from all sensors
                for i in range(4):
                    temperature = self.read_temperature_sensor(i)
                    if temperature is not None:
                        self.temperature[i] = temperature
                
                # Print and log the temperature readings
                print(f"Count {count} - Temperature readings:", self.temperature)
                self.write_temperature_to_file(count)
                
                # Increment counter and wait before next reading
                count += 1
                time.sleep(20)  # Take readings every 20 seconds

            print(f"Monitoring complete. End date ({self.end_date.date()}) reached.")
            
        except KeyboardInterrupt:
            print("Monitoring stopped by user.")
        except Exception as e:
            print(f"Error during monitoring: {e}")
        finally:
            # Always disconnect properly when done
            self.disconnect_from_acs_controller()


# main program

if __name__ == "__main__":
    temperature_monitoring = TemperatureMonitoring()
    temperature_monitoring.main_module()