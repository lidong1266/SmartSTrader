import httplib  
import urllib
import urllib2
import re
import sys
import ConfigParser
import logging

from urllib2 import Request, build_opener, HTTPCookieProcessor, HTTPHandler
import httplib, urllib, cookielib, Cookie, os


if sys.hexversion >= 0x02060000:
	from bs4 import BeautifulSoup
else:
	from BeautifulSoup import BeautifulSoup

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

cj=[]


config = ConfigParser.RawConfigParser()
config.read('SmartSTrader.cfg')

UOB_USERNAME = ''
UOB_PASSWORD = ''

UOB_USERNAME = config.get('UOB_ONLINE', 'username')
UOB_PASSWORD = config.get('UOB_ONLINE', 'password')

MARKET_SYMBOL = {"NASDAQ":"Q", "NYSE":"N", "AMEX":"A", "Q":"Q", "N":"N", "A":"A"}

order_pattern = re.compile("This order has been accepted under number:<b>(UB[0-9]+)</b>,<br>")
stock_symbol_pattern = re.compile("Market=[a-zA-Z]&Symbol=([A-Z]+)")

#SETP1
#fist connection attempt.
def ConnectToUOBWIthLogin():
	http_action = "GET"
	http_url    = '/hello/login.asp?reason=denied_empty&script_name=/'
	logger.debug("ACTION:%s\nURL:%s\n" % (http_action, http_url))
	conn=httplib.HTTPSConnection('us.uobkayhian.com', 443)
	conn.request(http_action, http_url)
	content = conn.getresponse()  
	#print content.status, content.reason
	if content.getheader('Set-Cookie') !=None:
		cj.append(content.getheader('Set-Cookie').split(';')[0])
		logger.debug("Set-Cookie:%s", content.getheader('Set-Cookie'))
	conn.close()

#SETP2 -- login
def SendLoginCredentialToUOB():
	http_action = "POST"
	http_url    = '/hello/login.asp'
	#print "ACTION:%s\nURL:%s\n" % (http_action, http_url)
	
	values = {'PlatBrow' : '',
			  'Script_Name' : '/',
			  'USERNAME' : UOB_USERNAME,
	'PASSWORD': UOB_PASSWORD,
	'submit1.x' : '23',
	'submit1.y': '14'		  }

	data = urllib.urlencode(values)
	#print data

	ck=''
	for item in cj:
		ck= ck+item + "; "
	ck=ck[0:-2]
	
	logger.debug("Cookie:%s", ck)
	
	data="PlatBrow=&Script_Name=%%2F&USERNAME=%s&PASSWORD=%s&submit1.x=23&submit1.y=14" % (UOB_USERNAME, UOB_PASSWORD) 
	conn=httplib.HTTPSConnection('us.uobkayhian.com', 443)
	user_agent = 'Mozilla/5.0 (Windows NT 5.1; rv:12.0) Gecko/20100101 Firefox/12.0'
	headers = { 'User-Agent' : user_agent,
	'Host': 'us.uobkayhian.com', 
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'en-us,en;q=0.5',
	'Accept-Encoding': 'gzip, deflate',
	#'Connection': 'keep-alive',
	'Referer': 'https://us.uobkayhian.com/hello/login.asp?reason=denied_empty&script_name=/',
	'Cookie':ck,
	"Content-type": "application/x-www-form-urlencoded"}

	#print headers
	conn.request("POST", "/hello/login.asp", data, headers)
	content = conn.getresponse()
	#print content.getheaders()
	#print content.read()
	#print content.reason, content.status
	hdrs = content.getheader('set-cookie')

	status = content.status
	if status == 302:
		location = content.getheader('location')
		if location == "/hello/failed.asp":
			raise Exception('Caution: Login failed, please check your login credential!')
		elif location == "/default.asp?PlatBrow=":
			logger.info('Login to UOB Kay Hian Successfully')
		else:	
			raise Exception('Caution: Unknown redirection url')
	else:
		raise Exception('Caution: Unexpected HTTP status code')
	if content.getheader('Set-Cookie')!=None:
		cj.append(content.getheader('Set-Cookie').split(';')[0])
		#print "xx"
		#print content.getheader('Set-Cookie')
	#hdrs = content.getheader('set-cookie')
	#print "STEP-2:%s" % hdrs
	#print cj
		
	conn.close()

	#print "##########\n\n"

	#exit(0)
	
