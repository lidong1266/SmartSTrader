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


from order.uob import  *
from session.session import UOBSession


if __name__ == '__main__':
	print "s"
	print UOB_USERNAME
	print UOB_PASSWORD
	session = UOBSession()
	print session.GetCookie()
	session.Login("UOB")
	print session.GetCookie()
	while True:
		todays_orders = session.GetTodaysOrder()
		print todays_orders
		if not todays_orders:
			print "You don't have any today's order"
			#(self, symbol, action, order_type, price, stop_price, quntity)
			print "Try to place an order"
			#PlaceOrder(self, symbol, action, order_type, price, stop_price, quntity):
			session.PlaceOrder('QIHU', 'B', 'limit', 82.05, '', 1)
		else:
			print "Today's Order"
			print todays_orders
			
			
			
		raw_input("xx")
