from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import backtrader as bt
from .basemodel import BaseStrategy

# 以上保持不变


class DemoStrategy(BaseStrategy):
    '''
    自定义参数
    '''
    params = (
        ('p_stoploss', 0.05),# 止损比例
        ('p_takeprofit', 0.10),# 止盈比例
        ('limit', 0.01),
        ('limdays', 15),
        ('limdays2', 15),
    )
    #
    def __init__(self):
        super(DemoStrategy,self).__init__()
        self.closeMap={}
        for i, d in enumerate(self.datas):
            self.closeMap[d._name] = self.datas[i].close
    def next(self):
        # 实盘设置，必须固定保留
        if self.liveskip():return
        # 打印当日持仓信息
        self.myholdings()

        #买入多个股票的方式
        for i, d in enumerate(self.datas):
            pos = self.getposition(d).size

            # 连跌5天 就买
            buy_sig=self.closeMap.get(d._name)[0]<self.closeMap.get(d._name)[-1] and self.closeMap.get(d._name)[-1]<self.closeMap.get(d._name)[-2] and self.closeMap.get(d._name)[-2]<self.closeMap.get(d._name)[-3] and self.closeMap.get(d._name)[-3]<self.closeMap.get(d._name)[-4]

            # 还没有仓位，才可以买
            if not pos:
                if buy_sig:  # 连跌3天
                    # 止损止盈单
                    # # 计算买入报价p1，止损价p2，止盈价p3
                    close = self.closeMap.get(d._name)[0]
                    p1 = close * (1.0 + self.p.limit)
                    p2 = p1 - self.p.p_stoploss * close
                    p3 = p1 + self.p.p_takeprofit * close
                    self.log('决定买入 {} , 当前价:{},挂单价:{},止损价:{}止盈价:{}'.format(d._name,round(d.close[0],2),p1,p2,p3))

                    os = self.buy_bracket(data=d,price=p1,exectype=bt.Order.Limit,
                            limitprice=p3,
                            stopprice=p2)
                    self.orefs = [o.ref for o in os]
