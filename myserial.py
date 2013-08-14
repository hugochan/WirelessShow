#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import sys

class myserial():
	"""serial for processing com data"""
	MyBaudrate = 9600
	data = []
	def __init__(self):
		try:
			self.ser = serial.Serial(port='COM1', baudrate=self.MyBaudrate, bytesize=8, 
				timeout=None) #Open a COM
		except:
			print "Error: Failed to Open COM!"
			sys.exit()
		print "Succeeded to Open COM!"

		self.ser.close() #close a COM
		self.ser.open() #open a COM
		self.COM = self.ser.portstr #
		#ser.write('h') #
		eachdata = self.ser.read()          # read one byte  
		while eachdata!=' ':
			int_eachdata = ord(eachdata)#covert char to int
			self.data.append(int_eachdata)
			#print int_eachdata
			eachdata = self.ser.read()          # read one byte  
		#print self.data
		self.ser.close() #close a COM
	
	def returndata(self):
		return self.data

if __name__ == '__main__':
	serial = myserial()
	data = serial.returndata()
	print data