def BrowserToPlatBrow():
	"""GET /default.asp?PlatBrow= HTTP/1.1
	Host: us.uobkayhian.com
	User-Agent: Mozilla/5.0 (Windows NT 5.1; rv:12.0) Gecko/20100101 Firefox/12.0
	Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
	Accept-Language: en-us,en;q=0.5
	Accept-Encoding: gzip, deflate
	Connection: keep-alive
	Referer: 
	Cookie: ASPSESSIONIDASDRCBTB=xxx; KDICKDKYKBIBII0XHVKVYKLKWIQUZTKPKCKAWIE...=xxx"""
		
	conn=httplib.HTTPSConnection('us.uobkayhian.com', 443)
	user_agent = 'Mozilla/5.0 (Windows NT 5.1; rv:12.0) Gecko/20100101 Firefox/12.0'
	ck=''
	for item in cj:
		ck= ck+item + "; "
	ck=ck[0:-2]
	#print "CK:%s" % ck
	hdrs = { 'User-Agent' : user_agent,
	'Host': 'us.uobkayhian.com', 
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'en-us,en;q=0.5',
	'Accept-Encoding': 'gzip, deflate',
	#'Connection': 'keep-alive',
	'Referer': 'https://us.uobkayhian.com/hello/login.asp?reason=denied_empty&script_name=/',
	'Cookie':ck}
	#print hdrs
	conn.request("GET", "/default.asp?PlatBrow=", headers=hdrs)
	content = conn.getresponse()
	#print content.getheaders()
	#print content.read()
	#print content.reason, content.status
	hdrs = content.getheader('set-cookie')

	status = content.status
	if status == 302:
		location = content.getheader('location')
		if location == "/markets/top/top.asp?MenuID=trade":
			logger.info('Browser to trade platform successfully')
		else:	
			raise Exception('Caution: Unknown redirection url')
	else:
		raise Exception('Caution: Unexpected HTTP status code')

	if content.getheader('Set-Cookie')!=None:
		cj.append(content.getheader('Set-Cookie').split(';')[0])
	hdrs = content.getheader('set-cookie')
	##print "STEP-3:%s" % hdrs
	#print cj
		
	conn.close()
	#print "##########\n\n"
	#exit(0)
	return cj
	
	
"""GET /markets/top/top.asp?MenuID=trade HTTP/1.1
Host: us.uobkayhian.com
User-Agent: Mozilla/5.0 (Windows NT 5.1; rv:12.0) Gecko/20100101 Firefox/12.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-us,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive
Referer: https://us.uobkayhian.com/hello/login.asp?reason=denied_empty&script_name=/
Cookie: ASPSESSIONIDASDRCBTB=xxxx; KDICKDKYKBIBII0XHVKVYKLKWIQUZTKPKCKAWIEKLKDHBIA=ssss; ASPSESSIONIDSQBTADTB=yyyy"""
def NavigateToTradeMenu():
	conn=httplib.HTTPSConnection('us.uobkayhian.com', 443)
	user_agent = 'Mozilla/5.0 (Windows NT 5.1; rv:12.0) Gecko/20100101 Firefox/12.0'
	ck=''
	for item in cj:
		ck= ck+item + "; "
	ck=ck[0:-2]
	#print "CK:%s" % ck
	hdrs = { 'User-Agent' : user_agent,
	'Host': 'us.uobkayhian.com', 
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'en-us,en;q=0.5',
	'Accept-Encoding': 'gzip, deflate',
	#'Connection': 'keep-alive',
	'Referer': 'https://us.uobkayhian.com/hello/login.asp?reason=denied_empty&script_name=/',
	'Cookie':ck}

	conn.request("GET", "/markets/top/top.asp?MenuID=trade", headers=hdrs)
	content = conn.getresponse()
	print content.getheaders()
	#print content.read()
	#print content.reason, content.status
	hdrs = content.getheader('set-cookie')

	status = content.status
	#if status == 302:

	if content.getheader('Set-Cookie')!=None:
		cj.append(content.getheader('Set-Cookie').split(';')[0])
	hdrs = content.getheader('set-cookie')
	#print "4:%s" % hdrs
	#print cj
		
	conn.close()
	#exit(0)
