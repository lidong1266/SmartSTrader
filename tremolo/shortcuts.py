#!/usr/bin/env python
#-*- coding:utf-8 -*-

from copy import copy
	
def makeKwargsList(kwargs, exception=[]):
	"""
	タプルやリストを含んだ辞書から、それらの値を含む任意の組み合わせを
	すべてリストとして返します.
	例:
	kwargs    = {"a":(1,2), "b":3, "c":(True,False), "d":(1,2)}
	exception = "d"の場合、返される辞書のリストは、
	[{"a":1, "b":3, "c":True, "d":(1,2)},
	 {"a":1, "b":3, "c":False, "d":(1,2)},
	 {"a":2, "b":3, "c":True, "d":(1,2)},
	 {"a":2, "b":3, "c":False, "d":(1,2)}] となります.
	 
	kwargs    : タプルやリストを含んだ辞書
	exception : 組み合わせとして出力してほしくないキーのリスト
	"""
	if type(kwargs) != dict: raise TypeError
	# キーワードの抽出
	kwdict = {}
	base   = {}
	for (key, value) in kwargs.items():
		if (type(value) == list or type(value) == tuple) and \
		   (not (key in exception)):
			kwdict[key] = value
		else: base[key] = value
	# key, kw の分離
	keys = kwdict.keys()
	values  = kwdict.values()
	kwargs_list = []
	__makeKw(values, [], kwargs_list)
	# 結合
	result = []
	for args in kwargs_list:
		new_dict = dict(zip(base.keys() + keys, base.values() + args))
		result.append(new_dict)
	return result

def __makeKw(kwlist=[], base=[], kwargs_list=[]):
	if len(kwlist) > 1:
		argslist  = kwlist[0]
		newKwlist = kwlist[1:]
		for kw in argslist:
			new_base = copy(base)
			new_base.append(kw)
			__makeKw(newKwlist, new_base, kwargs_list)
	else:
		argslist = kwlist[0]
		for kw in argslist:
			new_base = copy(base)
			new_base.append(kw)
			kwargs_list.append(new_base)
