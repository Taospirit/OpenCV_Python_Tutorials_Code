import cv2
import numpy as np

img = cv2.imread('D:\lena.jpg')

# 直接用split函数分离通道，比较耗时
b,g,r = cv2.split(img)
# 直接用merge函数合并
img = cv2.merge((b,g,r))

b = img[:, :, 0]  #也可以用遍历的方式,返回第一个通道。推荐用

# img[:, :, 2] = 0 # 将红通道的值直接全部值零

cv2.imshow('img_b',img[:, :, 0])
cv2.imshow('img_g',img[:, :, 1])
cv2.imshow('img_r',img[:, :, 2])

cv2.waitKey(0)