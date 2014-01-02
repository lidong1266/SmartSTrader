#!/usr/bin/env python
#
#  Copyright (c) 2013, Corey Goldberg (cgoldberg@gmail.com)
#
#  license: GNU LGPL
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License, or (at your option) any later version.
#
#  Requires: Python 2.7/3.2+

import sys
import stockquote
import time

from database.mysql import MySqlConfig, MySql


mysqlConfig = MySqlConfig(dbname='smartstrader')
mysql = MySql('smartstrader', 'smartstrader', True)
mysql.check(mysqlConfig)

EXG_ID = {"NASDAQ":1, "NYSE":2, "AMEX":3}

sql = "SELECT * FROM  `stock_symbols`  WHERE `exchange` = 0"
results = mysql.query(sql)
if results:
	for item in results:
		#print item[0]
		#print item[1]
		quote = stockquote.from_google(item[1])
		if not EXG_ID.has_key(quote['exchange']):
			print item[1], ":", quote['exchange']
		else:
			sql = """UPDATE  `smartstrader`.`stock_symbols` SET  `exchange` =  '%d' WHERE  `stock_symbols`.`sid` =%d;""" % (EXG_ID[quote['exchange']], item[0])
			print sql
			result = mysql.query(sql)
		time.sleep(30)

