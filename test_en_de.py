import base64
import numpy as np
import cv2

img = cv2.imread('test.jpg')
_, im_arr = cv2.imencode('.jpg', img)  # im_arr: image in Numpy one-dim array format.
im_bytes = im_arr.tobytes()
im_b64 = base64.b64encode(im_bytes)
print(im_b64)
im_bytes = base64.b64decode(im_b64)
im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
print(img)
while(True):
    cv2.imshow('aaa',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
