#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from database.mysql import MySqlConfig, MySql

import httplib  
import urllib
import urllib2
from urllib2 import Request, build_opener, HTTPCookieProcessor, HTTPHandler
import httplib, urllib, cookielib, Cookie, os
import simplejson as json
from  simplejson.scanner import JSONDecodeError

from gzip import GzipFile

# deflate support
import zlib
import yaml
import re
import time
from StringIO import StringIO
import datetime
import subprocess
import MySQLdb

#http://stock.finance.sina.com.cn/usstock/api/jsonp.php/IO.XSRV2.CallbackList%5B%27fa8Vo3U4TzVRdsLs%27%5D/US_CategoryService.getList?page=1&num=20&sort=&asc=0&market=&id=

"""
http://biz.finance.sina.com.cn/suggest/lookup_n.php?q=$1&country=usstock
"""

def deflate(data):   # zlib only provides the zlib compress format, not the deflate format;
  try:               # so on top of all there's this workaround:
    return zlib.decompress(data, -zlib.MAX_WBITS)
  except zlib.error:
    return zlib.decompress(data)

	
def GetLastUpdateTime():	
	last_update = None
	url = 'http://hq.sinajs.cn/rn=1389255083862&list=gb_dji'
	data = ''
	user_agent = 'Mozilla/5.0 (Windows NT 5.1; rv:12.0) Gecko/20100101 Firefox/12.0'
	headers = { 'User-Agent' : user_agent,
	'Host': 'hq.sinajs.cn', 
	'Accept': '*/*',
	'Accept-Language': 'en-us,en;q=0.5',
	'Accept-Encoding': 'gzip, deflate',
	#'Connection': 'keep-alive',
	'Referer': 'http://finance.sina.com.cn/stock/usstock/sector.shtml',
	}

	req = urllib2.Request(url, data, headers)
	resp = urllib2.urlopen(req)
	old_resp = resp

	if resp.headers.get("content-encoding") == "gzip":
		gz = GzipFile(
					fileobj=StringIO(resp.read()),
					mode="r"
				)
		#resp = urllib2.addinfourl(gz, old_resp.headers, old_resp.url, old_resp.code)
		resp = urllib2.addinfourl(gz, old_resp.headers, old_resp.url)
		resp.msg = old_resp.msg
		#json_html = gz.read()
		#print 'xxx'
	# deflate
	if resp.headers.get("content-encoding") == "deflate":
		gz = StringIO( deflate(resp.read()) )
		#resp = urllib2.addinfourl(gz, old_resp.headers, old_resp.url, old_resp.code)  # 'class to add info() and
		resp = urllib2.addinfourl(gz, old_resp.headers, old_resp.url)  # 'class to add info() and
		resp.msg = old_resp.msg
		#json_html = gz.read()
		#print 'YY'
	js_script = resp.read()
	#print js_script
	last_update_time = js_script.split(',')[25]
	#print last_update_time
	#Jan 08 04:13PM EST
	ridx = last_update_time.rfind('EST')
	
	if ridx == -1:
		#try:
		raise ValueError('Timezone EST value not set')
		#except ValueError, e:
		#	print e
	else:
		last_update_time = last_update_time[:ridx].strip()
		print last_update_time
		last_update = datetime.datetime.strptime(last_update_time, "%b %d %I:%M%p")
		last_update = last_update.replace(datetime.date.today().year)
		print last_update
	
	return last_update

