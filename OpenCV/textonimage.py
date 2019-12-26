import numpy as np
import cv2
'''
#METHOD 1
# Create a black image
img = np.zeros((512,512,3), np.uint8)

# Write some Text

font                   = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10,500)
fontScale              = 1
fontColor              = (255,255,255)
lineType               = 2
cv2.putText(img,"a",
    bottomLeftCornerOfText,
    font,
    fontScale,
    fontColor,
    lineType)

cv2.putText(img,"b",
    bottomLeftCornerOfText,
    font,
    fontScale,
    fontColor,
    lineType)

#Display the image
cv2.imshow("img",img)

#Save image
#cv2.imwrite("out.jpg", img)

cv2.waitKey(0)

#METHOD 2
# Read the image
img = cv2.imread('/home/parthivi/Pictures/Webcam/2019-05-12-113750.jpg')
# initialize counter
i = 0
while True:
    # Display the image
    cv2.imshow('a',img)
    # wait for keypress
    k = cv2.waitKey(0)
    # specify the font and draw the key using puttext
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img,chr(k),(140+i,250), font, .5,(255,255,255),2,cv2.LINE_AA)
    i+=10
    if k == ord('q'):
        break
cv2.destroyAllWindows()
'''
#METHOD 3
img = cv2.imread('/home/parthivi/Pictures/Webcam/2019-05-12-113750.jpg')

font = cv2.FONT_HERSHEY_SIMPLEX

brr=["|","'","'","'","'","!","'","'","'","'"]
k=0
for i in [1,2,3,4,5,6]:
	for j in brr:
		cv2.putText(img,j,(k,200), font, .5,(255,255,255),2,cv2.LINE_AA)
		k=k+10
cv2.putText(img,brr[0],(k,200), font, .5,(255,255,255),2,cv2.LINE_AA)

cv2.imshow('a',img)

cv2.waitKey(0)
