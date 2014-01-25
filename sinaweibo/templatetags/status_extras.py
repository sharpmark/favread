# -*- coding: utf-8 -*-

from django import template
from time import mktime
from datetime import datetime, date
import time
import re

register = template.Library()

@register.filter
def timefmt(value):
    status_time = datetime.fromtimestamp(mktime(time.strptime(value, '%a %b %d %H:%M:%S +0800 %Y')))
    #print status_time
    #print status_time.year, status_time.month, status_time.day

    if status_time.year == date.today().year:
        if status_time.month == date.today().month and status_time.day == date.today().day:
            return status_time.strftime('今天%H:%M')
        return status_time.strftime('%m月%d日')
    return status_time.strftime('%Y年%m月%d日')


def add_link(v):
    return '<a href="' + v.group() + '" target="_blank">' + v.group() + '</a>'

def add_at(v):
    return '<a href="http://weibo.com/n/' + v.group()[1:] + '" target="_blank">' + v.group() + '</a>'

def add_topic(v):
    return '<a href="http://huati.weibo.com/k/' + v.group()[1:-1] + '" target="_blank">' + v.group() + '</a>'

@register.filter
def statusfmt(value):
    #pattern_at = re.compile(r'\@[^\s\&\:\)\uff09\uff1a\@]+')
    pattern_at = re.compile(u'\@[^\s\&\:\)\@\uff1a\uff09]+')
    pattern_topic = re.compile(r'\#[^\#]+\#')
    pattern_link = re.compile(r'http\:\/\/[a-zA-Z0-9\_\/\.\-]+')

    value = value.replace('<', '&lt;').replace('>', '&gt;')

    value = pattern_link.sub(add_link, value)
    value = pattern_at.sub(add_at, value)
    value = pattern_topic.sub(add_topic, value)
    return value

@register.filter
def imagesquare(value):
    return value.replace('thumbnail', 'square')

@register.filter
def imagelarge(value):
    return value.replace('thumbnail', 'large')

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
 
def base62_encode(num, alphabet=ALPHABET):
    """Encode a number in Base X
 
    `num`: The number to encode
    `alphabet`: The alphabet to use for encoding
    """
    if (num == 0):
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
        rem = num % base
        num = num // base
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)
 
def base62_decode(string, alphabet=ALPHABET):
    """Decode a Base X encoded string into the number
 
    Arguments:
    - `string`: The encoded string
    - `alphabet`: The alphabet to use for encoding
    """
    base = len(alphabet)
    strlen = len(string)
    num = 0
 
    idx = 0
    for char in string:
        power = (strlen - (idx + 1))
        num += alphabet.index(char) * (base ** power)
        idx += 1
 
    return num

def url2mid(url):
    '''
    >>> url_to_mid('z0JH2lOMb')
    3501756485200075L
    >>> url_to_mid('z0Ijpwgk7')
    3501703397689247L
    '''
    url = str(url)[::-1]
    size = len(url) / 4 if len(url) % 4 == 0 else len(url) / 4 + 1
    result = []
    for i in range(size):
        s = url[i * 4: (i + 1) * 4][::-1]
        s = str(base62_decode(str(s)))
        s_len = len(s)
        if i < size - 1 and s_len < 7:
            s = (7 - s_len) * '0' + s
        result.append(s)
    result.reverse()
    return int(''.join(result))

@register.filter
def mid2url(value):
    '''
    >>> mid_to_url(3501756485200075)
    'z0JH2lOMb'
    >>> mid_to_url(3501703397689247)
    'z0Ijpwgk7'
    '''
    value = str(value)[::-1]
    size = len(value) / 7 if len(value) % 7 == 0 else len(value) / 7 + 1
    result = []
    for i in range(size):
        s = value[i * 7: (i + 1) * 7][::-1]
        s = base62_encode(int(s))
        s_len = len(s)
        if i < size - 1 and len(s) < 4:
            s = '0' * (4 - s_len) + s
        result.append(s)
    result.reverse()
    return ''.join(result)
