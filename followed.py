import rospy
import threading
import cv2
from sensor_msgs.msg import CompressedImage
import mediapipe as mp
import time

from geometry_msgs.msg import Twist
# rospy.init_node('turtlebot3_teleop')
pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)


def move(x,r):
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
        move(0.3,0.0)

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
                keep_do = 0
            # Display the resulting frame
            cv2.imshow('black and white', im)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except:
            pass
    cv2.destroyAllWindows()

if __name__ == '__main__':
    threading.Thread(target=followed_me).start()
    listener()