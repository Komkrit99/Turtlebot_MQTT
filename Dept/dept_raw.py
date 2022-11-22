#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import CompressedImage
import cv2
import numpy as np
import threading 
import cv2
import mediapipe as mp
import paho.mqtt.client as mqtt
import time

host = "enkey.bu.ac.th"
port = 1883

client = mqtt.Client()
client.connect(host)

mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils

def callback(data):
    newFile = open("img_raw.raw", "wb")
    newFile.write(data.data)

def listener():
    print('thread')
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('camera/color/image_raw/compressed', CompressedImage, callback)
    rospy.spin()

def open_cam():
    while(True):
        try:
                im = cv2.imread('img_raw.raw')
                results = pose.process(im)
                if results.pose_landmarks:
                    mpDraw.draw_landmarks(im, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
                    for id, lm in enumerate(results.pose_landmarks.landmark):
                        h, w,c = im.shape
                        cx, cy = int(lm.x*w), int(lm.y*h)
                        wc = ((w/2)-cx)
                        hc = ((h/2)-cy)
                        if(wc > 200 and wc >):
                            print('a')
                        if(wc < -100):

                        #cv2.circle(img, (cx, cy), 5, (255,0,0), cv2.FILLED)
                cv2.imshow('', im)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
        except:
                pass
    cv2.destroyAllWindows()

if __name__ == '__main__':
    threading.Thread(target=open_cam).start()
    listener()
    