def GetSinaUSStockCategory(mysql):
	url = 'http://stock.finance.sina.com.cn/usstock/api/jsonp.php/var%20category=/US_CategoryService.getCategory'
	data = ''
	user_agent = 'Mozilla/5.0 (Windows NT 5.1; rv:12.0) Gecko/20100101 Firefox/12.0'
	headers = { 'User-Agent' : user_agent,
	'Host': 'stock.finance.sina.com.cn', 
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'en-us,en;q=0.5',
	'Accept-Encoding': 'gzip, deflate',
	#'Connection': 'keep-alive',
	'Referer': 'http://finance.sina.com.cn/stock/usstock/sector.shtml',
	}

	req = urllib2.Request(url, data, headers)
	resp = urllib2.urlopen(req)
	old_resp = resp

	if resp.headers.get("content-encoding") == "gzip":
		gz = GzipFile(
					fileobj=StringIO(resp.read()),
					mode="r"
				)
		#resp = urllib2.addinfourl(gz, old_resp.headers, old_resp.url, old_resp.code)
		resp = urllib2.addinfourl(gz, old_resp.headers, old_resp.url)
		resp.msg = old_resp.msg
		#json_html = gz.read()
		#print 'xxx'
	# deflate
	if resp.headers.get("content-encoding") == "deflate":
		gz = StringIO( deflate(resp.read()) )
		#resp = urllib2.addinfourl(gz, old_resp.headers, old_resp.url, old_resp.code)  # 'class to add info() and
		resp = urllib2.addinfourl(gz, old_resp.headers, old_resp.url)  # 'class to add info() and
		resp.msg = old_resp.msg
		#json_html = gz.read()
		#print 'YY'
	json_html = resp.read()
	#
	j_start = json_html.find("var category=(")
	j_start = j_start + len("var category=(")
	j_end = json_html.rfind(");")
	#print j_end
	#print j_start
	#print json_html[j_start:j_end]
	#data = json.loads(json_html[j_start:j_end])
	#yaml.load('[{id:"1",category:"basic materials"}]')
	your_string = re.sub(r'([a-zA-Z_]+):', r'"\1":', json_html[j_start:j_end])
	#print your_string
	json_obj = json.loads(your_string.decode('gbk'))
	#print json_obj[0]
	#print len(json_obj)
	for item in json_obj:
		print item['id']
		print item['category']
		print item['category_cn']
		print item['parent']
		#print item['child']
		for citem in item['child']:
			print '\t', citem['id']
			print '\t', citem['category']
			print '\t', citem['category_cn']
			print '\t', citem['parent']
		print "####"
	

EXCHANGE_NAME_TO_ID = {"NASDAQ": 1, "NYSE":2, "AMEX": 3}

