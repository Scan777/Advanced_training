import math
import cv2
from ultralytics import YOLO
import supervision as sv
from operator import itemgetter
import numpy as np
import pyrealsense2
from realsense_camera import *
   
fx=604.602
fy=604.162
Cx=320
Cy=240

bounding_box_annotator = sv.BoundingBoxAnnotator()
percentage_bar_annotator = sv.BoundingBoxAnnotator()

class ObjectDetector:
    
    def __init__(self):
        self.x_sort = None
        self.currentClass = None
        self.second = [0]
        self.second_max = [0]

    def detect(self, frame, depth, model):
        result = model(frame, agnostic_nms=True, conf=0.5, verbose=False)[0]
        detections = sv.Detections.from_ultralytics(result)
        coord_center=[]
        for i in range (len(detections)):
            x=(detections.xyxy[i][0]+detections.xyxy[i][2])/2
            y=(detections.xyxy[i][1]+detections.xyxy[i][3])/2
            Y_mm=(depth[int(y), int(x)])*((Cy-y)/fy)
            coord_center.append([x,y,Y_mm])
        coord_center=np.array(coord_center) 
        if coord_center.size != 0:
            for i in range (len(detections)):
                frame = bounding_box_annotator.annotate(
                    scene=frame,
                    detections=detections
                )
                frame = percentage_bar_annotator.annotate(
                    scene=frame,
                    detections=detections
                )
                cv2.circle(frame, (int(coord_center[i][0]),int(coord_center[i][1])), 3, (118, 103, 154), 3) 
                cv2.line(frame, (580,0), (580, 480), (0, 255, 0), 5)
                cv2.line(frame, (100,0), (100, 480), (0, 255, 0), 5)
            self.x_sort=sorted(coord_center,key=itemgetter(0)) #Координаты [x,y] отсортированные по возрастанию x
            self.currentClass = detections.class_id[0]
            return self.getPosition()
        else:
            return self.getPosition()
        
    def getPosition(self):
        return {
            'x_sort': self.x_sort,
            'currentClass': self.currentClass,
            'second': self.second,
            'second_max': self.second_max
        }