"""
GET /stocks/search/findcompany.asp?market=N&choice=0&search_string=qihu&x=12&y=14 HTTP/1.1
Host: us.uobkayhian.com
User-Agent: Mozilla/5.0 (Windows NT 5.1; rv:25.0) Gecko/20100101 Firefox/25.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: https://us.uobkayhian.com/markets/top/top.asp?MenuID=trade
Cookie: ASPSESSIONIDASDRCBTB=xxxx; KDICKDKYKBIBII0XHVKVYKLKWIQUZTKPKCKAWIEKLKDHBIA=ssss; ASPSESSIONIDSQBTADTB=yyyy
Connection: keep-alive

HTTP/1.1 302 Object moved
Server: Microsoft-IIS/5.0
Date: Tue, 10 Dec 2013 09:52:38 GMT
Pragma: no-cache
Cache-Control: private, private
Expires: 0
Location: /stocks/quote/quote.asp?Market=N&Symbol=QIHU
Content-Length: 121
Content-Type: text/html

"""	
def FindCompanyBySymbol(symbol):
	stock_symbol = None
	http_location = None
	conn=httplib.HTTPSConnection('us.uobkayhian.com', 443)
	user_agent = 'Mozilla/5.0 (Windows NT 5.1; rv:12.0) Gecko/20100101 Firefox/12.0'
	ck=''
	for item in cj:
		ck= ck+item + "; "
	ck=ck[0:-2]
	#print "CK:%s" % ck
	hdrs = { 'User-Agent' : user_agent,
	'Host': 'us.uobkayhian.com', 
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'en-us,en;q=0.5',
	'Accept-Encoding': 'gzip, deflate',
	#'Connection': 'keep-alive',
	'Referer': 'https://us.uobkayhian.com/markets/top/top.asp?MenuID=trade',
	'Cookie':ck}

	http_url = "/stocks/search/findcompany.asp?market=N&choice=0&search_string=%s&x=12&y=14" % (symbol)
	conn.request("GET", http_url, headers=hdrs)
	content = conn.getresponse()
	print content.getheaders()
	#print content.read()
	#print content.reason, content.status
	hdrs = content.getheader('set-cookie')

	status = content.status
	if status == 302:
		http_location = content.getheader('Location')
		print http_location
		stock_symbol_m =  stock_symbol_pattern.search(http_location)
		if stock_symbol_m:
			stock_symbol = stock_symbol_m.group(1)
			print "stock_symbol:%s" % stock_symbol
	else:
		pass
	if content.getheader('Set-Cookie')!=None:
		cj.append(content.getheader('Set-Cookie').split(';')[0])
	hdrs = content.getheader('set-cookie')
	#print "4:%s" % hdrs
	#print cj
		
	conn.close()
	return (http_location, stock_symbol)


	#exit(0)	
"""
GET /stocks/quote/quote.asp?Market=N&Symbol=YOKU HTTP/1.1
Host: us.uobkayhian.com
User-Agent: Mozilla/5.0 (Windows NT 5.1; rv:12.0) Gecko/20100101 Firefox/12.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-us,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive
Referer: https://us.uobkayhian.com/markets/top/top.asp?MenuID=trade
Cookie: ASPSESSIONIDASDRCBTB=xxxx; KDICKDKYKBIBII0XHVKVYKLKWIQUZTKPKCKAWIEKLKDHBIA=ssss; ASPSESSIONIDSQBTADTB=yyyy"""
def SearchStockSymbol(symbol):
	conn=httplib.HTTPSConnection('us.uobkayhian.com', 443)
	user_agent = 'Mozilla/5.0 (Windows NT 5.1; rv:12.0) Gecko/20100101 Firefox/12.0'
	ck=''
	for item in cj:
		ck= ck+item + "; "
	ck=ck[0:-2]
	#print "CK:%s" % ck
	hdrs = { 'User-Agent' : user_agent,
	'Host': 'us.uobkayhian.com', 
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'en-us,en;q=0.5',
	'Accept-Encoding': 'gzip, deflate',
	#'Connection': 'keep-alive',
	'Referer': 'https://us.uobkayhian.com/markets/top/top.asp?MenuID=trade',
	'Cookie':ck}

	conn.request("GET", "/stocks/quote/quote.asp?Market=N&Symbol=YOKU", headers=hdrs)
	content = conn.getresponse()
	print content.getheaders()
	#print content.read()
	#print content.reason, content.status
	hdrs = content.getheader('set-cookie')

	status = content.status
	#if status == 302:

	if content.getheader('Set-Cookie')!=None:
		cj.append(content.getheader('Set-Cookie').split(';')[0])
	hdrs = content.getheader('set-cookie')
	#print "4:%s" % hdrs
	#print cj
		
	conn.close()


	#exit(0)

