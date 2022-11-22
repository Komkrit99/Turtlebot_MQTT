from inspect import Parameter
from multiprocessing.connection import wait
from random import getrandbits
import numpy as np
import cv2
from cv2 import waitKey
from matplotlib.transforms import Bbox
from numpy import array, size
import argparse
import os
import time

cap = cv2.VideoCapture(0)
net = cv2.dnn.readNetFromDarknet('yolov3.cfg', 'yolov3.weights')
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)


while True:
    _,img=cap.read()
    img = cv2.resize(img,(0,0),fx=0.7,fy=0.7)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    

    cv2.imshow("img",img)
    cv2.imshow("gray",gray)

    if cv2.waitKey(1)==113:
        break