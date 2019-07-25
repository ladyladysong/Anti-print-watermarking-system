# -*- coding: utf-8 -*-
#!/usr/bin/env python
from PIL import Image,ImageDraw,ImageFont,ImageFilter
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import cv2
import math
import os
import binascii  

#base_dir = ""
dst_dir = "./result4/"
min_val = 30
min_range = 20


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



#计算可翻转的一些图像的黑色像素点数
#不可翻转的像素点——黑色像素点为0
#完成嵌入的过程
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


#字符图像可翻转像素点的判断 
def judge_flip(im):
    flip =[]        #记录可翻转的黑色像素点的坐标
    flip1 =[]       #记录可翻转的白色像素点的坐标
    flip_b = 0          #im中黑色像素点的可翻转个数
    flip_w = 0          #im中白色像素点的可翻转个数
    #x = im.shape[0]
    #y = im.shape[1]
    x,y = im.shape
    #im = img[y:line_range[1], x:vertical_range[1]]
    for j in range(1,(y-1)):
        for i in range(1,(x-1)):
            #中心点为黑色：11B 12B 2B 31B 4B 52B       
            if im[i,j]==0:
                # 11B 12B
                if int(im[i-1,j-1]) + int(im[i,j-1]) + int(im[i+1,j-1]) + int(im[i-1,j]) + int(im[i+1,j]) + int(im[i-1,j+1]) + int(im[i,j+1]) + int(im[i+1,j+1]) == 255*7:
                    if int(im[i-1,j-1])==0 or int(im[i,j-1])==0 or int(im[i+1,j-1])==0 or int(im[i-1,j])==0 or int(im[i+1,j])==0 or\
                    int(im[i-1,j+1])==0 or int(im[i,j+1])==0 or int(im[i+1,j+1])==0:
                        flip.append((i,j))
                        flip_b =+1

                # 2B    
                elif int(im[i-1,j-1]) + int(im[i,j-1]) + int(im[i+1,j-1]) + int(im[i-1,j]) + int(im[i+1,j]) + int(im[i-1,j+1]) + int(im[i,j+1]) + int(im[i+1,j+1]) == 255*6:
                    if (int(im[i-1,j-1])+int(im[i,j-1]))==0 or (int(im[i,j-1])+int(im[i+1,j-1]))==0 or (int(im[i+1,j-1])+int(im[i+1,j]))==0 or\
                    (int(im[i+1,j])+int(im[i+1,j+1]))==0 or (int(im[i+1,j+1])+int(im[i,j+1]))==0 or (int(im[i,j+1])+int(im[i-1,j+1]))==0 or \
                    (int(im[i-1,j+1])+int(im[i-1,j]))==0 or (int(im[i-1,j])+int(im[i-1,j-1]))==0:
                        flip.append((i,j))
                        flip_b +=1

                #31B
                elif int(im[i-1,j-1]) + int(im[i,j-1]) + int(im[i+1,j-1]) + int(im[i-1,j]) + int(im[i+1,j]) + int(im[i-1,j+1]) + int(im[i,j+1]) + int(im[i+1,j+1]) == 255*5:
                    if (int(im[i-1,j-1])+int(im[i,j-1])+int(im[i+1,j-1]))==0 or (int(im[i+1,j-1])+int(im[i+1,j])+int(im[i+1,j+1]))==0 or\
                    (int(im[i+1,j+1])+int(im[i,j+1])+int(im[i-1,j+1]))==0 or (int(im[i-1,j+1])+int(im[i-1,j])+int(im[i-1,j-1]))==0 :
                        flip.append((i,j))
                        flip_b +=1

                #4B
                elif int(im[i-1,j-1]) + int(im[i,j-1]) + int(im[i+1,j-1]) + int(im[i-1,j]) + int(im[i+1,j]) + int(im[i-1,j+1]) + int(im[i,j+1]) + int(im[i+1,j+1]) == 255*4:
                    if (int(im[i-1,j-1]) + int(im[i-1,j]) + int(im[i-1,j+1]) + int(im[i,j+1]))==0 or (int(im[i-1,j-1]) + int(im[i-1,j]) + \
                    int(im[i-1,j+1]) + int(im[i,j-1]))==0 or (int(im[i-1,j-1]) + int(im[i,j-1]) + int(im[i+1,j-1]) + int(im[i+1,j]))==0 or\
                    (int(im[i+1,j+1]) + int(im[i,j-1]) + int(im[i+1,j-1]) + int(im[i+1,j]))==0 or (int(im[i+1,j+1]) + int(im[i,j+1]) + \
                    int(im[i-1,j+1]) + int(im[i+1,j]))==0 or (int(im[i+1,j+1]) + int(im[i,j+1]) + int(im[i+1,j-1]) + int(im[i+1,j]))==0 or\
                    (int(im[i-1,j-1]) + int(im[i,j-1]) + int(im[i+1,j-1]) + int(im[i-1,j]))==0 or (int(im[i-1,j+1]) + int(im[i,j+1]) + \
                    int(im[i+1,j+1]) + int(im[i-1,j]))==0 :
                        flip.append((i,j))
                        flip_b +=1

                #52B
                elif int(im[i-1,j-1]) + int(im[i,j-1]) + int(im[i+1,j-1]) + int(im[i-1,j]) + int(im[i+1,j]) + int(im[i-1,j+1]) + int(im[i,j+1]) + int(im[i+1,j+1]) == 255*3:
                    if (int(im[i-1,j-1]) + int(im[i-1,j]) + int(im[i,j-1]))==255*3 or (int(im[i,j-1]) + int(im[i+1,j-1]) + int(im[i+1,j]))==255*3 or\
                    (int(im[i+1,j]) + int(im[i+1,j+1]) + int(im[i,j+1]))==255*3 or (int(im[i-1,j]) + int(im[i-1,j+1]) + int(im[i,j+1]))==255*3 :
                        flip.append((i,j))
                        flip_b +=1
    


            #中心点为白色：51W 6W 71W 72W 4W 32W
            elif int(im[i,j])==255 :
                #71w 72w
                if int(im[i-1,j-1]) + int(im[i,j-1]) + int(im[i+1,j-1]) + int(im[i-1,j]) + int(im[i+1,j]) + int(im[i-1,j+1]) + int(im[i,j+1]) + int(im[i+1,j+1]) == 255:
                    if int(im[i-1,j-1])==225 or int(im[i,j-1])==225 or int(im[i+1,j-1])==225 or int(im[i-1,j])==225 or int(im[i+1,j])==225 or \
                    int(im[i-1,j+1])==225 or int(im[i,j+1])==225 or int(im[i+1,j+1])==225:
                        #记录可翻转的像素坐标
                        flip1.append((i,j))
                        flip_w +=1
                #6w
                elif int(im[i-1,j-1]) + int(im[i,j-1]) + int(im[i+1,j-1]) + int(im[i-1,j]) + int(im[i+1,j]) + int(im[i-1,j+1]) + int(im[i,j+1]) + int(im[i+1,j+1]) == 255*2:
                    if (int(im[i-1,j-1])+int(im[i,j-1]))==225 or (int(im[i,j-1])+int(im[i+1,j-1]))==225 or (int(im[i+1,j-1])+int(im[i+1,j]))==225 or\
                    (int(im[i+1,j])+int(im[i+1,j+1]))==225 or (int(im[i+1,j+1])+int(im[i,j+1]))==225 or (int(im[i,j+1])+int(im[i-1,j+1]))==225 or \
                    (int(im[i-1,j+1])+int(im[i-1,j]))==225 or (int(im[i-1,j])+int(im[i-1,j-1]))==225:
                        flip1.append((i,j))
                        flip_ +=1
                #51w
                elif int(im[i-1,j-1]) + int(im[i,j-1]) + int(im[i+1,j-1]) + int(im[i-1,j]) + int(im[i+1,j]) + int(im[i-1,j+1]) + int(im[i,j+1]) + int(im[i+1,j+1]) == 255*3:
                    if (int(im[i-1,j-1])+int(im[i,j-1])+int(im[i+1,j-1]))==255 or (int(im[i+1,j-1])+int(im[i+1,j])+int(im[i+1,j+1]))==255 or\
                    (int(im[i+1,j+1])+int(im[i,j+1])+int(im[i-1,j+1]))==255 or (int(im[i-1,j+1])+int(im[i-1,j])+int(im[i-1,j-1]))==255 :
                        flip1.append((i,j))
                        flip_w +=1
                #4w
                elif int(im[i-1,j-1]) + int(im[i,j-1]) + int(im[i+1,j-1]) + int(im[i-1,j]) + int(im[i+1,j]) + int(im[i-1,j+1]) + int(im[i,j+1]) + int(im[i+1,j+1]) == 255*4:
                    if (int(im[i-1,j-1]) + int(im[i-1,j]) + int(im[i-1,j+1]) + int(im[i,j+1]))==0 or (int(im[i-1,j-1]) + int(im[i-1,j]) + \
                    int(im[i-1,j+1]) + int(im[i,j-1]))==0 or (int(im[i-1,j-1]) + int(im[i,j-1]) + int(im[i+1,j-1]) + int(im[i+1,j]))==0 or\
                    (int(im[i+1,j+1]) + int(im[i,j-1]) + int(im[i+1,j-1]) + int(im[i+1,j]))==0 or (int(im[i+1,j+1]) + int(im[i,j+1]) + \
                    int(im[i-1,j+1]) + int(im[i+1,j]))==0 or (int(im[i+1,j+1]) + int(im[i,j+1]) + int(im[i+1,j-1]) + int(im[i+1,j]))==0 or\
                    (int(im[i-1,j-1]) + int(im[i,j-1]) + int(im[i+1,j-1]) + int(im[i-1,j]))==0 or (int(im[i-1,j+1]) + int(im[i,j+1]) + \
                    int(im[i+1,j+1]) + int(im[i-1,j]))==0 :
                        flip1.append((i,j))
                        flip_w +=1
                #32w
                elif int(im[i-1,j-1]) + int(im[i,j-1]) + int(im[i+1,j-1]) + int(im[i-1,j]) + int(im[i+1,j]) + int(im[i-1,j+1]) + int(im[i,j+1]) + int(im[i+1,j+1]) == 255*5:
                    if (int(im[i-1,j-1]) + int(im[i-1,j]) + int(im[i,j-1]))==0 or (int(im[i,j-1]) + int(im[i+1,j-1]) + int(im[i+1,j]))==0 or\
                    (int(im[i+1,j]) + int(im[i+1,j+1]) + int(im[i,j+1]))==0 or (int(im[i-1,j]) + int(im[i-1,j+1]) + int(im[i,j+1]))==0 :
                        flip1.append((i,j))
                        flip_w +=1
        

    return (flip_b,flip_w,flip,flip1)



