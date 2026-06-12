import SPiiPlusPython as sp
import sys
import socket
import struct
import time

# Connection 
global acs_axis_list
global wago_temparature_sensor
acs_axis_list = [sp.Axis.ACSC_AXIS_0,sp.Axis.ACSC_AXIS_1, sp.Axis.ACSC_AXIS_2, sp.Axis.ACSC_AXIS_3,sp.Axis.ACSC_AXIS_4,sp.Axis.ACSC_AXIS_5,sp.Axis.ACSC_AXIS_6]
#acs_axis_list = [1,2,3]
wago_temparature_sensor = ["Temparature_sensor_1", "Temparature_sensor_2", "Temparature_sensor_3", "Temparature_sensor_4"]

class scan_network():
    def __init__(self):
        pass

    def scan_network_function(self):
        IPAddresses = sp.GetEthernetCardsExt(sys.getsizeof( sp.ACSC_APPSL_INFO_c), 10, socket.INADDR_BROADCAST, True)           ## from snowflake 
        ips = []
        for ip_addr in IPAddresses:
            ip = socket.inet_ntoa(struct.pack("!L", socket.htonl(int(ip_addr.IpAddress.s_addr))))
            ips.append(ip)
            print("Card data:")                     
            print(f"Controller ip: {ip}")
            print(f"Controller FW version: {ip_addr.Version}")
            print(f"Controller serial number: {ip_addr.SerialNumber}\n\n")
        return ips

class enable_communication():
    def __init__ (self):
        pass
    def enable_communication_function(self,ip):
        #ip = "10.0.0.100"
        port = 701
        hc= sp.OpenCommEthernetTCP(ip, port)
        #if hc == -1:
        #    print ("Failed to connect", hc)
        #else :
        #    print(hc)
        return hc

class disconnect_communication():
    def __init__ (self):
        pass
    def disconnect_communication_function(self,hc):
        hc = sp.CloseComm(hc)
        #print("communication closed")
        return hc

class motor_activation():
    def __init__(self):
        pass
    def enable(self,hc,axis):       # to set enable
        global acs_axis_list
        tc = sp.Enable(hc, acs_axis_list[axis], sp.SYNCHRONOUS, True)
        return tc
    def disable(self,hc,axis):      # to set disable
        tc = sp.Disable(hc, acs_axis_list[axis], sp.SYNCHRONOUS, True)
        return tc
    def state(self,hc,axis):      # get the motor state to display current status
        buf = "?MST("+str(axis)+").#ENABLED \r"
        state = sp.Transaction(hc, buf, len(buf), 256, sp.SYNCHRONOUS, False)
        return int(state)
    
    def absolute_motion(self,hc,axis,position):
        global acs_axis_list
        tc = sp.ToPoint(hc, 0, acs_axis_list[axis], position, sp.SYNCHRONOUS, True)
        return tc


class control_all_axis():
    def __init__ (self):
        pass
    def desable_all(self,hc):
        tc = sp.DisableAll(hc,sp.SYNCHRONOUS, failure_check=False)
        return tc



# class to read paremters from the controller
class get_axis_parameters():
    def __init__(self):
        pass
    def axis_velocity(self,hc,axis):
        global acs_axis_list
        velocity = sp.GetVelocity(hc, acs_axis_list[axis], sp.SYNCHRONOUS, True)
        return velocity
    
    def axis_acceleration(self,hc,axis):
        global acs_axis_list
        acceleration = sp.GetAcceleration(hc,acs_axis_list[axis],sp.SYNCHRONOUS,True)
        return acceleration
    
    def axis_deceleration(self,hc,axis):
        global acs_axis_list
        deceleration = sp.GetDeceleration(hc,acs_axis_list[axis],sp.SYNCHRONOUS,True)
        return deceleration
    
    def axis_kill_deceleration(self,hc,axis):
        global acs_axis_list
        kill_deceleration = sp.GetKillDeceleration(hc,acs_axis_list[axis],sp.SYNCHRONOUS,True)
        return kill_deceleration
    
    def axis_jerk(self,hc,axis):
        global acs_axis_list
        jerk = sp.GetJerk(hc,acs_axis_list[axis],sp.SYNCHRONOUS,True)
        return jerk
    
    def axis_fpos(self,hc,axis):
        global acs_axis_list
        fpos = sp.GetFPosition(hc,acs_axis_list[axis],sp.SYNCHRONOUS,True)
        return fpos
    
    def axis_pe(self,hc,axis):
        buf = "?PE("+str(axis)+") \r"
        PE = sp.Transaction(hc, buf, len(buf), 256, sp.SYNCHRONOUS, True)
        return PE
    
    def axis_motion_state(self,hc,axis):
        buf = "?MST("+str(axis)+").#MOVE \r"
        axis_on_motion = sp.Transaction(hc, buf, len(buf), 256, sp.SYNCHRONOUS, True)
        return int(axis_on_motion)
    
# set peremters to the controller
class set_axis_perameters():
    def __init__(self): 
        pass
    def axis_velocity(self,hc,axis,velocity):
        global acs_axis_list
        sp.SetVelocity(hc,acs_axis_list[axis],velocity, sp.SYNCHRONOUS, False) # no error checking
        return 0
    
    def axis_acceleration(self,hc,axis,acceleration):
        global acs_axis_list
        sp.SetAcceleration(hc,acs_axis_list[axis],acceleration, sp.SYNCHRONOUS, False)
        return 0

    def axis_deceleration(self,hc,axis,deceleration):
        global acs_axis_list
        sp.SetDeceleration(hc,acs_axis_list[axis],deceleration,sp.SYNCHRONOUS,False)
        return 0
    
    def axis_kill_deceleration(self,hc,axis,kill_deceleration):
        global acs_axis_list
        sp.SetKillDeceleration(hc,acs_axis_list[axis],kill_deceleration,sp.SYNCHRONOUS,False)
        return 0

    def axis_jerk(self,hc,axis,jerk):
        global acs_axis_list
        sp.SetJerk(hc,acs_axis_list[axis],jerk,sp.SYNCHRONOUS,False)
        return 0
    
class read_parameters():
    def __init__(self):
        pass

    def read_temparature(self, hc, sensor_index):
        global wago_temparature_sensor
        value = (sp.ReadReal(hc, -1,wago_temparature_sensor[sensor_index],-1, -1, -1, -1,sp.SYNCHRONOUS))/10
        return value
    
    def read_led_status(self, hc, led_name):
        led_status = sp.ReadReal(hc, -1, led_name, -1, -1, -1, -1, sp.SYNCHRONOUS)
        return led_status
    
class write_parameters():
    def __init__(self):
        pass

    def write_led_status(self, hc, led_name, led_value):
        led_value = float(led_value)
        sp.WriteReal(hc, -1, led_name, -1, -1, -1, -1, led_value, sp.SYNCHRONOUS)   
        return 0

class error_mappting():
    def __init__(self):
        pass

    def get_current_error_map_status(self,hc,axis):
        global acs_axis_list
        buf = "#ERRORMAPREP\r"
        error_map_status = sp.Transaction(hc, buf, len(buf), 256, sp.SYNCHRONOUS, failure_check=False)
        return str(error_map_status)


    def load_buffer(self,hc, buffer_number, buffer_text):
        sp.LoadBuffer(hc,buffer_number,buffer_text,len(buffer_text),sp.SYNCHRONOUS, False)
        return 0

