import cv2
import numpy

cam = cv2.VideoCapture(0)
try:
    while True:
        b, img = cam.read()
        if b:
            cv2.imshow("Window",img)
        else:
            print("Pucked")
            break
        flag = cv2.waitKey(1) & 0xFF
        if flag==ord('q'):
            break
finally:
    cv2.destroyAllWindows()
    cam.release()
