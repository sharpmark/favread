# -*- coding: utf-8 -*-

from datetime import datetime
from weibo import APIClient
from sinaweibo.tools import *
from sinaweibo.models import User
from sinaweibo.config import *

def crawler_sinaweibo_task():
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    users = User.objects.all()
    for user in users:
        print u'crawler: [%d] last sync: %s' % (
            user.id, str(user.last_sync)[5:19]),
        client.set_access_token(user.auth_token, user.expired_time)
        print 'update statuses: %d.' % crawler_user(client, user, 20)

def crawler_user(client, user, count=50):
    try:
        cawler_count = crawler_favorites(client, user, count)
        user.last_sync = datetime.today()
        user.save()
        return cawler_count
    except Exception, e:
        print e
        return -1

def crawler_favorites(client, user, count=50):

    compare_date = user.last_sync

    favlist = client.favorites.ids.get(uid=user.id)
    total_number = favlist['total_number']
    cawler_count = 0

    if total_number == 0: return cawler_count

    if favlist['total_number'] / count == 0:
        total_page = favlist['total_number'] / count + 1
    else:
        total_page = favlist['total_number'] / count + 2

    for i in range(1, total_page):
        statuses = client.favorites.get(uid=user.id, page=i, count=count)
        page_first_time = strtodatetime(statuses['favorites'][0]['favorited_time'])

        if page_first_time < compare_date:
            return cawler_count

        for status in statuses['favorites']:
            if compare_date > strtodatetime(status['favorited_time']):
                return cawler_count

            #print 'saving status: %d' % status['status']['id']
            cawler_count = cawler_count + 1
            user.save_status(status)

    return cawler_count