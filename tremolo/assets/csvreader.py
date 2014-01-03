#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, csv
from foundation import Asset

class CSVReader (Asset):
	"""
	CSVを利用してAssetを作成するクラスです.
	"""
	@classmethod
	def isRealAsset(cls): return True
	@classmethod
	def getType(cls): return tuple
	
	def __init__(self, path, parent=None, column=(0,), datatype=float,
	             start=0, interval=1, title="", delimiter=","):
		"""
		オブジェクトのコンストラクタです.
		
		path      : CSVファイルのパス文字列
		parent    : 親となるオブジェクト
		column    : タプルとして返される数値の列をタプルで指定
		start     : 初めの行でのtの値
		interval  : 値が保持されるtの間隔
		title     : オブジェクトを説明する文字列
		delimiter : フィールド間を分割するのに用いられる文字
		"""
		if type(interval) == int and interval > 0:
			self.interval    = interval
		else: raise TypeError("the variable 'interval' is not valid.")
		self.__start       = start
		self.__title       = title
		self.__path        = path
		self.__delimiter   = delimiter
		self.__datatype    = datatype
		if type(column) == tuple and len(column) > 0: self.column = column
		elif type(column) != tuple: raise TypeError("the variable 'column' is not tuple.")
		else: raise TypeError("the number of 'column' is zero.")
		Asset.__init__(self, parent)
		self.__loadCSVData()
		self.__max   = self.start + interval*len(self.__rawDat)
		self.__index = 0
	
	def getStart(self): return self.__start
	def setStart(self, s):
		if type(s) == int and s > 0: self.__start = s
		else: raise TypeError("the variable 'start' is not valid.")
	start = property(getStart, setStart)
	
	def __loadCSVData(self):
		if not os.path.exists(self.__path):
			raise TypeError("filepath '%s' is not found.")
		reader = csv.reader(file(self.__path, "rb"), delimiter=self.__delimiter)
		self.reader = reader
		if self.__datatype == float:
			self.__rawDat = [[float(row[i]) for i in self.column] for row in reader]
		elif self.__datatype == int:
			self.__rawDat = [[int(row[i]) for i in self.column] for row in reader]
		else: raise TypeError("the valiable 'datatype' is not valid.")
	
	def getDescription(self):
		s = self.__title=="" and ("CSVReader(%s)" % self.__path) or \
		    ("CSVReader(%s)" % self.__title)
		return s
		
	def getTitle(self, t): return self.__title
	def setTitle(self, t):
		if type(t) == str or type(t) == unicode: self.__title = t
		else: raise TypeError("the variable 'title' is not valid.")
	title = property(getTitle, setTitle)
	
	def get(self, t=-1):
		"""
		t時点でのcolumnで指定された行の値をタプルで返します.
		"""
		self._check(t)
		if (self.start <= t < self.__max):
			return tuple( self.__rawDat[(t-self.start) // self.interval] )
		elif t == -1:
			return tuple( self.__rawDat[-1] )
		else: raise IndexError("the variable 't(%i)' out of range" % t)
	
	def __iter__(self): return self
	def next(self):
		if self.__index >= len(self.__rawDat):
			self.__index = 0
			raise StopIteration
		result = tuple(self.__rawDat[self.__index])
		self.__index += 1
		return result
	
	def __len__(self):
		return len(self.__rawDat)
