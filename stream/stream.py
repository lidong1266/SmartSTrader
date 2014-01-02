#!/usr/bin/python
# -*- coding: UTF-8 -*-
__all__ = ['Stream']

import warnings
import logging
import threading
import datetime
from time import time, sleep
import sys
import os
import urllib
import urllib2

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

"""http://www.saltycrane.com/blog/2008/01/how-to-use-args-and-kwargs-in-python/"""
class StreamHandler:
    def __init__(self, parent = None):
        self.parent = parent
    def Handle(self, event, *args):
        handler = 'Handle_' +event
        if hasattr(self, handler):
            func = getattr(self, handler)
            func(*args)
        elif self.parent:
            self.parent.Handle(event, *args)

class EST(datetime.tzinfo):
    def utcoffset(self, dt):
      return datetime.timedelta(hours=-5)

    def dst(self, dt):
        return datetime.timedelta(0)
		
class Stream(threading.Thread):
	def __init__(self, Symbol, url, handler = None, interval = 5):
		threading.Thread.__init__(self, name=Symbol)
		self.Symbol = Symbol
		self.Url = url
		self.Interval = interval
		self.handler = handler

	def RegisterHandler(self, handler):
		self.handler = handler
		
	def StartPoll(self):
		self.run()
		print "xx"
		return True
	def StopPoll(Self):
		return False
	def IsRunning(Self):
		return False
	#def 
	def run(self):
		
		while True:
			self.get_us_stock_price('gb_qihu')
			sleep(30)
			now = datetime.datetime.now(EST())
			print "%s says Hello World at time: %s" % (self.getName(), now)

	def get_us_stock_price(self, code):
		#http://hq.sinajs.cn/?_=0.9784360658377409&list=gb_yoku
		#http://hq.sinajs.cn/etag.php?rn=1386743228985&list=gb_yoku
		url = 'http://hq.sinajs.cn/etag.php?rn=%u&list=%s' % (int(time() * 1000), code)
		#ar hq_str_gb_yoku="
		"""	
		var hq_str_gb_sina="
		新浪, 80.95, 6.75, 2013-12-11 09:42:28, 5.12, 75.60, <开盘 >81.98, 最高 区间 75.60,最高 区间
		92.83,52最高 | 44.30,52最低
		5785410,今天成交量 | 2152413,10日均量 | 5407460000,市值 | -0.20,每股收益 | --,市盈率
		0.00 | 1.45,贝塔系数 | 0.00 | 0.00,
		66800000,股本 | 86.00,
		81.05 | 0.12 | 0.10 | Dec 10 07:20PM EDT | Dec 10 04:00PM EDT, | 75.83,前收盘 | 12912.00";成交量
		"""
		#print url
		req = urllib2.Request(url)
		#如果不需要设置代理，下面的set_proxy就不用调用了。由于公司网络要代理才能连接外网，所以这里有set_proxy...
		#req.set_proxy('proxy.XXX.com:911', 'http')
		content = urllib2.urlopen(req).read()
		str = content.decode('gbk')
			
		data = str.split('"')[1].split(',')
		print u"股票代码", data[0]
		print u"当前价", data[1]	#当前价
		print u"上涨%", data[2] 	#上涨百分比
		print u"上涨%", data[3] 	#上涨百分比
		print u"上涨", data[4] 		#上涨价格
		print u"开盘", data[5] 		#开盘价格
		print u"最高", data[6] 		#最高价格
		print u"最低", data[7] 		#最低价格
		'''print u"52周最高", data[8] 		#最低价格
		print u"52周最低", data[9] 		#最低价格
		print u"今天成交量", data[10] 		#今天成交量
		print u"10日均量", data[11] 		#10日均量
		print u"市值", data[12] 		#市值
		print u"每股收益", data[13] 		#每股收益
		print u"市盈率", data[14] 		#市盈率
		print u"---", data[15] 		#---
		print u"贝塔系数", data[16] 		#贝塔系数
		print u"---", data[17] 		#---
		print u"---", data[18] 		#---
		print u"股本", data[19] 		#股本
		print u"#---", data[20] 		##---
		print u"#---", data[21] 		##---
		print u"#---", data[22] 		##---
		print u"#---", data[23] 		##---
		print u"#---", data[24] 		##---
		print u"#---", data[25] 		##---
		print u"前收盘", data[26] 		##---
		print u"盘后交易", data[27] 		##---'''
		#exit(0)
		if self.handler:
			self.handler.Handle("Data", data)
		return  
		name = "%-6s" % data[0]
		price_current = "%-6s" % float(data[3])
		change_percent = ( float(data[3]) - float(data[2]) )*100 / float(data[2])
		change_percent = "%-6s" % round (change_percent, 2)
		#print("股票名称:{0} 涨跌幅:{1} 最新价:{2}".format(name, change_percent, price_current) )
		#print(u"股票名称:%s 涨跌幅:%s 最新价:%s" % (name.decode("gbk"), change_percent.decode("gbk"), price_current.decode("gbk")) )
		print u"股票名称"
		print name
		print change_percent
		print price_current
		print type(price_current)
		
if __name__ == "__main__":
	print "SSS"
	stream = Stream('QIHU', '')
	stream.StartPoll()
	print 'xxx'
	sleep(3600)
	print "xx"