"""
GET /trade/execute/trade_U.asp?market=N&preorgood=0&transaction=B&symbol=YOKU&quantity=1&type=0&price=1&stop=&fill=0&valid=0&currency=USD HTTP/1.1
Host: us.uobkayhian.com
User-Agent: Mozilla/5.0 (Windows NT 5.1; rv:12.0) Gecko/20100101 Firefox/12.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-us,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive
Referer: https://us.uobkayhian.com/stocks/quote/quote.asp?Market=N&Symbol=YOKU
Cookie: ASPSESSIONIDASDRCBTB=xxxx; KDICKDKYKBIBII0XHVKVYKLKWIQUZTKPKCKAWIEKLKDHBIA=ssss; ASPSESSIONIDSQBTADTB=yyyy"""
def PlaceOrderToUOB(cookie, symbol, market, type, limit, price, quantity, currency):
	conn=httplib.HTTPSConnection('us.uobkayhian.com', 443)
	user_agent = 'Mozilla/5.0 (Windows NT 5.1; rv:12.0) Gecko/20100101 Firefox/12.0'
	ck=''
	if not isinstance(cookie, str):
		ck = "; ".join(cookie)
	else:
		ck = cookie	
	#print "CK:%s" % ck
	hdrs = { 'User-Agent' : user_agent,
	'Host': 'us.uobkayhian.com', 
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'en-us,en;q=0.5',
	'Accept-Encoding': 'gzip, deflate',
	#'Connection': 'keep-alive',
	'Referer': 'https://us.uobkayhian.com/stocks/quote/quote.asp?Market=N&Symbol=YOKU',
	'Cookie':ck}
	
	if MARKET_SYMBOL.has_key(market.upper()):
		markey_symbol = MARKET_SYMBOL[market.upper()]
	else:
		return
	conn.request("GET", "/trade/execute/trade_U.asp?market=N&preorgood=0&transaction=B&symbol=YOKU&quantity=1&type=0&price=1&stop=&fill=0&valid=0&currency=USD", headers=hdrs)
	content = conn.getresponse()
	#print content.getheaders()
	#print content.reason, content.status
	hdrs = content.getheader('set-cookie')
	#print hdrs
	f_order = open("order.html", "w")
	html_order = content.read()
	f_order.write(html_order)
	f_order.close()
	status = content.status
	#if status == 302:

	if content.getheader('Set-Cookie')!=None:
		cj.append(content.getheader('Set-Cookie').split(';')[0])
	hdrs = content.getheader('set-cookie')
	#print "4:%s" % hdrs
	#print cj
		
	conn.close()
	
