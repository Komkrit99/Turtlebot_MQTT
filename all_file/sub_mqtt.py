#!/usr/bin/env python

from pickle import GLOBAL
import cv2
import sys, select , os
import paho.mqtt.client as mqtt
import base64
import numpy as np
import threading
host = "enkey.bu.ac.th"
port = 1883
url = ''
bts = ''
def on_connect(self, client, userdata, rc):
    print("MQTT Connected.")
    self.subscribe("TurtleBot/stream")

def on_message(client, userdata,msg):
    global bts
    bts = msg.payload
    print(bts)


def bts_to_img(bts):
    '''
    :param bts: results from image_to_bts
    '''
    buff = np.fromstring(bts, np.uint8)
    buff = buff.reshape(1, -1)
    img = cv2.imdecode(buff, cv2.IMREAD_COLOR)
    return img
    
def read64():
    im_bytes = base64.b64decode(url)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
    img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
    return img

def read_img():
    while (True):
        try:
            global bts
            img = bts_to_img(bts)
            cv2.imshow('black and white', img)
        except:
            pass
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

call_img = threading.Thread(target=read_img)
call_img.start()
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(host)
client.loop_forever()


# rospy.init_node('turtlebot3_teleop')
# pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)

# turtlebot3_model = rospy.get_param("model", "burger")
# twist = Twist()
# print('a')
# twist.linear.x = 0.1; twist.linear.y = 0.0; twist.linear.z = 0.0
# twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
# pub.publish(twist)