#计算不变量=图像黑点数/字符平均黑点数(保留两位小数)*字符个数
#计算m 嵌入水印信息的参数
def cal_K(img,line_ranges,vertical_line_ranges2d,w_po):
    global K
    count = 0   #所有的字符
    #NA,NB 字符图像个数

    black1 = [] #记录字符的黑色像素点
    A_embed = [] #嵌入部分的黑色像素点数
    B_adjust = [] #调整部分的黑色像素点数
    black_sum,white_sum = cal_black(img)  #文本图像的黑色像素点数
    cut_img1 = []       #记录字符图像的坐标
    sum_img1 = []
    change_all = []
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
            cv2.rectangle(img, pt1, pt2, 255)      
            #new_shape = (150, 150) img1 = cv2.resize(img1, new_shape)
            #输出每个字符的图片
            #cv2.imwrite(dst_dir + str(count) + ".jpg", img1)

            sum_img1.append(img1)
            cut_img1.append((y,line_range[1],x,vertical_range[1]))
            #每个字符的黑色、白色像素点
            
            #每个字符的黑色、白色像素点
            hh, bb =cal_black(img1)
            #对于每个字符对象的操作
            #black-记录每个字符的黑色像素点数
            black1.append(hh)
    cv2.imshow('re',img)
    cv2.waitKey(0)      
    black_sum1 = sum(black1)
    NB = count/4
    NA = count - NB
    A_embed = black1[0:NA]
    B_adjust = black1[NA:]
    #m——所有字符图像包晗的黑色像素点平局值
    m = round(float(sum(A_embed) + sum(B_adjust) )/float(NA + NB),3)
    #m = round(float(sum(A_embed) + sum(B_adjust) +sum(C_abandon))/float(NA + NB +NC),3)
    K = round(float(black_sum)/float(black_sum1)*float(count),3)
    print "不变量K,m: ",K,m
