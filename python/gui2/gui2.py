# -*- coding: utf-8 -*-

import wx
import os
import subprocess
import sys
import cPickle as pickle
import binascii
import en_main2
import de_main2
reload(sys)
sys.setdefaultencoding('utf-8')

###########################################################################
## Class gui_main
###########################################################################

class gui_main( wx.Frame ):

	def __init__ (self):
		wx.Frame.__init__(self, parent=None, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 500,400 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		self.panelNum = 1
		self.login_pa()
		self.Show()

	def login_background(self, event):
		dc = event.GetDC()
		if not dc:
			dc = wx.ClientDC(self)
			rect = self.GetUpdateRegion().GetBox()
			dc.SetClippingRect(rect)
		dc.Clear()
		#image = wx.Image("2.png",wx.BITMAP_TYPE_PNG).ConvertToBitmap()
		#bmp = image.Rescale(500,400)
		#wx.StaticBitmap(panel,-1,image)
		bmp = wx.Bitmap("2.jpg")
		dc.DrawBitmap(bmp,0,0)


	def login_pa( self ):

		#wx.Frame.login_la ( self, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 400,400 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		self.login_panel = wx.Panel(self,pos=(0,0),size=(500,400))
		#self.panelNum = 2
		font = wx.Font(14, wx.SCRIPT, wx.NORMAL, wx.NORMAL, False)

		#self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.line1_la = wx.StaticLine( self.login_panel, -1, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer1.Add( self.line1_la, 0, wx.EXPAND |wx.ALL, 5 )
		
		gSizer1 = wx.GridSizer( 2, 2, 0, 0 )
		
		self.ac_la = wx.StaticText( self.login_panel, -1, u"用户名", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.ac_la.Wrap( -1 )
		
		gSizer1.Add( self.ac_la, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 35 )
		
		self.ac_txt = wx.TextCtrl( self.login_panel, -1, "", pos = (0,0), size = (200,25), style = wx.TE_NOHIDESEL )
		self.ac_txt.SetForegroundColour('gray')
		self.ac_txt.SetFont(font)
		gSizer1.Add( self.ac_txt, 0, wx.TOP|wx.BOTTOM|wx.RIGHT, 35 )
		
		self.pw_la = wx.StaticText( self.login_panel, -1, u"密码", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.pw_la.Wrap( -1 )
		gSizer1.Add( self.pw_la, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 35 )
		
		self.pw_txt = wx.TextCtrl( self.login_panel, -1, '', pos = (0,0), size = (200,25), style = wx.TE_PASSWORD )
		self.pw_txt.SetForegroundColour('gray')
		content = self.pw_txt.GetValue()
		gSizer1.Add( self.pw_txt, 0, wx.TOP|wx.BOTTOM|wx.RIGHT, 35 )
		
		
		bSizer1.Add( gSizer1, 1, wx.EXPAND, 5 )
		
		self.button1 = wx.Button( self.login_panel, -1, u"确定", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1.Add( self.button1, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		self.button1.Bind( wx.EVT_BUTTON, self.click_next)
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )

		#绑定事件
		#if (content == '123456'):
		self.login_panel.Bind(wx.EVT_ERASE_BACKGROUND,self.login_background)

	def sureEvent(self, event):
		account = self.ac_txt.GetValue()
		pw = self.pw_txt.Getvalue()
		self.sureFunction(account,pw)
		self.Destroy()
		pass

		#回调接口
	def loginFunc(self,account,pw):
		accout,pw



	def click_next(self, event):
		#关闭控件
		self.login_panel.Destroy()
		self.MyPanel1()
		
###########################################################################

	def MyPanel1( self ):
		#wx.Panel.MyPanel1 ( self, id = -1, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL )
		self.panelNum = 2
		self.mypanel1_panel = wx.Panel(self, pos=(0,0),size =(500,400))
		#字体（大小，字体DECORATIVE，斜度，醒目程度）
		font1 = wx.Font(25, wx.ROMAN, wx.ITALIC, wx.LIGHT) 
		font2 = wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.NORMAL) 
		font3 = wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.NORMAL) 

		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		self.wel_la = wx.StaticText( self.mypanel1_panel, -1, u"  Welcome to the system~", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.wel_la.Wrap( -1 )
		self.wel_la.SetFont(font1) 
		self.wel_la.SetForegroundColour("#E6E6FA")
		bSizer2.Add( self.wel_la, 0, wx.ALL, 5 )
		#竖直的一行两列，纵横向间距

		gSizer2 = wx.GridSizer( 2, 2, 0, 0 )
		
		self.en_la = wx.StaticText( self.mypanel1_panel, -1, u"     PART 1", pos=(100,100), size=(150,30))
		self.en_la.SetForegroundColour("#EAEAEA") 
		self.en_la.SetFont(font2) 
		#self.en_la.SetBackgroundColour("#EAEAEA")
		#self.en_la.Wrap( -1 )
		gSizer2.Add( self.en_la, 0, wx.LEFT|wx.TOP, 70 )
		
		self.de_la = wx.StaticText( self.mypanel1_panel, -1, u"     PART 2", pos=(0,100), size=(150,30))
		self.de_la.SetForegroundColour("#4D4D4D") 
		self.de_la.SetFont(font2) 
		#self.de_la.SetBackgroundColour("#EAEAEA")
		self.de_la.Wrap( -1 )
		gSizer2.Add( self.de_la, 0, wx.RIGHT|wx.TOP, 70 )

		self.button_en = wx.Button( self.mypanel1_panel, -1, u"水印嵌入", pos=(0,100), size=(150,50) ) 
		self.button_en.SetFont(font3)

		gSizer2.Add( self.button_en, 0, wx.LEFT|wx.BOTTOM, 70 )
		self.button_en.Bind( wx.EVT_BUTTON, self.click_en)

		self.button_de = wx.Button( self.mypanel1_panel, -1, u"水印提取", pos=(0,100), size=(150,50) ) 
		self.button_de.SetFont(font3) 
		gSizer2.Add( self.button_de, 0, wx.RIGHT|wx.BOTTOM, 70 )
		self.button_de.Bind( wx.EVT_BUTTON, self.click_de)

		bSizer2.Add( gSizer2, 1, wx.EXPAND, 5 )

		self.SetSizer( bSizer2 )
		self.Layout()

		#绑定事件
		self.mypanel1_panel.Bind(wx.EVT_ERASE_BACKGROUND,self.login_background)

	

	def click_en(self,event):
		self.mypanel1_panel.Destroy()
		self.MyPanel2()

	def click_de(self,event):
		self.mypanel1_panel.Destroy()
		self.MyPanel4()


###########################################################################


	def MyPanel2( self ):
		#wx.Panel.MyPanel2 ( self, id = -1, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL )
		self.panelNum = 3
		self.mypanel2_panel = wx.Panel(self,pos=(0,0),size =(500,400))
		font1 = wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.LIGHT) 
		font2 = wx.Font(16, wx.ROMAN, wx.ITALIC, wx.LIGHT) 
		font3 = wx.Font(12, wx.ROMAN, wx.ITALIC, wx.LIGHT) 
		
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		self.panel2_la = wx.StaticText( self, wx.ID_ANY, u"  Please choose the picture", pos=(100,100),size=(50,50))
		self.panel2_la.SetFont(font2) 
		self.panel2_la.SetForegroundColour("#F7F7F7")
		bSizer3.Add( self.panel2_la, 0, wx.ALL|wx.EXPAND, 5 )
		
		gSizer3 = wx.GridSizer( 1, 2, 0, 0 )
		
		self.docu_la = wx.StaticText( self, wx.ID_ANY, u"   请选择图片文件：", pos=(0,0),size=(250,100) )
		self.docu_la.SetFont(font3) 
		self.docu_la.SetForegroundColour("#F7F7F7")
		self.docu_la.Wrap( -1 )
		gSizer3.Add( self.docu_la, 0, wx.ALL, 5 )
		
		m_comboBox1Choices = [ u"2px_黑体",u"2px_宋体",u"醉翁亭记", u"小石潭记", u"放鹤亭记", u"石钟山记",u"口技",u"前赤壁赋",u"岳阳楼记",u"核舟记"]

		self.m_comboBox1 = wx.ComboBox( self, -1, u"请选择文件", wx.DefaultPosition, wx.DefaultSize, m_comboBox1Choices, 0 )
		gSizer3.Add( self.m_comboBox1, 0, wx.ALL, 5 )
		
		
		bSizer3.Add( gSizer3, 1, wx.EXPAND, 5 )
		
		self.in_la = wx.StaticText( self, -1, u"  请输入嵌入信息", pos=(100,100),size=(300,20))
		self.in_la.Wrap( -1 )
		bSizer3.Add( self.in_la, 0, wx.ALL, 5 )
		
		self.en_txt = wx.TextCtrl( self, -1, wx.EmptyString, pos=(100,100),size=(350,130),style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
		bSizer3.Add( self.en_txt, 1, wx.EXPAND|wx.ALL, 5 )
		
		gSizer4 = wx.GridSizer( 1, 2, 0, 0 )
		
		self.button3 = wx.Button( self, -1, u"<-返回", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer4.Add( self.button3, 0, wx.ALL|wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT, 5 )
		
		self.button4 = wx.Button( self, -1, u"确定", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer4.Add( self.button4, 0, wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		
		bSizer3.Add( gSizer4, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer3 )
		self.Layout()
		self.m_comboBox1.Bind( wx.EVT_COMBOBOX, self.OnCombo)
		self.en_txt.Bind( wx.EVT_TEXT, self.input_info )
		self.button3.Bind( wx.EVT_BUTTON, self.back_click )
		self.button4.Bind( wx.EVT_BUTTON, self.click_next2 )
		

		#self.bro = wx.StaticText( self.mypanel2_panel, -1, u"浏览文件夹", pos=(100,100), size=(100,30),style = wx.TE_MULTILINE)
		#self.btn_bro = wx.Button(self.mypanel2_panel,label = "Open a File")
		#self.btn_bro.SetForegroundColour("#F7F7F7") 
		#self.btn_bro.SetFont(font2) 
		#gSizer3.Add(self.btn_bro,0,wx.ALL,5)


		#绑定事件
		self.mypanel2_panel.Bind(wx.EVT_ERASE_BACKGROUND,self.login_background)

	def transfer_to_bin(self, s):
		bin = lambda n:(n > 0) and (bin(n/2) + str(n%2)) or ''   
		s_16 = binascii.b2a_hex(s)  
		s_10 = int(s_16,16)  
		s_2 = bin(s_10) 
		s_2 = '0' + s_2 
		return s_2 


	def OnCombo(self,event):
		#GetCurrentSelection ()
		self.pic = self.m_comboBox1.GetValue()
		pic1 = self.transfer_to_bin(self.pic)
		self.mask = pic1[:8]
		print 'self.mask=',self.mask
		

	def input_info( self, event):
		info = self.en_txt.GetValue()
		info1 = self.transfer_to_bin(info)
		wii = pickle.dumps(info1)
		f = open(self.pic + '1.txt','w')
		f.write(wii)
		f.close()
		self.info1 = info1
		#简单同位加密操作
		i = 0
		txt = ''
		for x in info1:
			if i == 8:
				i = 0
			m = int(x) ^ int(self.mask[i])
			txt += str(m)
			i += 1
		self.cc_e = txt


	def click_next2( self, event ):
		c = en_main2.cuttt(self.cc_e,self.pic)
		cc = c.output()
		print 'cc=',cc
		self.cc = cc

		self.mypanel2_panel.Destroy()
		self.MyPanel3()
		
	
	def back_click( self, event ):
		if not self.panelNum == 1:
			if self.panelNum == 3:
				self.mypanel2_panel.Destroy()
			if self.panelNum == 4:
				self.mypanel3_panel.Destroy()
			if self.panelNum == 5:
				self.mypanel4_panel.Destroy()
			if self.panelNum == 6:
				self.mypanel5_panel.Destroy()
			self.panelNum = 2
			self.MyPanel1()
			


	def MyPanel3( self ):
		#wx.Panel.MyPanel3 ( self, id = -1, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL )
		self.panelNum = 4
		self.mypanel3_panel = wx.Panel(self,pos=(0,0),size =(500,400))
		font1 = wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.LIGHT) 
		font2 = wx.Font(24, wx.ROMAN, wx.ITALIC, wx.LIGHT) 
		font3 = wx.Font(12, wx.ROMAN, wx.ITALIC, wx.LIGHT) 

		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		self.ok_la1 = wx.StaticText( self, -1, u"   ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.ok_la1.Wrap( -1 )
		bSizer4.Add( self.ok_la1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

		self.info_la = wx.StaticText( self.mypanel3_panel, -1, u"  原信息流", pos=(100,100), size=(380,20) )
		self.info_la.SetForegroundColour("#F7F7F7")
		self.info_la.Wrap( -1 )
		bSizer4.Add( self.info_la, 0, wx.TOP|wx.RIGHT, 20 )
		
		self.info_txt = wx.TextCtrl( self.mypanel3_panel, -1, self.info1, pos=(100,100), size=(400,50),style=wx.TE_MULTILINE)
		bSizer4.Add( self.info_txt, 0, wx.ALL|wx.EXPAND, 5 )

		self.info_la = wx.StaticText( self.mypanel3_panel, -1, u"  加密信息流", pos=(100,100), size=(380,20) )
		self.info_la.SetForegroundColour("#F7F7F7")
		self.info_la.Wrap( -1 )
		bSizer4.Add( self.info_la, 0, wx.TOP|wx.RIGHT, 20 )
		
		self.info_txt = wx.TextCtrl( self.mypanel3_panel, -1, self.cc_e, pos=(100,100), size=(400,50),style=wx.TE_MULTILINE)
		bSizer4.Add( self.info_txt, 0, wx.ALL|wx.EXPAND, 5 )

		self.ok_la = wx.StaticText( self, -1, u"---------图片---已生成---------", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.ok_la.SetFont(font2) 
		self.ok_la.SetForegroundColour("#4F94CD")
		self.ok_la.Wrap( -1 )
		bSizer4.Add( self.ok_la, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 15 )
		
		gSizer5 = wx.GridSizer( 1, 2, 0, 0 )
		
		self.button5 = wx.Button( self, -1, u"<-返回", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer5.Add( self.button5, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_BOTTOM, 5 )
		
		self.button6 = wx.Button( self, -1, u"完成", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer5.Add( self.button6, 0, wx.ALL|wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT, 5 )
		
		
		bSizer4.Add( gSizer5, 1, wx.EXPAND, 5 )
		
	
		self.SetSizer( bSizer4 )
		self.Layout()

		#绑定事件
		self.button5.Bind( wx.EVT_BUTTON, self.back_click )
		#self.button6.Bind( wx.EVT_BUTTON, self.click_over )
		self.mypanel3_panel.Bind(wx.EVT_ERASE_BACKGROUND,self.login_background)
	
	
	def MyPanel4( self ):
		#wx.Panel.MyPanel21 ( self, id = -1, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL )
		self.mypanel4_panel = wx.Panel(self,pos=(0,0),size =(500,400))
		self.panelNum = 5
		font1 = wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.LIGHT) 
		font2 = wx.Font(16, wx.ROMAN, wx.ITALIC, wx.LIGHT) 
		font3 = wx.Font(12, wx.ROMAN, wx.ITALIC, wx.LIGHT) 

		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		self.panel4_la = wx.StaticText( self, wx.ID_ANY, u"  Please choose the picture", pos=(100,100),size=(50,50))
		self.panel4_la.SetFont(font2) 
		self.panel4_la.SetForegroundColour("#F7F7F7")
		bSizer5.Add( self.panel4_la, 0, wx.ALL|wx.EXPAND, 5 )
		
		gSizer6 = wx.GridSizer( 1, 2, 0, 0 )
		
		self.de_la = wx.StaticText( self, wx.ID_ANY, u"   请选择图片文件：", pos=(0,0),size=(250,100) )
		self.de_la.SetFont(font3) 
		self.de_la.SetForegroundColour("#F7F7F7")
		self.de_la.Wrap( -1 )
		gSizer6.Add( self.de_la, 0, wx.ALL, 5 )
		
		m_comboBox2Choices = [ u"2px_黑体",u"2px_宋体",u"醉翁亭记", u"小石潭记", u"放鹤亭记", u"石钟山记",u"口技",u"前赤壁赋",u"岳阳楼记",u"核舟记"]

		self.m_comboBox2 = wx.ComboBox( self, -1, u"请选择文件", wx.DefaultPosition, wx.DefaultSize, m_comboBox2Choices, 0)
		gSizer6.Add( self.m_comboBox2, 0, wx.ALL, 5 )
		
		
		bSizer5.Add( gSizer6, 1, wx.EXPAND, 5 )
		
		self.out_la = wx.StaticText( self, -1, u"  正在解密中......", pos=(100,100),size=(300,20))
		self.out_la.SetFont(font3) 
		#self.out_la.SetForegroundColour("#F7F7F7")
		self.out_la.Wrap( -1 )
		bSizer5.Add( self.out_la, 0, wx.ALL, 5 )
		
		gSizer7 = wx.GridSizer( 1, 2, 0, 0 )
		
		self.button7 = wx.Button( self, -1, u"<-返回", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer7.Add( self.button7, 0, wx.ALL|wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT, 5 )
		
		self.button8 = wx.Button( self, -1, u"提取", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer7.Add( self.button8, 0, wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		
		bSizer5.Add( gSizer7, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer5 )
		self.Layout()

		#绑定事件
		self.mypanel4_panel.Bind(wx.EVT_ERASE_BACKGROUND,self.login_background)
		self.m_comboBox2.Bind( wx.EVT_COMBOBOX, self.OnCombo1)
		self.button7.Bind( wx.EVT_BUTTON, self.back_click )
		self.button8.Bind( wx.EVT_BUTTON, self.click_sure )
#！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
	
	def transfer_to_str(self, wii):
		s_2 = wii
		s_10 = int(s_2,2)  
		s_16 = '%x'%(s_10)  
		s = binascii.a2b_hex(s_16)  
		return s


	def OnCombo1(self,event):
		#GetCurrentSelection ()
		self.pic_d = self.m_comboBox2.GetValue()
		pic1 = self.transfer_to_bin(self.pic_d)
		self.mask1 = pic1[:8]
		print 'self.mask=',self.mask1


	def Trate(self,wo,wi):
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
		return rate,wii


	def click_sure(self,event):
		f = open(self.pic_d + '.txt','r')
		w_po1 = f.read()
		self.w_po = pickle.loads(w_po1)
		f.close()
		d = de_main2.extracttt(self.w_po,self.pic_d)
		self.wii = d.output1()
		info1 = self.wii
		#简单同位加密操作
		i = 0
		txt = ''
		for x in info1:
			if i == 8:
				i = 0
			m = int(x) ^ int(self.mask1[i])
			txt += str(m)
			i += 1
		self.wi_d = txt
		#self.recover_info = self.transfer_to_str(txt)
		f = open(self.pic_d + '1.txt','r')
		self.wi = pickle.loads(f.read())
		f.close()
		self.rate,self.wi_d = self.Trate(self.wi,self.wi_d)
		self.mypanel4_panel.Destroy()
		self.MyPanel5()

	
	def MyPanel5 ( self ):
	
		#wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL )
		self.mypanel5_panel = wx.Panel(self,pos=(0,0),size =(500,400))
		self.panelNum = 6
		font1 = wx.Font(20, wx.DEFAULT, wx.ITALIC, wx.LIGHT) 
		font2 = wx.Font(16, wx.ROMAN, wx.ITALIC, wx.LIGHT) 
		font3 = wx.Font(12, wx.ROMAN, wx.ITALIC, wx.LIGHT) 

		bSizer6 = wx.BoxSizer( wx.VERTICAL )
		
		self.an_la = wx.StaticText( self, -1, u"---------结果分析--------", pos=(100,100), size=(100,25) )
		self.an_la.SetFont(font1) 
		self.an_la.SetForegroundColour("#F7F7F7")
		self.an_la.Wrap( -1 )
		bSizer6.Add( self.an_la, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 10 )
		
		self.mask_la = wx.StaticText( self, -1, u"   掩码信息", pos=(100,100), size=(380,20) )
		self.mask_la.SetForegroundColour("#F7F7F7")
		self.mask_la.Wrap( -1 )
		bSizer6.Add( self.mask_la, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.mask_txt = wx.TextCtrl( self, -1, self.mask1, pos=(100,100), size=(380,30),style=wx.TE_MULTILINE)
		bSizer6.Add( self.mask_txt, 0, wx.ALL|wx.EXPAND, 5 )
		
		#gSizer8 = wx.GridSizer( 2, 2, 0, 0 )
		
		self.wi_la = wx.StaticText( self, -1, u"   原信息流", pos=(100,100), size=(170,20) )
		self.wi_la.Wrap( -1 )
		bSizer6.Add( self.wi_la, 0, wx.EXPAND|wx.ALL|wx.ALIGN_BOTTOM, 5 )
				
		self.wi_txt = wx.TextCtrl( self, -1, self.wi, pos=(100,100), size=(150,30),style=wx.TE_MULTILINE )
		bSizer6.Add( self.wi_txt, 0, wx.ALL|wx.EXPAND|wx.ALIGN_TOP, 5 )

		self.wi_d_la = wx.StaticText( self, -1, u"   解码信息流", pos=(100,100), size=(170,20) )
		self.wi_d_la.Wrap( -1 )
		bSizer6.Add( self.wi_d_la, 0, wx.EXPAND|wx.ALL|wx.ALIGN_BOTTOM, 5 )
		
		self.wi_d_txt = wx.TextCtrl( self, -1, self.wi_d, pos=(100,100), size=(150,30),style=wx.TE_MULTILINE )
		bSizer6.Add( self.wi_d_txt, 0, wx.ALL|wx.EXPAND|wx.ALIGN_TOP, 5 )
		
		self.rate_la = wx.StaticText( self, -1, u"   提取率", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.rate_la.Wrap( -1 )
		bSizer6.Add( self.rate_la, 0, wx.ALL, 5 )
		
		self.rate_txt = wx.TextCtrl( self, -1, self.rate , pos=(100,100), size=(300,30),style=wx.TE_MULTILINE )
		bSizer6.Add( self.rate_txt, 0, wx.ALL|wx.EXPAND, 15 )
		
		gSizer9 = wx.GridSizer( 1, 2, 0, 0 )
		
		self.button9 = wx.Button( self, -1, u"退出", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer9.Add( self.button9, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_BOTTOM, 5 )
		
		self.button8 = wx.Button( self, -1, u"确定", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer9.Add( self.button8, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_BOTTOM, 5 )
		
		
		bSizer6.Add( gSizer9, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer6 )
		self.Layout()

		#绑定事件
		self.mypanel5_panel.Bind(wx.EVT_ERASE_BACKGROUND,self.login_background)
		self.button8.Bind( wx.EVT_BUTTON, self.back_click )
		self.button9.Bind(wx.EVT_BUTTON, self.click_exit)



	def click_exit(self,event):
		if self.panelNum == 5:
			self.mypanel4_panel.Destroy()
		if self.panelNum == 4:
			self.mypanel3_panel.Destroy()
		if self.panelNum == 6:
			self.mypanel5_panel.Destroy()
		self.panelNum = 1
		self.login_pa()
			#self.MyPanel1()

def __del__( self ):
		pass

	

	
if __name__ == '__main__':
	app = wx.App()
	#gui界面的class
	frame = gui_main()
	#frame.Show()
	app.MainLoop()




