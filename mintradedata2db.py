#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import os

from database.mysql import MySqlConfig, MySql
from stream.stream import Stream, StreamHandler

from datetime import *

class MysqlStreamHandler(StreamHandler):
	def __init__(self, db):
		self.db = db
	def Handle_Data(self, data):
		print data[0]
		print data[1]
		print data[2]
		dt_now = datetime.now()
		str_now = dt_now.strftime("%Y-%m-%d %H:%M:%S")
		sql = "INSERT INTO  `trade_minute_history` (`sid`, `price`, `volume`, `server_time`, `client_time`) VALUES (1, '%s', '%s', '%s', '%s')" % (data[1], data[10], data[3], str_now);
		#print sql
		self.db.query(sql)
		pass
		
def Main():
	mysqlConfig = MySqlConfig(dbname='smartstrader')
	mysql = MySql('smartstrader', 'smartstrader', True)
	mysql.check(mysqlConfig)
	stream = Stream('QUNR', '', None, 15)
	handler = MysqlStreamHandler(mysql)
	stream.RegisterHandler(handler)
	
	print "SSS"
	#stream = Stream('QIHU', '')
	stream.StartPoll()
	print 'xxx'
	sleep(10 * 3600)
	print "xx"
	
if __name__ == "__main__":
    Main()
