import cv2
import numpy as np

img = cv2.imread("D:/lena.jpg")

ball = img[100:200, 100:200]

img[50:150, 50:150] = ball

img = cv2.imshow('test', img)
cv2.waitKey(0)