import cv2
import base64
import paho.mqtt.client as mqtt
import base64
import numpy as np

client = mqtt.Client()

client.connect('enkey.bu.ac.th')

def image_to_bts(frame):
    '''
    :param frame: WxHx3 ndarray
    '''
    _, bts = cv2.imencode('.webp', frame)
    bts = bts.tostring()
    return bts

def bts_to_img(bts):
    '''
    :param bts: results from image_to_bts
    '''
    buff = np.fromstring(bts, np.uint8)
    buff = buff.reshape(1, -1)
    img = cv2.imdecode(buff, cv2.IMREAD_COLOR)
    return img

cap = cv2.VideoCapture(0)
while(True):
    retval, image = cap.read()
    string = image_to_bts(image)
    client.publish('TurtleBot/stream',string)
    
    img = bts_to_img(string)
    cv2.imshow('sss',img)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()