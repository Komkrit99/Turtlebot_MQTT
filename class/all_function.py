import rospy
import threading
import cv2
from sensor_msgs.msg import CompressedImage
import mediapipe as mp
import time
import paho.mqtt.client as mqtt
import base64
import numpy as np
client = mqtt.Client()
client.connect('enkey.bu.ac.th')
from geometry_msgs.msg import Twist
# rospy.init_node('turtlebot3_teleop')
pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
mode = ''

def on_connect(self, client, userdata, rc):
    print("MQTT Connected.")
    self.subscribe("TurtleBot/mode")

def on_message(client, userdata,msg):
    global mode
    mode = msg.payload
    print(mode)
    
def move(x, r):
#     while(True):
    twist = Twist()
    twist.linear.x = x; twist.linear.y = 0.0; twist.linear.z = 0.0
    twist.angular.x = 0.; twist.angular.y = 0.0; twist.angular.z = r
    pub.publish(twist)


def callback(data):
    newFile = open("img_raw.raw", "wb")
    newFile.write(data.data)


def listener():
    print('thread')
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('camera/color/image_raw/compressed',
                     CompressedImage, callback)
    rospy.spin()


def keepwalk():
    t_end = time.time() + 2
    while time.time() < t_end:
        move(0.3, 0.0)


def image_to_bts(frame):
    _, bts = cv2.imencode('.webp', frame)
    bts = bts.tostring()
    return bts

def bts_to_img(bts):
    buff = np.fromstring(bts, np.uint8)
    buff = buff.reshape(1, -1)
    img = cv2.imdecode(buff, cv2.IMREAD_COLOR)
    return img
def stream(cap):
    image = cap.read()
    string = image_to_bts(image)
    client.publish('TurtleBot/stream',string)

def followed_me():
    mpPose = mp.solutions.pose
    pose = mpPose.Pose()
    mpDraw = mp.solutions.drawing_utils
    keep_do = 0
    x = threading.Thread(target=keepwalk)
    while (True):
        try:
            im = cv2.imread('img_raw.raw')
            results = pose.process(im)
            if results.pose_landmarks:
                mpDraw.draw_landmarks(
                    im, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
                for id, lm in enumerate(results.pose_landmarks.landmark):
                    h, w, c = im.shape
                    cx, cy = int(lm.x*w), int(lm.y*h)
                    wc = ((w/2)-cx)
                    hc = ((h/2)-cy)
                    if (wc > 200):
                        print('left')
                        move(0.0,0.3)
                    elif (wc < -100):
                        print('right')
                        move(0.0,-0.3)
                    else:
                        print('middle')
                        move(0.5,0.0)
                        keep_do = 1
                        
            else:
                move(0.0,0.0)
                if keep_do== 1 :
                    x.start()
                    break
            # Display the resulting frame
            stream(im)
            # cv2.imshow('black and white', im)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
        except:
            pass
    cv2.destroyAllWindows()
def move_online(self, userdata, rc,msg):
    print("MQTT Connected.")
    self.subscribe("TurtleBot/move")
    while (True):
        key = msg.payload
        if key == 'w':
            move(move(0.5,0.0))
        elif key == 'a':
            move(0.0,0.3)
        elif key == 'd':
            move(0.0,-0.3)
        elif key == 'x':
            move(-0.3,0.0)
        elif key == 'q':
            break
        else:
           move(0.0,0.0) 
if __name__ == '__main__':
    status = ''
    while(True):
        if mode == 'follow' and status != 'follow':
            status = 'follow'
            threading.Thread(target=followed_me).start()
            listener()
        elif mode == 'tele' and status != 'tele':
            threading.Thread(target=move_online).start()
        elif mode == 'emer':
            threading.Thread(target=followed_me).terminate()
            threading.Thread(target=move_online).terminate()
            status = ''
