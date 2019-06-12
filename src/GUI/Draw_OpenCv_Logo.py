import cv2
import numpy as np

img = np.zeros((512, 512, 3), np.uint8)
cv2.rectangle(img, (0,0), (511,511),(255,255,255),-1)#画一个白布

cv2.circle(img, (256, 100), 70, (0, 0, 255), -1)
cv2.circle(img, (255,100), 30, (255,255,255), -1)
pts = np.array([[256, 100],[299, 174],[213, 171]], np.int32)
pts = pts.reshape((-1,1,2))
cv2.fillPoly(img,[pts],(255,255,255)) # 多边形填充


cv2.circle(img, (176, 238), 70, (0, 255, 0), -1)
cv2.circle(img, (176,238), 30, (255,255,255), -1)
pts = np.array([[176, 238],[219, 164],[262, 238]], np.int32)
pts = pts.reshape((-1,1,2))
cv2.fillPoly(img,[pts],(255,255,255))


cv2.circle(img, (336, 238), 70, (255, 0, 0), -1)
cv2.circle(img, (336, 238), 30, (255,255,255), -1)
pts = np.array([[336, 238],[379, 164],[293, 164]], np.int32)
pts = pts.reshape((-1,1,2))
cv2.fillPoly(img,[pts],(255,255,255))

font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img,'OpenCV',(10,450),font,4,(0,0,0),2,cv2.LINE_AA)

cv2.imshow('OpenCV', img)

cv2.waitKey(0)
cv2.destroyAllWindows()