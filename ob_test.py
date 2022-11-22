from sqlite3 import Row
import tensorflow_hub as hub
import cv2
import numpy
import csv
import tensorflow as tf
import pandas as pd
import pyrealsense2
from realsense_depth import *
# Carregar modelos
detector = hub.load("https://tfhub.dev/tensorflow/efficientdet/lite2/detection/1")
labels = pd.read_csv('labels.csv',sep=';',index_col='ID')
labels = labels['OBJECT (2017 REL.)']

cap = cv2.VideoCapture(0)
dc = DepthCamera()

width = 512
height = 512

while(True):
    #Capture frame-by-frame
    ret, frame = cap.read()
    ret2, depth_frame, color_frame = dc.get_frame()
    
    #Resize to respect the input_shape
    inp = cv2.resize(frame, (width , height ))

    #Convert img to RGB
    rgb = cv2.cvtColor(inp, cv2.COLOR_BGR2RGB)

    #Is optional but i recommend (float convertion and convert img to tensor image)
    rgb_tensor = tf.convert_to_tensor(rgb, dtype=tf.uint8)

    #Add dims to rgb_tensor
    rgb_tensor = tf.expand_dims(rgb_tensor , 0)
    
    boxes, scores, classes, num_detections = detector(rgb_tensor)
    
    pred_labels = classes.numpy().astype('int')[0]
    
    pred_labels = [labels[i] for i in pred_labels]
    pred_boxes = boxes.numpy()[0].astype('int')
    pred_scores = scores.numpy()[0]
   
   #loop throughout the detections and place a box around it  
    for score, (ymin,xmin,ymax,xmax), label in zip(pred_scores, pred_boxes, pred_labels):
        if score < 0.5:
            continue
        point = [round((xmax+xmax)/2),round((ymax+ymax)/2)]
        distance = depth_frame[point[1], point[0]]
        score_txt = f'{100 * round(score,0)}'
        # img_boxes = cv2.rectangle(inp,(xmin, ymax),(xmax, ymin),(0,255,0),2)
        img_boxes = cv2.line(inp, (xmin, ymax), (xmin+20, ymax), (0,0,255), 5)
        img_boxes = cv2.line(img_boxes, (xmin, ymax), (xmin, ymax-20), (0,0,255), 5)      
        img_boxes = cv2.line(img_boxes, (xmin, ymin), (xmin+20, ymin), (0,0,255), 5)      
        img_boxes = cv2.line(img_boxes, (xmin, ymin), (xmin, ymin+20), (0,0,255), 5)      
        img_boxes = cv2.line(img_boxes, (xmax, ymax), (xmax-20, ymax), (0,0,255), 5)      
        img_boxes = cv2.line(img_boxes, (xmax, ymax), (xmax, ymax-20), (0,0,255), 5)      
        img_boxes = cv2.line(img_boxes, (xmax, ymin), (xmax-20, ymin), (0,0,255), 5)      
        img_boxes = cv2.line(img_boxes, (xmax, ymin), (xmax, ymin+20), (0,0,255), 5)      
        cv2.putText(img_boxes, "{}mm".format(distance), (point[0], point[1] - 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img_boxes,label,(xmin, ymax-10), font, 0.5, (255,0,0), 2, cv2.LINE_AA)
        cv2.putText(img_boxes,score_txt,(xmax, ymax-10), font, 0.5, (255,0,0), 2, cv2.LINE_AA)



    #Display the resulting frame
    cv2.imshow('black and white',img_boxes)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()