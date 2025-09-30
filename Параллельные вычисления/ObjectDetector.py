import math
import cv2
from ultralytics import YOLO
import supervision as sv
from operator import itemgetter
import numpy as np
fx=604.602 #Фокусное расстояние по x для разрешения 640
fy=604.162 #Фокусное расстояние по x для разрешения 480
Cx=320 #Середина картинки по x для разрешения 640
Cy=240 #Середина картинки по y для разрешения 480
x0=282.73
y0=122.48
z0=451.23

class Robot_mm:
    def __init__(self):
        self.X_mm= None
        self.Y_mm = None
        self.Z_mm= None
        self.points=None
        
    def Kuka_base(self, kuka):
        # Чтение текущих координат робота
        kuka.read_cartesian()
        # Построение траектории
        first_point=[x0, y0, z0, 90.57, 0, 180]
        trajectory=np.array([first_point])
        kuka.lin_continuous(kuka,trajectory)

    def pixel_mm(self, depth, points):
        points=(int(points[0]), int (points[1]))
        print(points, depth[points[1], points[0]])
        X_mm=(depth[points[1], points[0]]*((Cx-points[0])/fx))
        Y_mm=(depth[points[1], points[0]]*((Cy-points[1])/fy))
        X_mm=X_mm+30 #Смещение камеры относительно центра захвата по x
        Y_mm=Y_mm+65 #Смещение камеры относительно центра захвата по y 
        Z_mm=depth[points[1], points[0]]-90 #Для (для магнитного захвата) 
        return X_mm, Y_mm, Z_mm

    def Kuka_move(self, kuka, depth, points):
        X_mm, Y_mm, Z_mm=self.pixel_mm(depth, points)
        # Чтение текущих координат робота
        kuka.read_cartesian()
        # Построение траектории
        first_point=[kuka.x_cartesian-X_mm, kuka.y_cartesian+Y_mm, kuka.z_cartesian-Z_mm, kuka.A_cartesian, 0, 180]
        trajectory=np.array([first_point])
        kuka.lin_continuous(kuka,trajectory)
        
class ObjectDetector:
    
    def __init__(self):
        self.x_sort = None
        self.currentClass = None

    def detect(self, frame, model):
        bounding_box_annotator = sv.BoxAnnotator()
        label_annotator = sv.LabelAnnotator(text_position=sv.Position.CENTER)
        percentage_bar_annotator = sv.BoxAnnotator()
        result = model(frame, agnostic_nms=True, conf=0.5, verbose=False)[0]
        detections = sv.Detections.from_ultralytics(result)
        coord_center=[]
        for i in range (len(detections)):
            x=(detections.xyxy[i][0]+detections.xyxy[i][2])/2
            y=(detections.xyxy[i][1]+detections.xyxy[i][3])/2
            coord_center.append([x,y])
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
        if coord_center.size != 0:   
            self.x_sort=sorted(coord_center,key=itemgetter(0)) #Координаты [x,y] отсортированные по возрастанию x
            self.currentClass = detections.class_id[0]
            return self.getPosition()
        else:
            return self.getPosition()
        
    def getPosition(self):
        return {
            'x_sort': self.x_sort,
            'currentClass': self.currentClass
        }