# coding:utf8
import sys

from .boc import Boc
from .jsl import Jsl
from .leverfun import Leverfun
from .sina import Sina
from .tencent import Tencent
from .timekline import TimeKline
from .daykline import DayKline
from .hkqoute import HKQuote

PY_VERSION = sys.version_info[:2]
if PY_VERSION < (3, 5):
    raise Exception('Python 版本需要 3.5 或以上, 当前版本为 %s.%s 请升级 Python' % PY_VERSION)


def use(source):
    if source in ['sina']:
        return Sina()
    elif source in ['leverfun', 'lf']:
        return Leverfun()
    elif source in ['jsl']:
        return Jsl()
    elif source in ['qq', 'tencent']:
        return Tencent()
    elif source in ['boc']:
        return Boc()
    elif source in ["timekline"]:
        return TimeKline()
    elif source in ['daykline']:
        return DayKline()
    elif source in ['hkquote']:
        return HKQuote()
    else:
        print('this source not exist')


if __name__ == '__main__':
    pass
