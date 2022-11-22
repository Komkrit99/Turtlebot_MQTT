import rospy
import threading
import cv2
from sensor_msgs.msg import CompressedImage

def callback(data):
    newFile = open("img_raw.raw", "wb")
    newFile.write(data.data)


def listener():
    print('thread')
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('camera/color/image_raw/compressed',
                     CompressedImage, callback)
    rospy.spin()

def open_cam():
    while (True):
        try:
            im = cv2.imread('img_raw.raw')
            cv2.imshow('', im)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except:
            pass
    cv2.destroyAllWindows()

if __name__ == '__main__':
    threading.Thread(target=open_cam).start()
    listener()