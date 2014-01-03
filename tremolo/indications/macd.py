#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys, os
from foundation import Indication
from moving_average import EMA
from scipy.ndimage.measurements import mean

class MACD (Indication):
	@classmethod
	def isRealIndication(cls): return True
	@classmethod
	def getType(cls): return tuple
	
	def __init__(self, asset, parent=None, x=12, y=26, z=9):
		Indication.__init__(self, asset, parent)
		self.setX(x)
		self.setY(y)
		self.setZ(z)
	
	def getX(self): return self.__x
	def setX(self, x):
		if type(x) == int and x > 0:
			self.__x = x
			self.__xEMA = EMA(self.asset, length=x)
		else: raise AttributeError
	x = property(getX, setX)
	
	def getY(self): return self.__y
	def setY(self, y):
		if type(y) == int and y > 0:
			self.__y = y
			self.__yEMA = EMA(self.asset, length=y)
		else: raise AttributeError
	y = property(getY, setY)
	
	def getZ(self): return self.__z
	def setZ(self, z):
		if type(z) == int and z > 0:
			self.__z = z
		else: raise AttributeError
	z = property(getZ, setZ)
	
	def getDescription(self):
		return "MACD(%i,%i,%i)" % (self.__x, self.__y, self.__z)
	
	def evaluate(self, t):
		"""t時点におけるMACDとMACDシグナルをタプルで返します."""
		return (self.getMACD(t), self.getMACDSignal(t))
	
	def getMACD(self, t):
		"""t時点におけるMACDを返します."""
		self.asset.lock(t)
		delta = self.__xEMA.evaluate(t) - self.__yEMA.evaluate(t)
		self.asset.unlock()
		return delta
	
	def getMACDSignal(self, t):
		"""t時点におけるMACDシグナルを返します."""
		dat = [self.getMACD(t-i) for i in xrange(self.__z)]
		return mean(dat)
