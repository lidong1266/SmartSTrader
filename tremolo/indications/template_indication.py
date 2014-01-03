#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys, os
# もしAssetクラスを使用するのであれば、以下の行をコメントアウトしてください.
# TREMOLO_PATH = os.path.split( os.path.dirname(__file__) )[0]
# if TREMOLO_PATH not in sys.path: sys.path.append(TREMOLO_PATH)
# from assets.foundation import Asset
from foundation import Indication

class Template_Indication (Indication):
	@classmethod
	def isRealIndication(cls): return False
	@classmethod
	def getType(cls): return float
	
	def __init__(self, asset, parent=None):
		Indication.__init__(self, asset, parent)
	
	def getDescription(self): return "Indication::Template_Indication"
	
	def evaluate(self, t=-1): return 0.0