def ConfirmOrderToUOB(cookie, symbol, market, type, limit, price, quantity, currency):
	conn=httplib.HTTPSConnection('us.uobkayhian.com', 443)
	user_agent = 'Mozilla/5.0 (Windows NT 5.1; rv:12.0) Gecko/20100101 Firefox/12.0'
	ck=''
	order_no = None

	if not isinstance(cookie, str):
		ck = "; ".join(cookie)
	else:
		ck = cookie	
	#print "CK:%s" % ck
	hdrs = { 'User-Agent' : user_agent,
	'Host': 'us.uobkayhian.com', 
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'en-us,en;q=0.5',
	'Accept-Encoding': 'gzip, deflate',
	#'Connection': 'keep-alive',
	'Referer': "https://us.uobkayhian.com/trade/execute/trade_U.asp?market=N&preorgood=0&transaction=B&symbol=YOKU&quantity=1&type=0&price=1&stop=&fill=0&valid=0&currency=USD",
	'Cookie':ck}

	url = "/trade/execute/exec_U.asp?market=U&transaction=B&quantity=1&symbol=YOKU&type=0&valid=0&fill=0&price=1&stop=&currency=USD&preorgood=1&Password=%s" % UOB_PASSWORD
	conn.request("GET", url, headers=hdrs)
	content = conn.getresponse()
	#print content.getheaders()
	#print content.reason, content.status
	hdrs = content.getheader('set-cookie')
	#print hdrs
	f_order = open("confirm.html", "w")
	html_order = content.read()
	f_order.write(html_order)
	f_order.close()
	status = content.status
	#if status == 302:

	if content.getheader('Set-Cookie')!=None:
		cj.append(content.getheader('Set-Cookie').split(';')[0])
	hdrs = content.getheader('set-cookie')
	#print "4:%s" % hdrs
	#print cj
	if status == 302:
		http_location = content.getheader('Location')
		print http_location
		order_no_m =  order_pattern.search(http_location)
		if order_no_m:
			order_no = order_no_m.group(1)
		#"placed_U.asp?market=U&transaction=B&quantity=1&symbol=YOKU&type=0&price=1&stop=&fill=0&valid=0&sOut=This order has been accepted under number:<b>UB1682331</b>,<br>and will be sent to the NYSE exchange.<br><br>Please note that number for future reference.&lastPrice=30.5&dBid=0&dAsk=0&dcommission=0&currency=USD"
		
	conn.close()
	return order_no
#https://us.uobkayhian.com/trade/execute/exec_U.asp?market=U&transaction=B&quantity=1&symbol=YOKU&type=0&valid=0&fill=0&price=1&stop=&currency=USD&preorgood=1&Password=%UOB_PASSWORD%	
#https://us.uobkayhian.com/trade/execute/placed_U.asp?market=U&transaction=B&quantity=1&symbol=YOKU&type=0&price=1&stop=&fill=0&valid=0&sOut=This%20order%20has%20been%20accepted%20under%20number:%3Cb%3EUB1682329%3C/b%3E,%3Cbr%3Eand%20will%20be%20sent%20to%20the%20NYSE%20exchange.%3Cbr%3E%3Cbr%3EPlease%20note%20that%20number%20for%20future%20reference.&lastPrice=30.5&dBid=0&dAsk=0&dcommission=0&currency=USD
#https://us.uobkayhian.com/trade/execute/placed_U.asp?market=U&transaction=B&quantity=1&symbol=YOKU&type=0&price=1&stop=&fill=0&valid=0&sOut=This%20order%20has%20been%20accepted%20under%20number:%3Cb%3EUB1682329%3C/b%3E,%3Cbr%3Eand%20will%20be%20sent%20to%20the%20NYSE%20exchange.%3Cbr%3E%3Cbr%3EPlease%20note%20that%20number%20for%20future%20reference.&lastPrice=30.5&dBid=0&dAsk=0&dcommission=0&currency=USD
#https://us.uobkayhian.com/myaccount/cancel/cancel2.asp
#Submit=Cancel
#order=UB1682334
#order=UB1682333
#order=UB1682331
#password=%UOB_PASSWORD%
#order=UB1682334&order=UB1682333&order=UB1682331&password=%UOB_PASSWORD%&Submit=Cancel
"""
POST /myaccount/cancel/cancel2.asp HTTP/1.1

Host: us.uobkayhian.com

User-Agent: Mozilla/5.0 (Windows NT 5.1; rv:25.0) Gecko/20100101 Firefox/25.0

Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8

Accept-Language: en-US,en;q=0.5

Accept-Encoding: gzip, deflate

Referer: https://us.uobkayhian.com/myaccount/portfolio/getOrders.asp?MenuID=orderb&type=today

Cookie: ASPSESSIONIDASDRCBTB=NAOMBHODOBFILKKHKANPAMAJ; KDICKDKYKBIBII0XHVKVYKLKWIQUZTKPKCKAWIEKLKDHBIAYKLKXIC=YWQIEKCHJFKDIBVIRUMKZEIANKJKGKXOAFN; ASPSESSIONIDQSBRCDTB=OAOMBHODPGFJNLPJDPGBDBLF

Connection: keep-alive

Request Headers From Upload Stre
"""
def CancelOrderToUOB(order_no):
	conn=httplib.HTTPSConnection('us.uobkayhian.com', 443)
	user_agent = 'Mozilla/5.0 (Windows NT 5.1; rv:12.0) Gecko/20100101 Firefox/12.0'
	ck=''
	for item in cj:
		ck= ck+item + "; "
	ck=ck[0:-2]
	#print "CK:%s" % ck
	hdrs = { 'User-Agent' : user_agent,
	'Host': 'us.uobkayhian.com', 
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'en-us,en;q=0.5',
	'Accept-Encoding': 'gzip, deflate',
	#'Connection': 'keep-alive',
	'Referer': "https://us.uobkayhian.com/myaccount/portfolio/getOrders.asp?MenuID=orderb&type=today",
	'Cookie':ck,
	"Content-type": "application/x-www-form-urlencoded"}

	if isinstance(order_no, str):
		data="order=%s&password=%s&Submit=Cancel" % (order_no, UOB_PASSWORD)
	else:
		order_params = ''
		for order in order_no:		
			order_params = order_params + "order=%s&" % (order)
		data="%spassword=%s&Submit=Cancel" % (order_params, UOB_PASSWORD)
	print data
	#order=UB1682364&password=%UOB_PASSWORD%&Submit=Cancel
	#order=UB1682364&password=%UOB_PASSWORD%&Submit=Cancel
	conn.request("POST", "/myaccount/cancel/cancel2.asp", data, headers=hdrs)
	content = conn.getresponse()
	#print content.getheaders()
	#print content.reason, content.status
	hdrs = content.getheader('set-cookie')
	#print hdrs
	f_order = open("cancel.html", "w")
	#UBxxxx: Order UBxxxx has been canceled.
	html_order = content.read()
	
	cancel_order_pattern = re.compile("(UB[0-9]+):\\s+Order\\s+(UB[0-9]+) has been canceled")
	#UBxxxx: Order UBxxxx has been canceled.
	cancel_order_m =  cancel_order_pattern.search(html_order)
	if cancel_order_m:
		order_no_result = cancel_order_m.group(1)
	if order_no_result == order_no:
		print "Cancel successfully"
	f_order.write(html_order)
	f_order.close()
	status = content.status
	#if status == 302:

	if content.getheader('Set-Cookie')!=None:
		cj.append(content.getheader('Set-Cookie').split(';')[0])
	hdrs = content.getheader('set-cookie')
	#print "4:%s" % hdrs
	#print cj
		
	conn.close()

