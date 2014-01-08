#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from database.mysql import MySqlConfig, MySql

import httplib  
import urllib
import urllib2
from urllib2 import Request, build_opener, HTTPCookieProcessor, HTTPHandler
import httplib, urllib, cookielib, Cookie, os
import simplejson as json
from gzip import GzipFile

# deflate support
import zlib
import yaml
import re
import time
from StringIO import StringIO
#http://stock.finance.sina.com.cn/usstock/api/jsonp.php/IO.XSRV2.CallbackList%5B%27fa8Vo3U4TzVRdsLs%27%5D/US_CategoryService.getList?page=1&num=20&sort=&asc=0&market=&id=

mysqlConfig = MySqlConfig(dbname='smartstrader')
mysql = MySql('smartstrader', 'smartstrader', True)
mysql.check(mysqlConfig)


def deflate(data):   # zlib only provides the zlib compress format, not the deflate format;
  try:               # so on top of all there's this workaround:
    return zlib.decompress(data, -zlib.MAX_WBITS)
  except zlib.error:
    return zlib.decompress(data)


def GetSinaUSStockCategory():
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
	

def GetSinaUSStockList(page):
	#http://stock.finance.sina.com.cn/usstock/api/jsonp.php/IO.XSRV2.CallbackList%5B%27fa8Vo3U4TzVRdsLs%27%5D/US_CategoryService.getList?page=1&num=20&sort=&asc=0&market=&id=
	url = 'http://stock.finance.sina.com.cn/usstock/api/jsonp.php/IO.XSRV2.CallbackList%%5B%%27fa8Vo3U4TzVRdsLs%%27%%5D/US_CategoryService.getList?page=%d&num=20&sort=&asc=0&market=&id=' % page
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
	json_html = json_html.replace("McDonald\\'s", "McDonald_s")
	
	
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
	json_obj = json.loads(your_string)
	print json_obj['count']
	items = json_obj['data']
	for item in items:
		print item['symbol']
	#print json_obj[0]
	#print len(json_obj)
	
	
	
if __name__ == "__main__":
	GetSinaUSStockCategory()
	for i in range(386):
		print "page:%d" % i
		print GetSinaUSStockList(i)
		time.sleep(5)
		print 

