import rospy
import threading
import cv2
from sensor_msgs.msg import CompressedImage
import mediapipe as mp
import time
from geometry_msgs.msg import Twist
import paho.mqtt.client as mqtt
import base64
import numpy as np
client = mqtt.Client()

client.connect('enkey.bu.ac.th')
pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)


class followed_me:
    def __init__(self,name):
        self.name = name

    def followMe(self):
        return self._followed_me


    def _move(self,x,r):
#     while(True):
        twist = Twist()
        twist.linear.x = x; twist.linear.y = 0.0; twist.linear.z = 0.0
        twist.angular.x = 0.; twist.angular.y = 0.0; twist.angular.z = r
        pub.publish(twist)

    def _callback(self,data):
        newFile = open("img_raw.raw", "wb")
        newFile.write(data.data)


    def _listener(self):
        print('thread')
        rospy.init_node('listener', anonymous=True)
        rospy.Subscriber('camera/color/image_raw/compressed',
                        CompressedImage, self._callback)
        rospy.spin()

    def _keepwalk(self):
        t_end = time.time() + 2
        while time.time() < t_end:
            self._move(0.3,0.0)
    def _image_to_bts(self,frame):
        '''
        :param frame: WxHx3 ndarray
        '''
        _, bts = cv2.imencode('.webp', frame)
        bts = bts.tostring()
        return bts

    def _bts_to_img(self,bts):
        '''
        :param bts: results from image_to_bts
        '''
        buff = np.fromstring(bts, np.uint8)
        buff = buff.reshape(1, -1)
        img = cv2.imdecode(buff, cv2.IMREAD_COLOR)
        return img
    def _followed_me(self):
        mpPose = mp.solutions.pose
        pose = mpPose.Pose()
        mpDraw = mp.solutions.drawing_utils
        keep_do = 0
        x = threading.Thread(target=self._keepwalk)
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
                            self._move(0.0,0.3)
                        elif (wc < -100):
                            print('right')
                            self._move(0.0,-0.3)
                        else:
                            print('middle')
                            self._move(0.5,0.0)
                            keep_do = 1
                            
                else:
                    self._move(0.0,0.0)
                    if keep_do== 1 :
                        x.start()
                    keep_do = 0
                # Display the resulting frame
                self._stream(im)
                cv2.imshow('black and white', im)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            except:
                pass
        cv2.destroyAllWindows()
    def _stream(self,cap):
        while(True):
            retval, image = cap.read()
            string = self._image_to_bts(image)
            client.publish('TurtleBot/stream',string)
            
            img = self._bts_to_img(string)
            cv2.imshow('sss',img)
            key = cv2.waitKey(1)
            if key == 27:
                break
        cap.release()
        cv2.destroyAllWindows()
