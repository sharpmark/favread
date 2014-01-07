from django.conf.urls import patterns, include, url
from django.contrib import admin
from sinaweibo import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^callback/$', views.callback, name='callback'),
    url(r'^page/(?P<page_id>\d+)/$', views.list, name='list'),
)
