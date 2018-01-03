# coding:utf8
import json
import yarl
import aiohttp
import asyncio

from .basequotation import BaseQuotation

"""
url = "http://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get?_var=kline_dayqfq&param=hk00001,day,,,660,qfq&r=0.7773272375526847"

url 参数改动
股票代码 :hk00001
日k线天数：660

更改为需要获取的股票代码和天数例如：

url = "http://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get?_var=kline_dayqfq&param=hk00700,day,,,350,qfq&r=0.7773272375526847"

"""


class DayKline(BaseQuotation):
    """腾讯免费行情获取"""
    max_num = 1

    def format_response_data(self, rep_data, prefix=False):
        stocks_detail = ''.join(rep_data)
        stock_detail_split = stocks_detail.split('kline_dayqfq=')
        stock_dict = dict()
        for daykline in stock_detail_split:
            try:
                daykline = json.loads(daykline)
            except Exception as e:
                continue

            status_code = daykline.get("code")
            if status_code not in ("0", 0):
                # 当返回错误状态码时候，不做处理
                continue
            daykline = daykline.get("data")
            if not isinstance(daykline, dict):
                continue

            for key, value in daykline.items():
                stock_code = key
                
                _stmt = value.get('qfqday')
                if _stmt is None:
                    _stmt = value.get('day')
            if _stmt is None:
                continue
            
            stock_dict[stock_code] = _stmt
            stock_dict = {
                "stock_code": stock_code,
                "kline": _stmt
            }

        return stock_dict

    async def get_stocks_by_range(self, *params):
        if self._session is None:
            self._session = aiohttp.ClientSession()
        headers = {
            'Accept-Encoding': 'gzip, deflate, sdch',
            'User-Agent': ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
                           ' (KHTML, like Gecko) Chrome/54.0.2840.100'
                           ' Safari/537.36')
        }
        if len(params) > 1:
            stock_code = params[0].lower()
            days = params[1]
        else:
            stock_code = params.lower()
            days = 60
        api_url = get_api_url(stock_code[:2])
        url = yarl.URL(api_url % (stock_code, days), encoded=True)
        print(url)
        try:
            async with self._session.get(url, timeout=10, headers=headers) as r:
                asyncio.sleep(0.1)
                response_text = await r.text()
                return response_text.replace('kline_dayqfq=', '')
        except asyncio.TimeoutError:
            return ''
    
    def get_stock_data(self, stock_list, days=60, **kwargs):
        coroutines = []

        for params in [x for x in stock_list if x]:
            coroutine = self.get_stocks_by_range(params, days)
            coroutines.append(coroutine)
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        res = loop.run_until_complete(asyncio.gather(*coroutines))
        return self.format_response_data(
            [x for x in res if x is not None], **kwargs)


def get_api_url(code):
    url = "http://web.ifzq.gtimg.cn/appstock/app/{}?_var=kline_dayqfq&param=%s,day,,,%s,{}&r=0.7773272375526847"
    if code == "sz":
        api_url = url.format("fqkline/get", "qfq")
    elif code == "hk":
        api_url = url.format("hkfqkline/get", "qfq")
    elif code == "sh":
        api_url = url.format("kline/kline", "")
    else:
        # TODO support US
        api_url = url.format("", "")

    return api_url


if __name__ == "__main__":
    pass
