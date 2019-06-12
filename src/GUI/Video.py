import cv2

cap = cv2.VideoCapture(0) # 0打开默认摄像头，如果是1打开其他的

if (cap.isOpened() == False): # cap.isOpened()来检测是否初始化,若打开不成功可用cap.open()
    print('failed to open the camera...')

else:
    print('the width of frame is', cap.get(3))
    print('the hight of frame is', cap.get(4))

    # cap.get(propld) 可获取视频的基础参数信息
    # 具体可查表https://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html#videocapture-get

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
    # out设置VideoWriter的存储后的参数

    k = 0
    while (True):
        ret, frame = cap.read()
        # cap.read()返回一个bool值，如果帧读取成功则为True，用来检测视频是否播放完毕

        key = cv2.waitKey(1)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('gray', gray)

        if k == 1:
            frame = cv2.flip(frame, 0)

        out.write(frame) #在视频中写入每一帧

        cv2.imshow('frame', frame)

        if key & 0xff == 9: #小玩意儿，每按一下tab键，视频颠倒一次
            if k == 1: k = 0
            else: k = 1

        if key & 0xff == 27:  # esc的ASCII码值是27
            break

cap.release()
out.release()
cv2.destroyAllWindows()