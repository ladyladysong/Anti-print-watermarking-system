# -*- coding: utf-8 -*-
#!/usr/bin/env python

from PIL import Image
import numpy as np
import cPickle as pickle
import cv2
import math
import os
import binascii 

#base_dir = ""
#dst_dir = "./result/"


class cuttt():
    def __init__(self,info,pic):
        
        self.pic = pic
        self.info = info
        self.main()

    # 记录像素段的位置 返回列表（起点，终点）
    def projection_line(self,array_vals, minimun_val, minimun_range):
        start_i = None
        end_i = None
        line_ranges = []
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
    def cal_black(self, im):
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
    def judge_flip(self, im):
        flip =[]        #记录可翻转的黑色像素点的坐标
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



    #计算不变量=图像黑点数/字符平均黑点数(保留两位小数)*字符个数
    #计算m 嵌入水印信息的参数
    def cal_K(self,img,line_ranges,vertical_line_ranges2d,wi,str1):
        global K
        count = 0   #所有的字符
        #NA,NB 字符图像个数
        black1 = [] #记录字符的黑色像素点
        A_embed = [] #嵌入部分的黑色像素点数
        B_adjust = [] #调整部分的黑色像素点数
        black_sum,white_sum = self.cal_black(img)  #文本图像的黑色像素点数
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
                #new_shape = (150, 150) img1 = cv2.resize(img1, new_shape)
                #输出每个字符的图片
                #cv2.imwrite(dst_dir + str(count) + ".jpg", img1)
                sum_img1.append(img1)
                cut_img1.append((y,line_range[1],x,vertical_range[1]))
                #每个字符的黑色、白色像素点
                
                #每个字符的黑色、白色像素点
                hh, bb = self.cal_black(img1)
                #对于每个字符对象的操作
                #black-记录每个字符的黑色像素点数
                black1.append(hh)
                
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

        for i in range(len(sum_img1)):
            img1 = sum_img1[i]
            change_all.append(self.embedInfo(img1,m))

        changeA = change_all[0:NA]    #记录A部分每个字符的黑色像素变化量
        w_po = []
        #plt.imshow(img_)
        #plt.show()
        change_sum = 0
        changeALL =[]
        flagA = [0] * len(changeA)
        ff = True
        for i in range(len(wi)):
            index = 0
            if wi[i] == '0':
                y,y1,x,x1 = cut_img1[index]
                #img_ = img[y:y1,x:x1]
                while ff:
                    change,_ = changeA[index]
                    if self.if_emded(img[y:y1,x:x1],change) and (flagA[index] == 0):
                        self.emdedding(img[y:y1,x:x1],change)
                        #embedInfo0(img_,m)
                        #cv2.imwrite(dst_dir + "img"+str(i)+"_" + str(index) +".jpg", img_)
                        w_po.append((i,index))
                        flagA[index] = 1
                        changeALL.append(change)
                        change_sum = change_sum + change
                        break
                    else :
                        index += 1
                        if index < NA:
                            y,y1,x,x1 = cut_img1[index]
                            #img_ = img[y:y1, x:x1]
                        elif index == NA:
                            ff = False
                            print "please cut your info,it's too long!"
                            break

            if wi[i] == '1':
                y,y1,x,x1 = cut_img1[index]
                #img_ = img[y:y1,x:x1]
                while ff:
                    _,change = changeA[index]
                    if self.if_emded(img[y:y1,x:x1],change) and (flagA[index] == 0):
                        self.emdedding(img[y:y1,x:x1],change)
                        #embedInfo1(img_,m)
                        #cv2.imwrite(dst_dir + "img"+str(i)+"_" + str(index) +".jpg", img_)
                        w_po.append((i,index))
                        flagA[index] = 1
                        changeALL.append(change)
                        change_sum = change_sum + change
                        break
                    else :
                        index += 1
                        if index < NA:
                            y,y1,x,x1 = cut_img1[index]
                            #img_ = img[y:y1, x:x1]

                        elif index == NA:
                            ff = False
                            ff = False
                            print "please cut your info,it's too long!"
                            break
            
            if ff == False :
                break
                print change_sum
        #print "the positon with wi is: ",w_po
        #print 
        #调整部分-黑变白
        if change_sum >= 0 :
            flag = True 
        else :
            # 白变黑
            flag = False
            change_sum = -change_sum
        index = NA
        while change_sum > 0:
            if (index <= len(sum_img1)):
                y,y1,x,x1 = cut_img1[index]
                change_sum = change_sum - self.embed_B(img[y:y1,x:x1], flag, change_sum)
                #cv2.imwrite(dst_dir + "img" + str(index) + ".jpg", img_B)
                index += 1

        thresh2 = img.copy()  #复制图像  
        for i in range(0,thresh2.shape[0]):         
            #thresh1.shape表示图像的尺寸和通道信息(高,宽,通道)  
            for j in range(0,thresh2.shape[1]):  
                thresh2[i,j]= 255 - img[i,j]  

        cv2.imwrite( str1 +"_new" + ".jpg", thresh2)
        return w_po



    def embed_B(self, img1, flag, change):
        flip_b,flip_w,flip,flip1 = self.judge_flip(img1)
        count_ = 0
        #需要调整黑色像素点为白色
        if ( flag == True ) :
            if change >= flip_b: 
                for i,j in flip:
                    img1[i,j] = 255
                count_ = flip_b
            else :
                for i,j in flip:
                    img1[i,j] = 255
                    count_ += 1
                    if count_ ==change:
                        break
        #需要调整白色为黑色
        else :
            if change >= flip_w:
                for i,j in flip1:
                    img1[i,j] = 0
                count_ = flip_w
            else :
                for i,j in flip:
                    img1[i,j] = 0
                    count_ += 1
                    if count_ ==change:
                        break    
        #print "this is count:",count_
        return count_

    def embedInfo0(self, img1, m):
        #m = 457.834
        hh,bb = self.cal_black(img1)
        
        change0_1 = []    #水印信息为0或1时每个字符的翻转值
        k = 0.15 
        #水印信息为0，此时翻转像素点使得总数为k的偶数倍
        k0 = hh/m/k
        k1 = int(round(k0))
        if k1%2 == 0:
            hh_new0 = k1*m*k

        elif int(k0)%2 == 0:
            k1 = int(k0)
            hh_new0 = k1*m*k

        elif int(k0)%2 == 1:
            k1 =int(k0) + 1
            hh_new0 = k1*m*k

        hh_new0 = int(hh_new0)
        print k1,0,hh_new0
       
        #print hh_new0,hh_new1
        #return hh_new0-hh,hh_new1-hh

    def embedInfo1(self, img1, m):
        hh,bb = self.cal_black(img1)
        k = 0.15
        k0 = hh/m/k
        k1 = int(round(k0))
        
        if k1%2 == 0:
            if int(k0)%2 == 0:
                k1 = int(k0) + 1
                hh_new1 = k1*m*k
            else:
                k1 = int(k0)
                hh_new1 = k1*m*k
        else:
            hh_new1 = k1*m*k

        hh_new1 = int(hh_new1)
        print k1,1,hh_new1


    def embedInfo(self, img1, m):
        #m = 457.834
        hh,bb = self.cal_black(img1)
        change0_1 = []    #水印信息为0或1时每个字符的翻转值
        k = 0.15 
        #水印信息为0，此时翻转像素点使得总数为k的偶数倍
        k0 = hh/m/k
        k1 = int(round(k0))

        if k1%2 == 0:
            hh_new0 = k1*m*k

        elif int(k0)%2 == 0:
            k1 = int(k0)
            hh_new0 = k1*m*k

        elif int(k0)%2 == 1:
            k1 =int(k0) + 1
            hh_new0 = k1*m*k

        hh_new0 = int(hh_new0)
        
        k0 = hh/m/k
        k1 = int(round(k0))
        if k1%2 == 0:
            if int(k0)%2 == 0:
                k1 = int(k0) + 1
                hh_new1 = k1*m*k
            else:
                k1 = int(k0)
                hh_new1 = k1*m*k
        else:
            hh_new1 = k1*m*k

        hh_new1 = int(hh_new1)
        #print hh_new0,hh_new1
        return hh_new0-hh,hh_new1-hh



    def if_emded(self, img1, change):
        # y,y1,x,x1 = cut_img1
        flip_b,flip_w,flip,flip1 = self.judge_flip(img1)
        flag =  False
        #需要翻转白色像素点为黑色
        if (change > 0) and (flip_w  > change):
            flag = True
        #需要翻转黑色为白色
        if (change < 0) and (flip_b  > -change):
            flag = True    
        return flag


    def emdedding(self, img1, change):
       # y,y1,x,x1 = cut_img1
        flip_b,flip_w,flip,flip1 = self.judge_flip(img1)
        count_ = 0
        #需要翻转白色像素点为黑色
        if (change > 0) :
            #print "h+change=",h,change,"flip_w =",flip_w,
            for i,j in flip1:
                img1[i,j] = 0
                count_ += 1
                if count_ == change :
                    break
        #需要翻转黑色为白色
        if (change < 0) :
            for i,j in flip:
                img1[i,j] = 255
                count_ += 1
                if count_ == -change :
                    break
        #h,_ = cal_black(img1)
        #print 'h_new=',h,"change=",change
        

    def main(self):

        info1 = self.info
        print info1
        wi = []
        for i in range(len(info1)):
           wi.append(info1[i])

        #图像处理
        img = cv2.imread( self.pic + ".jpg")
        Grayimg = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        #反向处理图像
        ret,thresh1 = cv2.threshold(Grayimg,127,255,cv2.THRESH_BINARY_INV )
        #thresh1 = cv2.adaptiveThreshold(Grayimg,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,5,5)
        #cv2.imwrite('tt1.jpg',thresh1)
        #adaptive_threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
        horizontal_sum = np.sum(thresh1, axis=1)
        min_val = 30
        min_range = 20
        line_ranges = self.projection_line(horizontal_sum, min_val, min_range)
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
        # 根据line_ranges[]切分每行，再对每行进行每个字符的切分
        vertical_line_ranges2d = []
        lines =0
        for line_range in line_ranges:
            start_y = line_range[0]
            end_y = line_range[1]
            line_img = thresh1[start_y:end_y, :]
            #竖直方向上 矩阵每列元素相加
            vertical_sum = np.sum(line_img, axis=0)
            vertical_line_ranges = self.projection_line(vertical_sum, min_val, min_range)
            #每个字符部分的竖直方向的(start,end)信息
            vertical_line_ranges2d.append(vertical_line_ranges)

        w_po = self.cal_K(thresh1,line_ranges,vertical_line_ranges2d,wi,self.pic)
        self.wpo = w_po
        w_po1 = pickle.dumps(w_po)
        f = open(self.pic + '.txt','w')
        f.write(w_po1)
        f.close()

    def output(self):
        return self.wpo
        










