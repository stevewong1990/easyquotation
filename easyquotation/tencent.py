# coding:utf8
import re
from datetime import datetime

from .basequotation import BaseQuotation


class Tencent(BaseQuotation):
    """腾讯免费行情获取"""
    stock_api = 'http://qt.gtimg.cn/q='
    grep_stock_code = re.compile(r'(?<=_)\w+')
    max_num = 60

    def format_response_data(self, rep_data, prefix=False):
        stocks_detail = ''.join(rep_data)
        stock_details = stocks_detail.split(';')
        stock_dict = dict()
        for stock_detail in stock_details:
            stock = stock_detail.split('~')
            if len(stock) <= 49:
                continue
            stock_code = self.grep_stock_code.search(
                stock[0]).group() if prefix else stock[2]
            stock_dict[stock_code] = {
                'name': stock[1],
                'stock_code': stock_code,
                'now_price': float(stock[3]),
                'opened_price': float(stock[5]),
                'yesterday_closed_price': float(stock[4]),
                'highest_price': float(stock[33]),
                'lowest_price': float(stock[34]),
                'volume': float(stock[6]) * 100,
                'turnover': float(stock[38]) if stock[38] != '' else None,
                'last_deal_time': datetime.strptime(stock[30], '%Y%m%d%H%M%S'),
            }
        return stock_dict
