from __future__ import (absolute_import, division, print_function,
						unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

# Import the backtrader platform
import backtrader as bt
import pandas as pd
import thoughts

def loadCsvStock(startdate,enddate,stname='AAPL'):
	# Create a Data Feed
	dataframe = pd.read_csv('./stockdata/'+stname+'.csv', index_col=0, parse_dates=True)
	dataframe['openinterest'] = 0
	data = bt.feeds.PandasData(
		dataname=dataframe,
		# openinterest=-1,
		fromdate=startdate,
		todate=enddate
		)
	return data


if __name__ == '__main__':

	'''
	参数设置
	'''
	mycash =10000*100 #初始100万
	brokerNumPerTrade =500 # 每次交易购买多少股
	brokerCommission =0.001 # 0.001 交易手续费 即是 0.1%
	cerebro = bt.Cerebro()

	# 自主修改部分
	#模拟时间区间
	fromdate=datetime.datetime(2014, 9, 1)
	todate=datetime.datetime(2016, 2, 1)
	#选定股票
	stock = 'JD' # JD MSFT AAPL BABA
	print(stock)
	# 选择交易模型
	cerebro.addstrategy(thoughts.demo.DemoStrategy,dailyprint=True)
	# 自主修改部分



	# 不修改
	data=loadCsvStock(startdate=fromdate,enddate=todate,stname=stock)
	cerebro.adddata(data)
	cerebro.broker.setcash(mycash)
	cerebro.broker.setcommission(commission=brokerCommission)
	cerebro.addsizer(bt.sizers.FixedSize, stake=brokerNumPerTrade)
	cerebro.run()

	print('\n')
	print('******************************************************')
	print('初始资金: %.2f' % mycash)
	print('末期资金: %.2f' % cerebro.broker.getvalue())
	print('盈利 : %.2f' % (cerebro.broker.getvalue()-mycash))
	print('******************************************************')

	try:
		pass
		cerebro.plot(style='candlestick')
	except Exception as e:
		# raise
		pass
