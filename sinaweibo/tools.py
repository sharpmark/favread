# -*- coding: utf-8 -*-

from datetime import datetime
from time import mktime
import time

def str2datetime(strvalue):
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

def get_page_count(total, pre=50):
    if total % pre == 0:
        return total / pre
    else:
        return total / pre + 1

def get_page_list(total, pre=50, current=1):

    pages = get_page_count(total, pre)

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

#import urllib2
#def decode_url(shorturl):
    #TODO: 还需要考虑服务器503的情况
    #http://adchoices.sinaapp.com/topic/47/python-%E6%A8%A1%E5%9D%97-httplib-urllib%E5%92%8Curllib2%E7%9A%84%E7%AE%80%E5%8D%95%E7%94%A8%E6%B3%95
    #return urllib2.urlopen(shorturl).geturl()