class UOBOrder():
	def __init__(self):
		self.orderId = ''
		self.orderUrl = ''
		self.orderType = 'B'
		self.Qty = 0
		self.Symbol = ''
		self.Price = 0
		self.time = None
		self.lastQuote = 0
		self.status = 'B'
		self.Aon = ''
		self.Gtc = 'Day'
		self.SettCur = 'USD'
		self.Value = 0
		self.crUrl = ''
	def __str__(self):
		return "Order:%s" % self.orderId
	
def ParseTodaysOrder(html):	
	
	uob_orders = []
	soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES)
	
	tables = soup.html.body.findAll(name='table', recursive=False)
	

	#Second table
	tds = soup.html.body.table.findNextSibling("table").tr.findAll(name='td', recursive=False)
	if len(tds) < 4:
		return None
	
	
	main_td = tds[2]
	
	main_tables = main_td.findAll(name='table', recursive=False)
	if len(main_tables) <= 1:
		return None
	
	if html.find("There are currently no orders to display") != -1:
		return None
	#Today's Orders 
	tdo_table = main_tables[0]
	tdo_tr_header = tdo_table.findNext("tr", attrs={"bgcolor":"white"})
	
	# Try to find text
	if tdo_tr_header.td.text.find("Today's Orders") == -1:
		return None

	# All today's order has a row with class "mainNormal"
	tdo_trs = tdo_tr_header.findNextSiblings("tr", attrs={"class":"mainNormal"})
	for tdo_tr in tdo_trs:
		tds = tdo_tr.findAll(name='td', recursive=False)
		uob_order = UOBOrder()
		print "Order Ref(href):", tds[1].a["href"]
		uob_order.orderUrl = tds[1].a["href"]
		
		uob_order.orderId = tds[1].a.text
		print "Order Ref:", tds[1].a.text
		
		print "B/S:", tds[2].text	#
		uob_order.orderType = tds[2].text
		
		print "Qty:", tds[3].text
		uob_order.Qty = int(tds[3].text)
		
		print "Symbol:", tds[4].text
		uob_order.Symbol = tds[4].text
		
		print "Price:", tds[5].text
		uob_order.Price = float(tds[5].text)
		
		print "C/E Time:", tds[6].text
		uob_order.time = tds[6].text
		
		print "Last Quote:", tds[7].text
		uob_order.lastQuote = float(tds[7].text)
		
		print "Status:",  tds[8].text
		uob_order.status = tds[8].text
		
		print "AON:",  tds[9].text
		uob_order.Aon = tds[9].text
		
		print "GTC:",  tds[10].text
		uob_order.Gtc = tds[10].text
		
		print "Sett Curr.:",  tds[11].text
		uob_order.SettCur = tds[11].text
		
		print "Value (USD):",  tds[12].text
		uob_order.Value = float(tds[12].text)
		
		print "C/R:",  tds[15].a["href"]
		uob_order.crUrl = tds[15].a["href"]
		
		print "xx"
		print uob_order
		uob_orders.append(uob_order)
	
	#Other Orders
	other_od_table = main_tables[1]
	#print other_od_table
	other_od_tr_header = other_od_table.findNext("tr", attrs={"bgcolor":"white"})
	#print other_od_tr_header.td.text
	other_od_tr_title = other_od_tr_header.findNextSibling("tr", attrs={"class":"mainBold"})
	other_od_trs = other_od_tr_title.findNextSiblings("tr")
	#print other_od_trs
	for other_od_tr in other_od_trs:
		#print other_od_tr
		tds = other_od_tr.findAll(name='td', recursive=False)
		#print other_od_tr
		print tds[0].text
		print tds[1].text
		print tds[2].text
		print tds[3].text
		print tds[4].text
		print tds[5].text
		print 	
	return uob_orders
	
