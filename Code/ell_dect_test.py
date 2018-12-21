import cv2
import numpy as np
import math

# 守夜人宣言：
# 长夜将至，我从今开始守望，至死方休。
# 我将不娶妻，不封地，不生子。
# 我将不戴王冠，不争荣宠。
# 我将尽忠职守，生死于斯。
# 我是黑暗中的利剑，长城上的守卫。
# 抵御寒冷的烈焰，破晓时分的光线，唤醒眠者的号角，守护王国的坚盾。
# 我将生命与荣耀献给守夜人，今夜如此，夜夜皆然。

WIDETH = 1280
HEIGHT = 720

error_alpha = 0.5
radius_alpha = 0.5
max_radius = 120
min_radius = 10

method_num = 0
point_list = []
lpoint_list = []
choose_point_list = []

camera_matrix = np.array(([693.2, 0, 666.8], # 内参矩阵
                          [0, 693.4, 347.7],
                          [0, 0, 1]), dtype=np.double)
dist_coefs = np.array([-0.050791, 0.217163, 0.0000878, -0.000388, -0.246122], dtype=np.double) # k1 k2 p1 p2 k3
object_3D_points = np.array(([], []), dtype=np.double)  # 3D 物理坐标

image_2D_points = np.array(([0, 32.29], [35, 0], [85, 0], [120, 32.29]), dtype=np.double)   # 图像坐标点

#  坐标构建如下：
#  ---2--3--------->X
#  1        4
#  |
#  |
#  V


class Point:
    def __init__(self, x_param, y_param, num):
        self.x = x_param
        self.y = y_param
        self.n = num

# 使用matchShape进行椭圆筛选，效果不太理想
# def checkEllipse(contours, cen_x, cen_y, a, b, theta, ratio = RATIO):
#     ellipse_point = []
#     a_2 = pow(a, 2)
#     b_2 = pow(b, 2)
#     angle = (theta * math.pi) / 180 # 角度单位转换成弧度单位
#
#     for i in range(0, 2*a):
#         x = -a + i
#         y_left = b * math.sqrt(1 - pow(x, 2)/a_2)
#
#         rotate_x = math.cos(angle) * x - math.sin(angle) * y_left
#         rotate_y = math.sin(angle) * x + math.cos(angle) * y_left
#
#         rotate_x += cen_x
#         rotate_y += cen_y
#         ellipse_point.append([rotate_x, rotate_y])
#
#     for j in range(0, 2*a):
#         x = a - j
#         y_right = -b * math.sqrt(1 - pow(x, 2)/a_2)
#
#         rotate_x = math.cos(angle) * x - math.sin(angle) * y_left
#         rotate_y = math.sin(angle) * x + math.cos(angle) * y_left
#
#         rotate_x += cen_x
#         rotate_y += cen_y
#         ellipse_point.append([rotate_x, rotate_y])
#
#     ell_point = np.array(ellipse_point, dtype=int) # list转array
#
#     retval = cv2.matchShapes(ell_point, contours, cv2.CONTOURS_MATCH_I1, 0) # 0 表示完全相同
#     print(retval)
#     if retval < ratio:
#         return True
#     else:
#         return False


#------筛选椭圆函数，待修正------#
def isEllipse(img, x, y, a, b): # 函数功能：稳定完整的识别出靶标的椭圆
    # 越界pass
    if x + a+3 > WIDETH or y + a+3 > HEIGHT:
        return False
    if x - a <0 or y - a <0:
        return False
    # 框内有黑pass
    for i in range(0, b-1):
        if img[y, x + i] == 0 or img[y, x - i] == 0:
            return False
        if img[y - i, x] == 0 or img[y + i, x] == 0:
            return False
    # 框外一点儿有白色pass
    for m in range(a+1, a+3):
        if img[y, x + m] == 255 or img[y, x - m] == 255:
            return False
        if img[y - m, x] == 255 or img[y + m,x] == 255:
            return False
    return True


