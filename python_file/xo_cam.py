from inspect import Parameter
from itertools import count
from multiprocessing.connection import wait
from random import gauss, getrandbits
from cv2 import circle
#from matplotlib.colors import TwoSlopeNorm
import numpy as np
import cv2
from cv2 import waitKey
from matplotlib.transforms import Bbox
import matplotlib.pyplot as plt
from numpy import array, size
import argparse
import os
import time

cap = cv2.VideoCapture(0)

one = ((250,100),(350,200))
two = ((350,100),(450,200))
three = ((450,100),(550,200))
four = ((250,200),(350,300))
five = ((350,200),(450,300))
six = ((450,200),(550,300))
seven = ((250,300),(350,400))
eight = ((350,300),(450,400))
nine = ((450,300),(550,400))

player_input = {}

def condition(x,y):
    print(five[0][0],'-',x,'-',five[1][0])
    if(x <= one[0][0] and x >= one[1][0] and y <= one[0][1] and y >= one[1][1] ):
        return '1'
    elif(x <= two[0][0] and x >= two[1][0] and y <= two[0][1] and y >= two[1][1] ):
        return '2'
    elif(x <= three[0][0] and x >= three[1][0] and y <= three[0][1] and y >= three[1][1] ):
        return '3'
    elif(x <= four[0][0] and x >= four[1][0] and y <= four[0][1] and y >= four[1][1] ):
        return '4'
    elif(x <= five[0][0] and x >= five[1][0] and y <= five[0][1] and y >= five[1][1] ):
        print(5)
        return '5'
    elif(x <= six[0][0] and x >= six[1][0] and y <= six[0][1] and y >= six[1][1] ):
        return '6'
    elif(x <= seven[0][0] and x >= seven[1][0] and y <= seven[0][1] and y >= seven[1][1] ):
        return '7'
    elif(x <= eight[0][0] and x >= eight[1][0] and y <= eight[0][1] and y >= eight[1][1] ):
        return '8'
    elif(x <= nine[0][0] and x >= nine[1][0] and y <= nine[0][1] and y >= nine[1][1] ):
        return '9'
    

while True:
    _,img=cap.read()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(7,7),cv2.BORDER_DEFAULT)
    ret, thresh = cv2.threshold(blur,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    find_circle = cv2.HoughCircles(blur,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=0,maxRadius=50)
    
    
    #cv2.circle(circles[0],circles[1],circles[2],(255,0,0),2)
    try:
        #circles = np.uint16(np.around(find_circle[0][0]))
        #cv2.circle(img,(circles[0],circles[1]),circles[2],(0,255,0),10)
        circles = np.uint16(np.around(find_circle))
        for i in circles[0,:]:
              cv2.circle(img,(i[0],i[1]),i[2],(0,0,255),10)
              #print(i[0],i[1],i[2])
              print(condition(i[0],i[1]))
              #player_input.add(condition(i[0],i[1]))
    except:
        pass
        
    img = cv2.rectangle(img,one[0],one[1],(255,0,0),5) #5
    img = cv2.putText(img,'1',four[0],cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),1)
    img = cv2.rectangle(img,two[0],two[1],(0,255,0),5) #6
    img = cv2.rectangle(img,three[0],three[1],(0,0,255),5) #4
    img = cv2.rectangle(img,four[0],four[1],(255,0,0),5) #8
    img = cv2.rectangle(img,five[0],five[1],(0,255,0),5) #9
    img = cv2.rectangle(img,six[0],six[1],(0,255,0),5) #3
    img = cv2.rectangle(img,seven[0],seven[1],(0,0,255),5) #7
    img = cv2.rectangle(img,eight[0],eight[1],(255,0,0),5) #2
    img = cv2.rectangle(img,nine[0],nine[1],(0,0,255),5) #1
    cv2.imshow("img",img)


    if cv2.waitKey(1)==113:
        break