def GetTodaysOrder(cookie):
	conn=httplib.HTTPSConnection('us.uobkayhian.com', 443)
	user_agent = 'Mozilla/5.0 (Windows NT 5.1; rv:12.0) Gecko/20100101 Firefox/12.0'
	ck=''	
	if not isinstance(cookie, str):
		ck = "; ".join(cookie)
	else:
		ck = cookie

	hdrs = { 'User-Agent' : user_agent,
	'Host': 'us.uobkayhian.com', 
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'en-us,en;q=0.5',
	'Accept-Encoding': 'gzip, deflate',
	#'Connection': 'keep-alive',
	'Referer': "https://us.uobkayhian.com/markets/top/top.asp?MenuID=trade",
	'Cookie':ck}

	url = "/myaccount/portfolio/getOrders.asp?MenuID=orderb&type=today"
	conn.request("GET", url, headers=hdrs)
	content = conn.getresponse()
	#print content.getheaders()
	#print content.reason, content.status
	#hdrs = content.getheader('set-cookie')
	#print hdrs
	f_order = open("today_order.html", "w")
	html_order = content.read()
	f_order.write(html_order)
	f_order.close()
	orders = ParseTodaysOrder(html_order)
	status = content.status
	
	conn.close()
	return orders

	
if __name__ == "__main__":
	print "HELLO UOB"
	ConnectToUOBWIthLogin()
	SendLoginCredentialToUOB()
	BrowserToPlatBrow()
	NavigateToTradeMenu()
	
	prompt = "Stock symbol you want to search:"
	choice = raw_input(prompt)
	http_location, stock_symbol = FindCompanyBySymbol(choice)
	print http_location
	print stock_symbol
	sys.exit(0)
	SearchStockSymbol("YOKU")
	PlaceOrderToUOB()
	order_no = ConfirmOrderToUOB()
	if order_no is not None:
		print "order:%s" % order_no
		prompt = "Do you want to cancel this oder(%s):" % order_no
		choice = raw_input(prompt)
		if choice == "Y" or choice == "y" :
			CancelOrderToUOB(order_no)
		