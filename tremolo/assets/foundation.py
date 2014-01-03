#!/usr/bin/env python
#-*- coding:utf-8 -*-

from numpy import int32

class Asset (object):
	"""
	各資産のデータ管理を行います.このクラスは抽象クラスです.
	"""
	@classmethod
	def isRealAsset(cls):
		"""
		このクラスが抽象クラスでなく、
		実際に動作するモジュールである場合にはTrueを返します.
		"""
		return False
	
	@classmethod
	def getType(cls):
		"""
		このクラスのget()が返す型を指定します.一意の場合はint,またはfloat型が返され、
		一意でない場合はtuple型が返されます.
		ただし、一番重要な値(始値など)は必ず一番前にもっていかなくてはなりません.
		"""
		raise NotImplementedError("the method 'gettype()' is not implemented.")
	
	def __init__(self, parent):
		self.parent    = parent
		self.isLocked  = False
		self.lock_time = 0
	
	def get(self, t=-1):
		"""
		t地点における資産の値を返します.返す値の種類はgetType()が返す型に準拠します.
		ただし、-1の場合は「最新」の資産の値を返します.
		"""
		raise NotImplementedError("the method 'get()' is not implemented.")
	
	def getPreviousData(self, t, n=5):
		"""
		t時点からn回前までの複数のデータを取得し、リストで返します.
		"""
		tp = self.getType()
		dat = []
		if tp == tuple:
			dat = [self.get(t-i)[0] for i in xrange(n)]
		elif tp == int or tp == float:
			dat = [self.get(t-i) for i in xrange(n)]
		return dat
	
	def getScalar(self, t):
		"""
		get()において返す値の種類にかかわらず、
		t時点における、かならずスカラとなる値を返します.
		"""
		tp = self.getType()
		if tp == tuple:
			return self.get(t)[0]
		else:
			return self.get(t)
	
	def __call__(self, t): self.get(t)
	
	def getDescription(self):
		"""
		このオブジェクトの説明を返します.返す文字列はインスタンスの状況によって違います.
		"""
		raise NotImplementedError("the method 'getDescription()' is not implemented.")
	description = property(getDescription)
	
	def max(self, start, end):
		"""
		指定されたtの範囲での最大値を返します.
		このメソッドはオーバーライドしなくても使えますが、低速です.
		"""
		t = self.getType()
		if t == tuple:
			return max( [self.get(t)[0] for t in xrange(start, end)] )
		elif t == float or t == int:
			return max( [self.get(t) for t in xrange(start, end)] )
		else: raise TypeError("'getType()' returns '%s', not tuple,float,and int." % str(t))
	
	def min(self, start, end):
		"""
		指定されたtの範囲での最小値を返します.
		このメソッドはオーバーライドしなくても使えますが、低速です.
		"""
		t = self.getType()
		if t == tuple:
			return min( [self.get(t)[0] for t in xrange(start, end)] )
		elif t == float or t == int:
			return min( [self.get(t) for t in xrange(start, end)] )
		else: raise TypeError("'getType()' returns '%s', not tuple,float,and int." % str(t))
	
	def getCandlestick(start, end):
		"""
		指定されたtの範囲での始値、高値、安値、終値から成るタプルを返します.
		"""
		s = self.get(start)
		h = self.max(start, end)
		l = self.min(start, end)
		e = self.get(end-1)
		return (s,h,l,e)
	
	
	def lock(self, t):
		"""
		指定されたt以降の情報にアクセスすることができなくなるように、
		オブジェクトをロックします.
		"""
		if t >= 0:
			self.isLocked  = True
			self.lock_time = t
		elif t == -1 : self.isLocked = False
		else: raise IndexError("list index out of range.")
	
	def _check(self, t):
		"""
		オブジェクトが実際にロックされているかどうかを確認します.
		また、t以降の情報にアクセスしようと試みている場合には例外を送出します.
		"""
		if not self.isLocked: return
		if not (type(t) == int or type(t) == int32):
			raise TypeError("the variable 't' is not valid.")
		elif self.lock_time < t:
			raise TypeError("this object is locked(t=%i)." % t)
		elif (t != -1) and (t < 0):
			raise IndexError("list index out of range.")
	
	def unlock(self):
		"""
		オブジェクトをアンロックします.
		"""
		self.isLocked = False
	
	def plot(self, start, end, legend=True, **kwargs):
		"""
		指定された範囲でプロットを行います.
		
		start  : 開始する値
		end    : 終了する値
		legend : 説明文を挿入するかどうか.デフォルトはTrue
		
		その他の引数を指定した場合、それらの引数はmatplotlibのplot()に引き継がれます.
		"""
		from pylab import plot, arange
		from pylab import legend as leg
		from matplotlib.font_manager import FontProperties
		x = arange(start, end)
		y = []
		if self.getType() == tuple:
			y = [self.get(t)[0] for t in xrange(start, end)]
		else:
			y = [self.get(t) for t in xrange(start, end)]
		
		if legend:
			plot(x, y, label=self.getDescription() ,**kwargs)
			leg(loc=0, prop=FontProperties(size=10))
		else:
			plot(x, y, **kwargs)

class Assets (Asset):
	"""
	Assetクラスを束ねる、親クラスです.
	"""
	@classmethod
	def isRealAsset(cls): return True
	@classmethod
	def getType(cls): return type(float)
	
	def __init__(self):
		"""コンストラクタです."""
		Asset.__init__(self, self)
		self.children = []
		self.__index  = 0
		
	def get(self, t=-1):
		"""各資産の平均値を返します."""
		return sum([x.get(t) for x in self.children]) / float( len(self) )
	
	def getDescription(self):
		return "Assets(%i)" % len(self.children)
	
	def addAsset(self, asset):
		"""子となるAssetインスタンスを追加します."""
		if issubclass(asset.__class__, Asset):
			self.children.append(asset)
		else: raise TypeError("value 'asset' is not valid.")
	
	def lock(self, t):
		"""オブジェクトの子をすべてロックします."""
		for x in self.children: x.lock(t)
	def unlock(self, t):
		for x in self.children: x.unlock()
	
	def __getitem__(self, key):
		"""オブジェクトの子をすべてアンロックします."""
		if (type(key) == int) and (0 <= key < len(self.children)):
			return self.children[key]
		else: raise IndexError("list index out of range.")
	
	def plot(self, start, end, legend=True, **kwargs):
		"""
		指定された範囲ですべてのassetに対してプロットを行います.
		"""
		for child in self.children: child.plot(start, end, legend, **kwargs)
	
	def __call__(self, t=-1): return self.get(t)
	def __str__(self): return self.getDescription()
	
	def __iter__(self): return self
	def next(self):
		if self.__index >= len(self.children):
			self.__index = 0
			raise StopIteration
		result = self.children[self.__index]
		self.__index += 1
		return result
		
	def __len__(self): return len(self.children)
