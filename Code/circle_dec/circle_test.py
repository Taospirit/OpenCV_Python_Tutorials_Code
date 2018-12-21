#霍夫圆检测
import cv2
import numpy as np

def detect_circles_demo(image):
    dst = cv2.pyrMeanShiftFiltering(image, 10, 100)   #边缘保留滤波EPF
    cimage = cv2.cvtColor(dst, cv2.COLOR_RGB2GRAY)
    circles = cv2.HoughCircles(cimage, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)
    circles = np.uint16(np.around(circles)) #把circles包含的圆心和半径的值变成整数
    for i in circles[0, : ]:
        cv2.circle(image, (i[0], i[1]), i[2], (0, 0, 255), 2)  #画圆
        cv2.circle(image, (i[0], i[1]), 2, (0, 0, 255), 2)  #画圆心
    cv2.imshow("circles", image)

cap = cv2.VideoCapture(1)

if (cap.isOpened() == False):
    print('failed to open the camera...')

else:
    while(True):
        rect, frame = cap.read()
        cv2.imshow('src', frame)
        detect_circles_demo(frame)

        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break

cv2.destroyAllWindows()