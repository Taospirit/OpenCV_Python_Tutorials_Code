import cv2
import numpy as np
from matplotlib import pyplot as plt

import math
#img=cv2.imread("D:\cv.png")

cap = cv2.VideoCapture(1)

if (cap.isOpened() == False):
    print('falied...')
else:
    while(cap.isOpened()):
        rect, frame = cap.read()
        #img=cv2.blur(img,(1,1))

        #frame = cv2.medianBlur(frame, 5)

        imgray=cv2.Canny(frame,600,100,3)#Canny边缘检测，参数可更改
        #cv2.imshow("canny",imgray)

        # imgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # cv2.imshow('imgray', imgray)

        ret,thresh = cv2.threshold(imgray,127,255,cv2.THRESH_BINARY) # 阈值127，变成255
        cv2.imshow('thresh', thresh)
        #print(thresh)

        image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)#contours为轮廓集，可以计算轮廓的长度、面积等
        # if d == True:
        #     print(contours)
        #     d = not d
        for cnt in contours:
            if len(cnt)>50:
                S1=cv2.contourArea(cnt)
                ell=cv2.fitEllipse(cnt)
                S2 =math.pi*ell[1][0]*ell[1][1]
                # if (S1/S2)>0.2 :#面积比例，可以更改，根据数据集。。。
                frame = cv2.ellipse(frame, ell, (0, 255, 0), 2)
                #     print(str(S1) + "    " + str(S2)+"   "+str(ell[0][0])+"   "+str(ell[0][1]))
        cv2.imshow("0",frame)
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break

#
# img = cv2.imread("D:\ell.png")
#
# img_c=cv2.Canny(img,600,100,3)#Canny边缘检测，参数可更改
# #cv2.imshow("1",img_c)
#
# # ret,thresh = cv2.threshold(img_c,127,255,cv2.THRESH_BINARY) # 阈值127，变成255
# # cv2.imshow('thresh', thresh)
#
# image, contours, hierarchy = cv2.findContours(img_c, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)#contours为轮廓集，可以计算轮廓的长度、面积等
# #print(contours)
#
# for cnt in contours:
#     if len(cnt)>50:
#         #S1=cv2.contourArea(cnt)
#         ell=cv2.fitEllipse(cnt)
#         print(ell)
#
#         S2 =math.pi*ell[1][0]*ell[1][1]
#         # if (S1/S2)>0.2 :#面积比例，可以更改，根据数据集。。。
#         res = cv2.ellipse(img, ell, (0, 0, 255), 2)
#         #     print(str(S1) + "    " + str(S2)+"   "+str(ell[0][0])+"   "+str(ell[0][1]))
#
# cv2.imshow("res",res)
# cv2.waitKey(0)
#
# k = cv2.waitKey(1) & 0xff
# if k == 27:
#     cv2.destroyAllWindows()
