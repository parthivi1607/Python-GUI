import cv2
import numpy

cam = cv2.VideoCapture('rtsp://192.168.1.10/user=admin&password=&channel=1&stream=0.sdp?real_stream--rtp-caching=1')
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
