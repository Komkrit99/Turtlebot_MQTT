from std_msgs.msg import String
import rospy
import sys
import select
import os
import threading
if os.name == 'nt':
    import msvcrt
    import time
else:
    import tty
    import termios
import paho.mqtt.client as mqtt
host = "test.mosquitto.org"
port = 8000


def on_connect(self, client, userdata, rc):
    print("MQTT Connected.")
    self.subscribe("TEST/MQTT")


def on_message(client, userdata, msg):
    global key
    key = msg.payload.decode("utf-8")
    print(key)


def connect_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host)
    client.loop_forever()

# def talker(msg):
#     pub = rospy.Publisher(msg.split(), String, queue_size=10)
#     rospy.init_node('publisher_node', anonymous=True)
#     rate = rospy.Rate(10)  # 10hz
#     while not rospy.is_shutdown():

#         rospy.loginfo(msg.split())
#         pub.publish(msg.split())
#         rate.sleep()

# state = ''
# if state != key:
#     talker(key)
#     state = key