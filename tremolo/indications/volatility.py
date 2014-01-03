#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys, os, math
from foundation import Indication
from moving_average import MovingAverage, SMA
from scipy.stats import stats
from numpy import int32

class BollingerBands (Indication):
	"""
	t時点におけるボリンジャーバンドを表すクラスです.
	"""
	@classmethod
	def isRealIndication(cls): return True
	@classmethod
	def getType(cls): return float
	
	def __init__(self, asset, parent=None, length=5, macls=SMA):
		"""
		オブジェクトのコンストラクタです.
		
		asset  : 対象となる資産
		parent : 親となるオブジェクト
		length : 過去に遡る回数.デフォルトは5
		macls  : 使用する移動平均線のクラス.デフォルトはmoving_averageのSMAが使用される
		"""
		if issubclass(macls, MovingAverage):
			self.moving_average = macls(asset, self, length)
		else: raise AttributeError
		self.length = length
		Indication.__init__(self, asset, parent)
	
	def getDescription(self):
		return "BolingerBands(%i)" % self.length
	
	def evaluate(self, t):
		"""
		t時点における、ボリンジャーバンドの相対位置を返します.
		"""
		d = self.asset.getPreviousData(t, self.length)
		stdev = stats.std(d)
		center = self.moving_average.evaluate(t)
		position = d[0]
		return (position - center) / stdev
	
	def getBollingerBands(self, t, level=1):
		"""
		t時点における、ボリンジャーバンドの値を返します.
		"""
		d = self.asset.getPreviousData(t, self.length)
		stdev = stats.std(d)
		center = self.moving_average.evaluate(t)
		return center + stdev*level
	
	def getVolatility(self, t):
		"""t時点における、ボラティリティの値を返します."""
		d = self.asset.getPreviousData(t, self.length)
		return stats.std(d)
	
	def plot(self, start, end, num=1, color="green", show_ma=True, **kwargs):
		"""
		指定された範囲でプロットを行います.
		
		start   : 開始する値
		end     : 終了する値
		num     : ボリンジャーバンドをどのくらいのレベルで表示させるか.デフォルトは1
		color   : ボリンジャーバンドの色.デフォルトはgreen
		show_ma : 中心である移動平均線を表示させるかどうか.デフォルトはTrue
		
		その他の引数を指定した場合、それらの引数はmatplotlibのplot()に引き継がれます.
		"""
		from pylab import plot, arange, legend
		from matplotlib.font_manager import FontProperties
		x = arange(start, end)
		center = [self.moving_average.evaluate(t) for t in x]
		stdev  = [self.getVolatility(t) for t in x]
		if show_ma: plot(x, center, color=color, **kwargs)
		for n in xrange(num):
			n += 1
			b_plus  = [c+s*n for (c,s) in zip(center, stdev)]
			b_minus = [c-s*n for (c,s) in zip(center, stdev)]
			plot(x, b_plus,  color=color, **kwargs)
			plot(x, b_minus, color=color, **kwargs)

class Volatility (Indication):
	"""
	t時点におけるボラティリティを表すクラスです.
	"""
	@classmethod
	def isRealIndication(cls): return True
	@classmethod
	def getType(cls): return float
	
	def __init__(self, asset, parent=None, length=5):
		"""
		オブジェクトのコンストラクタです.
		
		asset  : 対象となる資産
		parent : 親となるオブジェクト
		length : 過去に遡る回数.デフォルトは5
		"""
		self.setLength(length)
		Indication.__init__(self, asset, parent)
	
	def getDescription(self):
		return "Volatility(%i)" % self.__length
	
	def getLength(self): return self.__length
	def setLength(self, l):
		if (type(l) == int or type(l) == int32) and l > 0:
			self.__length = l
		else: raise AttributeError
	length = property(getLength, setLength)
	
	def evaluate(self, t):
		"""
		t地点における短期的ボラティリティを返します.
		"""
		d = self.asset.getPreviousData(t, self.__length)
		return stats.std(d)

class Skew (Indication):
	"""
	t時点における歪度を表すクラスです.
	"""
	@classmethod
	def isRealIndication(cls): return True
	@classmethod
	def getType(cls): return float
	
	def __init__(self, asset, parent=None, length=5):
		"""
		オブジェクトのコンストラクタです.
		
		asset  : 対象となる資産
		parent : 親となるオブジェクト
		length : 過去に遡る回数.デフォルトは5
		"""
		self.setLength(length)
		Indication.__init__(self, asset, parent)
	
	def getDescription(self):
		return "Skew(%i)" % self.length
	
	def getLength(self): return self.__length
	def setLength(self, l):
		if (type(l) == int or type(l) == int32) and l > 0:
			self.__length = l
		else: raise AttributeError
	length = property(getLength, setLength)
	
	def evaluate(self, t):
		"""
		t地点における短期的歪度を返します.
		"""
		d = self.asset.getPreviousData(t, self.__length)
		return stats.skew(d)

class Kurtosis (Indication):
	"""
	t時点における尖度を表すクラスです.
	"""
	@classmethod
	def isRealIndication(cls): return True
	@classmethod
	def getType(cls): return float
	
	def __init__(self, asset, parent=None, length=5, fisher=True):
		"""
		オブジェクトのコンストラクタです.
		
		asset  : 対象となる資産
		parent : 親となるオブジェクト
		length : 過去に遡る回数.デフォルトは5
		fisher : Trueならば計算にフィッシャーの定義が使われる.(正規分布=0)
		         Falseならば計算にペアソンの定義が使われる.(正規分布=3.0)
		"""
		self.setLength(length)
		self.setFisher(fisher)
		Indication.__init__(self, asset, parent)
	
	def getDescription(self):
		if self.fisher:
			return "Indication::Kurtosis(Fisher,%i)" % self.__length
		else:
			return "Indication::Kurtosis(Pearson,%i)" % self.__length
	
	def getLength(self): return self.__length
	def setLength(self, l):
		if (type(l) == int or type(l) == int32) and l > 0:
			self.__length = l
		else: raise AttributeError
	length = property(getLength, setLength)
	
	def getFisher(self): return self.__fisher
	def setFisher(self, f):
		if type(f) == bool: self.__fisher = f
		else: raise AttributeError
	fisher = property(getFisher, setFisher)
	
	def evaluate(self, t):
		"""
		t地点における短期的尖度を返します.
		"""
		d = self.asset.getPreviousData(t, self.__length)
		return stats.kurtosis(d, fisher=self.__fisher)

class Moment (Indication):
	"""
	t時点におけるn次のモーメントを表すクラスです.
	"""
	@classmethod
	def isRealIndication(cls): return True
	@classmethod
	def getType(cls): return float
	
	def __init__(self, asset, parent=None, length=5 ,moment=1):
		self.setMoment(moment)
		self.setLength(length)
		Indication.__init__(self, asset, parent)
	
	def getDescription(self):
		return "Moment(%i,%i)" % (self.__length, self.__moment)
	
	def getLength(self): return self.__length
	def setLength(self, l):
		if (type(l) == int or type(l) == int32) and l > 0:
			self.__length = l
		else: raise AttributeError
	length = property(getLength, setLength)
	
	def getMoment(self): return self.__moment
	def setMoment(self, m):
		if (type(m) == int or type(m) == int32) and m > 0:
			self.__moment = m
		else: raise AttributeError
	moment = property(getMoment, setMoment)
	
	def evaluate(self, t):
		"""
		t地点におけるn次のモーメントを返します.
		"""
		d = self.asset.getPreviousData(t, self.__length)
		return stats.moment(d, moment=self.__moment)