# -------对符合的椭圆重排序-------#
def locatePoint(p_list, lp_list, radius): # 函数功能：稳定完整的实现靶标定位
    temp = []
    for i in range(0, len(p_list)):  # 复制p_list给temp
        addPoint(p_list, temp, i, i+1)
    #                   1 4
    #   标准位置定义:   7     8
    #                   2 5
    #                   3 6

    #-----筛选出中间6点位置-----#
    Error = radius * error_alpha  # 用距离圆心占半径的百分比评估误差
    num = 0
    for i in range(0, len(p_list)):
        for j in range(i+1, len(p_list)):
            med_x = (p_list[i].x + p_list[j].x) / 2
            med_y = (p_list[i].y + p_list[j].y) / 2

            for m in range(0, len(p_list)):
                if m == i or m == j:
                    continue
                # 误差评估，计算距离
                error = math.sqrt(pow(med_x - p_list[m].x, 2) + pow(med_y - p_list[m].y, 2))
                if error < Error:
                    addPoint(p_list, lp_list, i, num+1)     #  1  4
                    addPoint(p_list, lp_list, m, num+2)     #  2  5
                    addPoint(p_list, lp_list, j, num+3)     #  3  6
                    #print(i+1, m+1, j+1)
                    num += 3

                    temp[i].n = -1  # -1说明已经选定
                    temp[m].n = -1
                    temp[j].n = -1
    #-----筛选6点完毕------#

    #-----确定7\8点------#
    if len(lp_list) != 6:
        pass
    else:
        for p in range(0, len(temp)):
            if temp[p].n == -1:
                continue
            if distance(p_list, lp_list, p, 2) > 8*radius :#这里有bug,检测到了未必只有8个，如果判断椭圆不够准确，这里会超过8。要根据距离进一步删选
                continue
            else:
                num += 1
                addPoint(p_list, lp_list, p, num)   # 7 和 8 添加进数组
            #lpoint_list.append(Point(p_list[p].x, p_list[p].y, num)) #先添加进list

    #至此，lpoint_list已经实现了对p_list元素的重排序

    if len(lp_list) < 8:
        pass
    else:
        cen_78_y = (lp_list[6].y + lp_list[7].y)/2   # 7 和 8 两点的中点的纵坐标
        cen_25_y = (lp_list[1].y + lp_list[4].y)/2   # 2 和 5 两点的中点的纵坐标

        if cen_78_y < cen_25_y and lp_list[6].x > lp_list[7].x: # 图像是正的
            swapPoint(lp_list, 6, 7)    # 7\8点交换
        if cen_78_y > cen_25_y and lp_list[6].x < lp_list[7].x: # 图像是倒的
            swapPoint(lp_list, 6, 7)    # 7\8点交换
    #-----2点位置确定完毕------#


        #-----定位方案待选------#
        #把点7定位为1，点8为定位为4
        addPoint(lp_list, choose_point_list, 6, 1)
        addPoint(lp_list, choose_point_list, 7, 4)

        #----- 定位方案一 ------#
        #           2  3
        #         1      4
        #           0  0
        #           0  0
        if method_num == 1:
            if cen_78_y < cen_25_y: # 图像是正的
                if distance(lp_list, lp_list, 2, 6) > distance(lp_list, lp_list, 5, 6): #待选点是点3和点6
                    swapPoint(lp_list, 2, 5)
                addPoint(lp_list, choose_point_list, 2, 2)
                addPoint(lp_list, choose_point_list, 5, 3)


            if cen_78_y > cen_25_y: # 图像是倒的
                if distance(lp_list, lp_list, 0, 6) > distance(lp_list, lp_list, 3, 6): #待选点是点1和点4
                    swapPoint(lp_list, 0, 3)
                addPoint(lp_list, choose_point_list, 0, 2)
                addPoint(lp_list, choose_point_list, 3, 3)

        #------ 定位方案二 ------#
        #用7\8点确定最中间2点，最终决定选取中间4点作为参考点，如下图：
        #          0  0
        #        1      4
        #          2  3
        #          0  0
        #-----问题:点距离太近,可能导致解算误差较大-------#
        if method_num == 2:
            if distance(lpoint_list, lpoint_list, 1, 6) > distance(lpoint_list, lpoint_list, 4, 6): #待选点是点2和点5
                swapPoint(lpoint_list, 1, 4)
            addPoint(lpoint_list, choose_point_list, 1, 2)
            addPoint(lpoint_list, choose_point_list, 4, 3)

        #----- 定位方案三 ----#
        #           0  0
        #         1      4
        #           0  0
        #           2  3
        #----- 问题:2、3点的位置过低，减小测距有效区间
        if method_num == 3:
            if cen_78_y < cen_25_y: # 图像是正的
                if distance(lpoint_list, lpoint_list, 0, 6) > distance(lpoint_list, lpoint_list, 3, 6): #带选点是点1和点4
                    swapPoint(lpoint_list, 0, 3)
                addPoint(lpoint_list, choose_point_list, 0, 2)
                addPoint(lpoint_list, choose_point_list, 3, 3)

            if cen_78_y > cen_25_y: # 图像是倒的
                if distance(lpoint_list, lpoint_list, 2, 6) > distance(lpoint_list, lpoint_list, 5, 6): #待选点是点3和点6
                    swapPoint(lpoint_list, 2, 5)
                addPoint(lpoint_list, choose_point_list, 2, 2)
                addPoint(lpoint_list, choose_point_list, 5, 3)



        #------排序完毕------#


def drawCenters(p_list, img):
    for i in range(0, len(p_list)):
        for j in range(i, len(p_list)):
            center_x = (p_list[i].x + p_list[j].x)/2
            center_y = (p_list[i].y + p_list[j].y)/2

            center_x_int = int(np.around(center_x))
            center_y_int = int(np.around(center_y))

            #cv2.circle(img, (center_x_int, center_y_int), 4, (0, 255, 0), -1)
            #cv2.imwrite('D:/img/c18.jpg', img)

