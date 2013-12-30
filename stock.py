#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import os
import urllib
import urllib2
from time import time
#http://wenku.baidu.com/link?url=x0pozy5pqLQlN5ex6v_v_Fop4zuejPpzsW4pSxMXMoVOXEbXl6CNQXEj5VDN-EoRooesJHJKM4ikSfMVNOjqI0PGR6yjZl7YIM0R5Sl-6pG
#http://wenku.baidu.com/link?url=xZk8ViilYUY09EuSq24K-kf7iRZp7LyoAlpEsyTWLz57EfODZlTYIvJsqYoj_3tRmSmadCHvYGDcj77o1wLeMqVODgdDOAhc53j5oHFER1C

"""
http://hi.baidu.com/pinotwu/item/e567678e0f3bff824514cf4d
http://blog.sciencenet.cn/home.php?mod=space&uid=461456&do=blog&id=455211
http://www.21andy.com/blog/20090530/1313.html


以大秦铁路（股票代码：601006）为例，如果要获取它的最新行情，只需访问新浪的股票数据
接口：
http://hq.sinajs.cn/list=sh601006

这个url会返回一串文本，例如：
var hq_str_sh601006="大秦铁路, 27.55, 27.25, 26.91, 27.55, 26.20, 26.91, 26.92,
22114263, 589824680, 4695, 26.91, 57590, 26.90, 14700, 26.89, 14300,
 26.88, 15100, 26.87, 3100, 26.92, 8900, 26.93, 14230, 26.94, 25150, 26.95, 15220, 26.96, 2008-01-11, 15:05:32";

这个字符串由许多数据拼接在一起，不同含义的数据用逗号隔开了，按照程序员的思路，顺序号从0开始。

    0：”大秦铁路”，股票名字；
    1：”27.55″，今日开盘价；
    2：”27.25″，昨日收盘价；
    3：”26.91″，当前价格；
    4：”27.55″，今日最高价；
    5：”26.20″，今日最低价；
    6：”26.91″，竞买价，即“买一”报价；
    7：”26.92″，竞卖价，即“卖一”报价；
    8：”22114263″，成交的股票数，由于股票交易以一百股为基本单位，所以在使用时，通常把该值除以一百；
    9：”589824680″，成交金额，单位为“元”，为了一目了然，通常以“万元”为成交金额的单位，所以通常把该值除以一万；
    10：”4695″，“买一”申请4695股，即47手；
    11：”26.91″，“买一”报价；
    12：”57590″，“买二”
    13：”26.90″，“买二”
    14：”14700″，“买三”
    15：”26.89″，“买三”
    16：”14300″，“买四”
    17：”26.88″，“买四”
    18：”15100″，“买五”
    19：”26.87″，“买五”
    20：”3100″，“卖一”申报3100股，即31手；
    21：”26.92″，“卖一”报价
    (22, 23), (24, 25), (26,27), (28, 29)分别为“卖二”至“卖四的情况”
    30：”2008-01-11″，日期；
    31：”15:05:32″，时间；
webservice来源于sina，感谢sina，例如http://hq.sinajs.cn/list=sh600547， 返回的结果如下：
var hq_str_sh600547="山东黄金,51.02,51.00,52.71,52.86,50.68,52.70,52.72,16389139
,850524809,3000,52.70,52500,52.69,100,52.67,28849,52.66,7400,52.65,1200,52.72,43
77,52.75,11200,52.76,20000,52.77,4000,52.78,2010-12-31,15:02:06";
http://www.cnblogs.com/itech/archive/2010/12/15/1907067.html

var hq_str_gb_qihu="
奇虎360,
82.89,
2.03,
2013-12-11 09:41:03,
1.65,
81.00,

83.25,
81.00,

96.74,
24.50,

1842562,
2612057,
10178892000, 市值

0.50,每股收益
165.78,市盈率

0.00,
0.00,
0.00,
0.00,

122800000,71.00,83.00,0.13,0.11,Dec 10 06:51PM EDT,Dec 10 04:01PM EDT,81.24,570.00";


var hq_str_gb_bidu="百度,179.93,4.67,2013-12-11 09:46:59,8.03,171.70,180.89,171.10,180.89,82.98,6906312,3100549,62939514000,

4.94,每股收益
36.42,市盈率

0.00,
1.54,
0.00,0.00,

349800000,
83.00,

180.30,
0.21,
0.37,
Dec 10 07:57PM EDT,
Dec 10 04:00PM EDT,

171.90,

60898.00";


var hq_str_gb_aapl="苹果,565.55,-0.16,2013-12-11 09:45:21,-0.88,563.58,567.88,561.20,575.14,385.10,9938230,13283148,508825334999,市值
39.63,14.27,
0.00,0.84,贝塔系数
12.20,2.16,股息/收益率： 	12.2/2.16
899700000,股本

61.00,

567.45,
0.34,
1.90,
Dec 10 07:59PM EDT,
Dec 10 04:00PM EDT,

566.43,前收盘

768976.00"; panhou成交量

"""
def get_us_stock_price(code):
	#http://hq.sinajs.cn/?_=0.9784360658377409&list=gb_yoku
	#http://hq.sinajs.cn/etag.php?rn=1386743228985&list=gb_yoku
	url = 'http://hq.sinajs.cn/etag.php?rn=%u&list=%s' % (int(time() * 1000), code)
	#ar hq_str_gb_yoku="
	"""	
	var hq_str_gb_sina="

	新浪,
	80.95,
	6.75,
	2013-12-11 09:42:28,
	5.12,
	75.60, <开盘

	81.98, 最高 区间
	75.60,最高 区间

	92.83,52最高
	44.30,52最低

	5785410,今天成交量
	2152413,10日均量
	5407460000,市值
	-0.20,每股收益
	--,市盈率
	
	0.00,
	1.45,贝塔系数
	0.00,
	0.00,
	
	66800000,股本
	86.00,
	
	81.05,
	0.12,
	0.10,
	Dec 10 07:20PM EDT,
	Dec 10 04:00PM EDT,
	75.83,前收盘
	12912.00";成交量

		#
	"""
	print url
	req = urllib2.Request(url)
	#如果不需要设置代理，下面的set_proxy就不用调用了。由于公司网络要代理才能连接外网，所以这里有set_proxy...
	#req.set_proxy('proxy.XXX.com:911', 'http')
	content = urllib2.urlopen(req).read()
	str = content.decode('gbk')
	#print type(str)
	#print str
	#print str.split('"')
		
	data = str.split('"')[1].split(',')
	print u"股票代码", data[0]
	print u"当前价", data[1]	#当前价
	print u"上涨%", data[2] #上涨百分比
	print u"上涨", data[4] #上涨价格
	print u"开盘", data[5] #开盘价格
	exit(0)
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

