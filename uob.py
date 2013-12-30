import httplib  
import urllib
import urllib2
import re
import sys
import ConfigParser


from urllib2 import Request, build_opener, HTTPCookieProcessor, HTTPHandler
import httplib, urllib, cookielib, Cookie, os

cj=[]


config = ConfigParser.RawConfigParser()
config.read('SmartSTrader.cfg')

UOB_USERNAME = ''
UOB_PASSWORD = ''

UOB_USERNAME = config.get('UOB_ONLINE', 'username')
UOB_PASSWORD = config.get('UOB_ONLINE', 'password')


order_pattern = re.compile("This order has been accepted under number:<b>(UB[0-9]+)</b>,<br>")
stock_symbol_pattern = re.compile("Market=[a-zA-Z]&Symbol=([A-Z]+)")
#SETP1
#fist connection attempt.
def ConnectToUOBWIthLogin():
	http_action = "GET"
	http_url    = '/hello/login.asp?reason=denied_empty&script_name=/'
	print "ACTION:%s\nURL:%s\n" % (http_action, http_url)
	conn=httplib.HTTPSConnection('us.uobkayhian.com', 443)
	conn.request(http_action, http_url)
	content = conn.getresponse()  
	#print content.getheaders()     
	#print content.status, content.reason


	if content.getheader('Set-Cookie')!=None:
		cj.append(content.getheader('Set-Cookie').split(';')[0])
	hdrs = content.getheader('set-cookie')
	#print "STEP-1:%s" % hdrs
	#print cj

	conn.close()

#SETP2 -- login
def SendLoginCredentialToUOB():
	http_action = "POST"
	http_url    = '/hello/login.asp'
	print "ACTION:%s\nURL:%s\n" % (http_action, http_url)
	
	values = {'PlatBrow' : '',
			  'Script_Name' : '/',
			  'USERNAME' : UOB_USERNAME,
	'PASSWORD': UOB_PASSWORD,
	'submit1.x' : '23',
	'submit1.y': '14'		  }

	data = urllib.urlencode(values)
	print data

	ck=''
	for item in cj:
		ck= ck+item + "; "
	ck=ck[0:-2]
	print "CK:%s" % ck
	
	data="PlatBrow=&Script_Name=%2F&USERNAME=%s&PASSWORD=%s&submit1.x=23&submit1.y=14" % (UOB_USERNAME, UOB_PASSWORD) 
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

	print headers
	conn.request("POST", "/hello/login.asp", data, headers)
	content = conn.getresponse()
	print content.getheaders()
	print content.read()
	print content.reason, content.status
	hdrs = content.getheader('set-cookie')

	status = content.status
	#if status == 302:

	if content.getheader('Set-Cookie')!=None:
		cj.append(content.getheader('Set-Cookie').split(';')[0])
		print "xx"
		print content.getheader('Set-Cookie')
	hdrs = content.getheader('set-cookie')
	print "STEP-2:%s" % hdrs
	print cj
		
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
	print "CK:%s" % ck
	hdrs = { 'User-Agent' : user_agent,
	'Host': 'us.uobkayhian.com', 
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'en-us,en;q=0.5',
	'Accept-Encoding': 'gzip, deflate',
	#'Connection': 'keep-alive',
	'Referer': 'https://us.uobkayhian.com/hello/login.asp?reason=denied_empty&script_name=/',
	'Cookie':ck}
	print hdrs
	conn.request("GET", "/default.asp?PlatBrow=", headers=hdrs)
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
	##print "STEP-3:%s" % hdrs
	#print cj
		
	conn.close()
	#print "##########\n\n"
	#exit(0)
	
	
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
def PlaceOrderToUOB():
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
	'Referer': 'https://us.uobkayhian.com/stocks/quote/quote.asp?Market=N&Symbol=YOKU',
	'Cookie':ck}

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
	
def ConfirmOrderToUOB():
	conn=httplib.HTTPSConnection('us.uobkayhian.com', 443)
	user_agent = 'Mozilla/5.0 (Windows NT 5.1; rv:12.0) Gecko/20100101 Firefox/12.0'
	ck=''
	order_no = None
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
		