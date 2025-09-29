import numpy as np
import time
import socket   

class Kuka:   
    def __init__(self, robot):
        self.robot = robot
        #Test connection
        if not self.robot.can_connect:
                print('Connection error')
                import sys
                sys.exit(-1)
        self.name = self.robot.read('$ROBNAME[]', debug=False).decode()
   
    def ptp(self, arr):
        #time.sleep(0.1)
        self.send_Frame(arr, "COM_FRAME")
        self.robot.write("COM_CASEVAR", "7", False)
        #while int(self.robot.read("COM_CASEVAR", False).decode())!=0:
        #    continue 
        
    def lin_continuous(self, arr):
        time.sleep(0.1)
        self.send_Frame_array(arr)
        self.robot.write("COM_LENGTH", str(arr.shape[0]-1), False)
        self.robot.write("COM_CASEVAR", "4", False)
        while int(self.robot.read("COM_CASEVAR", False).decode())!=0:
            continue 
            
    def open_grip(self):
        time.sleep(0.1)
        self.robot.write('OUT5', 'False')
        self.robot.write('OUT6', 'True')
        self.robot.write("COM_CASEVAR", "5", False)
        #print('open')
        while int(self.robot.read("COM_CASEVAR", False).decode())!=0:
            continue 
            
    def close_grip(self):
        time.sleep(0.1)
        self.robot.write('OUT5', 'True')
        self.robot.write('OUT6', 'False')
        self.robot.write("COM_CASEVAR", "5", False)
        #print('close')
        while int(self.robot.read("COM_CASEVAR", False).decode())!=0:
            continue        
         
    def E_close_grip(Nm, sock):
        #host = "192.168.1.160" #ESP32 IP in local network
        #port = 80             #ESP32 Server Port    
        #сила сжатия
        a=str(Nm)+str(",")+str(1)
        sock.send(a.encode('utf-8'))
        
    def E_open_grip(sock):
        #host = "192.168.1.160" #ESP32 IP in local network
        #port = 80             #ESP32 Server Port    
        #сила сжатия
        a=str(0)+str(",")+str(0)
        sock.send(a.encode('utf-8'))

    def vacuum_on(self):
        time.sleep(0.1)
        self.robot.write('OUT7', 'True')
        self.robot.write("COM_CASEVAR", "6", False)
        print('on')
        while int(self.robot.read("COM_CASEVAR", False).decode())!=0:
            continue 
 
    def vacuum_off(self):
        time.sleep(0.1)
        self.robot.write('OUT7', 'False')
        self.robot.write("COM_CASEVAR", "6", False)
        print('off')
        while int(self.robot.read("COM_CASEVAR", False).decode())!=0:
            continue 
              
    def ptp_continuous(self, arr):
        self.send_Frame_array(arr)
        self.robot.write("COM_LENGTH", str(arr.shape[0]-1))
        self.robot.write("COM_CASEVAR", "4")
        
    def read_base(self):
        string = self.robot.read("$BASE", False).decode()
        string = string.replace(',', '')
        string = string.replace('{', '')
        string = string.replace('}', '')
        string = string.split()
        self.base_frame_x = float(string[2])
        self.base_frame_y = float(string[4])
        self.base_frame_z = float(string[6])
        self.base_frame_A = float(string[8])
        self.base_frame_B = float(string[10])
        self.base_frame_C = float(string[12])
        self.base_frame = np.array([self.base_frame_x, self.base_frame_y, self.base_frame_z, self.base_frame_A, self.base_frame_B, self.base_frame_C])

    def read_cartessian(self):
        cartessian_string = self.robot.read("$POS_ACT", False).decode()
        cartessian_string = cartessian_string.replace(',', '')
        cartessian = cartessian_string.split()
        self.x_cartessian = float(cartessian[2])
        self.y_cartessian = float(cartessian[4])
        self.z_cartessian = float(cartessian[6])
        self.A_cartessian = float(cartessian[8])
        self.B_cartessian = float(cartessian[10])
        self.C_cartessian = float(cartessian[12])
        self.E1_cartessian = float(cartessian[14])
        self.E2_cartessian = float(cartessian[16])
        self.E3_cartessian = float(cartessian[18])
        self.E4_cartessian = float(cartessian[20])
        self.E5_cartessian = float(cartessian[22])
        self.E6_cartessian = float(cartessian[24])
        self.global_position = np.array([self.x_cartessian, self.y_cartessian, self.z_cartessian, self.A_cartessian, self.B_cartessian, self.C_cartessian])
           
    def set_base(self, base):
        time.sleep(0.1)
        Base=(self.robot.read(("BASE_DATA[" + str(base)+"]"), False).decode())
        self.robot.write("COM_FRAME", Base)
        self.robot.write("COM_CASEVAR", "1")
        while int(self.robot.read("COM_CASEVAR", False).decode())!=0:
            continue 
  
    def set_tool(self, tool):
        time.sleep(0.1)
        Tool=(self.robot.read(("TOOL_DATA[" + str(tool)+"]"), False).decode())
        self.robot.write("COM_FRAME", Tool)
        self.robot.write("COM_CASEVAR", "2")
        while int(self.robot.read("COM_CASEVAR", False).decode())!=0:
            continue 
            
    def read_tool(self):
        string = self.robot.read("$TOOL", False).decode()
        string = string.replace(',', '')
        string = string.replace('{', '')
        string = string.replace('}', '')
        string = string.split()
        self.tool_frame_x = float(string[2])
        self.tool_frame_y = float(string[4])
        self.tool_frame_z = float(string[6])
        self.tool_frame_A = float(string[8])
        self.tool_frame_B = float(string[10])
        self.tool_frame_C = float(string[12])
        self.tool_frame = np.array([self.tool_frame_x, self.tool_frame_y, self.tool_frame_z, self.tool_frame_A, self.tool_frame_B, self.tool_frame_C])

    def send_E6POS(self, arr, system_variable=""):
        string_arr = []
        for i in range(len(arr)):
            string_arr.append(str(arr[i]))
        string = ("{E6POS: X " + string_arr[0] + ", Y " + string_arr[1] + ", Z "+ string_arr[2] + ", A " + string_arr[3] + ", B " + string_arr[4] + ", C " + string_arr[5] + ", E1 " + str(self.E1_cartessian) + ", E2 " + str(self.E2_cartessian) + ", E3 " + str(self.E3_cartessian) + ", E4 " + str(self.E4_cartessian) + ", E5 " + str(self.E5_cartessian) + ", E6 " + str(self.E6_cartessian) + "}")
        print("string to be sent: ", string, " variable: ", system_variable)
        self.robot.write(system_variable, string, False)

    def send_Frame(self, arr, system_variable=""):
        string_arr = []
        for i in range(len(arr)):
            string_arr.append(str(arr[i]))
        cartessian_string = ("{FRAME: X " + string_arr[0] + ", Y " + string_arr[1] + ", Z "+ string_arr[2] + ", A " + string_arr[3] + ", B " + string_arr[4] + ", C " + string_arr[5] + "}")
        #print(cartessian_string)
        self.robot.write(system_variable, cartessian_string, False)
        
    def send_Frame_array(self, arr):
        #self.robot.write("COM_LENGTH", str(length)) # Send length of array
        for i in range(len(arr)):
            index_string = ("COM_FRAME_ARRAY[" + str(i) + "]")
            self.send_Frame(arr[i], index_string)
            
    def set_speed(self, value):
        time.sleep(0.1)
        #self.robot.write("$OV_PRO", str(value), False)
        self.robot.write("COM_VALUE1", str(value), False)
        self.robot.write("COM_CASEVAR", "3", False)
        while int(self.robot.read("COM_CASEVAR", False).decode())!=0:
            continue 
