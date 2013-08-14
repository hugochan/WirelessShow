#!/usr/bin/env python
# -*- coding: utf-8 -*-
import wx
import wx.html
from SketchWindow import SketchWindow
from ControlPanel import ControlPanel

class WirelessShowFrame(wx.Frame):
	def __init__(self, parent=None):
		self.title = 'WirelessShow'
		wx.Frame.__init__(self, parent, -1, self.title,
					size=(800,600))
		self.sketch = SketchWindow(self, -1)
		self.event = EventHandler()#实例化事件处理器类
		self.createPanel()
		self.createMenuBar()
		self.initStatusBar()
		
		self.sketch.Bind(wx.EVT_MOTION, self.OnSketchMotion)

	def createPanel(self):
		controlPanel = ControlPanel(self, -1)
		box = wx.BoxSizer(wx.HORIZONTAL)
		box.Add(controlPanel, 0, wx.EXPAND)
		box.Add(self.sketch, 1, wx.EXPAND)
		self.SetSizer(box)

	def menuData(self): #2 菜单数据
		return [('&File', (
			('About...', 'Show about window', self.event.OnAbout),
			('&Quit', 'Quit', self.OnCloseWindow)))]

	def createMenuBar(self):
		menuBar = wx.MenuBar()
		for eachMenuData in self.menuData():
			menuLabel = eachMenuData[0]
			menuItems = eachMenuData[1]
			menuBar.Append(self.createMenu(menuItems), menuLabel)
		self.SetMenuBar(menuBar)

	def createMenu(self, menuData):
		menu = wx.Menu()
		#3 创建子菜单
		for eachItem in menuData:
			if len(eachItem) == 2:
				label = eachItem[0]
				subMenu = self.createMenu(eachItem[1])
				menu.AppendMenu(wx.NewId(), label, subMenu)
			else:
				self.createMenuItem(menu, *eachItem)
		return menu

	def createMenuItem(self, menu, label, status, handler,
			kind=wx.ITEM_NORMAL):
		if not label:
			menu.AppendSeparator()
			return
		menuItem = menu.Append(-1, label, status, kind)#4 使用kind创建菜单项
		self.Bind(wx.EVT_MENU, handler, menuItem)
	
	def initStatusBar(self):
		ScrollPosxtext1 = str(100)
		ScrollPosxtext2 = str(200)
		self.statusbar = self.CreateStatusBar()
		self.statusbar.SetFieldsCount(2)
		self.statusbar.SetStatusWidths([-1,-1])
		#self.SetStatusText('ScrollPos:(%s,%s)'%(ScrollPosxtext1,ScrollPosxtext2))

	#some small handler
	def OnSketchMotion(self, event):
		#鼠标移动更新状态栏中鼠标坐标
		self.statusbar.SetStatusText('MousePos:'+ str(event.GetPositionTuple()),0)
		event.Skip()

	def OnCloseWindow(self, event):
		self.Destroy()
	
class EventHandler():
	"""EventHandler for event"""
	def __init__(self):
		pass

	def OnAbout(self, event):
		dlg = WirelessShowAbout()
		dlg.ShowModal()
		dlg.Destroy()

class WirelessShowAbout(wx.Dialog):
	text = '''
<html>
<body bgcolor="#ACAA60">
<center><table bgcolor="#455481" width="100%" cellspacing="0"
cellpadding="0" border="1">
<tr>
	<td align="center"><h1>WirelessShow!</h1></td>
</tr>
</table>
</center>
<p><b>WirelessShow</b> is a demonstration program for Wireless Pen.  It is based on the SuperDoodle demo included with wxPython,
available at http://www.wxpython.org/
</p>

<p><b>SuperDoodle</b> and <b>wxPython</b> are brought to you by
<b>Robin Dunn</b> and <b>Total Control Software</b>, Copyright
&copy; 1997-2006.</p>
</body>
</html>
'''

	def __init__(self, parent=None):
		wx.Dialog.__init__(self, parent, -1, 'About WirelessShow',
					size=(440, 400) )

		html = wx.html.HtmlWindow(self)
		html.SetPage(self.text)
		button = wx.Button(self, wx.ID_OK, "Okay")

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(html, 1, wx.EXPAND|wx.ALL, 5)
		sizer.Add(button, 0, wx.ALIGN_CENTER|wx.ALL, 5)

		self.SetSizer(sizer)
		self.Layout()

class WirelessShowApp(wx.App):
	def OnInit(self):
		bmp = wx.Image("splash.jpg").ConvertToBitmap()
		wx.SplashScreen(bmp, wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT,
			1000, None, -1)
		wx.Yield()

		frame = WirelessShowFrame()
		frame.Show(True)
		self.SetTopWindow(frame)
		return True

if __name__ == '__main__':
	app =WirelessShowApp(redirect=False)
	app.MainLoop()