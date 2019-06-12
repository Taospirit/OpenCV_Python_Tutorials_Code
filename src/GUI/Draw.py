# 画图的四元素
# image: 想要绘制的图像
# color: 形状颜色，注意opencv中是BGR的排列，（255,0,0）是蓝色。
# thickness: 线条的粗细，默认是1。如果设置为-1，代表闭合填充。
# linetype: 线条的类型，8联通、抗锯齿等等。默认8联通

import numpy as np
import cv2

# Create a black image
img = np.zeros((512,512,3), np.uint8) # 长宽为512的图片，8位3通道。

cv2.line(img,(0,0),(511,511),(255,0,0),5)
#cv2.line(img，起点，终点，颜色，粗细)

cv2.rectangle(img,(382,0),(510,216),(0,255,0),3)
#cv.rectangle(img，左上角，右下角，边框颜色，边框粗细)

cv2.circle(img,(125,125),40,(0,0,255),-1)
#cv2.circle(img,圆心，半径，颜色，粗细)

cv2.ellipse(img,(256,256),(100,50),20,0,360,255,-1)
#cv2.ellipse(img,圆心，长短半轴，逆时针旋转角度，起始角度，终止角度，颜色，粗细)

pts = np.array([[10,5],[20,30],[70,20],[50,10]], np.int32)
pts = pts.reshape((-1,1,2))
cv2.polylines(img,[pts],True,(0,255,255))
#cv2.polyline(图像，多边形曲线数值，是否闭合，颜色)

font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img,'OpenCV',(10,500),font,4,(255,255,255),2,cv2.LINE_AA)
#cv2.puText(img,文字，位置，字体类型，字体大小，字体颜色，其他属性)

#所有绘图函数的返回值都是None，不能用img = cv2.line(img,...)这种写法

winname = 'example'

cv2.namedWindow(winname)
cv2.imshow(winname,img)
cv2.waitKey(0)
cv2.destroyAllWindows()