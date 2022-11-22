import rospy
import threading
import cv2
from sensor_msgs.msg import CompressedImage

def callback(data):
    newFile = open('img_dept_raw.raw', "wb")
    newFile.write(data.data)

def show_distance(event, x, y, args, params):
    global point
    point = (x, y)

def listener():
    print('thread')
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('camera/color/image_raw/compressed',
                     CompressedImage, callback)
    rospy.spin()

def open_cam():
    while (True):
        try:
            im = cv2.imread('img_dept_raw.raw')
            show_distance(320,240)
            distance = im[point[1], point[0]]
            cv2.putText(im, "{}mm".format(distance), (point[0], point[1] - 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
            cv2.imshow('', im)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except:
            pass
    cv2.destroyAllWindows()

if __name__ == '__main__':
    threading.Thread(target=open_cam).start()
    listener()