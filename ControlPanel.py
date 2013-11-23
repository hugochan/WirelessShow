#!/usr/bin/env python
# -*- coding: utf-8 -*-
import wx
import cPickle
import os
from wx.lib import buttons
from myserial import myserial
from DataProcessModle import DataProcess
import pdb

class ControlPanel(wx.Panel):

	"""class for ControlPanel"""
	BMP_SIZE = 16
	BMP_BORDER = 3
	SPACING = 4
	datafilename = ''
	sketchfilename= ''
	
	wildcarddf = "Data files (*.df)|*.df|All files (*.*)|*.*"
	wildcardsketch = "Sketch files (*.sketch)|*.sketch|All files (*.*)|*.*"
	
	def __init__(self, parent, ID):
		wx.Panel.__init__(self, parent, ID, style=wx.RAISED_BORDER)
		buttonSize = (self.BMP_SIZE + 2 * self.BMP_BORDER,####??????Unused!!!
				self.BMP_SIZE + 2 * self.BMP_BORDER)		
		self.parent = parent
		self.ControlButtonList = []
		for eachbutton in self.buttonData():
			self.ControlButtonList.append(self.createControlButton(self, 
								*eachbutton))
		self.layout(self.ControlButtonList)
	
	def buttonData(self):#按钮数据
		return(('      New Sketch      ', 'New Sketch', 10, self.New_Sketch),#label, name, BezelWidth, handler
			('      Save Sketch      ','Save Sketch', 10, self.OnSave_Sketch),
			('Import&Show Sketch', 'Import&Show Sketch',10, self.OnOpen_Sketch),
			(' Recv&Save Datafile  ', 'Recv&Save Datafile', 10, self.Recv_Save_Datafile), 
			('     Import Datafile    ', 'Import Datafile', 10, self.Import_Datafile))

	def createControlButton(self, parent, label, name, BezelWidth, handler):
		"""单个控制按钮生成方法"""
		self.controlIdMap = {}
		self.controlButtons = {}
		#button = buttons.GenBitmapTextButton(parent, label='Recv&Save', name="genbutton")
		#button.SetBitmapLabel("D:\Learning_Library\Python\splash.png")
		button = buttons.GenButton(parent, label=label, name=name)
		button.SetBezelWidth(BezelWidth)
		button.SetUseFocusIndicator(False)
		self.Bind(wx.EVT_BUTTON, handler, button)
		return button

	def layout(self, ControlButtonList):
		"""控制按钮布局管理方法"""
		box = wx.BoxSizer(wx.VERTICAL)
		for eachControlButton in ControlButtonList:
			box.Add(eachControlButton, 1, wx.ALL, self.SPACING)
		self.SetSizer(box)
		box.Fit(self)

	def New_Sketch(self, event): #????
		#print 'NewSketch'
		self.sketchfilename = ''
		#使得新建后拖动滚动条触发事件处理器后无线条绘出
		self.parent.sketch.logicaldata = []
		#使得新建后保存图像为空白
		self.parent.sketch.logicallines = []
		#使得新建后不通过拖动滚动条触发事件处理器仍无线条绘出
		self.parent.sketch.devicelines = []
		#新建后执行刷新，空闲时进行具体刷新操作
		self.parent.sketch.reInitBuffer = True
		#event.Skip()

	def Import_Datafile(self, event):
		LogicalData = self.ReadDataFlie()
		#逻辑坐标整体平移
		LogicalData = self.LogicalDataOffset(LogicalData)
		self.parent.sketch.drawline(LogicalData)
		#event.Skip()

	def Recv_Save_Datafile(self, event):
		#######################################
		#shankhand
		#######################################
		print "console<<<start a shankhand~~~~"
		#shankhand begin from reading information from lower computer
		serialHandle = myserial(myTimeout=10)#max 10 secondes waiting
		serialdata = serialHandle.read(mySize=6)#shankhand sign:"ready?" total length is exactly 6
		#comfirm the shankhand sign:"ready?"
		if serialdata != "ready?":
			shankhandSuccess = False
			print "console<<<shankhand Failure!"
		else:
			#sends the shankhand ack to lower computer
			serialHandle.write("ok! ")#the end of the sign must be a space character for a easy recv
			#recvs the shankhand ack2(index) from lower computer
			serialHandle = myserial(myTimeout=1)
			serialdata = serialHandle.read(mySize=1000)
			indexRecg = "index"#the first five bytes are recognition sign "index" 
			if serialdata[0:len(indexRecg)] != indexRecg:
				shankhandSuccess = False
				print "console<<<shankhand Failure!"
			else:
				shankhandSuccess = True
				print "console<<<shankhand Success!"
				
				#############################################
				#interConsole to display and choose a segment 
				#############################################
				print "console<<<index list for choosing~~~~"
				#retrive indexList from every four bytes
				tempIndexElement = []
				tempIndexList = []
				indexList = []# a index list
				i = 0
				uniIndexLength = 3#every 3 elements make up an integral index 
				for eachserialdata in serialdata[len(indexRecg):]:
					tempIndexElement.append(ord(eachserialdata))
					if (i+1) % 4 == 0:#every 4 bytes make up an integral element
						tempIndexList.append((tempIndexElement[0]<<24)+(tempIndexElement[1]<<16)+(tempIndexElement[2]<<8)+tempIndexElement[3])
						tempIndexElement = []
						if (i+1) % (uniIndexLength*4) == 0:
							indexList.append(tempIndexList)
							tempIndexList = []
					i += 1
				#display the index list
				#print indexList
				indexCount = 0
				for eachIndexList in indexList:
					print str(indexCount) + "、name:" + str(eachIndexList[1]) + " size:" +  str(eachIndexList[2]) + "bytes address:" + str(eachIndexList[0])
					indexCount += 1
				if indexCount == 0:
					print "console<<<no index list for choosing~~~"
					print "console<<<cancel~~~~"
				else:
					#choose an index list
					print "console<<<choose a segment from 0 to " + str(indexCount-1) + "(-1 for cancel)~~~~" 
					indexChoose = 0
					chooseFlag = False
					while indexChoose != -1:
						# pdb.set_trace()
						indexChoose = raw_input('> ')
						try:
							indexChoose = int(indexChoose)
						except:
							print "console<<<please input a valid choice~~~~"
							continue
						if indexChoose == -1:
							print "console<<<cancel~~~~"
							break
						if indexChoose not in range(indexCount):
							print "console<<<please input a valid choice~~~~"
							continue
						chooseFlag = True
						break

					if chooseFlag:
						serialHandle.write(str(indexChoose)+" ")#choose No.0 segment, the end of the sign must be a space character for a easy recv
						# pdb.set_trace()
						serialdata = serialHandle.read(mySize=1000)
						accSerialData = []
						for eachserialdata in serialdata:
							accSerialData.append(ord(eachserialdata))
						# pdb.set_trace()#debug
						print "console<<<No.0 segment acceleration datas~~~"
						print accSerialData

						#change the unsigned acceleration datas to shift datas
						shift = DataProcess(accSerialData).returndata()
						print 'shift' 
						print shift
						
						#save the acc data file
						count = 0
						dlg = wx.FileDialog(self, 'Save DataFile as...', os.getcwd(),
										style=wx.SAVE | wx.OVERWRITE_PROMPT,
										wildcard = self.wildcarddf)
						if dlg.ShowModal() == wx.ID_OK:
							datafilename = dlg.GetPath()
							self.datafilename = datafilename
							
							f = open(self.datafilename, 'w')
							while count < len(shift)-1:
								f.write(shift[count])
								f.write(' ')
								count = count + 1
							f.write(shift[count])
							f.close()

							self.parent.SetTitle(self.parent.title + ' -- ' + self.datafilename)
							dlg.Destroy()

		

	def ReadDataFlie(self):
		LogicalData = []
		flag = 0
		
		dlg = wx.FileDialog(self, 'Import Datafile...', os.getcwd(),
						style=wx.OPEN, wildcard=self.wildcarddf)
		if dlg.ShowModal() == wx.ID_OK:
			self.datafilename = dlg.GetPath()
			f = open(self.datafilename,'rb')
			f.seek(0,0)#将指针移至起始位置
			LogicalData_str = f.read()
			f.close()
			if not f.closed:
				print 'Error: The file is not closed!'

			for eachData in LogicalData_str.split(' '):#将字符串文件中的整型数据提取出
				if not flag:
					LogicalData_xpos = int(eachData)
				else: 
					LogicalData_ypos = int(eachData)
				if flag:	LogicalData.append((LogicalData_xpos, LogicalData_ypos))
				flag = (flag + 1) % 2
		

			self.parent.SetTitle(self.parent.title + ' -- ' + self.datafilename)
			dlg.Destroy()
		return LogicalData
		

	def SaveSketchFile(self):
		if self.sketchfilename:
			data = self.parent.sketch.GetLinesData()
			f = open(self.sketchfilename, 'w')
			cPickle.dump(data, f)
			f.close()

	def ReadSketchFile(self):
		if self.sketchfilename:
			try:
				f = open(self.sketchfilename, 'r')
				data = cPickle.load(f)
				f.close()
				self.parent.sketch.SetLinesData(data)
			except cPickle.UnpicklingError:
				wx.MessageBox("%s is not a sketch file." % self.sketchfilename,
						"oops!", style=wx.OK|wx.ICON_EXCLAMATION)


	def OnOpen_Sketch(self, event):
		dlg = wx.FileDialog(self, 'Import&Show sketch file...', os.getcwd(),
						style=wx.OPEN, wildcard=self.wildcardsketch)
		if dlg.ShowModal() == wx.ID_OK:
			self.sketchfilename = dlg.GetPath()
			self.ReadSketchFile()
			self.parent.SetTitle(self.parent.title + ' -- ' + self.sketchfilename)
		dlg.Destroy()
		#event.Skip()

	def OnSave_Sketch(self, event):#????
		if not self.sketchfilename:
			#print 'OnSaveAs'
			self.OnSaveAs_Sketch(event)
		else:
			#print 'SaveSketchFile'
			self.SaveSketchFile()
		#event.Skip()

	def OnSaveAs_Sketch(self, event):
		dlg = wx.FileDialog(self, 'Save sketch as...', os.getcwd(),
						style=wx.SAVE | wx.OVERWRITE_PROMPT,
						wildcard = self.wildcardsketch)
		if dlg.ShowModal() == wx.ID_OK:
			sketchfilename = dlg.GetPath()
			if not os.path.splitext(sketchfilename)[1]:
				sketchfilename = sketchfilename + '.sketch'
			self.sketchfilename = sketchfilename
			self.SaveSketchFile()
			self.parent.SetTitle(self.parent.title + ' -- ' + self.sketchfilename)
		dlg.Destroy()

	def LogicalDataOffset(self, Data):
		"""实现逻辑坐标的整体平移，以在合适位置画图"""
		x_Offset = 0
		y_Offset = 0
		uni_Offset = 100
		LogicalDataOffset = []
		for eachData in Data:#第一次遍历找到合适偏移量
			if x_Offset > eachData[0]:
				x_Offset = eachData[0]
			if y_Offset > eachData[1]:
				y_Offset = eachData[1]
		x_Offset = -x_Offset + uni_Offset
		y_Offset = -y_Offset + uni_Offset

		for eachData in Data:
			LogicalDataOffset.append((eachData[0] + x_Offset, eachData[1] + y_Offset))
		print 'LogicalDataOffset'
		print LogicalDataOffset
		return LogicalDataOffset

class ControlPanelFrame(wx.Frame):
	def __init__(self, parent):
		wx.Frame.__init__(self, parent, -1, 'ControlPanel Frame',
					size=(800,600))
		self.panel = ControlPanel(self, -1)
		

if __name__ == '__main__':
	app = wx.PySimpleApp()
	frame = ControlPanelFrame(None)
	frame.Show(True)
	app.MainLoop()