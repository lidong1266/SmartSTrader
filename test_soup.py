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

f_html = open("today_order.html", "r")	
html_order = f_html.read()
f_html.close()
#print html_order
	
soup = BeautifulSoup(html_order, convertEntities=BeautifulSoup.HTML_ENTITIES)

#print soup.html.body.table
tables = soup.html.body.findAll(name='table', recursive=False)
#print soup.html.body.table.findNextSibling("table")

tds = soup.html.body.table.findNextSibling("table").tr.findAll(name='td', recursive=False)
#print len(tds)
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
	#print tds[1].txt
#print other_od_trs
#print other_od_tr_title
#
#print len(tdo_trs)
#print "########"
#print soup.html.body.table.next
#print soup.html.body.table.next.next
#print soup.html.body.table.nextSibling.name
#print soup.html.body.table.nextSibling.nextSibling.name
#print soup.html.body.table.nextSibling.nextSibling.nextSibling.name
#print soup.html.body.table.nextSibling.nextSibling.nextSibling.nextSibling.name
#print soup.html.body.table.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.name
#print soup.html.body.table.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.nextSibling.name



