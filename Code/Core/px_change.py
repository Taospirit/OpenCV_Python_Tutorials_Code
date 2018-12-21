import cv2
import numpy as np

img = cv2.imread("D:/lena.jpg")

px = img[100,100]
print(px)
blue = img[100,100,0]
print(blue)

img[50,50] = [255,255,255] # 改变第51行、第52列的元素BGR值
img[50,:] = [255,255,255] # 改变低51行的元素BGR值


#使用numpy的array.item()和array.itemset()来处理
print(img.item(100,100,0)) # 直接得到第100行、第100列像素的B值
img.itemset((100,100,2),100) #用itemset修改
print(img.item(100,100,2))


# 获得图像的属性：行、列、通道、图像数据类型
print(img.shape) # 获取图像的形状：行数、列数、通道数。当是灰度图时只有前2个参数
print(img.size, img.dtype) # img.size()返回图像的像素数目,img.dtype()返回数据类型，


cv2.imshow('image',img)

k = cv2.waitKey(0) & 0xff
if k == 27:
    cv2.destroyAllWindows()