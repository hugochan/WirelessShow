#!/usr/bin/env python
# -*- coding: utf-8 -*-

class DataProcess():
	"""docstring for DataProcess"""
	Shift_str = []
	Offset = 0#位移偏移
	del_t = 0.0025#采样周期2.5ms
	acc_rate = 176.22#加速度传感器精度18mg/digit,成都地区g=9.79m/s2,故acc_rate=176.22ms/s2,实际加速度值=acc_rate*accdata
	shi_rate = 4#实际1mm对应4像素点

	def __init__(self, AccData):
		count = 0
		acc_x = [0.0]
		acc_y = [0.0]
		shi_x = []
		shi_y = []
		for eachData in AccData:
			#将无符号整型转换为有符号整型(自行编写方法实现)
			signedint_eachData = self.unsigned2signed(eachData)
			#整型转换为浮点型(且换算成真实加速度值)
			if not count:
				acc_x.append(self.acc_rate*float(signedint_eachData))
			else:
				acc_y.append(self.acc_rate*float(signedint_eachData))
			count = (count + 1) % 2
		
		# print 'acc_x'
		# print acc_x
		# print 'acc_y'
		# print acc_y

		#通过加速度计算位移
		shi_x = self.acc2shi(acc_x)
		shi_y = self.acc2shi(acc_y)

		#将位移值转换为像素值
		shift_x = self.shi2shift(shi_x)
		shift_y = self.shi2shift(shi_y)

		#make an adjustment for good display
		count = 0
		Datalength = min(len(shift_x), len(shift_y))
		while count < Datalength:
			self.Shift_str.append(str(shift_x[count]))
			self.Shift_str.append(str(shift_y[count]))
			count += 1

	def shi2shift(self, Data):
		Shift = []
		for eachData in Data:
			#将位移值转换为像素值(已求整)
			Shift.append(int(self.shi_rate*eachData))
		# print 'Shift'
		# print Shift
		return Shift

	def acc2shi(self, Data):
		count = 0
		Datalength = len(Data)
		Acc = Data
		Vel = [0.0]
		Shi = [self.Offset] #位移偏置
		while count < Datalength - 1:
			#速度用浮点型参与运算，提高精度
			Vel.append(Vel[count] + ((Acc[count] + Acc[count + 1])/2)*self.del_t)
			#由速度求得位移
			Shi.append(Shi[count] + ((Vel[count] + Vel[count + 1])/2)*self.del_t)
			count += 1
		# print 'Vel'
		# print  Vel
		# print 'Shi'
		# print Shi
		return Shi

	def unsigned2signed(self, Data):
		if Data < 128:
			return Data
		else:
			return Data - 256

	def returndata(self):
		return self.Shift_str

if __name__ == '__main__':
	acc = [1,2,3,4]
	process = DataProcess(acc)
	shift = process.returndata()
	print shift