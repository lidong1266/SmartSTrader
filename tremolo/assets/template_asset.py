#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys, os
from foundation import Asset

class Template_Asset (Asset):
	"""
	Assetクラスのテンプレートです.
	"""
	# 実際に実装すべきメソッド群です.実装しない場合にはエラーが返されます.
	@classmethod
	def isRealAsset(cls): return False
	@classmethod
	def getType(cls): return float
	
	def __init__(self, parent): Asset.__init__(self, parent)
	def getDescription(self): return "Asset::Template_Asset"
	def get(self, t=-1):
		self._check(t)
		return 0.0
	
	# 実装しなくても動作しますが、オーバーライドしたほうが良いメソッド群です.
	def max(self): return 0.0
	def min(self): return 0.0
	
	# 実装してもしなくてもよいメソッド群です.
	def plot(self, start, end, legend=True, **kwargs):
		raise NotImplementedError
