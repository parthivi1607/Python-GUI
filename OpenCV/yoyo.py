import numpy
import cv2

img = numpy.zeros((512,1024,3), numpy.uint8)

font                   = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10,500)
fontScale              = 1
fontColor              = (255,255,255)
lineType               = 2

brr = numpy.chararray((1,55))
brr[:] = '.';
brr[:,::5] = '!';
brr[:,::10] = '|';
print(brr)

arr=["|","'","'","'","'","!","'","'","'","'"]

k=0
for i in [1,2,3,4,5,6]:
    for j in arr:
        cv2.putText(img,j,(k,200), font, .5,(255,255,255),2,cv2.LINE_AA)
        k=k+10
cv2.putText(img,arr[0],(k,200), font, .5,(255,255,255),2,cv2.LINE_AA)

cv2.imshow("img",img)
cv2.waitKey(0)
