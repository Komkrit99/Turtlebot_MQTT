import rospy
import threading
import paho.mqtt.client as mqtt
import cv2
client = mqtt.Client()

def callback(data):
    newFile = open("img_raw.raw", "wb")
    newFile.write(data.data)


def listener():
    print('thread')
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('camera/color/image_raw/compressed',
                     CompressedImage, callback)
    rospy.spin()

def pub_data():
    while(True):
        string = cv2.imread('img_raw.raw')
        client.publish('TurtleBot/stream',string)


if __name__ == '__main__':
    threading.Thread(target=pub_data).start()
    listener()