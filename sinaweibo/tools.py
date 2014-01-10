# -*- coding: utf-8 -*-

from datetime import datetime
from time import mktime
import time

def strtodatetime(strvalue):
    return datetime.fromtimestamp(
        mktime(time.strptime(strvalue, '%a %b %d %H:%M:%S +0800 %Y')))

# 将 dict 对象转化为 object
# 目前暂未使用
def dict2obj(d):
    if isinstance(d, list):
        d = [dict2obj(x) for x in d]
    if not isinstance(d, dict):
        return d
    class C(object):
        pass
    o = C()
    for k in d:
        o.__dict__[k] = dict2obj(d[k])
    return o

def get_page_list(total, pre = 50, current = 1):
    if total % pre == 0:
        pages = total / pre
    else:
        pages = total / pre + 1

    if current < 6:
        start = 1
        end = min(pages, 9)
    elif current + 4 > pages:
        end = pages
        start = max(pages - 9, 1)
    else:
        start = current - 4
        end = current + 4

    return range(start, end + 1)
