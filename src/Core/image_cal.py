import cv2
import numpy as np

# 加法运算，opencv中的加法是饱和运算
x = np.uint8([250])
y = np.uint8([10])
print(cv2.add(x,y)) # 250+10=260 => 255,推荐使用

print(x+y) # numpy中的加法， 250+10 = 260 % 256 => 4


# 图像混合，本质上就是加法，要分别考虑权重
img1 = cv2.imread('opencv_logo.jpg')
img2 = cv2.imread('opencv_logo.jpg')
# 要求图像的大小类型必须一致，否则报错
dst = cv2.addWeighted(img1, 0.7, img2, 0.3, 0) # dst = α · img1 + β · img2 + γ

cv2.imshow('dst', dst)

cv2.waitKey(0)
cv2.destroyAllWindows()


