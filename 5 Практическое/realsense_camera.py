import pyrealsense2 as rs
import numpy as np
import json

class RealsenseCamera:
    def __init__(self):
        self.pipeline = rs.pipeline() 
        config = rs.config()
        # Configure depth and color streams
        #print("Loading Intel Realsense Camera")
        #json_config_file = json.load(open("Default.json"))
        #json_config_string = str(json_config_file).replace("'", '\"')
       
        #print("W: ", int(json_config_file["viewer"]['stream-width']))
        #print("H: ", int(json_config_file["viewer"]['stream-height']))
        #print("FPS: ", int(json_config_file["viewer"]['stream-fps']))
        #config.enable_stream(rs.stream.depth, int(json_config_file["viewer"]['stream-width']), int(json_config_file["viewer"]['stream-height']), rs.format.z16, int(json_config_file["viewer"]['stream-fps']))
        #config.enable_stream(rs.stream.color, int(json_config_file["viewer"]['stream-width']), int(json_config_file["viewer"]['stream-height']), rs.format.bgr8, int(json_config_file["viewer"]['stream-fps']))
        #profile = self.pipeline.start(config)
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        
        dev = self.pipeline.start(config).get_device()
        align_to = rs.stream.color
        self.align = rs.align(align_to)
        
        self.depth_sensor = dev.first_depth_sensor()


        #advnc_mode = rs.rs400_advanced_mode(dev)
        #advnc_mode.load_json(json_config_string)
        
    
    def get_frame_stream(self):
        # Wait for a coherent pair of frames: depth and color
        frames = self.pipeline.wait_for_frames()
        aligned_frames = self.align.process(frames)
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        
        if not depth_frame or not color_frame:
            # If there is no frame, probably camera not connected, return False
            print("Error, impossible to get the frame, make sure that the Intel Realsense camera is correctly connected")
            return False, None, None
        
       # Apply filter to fill the Holes in the depth image
        spatial = rs.spatial_filter()
        spatial.set_option(rs.option.holes_fill, 3)
        filtered_depth = spatial.process(depth_frame)

        hole_filling = rs.hole_filling_filter()
        filled_depth = hole_filling.process(filtered_depth)

        
        # Create colormap to show the depth of the Objects
        colorizer = rs.colorizer()
        depth_colormap = np.asanyarray(colorizer.colorize(filled_depth).get_data())
        aligned_depth_frame = aligned_frames.get_depth_frame()

        depth = np.asanyarray(aligned_depth_frame.get_data())
        # Convert images to numpy arrays
        #distance = depth_frame.get_distance(int(50),int(50))
        #print("distance", distance)
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        #cv2.imshow("Colormap", depth_colormap)
        #cv2.imshow("depth img", depth_image)

        return True, depth_image, color_image, depth
    
    def release(self):
        self.pipeline.stop()
        #print(depth_image)
        
        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        #depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.10), 2)

        # Stack both images horizontally
        
        #images = np.hstack((color_image, depth_colormap))


