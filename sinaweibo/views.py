# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
#from django.core.paginator import Paginator
import hashlib, base64, time
from datetime import datetime
import json
from weibo import APIClient

from sinaweibo.config import *
from sinaweibo.models import User, Status, Favorite
from sinaweibo.crawler import *
from sinaweibo.tools import *

def test(request):
    return HttpResponseRedirect('/')

def index(request):
    if _check_cookie(request) is None:
        return HttpResponseRedirect('/welcome/')
    else:
        return HttpResponseRedirect('/page/1/')

def welcome(request):
    return render(request, 'welcome.html')

def login(request):
    return HttpResponseRedirect(_create_client().get_authorize_url())

def logout(request):
    response = HttpResponseRedirect('/welcome/')
    response.delete_cookie(COOKIE_USER)
    return response

def list(request, page_id):
    u = _check_cookie(request)
    client = _create_client()
    if u is None:
        return HttpResponseRedirect(client.get_authorize_url())
    client.set_access_token(u.auth_token, u.expired_time)

    favlist = u.get_statuses(page=int(page_id), count=10)

    return render(request, 'list.html', {
        'favlist': favlist, \
        'pages': get_page_list(u.statuses.count(), 10, int(page_id)), \
        'current_page': int(page_id), \
        'my': u, },)

def status(request, status_id):
    status = Status.objects.get(id=status_id)
    return render(request, 'status.html', {
        'status': json.loads(status.content),
        }, )

def callback(request):

    client = _create_client()
    r = client.request_access_token(request.GET['code'])
    access_token, expires_in, uid = r.access_token, r.expires_in, r.uid

    client.set_access_token(access_token, expires_in)

    u = client.users.show.get(uid=uid)

    try:
        user = User.objects.get(id=uid)
        user.auth_token = access.token
        user.expired_time = expires_in
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

    user.save()

    #crawler_user(client, user)

    response = HttpResponseRedirect('/')

    _make_cookie(uid, access_token, expires_in, response)
    return response


def _create_client():
    return APIClient(app_key=APP_KEY, \
        app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)

def _make_cookie(uid, token, expires_in, response):

    expires = str(int(expires_in))
    s = '%s:%s:%s:%s' % (str(uid), str(token), expires, SALT)
    md5 = hashlib.md5(s).hexdigest()
    cookie = '%s:%s:%s' % (str(uid), expires, md5)
    response.set_cookie(COOKIE_USER, \
        base64.b64encode(cookie).replace('=', '_'), expires=expires_in)

def _check_cookie(request):

    try:
        b64cookie = request.COOKIES[COOKIE_USER]
        cookie = base64.b64decode(b64cookie.replace('_', '='))
        uid, expires, md5 = cookie.split(':', 2)

        if int(expires) < time.time():
            return

        user = User.objects.get(id=uid)
        s = '%s:%s:%s:%s' % (uid, str(user.auth_token), expires, SALT)
        if md5 != hashlib.md5(s).hexdigest():
            return

        return user

    except BaseException:
        pass
