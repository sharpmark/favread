# -*- coding: utf-8 -*-

from django.db import models
import json, time
from time import mktime
from datetime import datetime
from sinaweibo.tools import *

class Status(models.Model):
    id = models.BigIntegerField(primary_key=True)
    raw_content = models.CharField(max_length=5000)                 # 原始内容
    parse_version = models.IntegerField(default=0)                  # 按照那个parse版本更新的
    parsed_content = models.CharField(max_length=5000, null=True)   # 转化后的内容
    extra_info = models.TextField(null=True)                        # 扩展内容，json格式，例如文章内容

class User(models.Model):
    name = models.CharField(max_length=50)
    image_url = models.CharField(max_length=1000)
    statuses_count = models.BigIntegerField()
    friends_count = models.BigIntegerField()
    followers_count = models.BigIntegerField()
    verified = models.BooleanField()
    verified_type = models.IntegerField()
    auth_token = models.CharField(max_length=2000)
    expired_time = models.DecimalField(max_digits=20, decimal_places=2)
    #expired_time = models.DateTimeField()
    statuses = models.ManyToManyField(Status, through='Favorite')

    last_sync = models.DateTimeField(default=datetime(2000, 1, 1))          # 最后一次同步的时间
    create_time = models.DateTimeField(default=datetime.today())            # 第一次登录时间
    #last_login = models.DateTimeField()             # 最后一次登录时间
    user_level = models.IntegerField(default=0)      # 用户等级

    def get_statuses(self, page=1, count=50):

        favlist = {}
        status_list = []

        start = (page - 1) * count;

        statuses = Favorite.objects.filter(user=self, is_archived=False).order_by('-fav_time')[start:start+count+1]
        for item in statuses:
            status_list.append(json.loads(item.status.raw_content))

        favlist['favorites'] = status_list
        return favlist

    def get_statuses_count(self):
        return Favorite.objects.filter(user=self, is_archived=False).count()

    def save_status(self, status_dict):
        try:
            status = Status.objects.get(id=status_dict['status']['id'])
        except Status.DoesNotExist:
            status = Status(
                id=status_dict['status']['id'], 
                content=json.dumps(status_dict['status']))
            status.save()

        try:
            fav = Favorite.objects.get(user=self, status=status)
        except Favorite.DoesNotExist:
            fav = Favorite(
                user=self, status=status,
                fav_time=strtodatetime(status_dict['favorited_time']))
            fav.save()

    def archive_status(self, status_id):
        status = self.statuses.get(id=status_id)
        if status:
            fav = Favorite.objects.get(user=self, status=status)
            fav.is_archived = True
            fav.save()
            return True
        else:
            return False


class Favorite(models.Model):
    user = models.ForeignKey(User)
    status = models.ForeignKey(Status)
    tags = models.CharField(max_length=2000)
    fav_time = models.DateTimeField()
    is_archived = models.BooleanField(default=False)
    is_destroyed = models.BooleanField(default=False)

