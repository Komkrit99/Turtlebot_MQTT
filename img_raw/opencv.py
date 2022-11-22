import cv2
import numpy as np

rows = 480
cols = 640

while(True):
        try:
                #fd = open('img_raw.raw')
                #f = np.fromfile(fd, dtype=np.uint8,count=rows*cols)
                #im = f.reshape((rows, cols)) #notice row, column format
                #fd.close()

                im = cv2.imread('img_raw.raw')
                cv2.imshow('', im)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
        except:
                pass
cv2.destroyAllWindows()