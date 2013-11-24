#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import sys

class myserial():
	"""serial for processing com data"""
	data = []
	def __init__(self, myBaudrate=19200, myTimeout=None):
		try:
			self.ser = serial.Serial(port='COM1', baudrate=myBaudrate, bytesize=8, 
				timeout=myTimeout) #set the timeout = 1 second
		except:
			print "upper Computer<<<Error: Failed to Open COM!"
			sys.exit()
		# print "upper Computer<<<Succeeded to Open COM!"
		self.ser.close() #close a COM
		# self.COM = self.ser.portstr
	
	def read(self, mySize=1):
		self.ser.open() #open a COM
		self.data = [] #empty the read list
		self.data = self.ser.read(size=mySize)
		# eachdata = self.ser.read(size=mySize)          # read one byte  
		# while eachdata != ' ':
		# 	int_eachdata = ord(eachdata)#covert char to int
		# 	self.data.append(int_eachdata)
		# 	#print int_eachdata
		# 	eachdata = self.ser.read()
		# 	print 'eachdata'
		# 	print eachdata
		self.ser.close() #close a COM
		return self.data
	
	def write(self, data):
		"""write a byte list through serial port """
		self.ser.open() #open a COM
		self.ser.write(data)
		# for eachdata in data:
		# 	if eachdata == ' ':
		# 		break
		# 	self.ser.write(eachdata)#space character must be and only be at the end
		self.ser.close() #close a COM

if __name__ == '__main__':
	serial = myserial()
	data = serial.read()
	print data
	serial.write("hello!")