def GetSinaUSStockList(page, last_update, mysql):
	#http://stock.finance.sina.com.cn/usstock/api/jsonp.php/IO.XSRV2.CallbackList%5B%27fa8Vo3U4TzVRdsLs%27%5D/US_CategoryService.getList?page=1&num=20&sort=&asc=0&market=&id=
	url = 'http://stock.finance.sina.com.cn/usstock/api/jsonp.php/IO.XSRV2.CallbackList%%5B%%27fa8Vo3U4TzVRdsLs%%27%%5D/US_CategoryService.getList?page=%d&num=60&sort=&asc=0&market=&id=' % page
	data = ''
	user_agent = 'Mozilla/5.0 (Windows NT 5.1; rv:12.0) Gecko/20100101 Firefox/12.0'
	headers = { 'User-Agent' : user_agent,
	'Host': 'stock.finance.sina.com.cn', 
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'en-us,en;q=0.5',
	'Accept-Encoding': 'gzip, deflate',
	#'Connection': 'keep-alive',
	'Referer': 'http://finance.sina.com.cn/stock/usstock/sector.shtml',
	}

	req = urllib2.Request(url, data, headers)
	resp = urllib2.urlopen(req)
	old_resp = resp

	if resp.headers.get("content-encoding") == "gzip":
		gz = GzipFile(
					fileobj=StringIO(resp.read()),
					mode="r"
				)
		#resp = urllib2.addinfourl(gz, old_resp.headers, old_resp.url, old_resp.code)
		resp = urllib2.addinfourl(gz, old_resp.headers, old_resp.url)
		resp.msg = old_resp.msg
		#json_html = gz.read()
		#print 'xxx'
	# deflate
	if resp.headers.get("content-encoding") == "deflate":
		gz = StringIO( deflate(resp.read()) )
		#resp = urllib2.addinfourl(gz, old_resp.headers, old_resp.url, old_resp.code)  # 'class to add info() and
		resp = urllib2.addinfourl(gz, old_resp.headers, old_resp.url)  # 'class to add info() and
		resp.msg = old_resp.msg
		#json_html = gz.read()
		#print 'YY'
	json_html = resp.read()
	#print json_html
	#
	json_html = re.sub(r'([a-zA-Z_]+):', r'"\1":', json_html)
	#json_html = re.sub(r'(McDonald\')', r"McDonald'", json_html)
	#json_html = json_html.replace("McDonald\\'s", "McDonald_s")
	#json_html = json_html.replace("O\\'Reilly", "O_Reilly")
	json_html = json_html.replace("\\'", "_")
	
	
	
	j_start = json_html.find("IO.XSRV2.CallbackList['fa8Vo3U4TzVRdsLs']((")
	j_start = j_start + len("IO.XSRV2.CallbackList['fa8Vo3U4TzVRdsLs']((")
	j_end = json_html.rfind("));")
	#print j_end
	#print j_start
	your_string = json_html[j_start:j_end]
	your_string = your_string.decode('gbk')
	#data = json.loads(json_html[j_start:j_end])
	#yaml.load('[{id:"1",category:"basic materials"}]')
	#your_string = re.sub(r'([a-zA-Z_]+):', r'"\1":', your_string)
	#print your_string
	#yesterday = datetime.date.today() - datetime.timedelta(1)
	#print yesterday
	s_trade_day = last_update.strftime("%Y-%m-%d")
	print s_trade_day
	#exit(0)
	try:
		json_obj = json.loads(your_string)
		print json_obj['count']
		items = json_obj['data']
		for item in items:
			print item['symbol']
			sql = "SELECT * FROM  `stock_symbols`  WHERE `symbol` = '%s' " % item['symbol'].encode('utf-8')
			result = mysql.query(sql)
			
			
			if result:
				#print "item['symbol']:%s in table" % item['symbol']
				result = mysql.query(sql)
				sid = result[0][0]
				#print sid
			else:
				sql = """INSERT INTO `stock_symbols` (`symbol`, `cname`, `fname`, `brief`, `ipodate`, `52weeklow`, `52weekhigh`, `lastpriceopen`, `lastpriceclose`, `lastpricehigh`, `lastpricelow`, `change`, `changepc`, `volumeoftoday`, `marketvalue`, `PE`, `industry`, `exchange`) VALUES
('%s', '%s', '%s', '', '0000-00-00', '0.0000', '0.0000', '0.0000', '0.0000', '0.0000', '0.0000', '0.0000', '0.0000', 0, '0.0000', '0.0000', 0, 0);""" % (item['symbol'].encode('utf-8').strip(), item['name'].encode('utf-8').strip(), item['cname'].encode('utf-8').strip())
				#print sql
				result = mysql.query(sql)
				#print "INSERT", mysql.lastrowid()
				sid = mysql.lastrowid()
			try:
				if item['pe'] is None:
					pe = 0
				else:
					pe = item['pe'].encode('utf-8').strip()
				sql = "INSERT INTO `smartstrader`.`trade_daily_history` (`sid`, `preclose`, `openprice`, `closeprice`, `highprice`, `lowprice`, `volume`, `mktcap`, `pe`, `tradeday`) VALUES ('%d', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (sid,  item['preclose'].encode('utf-8').strip(), item['open'].encode('utf-8').strip(), item['price'].encode('utf-8').strip(), item['high'].encode('utf-8').strip(), item['low'].encode('utf-8').strip(), item['volume'].encode('utf-8').strip(), item['mktcap'].encode('utf-8').strip(), pe, s_trade_day)
			except AttributeError:
				print item
				raise
				
			#print sql
			try:
				result = mysql.query(sql)
			except MySQLdb.IntegrityError, error:
				print error

		#print json_obj[0]
		#print len(json_obj)
	except JSONDecodeError, e:
		print your_string
		print e
		raise
	
def CheckWAMPServer():
	while True:
		process = subprocess.Popen(['pslist.exe', 'wampmanager'], shell=False, stdout=subprocess.PIPE)
		output = process.communicate()
		idx = output[0].find("wampmanager was not found on")
		if idx > 0:
			DETACHED_PROCESS = 0x00000008
			p = subprocess.Popen(["C:\\wamp\\wampmanager.exe"], shell=False, stdin=None, stdout=None, stderr=None, creationflags = DETACHED_PROCESS)
			time.sleep(120)
		else:
			return True
		#print output
	
if __name__ == "__main__":
	CheckWAMPServer()
	last_update = GetLastUpdateTime()
	#exit(0)
	mysqlConfig = MySqlConfig(dbname='smartstrader')
	mysql = MySql('smartstrader', 'smartstrader', True)
	mysql.check(mysqlConfig)

	GetSinaUSStockCategory(mysql)
	for i in range(1, 52):
		#if i < 50:
		#	continue
		print "page:%d" % i
		print GetSinaUSStockList(i, last_update, mysql)
		time.sleep(5)
		print 
		#exit(0)
	mysql.close()	
