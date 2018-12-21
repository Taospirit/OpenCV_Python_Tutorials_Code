import cv2
import numpy as np

planets = cv2.imread('D:\cv.png')
img_around = planets.copy()
# 灰度处理
gray_img = cv2.cvtColor(planets, cv2.COLOR_BGR2GRAY)
# medianBlur 平滑（模糊）处理
img = cv2.medianBlur(gray_img, 5)
#  圆检测
circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 100, param1=100, param2=30, minRadius=60, maxRadius=80)
# print(circles)
#  转化整数
circles_1 = np.uint16(np.around(circles))
#print(circles_1)
print(circles.shape)
print(circles[0,:])

for i in circles[0, :]:
    #  勾画圆形，planets图像、(i[0],i[1])圆心坐标，i[2]是半径
    cv2.circle(planets, (i[0], i[1]), i[2], (0, 255, 0), 1)
    #  勾画圆心，圆心实质也是一个半径为2的圆形
    cv2.circle(planets,(i[0],i[1]),2,(0,0,255),2)

for i in circles_1[0,:]:
    cv2.circle(img_around, (i[0], i[1]), i[2], (0, 0, 255), 1)
    cv2.circle(img_around,(i[0],i[1]),2,(0,0,255),2)
#  显示图像

#cv2.imshow("mypic", cimg)
cv2.imshow("on_around", planets)
cv2.imshow('around',img_around)

cv2.waitKey()
cv2.destroyAllWindows()
