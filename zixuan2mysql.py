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
if sys.hexversion >= 0x02060000:
	from bs4 import BeautifulSoup
else:
	from BeautifulSoup import BeautifulSoup

from database.mysql import MySqlConfig, MySql

f_html = open("zixuan2.html", "r")	
html_order = f_html.read()
f_html.close()
#print html_order
	
soup = BeautifulSoup(html_order, convertEntities=BeautifulSoup.HTML_ENTITIES)

mysqlConfig = MySqlConfig(dbname='smartstrader')
mysql = MySql('smartstrader', 'smartstrader', True)
mysql.check(mysqlConfig)


tables = soup.div.findAll(name='table', recursive=False)
print soup.contents[0].name
print len(tables)



tr_stock_lists = tables[0].tbody.findAll(name='tr', recursive=False)
print len(tr_stock_lists)

for tr_symbol in tr_stock_lists:
	tds = tr_symbol.findAll(name='td', recursive=False)
	#print len(tds)
	#print tds[2].text
	#print tds[3].text
	sql = "SELECT * FROM  `stock_symbols`  WHERE `symbol` = '%s' " % tds[2].text
	result = mysql.query(sql)
	if result:
		print "xx"
	else:
		sql = """INSERT INTO `stock_symbols` (`symbol`, `cname`, `fname`, `brief`, `ipodate`, `52weeklow`, `52weekhigh`, `lastpriceopen`, `lastpriceclose`, `lastpricehigh`, `lastpricelow`, `change`, `changepc`, `volumeoftoday`, `marketvalue`, `PE`, `industry`, `exchange`) VALUES
('%s', '', '%s', '', '0000-00-00', '0.0000', '0.0000', '0.0000', '0.0000', '0.0000', '0.0000', '0.0000', '0.0000', 0, '0.0000', '0.0000', 0, 0);""" % (tds[2].text.encode('utf-8').strip(), tds[3].text.encode('utf-8').strip())
		#print sql
		result = mysql.query(sql)
	ths = tr_symbol.findAll(name='th', recursive=False)
	#print len(ths)
mysql.close()	
exit(-1)
main_td = tds[2]
main_tables = main_td.findAll(name='table', recursive=False)
#print main_tables[1]
print len(main_tables)
tdo_table = main_tables[0]
tdo_tr_header = tdo_table.findNext("tr", attrs={"bgcolor":"white"})
#print type(tdo_tr.td.text)
#print tdo_tr_header.td.text.find("Today's Orders")

tdo_trs = tdo_tr_header.findNextSiblings("tr", attrs={"class":"mainNormal"})
for tdo_tr in tdo_trs:
	tds = tdo_tr.findAll(name='td', recursive=False)
	print "Order Ref(href):", tds[1].a["href"]
	print "Order Ref:", tds[1].a.text
	
	print "B/S:", tds[2].text	#
	print "Qty:", tds[3].text
	print "Symbol:", tds[4].text
	print "Price:", tds[5].text
	print "C/E Time:", tds[6].text
	print "Last Quote:", tds[7].text
	print "Status:",  tds[8].text
	print "AON:",  tds[9].text
	print "GTC:",  tds[10].text
	print "Sett Curr.:",  tds[11].text
	print "Value (USD):",  tds[12].text
	print "C/R:",  tds[15].a["href"]
	print 



