import rospy
import threading
import cv2
from sensor_msgs.msg import CompressedImage
count = 0
def callback(data):
    if count == 0:
        newFile = open("img_raw.txt", "wb")
        newFile.write(data.data)
        count = 1

def listener():
    print('thread')
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('camera/color/image_raw/compressed',
                     CompressedImage, callback)

if __name__ == '__main__':
    listener()