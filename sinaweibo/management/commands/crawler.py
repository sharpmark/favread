from django.core.management.base import BaseCommand,CommandError
from sinaweibo.crawler import *

class Command(BaseCommand):
    def handle(self, *args, **options):
        print 'start crawler.'
        crawl_weibo_task()
        print 'crawler finish!'
