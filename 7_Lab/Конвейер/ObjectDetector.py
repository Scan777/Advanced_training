import math
import cv2
from ultralytics import YOLO
import supervision as sv
from operator import itemgetter
import numpy as np

    
class ObjectDetector:
    
    def __init__(self):
        self.x_sort = None
        self.currentClass = None
        self.isEmpty = False
        self.second = None

    def detect(self, frame, model):
        isEmpty= False
        result = model(frame, agnostic_nms=True, conf=0.5)[0]
        detections = sv.Detections.from_ultralytics(result)
        coord_center=[]
        for i in range (len(detections)):
            x=(detections.xyxy[i][0]+detections.xyxy[i][2])/2
            y=(detections.xyxy[i][1]+detections.xyxy[i][3])/2
            y_mm=200/250*y
            coord_center.append([x,y,y_mm])
        coord_center=np.array(coord_center) 
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
            cv2.line(frame, (200,0), (200, 480), (0, 255, 0), 5)
        if coord_center.size != 0   
            self.x_sort=sorted(coord_center,key=itemgetter(0)) #Координаты [x,y] отсортированные по возрастанию x
            self.currentClass = detections.class_id[0]
            if self.x_sort[0][0]<=200:
                self.isEmpty = True
                self.second=int(time.time())
                return self.getPosition()
            else:
                self.second=int(time.time())
                self.isEmpty = False
                return self.getPosition()
        else:
            return self.getPosition()
        
    def getPosition(self):
        return {
            'x_sort': self.x_sort,
            'currentClass': self.currentClass,
            'isEmpty': self.isEmpty,
            'second': self.second
        }