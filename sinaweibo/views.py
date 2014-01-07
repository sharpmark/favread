# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import hashlib, base64, time
from datetime import datetime
import json
from weibo import APIClient

from sinaweibo.config import *
from sinaweibo.models import User, Status, Favorite
from sinaweibo.crawler import *

def test_get(request):
    u = _check_cookie(request)
    client = _create_client()
    if u is None:
        return HttpResponseRedirect(client.get_authorize_url())
    client.set_access_token(u.auth_token, u.expired_time)

    crawler(client, u)

    return HttpResponseRedirect('/')

def index(request):

    u = _check_cookie(request)
    client = _create_client()
    if u is None:
        return HttpResponseRedirect(client.get_authorize_url())
    client.set_access_token(u.auth_token, u.expired_time)

    favlist = u.get_statuses(page=1, count=50)

    return render(request, '/home/jiong/favread/sinaweibo/templates/index.html', { 'favlist': favlist, 'page_count': range(1, u.statuses.count() / 50 + 2) })

def list(request, page_id):
    u = _check_cookie(request)
    client = _create_client()
    if u is None:
        return HttpResponseRedirect(client.get_authorize_url())
    client.set_access_token(u.auth_token, u.expired_time)

    favlist = u.get_statuses(page=int(page_id), count=50)

    return render(request, '/home/jiong/favread/sinaweibo/templates/list.html', { 'favlist': favlist, 'page_count': range(1, u.statuses.count() / 50 + 2 ) })

def callback(request):

    print 'request callback'

    code = request.GET['code']
    client = _create_client()
    r = client.request_access_token(code)
    access_token, expires_in, uid = r.access_token, r.expires_in, r.uid

    client.set_access_token(access_token, expires_in)

    u = client.users.show.get(uid=uid)

    try:
        user = User.objects.get(id=uid)
        user.auth_token=access.token
        user.expired_time=expires_in
    except BaseException:
        user = User(id=uid, name=u.screen_name, \
            image_url=u.avatar_large or u.profile_image_url, \
            statuses_count=u.statuses_count, \
            friends_count=u.friends_count, \
            followers_count=u.followers_count, \
            verified=u.verified, \
            verified_type=u.verified_type, \
            auth_token=access_token, \
            expired_time=expires_in,
            #last_sync=datetime.today(),
            #create_time=datetime.today(),
            )

    # hard code
    if user.id == 1642723410:
        if user.last_sync is None or user.last_sync < datetime(2013, 12, 30, 0, 0, 0):
            user.last_sync = datetime.datetime(2013, 12,30,1,1,1)
    user.save()

    crawler_user(client, user)

    response = HttpResponseRedirect('/')

    _make_cookie(uid, access_token, expires_in, response)
    return response

_COOKIE = 'authuser'
_SALT = 'A rAnDoM sTrInG'

def _create_client():
    return APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)

def _make_cookie(uid, token, expires_in, response):

    expires = str(int(expires_in))
    s = '%s:%s:%s:%s' % (str(uid), str(token), expires, _SALT)
    md5 = hashlib.md5(s).hexdigest()
    cookie = '%s:%s:%s' % (str(uid), expires, md5)
    response.set_cookie(_COOKIE, base64.b64encode(cookie).replace('=', '_'), expires=expires_in)

def _check_cookie(request):

    try:
        b64cookie = request.COOKIES[_COOKIE]
        cookie = base64.b64decode(b64cookie.replace('_', '='))
        uid, expires, md5 = cookie.split(':', 2)

        if int(expires) < time.time():
            return

        user = User.objects.get(id=uid)

        s = '%s:%s:%s:%s' % (uid, str(user.auth_token), expires, _SALT)
        if md5 != hashlib.md5(s).hexdigest():
            return

        return user

    except BaseException:
        pass
