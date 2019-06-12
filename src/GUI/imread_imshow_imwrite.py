import cv2

#cv2.namedWindow('src', 0)
#cv2.namedWindow('gray', 0)
cv2.resizeWindow('src', 512, 512)#限制窗口大小，原图长宽均512像素
cv2.resizeWindow('gray', 512, 512)
cv2.moveWindow('src', 200, 100)
cv2.moveWindow('gray', 800, 100)

# WINDOW_AUTOSIZE 默认，固定尺寸
img_src = cv2.imread('D:\lena.jpg', cv2.WINDOW_AUTOSIZE)
# change BGR to gray
img_gray = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)

cv2.imshow('src', img_src)
cv2.imshow('gray', img_gray)
# 获取键盘输入的ASCII码
k = cv2.waitKey(0)

if k == 27: # wait for ESC to exit
    cv2.destroyAllWindows()
    print('ESC has been pressed.')
elif k == ord('s'):
    cv2.imwrite('lena_gray.jpg', img_gray)
    cv2.destroyWindow('gray')
    print('The gray image has been saved in local path')