'''
    wi = []
    w_len = len(w_po)
    for l in range(w_len):
        _,po = w_po[l]
        y,y1,x,x1 = cut_img1[po]
        img_ = img[y:y1,x:x1]
        cv2.imwrite(dst_dir + "img" + str(l) + ".jpg", img_) 
        wi.append(extract(img_,m))
    return wi
'''

def extract(img1, m):
    hh,bb = cal_black(img1)
    k = 0.15 
    k0 = hh/m/k
    k1 = int(round(k0))
    if k1%2 == 0:
        ww = '0'
    elif k1%2 == 1:
        ww = '1'
    print k1,ww,hh
    return ww       


def transfer_to_str(wii):
    s_2 = wii
    s_10 = int(s_2,2)  
    s_16 = '%x'%(s_10)  
    s = binascii.a2b_hex(s_16)  
    return s



img = cv2.imread("2px_原图.png")
Grayimg = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#反向处理图像
ret,thresh1 = cv2.threshold(Grayimg,127,255,cv2.THRESH_BINARY_INV )
print cal_black(thresh1)
#thresh1 = cv2.adaptiveThreshold(Grayimg,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,5,5)
#cv2.imwrite('tt1.jpg',thresh1)
#adaptive_threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

#w = list(str)
w_po = [(0, 0), (1, 14), (2, 1), (3, 2), (4, 6), (5, 9), (6, 17), (7, 10), (8, 18), (9, 20), (10, 15), (11, 19), (12, 22), (13, 26), (14, 23), (15, 24), (16, 28), (17, 30), (18, 27), (19, 31), (20, 33), (21, 32), (22, 36), (23, 38), (24, 43), (25, 47), (26, 41), (27, 44), (28, 50), (29, 46), (30, 48), (31, 53), (32, 54), (33, 58), (34, 56), (35, 59), (36, 61), (37, 65), (38, 64), (39, 67), (40, 69), (41, 72), (42, 71), (43, 78), (44, 74), (45, 77), (46, 79), (47, 82), (48, 86), (49, 90), (50, 83), (51, 85), (52, 94), (53, 97), (54, 103), (55, 88), (56, 104), (57, 108), (58, 89), (59, 115), (60, 91), (61, 93), (62, 99)]
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
        cv2.rectangle(line_rectangle, pt1, pt2, 255)
    #cv2.imshow('re1',line_rectangle)
    #cv2.waitKey(0)   
        #cv2.imwrite('./result3/' + str(i) + '.jpg',line_rectangle[y:y+h,x:x+w])

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
       
    cal_K(thresh1,line_ranges,vertical_line_ranges2d,w_po)
'''
    wii = reduce(lambda x, y:str(x)+str(y),wi)
    print wi
    print wii
    recover_info = transfer_to_str(wii)
    print recover_info
'''
pic(thresh1)









