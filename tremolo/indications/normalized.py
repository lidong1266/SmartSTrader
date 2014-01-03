#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
from foundation import Indication
from numpy import int32

class Normalized (Indication):
	"""
	対象の指標を0から1の範囲で正規化するクラスです.
	"""
	@classmethod
	def isRealIndication(cls): return True
	@classmethod
	def getType(cls): return float
	
	def __init__(self, indication, start, end, parent=None):
		"""
		オブジェクトのコンストラクタです.
		
		indication : 対象となる指標.このオブジェクトは
		             Indicationのサブクラスのオブジェクトでなければなりません.
		start      : サンプルに用いるtの開始範囲
		end        : サンプルに用いるtの終了範囲
		parent     : 親となるオブジェクト
		"""
		Indication.__init__(self, parent=parent)
		self.setIndication(indication)
		if (type(start) == int or type(start) == int32):
			self.__s = start
		else: raise TypeError("the variable 'start' is not valid.")
		if (type(end) == int or type(start) == int32):
			self.__e = end
		else: raise TypeError("the variable 'end' is not valid.")
		self.__initRange()
	
	def getStart(self): return self.__s
	def setStart(self, s):
		if (type(s) == int or type(s) == int32) and s < self.__e:
			self.__s = s
			self.__initRange()
		else: raise AttributeError
	start = property(getStart, setStart)
	
	def getEnd(self): return self.__e
	def setEnd(self, e):
		if (type(e) == int or type(e) == int32) and self.__s < e:
			self.__e = e
			self.__initRange()
		else: raise AttributeError
	end = property(getEnd, setEnd)
	
	def __initRange(self):
		dat = [self.indication.evaluate(t) for t in xrange(self.__s, self.__e)]
		self.__M     = max(dat)
		self.__m     = min(dat)
		self.__range = self.__M - self.__m
	
	def getIndication(self): return self.__indication
	def setIndication(self, i):
		if issubclass(i.__class__, Indication):
			self.__indication = i
		else: raise AttributeError
	indication = property(getIndication, setIndication)
	
	def getDescription(self):
		return "%s(normalized)" % self.indication.getDescription()
	
	def getMax(self): return self.__M
	def setMax(self, M):
		if type(M) == int or type(M) == int32: self.__M = M
	max = property(getMax, setMax)
	
	def getMin(self): return self.__m
	def setMin(self, m):
		if type(m) == int or type(m) == int32: self.__m = m
	min = property(getMin, setMin)
	
	def evaluate(self, t):
		return (self.indication.evaluate(t)-self.__m)/float(self.__range)
	
	def reverse(self, x):
		"""このオブジェクトによって写像された空間から、本来の空間へと戻します."""
		return (x*self.__range) + self.__m
