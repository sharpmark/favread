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
	if user.id == 1642723410 and user.last_sync < datetime(2013,10,21,1,1,1):
            user.last_sync = datetime(2013,12,25,1,1,1)
            user.save()
        try:
            print '============='
            print u'crawler user: %d with last sync data: %s' % (user.id, str(user.last_sync))
            client.set_access_token(user.auth_token, user.expired_time)
            crawler_user(client, user, 20)
            print 'crawler done. update user\'s last sync'
        except Exception, e:
            print e

def crawler_user(client, user, count=50):
    crawler_favorites(client, user, count)
    user.last_sync = datetime.today()
    user.save()

def crawler_favorites(client, user, count=50):

    print 'start crawler statuses ...'

    compare_date = user.last_sync

    favlist = client.favorites.ids.get(uid=user.id)
    total_number = favlist['total_number']

    if total_number == 0: return

    total_page = favlist['total_number'] / count + 2

    for i in range(1, total_page):
        statuses = client.favorites.get(uid=user.id, page=i, count=count)
        page_first_time = strtodatetime(statuses['favorites'][0]['favorited_time'])

        if page_first_time < compare_date:
            return

        for status in statuses['favorites']:
            if compare_date > strtodatetime(status['favorited_time']):
                return

            #print 'saving status: %d' % status['status']['id']
            user.save_status(status)

