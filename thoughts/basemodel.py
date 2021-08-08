from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects

# Import the backtrader platform
import backtrader as bt


orderstatustext ={
0:'Created',
1:'Submitted',
2:'Accepted',
3:'Partial',
4:'Complete',
5:'Rejected',
6:'Margin',
7:'Cancelled',
8:'Expired'
}


class BaseStrategy(bt.Strategy):
    '''

    '''
    params = (
        ('sizer', None),
        ('live', None),
        ('dailyprint', True),
        ('optmode', None),


    )
    #
    def live(self):
        pass

    def liveskip(self):
        pass

    def myholdings(self):
        self.bar_executed = len(self)
        if not self.params.dailyprint:
            return
        # self.log('acc cash :{}'.format(round(self.broker.get_value(),2)))
        print(self.data.datetime.date())
        for i, d in enumerate(self.datas):
            pos = self.getposition(d)
            if len(pos):
                # print('{}, 持仓:{:.2f}, 成本价:{:.2f}, 当前价:{:.2f}, 浮动盈亏:{:.2f}'.format(d._name, pos.size, pos.price, pos.adjbase, pos.size * (pos.adjbase - pos.price)))
                print('{}, 持仓:{:.2f}, 成本价:{:.2f}, 当前价:{:.2f}, 浮动盈亏:{:.2f}'.format(d._name, pos.size, pos.price, round(d.close[0],2), pos.size * (round(d.close[0],2) - pos.price)))

    def show_yourself(self):
        # print("当前是第{}个bar，所处阶段 {}".format(len(self), inspect.stack()[1][3]))
        pass
    def log(self, txt, dt=None, doprint=False):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
    def __init__(self):
        # self.dataclose = self.datas[0].close

        self.order = None    # 设置订单引用，用于取消以往发出的尚未执行的订单
        self.orefs = list() #一篮子 交易订单 使用

        #sizer
        if self.p.sizer is not None:
            self.sizer = self.p.sizer

        for i, d in enumerate(self.datas):
            if d._name == 'google':
                self.google_sentiment = d.close

    def notify_order(self, order):
        if not self.params.dailyprint:
            return
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        # print(dir(order))
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    '买入%s成功,%s, 价格: %.2f, 成本: %.2f, 手续费 %.2f' %
                    (order.data._name,
                    orderstatustext[order.status],
                     order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('卖出%s成功,%s, 价格: %.2f, 成本: %.2f, 手续费 %.2f' %
                         (order.data._name,
                         orderstatustext[order.status],
                          order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            # self.bar_executed = len(self)

        elif order.status ==order.Canceled:
            # print(order)
            # self.log('Order Canceled/Margin/Rejected : {}'.format(order.status))
            self.log('对不起,{}订单{}已被取消 : {}'.format(order.data._name,order.data[0],orderstatustext[order.status]))
        elif order.status ==order.Margin:
            # print(order)
            # self.log('Order Canceled/Margin/Rejected : {}'.format(order.status))
            self.log('对不起,{}订单{}余额不足已被拒绝 : {}'.format(order.data._name,order.data[0],orderstatustext[order.status]))
        elif order.status ==order.Rejected:
            # print(order)
            # self.log('Order Canceled/Margin/Rejected : {}'.format(order.status))
            self.log('对不起,{}订单{}已被拒绝 : {}'.format(order.data._name,order.data[0],orderstatustext[order.status]))

        # Write down: no pending order
        self.order = None

        if not order.alive() and order.ref in self.orefs:
            self.orefs.remove(order.ref)



    def notify_trade(self, trade):
        if not self.params.dailyprint:
            return
        if not trade.isclosed:
            return
        # print(dir(trade))
        # self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
        #          (trade.pnl, trade.pnlcomm))
        self.log('本次交易 %s 利润: 毛利 %.2f, 净利 %.2f' %
                 (trade.getdataname(),trade.pnl, trade.pnlcomm))

    # 每个新bar结束时触发调用一次，相当于其他框架的 on_bar()方法
    def next(self):
        # self.cancel(self.order) # 取消以往未执行订单
        # print(self.cal_next_bar_is_last_trading_day(self.data))

        pass
    # def nextstart(self):
    #     self.show_yourself(self)
    #     pass
    #
    # def prenext(self):
    #     self.show_yourself(self)
    #     pass
    #
    # def start(self):
    #     self.show_yourself(self)
    #     pass
    #
    # def stop(self):
    #     self.show_yourself(self)
    #     pass

        # self.log('account:, %.2f' % self.dataclose[0])

    # 如何定义需要优化的参数??
    def stop(self):
        if self.params.optmode:
            self.log('(params %s) Ending Value %.2f' %
                     (self.params.slower, self.broker.getvalue()), doprint=True)
