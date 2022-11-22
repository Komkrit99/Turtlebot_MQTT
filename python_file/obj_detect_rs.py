from inspect import Parameter
from multiprocessing.connection import wait
from random import getrandbits
import numpy as np
import cv2
from cv2 import waitKey
from matplotlib.transforms import Bbox
from numpy import array, size
import cv2.aruco as aruco
import pyrealsense2
from realsense_depth import *


framesize = [640, 480]
dc = DepthCamera() #call realsense camera
#cap = cv2.VideoCapture(0)
point = (400, 300)

def show_distance(event, x, y, args, params):
    global point
    point = (x, y)

def findARuco(img,depth_frame,marker_size=4,total_marker = 250,draw = True):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    key =getattr(aruco,f'DICT_{marker_size}X{marker_size}_{total_marker}')
    arucoDict = aruco.Dictionary_get(key)
    arucoParam = aruco.DetectorParameters_create()
    corners,ids,_objPoints = aruco.detectMarkers(gray,arucoDict,parameters=arucoParam)
    if ids != None:
        point = [round((corners[0][0][0][0]+corners[0][0][1][0]+corners[0][0][2][0]+corners[0][0][3][0])/4),round((corners[0][0][0][1]+corners[0][0][1][1]+corners[0][0][2][1]+corners[0][0][3][1])/4)]
        distance = depth_frame[int(point[1]), int(point[0])]

        cv2.putText(img, "{}mm".format(distance), (int(point[0]), int(point[1] )- 20), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
        print(point)
    if draw:
        aruco.drawDetectedMarkers(img,corners,ids)
    return (corners,ids)

while True:
    ret, depth_frame, color_frame = dc.get_frame()
    #_,img=cap.read()
    #img = cv2.imread("/home/n/python_file/images/singlemarkerssource.png")
    #img = cv2.resize(img,(0,0),fx=0.7,fy=0.7)
    #gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    corners,ids = findARuco(color_frame,depth_frame)
    

    #cv2.imshow("img",img)
    cv2.imshow("Color frame", color_frame)

    if cv2.waitKey(1)==113:
        break