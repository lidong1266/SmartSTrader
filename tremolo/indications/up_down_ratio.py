#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys, os
from foundation import Indication

class UpDownRatio (Indication):
	@classmethod
	def isRealIndication(cls): return True
	@classmethod
	def getType(cls): return float
	
	def __init__(self, asset, parent=None, length=25):
		if asset.__class__ == Assets:
			Indication.__init__(self, asset, parent)
		else: raise TypeError("the class of 'asset' is not 'Assets'.")
		self.setLength(length)
	
	def setLength(self, length):
		if type(length) != int:
			raise TypeError("the type of 'length' is not 'int'.")
		elif length > 0: self.__length = length
		else: raise TypeError("the variable 'length' is not valid.")
	
	def getDescription(self):
		return "UpDownRatio(%i)" % len(self.asset)
	
	def evaluate(self, t):
		children = self.asset.children
		n = self.__length
		up = len([x for x in children if x.get(t-n) < x.get(t)])
		down = len([x for x in children if x.get(t-n) > x.get(t)])
		if down > 0:
			return float(up) / float(down)
		else: raise TypeError("the sum of volume on down days equals zero.")
