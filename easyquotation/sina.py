# coding:utf8
import re
from datetime import datetime

from .basequotation import BaseQuotation


class Sina(BaseQuotation):
    """新浪免费行情获取"""
    max_num = 800
    grep_detail = re.compile(r'(\d+)=([^\s][^,]+?)%s%s' % (
        r',([\.\d]+)' * 29, r',([-\.\d:]+)' * 2))
    grep_detail_with_prefix = re.compile(r'(\w{2}\d+)=([^\s][^,]+?)%s%s' % (
        r',([\.\d]+)' * 29, r',([-\.\d:]+)' * 2))
    stock_api = 'http://hq.sinajs.cn/?format=text&list='

    def format_response_data(self, rep_data, prefix=False):
        stocks_detail = ''.join(rep_data)
        grep_str = self.grep_detail_with_prefix if prefix else self.grep_detail
        result = grep_str.finditer(stocks_detail)
        stock_dict = dict()
        for stock_match_object in result:
            stock = stock_match_object.groups()
            stock_dict[stock[0]] = dict(
                name=stock[1],
                stock_code=stock[0],
                now_price=float(stock[4]),
                open_price=float(stock[2]),
                yesterday_closed_price=float(stock[3]),
                highest_price=float(stock[5]),
                lowest_price=float(stock[6]),
                volume=float(stock[10]),
                turnover=int(stock[9]),
                last_deal_time=datetime.strptime(
                    " ".join([stock[31], stock[32]]), '%Y-%m-%d %H:%M:%S')
            )
        return stock_dict
