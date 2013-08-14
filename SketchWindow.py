#!/usr/bin/env python
# -*- coding: utf-8 -*-
import wx

class SketchWindow(wx.ScrolledWindow):
	def __init__(self, parent, ID):
		wx.ScrolledWindow.__init__(self, parent, ID)
		self.SetScrollbars(10, 10, 50000, 50000, xPos=0, yPos=0, #设置滚动条窗口
							 noRefresh=True)
		self.SetBackgroundColour('White')
		self.color = 'Black'
		self.thickness = 1
		self.pen = wx.Pen(self.color, self.thickness, wx.SOLID)
		self.logicaldata = []
		self.logicallines = []
		self.devicecurLine = []
		self.devicelines = []
		self.InitBuffer()
		
		self.Bind(wx.EVT_SIZE, self.OnSize)
		self.Bind(wx.EVT_IDLE, self.OnIdle)
		self.Bind(wx.EVT_PAINT, self.OnPaint)#窗口重绘
		self.Bind(wx.EVT_SCROLLWIN_THUMBRELEASE, self.OnSCROLLWIN_THUMBRELEASE)###????????

	def Data(self):
		return[(0,0),(100,500),(550,300),(300,10)]

	def logicaldata2devicedata(self, logicaldata):
		'''将逻辑坐标转换为设备坐标'''
		devicedata = []
		for eachdata in logicaldata:
			devicedata.append(self.CalcScrolledPosition(eachdata[0], eachdata[1]))
		return devicedata

	def data2curLine(self, data):
		'''将逻辑（设备）数据转换为逻辑（设备）线组'''
		self.curLine = []
		if data:
			pos = data[0]
			for eachpos in data:
				newPos = eachpos
				coords = pos + newPos
				pos = newPos
				self.curLine.append(coords)	
		return self.curLine

	def lines2data(self, lines):
		data = []
		for colour, thickness, curLine in lines:
			#pen = wx.Pen(colour, thickness, wx.SOLID)
			#dc.SetPen(pen)
			for coords in curLine:
				data.append((coords[0], coords[1])) 
			data.append((coords[2], coords[3]))
		return data

	def RefreshDevicelines(self):
		'''刷新设备线'''
		self.devicelines = []
		devicedata = self.logicaldata2devicedata(self.logicaldata)
		self.devicecurLine = self.data2curLine(devicedata)
		self.devicelines.append((self.color,
							self.thickness,
							self.devicecurLine))
		self.reInitBuffer = True
		#print self.devicecurLine
		return self.devicelines

	def InitBuffer(self):
		'''初始化设备上下文缓存'''
		size = self.GetClientSize()
		self.buffer = wx.EmptyBitmap(size.width, size.height)
		dc = wx.BufferedDC(None, self.buffer)
		dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
		dc.Clear()
		self.DrawLines(dc)
		self.reInitBuffer = False

	def GetLinesData(self):
		'''得到逻辑线'''
		return self.logicallines[:]

	def SetLinesData(self, lines):
		'''设置逻辑线'''
		self.logicallines = lines[:]
		self.logicaldata = self.lines2data(self.logicallines)
		self.RefreshDevicelines()
		self.reInitBuffer = True

	def drawline(self, data):
		'''根据给定的逻辑坐标列表画线'''
		self.logicaldata = data
		#生成逻辑线
		logicalcurLine = self.data2curLine(self.logicaldata)
		self.logicallines.append((self.color,
							self.thickness,
							logicalcurLine))
		#生成(刷新)设备线组
		self.RefreshDevicelines()

	def OnSCROLLWIN_THUMBRELEASE(self, event):
		'''滚动条事件（用户使用鼠标拖动滚动条
		   滚动不超过一页的范围，并释放鼠标后，
		   触发该事件）处理器，用于实现设备坐标更新'''
		self.RefreshDevicelines()

	def OnSize(self, event):
		'''窗口大小变化时使能更新缓存'''
		self.reInitBuffer = True

	def OnIdle(self, event):
		'''空闲时更新缓存'''
		if self.reInitBuffer:
			self.InitBuffer()
			self.Refresh(False)

	def OnPaint(self, event):
		'''重绘线条处理器'''
		dc = wx.BufferedPaintDC(self, self.buffer)

	def DrawLines(self, dc):
		'''画线'''
		for colour, thickness, line in self.devicelines:
			pen = wx.Pen(colour, thickness, wx.SOLID)
			dc.SetPen(pen)
			for coords in line:
				dc.DrawLine(*coords)

class SketchFrame(wx.Frame):
	def __init__(self, parent):
		wx.Frame.__init__(self, parent, -1, 'Sketch Frame',
					size=(800,600))
		self.sketch = SketchWindow(self, -1)
		#print self.sketch.CalcScrolledPosition(-1,-100)

if __name__ == '__main__':
	app = wx.PySimpleApp()
	frame = SketchFrame(None)
	frame.Show(True)
	app.MainLoop()