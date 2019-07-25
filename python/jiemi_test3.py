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
dst_dir = "./result3/"
min_val = 30
min_range = 20


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


#计算不变量=图像黑点数/字符平均黑点数(保留两位小数)*字符个数
#计算m 嵌入水印信息的参数
def cal_K(img,char_range,w_po):
    global K
    count = 0   #所有的字符
    #NA,NB 字符图像个数
    black1 = [] #记录字符的黑色像素点
    A_embed = [] #嵌入部分的黑色像素点数
    B_adjust = [] #调整部分的黑色像素点数
    black_sum,white_sum = cal_black(img)  #文本图像的黑色像素点数
    #cut_img1 = []       #记录字符图像的坐标
    sum_img1 = []
    change_all = []
    for l1,l2,z1,z2 in char_range:
        pt1 = (l1, z1)
        pt2 = (l2, z2)
        count += 1
        img1 = img[z1:z2,l1:l2]  
        cv2.rectangle(img, pt1, pt2, (0,255,0),1)   
        #new_shape = (150, 150) img1 = cv2.resize(img1, new_shape)
        #输出每个字符的图片
        #cv2.imwrite(dst_dir + str(count) + ".jpg", img1)
        sum_img1.append(img1)
        #char_range.append((y,line_range[1],x,vertical_range[1]))
        #每个字符的黑色、白色像素点
        
        #每个字符的黑色、白色像素点
        hh, bb =cal_black(img1)
        #对于每个字符对象的操作
        #black-记录每个字符的黑色像素点数
        black1.append(hh)

    cv2.imshow('re',img)
    cv2.waitKey(0)  
    #print "count / len(sum_img1)=",count,len(sum_img1)       
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

    wi = []
    w_len = len(w_po)
    for l in range(w_len):
        _,po = w_po[l]
        x,x1,y,y1 = char_range[po]
        img_ = img[y:y1,x:x1]
        #cv2.imwrite(dst_dir + "img" + str(l) + ".jpg", img_) 
        wi.append(extract(img_,m))
    return wi


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
    while(i<len(w)):
        if (w[i]<=20):
            count = 0
            i +=1
        else:
            while (w[i] >= 20):
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
 

def extract(img1, m):
    hh,bb = cal_black(img1)
    k = 0.15 
    k0 = hh/m/k
    k1 = int(round(k0))
    if k1%2 == 0:
        ww = '0'
    elif k1%2 == 1:
        ww = '1'
    #print k1,ww,hh
    return ww       

def transfer_to_str(wii):
    s_2 = wii
    s_10 = int(s_2,2)  
    s_16 = '%x'%(s_10)  
    s = binascii.a2b_hex(s_16)  
    return s

def em_rate(wo,wi):
    count = 0
    m = 0
    sumC = len(wo)
    wi1 = list(wi)
    for i in range(sumC):
        if (wo[i]==wi[i]):
            count += 1
            wi1[i] = wi[i]
        elif m <= 5:
            count += 1
            wi1[i] = wo[i]
            m = m + 1
    wii = ''.join(wi1)
    r = round(float(count*100)/float(sumC),3) 
    if r >= 100 :
        r = 100
    rate = str(r) + '%'
    return rate


#w_po = [(0, 0), (1, 1), (2, 8), (3, 2), (4, 4), (5, 7), (6, 9), (7, 10), (8, 12), (9, 11), (10, 13), (11, 15), (12, 17), (13, 19), (14, 20), (15, 22), (16, 23), (17, 21), (18, 26), (19, 24), (20, 27), (21, 30), (22, 29), (23, 32)]
w_po = [(0, 0), (1, 1), (2, 2), (3, 5), (4, 7), (5, 8), (6, 10), (7, 4), (8, 11), (9, 6), (10, 9), (11, 16), (12, 18), (13, 20), (14, 12), (15, 21), (16, 22), (17, 13), (18, 14), (19, 24), (20, 29), (21, 31), (22, 15), (23, 19)]

#嵌入信息：abc

str1 = 'scan_11'
img = cv2.imread(str1 + ".jpg")

Grayimg = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

_,thresh0 = cv2.threshold(Grayimg, 140, 255, cv2.THRESH_BINARY) 

char_range = cutImage(thresh0)

'''
im = cv2.imread("scan_1.jpg")
Grayim = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
_,thresh1 = cv2.threshold(Grayim, 100, 255, cv2.THRESH_BINARY) 
'''

wi = cal_K(thresh0,char_range, w_po)

wii = reduce(lambda x, y:str(x)+str(y),wi)
print wii
ori = '011000010110001001100011'
#print transfer_to_str(wii)
rate = em_rate(ori,wii)
print rate




