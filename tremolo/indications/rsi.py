#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys, os
from foundation import Indication

class Cutler_RSI (Indication):
	"""
	Cutlerが開発したRSIオシレータです.
	WilderのRSIの指数移動平均を単純移動平均に置き換えたものです.
	"""
	@classmethod
	def isRealIndication(cls): return True
	@classmethod
	def getType(cls): return float
	
	def __init__(self, asset, parent=None, length=14, delta=10):
		"""
		オブジェクトのコンストラクタです.
		
		length : 過去の値を取得する回数
		delta  : 値上がり、値下がりの判定として使われる時間幅
		"""
		Indication.__init__(self, asset, parent)
		self.setLength(length)
		self.setDelta(delta)
	
	def getLength(self): return self.__length
	def setLength(self, length):
		if type(length) == int and length > 0:
			self.__length = length
		else: raise TypeError("the variable 'length' is not valid.")
	length = property(getLength, setLength)
	
	def getDelta(self): return self.__delta
	def setDelta(self, delta):
		if type(delta) == int and delta > 0:
			self.__delta = delta
		else: raise TypeError("the variable 'delta' is not valid.")
	delta = property(getDelta, setDelta)
	
	def getDescription(self):
		return "RSI(Cutler,%i)" % self.__length
	
	def evaluate(self, t):
		d = self.__delta
		asset = self.asset
		asset.lock(t)
		delta_list = [asset.getScalar(t-i*d) - asset.getScalar(t-(i+1)*d)
		              for i in xrange(self.__length)]
		asset.unlock()
		u = sum([x for x in delta_list if x > 0])
		d = sum([-y for y in delta_list if y < 0])
		return float(u)/(u+d)
		
