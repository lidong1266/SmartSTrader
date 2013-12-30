import ystockquote


while True:
	symbol = raw_input("Please input stock symbol:")
	print(ystockquote.get_price_book(symbol))
	print(ystockquote.get_bid_realtime(symbol))
	print ystockquote.get_historical_prices(symbol, '2013-12-01', '2013-12-10')