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
            return status_time.strftime('今天 %H:%M')
        return status_time.strftime('%m 月 %d 日')
    return status_time.strftime('%Y 年 %m 月 %d 日')


def add_link(v):
    return '<a href="' + v.group() + '" target="_blank">' + v.group() + '</a>'

def add_at(v):
    return '<a href="http://weibo.com/n/' + v.group()[1:] + '" target="_blank">' + v.group() + '</a>'

def add_topic(v):
    return '<a href="http://huati.weibo.com/k/' + v.group() + '" target="_blank">' + v.group() + '</a>'

@register.filter
def statusfmt(value):
    #pattern_at = re.compile(r'\@[^\s\&\:\)\uff09\uff1a\@]+')
    pattern_at = re.compile(r'\@[^\s\&\:\)\@]+')
    pattern_topic = re.compile(r'\#[^\#]+\#')
    pattern_link = re.compile(r'http\:\/\/[a-zA-Z0-9\_\/\.\-]+')

    value = value.replace('<', '&lt;').replace('>', '&gt;')

    value = pattern_link.sub(add_link, value)
    value = pattern_at.sub(add_at, value)
    value = pattern_topic.sub(add_topic, value)
    return value
