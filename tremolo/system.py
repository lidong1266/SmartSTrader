#!/usr/bin/env python
#-*- coding:utf-8 -*-

from assets.foundation import Asset
from indications.foundation import Indication

class System (object):
	"""
	実際にトレーディングを行ったり、データの検証や評価を担当する抽象クラスです.
	"""

	def __init__(self, asset, indication):
		"""
		クラスを初期化します.asset,indicationはそれぞれ
		Asset,Indicationクラスのサブクラスのインスタンスでなければなりません.
		"""
		if issubclass(asset.__class__, Asset) and \
		   issubclass(indication.__class__, Indication):
			self.asset = asset
			self.indication = indication
		else:
			raise TypeError("value 'asset' or 'indication' is not valid.")
	
	def evaluate(self, t):
		"""
		t地点,すなわち現時点での評価を行います.このメソッドはオーバーライドして使います.
		tは必ずしも一定に増加していくわけではありません.
		また、必ずしも実際の現実時間を指すとも限りません.
		
		tの単位はsecであり、またUNIXのエポック時間を用いることもありますが、
		絶対というわけではありません.
		"""
		raise NotImplementedError
