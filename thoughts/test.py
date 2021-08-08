from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import datetime  # For datetime objects
# Import the backtrader platform
import backtrader as bt
import pandas as pd
import inspect
from .basemodel import BaseStrategy

# 以上保持不变


class TestStrategy(BaseStrategy):
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
        super(TestStrategy,self).__init__()

    def next(self):
        # 实盘设置，必须固定保留
        if self.liveskip():return
        # 打印当日持仓信息
        self.myholdings()

        # 这里写策略
