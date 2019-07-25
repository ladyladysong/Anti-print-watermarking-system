# -*- coding: utf-8 -*-
from PIL import Image,ImageDraw,ImageFont,ImageFilter
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import cv2
import math
import os
import binascii  


dst_dir = "./result4/"
min_val = 30
min_range = 20


def cal_black(im):
    count = 0
    white = 0
    x,y = im.shape
    for j in range(1,y):
        for i in range(1,x):
            if im[i,j]==0:
                count +=1
            else:
                white += 1
    return count,white


# 记录像素段的位置 返回列表（起点，终点）
def projection_line(array_vals, minimun_val, minimun_range):
    start_i = None
    end_i = None
    line_ranges = []
    '''
    for index, item in enumerate(list1):
    print index, item  
    '''
    for i, val in enumerate(array_vals):
        # 黑色像素起点
        if val > minimun_val and start_i is None:
            start_i = i
        # 黑色像素区间
        elif val > minimun_val and start_i is not None:
            pass
        # 黑色像素终点
        elif val < minimun_val and start_i is not None:
            # 黑色像素的长度
            if i - start_i >= minimun_range:
                end_i = i
                #print(end_i - start_i)
                # 记录此段黑色像素起始点
                line_ranges.append((start_i, end_i))
                start_i = None
                end_i = None
        # 白色像素区域
        elif val < minimun_val and start_i is None:
            pass
        else:
            raise ValueError("cannot parse this case...")
    return line_ranges

def cutImage(img,line_ranges,vertical_line_ranges2d):
    global K
    count = 0   #所有的字符
    count1 = 0
    #NA,NB 字符图像个数
    for i, line_range in enumerate(line_ranges):
        for vertical_range in vertical_line_ranges2d[i]:
            x = vertical_range[0]
            y = line_range[0]
            w = vertical_range[1] - x
            h = line_range[1] - y
            pt1 = (x, y)
            pt2 = (x + w, y + h)
            count += 1
            img1 = img[y:line_range[1], x:vertical_range[1]]  
            black,white=cal_black(img1)
            if white*4 > black:
                count1 += 1
                #cv2.rectangle(img, pt1, pt2, (255,0,0),2)   
            #cv2.imwrite(dst_dir + str(count) +'.jpg',img1)
    #cv2.imwrite('char_trangle.jpg',img)
    #cv2.imshow('re',img)
    #cv2.waitKey(0)
    print "count = ",count
    print "count1 = ",count1




#水平方向上 矩阵中每行元素相加
def pic(thresh1):

    horizontal_sum = np.sum(thresh1, axis=1)
    line_ranges = projection_line(horizontal_sum, min_val, min_range)
    line_rectangle = np.copy(thresh1)
    # 记录每行字符串的上下左右坐标
    for i, line_range in enumerate(line_ranges):
        x = 0
        y = line_range[0]
        w = line_rectangle.shape[1]       #width
        h = line_range[1] - y               #height
        pt1 = (x, y)
        pt2 = (x + w, y + h)                #确定每行字符串的起点坐标pt1和终点坐标pt2

        # 通过对角线确定矩形——长条矩形width不变
        #cv2.rectangle(line_rectangle, pt1, pt2, 255)
    #cv2.imshow('re',line_rectangle)
    #cv2.waitKey(0)

    # 根据line_ranges[]切分每行，再对每行进行每个字符的切分
    vertical_line_ranges2d = []
    lines =0
    for line_range in line_ranges:
        start_y = line_range[0]
        end_y = line_range[1]
        line_img = thresh1[start_y:end_y, :]
        #竖直方向上 矩阵每列元素相加
        vertical_sum = np.sum(line_img, axis=0)
        vertical_line_ranges = projection_line(vertical_sum, min_val, min_range)
        #每个字符部分的竖直方向的(start,end)信息
        vertical_line_ranges2d.append(vertical_line_ranges)

    count = 0
    cutImage(thresh1,line_ranges,vertical_line_ranges2d)


img = cv2.imread("石钟山记.jpg")

Grayimg = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#反向处理图像
#thresh1 = cv2.adaptiveThreshold(Grayimg,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,5,5)
_,thresh1 = cv2.threshold(Grayimg, 140, 255, cv2.THRESH_BINARY_INV) 
#cv2.imwrite('2px_.jpg',thresh1)
pic(thresh1)







