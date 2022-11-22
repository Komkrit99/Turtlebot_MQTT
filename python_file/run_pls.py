import rospy

from geometry_msgs.msg import Twist
import time
import datetime
import paho.mqtt.client as mqtt
rospy.init_node('turtlebot3_teleop')
pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)

turtlebot3_model = rospy.get_param("model", "burger")
count = 0

"""
while(True):
    count += 1
    twist = Twist()
    print('a')
    twist.linear.x = 1.0; twist.linear.y = 0.0; twist.linear.z = 0.0
    twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
    pub.publish(twist)
    pub.publish(twist)
    pub.publish(twist)
    pub.publish(twist)
    time.sleep(0.01)
    if count > 1000:
        break
"""

def move(x,r,second):
    a = datetime.datetime.now()
    while(True):
        twist = Twist()
        twist.linear.x = x; twist.linear.y = 0.0; twist.linear.z = 0.0
        twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = r
        pub.publish(twist)
        pub.publish(twist)
        pub.publish(twist)
        pub.publish(twist)
        b = datetime.datetime.now()
        delta = b - a
        time.sleep(0.01)
        print(int(delta.total_seconds() * 1000))
        if(int(delta.total_seconds() * 1000)> (second * 1000)):
            break


host = "enkey.bu.ac.th"
port = 1883

def on_connect(self, client, userdata, rc):
    print("MQTT Connected.")
    self.subscribe("Turtlebot3/MQTT")

def on_message(client, userdata,msg):
    print(msg.payload.decode("utf-8", "w"))
    if(msg.payload.decode("utf-8", "w") == 'w'):
        move(0.22,0.0,0.5)
    elif(msg.payload.decode("utf-8", "w") == 's'):
        move(-0.22,0.0,0.5)
    elif(msg.payload.decode("utf-8", "w") == 'a'):
        move(0.0,1.5,0.5)
    elif(msg.payload.decode("utf-8", "w") == 'd'):
        move(0.0,-1.5,0.5)
    elif(msg.payload.decode("utf-8", "w") == 'q'):
        move(0.0,0.0,0.0)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(host)
client.loop_forever()
