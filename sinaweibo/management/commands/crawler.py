from django.core.management.base import BaseCommand,CommandError
from sinaweibo.crawler import *

class Command(BaseCommand):
    def handle(self, *args, **options):
        print 'start crawler.'
        crawler_sinaweibo_task()
        print 'crawler finish!'