def distance(list_1, list_2, i, j): # list_1第i个索引点和list_2第j个索引点的距离
    if i > len(list_1) or j > len(list_2):
        return -1
    dis = math.sqrt(pow(list_1[i].x - list_2[j].x, 2) + pow(list_1[i].y - list_2[j].y, 2))
    return dis

def swapPoint(p_list, i, j): # 交换list中第i个索引和第j个索引数据的位置、索引
    p_list[i].n = j+1
    p_list[j].n = i+1
    p_list[i], p_list[j] = p_list[j], p_list[i]

def addPoint(src_list, new_list, i, n): #将src_list中的第i个索引的数据添加进new_list，且num为n
    p_new = Point(src_list[i].x, src_list[i].y, n)
    new_list.append(p_new)


# def main():

cap = cv2.VideoCapture(1)

if (cap.isOpened() == False):
    print("Failed to open the camera...")

else:
    method_num = 1
    ret = cap.set(3, WIDETH) # 设置显示尺寸 1280*720
    ret = cap.set(4, HEIGHT)
    k = 0
    while(True):
        ret, frame = cap.read()
        ret, img = cap.read()
        ret, img2 = cap.read()

        #-----基础图形处理-----#
        f_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        f_bulr = cv2.GaussianBlur(f_gray, (5, 5), 0)

        ret,f_thresh = cv2.threshold(f_bulr, 127, 255, cv2.THRESH_BINARY_INV)  # 阈值127，变成255
        #cv2.imshow("thresh", f_thresh)

        f_can = cv2.Canny(f_thresh, 50, 150, 3)
        #cv2.imshow('canny', f_can)
        #-----结束-----#

        #-----一帧椭圆检测-------#
        image, contours, hierarchy = cv2.findContours(f_can, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        count =0 # 用来计数
        sum = 0
        for cnt in contours:
            if len(cnt) > 4: # 点数超过5才能拟合椭圆
                ell = cv2.fitEllipse(cnt)

                b_double = ell[1][0] #拟合的矩阵宽，即短半轴2倍
                a_double = ell[1][1] #拟合的矩阵长，即长半轴2倍

                #-----椭圆基本筛选-----#
                if a_double > max_radius or b_double > max_radius:
                    continue
                if a_double < min_radius or b_double < min_radius:
                    continue
                if a_double < b_double * radius_alpha or b_double < a_double * radius_alpha:
                    continue
                # -----结束-----#

                # 开始对选定的进行处理
                cen_x = int(np.around(ell[0][0]))
                cen_y = int(np.around(ell[0][1]))
                a = int(np.around(a_double/2))
                b = int(np.around(b_double/2))
                theta = ell[2] # 旋转角度

                if  isEllipse(f_thresh, cen_x, cen_y, a, b):
                    #if  checkEllipse(cnt, cen_x, cen_y, a, b, theta):
                    #-----添加进组并计数、标记-----#
                    count += 1
                    sum = sum + b # sum是所有短半轴的集合
                    p_new = Point(cen_x, cen_y, count)
                    point_list.append(p_new)

                    # font = cv2.FONT_HERSHEY_SIMPLEX # 数字标记
                    # cv2.putText(frame, str(count), (cen_x, cen_y), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
                    #-----结束------#


                    #point_list.append(p_new)
                    cv2.ellipse(frame, ell, (0, 0, 255), 2)
                    cv2.circle(frame, (cen_x, cen_y), 2, (0, 0, 255), -1)

        #----一帧椭圆检测结束-----#


        #-----处理圆心坐标点集-----#
        if len(point_list) < 8:
            print('No enough ellipse in sight!')
        else:
            #-----排序测试------#
            locatePoint(point_list, lpoint_list,sum/count)
            #print(len(lpoint_list))

            for i in range(0, len(lpoint_list)):
                #print(lpoint_list[i].x, lpoint_list[i].y, lpoint_list[i].n)

                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, str(lpoint_list[i].n), (lpoint_list[i].x, lpoint_list[i].y), font, 1, (0, 255, 0), 2,
                            cv2.LINE_AA)

            for i in range(0, len(point_list)):
                #print(lpoint_list[i].x, lpoint_list[i].y, lpoint_list[i].n)

                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(img, str(point_list[i].n), (point_list[i].x, point_list[i].y), font, 1, (0, 255, 0), 2,
                            cv2.LINE_AA)

            for i in range(0, len(choose_point_list)):
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(img2, str(choose_point_list[i].n), (choose_point_list[i].x, choose_point_list[i].y), font, 1, (0, 255, 0), 2,
                            cv2.LINE_AA)
            #-----排序测试------#

        point_list = []
        lpoint_list = []
        choose_point_list = []# 结束后置空
        #------处理圆心坐标结束----#

        #cv2.imshow('ell', frame)
        #cv2.imshow('point_lis', img)
        #cv2.imshow('fresholde', f_thresh)
        cv2.imshow('locate', img2)

        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break

cv2.destroyAllWindows()
#retvel, rvev, tvec = cv2.solvePnP()
#
# if __name__ == '__main__':
#
#     main()