def get_all_us_stock_price(code_list):
	for code in code_list:
		get_us_stock_price(code)


def get_price(code):
	url = 'http://hq.sinajs.cn/?list=%s' % code
	req = urllib2.Request(url)
	#如果不需要设置代理，下面的set_proxy就不用调用了。由于公司网络要代理才能连接外网，所以这里有set_proxy...
	#req.set_proxy('proxy.XXX.com:911', 'http')
	content = urllib2.urlopen(req).read()
	str = content.decode('gbk')
	print type(str)
	data = str.split('"')[1].split(',')
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

def get_all_price(code_list):
	for code in code_list:
		get_price(code)


class Utility:
    @staticmethod
    def ToGB(str):
        return str.decode('gb2312')
    @staticmethod
    def ReadStocksToArray(file):
        file = open(file, 'r')
        stocks = []
        if file:
            for line in file:
                stocks.append(line.rstrip("\n"))
            file.close()
        else:
            print ("Error Opening File.")
        return stocks
        
class ColorConsole:
    @staticmethod
    def PrintStockInfoTitle():
        import datetime
        print(datetime.datetime.now())    
        print("Name".ljust(10) + "ID".ljust(10) + "CurrentPrice".ljust(20) + "Percent".ljust(10))  
        print('*****************************************************')
    @staticmethod
    def PrintStockInfoTitleWithColor():
        import WConio
        WConio.settitle("My Stock Info")
        WConio.clrscr()
        ColorConsole.PrintStockInfoTitle()
    @staticmethod    
    def PrintStockInfoItem(stockitem):
        print(stockitem[0].ljust(10) + str(stockitem[1]).ljust(10) +  str(stockitem[2]).ljust(20) + str(stockitem[3]).ljust(10))

    @staticmethod
    def PrintStockInfoItemWithColor(stockitem):
        import WConio
        WConio.textcolor(WConio.WHITE)
        if(stockitem[3]> 0.0):
            WConio.textcolor(WConio.RED)
            ColorConsole.PrintStockInfoItem(stockitem)
        else:
            WConio.textcolor(WConio.GREEN)
            ColorConsole.PrintStockInfoItem(stockitem)
        WConio.textcolor(WConio.WHITE)
"""http://www.cnblogs.com/itech/archive/2010/12/15/1907067.html"""            
class StockInfo:
    @staticmethod
    def GetStockStrByNum(num):
        f = urllib.urlopen('http://hq.sinajs.cn/list='+ str(num))
        stockstr = ""
        if f:
            stockstr = f.readline()
            f.close() 
        return  stockstr  
    @staticmethod                
    def ParseStockStr(stockstr):
        stockitem = []
        id = stockstr[13:19]
        slist=stockstr.split(',')
        name=slist[0][-4:]
        yesterdayendprice=slist[2]
        nowprice=slist[3]
        upgraderate=(float(nowprice)-float(yesterdayendprice))/float(yesterdayendprice)
        upgraderate= upgraderate * 100
        stockitem.append(name)
        stockitem.append(id)
        stockitem.append(nowprice)
        stockitem.append(upgraderate)
        return stockitem
    @staticmethod              
    def GetStockInfo(num):
        str=StockInfo.GetStockStrByNum(num)
        strGB=Utility.ToGB(str)
        return StockInfo.ParseStockStr(strGB)       

def RunWithOutColor():     
    stocks = Utility.ReadStocksToArray('Stocks.txt')
    ColorConsole.PrintStockInfoTitle()
    for stock in stocks:
        s = StockInfo.GetStockInfo(stock)
        ColorConsole.PrintStockInfoItem(s)
        
def RunWithColor():
    stocks = Utility.ReadStocksToArray('Stocks.txt')
    ColorConsole.PrintStockInfoTitleWithColor()
    for stock in stocks:
        s = StockInfo.GetStockInfo(stock)
        ColorConsole.PrintStockInfoItemWithColor(s)

def Main():
	print u"股票名称"
	print "我".decode("utf-8")
	get_all_us_stock_price(['gb_yoku'])
	sys.exit(0)
	code_list = ['sz300036', 'sz000977', 'sh600718', 'sh600452', 'sh600489']
	get_all_price(code_list)
	while(1):
		#RunWithOutColor()
		RunWithColor()
		import time
		time.sleep(60)


if __name__ == "__main__":
    Main()
