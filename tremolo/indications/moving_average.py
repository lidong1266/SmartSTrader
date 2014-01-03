#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys, os
from foundation import Indication
from scipy.ndimage.measurements import mean

class MovingAverage (Indication):
	"""
	すべての移動平均指標の基本となるクラスです.
	"""
	@classmethod
	def isRealIndication(cls): return False
	@classmethod
	def getType(cls): return float
	
	def __init__(self, asset, parent=None):
		Indication.__init__(self, asset, parent)
	
	def getDescription(self): return "MovingAverage"
	
	def evaluate(self, t): raise NotImplementedError

class SMA(MovingAverage):
	"""
	単純移動平均を表すクラスです.
	"""
	@classmethod
	def isRealIndication(cls): return True
	
	def __init__(self, asset, parent=None, length=5):
		MovingAverage.__init__(self, asset, parent)
		if type(length) == int and length > 0: self.length = length
		else: raise TypeError("the variable 'length' is not valid.")
	
	def getDescription(self):
		return "SMA(%i)" % self.__length
	
	def evaluate(self, t):
		self.asset.lock(t)
		dat = self.asset.getPreviousData(t, self.length)
		self.asset.unlock()
		return mean(dat)

class WMA(MovingAverage):
	"""
	加重移動平均を表すクラスです.
	"""
	@classmethod
	def isRealIndication(cls): return True
	
	def __init__(self, asset, parent=None, length=5):
		MovingAverage.__init__(self, asset, parent)
		if type(length) == int and length > 0:
			self.__length = length
			self.__denominator = length*(length+1)/2.0
			self.__cache_list  = [(length-i) for i in xrange(length)]
		else: raise TypeError("the variable 'length' is not valid.")
	
	def getDescription(self):
		return "WMA(%i)" % self.__length
	
	def getLength(self): return self.__length
	def setLength(self, length):
		if type(length) == int and length > 0:
			self.__length = length
			self.__denominator = length*(length+1)/2.0
			self.__cache_list  = [(length-i) for i in xrange(length)]
		else: raise TypeError("the variable 'length' is not valid.")
	length = property(getLength, setLength)
	
	def evaluate(self, t):
		self.asset.lock(t)
		dat       = self.asset.getPreviousData(t, self.__length)
		numerator = sum([x*dat[i] for (i, x) in enumerate(self.__cache_list)])
		self.asset.unlock()
		return numerator / self.__denominator

class EMA(MovingAverage):
	"""
	指数加重移動平均を表すクラスです.
	"""
	@classmethod
	def isRealIndication(cls): return True
	
	def getDescription(self):
		return "EMA(%i,%i)" % (self.__length, self.__alpha)
	
	def __init__(self, asset, parent=None, length=5, alpha=-1):
		"""
		オブジェクトのコンストラクタです。
		
		length        : 過去に参照する長さの値
		alpha         : 減衰率.0から1の間で指定.-1の場合は適切な値に設定される
		"""
		MovingAverage.__init__(self, asset, parent)
		
		if alpha == -1 or (type(alpha)==float and 0.0 < alpha < 1.0):
			self.__alpha = alpha
		else: raise TypeError("the variable 'alpha' is not valid.")
		if type(length) == int and length > 0:
			self.__length = length
		else: raise TypeError("the variable 'length' is not valid.")
		
		self.__initCache()
	
	def __initCache(self):
		k = self.__alpha == -1 and 2.0/(self.__length+1) or self.__alpha
		oneMinusK = 1.0 - k
		self.__cache_list = [(oneMinusK**i) for i in xrange(self.__length)]
		self.__denominator = sum(self.__cache_list)
	
	def getAlpha(self): return self.__alpha
	def setAlpha(self, alpha):
		if alpha == -1 or (type(alpha)==float and 0.0 < alpha < 1.0):
			self.__alpha = alpha
		else: raise TypeError("the variable 'alpha' is not valid.")
		self.__initCache()
	alpha = property(getAlpha, setAlpha)
	
	def getLength(self): return self.__length
	def setLength(self, length):
		if type(length) == int and length > 0:
			self.__length = length
		else: raise TypeError("the variable 'length' is not valid.")
		self.__initCache()
	length = property(getLength, setLength)
	
	def evaluate(self, t):
		self.asset.lock(t)
		n = self.__length
		dat = self.asset.getPreviousData(t, n)
		self.asset.unlock()
		numerator   = sum([x*dat[i] for (i, x) in enumerate(self.__cache_list)])
		return numerator / self.__denominator
