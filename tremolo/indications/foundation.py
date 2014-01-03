#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys, os
TREMOLO_PATH = os.path.split( os.path.dirname(__file__) )[0]
if TREMOLO_PATH not in sys.path: sys.path.append(TREMOLO_PATH)
from assets.foundation import Asset

class Indication (object):
	"""
	システムが判断する手がかりとなる、指標を担当するクラスです.
	このクラスは抽象クラスです.
	"""
	@classmethod
	def isRealIndication(cls):
		"""
		このクラスが抽象クラスでなく、
		実際に動作するモジュールである場合にはTrueを返します.
		"""
		return False
	
	@classmethod
	def getType(cls):
		"""
		このクラスのgetが返す型を指定します.一意の場合はint,float,またはstr型が返され、
		一意でない場合はtuple型が返されます.
		ただし、どの場合でも一番重要な値は必ず一番前にもっていかなくてはなりません.
		"""
		return type(None)
	type = property(getType)
	
	def __init__(self, asset=None, parent=None):
		"""コンストラクタです"""
		self.parent = parent
		if asset == None or asset.isRealAsset(): self.__asset = asset
		else: raise TypeError("the variable 'asset' is not valid.")
	
	def getAsset(self): return self.__asset
	def setAsset(self, asset):
		if asset == None or asset.isRealAsset(): self.__asset = asset
		else: raise AttributeError
	asset = property(getAsset, setAsset)
	
	def getDescription(self):
		"""
		このオブジェクトの説明する文字列を返します.
		返す文字列はインスタンスの状況によって違います.
		"""
		return "Indication"
	description = property(getDescription)
	
	def evaluate(self, t=-1):
		"""
		t時点における指標の値を返します.
		ただし、-1の場合は「最新」の指標の値を返します.
		"""
		raise NotImplementedError
	
	def getScalar(self, t, **kwargs):
		"""
		evaluate()において返す値の種類にかかわらず、
		t時点における、かならずスカラとなる値を返します.
		"""
		tp = self.getType()
		if tp == tuple:
			return self.evaluate(t, **kwargs)[0]
		else:
			return self.evaluate(t, **kwargs)

	
	def plot(self, start, end, legend=True, **kwargs):
		"""
		指定された範囲でプロットを行います.
		
		start  : 開始する値
		end    : 終了する値
		legend : 説明文を挿入するかどうか.デフォルトはTrue
		
		その他の引数を指定した場合、
		それらの引数はmatplotlibのplot()に引き継がれます.
		"""
		from pylab import plot, arange, legend
		from matplotlib.font_manager import FontProperties
		x = arange(start, end)
		y = []
		if self.getType() == tuple:
			y = [self.evaluate(t)[0] for t in xrange(start, end)]
		else:
			y = [self.evaluate(t) for t in xrange(start, end)]
		
		if legend:
			plot(x, y, label=self.getDescription() ,**kwargs)
			legend(loc=0, prop=FontProperties(family="monospace", size=10))
		else:
			plot(x, y, **kwargs)
	
	def __call__(self, t=-1): self.evaluate(t)
	
class Indications (Indication):
	"""
	Indicationクラスを束ねる、親クラスです.
	"""
	@classmethod
	def isRealIndication(cls): return True
	@classmethod
	def getType(cls): return float
	
	def __init__(self, parent):
		"""コンストラクタです."""
		self.children = []
		
	def evaluate(self, t=-1):
		"""各指標の平均値を返します."""
		return sum([x.evaluate(t) for x in self.children]) / float( len(self) )
	
	def getDescription(self): return "Indications(%i)" % len(self.children)
	
	def addIndication(self, indication):
		"""子となるIndicationインスタンスを追加します."""
		if issubclass(indication.__class__, Indication):
			self.children.add(indication)
		else: raise TypeError("value 'indicaiton' is not valid.")
	
	def plot(self, start, end, legend=True, **kwargs):
		"""
		オブジェクトの子すべてにプロットを行います.
		"""
		for child in self.children: child.plot(start, end, legend, **kwargs)
	
	def __getitem__(self, key):
		if type(key) == int : return self.children[key]
		else: raise TypeError
	def __iter__(self): return self.children
	def __len__(self): return len(self.children)
