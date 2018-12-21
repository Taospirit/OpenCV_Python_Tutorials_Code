import cv2
import numpy as np

img = cv2.imread("d:/img/ell.png")
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

ret, img_thresh = cv2.threshold(img_gray, 125, 255, cv2.THRESH_BINARY_INV)  # 阈值127，变成255

#img_canny = cv2.Canny(img_thresh, 50, 150, 3)

image, contours, hierarchy = cv2.findContours(img_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#print(contours)
#
# print(len(contours[0][:]))
# print(contours[0][:])

print(contours[0][0])
print(contours[0][0][0])
print(contours[0][1])
#print(contours[0][0][1])
#print(contours[0][0][2])
print(len(contours[0][:]))


for i in range(0, len(contours[0][:])):
    cv2.circle(img, (contours[0][i][0][0], contours[0][i][0][1]), 5, (0, 0, 255), -1)

#cv2.circle(img, (contours[0][0][0][0], contours[0][0][0][1]), 5, (0, 0, 255), -1)

cv2.imshow('test', img)
cv2.waitKey(0)