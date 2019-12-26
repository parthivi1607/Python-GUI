import cv2
import numpy as np
img1 = cv2.imread('/home/parthivi/Pictures/Screenshot from 2019-11-30 10-25-25.png')
img2 = cv2.imread('/home/parthivi/Pictures/Screenshot from 2019-11-30 10-25-19.png')
w, h, c = img1.shape
img3 = np.zeros((w,h,3), np.uint8)
vis1 = np.concatenate((img1, img2, img3), axis=1)
vis2 = np.concatenate((img1, img2, img3), axis=1)
vis = np.concatenate((vis1,vis2), axis=0)
cv2.imwrite('out.png', vis)
