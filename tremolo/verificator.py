#!/usr/bin/env python
#-*- coding:utf-8 -*-

from indications.foundation import Indication
from scipy.stats.stats import corrcoef

class Verificator(object):
	"""
	それぞれの指標に関する検証を行うクラスです.
	"""
	def __init__(self):
		self.__indicaitons = {}
	
	def getIndications(self): return self.__indications
	indications = property(getIndications)
	
	def addIndications(self, key, indication, method=None, kwargs={}):
		"""
		検証する指標オブジェクトを追加します.
		
		key        : 指標のキー
		indication : 対象となる指標オブジェクト
		mothod     : 呼び出すメソッド.指定しなければevaluate()が呼び出される
		kwargs     : 引数として指定する値.指定しなければ何も指定されない
		"""
		if issubclass(indication.__class__, Indication):
			inddic = {"indication" : indication,
			          "method" : method,
			          "kwargs" : kwargs}
			self.__indicaiton[key] = inddic
		else: raise TypeError
	
	def cor(self, key1, key2, start, end,
	        method1=None, method2=None, kwargs1=None, kwargs2=None):
		"""
		対象となる2つの指標オブジェクトの相関係数を返します.
		
		key1    : 対象となる第1指標のキー
		key2    : 対象となる第2指標のキー
		start   : tの開始範囲
		end     : tの終了範囲
		method1 : 第1指標に登録したメソッドとは別に呼び出してほしいものがあれば指定
		method2 : 第2指標に登録したメソッドとは別に呼び出してほしいものがあれば指定
		kwargs1 : 第1指標に登録した引数の辞書とは別に呼び出してほしいものがあれば指定
		kwargs2 : 第2指標に登録した引数の辞書とは別に呼び出してほしいものがあれば指定
		"""
		d1  = self.__indications[key1]
		d2  = self.__indications[key2]
		i1  = d1["indication"]
		i2  = d2["indication"]
		m1  = method1 and method1 or d1["method"]
		m2  = method2 and method2 or d2["method"]
		kw1 = kwargs1 and kwargs1 or d1["kwargs"]
		kw2 = kwargs2 and kwargs2 or d2["kwargs"]
		if m1 == None:
			r1 = [i1.evaluate(t, **kw1) for t in xrange(start, end)]
		else:
			r1 = [m1(t, **kw1) for t in xrange(start, end)]
		if m2 == None:
			r2 = [i2.evaluate(t, **kw2) for t in xrange(start, end)]
		else:
			r2 = [m2(t, **kw2) for t in xrange(start, end)]
		return corrcoef(r1, r2)[0,1]
	
	def getCorList(self, key1, key2, start, end,
	               attr1_list, method1=None, method2=None,
	               kwargs1=None, kwargs2=None, debug=False):
		"""
		第1指標がattr1_listに指定された属性値のリストをリストの個数分だけ施行し、
		第2指標との相関係数のリストを返します.
		
		key1       : 対象となる第1指標のキー
		key2       : 対象となる第2指標のキー
		start      : tの開始範囲
		end        : tの終了範囲
		attr1_list : 第1指標に施行させる属性値の辞書リスト[{"attr1":1},{"attr1":2},...]
		method1    : 第1指標に登録したメソッドとは別に呼び出してほしいものがあれば指定
		method2    : 第2指標に登録したメソッドとは別に呼び出してほしいものがあれば指定
		debug      : デバッグとして詳細な情報を出力したい場合はTrueを指定
		"""
		d1  = self.__indications[key1]
		d2  = self.__indications[key2]
		i1  = d1["indication"]
		i2  = d2["indication"]
		m1  = method1 and method1 or d1["method"]
		m2  = method2 and method2 or d2["method"]
		kw1 = kwargs1 and kwargs1 or d1["kwargs"]
		kw2 = kwargs2 and kwargs2 or d2["kwargs"]
		cor_list = []
		for attr1 in attr1_list:
			# 属性値を変更
			for (attr_name, attr_value) in attr1.items():
				setattr(i1, attr_name, attr_value)
			# 指標の評価を行う.
			if m1 == None:
				r1 = [i1.evaluate(t, **kw1) for t in xrange(start, end)]
			else:
				r1 = [m1(t, **kw1) for t in xrange(start, end)]
			if m2 == None:
				r2 = [i2.evaluate(t, **kw2) for t in xrange(start, end)]
			else:
				r2 = [m2(t, **kw2) for t in xrange(start, end)]
			cor_list.append(corrcoef(r1, r2)[0,1])
		return cor_list
	
	def __getattr__(self, key): return self.__indications[key]["indication"]
