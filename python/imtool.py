# -*- coding: utf-8 -*-
#!/usr/bin/env python

from PIL import Image,ImageEnhance,ImageFilter,ImageGrab
import matplotlib.pyplot as plt
import numpy as np
from pylab import *




def imresize(im,sz):
	'''使用PIL对象重新定义图像数组大小'''
	pil_im = Image.fromarry(unit8(im))

	return array(pil_im.resize(sz))


def histeq(im,nbr_bins=256):
	'''对灰度图像进行直方图均衡化'''
	#计算直方图
	imhist,bins = histogram(im.flatten(),nbr_bins,normed=True)
	cdf = imhist.cumsum()		#像素值累计分布函数
	cdf = 255*cdf/cdf[-1]		#归一化

	#使用累计分布函数的线性插值，计算新像素值
	im2 = interp(im.flatten(),bins[:-1],cdf)

	return im2.reshape(im.shape),cdf


# 依据图片像素颜色计算X轴投影
def Caculate_X(im):
	Image_Value=[]
	for i in range(im.size[0]):
		Y_pixel=0
		for j in range(im.size[1]):
			if im.getpixel((i,j))==0: #black
				temp_value=1
			else:
				temp_value=0
				Y_pixel = Y_pixel+temp_value
				Image_Value.append(Y_pixel)

	return Image_Value

 
 # 依据图片像素颜色计算Y轴投影
def Caculate_Y(im):
	Image_Value=[]
	for i in range(im.size[0]):
		X_pixel=0
		for j in range(im.size[1]):
			if im.getpixel((i,j))==0: #black
				temp_value=1
			else:
				temp_value=0
				X_pixel = X_pixel+temp_value
				Image_Value.append(X_pixel)

	return Image_Value

#记录图像的分割点
def find_end(start_):
	end_ = start_+1
	for m in range(start_+1,width-1):
		if (black_row[m] if arg else white_row[m]) > (0.95*black_row_max if arg else 0.95*white_row_max):
			end_ = m
			break
		return end_


#原始数据四周补0
def pad_data(data,nei_size):
    m,n= data.shape
    #m是高，n是宽
    t1 = np.zeros([nei_size//2,n])
    #置零数组，1/2高，等宽
    data = np.concatenate((t1,data,t1))
    #将元素连接起来，扩大data周围的高
    m,n = data.shape
    t2 = np.zeros([m,nei_size//2])
    data = np.concatenate((t2,data,t2),axis=1)  
    #扩大data周围的宽
    return data

#逐像素取大小为nei_size*nei_size的邻域数据
def gen_dataX(data,nei_size):
	nei_size=3
	data = pad_data(data,nei_size)
    x,y = data.shape
    m = x-nei_size//2*2
    n = y-nei_size//2*2
    res = np.zeros([m*n,nei_size**2])
    #res矩阵置零，高为m*n，宽为邻域平方
    print m,n
    k = 0
    for i in range(nei_size//2,m+nei_size//2):
        for j in range(nei_size//2,n+nei_size//2):
            res[k,:] = np.reshape(data[i-nei_size//2:i+nei_size//2+1,j-nei_size//2:j+nei_size//2+1].T,(1,-1))
            k += 1
    print k
    return res

    
#获取周围的黑点个数
def getN(p):
        count = 0
        x = [p[0]-1,p[0],p[0]+1]
        y = [p[1]-1,p[1],p[1]+1]
        for i in itertools.product(x,y):  # 笛卡尔积
            try:
                if img.getpixel(i) == 0:
                    count +=1
            except:
                print 'out of'
                continue
        print count
        return count









