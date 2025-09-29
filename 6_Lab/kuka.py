import numpy as np
import time
import socket   

class Kuka:   
    def __init__(self, robot):
        self.robot = robot
        if not self.robot.can_connect:
                print('Connection error')
                import sys
                sys.exit(-1)
        self.name = self.robot.read('$ROBNAME[]', debug=False).decode()
        
    def set_base(self, base):
        time.sleep(0.05)
        Base=(self.robot.read(("BASE_DATA[" + str(base)+"]"), False).decode())
        self.robot.write("COM_FRAME", Base)
        self.robot.write("COM_CASEVAR", "1")
        while int(self.robot.read("COM_CASEVAR", False).decode())!=0:
            continue         
        
    def set_tool(self, tool):
        time.sleep(0.05)
        Tool=(self.robot.read(("TOOL_DATA[" + str(tool)+"]"), False).decode())
        self.robot.write("COM_FRAME", Tool)
        self.robot.write("COM_CASEVAR", "2")
        while int(self.robot.read("COM_CASEVAR", False).decode())!=0:
            continue         
        
    def set_speed(self, value):
        time.sleep(0.05)
        self.robot.write("COM_VALUE1", str(value), False)
        self.robot.write("COM_CASEVAR", "3", False)
        while int(self.robot.read("COM_CASEVAR", False).decode())!=0:
            continue     
            
    def lin_continuous(self, kuka, massiv):
        time.sleep(0.05)
        arr=self.massiv_coord(kuka, massiv)
        self.send_Frame_array(arr)
        self.robot.write("COM_LENGTH", str(arr.shape[0]-1), False)
        self.robot.write("COM_CASEVAR", "4", False)
        while int(self.robot.read("COM_CASEVAR", False).decode())!=0:
            continue
            
    def lin_continuous_massiv(self, arr):
        time.sleep(0.1)
        self.send_Frame_array(arr)
        self.robot.write("COM_LENGTH", str(arr.shape[0]-1), False)
        self.robot.write("COM_CASEVAR", "4", False)
        while int(self.robot.read("COM_CASEVAR", False).decode())!=0:
            continue 
            
    def ptp_continuous(self, kuka, massiv):
        time.sleep(0.05)
        arr=self.massiv_coord(kuka, massiv)
        self.send_Frame_array(arr)
        self.robot.write("COM_LENGTH", str(arr.shape[0]-1), False)
        self.robot.write("COM_CASEVAR", "5", False)
        while int(self.robot.read("COM_CASEVAR", False).decode())!=0:
            continue  

    def sptp_continuous(self, kuka, massiv):
        time.sleep(0.05)
        arr=self.massiv_coord(kuka, massiv)
        self.send_Frame_array(arr)
        self.robot.write("COM_LENGTH", str(arr.shape[0]-1), False)
        self.robot.write("COM_CASEVAR", "6", False)
        while int(self.robot.read("COM_CASEVAR", False).decode())!=0:
            continue  

    def lin_continuous_4(self, kuka, massiv):
        time.sleep(0.05)
        arr=self.massiv_coord_4(kuka, massiv)
        self.send_Frame_array_4(arr)
        self.robot.write("COM_LENGTH", str(arr.shape[0]-1), False)
        self.robot.write("COM_CASEVAR", "4", False)
        while int(self.robot.read("COM_CASEVAR", False).decode())!=0:
            continue  
            
    def ptp_continuous_4(self, kuka, massiv):
        time.sleep(0.05)
        arr=self.massiv_coord_4(kuka, massiv)
        self.send_Frame_array_4(arr)
        self.robot.write("COM_LENGTH", str(arr.shape[0]-1), False)
        self.robot.write("COM_CASEVAR", "5", False)
        while int(self.robot.read("COM_CASEVAR", False).decode())!=0:
            continue  

    def sptp_continuous_4(self, kuka, massiv):
        time.sleep(0.05)
        arr=self.massiv_coord_4(kuka, massiv)
        self.send_Frame_array_4(arr)
        self.robot.write("COM_LENGTH", str(arr.shape[0]-1), False)
        self.robot.write("COM_CASEVAR", "6", False)
        while int(self.robot.read("COM_CASEVAR", False).decode())!=0:
            continue  
            
    def send_Frame_array(self, arr):
        for i in range(len(arr)):
            index_string = ("COM_FRAME_ARRAY[" + str(i) + "]")
            self.send_Frame(arr[i], index_string)
            
    def send_Frame_array_4(self, arr):
        for i in range(len(arr)):
            index_string = ("COM_FRAME_ARRAY[" + str(i) + "]")
            self.send_Frame_4(arr[i], index_string)
                  
    def open_grip(self):
        time.sleep(0.05)
        self.robot.write('OUT5', 'False')
        self.robot.write('OUT6', 'True')
        self.robot.write("COM_CASEVAR", "7", False)
        while int(self.robot.read("COM_CASEVAR", False).decode())!=0:
            continue 
            
    def close_grip(self):
        time.sleep(0.05)
        self.robot.write('OUT5', 'True')
        self.robot.write('OUT6', 'False')
        self.robot.write("COM_CASEVAR", "7", False)
        while int(self.robot.read("COM_CASEVAR", False).decode())!=0:
            continue        

    def vacuum_on(self):
        time.sleep(0.05)
        self.robot.write('OUT7', 'True')
        self.robot.write("COM_CASEVAR", "8", False)
        while int(self.robot.read("COM_CASEVAR", False).decode())!=0:
            continue 
 
    def vacuum_off(self):
        time.sleep(0.05)
        self.robot.write('OUT7', 'False')
        self.robot.write("COM_CASEVAR", "8", False)
        while int(self.robot.read("COM_CASEVAR", False).decode())!=0:
            continue 
    
    def quit(self):
        time.sleep(0.05)
        self.robot.write("COM_CASEVAR", "9", False)
        while int(self.robot.read("COM_CASEVAR", False).decode())!=0:
            continue  
            
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
        
    def read_joint(self):
        joint_string = self.robot.read("$AXIS_ACT", False).decode()
        joint_string = joint_string.replace(',', '')
        joint = joint_string.split()
        self.A1_joint = float(joint[2])
        self.A2_joint = float(joint[4])
        self.A3_joint = float(joint[6])
        self.A4_joint = float(joint[8])
        self.A5_joint = float(joint[10])
        self.A6_joint = float(joint[12])
        self.global_position_joint = np.array([self.A1_joint, self.A2_joint, self.A3_joint, self.A4_joint, self.A5_joint, self.A6_joint])
                   
    def read_cartesian(self):
        cartesian_string = self.robot.read("$POS_ACT", False).decode()
        cartesian_string = cartesian_string.replace(',', '')
        cartesian = cartesian_string.split()
        self.x_cartesian = float(cartesian[2])
        self.y_cartesian = float(cartesian[4])
        self.z_cartesian = float(cartesian[6])
        self.A_cartesian = float(cartesian[8])
        self.B_cartesian = float(cartesian[10])
        self.C_cartesian = float(cartesian[12])
        self.E1_cartesian = float(cartesian[14])
        self.E2_cartesian = float(cartesian[16])
        self.E3_cartesian = float(cartesian[18])
        self.E4_cartesian = float(cartesian[20])
        self.E5_cartesian = float(cartesian[22])
        self.E6_cartesian = float(cartesian[24])
        self.global_position = np.array([self.x_cartesian, self.y_cartesian, self.z_cartesian, self.A_cartesian, self.B_cartesian, self.C_cartesian])
        
    def send_Frame(self, arr, system_variable=""):
        string_arr = []
        for i in range(len(arr)):
            string_arr.append(str(arr[i]))
        cartesian_string = ("{FRAME: X " + string_arr[0] + ", Y " + string_arr[1] + ", Z "+ string_arr[2] + ", A " + string_arr[3] + ", B " + string_arr[4] + ", C " + string_arr[5] + "}")
        self.robot.write(system_variable, cartesian_string, False)
        
    def robot_read(self, types):  
        print(self.robot.read(str(types), False).decode())
        
    def send_Frame_4(self, arr, system_variable=""):
        string_arr = []
        for i in range(len(arr)):
            string_arr.append(str(arr[i]))
        cartessian_string = ("{FRAME: X " + string_arr[0] + ", Y " + string_arr[1] + ", Z "+ string_arr[2] + ", A " + string_arr[3] + "}")
        #print(cartessian_string)
        self.robot.write(system_variable, cartessian_string, False)
        
    def massiv_coord(self, kuka, massiv):  
        kuka.read_cartesian()
        start_point = np.array([kuka.x_cartesian, kuka.y_cartesian, kuka.z_cartesian, kuka.A_cartesian, kuka.B_cartesian, kuka.C_cartesian])
        trajectory = np.vstack([start_point,massiv])
        return trajectory
    
    def massiv_coord_4(self, kuka, massiv):  
        kuka.read_cartesian()
        start_point = np.array([kuka.x_cartesian, kuka.y_cartesian, kuka.z_cartesian, kuka.A_cartesian])
        trajectory = np.vstack([start_point,massiv])
        return trajectory