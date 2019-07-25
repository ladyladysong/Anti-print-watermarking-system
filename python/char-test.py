# -*- coding: utf-8 -*-
from PIL import Image,ImageDraw,ImageFont,ImageFilter
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import cv2
import math
import os
import binascii  
dst_dir = "./result3/"
img = cv2.imread("1.jpg")
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
height, width = img.shape[:2]
#print height, width
#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret,thresh1 = cv2.threshold(gray, 140, 255, cv2.THRESH_BINARY) 
print thresh1.shape

#字符图像可翻转像素点的判断 
def judge_flip(im):
    flip =[]	#记录可翻转的黑色像素点的坐标
    flip1 =[]       #记录可翻转的白色像素点的坐标
    flip_b = 0          #im中黑色像素点的可翻转个数
    flip_w = 0          #im中白色像素点的可翻转个数
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


flip = []
flip1 = []
flip_b,flip_w,flip,flip1 = judge_flip(thresh1)
thresh2 = thresh1.copy()
thresh3 = thresh1.copy()
#im = img[y:line_range[1], x:vertical_range[1]]
for i,j in flip:
	thresh2[i,j] = 255


#cv2.imwrite('1-255.jpg',thresh2)

for i,j in flip1:
	thresh3[i,j] = 0
#cv2.imwrite('1-0.jpg',thresh3)

plt.figure(figsize=(10,5)) #设置窗口大小
#plt.suptitle('Multi_Image') # 图片名称
plt.subplot(1,3,1), plt.title('image')
plt.imshow(thresh1), plt.axis('off')
plt.subplot(1,3,2), plt.title('black')
plt.imshow(thresh2), plt.axis('off')
plt.subplot(1,3,3), plt.title('white')
plt.imshow(thresh3), plt.axis('off')
plt.show()




