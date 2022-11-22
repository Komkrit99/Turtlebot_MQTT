from ast import arg
import cv2
import mediapipe as mp
import time
import mouse
import threading
cap = cv2.VideoCapture(0)
import pyautogui
import paho.mqtt.client as mqtt
import datetime
import sys
host = "enkey.bu.ac.th"
port = 1883
client = mqtt.Client()
client.connect(host)
mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False,
                      max_num_hands=2,
                      min_detection_confidence=0.5,
                      min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

def mouse_move(x,y):
    #time.sleep(0.2)
    pyautogui.moveTo(x,y)

point_start = []
hand_start = []
w = 900
h = 1600

def condition(x,y):
    if(x <= 200 and x >= 0 and y <= 200 and y >= 0 ):
        return 'a'
    elif(x <= 400 and x >= 201 and y <= 200 and y >= 0 ):
        return 'w'
    elif(x >= 401 and y <= 200 and y >= 0 ):
        return 'd'
    elif(x <= 400 and x >= 201 and y >= 200 ):
        return 's'
    else:
        return 'q'
a = datetime.datetime.now()
while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imgRGB = cv2.flip(imgRGB,1)
    results = hands.process(imgRGB)
    
    #mouse_pos = mouse.get_position()
    q = 0
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            list_position = []
            q += 1
            for id, lm in enumerate(handLms.landmark):
                #print(id,lm)
                h, w, c = img.shape
                cx, cy = int(lm.x *w), int(lm.y*h)
                #if id ==0:
                list_position.append([cx,cy])
                if id == 8 and q == 1:
                    cv2.circle(img, (cx,cy), 3, (255,0,255), cv2.FILLED)
        #print(abs(list_position[0][1] - list_position[8][1]))
        if(abs(list_position[0][1] - list_position[8][1])>100):
            if(point_start == []):
                point_start = mouse.get_position()
                hand_start = list_position[8]
                print("save first")
                pyautogui.moveTo(500,500)
            else:
                #print("-"*8)
                #print(point_start)
                #print(hand_start)
                #print(list_position[8])
                new_position = (((list_position[8][0]*point_start[0])/hand_start[0]),((list_position[8][1]*point_start[1])/hand_start[1]))
                new_position = [int(new_position[0]),int(new_position[1])]
                #print(condition(new_position[0],new_position[1]) , new_position)
                b = datetime.datetime.now()
                delta = b - a
                if((delta.total_seconds() * 1000 ) > 500):
                    a = datetime.datetime.now()
                    #print(list_position[8])
                    print(condition(list_position[8][0],list_position[8][1]))
                    client.publish("Turtlebot3/MQTT",condition(list_position[8][0],list_position[8][1]))
                    #client.publish("Turtlebot3/MQTT4",condition(new_position[0],new_position[1]))
                    #client.publish("Turtlebot3/MQTT3",condition(new_position[0],new_position[1]))
                #new_position[0] = new_position[0] if(new_position[0]>int(user32.GetSystemMetrics(0))) else int(user32.GetSystemMetrics(0))
                #new_position[1] = new_position[1] if(new_position[1]>int(user32.GetSystemMetrics(1))) else int(user32.GetSystemMetrics(1))
                #print(new_position)
                
                #threading.Thread(target=mouse_move,args=(int(new_position[0]+new_position[0]*0.15),int(new_position[1]+new_position[1]*0.15))).start()
                #threading.Thread(target=mouse_move,args=(10,10)).start()
                #print("-"*8)
        else:
            hand_start = []
            point_start = []

            #mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
    else:
        save_position = []
    
    img = cv2.flip(img,1)
    cv2.imshow("Image", img)
    cv2.waitKey(1)