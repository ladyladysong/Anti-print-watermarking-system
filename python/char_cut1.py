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
#scan_01_new
#scan_
img = cv2.imread("scan_11.jpg")
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
height, width = img.shape[:2]
#print height, width
#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret,thresh1 = cv2.threshold(gray, 140, 255, cv2.THRESH_BINARY) 
#_,thresh2 = cv2.threshold(gray, 140, 255, cv2.THRESH_BINARY_INV) 
print thresh1.shape
#cv2.imshow('yuantu',thresh1)
#cv2.waitKey(0)
emptyImage1 = np.zeros(img.shape, np.uint8) 
#cv2.Zero(cv2.cv.fromarry(paintx))
#创建width长度为0的数组


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


#整体图像切分为单个字符图像 
def chuizhi(img):
    #paintx = np.zeros(img.shape,np.unit8)
    w = [0]*img.shape[1]
    #对每行计算投影值
    for x in range(img.shape[1]):
        for y in range(img.shape[0]):
            t = img[y,x]
            if t == 0:
                w[x] += 1
            else:
                continue
    i = 0
    z_kuan = []
    #根据字高可知 一个字符宽度在25左右
    while(i<len(w)):
        if (w[i]<=6):
            count = 0
            i +=1
        else:
            while (w[i] >= 6):
                count += 1
                i += 1
            z_kuan.append(count)
    #print len(z_kuan)
    max_k = max(z_kuan)
    min_k = min(z_kuan)
    return w,min_k,max_k


#返回水平投影上的投影总值
def shuiping(img):
    h = [0]*img.shape[0]
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            t = img[y,x]
            #黑色像素点 
            if t == 0:
                h[y] += 1
            else :
                continue
    i = 0
    z_gao = []
    count = 0
    while (i< len(h)):
    #for i in range(len(h)):
        if (h[i] <= 20):
            count = 0
            i +=1
        else:
            while (h[i] >= 20):
                count += 1
                i += 1
            z_gao.append(count)
    #print len(z_gao)
    max_g = max(z_gao)
    min_g = min(z_gao)
    #print max_g,min_g
    return h,min_g,max_g


#根据水平投影值选择切割点
def shuiping_cut(img,h,min_g,max_g):
    start = 0
    line_ranges = [] 
    inline = 1
    for i in range(img.shape[0]):
        if inline ==1 and h[i] >= min_g:
            #从空白区进入文字区
            start = i
            #记录起始分割点
            inline = 0
        elif (i - start >3) and h[i] <= max_g and inline == 0:
            #从文字区进入空白区
            inline = 1
            line_ranges.append((start-2,i+2))
    #print line_ranges

    return line_ranges


def cutImage(thresh1):
    h,min_g,max_g = shuiping(thresh1)
    w,min_k,max_k =chuizhi(thresh1)
    line_ranges = []
    line_ranges = shuiping_cut(thresh1,h,min_g,max_g)
    line_rectangle = np.copy(thresh1)
    char_range = []
    count = 0
    for i,line_range in enumerate(line_ranges): 
        z1 = line_range[0]
        z2 = line_range[1]
        #img_line = thresh1[z1:z2,]
        #w,min_k,max_k = chuizhi(img_line)
        #count = 0
        incol = 1
        start1 = 0
        for i1 in range(thresh1.shape[1]):
            if incol == 1 and w[i1] >= min_g*4:
                start1 = i1
                incol = 0
            elif (i1-start1 >= min_g) and w[i1] <= max_g*4 and incol == 0:
                incol = 1
                l1 = start1 
                l2 = i1 +2
                img_ = thresh1[z1:z2,l1:l2]
                black,white=cal_black(img_)
                if black*4.6 > white:
                    count += 1
                    char_range.append((l1,l2,z1,z2))
                    cv2.rectangle(thresh1,(l1,z1),(l2,z2),(0,255,0),1)  
    cv2.imshow('re',thresh1)
    cv2.waitKey(0)
    return char_range

cutImage(thresh1)
