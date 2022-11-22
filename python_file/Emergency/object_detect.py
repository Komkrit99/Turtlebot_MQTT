import cv2
from matplotlib import pyplot as plt
cap = cv2.VideoCapture(0)
while True:
    success, img = cap.read()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    cv2.imshow("Image", gray)
    if cv2.waitKey(1)==113:
            break