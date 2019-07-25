# -*- coding: utf-8 -*-
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageEnhance
from PIL import Image
import numpy as np

import cv2
import math
import os
import binascii  


def rorate(img):
    # 读取图片
    #img = Image.open('qq_image.jpg')
    # 左右对换
    rorate = img.transpose(Image.FLIP_LEFT_RIGHT)
    rorate.show()
    # 上下翻转
    rorate1 = img.transpose(Image.FLIP_TOP_BOTTOM)
    rorate1.show()
    return rorate1

def resize(img):
    height, width = img.shape[:2]  
    size = (int(width*0.15), int(height*0.15))  
    shrink = cv2.resize(img, size, interpolation=cv2.INTER_AREA)  
    #cv2.resize(src, dsize[, dst[, fx[, fy[, INTER_AREA]]]]) -> dst  
    #重采样插值法
    return shrink

'''
img = cv2.imread('test1_new.jpg',0)
#img = resize(img)
#cv2.imwrite('scan_re.jpg',img)
img1 = np.power(img/float(np.max(img)), 1/1.5)
img2 = np.power(img/float(np.max(img)), 1.5)
#cv2.imwrite('scan_ga.jpg',img2)

#边缘检测
edges = cv2.Canny(img,100,200)#其他的默认
#
laplacian = cv2.Laplacian(img,cv2.CV_64F)#默认ksize=3
#cv2.imshow('laplacian',laplacian)
#中值滤波
blur = cv2.medianBlur(img,3)

#img = cv2.dilate(img, np.ones((3, 3), np.uint8), iterations=1)
erode = cv2.erode(blur, np.ones((2, 2), np.uint8), iterations=1)
#cv2.imshow('window',img)
#cv2.imwrite('scan_ro.jpg',erode)
cv2.imshow('erode',blur)
cv2.waitKey(0)
'''

def get_bin_table(threshold=140):
    """
    获取灰度转二值的映射table
    :param threshold:
    :return:
    """
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return table


def sum_9_region(img, x, y):
    """
    9邻域框,以当前点为中心的田字框,黑点个数
    :param x:
    :param y:
    :return:
    """
    # todo 判断图片的长宽度下限
    cur_pixel = img.getpixel((x, y))  # 当前像素点的值
    width = img.width
    height = img.height

    if cur_pixel == 1:  # 如果当前点为白色区域,则不统计邻域值
        return 0

    if y == 0:  # 第一行
        if x == 0:  # 左上顶点,4邻域
            # 中心点旁边3个点
            sum = cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 4 - sum
        elif x == width - 1:  # 右上顶点
            sum = cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1))

            return 4 - sum
        else:  # 最上非顶点,6邻域
            sum = img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 6 - sum
    elif y == height - 1:  # 最下面一行
        if x == 0:  # 左下顶点
            # 中心点旁边3个点
            sum = cur_pixel \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x, y - 1))
            return 4 - sum
        elif x == width - 1:  # 右下顶点
            sum = cur_pixel \
                  + img.getpixel((x, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y - 1))

            return 4 - sum
        else:  # 最下非顶点,6邻域
            sum = cur_pixel \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x, y - 1)) \
                  + img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x + 1, y - 1))
            return 6 - sum
    else:  # y不在边界
        if x == 0:  # 左边非顶点
            sum = img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))

            return 6 - sum
        elif x == width - 1:  # 右边非顶点
            # print('%s,%s' % (x, y))
            sum = img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1))

            return 6 - sum
        else:  # 具备9领域条件的
            sum = img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1)) \
                  + img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 9 - sum





def binarizing(im,threshold):
    pixdata=im.load()
    w,h=im.size
    for j in range(h):
        for i in range(w):
            if pixdata[i,j]<threshold:
                pixdata[i,j]=0
            else:
                pixdata[i,j]=255
    return im

################################图片去噪############################

##########对于像素值>245的邻域像素，判别为属于背景色################

##########，如果一个像素上下左右4各像素值有超过2个##################

##########像素属于背景色，那么该像素就是目标点，否则就是噪声##########

####################################################################

def denoising(im):

    pixdata=im.load()
    w,h=im.size
    for j in range(1,h-1):
        for i in range(1,w-1):
            count=0
            if pixdata[i,j-1]>245:
                count=count+1
            if pixdata[i,j+1]>245:
                count=count+1
            if pixdata[i+1,j]>245:
                count=count+1
            if pixdata[i-1,j]>245:
                count=count+1
            if count>2:
                pixdata[i,j]=255
    return im

###############################################################################
##############图片转换:打开图片,滤波器,增强,灰度图转换,去噪,二值化############
###############################################################################

def imgTransfer(f_name):
    im=Image.open(f_name)  #打开图片
    #im=resize(im)
    im=im.filter(ImageFilter.MedianFilter(1)) #对于输入图像的每个像素点，该滤波器从（size，size）的区域中拷贝中值对应的像素值存储到输出图像中
    #enhancer=ImageEnhance.Contrast(im)
    #im=enhancer.enhance(1)
    im=ImageEnhance.Contrast(im).enhance(1.5)#enhance()的参数factor决定着图像的对比度情况。从0.1到0.5，再到0.8，2.0，图像的对比度依次增大.0.0为纯灰色图像;1.0为保持原始
    im=im.convert('L')   #灰度图转换
    im=denoising(im)     #图片去噪
    im=binarizing(im,200)  #图片二值化
    #im=nse.removeNoisy(im)
    #im.save('小石潭记_new.jpg','jpeg')
    #im.show()
    #return im

def pre_process(img):
    im = ImageEnhance.Sharpness(img).enhance(1.2)
    imgry = im.convert('L')  # 转化为灰度图
    table = get_bin_table()
    out = imgry.point(table, '1')
    #out.show()
    for y in range(out.height):
        for x in range(out.width):
            if sum_9_region(out,x,y) <= 2:
                out.putpixel((x,y),1)
    #out.show()
    im.save(str1 + '1.jpg','jpeg')

img = cv2.imread('CPP6501271.jpg',0)
img = resize(img)
cv2.imwrite('scan_1.jpg',img)

str1 = 'scan_1'
image = Image.open(str1 + '.jpg')
#pre_process(image)

#imgTransfer('scan_1.jpg')

